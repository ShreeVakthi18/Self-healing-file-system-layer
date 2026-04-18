# 🛡️ SHFSL 2.0 — Self-Healing File System Layer

> **The file system doesn't just get attacked. With SHFSL 2.0, it fights back.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

---

## 🔥 The Problem Nobody Solved

### Security tools detect. They do not heal.

Every organisation deploys firewalls, antivirus software, and access control lists as their primary defence. These tools are built to watch and warn — not to undo what has already been done. When an attack succeeds, the alert fires and the damage stays.

### The two attacks that break every existing defence

**Ransomware** moves faster than any scheduled backup. An entire directory can be encrypted and renamed within 60 seconds. By the time the antivirus alert surfaces, every file in the folder is already locked behind an encryption key the organisation does not hold.

**Insider threats** are worse. A privileged employee with valid credentials does not trigger a single security rule. They open a folder, delete the files, and walk away. The system logs the action. The data is gone. The log changes nothing.

### The gap at the foundation

The file system is the most fundamental layer of any computing environment — and it has zero native ability to recognise a threat, classify it, and autonomously recover from it. Every tool built on top of it inherits that same limitation. Damage is recorded. It is never undone.

> **SHFSL 2.0 was built to close that gap — not by detecting better, but by healing automatically.**

---

## ⚡ What SHFSL 2.0 Does

### The core idea

SHFSL 2.0 operates as a silent user-space daemon running directly beneath the file system — no kernel modifications, no elevated system privileges, no changes to existing infrastructure. It sits and watches. The moment anything happens to any file, it intercepts the event, classifies the threat, and fires the right response — all before the damage can propagate.

### Three threats. Three automated outcomes.

| Threat | How It's Detected | What Happens |
|---|---|---|
| 🔴 **Ransomware** | `.lock` `.encrypted` `.ransom` `.crypted` extension on any file | Malicious file deleted instantly, original filename recovered, clean version restored from snapshot |
| 🟠 **Insider Activity** | Any interaction with a seeded decoy honeypot file | File restored from snapshot, administrator alerted — zero false positives by design |
| 🟡 **Sensitive Deletion** | Deletion of any file classified as SENSITIVE | No auto-rollback, administrator escalated immediately, clean snapshots held ready for human decision |

### What makes it different

Every existing tool stops at the alert. SHFSL 2.0 goes one step further — it **reverses the damage**. Ransomware-encrypted files are restored. Tampered honeypots are recovered. Sensitive deletions are escalated with clean snapshots ready. Every single action — detection, rollback, alert — is surfaced live on a real-time dashboard. Nothing happens in the dark.

---

## 🏗️ Overall Architecture

> `![Overall Architecture](images/overall_architecture.png)`

### How the system flows end-to-end

**Event Interception** — Any user interaction with the file system — creation, modification, deletion, or move — is intercepted by the File System Monitor the exact millisecond it occurs.

**Threat Classification** — The intercepted event flows directly into the Pattern Detection & Rollback Engine, where it is evaluated against all three threat signatures simultaneously. Every event gets a classification and a risk score update.

**Automated Response** — On threat confirmation, the Versioning System provides the latest clean immutable snapshot. The Rollback Engine writes it back to the original path atomically. For sensitive deletions, the escalation path fires instead and the snapshot is held for administrator decision.

**Live Visibility** — Every action — detection, rollback, escalation — is surfaced immediately on the live Streamlit dashboard and delivered to the administrator via HTML email alert. The loop is continuous across every monitored directory, every second.

---

## 🔩 Modules Architecture

> `![Modules Architecture](images/modules_architecture.png)`

SHFSL 2.0 is built across **six tightly integrated modules** — each with a precise responsibility, together forming one unbroken self-healing pipeline.

---

### 📡 Module 1 — File System Monitor *(The "Watcher")*

> `![Watcher Architecture](images/module_watcher.png)`

**What it does**

