from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask_cors import CORS  # 👈 NEW

# ✅ Load environment variables
load_dotenv()

# ✅ Configure Gemini correctly using env variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)  # 👈 NEW

# ✅ Initialize Firebase Admin with Render's secret path
cred_path = os.environ.get("FIREBASE_CREDENTIAL_PATH")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Agentic City Pulse backend is live"})

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        print("Received data:", data)

        location = data.get("location", "Unknown")
        desc = data.get("description", "No details")
        report_id = data.get("id", "unknown")

        # 🧠 Gemini prompt
        prompt = f"""
        You are a smart city AI assistant. Summarize and give insights about the following issue:
        Location: {location}
        Description: {desc}
        """

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        summary = response.text.strip()

        print("Summary from Gemini:", summary)

        # ✅ Store result in Firestore
        db.collection("reports").document(report_id).set({
            "summary": summary,
            "status": "analyzed"
        }, merge=True)

        return jsonify({"status": "success", "summary": summary})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/healthz", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
