from LessonRetriever import LessonRetriever

lr = LessonRetriever()
lr.GetLessons()

for table in lr.tables:
	print(table)
	input()
