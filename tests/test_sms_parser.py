import unittest
import sms_parser

class SmsParserTestCase(unittest.TestCase):
    """Tests Ror `sms_parser.py`."""

    def test_parse_point_value_change(self):
        input = '5 points for Gryffindor!'
        output = sms_parser.parse_point_value_change(input)
        expected = ('Gryffindor', 5)
        self.assertEqual(output, expected)

    def test_get_positive_single_digit_points(self):
        input = '5 points for Gryffindor!'
        output = sms_parser.get_points(input)
        self.assertEqual(output, 5)

    def test_get_positive_double_digit_points(self):
        input = '10 points for Gryffindor!'
        output = sms_parser.get_points(input)
        self.assertEqual(output, 10)

    def test_extra_from_does_not_go_negative(self):
        input = '1 point to Slytherin for electioneering trying to get double points from will for dishwashing'
        output = sms_parser.get_points(input)
        self.assertEqual(output, 1)

    def test_two_mentions_of_points(self):
        input = '1 point to Slytherin for fixing the 2 points bug'
        output = sms_parser.get_points(input)
        self.assertEqual(output, 1)        

    def test_two_mentions_of_points_in_inverted_order(self):
        input = 'for fixing the 2 points bug, 1 point to Slytherin '
        output = sms_parser.get_points(input)
        self.assertEqual(output, 1)        

    def test_get_negative_double_digit_points(self):
        input = '10 points from Gryffindor!'
        output = sms_parser.get_points(input)
        self.assertEqual(output, -10)

    def test_get_points_no_number(self):
        input = 'points from Gryffindor!'
        output = sms_parser.get_points(input)
        self.assertEqual(output, None)

    def test_get_house_gryffindor(self):
        input = '5 points for Gryffindor!'
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Gryffindor')

    def test_get_house_hufflepuff(self):
        input = '5 points for Hufflepuff!'
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Hufflepuff')

    def test_get_house_ravenclaw(self):
        input = '5 points for Ravenclaw!'
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Ravenclaw')

    def test_get_house_slytherin(self):
        input = '5 points for slytherin!'
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Slytherin')

    def test_get_house_with_mixed_case(self):
        input = '5 points for Hufflepuff!'
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Hufflepuff')

    def test_get_house_with_leading_padding(self):
        input = '    5 points for Slytherin!'
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Slytherin')

    def test_get_house_with_trailing_padding(self):
        input = '5 points for Slytherin!    '
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Slytherin')

    def test_get_house_with_stray_spaces_in_middle(self):
        input = '5 points for Slytherin!'
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Slytherin')

    def test_get_house_with_irrelevant_chars(self):
        input = '5 points Ror those stinking varmints over at slytherin?!!?##?#?!'
        output = sms_parser.get_house(input)
        self.assertEqual(output, 'Slytherin')


    # def test_parse(self):
    #   input = '5 points Ror Gryffindor!'
    #   output = sms_parser.parse(input)
    #   expected = 'gryffindor'
    #     self.assertEqual(output['house'], expected)

if __name__ == '__main__':
    unittest.main()