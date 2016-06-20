
##QUICKSTART SAT

### Requerimientos

1. Manejo de shell/bash
2. Algunas credenciales de acceso al SAT (RFC y CIEC)
3. [Python 2.7.6](https://www.python.org/downloads/)
4. Tener instalado [Python Install Package pip](https://pip.pypa.io/en/stable/installing/)
5. Tener instalada la librería requests de python (pip install requests)

### Introducción

A lo largo de este tutorial te enseñaremos como consumir el API Rest de Paybook por medio de la librería de Paybook. Al terminar este tutorial habrás podido crear nuevos usuarios en Paybook, sincronizar algunas instituciones de estos usuarios y visualizar las transacciones sincronizadas.

La documentación completa de la librería la puedes consultar [aquí](https://github.com/Paybook/sync-py/blob/master/readme.md) 

##En la consola:

####1. Instalamos la librería de Paybook y dependencias:

Para consumir el API de Paybook lo primero que tenemos que hacer es instalar la libreria de Paybook haciendo uso del paquete de instalaciones:

```
$ pip install paybook
```

**Importante: ** Es posible que la ejecución del comando anterior requiera permisos de super usuario (sudo) esto depende de como tengas configurado Python en tu equipo.

####2. Ejecutamos el Script:
Este tutorial está basado en el script [quickstart.py](https://github.com/Paybook/sync-py/blob/master/quickstart.py) por lo que puedes descargar el archivo y ejecutarlo de corrido en tu equipo:

```python
python quickstart_sat.py
```

A continuación explicaremos detalladamente la lógica del script que acabas de ejecutar.

####3. Importamos paybook
El primer paso es importar la librería y algunas dependencias:

```python
import time
import sys
import paybook.sdk as paybook
```

####4. Configuramos la librería
Una vez importada la librería tenemos que configurarla, para esto únicamente se necesita tu API KEY de Paybook.

```python
paybook.Paybook(YOUR_API_KEY)
```

####5. Creamos un usuario:
Una vez configurada la librería, el primer paso será crear un usuario, este usuario será, por ejemplo, aquel del cual queremos obtener sus facturas del SAT.

**Importante**: todo usuario estará ligado al API KEY con el que configuraste la librería (paso 4)

```python
user = paybook.User(name='MY_USER')
```

####6. Consultamos los usuarios ligados a nuestra API KEY:
Para verificar que el usuario creado en el paso 5 se haya creado corréctamente podemos consultar la lista de usuarios ligados a nuestra API KEY.

```python
my_users = paybook.User.get()
	for user in my_users:
	    print user.name
```

####7. Creamos una nueva sesión:
Para sincronizar las facturas del SAT, o bien, las cuentas de una institución bancaria de un usuario primero tenemos que crear una sesión, la sesión estará ligada al usuario y tiene un proceso de expiración de 5 minutos después de que ésta ha estado inactiva. Para crear una sesión:

```python
session = paybook.Session(user)
```

####8. Podemos validar la sesión creada:
De manera opcional podemos validar la sesión, es decir, checar que no haya expirado.

```python
session_verified = session.verify()
print 'Session verified: ' + str(session_verified)
```

####9. Consultamos el catálogo de instituciones que podemos sincronizar y extraemos el SAT:
Paybook tiene un catálogo de instituciones que podemos sincronizar por usuario:

![Instituciones](https://github.com/Paybook/sync-py/blob/master/sites.png "Instituciones")

A continuación consultaremos este catálogo y seleccionaremos el sitio del SAT para sincronizar las facturas del usuario que hemos creado en el paso 5:

```python
sat_site = None
sites = paybook.Catalogues.get_sites(session=session)
for site in sites:
	print site.name.encode('utf-8')
	if site.name == 'CIEC':
	    sat_site = site
print 'SAT site: ' + sat_site.id_site + ' ' + sat_site.id_site
```

####10. Configuramos nuestras credenciales del SAT:
Una vez que hemos obtenido el sitio del SAT del catálogo de institiciones, configuraremos las credenciales de nuestro usuario (estas credenciales son las que el usuario utiliza para acceder al portal del SAT).

```python
credentials_data = {
	'rfc' : 'RFC',
	'password' : 'CIEC'
}
sat_credentials = paybook.Credentials(session=session,id_site=sat_site.id_site,credentials=credentials_data)
print sat_credentials.username
```

####11. Checamos el estatus de sincronización de las credenciales creadas y esperamos a que la sincronización finalice:
Cada vez que registamos unas credenciales Paybook inicia un Job (proceso) que se encargará de validar esas credenciales y posteriormente sincronizar las transacciones. Este Job se puede representar como una maquina de estados:

![Job Estatus](https://github.com/Paybook/sync-py/blob/master/normal.png "Job Estatus")

Una vez registradas las credenciales se obtiene el primer estado (Código 100), posteriormente una vez que el Job ha empezado se obtiene el segundo estado (Código 101). Después de aquí, en caso de que las credenciales sean válidas, prosiguen los estados 202, 201 o 200. Estos indican que la sincronización está en proceso (código 201), que no se encontraron transacciones (código 202), o bien, la sincronización ha terminado (código 200). La librería proporciona un método para consultar el estado actual del Job. Este método se puede ejecutar constantemente hasta que se obtenga el estado requerido por el usuario, para este ejemplo especifico consultamos el estatus hasta que se obtenga un código 200, es decir, que la sincronización haya terminado:

```python
sat_sync_completed = False
while not sat_sync_completed: 
	print 'Polling ... '
	time.sleep(5)
	sat_status = sat_credentials.get_status(session=session)
	for status in sat_status:
		code = status['code']
		if code == 200:
			sat_sync_completed = True
```

####12. Consultamos las facturas sincronizadas:
Una vez que ya hemos checado el estado de la sincronización y hemos verificado que ha terminado (código 200) podemos consultar las facturas sincronizadas:
```python
sat_transactions = paybook.Transaction.get(session=session)
print 'Facturas del SAT: ' + str(len(sat_transactions))
```

####13. Consultamos la información de archivos adjuntos:
Podemos también consultar los archivos adjuntos a estas facturas, recordemos que por cada factura el SAT tiene una archivo XML y un archivo PDF por cada factura.
```python
attachments = paybook.Attachment.get(session=session)
print 'Archivos XML/PDF del SAT: ' + str(len(attachments))
```

####14. Obtenemos el XML y PDF de alguna factura:
Podemos descargar estos archivos:
```python
if len(attachments) > 0:
	i = 0
	for attachment in attachments:
		i+=1
		id_attachment = attachment.url[1:]
		print id_attachment
		attachment_content = paybook.Attachment.get(session=session,id_attachment=id_attachment)
		print 'Attachment ' + str(i) + ':'
		print str(attachment_content)
		if i == 2:
			break	
```

¡Felicidades! has terminado con este tutorial. 

### Siguientes Pasos

- Revisar el tutorial de como sincronizar una institución bancaria con credenciales simples (usuario y contraseña) [clic aquí](https://github.com/Paybook/sync-py/blob/master/quickstart_normal_bank.md)

- Revisar el tutorial de como sincronizar una institución bancaria con token [clic aquí](https://github.com/Paybook/sync-py/blob/master/quickstart_token_bank.md)

- Puedes consultar y analizar la documentación completa de la librería [aquí](https://github.com/Paybook/sync-py/blob/master/readme.md)

- Puedes consultar y analizar la documentación del API REST [aquí](https://www.paybook.com/sync/docs#api-Overview)

- Acceder a nuestro proyecto en Github y checar todos los recursos que Paybook tiene para ti [clic aquí](https://github.com/Paybook)


























