from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('folha', TOKEN_ORIGEM, 200)

lotes = []
idsOrigem = []
count = 1

print("Montando requisições para rota: folha")

for i in origem:
   
    if (buscarRegistro(i['id'], 'folha')) > 0:
        continue 

    idsOrigem.append(i['id'])

    if i.get('calculo'):
        i['calculo']['id'] = buscarIdDestino("calculo-folha-ferias', 'calculo-folha-rescisao', 'calculo-folha-decimo-terceiro', 'calculo-folha-mensal", i['calculo']['id'])
    
    if i.get('matricula'):
        i['matricula']['id'] = buscarIdDestino('matricula', i['matricula']['id'])

    i.pop('id')

    for j in i['eventos']:
        j.pop('id')

        j['configuracao']['id'] = buscarIdDestino('configuracao-evento', j['configuracao']['id'])

    for j in i['composicaoBases']:
        j.pop('id')

        j['configuracaoEvento']['id'] = buscarIdDestino('configuracao-evento', j['configuracaoEvento']['id'])
        j['base']['id'] = buscarIdDestino('base', j['base']['id'])

    conteudo = { 'conteudo': i }

    print("Número de requisições montadas: {}".format(count))
    count += 1

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('folha', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")    