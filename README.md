# RoosterAPI
RoosterAPI is een A.P.I. for het rooster van het horizoncollege.

https://horizon-rooster.herokuapp.com/api/rooster
neemt GET requests aan, en retourneerd een lijst van 'lesson' objecten waar alle informatie in staat.

https://horizon-rooster.herokuapp.com/api/rooster/tomorrow
neemt doet precies hetzelfde als de de vorige, maar geeft alle lessen van de volgende dag. Alleen de klas, sector en gebouw kunnen worden gespecificeerd in de url.


Url parameters


https://horizon-rooster.herokuapp.com/api/rooster?week_nummer=12

het weeknummer kan worden gespecificeert. de standaard waarde is het huidige weeknummer

https://horizon-rooster.herokuapp.com/api/rooster?vak=PORTF

filtert het vak. alleen de lessen van dit vak worden laten zien

https://horizon-rooster.herokuapp.com/api/rooster?docent=KERCK01

filtert het vak. alleen de lessen van deze docent worden laten zien

https://horizon-rooster.herokuapp.com/api/rooster?plaats=C207

filtert het vak. alleen de lessen op deze plaats worden laten zien

https://horizon-rooster.herokuapp.com/api/rooster?klas=H19AO-A

hiermee geef je aan van welke klas de vakken worden laten zien. de standaard waarde is H19AO-A

https://horizon-rooster.herokuapp.com/api/rooster?dag_van_week=2

specificeer welke dag van de week je ziet. zero-based.(maandag=0, dinsdag=1 etc.)

https://horizon-rooster.herokuapp.com/api/rooster?sector=ECO

hiermee geef je aan uit welke sector de vakken worden laten zien. de standaard waarde is ECO

https://horizon-rooster.herokuapp.com/api/rooster?gebouw=HRN

hiermee geef je aan uit welk gebouw de vakken worden laten zien. de standaard waarde is HRN





Todos:

	-CORS werkt niet goed
	-Change server from development to production