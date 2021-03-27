from LessonRetriever import LessonRetriever
from CustomObjects import LessonEncoder, ClientException
from flask import Flask, request, current_app, redirect, jsonify
from datetime import datetime
import json
# from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "Potato_Umbrella"

# CORS(app)
# cors = CORS(app, resources={
# 	r"/*": {
# 		"origins": "*"
# 	}
# })


@app.errorhandler(404)
def _404(e):
	return redirect("/api/rooster/")


@app.route('/api/rooster/tomorrow', methods=["GET"])
def tomorrow():
	try:
		classcode = request.args.get('klas')
		buildingcode = request.args.get('gebouw')
		sectorcode = request.args.get('sector')

		lesson_retriever = LessonRetriever(None, classcode, buildingcode, sectorcode)
		lessons = lesson_retriever.GetLessons()

		tomorrow_idx = datetime.today().weekday() + 1

		days_of_week = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"]
		lessons = [l for l in lessons if l.wanneer["dag"][:4].lower() == days_of_week[tomorrow_idx][:4].lower()]

		json_obj = json.dumps(lessons, indent=4, cls=LessonEncoder)
		return current_app.response_class(json_obj, mimetype="application/json"), 200

	except Exception as ex:
		return jsonify({"error_message": str(ex)}), 400


@app.route('/api/rooster/', methods=["GET"])
def rooster():
	try:
		weeknum = request.args.get('week_nummer')
		classcode = request.args.get('klas')
		buildingcode = request.args.get('gebouw')
		sectorcode = request.args.get('sector')

		lesson_retriever = LessonRetriever(weeknum, classcode, buildingcode, sectorcode)
		lessons = lesson_retriever.GetLessons()
		lessons.sort(key=lambda x: x.wanneer["dag"])

		#filters
		dayofweek = request.args.get('dag_van_week')
		if dayofweek is not None:
			if int(dayofweek) > 4:
				raise ClientException("Bij dag_van_week wordt er een waarde verwacht tussen 0(maandag) en vrijdag(4)")

			days_of_week = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag"]
			lessons = [l for l in lessons if l.wanneer["dag"][:4].lower() == days_of_week[int(dayofweek)][:4].lower()]

		subject = request.args.get('vak')
		if subject is not None:
			lessons = [l for l in lessons if l.vak.lower() == subject.lower()]

		docent = request.args.get("docent")
		if docent is not None:
			lessons = [l for l in lessons if l.docent.lower() == docent.lower()]

		place = request.args.get("plaats")
		if place is not None:
			lessons = [l for l in lessons if l.plaats.lower() == place.lower()]

		json_obj = json.dumps(lessons, indent=4, cls=LessonEncoder)
		return current_app.response_class(json_obj, mimetype="application/json"), 200

	except ClientException as cex:
		return jsonify({"error_message": str(cex)}), 400
	except Exception as ex:
		return ex, 500


if __name__ == "__main__":
	app.run()
