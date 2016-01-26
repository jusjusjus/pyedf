#! /usr/bin/python

import event
from datetime import timedelta


def interval2state(interval, sampling_rate, epoch_start, annot='new state'):

	assert len(interval) == 2
	t_start = interval[0]/float(sampling_rate)
	duration = (interval[1]-interval[0])/float(sampling_rate)
	start = epoch_start + timedelta(seconds=t_start)
	return state(start=start, duration=duration, annot=annot)



class state(event.event, object):


	def __new__(cls, start, duration=None, endstring=None, annot='None'):
		return super(state, cls).__new__(cls, time=start, annot=annot)




	def __init__(self, start, duration=None, endstring=None, annot='None'):
		event.event.__init__(self, time=start, annot=annot)

		if not duration == None:
			self.duration = float(duration) # in seconds 

		elif endstring:
			self.duration = (event.mystrtime(endstring)-self).total_seconds()

		else:
			print "start duration annot"
			print start, duration, annot
			raise ValueError

		self.compute_end()




	def __str__(self):
		return event.event.__str__(self)+','+repr(self.duration)+','+self.annot



	
	def __add__(self, other):
		return state(start=event.datetime.datetime.__add__(self, other), duration=self.duration, annot=self.annot)




	def compute_end(self): # datetime object of end
		self.end = event.datetime.datetime.__add__( self, timedelta(seconds=self.duration) )	# datetime object




	def state2time(self, start):
		return (self.timeSince(start), self.duration)	 # start of state,  duration of state




	def intersect(self, other_state, annot='intersection'):

		if self < other_state:
			new_start = other_state

		else:
			new_start = self

		if self.end < other_state.end:
			new_end = self.end

			if new_end < other_state:
				return None

		else:
			new_end = other_state.end

			if new_end < self:
				return None

		return state(start=new_start, duration=(new_end-new_start).total_seconds(), annot=annot)






if __name__=='__main__':

	state_1 = state(event.datetime.datetime(year=2001, month=4, day=5, hour=1, minute=4), 600., annot='state 1')
	#state_2 = state(event.datetime.datetime(year=2001, month=4, day=5, hour=1, minute=5), 600., annot='state 2')

	print state_1+event.datetime.timedelta(seconds=1.)

