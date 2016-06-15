#-*- coding: UTF-8 -*- 
from flask import Flask
from flask import request,jsonify,json
from flask import render_template
from flask import redirect,url_for
from models import *
from wtforms import Form,TextField,PasswordField,validators
from hashmd5 import *
import string

app = Flask(__name__)

class LoginForm(Form):
	username = TextField("username",[validators.Required()])
	password = PasswordField("password",[validators.Required()])


@app.route("/register",methods=['GET','POST'])
def register():
	myForm = LoginForm(request.form)
	if request.method=='POST':
		username = myForm.username.data
		password = myForm.password.data
		token = ''
		id = ''
		temp = checkName(username)
		if temp==False:		
			response = jsonify({
								'id':'',
								'state':'fail',
								'reason':'用户名不能包含中文且至少要两个字母',
								'token':'chinese'})
			return response
		token= hashToken(username,password)
		u=User(username=username,password=password,token=token)
		if u.isExistedusername() == 0:
			##未完成，加code验证码判断相关逻辑
			u.add()
			state = 'successful'
			reason = ''
			token = hashToken(username,password)
			id = getuserinformation(token).id
		else:
			state = 'fail'
			reason = '用户名已被注册'
			token = 'Haveresiger'
			id=''
		response = jsonify({'state':state,'reason':reason,'token':token,'id':id})
		return response
		#return "register sucessful"
	return render_template('index.html',form = myForm)

@app.route("/login",methods=['GET','POST'])
def login():
	myForm = LoginForm(request.form)
	if request.method=='POST':
		u=User(myForm.username.data,myForm.password.data)
		if (u.isExisted()):
			return "login sucessful"
		else:
			return "Login Failed"
	return render_template('index.html',form=myForm)

@app.route("/",methods=['GET','POST'])
def index():
	print "hi"
	#return "hello"
	#return redirect(url_for('static', filename='profile_small.jpg'), code=301)
	return render_template('managebase.html',userinfo = "zrr")


@app.route("/postmeasuredata",methods=['GET','POST'])
def postmeasuredata():
	try:
		token = request.json['token']
		datatype = request.json.get('datatype','')
		value_string = request.json.get('value','')
		value = float(str(value_string))
		u = getuserinformation(token)
		if u is not None:
			if(datatype in ['VDC','VAC','IDC','IAC']):
				tmpmeasure = Measuredata(datatype = datatype,value = value)
				u.publishmeasuredata(tmpmeasure)
				state = 'successful'
				reason = ''
			else:
				state = 'fail'
				reason = 'no this measure type'				
		else:
			state = 'fail'
			reason = 'no user'
	except Exception, e:	
		print e
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,
						'reason':reason})
	return response

@app.route("/appregister",methods=['POST'])
def appregister():
	try:
		username = request.json.get('username','')
		password = request.json.get('password','')
		token = ''
		id = ''
		temp = checkName(username)
		if temp==False:		
			response = jsonify({
								'id':'',
								'state':'fail',
								'reason':'用户名不能包含中文且至少要两个字母',
								'token':'chinese'})
			return response
		token= hashToken(username,password)
		u=User(username=username,password=password,token=token)
		if u.isExistedusername() == 0:
			##未完成，加code验证码判断相关逻辑
			u.add()
			state = 'successful'
			reason = ''
			token = hashToken(username,password)
			id = getuserinformation(token).id
		else:
			state = 'fail'
			reason = '用户名已被注册'
			token = 'Haveresiger'
			id=''
	
	except Exception, e:	
		print e
		state = 'fail'
		reason = 'exception'

	response = jsonify({'state':state,'reason':reason,'token':token,'id':id})
	return response


if __name__ == '__main__':
	app.run(port=8080,debug=True)
