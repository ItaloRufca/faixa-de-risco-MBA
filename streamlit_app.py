import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from pycaret.regression import predict_model
import holidays
import streamlit.components.v1 as components
import nbformat
from nbconvert import HTMLExporter

# --- Configuração da página e tema ---
st.set_page_config(
    page_title="Faixa de Risco",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS customizado para o seu primaryColor ---
st.markdown("""
<style>
  :root { --primary-color: #3872fb; }
  [data-baseweb="slider"] .innerTrack { background-color: var(--primary-color) !important; }
  .stDateInput .CalendarDay__selected,
  .stDateInput .CalendarDay__selected:hover {
    background-color: var(--primary-color) !important;
    border-color: var(--primary-color) !important;
  }
  button:hover { background-color: var(--primary-color) !important; border-color: var(--primary-color) !important; }
  /* Estiliza o selectbox de navegação e botões da sidebar */
  .stSidebar .stSelectbox, .stSidebar button {
    border-radius: 8px;
    padding: 6px;
  }
</style>
""", unsafe_allow_html=True)

# --- Header com logo e título ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=100)
with col2:
    st.title("Faixa de Risco")

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

# --- Navegação lateral ---
page = st.sidebar.selectbox("Página", ["Previsão","EDA Notebook","ML Notebook"])

# --- Página de Previsão ---
if page == "Previsão":
    st.sidebar.header("Parâmetros")
    data = st.sidebar.date_input("Data")
    municipio = st.sidebar.selectbox("Município", sorted(df0["municipio"].unique()))
    br_choices = df0[df0['municipio']==municipio]['br'].unique().tolist()
    br = st.sidebar.selectbox("BR", br_choices)
    if st.sidebar.button("Predizer 🚀"):
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

        c1,c2,c3 = st.columns(3)
        c1.metric("Acidentes Previstos",f"{qa:.2f}")
        c2.metric("% à Noite",f"{defaults['proporcao_noite']*100:.1f}%")
        c3.metric("% Clima Ruim",f"{defaults['clima_ruim']*100:.1f}%")
        st.markdown(f"**Feriado:** {fer}")

        st.markdown("### Detalhes")
        st.markdown(f"""
- **Município:** {municipio}
- **BR:** {br}
- **Data:** {data:%Y-%m-%d}
- **Ano:** {ano}
- **Mês:** {mes:02d}
        """)

        hist = (df0[(df0['municipio']==municipio)&(df0['br']==br)&(df0['mes']==mes)]
                .groupby('ano')['qtd_acidentes'].sum().reset_index())
        with st.expander("Histórico"):
            fig=px.line(hist,x='ano',y='qtd_acidentes',markers=True,
                        labels={'ano':'Ano','qtd_acidentes':'Qtd Acidentes'})
            fig.update_xaxes(dtick=1,tickformat='d')
            st.plotly_chart(fig,use_container_width=True)

    st.caption("Ítalo Rufca • Guilherme Predolin Dino • Carolina Althman")

# --- Página de EDA (nbconvert dinâmico) ---
elif page == "EDA Notebook":
    st.subheader("Análise Exploratória")
    nb = nbformat.read("notebooks/faixa_de_risco_Analise_Exploratoria.ipynb", as_version=4)
    nb.metadata.pop("widgets", None)
    for cell in nb.cells:
        cell.metadata.pop("widgets", None)
    exporter = HTMLExporter(template_name="classic")
    eda_html, _ = exporter.from_notebook_node(nb)
    components.html(eda_html, height=800, scrolling=True)

# --- Página de ML (nbconvert dinâmico) ---
else:
    st.subheader("Modelagem & AutoML")
    nb = nbformat.read("notebooks/faixa_de_risco_ML.ipynb", as_version=4)
    nb.metadata.pop("widgets", None)
    for cell in nb.cells:
        cell.metadata.pop("widgets", None)
    exporter = HTMLExporter(template_name="classic")
    html_ml, _ = exporter.from_notebook_node(nb)
    components.html(html_ml, height=800, scrolling=True)
