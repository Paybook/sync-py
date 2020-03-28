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
WEBHOOK_ENDPOINT = ''
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

        # Consultar un usuario en especifico
        response = Sync.run(
            API_KEY, 
            '/users', 
            {'id_external': 'KEMONITO09'}, 
            'GET'
        )
        logger(response, 'Consultar un usuario en especifico')         
        
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
        logger(response, 'Crear un Usuario')
        id_user = response['id_user']        
        tmp_id_user = id_user

        # Actualizar un usuario
        response = Sync.run(
            API_KEY,
            f"/users/{id_user}", 
            {"name":  'Rey Misterio Jr.'},
            'PUT'
        )
        logger(response, "Actualizar un usuario")
        
        # Obtener token de sesión
        token = Sync.auth(
            API_KEY,
            {"id_user": id_user}
        )
        logger(token, "Obtener token de sesión")        
        tokenCode = token['token']
        
        # Verificar token de sesión
        response = Sync.run(
            None,
            f"/sessions/{tokenCode}/verify", 
            None,
            'GET'
        )
        logger(response, "Verificar token de sesión")        

        # Consultar catálogos
        response = Sync.run(
            token,
            "/catalogues/sites", 
            {"limit": 3},
            'GET'
        )
        logger(response, "Consultar catálogos")        

        # Crear credenciales normal
        payload = {'id_site': "5da784f1f9de2a06483abec1"}
        response = Sync.run(
            token,
            "/catalogues/sites", 
            payload,
            'GET'
        )
        site = response[0]        
        credentials = dict()
        credentials[site['credentials'][0]['name']] = 'ACM010101ABC'
        credentials[site['credentials'][1]['name']] = 'test'
        payload['credentials'] = credentials
        response = Sync.run(
            token,
            "/credentials", 
            payload,
            'POST'
        )
        logger(response, "Crear credenciales normal")        
        satCredential = response
        sleep(30)

        # Consultar credenciales
        response = Sync.run(
            token,
            "/credentials", 
            None,
            'GET'
        )
        logger(response, "Consultar credenciales")        
        
        # Consulta status credenciales
        id_job = satCredential.id_job
        response = Sync.run(
            token,
            "/jobs/id_job/status", 
            None,
            'GET'
        )
        logger(response, "Consulta status credenciales")        
        end()

        # Consultar Cuentas
        response = Sync.run(
            token,
            "/accounts", 
            {"id_credential": satCredential.id_credential},
            'GET'
        )
        logger(response, "Consultar cuentas")        

        # Consultar Transacciones
        response = Sync.run(
            token,
            "/transactions", 
            {
                "id_credential": satCredential.id_credential,
                "limit": 1
            },
            'GET'
        )
        logger(response, "Consultar transacciones")        

        # Consultar el número de transacciones
        response = Sync.run(
            token,
            "/transactions/count", 
            {"id_credential": satCredential.id_credential},
            'GET'
        )
        logger(response, "Consultar el número de transacciones")        

        # Crear Webhook
        response = Sync.run(
            API_KEY,
            "/webhooks", 
            {
                "url": WEBHOOK_ENDPOINT, 
                "events": {"credential_create","credential_update","refresh"},
            },
            'POST'
        )
        logger(response, "Crear Webhook")        
        id_webhook = response['id_webhook']
        
        # Consultar Webhook
        response = Sync.run(
            API_KEY,
            "/webhooks", 
            None,
            'GET'
        )
        logger(response, "Consultar Webhook")        
        sleep(150)

        # Eliminar Webhook
        response = Sync.run(
            API_KEY,
            "/webhooks/id_webhook", 
            None,
            'DELETE'
        )
        logger(response, "Eliminar Webhook")        
        
        # Consultar Archivos adjuntos
        response = Sync.run(
            token,
            "/attachments", 
            {
                "id_credential": satCredential.id_credential,
                "limit": 1
            },
            'GET'
        )
        logger(response, "Consultar Archivos adjuntos")        

        # Obtener archivo adjunto
        attachment = response[0]
        attachmentUrl = attachment.url
        response = Sync.run(
            token,
            attachmentUrl, 
            None,
            'GET'
        )
        logger(response, "Obtener archivo adjunto")

        # Obtener info extra
        response = Sync.run(
            token,
            attachment.url+"/extra", 
            None,
            'GET'
        )
        logger(response, "Obtener info extra")        

        # --------------------- TWOFA --------------------------- #
        # Crear credenciales twofa
        payload = {"id_site": "56cf5728784806f72b8b4569"}
        response = Sync.run(
            token,
            "/catalogues/sites", 
            payload,
            'GET'
        )
        
        site = response[0]
        credentials = {}
        credentials[site['credentials'][0]['name']] = 'test'
        credentials[site['credentials'][1]['name']] = 'test'
        payload['credentials'] = credentials
        response = Sync.run(
            token,
            "/credentials", 
            payload,
            'POST'
        )
        logger(response, "Crear credenciales twofa")        
        twofaCredential = response
        sleep(20)

        id_job = twofaCredential.id_job
        response = Sync.run(
            token,
            "/jobs/id_job/status", 
            None,
            'GET'
        )
        logger(response, "Consulta status credenciales twofa")        
        is_twofa = False
        if(response[len(response).code] == 410):
            is_twofa = True
            logger(response, "Is two-fa!")
        
        # Manda TWOFA
        twofaToken = {"twofa" :  {} }
        twofaToken["twofa"][response[2].twofa[0].name] = "123456"
        twofa = Sync.run(
            token,
            "/jobs/id_job/twofa", 
            twofaToken, 
            'POST'
        )
        logger(response, "Manda TWOFA")        

        response = Sync.run(
            token,
            "/jobs/id_job/status", 
            None,
            'GET'
        )
        logger(response, "Consulta nuevamente status credenciales twofa")        

        # ------------------------- Eliminate --------------------- #

        # Eliminar credencial
        id_credential = satCredential.id_credential
        response = Sync.run(
            token,
            "/credentials/id_credential", 
            None,
            'DELETE'
        )
        logger(response, "Eliminar credencial")        

        # Eliminar un usuario
        response = Sync.run(
            API_KEY,
            "/users/id_user", 
            {},
            'DELETE'
        )
        logger(response, "Eliminar un usuario")
          
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