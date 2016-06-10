# -​*- coding: utf-8 -*​-

import main

class Session(main.Paybook):

	def __init__(self,user=None):
		Session.log('\n')
		Session.log('Session.__init__')
		self.user = user
		data = {
			'api_key' : Session.api_key, 
			'id_user' : self.user.id_user
		}#End of data
		session_json = Session.__call__(endpoint='sessions',method='post',data=data)
		self.token = session_json['token']

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

	
