
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
#from flask.ext.sqlalchemy import SQLALchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:root@localhost:3306/dataserverble?charset=utf8"

db = SQLAlchemy(app)
migrage = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),unique = True)
	password = db.Column(db.String(32))
	def __init__(self,username,password):
		self.username = username
		self.password = password
	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
			return self.id_
		except Exception, e:
			db.session.rollback()
			return e
		finally:
			return 0

	def isExisted(self):
		tempuser = User.query.filter_by(username=self.username,password=self.password).first()
		if tempuser is None:
			return 0
		else:
			return 1



if __name__ == '__main__':
	manager.run()