A persistent watchdog-based observer that registers against every monitored directory recursively and stays alive continuously — no polling, no delay, no gaps. Intercepts all four event types — **creation, modification, deletion, and move** — the instant they occur.

**How it stays clean**

Every event passes through a noise filter that strips temp files, Office swap files, and internal system artefacts before anything reaches the detection engine. A critical `is_rolling_back` flag cuts the Watcher completely silent during any active restore — ensuring the rollback operation itself never generates cascading false events.

**File classification at startup**

All file tiers — **DECOY, SENSITIVE, REAL** — are pre-loaded into the event registry at startup, so every event is contextualised from the very first millisecond of operation.

---

### 🧠 Module 2 — Pattern Detection & Rollback Engine *(The "Logic")*

> `![Pattern Detection & Rollback Architecture](images/module_pattern_rollback.png)`

**The brain of the system**

Every event the Watcher intercepts flows directly here and is classified in real time against three threat signatures. Each classification maps to a precision automated response — no guessing, no delay, no human required.

**① Ransomware Pattern → `HIGH_RANSOMWARE_ROLLBACK`**

Any file carrying `.lock`, `.encrypted`, `.ransom`, or `.crypted` is flagged immediately. The malicious file is deleted, the original filename is recovered by stripping the ransomware extension, and the latest clean snapshot is restored atomically. Risk score spikes to **100/100**.

**② Decoy Honeypot Tampering → `HIGH_DECOY_ALERT`**

Any modification or deletion of a designated decoy file is treated as definitive evidence of insider activity — no further confirmation required. The honeypot is instantly restored from its latest snapshot and a high-priority alert is dispatched to the administrator.

**③ Sensitive File Deletion → `HIGH_SENSITIVE_DELETION`**

No auto-rollback — the deletion may be legitimate, and human judgment must decide. The system escalates immediately to the administrator, holds clean snapshots ready, and preserves the decision for the appropriate person.

**Cumulative risk scoring**

Every confirmed threat updates the file's cumulative risk score — a persistent per-file behavioural signal that builds across events and caps at 100, giving the administrator a running history of each file's threat activity.

---

### 🗄️ Module 3 — Versioning System *(The "Snapshots")*

> `![Versioning System Architecture](images/module_versioning.png)`

**Continuous immutable versioning**

Every clean file modification triggers an immediate, immutable, timestamped snapshot written to a secured directory fully isolated from the monitored file system. Unlike scheduled backups, snapshots are captured at the exact moment a clean version exists — not on a timer.

**Snapshot naming and ordering**

Snapshots are named with millisecond precision — e.g. `Employee_List.xlsx.20260418_142328_624922` — making every version uniquely identifiable and chronologically ordered without any ambiguity.

**What gets excluded**

Temp files, swap files, and lock files are explicitly excluded from the snapshot pool. Only verified clean states ever enter storage.

**Pruning and rollback**

Pruning runs in a dedicated background daemon thread, retaining only the most recent `MAX_SNAPSHOTS_PER_FILE` versions per file without ever touching the live event pipeline. On rollback confirmation, the latest clean snapshot is written back to the original path atomically and instantly — as if the malicious event never occurred.

---

### 🍯 Module 4 — Decoy File System *(The "Honey-pot")*

> `![Decoy File System Architecture](images/module_decoy.png)`

**The tripwire layer**

Strategically named honeypot files are seeded across monitored directories, designed to look indistinguishable from real critical assets — `CEO_Contract.docx`, `API_Keys_Internal.json`, `Finance_Report_Q3.xlsx`. These files serve zero operational purpose — no authorised user, no legitimate process, has any reason to interact with them.

**Why it gives zero false positives**

Any interaction is unambiguous by design. No threshold, no confirmation window, no pattern matching required — the interaction itself is the proof. The moment a decoy is touched, `HIGH_DECOY_ALERT` fires, the tampered file is deleted, the clean version is restored from the latest snapshot, and a live HTML email alert is dispatched — all within milliseconds.

---

### 🔔 Module 5 — Administrator Module

