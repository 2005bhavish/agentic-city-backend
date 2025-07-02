from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)

# Init Firebase Admin
cred = credentials.Certificate("firebase-service-account.json")  # <-- download from Firebase console
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Agentic City Pulse backend is live"})

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    location = data.get("location", "Unknown")
    desc = data.get("description", "No details")
    report_id = data.get("id", "unknown")

    # 🧠 Here you'll add Gemini analysis later
    summary = f"Event at {location}: {desc}"

    db.collection("reports").document(report_id).set({
        "summary": summary,
        "status": "analyzed"
    }, merge=True)

    return jsonify({"status": "success", "summary": summary})
