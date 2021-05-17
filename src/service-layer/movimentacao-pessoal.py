from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('movimentacao-pessoal', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'movimentacao-pessoal')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i.get('ato'):
        i['ato']['id'] = buscarIdDestino('ato', i['ato']['id'])

    if i.get('tipoMovimentacaoPessoal'):
        i['tipoMovimentacaoPessoal']['id'] = buscarIdDestino('tipo-movimentacao-pessoal', i['tipoMovimentacaoPessoal']['id'])

    if i.get('matricula'):
        i['matricula']['id'] = buscarIdDestino('matricula', i['matricula']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('movimentacao-pessoal', idsOrigem, lotes, 20, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")