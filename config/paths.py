from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Paths:
    RAW_DATA = BASE_DIR / "data/raw"
    PROCESSED_DATA = BASE_DIR / "data/processed"
    LABELED_DATA = BASE_DIR / "data/labeled"
    MODELS = BASE_DIR / "models"
    LOGS = BASE_DIR / "logs"
    
paths = Paths()