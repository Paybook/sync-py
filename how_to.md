
# Tutorial for coding a Library for Sync's API

Follow these steps when you were working on a library to connect to Paybook Sync's API. Following this steps will ensure your library has the same structure and standards as all Paybook Sync's libraries.

## General Understanding:

Before building the library you must have a general understanting of what you are going to do. First of all it is important you to study **REST architecture**, you can read this [article](http://asiermarques.com/2013/conceptos-sobre-apis-rest/) were you can find a brief summary of what REST is and how it must be implemented. Once you know this, you must study our [Sync's API docs](https://www.paybook.com/sync/docs), you must know what this API is for, how to implement it and so on. You must be familiar with **Object-oriented programming** and **Uniform Markup Language** too.

Once you have studied REST architecture and our Sync's API you must be sure about what you are working on. Your working on a library in some technology (maybe Python, JAVA, Ruby or other) whose objective is to give access a developer to the Sync's API in a native way. For example, suppose Mark is a developer coding its application on Python and he wants to implement Sync's API to connect its app with bank institutions, of course he can consume our REST API directly from Python like this:

```python
import requests
data = {
	'api_key' : API_KEY,
	'id_user' : id_user,
	'id_site' : id_site
}#End of data
headers = {
	'Content-type' : 'application/json'
}#End of headers	
requests.post('https://sync.paybook.com/v1/credentials',data=data,headers=headers)
if conn.status_code == 200:
	# Code for handling success
	try:# JSON responses:
		return conn.json()['response']
	except Exception as e:# Attachments:
		return conn.content
	else:
		# Code for handling error
```

Mark must do this every time he is consuming Sync's API, of course if he is a good developer he can pack this code in a function and invoke it from his code and pass some parameters to it like the endpoint and the HTTP verb but even doing this he will have to code and implement all the API connection by his own, and this implies he has to study by detail Sync's REST API, see all the HTTP verbs he can use, check if he has to perform a query string or a JSON, match the content type, handling all the errors, and so on. Now, imagine that Paybook has a library in the technology you are coding, then instead of all the code you saw before he can do something like this:

```python
credentials = paybook.Credentials(session=session,id_site=id_site)
```

The functionallity will be the same, the difference is that Mark just have to execute a native method of a native class in the tecnhology that he was using, in this case Python. So the integration of Sync's API in that technology is easier when the library exists. 

So you're working on building that library that will simplify the life of Mark and all the developers who wants to consume Sync's API in that technology. But before you code that library you have to realize that there are some requirements that your library should fulfill.

### 1. UML:

You will have access to an UML diagram that match Sync's Rest API into a Object-oriented Programming project (OOP). So, for example, Sync's API has and endpoint for manage users "sync.paybook.com/v1/users" and depending on what you're doing, we say creating, deleting or just querying an user you should perform a GET or POST on that endpoint. This endpoint is matched into our OOP project using the User class which has the methods for creating, deleting or querying an user. So we have something like this for the match between users endpoint and the User class:

**User class methods:** 

	+ constructor User matchs with POST https://sync.paybook.com/v1/users endpoint
	+ static User.delete matchs with DELETE https://sync.paybook.com/v1/users endpoint
	+ static User.get matchs with GET https://sync.paybook.com/v1/users endpoint

And because an user has some attributes we have:

**User class attributes:**

	+ str name 
	+ str id_user 
	+ str id_external 
	+ str dt_create 
	+ str dt_modify

It is impotant to mention that all the classes have their instances so when you perform an User.get it should return an array of User instances, but the execution of **GET https://sync.paybook.com/v1/users** will return a JSON, so there should be a logic that parse all the Sync's API responses into classes instances. So instead of having a json user like this:

```
{"dt_create": 1466343938, "dt_modify": null, "id_external": null, "id_user": "5766a2020b212a3c058b456d", "name": "miguelmateo"}
```

You should have an User instance with its dt_create, dt_modify, id_extarnal, id_user and name attributes and of course its methods. 

This match should be applied for all the endpoints of Sync's API so we have this match:

* User class matchs with sync.paybook.com/v1/users endpoint
* Session class matchs with sync.paybook.com/v1/sessions endpoint
* Transaction class matchs with sync.paybook.com/v1/transactions endpoint
* Credentials class matchs with sync.paybook.com/v1/credentials endpoint
* Account class matchs with sync.paybook.com/v1/accounts endpoint
* Attachment class matchs with sync.paybook.com/v1/attachments endpoint
* Catalogues class matchs with sync.paybook.com/v1/catalogues endpoint

You can see and download the complete UML for the library [here](https://drive.google.com/file/d/0ByfSP0j-5EqmOU9Pc1FZLWpLajg/view?usp=sharing)

You should code the library according to this UML, in it they are specified:

* Classes
* Class attributes, specifiyng its type
* Class methods, specifiyng whether they are instace or static methods and 	the value returned. 
* Inheritances and relations between classes


And you should consider this:

* Almost all the classes inherit from Paybook class so they can access to its attributes and methods
* You will see a Paybook.__call__ method, this method should be used for the Sync API connection in order to centralize the call to the API in just one method.
* You will see a Paybook.API_KEY attribute, this attribute should be used every time another method requires the API_KEY
* You will see an Error class that inhertis from Exception, here you should implement this class and inherit from the Exception class used in the library's technology/programming language.
* All the errors returned by Sync API (e.g 401, 402, 500, etc) should be raised using the paybook.Error class (which is an exception class)
* You must catch exceptions in your code (library execution errors). Imagine that you are expecting in some library method a key in some dictionary and this key does not exist in that dictionary then your library method will fail, of course its a developer error but maybe it could not be. This kind of errors could be catched as exceptions, for this example in specific we can catch an exception like this  _KeyError
Raised when a mapping (dictionary) key is not found in the set of existing keys_. You must catch this code execution exceptions and raise it as paybook.Error instances just as Sync API errors, but these errors must have code 500 and the message should be the exception message. We expect our code to be as stable as posible and put it an exception handler does not mean that we don't trust in our code is just to have a better practice when coding libraries recognizing that we are humans and we can not predict everything, always there are use cases we did not consider and its better to return an internal error than your library just does not function affecting the execution of the developer's application.
* You can see that some methods recieve as params something like this: Session s or String id_user, this means this method could be executed using a session object, or using an id_user. In the last case the method must use the api_key attribute of Paybook Class and instead of performing a token authentication it should perform an id_user plus api_key authentication. The difference between them is that when you are using a Session (token authentication) you just can perform CRUD operations on the session's user owner and in the second case (id_user plus api key authentication) you can perform CRUD operations on any user because you can specify it by the id_user param, but the logic of both should be the same the only difference is the authentication process.

### 2. Unit Testing

Once you have coded your library and maybe perform some testing you should perform a general unit testing. The flow of the testing you must perform is the next:

	Initialization

		1. Start Library with incorrect API_KEY
		2. Perfom a call to the library (execute some method that uses the API_KEY) -> it should return error
		3. Start Library with incorrect API_KEY

	Users
			
		4. Get users
		5. Creates a new user (creates an instance of a new user)
		6. Get users (it should return 1 user more than step 4)
		7. Delete the created user 
		8. Get users (it should be equal to step 4)
		9. Creates a new user again (store its id_user it should be used in future steps)

	Sessions

		10. Creates a new user (using the id_user stored in step 9, this creates an instance of an existing user)
		11. Creates a new session of the user created in step 10
		12. Verify session
		13. Delete session
		14. Verify session -> it should return error because session does not exist, it was deleted
		15. Creates a new session again

	Catalogues

		16. Get account types
		17. Get attachment types
		18. Get countries
		19. Get site types
		20. Get test site types (store the test title which nama is "Token" it will be used in future steps
		21. Get site organization types
		22. Get the SAT/CIEC site, you must get sites and extract it from the array by iterating it (store it, it will be used in future steps)

	Credentials

		23. Get credentials
		24. Creates credentials params for SAT/CIEC site using its configuration structure (you should use the site obtained in step 22)
		25. Creates credentials for SAT/CIEC site (you should use the site obtained in step 22)
		26. Get credentials (it should return 1 user more than step 23)
		27. Delete credentials created in step 25
		28. Get credentials (they should be equal to step 23)
		29. Creates credentials for SAT/CIEC site again (you should use the site obtained in step 22)
		30. Creates credentials for Token test site (you should use the site obtained in step 20)
		32. Check status and wait for status 410
		33. Send token using set_twofa method

	Accounts

		34. Get accounts

	Transactions

		35. Get transactions count
		36. Get transactions

	Attachments 

		37. Get attachments count
		38. Get attachments

Your library should perform all this unit test with success execution or throw an error when you were expecting an error. You can build a script to perform this unit test. If you have any doubt you can see the Python Library [unit test script](https://github.com/Paybook/sync-py/blob/master/unit_test.py).

### 3. Package Manager

Once you have coded your library and have performed the unit test you can publish it so the developers that wants to implement Paybook Sync's API can use your library. But how can they find it? You can publish the project on git and they could perform a git clone or something like this but in order to do this you have to perform more than one step and it is not elegant at all. So you have to use the Package Manager of the technology your library is built. So these developers can install your library using the package manager and just import it as a dependency of their projects. 

Example of package managers are pip for Python, npm for NodeJS, gem for Ruby, cocoapod for swift/IOS and so on. If there is more than one package manager in your technology you could upload it to the most used ones. 

Once you have uploaded your library to the package manager try to install it using the package manager. It's important to perform the unit test again to verify that your library was uploaded correctly and that it is correctly installed with the package manager.

### 4. Quickstarts/Documentation:

Don't care about your library general documentation. As all the libraries were built below the same requirements and according to the same UML the general documentation for all the libraries will be the same. By general documentation we mean the documentation where all the classes, methods, attributes, returned values, parameters are described in detail. 

But you have to build the 3 basic quickstarts. A quickstart is a brief tutorial based on an exisitng script that performs a specific task. In this case we have 3 main quickstarts whose objective is to show how to connect to the Sync's API using you're library to do this:

1. Syncrhonize the tax bill institution (SAT)
2. Syncrhonize a simple bank institution (a bank whose authentication only requires user and password)
3. Syncrhonize a complex bank institution (a bank whose authentication requires user, password and token)

But don't worry about drafting you can have the documentation quickstart templates:

1. [quickstart_sat.md](https://github.com/Paybook/sync-py/blob/master/quickstart_sat.md)
2. [quickstart_normal_bank.md](https://github.com/Paybook/sync-py/blob/master/quickstart_normal_bank.md)
3. [quickstart_token_bank.md](https://github.com/Paybook/sync-py/blob/master/quickstart_token_bank.md)

These files are in the project [sync-py](https://github.com/Paybook/sync-py) so you can copy the content and paste it in your own quickstarts files, so in your project on git there must be a quickstart_sat.md, quickstart_normal_bank.md and and quickstart_token_bank.md. All this projects must have the same content (drafting) you just must customize the parts were there are code samples, for example if you're documenting the Java library you should change this (in Python):

```python
user = paybook.User(name='MY_USER')
my_users = paybook.User.get()
for user in my_users:
    print user.name
```

for this (in Java):

```java
User user = new User('MY_USER')
User[] my_users = User.get()
for(i=0; i<my_users.lenght; i++){
	user = my_users[i]
	System.out.println(user.name)
}
```

And you should do this for all the code samples, once you do this you will have your quickstarts ready. Apart from this you should have your quickstart scripts, for example, if your library is in Python:

1. [quickstart_sat.py](https://github.com/Paybook/sync-py/blob/master/quickstart_sat.py)
2. [quickstart_normal_bank.py](https://github.com/Paybook/sync-py/blob/master/quickstart_normal_bank.py)
3. [quickstart_token_bank.py](https://github.com/Paybook/sync-py/blob/master/quickstart_token_bank.py)

These scripts are the ones that support your quickstarts, the code you put on your quickstarts as code samples there must be in these scripts. So a developer can download these scripts and run them instead of write all the code. The quickstarts will tell them how this code works and how the connection to Paybook Sync's API should be implemented using the library. For example if your library is in javascript you should have a quickstart_sat.js, quickstart_normal_bank.js and quickstart_token_bank.js.

### You have finished!

Once you have coded your library, performing the unit testing, upload it to the package manager and build the quickstarts you library is finished :)