> `![Administrator Module Architecture](images/module_admin.png)`

**Centralised configuration**

All system parameters — snapshot storage path, log file path, sender email, receiver email, SMTP credentials — are controlled through a single `config.json` file for rapid deployment and zero-friction configuration changes.

**Alert delivery**

On every high-severity event, the system authenticates immediately via SMTP and dispatches a formatted HTML email alert containing the filename, event type, action taken, and exact timestamp. Alert delivery confirmed across all three threat types — decoy tampering, ransomware detection, and sensitive file deletion — with the administrator notified within seconds regardless of physical location.

---

### 📊 Module 6 — Visualization & Dashboard

> `![Dashboard Architecture](images/module_dashboard.png)`

**Live threat visibility**

A live Streamlit dashboard built with high-contrast dynamic theming — colour-coded by severity so critical events are impossible to miss the moment they appear. Every file event across all monitored directories is displayed alongside its classification (DECOY / SENSITIVE / REAL) and live cumulative risk score.

**What the administrator sees**

Every threat detection appears with its severity label and classification. Every rollback confirmation shows `AUTOMATIC ROLLBACK SUCCESSFUL` immediately after recovery. Every administrator escalation is flagged with a manual action required indicator. Ransomware detections, decoy breaches, and sensitive deletions each have their own dedicated live activity stream.

---

> 🔁 **Pipeline: Watcher → Logic → Snapshots → Honey-pot → Admin → Dashboard — every file, every second, without interruption.**

---

## 🔄 Detailed Workflow

---

### Step 1 — File Monitoring

> `![Step 1 - File Monitoring](images/step1_monitoring.png)`

**System Startup**

The File System Monitor activates the moment SHFSL 2.0 starts. All classified file tiers — DECOY, SENSITIVE, and REAL — are loaded into the event registry before a single event is processed.

**Active Interception**

The Watcher registers recursively against the monitored root directory. Every subdirectory is covered automatically. Every file event — creation, modification, deletion, move — is intercepted with zero polling delay.

**Noise Filtering**

Every intercepted event is passed through the ignore layer before it reaches the detection engine. Temp files, Office swap files, lock files, and internal system artefacts are silently dropped. Only real, meaningful events move forward.

**Rollback Guard**

The `is_rolling_back` flag ensures the Watcher goes completely silent during any active restore. The rollback operation itself never generates false cascading events. Monitoring resumes automatically the moment recovery completes.

---

### Step 2 — Pattern Recognition & Rollback Engine *(Decoy / Ransomware / Sensitive Detection)*

> `![Step 2 - Ransomware Detection](images/step2_ransomware.png)`

#### 🔴 Ransomware Detection & Rollback

**Detection**

When a file arrives carrying a known ransomware extension — `.lock`, `.encrypted`, `.ransom`, or `.crypted` — the Logic Engine classifies it as `HIGH_RANSOMWARE_ROLLBACK` immediately. No further confirmation is needed.

**What the engine does**

The malicious file is deleted from the monitored directory instantly. The original filename is recovered by stripping the ransomware extension from the file name. The Rollback Engine locates the latest clean snapshot from isolated versioning storage and writes it back to the original path atomically.

**Risk scoring**

The file's cumulative risk score spikes to **100/100**. The `is_rolling_back` flag silences the Watcher for the entire duration of the restore. Monitoring resumes the moment recovery completes.

**Live result**

`Server_Inventory.lock.xlsx` was detected the instant it appeared. The original `Server_Inventory.xlsx` was recovered. The entire sequence — detection, deletion, filename recovery, snapshot restore — completed in milliseconds.

> `![Step 2 - Decoy Detection](images/step2_decoy.png)`

#### 🟠 Decoy Honeypot Detection & Rollback

**Detection**

When any file classified as DECOY is modified or deleted, the Logic Engine classifies the event as `HIGH_DECOY_ALERT` immediately. The interaction alone is the proof — no authorised user or legitimate process has any reason to touch a decoy file.

**What the engine does**

