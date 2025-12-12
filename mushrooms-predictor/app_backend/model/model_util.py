import joblib
import pandas as pd
import os

# Apenas a variável global do modelo é necessária.
# A variável '_encoder' foi removida porque é desnecessária.
_model = None

def load_model():
    """Carrega o Pipeline (Encoder + Classificador) salvo em disco (model.joblib)."""
    global _model
    if _model is None:
        # Pega o diretório onde este arquivo (model_util.py) está
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "model.joblib")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo não encontrado em: {model_path}. Execute o script de treinamento primeiro.")
            
        # O Pipeline completo (com encoder) é carregado aqui
        _model = joblib.load(model_path)
    return _model



def predict_mushroom(attributes):

    """
    Recebe um dicionário com as características (códigos literais) e retorna 
    a previsão e probabilidades.
    """
    # Cria o DataFrame de entrada
    df = pd.DataFrame([attributes])
    
    # Carrega o Pipeline (modelo)
    model = load_model()

    # O Pipeline faz automaticamente: (1) Encoding e (2) Predição
    prediction = model.predict(df)[0]
    
    prob_dict = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(df)[0]
        classes = model.classes_
        # Cria o dicionário de probabilidades
        prob_dict = {c: p for c, p in zip(classes, probs)}

    return prediction, prob_dict