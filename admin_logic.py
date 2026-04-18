# admin_logic.py — SHFSL 2.0 (FULLY FIXED)
import os
import smtplib
import json
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- Load config ---
CONFIG_FILE = os.path.join(os.getcwd(), "config.json")
CONFIG = {}
try:
    with open(CONFIG_FILE, 'r') as f:
        CONFIG = json.load(f).get("ADMIN_CONFIG", {})
except FileNotFoundError:
    print("[CONFIG] ⚠️  config.json not found — email alerts will be skipped.")
except json.JSONDecodeError:
    print("[CONFIG] ⚠️  config.json is malformed — email alerts will be skipped.")

SENDER_EMAIL    = CONFIG.get("SENDER_EMAIL",   "admin.security@shfsl.com")
RECEIVER_EMAIL  = CONFIG.get("RECEIVER_EMAIL", "emergency.alerts@yourcompany.com")
SENDER_PASSWORD = CONFIG.get("SENDER_PASSWORD", "PASSWORD_MISSING")
SMTP_SERVER     = CONFIG.get("EMAIL_SERVER",   "smtp.gmail.com")
SMTP_PORT       = 587

DASHBOARD_LOG_PATH = os.path.join(os.getcwd(), "activity_dashboard.log")

# FIX: Use a threading lock to prevent race conditions between the watcher
# writing to the log and the dashboard reading it simultaneously.
_log_lock = threading.Lock()

MAX_LOG_LINES = 500


def send_alert_email(subject, body):
    """
    Sends a formatted HTML alert email for critical security events.
    FIX: Runs email sending in a background thread so it never blocks
    the watcher's real-time event processing loop.
    """
    if SENDER_PASSWORD == "PASSWORD_MISSING":
        print("[EMAIL] ⚠️  Skipping — SENDER_PASSWORD not set in config.json.")
        return

    def _send():
        try:
            msg = MIMEMultipart("alternative")
            msg['Subject'] = subject
            msg['From']    = SENDER_EMAIL
            msg['To']      = RECEIVER_EMAIL

            plain = MIMEText(body, "plain")

            severity_color = "#cc0033"
            if "SENSITIVE" in subject.upper():
                severity_color = "#b35900"
            elif "RANSOMWARE" in subject.upper():
                severity_color = "#8b0000"
            elif "DECOY" in subject.upper():
                severity_color = "#cc6600"

            html_body = f"""
            <html><body style="font-family:Courier New,monospace;background:#111;color:#eee;padding:20px;">
              <div style="border:2px solid {severity_color};border-radius:8px;padding:20px;max-width:600px;">
                <h2 style="color:{severity_color};margin-top:0;">🛡️ SHFSL 2.0 — Security Alert</h2>
                <hr style="border-color:{severity_color};">
                <pre style="color:#ddd;line-height:1.6;">{body}</pre>
                <hr style="border-color:#333;">
                <p style="color:#556677;font-size:12px;margin-bottom:0;">
                  Sent by Self-Healing File System Layer 2.0 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
              </div>
            </body></html>
            """
            html_part = MIMEText(html_body, "html")

            msg.attach(plain)
            msg.attach(html_part)

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

            print(f"[EMAIL] ✅ Alert sent to {RECEIVER_EMAIL}: {subject[:60]}")

        except smtplib.SMTPAuthenticationError:
            print("[EMAIL] ❌ Authentication failed — check your App Password in config.json.")
        except smtplib.SMTPConnectError:
            print("[EMAIL] ❌ Cannot connect to SMTP server — check network/server settings.")
        except Exception as e:
            print(f"[EMAIL] ❌ Failed to send alert: {e}")

    # FIX: Non-blocking — email is sent in background thread
    t = threading.Thread(target=_send, daemon=True)
    t.start()


def update_dashboard_log(message):
    """
    Appends a timestamped message to the activity dashboard log.
    FIX: Uses a threading lock to prevent race conditions between the watcher
    writing and the dashboard reading. Rotates log at MAX_LOG_LINES.
    """
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{timestamp} {message}\n"

    with _log_lock:
        try:
            existing_lines = []
            if os.path.exists(DASHBOARD_LOG_PATH):
                with open(DASHBOARD_LOG_PATH, 'r', encoding='utf-8', errors='replace') as f:
                    existing_lines = f.readlines()

            if len(existing_lines) >= MAX_LOG_LINES:
                existing_lines = existing_lines[-(MAX_LOG_LINES - 1):]
                print(f"[ADMIN] 🔄 Dashboard log rotated (kept last {MAX_LOG_LINES} lines)")

            existing_lines.append(log_entry)

            # FIX: Write atomically using temp file + rename
            tmp_path = DASHBOARD_LOG_PATH + ".tmp"
            with open(tmp_path, 'w', encoding='utf-8') as f:
                f.writelines(existing_lines)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, DASHBOARD_LOG_PATH)

        except Exception as e:
            print(f"[ADMIN] ❌ Failed to write dashboard log: {e}")