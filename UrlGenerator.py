from datetime import datetime
from CustomObjects import ClientException
import requests


class UrlGenerator:
	def __init__(self, weeknum, classcode, buildingcode, sectorcode):
		self.weeknum = datetime.isocalendar(datetime.today())[1]
		self.classcode = "H19AO-A"
		self.buildingcode = "HRN"
		self.sectorcode = "ECO"

		try:
			if weeknum is not None and isinstance(weeknum, str):
				self.weeknum = weeknum
			if classcode is not None and isinstance(classcode, str):
				self.classcode = classcode
			if buildingcode is not None and isinstance(buildingcode, str):
				self.buildingcode = buildingcode
			if sectorcode is not None and isinstance(sectorcode, str):
				self.sectorcode = sectorcode
		except:
			raise ClientException("Een van de url parameters die is ingevoerd, is ongeldig")

	def Generate(self):
		class_id = self.__GetClassId()

		return "https://rooster.horizoncollege.nl/" \
			f"rstr/{self.sectorcode}/{self.buildingcode}/Roosters/{self.weeknum}/c/c{class_id}.htm"

	#handles a bit of javascript code to retrieve the classId. the classId is the index ins the classes array + 1
	#this is EXTREMELY unstable. if they add one line-break at some point, it breaks.
	def __GetClassId(self):
		url = f"https://rooster.horizoncollege.nl/rstr/{self.sectorcode}/{self.buildingcode}/Roosters/frames/navbar.htm"

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
		class_id = classes_list.index(self.classcode) + 1
		return f"{str(100000 + class_id)[1:]}"
