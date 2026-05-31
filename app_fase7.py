import os
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# FARMTECH SOLUTIONS — FASE 7
# Dashboard integrada das Fases 1 a 6 + AWS SNS
# ============================================================

st.set_page_config(
    page_title="FarmTech Solutions — Fase 7",
    page_icon="🌱",
    layout="wide"
)


# -----------------------------
# ESTILO VISUAL
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #1B5E20;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .card {
        padding: 1.2rem;
        border-radius: 16px;
        background-color: #F7FAF7;
        border: 1px solid #DDEBDD;
        margin-bottom: 1rem;
    }
    .small-muted {
        color: #666;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# FUNÇÕES AUXILIARES
# -----------------------------
@st.cache_data
def gerar_dados_simulados(n=120):
    """Gera uma base simulada caso a conexão com banco Oracle/CSV não esteja disponível."""
    rng = np.random.default_rng(42)

    temperatura = rng.normal(27, 4, n).clip(15, 42)
    ph = rng.normal(6.5, 0.55, n).clip(4.5, 8.5)
    luminosidade = rng.normal(650, 180, n).clip(100, 1000)
    n_val = rng.normal(35, 10, n).clip(5, 70)
    p_val = rng.normal(25, 7, n).clip(5, 50)
    k_val = rng.normal(30, 8, n).clip(5, 60)

    # Relação sintética: umidade cai com temperatura/luminosidade e melhora com equilíbrio de solo.
    umidade = (
        75
        - 0.85 * temperatura
        - 0.015 * luminosidade
        + 0.20 * n_val
        + 0.15 * p_val
        + 0.12 * k_val
        - 3.5 * np.abs(ph - 6.5)
        + rng.normal(0, 5, n)
    ).clip(8, 95)

    return pd.DataFrame(
        {
            "TEMPERATURA": temperatura.round(2),
            "PH": ph.round(2),
            "LUMINOSIDADE": luminosidade.round(2),
            "N": n_val.round(2),
            "P": p_val.round(2),
            "K": k_val.round(2),
            "UMIDADE": umidade.round(2),
        }
    )


@st.cache_data
def carregar_dados():
    """
    Ordem de tentativa:
    1. data/sensores.csv
    2. conexão Oracle, se existir arquivo conexao.py com get_connection()
    3. base simulada
    """
    csv_path = "data/sensores.csv"

    if os.path.exists(csv_path):
        df_csv = pd.read_csv(csv_path)
        return preparar_dataframe(df_csv), "CSV local: data/sensores.csv"

    try:
        from conexao import get_connection

        conn = get_connection()
        df_oracle = pd.read_sql("SELECT * FROM sensores", conn)
        conn.close()
        return preparar_dataframe(df_oracle), "Banco Oracle: tabela sensores"
    except Exception:
        df_simulado = gerar_dados_simulados()
        return df_simulado, "Base simulada gerada pelo app"


def preparar_dataframe(df):
    colunas = ["TEMPERATURA", "PH", "LUMINOSIDADE", "N", "P", "K", "UMIDADE"]

    # Padroniza nomes caso venham em minúsculo
    df = df.copy()
    df.columns = [str(c).strip().upper() for c in df.columns]

    faltantes = [c for c in colunas if c not in df.columns]
    if faltantes:
        st.warning(
            f"A base não contém as colunas esperadas: {faltantes}. "
            "Será usada uma base simulada para manter a dashboard funcionando."
        )
        return gerar_dados_simulados()

    df = df[colunas]
    df = df.apply(pd.to_numeric, errors="coerce").dropna()
    return df


def treinar_modelo(df, entradas, test_size):
    X = df[entradas]
    y = df["UMIDADE"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    metricas = {
        "MAE": mean_absolute_error(y_test, y_pred),
        "MSE": mean_squared_error(y_test, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "R2": r2_score(y_test, y_pred),
    }

    return modelo, X_test, y_test, y_pred, metricas


def regra_recomendacao(umidade, ph=None, n=None, p=None, k=None):
    alertas = []
    recomendacoes = []

    if umidade < 30:
        alertas.append("Umidade crítica")
        recomendacoes.append("Acionar irrigação urgente e verificar sensores de umidade.")
    elif umidade < 50:
        alertas.append("Umidade moderada")
        recomendacoes.append("Programar irrigação leve e acompanhar evolução do solo.")
    else:
        recomendacoes.append("Umidade adequada. Irrigação não necessária no momento.")

    if ph is not None and (ph < 6.0 or ph > 7.0):
        alertas.append("pH fora da faixa ideal")
        recomendacoes.append("Corrigir pH do solo para a faixa entre 6.0 e 7.0.")

    if n is not None and n < 30:
        alertas.append("Nitrogênio baixo")
        recomendacoes.append("Avaliar aplicação de fertilizante nitrogenado.")

    if p is not None and p < 20:
        alertas.append("Fósforo baixo")
        recomendacoes.append("Avaliar aplicação de fertilizante fosfatado.")

    if k is not None and k < 25:
        alertas.append("Potássio baixo")
        recomendacoes.append("Reforçar adubação potássica.")

    status = "CRÍTICO" if alertas else "NORMAL"
    return status, alertas, recomendacoes


def publicar_sns(assunto, mensagem):
    """
    Publica mensagem no Amazon SNS.
    Requisitos:
    - pip install boto3
    - credenciais AWS disponíveis no ambiente
    - variável de ambiente SNS_TOPIC_ARN com o ARN do tópico
    """
    try:
        import boto3

        topic_arn = os.getenv("SNS_TOPIC_ARN", "").strip()
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-2").strip()

        if not topic_arn:
            return False, "Defina a variável de ambiente SNS_TOPIC_ARN com o ARN do tópico SNS."

        sns = boto3.client("sns", region_name=region)
        sns.publish(TopicArn=topic_arn, Subject=assunto, Message=mensagem)
        return True, "Alerta enviado com sucesso pelo Amazon SNS."
    except Exception as e:
        return False, f"Não foi possível enviar pelo SNS: {e}"


def bloco_fase(titulo, objetivo, tecnologias, entregas):
    st.markdown(f"### {titulo}")
    st.markdown(
        f"""
        <div class="card">
        <b>Objetivo:</b> {objetivo}<br><br>
        <b>Tecnologias:</b> {tecnologias}<br><br>
        <b>Entregas integradas:</b> {entregas}
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# CARREGAMENTO DE DADOS
# -----------------------------
df, fonte_dados = carregar_dados()


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🌱 FarmTech Fase 7")
pagina = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Visão Geral",
        "💧 Fase 1 — IoT e Irrigação",
        "🗄️ Fase 2 — Banco de Dados",
        "🤖 Fase 3 — Machine Learning",
        "📊 Fase 4 — Dashboard Preditiva",
        "☁️ Fase 5 — AWS e Alertas",
        "👁️ Fase 6 — Visão Computacional",
        "🚨 Central de Alertas",
        "📘 Como Rodar e Entregar",
    ],
)

st.sidebar.divider()
st.sidebar.caption(f"Fonte de dados: {fonte_dados}")
st.sidebar.caption("Projeto acadêmico — FIAP")


# -----------------------------
# PÁGINA: VISÃO GERAL
# -----------------------------
if pagina == "🏠 Visão Geral":
    st.markdown('<div class="main-title">FarmTech Solutions — Sistema Integrado Fase 7</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Dashboard final para integração das Fases 1 a 6, com análise de sensores, modelo preditivo, recomendações agrícolas e alertas via AWS SNS.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registros analisados", len(df))
    c2.metric("Umidade média", f"{df['UMIDADE'].mean():.1f}%")
    c3.metric("pH médio", f"{df['PH'].mean():.2f}")
    c4.metric("Temperatura média", f"{df['TEMPERATURA'].mean():.1f} °C")

    st.subheader("🔗 Integração entre as fases")
    st.markdown(
        """
        Esta aplicação consolida as entregas anteriores em um único sistema de gestão agrícola.
        O objetivo é permitir que o usuário acompanhe sensores, consulte dados, visualize análises
        de Machine Learning, acesse recomendações de manejo e valide o serviço de mensageria em nuvem.
        """
    )

    fluxo = pd.DataFrame(
        {
            "Fase": ["Fase 1", "Fase 2", "Fase 3", "Fase 4", "Fase 5", "Fase 6"],
            "Papel no sistema": [
                "Coleta/simulação de sensores e lógica de irrigação",
                "Estruturação dos dados em banco relacional",
                "Modelos de IA para análise agrícola",
                "Dashboard Streamlit e recomendações",
                "Mensageria AWS SNS para envio de alertas",
                "Visão computacional com YOLOv8/CNN",
            ],
            "Status": [
                "Integrada conceitualmente",
                "Integrada via dados de sensores",
                "Integrada via análise preditiva",
                "Base principal da Fase 7",
                "Validada com tópico SNS e e-mail",
                "Documentada e integrada ao menu final",
            ],
        }
    )
    st.dataframe(fluxo, use_container_width=True, hide_index=True)

    st.subheader("📌 Arquitetura resumida")
    st.code(
        "Sensores/Simulações → Banco/CSV → Dashboard Streamlit → Modelo Preditivo → Regras de Negócio → AWS SNS → E-mail de Alerta",
        language="text",
    )


# -----------------------------
# FASE 1
# -----------------------------
elif pagina == "💧 Fase 1 — IoT e Irrigação":
    bloco_fase(
        "💧 Fase 1 — IoT e Irrigação Inteligente",
        "Automatizar a irrigação com base em umidade, pH e nutrientes do solo.",
        "ESP32, Wokwi, DHT22, LDR, botões NPK e lógica de acionamento da bomba.",
        "A lógica da irrigação foi incorporada ao sistema final por meio das regras de recomendação agrícola e alertas.",
    )

    st.subheader("🧪 Simulador de regras da Fase 1")
    col1, col2, col3, col4 = st.columns(4)
    umidade = col1.slider("Umidade do solo (%)", 0, 100, 45)
    ph = col2.slider("pH", 3.5, 9.0, 6.5)
    n_ok = col3.checkbox("Nitrogênio disponível", value=True)
    p_ok = col3.checkbox("Fósforo disponível", value=True)
    k_ok = col4.checkbox("Potássio disponível", value=True)

    condicao_ideal = umidade < 65 and 6.0 <= ph <= 7.0 and n_ok and p_ok and k_ok

    if condicao_ideal:
        st.success("✅ Condições ideais: bomba de irrigação LIGADA.")
    elif umidade >= 80:
        st.error("🚫 Solo saturado: bomba DESLIGADA.")
    elif not (6.0 <= ph <= 7.0):
        st.warning("⚠️ pH fora da faixa ideal: corrigir solo antes de irrigar.")
    elif not (n_ok and p_ok and k_ok):
        st.warning("⚠️ Nutrientes incompletos: corrigir NPK.")
    else:
        st.info("ℹ️ Bomba desligada: monitoramento em andamento.")


# -----------------------------
# FASE 2
# -----------------------------
elif pagina == "🗄️ Fase 2 — Banco de Dados":
    bloco_fase(
        "🗄️ Fase 2 — Banco de Dados Estruturado",
        "Organizar os dados agrícolas em uma base relacional para consulta e análise.",
        "Oracle Database, SQL, MER/DER e tabela de sensores.",
        "A dashboard lê dados de data/sensores.csv ou da tabela sensores do Oracle, quando a conexão estiver configurada.",
    )

    st.subheader("📄 Amostra da base usada pela dashboard")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("📌 Colunas esperadas")
    st.code("TEMPERATURA, PH, LUMINOSIDADE, N, P, K, UMIDADE", language="text")

    st.subheader("🔍 Consulta SQL esperada")
    st.code("SELECT * FROM sensores;", language="sql")


# -----------------------------
# FASE 3
# -----------------------------
elif pagina == "🤖 Fase 3 — Machine Learning":
    bloco_fase(
        "🤖 Fase 3 — Machine Learning no Agronegócio",
        "Aplicar modelos de IA para apoiar decisões agrícolas com base em variáveis de solo e clima.",
        "Python, Pandas, Scikit-Learn, análise exploratória e modelos preditivos.",
        "A Fase 7 utiliza a abordagem preditiva para estimar umidade do solo e sugerir ações de manejo.",
    )

    st.subheader("🔗 Correlação entre variáveis")
    fig, ax = plt.subplots(figsize=(8, 5))
    corr = df.corr(numeric_only=True)
    im = ax.imshow(corr)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    ax.set_title("Mapa de correlação")
    fig.colorbar(im)
    st.pyplot(fig)

    st.subheader("📊 Distribuição da umidade")
    fig2, ax2 = plt.subplots()
    ax2.hist(df["UMIDADE"], bins=20)
    ax2.set_xlabel("Umidade")
    ax2.set_ylabel("Frequência")
    ax2.set_title("Distribuição da umidade do solo")
    st.pyplot(fig2)


# -----------------------------
# FASE 4
# -----------------------------
elif pagina == "📊 Fase 4 — Dashboard Preditiva":
    st.markdown('<div class="main-title">📊 Dashboard Preditiva — Umidade do Solo</div>', unsafe_allow_html=True)
    st.markdown(
        "Esta aba reaproveita e aprimora a dashboard da Fase 4, com regressão linear, métricas do modelo e recomendações automáticas."
    )

    st.sidebar.subheader("Configurações do Modelo")
    test_size = st.sidebar.slider("Tamanho do conjunto de teste", 0.1, 0.5, 0.3)

    sensores = ["TEMPERATURA", "PH", "LUMINOSIDADE", "N", "P", "K"]
    entradas = st.sidebar.multiselect(
        "Sensores usados para prever a UMIDADE:",
        sensores,
        default=["TEMPERATURA", "PH", "LUMINOSIDADE", "N", "P", "K"],
    )

    if len(entradas) == 0:
        st.warning("Selecione pelo menos um sensor.")
        st.stop()

    modelo, X_test, y_test, y_pred, metricas = treinar_modelo(df, entradas, test_size)

    st.subheader("📊 Desempenho do modelo")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("MAE", f"{metricas['MAE']:.2f}")
    c2.metric("MSE", f"{metricas['MSE']:.2f}")
    c3.metric("RMSE", f"{metricas['RMSE']:.2f}")
    c4.metric("R²", f"{metricas['R2']:.2f}")

    st.subheader("📈 Umidade real x prevista")
    fig1, ax1 = plt.subplots()
    ax1.scatter(y_test, y_pred)
    ax1.set_xlabel("Umidade real")
    ax1.set_ylabel("Umidade prevista")
    ax1.set_title("Comparação entre valores reais e previstos")
    st.pyplot(fig1)

    st.subheader("🤖 Simulador de campo")
    valores = {}
    cols = st.columns(3)
    for i, col in enumerate(entradas):
        valores[col] = cols[i % 3].number_input(
            col,
            value=float(df[col].mean()),
            key=f"manual_{col}",
        )

    if st.button("Prever umidade e gerar recomendações", type="primary"):
        entrada_array = np.array([valores[col] for col in entradas]).reshape(1, -1)
        umidade_prevista = float(modelo.predict(entrada_array)[0])

        st.success(f"🌧️ Umidade prevista: **{umidade_prevista:.2f}%**")

        status, alertas, recomendacoes = regra_recomendacao(
            umidade_prevista,
            ph=valores.get("PH"),
            n=valores.get("N"),
            p=valores.get("P"),
            k=valores.get("K"),
        )

        if status == "CRÍTICO":
            st.error("🚨 Status: condição crítica identificada.")
        else:
            st.success("✅ Status: condição normal.")

        st.write("**Recomendações:**")
        for rec in recomendacoes:
            st.write(f"- {rec}")


# -----------------------------
# FASE 5
# -----------------------------
elif pagina == "☁️ Fase 5 — AWS e Alertas":
    bloco_fase(
        "☁️ Fase 5 — Cloud Computing e Mensageria AWS",
        "Configurar um serviço de mensageria para envio de alertas agrícolas.",
        "Amazon SNS, assinatura por e-mail, publicação de mensagens e validação de recebimento.",
        "Foi criado o tópico SNS farmtech-alertas, com assinatura de e-mail confirmada e teste de alerta recebido.",
    )

    st.subheader("📨 Validação do Amazon SNS")
    st.markdown(
        """
        Na AWS foi criado um tópico **farmtech-alertas** no Amazon SNS.
        Um e-mail foi cadastrado como assinatura, confirmado pelo usuário e testado com envio de alerta.
        """
    )

    st.code(
        """Mensagem testada:
Alerta: umidade do solo abaixo do limite ideal.
Ação recomendada: acionar irrigação e verificar sensores de campo.""",
        language="text",
    )

    st.info(
        "Para envio real via código, configure a variável de ambiente SNS_TOPIC_ARN com o ARN do tópico e rode a aplicação com credenciais AWS válidas."
    )


# -----------------------------
# FASE 6
# -----------------------------
elif pagina == "👁️ Fase 6 — Visão Computacional":
    bloco_fase(
        "👁️ Fase 6 — Visão Computacional",
        "Aplicar modelos de visão computacional para detectar ou classificar objetos/imagens relacionados ao contexto agrícola.",
        "YOLOv8, CNN, Google Colab, dataset próprio e MakeSense.ai.",
        "A Fase 6 foi documentada na dashboard final como módulo de inspeção visual, com possibilidade de integração futura a imagens reais da lavoura.",
    )

    st.subheader("📋 Comparativo das abordagens")
    comparativo = pd.DataFrame(
        {
            "Abordagem": ["YOLOv8 Customizado", "YOLO Padrão", "CNN do Zero"],
            "Função": ["Detecta e localiza", "Detecta classes COCO", "Classifica imagem inteira"],
            "Vantagem": ["Mais aplicável ao caso específico", "Rápido de testar", "Boa acurácia com simplicidade"],
            "Limitação": ["Exige rotulação", "Não reconhece classes fora do COCO", "Não gera bounding boxes"],
        }
    )
    st.dataframe(comparativo, use_container_width=True, hide_index=True)

    st.info(
        "Para o vídeo, explique que este módulo representa a frente de inspeção visual da FarmTech e pode ser conectado a imagens da lavoura ou de processos operacionais."
    )


# -----------------------------
# CENTRAL DE ALERTAS
# -----------------------------
elif pagina == "🚨 Central de Alertas":
    st.markdown('<div class="main-title">🚨 Central de Alertas Agrícolas</div>', unsafe_allow_html=True)
    st.markdown(
        "Simule uma condição de campo e gere uma mensagem de alerta. Opcionalmente, envie pelo Amazon SNS se as credenciais estiverem configuradas."
    )

    col1, col2, col3 = st.columns(3)
    umidade = col1.slider("Umidade prevista (%)", 0, 100, 28)
    ph = col2.slider("pH do solo", 3.5, 9.0, 6.2)
    temperatura = col3.slider("Temperatura (°C)", 10, 45, 32)

    col4, col5, col6 = st.columns(3)
    n = col4.slider("Nitrogênio (N)", 0, 80, 25)
    p = col5.slider("Fósforo (P)", 0, 60, 18)
    k = col6.slider("Potássio (K)", 0, 70, 22)

    status, alertas, recomendacoes = regra_recomendacao(umidade, ph=ph, n=n, p=p, k=k)

    assunto = f"Alerta FarmTech — {status}"
    mensagem = f"""
Data/hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

Status: {status}

Leituras:
- Umidade prevista: {umidade}%
- pH: {ph}
- Temperatura: {temperatura} °C
- N: {n}
- P: {p}
- K: {k}

Alertas identificados:
{chr(10).join('- ' + a for a in alertas) if alertas else '- Nenhum alerta crítico'}

Ações recomendadas:
{chr(10).join('- ' + r for r in recomendacoes)}
"""

    st.subheader("📩 Mensagem gerada")
    st.text_area("Conteúdo do alerta", mensagem, height=280)

    if status == "CRÍTICO":
        st.error("🚨 Condição crítica: alerta deve ser enviado ao responsável.")
    else:
        st.success("✅ Condição normal: apenas monitoramento.")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Validar alerta local", type="primary"):
            st.success("Alerta validado localmente na dashboard.")

    with col_b:
        if st.button("Enviar via AWS SNS"):
            ok, retorno = publicar_sns(assunto, mensagem)
            if ok:
                st.success(retorno)
            else:
                st.warning(retorno)


# -----------------------------
# COMO RODAR
# -----------------------------
elif pagina == "📘 Como Rodar e Entregar":
    st.markdown('<div class="main-title">📘 Como Rodar e Entregar</div>', unsafe_allow_html=True)

    st.subheader("1. Estrutura de pastas sugerida")
    st.code(
        """FarmTech_Fase7/
├── app_fase7.py
├── requirements.txt
├── README.md
├── data/
│   └── sensores.csv
├── img/
│   └── aws/
│       ├── aws_topic.png
│       ├── aws_subscription.png
│       ├── aws_confirmed.png
│       ├── aws_email_confirmation.png
│       └── aws_alert_email.png
├── fase1/
├── fase2/
├── fase3/
├── fase4/
├── fase5/
└── fase6/""",
        language="text",
    )

    st.subheader("2. Comando para rodar")
    st.code("streamlit run app_fase7.py", language="bash")

    st.subheader("3. Entrega")
    st.markdown(
        """
        - Subir o projeto no GitHub;
        - Incluir prints da AWS no README;
        - Colocar o link do vídeo do YouTube como não listado;
        - Enviar o link do GitHub ou PDF com o link pelo portal da FIAP;
        - Não incluir os tópicos de “Ir Além”.
        """
    )
