import os
from dotenv import load_dotenv
#importa a função que carrega as variáveis definidas em um arquivo .env.


load_dotenv()
#lê o arquivo .env e coloca suas variáveis no ambiente do processo.

#obtém a chave da API Ticketmaster usando o nome definido no ambiente.
CHAVE_API = os.getenv("TICKETMASTER_API_KEY")
# informa qual variável de ambiente deve ser consultada.


#coloquei este padrão que vi que tinha na API, mas pode ser colocado qualquer outro
NOME_EVENTO = "Eagles Live at Sphere"

#aqui se coloca o código do país usado no filtro da API.
PAIS = "us"

#define o intervalo, em segundos, entre as verificações do monitor.
INTERVALO_VERIFICACAO = 15


#interrompe a execução caso a chave da API não tenha sido configurada.
if not CHAVE_API:

    #gera um erro claro para informar como resolver a configuração ausente.
    raise RuntimeError(
        #explica que a chave deve ser adicionada ao arquivo .env.
        "Chave da API não encontrada. "
        "Verifique o arquivo .env."
    )
