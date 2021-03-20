# RoosterAPI
RoosterAPI is een A.P.I. for het rooster van het horizoncollege.

https://horizon-rooster.herokuapp.com/api/rooster
neemt GET requests aan, en retourneerd een lijst van 'lesson' objecten waar alle informatie in staat.


Url parameters


https://horizon-rooster.herokuapp.com/api/rooster?week_nummer=12

het weeknummer kan worden gespecificeert. de standaard waarde is het huidige weeknummer

https://horizon-rooster.herokuapp.com/api/rooster?vak=PORTF

filtert het vak. alleen de lessen van dit vak worden laten zien

https://horizon-rooster.herokuapp.com/api/rooster?klas=H19AO-B

hiermee geef je aan van welke klas de vakken worden laten zien. de standaard waarde is H19AO-A

https://horizon-rooster.herokuapp.com/api/rooster?dag_van_week=2

specificeer welke dag van de week je ziet. zero-based.(maandag=0, dinsdag=1 etc.)




Todos:

	-Specificeer gebouw en afdeling van de url(zodat niet alleen de economie studenten van hoorn kunnen kieken)
	-Have double lessons be returned as a single object, instead of multiple
	-Error handling