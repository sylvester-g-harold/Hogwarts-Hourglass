from flask import Flask
from flask import request
import logging
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World yo yo!'

@app.route('/pork')
def pork():
	return 'Human hair is underrepresented in government.'

@app.route('/sms', methods=['POST'])
def sms():
	app.logger.info(request.form)
	return 'blah'

if __name__ == '__main__':
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
