from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('cargo', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'cargo')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    
    for j in i['camposAdicionais']['campos']:
        j['id'] = buscarIdDestino('campo-adicional-campos', j['id']) 
          

    if i['ato']:
        i['ato']['id'] = buscarIdDestino('ato', i['ato']['id'])

    if i['tipo']:
        i['tipo']['id'] = buscarIdDestino('tipo-cargo', i['tipo']['id'])

    if i['configuracaoLicencaPremio']:
        i['configuracaoLicencaPremio']['id'] = buscarIdDestino('configuracao-licenca-premio', i['configuracaoLicencaPremio']['id'])

    if i['configuracaoFerias']:
        i['configuracaoFerias']['id'] = buscarIdDestino('configuracao-ferias', i['configuracaoFerias']['id'])  

    for j in i['remuneracoes']:
        j['nivelSalarial']['id'] = buscarIdDestino('nivel-salarial', j['nivelSalarial']['id'])

        if j['classeReferenciaInicial']:
            j['classeReferenciaInicial']['id'] = buscarIdDestino('classe-referencia', j['classeReferenciaInicial']['id'])

        if j['classeReferenciaFinal']:
            j['classeReferenciaFinal']['id'] = buscarIdDestino('classe-referencia', j['classeReferenciaFinal']['id'])
    
    for j in i['historicos']:
        if j['ato']:
            j['ato']['id'] = buscarIdDestino('ato', j['ato']['id'])

        if j['tipo']:
            j['tipo']['id'] = buscarIdDestino('tipo-cargo', j['tipo']['id'])

        if j['configuracaoLicencaPremio']:
            j['configuracaoLicencaPremio']['id'] = buscarIdDestino('configuracao-licenca-premio', j['configuracaoLicencaPremio']['id'])

        if j['configuracaoFerias']:
            j['configuracaoFerias']['id'] = buscarIdDestino('configuracao-ferias', j['configuracaoFerias']['id'])  

        for k in j['remuneracoes']:
            k['nivelSalarial']['id'] = buscarIdDestino('nivel-salarial', k['nivelSalarial']['id'])

            if k['classeReferenciaInicial']:
                k['classeReferenciaInicial']['id'] = buscarIdDestino('classe-referencia', k['classeReferenciaInicial']['id'])

            if k['classeReferenciaFinal']:
                k['classeReferenciaFinal']['id'] = buscarIdDestino('classe-referencia', k['classeReferenciaFinal']['id'])

           
    conteudo = { 'conteudo': i }

    lotes.append(conteudo) 

if len(lotes) > 0:
    inserir('cargo', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")