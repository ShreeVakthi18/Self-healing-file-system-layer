# dashboard.py (READABLE + CYBERPUNK AESTHETIC)
import streamlit as st
import pandas as pd
import json
import time
import os
from pathlib import Path

# --- Configuration ---
WATCHER_LOG = Path(os.getcwd()) / "watcher_log.json"
DASHBOARD_LOG = Path(os.getcwd()) / "activity_dashboard.log"

st.set_page_config(layout="wide", page_title="Self Healing File System Layer2.0 (SHFSL2.0)", page_icon="🛡️")

# --- Functions ---

def load_watcher_log():
    try:
        with open(WATCHER_LOG, 'r') as f:
            data = json.load(f)
        records = []
        for filename, details in data.items():
            records.append({
                "File": filename,
                "Status": details.get("status", "REAL"),
                "Last Event": details.get("last_event", "N/A"),
                "Risk Outcome": details.get("risk_outcome", "NONE"),
                "Last Modified": details.get("last_modified", "N/A")
            })
        df = pd.DataFrame(records)
        df = df[['File', 'Status', 'Risk Outcome', 'Last Event', 'Last Modified']]
        return df
    except FileNotFoundError:
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def load_dashboard_log():
    try:
        with open(DASHBOARD_LOG, 'r') as f:
            log_content = f.read()
        return log_content
    except FileNotFoundError:
        return "System boot sequence complete. Waiting for file system events..."

def create_html_table(df):
    if df.empty:
        return ""
    html = """
    <div class="table-container">
    <table>
        <thead><tr>
    """
    for col in df.columns:
        html += f'<th>{col}</th>'
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            value = str(row[col])
            style = "border-bottom: 1px dashed rgba(0,255,255,0.2);"
            if col == 'Risk Outcome':
                if 'HIGH_RANSOMWARE' in value or 'HIGH_DECOY' in value:
                    style += 'background-color:#ff004c !important;color:white !important;font-weight:bold;animation:critical_pulse_html 0.6s infinite;'
                elif 'HIGH_SENSITIVE' in value:
                    style += 'background-color:#ff8c00 !important;color:white !important;font-weight:bold;'
                elif 'LOW_' in value:
                    style += 'background-color:#00b300 !important;color:white;'
                else:
                    style += 'color:#00ff7f;'
            html += f'<td style="{style}">{value}</td>'
        html += "</tr>"
    html += "</tbody></table></div>"

    html += """
    <style>
        @keyframes critical_pulse_html {
            0%   { background-color:#ff004c; box-shadow:0 0 8px #ff004c; }
            50%  { background-color:#ff3377; box-shadow:0 0 14px #ff3377; }
            100% { background-color:#ff004c; box-shadow:0 0 8px #ff004c; }
        }
        .table-container table {
            width:100%;
            border-collapse:collapse;
            border:2px solid #00ffff;
            box-shadow:0 0 20px rgba(0,255,255,0.5);
            background-color:rgba(0,0,0,0.7);
            font-size:0.92rem;
        }
        .table-container th, .table-container td {
            padding:10px 14px;
            text-align:left;
            color:#ffffff;
            font-family:'Courier New', monospace;
            font-size:0.9rem;
        }
        .table-container th {
            background-color:#1a1a1a;
            color:#00ffff;
            text-shadow:0 0 4px #00ffff;
            border-bottom:2px solid #00ffff;
            font-size:0.95rem;
            letter-spacing:0.05em;
        }
    </style>
    """
    return html


