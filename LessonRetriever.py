import requests
from bs4 import BeautifulSoup
from Lesson import Lesson


class LessonRetriever:
	def __init__(self):
		self.soup = self.__GetSoup()

		self.grid = [[None for _ in range(8)] for _ in range(15)]
		self.tables = []
		self.lessons = []

	def GetLessons(self):
		self.__SetTables()
		self.__SetRepeaters()
		self.__CreateGrid()

	def __CreateGrid(self):
		counter = 0
		for i in range(15):
			for j in range(8):
				retrieved_value = self.__TryRetrieveLesson(self.tables[counter])
				if retrieved_value == "Repeater":
					retrieved_value = self.__TryRetrieveLesson(self.tables[counter - 8])

				self.grid[i][j] = retrieved_value
				counter += 1

	#Set a value at the double lessons, to prevent everything breaking
	def __SetRepeaters(self):
		for i, table in enumerate(self.tables):
			try:
				parent = self.tables[i].previous_element
				rowspan = int(parent["rowspan"])

				#for the normal lessons, the rowspan is 2. otherwise it is 4
				if rowspan != 2:
					self.tables.insert(i + 8, "Repeater")
			except:
				pass

	#Returns a list of tables.
	def __SetTables(self):
		#searches for a table with specific attributes. the only table that matches is the one needed
		main_table = self.soup.find("table", {"border": 3, "rules": "all"})

		#a table is a cell in the main table. the first 6 can be skipped, as they are the headers
		self.tables = main_table.find_all("table")[6:]

	@staticmethod
	def __GetSoup():
		url = f"https://rooster.horizoncollege.nl/rstr/ECO/HRN/Roosters/09/c/c00038.htm"

		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')

		return soup

	#Try to get a lesson object out of a table. when not a lesson, it returns None
	@staticmethod
	def __TryRetrieveLesson(table):
		if table == "Repeater":
			return "Repeater"

		soup = BeautifulSoup(str(table), 'html.parser')
		rows = soup.table.find_all("tr")

		try:
			docent = rows[0].td.font.b.text.strip()
			name = rows[1].td.font.b.text.strip()
			place = rows[2].td.font.b.text.strip()
		except:
			return None

		return Lesson(name, docent, place)
