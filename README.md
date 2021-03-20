# RoosterAPI
A restful API for the school schedule of the horizoncollege


https://horizon-rooster.herokuapp.com/api/rooster
accepts GET requests, and returns a list of 'lesson' objects which you can work with.

https://horizon-rooster.herokuapp.com/api/rooster?weeknum=12&dayofweek=Maandag&classname=H19AO-A

allows you to specify which week you want the data from. when not specified, it gets the current weeknum.
You can also specify which day of the week you want the data from or which class to get the data from


Todos:

	-Have double lessons be returned as a single object, instead of multiple	
	-Error handling
	-Clean up the ui. it is currently both english and dutch