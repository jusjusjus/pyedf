#! /usr/bin/python



import datetime



def mystrtime(timestring):

	try:	 return datetime.datetime.strptime(timestring[:25], "%Y-%m-%dT%H:%M:%S.%f")
	except:	 return datetime.datetime.strptime(timestring[:19], "%Y-%m-%dT%H:%M:%S")



class event(datetime.datetime, object):

	def __new__(cls, time, annot='event'):

		if isinstance(time, str):
			time = mystrtime(time)	# returns datetime object

		return super(event, cls).__new__(cls, time.year, time.month, time.day, time.hour, time.minute, time.second, time.microsecond)



	def __init__(self, time, annot='event'):

		annot = annot.strip('\n').strip('\r')	# Remove endline characters.

		self.annot = annot



	def __str__(self):
		time_string = str(self.time())

		if len(time_string) < 10:
			time_string += '.000000'

		return str(self.date())+'T'+time_string



	def __add__(self, other):
		return event(time=datetime.datetime.__add__(self, other), annot=self.annot)



	def timeSince(self, start): # time of event since 'start'
		return (self-start).total_seconds()



	def time_since(self, start): # time of event since 'start'
		print "obsolete.  Use timeSince() instead"
		return self.timeSince(start)








if __name__=='__main__':

	event_1 = event(datetime.datetime(year=2001, month=4, day=5))
	event_2 = event(datetime.datetime(year=2001, month=4, day=6))

	print event_2.timeSince(event_1), 'seconds'
	print event_2+datetime.timedelta(seconds=1.), 'seconds'
