# 🛍️ Customer Segmentation & Clustering Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Scikit-Learn](https://img.shields.io/badge/ML-KMeans-orange)

## 📌 Sobre o Projeto

Este projeto consiste em uma solução *End-to-End* de Ciência e Engenharia de Dados para segmentação de clientes de um E-commerce internacional. 

O objetivo foi transformar dados transacionais brutos em inteligência de negócio, identificando perfis de consumo através da metodologia **RFM (Recência, Frequência e Monetarização)** e agrupamento com algoritmo **K-Means**. A entrega final é uma aplicação Web onde o time de Marketing pode fazer upload de novos dados e receber a classificação automática dos clientes (VIPs, Leais, Em Risco, etc.).

## 🏗️ Arquitetura e Tecnologias

O projeto foi estruturado simulando um cenário real de produção:

* **Coleta de Dados:** Script automatizado para download de dados via API do Kaggle.
* **ETL (Extract, Transform, Load):** Limpeza de dados, tratamento de nulos/devoluções e engenharia de atributos (Criação da tabela RFM) utilizando **Pandas**.
* **Machine Learning:**
    * Padronização de dados com `StandardScaler`.
    * Clusterização com **K-Means**.
    * Otimização de hiperparâmetros (Método do Cotovelo e Silhouette Score).
* **Deploy / Aplicação:** Interface interativa desenvolvida em **Streamlit**.

## 📊 Resultados e Perfis Identificados

O modelo identificou 4 clusters distintos de comportamento:

| Perfil | Características | Estratégia Recomendada |
| :--- | :--- | :--- |
| **🏆 VIP (Ouro)** | Alto ticket, alta frequência e compra recente. | Atendimento exclusivo e retenção. |
| **🥈 Leais (Prata)** | Compram com regularidade e bom ticket. | Programas de fidelidade e Cross-sell. |
| **🥉 Casuais (Bronze)** | Ticket baixo e compras esporádicas. | Incentivos de volume (cupons). |
| **⚠️ Inativos (Churn)** | Não compram há muito tempo (+200 dias). | Campanhas de reativação ou limpeza de base. |

##  Como Executar o Projeto

### Pré-requisitos
* Python 3.x
* Conta no Kaggle (para baixar o dataset original)

### 1. Instalação
Clone este repositório e instale as dependências:

```bash
git clone [https://github.com/nayarasudariodiniz/clusterizacao_segmentacao_clientes.git](https://github.com/nayarasudariodiniz/clusterizacao_segmentacao_clientes.git)
cd NOME-DO-REPO
pip install -r requirements.txt
```
### 2. Coleta dos Dados (Automática)
Para baixar a base de dados original ("E-Commerce Data" da UCI), você precisa configurar sua API do Kaggle:

* Gere seu token no site do Kaggle (`kaggle.json`).
* Coloque o arquivo na pasta padrão (`~/.kaggle/` ou `C:\Users\Voce\.kaggle\`).
* Execute o Jupyter Notebook `01_analise_exploratoria.ipynb`. A primeira célula fará o download automático.

### 3. Rodando a Aplicação Web
Com os arquivos de modelo (`.pkl`) gerados pelo notebook (ou já presentes no repo), execute:

```bash
streamlit run app.py
```

O navegador abrirá automaticamente a interface de segmentação.

### 4. Testando com Novos Dados
Para simular novos dados de entrada, execute o script gerador:

```bash
python gerar_teste.py
```

Isso criará o arquivo `novas_entradas.csv`, que pode ser carregado na aplicação Streamlit para validação.

## 📈 Aprendizados e Desafios

* **Tratamento de Dados Transacionais:** O maior desafio foi converter um log de vendas (transacional) em uma visão única por cliente (analítica) usando agregações complexas.
* **Validação de Clusters:** O uso conjunto da Inércia e Silhouette Score foi fundamental para decidir entre 2 ou 4 clusters, equilibrando matemática e utilidade de negócio.
* **Engenharia de Software:** A estruturação do `app.py` exigiu encapsular o pré-processamento em funções para garantir que novos dados passem pelo mesmo tratamento do treino.
