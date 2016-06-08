# SDK_UML - REST_API mapping

# Users

Creates a new user:

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates a user | POST https://sync.paybook.com/v1/users   | ```user = User(username)```          |
| Deletes a user | DELETE https://sync.paybook.com/v1/users | ```user.delete()```                  |
| Get users      | GET https://sync.paybook.com/v1/users    | ```users = User.get(config_params)```|


# Sessions

Creates a new session (login):

| Action         | REST API                                 | SDK                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates a session | POST https://sync.paybook.com/v1/sessions   | ```session = Session(user)```          |
| Verify a session | GET https://sync.paybook.com/v1/sessions/:token/verify | ```session.verify()```                  |
| Deletes a session     | DELETE https://sync.paybook.com/v1/sessions/:token    | ```users = session.delete()```|

# Catalogues

Request account types:










