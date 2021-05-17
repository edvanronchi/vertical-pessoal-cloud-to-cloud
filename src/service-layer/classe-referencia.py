from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('classe-referencia', TOKEN_ORIGEM, 100)
destino = buscarTodos('classe-referencia', TOKEN_DESTINO, 100)

lotes = []

for i in origem:

    if (buscarRegistro(i['id'], 'classe-referencia')) > 0:
        continue 

    for j in destino:
        if i['classe'] == j['classe'] and i['referencia'] == j['referencia'] and i['fatorValor'] == j['fatorValor'] and i['ordem'] == j['ordem']:
            lotes.append({'idOrigem': i['id'], 'idDestino': j['id']})         

if len(lotes) > 0:
    for i in lotes: 
        insert(i['idOrigem'], i['idDestino'], '', 'classe-referencia', '', '', 'true')

    print("Migração realizada para rota: classe-referencia")
    
else:
    print("Já foram migrados os dados!\n-")