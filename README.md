# 🤖 Agentic AI for DevOps — Self-Healing Kubernetes System 🚀

🚀 An AI-powered DevOps automation system that continuously monitors a Kubernetes cluster ☸️, detects failures 🚨, automatically heals applications 🔧, performs intelligent auto-scaling 📈, and sends real-time alerts 📧 using an LLM-based agent (Ollama + Llama 3.2 🧠).

This project simulates a **production-grade self-healing infrastructure**, where AI acts as an autonomous DevOps engineer.

---

## 🌍 Real-World Integration

This project works at the Kubernetes infrastructure layer ☸️, where real-world applications like Amazon, Flipkart, Swiggy, and Zomato run their backend microservices. Instead of interacting with frontend apps, it manages backend services running inside Kubernetes pods, detects failures 🚨, automatically applies fixes 🔧, restarts or redeploys applications 🔄, and scales resources 📈 during high traffic. In production systems, this type of AI-driven automation is used for self-healing infrastructure, reducing downtime, improving reliability, and minimizing manual DevOps intervention.

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
agent/agent.py → AI decision engine 🧠  
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

## ⚙️ Setup & Run

### 1️⃣ Clone Repository
git clone https://github.com/your-username/Agentic-Ai.git  
cd Agentic-Ai  

---

### 2️⃣ Create Virtual Environment
python -m venv venv  

Activate:
Windows:
venv\Scripts\activate  

Linux/Mac:
source venv/bin/activate  

---

### 3️⃣ Install Dependencies
pip install langchain-ollama flask python-dotenv colorama requests  

---

### 4️⃣ Start Kubernetes
minikube start --driver=docker  

---

### 5️⃣ Start AI Model
ollama pull llama3.2  
ollama serve  

---

### 6️⃣ Configure Email (.env)
EMAIL_SENDER=your_email@gmail.com  
EMAIL_PASSWORD=your_app_password  
EMAIL_RECEIVER=receiver_email@gmail.com  

---

## 🚀 Run System

Dashboard:
python dashboard.py  

Monitor (Auto Healing):
python monitor.py  

Scaler:
python scaler.py  

---

## 🧪 Testing

kubectl delete pod -l app=my-app  

System will:
🚨 Detect failure  
🧠 Analyze logs  
🔧 Apply fix  
🔄 Restart pod  
📈 Scale if needed  
📧 Send alert  
🌐 Update dashboard  

---

## 📊 Dashboard Features
- Live pod status  
- Healthy vs crashed pods  
- Incident history  
- Auto-refresh every 10 seconds  

---

## 📧 Email Alerts
Sends notifications for:
- 🚨 Incident detected  
- ✅ Incident resolved  
- ⚠️ Manual intervention required  

---

## 🧠 AI Behavior Flow
Observe → Decide → Act  
(Kubernetes state → LLM reasoning → kubectl execution)

---

## ⚠️ Requirements
- Minikube running  
- Kubectl configured  
- Ollama server active  
- Gmail App Password required  

---

## 🔥 Troubleshooting
❌ kubectl not found → install kubectl  
❌ Ollama error → run `ollama serve`  
❌ Email not working → check .env (use app password)  

---

## 👨‍💻 Author
Aaftab Pathan  
💡 DevOps + AI Engineer  
🚀 Kubernetes Automation Enthusiast  

---

## ⭐ Future Improvements
- Prometheus + Grafana integration  
- Predictive scaling (ML)  
- Multi-cluster support  
- Production SaaS deployment  

---

⭐ Star this repo if you like it  
💡 “AI is not replacing DevOps engineers — it is upgrading them.”
