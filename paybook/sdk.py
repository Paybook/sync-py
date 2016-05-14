# -​*- coding: utf-8 -*​-

import requests
from json import dumps
from flask import json
from flask import make_response
from paybook1 import db as _DB
import logging

PAYBOOK_URL = 'https://sync.paybook.com/v1/'

class Paybook():

	def __init__(self,api_key,db_environment=False,web_environment=False,logger=None):
		self.api_key = api_key
		self.db_environment = db_environment
		self.web_environment = web_environment
		self.logger = logger

	def call(self,endpoint=None,method=None,data=None,params=None,headers=None,url=None):
		if url is None:
			url = PAYBOOK_URL + endpoint
		if method == 'post':
			conn = requests.post(url,data=data,params=params,headers=headers)
		elif method == 'get':
			conn = requests.get(url,data=data,params=params,headers=headers)
		if conn.status_code == 200:
			return conn.json()['response']
		else:
			raise self.get_api_error(conn)

	def get_api_error(self,conn):
		try:
			self.logger.debug('Paybook API error catched')
			error_response = conn.json()# Execution problem happens when there is a connection error
			self.logger.debug(error_response)
			message = error_response['message']
			code = error_response['code']
			api_error = Error(message,code)
		except Exception as e:
			api_error = Error('Connection Error',500)
		return api_error

	def _signup(self,username):
		data = {
			"api_key":self.api_key, 
			"name":username
		}#End of data
		return self.call(endpoint='users',method='post',data=data)

	def signup(self,username,password):
		if self.db_environment:
			self.logger.debug('DB environment available')
			signup_response = {
				'sdk_message' : 'User already exists'
			}#End of signup_response
			user = _DB.User(username,password)
			user_exist = user.do_i_exist()
			self.logger.debug('User exist: ' + str(user_exist))
			if not user_exist:
				self.logger.debug('Singning up user ... ')
				signup_response = self._signup(username)
				self.logger.debug(signup_response)
				self.logger.debug('Updating id_user in db ... ')
				user.set_id_user(signup_response['id_user'])
				user.save()
				signup_response['sdk_message'] = 'User signed up'
		else:
			signup_response = self._signup(username)
		return signup_response

	def _login(self,id_user):
		data = {
			"api_key":self.api_key, 
			"id_user":id_user
		}#End of data
		login_response = self.call(endpoint='sessions',method='post',data=data)
		return login_response

	def login(self,username,password):
		if self.db_environment:
			self.logger.debug('DB environment available')
			user = _DB.User(username,password)
			if user.login():
				self.logger.debug('User logged in at db ... ')
				id_user = user.get_id_user()
				self.logger.debug('Login to paybook ... ')
				login_response = self._login(id_user)
				self.logger.debug('Updating token in db ... ')
				user.set_token(login_response['token'])
			else:
				self.logger.debug('User was not logged in ... ')
				raise Error('Invalid username or password',400)
		else:
			login_response = paybook._login(id_user)
		return login_response

	def _catalogues(self,token):
		params = {
			"token":token
		}#End of params
		self.logger.info('Getting catalogues ... ')
		catalogs = self.call(endpoint='catalogues/sites',method='get',params=params)
		return catalogs

	def catalogues(self,token):
		if self.db_environment:
			self.logger.debug('DB environment available')
			user = _DB.User(token)
			if user.am_i_logged_in():
				catalogs = self._catalogues(token)
			else:
				raise Error('Invalid token',400)
		else:
			catalogs = self._catalogues(token)
		return catalogs

	def _credentials(self,token,id_site,id_user,credentials):
		data = {
			'api_key' : self.api_key,
			'token' : token,
			'id_site' : id_site,
			'id_user' : id_user,
			'credentials' : credentials
		}#End of data
		credentials_response = self.call(endpoint='credentials',method='post',data=dumps(data))
		return credentials_response

	def credentials(self,token,id_site,credentials):
		if self.db_environment:
			self.logger.debug('DB environment available')
			user = _DB.User(token)
			if user.am_i_logged_in():
				self.logger.debug('Valid token ... ')
				id_user = user.get_id_user()
				db_credentials = _DB.Credentials(id_user,id_site)
				if not db_credentials.do_i_exist():
					self.logger.debug('Creating credentials ... ')
					credentials_response = self._credentials(token,id_site,id_user,credentials)
					ws = credentials_response['ws']
					status = credentials_response['status']
					twofa = credentials_response['twofa']
					id_credential = credentials_response['id_credential']
					self.logger.debug('Updating credentials in db ... ')
					db_credentials = _DB.Credentials(id_user,id_site,ws,status,twofa,id_credential)
					db_credentials.save()
					credentials_response['sdk_message'] = 'Credentials created'
				else:
					self.logger.debug('Credentials already exist ... ')
					status = db_credentials.get_status()
					twofa = db_credentials.get_twofa()
					ws = db_credentials.get_ws()
					credentials_response = {
						'status' : status,
						'twofa' : twofa,
						'ws' : ws,
						'sdk_message' : 'Credentials already exist'
					}#End of credentials_response
					return credentials_response
			else:
				self.logger.debug('Invalid token ... ')
				raise Error('Invalid token',400)
		else:
			credentials_response = self._credentials(token,id_site,id_user,credentials_user,credentials_password)
		return credentials_response

	def _status(self,token,id_site,status):
		headers = {'Content-type' : 'application/json'}		
		data = {
			'token' : token,
			'id_site' : id_site
		}# End of data		
		site_status = self.call(method='get',data=dumps(data),headers=headers,url=status)
		return site_status

	def status(self,token,id_site,url_status=None):
		if self.db_environment:
			self.logger.debug('DB environment available')
			user = _DB.User(token)
			if user.am_i_logged_in():
				self.logger.debug('User logged in ... ')
				id_user = user.get_id_user()
				credentials = _DB.Credentials(id_user,id_site)
				if credentials.do_i_exist():
					url_status = credentials.get_status()
					self.logger.debug('Getting status ... ')
					site_status = self._status(token,id_site,url_status)
				else:
					self.logger.debug('Credential does not exist')
					raise Error('Credential does not exist',400)
			else:
				self.logger.debug('Invalid token ... ')
				raise Error('Invalid token',400)
		elif url_status is not None:
			self.logger.debug('Getting status ... ')
			site_status = self._status(token,id_site,url_status)
		else:
			self.logger.debug('url_status is required in non-db_environment mode')
			raise Error('url_status is required in non-db_environment mode',400)
		return site_status

	def twofa(self,token,id_site,twofa,url_twofa=None):
		if self.db_environment:
			self.logger.debug('DB environment available')
			user = _DB.User(token)
			if user.am_i_logged_in():
				self.logger.debug('User logged in ... ')
				id_user = user.get_id_user()
				credentials = _DB.Credentials(id_user,id_site)
				if credentials.do_i_exist():
					url_twofa = credentials.get_twofa()
					self.logger.debug('Posting twofa ... ')
					self.logger.debug(url_twofa)
					twofa_response = self._status(token,id_site,url_twofa)
				else:
					self.logger.debug('Credential does not exist')
					raise Error('Credential does not exist',400)
			else:
				self.logger.debug('Invalid token ... ')
				raise Error('Invalid token',400)
		elif url_twofa is not None:
			self.logger.debug('Posting twofa ... ')
			twofa_response = self._status(token,id_site,url_twofa)
		else:
			self.logger.debug('url_status is required in non-db_environment mode')
			raise Error('url_status is required in non-db_environment mode',400)
		return twofa_response

	def _accounts(self,token,id_site):
		params = {
			'token' : token,
			'id_site' : id_site
		}# End of params
		site_accounts = self.call(endpoint='accounts',method='get',params=params)
		return site_accounts

	def accounts(self,token,id_site):
		if self.db_environment:
			self.logger.debug('DB environment available')
			user = _DB.User(token)
			if user.am_i_logged_in():
				self.logger.debug('User logged in ... ')
				id_user = user.get_id_user()
				credentials = _DB.Credentials(id_user,id_site)
				if credentials.do_i_exist():
					self.logger.debug('Getting accounts ... ')
					site_accounts = self._accounts(token,id_site)
				else:
					self.logger.debug('Credential does not exist')
					raise Error('Credential does not exist',400)
			else:
				self.logger.debug('Invalid token ... ')
				raise Error('Invalid token',400)
		else:
			self.logger.debug('Getting accounts ... ')
			site_accounts = self._accounts(token,id_site)
		return site_accounts	

	def _transactions(self,token,id_account):
		params = {
			'token' : token,
			'id_account' : id_account
		}#End of params
		account_transactions = self.call(endpoint='transactions',method='get',params=params)
		return account_transactions

	def transactions(self,token,id_account):
		if self.db_environment:
			self.logger.debug('DB environment available')
			user = _DB.User(token)
			if user.am_i_logged_in():
				self.logger.debug('Getting transactions ... ')
				account_transactions = self._transactions(token,id_account)
			else:
				self.logger.debug('Invalid token ... ')
				raise Error('Invalid token',400)
		else:
			self.logger.debug('Getting transactions ... ')
			account_transactions = self._transactions(token,id_account)
		return account_transactions

	def validate_session(self,token):
		is_valid = self.call(endpoint='session/' + token + '/verify',method='get')

class Error(Exception):

	http_code = ''
	content = ''

	def __init__(self,content,code):
		self.http_code = code
		self.content = content

	def get_json(self):
		error_json = self.content
		return json.dumps(error_json)

	def get_response(self):
		return make_response(self.get_json(),self.http_code)




