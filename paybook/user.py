# -​*- coding: utf-8 -*​-

import main

class User(main.Paybook):

	def __init__(self,name=None,id_user=None,user_json=None):# If it already exists it retrieves the existing one
		User.log('\n')
		User.log('User.__init__')
		if user_json is None:
			if id_user is None and name is not None:# New user
				User.log('Creating new user ... ')
				data = {
					'api_key' : User.api_key, 
					'name' : name
				}#End of data
				user_json = User.__call__(endpoint='users',method='post',data=data)
			elif id_user is not None:# Existing user
				User.log('Retrieveing existing user ... ')
				existing_users = User.get()
				for existing_user in existing_users:
					id_existing_user = existing_user.id_user
					if id_existing_user == id_user:
						user_json = existing_user.get_json()
		self.name = user_json['name']
		self.id_user = user_json['id_user']
		self.id_external = user_json['id_external']
		self.dt_create = user_json['dt_create']
		self.dt_modify = user_json['dt_modify']

	@staticmethod
	def delete(id_user=None):
		User.log('\n')
		User.log('User.delete')
		params = {
			'api_key' : User.api_key
		}#End of params
		delete_response = User.__call__(endpoint='users/'+id_user,method='delete',params=params)
		return True

	@staticmethod
	def get(options=None):
		User.log('\n')
		User.log('User.get')
		params = {
			'api_key' : User.api_key
		}#End of params
		user_jsons = User.__call__(endpoint='users',method='get',params=params)
		users = []
		for user_json in user_jsons:
			user = User(user_json=user_json)
			users.append(user)
		return users

	def get_json(self):
		return {
			'name' : self.name,
			'id_user' : self.id_user,
			'id_external' : self.id_external,
			'dt_create' : self.dt_create,
			'dt_modify' : self.dt_modify
		}#End of return
