# -​*- coding: utf-8 -*​-
from traceback import format_exc
from sync import Sync
from os import getenv
from json import dumps
from time import sleep
from dotenv import load_dotenv
load_dotenv()

API_KEY = {
    'api_key': getenv('API_KEY')
}
WEBHOOK_ENDPOINT = getenv('webhook_url')
tmp_id_user = None

def prettyPrint(parsed):
    print(dumps(parsed, indent=4, sort_keys=True))

def logger(parsed, message):
    print('', message)
    prettyPrint(parsed)

def end():
    raise Exception("Exit pushed")

if __name__ == "__main__":
    try:
        # Consultar usarios
        response = Sync.run(
            API_KEY, 
            '/users', 
            None, 
            'GET'
        )
        logger(response, 'Consultar usuarios')

        # Crear un Usuario
        response = Sync.run(
            API_KEY, 
            '/users', 
            {
                "id_external": 'ACM010101ABC_3',
                "name": 'Test CFDI 3.X'
            }, 
            'POST'
        )
        logger(response, 'Crear un Usuario')
        id_user = response['id_user']        
        tmp_id_user = id_user

        # Obtener token de sesión
        token = Sync.auth(
            API_KEY,
            {"id_user": id_user}
        )
        logger(token, "Obtener token de sesión")        
        tokenCode = token['token']

        # Create credentials for SAT CIEC
        payload = {
            'id_site': '5da784f1f9de2a06483abec1',
            'credentials': {
                'rfc': 'ACM010101ABC',
                'password': 'test'
            }
        }
        response = Sync.run(
            token,
            "/credentials", 
            payload,
            'POST'
        )
        logger(response, "Crear credenciales")        
        ciec_credential = response
        # Consulta status credenciales
        id_job = ciec_credential['id_job']
        response = Sync.run(
            token,
            f"/jobs/{id_job}/status", 
            None,
            'GET'
        )
        logger(response, "Consulta status credenciales")
        current_status_code = response[len(response)-1]['code']
        while current_status_code != 200:
            if current_status_code != 200 : sleep(20)
            response = Sync.run(
                token,
                f"/jobs/{id_job}/status",
                None,
                'GET'
            )
            logger(response, "Consulta status credenciales")
            current_status_code = response[len(response)-1]['code']

        # Obtener transaccion 3.X
        response = Sync.run(
            token,
            "/transactions",
            {
                'id_credential': ciec_credential['id_credential'],
                'keywords': '3.3'
            },
            'GET'
        )
        logger(response, "Consultar transacciones")

        # Obtener attachments
        transactions = response
        for trans in transactions:
            print('     --->>> ID TRANS', trans['id_transaction'])
            attach_url = trans['attachments'][0]['url']
            response = Sync.run(
                token,
                attach_url,
                None,
                'GET'
            )
            if response : print(' OK')
        raise 'This is the end'

    except Exception as e:
        print('=============== UNIT TESTING ERROR ===============')
        if tmp_id_user:
            response = Sync.run(
                API_KEY,
                f"/users/{tmp_id_user}",
                None,
                'DELETE'
            )
            logger(response, 'USER DELETED ON EXEPTION')
        tb = format_exc()
    else:
        tb = f"FINALIZED WITH ALL TESTS PASSED"
    finally:
        print(tb)
