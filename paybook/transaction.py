# -​*- coding: utf-8 -*​-

import main

class Transaction(main.Paybook):

	def __init__(self,transaction_json):
		self.id_transaction = transaction_json['id_transaction']
		self.id_user = transaction_json['id_user']
		self.id_external = transaction_json['id_external']
		self.id_site = transaction_json['id_site']
		self.id_site_organization = transaction_json['id_site_organization']
		self.id_site_organization_type = transaction_json['id_site_organization_type']
		self.id_account = transaction_json['id_account']
		self.id_account_type = transaction_json['id_account_type']
		self.is_disable = transaction_json['is_disable']
		self.description = transaction_json['description']
		self.amount = transaction_json['amount']
		self.dt_transaction = transaction_json['dt_transaction']
		self.dt_refresh = transaction_json['dt_refresh']

	@staticmethod
	def get(session=None,id_user=None,options=None):
		Transaction.log('\n')
		Transaction.log('Transaction.get')
		if id_user is not None:
			params = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		transaction_jsons = Transaction.__call__(endpoint='transactions',method='get',params=params)
		transactions = []
		for transaction_json in transaction_jsons:
			transaction = Transaction(transaction_json)
			transactions.append(transaction)
		return transactions

	@staticmethod
	def get_count(session=None,id_user=None,options=None):
		Transaction.log('\n')
		Transaction.log('Transaction.get_count')
		if id_user is not None:
			params = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		count_json = Transaction.__call__(endpoint='transactions/count',method='get',params=params)
		transactions_count = count_json['count']
		return transactions_count
	
	def get_json(self):
		return {
			'id_transaction' : self.id_transaction,
			'id_user' : self.id_user,
			'id_external' : self.id_external,
			'id_site' : self.id_site,
			'id_site_organization' : self.id_site_organization,
			'id_site_organization_type' : self.id_site_organization_type,
			'id_account' : self.id_account,
			'id_account_type' : self.id_account_type,
			'is_disable' : self.is_disable,
			'description' : self.description,
			'amount' : self.amount,
			'dt_transaction' : self.dt_transaction,
			'dt_refresh' : self.dt_refresh,
		}#End of return



		
