</div>

- The Watchdog Observer registers with the operating system and begins receiving raw file events across the entire monitored directory tree, including all subdirectories, the instant the watcher process starts running.
- Every incoming event is first checked against the `is_rolling_back` flag — if a rollback is in progress, the event is silently dropped at the `dispatch()` level before any processing begins, preventing false positives from the restoration write contaminating the event queue.
- Events that pass the rollback gate are routed through `_should_ignore()`, which filters out temp files, Office swap files like `~$document.docx`, lock files, and all internal system files, ensuring only meaningful real file interactions ever reach the detection engine.
- The `resolve_file_status()` resolver classifies the file — checking the existing log first, then exact registry match, then fuzzy base-name matching that strips Windows copy suffixes like ` - Copy` and ` (2)` to correctly classify variants of protected files automatically.
- The classified event and file status are handed into `assess_and_handle_event()` in the Detection Engine, which takes over all threat analysis and automated response from this point forward.

---

### Module 2 — 🧠 Pattern Detection & Rollback Engine

> *The core intelligence. Every event gets a verdict. Every confirmed threat gets an immediate, precise, automated response.*

**Purpose:** The Detection Engine is the brain of SHFSL 2.0 — evaluating every file event against three distinct threat signatures and triggering the precise automated response each threat demands, with no human confirmation required for high-confidence detections.

---

#### 🔩 Components

| Component | Role |
|---|---|
| `assess_and_handle_event()` | Master orchestrator routing every event through all three threat signature checks |
| `Pattern 1 — Ransomware` | Detects known ransomware extensions and triggers instant atomic rollback |
| `Pattern 2 — Decoy Tamper` | Detects any interaction with honeypot files and triggers instant atomic rollback |
| `Pattern 3 — Sensitive Delete` | Detects deletion of sensitive assets and escalates immediately to administrator |
| `_derive_original_filename()` | Strips ransomware extensions to recover the original clean filename for restoration |
| `Re-trigger guard` | Checks event log before rollback to prevent infinite restoration loops |
| `Risk scorer` | Assigns cumulative weighted risk scores per file across all events in the session |

---

#### 🏛️ Architecture

<div align="center">
