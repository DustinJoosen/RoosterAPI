import requests
import math
from bs4 import BeautifulSoup
from Lesson import Lesson


class LessonRetriever:
	def __init__(self):
		self.soup = self.__GetSoup()

		self.tables = []
		self.lessons = []

		self.rowspans = {}

		self.dates = [None, None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", None]
		self.start_times = ["08:30", "09:20", "10:25", "11:15", "12:05", "12:55", "13:45", "14:35", "15:40", "16:30", "17:20", "18:10", "19:00", "19:50", "20:40"]
		self.end_times = ["09:20", "10:10", "11:15", "12:05", "12:55", "13:45", "14:35", "15:25", "16:30", "17:20", "18:10", "19:00", "19:50", "20:40", "21:30"]

	def GetLessons(self):
		self.__SetTables()
		self.__SetRowspans()

	def __SetRowspans(self):
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
