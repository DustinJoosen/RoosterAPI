from json import JSONEncoder


class Lesson:
	def __init__(self, name, docent, place):
		self.subject = name
		self.docent = docent
		self.place = place

		self.when = None

	def SetDateTime(self, date, starttime, endtime):
		self.when = {
			"day": date,
			"time": {
				"start": starttime,
				"end": endtime
			}
		}


class LessonEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__
