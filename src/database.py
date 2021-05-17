from decouple import config
from json import dumps
import psycopg2

#Faz a conexão com o banco
def connect():
    conn = psycopg2.connect(
        database=config('DATABASE'),
        user=config('USER'),
        password=config('PASSWORD'),
        host=config('HOST'),
        port=config('PORT')
    )

    return { 'cur': conn.cursor(), 'conn': conn }

#Cria a tabela para controle de migração
def createTable():

    conection = connect()

    conection['cur'].execute("""
        CREATE TABLE IF NOT EXISTS public.controle_migracao (
            id serial NOT NULL,
            id_origem varchar NOT NULL,
            id_destino varchar NOT NULL,
            id_lote varchar NOT NULL,
            service_layer varchar NOT NULL,
            conteudo_json varchar,
            mensagem varchar,
            status varchar,
            data timestamp NOT NULL DEFAULT CURRENT_DATE
        )
    """)

    conection['cur'].close()
    conection['conn'].commit()

#Inseri os registros conforme algum erro ou sucesso de requisição
def insert(idOrigem, idDestino, idLote, serviceLayer, conteudoJson, mensagem, status):
    conection = connect()

    conection['cur'].execute('INSERT INTO public.controle_migracao (id_origem, id_destino, id_lote, service_layer, conteudo_json, mensagem, status) VALUES(%s, %s, %s, %s, %s, %s, %s)', (idOrigem, idDestino, idLote, serviceLayer, str(dumps(conteudoJson)), str(mensagem), status))
    
    conection['cur'].close()
    conection['conn'].commit()

#Faz busca do registro se ele já se encontra migrado.
def buscarRegistro(idOrigem, serviceLayer):
    conection = connect()

    conection['cur'].execute("SELECT * FROM controle_migracao WHERE id_origem = '{}' and service_layer = '{}' and status = 'true'".format(idOrigem, serviceLayer))

    result = len(conection['cur'].fetchall())

    conection['cur'].close()

    return result

#Busca o id referente a base de destino
def buscarIdDestino(service_layer, idOrigem):
    conection = connect()

    result = conection['cur'].execute("SELECT id_destino FROM controle_migracao WHERE service_layer in ('{}') and id_origem = '{}' and status = 'true'".format(service_layer, idOrigem))
    
    result = conection['cur'].fetchall()

    conection['cur'].close()

    if result:
        return result[0][0]

    return result

#Consulta, atualiza, insere o registro
def query(query):
    conection = connect()

    conection['cur'].execute(query)

    result = conection['cur'].fetchall()

    conection['cur'].close()

    return result

#Deleta o registro
def delete(query):
    conection = connect()

    conection['cur'].execute(query)
    conection['cur'].close()
    conection['conn'].commit()