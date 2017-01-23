
# -​*- coding: utf-8 -*​-

import paybook
import paybook.sdk as paybook_sdk

try:
	INDENT = '   '
	PAYBOOK_API_KEY = 'YOUR_API_KEY'
	ID_USER = 'SOME_ID_USER'

	step = 0

	print str(step) + '. Inicializar SDK con API KEY correcta:'
	paybook_sdk.Paybook(PAYBOOK_API_KEY)
	print INDENT + 'ok'
	step += 1

	print str(step) + '. Crear un usuario a partir de id_user (consultar usuario existente)'
	session_user = paybook_sdk.User(id_user=ID_USER)
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

	print str(step) + '. Consultar la lista de transacciones del usuario'
	transactions = paybook_sdk.Transaction.get(session=session)
	print INDENT + 'transactions_count: ' + str(len(transactions))
	step += 1

except paybook_sdk.Error as error:
	print INDENT + 'error: ' + str(error.code) + ' ' + error.message
	print'\Test script uncompleted :('
	print'\n'