from LessonRetriever import LessonRetriever
from flask import Flask, jsonify
from Lesson import LessonEncoder
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "PotatoHead"


@app.route("/api/rooster/", methods=["GET"])
def getAll():
	lesson_retriever = LessonRetriever()
	lesson_list = lesson_retriever.GetList()

	return json.dumps(lesson_list, indent=4, cls=LessonEncoder)


if __name__ == "__main__":
	app.run()
