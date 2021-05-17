from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('tipo-funcao', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'tipo-funcao')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('tipo-funcao', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")