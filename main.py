from src.database import *
from src.service import * 
from src.routes import orderedRoutes
from decouple import config

#Tokens das entidades
TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

#Cria a tabela de controle de migração
createTable()

for route in orderedRoutes:

    if not route['useable']:
        continue
    
    registrosOrigem  = totalRegistros(route['route'], TOKEN_ORIGEM)
    registrosDestino = totalRegistros(route['route'], TOKEN_DESTINO)

    print("-\nInicinado migração para a rota: {}\n-".format(route['route']))
    print("Consultando número de registros pré-migração: ")
    print("Cloud Origem:  {}".format(registrosOrigem))
    print("Cloud Destino: {}\n-".format(registrosDestino))

    #Importando rota
    __import__("src.service-layer.{}".format(route['route']))

    registrosOrigem  = totalRegistros(route['route'], TOKEN_ORIGEM)
    registrosDestino = totalRegistros(route['route'], TOKEN_DESTINO)

    print("Consultando número de registros pós-migração: ")
    print("Cloud Origem:  {}".format(registrosOrigem))
    print("Cloud Destino: {}".format(registrosDestino))

    if registrosOrigem != registrosDestino:
        resposta = input("Foi constatado que os totais estão divergentes para rota {}, deseja continuar? s/n\n".format(route['route']))
        
        if resposta == 'n':
            break