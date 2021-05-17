from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('configuracao-evento', TOKEN_ORIGEM, 50)

lotes = []
idsOrigem = []
count = 1

print("Montando requisições para rota: configuracao-evento")

for i in origem:

    if (buscarRegistro(i['id'], 'configuracao-evento')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    
    for j in i['camposAdicionais']['campos']:
        j['id'] = buscarIdDestino('campo-adicional-campos', j['id'])   

    if i['ato']:
        i['ato']['id'] = buscarIdDestino('ato', i['ato']['id'])
    
    if i['configuracaoProcessamentos'].get('DECIMO_TERCEIRO_SALARIO'):
        for j in i['configuracaoProcessamentos']['DECIMO_TERCEIRO_SALARIO']['motivosRescisao']:
            j['id'] = buscarIdDestino('motivo-rescisao', j['id'])

    if i['configuracaoProcessamentos'].get('MENSAL'):
        for j in i['configuracaoProcessamentos']['MENSAL']['motivosRescisao']:
            j['id'] = buscarIdDestino('motivo-rescisao', j['id'])

    if i['configuracaoProcessamentos'].get('RESCISAO'):
        for j in i['configuracaoProcessamentos']['RESCISAO']['motivosRescisao']:
            j['id'] = buscarIdDestino('motivo-rescisao', j['id'])

    if i['configuracaoProcessamentos'].get('FERIAS'):
        for j in i['configuracaoProcessamentos']['FERIAS']['motivosRescisao']:
            j['id'] = buscarIdDestino('motivo-rescisao', j['id'])

    for j in i['historicos']:
        if j['ato']:
            j['ato']['id'] = buscarIdDestino('ato', j['ato']['id'])
        
        if j['configuracaoProcessamentos'].get('DECIMO_TERCEIRO_SALARIO'):
            for k in j['configuracaoProcessamentos']['DECIMO_TERCEIRO_SALARIO']['motivosRescisao']:
                k['id'] = buscarIdDestino('motivo-rescisao', k['id'])

        if j['configuracaoProcessamentos'].get('MENSAL'):
            for k in j['configuracaoProcessamentos']['MENSAL']['motivosRescisao']:
                k['id'] = buscarIdDestino('motivo-rescisao', k['id'])

        if j['configuracaoProcessamentos'].get('RESCISAO'):
            for k in j['configuracaoProcessamentos']['RESCISAO']['motivosRescisao']:
                k['id'] = buscarIdDestino('motivo-rescisao', k['id'])

        if j['configuracaoProcessamentos'].get('FERIAS'):
            for k in j['configuracaoProcessamentos']['FERIAS']['motivosRescisao']:
                k['id'] = buscarIdDestino('motivo-rescisao', k['id'])
        
    conteudo = { 'conteudo': i }

    print("Número de requisições montadas: {}".format(count))
    count += 1

    lotes.append(conteudo)

if len(lotes) > 0:
    inserir('configuracao-evento', idsOrigem, lotes, 50, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")