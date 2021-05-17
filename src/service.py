from src.database import *            
from json import dumps
from time import sleep
from math import ceil
import requests

#Faz a busca com paginação no service layer 
def buscarTodos(serviceLayer, token, limit=20):

    headers = {'Authorization': "Bearer {}".format(token)}

    hasNext = True
    page = 0
    query = []

    while hasNext:
        offset = page * limit

        params = {'limit': limit, 'offset': offset}
    
        response = requests.get("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}".format(serviceLayer), params=params, headers=headers)
        
        if not response.ok:
            print('Falha na requisição!')
            print(response.text)
            return []
    
        response = response.json()

        for r in response['content']: 
            query.append(r)

        hasNext = response['hasNext']
        
        page += 1
    return query

#Faz a busca de um registro especifico no service layer
def buscar(serviceLayer, id, token):
    headers = {'Authorization': "Bearer {}".format(token)}

    response = requests.get("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}/{}".format(serviceLayer, id), headers=headers)

    if not response.ok:
        print('Falha na requisição!')
        return {'status': False}   
    
    return response.json()

#Faz a inserção dos registros por lote
def inserir(serviceLayer, idsOrigem, lotes, registrosPorLote, token):
    print("Iniciando inserção de dados para rota: {}".format(serviceLayer))

    headers = {'Authorization': "Bearer {}".format(token)}

    numeroRegistrosLotes = len(lotes)
    numerosLotes = ceil(numeroRegistrosLotes / registrosPorLote)

    valorInicial = 0
    valorFinal = registrosPorLote

    for i in range(1, (numerosLotes+1)):
        lote = []

        print("-\nLote número: {}\n-".format(i))
  
        if valorFinal > numeroRegistrosLotes:
            valorFinal = numeroRegistrosLotes 

        for j in range(valorInicial, valorFinal):
            lote.append(lotes[j])

        response = requests.post("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}".format(serviceLayer), json=lote, headers=headers)

        if not response.ok:
            insert(idsOrigem, '', '', serviceLayer, lote, response.text, 'false')
            print("Falha na requisição para rota: {}".format(serviceLayer))
            return 

        idLote = response.json()['id'] 
        
        print("Identificador do lote: {}".format(idLote))
        print('-')

        aguardando = True
        while aguardando:
            sleep(3)

            print('Aguardando execução do lote...')

            lote = requests.get("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}/lotes/{}".format(serviceLayer, idLote), headers=headers)
            lote = lote.json()

            if lote['situacao'] != 'EXECUTADO':
                continue

            aguardando = False
            
            for j in range(0, len(lote['retorno'])):

                idGerado = lote['retorno'][j]['idGerado'] 
                mensagem = lote['retorno'][j]['mensagem']

                if not idGerado:
                    print("Id não foi gerado para rota: {}".format(serviceLayer))
                    insert(idsOrigem[(valorInicial+j)], '', idLote, serviceLayer, lotes[(valorInicial+j)], mensagem, 'false')
                    continue

                insert(idsOrigem[(valorInicial+j)], idGerado, idLote, serviceLayer, lotes[(valorInicial+j)], mensagem, 'true')
                print("Inserção realizada para rota: {}".format(serviceLayer))

        valorInicial = valorFinal
        valorFinal += registrosPorLote
    
    print("-\nMigração realizada para rota: {}\n-".format(serviceLayer))

#Consulta o total de registros para rota informada
def totalRegistros(serviceLayer, token):
    headers = {'Authorization': "Bearer {}".format(token)}
    params = {'limit': 1, 'offset': 0}

    response = requests.get("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}".format(serviceLayer), params=params, headers=headers)

    if not response.ok:
        print('Falha na requisição!')

        return {'error': 'Request failude'}   
        
    response = response.json()

    return response['total']

#Busca os id's de destino referentes aos id's de origem
def campoAdicional(camposAdicionais, tokenOrigem, tokenDestino):

    if not camposAdicionais:
        return []

    if len(camposAdicionais) == 0:
        return []
    
    tipoCA = camposAdicionais['tipo'] 

    origem = buscarTodos('campo-adicional', tokenOrigem, 100)

    idCAOrigem = [i['id'] for i in origem if i['tipo'] == tipoCA]

    idCADestino = buscarIdDestino('campo-adicional', idCAOrigem[0])

    campos = buscar('campo-adicional', idCADestino, tokenDestino)

    idsCampos = []
    for i in campos['agrupador']['campos']:
        idsCampos.append(i['id'])

    return idsCampos