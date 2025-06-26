
<p align="center">
  <img src="assets/logo.png" alt="Faixa de Risco" width="300"/>
</p>

<h1 align="center">Faixa de Risco</h1>

<p align="center">
  Previsão e análise de riscos de acidentes em rodovias brasileiras.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" />
  <img src="https://img.shields.io/badge/Streamlit-Enabled-brightgreen" />
  <img src="https://img.shields.io/github/license/ItaloRufca/faixa-de-risco-MBA" />
</p>

---

## 🔎 Sobre o Projeto

**Faixa de Risco** é uma aplicação web interativa desenvolvida em Streamlit para:

- **Prever** a quantidade de acidentes rodoviários em um trecho específico (`município + BR`) para uma data determinada.
- Exibir **estatísticas detalhadas** (percentual de acidentes à noite, clima ruim, feriado).
- Mostrar **histórico** de acidentes em anos anteriores.
- Incluir **notebooks** completos de Análise Exploratória (EDA) e Modelagem (AutoML).

👨‍🎓 Projeto final do **MBA em Engenharia de Dados** – Mackenzie  
👥 Desenvolvido por:
- Ítalo Rufca
- Guilherme Predolin Dino
- Carolina Althman

---

## 🚀 Tecnologias Utilizadas

- 🔧 Python 3.10
- ⚡ Streamlit
- 🤖 PyCaret (AutoML de Regressão)
- 📊 Plotly Express
- 📅 Holidays (feriados nacionais)
- 📓 Jupyter Notebook
- 💻 Git & GitHub
- 💾 Git LFS

---

## 📁 Estrutura do Repositório

```
faixa-de-risco/
├── .streamlit/              # Tema do Streamlit
├── assets/                  # Logo do projeto
├── data/                    # Arquivos de dados
├── model/                   # Modelo treinado (pkl via LFS)
├── notebooks/               # Jupyter Notebooks (EDA e ML)
├── streamlit_app.py         # Aplicação principal
├── requirements.txt         # Dependências
└── README.md                # Documentação
```

---

## 🛠️ Guia de Instalação

### 1. Clone este repositório

```bash
git clone https://github.com/ItaloRufca/faixa-de-risco-MBA.git
cd faixa-de-risco-MBA
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv venv
.env\Scriptsctivate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Execução da Aplicação

Para iniciar a aplicação Streamlit:

```bash
streamlit run streamlit_app.py
```

---

## 📓 Como Reproduzir os Notebooks Localmente

### 1. Acesse a pasta `notebooks/`

```bash
cd notebooks
```

### 2. Execute via Jupyter

```bash
jupyter notebook
```

### 3. Notebooks disponíveis

- `faixa_de_risco_Analise_Exploratoria.ipynb`: análise exploratória dos dados de acidentes.
- `faixa_de_risco_ML.ipynb`: pipeline de modelagem preditiva com AutoML.

> ⚠️ Garanta que os dados estejam na pasta `data/` e que as dependências estejam instaladas para o funcionamento correto.

---

## 🧪 Uso

- No menu lateral do app, selecione **Previsão**
  - Informe: `Data`, `Município`, `BR`
- Clique em **Predizer 🚀**
  - Veja os resultados:
    - Previsão de acidentes
    - Acidentes em clima ruim ou à noite
    - Verificação de feriado
    - Histórico do mês/trecho

- Acesse também os notebooks completos:
  - **EDA Notebook**
  - **ML Notebook**

---

## ☁️ Deploy

Você pode acessar a aplicação online via Streamlit Cloud:

```bash
https://share.streamlit.io/ItaloRufca/faixa-de-risco-MBA/main/streamlit_app.py
```

---

## 🤝 Contribuição

Contribuições são muito bem-vindas!  
Abra uma *issue* com sua sugestão, correção ou melhoria.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
