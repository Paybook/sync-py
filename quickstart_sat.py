# -​*- coding: utf-8 -*​-
YOUR_API_KEY = 'YOUR_API_KEY'
RFC = 'YOUR_RFC'
CIEC = 'YOUR_CIEC'
import time
import sys
import paybook.sdk as paybook
try:
	paybook.Paybook(YOUR_API_KEY)
	user = paybook.User(name='MY_USER')
	my_users = paybook.User.get()
	for user in my_users:
	    print user.name
	session = paybook.Session(user)
	print 'Session token: ' + session.token
	session_verified = session.verify()
	print 'Session verified: ' + str(session_verified)
	sat_site = None
	sites = paybook.Catalogues.get_sites(session=session)
	for site in sites:
	    print site.name.encode('utf-8')
	    if site.name == 'CIEC':
	        sat_site = site
	print 'SAT site: ' + sat_site.id_site + ' ' + sat_site.id_site
	credentials_data = {
	    'rfc' : RFC,
	    'password' : CIEC
	}
	sat_credentials = paybook.Credentials(session=session,id_site=sat_site.id_site,credentials=credentials_data)
	print sat_credentials.username
	sat_sync_completed = False
	while not sat_sync_completed: 
		print 'Polling ... '
		time.sleep(5)
		sat_status = sat_credentials.get_status(session=session)
		for status in sat_status:
			code = status['code']
			if code >= 200 and code <= 205:
				sat_sync_completed = True
			if code >= 400 and code <= 405:
				print 'There was an error with your credentials with code: ' + str(code) + '.'
				print 'Please check your credentials and run this script again. \n\n'
				sys.exit()
	sat_transactions = paybook.Transaction.get(session=session)
	print 'Facturas del SAT: ' + str(len(sat_transactions))
	attachments = paybook.Attachment.get(session=session)
	print 'Archivos XML/PDF del SAT: ' + str(len(attachments))
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
	print 'Quickstart script executed successfully\n\n'
except paybook.Error as error:
	print 'Paybook error:  ' +  str(error.code)
