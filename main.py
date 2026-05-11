# main.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import Fore, Style, init
from agent import create_devops_agent
import agent.tools as tools
import subprocess
import time

init(autoreset=True)

def print_banner():
    print(f"""
{Fore.CYAN}
╔════════════════════════════════════════════════════╗
║   🤖 REAL AGENTIC AI FOR DEVOPS                   ║
║   Autonomous Incident Remediation — Minikube K8s  ║
╚════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

def deploy_crash_app():
    print(f"{Fore.YELLOW}🚀 Deploying crash-app to Kubernetes...{Style.RESET_ALL}")
    subprocess.run(["kubectl", "delete", "pod", "crash-app", "--ignore-not-found"],
                   capture_output=True)
    result = subprocess.run(
        ["kubectl", "apply", "-f", "k8s/crash-app.yaml"],
        capture_output=True, text=True
    )
    print(result.stdout)
    print(f"{Fore.YELLOW}⏳ Waiting 20 seconds for pod to crash...{Style.RESET_ALL}")
    time.sleep(20)

def main():
    print_banner()
    print(f"{Fore.GREEN}✅ Starting Real DevOps AI Agent...{Style.RESET_ALL}\n")

    deploy_crash_app()

    print(f"\n{Fore.CYAN}📊 INITIAL CLUSTER STATUS:{Style.RESET_ALL}")
    print(tools.get_cluster_status())

    input(f"\n{Fore.YELLOW}▶ Press ENTER to start AI Agent remediation...{Style.RESET_ALL}")

    print(f"\n{Fore.MAGENTA}🤖 AI AGENT STARTING...{Style.RESET_ALL}")
    agent = create_devops_agent()

    task = """
    A pod named 'crash-app' has crashed in our Kubernetes cluster.
    Check cluster status, get pod logs, apply fix using k8s/healthy-app.yaml,
    verify cluster is healthy again.
    """

    result = agent.invoke({"input": task})

    print(f"\n{'='*50}")
    print(f"{Fore.GREEN}🎯 AGENT FINAL REPORT:{Style.RESET_ALL}")
    print(f"{'='*50}")
    print(result["output"])

    print(f"\n{Fore.CYAN}📊 FINAL CLUSTER STATUS:{Style.RESET_ALL}")
    print(tools.get_cluster_status())

if __name__ == "__main__":
    main()