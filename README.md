<div align="center">

<br>

```
███████╗██╗  ██╗███████╗███████╗██╗      ██████╗     ██████╗      ██████╗
██╔════╝██║  ██║██╔════╝██╔════╝██║     ╚════██╗    ██╔═████╗    ╚════██╗
███████╗███████║█████╗  ███████╗██║      █████╔╝    ██║██╔██║     █████╔╝
╚════██║██╔══██║██╔══╝  ╚════██║██║     ██╔═══╝     ████╔╝██║    ██╔═══╝
███████║██║  ██║██║     ███████║███████╗███████╗    ╚██████╔╝    ███████╗
╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝╚══════╝╚══════╝     ╚═════╝     ╚══════╝
```

# SHFSL 2.0 — Self Healing File System Layer

**Not another security tool that watches and logs. One that intercepts, classifies, and reverses.**

<br>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Watchdog](https://img.shields.io/badge/Watchdog-Real--Time-00C896?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-Academic-blueviolet?style=for-the-badge)

<br>

</div>

---

<br>

## The Problem

- Firewalls block traffic. They do not restore encrypted files.
- Antivirus detects known malware signatures. It does not undo ransomware damage.
- Access control lists manage permissions. They do not stop a privileged insider from deleting critical assets.
- Scheduled backups run every few hours. Ransomware encrypts an entire directory in seconds.
- Every conventional security tool generates logs and alerts after damage occurs. None of them reverse it.

> I built SHFSL 2.0 to be the first layer that autonomously heals the file system in real time before damage can propagate.

<br>

---

<br>

## Core Capabilities

- Real-time watchdog-based interception of every file creation, modification, deletion, and move event
- Rule-based pattern detection engine evaluating three high-fidelity threat signatures
- Automated rollback via immutable, millisecond-timestamped versioned snapshots
- Honeypot decoy layer for zero-false-positive insider threat detection
- Live HTML email alerting via authenticated SMTP on every high-severity event
- Adaptive cumulative risk scoring per file, capping at 100
- Real-time Streamlit dashboard with color-coded severity theming

<br>

---

<br>

## System Architecture

```
           +------------------------------------------+
           |            USER ACTIVITY                  |
           |   file create / modify / delete / move    |
           +--------------------+---------------------+
                                |
                                v
           +------------------------------------------+
           |        FILE SYSTEM MONITOR               |
           |            (The Watcher)                 |
           |  watchdog observer, zero polling delay   |
           |  noise filter + event forwarding         |
           +--------------------+---------------------+
                                |
                                v
           +------------------------------------------+
           |   PATTERN DETECTION & ROLLBACK ENGINE    |
           |             (The Logic)                  |
           |  ransomware / decoy tamper /             |
           |  sensitive deletion classification       |
           +----------+-----------------+------------+
                      |                 |
          +-----------v------+   +------v------------------+
          | VERSIONING       |   | ADMINISTRATOR MODULE    |
          | SYSTEM           |   | HTML email alerts       |
          | (Snapshots)      |   | SMTP dispatch           |
          +--------+---------+   +----------+--------------+
                   |                        |
                   +------------+-----------+
                                |
                                v
               +-----------------------------------+
               |   VISUALIZATION & DASHBOARD      |
               |   live Streamlit interface        |
               |   real-time threat visibility     |
               +-----------------------------------+
```

<br>

---

<br>

## The Six Modules

<br>

### 1. File System Monitor — The "Watcher"

![Watcher](./images/watcher.png)

**Purpose**

Entry point of the entire SHFSL 2.0 pipeline. Maintains a persistent real-time watch over all designated directories.

**How It Works**

- Built on Python's `watchdog` library
- Registers a recursive event handler against the monitored root directory
- Intercepts every `FileCreatedEvent`, `FileModifiedEvent`, `FileDeletedEvent`, and `FileMovedEvent` with zero polling delay
- Passes all events through an ignore filter that strips temp files, Office swap files, and internal system files
- Implements an `is_rolling_back` flag that completely silences watchdog during active rollback — preventing restore operations from generating cascading false events
- Resumes full monitoring automatically once rollback completes

<br>

### 2. Pattern Detection and Rollback Engine — The "Logic"

![Logic Engine](./images/logic-engine.png)

**Purpose**

The core intelligence of SHFSL 2.0. Classifies every intercepted event, assigns severity, and fires the precise automated response.

**Threat Classifications**

- `HIGH_RANSOMWARE_ROLLBACK` — file creation or modification carrying a known ransomware extension (`.lock`, `.encrypted`, `.ransom`, `.crypted`)
- `HIGH_DECOY_ALERT` — any modification or deletion of a designated DECOY file
- `HIGH_SENSITIVE_DELETION` — deletion of a SENSITIVE-classified asset

**Rollback Logic**

- Ransomware: malicious file deleted, original filename recovered by stripping the ransomware extension, latest clean snapshot restored atomically
- Decoy tamper: tampered file deleted, decoy restored from latest snapshot, `HIGH_DECOY_ALERT` dispatched
- Sensitive deletion: no auto-rollback triggered, `HIGH_SENSITIVE_DELETION` alert dispatched, snapshot held for manual administrator restoration

**Risk Scoring**

- Cumulative risk score maintained per file across all events
- Spikes on high-severity detections
- Hard cap at 100 out of 100
- Persists across sessions — giving administrators a behavioral history signal beyond individual event alerts

<br>

### 3. Versioning System — The "Snapshots"

![Versioning System](./images/versioning-system.png)

**Purpose**

Continuous, automated snapshot engine. Every clean file modification produces an immutable backup before any threat can overwrite it.

**How It Works**

- Writes a timestamped snapshot to a secured directory fully isolated from the monitored file system on every clean file modification
- Names each snapshot with millisecond precision — e.g. `Employee_List.xlsx.20260418_142328_624922`
- Explicit filter blocks temp files, Office swap files, and lock files from entering the snapshot pool
- Background pruning daemon trims snapshots to the configured `MAX_SNAPSHOTS_PER_FILE` without blocking the real-time event pipeline
- On confirmed threat detection, selects the latest clean snapshot and writes it back atomically to the original path

<br>

### 4. Decoy File System — The "Honey-Pot"

![Decoy File System](./images/decoy-filesystem.png)

**Purpose**

A strategically placed honeypot layer seeded across monitored directories to catch insider activity with zero false positives.

**Decoy Files Seeded**

- `CEO_Contract.docx`
- `API_Keys_Internal.json`
- `Finance_Report_Q3.xlsx`

**How It Works**

- No authorized user or legitimate process has any operational reason to interact with these files
- Any modification or deletion of a decoy is classified as `HIGH_DECOY_ALERT` with zero confirmation required
- Instant response: tampered file deleted, snapshot restored, live alert dispatched to administrator
- Zero false positives by design — every trigger is a confirmed breach

<br>

### 5. Administrator Module

![Administrator Module](./images/admin-module.png)

**Purpose**

Central configuration and live notification hub. Ensures the right personnel receive instant alerts on every high-severity event.

**How It Works**

- All system parameters managed through a single `config.json` — snapshot storage path, log file path, SMTP credentials
- Authenticates via Gmail App Password and dispatches HTML-formatted email alerts through SMTP
- Every alert contains the filename, event type, severity classification, action taken, and exact timestamp
- Covers three distinct alert formats — decoy tamper, ransomware detection, sensitive file deletion

<br>

### 6. Visualization and Dashboard

![Dashboard](./images/dashboard.png)

**Purpose**

Real-time administrator interface. Live visibility into every file event, threat classification, risk score, and rollback confirmation across the entire monitored file system.

**What the Dashboard Displays**

- Critical alert stream — live chronological log of all system actions, color-coded with high-visibility theming (bright pinks and yellows) for critical events
- File events and status — all creation, modification, and deletion events alongside each file's classification (DECOY, SENSITIVE, REAL)
- Restoration logs — `AUTOMATIC ROLLBACK SUCCESSFUL` confirmations on every completed recovery
- Escalation flags — events requiring mandatory manual administrator action clearly surfaced

<br>

---

<br>

## Workflow Scenarios

Full end-to-end trace of what SHFSL 2.0 does from threat entry to reversal.

<br>

### Watcher Initialization

![Watcher Active](./images/watcher.png)

**What happens at startup**

- All classified file tiers loaded into the event registry
- Watchdog observer registered recursively across the entire monitored root directory
- `is_rolling_back` flag initialized to `False`
- Real-time interception active — zero polling delay from this point

<br>

---

<br>

### Scenario 1 — Decoy File Tampered

<br>

#### Pattern Recognition

![Decoy Pattern Detection](./images/decoy-pattern.png)

**What fired**

- Insider modified `CEO_Contract.docx` — a file seeded as a DECOY
- Watcher intercepted the `FileModifiedEvent` instantly
- Logic Engine classified the event as `HIGH_DECOY_ALERT`
- Live HTML email dispatched to `vakthishree@gmail.com`

**Why this is a zero-ambiguity detection**

- No legitimate process has any operational reason to touch a decoy file
- No behavioral analysis needed — classification is immediate and final

<br>

#### Rollback Engine

![Decoy Rollback](./images/decoy-rollback.png)

**What executed**

- `is_rolling_back` flag set to `True` — Watcher silenced
- Tampered `CEO_Contract.docx` deleted from the monitored directory
- Latest clean snapshot restored atomically to the original path
- `is_rolling_back` flag reset to `False` — Watcher resumed
- Full sequence completed in milliseconds

<br>

---

<br>

### Scenario 2 — Ransomware Attack

<br>

#### Pattern Recognition

![Ransomware Pattern Detection](./images/ransom-pattern.png)

**What fired**

- Ransomware renamed `Server_Inventory.xlsx` to `Server_Inventory.lock.xlsx`
- Watcher intercepted the `FileCreatedEvent` on the renamed file
- `.lock` extension matched a known ransomware signature in the detection engine
- Event classified as `HIGH_RANSOMWARE_ROLLBACK` — highest severity level in the system
- Cumulative risk score for this file spiked to 100 out of 100
- Live alert dispatched immediately

<br>

#### Rollback Engine

![Ransomware Rollback](./images/ransom-rollback.png)

**What executed**

- `is_rolling_back` flag set to `True` — Watcher silenced
- Malicious file `Server_Inventory.lock.xlsx` deleted
- Original filename `Server_Inventory.xlsx` recovered by stripping the ransomware extension
- Latest clean snapshot restored atomically to the recovered original path
- `is_rolling_back` flag reset — Watcher resumed
- Encryption contained before it could propagate to adjacent files

<br>

---

<br>

### Scenario 3 — High Sensitivity File Deleted

<br>

#### Pattern Recognition

![Sensitive Pattern Detection](./images/sensitive-pattern.png)

**What fired**

- `Roadmap_2025.docx` deleted — pre-classified as SENSITIVE in the file registry
- Watcher intercepted the `FileDeletedEvent` instantly
- Logic Engine classified the event as `HIGH_SENSITIVE_DELETION`
- Cumulative risk score escalated to 85 out of 100
- No auto-rollback triggered — deletion may be a legitimate authorized action, human judgment preserved

<br>

#### Rollback Engine

![Sensitive File Rollback](./images/hign%20snesi%20del%20rollback.png)

**What executed**

- No automated file restoration fired
- `HIGH_SENSITIVE_DELETION` alert dispatched immediately to the administrator
- Clean versioned snapshots of `Roadmap_2025.docx` held in secured snapshot storage
- Event flagged for mandatory administrator review and manual restoration approval

<br>

---

<br>

## Versioning System — Snapshot Evidence

<br>

### Decoy File Recovery

![Decoy Recovery Snapshots](./images/decoy-recovery.png)

**What the snapshot directory confirmed**

- Multiple immutable versioned copies of `CEO_Contract.docx` present in the secured storage directory
- Each copy timestamped to the millisecond
- Latest clean snapshot confirmed as the restored version
- Proof that rollback executed correctly to the last trusted state

<br>

### Ransomware File Recovery

![Ransomware Recovery Snapshots](./images/ransom-recovery.png)

**What the snapshot directory confirmed**

- Ransomware-renamed `Server_Inventory.lock.xlsx` captured in the snapshot sequence
- Immediately followed by two clean versioned copies of `Server_Inventory.xlsx`
- Confirms correct filename recovery and successful rollback execution
- Chronological order validates the full detection-to-restoration pipeline

<br>

### Sensitive File Recovery

![Sensitive File Recovery Snapshots](./images/sensitive-recovery.png)

**What the snapshot directory confirmed**

- Two clean immutable versioned copies of `Roadmap_2025.docx` held in snapshot storage
- Both available for manual restoration upon administrator approval
- Millisecond-precision timestamps confirm capture occurred before the deletion event

<br>

---

<br>

## Decoy File System — Honey-Pot Layer

![Decoy System](./images/decoy-system.png)

**Decoy files seeded across monitored directories**

- `CEO_Contract.docx`
- `API_Keys_Internal.json`
- `Finance_Report_Q3.xlsx`

**Detection logic**

- No authorized user or legitimate process has any reason to touch these files
- Any interaction — modification or deletion — is unambiguous evidence of insider or malicious activity
- Classification fires as `HIGH_DECOY_ALERT` with no further confirmation required

**Response pipeline**

- Tampered file deleted immediately
- Decoy restored from latest clean snapshot
- Live HTML email alert dispatched to administrator
- Full incident logged in the dashboard event stream
- Zero false positives by design — every trigger is a confirmed breach

<br>

---

<br>

## Administrator Module — Live Alerts

<br>

### Alert Contents — Every High-Severity Event

- Filename involved
- Event type and severity classification
- Action taken by the system
- Exact timestamp down to the millisecond

<br>

### Decoy Tamper Alert

![Decoy Alert Email](./images/decoy-alert.png)

- Confirms the honeypot file that was touched
- Confirms the `HIGH_DECOY_ALERT` classification
- Confirms automatic rollback was already executed before the alert arrived

<br>

### Ransomware Detection Alert

![Ransomware Alert Email](./images/ransom-alert.png)

- Confirms the ransomware-named file that was detected
- Confirms the `HIGH_RANSOMWARE_ROLLBACK` classification
- Confirms successful file restoration to the original clean state

<br>

### Sensitive File Deletion Alert

![Sensitive Alert Email](./images/sensitive-alert.png)

- Confirms the SENSITIVE file that was deleted
- Confirms the `HIGH_SENSITIVE_DELETION` classification
- Explicitly prompts the administrator for manual review and restoration approval

<br>

---

<br>

## Visualization and Dashboard

<br>

### Live Activity Stream

![Live Dashboard Activity](./images/live-activity.png)

- Rotating chronological log of all system events
- Every file event, threat classification, risk score update, and rollback confirmation displayed in real time
- High-visibility color coding — bright pink and yellow theming for critical events

<br>

### Decoy Events

![Decoy Events Dashboard](./images/decoy-events.png)

- Every honeypot tamper event logged instantly
- `HIGH_DECOY_ALERT` classification displayed alongside automatic rollback confirmation
- Flagged in maximum-visibility color theming

<br>

### Ransomware Detection

![Ransomware Detection Dashboard](./images/ransomware-detection.png)

- Malicious file extension event displayed in real time
- Recovered original filename shown alongside the ransomware-named file
- `AUTOMATIC ROLLBACK SUCCESSFUL` confirmation prominently displayed

<br>

### Sensitive File Alerts

![Sensitive Alerts Dashboard](./images/sensitive-dashboard.png)

- `HIGH_SENSITIVE_DELETION` event flagged for mandatory human review
- Full incident log preserved in the event stream
- Escalation status clearly surfaced to the administrator

<br>

---

<br>

## Threat Response Reference

| Threat | Detection Method | Automated Response | Administrator Alert |
|---|---|---|---|
| Ransomware | `.lock` `.encrypted` `.ransom` `.crypted` extension detection | Malicious file deleted, original filename recovered, latest clean snapshot restored atomically | Yes — with rollback confirmation |
| Decoy Tamper | Any interaction with a DECOY-classified file | Decoy deleted, snapshot restored immediately | Yes — highest priority |
| Sensitive Deletion | Deletion of a SENSITIVE-classified asset | No auto-rollback, snapshot preserved for manual restoration | Yes — prompts human review |

<br>

---

<br>

## Adaptive Risk Scoring

- Every monitored file carries a cumulative risk score that builds across events
- Score spikes on high-severity detections — `HIGH_RANSOMWARE_ROLLBACK` pushes to 100, `HIGH_SENSITIVE_DELETION` to 85
- Hard cap at 100 out of 100
- Persists across the session as a per-file behavioral signal
- Helps surface files and directories being repeatedly targeted beyond individual event-level alerts

<br>

---

<br>

## Tech Stack

| Layer | Technology |
|---|---|
| File Event Monitoring | Python `watchdog` library |
| Pattern Detection Engine | Custom rule-based classifier |
| Snapshot and Versioning | Python file system operations, millisecond-precision timestamps |
| Email Alerting | Authenticated SMTP via Gmail App Password |
| Live Dashboard | Streamlit with high-contrast severity theming |
| System Configuration | Single `config.json` |

<br>

---

<br>

## Future Enhancements

- **ML-based Threat Detection** — replace fixed rules with trained models capable of recognizing novel and zero-day attack patterns
- **Blockchain Snapshot Storage** — store rollback history on an immutable blockchain ledger for tamper-proof auditability
- **Cloud Integration** — extend snapshot storage to AWS S3, Azure Blob, and GCP Cloud Storage for distributed environments
- **Cross-Platform Support** — expand from Linux to Windows NTFS and macOS HFS+ file systems
- **User Behavior Analytics (UBA)** — track per-user file access patterns to detect insider threats through behavioral deviation
- **Automated Incident Response** — trigger predefined containment actions (directory isolation, process kill) without waiting for manual approval

<br>

---

<br>

## References

1. Python Watchdog Library Documentation — https://python-watchdog.readthedocs.io
2. "File System Snapshot and Rollback Mechanisms in Modern Operating Systems," IEEE Transactions on Computers, 2021
3. "Ransomware Detection using Honeypot-based File Integrity Monitoring," International Journal of Cyber Security and Digital Forensics, 2022
4. "Design and Implementation of Self-Healing Systems," ACM Computing Surveys, 2020
5. GitHub repositories — watchdog, rsync, Timeshift

<br>

---

<br>

<div align="center">

*Security should not just detect damage. It should undo it.*

<br>

**SHFSL 2.0** — Niral Thiruvizha 3.0 Submission

</div>
