import joblib
import pandas as pd
import os

_model = None

def load_model():
    global _model
    if _model is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "model.joblib")
        _model = joblib.load(model_path)
    return _model

def predict_mushroom(attributes):
    df = pd.DataFrame([attributes])
    model = load_model()

    prediction = model.predict(df)[0]

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(df)[0]
    else:
        probs = None

    return prediction, probs
