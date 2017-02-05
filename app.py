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

@app.route('/dump_db', methods=['GET'])
def dump():
	db = get_db()
	cursor = db.cursor()
	cursor.execute("SELECT * FROM hourglass_points;")
	result_set = cursor.fetchall()
	msg = '--- FETCH FROM DB ---\n' + str(result_set)
	app.logger.info(msg)
	return str(result_set)

@app.route('/sms', methods=['POST'])
def sms(): 
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
	# Print the payload from the client.
	app.logger.info(request.form)
	professor_name = get_professor_name_from_phone_number(request.form['From'])
	body = request.form['Body']


	point_value_change = sms_parser.parse_point_value_change(body)


	if is_valid_point_value_change(point_value_change):
		app.logger.info('Storing: {}'.format(point_value_change))
		store_point_value_change(body, professor_name, point_value_change)
	else:
		app.logger.warning('Unable to parse {}'.format(body))

	return 'ok'


if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
