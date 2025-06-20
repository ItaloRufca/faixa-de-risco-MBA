import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import holidays
import streamlit.components.v1 as components
import nbformat
from nbconvert import HTMLExporter
from pycaret.regression import predict_model


# --- Configuração da página e tema ---
st.set_page_config(
    page_title="Faixa de Risco",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS customizado ---
st.markdown("""
<style>
  :root { --primary-color: #3872fb; }
  .st-emotion-cache-1r6slb0, .st-emotion-cache-1r6slb0:hover {
      border-color: #e0e0e0;
      border-radius: 10px;
  }
  [data-baseweb="slider"] .innerTrack { background-color: var(--primary-color) !important; }
  .stDateInput .CalendarDay__selected,
  .stDateInput .CalendarDay__selected:hover {
    background-color: var(--primary-color) !important;
    border-color: var(--primary-color) !important;
  }
  button:hover { background-color: var(--primary-color) !important; border-color: var(--primary-color) !important; }
</style>
""", unsafe_allow_html=True)


# --- Carregar dados e modelo ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/acidentes_pronto.csv")
    df['mes'] = df['mes'].astype(int)
    num = ['km','qtd_mortos','qtd_feridos_graves','qtd_feridos_leves',
           'media_idade_envolvidos','proporcao_noite',
           'proporcao_dia_semana_fds','clima_ruim',
           'frequencia_feriado','qtd_infracoes']
    df[num] = df[num].apply(pd.to_numeric, errors='coerce')
    return df

@st.cache_resource
def load_model():
    return joblib.load("model/model.pkl")

df0 = load_data()
model = load_model()
br_hols = holidays.Brazil(years=range(df0['ano'].min(), df0['ano'].max()+1))


# --- HEADER ---
st.sidebar.image("assets/logo.png", width=80)
st.title("Faixa de Risco")
st.markdown("Plataforma para previsão de risco de acidentes e análise de dados.")
st.divider()


# --- Criação das Abas de Navegação ---
tab_previsao, tab_eda, tab_ml = st.tabs(["🔮 **Previsão**", "📊 **Análise Exploratória (EDA)**", "🤖 **Modelagem (ML)**"])


# --- Conteúdo da Aba 1: Previsão ---
with tab_previsao:
    st.header("Previsão de Risco de Acidentes", anchor=False)
    
    # A sidebar agora só mostra os filtros para esta aba
    st.sidebar.header("Parâmetros de Previsão")
    data = st.sidebar.date_input("Data")
    municipio = st.sidebar.selectbox("Município", sorted(df0["municipio"].unique()))
    br_choices = df0[df0['municipio']==municipio]['br'].unique().tolist()
    br = st.sidebar.selectbox("BR", br_choices)

    if st.sidebar.button("Predizer 🚀", use_container_width=True):
        ano, mes = data.year, data.month
        feats = ['km','qtd_mortos','qtd_feridos_graves','qtd_feridos_leves',
                 'media_idade_envolvidos','proporcao_noite',
                 'proporcao_dia_semana_fds','clima_ruim',
                 'frequencia_feriado','qtd_infracoes']
        gm = df0.groupby(['municipio','br','mes'])[feats].mean().reset_index()
        om = df0[feats].mean().to_dict()
        row = gm[(gm['municipio']==municipio)&(gm['br']==br)&(gm['mes']==mes)]
        defaults = row.iloc[0][feats].to_dict() if not row.empty else om
        inp = {'ano':ano,'mes':mes,'municipio':municipio,'br':br, **defaults}
        df_in = pd.DataFrame([inp])
        preds = predict_model(model,data=df_in)
        pcol = [c for c in preds.columns if c not in df_in.columns][0]
        preds = preds.rename(columns={pcol:'qtd_acidentes'})
        qa = preds['qtd_acidentes'].iloc[0]
        fer = "Sim" if data in br_hols else "Não"
        
        st.subheader("Resultados da Previsão", anchor=False)
        with st.container(border=True):
            c1,c2,c3 = st.columns(3)
            c1.metric("Acidentes Previstos",f"{qa:.2f}", help="Número de acidentes estimados pelo modelo para a data e local selecionados.")
            c2.metric("Proporção Noturna Média",f"{defaults['proporcao_noite']*100:.1f}%", help="Média histórica de acidentes ocorridos à noite para este local e mês.")
            c3.metric("Média de Clima Ruim",f"{defaults['clima_ruim']*100:.1f}%", help="Média histórica da proporção de acidentes em condições climáticas adversas.")
        st.write("")
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("##### Detalhes da Consulta")
                st.markdown(f"""
                - **Município:** `{municipio}`
                - **BR:** `{br}`
                - **Data:** `{data:%d/%m/%Y}`
                - **É Feriado?** `{fer}`
                """)
            with col2:
                st.markdown("##### Histórico Anual de Acidentes (para o mesmo mês)")
                hist = (df0[(df0['municipio']==municipio)&(df0['br']==br)&(df0['mes']==mes)]
                        .groupby('ano')['qtd_acidentes'].sum().reset_index())
                if hist.empty:
                    st.warning("Não há dados históricos para este mês e local específicos.")
                else:
                    fig=px.line(hist,x='ano',y='qtd_acidentes',markers=True,
                                labels={'ano':'Ano','qtd_acidentes':'Qtd. de Acidentes'})
                    fig.update_xaxes(dtick=1,tickformat='d')
                    st.plotly_chart(fig,use_container_width=True)
    else:
        st.info("Aguardando parâmetros na barra lateral para gerar a previsão.")

# --- Conteúdo da Aba 2: Análise Exploratória (EDA) ---
with tab_eda:
    st.header("Análise Exploratória dos Dados (EDA)", anchor=False)
    try:
        # CORREÇÃO: Buscando o arquivo na pasta 'notebooks'
        with open("notebooks/faixa_de_risco_Analise_Exploratoria.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=800, scrolling=True)
    except FileNotFoundError:
        st.error("Arquivo `faixa_de_risco_Analise_Exploratoria.html` não encontrado na pasta `notebooks`.")

# --- Conteúdo da Aba 3: Modelagem (ML) ---
with tab_ml:
    st.header("Detalhes da Modelagem e AutoML", anchor=False)
    with st.spinner("Carregando notebook, isso pode levar um momento..."):
        try:
            nb = nbformat.read("notebooks/faixa_de_risco_ML.ipynb", as_version=4)
            nb.metadata.pop("widgets", None)
            for cell in nb.cells:
                cell.metadata.pop("widgets", None)
            exporter = HTMLExporter(template_name="classic")
            html_ml, _ = exporter.from_notebook_node(nb)
            components.html(html_ml, height=800, scrolling=True)
        except FileNotFoundError:
            st.error("Arquivo `faixa_de_risco_ML.ipynb` não encontrado na pasta `notebooks`.")

st.sidebar.divider()
st.sidebar.caption("Desenvolvido por: Ítalo Rufca • Guilherme Predolin Dino • Carolina Althman")