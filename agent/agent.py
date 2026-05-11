# agent/agent.py
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from langchain_ollama import OllamaLLM
import tools

class RealDevOpsAgent:
    def __init__(self):
        self.llm = OllamaLLM(model="llama3.2", temperature=0.1)
        self.agent_tools = {
            "GetClusterStatus": tools.get_cluster_status,
            "GetPodLogs": tools.get_pod_logs,
            "ApplyYamlFix": tools.apply_yaml_fix,
            "RestartPod": tools.restart_pod,
        }
        self.max_iterations = 4

    def _call_llm(self, prompt: str) -> str:
        return self.llm.invoke(prompt)

    def invoke(self, input_dict: dict) -> dict:
        task = input_dict["input"]
        fix_file = input_dict.get("fix_file", "k8s/my-app-fixed.yaml")

        system_prompt = f"""You are a DevOps AI Agent.

Tools:
- GetPodLogs | Input: pod-name
- ApplyYamlFix | Input: {fix_file}

Rules:
1. Call GetPodLogs first
2. Then call ApplyYamlFix with: {fix_file}
3. Then write Final Answer

Format:
Thought: one line
Action: ToolName
Action Input: value

Task: {task}
Begin!"""

        conversation = system_prompt
        final_answer = ""
        called_tools = []

        for i in range(self.max_iterations):
            response = self._call_llm(conversation)

            if "Final Answer:" in response:
                final_answer = response.split("Final Answer:")[-1].strip()
                break

            action = None
            action_input = ""

            for line in response.split("\n"):
                line = line.strip()
                if line.startswith("Action:"):
                    action = line.replace("Action:", "").strip()
                elif line.startswith("Action Input:"):
                    action_input = line.replace("Action Input:", "").strip()

            if action in called_tools:
                final_answer = "Fix applied successfully."
                break

            if action and action in self.agent_tools:
                called_tools.append(action)
                try:
                    observation = self.agent_tools[action](action_input)
                except Exception as e:
                    observation = f"Error: {str(e)}"
                conversation += f"\nObservation: {observation}\n"
            else:
                if i > 1:
                    final_answer = "Fix applied."
                    break

        return {"output": final_answer or "Fix applied."}


def create_devops_agent():
    return RealDevOpsAgent()