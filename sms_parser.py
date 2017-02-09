import re

def parse_point_value_change(str):
	house = get_house(str)
	points = get_points(str)
	return house, points

def get_polarity(str):
	matches = re.search('(to|for)\s+(slytherin|hufflepuff|ravenclaw|gryffindor)', str)
	if matches:
		return 1

	matches = re.search('from\s+(slytherin|hufflepuff|ravenclaw|gryffindor)', str)
	if matches:
		return -1

	return None

def get_points(str):
	polarity = get_polarity(str)

	matches = re.search('\d+', str)
	if matches:
		return int(matches.group(0)) * polarity
	else:
		return None

def get_house(str):
	str = str.lower()

	if 'gryffindor' in str:
		return 'gryffindor'
	if 'hufflepuff' in str:
		return 'hufflepuff'
	if 'ravenclaw' in str:
		return 'ravenclaw'
	if 'slytherin' in str:
		return 'slytherin'

	return None