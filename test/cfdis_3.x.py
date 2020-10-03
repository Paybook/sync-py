# -​*- coding: utf-8 -*​-
from traceback import format_exc, print_exc
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
ID_USER = getenv('id_user_test')
ID_CREDENTIAL = getenv('id_credential_test')
ID_TRANSACTION = getenv('id_transaction_test')

def prettyPrint(parsed):
    print(dumps(parsed, indent=4, sort_keys=True))

def logger(parsed, message):
    print('', message)
    prettyPrint(parsed)

def end():
    raise Exception("Exit pushed")

if __name__ == "__main__":
    try:
        # Obtener token de sesión
        token = Sync.auth(
            API_KEY,
            {"id_user": ID_USER}
        )
        logger(token, "Obtener token de sesión")        
        tokenCode = token['token']

        # Obtener transaccion 3.X
        response = Sync.run(
            token,
            "/transactions",
            {
                'id_credential': ID_CREDENTIAL,
                'id_transaction': ID_TRANSACTION,
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
            print(response)
        print('-----This is the end-------')
        exit()

    except Exception as e:
        print('=============== UNIT TESTING ERROR ===============')
        print(e)
        print_exc()
    else:
        print("FINALIZED WITH ALL TESTS PASSED")