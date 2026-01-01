from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Create Flask app
app = Flask(__name__)

# Load Firebase service account key
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize Firebase Admin
firebase_admin.initialize_app(cred, {
    "storageBucket": "skillbridge-5195a.appspot.com"
})

# Firestore database reference
db = firestore.client()

# Firebase Storage bucket reference
bucket = storage.bucket()

@app.route("/")
def home():
    return "SkillBridge Backend + Firebase Connected"
@app.route("/test-db")
def test_db():
    test_ref = db.collection("test").document("ping")
    test_ref.set({"status": "ok"})
    return "Firestore working"


if __name__ == "__main__":
    app.run(debug=True)
