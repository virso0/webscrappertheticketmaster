import requests

#importa a chave da API carregada pelo módulo de configuração.
from configuracao import CHAVE_API


#define a classe que encapsula as operações da API Ticketmaster.
class TicketmasterAPI:

    #define a URL base usada para montar os endpoints da API.
    URL_BASE = "https://app.ticketmaster.com/discovery/v2"

    #inicializa uma nova instância do cliente da API.
    def __init__(self):

        #garante que a aplicação não tente acessar a API sem uma chave.
        if not CHAVE_API:
            #informa que a configuração obrigatória está ausente.
            raise RuntimeError(
                "Chave da API não encontrada."
            )

        #cria uma sessão HTTP reutilizável para as requisições.
        self.sessao = requests.Session()

    #define um método para buscar vários eventos.
    def buscar_eventos(
        self,
        #define a palavra-chave opcional da busca.
        palavra_chave=None,
        #define a cidade opcional da busca.
        cidade=None,
        #define o país padrão como Brasil.
        pais="BR",
        #define a quantidade padrão de resultados.
        quantidade=20
    ):

        #monta a url completa do endpoint de eventos.
        url = f"{self.URL_BASE}/events.json"

        #cria os parâmetros enviados à API.
        parametros = {
            #esse nome precisa permanecer
            #exatamente como a API espera.
            #envia a chave de autenticação.
            "apikey": CHAVE_API,

            #envia o código do país para filtrar os resultados.
            "countryCode": pais,

            #define o número máximo de eventos retornados.
            "size": quantidade
        }

        #só adiciona a palavra-chave quando ela foi informada.
        if palavra_chave:
            #usa a palavra-chave no parâmetro esperado pela API.
            parametros["keyword"] = palavra_chave

        #faz a requisição GET com os parâmetros e um limite de espera.
        resposta = self.sessao.get(
            url,
            params=parametros,
            timeout=15
        )

        #lança uma exceção se a API retornar um status HTTP de erro.
        resposta.raise_for_status()

        #converte a resposta JSON em um dicionário Python e o retorna.
        return resposta.json()

    #define um método para buscar um evento específico pelo ID.
    def buscar_evento(self, id_evento):

        #monta a URL do endpoint que representa um evento individual.
        url = (
            f"{self.URL_BASE}/events/"
            f"{id_evento}.json"
        )

        #cria os parâmetros necessários para autenticar a consulta.
        parametros = {
            #envia a chave da API.
            "apikey": CHAVE_API
        }

        #faz a requisição GET para o evento informado.
        resposta = self.sessao.get(
            url,
            params=parametros,
            timeout=15
        )

        #lança uma exceção caso a resposta indique um erro HTTP.
        resposta.raise_for_status()

        #converte a resposta JSON em um dicionário Python e o retorna.
        return resposta.json()
