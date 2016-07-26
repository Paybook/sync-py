# -​*- coding: utf-8 -*​-

import requests

PAYBOOK_URL = 'https://sync.paybook.com/v1/'

class Paybook():

	api_key = None
	logger = None
	print_calls = False
	__INDENT__ = '   '

	def __init__(self,api_key=None,logger=None,print_calls=False):
		Paybook.api_key = api_key
		Paybook.logger = logger
		Paybook.print_calls = print_calls#For debugging

	@staticmethod
	def __call__(endpoint=None,method=None,data=None,params=None,headers=None,url=None):
		Paybook.log('API Call: ',call=True)
		if url is None:
			url = PAYBOOK_URL + endpoint
		Paybook.log(Paybook.__INDENT__ + 'API Key:     ' + str(Paybook.api_key),call=True)
		Paybook.log(Paybook.__INDENT__ + 'Endpoint:    ' + str(url),call=True)
		Paybook.log(Paybook.__INDENT__ + 'HTTP Method: ' + str(method),call=True)
		Paybook.log(Paybook.__INDENT__ + 'Data:        ' + str(data),call=True)
		Paybook.log(Paybook.__INDENT__ + 'Params:      ' + str(params),call=True)
		Paybook.log(Paybook.__INDENT__ + 'Headers:     ' + str(headers),call=True)
		if method == 'post':
			conn = requests.post(url,data=data,params=params,headers=headers)
		elif method == 'get':
			conn = requests.get(url,data=data,params=params,headers=headers)
		elif method == 'delete':
			conn = requests.delete(url,data=data,params=params,headers=headers)
		Paybook.log(Paybook.__INDENT__ + 'API Response code: ' + str(conn.status_code),call=True)
		if conn.status_code == 200:
			Paybook.log('Success response: ')
			try:# JSON responses:
				Paybook.log(Paybook.__INDENT__ + str(conn.json()))
				return conn.json()['response']
			except Exception as e:# Attachments:
				Paybook.log(Paybook.__INDENT__ + str(conn.content))
				return conn.content
		else:
			Paybook.log('Error catched')
			raise Paybook.__get_api_error__(conn)

	@staticmethod
	def __get_api_error__(conn):
		try:
			api_error = Error(conn.status_code,'','','')
		except Exception as e:
			api_error = Error(500,'Connection Error')
		return api_error

	@staticmethod
	def log(message,call=False):
		if Paybook.print_calls == True and call == True:
			print message
		if Paybook.logger is not None:
			Paybook.logger.debug(message)

class Error(Exception):

	def __init__(self,code,response,message,status):
		self.code = code
		self.response = response
		self.message = message
		self.status = status

	def get_json(self):
		return {
			'code' : self.code,
			'response' : self.response,
			'message' : self.message,
			'status' : self.status
		}# End of return




