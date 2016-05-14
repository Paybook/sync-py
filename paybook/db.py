# -​*- coding: utf-8 -*​-

import sqlite3
import datetime

connection = sqlite3.connect('./paybook.db',check_same_thread=False)
cur = connection.cursor()

users_table_cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
users_table_exist = cur.execute(users_table_cmd).fetchone()
if not users_table_exist:
	cur.execute('''CREATE TABLE users (username text, password text, id_user text, date text, token text)''')
credentials_table_cmd = "SELECT name FROM sqlite_master WHERE type='table' AND name='credentials'"
credentials_table_exist = cur.execute(credentials_table_cmd).fetchone()
if not credentials_table_exist:
	cur.execute(''' CREATE TABLE credentials (id_user text, id_site text, ws text, status text, twofa text, id_credential text)''')

class User():	

	def __init__(self,*args,**kwargs):
		if len(args) == 2:
			self.username = args[0]
			self.password = args[1]
			self.token = None
		if len(args) == 1:
			self.token = args[0]
			self.username = None
			self.password = None

	def save(self):
		date = datetime.datetime.utcnow()
		insert_user = [(self.username,self.password ,self.id_user,date,''),]
		cur.executemany('INSERT INTO users VALUES (?,?,?,?,?)', insert_user)
		connection.commit()	
	
	def set_token(self,token):
		self.token = token
		update_user = [(self.token,self.username),]
		cur.executemany('''UPDATE users SET token = ? WHERE username = ? ''',update_user)
		connection.commit()

	def set_id_user(self,id_user):
		self.id_user = id_user

	def am_i_logged_in(self):
		yes = False
		if self.token is not None:
			cur.execute('SELECT * FROM users WHERE token=?',(self.token,))
		user = cur.fetchone()
		if user is not None:
			yes = True
		return yes

	def get_id_user(self):
		if self.token is not None:
			cur.execute('SELECT * FROM users WHERE token=?',(self.token,))
		else:
			username = self.username
			cur.execute('SELECT * FROM users WHERE username=?',(username,))
		user = cur.fetchone()
		return user[2]

	def do_i_exist(self):
		username = self.username
		cur.execute('SELECT * FROM users WHERE username=?',(username,))
		user = cur.fetchone()	
		if user is not None:
			return True
		else:
			return False

	def login(self):
		username = self.username
		cur.execute('SELECT username, password FROM users WHERE username=?',(username,))
		user_and_psw = cur.fetchone()
		username = None
		password = None
		if user_and_psw is not None:
			username = user_and_psw[0]
			password = user_and_psw[1]		
		if username == self.username and password == self.password:	
			return True
		else:		
			return False

class Credentials():	

	def __init__(self,*args,**kwargs):
		if len(args) == 6:
			self.id_user = args[0]
			self.id_site = args[1]
			self.ws = args[2]
			self.status = args[3]
			self.twofa = args[4]
			self.id_credential = args[5]
		if len(args) == 2:
			self.id_user = args[0]
			self.id_site = args[1]
			self.ws = None
			self.status = None
			self.twofa = None
			self.id_credential = None
		if 'id_credential' in kwargs:
			self.id_user = args[0]
			self.id_credential = kwargs['id_credential']
			self.id_site = None

	def save(self):
		date = datetime.datetime.utcnow()
		credentials = [(self.id_user,self.id_site ,self.ws,self.status,self.twofa,self.id_credential),]
		cur.executemany('INSERT INTO credentials VALUES (?,?,?,?,?,?)', credentials)
		connection.commit()	

	def delete(self):
		id_user = self.id_user
		if self.id_credential:	
			id_credential = self.id_credential
			cur.execute('DELETE FROM credentials WHERE id_user=? AND id_credential=?',(id_user,id_credential))
		else:
			id_site = self.id_site
			cur.execute('DELETE FROM credentials WHERE id_user=? AND id_site=?',(id_user,id_site))

	def do_i_exist(self):
		id_user = self.id_user
		if self.id_credential:	
			id_credential = self.id_credential
			cur.execute('SELECT * FROM credentials WHERE id_user=? AND id_credential=?',(id_user,id_credential))
		else:
			id_site = self.id_site
			cur.execute('SELECT * FROM credentials WHERE id_user=? AND id_site=?',(id_user,id_site))
		credentials = cur.fetchone()	
		if credentials is not None:
			return True
		else:
			return False

	def get_twofa(self):
		id_user = self.id_user
		id_site = self.id_site
		cur.execute('SELECT * FROM credentials WHERE id_user=? AND id_site=?',(id_user,id_site))
		credentials = cur.fetchone()
		twofa = credentials[4]
		return twofa

	def get_status(self):
		id_user = self.id_user
		id_site = self.id_site
		cur.execute('SELECT * FROM credentials WHERE id_user=? AND id_site=?',(id_user,id_site))
		credentials = cur.fetchone()
		twofa = credentials[3]
		return twofa

	def get_ws(self):
		id_user = self.id_user
		id_site = self.id_site
		cur.execute('SELECT * FROM credentials WHERE id_user=? AND id_site=?',(id_user,id_site))
		credentials = cur.fetchone()
		ws = credentials[2]
		return ws

	@staticmethod
	def get(id_user):
		credentials_list = []
		cur.execute('SELECT * FROM credentials WHERE id_user=?',(id_user,))
		fetched_credentials = cur.fetchall()
		for fetched_credential in fetched_credentials:
			credential = {
				'id_credential' : fetched_credential[5],
				'ws' : fetched_credential[2],
				'status' : fetched_credential[3],
				'twofa' : fetched_credential[4]
			}#End of credential
			credentials_list.append(credential)
		return credentials_list




