import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "../../mushrooms.csv")

df = pd.read_csv(csv_path)

y = df["class"]
X = df.drop(columns=["class"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

cat_columns = X.columns.tolist()
preprocessor = ColumnTransformer(
    [("cat", OneHotEncoder(handle_unknown="ignore"), cat_columns)]
)

model = Pipeline([
    ("pre", preprocessor),
    ("clf", RandomForestClassifier(n_estimators=150, random_state=42))
])

model.fit(X_train, y_train)

pred = model.predict(X_test)

print("\nACURÁCIA:", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))
print(confusion_matrix(y_test, pred))

model_path = os.path.join(base_dir, "../app_backend/model.joblib")
joblib.dump(model, model_path)

print("\nModelo salvo em:", model_path)
