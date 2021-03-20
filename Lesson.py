from json import JSONEncoder


class Lesson:
	def __init__(self, subject, docent, place):
		self.vak = subject
		self.docent = docent
		self.plaats = place

		self.wanneer = None

	def SetDateTime(self, date, starttime, endtime):
		self.wanneer = {
			"dag": date,
			"tijd": {
				"start": starttime,
				"eind": endtime
			}
		}


class LessonEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__
