from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('tipo-movimentacao-pessoal', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'tipo-movimentacao-pessoal')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    
    for j in i['camposAdicionais']['campos']:
        j['id'] = buscarIdDestino('campo-adicional-campos', j['id'])                   

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)

if len(lotes) > 0:
    inserir('tipo-movimentacao-pessoal', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")