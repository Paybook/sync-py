# -​*- coding: utf-8 -*​-

import main

class Session(main.Paybook):

	def __init__(self,user=None,token=None):
		self.user = user
		if token is not None:
			self.token = token
			self.iv = None
			self.key = None
		else:
			Session.log('\n')
			Session.log('Session.__init__')
			data = {
				'api_key' : Session.api_key, 
				'id_user' : self.user.id_user
			}#End of data
			session_json = Session.__call__(endpoint='sessions',method='post',data=data)
			self.token = session_json['token'] if 'token' in session_json else None
			self.iv = session_json['iv'] if 'iv' in session_json else None
			self.key = session_json['key'] if 'key' in session_json else None

	def verify(self):
		Session.log('\n')
		Session.log('Session.verify')
		Session.__call__(endpoint='sessions/' + self.token + '/verify',method='get')# If not, raise Error
		return True

	@staticmethod
	def delete(token=None):
		Session.log('\n')
		Session.log('Session.delete')
		Session.__call__(endpoint='sessions/' + token + '',method='delete')# If error, raise Error
		return True

	def set_token(self,token):
		self.token = token

	def get_json(self):
		return {
			'iv' : self.iv,
			'key' : self.key,
			'token' : self.token
		}#End of return

