from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "sample_training_data.csv"

@dataclass
class Prediction:
    category: str
    confidence_value: float

    @property
    def confidence(self):
        return f"{self.confidence_value:.2f}"

def build_model():
    data = pd.read_csv(DATA_PATH)
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42))
    ])
    model.fit(data["description"], data["category"])
    return model

MODEL = build_model()

def predict_category(description: str) -> Prediction:
    category = MODEL.predict([description])[0]
    confidence = float(max(MODEL.predict_proba([description])[0]))
    return Prediction(category=category, confidence_value=round(confidence, 4))
