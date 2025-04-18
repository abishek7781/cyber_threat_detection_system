import threading
import time
import datetime
import random
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

monitoring_data = {
    "website": None,
    "threat_detected": False,
    "status": "Idle",
    "threat_logs": []
}

stop_event = threading.Event()

threat_names = [
    "Phishing Attack",
    "Ransomware",
    "SQL Injection",
    "Cross-Site Scripting",
    "DDoS Attack",
    "Zero-Day Exploit"
]

threat_solutions = {
    "Phishing Attack": "Educate users to recognize phishing emails and avoid clicking suspicious links.",
    "Ransomware": "Maintain regular backups and use updated antivirus software.",
    "SQL Injection": "Use parameterized queries and input validation to prevent injection.",
    "Cross-Site Scripting": "Implement proper input sanitization and Content Security Policy.",
    "DDoS Attack": "Use traffic filtering and rate limiting to mitigate attacks.",
    "Zero-Day Exploit": "Keep software updated and apply security patches promptly."
}

def threat_detection_simulator():
    print("Threat detection simulator thread started.")
    while True:
        print(f"Threat detection loop: monitoring_data['website'] = {monitoring_data['website']}")
        if monitoring_data["website"]:
            monitoring_data["status"] = "Monitoring"
            print(f"Monitoring {monitoring_data['website']}, current threat_detected: {monitoring_data['threat_detected']}")
            # Simulate threat detection logic
            new_threat_status = not monitoring_data["threat_detected"]
            monitoring_data["threat_detected"] = new_threat_status
            if new_threat_status:
                threat_name = random.choice(threat_names)
                domain = monitoring_data["website"]
                if domain.startswith("http://"):
                    domain = domain[len("http://"):]
                elif domain.startswith("https://"):
                    domain = domain[len("https://"):]
                solution = threat_solutions.get(threat_name, "No solution available.")
                monitoring_data["threat_logs"].append({
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "website": monitoring_data["website"],
                    "threat_name": threat_name,
                    "domain": domain,
                    "message": "Threat detected",
                    "solution": solution
                })
                print(f"Threat detected: {threat_name} on {monitoring_data['website']}")
            else:
                print("No threat detected this cycle.")
            # Wait for stop_event or timeout 5 seconds for faster updates
            stop_event.wait(5)
            stop_event.clear()
        else:
            print("No website to monitor, idling.")
            monitoring_data["status"] = "Idle"
            monitoring_data["threat_detected"] = False
            monitoring_data["threat_logs"] = []
            stop_event.wait(1)
            stop_event.clear()

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    data = request.json
    website = data.get("website")
    print(f"Received start monitoring request for website: {website}")
    if not website:
        return jsonify({"error": "Website URL is required"}), 400
    monitoring_data["website"] = website
    monitoring_data["threat_detected"] = False
    monitoring_data["status"] = "Monitoring"  # Set immediately to Monitoring
    monitoring_data["threat_logs"] = []
    stop_event.clear()
    print(f"Set monitoring_data['website'] to: {monitoring_data['website']}")
    return jsonify({"message": f"Started monitoring {website}"}), 200

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    print(f"Stop monitoring request received. Current website: {monitoring_data['website']}")
    monitoring_data["website"] = None
    print(f"Set monitoring_data['website'] to: {monitoring_data['website']}")
    monitoring_data["threat_detected"] = False
    monitoring_data["status"] = "Idle"
    monitoring_data["threat_logs"] = []
    stop_event.set()
    return jsonify({"message": "Monitoring stopped"}), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": monitoring_data.get("status", "Idle"),
        "threat_detected": monitoring_data.get("threat_detected", False),
        "status_level": "danger" if monitoring_data.get("threat_detected", False) else "success"
    })

@app.route('/threat_logs', methods=['GET'])
def threat_logs():
    return jsonify(monitoring_data.get("threat_logs", []))

if __name__ == '__main__':
    print("Starting Flask app...")
    thread = threading.Thread(target=threat_detection_simulator, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5001, use_reloader=False)
