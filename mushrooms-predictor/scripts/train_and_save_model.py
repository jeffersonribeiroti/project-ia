import pandas as pd
from sklearn.model_selection import train_test_split
# 1. Importe o modelo de Floresta Aleatória
from sklearn.ensemble import RandomForestClassifier 
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os
# 1. Configuração de Caminhos Absolutos
# O base_dir é a pasta onde ESTE script está localizado (.../scripts)
base_dir = os.path.dirname(os.path.abspath(__file__))

# O CSV está duas pastas acima de scripts (projeto_mushrooms/mushrooms.csv)
csv_path = os.path.join(base_dir, "../../mushrooms.csv")

# O modelo será salvo em ../app_backend/model.joblib
model_dir = os.path.join(base_dir, "../app_backend")
model_path = os.path.join(model_dir, "model.joblib")

# Criar diretório do backend se não existir
os.makedirs(model_dir, exist_ok=True)

print(f"Lendo dataset de: {os.path.abspath(csv_path)}")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

df = pd.read_csv(csv_path)

# 2. Separação X e y
y = df["class"]  # p=poisonous, e=edible
X = df.drop(columns=["class"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Pipeline com Árvore de Decisão
cat_columns = X.columns.tolist()

preprocessor = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore"), cat_columns)]
)

# Usando RandomForestClassifier
model = Pipeline([
    ("pre", preprocessor),
    ("clf", RandomForestClassifier(random_state=42, n_estimators=100)) # n_estimators, quanto maior o número de comparações, melhor e mais acertivo torna a técnica de aprendizado de máquina.
])

print("Treinando Floresta Aleatória...")
model.fit(X_train, y_train)

# 4. Avaliação
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)

print(f"\nACURÁCIA: {acc:.4f}")
print(classification_report(y_test, pred))

# 5. Salvar Modelo
joblib.dump(model, model_path)
print(f"Modelo salvo em: {model_path}")

# (Opcional) Visualizar regras da árvore

"""
try:
    feature_names = model.named_steps['pre'].get_feature_names_out()
    tree_rules = export_text(model.named_steps['clf'], feature_names=list(feature_names))
    print("\n--- Regras da Árvore (Exemplo) ---")
    print(tree_rules[:500] + "...\n")
except Exception as e:
    print(f"Não foi possível exportar o texto da árvore: {e}")
"""