from ticketmaster import TicketmasterAPI

# Cria um objeto que será usado para consultar os eventos.
api = TicketmasterAPI()

# Faz uma busca de eventos na API.
data = api.buscar_eventos(
    # Envia o nome do evento como palavra-chave da busca.
    palavra_chave ={'NOME_EVENTO'},
    # Envia o país que deve ser usado como filtro.
    pais={'PAIS'}
)

# Extrai a lista de eventos da resposta, usando listas vazias se faltarem dados.
events = data.get(
    # Acessa o objeto que contém os dados incorporados na resposta.
    "_embedded",
    # Usa um dicionário vazio caso a chave _embedded não exista.
    {}
).get(
    # Dentro de _embedded, acessa a lista de eventos.
    "events",
    # Usa uma lista vazia caso a chave events não exista.
    []
)

# Percorre cada evento retornado pela API.
for event in events:

    # Imprime uma linha para separar visualmente os eventos.
    print("=" * 50)

    # Exibe o nome do evento, ou None se o nome não estiver disponível.
    print("Evento:", event.get("name"))

    # Exibe o identificador único do evento.
    print(
        "ID:",
        event.get("id")
    )

    # Exibe o horário local de início do evento.
    print(
        "Horário:",
        event.get("dates", {})
             # Acessa o bloco de informações de início.
             .get("start", {})
             # Obtém apenas o horário local dentro desse bloco.
             .get("localTime")
    )
