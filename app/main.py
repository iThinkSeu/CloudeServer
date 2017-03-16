#-*- coding: UTF-8 -*- 
from flask import Flask
from flask import request,jsonify,json
from flask import render_template
from flask import redirect,url_for,flash
from models import *
from wtforms import Form,TextField,PasswordField,validators
from hashmd5 import *
import string
import os, stat
from flask.ext.bootstrap import Bootstrap
from datetime import *
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.secret_key = 'some_secret'
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
		ErrorResult = request.json.get('separation','')
		VWRTHD = request.json.get('VWRTHD','')
		stand = request.json.get('stand','')
		up = request.json.get('up','')
		down = request.json.get('down','')
		instrumentID = request.json.get('ID','ABCDEF')
		fre = request.json.get("fre","--")
		u = getinstrumentbyID(instrumentID)
		if u is not None:
			if(datatype in ['VDC','VAC','IDC','IAC','VAC-T','VDC-T']):
				tmpmeasure = Measuredata(datatype = datatype,value = value,separation=ErrorResult,VWRTHD=VWRTHD,stand=stand,up=up,down=down,fre=fre)
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
	instrumentID = dataArr[1]
	if(dataArr[2]=='CAL'):
		revisetype = dataArr[3]
		print "receive:CAL!"+revisetype
		if(dataArr[3]!='OK'):
			calrevises = revise.query.filter_by(instrumentID=instrumentID,type=revisetype,flag=True).all()
			calstr = ''
			print "CAL!"+revisetype
			num = 0;
			update = False
			for rev in calrevises:
				update = True
				num = num+1;
				print "CAL! in num="
				print num
				calstr = calstr+"CAL:"+revisetype+" "+str(num)+":"+str(rev.realvalue)+":"+str(rev.measurevalue)+"#"
				rev.flag=False
				rev.add()
			if(update==True):
				calstr = calstr+"CAL:"+revisetype+" "+str(num)+"E#"
				response = calstr
			else:
				response = 'CAL:NOUPdate#'
			return response
		elif (dataArr[3]=='OK'):
			response = 'CAL:COMPlete#'
	elif (dataArr[2]=='MEA'):
		print "receive:MEA!"
		print dataArr
		ID = dataArr[1]
		datatype = dataArr[3]
		VAL = dataArr[4]
		ErrorResult = dataArr[6]
		up = float(str(dataArr[8].rstrip('kV').rstrip('mA').rstrip('S')))
		stand = float(str(dataArr[10].rstrip('kV').rstrip('mA').rstrip('S')))
		down = float(str(dataArr[12].rstrip('kV').rstrip('mA').rstrip('S')))
		if(dataArr[3]==u'VAC'or dataArr[3]==u'IAC'):
			Freq = dataArr[14]
		else:
			Freq = "--"
		if(datatype==u"VAC"):
			VWRTHD = dataArr[16]
		elif(datatype==u"VDC"):
			VWRTHD = dataArr[14]
		else:
			VWRTHD = "--"
		value = float(str(VAL.rstrip('kV').rstrip('mA').rstrip('S')))
		instrumentID='001'
		u = getinstrumentbyID(instrumentID)
		if u is not None:
			if(datatype in ['VDC','VAC','IDC','IAC']):
				tmpmeasure = Measuredata(datatype = datatype,value = value,separation=ErrorResult,VWRTHD=VWRTHD,stand=stand,up=up,down=down,fre = Freq)
				u.publishmeasuredata(tmpmeasure)
				response = ''
			else:
				response = 'fail no this measure type#'				
		else:
			response = 'fail,no instrumentID#'
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
	print "starttime="+starttime
	print "endtime="+endtime
	u = getuserinformation(token)
	if u is not None:	
		reason = ''
		state = 'successful'
		history_data_list = get_history_data(['VAC','VDC'],starttime,endtime)
		for tmp in history_data_list:
			state = "successful"
			output = {"dataid":tmp.id ,"datatype":tmp.datatype,"value":tmp.value,"separation":tmp.separation,"timestamp":str(tmp.timestamp)}
			result.append(output)
	else:
		state = 'fail'
		reason = 'no user'

	response = jsonify({'state':state,'reason':reason,'result':result})
	return response
