# SDK_UML - REST_API mapping

# Users

Creates a new user:

|Action | REST API        | SDK      |
| -| ------------- |:-------------:| 
|Creates a new user| POST https://sync.paybook.com/v1/users     | `user = User(username)` | 
|Deletes a user | DELETE https://sync.paybook.com/v1/users     | `user_deleted_flag = user.delete()` | 
|Get users | GET https://sync.paybook.com/v1/users     | `users = User.get(config_params)` | 

# Sessions

Creates a new session (login):

|Action | REST API        | SDK      |
|-| ------------- |:-------------:| 
|Creates a new session (login)| POST https://sync.paybook.com/v1/sessions     | `user = User(id_user)`<br> `session = Session(user)`<br> `token = session.token` | 
|Verify a session| GET https://sync.paybook.com/v1/sessions/:token/verify    | `session.verify()` | 
|Deletes a session (logout)| DELETE https://sync.paybook.com/v1/sessions/:token     | `session.delete()` |  


# Catalogues

Request account types:










