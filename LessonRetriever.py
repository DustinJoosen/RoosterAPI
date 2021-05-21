import requests
from bs4 import BeautifulSoup
from datetime import datetime
from CustomObjects import Lesson, ClientException

repeater = "repeater"

start_times = ["08:30", "09:20", "10:25", "11:15", "12:05", "12:55", "13:45", "14:35", "15:40", "16:30"]
end_times = ["09:20", "10:10", "11:15", "12:05", "12:55", "13:45", "14:35", "15:25", "16:30", "17:20"]


class LessonRetriever:

	COLUMNS = 6
	ROWS = 10

	def __init__(self, url):
		self.soup = self.__GetSoup(url)

		self.tables = []
		self.headers = []

		self.grid = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
		self.lessons = []

	def GetLessons(self):
		self.__SetTables()
		self.__CreateGrid()

		header_subtraction = 2 if self.COLUMNS == 8 else 1

		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				if type(self.grid[i][j]) == Lesson:
					self.grid[i][j].SetDateTime(self.headers[j - header_subtraction], start_times[i], end_times[i])
					self.lessons.append(self.grid[i][j])

		return self.lessons

	#this places the items in a multidimensional grid,
	#making it possible to assign dates and times to it depending on the place
	def __CreateGrid(self):
		if len(self.tables) != self.COLUMNS * self.ROWS:
			raise ClientException("Er ging iets mis met het ophalen van de lessen. misschien is er een vrije dag?")

		counter = 0
		for i in range(self.ROWS):
			for j in range(self.COLUMNS):
				if self.tables[counter] == repeater:
					retrieved_value = self.__TryRetrieveLesson(self.tables[counter - self.COLUMNS])
				else:
					retrieved_value = self.__TryRetrieveLesson(self.tables[counter])

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
					amount_of_lessons = int((rowspan - 2) / 2)

					for j in range(amount_of_lessons):
						x = ((j + 1) * self.COLUMNS)
						self.tables.insert(x + i, repeater)

			except:
				pass

	def __SetTables(self):
		# searches for a table with specific attributes. the only table that matches is the one needed
		main_table = self.soup.find("table", {"border": 3, "rules": "all"})

		# a table is a cell in the main table.
		tables = main_table.find_all("table")
		self.tables = tables[6:]

		for header in tables[1:6]:
			self.headers.append(self.__TryRetrieveHeader(header))

		self.__SetRepeaters()

	#Try to get a lesson object out of a table. when not a lesson, it returns None
	#TODO: Improve this one
	@staticmethod
	def __TryRetrieveLesson(table):
		if table == repeater:
			return repeater

		soup = BeautifulSoup(str(table), 'html.parser')
		rows = soup.table.find_all("tr")

		try:
			docent = rows[0].td.font.b.text.strip()
			subject = rows[1].td.font.b.text.strip()
			place = rows[2].td.font.b.text.strip()

			if subject == "---":
				raise Exception()
		except:
			return None

		return Lesson(subject, docent, place)

	# Try to get a header text out of the header
	@staticmethod
	def __TryRetrieveHeader(header):
		soup = BeautifulSoup(str(header), 'html.parser')

		try:
			header = soup.tr.td.font.b.text.strip()
			return header
		except:
			return "Unknown"

	#returns the soup object of the url
	@staticmethod
	def __GetSoup(url):
		response = requests.get(url)
		if response.status_code != 200:
			raise ClientException("De url is ongeldig")

		return BeautifulSoup(response.content, 'html.parser')
