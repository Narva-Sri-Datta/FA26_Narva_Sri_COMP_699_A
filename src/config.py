import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "change-this-development-key")
    DATABASE = os.environ.get("SERVICE_REQUEST_DB", str(BASE_DIR / "instance" / "local_service_connect.db"))
    TRAINING_DATA = str(BASE_DIR / "sample_training_data.csv")
