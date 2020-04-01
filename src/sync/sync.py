# -​*- coding: utf-8 -*​-
import requests

SYNC_API_URL = 'https://sync.paybook.com/v1'

def testIP():
    response = requests.get('https://httpbin.org/ip')
    print('Your IP is {0}'.format(response.json()['origin']))

class Sync():
    @staticmethod
    def auth(AUTH: dict, id_user: dict) -> dict:
        try:
            session = Sync.run(AUTH, '/sessions', id_user, 'POST')
            if 'token' in session:
                response = {"token": session['token']}                
                return response
            else:
                raise session
                # raise new Error(
                #     session.code,
                #     session.response,
                #     session.message,
                #     session.satus
                # )            
        except Exception as e:
            raise e
         
    
    @staticmethod
    def strictAuth():
        print("Stric auth mode ON!")
        pass

    @staticmethod
    def run(AUTH: dict, route: str, payload: dict, method: str) -> dict:
        try:
            # BUILD URI
            uri = SYNC_API_URL+route
            # SET HEADERS
            headers = {
                'Content-type': "application/json"
            }
            # CHECK AUTH TYPE 
            if AUTH:       
                if 'api_key' in AUTH:
                    headers['Authorization'] = "API_KEY api_key="+AUTH['api_key']
                elif 'token' in AUTH:
                    headers['Authorization'] = "TOKEN token="+AUTH['token']        
            #  ASSIGN HTTP METHOD
            headers['X-Http-Method-Override'] = {
                'GET': 'GET',
                'POST': 'POST',
                'PUT': 'PUT',
                'DELETE': 'DELETE'
            }[method]

            response = requests.post(uri, headers=headers, params=payload)
            return response.json()['response']
        except KeyError as bad_method:
            print(f"INCORRECT METHOD ASKED: {bad_method}")            
            raise bad_method 

