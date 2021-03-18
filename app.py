from LessonRetriever import LessonRetriever
from Lesson import LessonEncoder
from flask import Flask
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "Potato_Umbrella"


@app.route('/api/rooster/', methods=["GET"])
def rooster():
	lesson_retriever = LessonRetriever()
	lessons = lesson_retriever.GetLessons()

	return json.dumps(lessons, indent=4, cls=LessonEncoder)


if __name__ == "__main__":
	app.run()
