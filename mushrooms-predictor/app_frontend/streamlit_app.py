# app_frontend/streamlit_app.py - Versão em Português
import streamlit as st
import pandas as pd
import os
import sys

# --- Dicionários de Tradução (Português/Inglês) ---

# Mapeia as Colunas (Características) do CSV para o Português
FEATURE_MAP = {
    'cap-shape': 'Formato do Chapéu',
    'cap-surface': 'Superfície do Chapéu',
    'cap-color': 'Cor do Chapéu',
    'bruises': 'Contusões (Machucados)',
    'odor': 'Odor (Cheiro)',
    'gill-attachment': 'Afixação da Brânquia',
    'gill-spacing': 'Espaçamento da Brânquia',
    'gill-size': 'Tamanho da Brânquia',
    'gill-color': 'Cor da Brânquia',
    'stalk-shape': 'Formato do Talo',
    'stalk-root': 'Raiz do Talo',
    'stalk-surface-above-ring': 'Superfície do Talo (Acima do Anel)',
    'stalk-surface-below-ring': 'Superfície do Talo (Abaixo do Anel)',
    'stalk-color-above-ring': 'Cor do Talo (Acima do Anel)',
    'stalk-color-below-ring': 'Cor do Talo (Abaixo do Anel)',
    'veil-type': 'Tipo de Véu',
    'veil-color': 'Cor do Véu',
    'ring-number': 'Número de Anéis',
    'ring-type': 'Tipo de Anel',
    'spore-print-color': 'Cor de impressão dos poros',
    'point-of-contact': 'Ponto de Contato',
    'population': 'População',
    'habitat': 'Habitat',
}

# Mapeia os Valores Únicos (Códigos) do CSV para o Português
# A chave é o nome da coluna original, e o valor é um dicionário de código:tradução
VALUE_MAP = {
    'cap-shape': {'b': 'Sino', 'c': 'Cônico', 'x': 'Convexo', 'f': 'Plano', 'k': 'Nó', 's': 'Afundado'},
    'cap-surface': {'f': 'Fibroso', 'g': 'Sulcos', 'y': 'Escamoso', 's': 'Suave'},
    'cap-color': {'n': 'Marrom', 'b': 'Amarelado', 'c': 'Canela', 'g': 'Cinza', 'r': 'Verde', 'p': 'Rosa', 'u': 'Roxo', 'e': 'Bege', 'w': 'Branco', 'y': 'Amarelo'},
    'bruises': {'t': 'Sim', 'f': 'Não'},
    'odor': {'a': 'Amêndoa', 'l': 'Anis', 'c': 'Creosote', 'y': 'Fétido', 'f': 'Fedorento', 'm': 'Mostarda', 'n': 'Nenhum', 'p': 'Picante', 's': 'Azedo'},
    'gill-attachment': {'a': 'Anexado', 'd': 'Livre', 'f': 'Livre'}, # Assumindo 'd' e 'f' são tratados como livres ou livres na base original
    'gill-spacing': {'c': 'Perto', 'w': 'Longe', 'd': 'Distante'},
    'gill-size': {'b': 'Largo', 'n': 'Estreito'},
    'gill-color': {'k': 'Preto', 'n': 'Marrom', 'b': 'Amarelado', 'h': 'Cinza', 'r': 'Verde', 'o': 'Laranja', 'u': 'Roxo', 'e': 'Bege', 'w': 'Branco', 'y': 'Amarelo', 'p': 'Rosa', 'g': 'Verde Oliva'},
    'stalk-shape': {'e': 'Aumentando', 't': 'Afilando'},
    'stalk-root': {'b': 'Bulboso', 'c': 'Club', 'e': 'Equilibrado', 'r': 'Enraizado', 'z': 'Faltando', '?': 'Desconhecido'},
    'stalk-surface-above-ring': {'f': 'Fibroso', 'y': 'Escamoso', 'k': 'Sedoso', 's': 'Suave'},
    'stalk-surface-below-ring': {'f': 'Fibroso', 'y': 'Escamoso', 'k': 'Sedoso', 's': 'Suave'},
    'stalk-color-above-ring': {'n': 'Marrom', 'b': 'Amarelado', 'c': 'Canela', 'g': 'Cinza', 'o': 'Laranja', 'p': 'Rosa', 'e': 'Bege', 'w': 'Branco', 'y': 'Amarelo'},
    'stalk-color-below-ring': {'n': 'Marrom', 'b': 'Amarelado', 'c': 'Canela', 'g': 'Cinza', 'o': 'Laranja', 'p': 'Rosa', 'e': 'Bege', 'w': 'Branco', 'y': 'Amarelo'},
    'veil-type': {'p': 'Parcial'},
    'veil-color': {'n': 'Marrom', 'o': 'Laranja', 'w': 'Branco', 'y': 'Amarelo'},
    'ring-number': {'n': 'Nenhum', 'o': 'Um', 't': 'Dois'},
    'ring-type': {'c': 'Pendente', 'e': 'Evanescente', 'f': 'Alargando', 'l': 'Grande', 'n': 'Nenhum', 'p': 'Pingente', 's': 'Bainha', 'z': 'Zona'},
    'spore-print-color': {'b': 'Sino','h': 'Cinza','k': 'Nó','n': 'Marrom','o': 'Laranja', 'r': 'Verde','u': 'Roxo', 'w': 'Branco','y': 'Amarelo'},
    'population': {'a': 'Abundante', 'c': 'Agrupado', 'n': 'Numeroso', 's': 'Espalhado', 'v': 'Vários', 'y': 'Solitário'},
    'habitat': {'g': 'Gramados', 'l': 'Folhas', 'm': 'Prados', 'p': 'Caminhos', 'u': 'Urbano', 'w': 'Estrume', 'd': 'Madeira'},
}

