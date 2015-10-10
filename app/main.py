from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from models import *
from wtforms import Form,TextField,PasswordField,validators

app = Flask(__name__)

class LoginForm(Form):
	username = TextField("username",[validators.Required()])
	password = PasswordField("password",[validators.Required()])


@app.route("/register",methods=['GET','POST'])
def register():
	myForm = LoginForm(request.form)
	if request.method=='POST':
		u=User(myForm.username.data,myForm.password.data)
		u.add()
		return "register sucessful"
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


if __name__ == '__main__':
	app.run(port=5000)
