import unittest
import app
from xml.dom import minidom

class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        # with app.app_context():
        #     app.init_db()

    def test_handle_sms_5_points_for_gryffindor(self):
        twilio_request =\
            {'AccountSid': u'ACfc502b87d78195dde44c7d952f835c7e',
             'ApiVersion': u'2010-04-01',
             'Body': u'5 points to gryffindor',
             'From': u'+16506309505',
             'FromCity': u'PALO ALTO',
             'FromCountry': u'US',
             'FromState': u'CA',
             'FromZip': u'94304',
             'MessageSid': u'SM7d046bca6423d27801e50f1a323152a6',
             'NumMedia': u'0',
             'NumSegments': u'1',
             'SmsMessageSid': u'SM7d046bca6423d27801e50f1a323152a6',
             'SmsSid': u'SM7d046bca6423d27801e50f1a323152a6',
             'SmsStatus': u'received',
             'To': u'+15107571733',
             'ToCity': u'SAN FRANCISCO',
             'ToCountry': u'US',
             'ToState': u'CA',
             'ToZip': u'94571'}

        response = self.app.post('/sms', data=twilio_request)

        xmldoc = minidom.parseString(response.data)
        message_element = xmldoc.getElementsByTagName('Message')
        message = message_element[0].childNodes[0].nodeValue

        self.assertEqual(message, 'Message managed! 5 points for gryffindor!')

    def test_handle_sms_block_isy_trying_to_award_himself_points(self):
        twilio_request =\
            {'Body': u'5 points to gryffindor',
             'From': u'+15107039410',
             'To': u'+15107571733'}

        response = self.app.post('/sms', data=twilio_request)

        xmldoc = minidom.parseString(response.data)
        message_element = xmldoc.getElementsByTagName('Message')
        message = message_element[0].childNodes[0].nodeValue

        self.assertEqual(message, 'Message managed! Nice try, Isy! 1 point for Slytherin!')


if __name__ == '__main__':
    unittest.main()