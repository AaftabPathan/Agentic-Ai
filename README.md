# 🤖 Agentic AI for DevOps
### Autonomous Incident Remediation Agent — Self-Healing Kubernetes Infrastructure

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![Ollama](https://img.shields.io/badge/Ollama-Llama3.2-orange)

---

## 🎯 Project Overview

An **AI-powered self-healing Kubernetes infrastructure** that autonomously monitors pods, detects failures, and applies fixes — all without human intervention.

> Pod crash hua → AI detect kiya → AI fix kiya → Email aaya → Done! ⚡

---

## 🚀 Features

- ✅ **24/7 Auto Monitoring** — Checks every 10 seconds
- ✅ **Auto Healing** — Fixes pods in 3-15 seconds
- ✅ **AI Scaling** — Automatically scales pods up/down
- ✅ **Gmail Alerts** — Email on every incident
- ✅ **Live Dashboard** — Real-time web UI
- ✅ **No Engineer Needed** — Fully autonomous!

---

## 🏗️ Architecture
┌─────────────────────────────────────────┐
│           monitor.py (24/7)             │
│  Checks every 10s → Detects crashes     │
├─────────────────────────────────────────┤
│           agent.py (AI Brain)           │
│  LangChain + Ollama (Llama 3.2)        │
│  ReAct Pattern — Think → Act → Fix     │
├─────────────────────────────────────────┤
│        kubernetes_client.py             │
│  kubectl commands — Real K8s API       │
├─────────────────────────────────────────┤
│           scaler.py (AI Scaling)        │
│  Auto scale pods based on health       │
├─────────────────────────────────────────┤
│      dashboard.py + alerts.py           │
│  Flask UI + Gmail SMTP alerts          │
└─────────────────────────────────────────┘

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python | Core language |
| LangChain | AI Agent framework |
| Ollama + Llama 3.2 | Local LLM (Free!) |
| Kubernetes (Minikube) | Container orchestration |
| Docker | Container runtime |
| Flask | Web dashboard |
| Gmail SMTP | Email alerts |
| kubectl | K8s CLI |

---

## 📁 Project Structure
agentic-ai-devops/
├── agent/
│   ├── init.py
│   ├── agent.py          # AI Brain
│   ├── tools.py          # AI Tools
│   └── kubernetes_client.py  # K8s API
├── k8s/
│   ├── my-app.yaml       # App deployment
│   └── my-app-fixed.yaml # Fixed version
├── monitor.py            # 24/7 Monitor
├── scaler.py             # AI Auto Scaling
├── dashboard.py          # Web Dashboard
├── alerts.py             # Gmail Alerts
└── README.md

---

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- Docker Desktop
- Minikube
- Ollama

### Installation

```bash
# 1. Clone karo
git clone https://github.com/USERNAME/agentic-ai-devops.git
cd agentic-ai-devops

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Dependencies install karo
pip install langchain-ollama colorama flask python-dotenv requests

# 4. Ollama model download karo
ollama pull llama3.2

# 5. .env file banao
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=your@gmail.com

# 6. Minikube start karo
minikube start --driver=docker
```

### Run Karo

```bash
# Terminal 1 - Ollama
ollama serve

# Terminal 2 - Dashboard
python dashboard.py

# Terminal 3 - Monitor
python monitor.py

# Terminal 4 - Scaler
python scaler.py
```

### Test Karo

```bash
# Pod delete karo — AI khud fix karega!
kubectl delete pod -l app=my-app
```

---

## 📊 Demo
[11:25:23] 🚨 INCIDENT #1 | Pod: my-app | ContainerCreating
[11:25:23] 🤖 AI Agent fixing...
[11:25:28] ✅ AUTO HEALED! | my-app | 4.6s
[11:25:28] 📧 Email sent!
[11:25:45] ✅ Cycle #81 — my-app Running! ✅

---

## 🎯 Real World Use Case
Company Server Crash → AI detects in 10s
→ Logs analyze kiye
→ Fix apply kiya in 5s
→ Email alert gaya
→ Engineer ko pata bhi nahi chala!

---

## 👨‍💻 Author

**Aaftab Aayub Pathan**
- DevOps + AI Engineer

```
kubectl delete pod → AI detects → AI fixes → Email sent → Dashboard updated
```
