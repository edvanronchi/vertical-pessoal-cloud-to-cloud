from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('lotacao-fisica', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'lotacao-fisica')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i['configuracao']:
        i['configuracao']['id'] = buscarIdDestino('configuracao-lotacao-fisica', i['configuracao']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)   

if len(lotes) > 0:
    inserir('lotacao-fisica', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")