# -​*- coding: utf-8 -*​-

from json import dumps
import main

class Credentials(main.Paybook):

	def __init__(self,session=None,id_user=None,id_site=None,credentials=None,credentials_json=None):# If it already exists it retrieves the existing one
		Credentials.log('\n')
		Credentials.log('Credentials.__init__')
		self.id_site = None
		self.twofa_config = None
		if credentials_json is None:
			if id_user is not None:
				data = {
					'api_key' : Credentials.api_key,
					'id_user' : id_user
				}#End of data
			else:
				data = {
					'token' : session.token
				}#End of data
			data['id_site'] = id_site
			data['credentials'] = credentials
			credentials_json = Credentials.__call__(endpoint='credentials',method='post',data=dumps(data))
		if id_site is not None:
			self.id_site = id_site
		elif 'id_site' in credentials_json:
			self.id_site = credentials_json['id_site']
		self.id_credential = credentials_json['id_credential']
		self.username = credentials_json['username']
		self.id_site_organization = credentials_json['id_site_organization'] if 'id_site_organization' in credentials_json else None
		self.id_site_organization_type = credentials_json['id_site_organization_type'] if 'id_site_organization_type' in credentials_json else None
		self.ws = credentials_json['ws'] if 'ws' in credentials_json else None
		self.status = credentials_json['status'] if 'status' in credentials_json else None
		self.twofa = credentials_json['twofa'] if 'twofa' in credentials_json else None

	@staticmethod
	def delete(session=None,id_user=None,id_credential=None):
		Credentials.log('\n')
		Credentials.log('Credentials.delete')
		if id_user is not None:
			params = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		delete_response = Credentials.__call__(endpoint='credentials/'+id_credential,method='delete',params=params)
		return True

	@staticmethod
	def get(session=None,id_user=None):
		Credentials.log('\n')
		Credentials.log('Credentials.get')
		if id_user is not None:
			params = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		credentials_jsons = Credentials.__call__(endpoint='credentials',method='get',params=params)
		credentials_list = []
		for credentials_json in credentials_jsons:
			credentials = Credentials(credentials_json=credentials_json)
			credentials_list.append(credentials)
		return credentials_list

	def get_status(self,session=None,id_user=None):
		Credentials.log('\n')
		Credentials.log('Credentials.status')
		headers = {'Content-type' : 'application/json'}		
		if id_user is not None:
			data = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of data
		else:
			data = {
				'token' : session.token
			}#End of data
		if self.id_site is not None:
			data['id_site'] = self.id_site
			status = Credentials.__call__(method='get',data=dumps(data),headers=headers,url=self.status)
			for each_status in status:
				code = each_status['code']
				if code == 410:
					self.twofa = each_status['address']
					self.twofa_config = each_status['twofa'][0]
			return status

	def set_twofa(self,session=None,id_user=None,twofa_value=None):
		Credentials.log('\n')
		Credentials.log('Credentials.twofa')
		headers = {'Content-type' : 'application/json'}		
		if id_user is not None:
			data = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of data
		else:
			data = {
				'token' : session.token
			}#End of data
		if self.id_site:
			data['id_site'] = self.id_site
			data['twofa'] = {}
			data['twofa'][self.twofa_config['name']] = twofa_value
			Credentials.__call__(method='post',data=dumps(data),url=self.twofa)
			return True

	def get_json(self):
		return {
			'id_site' : self.id_site,
			'id_site_organization' : self.id_site_organization,
			'id_site_organization_type' : self.id_site_organization_type,
			'id_credential' : self.id_credential,
			'status' : self.status,
			'twofa' : self.twofa,
			'ws' : self.ws,
			'username' : self.username
		}#End of return

	# @staticmethod# Pending because it is not implemented in REST API yet
	# def status(session=None,id_user=None,id_credential=None):
	# 	Credentials.log('\n')
	# 	Credentials.log('Credentials.get_status')
	# 	if id_user is not None:
	# 		params = {
	# 			'api_key' : Credentials.api_key,
	# 			'id_user' : id_user
	# 		}#End of params
	# 	else:
	# 		params = {
	# 			'token' : session.token
	# 		}#End of params
	# 	status_json = Credentials.__call__(endpoint='credentials/'+id_credential+'/status',method='get',params=params)
	# 	print status_json








