from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('averbacao-matricula', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'averbacao-matricula')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i.get('matricula'):
        i['matricula']['id'] = buscarIdDestino('matricula', i['matricula']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('averbacao-matricula', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")