from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('campo-adicional', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = [] 

for i in origem:
    campoAdicional = buscar('campo-adicional', i['id'], TOKEN_ORIGEM)

    if (buscarRegistro(i['id'], 'campo-adicional')) > 0:
        continue 

    idsOrigem.append(campoAdicional['id'])

    campoAdicional.pop('id')
    campoAdicional['agrupador'].pop('id')
    
    for j in campoAdicional['agrupador']['campos']:
        j['placeholder'] = None
    
    conteudo = { 'conteudo': campoAdicional }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('campo-adicional', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")

campoAdicional = query("SELECT id_origem, id_destino FROM public.controle_migracao WHERE status = 'true' and service_layer = 'campo-adicional'")

lotesCampos = []

for i in campoAdicional:
    campoIdOrigem = i[0]
    campoIdDestino = i[1]

    camposOrigem = buscar('campo-adicional', campoIdOrigem, TOKEN_ORIGEM)
    camposDestino = buscar('campo-adicional', campoIdDestino, TOKEN_DESTINO)
    
    for j in camposOrigem['agrupador']['campos']:
        if (buscarRegistro(j['id'], 'campo-adicional-campos')) > 0:
            continue 

        for k in camposDestino['agrupador']['campos']:
            if j['titulo'] == k['titulo'] and j['textoAjuda'] == k['textoAjuda'] and j['formato'] == k['formato'] and j['variavel'] == k['variavel']:
                lotesCampos.append({'idOrigem': j['id'], 'idDestino': k['id']})
    
for i in lotesCampos:
    insert(i['idOrigem'], i['idDestino'], '', 'campo-adicional-campos', '', '', 'true')