

# Paybook SDK


# Users

| Action         | REST API ENDPOINT                                 | SDK METHOD                                 |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates a user | POST https://sync.paybook.com/v1/users   | ```User user = User(name=String,id_user=String)```          |
| Deletes a user | DELETE https://sync.paybook.com/v1/users | ```bool deleted = User.delete(id_user=None)```                  |
| Get users      | GET https://sync.paybook.com/v1/users    | ```list [User] = User.get()```|


# Sessions

| Action         | REST API ENDPOINT                                 | SDK METHOD                                  |
| -------------- | ---------------------------------------- | ------------------------------------ |
| Creates a session | POST https://sync.paybook.com/v1/sessions   | ```Session session = Session(user=String)```          |
| Verify a session | GET https://sync.paybook.com/v1/sessions/:token/verify | ```bool verified = session.verify()```                  |
| Deletes a session     | DELETE https://sync.paybook.com/v1/sessions/:token    | ```bool deleted = Session.delete(token)```|



