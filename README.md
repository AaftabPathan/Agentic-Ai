# 🤖 Agentic AI for DevOps — Self-Healing Kubernetes System 🚀

🚀 An AI-powered DevOps automation system that continuously monitors a Kubernetes cluster ☸️,
detects failures 🚨, 
automatically heals applications 🔧,
performs intelligent auto-scaling 📈,
and sends real-time alerts 📧 using an LLM-based agent (Ollama + Llama 3.2 🧠).

This project simulates a **production-grade self-healing infrastructure**, where AI acts as an autonomous DevOps engineer.

## 🌍 Real-World Integration

This project works at the Kubernetes infrastructure layer ☸️, where real-world applications like Amazon, Flipkart, Swiggy, and Zomato run their backend microservices. Instead of interacting with frontend apps directly, it monitors and manages backend services running inside Kubernetes pods, detects failures 🚨, automatically applies fixes 🔧, restarts or redeploys applications 🔄, and scales resources 📈 during high traffic. In production systems, this type of AI-driven automation is used for self-healing infrastructure, reducing downtime, improving reliability, and minimizing manual DevOps intervention, making the system behave like an autonomous operations engineer managing cloud applications in real time.
---

## ⚡ Key Capabilities
- 👀 Continuous Kubernetes cluster monitoring  
- 🚨 Automatic pod failure detection  
- 🧠 AI-powered log analysis & decision making  
- 🔧 Self-healing pod recovery using kubectl  
- 🔄 Automatic restart & redeployment  
- 📈 Smart auto-scaling based on workload  
- 🌐 Real-time dashboard for observability  
- 📧 Email notifications for incidents  

---

## 🏗️ System Architecture

monitor.py → Cluster watcher & incident detector 👀  
agent/agent.py → AI decision engine (LLM brain) 🧠  
tools.py → Kubernetes action executor ⚙️  
kubernetes_client.py → Kubernetes API interaction layer ☸️  
scaler.py → Intelligent auto-scaling system 📈  
alerts.py → Email + dashboard notification system 📧  
dashboard.py → Real-time Flask monitoring UI 🌐  

---

## 🧰 Tech Stack
🐍 Python 3.9+  
☸️ Kubernetes (Minikube)  
🐳 Docker  
🧠 Ollama (Llama 3.2)  
🔗 LangChain  
🌐 Flask  
⚙️ kubectl  
📧 SMTP (Gmail Alerts)  

---

## ⚙️ Setup Guide (Step-by-Step)

### 1️⃣ Clone Repository
👉 Get the project locally
git clone https://github.com/your-username/Agentic-Ai.git  
cd Agentic-Ai  

---

### 2️⃣ Setup Virtual Environment
👉 Isolate dependencies
python -m venv venv 

Activate Environment
Windows:
venv\Scripts\activate  

Linux / Mac:
source venv/bin/activate
---

### 3️⃣ Install Dependencies
👉 Required Python packages
pip install langchain-ollama flask python-dotenv colorama requests  

---

### 4️⃣ Start Kubernetes Cluster
👉 Local cluster setup using Minikube
minikube start --driver=docker  

---

### 5️⃣ Setup AI Model (Ollama)
👉 Local LLM setup
ollama pull llama3.2  
ollama serve  

---

### 6️⃣ Configure Email Alerts
👉 Create `.env` file for notifications

EMAIL_SENDER=your_email@gmail.com  
EMAIL_PASSWORD=your_app_password  
EMAIL_RECEIVER=receiver_email@gmail.com  

---

## 🚀 Run the System

### 🌐 Start Dashboard (Observability UI)
👉 View cluster health in browser
python dashboard.py  

---

### 🤖 Start AI Monitoring Engine
👉 Detect + auto-fix failures
python monitor.py  

---

### 📈 Start Auto Scaling Engine
👉 Dynamic scaling based on workload
python scaler.py  

---

## 🧪 Testing the System

👉 Simulate failure:
kubectl delete pod -l app=my-app  

---

## ⚡ What Happens Automatically

🚨 Failure is detected  
🧠 AI analyzes logs & state  
🔧 Fix is applied automatically  
🔄 Pod is restarted or redeployed  
📈 Cluster is scaled if required  
📧 Email alert is sent  
🌐 Dashboard updates in real-time  

---
## 📊 Dashboard Features
• Live pod status
• Healthy vs crashed pods
• Incident history
• Auto refresh every 10 seconds
• Real-time timestamps

## 📧 Email Alerts

## System sends emails for:

🚨 Incident detected
✅ Incident resolved
⚠️ Manual intervention required


## 🧠 AI Behavior

## AI works in 3 phases:

1. Observe
cluster state read
2. Decide
logs + reasoning via LLM
3. Act
kubectl commands execute


## 🧪 Example Workflow:
Pod crashes →
Monitor detects →
AI analyzes logs →
Fix YAML applied →
Pod restored →
Email sent →
Dashboard updated

## ⚠️ Important Notes:
➡ Minikube must be running
➡ Ollama server must be active
➡ kubectl configured properly
➡ Gmail app password required

## 🔥 Troubleshooting:-
## ❌ kubectl not found
Install kubectl and restart terminal

## ❌ Ollama error
ollama serve

## ❌ Email not sending
check .env
use app password not normal password


## 👨‍💻 Author
Aaftab Pathan  
💡 DevOps + AI Engineer  
🚀 Kubernetes Automation Enthusiast  

---

## 🚀 Future Improvements
Prometheus integration
Grafana dashboards
Predictive scaling (ML model)
Multi-cluster support
SaaS deployment version

## ⭐ Project Highlight
This project demonstrates a real-world **AI-driven self-healing DevOps system**, capable of autonomous infrastructure management with zero manual intervention.

## ⭐ Star this repo if you like it
“AI is not replacing DevOps engineers — it is upgrading them.”
