import re

def parse_point_value_change(str):
	house = get_house(str)
	points = get_points(str)
	result = {
		'house': house,
		'points': points
	}
	return result

def get_polarity(str):
	polarity = 1
	if 'from' in str:
		polarity = -1
	return polarity

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