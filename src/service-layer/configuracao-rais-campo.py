from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('configuracao-rais-campo', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'configuracao-rais-campo')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')

    for j in i['eventos']:
        j.pop('id')
        j['configuracaoEvento']['id'] = buscarIdDestino('configuracao-evento', j['configuracaoEvento']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('configuracao-rais-campo', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")