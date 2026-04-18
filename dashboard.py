# dashboard.py — SHFSL 2.0 (FULLY FIXED)
import streamlit as st
import pandas as pd
import json
import time
import os
from pathlib import Path
from datetime import datetime

# --- Configuration ---
WATCHER_LOG    = Path(os.getcwd()) / "watcher_log.json"
DASHBOARD_LOG  = Path(os.getcwd()) / "activity_dashboard.log"

st.set_page_config(
    layout="wide",
    page_title="SHFSL 2.0 — Self Healing File System",
    page_icon="🛡️"
)

# ── Data Loading ──────────────────────────────────────────────────────────────

def load_watcher_log():
    """
    Loads the watcher JSON log.
    FIXED: Retries on empty/corrupt JSON (watcher may be mid-write).
    FIXED: Returns (real_events_df, initialized_df) tuple — only files with
           actual filesystem events appear in the main grid.
    """
    MAX_READ_RETRIES = 3

    data = None
    for attempt in range(MAX_READ_RETRIES):
        try:
            with open(WATCHER_LOG, 'r', encoding='utf-8', errors='replace') as f:
                raw = f.read().strip()
            if not raw:
                time.sleep(0.1)
                continue
            data = json.loads(raw)
            break
        except FileNotFoundError:
            break
        except (json.JSONDecodeError, ValueError):
            if attempt < MAX_READ_RETRIES - 1:
                time.sleep(0.1)
            # All retries exhausted — fall through to empty return

    _empty = pd.DataFrame(columns=['File', 'Status', 'Risk Outcome', 'Last Event', 'Last Modified', 'Risk Score'])
    if data is None:
        return _empty, _empty

    real_records  = []
    quiet_records = []

    for filename, details in data.items():
        last_event = details.get("last_event", "initialized")
        record = {
            "File":          filename,
            "Status":        details.get("status", "REAL"),
            "Last Event":    last_event,
            "Risk Outcome":  details.get("risk_outcome", "NONE"),
            "Last Modified": details.get("last_modified", "N/A"),
            "Risk Score":    details.get("risk_score", 0),
        }
        if last_event not in ("initialized", "status_corrected"):
            real_records.append(record)
        else:
            quiet_records.append(record)

    cols = ['File', 'Status', 'Risk Outcome', 'Last Event', 'Last Modified', 'Risk Score']
    df_real  = pd.DataFrame(real_records,  columns=cols) if real_records  else _empty.copy()
    df_quiet = pd.DataFrame(quiet_records, columns=cols) if quiet_records else _empty.copy()
    return df_real, df_quiet


