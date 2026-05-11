# agent/tools.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from kubernetes_client import RealKubernetesClient
from colorama import Fore, Style, init

init(autoreset=True)
k8s = RealKubernetesClient()

FIX_FILES = {
    "my-app": "k8s/my-app-fixed.yaml",
    "web-app": "k8s/my-app-fixed.yaml",
    "crash-app": "k8s/my-app-fixed.yaml",
}

def get_cluster_status(x="") -> str:
    pods = k8s.get_all_pods()
    result = "\n📊 CLUSTER STATUS:\n"
    result += "-" * 40 + "\n"
    for pod in pods:
        icon = "✅" if pod["status"] == "Running" else "❌"
        result += f"{icon} {pod['name']} — {pod['status']}\n"
    result += "-" * 40 + "\n"
    return result

def get_pod_logs(pod_name: str) -> str:
    pod_name = pod_name.strip().strip("'\"")
    logs = k8s.get_pod_logs(pod_name)
    return f"LOGS:\n{logs[:500]}"

def apply_yaml_fix(yaml_file: str) -> str:
    yaml_file = yaml_file.strip().strip("'\"")
    return k8s.apply_yaml(yaml_file)

def restart_pod(pod_name: str) -> str:
    return k8s.delete_pod(pod_name.strip())

def get_fix_file(pod_name: str) -> str:
    for key, fix_file in FIX_FILES.items():
        if key in pod_name:
            return fix_file
    return "k8s/my-app-fixed.yaml"