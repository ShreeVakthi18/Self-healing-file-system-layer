# watcher.py — SHFSL 2.0 (FULLY FIXED)
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from logic_and_snapshots import assess_and_handle_event
from utils import load_log, save_log, update_risk_score

# --- Configuration ---
ROOT_FOLDER = os.getcwd()
LOG_FILE    = os.path.join(ROOT_FOLDER, "watcher_log.json")

# --- File Status Registry ---
INITIAL_FILE_STATUSES = {
    # DECOY FILES (honeypots)
    "API_Keys_Internal.json":       "DECOY",
    "CEO_Contract.docx":            "DECOY",
    "Finance_Report_Q3.xlsx":       "DECOY",
    "Client_Records.csv":           "DECOY",
    "Production_Users.db":          "DECOY",
    "server_settings.conf":         "DECOY",

    # SENSITIVE FILES
    "credentials_backup.zip":           "SENSITIVE",
    "archived_emails.pst":              "SENSITIVE",
    "User_Access_Log.xlsx":             "SENSITIVE",
    "Legal_Settlement_Docs.docx":       "SENSITIVE",
    "HR_Disciplinary_Records.docx":     "SENSITIVE",
    "Patent_Application_Draft.docx":    "SENSITIVE",
    "Executive_Meeting_Summary.docx":   "SENSITIVE",
    "Q4_Budget_Forecast.xlsx":          "SENSITIVE",
    "Vendor_Payment_Schedules.xlsx":    "SENSITIVE",
    "Server_Inventory.xlsx":            "SENSITIVE",
    "Server_Inventory - Copy.xlsx":     "SENSITIVE",
    "Employee_List.xlsx":               "SENSITIVE",
    "Database_Schema.sql":              "SENSITIVE",
    "app_config.ini":                   "SENSITIVE",
    "Full_Backup_2025.zip":             "SENSITIVE",
    "ProjectPlan.docx":                 "SENSITIVE",
    "Roadmap_2025.docx":                "SENSITIVE",
    "Company_Policy_Manual.docx":       "SENSITIVE",
    "Onboarding_Checklist.docx":        "SENSITIVE",
    "meeting_transcript.txt":           "SENSITIVE",
    "server_log_2025-10.log":           "SENSITIVE",
}

IGNORE_FOLDERS = ["__pycache__", "snapshot_storage", "snapshots", "staging", ".git"]
IGNORE_FILES = [
    "watcher.py", "logic_and_snapshots.py", "admin_logic.py", "config.json",
    "watcher_log.json", "watcher_log.json.tmp",
    "create_office_files.py", "create_dummy_files.py", "create_files_root.py",
    "activity_dashboard.log", "activity_dashboard.log.tmp",
    "utils.py", "dashboard.py",
]


def resolve_file_status(filename, log_data):
    """
    Determines the security status of a file with fuzzy matching.

    Priority order:
      1. Already classified in log_data (from a prior event in this session)
      2. Exact match in INITIAL_FILE_STATUSES registry
      3. Fuzzy base-name match: strips Windows copy suffixes like ' (2)', ' - Copy'
         and matches against registry  (e.g. "CEO_Contract (3).docx" → DECOY)
      4. Default: REAL
    """
    import re

    # 1. Already classified
    existing = log_data.get(filename, {}).get("status")
    if existing in ("DECOY", "SENSITIVE"):
        return existing

    # 2. Exact match
    if filename in INITIAL_FILE_STATUSES:
        return INITIAL_FILE_STATUSES[filename]

    # 3. Fuzzy base-name match
    base, ext = os.path.splitext(filename)
    stripped = re.sub(r'\s*-\s*Copy(\s*\(\d+\))?$', '', base, flags=re.IGNORECASE)
    stripped = re.sub(r'\s*\(\d+\)$', '', stripped).strip()
    candidate = stripped + ext

    if candidate in INITIAL_FILE_STATUSES:
        status = INITIAL_FILE_STATUSES[candidate]
        print(f"[STATUS] '{filename}' matched as variant of '{candidate}' → {status}")
        return status

    # 4. Default
    return "REAL"


