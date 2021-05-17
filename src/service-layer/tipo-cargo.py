from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('tipo-cargo', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'tipo-cargo')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
  
    for j in i['camposAdicionais']['campos']:
        j['id'] = buscarIdDestino('campo-adicional-campos', j['id'])   

    if i['tipoMovimentacao']:
        i['tipoMovimentacao']['id'] = buscarIdDestino('tipo-movimentacao-pessoal', i['tipoMovimentacao']['id'])
    
    if i['tipoMovimentacaoSubstituto']:
        i['tipoMovimentacaoSubstituto']['id'] = buscarIdDestino('tipo-movimentacao-pessoal', i['tipoMovimentacaoSubstituto']['id'])

    if i['tipoMovimentacaoSaida']:
        i['tipoMovimentacaoSaida']['id'] = buscarIdDestino('tipo-movimentacao-pessoal', i['tipoMovimentacaoSaida']['id'])
    
    if i['tipoMovimentacaoSaidaSubstituto']:
        i['tipoMovimentacaoSaidaSubstituto']['id'] = buscarIdDestino('tipo-movimentacao-pessoal', i['tipoMovimentacaoSaidaSubstituto']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)  

if len(lotes) > 0:
    inserir('tipo-cargo', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")