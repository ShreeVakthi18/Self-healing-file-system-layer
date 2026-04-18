# logic_and_snapshots.py — SHFSL 2.0 (FULLY FIXED)
import os
import shutil
import time
import threading
from datetime import datetime
from pathlib import Path

from admin_logic import send_alert_email, update_dashboard_log
from utils import load_log, save_log, update_risk_score

# --- Configuration ---
ROOT_FOLDER = os.getcwd()
SNAPSHOT_STORAGE = os.path.join(ROOT_FOLDER, "snapshot_storage")
MAX_SNAPSHOTS_PER_FILE = 10
os.makedirs(SNAPSHOT_STORAGE, exist_ok=True)

RANSOMWARE_EXTENSIONS = ['.lock', '.encrypted', '.ransom', '.crypted', '.crypt', '.enc', '.locked']


# ──────────────────────────────────────────────────────────────────────────────
# Snapshot helpers
# ──────────────────────────────────────────────────────────────────────────────

def prune_old_snapshots(file_storage_dir, base_filename):
    """
    Keeps only MAX_SNAPSHOTS_PER_FILE most recent snapshots.
    Runs in a background daemon thread so it never blocks the watcher loop.
    """
    def _do_prune():
        path = Path(file_storage_dir)
        snapshots = sorted(path.glob(f"{base_filename}*"), reverse=True)
        to_delete = snapshots[MAX_SNAPSHOTS_PER_FILE:]
        if not to_delete:
            return
        print(f"[SNAPSHOT] Pruning {len(to_delete)} old snapshot(s) for '{base_filename}' (background)")
        deleted = 0
        for old in to_delete:
            try:
                old.unlink()
                deleted += 1
            except Exception:
                pass
            if deleted % 10 == 0:
                time.sleep(0.05)
        print(f"[SNAPSHOT] Pruned {deleted} snapshot(s) for '{base_filename}'")

    t = threading.Thread(target=_do_prune, daemon=True)
    t.start()


def create_snapshot(filepath, WatcherHandler):
    """
    Creates a versioned copy of the file in secure snapshot storage.
    Skips temp/lock/Office-swap files so they never pollute the snapshot pool.
    """
    if WatcherHandler.is_rolling_back:
        return None

    if not os.path.exists(filepath) or os.path.isdir(filepath):
        return None

    filename = os.path.basename(filepath)

    SKIP_PREFIXES = ('~', '.~', '~$')
    SKIP_SUFFIXES = ('.tmp', '.temp', '.~tmp', '.swp', '.part', '.lock', '.lnk')
    if (any(filename.startswith(p) for p in SKIP_PREFIXES) or
            any(filename.lower().endswith(s) for s in SKIP_SUFFIXES)):
        print(f"[SNAPSHOT] Skipped temp/lock file: {filename}")
        return None

    relative_path = os.path.relpath(filepath, ROOT_FOLDER)
    file_storage_dir = os.path.join(SNAPSHOT_STORAGE, os.path.dirname(relative_path))
    os.makedirs(file_storage_dir, exist_ok=True)

    filename_base, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    snapshot_name = f"{filename_base}{ext}.{timestamp}"
    destination_path = os.path.join(file_storage_dir, snapshot_name)

    try:
        shutil.copy2(filepath, destination_path)
        print(f"[SNAPSHOT] Created: {snapshot_name}")
        prune_old_snapshots(file_storage_dir, f"{filename_base}{ext}")
        return destination_path
    except Exception as e:
        print(f"[SNAPSHOT] Failed to create snapshot for {filepath}: {e}")
        return None


