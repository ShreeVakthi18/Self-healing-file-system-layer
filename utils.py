# utils.py — SHFSL 2.0 (FULLY FIXED)
import json
import os
import shutil
from datetime import datetime

ROOT_FOLDER = os.getcwd()
LOG_FILE = os.path.join(ROOT_FOLDER, "watcher_log.json")


def save_log(log_data):
    """
    Saves the file event log to disk atomically.
    Writes to a temp file first then renames — prevents the dashboard from
    ever reading a half-written (empty/corrupt) JSON file.
    """
    tmp_path = LOG_FILE + ".tmp"
    try:
        json_str = json.dumps(log_data, indent=4)
        with open(tmp_path, 'w') as f:
            f.write(json_str)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, LOG_FILE)
    except TypeError as e:
        print(f"[UTILS] ❌ Log data not serializable: {e}")
    except Exception as e:
        print(f"[UTILS] ❌ Could not save log file: {e}")
        try:
            os.remove(tmp_path)
        except Exception:
            pass


def load_log(initial_statuses):
    """
    Loads the file event log, initializing entries for any new tracked files.
    Handles JSON corruption by backing up and re-initializing.
    FIX: Preserves risk_score on all updates — never overwrites accumulated score.
    """
    log_data = {}

    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                content = f.read().strip()
            if content:
                log_data = json.loads(content)
        except json.JSONDecodeError:
            backup_path = LOG_FILE + f".corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            try:
                shutil.copy2(LOG_FILE, backup_path)
                print(f"[UTILS] ⚠️  Corrupted log backed up to {backup_path}")
            except Exception:
                pass
            print("[UTILS] ⚠️  Corrupted JSON log. Re-initializing from scratch.")
            log_data = {}

    changed = False
    for filename, initial_status in initial_statuses.items():
        if filename not in log_data or "status" not in log_data[filename]:
            log_data[filename] = {
                "last_modified": "N/A",
                "initialized_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": initial_status,
                "event": "initialized",
                "risk_outcome": "NONE",
                "last_event": "initialized",
                "risk_score": 0,
            }
            changed = True
        elif (
            os.path.exists(os.path.join(ROOT_FOLDER, filename)) and
            log_data[filename].get("status") != initial_status
        ):
            # FIX: Only update status — NEVER wipe risk_score on a status correction
            log_data[filename]["status"] = initial_status
            log_data[filename]["last_event"] = "status_corrected"
            changed = True

    if changed:
        save_log(log_data)

    return log_data


def update_risk_score(log_data, filename, new_outcome):
    """
    FIX: Centralized risk score update that operates directly on the log_data dict
    in memory, then returns the updated score. This prevents the race condition where
    get_adaptive_risk_score() would save to disk and then process_event() would
    overwrite the risk_score by loading an old snapshot.

    Risk score weights:
      HIGH_RANSOMWARE_ROLLBACK → +100 (capped at 100)
      HIGH_DECOY_ALERT         → +90
      HIGH_SENSITIVE_DELETION  → +75
      LOW_NORMAL_ACTIVITY      → +5
      NONE                     → +0
    """
    RISK_WEIGHTS = {
        "HIGH_RANSOMWARE_ROLLBACK": 100,
        "HIGH_DECOY_ALERT":         90,
        "HIGH_SENSITIVE_DELETION":  75,
        "LOW_NORMAL_ACTIVITY":      5,
        "NONE":                     0,
    }
    entry = log_data.get(filename, {})
    current_score = entry.get("risk_score", 0)
    spike = RISK_WEIGHTS.get(new_outcome, 0)
    new_score = min(current_score + spike, 100)

    if filename in log_data:
        log_data[filename]["risk_score"] = new_score
    return new_score


def get_risk_summary(log_data):
    """Returns a summary dict of current risk state across all files."""
    summary = {
        "total_files": len(log_data),
        "high_risk_count": 0,
        "sensitive_deletions": 0,
        "ransomware_events": 0,
        "decoy_tampers": 0,
        "max_risk_score": 0,
        "highest_risk_file": None,
    }

    for filename, entry in log_data.items():
        outcome = entry.get("risk_outcome", "NONE")
        score = entry.get("risk_score", 0)

        if outcome.startswith("HIGH_"):
            summary["high_risk_count"] += 1
        if "SENSITIVE_DELETION" in outcome:
            summary["sensitive_deletions"] += 1
        if "RANSOMWARE" in outcome:
            summary["ransomware_events"] += 1
        if "DECOY" in outcome:
            summary["decoy_tampers"] += 1
        if score > summary["max_risk_score"]:
            summary["max_risk_score"] = score
            summary["highest_risk_file"] = filename

    return summary