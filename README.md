# RoosterAPI
A restful API for the school schedule of the horizoncollege

https://horizon-rooster.herokuapp.com/api/rooster
accepts GET requests, and returns a list of 'lesson' objects which you can work with.

https://horizon-rooster.herokuapp.com/api/rooster?weeknum=12
allows you to specify which week you want the data from. when not specified, it gets the current weeknum.


Todos:

	-Allow customization of the url that is retrieved(weeknum, class etc.)
	-Stop harcoding dates and times(it works, but is really fragile and will probaly break at some point)
	-Have double lessons be returned as a single object, instead of multiple
	-Make methods for specifying things like the date, or teacher or subject.	
	-When there are multiple lessons at the same time, it only includes the first teacher/subject/place