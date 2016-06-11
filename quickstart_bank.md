
##QUICKSTART PARA INSTITUCIONES BANCARIAS

A lo largo de este tutorial te enseñaremos como sincronizar una institución bancara de un usuario. Te recomendamos que antes de tomar este tutorial consultes el [Quickstart General](https://github.com/Paybook/sync-py/blob/master/quickstart.md). En el tutorial asumiremos que ya hemos creado usuarios y por tanto tenemos usuarios ligados a nuestra API KEY, que hemos instalado el SDK de python y hecho las configuraciones pertinentes. 

##En la consola:

####1. Obetenemos un usuario e iniciamos sesión:
El primer paso para realizar la mayoría de las acciones en Paybook es tener un usuario e iniciar una sesión, por lo tanto haremos una consulta por nuestra lista de usuarios y seleccionaremos el usuario con el que deseamos trabajar. Una vez que tenemos al usuario iniciamos sesión con éste.


```python
user_list = paybook_sdk.User.get()
user = user_list[0]
print user.name + ' ' + user.id_user
session = paybook_sdk.Session(user=user)
print session.token
```

####2. Consultamos el catálogo de las instituciones de Paybook:
Recordemos que Paybook tiene un catálogo de instituciones que podemos sincronizar por usuario. A continuación consultaremos este catálogo:

```python
sat_site = None
sites = paybook_sdk.Catalogues.get_sites(session=session)
for site in sites:
	print site.name
	if site.name == 'CIEC':
		sat_site = site
```

El catálogo muestra las siguienes instituciones:

1. AfirmeNet
2. Personal
3. BancaNet Personal
4. eBanRegio
5. Banorte Personal
6. CIEC
7. Banorte en su empresa
8. BancaNet Empresarial
9. Banca Personal
10. Corporativo
11. Banco Azteca
12. American Express México
13. SuperNET Particulares
14. ScotiaWeb
15. Empresas
16. InbuRed

Para efectos de este tutorial seleccionaremos **Banorte en su empresa** pero tu puedes seleccionar la institución de la cual tienes credenciales.

####3. Registramos las credenciales:

A continuación registraremos las credenciales de nuestro banco, es decir, el usuario y contraseña que nos proporcionó para acceder a sus servicios en línea:

```python
CREDENTIALS = {
	'username' : 'my_bank_username',
	'password' : 'my_bank_password'
}#End of CREDENTIALS
bank_credentials = paybook_sdk.Credentials(session=session,id_site=bank_site.id_site,credentials=CREDENTIALS)
print bank_credentials.id_credential + ' ' + bank_credentials.username
```
####4. Checamos el estatus

Una vez que has registrado las credenciales de una institución bancaria para un usuario en Paybook el siguiente paso consiste en checar el estatus de las credenciales, el estatus será una lista con los diferentes estatus por los que las credenciales han pasado, el último será el estatus actual. A continuación se describen los diferentes estatus de las credenciales:

| Código         | Descripción                                |                                
| -------------- | ---------------------------------------- | ------------------------------------ |
| 100 | Credenciales registradas para su futura validación   | 
| 401      | Credenciales inválidas    |
| 410      | Esperando token   |
| 102      | Credenciales validas, la institución se está sincronizando    |
| 200      | La institución ha sido sincronizada    | 

**Importante** El código 410 se puede presentar múltiples veces en caso de que la autenticación con la institución bancaria requiera múltiples pasos e.g. usuario, contraseña (primera autenticación) y además token (segunda autenticación). Entonces el código 410 únicamente le puede preceder a un código 100 (después de introducir usuario y password), o bien, a un código 410 (después de haber introducido un token).

Checamos el estatus de las credenciales:

```python
sync_status = bank_credentials.get_status(session=session)
```
####5. Analizamos en estatus y se manda el token del banco:

El estatus se muestra a continuación:

```
[{u'code': 100}, {u'code': 101}]
```

Esto quiere decir que las credenciales registradas han sido correctas. La institución bancaria a sincronizar i.e. Banorte, requiere de token por lo que debemos esperar un estatus 410, para esto podemos polear mediante un bucle sobre los estatus de las credenciales hasta que se tenga un estatus 410, es decir, que el token sea solicitado por el SDK:

```python
print 'Esperando por estatus 410 ... '
status_410 = None
while status_410 is None:
	print ' . . . '
	time.sleep(3)
	sync_status = bank_credentials.get_status(session=session)
	print sync_status
	for status in sync_status:
		code = status['code']
		if code == 410:
			status_410 = status
```

Ahora hay que ingresar el valor del token, el cual lo podemos solicitar en python a través de la interfaz raw_input:

```python
twofa_value = raw_input('Ingresa el código de seguridad: ')
twofa = bank_credentials.set_twofa(session=session,twofa_value=twofa_value)
```

Una vez que el token bancario es enviado, volvemos a polear por medio de un bucle buscando que el estatus sea 102, es decir, que el token haya sido validado y ahora Paybook se encuentre sincronzando a nuestra institución bancaria, o bien, buscando el estatus 401, es decir, que el token no haya sido validado y por tanto lo tengamos que volver a enviar:

```python
while status_102_or_401 is None:
	print ' . . . '
	time.sleep(3)
	sync_status = bank_credentials.get_status(session=session)
	print sync_status
	for status in sync_status:
		code = status['code']
		if code == 102 or code == 401:
			status_102_or_401 = status
```

Checamos el código del estatus y de ser 401 se programa una rutina para pedir el token nuevamente:

```python
if status['code'] == 401:
	None
	# Rutina para pedir el token nuevamente	
```

En caso de que el estatus sea 102, evitara la validación previa y podremos continuar con los siguientes pasos.

####6. Esperamos a que la sincronización termine

Una vez que la sincronización se encuentra en proceso (código 102), podemos construir un bucle para polear y esperar por el estatus de fin de sincronización (código 200).

```python
status_200 = None
while status_200 is None:
	print ' . . . '
	time.sleep(3)
	sync_status = bank_credentials.get_status(session=session)
	print sync_status
	for status in sync_status:
		code = status['code']
		if code == 200:
			status_200 = status
```

####7. Consultamos las transacciones de la institución bancaria:

Una vez que la sincronización ha terminado podemos consultar las transacciones:

```python
transactions = paybook_sdk.Transaction.get(session=session)
```

Podemos desplegar información de las transacciones:

```python
i = 0
for transaction in transactions:
	i+=1
	print str(i) + '. ' + transaction.description + ' $' + str(transaction.amount) 
``

¡Felicidades! has terminado con este tutorial.


###Siguientes Pasos


- Puedes consultar y analizar la documentación del API REST [aquí](https://www.paybook.com/sync/docs#api-Overview)

- Acceder a nuestro proyecto en Github y checar todos los recursos que Paybook tiene para ti [clic aquí](https://github.com/Paybook)














