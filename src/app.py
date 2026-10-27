from pathlib import Path
import sqlite3
from flask import Flask, request, render_template_string
from classifier import predict_category

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "service_requests.db"
app = Flask(__name__)

PAGE = """
<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Service Problem Classification POC</title>
<style>
body{font-family:Arial,sans-serif;max-width:760px;margin:40px auto;padding:0 16px;color:#222}
textarea{width:100%;min-height:110px;padding:10px;box-sizing:border-box}
button{padding:10px 16px;margin-top:10px;cursor:pointer}
.card{border:1px solid #ddd;border-radius:8px;padding:16px;margin-top:20px}
small{color:#555}
</style></head>
<body>
<h1>Service Problem Diagnosis and Matching — Proof of Concept</h1>
<p>Enter a sample household or equipment problem. The prototype predicts a service category and saves the request to SQLite.</p>
<form method="post">
<label for="description">Problem description</label>
<textarea id="description" name="description" required>{{ description }}</textarea>
<button type="submit">Classify and Save</button>
</form>
{% if result %}
<div class="card">
<h2>Preliminary result</h2>
<p><strong>Predicted category:</strong> {{ result.category }}</p>
<p><strong>Model confidence:</strong> {{ result.confidence }}</p>
<p><strong>Saved request ID:</strong> {{ request_id }}</p>
<small>This is a demonstration model trained on a small illustrative dataset. It is not a technical diagnosis and must not be treated as a validated production model.</small>
</div>
{% endif %}
</body></html>
"""

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS poc_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_description TEXT NOT NULL,
                predicted_category TEXT NOT NULL,
                confidence REAL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/", methods=["GET", "POST"])
def home():
    init_db()
    description = ""
    result = None
    request_id = None
    if request.method == "POST":
        description = request.form.get("description", "").strip()
        if description:
            result = predict_category(description)
            with sqlite3.connect(DB_PATH) as con:
                cur = con.execute(
                    "INSERT INTO poc_requests (problem_description, predicted_category, confidence) VALUES (?, ?, ?)",
                    (description, result.category, result.confidence_value)
                )
                request_id = cur.lastrowid
    return render_template_string(PAGE, description=description, result=result, request_id=request_id)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/api/classify", methods=["POST"])
def api_classify():
    data = request.get_json(silent=True) or {}
    description = str(data.get("description", "")).strip()
    if not description:
        return {"error": "description is required"}, 400
    result = predict_category(description)
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute(
            "INSERT INTO poc_requests (problem_description, predicted_category, confidence) VALUES (?, ?, ?)",
            (description, result.category, result.confidence_value)
        )
        request_id = cur.lastrowid
    return {
        "request_id": request_id,
        "predicted_category": result.category,
        "confidence": result.confidence_value
    }

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
