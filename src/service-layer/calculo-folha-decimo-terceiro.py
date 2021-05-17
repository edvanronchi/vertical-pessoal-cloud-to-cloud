from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('calculo-folha-decimo-terceiro', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'calculo-folha-decimo-terceiro')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')

    for j in i['calculoFolhaMatriculas']:
        if j.get('matricula'):
            j['matricula']['id'] = buscarIdDestino('matricula', j['matricula']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('calculo-folha-decimo-terceiro', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")