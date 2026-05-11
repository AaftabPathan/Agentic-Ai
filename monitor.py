# monitor.py
import sys
import os
import time
import subprocess
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.join(BASE_DIR, 'agent')
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, AGENT_DIR)

from colorama import Fore, Style, init
from agent import create_devops_agent
import tools
from alerts import send_incident_alert, send_manual_intervention_alert, send_to_dashboard

init(autoreset=True)

CHECK_INTERVAL = 10
MAX_FIX_ATTEMPTS = 3

fixed_pods = {}
incident_count = 0

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(message, color=Fore.WHITE):
    print(f"{color}[{get_timestamp()}] {message}{Style.RESET_ALL}")

def print_banner():
    print(f"{Fore.CYAN}")
    print("╔══════════════════════════════════════════════════╗")
    print("║  🤖 AGENTIC AI — REAL WORLD AUTO HEALING        ║")
    print("║  Self-Healing Kubernetes Infrastructure          ║")
    print("╚══════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

def deploy_my_app():
    """my-app Deployment deploy karo"""
    subprocess.run(
        ["kubectl", "apply", "-f", "k8s/my-app.yaml"],
        capture_output=True
    )

def check_crashed_pods():
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-o", "json"],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        crashed = []
        my_app_found = False

        for item in data.get("items", []):
            name = item["metadata"]["name"]
            phase = item["status"].get("phase", "Unknown")
            container_statuses = item["status"].get("containerStatuses", [])
            actual_status = phase
            restarts = 0

            for cs in container_statuses:
                restarts = cs.get("restartCount", 0)
                waiting = cs.get("state", {}).get("waiting", {})
                if waiting:
                    actual_status = waiting.get("reason", phase)

            # my-app ka koi bhi pod found karo
            if "my-app" in name:
                my_app_found = True
                if actual_status == "Running":
                    pass  # healthy hai
                else:
                    crashed.append({
                        "name": "my-app",
                        "status": actual_status,
                        "restarts": restarts
                    })

        # Agar my-app ka koi pod nahi mila
        if not my_app_found:
            # Deployment check karo
            dep = subprocess.run(
                ["kubectl", "get", "deployment", "my-app"],
                capture_output=True, text=True
            )
            if dep.returncode != 0:
                # Deployment bhi nahi hai — missing!
                crashed.append({
                    "name": "my-app",
                    "status": "Missing",
                    "restarts": 0
                })

        return crashed

    except Exception as e:
        log(f"Error: {e}", Fore.RED)
        return []

def fix_pod(pod, agent):
    global incident_count
    incident_count += 1
    pod_name = pod["name"]

    log(f"🚨 INCIDENT #{incident_count} | Pod: {pod_name} | {pod['status']}", Fore.RED)
    log(f"🤖 AI Agent fixing...", Fore.YELLOW)

    start = time.time()
    fix_file = tools.get_fix_file(pod_name)

    try:
        result = agent.invoke({
            "input": f"Pod '{pod_name}' is down ({pod['status']}). Apply fix using {fix_file} now.",
            "fix_file": fix_file
        })
        elapsed = round(time.time() - start, 1)

        log(f"✅ AUTO HEALED! | {pod_name} | {elapsed}s", Fore.GREEN)
        log(f"📧 Sending email...", Fore.CYAN)

        # Email alert
        send_incident_alert(
            pod_name=pod_name,
            status_was=pod["status"],
            fix_applied=fix_file,
            time_to_fix=elapsed,
            incident_num=incident_count
        )

        # Dashboard update
        send_to_dashboard(
            pod_name=pod_name,
            status_was=pod["status"],
            fix_applied=fix_file,
            time_to_fix=elapsed,
            incident_num=incident_count
        )

        fixed_pods[pod_name] = {
            "incident": incident_count,
            "status_was": pod["status"],
            "fixed_at": get_timestamp(),
            "resolution_time": elapsed,
            "attempts": fixed_pods.get(pod_name, {}).get("attempts", 0) + 1
        }
        return True

    except Exception as e:
        log(f"❌ Fix failed: {e}", Fore.RED)
        return False

def print_summary():
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"📊 SESSION SUMMARY")
    print(f"{'='*50}{Style.RESET_ALL}")
    print(f"Total Auto-Healed: {incident_count}")
    if fixed_pods:
        for pod_name, info in fixed_pods.items():
            print(f"  • {pod_name} — Fixed in {info['resolution_time']}s")
    print(f"{'='*50}\n")

def main():
    print_banner()

    log("🔄 Loading AI Agent...", Fore.YELLOW)
    agent = create_devops_agent()
    log("✅ Agent Ready!", Fore.GREEN)

    # Pehle sab clean karo
    subprocess.run(["kubectl", "delete", "deployment", "my-app",
                    "--ignore-not-found"], capture_output=True)
    time.sleep(2)

    # my-app deploy karo
    log("🚀 Deploying my-app...", Fore.YELLOW)
    deploy_my_app()
    time.sleep(5)  # Pod start hone do
    log("✅ my-app Deployment deployed!", Fore.GREEN)
    log("📌 Test: Run 'kubectl delete pod -l app=my-app' to test!\n", Fore.CYAN)
    log(f"👁️  Auto-healing active — checking every {CHECK_INTERVAL}s", Fore.CYAN)
    log("🌐 Dashboard: http://localhost:5000\n", Fore.CYAN)
    log("Press Ctrl+C to stop\n", Fore.YELLOW)

    cycle = 0
    try:
        while True:
            cycle += 1
            crashed = check_crashed_pods()

            if not crashed:
                log(f"✅ Cycle #{cycle} — my-app Running! ✅", Fore.GREEN)
            else:
                for pod in crashed:
                    attempts = fixed_pods.get(pod["name"], {}).get("attempts", 0)

                    if attempts >= MAX_FIX_ATTEMPTS:
                        log(f"⚠️  {pod['name']} — Max attempts! Manual needed.", Fore.YELLOW)
                        send_manual_intervention_alert(
                            pod_name=pod["name"],
                            incident_num=incident_count,
                            attempts=attempts
                        )
                    else:
                        fix_pod(pod, agent)

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print()
        log("⏹️  Stopped!", Fore.YELLOW)
        print_summary()

if __name__ == "__main__":
    main()