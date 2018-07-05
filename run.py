from __future__ import print_function
import sys

from flask import Flask, jsonify, request, make_response, Response, flash
from flask_httpauth import HTTPBasicAuth
from flask import render_template, redirect, url_for
import random, time
from socket import gethostname
from flask_wtf import Form
from wtforms import StringField, TextField, TextAreaField, SubmitField, IntegerField
from wtforms import validators
from functools import wraps
import re, json
from flask_mail import Message, Mail

mail = Mail()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisishowyouremindme'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'gaoning777@gmail.com'
app.config["MAIL_PASSWORD"] = 'thisishowyouremindme'

auth = HTTPBasicAuth()
mail.init_app(app)

current_time_in_millis = lambda: int(round(time.time() * 1000))

resume_pdf_link = 'https://drive.google.com/open?id=0B2BrrDjIiyvmcWp5T194cy00UmM'

def check_auth(username, password):
	return username == 'rish' and password == 'kidinjp2'

def authenticate():
	return Response('Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

class Trip():
	m_name = ""
	m_text = ""
	m_dirname = ""

	def __init__(self, m_name, m_text, m_dirname):
		self.m_name = m_name
		self.m_text = m_text
		self.m_dirname = m_dirname

def add_trips():
	trips = []
	trip = Trip("2018 Graduation Trip", "Graduation trip during 2018 summer", "2018_graduation_trip")
	trips.append(trip)
	return trips

class ContactForm(Form):
	c_name = StringField('c_name', validators=[validators.required()])
	c_email = StringField('c_email', validators=[validators.required()])
	c_msg = TextAreaField('c_msg', validators=[validators.required()])

@app.route("/")
def root():
	return redirect(url_for('home'))

@app.route('/home')
def home():
	color = 'blue'
	title = "Ning Gao"
	titleback = "NG"
	subtitle = "Coder | Snowboarder | Climber | Hiker | Diver"
	subcontent = "Seattle, WA"
	#subcontent = "Me? 5+ apps on Google Plays, developer, creative thinker, problem solver. Undergrad in CS at DA-IICT- Junior year. I love keeping myself super busy, making things people will use, running, and playing football. FIFA 14, labradors, traveling, meeting new people :D"
	#subcontent = '<a href = "/aboutme" class="aref">Here\'s what I\'ve done in the past 2 years.</a>'
	return render_template('home.html',color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

#@app.route('/portfolio')
#def portfolio():

#	projectsFile = app.open_resource('static/projects.json')
#	projects = json.loads(projectsFile.read())['projects']
#
#	color = 'blue'
#	title = "Portfolio"
#	titleback = "CV"
#	subtitle = "A log of my perpetually increasing list of projects."
#	subcontent = "I could have made a fancy resume here, listing my work-exs, education history, but that's boring and we've got LinkedIn for that. This is a log of projects I've worked on indepenently, with organizations, and in my university."
#	return render_template('portfolio.html', projects = projects, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent, resume_pdf_link=resume_pdf_link)

@app.route('/code')
def code():
	color = 'green'
	title = "Code"
	titleback = "C"
	subtitle = "I love making things. And code allows me to do so in the laziest way possible. Laptop, bed, and some coffee."
	subcontent = "Coding has become a major part of my life. Majorly because code just makes life so much easier. Whether it's a mobile app, an arduino based room locker, or a simple shell script to boot your laptop faster. Oh, and partly because this is the only way I see myself making money to fund my bucketlist."
	return render_template('code.html', color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/weblog', defaults={'weblogno':None})
@app.route('/weblog/<weblogno>')
def weblog_ind(weblogno):

	return redirect("http://bhardwajrish.blogspot.in/");

	weblogs = None

	if weblogno == None:
		#weblogs = Weblog.query.all()
		weblogsFile = app.open_resource('static/weblogs.json')
		weblogs = json.loads(weblogsFile.read())['weblogs']

	elif weblogno == 'random-list':
		weblogsFile = app.open_resource('static/weblogs.json')
		weblogs = json.loads(weblogsFile.read())['weblogs']
		random.shuffle(weblogs, random.random)

	elif weblogno == 'favorites':
		weblogs = []
		weblogsFile = app.open_resource('static/weblogs.json')
		weblogs_temp = json.loads(weblogsFile.read())['weblogs']
		for w in weblogs_temp :
			if w['w_weight'] is 1 :
				weblogs.append(w)

	if weblogs is not None:
		# DISPLAY WEBLOG PAGE WITH SELECTED FILTERS
		color = 'dark'
		title = "WebLog"
		titleback = "W"
		subtitle = "A log of random musings, notes and things I find interesting"
		subcontent = "Most of my notes are short paragraphs (and not super long blogs that no one reads) on ideas and thoughts that cross my mind, fun observations about people and my surroundings, songs, travel, and sport."
		return render_template('weblog.html', weblogs = weblogs, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

	else:
		# DISPLAY INDIVIDUAL WEBLOG
		color = 'green'
		title = "WebLog"
		titleback = "W"
		subtitle = "A log of random musings, notes and things I find interesting"
		subcontent = "Most of my notes are short paragraphs (and not super long blogs that no one reads) on ideas and thoughts that cross my mind, fun observations about people and my surroundings, songs, travel, and sport."
		#weblog = Weblog.query.filter_by(id = weblogno).first()
		weblogsFile = app.open_resource('static/weblogs.json')
		weblogs = json.loads(weblogsFile.read())['weblogs']
		for w in weblogs:
			if w['id'] is int(weblogno):
				return render_template('weblog_ind.html', weblog = w, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)
		return redirect(url_for('page_not_found'))

@app.route('/travel', defaults={'link':None}, methods = ['GET', 'POST'])
@app.route('/travel/<link>', methods = ['GET', 'POST'])
def travel(link):
	trips = None
	if link is not None:
		return render_template(link + '/index.html')
	else:
		trips = add_trips()
		color = 'red'
		title = "Travel"
		titleback = "T"
		subtitle = "A Travel Log"
		subcontent = "To live is to enjoy the beauties that our nature has to offer."
		return render_template('travel.html', 	trips = trips, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
	form = ContactForm()
	color = 'orange'
	title = "Contact"
	titleback = "C"
	subtitle = "Let's get in touch"
	subcontent = "I love meeting new people and working on amazing things. If you'd like to work on a project with me, or get to know more about the work I do, do drop me a message. "

	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('contact.html', form = form, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)
		else:
			msg = Message("Great Website Man!", sender='pythonwalter@gmail.com', recipients=['gaoning777@gmail.com'])
			msg.body = """ From: %s <%s> %s """ % (form.c_name.data, form.c_email.data, form.c_msg.data)
			mail.send(msg)
			form = ContactForm()
			return render_template('contact.html', success=True, form = form, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

	return render_template('contact.html', form = form, color = color, title = title, titleback = titleback, subtitle = subtitle, subcontent = subcontent)

@app.route('/aboutme')
def aboutme():
	return render_template('aboutme.html', resume_pdf_link=resume_pdf_link)

#@app.route('/places')
#def places():
#	return render_template('places.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', color = 'yellow', title = "Hold On!", titleback = "404", subtitle = "This page does not exist."), 404

if __name__ == '__main__':
	db.create_all()
	app.run(host="127.0.0.1", port=8080, debug=True)
