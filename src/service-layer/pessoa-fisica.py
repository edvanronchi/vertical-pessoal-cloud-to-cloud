from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('pessoa-fisica', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'pessoa-fisica')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    
    for j in i['camposAdicionais']['campos']:
        j['id'] = buscarIdDestino('campo-adicional-campos', j['id'])   

    for j in i['contasBancarias']:
        j['agencia']['id'] = buscarIdDestino('agencia-bancaria', j['agencia']['id'])

    for j in i['enderecos']:
        j['logradouro']['id'] = buscarIdDestino('logradouro', j['logradouro']['id'])
        
        bairro = buscarIdDestino('bairro', j['bairro']['id'])

        if bairro:
            j['bairro']['id'] = bairro
           
    conteudo = { 'conteudo': i }

    lotes.append(conteudo) 

if len(lotes) > 0:
    inserir('pessoa-fisica', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")