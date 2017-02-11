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
	str = str.lower()
	polarity = get_polarity(str)

	matches = re.search('(\d+)\s*points?\s+(to|from|for)', str)
	if matches:
		return int(matches.groups()[0]) * polarity
	else:
		return None

def get_house(str):
	str = str.lower()

	if 'gryffindor' in str:
		return 'Gryffindor'
	if 'hufflepuff' in str:
		return 'Hufflepuff'
	if 'ravenclaw' in str:
		return 'Ravenclaw'
	if 'slytherin' in str:
		return 'Slytherin'

	return None