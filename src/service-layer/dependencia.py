from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('dependencia', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'dependencia')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    i.pop('camposAdicionais')
    i.pop('contaBancaria')

    if i.get('pessoa'):
        i['pessoa']['id'] = buscarIdDestino('pessoa-fisica', i['pessoa']['id'])
    
    if i.get('pessoaDependente'):
        i['pessoaDependente']['id'] = buscarIdDestino('pessoa-fisica', i['pessoaDependente']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('dependencia', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")