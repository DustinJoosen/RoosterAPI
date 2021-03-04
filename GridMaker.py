import requests
import math
from bs4 import BeautifulSoup
from Lesson import Lesson

rowspans = {}


# Will be used in later versions, but for now it is locally saved to keep a stable input
def getSoup():
	url = "https://rooster.horizoncollege.nl/rstr/ECO/HRN/Roosters/09/c/c00051.htm"

	response = requests.get(url)
	soup = BeautifulSoup(response.content, 'html.parser')

	return soup


def getTables():
	soup = getSoup()
	main_table = soup.find("table", {"border": 3, "rules": "all"})

	#each table, is one cell in the main table
	tables = main_table.find_all("table")[6:]

	return tables


#tries to return a lesson object, filled with the data from the parameter
def tryRetrieveLesson(table, prev=None):
	soup = BeautifulSoup(str(table), 'html.parser')
	rows = soup.table.find_all("tr")

	print("_______________")
	print(prev)
	print("_______________")

	# print(p)

	try:
		docent = rows[0].td.font.b.text.strip()
		name = rows[1].td.font.b.text.strip()
		place = rows[2].td.font.b.text.strip()

	except:
		return None

	return Lesson(name, docent, place)


def createGrid():
	tables = getTables()
	grid = [[None for i in range(8)] for j in range(int(math.ceil(len(tables) / 8)))]

	counter = 0

	for i in range(int(math.ceil(len(tables) / 8))):
		if i != math.ceil(len(tables) / 8) - 1:
			for j in range(8):
				grid[i][j] = tryRetrieveLesson(tables[counter], tables[counter].previous_element)
				counter += 1
		else:
			for j in range(len(tables) % 8):
				grid[i][j] = tryRetrieveLesson(tables[counter], tables[counter].previous_element)
				counter += 1

	return grid
