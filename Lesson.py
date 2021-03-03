class Lesson:
	def __init__(self, name, docent, place):
		self.name = name
		self.docent = docent
		self.place = place

		self.starttime = None
		self.endtime = None
		self.datum = None

	def ShowData(self):
		print(f"Name: {self.name}\nDocent: {self.docent}\nPlace: {self.place}")
