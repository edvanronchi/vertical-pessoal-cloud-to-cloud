from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('motivo-rescisao', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'motivo-rescisao')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i['tipoAfastamento']:
        i['tipoAfastamento']['id'] = buscarIdDestino('tipo-afastamento', i['tipoAfastamento']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)   

if len(lotes) > 0:
    inserir('motivo-rescisao', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")