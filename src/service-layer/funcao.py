from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('funcao', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'funcao')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i['tipo']:
        i['tipo']['id'] = buscarIdDestino('tipo-funcao', i['tipo']['id'])

    if i['tipoMovimentacaoEntrada']:
        i['tipoMovimentacaoEntrada']['id'] = buscarIdDestino('tipo-movimentacao-pessoal', i['tipoMovimentacaoEntrada']['id'])
    
    if i['tipoMovimentacaoSaida']:
        i['tipoMovimentacaoSaida']['id'] = buscarIdDestino('tipo-movimentacao-pessoal', i['tipoMovimentacaoSaida']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)   

if len(lotes) > 0:
    inserir('funcao', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")