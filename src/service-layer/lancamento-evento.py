from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('lancamento-evento', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:
    vigenciaInicialEvento = []

    if (buscarRegistro(i['id'], 'lancamento-evento')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    if i.get('configuracao'):
        idDestino = buscarIdDestino('configuracao-evento', i['configuracao']['id'])

        i['configuracao']['id'] = idDestino

        eventoDestino = buscar('configuracao-evento', idDestino, TOKEN_DESTINO)

        vigenciaInicialEvento.append(eventoDestino['inicioVigencia'])

        for j in eventoDestino['historicos']:
            vigenciaInicialEvento.append(j['inicioVigencia'])

        vigenciaInicialDestino = min(vigenciaInicialEvento) + "-01"
        dataInicialOrigem = i.get('dataInicial')[:7]

        if dataInicialOrigem < vigenciaInicialDestino and vigenciaInicialDestino <= i.get('dataFinal')[:7]:
            i['dataInicial'] = vigenciaInicialDestino

    if i.get('matricula'):
        i['matricula']['id'] = buscarIdDestino('matricula', i['matricula']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('lancamento-evento', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")