The tampered or deleted decoy file is purged immediately. The Rollback Engine restores it from the latest clean snapshot. A high-priority HTML email alert is dispatched to the administrator in parallel with the restore.

**Live result**

`CEO_Contract.docx` — a honeypot seeded to mimic a real critical asset — was modified by a simulated insider. Classification, rollback, and alert all completed in milliseconds. Zero false positives by design.

> `![Step 2 - Sensitive Detection](images/step2_sensitive.png)`

#### 🟡 Sensitive File Deletion — Escalation Path

**Detection**

When a file classified as SENSITIVE is deleted, the Logic Engine classifies the event as `HIGH_SENSITIVE_DELETION`. This is the only path in the system that deliberately does not trigger an automatic rollback.

**Why no auto-rollback**

The deletion may be a legitimate operation performed by an authorised user. Autonomously overwriting that decision could cause more harm than the deletion itself. Human judgment is preserved exactly where it matters most.

**What the engine does**

The event is escalated to the administrator immediately via a live HTML email alert. The file's cumulative risk score is updated — it reached **85/100** in the live test for `Roadmap_2025.docx`. All clean snapshots are held ready in isolated storage for manual restoration on administrator approval.

---

### Step 3 — Version Recovery *(Snapshots for All Cases)*

> `![Step 3 - Decoy Snapshots](images/step3_snapshots_decoy.png)`

#### 🍯 Decoy Case — Snapshot Evidence

**What the snapshot directory shows**

Multiple immutable versioned copies of `CEO_Contract.docx` are confirmed in snapshot storage, each timestamped to the millisecond. Every time the decoy existed in a clean state, a snapshot was captured.

**How rollback used them**

The moment the honeypot tamper event fired, the Rollback Engine pulled the latest of these copies and restored it to the original path instantly. Clean states remain available for every future trigger on this file, with no additional configuration needed.

> `![Step 3 - Ransomware Snapshots](images/step3_snapshots_ransomware.png)`

#### 🔴 Ransomware Case — Snapshot Evidence

**What the snapshot directory shows**

The snapshot directory captured both the ransomware-renamed `Server_Inventory.lock.xlsx` and the two clean restored copies of `Server_Inventory.xlsx` in correct chronological sequence.

**What this proves**

This is the full audit trail of the attack and the recovery — the malicious state recorded, the original filename recovered, and the clean version written back atomically. Filename recovery and rollback execution are both independently verified in the snapshot record.

> `![Step 3 - Sensitive Snapshots](images/step3_snapshots_sensitive.png)`

#### 🟡 Sensitive Deletion Case — Snapshot Evidence

**What the snapshot directory shows**

Two clean immutable versioned copies of `Roadmap_2025.docx` are preserved in the isolated snapshot storage directory, each timestamped with millisecond precision.

**Current state**

These copies were captured during normal operation, before the deletion event occurred. They remain untouched and ready — no running attack can reach or overwrite the snapshot directory. They await administrator approval for manual restoration.

---

### Step 4 — Administrator Alerts *(All Cases)*

> `![Step 4 - Decoy Alert](images/step4_alert_decoy.png)`

#### 🍯 Decoy Honeypot Alert

**What triggered it**

`CEO_Contract.docx` was modified. The event was classified as `HIGH_DECOY_ALERT` and the rollback executed immediately.

**What the alert contained**

The Administrator Module authenticated via SMTP and dispatched a formatted HTML email carrying the exact filename, the event classification, confirmation that automatic rollback had already executed, and the precise UTC timestamp. The administrator was fully informed within seconds of the breach — regardless of physical location.

> `![Step 4 - Ransomware Alert](images/step4_alert_ransomware.png)`

#### 🔴 Ransomware Detection Alert

**What triggered it**

`Server_Inventory.lock.xlsx` was detected and classified as `HIGH_RANSOMWARE_ROLLBACK`. The alert fired in parallel with the rollback — both executing simultaneously.

**What the alert contained**

