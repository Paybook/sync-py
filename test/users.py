from sync import Sync
from os import getenv
from json import dumps
from time import sleep
from dotenv import load_dotenv
load_dotenv()

def pp(text):
    print(dumps(text, indent=4, sort_keys=True))

API_KEY = {
    'api_key': getenv('API_KEY')
}
response = Sync.run(
    API_KEY, 
    '/users', 
    None, 
    'GET'
)

pp(response)