# --- Global CSS (Readable + Cyberpunk) ---
st.markdown("""
<style>
/* Matrix scrolling background */
@keyframes matrix_scroll {
    from { background-position: 0 0; }
    to   { background-position: 0 -1000px; }
}
.stApp {
    background-color: #000000;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100'%3E%3Ctext x='5' y='15' fill='%23004000' font-size='12' font-family='monospace'%3E1010%3C/text%3E%3Ctext x='55' y='65' fill='%23004000' font-size='12' font-family='monospace'%3E0110%3C/text%3E%3C/svg%3E");
    background-repeat: repeat;
    animation: matrix_scroll 60s linear infinite;
    color: #e0e0e0;
    font-family: 'Courier New', monospace;
}

/* Screen shake on critical */
@keyframes screen_shake {
    0%, 100% { transform: translate(0,0) rotate(0); }
    10% { transform: translate(-1px,-1px) rotate(-0.3deg); }
    20% { transform: translate(1px,1px) rotate(0.3deg); }
    30% { transform: translate(-1px,1px) rotate(0); }
    40% { transform: translate(1px,-1px) rotate(-0.3deg); }
    50% { transform: translate(0,0) rotate(0); }
}
.critical-mode .main { animation: screen_shake 0.1s infinite; }

/* Headers */
h1 {
    color: #00ffff !important;
    text-shadow: 0 0 8px #00ffff, 0 0 20px rgba(0,255,255,0.6);
    font-size: 2.0rem !important;
    margin-bottom: 4px !important;
}
h2 {
    color: #ff00ff !important;
    border-bottom: 3px dashed #00ffff !important;
    padding-bottom: 8px !important;
    margin-top: 24px !important;
    text-shadow: 0 0 6px #ff00ff;
    font-size: 1.3rem !important;
}
h3 { font-size: 1.1rem !important; }

/* Body text */
.stMarkdown p { color: #cccccc; font-size: 0.9rem !important; }

/* Log text area */
.stTextArea label {
    color: #00ff7f !important;
    text-shadow: 0 0 6px #00ff7f;
    font-size: 0.95rem !important;
}
.stTextArea textarea {
    color: #00ffff !important;
    background-color: rgba(10, 0, 20, 0.85) !important;
    text-shadow: 0 0 2px rgba(0,255,255,0.5) !important;
    border: 2px solid #00ffff !important;
    box-shadow: 0 0 12px rgba(0,255,255,0.4) !important;
    font-size: 0.85rem !important;
    font-family: 'Courier New', monospace !important;
}

/* Metric blocks */
.metric-block {
    background-color: rgba(20,20,40,0.9) !important;
    border: 1px solid #3a3a5a !important;
    box-shadow: 0 0 12px rgba(0,255,255,0.3) !important;
    border-radius: 6px;
    padding: 16px !important;
}
.metric-block p  { font-size: 0.8rem !important; margin-bottom: 6px !important; color: #999; }
.metric-block h3 { font-size: 2.2rem !important; margin: 0 !important; }
.metric-block p:last-child { font-size: 0.75rem !important; margin-top: 6px !important; }

/* Caption / small text */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #888888 !important;
    font-size: 0.8rem !important;
}
</style>
""", unsafe_allow_html=True)


st.title("🛡️ Self Healing File System Layer 2.0")
st.caption("⚡ System Status: Online | V2.1.0 | Cyber-Security Level: Max")

# --- 1. Alert Stream ---
st.header("1. Critical Alert Stream")

if 'log_content_value' not in st.session_state:
    st.session_state.log_content_value = load_dashboard_log()

