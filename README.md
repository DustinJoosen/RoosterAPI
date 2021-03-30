#RoosterAPI
#####RoosterAPI is een A.P.I. for het rooster van het horizoncollege.

#####Deze A.P.I. Kan worden gebruikt om GET requesten te sturen voor een lijst met objecten, waar informatie in staat over het rooster. De A.P.I. wordt gehost met heroku, op de volgende url:
#####*https://horizon-rooster.herokuapp.com/api/rooster/*

##Url parameters

de url parameters en filters kunnen worden gebruikt met elkaar. voorbeeld: /api/rooster?week_nummer=13&plaats=C207

###Url varianten

*https://horizon-rooster.herokuapp.com/api/rooster*
is de standaard url, en geeft een lijst met alle lessen van de huidige week.

*https://horizon-rooster.herokuapp.com/api/rooster/tomorrow*
geeft een lijst terug met alle lessen van morgen. Er kunnen geen filters worden gebruikt.

*https://horizon-rooster.herokuapp.com/api/rooster/today*
geeft een lijst terug met alle lessen van vandaag. Er kunnen geen filters worden gebruikt.


###Url parameters(worden gebruikt om het juiste rooster te vinden)

*https://horizon-rooster.herokuapp.com/api/rooster?sector=ECO*
hiermee geef je aan uit welk sector, het rooster wordt opgehaald. De standaard waarde is ECO

*https://horizon-rooster.herokuapp.com/api/rooster?gebouw=HRN*
hiermee geef je aan uit welk gebouw het rooster wordt opgehaald. De standaard waarde is HRN

*https://horizon-rooster.herokuapp.com/api/rooster?klas=H19AO-A*
hiermee geef je aan van welke klas het rooster wordt opgehaald. de standaard waarde is H19AO-A

*https://horizon-rooster.herokuapp.com/api/rooster?week_nummer=13*
hiermee geef je aan van welke week het rooster wordt opgehaald. De standaard waarde is het huidige weeknummer



###Url filters(worden gebruikt om aan te geven welke data wordt teruggegeven)



*https://horizon-rooster.herokuapp.com/api/rooster?vak=PORTF*
filtert het vak. alleen de lessen van dit vak worden laten zien

*https://horizon-rooster.herokuapp.com/api/rooster?docent=KERCK0*
filtert de docent. alleen de lessen van deze docent worden laten zien

*https://horizon-rooster.herokuapp.com/api/rooster?plaats=C207*
filtert de plaats. alleen de lessen op deze plaats worden laten zien

*https://horizon-rooster.herokuapp.com/api/rooster?dag_van_week=2*
specificeerd welke dag van de week je ziet. zero-based.(maandag=0, dinsdag=1 etc.)





##Todos:

	-CORS werkt niet goed
	-Change server from development to production



Gemaakt door Dustin Joosen. 