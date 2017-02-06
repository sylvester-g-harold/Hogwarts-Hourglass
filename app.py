from flask import Flask
from flask import g
from flask import request
import logging
import os
import sms_parser
import psycopg2
import urlparse

urlparse.uses_netloc.append('postgres')
app = Flask(__name__)

def connect_db():
	conn = None
	if os.environ.get('DATABASE_URL'):
		url = urlparse.urlparse(os.environ['DATABASE_URL'])

		conn = psycopg2.connect(
		    database=url.path[1:],
		    user=url.username,
		    password=url.password,
		    host=url.hostname,
		    port=url.port
		)
	else:
		conn = psycopg2.connect(
			database='hoggyhoggywartswarts',
			user='isy',
			password='')
	return conn

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = connect_db()
    return g.postgres_db

@app.route('/')
def hello():
    return 'Hello World yo yo!'

@app.route('/pork')
def pork():
	return 'Human hair is underrepresented in government.'

def is_valid_point_value_change(point_value_change):
	return point_value_change['house'] and point_value_change['points']

def store_point_value_change(message, professor_name, point_value_change):
	"""
	Sample working SQL insert statement
	insert into hourglass_points 
		(house, points, professor_name, message)
		values ('gryffindor', -3, 'floyd', '3 points from gryffindor! good job bu!');

	Sample `point_value_change` value:
	{
	    'house': 'gryffindor',
	    'points': 5
    }	
	"""
	house = point_value_change['house']
	points = point_value_change['points']

	db = get_db()
	cursor = db.cursor()

	statement = ('insert into hourglass_points '
				 '(house, points, professor_name, message)'
				 'values (\'{}\', {}, \'{}\', \'{}\');'
				).format(house, points, professor_name, message)

	cursor.execute(statement)
	db.commit()

	app.logger.info('Inserted values into db: {}, {}, {}, {}'
		.format(house, points, professor_name, message))

def get_professor_name_from_phone_number(phone_number):
	# TODO: actually look up the name from this phone number
	return phone_number

@app.route('/log', methods=['GET'])
def handle_log():
	db = get_db()
	cursor = db.cursor()
	cursor.execute("SELECT * FROM hourglass_points;")
	result_set = cursor.fetchall()
	msg = '--- FETCH FROM DB ---\n' + str(result_set)
	app.logger.info(msg)

	# TODO: factor out in helper function... #get_totals()
	totals = {
		'gryffindor': 0, #gryffindor
		'hufflepuff': 0,
		'ravenclaw': 0,
		'slytherin': 0
	}
	for row in result_set:
		house = row[1].lower()
		points = int(row[2])
		if totals.get('gryffindor') is not None:
			totals[house] += points
		else:
			app.logger.warning('Could not find house name: {}'.format(house))

	totals_html = (
			'<style>'
			'table {{ border-collapse:collapse; }}'
			'th, td {{ border: 1px solid black; padding: 5px; text-align: center }}'
			'</style>'

			'<table>'
			'<tr><th colspan="4"><h1>TOTALS</h1></th></tr>'
			'<tr>'
			'<th>Gryffindor</th>'
			'<th>Hufflepuff</th>'
			'<th>Ravenclaw</th>'
			'<th>Slytherin</th>'
			'</tr>'
			'<tr>'
			'<td>{}</td>'
			'<td>{}</td>'
			'<td>{}</td>'
			'<td>{}</td>'
			'</tr>'
			'</table>'
			'<br>'
			'<br>'
			'<br>'
	).format(
		totals['gryffindor'],
		totals['hufflepuff'],
		totals['ravenclaw'],
		totals['slytherin'])

	#TODO factor out to helper function #get_details_html()
	details_headers = (
		'<tr>'
		'<th>House</th>'
		'<th>Points</th>'
		'<th>Professor</th>'
		'<th>Message</th>'
		'<tr>'
	)

	details_body = ''
	for row in result_set:
		house = row[1]
		points = row[2]
		professor_name = row[3]
		message = row[4]

		details_body += (
			'<tr>'
			'<td>{}</td>'
			'<td>{}</td>'
			'<td>{}</td>'
			'<td>{}</td>'
			'<tr>'
		).format(
			house,
			points,
			professor_name,
			message
		)

	details_html = (
		'<table>'
		'<tr><th colspan="4"><h1>Detailed Points Log</h1></th></tr>'
		'{}'
		'{}'
		'</table>'
	).format(details_headers, details_body)

	return totals_html + details_html

@app.route('/sms', methods=['POST'])
def handle_sms(): 
	"""
	Sample payload from Twilio:
	[('ToCountry', u'US'),
	 ('From', u'+16506309505'),
	 ('SmsStatus', u'received'),
	 ('NumMedia', u'0'),
	 ('ToState', u'CA'),
	 ('FromCity', u'PALO ALTO'),
	 ('SmsMessageSid', u'SM7d046bca6423d27801e50f1a323152a6'),
	 ('ToCity', u'SAN FRANCISCO'),
	 ('NumSegments', u'1'),
	 ('FromZip', u'94304'),
	 ('To', u'+15107571733'),
	 ('AccountSid', u'ACfc502b87d78195dde44c7d952f835c7e'),
	 ('ToZip', u'94571'),
	 ('Body', u'5 points to gryffindor'),
	 ('SmsSid', u'SM7d046bca6423d27801e50f1a323152a6'),
	 ('MessageSid', u'SM7d046bca6423d27801e50f1a323152a6'),
	 ('FromState', u'CA'),
	 ('ApiVersion', u'2010-04-01'),
	 ('FromCountry', u'US')]
	"""
	# Print the payload from the client
	app.logger.info(request.form)
	professor_name = get_professor_name_from_phone_number(request.form['From'])
	body = request.form['Body']


	point_value_change = sms_parser.parse_point_value_change(body)


	custom_reply = ''
	if is_valid_point_value_change(point_value_change):
		was_cheating_attempt = False
		if professor_name == '+15107039410':
			point_value_change['house'] = 'slytherin'
			point_value_change['points'] = '1'
			was_cheating_attempt = True

		store_point_value_change(body, professor_name, point_value_change)

		points = point_value_change['points']
		house = point_value_change['house']

		if was_cheating_attempt:
			custom_reply = 'Message managed! Nice try, Isy! 1 point for Slytherin!'
		else:
			custom_reply = 'Message managed! {} points for {}!'.format(points, house)
		app.logger.info(custom_reply)

	else:
		custom_reply = 'Unable to parse {}'.format(body)
		app.logger.warning(custom_reply)

	twiml_response = (
		'<?xml version="1.0" encoding="UTF-8"?>'
		'<Response>'
		'<Message>{}</Message>'
		'</Response>'
	).format(custom_reply)

	return twiml_response


if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
