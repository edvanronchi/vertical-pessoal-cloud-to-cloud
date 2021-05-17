from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('periodo-aquisitivo-ferias', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'periodo-aquisitivo-ferias')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i.get('matricula'):
        i['matricula']['id'] = buscarIdDestino('matricula', i['matricula']['id'])
    
    if i.get('configuracaoFerias'):
        i['configuracaoFerias']['id'] = buscarIdDestino('configuracao-ferias', i['configuracaoFerias']['id'])

    for j in i['movimentacoes']:
        j['ferias'] = None
            
    conteudo = { 'conteudo': i }

    lotes.append(conteudo)

if len(lotes) > 0:
    inserir('periodo-aquisitivo-ferias', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")