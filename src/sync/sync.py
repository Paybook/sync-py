# -​*- coding: utf-8 -*​-
import requests
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError

SYNC_API_URL = 'https://sync.paybook.com/v1'

class Sync():
    @staticmethod
    def auth(AUTH: dict, id_user: dict) -> dict:
        try:
            session = Sync.run(AUTH, '/sessions', id_user, 'POST')
            if 'token' in session:
                response = {"token": session['token']}                
                return response
            else:
                raise Error(
                    session['code'],
                    session['response'],
                    session['message'],
                    session['status']
                )            
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

            # response = requests.post(uri, headers=headers, params=payload)
            response = requests.post(uri, headers=headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            sync_response = response_json['response']
            is_array = isinstance(sync_response, list)
            is_bool = isinstance(sync_response, bool)
            response = sync_response if is_array or not is_bool else response_json
            return response
        except KeyError as bad_method:
            print(f"INCORRECT METHOD ASKED: {bad_method}")            
            raise bad_method 
        except HTTPError as http_err:            
            raise Error(
                response.status_code, 
                response.json(),
                response.json()['message'],
                http_err
            )
        except JSONDecodeError as json_error:
            return response.text
class Error(Exception):

    def __init__(self, code, response, message, status):
        self.code = code
        self.response = response
        self.message = message
        self.status = status

    def get_json(self):
        return {
            'code': self.code,
            'response': self.response,
            'message': self.message,
            'status': self.status
} # End of return