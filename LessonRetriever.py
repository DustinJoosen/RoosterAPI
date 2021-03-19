import requests
from bs4 import BeautifulSoup
from datetime import datetime
from Lesson import Lesson

start_times = ["08:30", "09:20", "10:25", "11:15", "12:05", "12:55", "13:45", "14:35", "15:40", "16:30",
				"17:20", "18:10", "19:00", "19:50", "20:40"]
end_times = ["09:20", "10:10", "11:15", "12:05", "12:55", "13:45", "14:35", "15:25", "16:30", "17:20",
				"18:10", "19:00", "19:50", "20:40", "21:30"]


class LessonRetriever:
	#default for the weeknum, is the current weeknum
	weeknum = datetime.isocalendar(datetime.today())[1] - 1

	def __init__(self):
		self.soup = self.__GetSoup()

		self.grid = [[None for _ in range(8)] for _ in range(15)]
		self.tables = None

		self.headers = []
		self.lessons = []

	#places all the items from the grid inside a list, and assigns dates and times
	def GetLessons(self):
		self.__CreateGrid()

		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				if self.grid[i][j] is not None:
					self.grid[i][j].SetDateTime(self.headers[j - 2], start_times[i], end_times[i])
					self.lessons.append(self.grid[i][j])

		return self.lessons

	#this places the items in a multidimensional grid, making it possible to assign dates and times to it depending on the place
	def __CreateGrid(self):
		if self.tables is None:
			self.__SetTables()

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

		#a table is a cell in the main table.
		tables = main_table.find_all("table")
		self.tables = tables[6:]

		for header in tables[1:6]:
			self.headers.append(self.__TryRetrieveHeader(header))

		#where there are double lessons, there are gaps. this method temporary fills those gaps.
		self.__SetRepeaters()

	@staticmethod
	def __GetSoup():
		url = f"https://rooster.horizoncollege.nl/rstr/ECO/HRN/Roosters/{LessonRetriever.weeknum}/c/c00052.htm"

		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html.parser')

		return soup

	#Try to get a header text out of the header
	@staticmethod
	def __TryRetrieveHeader(header):
		soup = BeautifulSoup(str(header), 'html.parser')

		try:
			header = soup.tr.td.font.b.text.strip()
			return header
		except:
			return "Unknown"

	#Try to get a lesson object out of a table. when not a lesson, it returns None
	@staticmethod
	def __TryRetrieveLesson(table):
		if table == "Repeater":
			return "Repeater"

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
