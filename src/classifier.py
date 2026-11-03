import csv
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DEFAULT_ROWS = [
    ("sink pipe is leaking", "Plumbing"),
    ("bathroom faucet is dripping", "Plumbing"),
    ("blocked drain", "Plumbing"),
    ("water leaking under sink", "Plumbing"),
    ("power outlet is not working", "Electrical"),
    ("lights keep flickering", "Electrical"),
    ("circuit breaker keeps tripping", "Electrical"),
    ("switch makes a buzzing sound", "Electrical"),
    ("washing machine will not start", "Appliance Repair"),
    ("refrigerator is not cooling", "Appliance Repair"),
    ("microwave stopped heating", "Appliance Repair"),
    ("dishwasher makes loud noise", "Appliance Repair"),
]

class ProblemClassifier:
    def __init__(self, csv_path=None):
        rows = self.load_rows(csv_path) if csv_path else []
        if len(rows) < 3 or len({label for _, label in rows}) < 2:
            rows = DEFAULT_ROWS
        x = [description for description, _ in rows]
        y = [category for _, category in rows]
        self.categories = sorted(set(y))
        self.pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
            ("model", LogisticRegression(max_iter=1000, random_state=42)),
        ])
        self.pipeline.fit(x, y)

    @staticmethod
    def load_rows(csv_path):
        path = Path(csv_path)
        if not path.exists():
            return []
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or not {"description", "category"}.issubset(reader.fieldnames):
                return []
            return [(r["description"].strip(), r["category"].strip())
                    for r in reader if r.get("description", "").strip()
                    and r.get("category", "").strip()]

    def predict(self, description):
        scores = self.pipeline.predict_proba([description])[0]
        i = scores.argmax()
        return self.pipeline.classes_[i], float(scores[i])
