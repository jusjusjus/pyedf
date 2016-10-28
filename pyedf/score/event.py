#! /usr/bin/python



import datetime



def strtime_format1(timestring):

	if len(timestring) < 25:
		return None

	if timestring[4] == '-' and timestring[7] == '-' and timestring[10] == 'T' and timestring[13] == ':' and timestring[16] == ':' and timestring[19] == '.':
		return datetime.datetime.strptime(timestring[:25], "%Y-%m-%dT%H:%M:%S.%f")

	else:
		return None



def strtime_format2(timestring):

	if len(timestring) < 19:
		return None

	if timestring[4] == '-' and timestring[7] == '-' and timestring[10] == 'T' and timestring[13] == ':' and timestring[16] == ':':
		return datetime.datetime.strptime(timestring[:19], "%Y-%m-%dT%H:%M:%S")

	else:
		return None



def strtime_format3(timestring):

	if len(timestring) < 25:
		return None

	if timestring[2] == '/' and timestring[5] == '/' and timestring[10] == ' ' and timestring[13] == ':' and timestring[16] == ':' and timestring[19] == '.':
		return datetime.datetime.strptime(timestring[:25], "%m/%d/%Y %H:%M:%S.%f")

	else:
		return None



def strtime_format4(timestring):

	if len(timestring) < 19:
		return None

	if timestring[2] == '/' and timestring[5] == '/' and timestring[10] == ' ' and timestring[13] == ':' and timestring[16] == ':':
		return datetime.datetime.strptime(timestring[:19], "%m/%d/%Y %H:%M:%S")

	else:
		return None



strtime_formats = [strtime_format1,
		   strtime_format2,
		   strtime_format3,
		   strtime_format4]



def mystrtime(timestring):

	dtime = None

	for strtime in strtime_formats:
		dtime = strtime( timestring )
	
		if not dtime == None:
			return dtime
	
	if dtime == None:
		print("mystrtime::error : Unknown time string '"+timestring+"'")

	return None




class Event(datetime.datetime, object):

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
		print("obsolete.  Use timeSince() instead")
		return self.timeSince(start)



event = Event




if __name__=='__main__':

	event_1 = event(datetime.datetime(year=2001, month=4, day=5))
	event_2 = event(datetime.datetime(year=2001, month=4, day=6))

	print(event_2.timeSince(event_1), 'seconds')
	print(event_2+datetime.timedelta(seconds=1.), 'seconds')