def load_dashboard_log():
    """
    Reads the activity log file.
    FIXED: Uses a threading-safe read with error replacement so a partially
    written file never crashes the dashboard.
    """
    try:
        with open(DASHBOARD_LOG, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        return "".join(lines[-100:])
    except FileNotFoundError:
        return ""


# ── Severity Classification ───────────────────────────────────────────────────

def classify_log_severity(log_text):
    """
    Classifies the overall alert level from the most recent log lines.
    Returns: 'critical' | 'high' | 'warning' | 'normal'
    """
    if not log_text:
        return 'normal'
    lines = log_text.strip().split('\n')
    recent = " ".join(lines[-20:]).upper()

    if "RANSOMWARE" in recent or "HIGH_RANSOMWARE" in recent or "DECOY" in recent:
        return 'critical'
    if "SENSITIVE" in recent or "HIGH_SENSITIVE" in recent or "SENSITIVE FILE DELETED" in recent:
        return 'high'
    if "ALERT" in recent:
        return 'warning'
    return 'normal'


# ── HTML Table ────────────────────────────────────────────────────────────────

def create_html_table(df):
    if df.empty:
        return (
            "<div style='text-align:center;padding:40px 20px;"
            "border:1px dashed rgba(0,255,255,0.2);border-radius:8px;"
            "background:rgba(0,0,0,0.3);'>"
            "<p style='color:#334455;font-family:monospace;font-size:0.9rem;margin:0;'>"
            "⏳ No file events yet — waiting for watcher activity…</p></div>"
        )

    html = '<div class="shfsl-table-wrap"><table><thead><tr>'
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            value = str(row[col])
            style = "border-bottom:1px dashed rgba(0,255,255,0.15);"

            if col == 'Risk Outcome':
                if 'HIGH_RANSOMWARE' in value or 'HIGH_DECOY' in value:
                    style += ('background-color:#cc0033 !important;color:#fff !important;'
                              'font-weight:bold;animation:critical_pulse 0.7s infinite;text-align:center;')
                elif 'HIGH_SENSITIVE' in value:
                    style += ('background-color:#b35900 !important;color:#fff !important;'
                              'font-weight:bold;border-left:4px solid #ff8c00 !important;')
                elif value.startswith('LOW_'):
                    style += 'color:#00cc66;'
                elif value == 'NONE':
                    style += 'color:#334455;'
                else:
                    style += 'color:#aaaaaa;'

            elif col == 'Status':
                if value == 'DECOY':
                    style += 'color:#ff8c00;font-weight:bold;'
                elif value == 'SENSITIVE':
                    style += 'color:#00bfff;font-weight:bold;'
                else:
                    style += 'color:#778899;'

            elif col == 'Last Event':
                if value == 'deleted':
                    style += 'color:#ff4d6d;'
                elif value == 'modified':
                    style += 'color:#ffcc00;'
                elif value == 'created':
                    style += 'color:#00cc66;'
                else:
                    style += 'color:#556677;'

            elif col == 'Risk Score':
                try:
                    score = int(value)
                    if score >= 75:
                        style += 'color:#ff4d6d;font-weight:bold;'
                    elif score >= 40:
                        style += 'color:#ff8c00;font-weight:bold;'
                    elif score > 0:
                        style += 'color:#ffcc00;'
                    else:
                        style += 'color:#334455;'
                    value = f"{score}/100"
                except (ValueError, TypeError):
                    style += 'color:#334455;'

            html += f'<td style="{style}">{value}</td>'
        html += "</tr>"

    html += "</tbody></table></div>"
    html += """
    <style>
        @keyframes critical_pulse {
            0%   { background-color:#cc0033; box-shadow:0 0 6px #cc0033; }
            50%  { background-color:#ff1a4d; box-shadow:0 0 14px #ff1a4d; }
            100% { background-color:#cc0033; box-shadow:0 0 6px #cc0033; }
        }
        .shfsl-table-wrap { overflow-x:auto; }
        .shfsl-table-wrap table {
            width:100%; border-collapse:collapse;
            border:2px solid #00ffff;
            box-shadow:0 0 24px rgba(0,255,255,0.3);
            background-color:rgba(5,5,15,0.85);
        }
        .shfsl-table-wrap th, .shfsl-table-wrap td {
            padding:11px 15px; text-align:left;
            color:#dddddd; font-family:'Courier New',monospace; font-size:0.875rem;
        }
        .shfsl-table-wrap th {
            background-color:#0a0a1a; color:#00ffff;
            text-shadow:0 0 5px rgba(0,255,255,0.6);
            border-bottom:2px solid #00ffff;
            font-size:0.82rem; letter-spacing:0.06em; text-transform:uppercase;
        }
        .shfsl-table-wrap tr:hover td { background-color:rgba(0,255,255,0.04); }
    </style>
    """
    return html


# ── Alert Banner ──────────────────────────────────────────────────────────────

def render_alert_banner(severity):
    if severity == 'critical':
        st.markdown("""
        <div style='background:linear-gradient(90deg,#8b0000,#cc0033);
                    padding:18px 24px;border-radius:8px;
                    border:3px solid #ff1a4d;
                    animation:flash_crit 0.4s infinite;margin-bottom:12px;'>
            <p style='color:#fff;margin:0;text-align:center;font-size:1.1rem;
                      font-weight:bold;font-family:monospace;letter-spacing:0.08em;'>
                🚨 CRITICAL BREACH — RANSOMWARE / DECOY TAMPER DETECTED — ROLLBACK INITIATED 🚨
            </p>
        </div>
        <style>@keyframes flash_crit{0%,100%{opacity:1;}50%{opacity:0.4;}}</style>
        """, unsafe_allow_html=True)

    elif severity == 'high':
        st.markdown("""
        <div style='background:linear-gradient(90deg,#5c2e00,#b35900);
                    padding:16px 24px;border-radius:8px;
                    border:3px solid #ff8c00;margin-bottom:12px;'>
            <p style='color:#fff;margin:0;text-align:center;font-size:1.05rem;
                      font-weight:bold;font-family:monospace;letter-spacing:0.06em;'>
                ⚠️ HIGH ALERT — SENSITIVE FILE DELETED — IMMEDIATE ADMINISTRATOR REVIEW REQUIRED ⚠️
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif severity == 'warning':
        st.markdown("""
        <div style='background:rgba(255,200,0,0.12);
                    padding:14px 24px;border-radius:8px;
                    border:2px solid #ffcc00;margin-bottom:12px;'>
            <p style='color:#ffcc00;margin:0;text-align:center;font-size:0.95rem;
                      font-weight:bold;font-family:monospace;'>
                ⚡ ALERT DETECTED — Review activity log below
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.success("🟢  Status: Operational  //  Threat Level: Zero  //  All Systems Nominal", icon="✅")


# ── Activity Log ──────────────────────────────────────────────────────────────

def render_activity_log(log_text):
    """Renders the log with color-coded lines by severity, most recent first."""
    if not log_text.strip():
        st.markdown(
            "<p style='color:#555;font-family:monospace;font-size:0.82rem;'>No activity logged yet.</p>",
            unsafe_allow_html=True
        )
        return

    lines = log_text.strip().split('\n')[-40:]
    html_lines = []
    for line in reversed(lines):
        upper = line.upper()
        if "RANSOMWARE" in upper or "HIGH_RANSOMWARE" in upper:
            color, bg, prefix = "#ff4d6d", "rgba(200,0,50,0.12)", "🔴"
        elif "DECOY" in upper or "HIGH_DECOY" in upper:
            color, bg, prefix = "#ff6b35", "rgba(200,80,0,0.12)", "🟠"
        elif "SENSITIVE" in upper or "HIGH_SENSITIVE" in upper:
            color, bg, prefix = "#ffa040", "rgba(180,90,0,0.10)", "🟡"
        elif "ROLLBACK SUCCESSFUL" in upper:
            color, bg, prefix = "#00e676", "rgba(0,180,80,0.10)", "✅"
        elif "ALERT" in upper:
            color, bg, prefix = "#ffcc00", "rgba(200,160,0,0.08)", "⚡"
        else:
            color, bg, prefix = "#778899", "transparent", "·"

        safe_line = line.replace('<', '&lt;').replace('>', '&gt;')
        html_lines.append(
            f"<div style='padding:4px 10px;background:{bg};border-radius:3px;margin:2px 0;'>"
            f"<span style='color:{color};font-family:\"Courier New\",monospace;font-size:0.82rem;'>"
            f"{prefix} {safe_line}</span></div>"
        )

    st.markdown(
        "<div style='max-height:340px;overflow-y:auto;border:1px solid #1a1a2e;"
        "border-radius:6px;padding:8px;background:rgba(0,0,0,0.5);'>"
        + "".join(html_lines) +
        "</div>",
        unsafe_allow_html=True
    )


# ── Global CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@keyframes matrix_scroll {
    from { background-position:0 0; }
    to   { background-position:0 -800px; }
}
.stApp {
    background-color:#020209;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Ctext x='8' y='18' fill='%23001800' font-size='11' font-family='monospace'%3E1010%3C/text%3E%3Ctext x='60' y='70' fill='%23001800' font-size='11' font-family='monospace'%3E0110%3C/text%3E%3Ctext x='20' y='100' fill='%23001800' font-size='11' font-family='monospace'%3E1001%3C/text%3E%3C/svg%3E");
    background-repeat:repeat;
    animation:matrix_scroll 80s linear infinite;
    color:#e0e0e0;
    font-family:'Courier New', monospace;
}
h1 {
    color:#00ffff !important;
    text-shadow:0 0 10px #00ffff, 0 0 30px rgba(0,255,255,0.4);
    font-size:1.9rem !important;
    letter-spacing:0.04em;
    margin-bottom:2px !important;
}
h2 {
    color:#cc88ff !important;
    border-bottom:2px dashed rgba(0,255,255,0.3) !important;
    padding-bottom:8px !important;
    margin-top:28px !important;
    font-size:1.2rem !important;
    letter-spacing:0.05em;
}
.stCaption, [data-testid="stCaptionContainer"] p {
    color:#556677 !important;
    font-size:0.78rem !important;
}
.metric-card {
    background:rgba(8,8,22,0.9);
    border:1px solid #1a1a3a;
    box-shadow:0 0 16px rgba(0,255,255,0.12);
    border-radius:8px;
    padding:18px 20px;
    margin-bottom:8px;
}
.metric-card .metric-label {
    font-size:0.72rem;
    color:#556677;
    text-transform:uppercase;
    letter-spacing:0.1em;
    margin-bottom:8px;
}
.metric-card .metric-value {
    font-size:2.4rem;
    font-weight:bold;
    margin:0;
    line-height:1;
}
.metric-card .metric-sub {
    font-size:0.72rem;
    color:#445566;
    margin-top:8px;
}
</style>
""", unsafe_allow_html=True)


# ── Main Dashboard ────────────────────────────────────────────────────────────

st.title("🛡️ Self Healing File System Layer 2.0")
st.caption("⚡ SHFSL v2.1.0  |  Real-time Threat Detection & Auto-Rollback  |  Cyber-Security Level: MAX")

# FIX: Use st.rerun() pattern instead of while True + st.empty().container()
# The old pattern caused memory leaks in newer Streamlit versions because each
# loop iteration stacked new widget trees without clearing the old ones.
# The correct Streamlit pattern for auto-refresh is: render → sleep → st.rerun().

df_real, df_quiet = load_watcher_log()
log_text           = load_dashboard_log()
severity           = classify_log_severity(log_text)

render_alert_banner(severity)

# ── Section 1: Live File Events Grid ──────────────────────────────────────────
st.header("1 · Live File Events")

total_monitored = len(df_real) + len(df_quiet)
active_count    = len(df_real)
quiet_count     = len(df_quiet)

if total_monitored > 0:
    st.markdown(
        f"<p style='color:#334455;font-family:monospace;font-size:0.8rem;margin-bottom:8px;'>"
        f"📂 <span style='color:#556677;'>Monitoring</span> "
        f"<span style='color:#00ffff;'>{total_monitored}</span> files total — "
        f"<span style='color:#00cc66;'>{active_count}</span> with real events — "
        f"<span style='color:#334455;'>{quiet_count}</span> quiet</p>",
        unsafe_allow_html=True
    )

st.markdown(create_html_table(df_real), unsafe_allow_html=True)

if not df_quiet.empty:
    with st.expander(f"🔕  {quiet_count} monitored files with no events yet (click to expand)"):
        st.dataframe(df_quiet[['File', 'Status']], hide_index=True, use_container_width=True)

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# ── Section 2: Metrics ────────────────────────────────────────────────────────
st.header("2 · System Metrics")

all_df = pd.concat([df_real, df_quiet]) if total_monitored > 0 else pd.DataFrame(columns=['Status', 'Risk Outcome'])
all_statuses = all_df['Status'].value_counts() if not all_df.empty else pd.Series(dtype=int)

high_risk_count     = df_real['Risk Outcome'].str.contains('HIGH_', na=False).sum()      if not df_real.empty else 0
sensitive_del_count = df_real['Risk Outcome'].str.contains('HIGH_SENSITIVE', na=False).sum() if not df_real.empty else 0
ransomware_count    = df_real['Risk Outcome'].str.contains('HIGH_RANSOMWARE', na=False).sum() if not df_real.empty else 0
decoy_count         = df_real['Risk Outcome'].str.contains('HIGH_DECOY', na=False).sum()   if not df_real.empty else 0

col1, col2, col3, col4, col5 = st.columns(5)

def metric_card(col, label, value, color, sub=""):
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>{label}</div>
            <p class='metric-value' style='color:{color};text-shadow:0 0 8px {color};'>{value}</p>
            <div class='metric-sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

metric_card(col1, "Active Events",    active_count,                          "#00ffff",  f"of {total_monitored} monitored")
metric_card(col2, "Decoy Honeypots",  all_statuses.get("DECOY",     0),      "#ff8c00",  "traps active")
metric_card(col3, "Sensitive Assets", all_statuses.get("SENSITIVE",  0),     "#00bfff",  "access restricted")
metric_card(col4, "Sensitive Deleted",
            sensitive_del_count,
            "#ff8c00" if sensitive_del_count > 0 else "#334455",
            "⚠️ review needed" if sensitive_del_count > 0 else "all clear")
metric_card(col5, "Ransomware/Decoy",
            ransomware_count + decoy_count,
            "#ff4d6d" if (ransomware_count + decoy_count) > 0 else "#334455",
            "🔴 rollback triggered" if (ransomware_count + decoy_count) > 0 else "all clear")

# ── Section 3: Activity Log ───────────────────────────────────────────────────
st.header("3 · Live Activity Log")
st.caption("Most recent events shown first · Color-coded by severity · Last 40 entries")
render_activity_log(log_text)

# ── Section 4: Event Breakdown ────────────────────────────────────────────────
if not df_real.empty:
    st.header("4 · Event Breakdown")
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("ACTIVE FILES BY STATUS")
        s_df = df_real['Status'].value_counts().reset_index()
        s_df.columns = ['Status', 'Count']
        st.dataframe(s_df, hide_index=True, use_container_width=True)
    with col_b:
        st.caption("ACTIVE FILES BY RISK OUTCOME")
        r_df = df_real['Risk Outcome'].value_counts().reset_index()
        r_df.columns = ['Risk Outcome', 'Count']
        st.dataframe(r_df, hide_index=True, use_container_width=True)

st.markdown(
    f"<p style='color:#1a2233;font-size:0.75rem;margin-top:20px;text-align:right;'>"
    f"⟳ Last refreshed: {datetime.now().strftime('%H:%M:%S')} · auto-refresh: 2s</p>",
    unsafe_allow_html=True
)

# FIX: Use st.rerun() for auto-refresh — correct Streamlit pattern.
# This renders the full page once, sleeps, then triggers a clean re-render
# from the top. No memory leak, no stacked widget trees.
time.sleep(2)
st.rerun()