The email documented the malicious filename `Server_Inventory.lock.xlsx`, the recovered original filename `Server_Inventory.xlsx`, the action taken, and the timestamp. No manual log-checking was required — everything the administrator needed was in one notification.

> `![Step 4 - Sensitive Alert](images/step4_alert_sensitive.png)`

#### 🟡 Sensitive File Deletion Alert

**What triggered it**

`Roadmap_2025.docx` was deleted and classified as `HIGH_SENSITIVE_DELETION`. No rollback was performed.

**What the alert contained**

The email flagged the event explicitly for mandatory human review, confirmed that no automatic action had been taken, noted that clean snapshots were available in isolated storage, and included the filename, classification, and timestamp. The administrator had everything needed to make the restoration decision from a single notification.

---

### Step 5 — Decoy File System in Action

> `![Step 5 - Decoy File Breach](images/step5_decoy.png)`

#### How the Honey-pot Layer Works

**The seeding strategy**

Honeypot files are seeded across monitored directories under names that look indistinguishable from real critical assets — `CEO_Contract.docx`, `API_Keys_Internal.json`, `Finance_Report_Q3.xlsx`. None of these files serve any operational purpose and no legitimate process ever needs to interact with them.

**Why it gives zero false positives**

Because no authorised user has any reason to touch a decoy file, every single interaction is by definition a confirmed breach. There is no threshold to tune, no pattern to match, no confirmation window to wait for — the touch alone is the evidence.

**Live test result**

A simulated insider modified `CEO_Contract.docx`. The Watcher intercepted the event instantly. The Logic Engine classified it as `HIGH_DECOY_ALERT` without hesitation. The tampered file was deleted. The clean version was restored from the latest snapshot. The live email alert was fired to the administrator. The snapshot directory confirmed multiple preserved clean copies of the decoy, each ready for instant rollback on every future trigger. The entire sequence completed in milliseconds.

---

### Step 6 — Live Dashboard View *(Live / Decoy / Ransomware / Sensitive)*

> `![Step 6 - Full Live Dashboard](images/step6_dashboard_live.png)`

#### 📺 Full Live Activity View

**What the dashboard shows**

The Streamlit dashboard displays every file event across all monitored directories — creation, modification, deletion — alongside each file's classification (DECOY / SENSITIVE / REAL) and its live cumulative risk score. The activity log updates continuously and is colour-coded by severity. Critical events are visually unmissable the moment they appear.

**What the administrator gets**

A real-time, zero-latency window into every action SHFSL 2.0 is taking — detections, rollbacks, escalations, and risk scores — all in one place, without opening a single log file.

> `![Step 6 - Dashboard Decoy View](images/step6_dashboard_decoy.png)`

#### 🍯 Decoy Breach on Dashboard

**What appeared on screen**

The moment `CEO_Contract.docx` was tampered with, the dashboard surfaced the event instantly. The file was flagged, the classification `HIGH_DECOY_ALERT` was displayed, the automatic rollback was triggered and confirmed on screen, and the critical event entry appeared in the activity log in real time with full detail.

**What the administrator saw**

Exactly what happened, exactly which file was affected, and exactly what the system did about it — all visible without any manual investigation.

> `![Step 6 - Dashboard Ransomware View](images/step6_dashboard_ransom.png)`

#### 🔴 Ransomware Detection on Dashboard

**What appeared on screen**

When `Server_Inventory.lock.xlsx` was detected, the dashboard lit up immediately. The malicious extension was flagged, the rollback fired, and `AUTOMATIC ROLLBACK SUCCESSFUL` was confirmed on screen alongside the recovered filename `Server_Inventory.xlsx`. The risk score updated to 100/100 in real time.

**What the administrator saw**

The full attack-and-recovery sequence playing out live — from detection through filename recovery to confirmed restore — visible in one view without opening a single log file.

> `![Step 6 - Dashboard Sensitive View](images/step6_dashboard_sensitive.png)`

#### 🟡 Sensitive Deletion on Dashboard

