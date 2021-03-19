from LessonRetriever import LessonRetriever
from Lesson import LessonEncoder
from flask import Flask, request
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "Potato_Umbrella"


@app.route('/api/rooster/', methods=["GET"])
def rooster():
	weeknum = request.args.get('weeknum')
	if weeknum is not None:
		LessonRetriever.weeknum = int(weeknum)

	lesson_retriever = LessonRetriever()
	lessons = lesson_retriever.GetLessons()

	return json.dumps(lessons, indent=4, cls=LessonEncoder)


if __name__ == "__main__":
	app.run()
