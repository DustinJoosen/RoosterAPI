from LessonRetriever import LessonRetriever
from Lesson import LessonEncoder
from flask import Flask, request, current_app
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "Potato_Umbrella"


@app.route('/api/rooster/', methods=["GET"])
def rooster():
	weeknum = request.args.get('weeknum')
	if weeknum is not None:
		LessonRetriever.weeknum = int(weeknum)

	classname = request.args.get('classname')
	if classname is not None:
		LessonRetriever.classname = str(classname)

	lesson_retriever = LessonRetriever()
	lessons = lesson_retriever.GetLessons()
	lessons.sort(key=lambda x: x.when["day"])

	dayofweek = request.args.get('dayofweek')
	if dayofweek is not None:
		lessons = [l for l in lessons if l.when["day"][:4].lower() == dayofweek[:4].lower()]

	subject = request.args.get('subject')
	if subject is not None:
		lessons = [l for l in lessons if l.subject.lower() == subject.lower()]

	return current_app.response_class(json.dumps(lessons, indent=4, cls=LessonEncoder), mimetype="application/json")


if __name__ == "__main__":
	app.run()