class WatcherHandler(FileSystemEventHandler):

    # Class-level flag shared across all instances/threads
    is_rolling_back = False

    def dispatch(self, event):
        """Drop ALL events while a rollback is in progress."""
        if self.is_rolling_back:
            return
        super().dispatch(event)

    def _should_ignore(self, filepath):
        """Returns True if this file/path should be silently skipped."""
        filename = os.path.basename(filepath)
        fn_lower = filename.lower()

        # Temp/lock/Office swap files
        SKIP_PREFIXES = ('~wrl', '~$', '.~', '~')
        SKIP_SUFFIXES = ('.tmp', '.temp', '.swp', '.part', '.lnk', '.db-journal')
        if (any(fn_lower.startswith(p) for p in SKIP_PREFIXES) or
                any(fn_lower.endswith(s) for s in SKIP_SUFFIXES) or
                filename.startswith('.')):
            return True

        # System/internal folders
        if any(folder in filepath for folder in IGNORE_FOLDERS):
            return True

        # System/internal files
        if filename in IGNORE_FILES:
            return True

        return False

    def process_event(self, event_type, path):
        """
        Core event processing pipeline.

        FIXED BUGS:
        1. Risk score is now updated IN THE SAME log_data dict that gets saved,
           preventing the race where an old snapshot would overwrite the new score.
        2. on_moved now correctly checks is_rolling_back for its synthetic delete event.
        3. log_entry update preserves the existing risk_score rather than always
           resetting it to whatever was in the (potentially stale) loaded dict.
        """
        if self.is_rolling_back:
            return

        filepath = os.path.abspath(path)
        filename = os.path.basename(filepath)

        if self._should_ignore(filepath):
            return

        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"\n[{ts}] EVENT: {event_type.upper()} → {filename}")

        # Load current log state (with all initialized statuses seeded)
        log_data = load_log(INITIAL_FILE_STATUSES)

        # Resolve file status (fuzzy match for copies/variants)
        file_status = resolve_file_status(filename, log_data)
        print(f"[{ts}] STATUS: {filename} classified as '{file_status}'")

        # Run through the logic/pattern-detection engine
        risk_outcome = assess_and_handle_event(event_type, filepath, file_status, self)

        # Determine last_modified timestamp
        last_modified = "DELETED"
        if os.path.exists(filepath):
            try:
                last_modified = time.ctime(os.path.getmtime(filepath))
            except FileNotFoundError:
                last_modified = "DELETED"

        # FIX: Reload log_data after assess_and_handle_event because rollback_file
        # may have taken several seconds; another event could have updated the log
        # in the meantime. We want to write fresh, not stale data.
        log_data = load_log(INITIAL_FILE_STATUSES)

        # FIX: Update risk score IN MEMORY on this log_data dict before saving.
        # This replaces the old get_adaptive_risk_score() which saved separately
        # and was then overwritten by save_log() here.
        new_score = update_risk_score(log_data, filename, risk_outcome)
        if new_score >= 75:
            print(f"[RISK] ⚠️  {filename} cumulative risk score: {new_score}/100")

        # Build/update the log entry for this file
        existing_entry = log_data.get(filename, {})
        existing_entry.update({
            "last_modified": last_modified,
            "status":        file_status,
            "event":         event_type,
            "risk_outcome":  risk_outcome,
            "last_event":    event_type,
            # risk_score already updated in-memory by update_risk_score() above
        })
        log_data[filename] = existing_entry

        save_log(log_data)

        print(f"[{ts}] RESULT: {filename} → {risk_outcome} (score: {new_score}/100)")

    # ── Watchdog Event Handlers ───────────────────────────────────────────────

    def on_created(self, event):
        if not event.is_directory and not self.is_rolling_back:
            self.process_event("created", event.src_path)

    def on_deleted(self, event):
        # FIX: Also guard on_deleted with is_rolling_back — previously only
        # on_created and on_modified had this guard, leaving on_deleted unprotected.
        if not event.is_directory and not self.is_rolling_back:
            self.process_event("deleted", event.src_path)

    def on_modified(self, event):
        if not event.is_directory and not self.is_rolling_back:
            self.process_event("modified", event.src_path)

    def on_moved(self, event):
        # FIX: Guard both synthetic events with is_rolling_back check.
        # Previously on_moved had NO is_rolling_back guard at all.
        if not event.is_directory and not self.is_rolling_back:
            self.process_event("deleted", event.src_path)
            # Small delay so the "deleted" write completes before "created" runs
            time.sleep(0.05)
            if not self.is_rolling_back:
                self.process_event("created", event.dest_path)


def start_watcher():
    """Initialize the file registry and start the observer."""
    load_log(INITIAL_FILE_STATUSES)  # Seed the log with all file statuses on startup

    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, ROOT_FOLDER, recursive=True)
    observer.start()

    print("\n╔══════════════════════════════════════════════════╗")
    print("║   SHFSL 2.0 — Watcher ACTIVE                    ║")
    print(f"║   Monitoring: {ROOT_FOLDER[:34]:<34} ║")
    print(f"║   Protected files: {len(INITIAL_FILE_STATUSES):<29} ║")
    print("╚══════════════════════════════════════════════════╝\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[WATCHER] Stopping — KeyboardInterrupt received.")

    observer.join()
    print("[WATCHER] Stopped cleanly.")


if __name__ == "__main__":
    print("─── SHFSL 2.0 Watcher Initializing ───")
    print(f"Root folder: {ROOT_FOLDER}")
    start_watcher()