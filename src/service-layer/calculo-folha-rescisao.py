from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('calculo-folha-rescisao', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'calculo-folha-rescisao')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i.get('motivoRescisao'):
        i['motivoRescisao']['id'] = buscarIdDestino('motivo-rescisao', i['motivoRescisao']['id'])

    if i.get('ato'):
        i['ato']['id'] = buscarIdDestino('ato', i['ato']['id'])       

    for j in i['calculoFolhaMatriculas']:
        if j.get('matricula'):
            j['matricula']['id'] = buscarIdDestino('matricula', j['matricula']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('calculo-folha-rescisao', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")