#! /usr/bin/python



import logging
import datetime
import numpy as np


logger = logging.getLogger(name='event')


def strtime_format1(timestring):
    if len(timestring) < 19:
        return None
    if timestring[4] == '-' and timestring[7] == '-' and timestring[10] == 'T' and timestring[13] == ':' and timestring[16] == ':':
        datehourmin = datetime.datetime.strptime(timestring[:16], "%Y-%m-%dT%H:%M")
        seconds =  datetime.timedelta(seconds=np.float(timestring[17:]))
        return datehourmin + seconds
    else:
        return None



def strtime_format3(timestring):
    if len(timestring) < 19:
        return None
    if timestring[2] == '/' and timestring[5] == '/' and timestring[10] == ' ' and timestring[13] == ':' and timestring[16] == ':':
        datehourmin = datetime.datetime.strptime(timestring[:16], "%m/%d/%Y %H:%M")
        seconds =  datetime.timedelta(seconds=np.float(timestring[17:]))
        return datehourmin + seconds
    else:
        return None



def strtime_lastresort(timestring):
    try:
        return datetime.datetime.strptime(timestring[:25], "%Y-%m-%dT%H:%M:%S.%f")
    except:
        return None


strtime_formats = [strtime_format1,
                   strtime_format3,
                   strtime_lastresort]



def mystrtime(timestring):
    dtime = None
    timestring = timestring.strip('\n').strip('\r').strip(' ')
    for strtime in strtime_formats:
        dtime = strtime( timestring )
        if not dtime is None:
            return dtime
    if dtime is None:
        logger.debug("mystrtime::error : Unknown time string '"+timestring+"'")
    return None




class Event(datetime.datetime, object):

    def __new__(cls, time, annot='event'):

        if isinstance(time, str):
            time = mystrtime(time)    # returns datetime object

        return super(event, cls).__new__(cls, time.year, time.month, time.day, time.hour, time.minute, time.second, time.microsecond)



    def __init__(self, time, annot='event'):

        annot = annot.strip('\n').strip('\r')    # Remove endline characters.

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
