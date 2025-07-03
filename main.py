from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)

# ✅ Initialize Firebase Admin with Render's secret file path
cred = credentials.Certificate("firebase-service-account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Agentic City Pulse backend is live"})

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        print("Received data:", data)  # 🐞 Debug print

        location = data.get("location", "Unknown")
        desc = data.get("description", "No details")
        report_id = data.get("id", "unknown")

        summary = f"Event at {location}: {desc}"
        print("Summary generated:", summary)  # 🐞 Debug print

        db.collection("reports").document(report_id).set({
            "summary": summary,
            "status": "analyzed"
        }, merge=True)

        return jsonify({"status": "success", "summary": summary})

    except Exception as e:
        print("❌ ERROR:", e)  # 🐞 Print actual error to terminal
        return jsonify({"error": str(e)}), 500

# ✅ Add health check route for Render monitoring
@app.route("/healthz", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# ✅ Use Render's PORT environment variable
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
