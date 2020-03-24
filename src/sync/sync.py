# -​*- coding: utf-8 -*​-
import requests

def test():
    response = requests.get('https://httpbin.org/ip')
    print('Your IP is {0}'.format(response.json()['origin']))

