# Summer Project For Fun :) #

from flask import Flask, redirect, render_template, request, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from urllib.request import urlopen

app = Flask(__name__)
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.permanent_session_lifetime = timedelta(days=5)


class REQUESTS2(db.Model):
	__tablename__ = 'Requests'
	_id = db.Column('id', db.Integer, primary_key=True) # id of post (will be used to find posts)
	title = db.Column('title', db.String(255)) # title of post # max 255 chars #
	description = db.Column('desc', db.String(2000)) # description of post # max 2000 chars #
	user = db.Column('user', db.String(255)) # username is 100 chars so there #
	img = db.Column('path', db.String(255)) # path shouldnt really be that long... #
	tag = db.Column('tag', db.String(255))

	def __init__(self, title, description, user, path, tag):
		self.title = title
		self.description = description
		self.user = user
		self.img = path
		self.tag = tag


class USER(db.Model):
	__tablename__ = '__Accounts__'
	_id = db.Column('id', db.Integer, primary_key=True) # user id
	username = db.Column('username', db.String(50)) # 50 char username
	password = db.Column('password', db.String(100)) # 100 char password
	verified = db.Column('verified', db.Boolean()) # if they are verified
	description = db.Column('description', db.String(1000)) # 1000 char max
	img = db.Column('path', db.String(255)) # path to user's image

	def __init__(self, un, pw, v, d, p):
		self.username = un
		self.password = pw
		self.verified = v
		self.description = d
		self.img = p


def isimage(url):
	formats = ['image/png', 'image/jpeg', 'image/gif', 'image/jpg']
	try:
		req = urlopen(url)
		meta = req.info()
	except:
		return False 
	return req.headers['content-type'] in formats


def getlist(arr, word):
	tbr = []
	for i in range(len(arr)):
		if word in arr[i].tag:
			tbr.append(arr[i])
	return tbr


@app.route('/', methods=['POST', 'GET'])
@app.route('/home/', methods=['POST', 'GET'])
def home():
	if request.method == 'POST':
		return redirect(url_for('create'))
	return render_template('home.html', reqs=REQUESTS2.query.all(), pagetitle='Home Page', pagepath='Home') 


@app.route('/design/', methods=['POST', 'GET'])
def design():
	if request.method == 'POST':
		return redirect(url_for('create'))

	REQUESTS2.query.all()
	sendme = getlist(REQUESTS2.query.all(), 'design')
	return render_template('home.html', reqs=sendme, pagetitle='Design Page', pagepath='Design')


@app.route('/software/', methods=['POST', 'GET'])
def software():
	if request.method == 'POST':
		return redirect(url_for('create'))

	REQUESTS2.query.all()
	sendme = getlist(REQUESTS2.query.all(), 'software')
	return render_template('home.html', reqs=sendme, pagetitle='Software Page', pagepath='Software')

@app.route('/discussion/', methods=['POST', 'GET'])
def discussion():
	if request.method == 'POST':
		return redirect(url_for('create'))

	REQUESTS2.query.all()
	sendme = getlist(REQUESTS2.query.all(), 'discussion')
	return render_template('home.html', reqs=sendme, pagetitle='Discussion Page', pagepath='Disc')


@app.route('/<postid>/')
def reqpage(postid):
	for req in REQUESTS2.query.all():
		print(req._id)
		if req._id == int(postid):
			return postid
	return 'lol'


@app.route('/delete/')
def delete():
	removelol = REQUESTS2.query.filter_by().delete()
	db.session.commit()
	return '<h1>Deleted</h1>'


@app.route('/create/', methods=['POST', 'GET'])
def create():
	returnme = 'Create Page'
	if request.method == 'POST':
		title = request.form['title']
		desc = request.form['desc']
		un = request.form['username']
		path = request.form['path']
		tags = ''
		try:
			des = request.form['design']
			tags += 'design  '
		except:
			pass
		try:
			sof = request.form['software']
			tags += 'software  '
		except:
			pass
		try:
			dis = request.form['discussion']
			tags += 'discussion  '
		except:
			pass

		if not un:
			un = 'anon'
		if path and not isimage(path):
			print('not image')
		
		newReq = REQUESTS2(title, desc, un, path, tags) 
		db.session.add(newReq)	
		db.session.commit()
		return redirect(url_for('home'))
	return render_template('create.html', display=returnme) 

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
