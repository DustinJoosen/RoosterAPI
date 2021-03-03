import requests
import math
from bs4 import BeautifulSoup
from Lesson import Lesson

# Will be used in later versions, but for now it is locally saved to keep a stable input
# def getSoup():
# 	url = "https://rooster.horizoncollege.nl/rstr/ECO/HRN/Roosters/09/c/c00046.htm"
#
# 	response = requests.get(url)
# 	soup = BeautifulSoup(response.content, 'html.parser')
#
# 	return soup


def getSoup():
	with open("default.html", 'r') as file:
		soup = BeautifulSoup(file.read(), 'html.parser')
		return soup


#tries to return a lesson object, filled with the data from the parameter
def tryRetrieveLesson(table):
	soup = BeautifulSoup(str(table), 'html.parser')
	rows = soup.table.find_all("tr")

	try:
		name = rows[0].td.font.b.text.strip()
		docent = rows[1].td.font.b.text.strip()
		place = rows[2].td.font.b.text.strip()
	except:
		return None

	return Lesson(name, docent, place)


def getTables():
	soup = getSoup()
	main_table = soup.find("table", {"border": 3, "rules": "all"})

	#each table, is one cell in the main table
	tables = main_table.find_all("table")[6:]

	return tables


def createGrid():
	tables = getTables()
	grid = [[0 for i in range(8)] for j in range(int(math.ceil(len(tables) / 8)))]

	print(len(tables))
	counter = 0

	for i in range(int(math.ceil(len(tables) / 8))):

		if i != math.ceil(len(tables) / 8) - 1:
			for j in range(8):
				grid[i][j] = tryRetrieveLesson(tables[counter])
				counter += 1
		else:
			for j in range(len(tables) % 8):
				grid[i][j] = tryRetrieveLesson(tables[counter])
				counter += 1

	print(grid)
