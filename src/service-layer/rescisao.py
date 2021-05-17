from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('rescisao', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'rescisao')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i.get('ato'):
        i['ato']['id'] = buscarIdDestino('ato', i['ato']['id'])

    if i.get('matricula'):
        i['matricula']['id'] = buscarIdDestino('matricula', i['matricula']['id'])

    if i.get('motivoRescisao'):
        i['motivoRescisao']['id'] = buscarIdDestino('motivo-rescisao', i['motivoRescisao']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('rescisao', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")