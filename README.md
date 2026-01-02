# 📊 ETL Vagas Gupy - Monitor de Oportunidades de Dados

Este projeto é um pipeline de Engenharia de Dados (ETL) que automatiza a coleta, tratamento e análise de vagas de emprego na plataforma Gupy, focado em tecnologias de dados (Power BI, SQL, Python) em todo o território nacional.

## 🚀 Funcionalidades

* **Extract (Extração):** Robô (Web Scraper) desenvolvido com `Selenium` que simula navegação humana para buscar vagas.
* **Transform (Transformação):**
    * Classificação automática de localidade (identifica cidades polo como Barueri, Campinas e capitais).
    * Identificação de ferramentas exigidas (Power BI, SQL, Python, Excel).
    * Padronização de dados e remoção de duplicatas.
* **Load (Carga):** Conexão via API com o **Google Sheets** para armazenamento em nuvem.
* **Dashboard:** Os dados alimentam um painel no **Power BI** para visualização de tendências de mercado.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Automação Web:** Selenium WebDriver
* **Manipulação de Dados:** Pandas
* **Cloud/Armazenamento:** Google Sheets API (`gspread`)
* **Ambiente de Execução:** Kaggle Notebooks (Cloud Computing)

## ⚙️ Como Funciona a Lógica de Geolocalização

O script possui um mapeamento inteligente que corrige inconsistências comuns em descrições de vagas.
* *Exemplo:* Uma vaga listada como "Barueri - SP" ou "Alphaville" é automaticamente categorizada como **São Paulo**.
* *Exemplo:* Vagas com termos "Home Office" ou "Remote" têm prioridade e são classificadas como **Remoto**, independente da cidade sede da empresa.

## 📦 Como Executar

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/SEU-USUARIO/ETL-VAGAS-GUPY.git](https://github.com/SEU-USUARIO/ETL-VAGAS-GUPY.git)
    ```
2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configuração de Credenciais:
    * É necessário um arquivo `service_account.json` do Google Cloud Platform para acesso à API do Sheets.
    * *Nota: Por segurança, as credenciais não estão incluídas neste repositório.*

