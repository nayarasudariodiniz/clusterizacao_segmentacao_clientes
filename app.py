import streamlit as st
import pandas as pd
import joblib
from io import BytesIO

# Configuração da Página
st.set_page_config(page_title="Segmentação de Clientes", page_icon="🛍️", layout="wide")

@st.cache_resource
def load_model():
    # Carregando os artefatos salvos
    model = joblib.load('kmeans_model.pkl')
    scaler = joblib.load('rfm_scaler.pkl')
    return model, scaler

# Função para converter CSV de Transações em Tabela RFM (Engenharia de Dados)
def pre_processar_dados(df):
    # 1. Limpeza básica
    df_clean = df.dropna(subset=['CustomerID'])
    df_clean = df_clean[(df_clean['Quantity'] > 0) & (df_clean['UnitPrice'] > 0)]
    
    # 2. Criar TotalAmount
    df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['UnitPrice']
    
    # 3. Tratamento de Data
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    snapshot_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    # 4. Cálculo do RFM
    rfm = df_clean.groupby(['CustomerID']).agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalAmount': 'sum'
    })
    
    rfm.rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'TotalAmount': 'Monetary'
    }, inplace=True)
    
    return rfm

# --- INÍCIO DA INTERFACE ---

st.title("🛍️ Sistema de Segmentação de Clientes")
st.markdown("""
Esta aplicação utiliza Inteligência Artificial (K-Means) para agrupar clientes baseados em seu comportamento de compra.
**Faça upload do arquivo de transações (CSV) para descobrir quem são seus clientes VIPs.**
""")

# Carregar modelo e scaler
try:
    kmeans_model, scaler = load_model()
    st.sidebar.success("Modelo e Scaler carregados com sucesso!")
except FileNotFoundError:
    st.error("Erro: Arquivos .pkl não encontrados. Verifique se 'kmeans_model.pkl' e 'rfm_scaler.pkl' estão na pasta.")
    st.stop()

# Upload do Arquivo
uploaded_file = st.file_uploader("Escolha um arquivo CSV de transações", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # Leitura do arquivo (suporta CSV com encoding europeu ou Excel)
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        else:
            df_raw = pd.read_excel(uploaded_file)
            
        st.write("### 1. Visualização dos Dados Brutos")
        st.dataframe(df_raw.head())
        
        # Botão para processar
        if st.button("Processar e Segmentar Clientes"):
            with st.spinner('Calculando métricas RFM e aplicando o modelo...'):
                
                # 1. Transformar Transações em RFM
                df_rfm = pre_processar_dados(df_raw)
                st.write(f"Dados transformados! Total de Clientes Únicos identificados: {df_rfm.shape[0]}")
                
                # 2. Padronizar os dados (Usando o scaler treinado)
                # Importante: O modelo espera dados na mesma escala do treinamento
                rfm_scaled = scaler.transform(df_rfm)
                
                # 3. Predição (Clusterização)
                clusters = kmeans_model.predict(rfm_scaled)
                df_rfm['Cluster'] = clusters
                
                # 4. Dar nomes aos bois (Mapas de Cluster)
                # ATENÇÃO: Verifique se os números batem com o seu treinamento anterior!
                cluster_names = {
                    2: 'VIP (Ouro)',        # Gastam muito
                    3: 'Leais (Prata)',     # Compram sempre
                    0: 'Casuais (Bronze)',  # Compram pouco
                    1: 'Inativos (Churn)'   # Sumidos
                }
                df_rfm['Perfil'] = df_rfm['Cluster'].map(cluster_names)
                
                # 5. Exibir Resultados
                st.write("### 2. Resultado da Segmentação")
                st.dataframe(df_rfm.sort_values('Monetary', ascending=False).head(10))
                
                # 6. Botão de Download
                csv = df_rfm.to_csv().encode('utf-8')
                st.download_button(
                    label="📥 Baixar Relatório Classificado (CSV)",
                    data=csv,
                    file_name='clientes_segmentados.csv',
                    mime='text/csv',
                )
                
                # 7. Resumo Gerencial
                st.write("### 3. Resumo da Base")
                resumo = df_rfm['Perfil'].value_counts()
                st.bar_chart(resumo)

                # --- NOVO BLOCO: Explicação dos Perfis (Agora alinhado corretamente) ---
                st.markdown("---") 
                
                with st.expander("ℹ️ Entenda cada Perfil e Sugestão de Ação"):
                    st.markdown("""
                    **🏆 VIP (Ouro)**
                    * **Quem são:** Clientes que gastam muito, compram com frequência e fizeram compras recentemente.
                    * **Ação:** Atendimento VIP, acesso antecipado a produtos, frete grátis incondicional. Foco em retenção total.
                    
                    **🥈 Leais (Prata)**
                    * **Quem são:** Clientes com gasto consistente e boa frequência. São a base sustentável da loja.
                    * **Ação:** Oferecer programas de fidelidade (pontos) e recomendar produtos complementares (Cross-sell) para aumentar o ticket.
                    
                    **🥉 Casuais (Bronze)**
                    * **Quem são:** Clientes que compram pouco e com baixa frequência. Geralmente buscam preço.
                    * **Ação:** Enviar cupons de desconto agressivos e promoções de "Leve 3, Pague 2" para criar o hábito de compra.
                    
                    **⚠️ Inativos (Churn)**
                    * **Quem são:** Clientes que não compram há muito tempo (alta recência).
                    * **Ação:** Tentar reativação com e-mails de "Sentimos sua falta". Se não responderem, parar de gastar verba de marketing com eles.
                    """)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo: {e}")