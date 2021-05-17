from src.service import *
from src.database import *
from decouple import config
from json import loads

TOKEN_ORIGEM  = config('TOKEN_ORIGEM')
TOKEN_DESTINO = config('TOKEN_DESTINO')

origem = loads("""
[
    {
        "id": 177893,
        "nome": "Borges",
        "municipio": {
            "id": 213
        },
        "zonaRural": null,
        "version": 0
    },
    {
        "id": 177894,
        "nome": "Interior",
        "municipio": {
            "id": 213
        },
        "zonaRural": null,
        "version": 0
    },
    {
        "id": 177895,
        "nome": "Coopercampos",
        "municipio": {
            "id": 213
        },
        "zonaRural": null,
        "version": 0
    },
    {
        "id": 177896,
        "nome": "SÃO SEBASTIÃO",
        "municipio": {
            "id": 213
        },
        "zonaRural": null,
        "version": 0
    },
    {
        "id": 177897,
        "nome": "SÃO SEBASTIÃO",
        "municipio": {
            "id": 3866
        },
        "zonaRural": null,
        "version": 0
    },
    {
        "id": 177898,
        "nome": "Rural",
        "municipio": {
            "id": 213
        },
        "zonaRural": null,
        "version": 0
    }
]""")

lotes = []
idsOrigem = []

for i in origem:

    if (buscarRegistro(i['id'], 'bairro')) > 0:
        continue 

    idsOrigem.append(i['id'])

    i.pop('id')
    i.pop('version')

    conteudo = { 'conteudo': i }

    lotes.append(conteudo)    

if len(lotes) > 0:
    inserir('bairro', idsOrigem, lotes, 100, TOKEN_DESTINO)
else:
    print("Já foram migrados os dados!\n-")