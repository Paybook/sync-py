

# Paybook SDK

Paybook(api_key,db_environment=False,web_environment=False,logger=None)

**Sessions**

paybook.signup(username, password)
paybook.login(username, password)
paybook.validate_session(self, token)

----

**Catalogues**

paybook.catalogues(token)

----

**Credentials**

paybook.credentials(token, id_site, credentials)
paybook.delete_credentials(token, id_credential, id_user=None)
paybook.get_credentials(token, id_user=None)
paybook.status(self, token, id_site, url_status=None)
paybook.twofa(self, token, id_site, twofa, url_twofa=None)

----

**Transactions**

paybook.transactions(self, token, id_account)
paybook.accounts(token, id_site)

----


  



