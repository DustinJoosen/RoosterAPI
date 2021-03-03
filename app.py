from LessonRetriever import LessonRetriever

#will be a flask page#

lessonRetriever = LessonRetriever()
lessonlist = lessonRetriever.GetList()

for lesson in lessonlist:
	print(lesson.ShowData())
	print("\n___")
