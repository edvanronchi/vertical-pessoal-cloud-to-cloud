from src.service import *
from src.database import *
from decouple import config

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = buscarTodos('afastamento', TOKEN_ORIGEM, 100)

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'afastamento')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')
    i.pop('descontar')
    i.pop('competenciaDesconto')
    i.pop('abonar')
    i.pop('quantidadeAbono')
    i.pop('competenciaAbono')
    i.pop('afastamentoOrigem')
    i.pop('pessoaJuridica')
    i.pop('atestados')
    i.pop('cedencia')
    i.pop('camposAdicionais')

    if i.get('ato'):
        i['ato']['id'] = buscarIdDestino('ato', i['ato']['id'])
    
    if i.get('matricula'):
        i['matricula']['id'] = buscarIdDestino('matricula', i['matricula']['id'])
    
    if i.get('tipoAfastamento'):
        i['tipoAfastamento']['id'] = buscarIdDestino('tipo-afastamento', i['tipoAfastamento']['id'])

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('afastamento', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")