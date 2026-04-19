# SHFSL 2.0 — Self Healing File System Layer
**Intercept. Detect. Rollback. Zero-latency file protection with live Streamlit visualization.**

<br>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Watchdog](https://img.shields.io/badge/Watchdog-Real--Time-00C896?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

<br>

**The Unsolved Problem in File Integrity Protection:**

Modern data protection systems are designed to detect and log security events, not to reverse their impact. Once an attack reaches the file system, whether through ransomware or malicious insider activity, damage is often already in progress or completed.

The core limitations of existing systems are:

**Detection Without Action:**
Security tools such as antivirus software, EDR systems, and firewalls are effective at identifying intrusions and generating alerts, but they typically do not provide mechanisms to restore affected data states after compromise.

**Backup Latency Gap:**
Traditional backup systems operate on scheduled intervals. Any changes made between backup cycles are not recoverable if a destructive event occurs within that window.

**Passive File System Behavior:**
Conventional file systems execute file operations without contextual awareness, treating all write and delete operations equally, which allows malicious processes to overwrite or destroy valid data without intervention.

**Insider Threat Limitations:**
Authorized users can perform destructive actions using valid credentials. Such operations often bypass traditional detection systems until after data loss has already occurred.

**Solution Overview:**


The Self-Healing File System Layer (SHFSL 2.0) is a proactive, user-space security daemon designed to transform a passive file system into an active, self-defending infrastructure. Unlike traditional reactive security, this system focuses on immediate restoration of data integrity the moment a threat is identified.

The system operates through four core technical pillars:

**Real-Time Event Interception:** Utilizing a high-performance watchdog mechanism, the system monitors every file event—creation, modification, move, or deletion—across protected directories with zero-latency overhead.

**Intelligent Signature Analysis:** Instead of relying on broad heuristic scans, every event is filtered through a specialized logic engine that identifies specific malicious behaviors:

**Ransomware Fingerprinting:** Detection of unauthorized file extension changes and rapid patterns of encryption.

**Decoy/Honeypot Triggers:** Monitoring "trap" files that, if touched, provide unambiguous proof of an intrusion or insider threat.

**Sensitive Asset Protection:** Identifying the targeted removal or tampering of critical system and project files.

**Immutable Versioning & Rollback:** The system maintains a secure, isolated snapshot directory. When a threat is detected, the compromised file is instantly purged and replaced with its most recent "clean" version, ensuring that the window of data loss is near-zero.

**Live Visualization & Alerting:** A centralized dashboard provides a real-time heatmap of file system health, while an automated administrative module dispatches high-priority SMTP alerts to ensure the security team is fully informed while the system heals itself.

**Overall System Architecture**


<img width="966" height="806" alt="Screenshot 2026-04-18 214118" src="https://github.com/user-attachments/assets/316e8fcc-6a66-403a-8a13-c707a8405a8f" />

The system utilizes a high-speed Watchdog Monitor to intercept real-time I/O events, passing them through an Intelligence Core that identifies ransomware and insider threats.

Detected anomalies trigger the Rollback Engine, which instantly restores compromised data using timestamped snapshots from a secured Immutable Protection Vault.

A centralized Streamlit Command Center provides live threat telemetry and risk scoring, while the SMTP Module ensures immediate administrative escalation.


**System Modules**


**1. File System Monitor — The "Watcher"**

**Core Function:**
The Watcher is the first layer of SHFSL 2.0, built to observe file system activity as it happens rather than after the fact. It runs continuously over all monitored directories, capturing every file operation in real time. Creation, modification, deletion, and movement events are intercepted immediately and forwarded for analysis, allowing the system to respond to suspicious behavior without delay, including ransomware-style activity.

**Operational Flow**

**Step 1: Continuous Event Listening**

The Watcher operates as a persistent listener on the file system event stream. Instead of actively scanning files, it passively receives OS-level notifications whenever a file operation occurs.

**Step 2: Event Capture**

On every file interaction, the Watcher extracts structured metadata including:

File path
Operation type (create, modify, delete, move)
Timestamp
Source and destination (if applicable)

**Step 3: Noise Filtering**

A filtering layer removes non-critical system activity such as temporary files, cache updates, and background application artifacts. This ensures only meaningful events are processed downstream.

**Step 4: Rollback State Awareness**

During active recovery operations, a system flag (`is_rolling_back`) temporarily disables event propagation. This prevents restoration actions from being misinterpreted as new file system attacks.

**Step 5: Event Forwarding**

Validated events are immediately forwarded to the Logic Engine for threat classification and response execution. This handoff is designed for minimal latency to enable near-instant reaction.

**Example Scenario**

If a ransomware process renames `Financial_Records.xlsx` to `Financial_Records.xlsx.enc`:

The Watcher detects the file move event in real time
The `.enc` extension is flagged as a high-risk pattern
Event metadata is forwarded to the Logic Engine
The system triggers rollback using the latest immutable snapshot, restoring the original file before encryption propagates

**Architecture:**
<img width="475" height="694" alt="Screenshot 2026-04-18 204329" src="https://github.com/user-attachments/assets/8a5a31e1-8b43-4f8a-8500-21bbe98efff7" />

**Pattern Detection & Rollback Engine (The "Logic")**

**Core Function:**
The Logic Engine is the brain of SHFSL 2.0. It reads the live event stream from the Watcher to tell apart normal user activity from a real attack. The moment a threat is confirmed, it acts immediately — neutralizing the damage and restoring the file without waiting for anyone to step in.

**Operation:**

**1. Decoy Monitoring (The Honeypot Trap)**

**Pattern Recognition**

Any modification or deletion of a honeypot file is instantly classified as `HIGH_DECOY_ALERT`.
Since no legitimate user has any reason to touch these files, every trigger is a confirmed breach with zero false positives.

**Rollback Engine**

The tampered decoy is immediately deleted.
The clean original is restored from the latest immutable snapshot.
A high-priority alert email is dispatched to the administrator in real time.
Monitoring resumes automatically once the restore is complete.

**Example**
A script scanning all folders stumbles onto a hidden decoy file. The engine catches the touch, removes the threat, and replaces the decoy instantly — before the script can move further.

**2. Ransomware Detection (Pattern Matching)**

**Pattern Recognition**

Any file created or modified carrying a known ransomware extension — `.lock`, `.encrypted`, `.ransom`, `.crypted` — is instantly classified as `HIGH_RANSOMWARE_ROLLBACK`.
The engine also catches mid-name injections like `report.lock.xlsx`, not just trailing extensions.

**Rollback Engine**

The ransomware-named file is immediately deleted.
The original filename is recovered by stripping the malicious extension — `report.xlsx.lock` becomes `report.xlsx`.
The clean version is restored from the latest snapshot to the recovered path.
A specialized flag silences the Watcher during the restore to prevent a cascading false-event loop.

**Example**
Ransomware renames a file to `Final_Thesis.pdf.crypt`. The engine spots the extension, deletes the encrypted version, and recovers the original PDF in milliseconds — before the attack can reach the next file.

**3. High-Sensitivity Deletion Guard (Asset Protection)**

**Pattern Recognition**

Any deletion of a file on the protected list is instantly classified as `HIGH_SENSITIVE_DELETION`.
Because a deletion might be intentional, the engine treats this with caution rather than acting automatically.

**Rollback Engine**

No automatic rollback is triggered, to avoid interfering with legitimate user actions.
A `HIGH_SENSITIVE_DELETION` alert is dispatched to the administrator immediately.
Clean versioned snapshots remain preserved in storage, ready for manual restoration upon administrator approval.

**Example**
A user accidentally deletes a core database file. The system holds back from forcing it back immediately but fires an emergency alert to the administrator, who can restore it from the snapshot vault with a single action.

**Architecture:**
<img width="739" height="695" alt="Screenshot 2026-04-18 211510" src="https://github.com/user-attachments/assets/d616d200-b8ff-41af-9043-5726b8b389ee" />

**Versioning System (The "Snapshots")**

**Core Function**

The Snapshot system is the memory of SHFSL 2.0. Every time a monitored file is modified, an exact copy of its clean state is captured and locked away in a secured, isolated directory — completely separate from the files being watched. Unlike scheduled backups that run once a day and can miss hours of clean work, snapshots are taken continuously, at the exact moment a clean version exists.

**Operation: Stability & Efficiency**

**Decoy File**

A fresh snapshot is written every time the decoy is modified, keeping the vault stocked with the latest clean version of the trap at all times.
Since no legitimate process touches decoy files, the snapshot pool stays minimal and uncluttered — every version in it is a verified clean state.
Older decoy snapshots are pruned automatically once the version limit is hit, keeping storage lean without any manual intervention.

**Ransomware File**

A new timestamped snapshot is captured on every clean modification, ensuring the vault always holds the most recent safe version before any encryption attempt lands.
Temp files and lock files generated during ransomware activity are explicitly filtered out, so only genuine clean states enter the snapshot pool.
Once the version limit is reached, the oldest snapshots are rotated out in a background thread — the real-time pipeline is never blocked or slowed during cleanup.

**Sensitive File**

Every modification produces a new versioned snapshot, building a full chronological history of the file's clean states over time.
Multiple versions are retained up to the configured maximum, giving the administrator a range of clean restore points to choose from — not just the latest one.
Pruning runs silently in the background, archiving older versions automatically so storage stays optimized without administrator involvement.

**Example**
`Server_Inventory.xlsx` is modified three times by a legitimate user, with each change producing a new timestamped snapshot silently archived in the vault. When ransomware renames it to `Server_Inventory.xlsx.lock`, the Rollback Engine pulls the most recent clean copy, deletes the malicious file, and restores the original in milliseconds — as if the attack never happened.

**Architecture:**
<img width="471" height="613" alt="Screenshot 2026-04-18 213421" src="https://github.com/user-attachments/assets/03c213d9-cda6-4230-9367-1350b92c51db" />


**4. Decoy File System (The "Honeypot")**

**Core Function**
The Decoy File System is the tripwire of SHFSL 2.0. Honeypot files with names that mimic real critical assets — `CEO_Contract.docx`, `API_Keys_Internal.json`, `Finance_Report_Q3.xlsx` — are planted across monitored directories. They serve no operational purpose whatsoever. Their only job is to get touched, because anyone who does is immediately confirmed as a threat.

**Operation**

**Zero Ambiguity**

Since no legitimate user or authorized process has any reason to interact with a decoy, any modification or deletion is treated as a confirmed breach — no further verification needed.

**Instant Classification**

The moment a decoy is touched, the event is instantly classified as `HIGH_DECOY_ALERT` — the highest confidence threat classification in the system.

**Automated Recovery**

An automated rollback fires immediately, restoring the decoy to its original state and resetting the trap for the next attempt.

**Example**

**Scenario**
An insider with valid credentials begins scanning the monitored directory, looking for sensitive documents to exfiltrate.

**Trigger**
They open and modify `CEO_Contract.docx` — a decoy file planted specifically to catch this behavior.

**Detection**
The Watcher intercepts the modification instantly and classifies it as `HIGH_DECOY_ALERT` with zero ambiguity.

**Response**
The tampered file is deleted, the clean original is restored from the latest snapshot, and a high-priority alert is dispatched to the administrator — all within milliseconds, before the insider can reach another file.

**Architecture:**
<img width="425" height="768" alt="Screenshot 2026-04-18 213605" src="https://github.com/user-attachments/assets/9146505e-c088-41ac-bb69-1b145f817b56" />

**Administrator Module**

**Core Function**
The Administrator Module is the communication hub of SHFSL 2.0. While the rest of the system operates autonomously, this module ensures the right person is informed the moment something critical happens — delivering precise, actionable alerts so the administrator is never left in the dark, regardless of where they are.

**Operation**

**Instant Alerting**

Every high-severity event — ransomware detection, decoy tampering, or sensitive file deletion — triggers an immediate alert routed directly to the configured administrator.

**Non-Blocking Delivery**

Alerts are dispatched in a background thread so email sending never blocks or slows down the real-time event pipeline.

**Centralized Configuration**

The entire system is controlled through a single `config.json` file, covering snapshot storage paths, log file paths, and all email routing parameters.

**Example**

**Scenario**
Ransomware begins encrypting files in the monitored directory late at night with no one at the terminal.

**Trigger**
`Server_Inventory.xlsx` is renamed to `Server_Inventory.xlsx.lock` — classified instantly as `HIGH_RANSOMWARE_ROLLBACK`.

**Response**
The Rollback Engine deletes the malicious file and restores the clean original from the snapshot vault. Simultaneously, a formatted HTML alert is dispatched to the administrator's email — carrying the filename, threat type, action taken, and timestamp — ensuring they are informed and can verify the recovery the moment they check their inbox.

**Architecture**
<img width="846" height="755" alt="Screenshot 2026-04-18 213713" src="https://github.com/user-attachments/assets/4d64b3b8-f01c-4a1d-9ee2-75b3a62eae81" />

**Visualization & Dashboard Layer**

**Core Function**
The Dashboard is the control room of SHFSL 2.0. Every detection, rollback, and alert that happens silently under the hood is surfaced here in real time — giving the administrator a live, visual overview of everything the system is doing. Nothing happens in the dark.

**Operation**

**Live Auto-Refresh**

A live Streamlit interface auto-refreshes every two seconds, pulling the latest event data from the watcher log and activity log without any manual input.

**Real-Time Event Tracking**

Every file event — created, modified, or deleted — appears in the live grid alongside its classification, risk outcome, and current risk score.

**Dynamic Severity Awareness**

The dashboard reads severity directly from the most recent log entries and adjusts the alert banner at the top of the page accordingly — from a steady green for all-clear to a flashing red for a confirmed breach.

**Example**

**Scenario**
Ransomware begins renaming files in the monitored directory during off-hours with no one at the terminal.

**Trigger**
`Server_Inventory.xlsx` is renamed to `Server_Inventory.xlsx.lock` — classified instantly as `HIGH_RANSOMWARE_ROLLBACK`.

**Response**
The alert banner shifts to flashing red, the live grid updates with the malicious filename highlighted in deep red, the activity log prepends a confirmed rollback entry, and the ransomware counter in system metrics increments — all within the next two-second refresh cycle, giving the administrator a complete picture of exactly what happened and what the system did about it.

**Workflow**

## Watcher Initialization

<img width="924" height="241" alt="Screenshot 2025-10-11 020224" src="https://github.com/user-attachments/assets/fd5e2aa9-61ab-4a45-9b89-5dff6a9e2ff1" />

### What Happens at Startup

| Step | Action |
|------|--------|
| **Registry Load** | All classified file tiers — `DECOY`, `SENSITIVE`, and `REAL` — loaded into the event registry |
| **Observer Registration** | Watchdog observer registered recursively across the entire monitored root directory |
| **Flag Initialization** | `is_rolling_back` flag set to `False` — system ready, no active rollback in progress |
| **Live Interception** | Real-time event capture active — zero polling delay from this point forward |

### Scenario 1 — Decoy File Tampered

---

#### Pattern Recognition

**What Fired**
| Event | Detail |
|-------|--------|
| **Target File** | `CEO_Contract.docx` — classified as `DECOY` |
| **Trigger** | Watcher intercepted `FileModifiedEvent` instantly |
| **Classification** | `HIGH_DECOY_ALERT` — highest confidence threat level |
| **Alert** | Live HTML email dispatched to `vakthishree@gmail.com` |

**Why This Is a Zero-Ambiguity Detection**

No legitimate process has any operational reason to touch a decoy file.
No behavioral analysis needed — classification is immediate and final.

---

#### Rollback Engine

**What Executed**
| Step | Action |
|------|--------|
| **Silence** | `is_rolling_back` flag set to `True` — Watcher silenced |
| **Purge** | Tampered `CEO_Contract.docx` deleted from monitored directory |
| **Restore** | Latest clean snapshot restored atomically to original path |
| **Resume** | `is_rolling_back` flag reset to `False` — Watcher resumed |
| **Speed** | Full sequence completed in milliseconds |

<img width="1504" height="369" alt="Screenshot 2026-04-18 141624" src="https://github.com/user-attachments/assets/80168c1c-a499-4c46-90dc-a2a9dfdc226e" />

### Scenario 2 — Ransomware Attack

---

#### Pattern Recognition

**What Fired**
| Event | Detail |
|-------|--------|
| **Target File** | `Server_Inventory.xlsx` renamed to `Server_Inventory.lock.xlsx` |
| **Trigger** | Watcher intercepted `FileCreatedEvent` on the renamed file |
| **Signature Match** | `.lock` extension matched a known ransomware signature |
| **Classification** | `HIGH_RANSOMWARE_ROLLBACK` — highest severity level in the system |
| **Risk Score** | Cumulative risk score spiked to `100/100` |
| **Alert** | Live alert dispatched immediately |

---

#### Rollback Engine

**What Executed**
| Step | Action |
|------|--------|
| **Silence** | `is_rolling_back` flag set to `True` — Watcher silenced |
| **Purge** | Malicious file `Server_Inventory.lock.xlsx` deleted |
| **Recovery** | Original filename `Server_Inventory.xlsx` recovered by stripping ransomware extension |
| **Restore** | Latest clean snapshot restored atomically to recovered original path |
| **Resume** | `is_rolling_back` flag reset to `False` — Watcher resumed |
| **Contained** | Encryption stopped before it could propagate to adjacent files |

<img width="1458" height="356" alt="Screenshot 2026-04-18 142421" src="https://github.com/user-attachments/assets/fca5e332-65c2-4447-8ff7-85f8036b957d" />

### Scenario 3 — High Sensitivity File Deleted

---

#### Pattern Recognition

**What Fired**
| Event | Detail |
|-------|--------|
| **Target File** | `Roadmap_2025.docx` — pre-classified as `SENSITIVE` in the file registry |
| **Trigger** | Watcher intercepted `FileDeletedEvent` instantly |
| **Classification** | `HIGH_SENSITIVE_DELETION` |
| **Risk Score** | Cumulative risk score escalated to `85/100` |
| **Judgment** | No auto-rollback — deletion may be a legitimate authorized action, human judgment preserved |

---

#### Rollback Engine

**What Executed**
| Step | Action |
|------|--------|
| **No Auto-Restore** | Automated file restoration deliberately withheld |
| **Alert** | `HIGH_SENSITIVE_DELETION` alert dispatched immediately to the administrator |
| **Snapshots** | Clean versioned copies of `Roadmap_2025.docx` held securely in snapshot storage |
| **Escalation** | Event flagged for mandatory administrator review and manual restoration approval |

<img width="1447" height="194" alt="Screenshot 2026-04-18 142845" src="https://github.com/user-attachments/assets/739cb6ba-50a7-4b6a-8fca-85e3b2e376e3" />

## Versioning System — Snapshot Evidence

---

### Decoy File Recovery

<img width="1228" height="270" alt="Screenshot 2026-04-18 142045" src="https://github.com/user-attachments/assets/9117b616-7763-4eb0-839d-fc5e5d51ef5b" />

**What the Snapshot Directory Confirmed**
| Evidence | Detail |
|----------|--------|
| **Versions** | Multiple immutable versioned copies of `CEO_Contract.docx` present in secured storage |
| **Timestamps** | Each copy timestamped to the millisecond |
| **Restored From** | Latest clean snapshot confirmed as the version used for rollback |
| **Integrity** | Proof that rollback executed correctly to the last trusted state |

---

### Ransomware File Recovery

<img width="1198" height="200" alt="Screenshot 2026-04-18 142514" src="https://github.com/user-attachments/assets/d1d8bd5f-be66-4b8b-a2e2-cb6deaefb837" />

**What the Snapshot Directory Confirmed**
| Evidence | Detail |
|----------|--------|
| **Captured** | Ransomware-renamed `Server_Inventory.lock.xlsx` present in the snapshot sequence |
| **Restored** | Immediately followed by two clean versioned copies of `Server_Inventory.xlsx` |
| **Filename** | Confirms correct filename recovery — malicious extension stripped successfully |
| **Pipeline** | Chronological order validates the full detection-to-restoration sequence |

---

### Sensitive File Recovery

<img width="1205" height="112" alt="Screenshot 2026-04-18 142941" src="https://github.com/user-attachments/assets/884a10ad-dd69-440b-8f77-7c8733eb1364" />

**What the Snapshot Directory Confirmed**
| Evidence | Detail |
|----------|--------|
| **Versions** | Two clean immutable versioned copies of `Roadmap_2025.docx` held in snapshot storage |
| **Awaiting** | Both available for manual restoration upon administrator approval |
| **Timestamps** | Millisecond-precision timestamps confirm capture occurred before the deletion event |

## Administrator Module — Live Alerts

---

### Alert Contents — Every High-Severity Event

| Field | Detail |
|-------|--------|
| **File** | Filename involved in the event |
| **Classification** | Event type and severity classification |
| **Action** | Action taken by the system |
| **Timestamp** | Exact timestamp down to the millisecond |

---

### Decoy Tamper Alert
<img width="1080" height="1323" alt="honey" src="https://github.com/user-attachments/assets/ef35aa75-ce58-4b29-be31-241beab86b5d" />

| Confirmation | Detail |
|--------------|--------|
| **Target** | Honeypot file that was touched |
| **Classification** | `HIGH_DECOY_ALERT` confirmed |
| **Action** | Automatic rollback already executed before the alert arrived |

---

### Ransomware Detection Alert
<img width="1080" height="1417" alt="rans" src="https://github.com/user-attachments/assets/8c45ff0b-b1ac-459c-8f02-22c7f82950ca" />

| Confirmation | Detail |
|--------------|--------|
| **Target** | Ransomware-named file that was detected |
| **Classification** | `HIGH_RANSOMWARE_ROLLBACK` confirmed |
| **Action** | Successful file restoration to the original clean state |

---

### Sensitive File Deletion Alert
<img width="1080" height="1417" alt="rans" src="https://github.com/user-attachments/assets/d3665412-6071-442a-b047-8a74cf95163b" />

| Confirmation | Detail |
|--------------|--------|
| **Target** | `SENSITIVE` file that was deleted |
| **Classification** | `HIGH_SENSITIVE_DELETION` confirmed |
| **Next Step** | Administrator prompted for manual review and restoration approval |

## Visualization and Dashboard

---

### Live Activity Stream

<img width="1903" height="813" alt="Screenshot 2026-04-18 174657" src="https://github.com/user-attachments/assets/3bb7a7c8-2a83-40f8-952f-ac1dd316e2ea" />

| Feature | Detail |
|---------|--------|
| **Event Log** | Rotating chronological log of all system events |
| **Real-Time** | Every file event, threat classification, risk score update, and rollback confirmation displayed instantly |
| **Color Coding** | High-visibility theming — bright pink and yellow for critical events |

---

### Decoy Events

<img width="1686" height="521" alt="Screenshot 2026-04-18 174858" src="https://github.com/user-attachments/assets/f08deefe-9b82-49ee-9a54-af8306542bc4" />

| Feature | Detail |
|---------|--------|
| **Logging** | Every honeypot tamper event logged instantly |
| **Classification** | `HIGH_DECOY_ALERT` displayed alongside automatic rollback confirmation |
| **Visibility** | Flagged in maximum-visibility color theming |

---

### Ransomware Detection
<img width="1650" height="191" alt="Screenshot 2026-04-18 175107" src="https://github.com/user-attachments/assets/1b5fd569-fa39-4398-9c5c-f8c4c2227e02" />

| Feature | Detail |
|---------|--------|
| **Real-Time** | Malicious file extension event displayed the moment it is intercepted |
| **Recovery** | Recovered original filename shown alongside the ransomware-named file |
| **Confirmation** | `AUTOMATIC ROLLBACK SUCCESSFUL` prominently displayed |

---

### Sensitive File Alerts
<img width="1654" height="320" alt="Screenshot 2026-04-18 175223" src="https://github.com/user-attachments/assets/5dd66d3a-e964-4602-878f-496981a5d2d5" />

| Feature | Detail |
|---------|--------|
| **Flag** | `HIGH_SENSITIVE_DELETION` event flagged for mandatory human review |
| **Log** | Full incident log preserved in the event stream |
| **Escalation** | Escalation status clearly surfaced to the administrator |

## Threat Response Reference

| Threat | Detection Method | Automated Response | Administrator Alert |
|---|---|---|---|
| **Ransomware** | `.lock` `.encrypted` `.ransom` `.crypted` extension detection | Malicious file deleted, original filename recovered, latest clean snapshot restored atomically | Yes — with rollback confirmation |
| **Decoy Tamper** | Any interaction with a `DECOY`-classified file | Decoy deleted, snapshot restored immediately | Yes — highest priority |
| **Sensitive Deletion** | Deletion of a `SENSITIVE`-classified asset | No auto-rollback, snapshot preserved for manual restoration | Yes — prompts human review |

<br>

---

<br>

## Adaptive Risk Scoring

Every monitored file carries a cumulative risk score that builds across events.
Score spikes on high-severity detections — `HIGH_RANSOMWARE_ROLLBACK` pushes to 100, `HIGH_SENSITIVE_DELETION` to 85.
Hard cap at 100 out of 100.
Persists across the session as a per-file behavioral signal.
Helps surface files and directories being repeatedly targeted beyond individual event-level alerts.

<br>

---

<br>

## Tech Stack

| Layer | Technology |
|---|---|
| **File Event Monitoring** | Python watchdog library |
| **Pattern Detection Engine** | Custom rule-based classifier |
| **Snapshot and Versioning** | Python file system operations, millisecond-precision timestamps |
| **Email Alerting** | Authenticated SMTP via Gmail App Password |
| **Live Dashboard** | Streamlit with high-contrast severity theming |
| **System Configuration** | Single `config.json` |

<br>

---

<br>

## Future Enhancements

**ML-based Threat Detection** — replace fixed rules with trained models capable of recognizing novel and zero-day attack patterns
**Blockchain Snapshot Storage** — store rollback history on an immutable blockchain ledger for tamper-proof auditability
**Cloud Integration** — extend snapshot storage to AWS S3, Azure Blob, and GCP Cloud Storage for distributed environments
**Cross-Platform Support** — expand from Linux to Windows NTFS and macOS HFS+ file systems
**User Behavior Analytics (UBA)** — track per-user file access patterns to detect insider threats through behavioral deviation
**Automated Incident Response** — trigger predefined containment actions (directory isolation, process kill) without waiting for manual approval

## Author

Built by **Shree vakthi** as a security research project.
