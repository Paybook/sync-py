###Instalamos el sdk de Paybook
pip install paybook  
o  
sudo pip install paybook  

###En la consola de Python
python

###Configuramos las llaves e instanciamos el sdk
```python
api_key = 'YOUR_API_KEY'  
from paybook.sdk import Paybook  
pb = Paybook(api_key,db_environment=True,logger=None)
```

###Creamos un usuario
```python
r = pb.signup("sdk_test", "sdk_test")  
print r  
```

###Hacemos login
```python
r = pb.login("sdk_test", "sdk_test")  
print r  
```

###Guardamos el token para las solicitudes posteriores
```python
token = r['token']
```

###Buscamos el id del SAT
```python
r = pb.catalogues(token=token)  
print r  
for site in r:  
    if site['name'] == 'SAT':  
        id_site = site['id_site']
        print id_site
```

###Cargamos las credenciales del SAT
```python
credentials = {'rfc':'YOUR_RFC', 'password':'YOUR_CIEC'}
credentials_response = pb.credentials(token=token, id_site=id_site, credentials=credentials)
print credentials_response
```

###Revisamos el status del agregador
```python  
r = pb.status(token=token, id_site=id_site, url_status=credentials_response['status'])  
```

###Obtenemos las transacciones
```python
for c in r:
    if c['code'] == 202 or c['code'] == 200:
        transactions_response= pb.transactions(token=token, id_account=None)
        for tr in transactions_response:
            print tr
```
