from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('nivel-salarial', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'nivel-salarial')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    
    for j in i['camposAdicionais']['campos']:
        j['id'] = buscarIdDestino('campo-adicional-campos', j['id'])   

    if i['atoCriacao']:
        i['atoCriacao']['id'] = buscarIdDestino('ato', i['atoCriacao']['id'])
    
    if i['planoCargoSalario']:
        i['planoCargoSalario']['id'] = buscarIdDestino('plano-cargo-salario', i['planoCargoSalario']['id'])

    for j in i['historicos']:
        if j['atoCriacao']:
            j['atoCriacao']['id'] = buscarIdDestino('ato', j['atoCriacao']['id'])
    
        if j['planoCargoSalario']:
            j['planoCargoSalario']['id'] = buscarIdDestino('plano-cargo-salario', j['planoCargoSalario']['id'])

        if j['motivoAlteracao']:
            j['motivoAlteracao']['id'] = buscarIdDestino('motivo-alteracao-salarial', j['motivoAlteracao']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)   

if len(lotes) > 0:
    inserir('nivel-salarial', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")