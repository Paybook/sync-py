# -​*- coding: utf-8 -*​-

import main

class Account(main.Paybook):

	def __init__(self,account_json):
		self.id_account = account_json['id_account']
		self.id_user = account_json['id_user']
		self.id_external = account_json['id_external']
		self.id_credential = account_json['id_credential']
		self.id_site = account_json['id_site']
		self.id_site_organization = account_json['id_site_organization']
		self.name = account_json['name']
		self.number = account_json['number']
		self.balance = account_json['balance']
		self.site = account_json['site']
		self.dt_refresh = account_json['dt_refresh']

	@staticmethod
	def get(session=None,id_user=None,options=None):
		Account.log('\n')
		Account.log('Account.get')
		if id_user is not None:
			params = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		account_jsons = Account.__call__(endpoint='accounts',method='get',params=params)
		accounts = []
		for account_json in account_jsons:
			account = Account(account_json)
			accounts.append(account)
		return accounts

	def get_json(self):
		return {
			'id_account' : self.id_account,
			'id_user' : self.id_user,
			'id_external' : self.id_external,
			'id_credential' : self.id_credential,
			'id_site' : self.id_site,
			'id_site_organization' : self.id_site_organization,
			'name' : self.name,
			'number' : self.number,
			'balance' : self.balance,
			'site' : self.site,
			'dt_refresh' : self.dt_refresh
		}#End of return


