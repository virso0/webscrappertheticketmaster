import time

#importa a classe que acessa a API Ticketmaster.
from ticketmaster import TicketmasterAPI
#importa as configurações usadas pelo monitoramento.
from configuracao import (
    #nome do evento que será pesquisado.
    NOME_EVENTO,
    #código do país usado na consulta.
    PAIS,
    #tempo, em segundos, entre duas consultas.
    INTERVALO_VERIFICACAO
)


#define uma função para extrair eventos de uma resposta da API.
def obter_eventos(data):

    #retorna a lista de eventos ou uma lista vazia quando ela não existe.
    return (
        #acessa o conteúdo incorporado da resposta.
        data
        .get("_embedded", {})
        #acessa a chave que contém os eventos.
        .get("events", [])
    )


#define uma função para indexar os eventos pelo identificador único.
def criar_dicionario_eventos(eventos):

    #cria um dicionário usando o ID como chave e o evento completo como valor.
    return {
        #guarda cada evento sob seu identificador.
        evento["id"]: evento
        #percorre todos os eventos recebidos.
        for evento in eventos
        #ignora eventos que não possuam um ID válido.
        if evento.get("id")
    }


#define uma função para mostrar os dados principais de um evento.
def mostrar_evento(evento):

    #obtém o bloco de datas do evento.
    datas = evento.get("dates", {})
    #obtém o bloco com a data e o horário de início.
    inicio = datas.get("start", {})

    #obtém o bloco de informações incorporadas ao evento.
    informacoes = evento.get(
        "_embedded",
        {}
    )

    #obtém a lista de locais associados ao evento.
    locais = informacoes.get(
        "venues",
        []
    )

    #usa o primeiro local quando houver algum; caso contrário, usa um dicionário vazio.
    local = locais[0] if locais else {}

    #imprime uma linha em branco antes dos detalhes.
    print()
    #imprime uma linha separadora para facilitar a leitura.
    print("=" * 50)

    #exibe o nome do evento.
    print(
        f"🎟️ {evento.get('name')}"
    )

    #exibe a data local de início.
    print(
        f"📅 {inicio.get('localDate')}"
    )

    #exibe o horário local de início.
    print(
        f"🕐 {inicio.get('localTime')}"
    )

    #exibe o nome do local do evento.
    print(
        f"📍 {local.get('name')}"
    )

    #exibe o nome da cidade do local.
    print(
        f"🏙️ {local.get('city', {}).get('name')}"
    )

    #exibe o endereço online do evento.
    print(
        f"🔗 {evento.get('url')}"
    )

    #fecha visualmente o bloco de informações.
    print("=" * 50)


#define a função principal que executa o monitoramento contínuo.
def iniciar_monitoramento():

    #cria o cliente usado para consultar a API.
    api = TicketmasterAPI()
    #guarda os eventos encontrados na verificação anterior.
    eventos_anteriores = {}

    #exibe o título do monitor no terminal.
    print("🎟️ TICKET MONITOR")
    #insere uma linha em branco para separar o cabeçalho.
    print()
    #exibe o evento configurado.
    print(f"Evento: {NOME_EVENTO}")
    #exibe o país configurado.
    print(f"País: {PAIS}")
    #exibe o intervalo configurado entre as consultas.
    print(f"Intervalo: {INTERVALO_VERIFICACAO}s")
    #insere uma linha em branco antes de iniciar o loop.
    print()

    #permite encerrar o monitor com Ctrl+C sem mostrar um erro técnico.
    try:

        #mantém o monitor executando continuamente.
        while True:

            #isola erros de uma consulta para que o monitor continue tentando.
            try:

                #consulta os eventos correspondentes ao nome e ao país configurados.
                dados = api.buscar_eventos(
                    #informa a palavra-chave da busca.
                    palavra_chave=NOME_EVENTO,
                    #informa o país da busca.
                    pais=PAIS,
                    #solicita até 100 resultados.
                    quantidade=100
                )

                #extrai a lista de eventos da resposta recebida.
                eventos = obter_eventos(dados)

                #converte a lista atual em um dicionário indexado por ID.
                eventos_atuais = (
                    criar_dicionario_eventos(eventos)
                )

                #informa quantos eventos foram encontrados nesta consulta.
                print(
                    f"🔎 {len(eventos_atuais)} "
                    "eventos encontrados."
                )

                #descobrir eventos novos
                #compara os eventos atuais com os registrados anteriormente.
                for id_evento, evento in eventos_atuais.items():

                    #considera novo todo ID que não existia na consulta anterior.
                    if id_evento not in eventos_anteriores:

                        #insere uma linha em branco antes do alerta.
                        print()
                        #informa que um novo evento foi detectado.
                        print("🚨 NOVO EVENTO ENCONTRADO!")

                        #mostra os detalhes do evento recém-encontrado.
                        mostrar_evento(evento)

                #atualiza a referência para comparar com a próxima consulta.
                eventos_anteriores = eventos_atuais

            #captura qualquer erro ocorrido durante a consulta ou o processamento.
            except Exception as erro:

                #insere uma linha em branco antes da mensagem de erro.
                print()
                #exibe o erro sem encerrar o monitor.
                print(
                    f"❌ Ocorreu um erro: {erro}"
                )

            #insere uma linha em branco antes da próxima mensagem.
            print()
            #informa quando a próxima verificação será realizada.
            print(
                f"⏳ Próxima verificação em "
                f"{INTERVALO_VERIFICACAO} segundos..."
            )

            #pausa o programa pelo intervalo configurado.
            time.sleep(
                INTERVALO_VERIFICACAO
            )

    #trata o encerramento manual feito com Ctrl+C.
    except KeyboardInterrupt:

        #insere uma linha em branco antes da mensagem final.
        print()
        #confirma que o monitor foi encerrado pelo usuário.
        print("🛑 Monitoramento encerrado pelo usuário.")
        #o comando para finalizar o código é "ctrl + c" diretamente sob o terminal.


#executa o monitor apenas quando este arquivo é iniciado diretamente.
if __name__ == "__main__":
    #chama a função principal do monitoramento.
    iniciar_monitoramento()
