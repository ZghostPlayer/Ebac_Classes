#import das bibliotecas a serem utilizadas
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

#criação da função para automatização da criação de gráficos
def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index, aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None

# Verificar se os meses foram passados como argumento
if len(sys.argv) < 2:
    print("Por favor, forneça uma lista de abreviaturas de meses (ex: MAR ABR MAI JUN)")
    sys.exit(1)

# Obter a lista de meses a partir dos argumentos do script
meses = sys.argv[1:]

for mes in meses:
    print(f'Processando mês de referência: {mes}')

    # Definição do arquivo CSV a ser lido
    sinasc = pd.read_csv(f'./input/SINASC_RO_2019_{mes}.csv')

    # Definir o nome que será utilizado como título da pasta onde serão salvos os gráficos
    max_data = sinasc.DTNASC.max()[:7]
    print(max_data)

    # Criar o diretório que será utilizado para guardar os gráficos
    output_dir = f'./output/figs/{max_data}'
    os.makedirs(output_dir, exist_ok=True)

    # Utilizar a função para gerar os gráficos no formato PNG e armazenar no diretório anteriormente definido
    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')
    plt.savefig(f'{output_dir}/media idade mae por data.png')

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'peso bebe', 'escolaridade mae', 'sort')
    plt.savefig(f'{output_dir}/peso por escolaridade mae.png')

    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae', 'data de nascimento', 'unstack')
    plt.savefig(f'{output_dir}/media idade mae por sexo.png')

    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe', 'data de nascimento', 'unstack')
    plt.savefig(f'{output_dir}/media peso bebe por sexo.png')

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'PESO mediano', 'escolaridade mae', 'sort')
    plt.savefig(f'{output_dir}/PESO mediano por escolaridade mae.png')

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio', 'gestacao', 'sort')
    plt.savefig(f'{output_dir}/media apgar1 por gestacao.png')

print("Processamento concluído.")
