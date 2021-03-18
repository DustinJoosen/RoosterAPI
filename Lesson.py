import json
from json import JSONEncoder


class Lesson:
	def __init__(self, name, docent, place):
		self.name = name
		self.docent = docent
		self.place = place

		self.starttime = None
		self.endtime = None
		self.datum = None

	def ShowData(self):
		print(f"You have {self.name} from {self.docent} in {self.place}")
		print(f"On {self.datum} from {self.starttime} until {self.endtime}")


class LessonEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__
