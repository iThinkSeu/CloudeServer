# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import *
from sqlalchemy import or_
from sqlalchemy import and_

#from flask.ext.sqlalchemy import SQLALchemy

#app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:0596@223.3.56.220:3306/dataserverble?charset=utf8"
#app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:root@127.0.0.1:3306/dataserverble?charset=utf8"
#app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:SEUqianshou2015@218.244.147.240:3306/dataserverble?charset=utf8"
"""
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
"""
from dbSetting import create_app,db,sqlurl
"""
if __name__ == '__main__':
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI']=sqlurl
	db.init_app(app)
	migrage = Migrate(app,db)
	manager = Manager(app)
	manager.add_command('db',MigrateCommand)
"""
class manageinstrument(db.Model):
	__tablename__ = 'manageinstruments'
	id = db.Column(db.Integer, primary_key = True)
	userid = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
	instrumentid = db.Column(db.Integer, db.ForeignKey('instruments.id'), primary_key = True)
	timestamp = db.Column(db.DateTime,default = datetime.now)
	def add(self):
		try:
			db.session.add(self)
			db.session.commit()
		except Exception, e:
			print e
			db.session.rollback()
			return 2
			
class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(32),unique = True)
	password = db.Column(db.String(32))
	token = db.Column(db.String(32))
	#manageinstruments的外键，该用户管理了哪些仪器
	manageinstruments = db.relationship('manageinstrument', foreign_keys = [manageinstrument.userid], backref = db.backref('manageuser', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')

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
	def manageinstrument(self,instrument):
		try:
			lp = self.manageinstruments.filter_by(instrumentid = instrument.id).first()
			if lp is None:
				lp = manageinstrument(manageuser = self, managewhatinstrument = instrument)
				db.session.add(lp)
				db.session.commit()
				return 0
			else:
				return 1
		except Exception, e:
			print e
			db.session.rollback()
			return 2	

class instrument(db.Model):
	__tablename__ = "instruments"
	id = db.Column(db.Integer,primary_key=True)
	instrumentID = db.Column(db.String(64),unique = True)
	password = db.Column(db.String(32))
	timestamp = db.Column(db.DateTime, default = datetime.now)
	measuredatas = db.relationship('Measuredata',backref = 'instrument', lazy = 'dynamic')
	savedatas = db.relationship('savedata',backref = 'instrument', lazy = 'dynamic')

	#管理这个仪器的所有帐号用户
	manageusers = db.relationship('manageinstrument', foreign_keys = [manageinstrument.instrumentid], backref = db.backref('managewhatinstrument', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')
	def add(self):
		try:
			temp = instrument.query.filter_by(instrumentID=self.instrumentID).first()
			if temp is None:
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
		temp = instrument.query.filter_by(instrumentID=self.instrumentID,password=self.password).first()
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
	def publishsavedata(self,savedata):
		try:
			savedata.instrument = self
			db.session.add(savedata)
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
	instrumentID = db.Column(db.String(32),db.ForeignKey('instruments.instrumentID'))
	datatype = db.Column(db.String(32))
	value = db.Column(db.Float)
	separation = db.Column(db.String(32))
	VWRTHD = db.Column(db.String(32))
	stand = db.Column(db.Float)
	up = db.Column(db.Float)
	down = db.Column(db.Float)
	fre = db.Column(db.String(32))
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
class savedata(db.Model):
	__tablename__ = "savedatas"
	id = db.Column(db.Integer,primary_key = True)
	instrumentID = db.Column(db.String(32),db.ForeignKey('instruments.instrumentID'))
	datatype = db.Column(db.String(32))
	value = db.Column(db.String(32))
	separation = db.Column(db.String(32))
	VWRTHD = db.Column(db.String(32))
	stand = db.Column(db.String(32))
	up = db.Column(db.String(32))
	down = db.Column(db.String(32))
	fre = db.Column(db.String(32))
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


class revise(db.Model):
	"""docstring for revises"""
	__tablename__ = "revises"
	id = db.Column(db.Integer,primary_key=True)
	instrumentID = db.Column(db.String(32))
	type = db.Column(db.String(32))
	realvalue = db.Column(db.Float)
	measurevalue = db.Column(db.Float)
	flag = db.Column(db.Boolean)
	def add(self):
		try:
			tempuser = revise.query.filter_by(instrumentID=self.instrumentID,type = self.type,realvalue=self.realvalue).first()
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
	def addpwd(self):
		try:
			db.session.add(self)
			db.session.commit()
			return 0
		except Exception, e:
			print e
			db.session.rollback()
			return 2

def getuserinformation(token):
	u=User.query.filter_by(token=token).first()
	return u 
def getinstrumentbyID(instrumentID):
	u=instrument.query.filter_by(instrumentID=instrumentID).first()
	return u 

def getTokeninformation(username):
	u=User.query.filter_by(username=username).first()
	return u 

def get_history_data(typelist,start_time,end_time):
	a = savedata.query.filter(savedata.datatype.in_(typelist)).filter(savedata.timestamp.between(start_time,end_time)).order_by(savedata.timestamp.desc()).all()
	#a = Measuredata.query.filter(Measuredata.datatype.in_(typelist)).order_by(Measuredata.timestamp.desc()).all()
	return a 
def get_data_from_starttime(start_time,end_time):
	a = Measuredata.query.filter(Measuredata.timestamp.between(start_time,end_time)).order_by(Measuredata.timestamp.asc()).all()
	return a
def get_data_up(instrumentID,starttime):
	a = Measuredata.query.filter_by(instrumentID=instrumentID).filter(Measuredata.timestamp>starttime).all()
	return a
def get_savedata_up(instrumentID,starttime):
	a = savedata.query.filter_by(instrumentID=instrumentID).filter(savedata.timestamp>starttime).all()
	return a
def getrevisetabledb(instrumentID,revisetype):
	a = revise.query.filter_by(instrumentID=instrumentID,type=revisetype).order_by(revise.realvalue.asc()).all()
	return a	 
if __name__ == '__main__':
	manager.run()







