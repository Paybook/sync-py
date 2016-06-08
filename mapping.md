# SDK_UML - REST_API mapping

Here is the underlying mapping between Paybook SDK projects i.e. sync projects, and [Paybook Sync Rest API](https://www.paybook.com/sync/docs). In the next tables there are examples of how an endpoint must be requested from an SDK and which is the REST API endpoint that is called when this happens.

You can view or download SDK UML [here](https://drive.google.com/file/d/0ByfSP0j-5EqmWDF3bDV0Um9oT2c/view?usp=sharing).

**Important:** the SDK sample code is python-based but the execution's essence must be the same independent of the platform. 

# Users

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates a user | POST https://sync.paybook.com/v1/users   | ```user = User(username)```          |
| Deletes a user | DELETE https://sync.paybook.com/v1/users | ```User.delete(id_user)```                  |
| Get users      | GET https://sync.paybook.com/v1/users    | ```users = User.get(options)```|


# Sessions

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates a session | POST https://sync.paybook.com/v1/sessions   | ```session = Session(user)```          |
| Verify a session | GET https://sync.paybook.com/v1/sessions/:token/verify | ```session.verify()```                  |
| Deletes a session     | DELETE https://sync.paybook.com/v1/sessions/:token    | ```Session.delete(token)```|

# Catalogues

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Request account types | GET https://sync.paybook.com/v1/catalogues/account_types   | ```account_types = Catalogues.get_account_types(session,options)```          |
| Request attachment types | GET https://sync.paybook.com/v1/catalogues/attachment_types   | ```attachment_types = Catalogues.get_attachment_types(session,options)```          |
| Request available countries | GET https://sync.paybook.com/v1/catalogues/countries   | ```countries = Catalogues.get_countries(session,options)```          |
| Request available sites | GET https://sync.paybook.com/v1/catalogues/sites   | ```sites = Catalogues.get_sites(session,options)```          |
| Request site organizations | GET https://sync.paybook.com/v1/catalogues/site_organizations   | ```site_organizations = Catalogues.get_site_organizations(session,options)```          |

# Credentials

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates or updates credentials | POST https://sync.paybook.com/v1/credentials | ```credentials = Credential(session,id_site,credentials_data)```          |
| Deletes credentials | DELETE https://sync.paybook.com/v1/credentials/:id_credential | ```Credentials.delete(session,id_credential)```          |
| Request history of changes made to this credentials | GET https://sync.paybook.com/v1/credentials/:id_credential/status | ```It is pending```          |
| Request register credentials | GET https://sync.paybook.com/v1/credentials | ```credentials_list = Credentials.get(session)```          |

# Accounts

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Requests accounts of a user | GET https://sync.paybook.com/v1/accounts | ```accounts = Account.get(session,options)```          |

# Transactions

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Requests number of transactions | GET https://sync.paybook.com/v1/transactions/count | ```transactions_count = Transaction.get_count(session,options)```          |
| Requests transactions | GET https://sync.paybook.com/v1/transactions | ```transactions = Transaction.get(session,options)```          |

# Attachments

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Requests attachments | GET https://sync.paybook.com/v1/attachments | ```attachments = Attachment.get(session,options)```          |
| Request an attachments | GET https://sync.paybook.com/v1/attachments/:id_attachment | ```attachment = Attachment.get(session,id_attachment)```          |
| Request the extracted data from attachment | GET https://sync.paybook.com/v1/attachments/:id_attachment/extra | ```attachments = Attachment.get(session,id_attachment,extra=True)```          |
| Request the number of attachments | GET https://sync.paybook.com/v1/attachments/counts | ```attachments_count = Attachment.get_count(session,options)```          |