**What appeared on screen**

When `Roadmap_2025.docx` was deleted, the dashboard flagged the event instantly as `HIGH_SENSITIVE_DELETION`. The administrator alert was shown as dispatched. The risk score was displayed at 85/100. The incident was locked into the activity log with a clear indicator that manual review and a restoration decision were required.

**What the administrator saw**

No automatic action was taken — and the dashboard showed exactly that. The administrator had the full context to make the restoration call directly from the dashboard, with no ambiguity about what had happened or what was needed next.

---

## 📁 Project Structure

```
SHFSL-2.0/
├── monitor.py              # File System Monitor — The Watcher
├── engine.py               # Pattern Detection & Rollback Engine — The Logic
├── versioning.py           # Versioning System — The Snapshots
├── decoy_seeder.py         # Decoy File System — The Honey-pot
├── admin_alerts.py         # Administrator Module
├── dashboard.py            # Visualization & Dashboard
├── config.json             # Central System Configuration
├── snapshots/              # Isolated Immutable Snapshot Storage
├── logs/                   # Activity & Event Log Files
└── images/                 # Architecture & Workflow Diagrams
```

---

## ⚙️ Getting Started

### Prerequisites

```bash
Python 3.8+
pip
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/SHFSL-2.0.git
cd SHFSL-2.0

# Install dependencies
pip install watchdog streamlit
```

### Configuration

```bash
# Open and configure the central config file
nano config.json
```

Set the following fields inside `config.json`:

```json
{
  "MONITORED_DIR": "/path/to/watch",
  "SNAPSHOT_DIR": "/path/to/snapshots",
  "LOG_FILE": "/path/to/logs/activity.log",
  "SENDER_EMAIL": "your.sender@gmail.com",
  "RECEIVER_EMAIL": "admin@yourdomain.com",
  "SENDER_PASSWORD": "your-app-password",
  "MAX_SNAPSHOTS_PER_FILE": 5
}
```

### Running the System

```bash
# Start the protection daemon
python monitor.py

# Launch the live dashboard (open a separate terminal)
streamlit run dashboard.py
```

---

## 🔭 What's Next for SHFSL

**ML-based Threat Detection** — Moving beyond fixed rule signatures to a model that learns abnormal behavioural patterns and adapts to attack methods not yet defined in the ruleset.

**Blockchain-based Snapshot Storage** — Making every rollback history tamper-proof, cryptographically auditable, and legally admissible as forensic evidence.

**Cloud Integration** — Extending snapshot storage to AWS, Azure, and GCP for distributed, cross-environment protection at scale.

**Cross-Platform Support** — Currently Linux-native. Windows and macOS compatibility is the next milestone.

**User Behaviour Analytics (UBA)** — Tracking per-user file access patterns to surface insider threats before they reach the confirmed breach stage.

**Automated Incident Response** — Pairing alerts with predefined automated actions including directory isolation, user session termination, and cross-system notifications via Slack and SMS.

---

## 📚 References

1. [Python Watchdog Library Documentation](https://python-watchdog.readthedocs.io/)
2. "File System Snapshot and Rollback Mechanisms in Modern Operating Systems" — IEEE Transactions on Computers, 2021
3. "Ransomware Detection using Honeypot-based File Integrity Monitoring" — IJCSDF, 2022
4. "Design and Implementation of Self-Healing Systems" — ACM Computing Surveys, 2020
5. GitHub repositories: `watchdog`, `rsync`, `Timeshift`

---

## 🏁 The Bottom Line

Detection without recovery is **incomplete security** — that was the founding premise of this project.

Every existing tool stops at the alert. SHFSL 2.0 goes further — it reverses the damage. Real-time monitoring, intelligent classification, automated self-healing, and live visibility working as one system means that even when a threat lands inside the perimeter, the data survives.

This is not a backup solution. This is not a monitoring tool. This is the file system's **last line of defence** — and it holds.

---

*Built with 🔐 by Shree Vakthi — SHFSL 2.0*
