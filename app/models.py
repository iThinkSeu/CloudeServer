
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import *
#from flask.ext.sqlalchemy import SQLALchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:0596@223.3.56.220:3306/dataserverble?charset=utf8"

db = SQLAlchemy(app)
migrage = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),unique = True)
	password = db.Column(db.String(32))
	token = db.Column(db.String(32))
	measuredatas = db.relationship('Measuredata',backref = 'instrument', lazy = 'dynamic')

	def add(self):
		try:
			tempuser = User.query.filter_by(username=self.username).first()
			if tempuser is None:
				db.session.add(self)
				db.session.commit()
				return 0
			else:
				return 1
		except Exception, e:
			print e
			db.session.rollback()
			return 2
	def isExisted(self):
		tempuser = User.query.filter_by(username=self.username,password=self.password).first()
		if tempuser is None:
			return 0
		else:
			return 1
	def isExistedusername(self):
		tempuser = User.query.filter_by(username = self.username).first()
		if tempuser is None:
			return 0
		else:
			return 1
	def publishmeasuredata(self,measuredata):
		try:
			measuredata.instrument = self
			db.session.add(measuredata)
			db.session.execute('set names utf8mb4')
			db.session.commit()
			return 0
		except Exception, e:
			print e
			db.session.rollback()
			return 2	

class Measuredata(db.Model):
	__tablename__ = "messuredatas"
	id = db.Column(db.Integer,primary_key = True)
	instrumentid = db.Column(db.Integer,db.ForeignKey('users.id'))
	datatype = db.Column(db.String(32))
	value = db.Column(db.Float)
	timestamp = db.Column(db.DateTime, default = datetime.now)
	def add(self):
		try:
			db.session.add(self)
			db.session.execute('set names utf8mb4')
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
			return 2

def getuserinformation(token):
	u=User.query.filter_by(token=token).first()
	return u 

def getTokeninformation(username):
	u=User.query.filter_by(username=username).first()
	return u 

if __name__ == '__main__':
	manager.run()







