from flask import Flask,render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt
from fuzzywuzzy import fuzz

app= Flask(__name__)

#config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='prajnabhat'
app.config['MYSQL_DB']='haxkathon'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#initialize
mysql=MySQL(app)

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/questions')
def questions():
	cur=mysql.connection.cursor()
	result = cur.execute("SELECT * FROM quiz")
	questions = cur.fetchall()
	if result>0:
		return render_template('questions.html', questions=questions)
	else:
		msg="no questions in the database"
		return render_template('home.html', msg=msg)
	cur.close()

class AnswerForm(Form):
	id1 = IntegerField('id1')

@app.route('/answers', methods=['GET', 'POST'])
def answers():
	form = AnswerForm(request.form)
	if request.method =='POST':
		id1= form.id1.data
		cur = mysql.connection.cursor()
		result = cur.execute("SELECT * FROM  quiz WHERE qid= %s", [id1])
		if result >0:
			data = cur.fetchone()
			i = data['qid']
			ques=data['ques']
			a=data['a']
			b=data['b']
			c=data['c']
			d=data['d']
			if id1 == i:
				session['logged_in']=True
				session['i']=i
				session['ques']=ques
				session['a']=a
				session['b']=b
				session['c']=c
				session['d']=d
				app.logger.info("match")
				return redirect(url_for('dashboard'))
			else:
				app.logger.info("no match")
				flash("invalid id")
				return render_template('regsiter.html', form=form)
			cur.close()
		else:
			app.logger.info("invalid")
			error="not exists"
			return render_template('answers.html', error=error)

	return render_template('answers.html', form=form)

def convert(lst):
    return ([i for item in lst for i in item.split()])

class DashBoaed(Form):
	ans=StringField('ans')

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
	no_p=""
	punc ='''!()-[]{};:'"\,<>./?@#$%^&*_~'''
	conj = ['and','the','an','but','is','are','in','for','to','so','of']
	form = DashBoaed(request.form)
	if request.method =='POST':
		id1=session.get('i')
		ans=form.ans.data
		for char in ans:
			if char not in punc:
				no_p = no_p + char
		cur=mysql.connection.cursor()
		resu = cur.execute("SELECT * FROM answers WHERE qid= %s", [id1])
		if resu == 1:
			app.logger.info("inside resu=1")
			dat = cur.fetchone()
			lisdat = dat["answers"]
			c = fuzz.token_set_ratio(lisdat,no_p)
			#d = fuzz.token_set_ratio(listat,)
			app.logger.info(c)
			if c>=50:
				flash("Duplicate")
			else:
				flash("submitted")
				cur.execute("INSERT INTO answers(a_id,answers,qid) VALUES(%s,%s,%s)",(None,ans,id1))
			mysql.connection.commit()
		elif resu>1:
			count=0
			app.logger.info("inside resu>1")
			dat = cur.fetchall()
			for row in dat:
				dno_p=""
				dli = row["answers"]
				for char in dli:
					if char not in punc:
						dno_p = dno_p + char
				m= fuzz.token_set_ratio(no_p,dno_p)
				app.logger.info(m)
				if m >=70:
					count+=1
		if count>0:
			flash("Duplicate")
		else:
			flash("submitted")
			cur.execute("INSERT INTO answers(a_id,answers,qid) VALUES(%s,%s,%s)",(None,ans,id1))
			mysql.connection.commit()
		cur.close()
		return redirect(url_for('answers'))
	return render_template('dashboard.html')


if __name__=='__main__':
	app.secret_key='secret123'
	app.run(debug=True)
