<div align="center">

# 🛡️ SHFSL 2.0
### Self-Healing File System Layer

> *"I built a file system that fights back — autonomously, instantly, and without mercy."*

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Watchdog](https://img.shields.io/badge/Watchdog-Live%20Monitor-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)
![Threats](https://img.shields.io/badge/Threats-Neutralized%20Instantly-brightgreen?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

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