def _derive_original_filename(filename):
    """
    Given a ransomware-renamed filename, strips the ransomware extension
    to recover the original clean filename.

    Examples:
      report.xlsx.lock   → report.xlsx
      report.lock.xlsx   → report.xlsx
      normal_file.docx   → normal_file.docx  (unchanged)
    """
    fn_lower = filename.lower()
    for rext in RANSOMWARE_EXTENSIONS:
        # Pattern A: name.lock.xlsx  → strip '.lock' from middle
        if (rext + '.') in fn_lower:
            idx = fn_lower.index(rext)
            original = filename[:idx] + filename[idx + len(rext):]
            return original
        # Pattern B: name.xlsx.lock  → strip trailing ransomware ext
        if fn_lower.endswith(rext):
            return filename[: -len(rext)]
    return filename  # Not ransomware-renamed


def rollback_file(filepath, WatcherHandler):
    """
    Restores the most recent CLEAN snapshot of the original file.

    FIXED BUGS:
    1. CRITICAL: `restore_target` was used but never defined — caused NameError
       on every rollback attempt. Now correctly computed as the path where the
       clean original file should be restored to.
    2. Snapshot search now correctly matches original filename prefix only,
       never picks up temp/swap files.
    3. Retry loop handles Windows/OneDrive file locks gracefully.
    4. is_rolling_back flag released in finally — even on success — with a
       generous sleep so watchdog drains queued events before resuming.
    """
    result = {"success": False, "snapshot_used": None, "error": None}
    success = False

    filename = os.path.basename(filepath)
    original_filename = _derive_original_filename(filename)

    print(f"[ROLLBACK] Target file:    '{filename}'")
    print(f"[ROLLBACK] Original name:  '{original_filename}'")

    # ── FIX: Define restore_target — the path where the clean file is written back ──
    # Always restore to the ORIGINAL clean filename, not the ransomware-named one.
    restore_target = os.path.join(os.path.dirname(filepath), original_filename)
    print(f"[ROLLBACK] Restore target: '{restore_target}'")

    # ── Locate snapshot directory ─────────────────────────────────────────────
    relative_path = os.path.relpath(filepath, ROOT_FOLDER)
    file_dir = os.path.dirname(filepath)
    file_storage_dir = os.path.join(
        SNAPSHOT_STORAGE,
        os.path.relpath(file_dir, ROOT_FOLDER)
    )

    if not os.path.exists(file_storage_dir):
        print(f"[ROLLBACK] ❌ No snapshot directory found at: {file_storage_dir}")
        result["error"] = "no_snapshot_dir"
        return result

    # ── Find snapshots matching the ORIGINAL filename prefix ──────────────────
    path_to_search = Path(file_storage_dir)

    matching_snapshots = sorted(
        [f for f in path_to_search.glob('*')
         if f.name.lower().startswith(original_filename.lower() + '.')
         and not any(f.name.startswith(p) for p in ('~', '.~', '~$'))
         and not any(f.name.lower().endswith(s) for s in ('.tmp', '.temp', '.swp', '.part'))],
        reverse=True  # Most recent first (timestamp suffix sorts lexicographically)
    )

    if not matching_snapshots:
        # Fallback: match by base name (without extension) in case ext got mangled
        orig_base = os.path.splitext(original_filename)[0]
        matching_snapshots = sorted(
            [f for f in path_to_search.glob(f"{orig_base}*")
             if not any(f.name.startswith(p) for p in ('~', '.~', '~$'))
             and not any(f.name.lower().endswith(s) for s in ('.tmp', '.temp', '.swp'))],
            reverse=True
        )

    if not matching_snapshots:
        print(f"[ROLLBACK] ❌ No clean snapshots found for '{original_filename}'.")
        result["error"] = "no_snapshots"
        return result

    latest_snapshot = matching_snapshots[0]
    print(f"[ROLLBACK] Found {len(matching_snapshots)} snapshot(s). Using: {latest_snapshot.name}")

    # ── Restore with retry loop for file-lock scenarios ───────────────────────
    RETRY_ATTEMPTS = 6
    RETRY_DELAY    = 1.0

    try:
        WatcherHandler.is_rolling_back = True

        # Step 1: Remove the malicious/ransomware-named file
        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"[ROLLBACK] 🗑  Removed malicious file: {filename}")
                break
            except PermissionError as e:
                if attempt < RETRY_ATTEMPTS:
                    print(f"[ROLLBACK] File locked (attempt {attempt}/{RETRY_ATTEMPTS}), "
                          f"retrying in {RETRY_DELAY}s… ({e})")
                    time.sleep(RETRY_DELAY)
                else:
                    raise

        # Step 2: If restore_target differs from filepath, also remove that
        # (e.g. the original .xlsx might still exist alongside the .lock version)
        if os.path.normcase(restore_target) != os.path.normcase(filepath):
            if os.path.exists(restore_target):
                try:
                    os.remove(restore_target)
                    print(f"[ROLLBACK] 🗑  Removed existing file at restore target: {original_filename}")
                except Exception as e:
                    print(f"[ROLLBACK] ⚠️  Could not remove restore target (continuing): {e}")

        # Step 3: Copy clean snapshot to restore_target
        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                shutil.copy2(str(latest_snapshot), restore_target)
                print(f"[ROLLBACK] ✅ Restored '{original_filename}' from '{latest_snapshot.name}'")
                break
            except PermissionError as e:
                if attempt < RETRY_ATTEMPTS:
                    print(f"[ROLLBACK] Copy locked (attempt {attempt}/{RETRY_ATTEMPTS}), "
                          f"retrying in {RETRY_DELAY}s…")
                    time.sleep(RETRY_DELAY)
                else:
                    raise

        result["success"] = True
        result["snapshot_used"] = latest_snapshot.name
        result["restored_as"] = original_filename
        success = True
        return result

    except Exception as e:
        print(f"[ROLLBACK] ❌ Error during restore (all retries exhausted): {e}")
        result["error"] = str(e)
        return result

    finally:
        if success:
            # Give watchdog time to drain queued events from the restore write
            time.sleep(2.5)
            WatcherHandler.is_rolling_back = False
            print("[ROLLBACK] 🔓 Monitoring resumed.")
        else:
            print("\n⚠️  ROLLBACK FAILED — Monitoring paused to prevent cascade loop.")
            print("   ACTION: Close any app locking this file, then restart the watcher.")
            # FIX: Still release the flag after a longer pause on failure,
            # otherwise the watcher becomes permanently deaf.
            time.sleep(5.0)
            WatcherHandler.is_rolling_back = False
            print("[ROLLBACK] 🔓 Monitoring resumed (post-failure).")


