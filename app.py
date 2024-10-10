import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st


path_ibyte = 'RECLAMEAQUI_IBYTE.csv'
path_hapvida = 'RECLAMEAQUI_HAPVIDA.csv'
path_nagem = 'RECLAMEAQUI_NAGEM.csv'



df_ibyte = pd.read_csv(path_ibyte)
df_hapvida = pd.read_csv(path_hapvida)
df_nagem = pd.read_csv(path_nagem)


#Adicionando colunas com o nome da empresa
df_ibyte["EMPRESA"] = "Ibyte"
df_hapvida["EMPRESA"] = "Hapvida"
df_nagem["EMPRESA"] = "Nagem"


df_total = pd.concat([df_ibyte, df_hapvida, df_nagem], ignore_index=True)


# Análise de Serie temporal

# Convertendo as colunas de 'ANO', 'MES' e 'DIA' em um datetime
df_total['DATA'] = pd.to_datetime(df_total[['ANO', 'MES', 'DIA']].rename(columns={'ANO': 'year', 'MES': 'month', 'DIA': 'day'}))

# Agrupar por data e contar o número de reclamações por dia
serie_temporal = df_total.groupby('DATA').size()

# Plotando
plt.figure(figsize=(12, 6))
serie_temporal.plot()
plt.title('Série Temporal do Número de Reclamações')
plt.xlabel('Data')
plt.ylabel('Número de Reclamações')
plt.show()



# Frequencia por estado

frequencia_por_estado = df_total['LOCAL'].value_counts()
print(frequencia_por_estado)


# Agrupamento por 'STATUS'
frequencia_por_status = df_total['STATUS'].value_counts()
print(frequencia_por_status)


# Distribuição do tamanho do texto (coluna DESCRIÇÃO)

df_total['TAMANHO_DESCRICAO'] = df_total['DESCRICAO'].apply(len)

plt.figure(figsize=(12, 6))
df_total['TAMANHO_DESCRICAO'].hist(bins=30)
plt.title('Distribuição do Tamanho das Descrições')
plt.xlabel('Tamanho do Texto')
plt.ylabel('Frequência')
plt.show()


# CRIANDO O PAINEL NO STREAMLIT


st.title("PAINEL DE RECLAMAÇÕES")

print("")

empresas = df_total['EMPRESA'].unique()



# Menu lateral
st.sidebar.title('Menu')
paginaSelecionada = st.sidebar.selectbox('Selecione a análise', [
    '1. Série temporal do número de reclamações.',
    '2. Frequência de reclamações por estado.',
    '3. Frequência de cada tipo de **STATUS**',
    '4. Distribuição do tamanho do texto (coluna **DESCRIÇÃO**)'
], key='pagina_selecionada') 


empresa_selecionada = st.sidebar.selectbox("Selecione a Empresa", empresas, key='empresa_selecionada')  

df_filtrado = df_total[df_total['EMPRESA'] == empresa_selecionada]

    

# Análises com base na página selecionada
if paginaSelecionada == '1. Série temporal do número de reclamações.':
    st.title('Série temporal do número de reclamações')
    
    df_filtrado['DATA'] = pd.to_datetime(df_filtrado[['ANO', 'MES', 'DIA']].rename(columns={'ANO': 'year', 'MES': 'month', 'DIA': 'day'}))
    
    serie_temporal = df_filtrado.groupby('DATA').size()
    
    # Plotando
    plt.figure(figsize=(12, 6))
    serie_temporal.plot()
    plt.title(f'Série Temporal do Número de Reclamações - {empresa_selecionada}')
    plt.xlabel('Data')
    plt.ylabel('Número de Reclamações')
    st.pyplot(plt)
    plt.clf()  

elif paginaSelecionada == '2. Frequência de reclamações por estado.':
    st.title('Frequência de reclamações por estado')
    
    # Agrupamento por local
    frequencia_por_estado = df_filtrado['LOCAL'].value_counts()
    
    st.bar_chart(frequencia_por_estado)  
    st.table(frequencia_por_estado)  

elif paginaSelecionada == '3. Frequência de cada tipo de **STATUS**':
    st.title('Frequência de cada tipo de **STATUS**')
    
    # Agrupamento por 'STATUS' 
    frequencia_por_status = df_filtrado['STATUS'].value_counts()
    
    st.bar_chart(frequencia_por_status)  
    st.table(frequencia_por_status)  

elif paginaSelecionada == '4. Distribuição do tamanho do texto (coluna **DESCRIÇÃO**)':
    st.title('Distribuição do tamanho do texto (coluna **DESCRIÇÃO**)')
    
    df_filtrado['TAMANHO_DESCRICAO'] = df_filtrado['DESCRICAO'].apply(len)
    
    # Plotando
    plt.figure(figsize=(12, 6))
    df_filtrado['TAMANHO_DESCRICAO'].hist(bins=30)
    plt.title(f'Distribuição do Tamanho das Descrições para {empresa_selecionada}')
    plt.xlabel('Tamanho do Texto')
    plt.ylabel('Frequência')
    
    st.pyplot(plt)
    plt.clf()  
