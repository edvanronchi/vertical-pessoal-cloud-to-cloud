from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('calculo-folha-mensal', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []
count = 1

print("Montando requisições para rota: calculo-folha-mensal")

for i in origem:
 
    if (buscarRegistro(i['id'], 'calculo-folha-mensal')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')

    for j in i['calculoFolhaMatriculas']:
        j.pop('id')
        j['matricula']['id'] = buscarIdDestino('matricula', j['matricula']['id'])

    conteudo = { 'conteudo': i }

    print("Número de requisições montadas: {}".format(count))
    count += 1

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('calculo-folha-mensal', idsOrigem, lotes, 200, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")