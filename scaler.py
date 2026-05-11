# scaler.py
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
from langchain_ollama import OllamaLLM

init(autoreset=True)

CHECK_INTERVAL = 30
MIN_PODS = 1
MAX_PODS = 5
DEPLOYMENT_NAME = "my-app"

llm = OllamaLLM(model="llama3.2", temperature=0)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(message, color=Fore.WHITE):
    print(f"{color}[{get_timestamp()}] {message}{Style.RESET_ALL}")

def print_banner():
    print(f"{Fore.MAGENTA}")
    print("╔══════════════════════════════════════════════════╗")
    print("║  🤖 AGENTIC AI — INTELLIGENT AUTO SCALING       ║")
    print("║  AI Powered Kubernetes Pod Scaling               ║")
    print("╚══════════════════════════════════════════════════╝")
    print(f"{Style.RESET_ALL}")

def get_current_replicas():
    try:
        result = subprocess.run(
            ["kubectl", "get", "deployment", DEPLOYMENT_NAME,
             "-o", "jsonpath={.spec.replicas}"],
            capture_output=True, text=True
        )
        return int(result.stdout.strip()) if result.stdout.strip() else 1
    except:
        return 1

def get_cluster_info():
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-o", "json"],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        current_replicas = get_current_replicas()
        running_pods = 0
        crashed_pods = 0
        total_restarts = 0

        for item in data.get("items", []):
            name = item["metadata"]["name"]
            if DEPLOYMENT_NAME not in name:
                continue

            phase = item["status"].get("phase", "Unknown")
            container_statuses = item["status"].get("containerStatuses", [])
            actual_status = phase

            for cs in container_statuses:
                restarts = cs.get("restartCount", 0)
                total_restarts += restarts
                waiting = cs.get("state", {}).get("waiting", {})
                if waiting:
                    actual_status = waiting.get("reason", phase)

            if actual_status == "Running":
                running_pods += 1
            else:
                crashed_pods += 1

        return {
            "current_replicas": current_replicas,
            "running_pods": running_pods,
            "crashed_pods": crashed_pods,
            "total_restarts": total_restarts
        }
    except Exception as e:
        return None

def ai_decide_scaling(info):
    """AI se scaling decision lo — simple logic"""

    # Simple rule-based decision — AI verify karega
    crashed = info['crashed_pods']
    restarts = info['total_restarts']
    current = info['current_replicas']
    running = info['running_pods']

    # Simple rules pehle apply karo
    if crashed == 0 and restarts == 0 and current > 1:
        suggested = current - 1  # Scale down
    elif crashed > 0:
        suggested = min(current + 1, MAX_PODS)  # Scale up
    else:
        suggested = current  # Keep same

    # AI se confirm karo
    prompt = f"""Kubernetes scaling decision needed.

FACTS (use ONLY these):
- current_replicas: {current}
- running_pods: {running}
- crashed_pods: {crashed}
- total_restarts: {restarts}
- min_pods: {MIN_PODS}
- max_pods: {MAX_PODS}

RULES:
- crashed_pods == 0 AND restarts == 0 AND current == 1: keep 1 (perfect)
- crashed_pods == 0 AND restarts == 0 AND current > 1: decrease by 1
- crashed_pods > 0: increase by 1
- Never go below {MIN_PODS} or above {MAX_PODS}

RESPOND ONLY IN THIS FORMAT:
DECISION: {suggested}
REASON: one line explanation"""

    try:
        response = llm.invoke(prompt)
        decision = suggested
        reason = "Rule based decision"

        for line in response.strip().split('\n'):
            if line.startswith("DECISION:"):
                try:
                    decision = int(line.replace("DECISION:", "").strip())
                except:
                    decision = suggested
            elif line.startswith("REASON:"):
                reason = line.replace("REASON:", "").strip()

        # Validate
        decision = max(MIN_PODS, min(MAX_PODS, decision))
        return decision, reason

    except Exception as e:
        return suggested, "Rule based decision"

def scale_deployment(replicas):
    try:
        result = subprocess.run(
            ["kubectl", "scale", "deployment", DEPLOYMENT_NAME,
             f"--replicas={replicas}"],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except:
        return False

def main():
    print_banner()

    log("🤖 AI Scaling Agent starting...", Fore.YELLOW)
    log(f"📊 Monitoring: {DEPLOYMENT_NAME}", Fore.CYAN)
    log(f"📈 Scale range: {MIN_PODS} — {MAX_PODS} pods", Fore.CYAN)
    log(f"⏱️  Check interval: {CHECK_INTERVAL}s", Fore.CYAN)
    log("Press Ctrl+C to stop\n", Fore.YELLOW)

    # Pehle reset karo
    log("🔄 Resetting to 1 pod...", Fore.YELLOW)
    scale_deployment(1)
    time.sleep(3)
    log("✅ Reset done!\n", Fore.GREEN)

    cycle = 0
    try:
        while True:
            cycle += 1
            log(f"--- Scaling Check #{cycle} ---", Fore.CYAN)

            info = get_cluster_info()
            if not info:
                log("❌ Could not get cluster info!", Fore.RED)
                time.sleep(CHECK_INTERVAL)
                continue

            current = info['current_replicas']
            running = info['running_pods']
            crashed = info['crashed_pods']
            restarts = info['total_restarts']

            log(f"📊 Pods: {current} total | "
                f"{running} running | "
                f"{crashed} crashed | "
                f"{restarts} restarts", Fore.WHITE)

            # AI decision
            log("🤖 AI deciding...", Fore.YELLOW)
            new_replicas, reason = ai_decide_scaling(info)

            if new_replicas > current:
                log(f"📈 SCALE UP: {current} → {new_replicas}", Fore.GREEN)
                log(f"🧠 Reason: {reason}", Fore.YELLOW)
                scale_deployment(new_replicas)
                log(f"✅ Scaled to {new_replicas} pods!", Fore.GREEN)

            elif new_replicas < current:
                log(f"📉 SCALE DOWN: {current} → {new_replicas}", Fore.CYAN)
                log(f"🧠 Reason: {reason}", Fore.YELLOW)
                scale_deployment(new_replicas)
                log(f"✅ Scaled to {new_replicas} pods!", Fore.CYAN)

            else:
                log(f"✅ No change needed — {current} pod optimal", Fore.GREEN)
                log(f"🧠 Reason: {reason}", Fore.YELLOW)

            log(f"⏳ Next check in {CHECK_INTERVAL}s...\n", Fore.WHITE)
            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print()
        log("⏹️  Scaler stopped!", Fore.YELLOW)

if __name__ == "__main__":
    main()