from GridMaker import createGrid


class LessonRetriever:
	def __init__(self):
		pass

	def GetList(self):
		lessonlist = self._CreateLessonList()
		if lessonlist is not None:
			return lessonlist

	@staticmethod
	def _CreateLessonList():
		grid = createGrid()
		lessonlist = []

		dates = [None, None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", None]
		start_times = ["08:30", "09:20", "10:25", "11:15", "12:05", "12:55", "13:45", "14:35", "15:40", "16:30", "17:20", "18:10", "19:00", "19:50", "20:40"]
		end_times = ["09:20", "10:10", "11:15", "12:05", "12:55", "13:45", "14:35", "15:25", "16:30", "17:20", "18:10", "19:00", "19:50", "20:40", "21:30"]

		for i in range(len(grid)):
			for j in range(len(grid[i])):
				if grid[i][j] is not None:
					grid[i][j].datum = dates[j]
					grid[i][j].starttime = start_times[i]
					grid[i][j].endtime = end_times[i]

					lessonlist.append(grid[i][j])

		return lessonlist