# Função para traduzir o código de valor do CSV para o nome em Português
def translate_value(feature_name, code):
    return VALUE_MAP.get(feature_name, {}).get(code, code) # Retorna o código se não encontrar a tradução

# Função para obter a lista de opções traduzidas e seus códigos originais
def get_translated_options(df, col):
    original_codes = sorted(df[col].astype(str).unique())
    # Cria uma lista de tuplas (Tradução em Português, Código Original)
    translated_options = [(translate_value(col, code), code) for code in original_codes]
    return translated_options

# --- Configuração de Caminhos ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

try:
    # A importação usa o caminho original, o que é ótimo
    from app_backend.model.model_util import predict_mushroom
except ImportError as e:
    st.error(f"Erro de importação: {e}. Verifique se a estrutura de pastas está correta e se o arquivo 'model_util.py' existe.")
    st.stop()

# --- Configuração da Página ---
st.set_page_config(
    page_title="Detector de Cogumelos",
    page_icon="🍄",
    layout="wide"
)

st.title("🍄 Classificador de Cogumelos (Árvore de Busca)")
st.markdown("""
Esta aplicação utiliza Inteligência Artificial para analisar as características de um cogumelo
e determinar se ele é *Comestível* ou *Venenoso*.
""")





# --- Carregamento de Dados para o Formulário ---
csv_path = os.path.join(current_dir, "../../mushrooms.csv")

if not os.path.exists(csv_path):
    st.error(f"Erro: O arquivo de dados **mushrooms.csv** não foi encontrado em: {csv_path}")
    st.stop()

@st.cache_data
def load_data():
    return pd.read_csv(csv_path)

df = load_data()

# Remove a coluna alvo 'class' e 'veil-type' (que tem apenas um valor em todo o dataset)
feature_columns = [col for col in df.columns if col not in ['class', 'veil-type']]

# --- Barra Lateral (Entrada de Dados) ---
st.sidebar.header("🔎 Características do Cogumelo")
st.sidebar.info("Selecione as propriedades abaixo:")

user_input = {}

