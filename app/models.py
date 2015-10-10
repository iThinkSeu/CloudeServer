
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from flask.ext.sqlalchemy import SQLALchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:mysql_HGR@210.73.154.11:3306/flasktestdb"

db = SQLAlchemy(app)

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









