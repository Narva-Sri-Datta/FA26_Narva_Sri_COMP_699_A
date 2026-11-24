import csv
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

DEFAULT_ROWS = [
 ("sink pipe is leaking", "Plumbing"), ("bathroom faucet is dripping", "Plumbing"), ("blocked drain", "Plumbing"),
 ("water leaking under sink", "Plumbing"), ("power outlet is not working", "Electrical"), ("lights keep flickering", "Electrical"),
 ("circuit breaker keeps tripping", "Electrical"), ("switch makes a buzzing sound", "Electrical"),
 ("washing machine will not start", "Appliance Repair"), ("refrigerator is not cooling", "Appliance Repair"),
 ("microwave stopped heating", "Appliance Repair"), ("dishwasher makes loud noise", "Appliance Repair"),
 ("door hinge is broken", "Carpentry"), ("wooden cabinet door is loose", "Carpentry"),
 ("wall needs a fresh coat of paint", "Painting"), ("paint is peeling from wall", "Painting"),
 ("house needs deep cleaning", "Cleaning"), ("kitchen cleaning service needed", "Cleaning")]
class ProblemClassifier:
    def __init__(self, csv_path=None):
        rows=self.load_rows(csv_path) if csv_path else []
        if len(rows)<6 or len({label for _,label in rows})<2: rows=DEFAULT_ROWS
        self.categories=sorted({label for _,label in rows})
        self.pipeline=Pipeline([("tfidf",TfidfVectorizer(ngram_range=(1,2),lowercase=True, strip_accents="unicode")),
                                ("model",LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42))])
        self.pipeline.fit([x for x,_ in rows],[y for _,y in rows])
    @staticmethod
    def load_rows(path):
        p=Path(path)
        if not p.exists(): return []
        with p.open(encoding="utf-8-sig",newline="") as f:
            r=csv.DictReader(f)
            if not r.fieldnames or not {"description","category"}.issubset(r.fieldnames): return []
            return [(x["description"].strip(),x["category"].strip()) for x in r if x.get("description","").strip() and x.get("category","").strip()]
    def predict(self, description):
        probs=self.pipeline.predict_proba([description])[0]; i=probs.argmax()
        return self.pipeline.classes_[i],float(probs[i])
