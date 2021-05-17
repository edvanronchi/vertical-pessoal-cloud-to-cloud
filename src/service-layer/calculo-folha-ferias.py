from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('calculo-folha-ferias', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'calculo-folha-ferias')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    for j in i['calculoFolhaMatriculas']:
        j.pop('id')
        j.pop('version')

        if j.get('matricula'):
            j['matricula']['id'] = buscarIdDestino('matricula', j['matricula']['id'])
        
        for k in j['periodos']:
            k['id'] = buscarIdDestino('periodo-aquisitivo-ferias', k['id'])
            k.pop('configuracaoFerias')
            k.pop('matricula')
            k.pop('situacao')
            k.pop('dataInicial')
            k.pop('dataFinal')
            k.pop('competenciaFechamentoProvisao')
            k.pop('faltas')
            k.pop('diasAdquiridos')
            k.pop('cancelados')
            k.pop('suspensos')
            k.pop('saldo')
            k.pop('pagou1TercoIntegral')
            k.pop('diasAnuladosRescisao')
            k.pop('movimentacoes')
            k.pop('version')
            
    if i.get('ato'):
        i['ato']['id'] = buscarIdDestino('ato', i['ato']['id'])

    if i.get('tipoAfastamento'):
        i['tipoAfastamento']['id'] = buscarIdDestino('tipo-afastamento', i['tipoAfastamento']['id'])
    
    if i.get('matricula'):
        i['matricula']['id'] = buscarIdDestino('matricula', i['matricula']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('calculo-folha-ferias', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")