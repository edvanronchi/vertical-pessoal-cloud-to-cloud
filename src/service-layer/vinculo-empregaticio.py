from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('vinculo-empregaticio', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'vinculo-empregaticio')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    
    for j in i['camposAdicionais']['campos']:
        j['id'] = buscarIdDestino('campo-adicional-campos', j['id'])   

    if i['categoriaTrabalhador']:
        i['categoriaTrabalhador']['id'] = buscarIdDestino('categoria-trabalhador', i['categoriaTrabalhador']['id'])
    
    if i['motivoRescisao']:
        i['motivoRescisao']['id'] = buscarIdDestino('motivo-rescisao', i['motivoRescisao']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)

if len(lotes) > 0:
    inserir('vinculo-empregaticio', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")