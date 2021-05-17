from src.database import *
from src.service import *
from decouple import config
from os import path

TOKEN_ORIGEM = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

#Apaga todos os registros da rota especificada
def apagarGeral(service_layer, token):
    lotes = []

    headers = {'Authorization': "Bearer {}".format(token)}

    resultado = buscarTodos(service_layer, token, 20)

    print("Quantidade Total: {}".format(len(resultado)))
    print('-')

    for i in resultado:    
        print("Id: {}".format(i['id'])) 

        conteudo = {
            'idGerado': i['id'],
            'conteudo': {
                'id': i['id']
            }
        }

        lotes.append(conteudo)

    response = requests.delete("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}".format(service_layer), json=lotes, headers=headers)

    print(response.json())
    
#Apaga todos os registros da rota especificada com base na tabela controle de migração
def apagarRegistros(service_layer, token):
    registrosDestino = totalRegistros(service_layer, token)

    print("Iniciando remoção de dados para rota: {}".format(service_layer))
    print('-')
    print("Número total de registros: {}".format(registrosDestino))

    headers = {'Authorization': "Bearer {}".format(token)}

    resultado = query("SELECT * FROM public.controle_migracao WHERE service_layer = '{}' and status = 'true'".format(service_layer))

    if len(resultado) == 0:
        print("Sem dados para deletar!")
        return 

    lotes = []

    for i in resultado:
        idGerado = i[2]
        
        conteudo = {
            'idGerado': str(idGerado),
            'conteudo': {
                'id': str(idGerado)
            }
        }

        lotes.append(conteudo)

    response = requests.delete("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}".format(service_layer), json=lotes, headers=headers)

    if not response.ok:
        print("Falha na requisição para rota: {}".format(service_layer))
        return {'status': False}  

    idLote = response.json()['id'] 

    print("Identificador do lote: {}".format(idLote))

    aguardando = True
    while aguardando:
        sleep(1)

        print('Aguardando execução do lote...')

        lote = requests.get("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}/lotes/{}".format(service_layer, idLote), headers=headers)
        lote = lote.json()
        
        if lote['situacao'] != 'EXECUTADO':
            continue

        aguardando = False

        for j in lote['retorno']:
            if j['mensagem']:
                print(j['mensagem'])
                continue

            print("{} excluido com sucesso!".format(j['idGerado']))

            delete("DELETE FROM public.controle_migracao WHERE service_layer = '{}' and id_destino = '{}' and status = 'true'".format(service_layer, j['idGerado']))

#Compara todas as rotas do service layer
def compararBases(tokenOrigem, tokenDestino):
    arquivo = open(path.dirname(path.realpath(__file__)) + "\src\\files\service-layer.txt", "r")
    
    headersOrigem = {'Authorization': "Bearer {}".format(tokenOrigem)}
    headersDestino = {'Authorization': "Bearer {}".format(tokenDestino)}

    params = {'limit': 1, 'offset': 0}

    for serviceLayer in arquivo:
        serviceLayer = serviceLayer.rstrip()
        
        responseOrigem = requests.get("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}".format(serviceLayer), params=params, headers=headersOrigem)
        responseDestino = requests.get("https://pessoal.cloud.betha.com.br/service-layer/v1/api/{}".format(serviceLayer), params=params, headers=headersDestino)
        
        if not responseOrigem.ok:
            print("Falha na requisição Origem: {}".format(serviceLayer))
            continue

        if not responseDestino.ok:
            print("Falha na requisição Destino: {}".format(serviceLayer))
            continue

        totalOrigem = responseOrigem.json()['total']
        totalDestino = responseDestino.json()['total']

        if totalOrigem != totalDestino:
            print("Rota: {}".format(serviceLayer))
            print("Origem: {}".format(totalOrigem))
            print("Destino: {}".format(totalDestino))
            print('-')

compararBases(TOKEN_ORIGEM, TOKEN_DESTINO)
#apagarRegistros('folha', TOKEN_DESTINO)
#apagarGeral('folha', TOKEN_DESTINO)