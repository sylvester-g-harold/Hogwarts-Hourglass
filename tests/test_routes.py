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

        self.assertEqual(message, 'Message managed! 5 points for Gryffindor!')

    def test_handle_sms_parse_the_for_from_case(self):
        twilio_request =\
            {'Body': u'1 point to Slytherin for electioneering trying to get double points from will for dishwashing',
             'From': u'+16502184081'}

        response = self.app.post('/sms', data=twilio_request)

        xmldoc = minidom.parseString(response.data)
        message_element = xmldoc.getElementsByTagName('Message')
        message = message_element[0].childNodes[0].nodeValue

        self.assertEqual(message, 'Message managed! 1 point for Slytherin!')

    def test_handle_sms_award_slytherin_point_via_basic_message(self):
        twilio_request =\
            {'Body': u'1 point to slytherin!',
             'From': u'+16502184081',
             'To': u'+15107571733'}
        response = self.app.post('/sms', data=twilio_request)

        xmldoc = minidom.parseString(response.data)
        message_element = xmldoc.getElementsByTagName('Message')
        message = message_element[0].childNodes[0].nodeValue

        self.assertEqual(message, 'Message managed! 1 point for Slytherin!')

    def test_handle_sms_award_slytherin_point_via_complex_message(self):
        twilio_request =\
            {'Body': u"1 point to slytherin for calling his sister's tickling harassment and calling his own tickling playing. not cool!",
             'From': u'+16502184081',
             'To': u'+15107571733'}
        response = self.app.post('/sms', data=twilio_request)

        xmldoc = minidom.parseString(response.data)
        message_element = xmldoc.getElementsByTagName('Message')
        message = message_element[0].childNodes[0].nodeValue

        self.assertEqual(message, 'Message managed! 1 point for Slytherin!')


    def test_handle_sms_block_isy_trying_to_award_himself_points(self):
        twilio_request =\
            {'Body': u'1 points from slytherin!',
             'From': u'+15107039410',
             'To': u'+15107571733'}
        response = self.app.post('/sms', data=twilio_request)

        xmldoc = minidom.parseString(response.data)
        message_element = xmldoc.getElementsByTagName('Message')
        message = message_element[0].childNodes[0].nodeValue

        self.assertEqual(message, 'Message managed! Nice try, Isy! 1 point for Slytherin!')


    def test_handle_possible_cheat_attempt(self):
        cheaty_mccheaterson_really_this_is_not_isy_trust_me_also_give_me_your_wallet = '+15107039410'
        point_value_change = {
            'house': 'gryffindor',
            'points': 5,
            'message': 'isy really, really deserves this',
            'professor_name': cheaty_mccheaterson_really_this_is_not_isy_trust_me_also_give_me_your_wallet
        }
        reply = app.handle_possible_cheat_attempt(point_value_change)

        self.assertEqual(point_value_change['house'], 'slytherin')
        self.assertEqual(point_value_change['points'], 1)
        self.assertTrue('CHEAT' in point_value_change['message'])

        self.assertEqual(reply, 'Message managed! Nice try, Isy! 1 point for Slytherin!')


if __name__ == '__main__':
    unittest.main()