import tornado.ioloop
import tornado.web
import sqlite3
import datetime
import json

def checkDB():
	conn = sqlite3.connect('api.db')
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS user (\
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
		name TEXT,\
		created_datetime TEXT,\
		updated_datetime TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS listing (\
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
		userid INTEGER,\
		price TEXT,\
		listing_type TEXT,\
		postal_code TEXT,\
		status TEXT,\
		created_datetime TEXT,\
		updated_datetime TEXT,\
		FOREIGN KEY (userid) REFERENCES User(id),\
		CHECK (listing_type IN ("rent","sale")),\
		CHECK (status IN ("active","closed","deleted")))')
	conn.commit()
	conn.close()

def execute_query(_query):
    #Function to connect db and execute queries
    dbPath = 'api.db'
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    try:
    	c.execute(_query)
        result = c.fetchall()
        conn.commit()
    except Exception:
        raise
    conn.close()
    return result

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/api/user/get_users/?", ListUserHandler),
			(r"/api/user/new_user/?", NewUserHandler),
			(r"/api/user/update_user/?", UpdateUserHandler),
			(r"/api/user/delete_user/?", DeleteUserHandler),
			(r"/api/listing/get_listings/?", ShowListingHandler),
			(r"/api/listing/new_listing/?", NewListingHandler),
			(r"/api/listing/update_listing/?", UpdateListingHandler),
			(r"/api/listing/delete_listing/?", DeleteListingHandler),
		]
		tornado.web.Application.__init__(self,handlers)

class NewListingHandler(tornado.web.RequestHandler):
	def post(self):
		userid = self.get_argument('userid',None)
		price = self.get_argument('price',None)
		listing_type = self.get_argument('listing_type',None)
		postal_code = self.get_argument('postal_code',None)
		status = self.get_argument('status',None)
		execute_query("INSERT INTO listing (userid,price,listing_type,postal_code,status,created_datetime,updated_datetime) VALUES (%s,'%s','%s','%s','%s',DateTime('now'),DateTime('now'))"%(userid,price,listing_type,postal_code,status))
		self.write(json.dumps(dict(result="New Listing Created")))

class ShowListingHandler(tornado.web.RequestHandler):
	def get(self):
		retval = []
		listings = execute_query("SELECT * FROM listing")
		for listing in listings:
			listing_dict = dict()
			listing_dict['id'] = listing[0]
			listing_dict['userid'] = listing[1]
			listing_dict['price'] = listing[2]
			listing_dict['listing_type'] = listing[3]
			listing_dict['postal_code'] = listing[4]
			listing_dict['status'] = listing[5]
			retval.append(listing_dict)
		self.write(json.dumps(retval))

class UpdateListingHandler(tornado.web.RequestHandler):
	def post(self):
		lid = self.get_argument('id',None)
		userid = self.get_argument('userid',None)
		price = self.get_argument('price',None)
		listing_type = self.get_argument('listing_type',None)
		postal_code = self.get_argument('postal_code',None)
		status = self.get_argument('status',None)
		execute_query("UPDATE listing SET userid=%s,price='%s',listing_type='%s',postal_code='%s',status='%s',updated_datetime=DateTime('now') where id=%s"%(userid,price,listing_type,postal_code,status,lid))
		self.write("")

class DeleteListingHandler(tornado.web.RequestHandler):
	def post(self):
		lid = self.get_argument('id',None)
		execute_query("DELETE FROM listing WHERE id = %s"%lid)
		self.write(json.dumps(dict(result="Listing Deleted")))

class NewUserHandler(tornado.web.RequestHandler):
	def post(self):
		name = self.get_argument('name',None)
		execute_query("INSERT INTO user (name,created_datetime,updated_datetime) VALUES ('%s',DateTime('now'),DateTime('now'))"%(name))
		self.write(json.dumps(dict(result="New User Created")))

class ListUserHandler(tornado.web.RequestHandler):
	def get(self):
		retval = []
		users = execute_query('SELECT * FROM user')
		for user in users:
			user_dict = dict()
			user_dict['id'] = user[0]
			user_dict['name'] = user[1]
			retval.append(user_dict)
		self.write(json.dumps(retval))

class UpdateUserHandler(tornado.web.RequestHandler):
	def post(self):
		uid = self.get_argument('id',None)
		name = self.get_argument('name',None)
		execute_query("UPDATE user SET name = '%s',updated_datetime=DateTime('now') WHERE id = %s"%(name,uid))
		self.write(json.dumps(dict(result="User Updated")))

class DeleteUserHandler(tornado.web.RequestHandler):
	def post(self):
		uid = self.get_argument('id',None)
		execute_query("DELETE FROM user WHERE id=%s"%uid)
		self.write(json.dumps(dict(result="User Deleted")))

def set_ping(ioloop, timeout):
    ioloop.add_timeout(timeout, lambda: set_ping(ioloop, timeout))

def main():
	try:
		#check database and create tables if doesn't exist
		checkDB()

		#setup the application with port 8888
		app = Application()
		app.listen(8888)
		ioloop = tornado.ioloop.IOLoop.instance()
		#prevent thread blocking with 2 seconds timeout
		set_ping(ioloop,datetime.timedelta(seconds=2))
		ioloop.start()
	except KeyboardInterrupt:
		tornado.ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    main()