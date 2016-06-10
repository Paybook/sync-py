# -​*- coding: utf-8 -*​-

import main

class Attachment(main.Paybook):

	def __init__(self,attachment_json):
		self.id_account = attachment_json['id_account']
		self.id_user = attachment_json['id_user']
		self.id_external = attachment_json['id_external']
		self.id_attachment_type = attachment_json['id_attachment_type']
		self.id_transaction = attachment_json['id_transaction']
		self.file = attachment_json['file']
		self.extra = attachment_json['extra'] if 'extra' in attachment_json else None
		self.url = attachment_json['url']
		self.dt_refresh = attachment_json['dt_refresh']

	@staticmethod
	def get(session=None,id_user=None,options=None,id_attachment=None,extra=None):
		Attachment.log('\n')
		Attachment.log('Attachment.get')
		if id_user is not None:
			params = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params
		if id_attachment:# Attachment content
			if extra is True:# Extracted data (not the content)
				id_attachment = id_attachment + '/extra'
			attachment_data = Attachment.__call__(endpoint=id_attachment,method='get',params=params)
			return attachment_data
		else:
			attachment_jsons = Attachment.__call__(endpoint='attachments',method='get',params=params)
		attachments = []
		for attachment_json in attachment_jsons:
			attachment = Attachment(attachment_json)
			attachments.append(attachment)
		return attachments

	@staticmethod
	def get_count(session=None,id_user=None,options=None):
		Attachment.log('\n')
		Attachment.log('Attachment.get_count')
		if id_user is not None:
			params = {
				'api_key' : Credentials.api_key,
				'id_user' : id_user
			}#End of params
		else:
			params = {
				'token' : session.token
			}#End of params			
		attachments_count_json = Attachment.__call__(endpoint='attachments/count',method='get',params=params)
		attachments_count = attachments_count_json['count']
		return attachments_count


