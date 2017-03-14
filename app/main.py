#-*- coding: UTF-8 -*- 
from flask import Flask
from flask import request,jsonify,json
from flask import render_template
from flask import redirect,url_for
from models import *
from wtforms import Form,TextField,PasswordField,validators
from hashmd5 import *
import string
import os, stat
from flask.ext.bootstrap import Bootstrap
from datetime import *
import re

app = Flask(__name__)
bootstrap=Bootstrap()
bootstrap.init_app(app)

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

@app.route("/applogin",methods=['POST'])
def applogin():
	try:
		username = request.json['username']
		password = request.json['password']
		u=User(username=username,password=password)
		if u.isExisted():
			state = 'successful'
			tmp = getTokeninformation(username)
			token = tmp.token
			id = tmp.id
			reason = ''
		else:
			id=''
			state = 'fail'
			token = 'None'
			reason = '用户名密码错误'
	except Exception, e:
		print "login error!!"
		print e
		state = 'fail'
		reason='服务器异常'
		token = 'None'
		id = ''

	response = jsonify({'id':id,
						'state':state,
						'username':username,
						'reason':reason,
						'token':token})
	#print state, reason
	return response


@app.route("/",methods=['GET','POST'])
def index():
	print "hi"
	#return "hello"
	#return redirect(url_for('static', filename='profile_small.jpg'), code=301)
	return render_template('index.html');

@app.route("/index",methods=['GET','POST'])
def indexmain():
	print "hi"
	#return "hello"
	#return redirect(url_for('static', filename='profile_small.jpg'), code=301)
	return render_template('indexMain.html')

@app.route("/postmeasuredata",methods=['GET','POST'])
def postmeasuredata():
	try:
		token = request.json['token']
		datatype = request.json.get('datatype','')
		value_string = request.json.get('value','')
		value = float(str(value_string))
		ErrorResult = request.json.get('ErrorResult','')
		VWRTHD = request.json.get('VWRTHD','')
		stand = request.json.get('stand','')
		up = request.json.get('up','')
		down = request.json.get('down','')
		instrumentID = request.json.get('instrumentID','ABCDEF')
		u = getinstrumentbyID(instrumentID)
		if u is not None:
			if(datatype in ['VDC','VAC','IDC','IAC']):
				tmpmeasure = Measuredata(datatype = datatype,value = value,separation=ErrorResult,VWRTHD=VWRTHD,stand=stand,up=up,down=down)
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


@app.route("/user/<name>",methods=['GET'])
def getname(name):
	print name;
	return "hello"+str(name);

@app.route('/getJsonData')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	timestamp = datetime.now()
	print timestamp
	state = "successful"
	reason = ''
	response = jsonify({'state':state,'reason':reason,'timestamp':timestamp,'data':20})
	return response
@app.route('/starttime',methods=['GET','POST'])
def starttime():
	state = "successful"
	reason = ""
	#start_time = "2017-06-16 15:40:29"
	start_time = request.args.get('latesttime',"2017-06-16 15:40:29")
	print start_time
	end_time = datetime.now()
	#datalist = get_data_from_starttime(start_time,end_time)
	datalist = get_data_up(start_time)
	result = []
	for tmp in datalist:
		output = {"dataid":tmp.id ,"datatype":tmp.datatype,"value":tmp.value,"separation":tmp.separation,"VWRTHD":tmp.VWRTHD,"stand":tmp.stand,"up":tmp.up,"down":tmp.down,"timestamp":str(tmp.timestamp)}
		result.append(output)
	response = jsonify({'state':state,'reason':reason,'result':result})
	return response

@app.route("/datainget",methods=['GET'])
def datainget():
	data = request.args.get('data','')
	dataArr = re.split(':|_|\n',data)
	print "receive data:"+data
	response = 'CAL:NOUPdate#'
	if(dataArr[0]=='CAL'):
		print "receive:CAL!"
		if(dataArr[1]=='VACV'):
			response = 'CAL:VACV 1:50.00:50.01#CAL:VACV 2:60.00:60.02#CAL:VACV 2E#'
		elif (dataArr[1]=='OK'):
			response = 'CAL:COMPlete#'
	elif (dataArr[0]=='MEA'):
		print "receive:MEA!"
		print dataArr
		datatype = dataArr[1]
		VAL = dataArr[2]
		VWRTHD = dataArr[4]
		ErrorResult = dataArr[8]
		up = dataArr[10]
		stand = dataArr[12]
		down = dataArr[14]
		value = float(str(VAL.rstrip('kV').rstrip('mA').rstrip('S')))
		instrumentID='ABCDEF'
		u = getinstrumentbyID(instrumentID)
		if u is not None:
			if(datatype in ['VDC','VAC','IDC','IAC']):
				tmpmeasure = Measuredata(datatype = datatype,value = value,separation=ErrorResult,VWRTHD=VWRTHD,stand=stand,up=up,down=down)
				u.publishmeasuredata(tmpmeasure)
				response = 'successful#'
			else:
				response = 'fail no this measure type#'				
		else:
			response = 'fail,no user#'
	else:
		response = 'no CAL or MEA type#'

	return response

@app.route("/get_web_history",methods=['GET','POST'])
def get_web_history():
	result = []
	token = request.args.get('token','')
	modelist = request.args.get('modelist','')
	starttime = request.args.get('starttime',"2017-06-16 15:40:29")
	endtime = request.args.get('endtime','')
	u = getuserinformation(token)
	if u is not None:	
		reason = ''
		state = 'successful'
		history_data_list = get_history_data(['VAC'],starttime,endtime)
		for tmp in history_data_list:
			state = "successful"
			output = {"dataid":tmp.id ,"datatype":tmp.datatype,"value":tmp.value,"timestamp":str(tmp.timestamp)}
			result.append(output)
	else:
		state = 'fail'
		reason = 'no user'

	response = jsonify({'state':state,'reason':reason,'result':result})
	return response
@app.route("/history_data",methods=['GET','POST'])
def history_data():
	
	result = []
	token = request.json['token']
	modelist = request.json.get('modelist','')
	starttime = request.json.get('starttime','')
	endtime = request.json.get('endtime','')
	u = getuserinformation(token)
	if u is not None:	
		reason = ''
		state = 'successful'
		history_data_list = get_history_data(['VAC'],starttime,endtime)
		for tmp in history_data_list:
			state = "successful"
			output = {"dataid":tmp.id ,"datatype":tmp.datatype,"value":tmp.value,"timestamp":str(tmp.timestamp)}
			result.append(output)
	else:
		state = 'fail'
		reason = 'no user'

	response = jsonify({'state':state,'reason':reason,'result':result})
	return response
#历史数据	
@app.route("/history",methods=['GET','POST'])
def history():
	return render_template('manageHistoryData.html')

@app.route("/report",methods=['GET','POST'])
def report():
	return render_template('manageReport.html')

#管理界面
@app.route("/manage",methods=['GET','POST'])
def manage():
	return render_template('manageIndex.html')

#管理界面2
@app.route("/indicator",methods=['GET','POST'])
def indicator():
	start_time = "2017-07-9 15:40:29"
	print start_time
	#print history_data_list;
	return render_template('indicator.html')

#管理界面2
@app.route("/user",methods=['GET','POST'])
def manageuser():
	return render_template('manageUser.html')


#管理界面2
@app.route("/revise",methods=['GET','POST'])
def managerevise():
	revises = revise.query.all()
	return render_template('manageRevise.html',revises=revises)

if __name__ == '__main__':
	app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',4020)),debug = True)

	