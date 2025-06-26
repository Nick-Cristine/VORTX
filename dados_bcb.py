import pandas as pd
import requests

# -----------------------------------------------
# Função para buscar dados na API
# -----------------------------------------------
def buscar_dados(url, parametros=None):
    try:
        resposta = requests.get(url, params=parametros)
        # Garante que erros HTTP dispararão exceções
        resposta.raise_for_status()
        print(f"DEBUG: Dados obtidos com sucesso da URL: {url}")
        return resposta.json()
    except requests.exceptions.RequestException as e:
        # Trata qualquer erro de rede ou HTTP não-OK
        print(f"ERRO: Falha ao buscar dados da URL {url}. Erro: {e}")
        raise

# ==================================================
# 1. Coleta do IPCA (série 10844) para o ano 2024
# ==================================================
print("--- Iniciando busca de dados do IPCA para 2024 ---")
url_ipca = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.10844/dados'

# Parâmetros que definem período e formato da resposta
parametros_ipca_2024 = {
    'formato': 'json',
    'dataInicial': '01/01/2024',
    'dataFinal': '31/12/2024'
}

# Chamada à função de busca da api
dados_ipca = buscar_dados(url_ipca, parametros_ipca_2024)

if dados_ipca:
    # Converte JSON → DataFrame
    df_ipca_2024 = pd.DataFrame(dados_ipca)

    # Exporta direto para Excel
    nome_arquivo_ipca = 'ipca_2024.xlsx'
    df_ipca_2024.to_excel(nome_arquivo_ipca, index=False)
    print(f"SUCESSO: Arquivo '{nome_arquivo_ipca}' salvo com os dados do IPCA de 2024.")
else:
    # Caso a API retorna lista vazia
    print("AVISO: Nenhum dado de IPCA foi retornado ou houve um erro na busca.")

# ==================================================
# 2. Coleta de Meios de Pagamento Mensais 2024
# ==================================================
print("\n--- Iniciando busca de dados de Meios de Pagamento Mensais ---")

url_base_meios_pagamento = (
    "https://olinda.bcb.gov.br/olinda/servico/"
    "MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosMensalDA(AnoMes=@AnoMes)"
)

# Consulta de Janeiro de 2024 até o último mês apurado
parametros_inicio_2024 = {
    '@AnoMes': "'202401'",
    '$format': 'json'
}

print("DEBUG: Buscando dados de Meios de Pagamento a partir de 202401...")
# Retorna dicionário contendo chave 'value' com a lista de registros
resposta_meios_pagamento = buscar_dados(url_base_meios_pagamento, parametros=parametros_inicio_2024)
registros_meios_pagamento = resposta_meios_pagamento.get('value', [])

if registros_meios_pagamento:
    # DataFrame bruto com todos os registros retornados
    df_meios_pagamento_bruto = pd.DataFrame(registros_meios_pagamento)

    # Filtra apenas meses de 202401 a 202412
    df_meios_pagamento_2024 = df_meios_pagamento_bruto[
        (df_meios_pagamento_bruto['AnoMes'].astype(int) >= 202401) &
        (df_meios_pagamento_bruto['AnoMes'].astype(int) <= 202412)
    ].copy()

    # Exporta resultado final
    nome_arquivo_meios_pagamento = "meios_pagamento_2024.xlsx"
    df_meios_pagamento_2024.to_excel(nome_arquivo_meios_pagamento, index=False)
    print(f"SUCESSO: Arquivo '{nome_arquivo_meios_pagamento}' salvo com os dados de Meios de Pagamento de 2024.")
else:
    print("AVISO: Nenhum dado de Meios de Pagamento foi retornado ou houve um erro na busca.")

print("\n--- Processo de busca e salvamento de dados concluído ---")
