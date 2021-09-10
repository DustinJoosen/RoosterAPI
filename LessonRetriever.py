import requests
from bs4 import BeautifulSoup
from datetime import datetime
from CustomObjects import Lesson, ClientException

repeater = "repeater"

start_times = ["08:30", "09:20", "10:25", "11:15", "12:05", "12:55", "13:45", "14:35", "15:40", "16:30"]
end_times = ["09:20", "10:10", "11:15", "12:05", "12:55", "13:45", "14:35", "15:25", "16:30", "17:20"]
dates = [None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", None]


class LessonRetriever:
	def __init__(self, url):
		self.tables = self.__GetTables(url)

	def GetLessons(self):
		self.tables = self.__ListifyTables(self.tables)
		self.tables = self.__SetRepeaters(self.tables)

		grid = self.__CreateGrid(self.tables)
		lessons = []

		for i in range(len(grid)):
			for j in range(len(grid[i])):
				if type(grid[i][j]) == Lesson:
					grid[i][j].SetDateTime(dates[j + 1], start_times[i], end_times[i])
					lessons.append(grid[i][j])

		return lessons

	def __CreateGrid(self, tables):
		grid = [[None for _ in range(10)] for _ in range(15)]

		for i in range(len(tables)):
			for j in range(len(tables[i])):
				if tables[i][j] == repeater:
					retrieved_value = self.__TryRetrieveLesson(tables[i][j - len(tables[i - 1])])
				else:
					retrieved_value = self.__TryRetrieveLesson(tables[i][j])

				grid[i][j] = retrieved_value

		return grid

	@staticmethod
	def __SetRepeaters(tables):

		for i in range(len(tables)):
			for j in range(len(tables[i])):

				table = tables[i][j]

				try:
					parent = table.previous_element
					rowspan = int(parent["rowspan"])
					colspan = int(parent["colspan"])

					if rowspan == 2 and colspan == 12:
						continue

					amount_of_lessons = int(rowspan / 2)
					for k in range(1, amount_of_lessons):
						tables[i + k].insert(j, repeater)

				except Exception as ex:
					if table != repeater:
						pass
					pass

		return tables

	@staticmethod
	def __ListifyTables(tables):
		listified = [[]]

		row = 0
		for i in range(1, len(tables)):
			if '<table><tr><td align="center" rowspan="2"><font face="Verdana" size="4">' in str(tables[i]):

				if True:
					listified[row] = listified[row][1:len(listified[row]) - 1]

				row += 1
				listified.append([])

				continue

			listified[row].append(tables[i])

		return listified

	def __GetTables(self, url):
		soup = self.__GetSoup(url=url)

		main_table = soup.find("table", {"border": 3, "rules": "all"})
		return main_table.find_all("table")[6:]

	#returns the soup object of the url
	@staticmethod
	def __GetSoup(url):
		response = requests.get(url)
		if response.status_code != 200:
			raise ClientException("De url is ongeldig")

		return BeautifulSoup(response.content, 'html.parser')

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