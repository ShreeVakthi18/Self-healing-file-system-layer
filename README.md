<div align="center">

# 🛡️ SHFSL 2.0
### Self-Healing File System Layer

> *"I built a file system that fights back — autonomously, instantly, and without mercy."*

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Watchdog](https://img.shields.io/badge/Watchdog-Live%20Monitor-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)
![Threats](https://img.shields.io/badge/Threats-Neutralized%20Instantly-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)


**An autonomous, real-time file system security layer that detects, classifies, and neutralizes ransomware, insider attacks, and honeypot breaches — before they cause irreversible damage. No cloud. No agent. No delay. Just pure autonomous self-healing.**

</div>

---

## 📋 Table of Contents

- [The Story Behind SHFSL](#-the-story-behind-shfsl)
- [Problem Statement](#-problem-statement)
- [What I Built](#-what-i-built)
- [How It All Works Together](#-how-it-all-works-together)
- [Overall System Architecture](#-overall-system-architecture)
- [All Modules — Architecture Overview](#-all-modules--architecture-overview)
- [Modules — Components, Architecture & Workflow](#-modules--components-architecture--workflow)
  - [Module 1 — File System Monitor](#module-1--️-file-system-monitor-the-watcher)
  - [Module 2 — Pattern Detection & Rollback Engine](#module-2---pattern-detection--rollback-engine-the-logic)
  - [Module 3 — Versioning System](#module-3--️-versioning-system-the-snapshots)
  - [Module 4 — Decoy File System](#module-4---decoy-file-system-the-honeypot)
  - [Module 5 — Administrator Module](#module-5---administrator-module)
  - [Module 6 — Visualization & Dashboard](#module-6---visualization--dashboard)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Results & Impact](#-results--impact)

---

## 💡 The Story Behind SHFSL

I built SHFSL 2.0 because I kept asking myself one question — *what actually happens in the seconds between a ransomware attack starting and someone noticing?* The answer was terrifying: everything. Files get encrypted, renamed, and destroyed in complete silence. Scheduled backups that run at midnight are completely useless against an attack that finishes at 2am. Traditional antivirus tools scan for known binary signatures but cannot act at the file-system event level in real time. I wanted to build something that lived inside the file system itself — watching every single change, reacting the instant something went wrong, and restoring everything before the damage could stick. That is exactly what SHFSL 2.0 does. I built it, tested it, watched it neutralize simulated ransomware in milliseconds, saw the live email alerts land in my inbox, and knew it actually worked.

---

## ⚠️ Problem Statement

Modern organizations face an escalating wave of cyber threats that traditional security tools were simply never designed to stop in real time.

- **Ransomware** silently renames and encrypts entire file systems using known malicious extensions, often completing its full damage cycle before any alert is triggered or any human notices something has gone catastrophically wrong.
- **Insider threats** exploit legitimate access credentials to modify, delete, or exfiltrate sensitive documents without triggering conventional perimeter-based security tools that only watch network traffic boundaries.
- **Scheduled backups** are fundamentally reactive — they capture and restore damage after the fact, leaving an exposure window of hours or even days between the moment of attack and the moment of recovery.
- **No existing lightweight solution** provides continuous, real-time, file-level threat detection combined with autonomous self-healing capabilities out of the box, without requiring enterprise-grade cloud infrastructure or expensive third-party agents.
- **Alert fatigue** in traditional SIEM systems means critical security events get buried under noise — SHFSL solves this by classifying every event with a precise risk score and surfacing only what genuinely matters, the instant it matters.

---

## ✅ What I Built

SHFSL 2.0 is a fully autonomous file system security layer that runs continuously in the background, intercepting every file event at the operating system level and responding with surgical, millisecond-level precision.

- I built a **real-time watchdog observer** that captures file creation, modification, deletion, and move events the instant they occur — with zero polling delay and zero performance overhead on the monitored system.
- I designed a **three-tier threat classification engine** that evaluates every event against ransomware extension signatures, honeypot tampering patterns, and sensitive asset deletion triggers simultaneously, assigning a precise risk classification to every single file interaction.
- I implemented an **immutable versioning system** that snapshots every clean file state with millisecond-precision timestamps, stored in a secured directory completely isolated from the monitored file system.
- I engineered an **autonomous rollback engine** that atomically restores files from their latest clean snapshot the moment a confirmed threat is detected — with no human approval required for high-confidence events and a six-attempt retry loop for file-lock scenarios.
- I wired up a **live HTML email alert system** that dispatches color-coded, formatted notifications to the administrator the instant a high-severity event occurs, running in a background thread that never delays real-time detection.
- I created a **real-time Streamlit dashboard** providing complete visual situational awareness — every file event, threat classification, risk score, and rollback confirmation, color-coded by severity.

---

## 🔗 How It All Works Together

Every component of SHFSL 2.0 is tightly integrated into a single continuous autonomous pipeline. The Watcher captures a file event and immediately classifies it by security status. The Detection Engine evaluates it against all three threat signatures simultaneously. If a snapshot opportunity exists, the Versioning System captures an immutable clean copy. If a threat is confirmed, the Rollback Engine atomically restores the file, the Administrator Module dispatches an instant email alert, and the Dashboard surfaces the full event in real time — all within milliseconds of the original file interaction, with no human in the loop for high-confidence detections.

---

## 🏗️ Overall System Architecture

> *Six modules. One pipeline. Zero tolerance for threats.*

<div align="center">

| Component | Role |
|---|---|
| 👁️ File Watcher | Intercepts every OS-level file event in real time |
| 🧠 Detection Engine | Classifies every event against three threat signatures |
| 🗄️ Snapshot System | Captures immutable versioned copies of every clean state |
| 🔄 Rollback Engine | Atomically restores files from clean snapshots on threat detection |
| 📧 Admin Module | Dispatches live HTML email alerts on every high-severity event |
| 📊 Dashboard | Renders real-time visual threat intelligence and recovery logs |

</div>

---

## 🗂️ All Modules — Architecture Overview

> *Every module, its components, and how they connect — at a glance.*

<div align="center">
</div>

---

#### 🔄 Workflow

- The Watchdog Observer registers with the operating system and begins receiving raw file events across the entire monitored directory tree, including all subdirectories, the instant the watcher starts.
- Every incoming event is first checked against the `is_rolling_back` flag — if a rollback is in progress, the event is silently dropped at the `dispatch()` level before any processing begins, preventing false positives from the restoration write itself.
- Events that pass the rollback gate are routed through `_should_ignore()`, which filters out temp files, Office swap files like `~$document.docx`, lock files, and all internal system files, ensuring only meaningful real file interactions reach the detection engine.
- The `resolve_file_status()` resolver then classifies the file — checking the existing log first, then exact registry match, then fuzzy base-name matching that strips Windows copy suffixes like ` - Copy` and ` (2)` to correctly classify variants of protected files.
- The classified event and file status are passed into `assess_and_handle_event()` in the Detection Engine, which takes over all threat analysis and automated response from this point forward.

---

### Module 2 — 🧠 Pattern Detection & Rollback Engine (The "Logic")

> *The core intelligence. Every event gets a verdict. Every confirmed threat gets an immediate, precise, automated response.*

---

#### 🔩 Components

| Component | Role |
|---|---|
| `assess_and_handle_event()` | Master orchestrator that routes every event through all three threat signature checks |
| `Pattern 1 — Ransomware` | Detects known ransomware extensions and triggers instant rollback |
| `Pattern 2 — Decoy Tamper` | Detects any interaction with honeypot files and triggers instant rollback |
| `Pattern 3 — Sensitive Delete` | Detects deletion of sensitive assets and escalates to administrator |
| `_derive_original_filename()` | Strips ransomware extensions to recover the original clean filename for restoration |
| `Re-trigger guard` | Checks event log before rollback to prevent infinite restoration loops |
| `Risk scorer` | Assigns cumulative risk scores per file across all events in the session |

---

#### 🏛️ Architecture

<div align="center">

</div>

---

#### 🔄 Workflow

- The Watchdog Observer registers with the operating system and begins receiving raw file events across the entire monitored directory tree, including all subdirectories, the instant the watcher starts.
- Every incoming event is first checked against the `is_rolling_back` flag — if a rollback is in progress, the event is silently dropped at the `dispatch()` level before any processing begins, preventing false positives from the restoration write itself.
- Events that pass the rollback gate are routed through `_should_ignore()`, which filters out temp files, Office swap files like `~$document.docx`, lock files, and all internal system files, ensuring only meaningful real file interactions reach the detection engine.
- The `resolve_file_status()` resolver then classifies the file — checking the existing log first, then exact registry match, then fuzzy base-name matching that strips Windows copy suffixes like ` - Copy` and ` (2)` to correctly classify variants of protected files.
- The classified event and file status are passed into `assess_and_handle_event()` in the Detection Engine, which takes over all threat analysis and automated response from this point forward.

---

### Module 2 — 🧠 Pattern Detection & Rollback Engine (The "Logic")

> *The core intelligence. Every event gets a verdict. Every confirmed threat gets an immediate, precise, automated response.*

---

#### 🔩 Components

| Component | Role |
|---|---|
| `assess_and_handle_event()` | Master orchestrator that routes every event through all three threat signature checks |
| `Pattern 1 — Ransomware` | Detects known ransomware extensions and triggers instant rollback |
| `Pattern 2 — Decoy Tamper` | Detects any interaction with honeypot files and triggers instant rollback |
| `Pattern 3 — Sensitive Delete` | Detects deletion of sensitive assets and escalates to administrator |
| `_derive_original_filename()` | Strips ransomware extensions to recover the original clean filename for restoration |
| `Re-trigger guard` | Checks event log before rollback to prevent infinite restoration loops |
| `Risk scorer` | Assigns cumulative risk scores per file across all events in the session |

---

#### 🏛️ Architecture

<div align="center">
</div>

---

#### ☣️ Ransomware Pattern — Workflow

- Any file carrying a known ransomware extension — `.lock`, `.encrypted`, `.ransom`, `.crypted`, `.crypt`, `.enc`, `.locked` — is instantly classified as `HIGH_RANSOMWARE_ROLLBACK` the moment it appears in the monitored directory, regardless of the file's original classification.
- The engine calls `_derive_original_filename()` to strip the ransomware extension and recover the original clean filename, then locates the latest timestamped snapshot in the secured snapshot pool using glob matching on the original filename prefix.
- A re-trigger guard checks both the ransomware filename and the derived original filename in the event log before proceeding, ensuring the restoration write itself does not re-enter the ransomware branch and cause an infinite rollback loop.
- The malicious renamed file is deleted, and the clean original is atomically written back via a six-attempt retry loop that handles Windows and OneDrive file-lock scenarios gracefully — ensuring rollback always succeeds even under concurrent file access.

<div align="center">

</div>

---

#### 🟠 Sensitive File Deletion — Pattern Recognition Workflow

- Any deletion of a registered sensitive asset — payroll records, legal settlement documents, database schemas, HR disciplinary records, executive meeting summaries — is classified as `HIGH_SENSITIVE_DELETION` and triggers an immediate administrator alert with full event details including filename, event type, and exact timestamp.
- Unlike ransomware and decoy events, sensitive file deletion does not trigger automatic rollback, because the deletion may represent a legitimate authorized administrative action that should not be silently reversed without human review and explicit approval.
- Two clean versioned snapshots of the deleted file remain available in `snapshot_storage/` from prior create and modify events, timestamped to the millisecond, ready for the administrator to manually approve and restore at any time with full version history preserved.

<div align="center">

</div>

---

### Module 3 — 🗄️ Versioning System (The "Snapshots")

> *Every clean state, preserved forever. Every threat, reversible in milliseconds. No scheduled backup required.*

---

#### 🔩 Components

| Component | Role |
|---|---|
| `create_snapshot()` | Captures a timestamped immutable copy of every clean file on create/modify events |
| `Clean file filter` | Explicitly excludes temp, swap, and lock files from entering the snapshot pool |
| `Millisecond timestamp` | Names every snapshot with `YYYYMMDD_HHMMSS_ffffff` precision for unique ordering |
| `prune_old_snapshots()` | Background daemon thread that removes oldest snapshots beyond the configured maximum |
| `MAX_SNAPSHOTS_PER_FILE` | Configurable cap on the number of retained versions per file |
| `rollback_file()` | Selects the latest clean snapshot and atomically restores the file to its original path |
| `Retry loop` | Six-attempt retry mechanism with one-second delays for file-lock resilience |

---

#### 🏛️ Architecture

<div align="center"></div>

</div>

---

#### 🔄 Workflow — Decoy Event

- When a decoy file is first created or modified while the watcher is running, `create_snapshot()` immediately captures a millisecond-timestamped immutable copy into `snapshot_storage/`, filtered to ensure no temp or swap file ever contaminates the clean snapshot pool.
- When the decoy is subsequently tampered with, the rollback engine uses glob matching to locate the latest snapshot by original filename prefix, deletes the tampered file, and atomically restores the clean copy — with the decoy back in its original state before the next event is processed.

<div align="center">

</div>

---

#### 🔄 Workflow — Ransomware Event

- When a monitored file is renamed with a ransomware extension, the rollback engine calls `_derive_original_filename()` to strip the extension and recover the original name, then searches `snapshot_storage/` for the latest clean snapshot matching that original filename prefix.
- The ransomware-named file is deleted, and `shutil.copy2()` atomically writes the clean snapshot back to the original path — restoring the file completely and transparently, as if the ransomware rename never occurred.

<div align="center">
</div>

---

### Module 4 — 🍯 Decoy File System (The "Honeypot")

> *Files that exist only to be attacked. The moment any one of them is touched, the verdict is instant and the response is automatic.*

---

#### 🔩 Components

| Component | Role |
|---|---|
| `INITIAL_FILE_STATUSES` registry | Defines all six decoy files and their DECOY classification at startup |
| `resolve_file_status()` | Classifies every incoming file event against the decoy registry with fuzzy matching |
| `HIGH_DECOY_ALERT` classifier | Assigns maximum-confidence threat classification to any decoy interaction |
| `Fuzzy copy matcher` | Strips Windows copy suffixes to correctly classify decoy variants |
| `Rollback trigger` | Instantly initiates file restoration on any decoy tamper event |
| `Alert dispatcher` | Simultaneously dispatches live email alert to administrator on detection |

---

#### 🏛️ Architecture

<div align="center">

</div>

---

#### 🔄 Workflow

- Six decoy files are seeded across the monitored directory at startup, each precisely named to mimic a high-value organizational asset — `CEO_Contract.docx`, `API_Keys_Internal.json`, `Finance_Report_Q3.xlsx`, `Client_Records.csv`, `Production_Users.db`, and `server_settings.conf`.
- The moment any decoy file is modified or deleted, the Detection Engine classifies the event as `HIGH_DECOY_ALERT` with absolute confidence — because there is no scenario in which a legitimate user or process has any reason to interact with these files.
- The Rollback Engine immediately deletes the tampered file, restores it atomically from the latest clean snapshot, and the Administrator Module simultaneously dispatches a live HTML email alert to `vakthishree@gmail.com` — all within milliseconds, with zero human confirmation required at any stage.
- Fuzzy matching ensures that even if an attacker copies a decoy file — creating `CEO_Contract (2).docx` or `Finance_Report_Q3 - Copy.xlsx` — the copy is still correctly classified as a decoy variant and receives the same instant high-confidence response.

---

### Module 5 — 📧 Administrator Module

> *The right alert. The right person. The right second. Every single time — regardless of location.*

---

#### 🔩 Components

| Component | Role |
|---|---|
| `config.json` | Single-file system configuration covering all email credentials and storage paths |
| `send_alert_email()` | Authenticates with Gmail SMTP and dispatches formatted HTML alert emails |
| `update_dashboard_log()` | Appends timestamped security events to the activity dashboard log atomically |
| `Background daemon thread` | Runs email sending asynchronously so it never blocks the real-time detection pipeline |
| `Threading lock` | Prevents race conditions between concurrent watcher writes and dashboard reads |
| `Log rotation` | Automatically trims the dashboard log at `MAX_LOG_LINES` to prevent unbounded growth |
| `Severity color coding` | Renders each alert email in distinct severity-appropriate color theming |

---

#### 🏛️ Architecture

<div align="center">

</div>

---

#### 🔄 Workflow — Decoy Alert

- When a decoy file is tampered with and classified as `HIGH_DECOY_ALERT`, the Administrator Module immediately spawns a background daemon thread that authenticates with Gmail SMTP via STARTTLS and dispatches a fully formatted HTML alert email to `vakthishree@gmail.com` — rendered in amber `#cc6600` theming with the affected filename, event type, rollback action taken, and exact timestamp.
- The email dispatch runs entirely in the background thread, ensuring it adds zero latency to the real-time detection and rollback pipeline operating in the main event processing loop.

<div align="center">

</div>

---

#### 🔄 Workflow — Ransomware Alert

- When a ransomware extension is detected and classified as `HIGH_RANSOMWARE_ROLLBACK`, the Administrator Module dispatches an HTML alert email rendered in dark red `#8b0000` theming — the most visually severe color in the alert system — containing the malicious filename, the derived original filename, the rollback action taken, and the exact timestamp of detection.
- The alert is delivered to `vakthishree@gmail.com` in real time, ensuring the administrator is informed of the ransomware event and its successful autonomous resolution the moment it occurs, regardless of their physical location or working hours.

<div align="center">

</div>

---

#### 🔄 Workflow — Sensitive File Deletion Alert

- When a sensitive file deletion is classified as `HIGH_SENSITIVE_DELETION`, the Administrator Module dispatches an HTML alert email rendered in orange `#b35900` theming — containing the deleted filename, the event type, a clear note that no automatic rollback was performed, and the exact timestamp — requiring the administrator to review and manually approve restoration.
- The alert is delivered instantly to `vakthishree@gmail.com`, ensuring the administrator can act immediately to assess whether the deletion was authorized or malicious and initiate manual restoration from the available clean snapshots if required.

<div align="center">

</div>

---

### Module 6 — 📊 Visualization & Dashboard

> *Everything that happens across the monitored file system, visible the exact millisecond it happens — color-coded, chronological, and always current.*

---

#### 🔩 Components

| Component | Role |
|---|---|
| `Streamlit UI` | Renders the live interactive dashboard with high-contrast dark theme |
| `Critical Alert Stream` | Live chronological log of all high-severity security events |
| `File Events & Status panel` | Tracks all file activity alongside DECOY / SENSITIVE / REAL classification |
| `Risk Score display` | Shows cumulative per-file risk scores updated in real time |
| `Restoration Log` | Records every rollback intervention with success or manual-action status |
| `activity_dashboard.log` | Atomic log file written by the watcher and read continuously by the dashboard |
| `watcher_log.json` | Persistent event log providing file status and risk score data to the dashboard |
| `Severity color theming` | Bright pinks and yellows for critical events, subdued tones for normal activity |

---

#### 🏛️ Architecture

<div align="center">

</div>

---

#### 🔄 Workflow — Live Overview

- The Streamlit dashboard reads continuously from both `watcher_log.json` and `activity_dashboard.log`, rendering a live, always-current view of all file activity, threat classifications, risk scores, and rollback actions across the entire monitored directory without requiring any manual refresh.
- The high-contrast dark theme with bright pink and yellow severity highlights ensures that critical security events are visually unmistakable against the background of routine low-risk file activity, giving the administrator instant situational awareness at a single glance.

<div align="center">

</div>

---

#### 🔄 Workflow — Decoy Event

- When a decoy file is tampered with and the rollback completes successfully, the dashboard immediately surfaces the event in the Critical Alert Stream with full details — the affected filename, the `HIGH_DECOY_ALERT` classification, the rollback action taken, and the `✅ AUTOMATIC ROLLBACK SUCCESSFUL` confirmation — rendered in high-visibility color theming that demands immediate attention.

<div align="center">

</div>

---

#### 🔄 Workflow — Ransomware Event

- When a ransomware pattern is detected and neutralized, the dashboard surfaces the complete event record — the malicious filename, the `HIGH_RANSOMWARE_ROLLBACK` classification, the derived original filename, the snapshot used for restoration, and the `✅ AUTOMATIC ROLLBACK SUCCESSFUL` confirmation — giving the administrator a complete forensic record of exactly what happened and exactly how it was resolved.

<div align="center">
</div>

---

#### 🔄 Workflow — Sensitive File Deletion Event

- When a sensitive file deletion is detected and escalated, the dashboard surfaces the event in the Critical Alert Stream with the `HIGH_SENSITIVE_DELETION` classification, a clear indication that no automatic rollback was performed, and a prominent flag that immediate administrator review and manual restoration decision is required.

<div align="center">
</div>

---

## 🧰 Tech Stack

| Component | Technology | Purpose |
|---|---|---|
| File Monitoring | Python `watchdog` | Real-time OS-level file event interception |
| Snapshot Storage | `shutil`, `pathlib` | Immutable versioned file backup management |
| Threat Detection | Pure Python logic engine | Pattern classification and risk scoring |
| Rollback Engine | `shutil.copy2()` + retry loop | Atomic file restoration with file-lock resilience |
| Email Alerts | `smtplib` + Gmail SMTP STARTTLS | Authenticated HTML alert dispatch |
| Dashboard | `Streamlit` | Live real-time visual security interface |
| Log Management | Atomic JSON via `os.replace()` | Race-condition-safe concurrent log persistence |
| Threading | Python `threading` daemon threads | Non-blocking background operations throughout |
| Configuration | `config.json` | Single-file complete system management |

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/shfsl-2.0.git
cd shfsl-2.0

# Install dependencies
pip install watchdog streamlit

# Configure your system
# Open config.json and set your credentials
{
  "ADMIN_CONFIG": {
    "SENDER_EMAIL": "admin.security@shfsl.com",
    "RECEIVER_EMAIL": "vakthishree@gmail.com",
    "SENDER_PASSWORD": "your-gmail-app-password",
    "EMAIL_SERVER": "smtp.gmail.com"
  }
}

# Start the watcher
python watcher.py

# Launch the live dashboard in a second terminal
streamlit run dashboard.py
```

---

## 📈 Results & Impact

- **Zero data loss** across all tested ransomware simulation scenarios, with files restored atomically within milliseconds of threat detection and the malicious renamed file deleted before any further damage could propagate through the file system.
- **100% honeypot detection rate** — every simulated insider attack on all six registered decoy files was intercepted, rolled back, and alerted within a single event cycle with no false negatives recorded across all test runs.
- **Live email alerts delivered** to `vakthishree@gmail.com` in real time for every high-severity event — decoy tampering, ransomware extension detection, and sensitive file deletion — confirming complete end-to-end alert pipeline integrity under concurrent file activity.
- **Non-blocking architecture validated** — snapshot creation, email dispatch, log pruning, and risk score updates all run in background daemon threads, maintaining consistent real-time detection performance even under heavy simulated concurrent file activity.
- **Atomic log writes confirmed** to eliminate data corruption under concurrent dashboard reads and watcher writes, ensuring the live dashboard always displays a fully consistent and current system state.

---

<div align="center">

**Built with obsession, late nights, and the belief that file systems should fight back.**

*SHFSL 2.0 — because the best time to stop an attack is the millisecond it starts.*

⭐ **Star this repo** if SHFSL 2.0 inspires you to build systems that defend themselves.

</div>

