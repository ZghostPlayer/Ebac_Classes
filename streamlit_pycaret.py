import streamlit as st
import pandas as pd
import pickle
from pycaret.classification import load_model, predict_model
from sklearn.decomposition import PCA

# Carregar o modelo treinado
@st.cache_resource()
def carregar_modelo():
    return load_model('model_final')

# Função para carregar e exibir CSV
def carregar_csv():
    uploaded_file = st.file_uploader("Carregar arquivo CSV", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Prévia dos dados carregados:")
        st.dataframe(df.head())
        return df
    return None

# Função de pré-processamento
def preprocessamento(df):
    df = df.copy()

    # Se 'data_ref' for esperada pelo modelo, adicionamos uma data fake
    if 'data_ref' in modelo.feature_names_in_:
        if 'data_ref' not in df.columns:
            df['data_ref'] = pd.Timestamp('2000-01-01')  # Data fixa para evitar erro
        else:
            df['data_ref'] = pd.to_datetime(df['data_ref'], errors='coerce')  # Converter se existir
    
    # Substituição de nulos
    df.fillna(df.median(numeric_only=True), inplace=True)
    
    # Criando dummies para a variável 'posse_de_veiculo'
    if 'posse_de_veiculo' in df.columns:
        df = pd.get_dummies(df, columns=['posse_de_veiculo'], drop_first=True)
    
    return df

# Função para aplicar PCA na nova base de dados
def aplicar_pca(df, n_components=2):
    if 'pca_1' not in df.columns or 'pca_2' not in df.columns:
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(df.select_dtypes(include=['number']))
        df['pca_1'] = pca_result[:, 0]
        df['pca_2'] = pca_result[:, 1]
    return df

# Interface do Streamlit
st.title("Escoragem de Crédito com PyCaret")
modelo = carregar_modelo()

df = carregar_csv()
if df is not None:
    df_preprocessado = preprocessamento(df)

    # Aplicando PCA se necessário
    df_preprocessado = aplicar_pca(df_preprocessado)

    # Garantindo que as colunas esperadas existem antes de passar para o modelo
    colunas_esperadas = modelo.feature_names_in_
    df_preprocessado = df_preprocessado.reindex(columns=colunas_esperadas, fill_value=0)

    # Aplicando o modelo treinado para escorar os dados
    previsoes = predict_model(modelo, data=df_preprocessado)

    st.write("Resultados da escoragem:")
    st.dataframe(previsoes)

    # Opção para baixar os resultados
    csv = previsoes.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar resultado", data=csv, file_name="resultado_escoragem.csv", mime="text/csv")
