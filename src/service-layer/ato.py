from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('ato', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'ato')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')  
    
    for j in i['camposAdicionais']['campos']:
        j['id'] = buscarIdDestino('campo-adicional-campos', j['id'])   

    if i['tipo']:
        i['tipo']['id'] = buscarIdDestino('tipo-ato', i['tipo']['id'])

    if i['naturezaTextoJuridico']:
        i['naturezaTextoJuridico']['id'] = buscarIdDestino('natureza-texto-juridico', i['naturezaTextoJuridico']['id'])
    
    for j in i['fontesDivulgacao']:
        if j['fonteDivulgacao']:
            j['fonteDivulgacao']['id'] = buscarIdDestino('fonte-divulgacao', j['fonteDivulgacao']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)   

if len(lotes) > 0:
    inserir('ato', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")