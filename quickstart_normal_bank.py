# -​*- coding: utf-8 -*​-
YOUR_API_KEY = 'YOUR_API_KEY'
BANK_USERNAME = 'YOUR_BANK_USERNAME'
BANK_PASSWORD = 'YOUR_BANK_PASSWORD'
import time
import sys
import paybook.sdk as paybook_sdk
try:
	paybook_sdk.Paybook(YOUR_API_KEY)
	user_list = paybook_sdk.User.get()
	user = user_list[0]
	print user.name + ' ' + user.id_user
	session = paybook_sdk.Session(user=user)
	print session.token
	bank_site = None
	sites = paybook_sdk.Catalogues.get_sites(session=session)
	for site in sites:
	    print site.name
	    if site.name == 'Banorte en su empresa':
	    	bank_site = site
	print 'Bank site: ' + bank_site.name + ' ' + bank_site.id_site
	CREDENTIALS = {
	    'username' : BANK_USERNAME,
	    'password' : BANK_PASSWORD
	}#End of CREDENTIALS
	bank_credentials = paybook_sdk.Credentials(session=session,id_site=bank_site.id_site,credentials=CREDENTIALS)
	print 'Esperando validacion de credenciales ... '
	status_102_or_401 = None
	while status_102_or_401 is None:
	    print ' . . . '
	    time.sleep(3)
	    sync_status = bank_credentials.get_status(session=session)
	    print sync_status
	    for status in sync_status:
	        code = status['code']
	        if code == 102 or code == 401:
	            status_102_or_401 = status
		if status['code'] == 401:
		    print 'Error en credenciales'
		    sys.exit()
	print 'Esperando sincronizacion ... '
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
	transactions = paybook_sdk.Transaction.get(session=session)
	i = 0
	for transaction in transactions:
	    i+=1
	    print str(i) + '. ' + transaction.description + ' $' + str(transaction.amount)
	print 'Quickstart bank script executed successfully\n\n'
except paybook_sdk.Error as error:
	print 'Paybook error:  ' +  str(error.code)