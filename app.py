from flask import Flask
from flask import g
from flask import request
import logging
import os
import sms_parser

app = Flask(__name__)
cache = {
	'messages': []
}

@app.route('/')
def hello():
    return 'Hello World yo yo!'

@app.route('/pork')
def pork():
	return 'Human hair is underrepresented in government.'

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
	 ('Body', u'hey man'),
	 ('SmsSid', u'SM7d046bca6423d27801e50f1a323152a6'),
	 ('MessageSid', u'SM7d046bca6423d27801e50f1a323152a6'),
	 ('FromState', u'CA'),
	 ('ApiVersion', u'2010-04-01'),
	 ('FromCountry', u'US')]
	"""
	app.logger.info(request.form)

	body = request.form['Body']
	point_value_change = sms_parser.parse_point_value_change(body)
	if point_value_change['house'] and point_value_change['points']:
		app.logger.info('Parsed: {}'.format(point_value_change))
		cache['messages'].append(point_value_change)
		app.logger.info('Cache: {}'.format(cache))
	else:
		app.logger.warning('Unable to parse {}'.format(body))

	return 'ok'

if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
