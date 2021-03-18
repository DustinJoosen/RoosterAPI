from old.LessonRetriever import LessonRetriever
from flask import Flask
from Lesson import LessonEncoder
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "PotatoHead"


@app.route("/api/rooster/", methods=["GET"])
def getAll():
	lesson_retriever = LessonRetriever()
	lesson_list = lesson_retriever.GetList()

	#There are 9 portfolio objects, but only 8 portfolio lessons!!!

	#expected value:27
	print(len(lesson_list))

	return json.dumps(lesson_list, indent=4, cls=LessonEncoder)


if __name__ == "__main__":
	app.run()
