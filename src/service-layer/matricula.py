from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('matricula', TOKEN_ORIGEM, 10)

lotes = []
idsOrigem = []
count = 1

for i in origem:

    if (buscarRegistro(i['id'], 'matricula')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    
    if i.get('camposAdicionais'):
        for j in i['camposAdicionais']['campos']:
            j['id'] = buscarIdDestino('campo-adicional-campos', j['id']) 
    else:
        i.pop('camposAdicionais')

    if i.get('atoContrato'):
        i['atoContrato']['id'] = buscarIdDestino('ato', i['atoContrato']['id'])
    
    if i.get('atoAlteracaoSalario'):
        i['atoAlteracaoSalario']['id'] = buscarIdDestino('ato', i['atoAlteracaoSalario']['id'])
    
    if i.get('motivoAlteracaoSalario'):
        i['motivoAlteracaoSalario']['id'] = buscarIdDestino('motivo-alteracao-salarial', i['motivoAlteracaoSalario']['id'])
    
    if i.get('pessoa'):
        i['pessoa']['id'] = buscarIdDestino('pessoa-fisica', i['pessoa']['id'])
    
    if i.get('grupoFuncional'):
        i['grupoFuncional']['id'] = buscarIdDestino('grupo-funcional', i['grupoFuncional']['id'])

    if i.get('organograma'):
        i['organograma']['id'] = buscarIdDestino('organograma', i['organograma']['id'])
    
    if i.get('vinculoEmpregaticio'):
        i['vinculoEmpregaticio']['id'] = buscarIdDestino('vinculo-empregaticio', i['vinculoEmpregaticio']['id'])

    if i.get('cargo'):
        i['cargo']['id'] = buscarIdDestino('cargo', i['cargo']['id'])

    if i.get('nivelSalarial'):
        i['nivelSalarial']['id'] = buscarIdDestino('nivel-salarial', i['nivelSalarial']['id'])
    
    if i.get('leiContrato'):
        i['leiContrato']['id'] = buscarIdDestino('ato', i['leiContrato']['id'])
    
    if i.get('categoriaTrabalhador'):
        i['categoriaTrabalhador']['id'] = buscarIdDestino('categoria-trabalhador', i['categoriaTrabalhador']['id'])
    
    for j in i['lotacoesFisicas']:
        j['lotacaoFisica']['id'] = buscarIdDestino('lotacao-fisica', j['lotacaoFisica']['id'])
    
    for j in i['historicos']:
        j.pop('id')

        if j.get('camposAdicionais'):
            for k in j['camposAdicionais']['campos']:
                k['id'] = buscarIdDestino('campo-adicional-campos', k['id']) 

        if j.get('atoContrato'):
            j['atoContrato']['id'] = buscarIdDestino('ato', j['atoContrato']['id'])
    
        if j.get('atoAlteracaoSalario'):
            j['atoAlteracaoSalario']['id'] = buscarIdDestino('ato', j['atoAlteracaoSalario']['id'])
        
        if j.get('motivoAlteracaoSalario'):
            j['motivoAlteracaoSalario']['id'] = buscarIdDestino('motivo-alteracao-salarial', j['motivoAlteracaoSalario']['id'])
        
        if j.get('pessoa'):
            j['pessoa']['id'] = buscarIdDestino('pessoa-fisica', j['pessoa']['id'])
        
        if j.get('grupoFuncional'):
            j['grupoFuncional']['id'] = buscarIdDestino('grupo-funcional', j['grupoFuncional']['id'])

        if j.get('organograma'):
            j['organograma']['id'] = buscarIdDestino('organograma', j['organograma']['id'])
        
        if j.get('vinculoEmpregaticio'):
            j['vinculoEmpregaticio']['id'] = buscarIdDestino('vinculo-empregaticio', j['vinculoEmpregaticio']['id'])

        if j.get('cargo'):
            j['cargo']['id'] = buscarIdDestino('cargo', j['cargo']['id'])

        if j.get('nivelSalarial'):
            j['nivelSalarial']['id'] = buscarIdDestino('nivel-salarial', j['nivelSalarial']['id'])
        
        if j.get('leiContrato'):
            j['leiContrato']['id'] = buscarIdDestino('ato', j['leiContrato']['id'])
        
        if j.get('categoriaTrabalhador'):
            j['categoriaTrabalhador']['id'] = buscarIdDestino('categoria-trabalhador', j['categoriaTrabalhador']['id'])
        
        for k in j['lotacoesFisicas']:
            k['lotacaoFisica']['id'] = buscarIdDestino('lotacao-fisica', k['lotacaoFisica']['id'])

    conteudo = { 'conteudo': i }

    print("Número de requisições montadas: {}".format(count))
    count += 1

    lotes.append(conteudo) 

if len(lotes) > 0:
    inserir('matricula', idsOrigem, lotes, 1, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")