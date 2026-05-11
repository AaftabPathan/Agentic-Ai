# dashboard.py
import sys
import os
import json
import subprocess
from datetime import datetime
from flask import Flask, jsonify, render_template_string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AGENT_DIR = os.path.join(BASE_DIR, 'agent')
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, AGENT_DIR)

app = Flask(__name__)

# Incident history store karo
incidents = []

def get_pods():
    """Real kubectl se pods lao"""
    try:
        result = subprocess.run(
            ["kubectl", "get", "pods", "-o", "json"],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)
        pods = []

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

            pods.append({
                "name": name,
                "status": actual_status,
                "restarts": restarts,
                "healthy": actual_status == "Running"
            })

        return pods
    except:
        return []

def get_stats():
    """Stats calculate karo"""
    pods = get_pods()
    total = len(pods)
    healthy = sum(1 for p in pods if p["healthy"])
    crashed = total - healthy

    return {
        "total_pods": total,
        "healthy_pods": healthy,
        "crashed_pods": crashed,
        "total_incidents": len(incidents),
        "last_updated": datetime.now().strftime("%H:%M:%S")
    }

# ─── HTML Template ───────────────────────────────────

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 DevOps AI Agent Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', sans-serif;
            background: #0f1117;
            color: #ffffff;
            min-height: 100vh;
        }

        .header {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            padding: 20px 40px;
            border-bottom: 2px solid #00d4ff;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .header h1 {
            font-size: 24px;
            color: #00d4ff;
        }

        .header .status {
            background: #00ff88;
            color: #000;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }

        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }

        /* Stats Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: #1a1a2e;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #2a2a4a;
            transition: transform 0.2s;
        }

        .stat-card:hover { transform: translateY(-3px); }

        .stat-card .number {
            font-size: 40px;
            font-weight: bold;
            margin-bottom: 8px;
        }

        .stat-card .label {
            color: #888;
            font-size: 13px;
        }

        .stat-card.healthy .number { color: #00ff88; }
        .stat-card.crashed .number { color: #ff4444; }
        .stat-card.total .number { color: #00d4ff; }
        .stat-card.incidents .number { color: #ffaa00; }

        /* Pods Section */
        .section {
            background: #1a1a2e;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid #2a2a4a;
        }

        .section h2 {
            font-size: 18px;
            margin-bottom: 20px;
            color: #00d4ff;
            border-bottom: 1px solid #2a2a4a;
            padding-bottom: 10px;
        }

        .pod-card {
            display: flex;
            align-items: center;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            background: #0f1117;
            border: 1px solid #2a2a4a;
            transition: all 0.3s;
        }

        .pod-card:hover { border-color: #00d4ff; }

        .pod-indicator {
            width: 14px;
            height: 14px;
            border-radius: 50%;
            margin-right: 15px;
            flex-shrink: 0;
        }

        .pod-indicator.running {
            background: #00ff88;
            box-shadow: 0 0 8px #00ff88;
            animation: pulse 2s infinite;
        }

        .pod-indicator.crashed {
            background: #ff4444;
            box-shadow: 0 0 8px #ff4444;
        }

        .pod-name {
            font-weight: bold;
            font-size: 16px;
            flex: 1;
        }

        .pod-status {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 15px;
        }

        .pod-status.running {
            background: rgba(0, 255, 136, 0.15);
            color: #00ff88;
            border: 1px solid #00ff88;
        }

        .pod-status.crashed {
            background: rgba(255, 68, 68, 0.15);
            color: #ff4444;
            border: 1px solid #ff4444;
        }

        .pod-restarts {
            color: #888;
            font-size: 13px;
        }

        .no-pods {
            text-align: center;
            color: #888;
            padding: 30px;
            font-size: 15px;
        }

        /* Incidents Table */
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            text-align: left;
            padding: 12px;
            color: #888;
            font-size: 13px;
            border-bottom: 1px solid #2a2a4a;
        }

        td {
            padding: 12px;
            border-bottom: 1px solid #1a1a2e;
            font-size: 14px;
        }

        tr:hover td { background: #0f1117; }

        .badge-fixed {
            background: rgba(0, 255, 136, 0.15);
            color: #00ff88;
            border: 1px solid #00ff88;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 12px;
        }

        .no-incidents {
            text-align: center;
            color: #888;
            padding: 30px;
        }

        /* Last Updated */
        .footer {
            text-align: center;
            color: #555;
            font-size: 12px;
            padding: 20px;
        }

        /* Auto refresh indicator */
        .refresh-bar {
            height: 3px;
            background: #00d4ff;
            animation: shrink 10s linear infinite;
            border-radius: 3px;
            margin-bottom: 20px;
        }

        @keyframes shrink {
            from { width: 100%; }
            to { width: 0%; }
        }
    </style>

    <script>
        // Har 10 second mein auto refresh
        setTimeout(() => location.reload(), 10000);

        // Live time update
        function updateTime() {
            const el = document.getElementById('live-time');
            if (el) el.textContent = new Date().toLocaleTimeString();
        }
        setInterval(updateTime, 1000);
    </script>
</head>
<body>

<div class="header">
    <div>
        <h1>🤖 DevOps AI Agent — Live Dashboard</h1>
        <p style="color: #888; font-size: 13px; margin-top: 4px;">
            Agentic AI for DevOps — Self Healing Infrastructure
        </p>
    </div>
    <div>
        <div class="status">🟢 MONITORING ACTIVE</div>
        <p style="color: #555; font-size: 12px; text-align: right; margin-top: 6px;">
            🕐 <span id="live-time"></span>
        </p>
    </div>
</div>

<div class="container">

    <!-- Auto refresh bar -->
    <div class="refresh-bar"></div>

    <!-- Stats Cards -->
    <div class="stats-grid">
        <div class="stat-card total">
            <div class="number">{{ stats.total_pods }}</div>
            <div class="label">Total Pods</div>
        </div>
        <div class="stat-card healthy">
            <div class="number">{{ stats.healthy_pods }}</div>
            <div class="label">✅ Healthy</div>
        </div>
        <div class="stat-card crashed">
            <div class="number">{{ stats.crashed_pods }}</div>
            <div class="label">❌ Crashed</div>
        </div>
        <div class="stat-card incidents">
            <div class="number">{{ stats.total_incidents }}</div>
            <div class="label">🔧 Auto Fixed</div>
        </div>
    </div>

    <!-- Pods Status -->
    <div class="section">
        <h2>📦 Pod Status — Live</h2>

        {% if pods %}
            {% for pod in pods %}
            <div class="pod-card">
                <div class="pod-indicator {{ 'running' if pod.healthy else 'crashed' }}"></div>
                <div class="pod-name">{{ pod.name }}</div>
                <div class="pod-status {{ 'running' if pod.healthy else 'crashed' }}">
                    {{ pod.status }}
                </div>
                <div class="pod-restarts">🔄 Restarts: {{ pod.restarts }}</div>
            </div>
            {% endfor %}
        {% else %}
            <div class="no-pods">No pods found. Deploy a pod first!</div>
        {% endif %}
    </div>

    <!-- Incidents History -->
    <div class="section">
        <h2>🚨 Incident History</h2>

        {% if incidents %}
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Pod</th>
                    <th>Was</th>
                    <th>Fix Applied</th>
                    <th>Time</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {% for inc in incidents|reverse %}
                <tr>
                    <td>#{{ inc.id }}</td>
                    <td><b>{{ inc.pod }}</b></td>
                    <td style="color: #ff4444;">{{ inc.status_was }}</td>
                    <td style="color: #888;">{{ inc.fix_file }}</td>
                    <td style="color: #00d4ff;">{{ inc.time_to_fix }}s</td>
                    <td><span class="badge-fixed">✅ FIXED</span></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% else %}
            <div class="no-incidents">
                No incidents yet! Kill a pod to see auto-healing in action 🚀
            </div>
        {% endif %}
    </div>

</div>

<div class="footer">
    Last updated: {{ stats.last_updated }} | Auto-refreshes every 10 seconds
</div>

</body>
</html>
"""

# ─── Routes ──────────────────────────────────────────

@app.route("/")
def index():
    pods = get_pods()
    stats = get_stats()
    return render_template_string(HTML, pods=pods, stats=stats, incidents=incidents)

@app.route("/api/pods")
def api_pods():
    return jsonify(get_pods())

@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats())

@app.route("/api/incident", methods=["POST"])
def add_incident():
    """Monitor.py se incident data receive karo"""
    from flask import request
    data = request.json
    incidents.append({
        "id": len(incidents) + 1,
        "pod": data.get("pod_name"),
        "status_was": data.get("status_was"),
        "fix_file": data.get("fix_applied"),
        "time_to_fix": data.get("time_to_fix"),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    return jsonify({"ok": True})

if __name__ == "__main__":
    print("\n🌐 Dashboard starting...")
    print("👉 Open: http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False)