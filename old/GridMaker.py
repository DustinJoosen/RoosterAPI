import requests
import math
from bs4 import BeautifulSoup
from Lesson import Lesson
import datetime

rowspans = {
	4: 4,
	5: 4,
	19: 4,
	23: 4,
	32: 4,
	37: 4,
	47: 4,
	48: 4,
	53: 4,
	62: 4
}


def getSoup():
	# weeknum = datetime.date.today().isocalendar()[1]
	url = f"https://rooster.horizoncollege.nl/rstr/ECO/HRN/Roosters/09/c/c00038.htm"

	print(url)

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
def tryRetrieveLesson(table, prev, counter):
	global rowspans

	soup = BeautifulSoup(str(table), 'html.parser')
	rows = soup.table.find_all("tr")

	try:
		rowspan = prev["rowspan"]
		if int(rowspan) != int(2):
			pass
			# rowspans[counter] = rowspan
	except KeyError as ex:
		rowspan = 2

	try:
		docent = rows[0].td.font.b.text.strip()
		name = rows[1].td.font.b.text.strip()
		place = rows[2].td.font.b.text.strip()

	except:
		return None

	return Lesson(name, docent, place, rowspan=rowspan)


def insertRowspawns(grid):
	global rowspans

	counter = 0
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if counter in rowspans:
				grid[i+1][j] = grid[i][j]

				del rowspans[counter]
				for key, value in rowspans.items():
					rowspans[key] = str(int(value) + 1)

			counter += 1

	return grid


def createGrid():
	tables = getTables()
	grid = [[None for i in range(8)] for j in range(int(math.ceil(len(tables) / 8)) + 1)]

	counter = 0

	for i in range(int(math.ceil(len(tables) / 8))):
		if i != math.ceil(len(tables) / 8) - 1:
			for j in range(8):
				grid[i][j] = tryRetrieveLesson(tables[counter], tables[counter].previous_element, counter)
				counter += 1
		else:
			for j in range(len(tables) % 8):
				grid[i][j] = tryRetrieveLesson(tables[counter], tables[counter].previous_element, counter)
				counter += 1

	print(rowspans)

	grid = insertRowspawns(grid)
	return grid
