# -​*- coding: utf-8 -*​-
import os
import json
import traceback
from sync import Sync
from dotenv import load_dotenv
load_dotenv()

API_KEY = {
    'api_key': os.getenv('API_KEY')
}
WEBHOOK_ENDPOINT = ''
tmp_id_user = None

def prettyPrint(parsed):
    print(json.dumps(parsed, indent=4, sort_keys=True))

def logger(parsed, message):
    print('->', message)
    prettyPrint(parsed)

if __name__ == "__main__":
    try:
        # Consultar usarios
        response = Sync.run(
            API_KEY, 
            '/users', 
            None, 
            'GET'
        )
        logger(response.json(), 'Consultar usuarios')

        # Consultar un usuario en especifico
        response = Sync.run(
            API_KEY, 
            '/users', 
            {"id_user": '5df859c4a7a6442757726ef4'}, 
            'GET'
        )
        logger(response.json(), 'Consultar un usuario en especifico')         
        # Crear un Usuario
        response = Sync.run(
            API_KEY, 
            '/users', 
            {
                "id_external": 'MIST030794',
                "name": 'Rey Misterio'
            }, 
            'POST'
        )
        logger(response.json(), 'Crear un Usuario')
        id_user = response.json()['id_user']
        tmp_id_user = id_user
        raise Exception('Exit')    
    except Exception as e:
        print('=============== UNIT TESTING ERROR ===============')
        if tmp_id_user:
            response = Sync.run(
                API_KEY,
                f"/users/{tmp_id_user}",
                None,
                'DELETE'
            )
            logger(response.json(), 'USER DELETED ON EXEPTION')
        tb = traceback.format_exc()
    else:
        tb = f"FINALIZED WITH ALL TESTS PASSED"
    finally:
        print(tb)