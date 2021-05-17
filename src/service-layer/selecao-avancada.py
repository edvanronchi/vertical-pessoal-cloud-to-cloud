from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('selecao-avancada', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'selecao-avancada')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    for j in i['filtro']['organogramas']:
        j['id'] = buscarIdDestino('organograma', j['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('selecao-avancada', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")