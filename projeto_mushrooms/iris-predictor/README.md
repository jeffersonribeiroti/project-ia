# Iris Predictor (FastAPI + Streamlit)

## Requisitos
- Python 3.10+ (ou 3.8+)
- VS Code (opcional)
- pip

## Instalação (recomendo usar virtualenv)
1. Abra o terminal no diretório do projeto `iris-predictor/`.

2. Criar e ativar ambiente virtual (Windows):
   - `python -m venv .venv`
   - `.\.venv\Scripts\activate`

   (Linux / macOS):
   - `python -m venv .venv`
   - `source .venv/bin/activate`

3. Instalar dependências:
   - `pip install -r requirements.txt`

## Preparar o modelo
Se você já tem `iris_model.pkl`, coloque-o em `app_backend/model/iris_model.pkl`.
Se NÃO tiver o modelo, rode:
   - `python scripts/train_and_save_model.py`
Isso vai treinar um RandomForest no dataset Iris e salvar em `app_backend/model/iris_model.pkl`.

## Rodar a API (FastAPI)
No terminal com ambiente ativado:
   - `uvicorn app_backend.api:app --reload --port 8000`
A API ficará disponível em `http://localhost:8000/`.

Testar endpoint:
   - `curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d "{\"sepal_length\":5.1, \"sepal_width\":3.5, \"petal_length\":1.4, \"petal_width\":0.2}"`

## Rodar a interface (Streamlit)
Em outro terminal (também com o venv ativado):
   - `streamlit run app_frontend/streamlit_app.py`

A interface abrirá em `http://localhost:8501/` (padrão).

## Ordem recomendada
1. Iniciar API (uvicorn)
2. Abrir Streamlit (streamlit run ...)

## Observações
- A API responde com: `predicted_class`, `confidence` (0..1) e `probabilities` (lista).
- Em produção, configure CORS apropriado e cole o modelo com segurança.
