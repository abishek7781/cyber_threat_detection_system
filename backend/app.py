import threading
import time
import datetime
import random
import uuid
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

monitoring_data = {
    "website": None,
    "threat_detected": False,
    "status": "Idle",
    "threat_logs": []
}

stop_event = threading.Event()

# Define 30 different threat names for simulation
threat_names = [
    "Phishing Attack",
    "Ransomware",
    "SQL Injection",
    "Cross-Site Scripting",
    "DDoS Attack",
    "Zero-Day Exploit",
    "Malware Infection",
    "Trojan Horse",
    "Spyware",
    "Adware",
    "Rootkit",
    "Botnet",
    "Man-in-the-Middle",
    "Credential Stuffing",
    "Drive-by Download",
    "Watering Hole Attack",
    "Session Hijacking",
    "DNS Spoofing",
    "Privilege Escalation",
    "Code Injection",
    "Buffer Overflow",
    "Cryptojacking",
    "Logic Bomb",
    "Backdoor",
    "Exploit Kit",
    "Keylogger",
    "Rogue Software",
    "Social Engineering",
    "Supply Chain Attack",
    "Insider Threat"
]

threat_solutions = {
    "Phishing Attack": "Educate users to recognize phishing emails and avoid clicking suspicious links.",
    "Ransomware": "Maintain regular backups and use updated antivirus software.",
    "SQL Injection": "Use parameterized queries and input validation to prevent injection.",
    "Cross-Site Scripting": "Implement proper input sanitization and Content Security Policy.",
    "DDoS Attack": "Use traffic filtering and rate limiting to mitigate attacks.",
    "Zero-Day Exploit": "Keep software updated and apply security patches promptly.",
    "Malware Infection": "Use reputable antivirus and keep systems updated.",
    "Trojan Horse": "Avoid downloading software from untrusted sources.",
    "Spyware": "Use anti-spyware tools and monitor network traffic.",
    "Adware": "Install ad blockers and avoid suspicious websites.",
    "Rootkit": "Use rootkit detection tools and keep OS patched.",
    "Botnet": "Monitor network for unusual traffic and isolate infected devices.",
    "Man-in-the-Middle": "Use encrypted connections and VPNs.",
    "Credential Stuffing": "Implement multi-factor authentication and monitor login attempts.",
    "Drive-by Download": "Keep browsers and plugins updated.",
    "Watering Hole Attack": "Monitor trusted websites for compromise.",
    "Session Hijacking": "Use secure cookies and session management.",
    "DNS Spoofing": "Use DNSSEC and monitor DNS traffic.",
    "Privilege Escalation": "Apply least privilege principle and patch vulnerabilities.",
    "Code Injection": "Validate and sanitize all inputs.",
    "Buffer Overflow": "Use safe coding practices and memory protection.",
    "Cryptojacking": "Monitor CPU usage and block malicious scripts.",
    "Logic Bomb": "Audit code and monitor system behavior.",
    "Backdoor": "Conduct regular security audits and scans.",
    "Exploit Kit": "Keep software updated and use intrusion detection.",
    "Keylogger": "Use anti-keylogger software and secure input methods.",
    "Rogue Software": "Avoid installing unknown software and use trusted sources.",
    "Social Engineering": "Train employees and verify identities.",
    "Supply Chain Attack": "Vet suppliers and monitor software integrity.",
    "Insider Threat": "Implement access controls and monitor user activity."
}

# List of malicious URLs to trigger threat simulation
malicious_urls = [
    "https://urlhaus.abuse.ch/static/malware/2023/02/15/abcdef1234567890.exe",
    "http://secure-login-paypal.com/account-update",
    "https://urlhaus.abuse.ch/static/malware/2023/01/01/1a2b3c4d5e6f7g8h9i0j.exe",
    "http://phishing-example.com/login",
    "http://fakebank.phishingsite.com"
]

def threat_detection_simulator():
    print("Threat detection simulator thread started.")
    while True:
        if monitoring_data["website"]:
            monitoring_data["status"] = "Monitoring"
            url = monitoring_data["website"].strip().lower()
            safe_domains = ["google.com", "youtube.com", "facebook.com", "twitter.com", "linkedin.com", "wikipedia.org"]
            if any(safe_domain in url for safe_domain in safe_domains):
                monitoring_data["threat_detected"] = False
                monitoring_data["threat_logs"] = [{
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "threat_location": monitoring_data["website"],
                    "threat_name": "Safe Site",
                    "domain": monitoring_data["website"],
                    "message": f"URL {monitoring_data['website']} is in safe domains whitelist. No threats detected.",
                    "solution": "No action needed.",
                    "severity": "Low",
                    "malware_family": "",
                    "platform_type": "",
                    "threat_entry_type": "",
                    "cache_duration": ""
                }]
                print(f"URL {monitoring_data['website']} is in safe domains whitelist. No threats detected.")
            elif url in malicious_urls:
                monitoring_data["threat_detected"] = True
                monitoring_data["threat_logs"] = []
                for _ in range(30):
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
                        "threat_location": monitoring_data["website"],
                        "threat_name": threat_name,
                        "domain": domain,
                        "message": "Threat detected",
                        "solution": solution,
                        "severity": random.choice(["Low", "Medium", "High", "Critical"]),
                        "malware_family": "Unknown",
                        "platform_type": "Unknown",
                        "threat_entry_type": "Unknown",
                        "cache_duration": "N/A"
                    })
                print(f"Simulated 30 threat detections on {monitoring_data['website']}")
            else:
                monitoring_data["threat_detected"] = False
                monitoring_data["threat_logs"] = [{
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "threat_location": monitoring_data["website"],
                    "threat_name": "Safe Site",
                    "domain": monitoring_data["website"],
                    "message": "The URL is safe. No threat will be detected on this site.",
                    "solution": "No action needed.",
                    "severity": "Low",
                    "malware_family": "",
                    "platform_type": "",
                    "threat_entry_type": "",
                    "cache_duration": ""
                }]
                print(f"URL {monitoring_data['website']} is safe. No threats detected.")
        else:
            monitoring_data["status"] = "Idle"
            monitoring_data["threat_detected"] = False
            monitoring_data["threat_logs"] = []
        stop_event.wait(12)
        stop_event.clear()

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    data = request.json
    website = data.get("website")
    if not website:
        return jsonify({"error": "Website URL is required"}), 400
    monitoring_data["website"] = website
    monitoring_data["threat_detected"] = False
    monitoring_data["status"] = "Monitoring"
    monitoring_data["threat_logs"] = []
    stop_event.clear()
    return jsonify({"message": f"Started monitoring {website}"}), 200

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    monitoring_data["website"] = None
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

def event_stream():
    last_log_count = 0
    while True:
        if monitoring_data["website"]:
            logs = monitoring_data["threat_logs"]
            if len(logs) != last_log_count:
                data = f"data: {json.dumps(logs)}\n\n"
                yield data
                last_log_count = len(logs)
        time.sleep(2)

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    print("Starting Flask app...")
    thread = threading.Thread(target=threat_detection_simulator, daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=5001, use_reloader=False)
