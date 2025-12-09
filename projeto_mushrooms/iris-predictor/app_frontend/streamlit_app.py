import streamlit as st
import pandas as pd
from app_backend.model_util import predict_mushroom
import os

st.title("🍄 Classificador de Cogumelos — Comestível ou Venenoso")

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "../../mushrooms.csv")

df = pd.read_csv(csv_path)
columns = [c for c in df.columns if c != "class"]

st.sidebar.header("Atributos do Cogumelo")
inputs = {}

for col in columns:
    values = sorted(df[col].unique())
    inputs[col] = st.sidebar.selectbox(col, values)

if st.sidebar.button("Prever"):
    pred, prob = predict_mushroom(inputs)

    if pred == "e":
        st.success("COMESTÍVEL (e)")
    else:
        st.error("VENENOSO (p)")

    if prob is not None:
        st.write("Probabilidades:", prob)
