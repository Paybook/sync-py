# -​*- coding: utf-8 -*​-

import main

class Catalogues(main.Paybook):

	@staticmethod
	def get_account_types(session=None,id_user=None,options=None):
		Catalogues.log('\n')
		Catalogues.log('Catalogues.get_account_types')
		if id_user is not None:
			params = {
				'api_key' : Catalogues.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		account_type_jsons = Catalogues.__call__(endpoint='catalogues/account_types',method='get',params=params)
		account_types = []
		for account_type_json in account_type_jsons:
			account_type = Account_type(account_type_json)
			account_types.append(account_type)
		return account_types

	@staticmethod
	def get_attachment_types(session=None,id_user=None,options=None):
		Catalogues.log('\n')
		Catalogues.log('Catalogues.get_attachment_types')
		if id_user is not None:
			params = {
				'api_key' : Catalogues.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		attachment_type_jsons = Catalogues.__call__(endpoint='catalogues/attachment_types',method='get',params=params)
		attachment_types = []
		for attachment_type_json in attachment_type_jsons:
			attachment_type = Attachment_type(attachment_type_json)
			attachment_types.append(attachment_type)
		return attachment_types

	@staticmethod
	def get_countries(session=None,id_user=None,options=None):
		Catalogues.log('\n')
		Catalogues.log('Catalogues.get_countries')
		if id_user is not None:
			params = {
				'api_key' : Catalogues.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		country_jsons = Catalogues.__call__(endpoint='catalogues/countries',method='get',params=params)
		countries = []
		for country_json in country_jsons:
			country = Country(country_json)
			countries.append(country)
		return countries

	@staticmethod
	def get_sites(session=None,id_user=None,options=None,is_test=False):
		Catalogues.log('\n')
		Catalogues.log('Catalogues.get_sites')
		if id_user is not None:
			params = {
				'api_key' : Catalogues.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		if is_test is True:
			params['is_test'] = is_test
		site_jsons = Catalogues.__call__(endpoint='catalogues/sites',method='get',params=params)
		sites = []
		for site_json in site_jsons:
			site = Site(site_json)
			sites.append(site)
		return sites
 
	@staticmethod
	def get_site_organizations(session=None,id_user=None,options=None,is_test=False):
		Catalogues.log('\n')
		Catalogues.log('Catalogues.get_site_organizations')
		if id_user is not None:
			params = {
				'api_key' : Catalogues.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		if is_test is True:
			params['is_test'] = is_test
		site_organization_jsons = Catalogues.__call__(endpoint='catalogues/site_organizations',method='get',params=params)
		site_organizations = []
		for site_organization_json in site_organization_jsons:
			site_organization = Site_organization(site_organization_json)
			site_organizations.append(site_organization)
		return site_organizations

class Account_type():

	def __init__(self,account_type_json):
		self.id_account_type = account_type_json['id_account_type']
		self.name = account_type_json['name']

class Attachment_type():

	def __init__(self,attachment_type_json):
		self.id_attachment_type = attachment_type_json['id_attachment_type']
		self.name = attachment_type_json['name']

class Country():

	def __init__(self,country_json):
		self.id_country = country_json['id_country']
		self.name = country_json['name']
		self.code = country_json['code']

class Site():

	def __init__(self,site_json):
		self.id_site = site_json['id_site']
		self.id_site_organization = site_json['id_site_organization']
		self.id_site_organization_type = site_json['id_site_organization_type']
		self.name = site_json['name']
		credentials_structures = []
		for credential_structure_json in site_json['credentials']:
			credentials_structure = Credentials_structure(credential_structure_json)
			credentials_structures.append(credentials_structure)
		self.credentials = credentials_structures
		self.site_json = site_json

	def get_json(self):
		return self.site_json

class Credentials_structure():

	def __init__(self,credentials_structure_json):
		self.name = credentials_structure_json['name']
		self.type = credentials_structure_json['type']
		self.label = credentials_structure_json['label']
		self.required = credentials_structure_json['required']
		self.username = credentials_structure_json['username']
		self.validation = None

class Site_organization():

	def __init__(self,site_organization_json):
		self.id_site_organization = site_organization_json['id_site_organization']
		self.id_site_organization_type = site_organization_json['id_site_organization_type']
		self.id_country = site_organization_json['id_country']
		self.name = site_organization_json['name']
		self.avatar = site_organization_json['avatar']
		self.small_cover = site_organization_json['small_cover']
		self.cover = site_organization_json['cover']
		self.site_organization_json = site_organization_json

	def get_json(self):
		return self.site_organization_json






























