import streamlit as st
import pandas as pd
import numpy as np
from conexao import get_connection
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="FarmTech IA", layout="wide")

# --------------------- CONEXÃO ORACLE ------------------------
conn = get_connection()
df = pd.read_sql("SELECT * FROM sensores", conn)
conn.close()

st.title("🌱 FarmTech Solutions — IA Agrícola (PARTE 2)")

# ------------------ LIMPEZA DOS DADOS ------------------------
colunas = ["TEMPERATURA", "PH", "LUMINOSIDADE", "N", "P", "K", "UMIDADE"]
df = df[colunas]
df = df.apply(pd.to_numeric, errors="coerce").dropna()

# -------------------- CONFIGURAÇÕES --------------------------
st.sidebar.header("Configurações do Modelo")

test_size = st.sidebar.slider("Tamanho do conjunto de teste", 0.1, 0.5, 0.3)

sensores = ["TEMPERATURA", "PH", "LUMINOSIDADE", "N", "P", "K"]

entradas = st.sidebar.multiselect(
    "Sensores usados para prever a UMIDADE:",
    sensores,
    default=["TEMPERATURA", "PH"]
)

if len(entradas) == 0:
    st.warning("Selecione pelo menos um sensor!")
    st.stop()

# -------------------- TREINAMENTO ----------------------------
X = df[entradas]
y = df["UMIDADE"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42
)

modelo = LinearRegression()
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

# -------------------- MÉTRICAS -------------------------------
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# -------------------- DASHBOARD ------------------------------
st.subheader("📊 Desempenho do Modelo")

c1, c2, c3, c4 = st.columns(4)
c1.metric("MAE", f"{mae:.2f}")
c2.metric("MSE", f"{mse:.2f}")
c3.metric("RMSE", f"{rmse:.2f}")
c4.metric("R²", f"{r2:.2f}")

# -------------------- GRÁFICO REAL vs PREVISTO ---------------
st.subheader("📈 Umidade Real x Prevista")

fig1, ax1 = plt.subplots()
ax1.scatter(y_test, y_pred)
ax1.set_xlabel("Umidade Real")
ax1.set_ylabel("Umidade Prevista")
ax1.set_title("Comparação das previsões")
st.pyplot(fig1)

# -------------------- CORRELAÇÃO -----------------------------
st.subheader("🔗 Correlação entre Variáveis")

fig2, ax2 = plt.subplots(figsize=(8,5))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax2)
st.pyplot(fig2)

# -------------------- PREVISÃO MANUAL ------------------------
st.subheader("🤖 Simulador de Campo (Previsão e Recomendações)")

valores = {}
for col in entradas:
    valores[col] = st.number_input(col, value=float(df[col].mean()))

if st.button("Prever e gerar recomendações"):
    entrada_array = np.array(list(valores.values())).reshape(1, -1)
    umidade_prevista = modelo.predict(entrada_array)[0]

    st.success(f"🌧️ Umidade prevista: **{umidade_prevista:.2f}**")

    # ------------------- REGRAS INTELIGENTES ----------------------
    st.subheader("🚜 Recomendações Agrícolas")

    # IRRIGAÇÃO
    if umidade_prevista < 30:
        st.error("💧 Solo seco! Recomenda-se irrigação URGENTE.")
    elif umidade_prevista < 50:
        st.warning("💦 Umidade moderada. Irrigação leve recomendada.")
    else:
        st.success("✅ Umidade adequada. Irrigação não necessária.")

    # FERTILIZAÇÃO (apenas se NPK estiver selecionado)
    if "N" in entradas and "P" in entradas and "K" in entradas:
        n = valores["N"]
        p = valores["P"]
        k = valores["K"]

        if n < 30:
            st.warning("🌿 Nitrogênio baixo — aplicar fertilizante nitrogenado.")
        if p < 20:
            st.warning("🌱 Fósforo insuficiente — aplicar fertilizante fosfatado.")
        if k < 25:
            st.warning("🍃 Potássio insuficiente — reforçar adubação.")

        if n >= 30 and p >= 20 and k >= 25:
            st.success("✅ NPK equilibrado. Nenhuma correção necessária.")

    else:
        st.info("ℹ️ Inclua N, P e K nos sensores para recomendações de fertilização.")
