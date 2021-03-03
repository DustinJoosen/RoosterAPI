import requests
from bs4 import BeautifulSoup
from Lesson import Lesson

# Will be used in later versions, but for now it is locally saved to keep a stable input
# def getSoup():
# 	url = "https://rooster.horizoncollege.nl/rstr/ECO/HRN/Roosters/09/c/c00046.htm"
#
# 	response = requests.get(url)
# 	soup = BeautifulSoup(response.content, 'html.parser')

#	return soup.prettify()


def getSoup():
	with open("default.html", 'r') as file:
		soup = BeautifulSoup(file.read(), 'html.parser')
		return soup


# def filter(soup):


def getTables():
	soup = getSoup()
	main_table = soup.find("table", {"border": 3, "rules": "all"})

	#each table, is one cell in the main table
	tables = main_table.find_all("table")[6:]

	for table in tables:
		print(table, end="\n___\n")

	return tables


def createGrid():
	rows = getTables()
	grid = [[]]
