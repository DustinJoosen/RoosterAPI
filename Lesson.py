class Lesson:
	def __init__(self, name, docent, place, rowspan=2):
		self.name = name
		self.docent = docent
		self.place = place

		self.starttime = None
		self.endtime = None
		self.datum = None

		self.rowspan = rowspan

	def ShowData(self):
		print(f"You have {self.name} from {self.docent} in {self.place}")
		print(f"On {self.datum} from {self.starttime} until {self.endtime}")
