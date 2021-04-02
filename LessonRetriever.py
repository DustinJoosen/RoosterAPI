import requests
from bs4 import BeautifulSoup
from datetime import datetime
from CustomObjects import Lesson, ClientException

start_times = ["08:30", "09:20", "10:25", "11:15", "12:05", "12:55", "13:45", "14:35", "15:40", "16:30",
				"17:20", "18:10", "19:00", "19:50", "20:40"]
end_times = ["09:20", "10:10", "11:15", "12:05", "12:55", "13:45", "14:35", "15:25", "16:30", "17:20",
				"18:10", "19:00", "19:50", "20:40", "21:30"]


class LessonRetriever:

	COLUMNS = 8
	ROWS = 15

	def __init__(self, weeknum, _class, building, sector):
		# default for the weeknum, is the current weeknum
		self.weeknum = datetime.isocalendar(datetime.today())[1]

		#default values for if there are no matching url parameters
		self.url_codes = {"class": "H19AO-A", "building": "HRN", "sector": "ECO"}

		try:
			if _class is not None and isinstance(_class, str):
				self.url_codes["class"] = _class

			if building is not None and isinstance(building, str):
				self.url_codes["building"] = building

			if sector is not None and isinstance(sector, str):
				self.url_codes["sector"] = sector

			if weeknum is not None and isinstance(weeknum, str):
				self.weeknum = int(weeknum)

		except:
			raise ClientException("Een van de url parameters die is ingevoerd, is ongeldig")

		self.classId = self.__GetClassId(self.url_codes)
		self.soup = self.__GetSoup(self.classId, self.weeknum, self.url_codes)

		self.grid = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
		self.tables = None

		self.headers = []
		self.lessons = []

	#places all the items from the grid inside a list, and assigns dates and times
	def GetLessons(self):
		self.__CreateGrid()

		for i in range(len(self.grid)):
			for j in range(len(self.grid[i])):
				if type(self.grid[i][j]) == Lesson:
					self.grid[i][j].SetDateTime(self.headers[j - 2], start_times[i], end_times[i])
					self.lessons.append(self.grid[i][j])

		return self.lessons

	#this places the items in a multidimensional grid, making it possible to assign dates and times to it depending on the place
	def __CreateGrid(self):
		if self.tables is None:
			self.__SetTables()

		if len(self.tables) != (self.COLUMNS * self.ROWS):
			raise ClientException("Er ging iets mis met het ophalen van de lessen. Misschien is er een speciale les")

		counter = 0
		for i in range(self.ROWS):
			for j in range(self.COLUMNS):
				if self.tables[counter] == "Repeater":
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
						self.tables.insert(x + i, "Repeater")

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

	#returns a beautifulsoup to work with the page contents
	@staticmethod
	def __GetSoup(classId, weeknum, codes):
		url = "https://rooster.horizoncollege.nl/" \
				f"rstr/{codes['sector']}/{codes['building']}/Roosters/{weeknum}/c/c{classId}.htm"

		response = requests.get(url)
		if response.status_code != 200:
			raise ClientException("De url is ongeldig")

		soup = BeautifulSoup(response.content, 'html.parser')

		return soup

	#handles a bit of javascript code to retrieve the classId. the classId is the index ins the classes array + 1
	@staticmethod
	def __GetClassId(codes):
		url = f"https://rooster.horizoncollege.nl/rstr/{codes['sector']}/{codes['building']}/Roosters/frames/navbar.htm"

		response = requests.get(url)
		if response.status_code != 200:
			raise ClientException("De url is ongeldig")

		content = str(response.content)

		#find the indexes where the classes array starts and ends
		classes_starting_idx = content.find("var classes = [")
		teachers_starting_idx = content.find("var teachers = [")

		#get the javascript classes array
		classes_js_array = content[classes_starting_idx:teachers_starting_idx]

		#cut text away so that it can be made into a list
		classes_js_array = classes_js_array.replace("var classes = [", '')
		classes_js_array = classes_js_array.replace("];\\r\\n", '')
		classes_js_array = classes_js_array.replace("\"", '')

		classes_list = classes_js_array.split(",")

		#need to add one because the array is zero-based, but the page id starts at 1
		class_id = classes_list.index(codes['class']) + 1
		return f"{str(100000 + class_id)[1:]}"

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