@app.route("/getrevisetable",methods=['GET','POST'])
def getrevisetable():
	result = []
	token = request.args.get('token','')
	instrumentID = request.args.get('instrumentID','ABCDEF')
	revisetype = request.args.get('revisetype',"VACV")
	print "instrumentID="+instrumentID
	print "revisetype="+revisetype
	u = getuserinformation(token)
	if u is not None:	
		reason = ''
		state = 'successful'
		revisetablelist = getrevisetabledb(instrumentID,revisetype)
		for tmp in revisetablelist:
			state = "successful"
			output = {"instrumentID":tmp.instrumentID ,"id":tmp.id,"revisetype":tmp.type,"realvalue":tmp.realvalue,"measurevalue":tmp.measurevalue,"flag":tmp.flag}
			result.append(output)
	else:
		state = 'fail'
		reason = 'no user'
	response = jsonify({'state':state,'reason':reason,'result':result})
	return response
@app.route("/deleterevise",methods=['GET','POST'])
def deleterevise():
	if request.method=="POST":
		reviseid = request.values.get('id',None)
		print reviseid
		if reviseid:
			rs = revise.query.filter(revise.id==reviseid).first()
			if rs:
				db.session.delete(rs)
				db.session.commit()
	return "successful"

@app.route("/addrevise",methods=['GET','POST'])
def addrevise():
	response = "添加成功"
	if request.method=="POST":
		revisetype = request.values.get('revisetype',None)
		realvalue = request.values.get('realvalue','')
		measurevalue = request.values.get('measurevalue','')
		instrumentID = request.values.get('instrumentID',"001")
		print revisetype
		if revisetype:
			rs = revise(instrumentID=instrumentID,type=revisetype,realvalue=realvalue,measurevalue=measurevalue,flag=True)
			state = rs.add()
			if(state==1): 
				response = "已经存在"
			elif(state==2):
				response = "dberror"
	return response

@app.route("/submitrevise",methods=['GET','POST'])
def submitrevise():
	response = "设置成功"
	if request.method=="POST":
		data = request.values.get('data','')
		revisetype = request.values.get('revisetype','VACV')
		instrumentID = request.values.get('instrumentID',"001")
		print "data!!!!!!!!!!!!!!!!!"
		print data
		dataArr = re.split(':|\n',data)
		drs = revise.query.filter_by(instrumentID=instrumentID,type=revisetype).all();
		for tmp in drs:
			print "delete"
			db.session.delete(tmp)	
			db.session.commit()
		print "len="
		print len(dataArr)
		for i in range(1,len(dataArr),3):
			print i
			realvalue = dataArr[i]
			measurevalue = dataArr[i+1]
			print realvalue+":"+measurevalue
			rs = revise(instrumentID=instrumentID,type=revisetype,realvalue=realvalue,measurevalue=measurevalue,flag=1)
			print "flag!!!!!"
			print rs.flag
			rs.flag = True
			print rs.add()
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
	#if request.method=='POST':
	#	instrumentID = request.values.get('instrumentID','ABCDEF')
	#	revisetype = request.values.get('revisetype',"VACV")
	#	print revisetype
	#	print instrumentID
	#	rs = revise.query.filter_by(instrumentID=instrumentID,type=revisetype).all()
	#	print rs
	#	return render_template('manageRevise.html',revises=rs);
	rs = revise.query.filter_by(instrumentID="ABCDEF",type="VACV").all();
	return render_template('manageRevise.html',revises=rs)

@app.route("/getrevisetable",methods=['GET','POST'])
def getrevise():
	revises = revise.query.all()
	return "test"



if __name__ == '__main__':
	app.run(host=os.getenv('IP','0.0.0.0'),port=int(os.getenv('PORT',4020)),debug = True)

	