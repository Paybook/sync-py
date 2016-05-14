

# Paybook SDK

----

Constructor
----------

**Paybook**(api_key,db_environment=None,logger=None)

----

Sessions
----------

**paybook.signup**(username)

**paybook.login**(username)

**paybook.validate_session**(token)

----

Catalogues
----------

**paybook.catalogues**(token)

----

Credentials
----------


**paybook.credentials**(token, id_site,credentials)
**paybook.delete_credentials**(token,id_credential,id_user=None)
**paybook.get_credentials**(token,id_user=None)
**paybook.status**(token,id_site,url_status=None)
**paybook.twofa**(token,id_site,twofa,url_twofa=None)

----

Transactions
----------

**paybook.transactions**(token,id_account)
**paybook.accounts**(token,id_site)

----


  