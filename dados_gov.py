import pandas as pd
import requests

def buscar_dados(url, parametros=None):
    try:
        resposta = requests.get(url, params=parametros)
        resposta.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        print(f"DEBUG: Dados obtidos com sucesso da URL: {url}")
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao buscar dados da URL {url}. Erro: {e}")
        raise

# --- 1. IPCA - Série 2024 ---
print("--- Iniciando busca de dados do IPCA para 2024 ---")
url_ipca = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.10844/dados'
parametros_ipca_2024 = {
    'formato': 'json',
    'dataInicial': '01/01/2024',
    'dataFinal': '31/12/2024'
}
dados_ipca = buscar_dados(url_ipca, parametros_ipca_2024)

if dados_ipca:
    df_ipca_2024 = pd.DataFrame(dados_ipca)
    nome_arquivo_ipca = 'ipca_2024.xlsx'
    df_ipca_2024.to_excel(nome_arquivo_ipca, index=False)
    print(f"SUCESSO: Arquivo '{nome_arquivo_ipca}' salvo com os dados do IPCA de 2024.")

else:
    print("AVISO: Nenhum dado de IPCA foi retornado ou houve um erro na busca.")

# --- 2. Meios de Pagamento Mensais (por AnoMes) ---
print("\n--- Iniciando busca de dados de Meios de Pagamento Mensais ---")
url_base_meios_pagamento = (
    "https://olinda.bcb.gov.br/olinda/servico/"
    "MPV_DadosAbertos/versao/v1/odata/MeiosdePagamentosMensalDA(AnoMes=@AnoMes)"
)

# Parâmetros para buscar dados a partir de Janeiro de 2024
parametros_inicio_2024 = {
    '@AnoMes': "'202401'",
    '$format': 'json'
}

print("DEBUG: Buscando dados de Meios de Pagamento a partir de 202401...")
resposta_meios_pagamento = buscar_dados(url_base_meios_pagamento, parametros=parametros_inicio_2024)
registros_meios_pagamento = resposta_meios_pagamento.get('value', [])

if registros_meios_pagamento:
    df_meios_pagamento_bruto = pd.DataFrame(registros_meios_pagamento)
    # Filtra o DataFrame para incluir apenas os meses até 202412
    # Convertemos 'AnoMes' para inteiro para facilitar a comparação numérica.
    df_meios_pagamento_2024 = df_meios_pagamento_bruto[
        (df_meios_pagamento_bruto['AnoMes'].astype(int) >= 202401) &
        (df_meios_pagamento_bruto['AnoMes'].astype(int) <= 202412)
    ].copy()

    nome_arquivo_meios_pagamento = "meios_pagamento_2024.xlsx"
    df_meios_pagamento_2024.to_excel(nome_arquivo_meios_pagamento, index=False)
    print(f"SUCESSO: Arquivo '{nome_arquivo_meios_pagamento}' salvo com os dados de Meios de Pagamento de 2024.")
else:
    print("AVISO: Nenhum dado de Meios de Pagamento foi retornado ou houve um erro na busca.")

print("\n--- Processo de busca e salvamento de dados concluído ---")