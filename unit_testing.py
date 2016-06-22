
# -​*- coding: utf-8 -*​-

import paybook
import paybook.sdk as paybook_sdk
import time

try:
	INDENT = '   '
	PAYBOOK_API_KEY = 'YOUR_API_KEY'
	USERNAME = 'SOME_PAYBOOK_USERNAME'
	TEST_SITE_NAME = 'CIEC'#For testing with SAT
	CREDENTIALS = {
		'rfc' : 'SOME_RFC',
		'password' : 'SOME_CIEC'
	}#End of CREDENTIALS

	step = 0

	print '\n ******* PAYBOOK PYTHON LIBRARY UNIT TESTING SCRIPT ***** \n'

	step += 1

	print '\n -> INIT \n'

	print str(step) + '. Inicializar SDK con API KEY incorrecta:'
	paybook_sdk.Paybook('hola')
	print INDENT + 'ok'
	step += 1

	print str(step) + '. Hacer una llamada al API '
	try:
		user_list = paybook_sdk.User.get()
	except paybook_sdk.Error as error:
		print INDENT + 'error: ' + str(error.code) + ' ' + error.message
	step += 1

	print str(step) + '. Inicializar SDK con API KEY correcta:'
	paybook_sdk.Paybook(PAYBOOK_API_KEY)
	print INDENT + 'ok'
	step += 1

	print '\n -> USERS ENDPOINTS \n'

	print str(step) + '. Consultar la lista de usuarios: '
	user_list = paybook_sdk.User.get()
	print INDENT + 'users: ' + str(len(user_list))
	step += 1

	print str(step) + '. Crear un usuario nuevo: '
	user = paybook_sdk.User(name=USERNAME)
	print INDENT + 'username: ' + user.name + ' id_user: ' + user.id_user
	step += 1

	print str(step) + '. Consultar lista de usuarios (debe haber uno más que en el paso 1): '
	user_list = paybook_sdk.User.get()
	print INDENT + 'users: ' + str(len(user_list))
	step += 1

	print str(step) + '. Borrar al usuario: '
	deleted = paybook_sdk.User.delete(id_user=user.id_user)
	print INDENT + 'deleted: ' + str(deleted)
	step += 1

	print str(step) + '. Consultar lista de usuarios (debe haber los mismos que en el paso 1): '
	user_list = paybook_sdk.User.get()
	print INDENT + 'users: ' + str(len(user_list))
	step += 1

	print str(step) + '. Crear un usuario nuevo (nuevamente) y guardar su id_user: '
	user_again = paybook_sdk.User(name=USERNAME)
	id_user = user_again.id_user
	print INDENT + 'username: ' + user_again.name + ' id_user: ' + user_again.id_user
	step += 1

	print '\n -> SESSION ENDPOINTS \n'

	print str(step) + '. Crear un usuario a partir de id_user (consultar usuario existente)'
	session_user = paybook_sdk.User(id_user=id_user)
	print INDENT + 'username: ' + session_user.name + ' id_user: ' + session_user.id_user
	step += 1

	print str(step) + '. Crear una sesión para el usuario del paso 8'
	session = paybook_sdk.Session(session_user)
	print INDENT + 'token: ' + str(session.token)
	step += 1

	print str(step) + '. Verificar la sesión (debe ser valida)'
	session_verified = session.verify()
	print INDENT + 'verified: '+ str(session_verified)
	step += 1

	print str(step) + '. Borrar la sesión'
	session_deleted = paybook_sdk.Session.delete(token=session.token)
	print INDENT + 'deleted: ' + str(session_deleted)
	step += 1

	print str(step) + '. Verificar sesión nuevamente (debe ser invalida puesto que ya no existe)'
	try:
		session_verified = session.verify()
	except paybook_sdk.Error as error:
		print INDENT + 'error: ' + str(error.code) + ' ' + error.message
	step += 1

	print str(step) + '. Crear una sesión nuevamente para el usuario del paso 8'
	session = paybook_sdk.Session(session_user)
	print INDENT + 'token: ' + str(session.token)
	step += 1

	print '\n -> CATALOGUES ENDPOINTS \n'

	print str(step) + '. Consultar los catálogos de tipos de cuentas'
	account_types = paybook_sdk.Catalogues.get_account_types(session=session)
	print INDENT + 'account_types: ' + str(len(account_types))
	step += 1

	print str(step) + '. Consultar los catálogos de tipos de archivos adjuntos'
	attachment_types = paybook_sdk.Catalogues.get_attachment_types(session=session)
	print INDENT + 'attachment_types: ' + str(len(attachment_types))
	step += 1

	print str(step) + '. Consultar los catálogos de tipos de paises'
	countries = paybook_sdk.Catalogues.get_countries(session=session)
	print INDENT + 'countries: ' + str(len(countries))
	step += 1

	print str(step) + '. Consultar los catálogos de tipos de sitios'
	sites = paybook_sdk.Catalogues.get_sites(session=session)
	print INDENT + 'sites: ' + str(len(sites))
	step += 1

	print str(step) + '. Consultar los catálogos de tipos de sitios (test) y guarda el de test token'
	test_sites = paybook_sdk.Catalogues.get_sites(session=session,is_test=True)
	test_site = None
	print INDENT + 'test_sites: ' + str(len(test_sites))
	for site in test_sites:
		if site.name == 'Token':
			test_site = site
			break
	print INDENT + 'test id_site: ' + test_site.id_site + ' ' + test_site.name
	step += 1

	print str(step) + '. Consultar los catálogos de tipos de organizaciones'
	site_organizations = paybook_sdk.Catalogues.get_site_organizations(session=session)
	print INDENT + 'site_organizations: ' + str(len(site_organizations))
	step += 1

	print str(step) + '. Obtener el site del SAT'
	SAT_site = None
	for site in sites:
		if site.name == TEST_SITE_NAME:
			SAT_site = site
			break
	print INDENT + 'SAT id_site: ' + SAT_site.id_site + ' ' + SAT_site.name
	step += 1

	print '\n -> CREDENTIALS ENDPOINTS \n'

	print str(step) + '. Consultar la lista de credenciales'
	credentials_list = paybook_sdk.Credentials.get(session=session)
	print INDENT + 'credentials: ' + str(len(credentials_list))
	step += 1

	print str(step) + '. A partir del site del SAT crear unas credenciales con la configuración correcta'
	credentials_params = {}
	for cred_structure in SAT_site.credentials:
		credentials_params[cred_structure.name] = CREDENTIALS[cred_structure.name]
	print INDENT + 'credentials: ' + str(credentials_params)
	step += 1

	print str(step) + '. Crear las credenciales del SAT'
	credentials = paybook_sdk.Credentials(session=session,id_site=SAT_site.id_site,credentials=credentials_params)
	print INDENT + 'id_credential: ' + credentials.id_credential
	print INDENT + 'username: ' + credentials.username
	print INDENT + 'ws: ' + credentials.id_credential
	print INDENT + 'status: ' + credentials.status
	print INDENT + 'twofa: ' + credentials.twofa
	step += 1

	print str(step) + '. Consultar la lista de credenciales (debe haber una más que en el paso 21)'
	credentials_list = paybook_sdk.Credentials.get(session=session)
	print INDENT + 'credentials: ' + str(len(credentials_list))
	step += 1

	print str(step) + '. Borrar las credenciales del SAT creadas'
	credentials_deleted = paybook_sdk.Credentials.delete(session=session,id_credential=credentials.id_credential)
	print INDENT + 'deleted: ' + str(credentials_deleted)
	step += 1

	print str(step) + '. Consultar la lista de credenciales (debe haber las mismas que en paso 21)'
	credentials_list = paybook_sdk.Credentials.get(session=session)
	print INDENT + 'credentials: ' + str(len(credentials_list))
	step += 1

	print str(step) + '. Crear las credenciales del SAT nuevamente'
	credentials = paybook_sdk.Credentials(session=session,id_site=SAT_site.id_site,credentials=credentials_params)
	print INDENT + 'id_credential: ' + credentials.id_credential
	print INDENT + 'username: ' + credentials.username
	print INDENT + 'ws: ' + credentials.ws
	print INDENT + 'status: ' + credentials.status
	print INDENT + 'twofa: ' + credentials.twofa
	step += 1

	print str(step) + '. Crear las credenciales de Token (test)'
	credentials_params = {
		'username' : 'test',
		'password' : 'test'
	}#End of credentials_params
	credentials = paybook_sdk.Credentials(session=session,id_site=test_site.id_site,credentials=credentials_params)
	print INDENT + 'id_credential: ' + credentials.id_credential
	print INDENT + 'username: ' + credentials.username
	print INDENT + 'ws: ' + credentials.ws
	print INDENT + 'status: ' + credentials.status
	print INDENT + 'twofa: ' + credentials.twofa
	step += 1

	print str(step) + '. Checa el estatus y espera el code 410 para introducir token'
	code_410 = False
	while not code_410:
		print INDENT + ' . . . '
		time.sleep(1)
		statuses = credentials.get_status(session=session)
		for status in statuses:
			code = status['code']
			if code == 410:
				code_410 = True
	print INDENT + '410: ' + str(code_410)

	print str(step) + '. Manda el token'
	twofa = credentials.set_twofa(session=session,twofa_value='test')
	print INDENT + 'Token sent: ' + str(twofa)

	print '\n -> ACCOUNTS ENDPOINTS \n'

	print str(step) + '. Consultar la lista de cuentas del usuario'
	accounts = paybook_sdk.Account.get(session=session)
	print INDENT + 'accounts: ' + str(len(accounts))
	step += 1

	print '\n -> TRANSACTION ENDPOINTS \n'

	print str(step) + '. Consultar el número de transacciones del usuario'
	transactions_count = paybook_sdk.Transaction.get_count(session=session)
	print INDENT + 'transactions_count: ' + str(transactions_count)
	step += 1

	print str(step) + '. Consultar la lista de transacciones del usuario'
	transactions = paybook_sdk.Transaction.get(session=session)
	print INDENT + 'transactions_count: ' + str(len(transactions))
	step += 1

	print '\n -> ATTACHMENT ENDPOINTS \n'

	print str(step) + '. Consultar el número de attachments del usuario'
	attachments_count = paybook_sdk.Attachment.get_count(session=session)
	print INDENT + 'attachments: ' + str(attachments_count)
	step += 1

	print str(step) + '. Consultar la lista de attachments del usuario'
	attachments = paybook_sdk.Attachment.get(session=session)
	print INDENT + 'attachments: ' + str(len(attachments))
	step += 1

	if attachments_count > 0:
		id_attachment = attachments[0]['url']
		print id_attachment
		
		# print str(step) + '. Consultar el contenido de un attachment especifico'
		# attachment = paybook_sdk.Attachment.get(session=session,id_attachment=id_attachment)
		# print INDENT + str(attachment)
		# step += 1

		# print str(step) + '. Consultar el extra de un attachment especifico'
		# attachment = paybook_sdk.Attachment.get(session=session,id_attachment=id_attachment,extra=True)
		# print INDENT + str(attachment)
		# step += 1

	print'\nChecklist completed \\0/'
	print'\n'
except paybook_sdk.Error as error:
	print INDENT + 'error: ' + str(error.code) + ' ' + error.message
	print'\nChecklist uncompleted :('
	print'\n'