# Cria um menu suspenso para cada coluna do CSV usando as traduções
with st.sidebar.form("mushroom_form"):
    
    for col in feature_columns:
        # Pega a lista de opções traduzidas (Tradução, Código Original)
        translated_options = get_translated_options(df, col)
        
        # Cria uma lista de strings para exibição no Streamlit (apenas as traduções)
        display_options = [opt[0] for opt in translated_options]
        
        # Mapeia a tradução de volta para o código original
        translation_to_code = {opt[0]: opt[1] for opt in translated_options}
        
        # Título da característica traduzido
        translated_feature_name = FEATURE_MAP.get(col, col)

        # Seletor do Streamlit
        selected_display_value = st.selectbox(
            label=f"**{translated_feature_name}**", 
            options=display_options,
            key=col # Chave única para o widget
        )
        
        # Armazena o CÓDIGO ORIGINAL para enviar ao modelo
        user_input[col] = translation_to_code[selected_display_value]
    
    # Adiciona o 'veil-type' com valor fixo para a entrada do modelo, se o modelo precisar (valor: 'p')
    # Assumindo que o modelo treinado espera todas as colunas do dataset original.
    user_input['veil-type'] = 'p' 
    
    submit_button = st.form_submit_button("Analisar Cogumelo 🔍")

# --- Área Principal (Resultados) ---
col1, col2 = st.columns([3, 1])

if submit_button:
    with col1:
        st.subheader("Resultado da Análise:")
        try:
            # Chama o backend para fazer a previsão usando o 'user_input' (códigos originais)
            # Retorna pred ('e' ou 'p') e probs (dicionário)
            pred, probs = predict_mushroom(user_input)
            
            # --- Exibição do Resultado Principal ---
            
            if pred == 'p':
                st.error("## ☠️ RESULTADO: VENENOSO (Poisonous)")
                st.warning("Atenção! O modelo identificou características perigosas. **NÃO CONSUMA!**")
            else:
                st.success("## 🍽️ RESULTADO: COMESTÍVEL (Edible)")
                st.info("O modelo indica que é seguro, mas **SEMPRE consulte um especialista** antes de consumir cogumelos selvagens.")

            st.divider()

            # --- Exibição da Certeza ---
            if probs and isinstance(probs, dict):
                st.write("### Nível de Certeza do Modelo:")
                
                # Tradução e Formatação
                label_p = "Venenoso"
                label_e = "Comestível"
                
                confidence = probs[pred] * 100
                
                if pred == 'p':
                    st.metric(label=f"Certeza de ser **{label_p}**", value=f"{confidence:.2f}%", delta=f"{probs['e']*100:.2f}% de ser Comestível")
                    color_map = {'e': 'green', 'p': 'red'}
                else:
                    st.metric(label=f"Certeza de ser **{label_e}**", value=f"{confidence:.2f}%", delta=f"{probs['p']*100:.2f}% de ser Venenoso", delta_color="inverse")
                    color_map = {'e': 'green', 'p': 'red'}


                # Gráfico de Barras com as probabilidades
                st.write("#### Probabilidades Detalhadas")
                prob_df = pd.DataFrame({
                    "Classe": [label_e, label_p],
                    "Probabilidade": [probs['e'], probs['p']]
                })
                prob_df = prob_df.set_index("Classe")
                st.bar_chart(prob_df)

        except Exception as e:
            st.error("Ocorreu um erro ao processar a previsão no backend.")
            st.error(f"Detalhes: {e}")

else:
    with col1:
        st.info("👈 Use a barra lateral para selecionar as características do cogumelo e clique em 'Analisar Cogumelo'.")

with col2:
    st.subheader("Legenda dos Atributos")
    st.markdown("""
    * **Comestível (e):** Edible
    * **Venenoso (p):** Poisonous
    """)
    st.divider()
    st.caption("A Árvore de Decisão é um modelo de Machine Learning que simula uma série de perguntas (características) para chegar a uma classificação final.")


# Rodapé
st.markdown("---")
st.caption("Sistema desenvolvido com Python, Scikit-learn e Streamlit. Base de dados: Kaggle (UCI Mushroom Dataset).")