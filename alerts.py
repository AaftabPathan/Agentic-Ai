# alerts.py
import smtplib
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv("EMAIL_SENDER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_incident_alert(pod_name, status_was, fix_applied, time_to_fix, incident_num):
    """Pod crash hone pe email bhejo"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🚨 INCIDENT #{incident_num} RESOLVED — {pod_name}"
        msg["From"] = SENDER
        msg["To"] = RECEIVER

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        text = f"""
DEVOPS AI AGENT — INCIDENT REPORT
===================================
Incident #: {incident_num}
Timestamp : {timestamp}

Pod Name  : {pod_name}
Was Status: {status_was}
Fix Applied: {fix_applied}
Time to Fix: {time_to_fix} seconds

Status: RESOLVED ✅
===================================
This was auto-fixed by AI Agent.
        """

        html = f"""
<html>
<body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px;">
  <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: auto; border-left: 5px solid #28a745;">
    <h2 style="color: #28a745;">✅ INCIDENT #{incident_num} RESOLVED</h2>
    <p style="color: #666;">Auto-fixed by Agentic AI DevOps System</p>
    <hr style="border: 1px solid #eee;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr style="background: #f8f9fa;">
        <td style="padding: 10px; font-weight: bold;">🕐 Timestamp</td>
        <td style="padding: 10px;">{timestamp}</td>
      </tr>
      <tr>
        <td style="padding: 10px; font-weight: bold;">📦 Pod Name</td>
        <td style="padding: 10px;">{pod_name}</td>
      </tr>
      <tr style="background: #f8f9fa;">
        <td style="padding: 10px; font-weight: bold;">❌ Was Status</td>
        <td style="padding: 10px; color: #dc3545;">{status_was}</td>
      </tr>
      <tr>
        <td style="padding: 10px; font-weight: bold;">🔧 Fix Applied</td>
        <td style="padding: 10px;">{fix_applied}</td>
      </tr>
      <tr style="background: #f8f9fa;">
        <td style="padding: 10px; font-weight: bold;">⚡ Time to Fix</td>
        <td style="padding: 10px; color: #28a745;"><b>{time_to_fix} seconds</b></td>
      </tr>
      <tr>
        <td style="padding: 10px; font-weight: bold;">✅ Final Status</td>
        <td style="padding: 10px; color: #28a745;"><b>RESOLVED</b></td>
      </tr>
    </table>
    <hr style="border: 1px solid #eee;">
    <p style="color: #999; font-size: 12px;">
      🤖 This incident was automatically detected and resolved by<br>
      <b>Agentic AI for DevOps — Autonomous Incident Remediation Agent</b>
    </p>
  </div>
</body>
</html>
"""
        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())

        print(f"📧 Email sent successfully!")
        return True

    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def send_manual_intervention_alert(pod_name, incident_num, attempts):
    """Max attempts pe warning email bhejo"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"⚠️ MANUAL INTERVENTION NEEDED — {pod_name}"
        msg["From"] = SENDER
        msg["To"] = RECEIVER

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""
<html>
<body style="font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px;">
  <div style="background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: auto; border-left: 5px solid #dc3545;">
    <h2 style="color: #dc3545;">⚠️ MANUAL INTERVENTION NEEDED</h2>
    <p style="color: #666;">AI Agent could not fix the pod automatically</p>
    <hr style="border: 1px solid #eee;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr style="background: #f8f9fa;">
        <td style="padding: 10px; font-weight: bold;">🕐 Timestamp</td>
        <td style="padding: 10px;">{timestamp}</td>
      </tr>
      <tr>
        <td style="padding: 10px; font-weight: bold;">📦 Pod Name</td>
        <td style="padding: 10px;">{pod_name}</td>
      </tr>
      <tr style="background: #f8f9fa;">
        <td style="padding: 10px; font-weight: bold;">🔁 Fix Attempts</td>
        <td style="padding: 10px; color: #dc3545;">{attempts} times tried</td>
      </tr>
      <tr>
        <td style="padding: 10px; font-weight: bold;">🚨 Action Needed</td>
        <td style="padding: 10px; color: #dc3545;"><b>Please check manually!</b></td>
      </tr>
    </table>
    <hr style="border: 1px solid #eee;">
    <p style="color: #999; font-size: 12px;">
      🤖 Agentic AI for DevOps — Autonomous Incident Remediation Agent
    </p>
  </div>
</body>
</html>
"""
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, PASSWORD)
            server.sendmail(SENDER, RECEIVER, msg.as_string())

        print(f"📧 Warning email sent!")
        return True

    except Exception as e:
        print(f"❌ Warning email failed: {e}")
        return False


def send_to_dashboard(pod_name, status_was, fix_applied, time_to_fix, incident_num):
    """Dashboard ko incident data bhejo"""
    try:
        requests.post(
            "http://localhost:5000/api/incident",
            json={
                "pod_name": pod_name,
                "status_was": status_was,
                "fix_applied": fix_applied,
                "time_to_fix": time_to_fix
            },
            timeout=2
        )
    except:
        pass  # Dashboard band ho toh ignore karo