# --- MATRIX RAIN SYSTEM LOG COMPONENT ---
def render_matrix_log(log_text):
    # Convert log lines to JS array string
    lines = [l.replace("'", "\\'").replace('"', '\\"') for l in log_text.strip().split("\n") if l.strip()]
    lines_js = "[" + ",".join([f'"{l}"' for l in lines[-30:]]) + "]"  # last 30 lines

    html = f"""
    <div id="matrix-log-wrapper" style="position:relative;width:100%;height:260px;
         border:2px solid #00ff41;border-radius:6px;overflow:hidden;
         box-shadow:0 0 24px rgba(0,255,65,0.5), inset 0 0 40px rgba(0,0,0,0.9);
         background:#000;">

      <!-- Matrix rain canvas behind -->
      <canvas id="matrixCanvas" style="position:absolute;top:0;left:0;width:100%;height:100%;opacity:0.18;z-index:0;"></canvas>

      <!-- Scanline overlay -->
      <div style="position:absolute;top:0;left:0;width:100%;height:100%;
           background:repeating-linear-gradient(0deg,rgba(0,0,0,0.07) 0px,rgba(0,0,0,0.07) 1px,transparent 1px,transparent 3px);
           z-index:1;pointer-events:none;"></div>

      <!-- Log header bar -->
      <div style="position:absolute;top:0;left:0;width:100%;padding:5px 14px;
           background:rgba(0,30,0,0.95);border-bottom:1px solid #00ff41;
           z-index:3;display:flex;align-items:center;gap:10px;">
        <span style="color:#00ff41;font-family:'Courier New',monospace;font-size:0.78rem;letter-spacing:0.1em;
              text-shadow:0 0 6px #00ff41;">▶ SYSTEM LOG // LIVE FEED</span>
        <span id="blink-dot" style="width:8px;height:8px;border-radius:50%;background:#00ff41;
              display:inline-block;animation:blink_dot 1s infinite;box-shadow:0 0 6px #00ff41;"></span>
      </div>

      <!-- Scrolling log lines -->
      <div id="log-feed" style="position:absolute;top:32px;left:0;width:100%;
           height:calc(100% - 32px);overflow-y:auto;padding:10px 14px;
           font-family:'Courier New',monospace;font-size:0.82rem;line-height:1.7;
           z-index:2;scrollbar-width:thin;scrollbar-color:#00ff41 #000;">
      </div>
    </div>

    <style>
      @keyframes blink_dot {{ 0%,100%{{opacity:1;}} 50%{{opacity:0;}} }}
      @keyframes glitch_line {{
        0%   {{ transform:translateX(0);    opacity:1; }}
        20%  {{ transform:translateX(-3px); opacity:0.8; }}
        40%  {{ transform:translateX(3px);  opacity:1; }}
        60%  {{ transform:translateX(-1px); opacity:0.9; }}
        100% {{ transform:translateX(0);    opacity:1; }}
      }}
      #log-feed::-webkit-scrollbar {{ width:4px; }}
      #log-feed::-webkit-scrollbar-track {{ background:#000; }}
      #log-feed::-webkit-scrollbar-thumb {{ background:#00ff41;border-radius:2px; }}
    </style>

    <script>
    (function() {{
      // --- Matrix Rain ---
      const canvas = document.getElementById('matrixCanvas');
      const ctx = canvas.getContext('2d');
      function resizeCanvas() {{
        canvas.width  = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
      }}
      resizeCanvas();
      const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノABCDEF';
      const fontSize = 13;
      let cols = Math.floor(canvas.width / fontSize);
      let drops = Array(cols).fill(1);
      function drawMatrix() {{
        ctx.fillStyle = 'rgba(0,0,0,0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px monospace';
        for (let i = 0; i < drops.length; i++) {{
          const c = chars[Math.floor(Math.random() * chars.length)];
          ctx.fillText(c, i * fontSize, drops[i] * fontSize);
          if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
          drops[i]++;
        }}
      }}
      setInterval(drawMatrix, 50);

      // --- Typewriter log feed ---
      const logLines = {lines_js};
      const feed = document.getElementById('log-feed');

      function getLineColor(line) {{
        if (line.includes('CRITICAL') || line.includes('BREACH') || line.includes('RANSOMWARE'))
          return '#ff2244';
        if (line.includes('ALERT') || line.includes('HIGH'))
          return '#ff8c00';
        if (line.includes('ROLLBACK') || line.includes('RESTORED'))
          return '#00e5ff';
        if (line.includes('OK') || line.includes('SAFE') || line.includes('LOW'))
          return '#00ff7f';
        return '#00ff41';
      }}

      function getPrefix(line) {{
        if (line.includes('CRITICAL') || line.includes('BREACH')) return '🚨';
        if (line.includes('ALERT') || line.includes('HIGH'))      return '⚠️';
        if (line.includes('ROLLBACK'))                             return '🔄';
        if (line.includes('OK') || line.includes('SAFE'))         return '✅';
        return '▸';
      }}

      let lineIndex = 0;
      function typeNextLine() {{
        if (lineIndex >= logLines.length) {{
          lineIndex = 0;
          feed.innerHTML = '';
        }}
        const raw = logLines[lineIndex++];
        const color = getLineColor(raw);
        const prefix = getPrefix(raw);
        const div = document.createElement('div');
        div.style.cssText = `color:${{color}};white-space:pre-wrap;word-break:break-all;
          text-shadow:0 0 4px ${{color}};padding:1px 0;
          animation:glitch_line 0.3s ease;`;

        // typewriter char-by-char
        const full = prefix + ' ' + raw;
        let i = 0;
        div.textContent = '';
        feed.appendChild(div);
        feed.scrollTop = feed.scrollHeight;

        const typer = setInterval(() => {{
          div.textContent += full[i++];
          if (i >= full.length) {{
            clearInterval(typer);
            setTimeout(typeNextLine, 180);
          }}
        }}, 18);
      }}

      // Seed all lines instantly first, then typewriter new ones
      logLines.forEach((raw, idx) => {{
        const color = getLineColor(raw);
        const prefix = getPrefix(raw);
        const div = document.createElement('div');
        div.style.cssText = `color:${{color}};white-space:pre-wrap;word-break:break-all;
          text-shadow:0 0 4px ${{color}};padding:1px 0;`;
        div.textContent = prefix + ' ' + raw;
        feed.appendChild(div);
      }});
      feed.scrollTop = feed.scrollHeight;
      lineIndex = logLines.length;
      setTimeout(typeNextLine, 1200);
    }})();
    </script>
    """
    return html

