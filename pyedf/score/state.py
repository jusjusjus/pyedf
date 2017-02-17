#! /usr/bin/python

from .event import Event, mystrtime
import numpy as np
from datetime import timedelta, datetime
import logging



def interval2state(interval, sampling_rate, epoch_start, annot=''):

    assert len(interval) == 2

    t_start = interval[0]/float(sampling_rate)
    duration = (interval[1]-interval[0])/float(sampling_rate)
    start = epoch_start + timedelta(seconds=t_start)
    return state(start=start, duration=duration, annot=annot)



class State(Event):

    logger = logging.getLogger(name='State')

    MINIMUM_DURATION = 0.1 # sec.

    def __new__(cls, start, duration=None, endstring=None, annot='None'):

        return super(State, cls).__new__(cls, time=start, annot=annot)


    def __init__(self, start, duration=None, endstring=None, annot='None'):

        super(State, self).__init__(time=start, annot=annot)

        self.set_duration(duration=duration, endstring=endstring)
    

    def set_duration(self, duration=None, endstring=None):

        if not duration == None:
            self.duration = float(duration) # in seconds 

        elif not endstring == None:
            self.duration = (mystrtime(endstring)-self).total_seconds()

        else:
            raise ValueError("start, duration, annot = %s, %s, %s" % (str(start), str(duration), str(annot)))

        #if self.duration < self.MINIMUM_DURATION:
        #    raise ValueError("start, duration, annot = %s, %s, %s" % (str(start), str(duration), str(annot)))

        self.compute_end()


    def __str__(self):

        return Event.__str__(self)+','+repr(self.duration)+','+self.annot

    
    def __add__(self, other):

        return State(start=datetime.__add__(self, other), duration=self.duration, annot=self.annot)


    def compute_end(self): # datetime object of end

        self.end = datetime.__add__( self, timedelta(seconds=self.duration) )    # datetime object


    def state2time(self, start):

        return (self.timeSince(start), self.duration)     # start of state,  duration of state

    
    def intersect(self, other, annot=None):

        if np.iterable(other):
            result = []

            for s in other:
                section_s = self.intersect_state(s, annot)

                if not section_s == None:
                    result.append( section_s )


        else:
            result = self.intersect_state(other, annot)

        return result


    def intersect_state(self, other_state, annot=None):

        assert isinstance(other_state, State)

        if self.end < other_state or \
           self     > other_state.end:
           return None

        if self < other_state:
            start = other_state
        else:
            start = self

        if self.end < other_state.end:
            end = self.end
        else:
            end = other_state.end

        duration = (end-start).total_seconds()

        if duration < self.MINIMUM_DURATION:
            return None

        if annot == None:
            annot = self.annot

        return state(start=start, duration=duration, annot=annot)



state = State




if __name__=='__main__':

    state_1 = State(event.datetime.datetime(year=2001, month=4, day=5, hour=1, minute=4), 600., annot='state 1')
    #state_2 = State(event.datetime.datetime(year=2001, month=4, day=5, hour=1, minute=5), 600., annot='state 2')

    print(state_1+event.datetime.timedelta(seconds=1.))

