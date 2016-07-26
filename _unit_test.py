
# -​*- coding: utf-8 -*​-

import paybook
import paybook.sdk as paybook_sdk
import time

# Utilities:
def order_by_key(some_list,key):
	items_by_key = {}
	for item in some_list:
		json_item = item.get_json()
		key_value = json_item[key]
		if not key_value in some_list:

try:
	INDENT = '   '
	PAYBOOK_API_KEY = 'sadsadasdas'
	paybook_sdk.Paybook(PAYBOOK_API_KEY,print_calls=False)
	users = paybook_sdk.User.get()
	user = users[0]
	session = paybook_sdk.Session(user=user)
	step = 0
	print '\n ******* PAYBOOK PYTHON LIBRARY UNIT TESTING SCRIPT ***** \n'
	step += 1
	print '\n -> ACCOUNTS \n'
	accounts = paybook_sdk.Account.get(session=session)
	total_accounts = len(accounts)
	print 'All accounts: ' + str(total_accounts)
	id_account = accounts[0].id_account
	accounts_by_id_credential = {}
	accounts_by_id_site = {}
	accounts_by_id_site_organization = {}
	accounts_by_id_site_organization_type = {}
	for account in list(accounts):
		id_credential = account.id_credential
		id_site = account.id_site
		id_site_organization = account.id_site_organization
		id_site_organization_type = account.id_site_organization_type
		if not id_credential in accounts_by_id_credential:
			accounts_by_id_credential[id_credential] = 0
		accounts_by_id_credential[id_credential]+=1
		if not id_site in accounts_by_id_site:
			accounts_by_id_site[id_site] = 0
		accounts_by_id_site[id_credential]+=1
		if not id_site_organization in accounts_by_id_site_organization:
			accounts_by_id_site_organization[id_site_organization] = 0
		accounts_by_id_site_organization[id_credential]+=1
		if not id_site_organization_type in accounts_by_id_site_organization_type:
			accounts_by_id_site_organization_type[id_site_organization_type] = 0
		accounts_by_id_site_organization_type[id_credential]+=1
	print '\nTesting id_credential option'
	for id_credential in accounts_by_id_credential:
		options = {
			'id_credential' : id_credential
		}#End of options
		accounts = paybook_sdk.Account.get(session=session,options=options)
		if len(accounts) == accounts_by_id_credential[id_credential]:
			print 'Id credential ' + id_credential + '. API Accounts: ' + str(len(accounts)) + ' Script Accounts: ' + str(accounts_by_id_credential[id_credential]) + ' -> OK'
		else:
			print 'Id credential ' + id_credential + '. API Accounts: ' + str(len(accounts)) + ' Script Accounts: ' + str(accounts_by_id_credential[id_credential]) + ' -> ERROR'
	
	print '\nTesting id_credential option'
	for id_credential in accounts_by_id_credential:
		options = {
			'id_credential' : id_credential
		}#End of options
		accounts = paybook_sdk.Account.get(session=session,options=options)
		if len(accounts) == accounts_by_id_credential[id_credential]:
			print 'Id credential ' + id_credential + '. API Accounts: ' + str(len(accounts)) + ' Script Accounts: ' + str(accounts_by_id_credential[id_credential]) + ' -> OK'
		else:
			print 'Id credential ' + id_credential + '. API Accounts: ' + str(len(accounts)) + ' Script Accounts: ' + str(accounts_by_id_credential[id_credential]) + ' -> ERROR'

	options = {
		'id_account' : id_account
	}#End of options
	accounts = paybook_sdk.Account.get(session=session,options=options)
	if len(accounts) == 1:
		print 'Id account ' + id_account + '. Accounts: ' + str(len(accounts)) + ' -> OK'
	else: 
		print 'Id account ' + id_account + '. Accounts: ' + str(len(accounts)) + ' -> ERROR'
	skip = 2
	options = {
		'skip' : skip
	}#End of options
	accounts = paybook_sdk.Account.get(session=session,options=options)
	if len(accounts) == total_accounts - skip:
		print 'Skiping: ' + str(skip) + '. Accounts: ' + str(len(accounts)) + ' -> OK'
	else:
		print 'Skiping: ' + str(skip) + '. Accounts: ' + str(len(accounts)) + ' -> ERROR'
	limit = 1
	options = {
		'limit' : limit
	}#End of options
	accounts = paybook_sdk.Account.get(session=session,options=options)
	if len(accounts) == limit:
		print 'Limit: ' + str(limit) + '. Accounts: ' + str(len(accounts)) + ' -> OK'
	else:
		print 'Limit: ' + str(limit) + '. Accounts: ' + str(len(accounts)) + ' -> ERROR'
except paybook_sdk.Error as error:
	print INDENT + 'error: ' + str(error.code) + ' ' + error.message
	print'\nChecklist uncompleted :('
	print'\n'


# id_site optional	String	
# Site ID.

# id_site_organization optional	String	
# Site Organization ID.

# id_site_organization_type optional	String	
# Site Organization Type ID.

# fields optional	String	
# Select fields to be returned.
