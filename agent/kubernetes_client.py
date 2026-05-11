# agent/kubernetes_client.py
import subprocess
import json

class RealKubernetesClient:

    def get_all_pods(self, namespace="default"):
        try:
            result = subprocess.run(
                ["kubectl", "get", "pods", "-n", namespace, "-o", "json"],
                capture_output=True, text=True
            )
            data = json.loads(result.stdout)
            pods = []
            for item in data.get("items", []):
                name = item["metadata"]["name"]
                phase = item["status"].get("phase", "Unknown")
                container_statuses = item["status"].get("containerStatuses", [])
                restart_count = 0
                actual_status = phase
                for cs in container_statuses:
                    restart_count = cs.get("restartCount", 0)
                    waiting = cs.get("state", {}).get("waiting", {})
                    if waiting:
                        actual_status = waiting.get("reason", phase)
                pods.append({
                    "name": name,
                    "status": actual_status,
                    "restarts": restart_count,
                    "namespace": namespace
                })
            return pods
        except Exception as e:
            return []

    def get_pod_logs(self, pod_name, namespace="default", lines=30):
        try:
            result = subprocess.run(
                ["kubectl", "logs", pod_name, "-n", namespace,
                 f"--tail={lines}", "--previous"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout
            result = subprocess.run(
                ["kubectl", "logs", pod_name, "-n", namespace, f"--tail={lines}"],
                capture_output=True, text=True
            )
            return result.stdout if result.stdout else result.stderr
        except Exception as e:
            return f"Log error: {str(e)}"

    def get_pod_description(self, pod_name, namespace="default"):
        try:
            result = subprocess.run(
                ["kubectl", "describe", "pod", pod_name, "-n", namespace],
                capture_output=True, text=True
            )
            return result.stdout
        except Exception as e:
            return f"Describe error: {str(e)}"

    def apply_yaml(self, yaml_file):
        try:
            result = subprocess.run(
                ["kubectl", "apply", "-f", yaml_file],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return f"Applied successfully!\n{result.stdout}"
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Apply error: {str(e)}"

    def delete_pod(self, pod_name, namespace="default"):
        try:
            result = subprocess.run(
                ["kubectl", "delete", "pod", pod_name,
                 "-n", namespace, "--ignore-not-found"],
                capture_output=True, text=True
            )
            return result.stdout
        except Exception as e:
            return f"Delete error: {str(e)}"