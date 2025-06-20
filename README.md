# Faixa de Risco



> Previsão e análise de riscos de acidentes em rodovias brasileiras.

---

## Sobre o Projeto

**Faixa de Risco** é uma aplicação web interativa desenvolvida em Streamlit para:

- **Prever** a quantidade de acidentes rodoviários em um trecho específico (município + BR) para uma data determinada.
- Exibir **estatísticas detalhadas** (percentual de acidentes à noite, clima ruim, feriado).
- Mostrar **histórico** de acidentes em anos anteriores para o mesmo trecho e mês.
- Incluir **notebooks** completos de Análise Exploratória (EDA) e Modelagem (AutoML) diretamente na interface.

Este projeto faz parte do **MBA em Engenharia de Dados** do Mackenzie e foi criado em equipe por:

- **Ítalo Rufca**
- **Guilherme Predolin Dino**
- **Carolina Althman**

---

## Tecnologias

- 🔧 **Python 3.10**
- ⚡ **Streamlit** para dashboard interativo
- 🤖 **PyCaret** para AutoML de regressão
- 📊 **Plotly Express** para visualizações
- 📅 **holidays** para vendas de feriados nacionais
- 📝 **Jupyter Notebook** para EDA e ML
- 📦 **Git & GitHub** para versionamento
- 💾 **Git LFS** para armazenamento do modelo

---

## Estrutura do Repositório

```text
faixa-de-risco/
├── .streamlit/              # Configurações de tema do Streamlit
├── assets/
│   └── logo.png             # Logo do projeto
├── data/
│   ├── acidentes_pronto.csv
│   └── ...                  # Outros CSVs de dados
├── model/
│   └── model.pkl            # Modelo treinado (Git LFS)
├── notebooks/
│   ├── faixa_de_risco_Analise_Exploratoria.ipynb
│   └── faixa_de_risco_ML.ipynb
├── streamlit_app.py         # Aplicação principal
├── requirements.txt         # Dependências Python
└── README.md                # Documentação do projeto
```

---

## Guia de Instalação

1. **Clone este repositório**

   ```bash
   git clone https://github.com/ItaloRufca/faixa-de-risco-MBA.git
   cd faixa-de-risco-MBA
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o app**

   ```bash
   streamlit run streamlit_app.py
   ```

---

## Uso

- No menu lateral, selecione **Previsão**, informe `Data`, `Município` e `BR`.

- Clique em **Predizer 🚀** para exibir:

  - Quantidade prevista de acidentes.
  - Percentuais de acidentes à noite e em clima ruim.
  - Indicação de feriado.
  - Histórico de acidentes (expansível).

- Para ver os Notebooks completos:

  - Selecione **EDA Notebook** ou **ML Notebook** no menu lateral.

---

## Deploy

Este app está disponível online via Streamlit Community Cloud:

```
https://share.streamlit.io/ItaloRufca/faixa-de-risco-MBA/main/streamlit_app.py
```

---

## Contribuição

Contribuições são bem-vindas! Abra issues para sugestões, correções ou melhorias.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

