import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configurações
num_linhas = 200
data_hoje = datetime.now()

# Listas para simular dados reais
produtos = [
    ('WHITE HANGING HEART T-LIGHT HOLDER', 2.55),
    ('WHITE METAL LANTERN', 3.39),
    ('CREAM CUPID HEARTS COAT HANGER', 2.75),
    ('KNITTED UNION FLAG HOT WATER BOTTLE', 3.39),
    ('RED WOOLLY HOTTIE WHITE HEART.', 3.39),
    ('SET 7 BABUSHKA NESTING DOLLS', 7.65),
    ('GLASS STAR FROSTED T-LIGHT HOLDER', 4.25)
]

dados = []

# Gerando linhas
for i in range(num_linhas):
    # Escolhe um produto aleatório
    prod_desc, prod_price = random.choice(produtos)
    
    # Simula Quantidade (maioria positiva, alguns negativos para testar limpeza)
    if random.random() < 0.05: # 5% de chance de ser devolução
        qtd = random.randint(-5, -1)
        invoice_no = f"C{random.randint(500000, 600000)}" # Começa com C de Cancelamento
    else:
        qtd = random.randint(1, 50)
        invoice_no = f"{random.randint(500000, 600000)}"
    
    # Simula Data (nos últimos 365 dias)
    dias_atras = random.randint(0, 365)
    data_fatura = data_hoje - timedelta(days=dias_atras)
    
    # Simula CustomerID (alguns nulos para testar o dropna)
    if random.random() < 0.1: # 10% de chance de ser nulo
        cust_id = np.nan
    else:
        # Cria alguns perfis fixos para cair nos clusters certos
        tipo_cliente = random.choice(['VIP', 'Normal', 'Sumido'])
        if tipo_cliente == 'VIP':
            cust_id = 10001 # Vai gastar muito
            qtd = qtd * 5 # Aumenta o volume
        elif tipo_cliente == 'Sumido':
            cust_id = 10002
            data_fatura = data_hoje - timedelta(days=random.randint(200, 360)) # Data antiga
        else:
            cust_id = random.randint(11000, 18000)

    # Monta a linha
    dados.append({
        'InvoiceNo': invoice_no,
        'StockCode': f"{random.randint(10000, 99999)}",
        'Description': prod_desc,
        'Quantity': qtd,
        'InvoiceDate': data_fatura.strftime("%m/%d/%Y %H:%M"), # Formato padrão do dataset original
        'UnitPrice': prod_price,
        'CustomerID': cust_id,
        'Country': 'United Kingdom'
    })

# Cria o DataFrame
df_teste = pd.DataFrame(dados)

# Salva como CSV
df_teste.to_csv('novas_entradas.csv', index=False, encoding='ISO-8859-1')

print("Arquivo 'novas_entradas.csv' gerado com sucesso!")
print(f"Amostra:\n{df_teste.head()}")