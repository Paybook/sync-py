

# Paybook SDK






### Accounts

Estructura de los atributos de la clase:

| Account         |                                  
| -------------- | 
| + id_account <br> + id_external <br> + id_user <br> + id_credential <br> + id_site <br> + id_site_organization <br> + name <br> + number <br> + balance <br> + site <br> + dt_refresh  |
				
Descripción de los métodos de la clase:

| Action         | REST API ENDPOINT                                 | SDK METHOD                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Requests accounts of a user | GET https://sync.paybook.com/v1/accounts | ```list [Account] = Account.get(session=Session,id_user=str)```          |

### Attachments

| Action         | REST API ENDPOINT                                 | SDK METHOD                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Requests attachments | GET https://sync.paybook.com/v1/attachments <br> GET https://sync.paybook.com/v1/attachments/:id_attachment <br> GET https://sync.paybook.com/v1/attachments/:id_attachment/extra | ```attachments = Attachment.get(session=Session,id_user=str,id_attachment=str,extra=bool)```          |
| Request the number of attachments | GET https://sync.paybook.com/v1/attachments/counts | ```int attachments_count = Attachment.get_count(session=Session,id_user=str)```          |


### Catalogues

| Action         | REST API ENDPOINT                                 | SDK METHOD                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Request account types | GET https://sync.paybook.com/v1/catalogues/account_types   | ```list [Account_type] = Catalogues.get_account_types(session=Session,id_user=str)```          |
| Request attachment types | GET https://sync.paybook.com/v1/catalogues/attachment_types   | ```list [Attachment_type] = Catalogues.get_attachment_types(session=Session,id_user=str)```          |
| Request available countries | GET https://sync.paybook.com/v1/catalogues/countries   | ```list [Country] = Catalogues.get_countries(session=Session,id_user=str)```          |
| Request available sites | GET https://sync.paybook.com/v1/catalogues/sites   | ```list [Site] = Catalogues.get_sites(session=Session,id_user=str)```          |
| Request site organizations | GET https://sync.paybook.com/v1/catalogues/site_organizations   | ```list [Site_organization] = Catalogues.get_site_organizations(session=Session,id_user=str)```          |

### Credentials

| Action         | REST API ENDPOINT                                 | SDK METHOD                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates or updates credentials | POST https://sync.paybook.com/v1/credentials | ```Credentials credentials = Credential(session=str,id_user=str,id_site=str,credentials=dict)```          |
| Deletes credentials | DELETE https://sync.paybook.com/v1/credentials/:id_credential | ```bool deleted Credentials.delete(session=Session,id_user=str,id_credential=str)```          |
| Request history of changes made to this credentials | GET https://sync.paybook.com/v1/credentials/:id_credential/status | ```It is pending```          |
| Request register credentials | GET https://sync.paybook.com/v1/credentials | ```list [Credentials] = Credentials.get(session=Session,id_user=str)```          |


### Sessions

| Action         | REST API ENDPOINT                                 | SDK METHOD                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates a session | POST https://sync.paybook.com/v1/sessions   | ```Session session = Session(user=str)```          |
| Verify a session | GET https://sync.paybook.com/v1/sessions/:token/verify | ```bool verified = session.verify()```                  |
| Deletes a session     | DELETE https://sync.paybook.com/v1/sessions/:token    | ```bool deleted = Session.delete(token=str)```|


### Transactions

| Action         | REST API ENDPOINT                                 | SDK METHOD                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Requests number of transactions | GET https://sync.paybook.com/v1/transactions/count | ```int transactions_count = Transaction.get_count(session=Session,id_user=str)```          |
| Requests transactions | GET https://sync.paybook.com/v1/transactions | ```list [Transaction] = Transaction.get(session=Session,id_user=str)```          |

### Users

| Action         | REST API ENDPOINT                                 | SDK METHOD                                 |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates a user | POST https://sync.paybook.com/v1/users   | ```User user = User(name=str,id_user=str)```          |
| Deletes a user | DELETE https://sync.paybook.com/v1/users | ```bool deleted = User.delete(id_user=str)```                  |
| Get users      | GET https://sync.paybook.com/v1/users    | ```list [User] = User.get()```|