log_placeholder = st.empty()
with log_placeholder.container():
    st.markdown(render_matrix_log(st.session_state.log_content_value), unsafe_allow_html=True)

st.markdown("<hr style='border-top:2px solid #00ffff;margin:10px 0;'>", unsafe_allow_html=True)

data_placeholder = st.empty()

while True:
    df_raw = load_watcher_log()
    log_text = load_dashboard_log()
    st.session_state.log_content_value = log_text

    incident_detected = "CRITICAL" in log_text or "ALERT" in log_text

    # Refresh the matrix log panel
    with log_placeholder.container():
        st.markdown(render_matrix_log(log_text), unsafe_allow_html=True)

    js_toggle = f"""
    <script>
        const app = window.parent.document.querySelector('.stApp');
        if (app) {{
            if ({'true' if incident_detected else 'false'}) {{
                app.classList.add('critical-mode');
            }} else {{
                app.classList.remove('critical-mode');
            }}
        }}
    </script>
    """
    st.markdown(js_toggle, unsafe_allow_html=True)

    with data_placeholder.container():

        if incident_detected:
            st.markdown(
                """
                <div style='background-color:#ff0000;padding:18px;border-radius:8px;
                     border:4px solid #ffffff;animation:flash_error 0.2s infinite;'>
                    <p style='color:white;margin:0;text-align:center;
                              text-shadow:0 0 10px white;font-size:1.1rem;font-weight:bold;'>
                        🚨 BREACH DETECTED — Security Protocol Engaged — Rollback Initiated 🚨
                    </p>
                </div>
                <style>
                    @keyframes flash_error { 0%,100%{opacity:1;} 50%{opacity:0.35;} }
                </style>
                """,
                unsafe_allow_html=True
            )
        else:
            st.success("🟢 Status: Operational // Threat level: Zero", icon="✅")

        st.header("2. Monitored File System Grid")

        if not df_raw.empty:
            st.markdown(create_html_table(df_raw), unsafe_allow_html=True)

            status_counts = df_raw['Status'].value_counts()
            high_risk_count = len(df_raw[df_raw['Risk Outcome'].str.contains('HIGH_')])

            col1, col2, col3, col4 = st.columns(4)

            def display_metric_html(title, value, color, delta_text=""):
                st.markdown(f"""
                <div class='metric-block'>
                    <p>{title}</p>
                    <h3 style='color:{color};text-shadow:0 0 8px {color};'>{value}</h3>
                    <p style='color:#555577;'>{delta_text}</p>
                </div>
                """, unsafe_allow_html=True)

            with col1:
                display_metric_html("ASSET COUNT", len(df_raw), "#00ffff", "System scan complete")
            with col2:
                display_metric_html("DECOY HONEYPOTS", status_counts.get("DECOY", 0), "#ff8c00", "Traps active")
            with col3:
                display_metric_html("SENSITIVE ASSETS", status_counts.get("SENSITIVE", 0), "#00ff7f", "Access restricted")
            with col4:
                mc = "#ff004c" if high_risk_count > 0 else "#00ff7f"
                dt = "Protocols engaged" if high_risk_count > 0 else "All clear"
                display_metric_html("HIGH-RISK EVENTS", high_risk_count, mc, dt)
        else:
            st.info("Waiting for the watcher to initialize file status...")

        st.markdown(
            "<p style='color:#00ffff;font-size:0.8rem;margin-top:16px;'>"
            "⟳ System refresh: core data synced (1s)...</p>",
            unsafe_allow_html=True
        )

    time.sleep(1)