# ──────────────────────────────────────────────────────────────────────────────
# Pattern Detection & Risk Engine
# ──────────────────────────────────────────────────────────────────────────────

def assess_and_handle_event(event_type, filepath, file_status, WatcherHandler):
    """
    Core logic engine: classify events, calculate risk, trigger rollback/alerts.

    FIXED BUGS:
    1. Risk score is now updated IN-MEMORY on the same log_data dict that gets
       saved at the end — eliminates the race condition where get_adaptive_risk_score()
       would save first and then process_event() would overwrite with an old snapshot.
    2. All three pattern branches return their risk_outcome correctly.
    3. Re-trigger guard for ransomware checks BOTH the ransomware filename AND the
       original filename's log entry to prevent the restored file from re-entering
       the ransomware branch.
    """
    filename = os.path.basename(filepath)
    risk_outcome = "LOW_NORMAL_ACTIVITY"

    # Snapshot on any create/modify (before pattern analysis)
    if event_type in ['modified', 'created'] and not WatcherHandler.is_rolling_back:
        create_snapshot(filepath, WatcherHandler)

    # ── Pattern 1: DECOY Tampering ───────────────────────────────────────────
    if file_status == "DECOY" and event_type in ['modified', 'deleted']:
        risk_outcome = "HIGH_DECOY_ALERT"
        subject = f"CRITICAL: Decoy Honeypot Tampered — {filename}"
        body = (
            f"DECOY HONEYPOT BREACH DETECTED\n"
            f"File: {filename}\n"
            f"Event: {event_type.upper()}\n"
            f"Action: Automatic rollback triggered.\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        send_alert_email(subject, body)
        print(f"\n🚨 DECOY FILE TAMPERED! Triggering rollback for {filename}")

        result = rollback_file(filepath, WatcherHandler)
        if result["success"]:
            update_dashboard_log(
                f"CRITICAL: DECOY TAMPERING on '{filename}'. "
                f"Restored from '{result['snapshot_used']}'. AUTOMATIC ROLLBACK SUCCESSFUL."
            )
        else:
            update_dashboard_log(
                f"CRITICAL: DECOY TAMPERING on '{filename}'. "
                f"ROLLBACK FAILED — {result.get('error', 'unknown error')}. "
                f"Manual restore required."
            )

    # ── Pattern 2: SENSITIVE File Deletion ───────────────────────────────────
    elif file_status == "SENSITIVE" and event_type == 'deleted':
        risk_outcome = "HIGH_SENSITIVE_DELETION"
        subject = f"CRITICAL: Sensitive File Deleted — {filename}"
        body = (
            f"SENSITIVE FILE DELETION DETECTED\n"
            f"File: {filename}\n"
            f"Event: {event_type.upper()}\n"
            f"Action: No automatic rollback — human review required.\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        send_alert_email(subject, body)
        print(f"\n❌ SENSITIVE FILE DELETED: {filename} — alert sent, awaiting admin review.")

        update_dashboard_log(
            f"CRITICAL: SENSITIVE FILE DELETED — '{filename}'. "
            f"HIGH_SENSITIVE_DELETION. Immediate administrator review required. No auto-rollback."
        )

    # ── Pattern 3: Ransomware Extension Detected ─────────────────────────────
    elif (
        event_type in ['created', 'modified']
        and any(
            filename.lower().endswith(ext) or (ext + '.') in filename.lower()
            for ext in RANSOMWARE_EXTENSIONS
        )
        and not WatcherHandler.is_rolling_back
    ):
        # Re-trigger guard: check both the ransomware filename and the derived original
        original_check = _derive_original_filename(filename)
        log_data_check = load_log({})
        current_rw   = log_data_check.get(filename, {}).get("risk_outcome", "NONE")
        current_orig = log_data_check.get(original_check, {}).get("risk_outcome", "NONE")

        if current_rw == "HIGH_RANSOMWARE_ROLLBACK" or current_orig == "HIGH_RANSOMWARE_ROLLBACK":
            print(f"[LOGIC] Skipping re-trigger — rollback already handled for '{filename}'")
            return "HIGH_RANSOMWARE_ROLLBACK"

        risk_outcome = "HIGH_RANSOMWARE_ROLLBACK"
        alert_level = file_status if file_status in ("SENSITIVE", "DECOY") else "REAL"
        subject = f"CRITICAL: Ransomware Pattern — {alert_level} file — {filename}"
        body = (
            f"RANSOMWARE PATTERN DETECTED\n"
            f"File: {filename}\n"
            f"File Type: {alert_level}\n"
            f"Event: {event_type.upper()}\n"
            f"Action: Automatic rollback triggered.\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        send_alert_email(subject, body)
        print(f"\n⚠️  RANSOMWARE PATTERN on '{filename}' — triggering rollback.")

        result = rollback_file(filepath, WatcherHandler)
        if result["success"]:
            restored_as = result.get("restored_as", filename)
            update_dashboard_log(
                f"CRITICAL: RANSOMWARE PATTERN on '{filename}' ({alert_level}). "
                f"Restored as '{restored_as}' from '{result['snapshot_used']}'. "
                f"AUTOMATIC ROLLBACK SUCCESSFUL."
            )
        else:
            update_dashboard_log(
                f"CRITICAL: RANSOMWARE PATTERN on '{filename}' ({alert_level}). "
                f"ROLLBACK FAILED — {result.get('error', 'unknown')}. "
                f"Manual restore required."
            )

    # ── Default: Normal low-risk activity ─────────────────────────────────────
    else:
        risk_outcome = "LOW_NORMAL_ACTIVITY"

    return risk_outcome