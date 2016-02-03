#! /usr/bin/python

import numpy as np

from my_hdr_struct import my_hdr_struct
import state
import montages
import datetime




class recording(my_hdr_struct):

	def __init__(self, filename, verbose=0):
		my_hdr_struct.__init__(self, filename)

		self.verbose = verbose

		if self.verbose:
			print "recording: Opening edf file", filename


	def get_data(self, state_of_interest=None, start=None, end=None, duration=None, channels=None):

		# Setup the channel information ..
		if channels == None:
			channels = np.arange(self.edfsignals)	# Load all channels.
		else:
			channels = np.asarray(channels)

		if channels.dtype == int:
			samplingrate = self.samplingrates[channels]
			if np.iterable(samplingrate):
				print 'samplingrate', samplingrate
				if not all(samplingrate == samplingrate[0]*np.ones((samplingrate.size), dtype=int)):	# If sampling rates are unqual ..
					print "recording : Unqual sampling rates.", samplingrate
					return None

				samplingrate = samplingrate[0]
					

		# Check the time ..
		# Start
		if isinstance(state_of_interest, state.state):
			start = state_of_interest
			duration = state_of_interest.duration

		if isinstance(start, datetime.datetime):	# start is a datetime object
			n_start = int((start-self.start).total_seconds() * samplingrate)

		elif isinstance(start, float):	# start is in seconds
			n_start = int(start * samplingrate)

		else:
			print "# start is not defined:", start
			raise ValueError

		# n_duration
		if isinstance(end, datetime.datetime):	# end is a datetime object
			n_duration = int((end-self.start).total_seconds() * samplingrate) - n_start

		if isinstance(duration, float):	# duration is given in seconds
			n_duration = int(duration * float(samplingrate))

		if self.verbose: print "# Loading from", start, "(= datapoint", n_start, "), ", n_duration, "datapoints of channels", channels

		return self.read_physical_samples(channels, start=n_start, size=n_duration)


	def __str__(self):
		string = '############## %s ################\n' % (self.fields['patient'])

		string +='start : %s\n' % (str(self.start))
		string +='edfsignals : %i\n' % (self.edfsignals)

		string += '\nSignal Information\n'
		string += '------------------\n' 
		for i in xrange(self.edfsignals):
			string += 'Signal %i\n' % (i)
			string += 'Name : %s\n' % (self.channelnames[i])
			string += 'Sampling rate : %i Hz\n' % (self.samplingrates[i])

			string += '\n'
		string += '------------------\n'
		

		string += '############## %s ################' % ('#'*len(self.fields['patient']))

		return string








if __name__ == "__main__":

	import pylab

	

	START = 0
	SIZE = 100000
	ch = pylab.array([1, 15, 1], dtype=long)
	dur = 100.


	rec = recording(filename="/home/jus/Data/capslpdb/brux2/brux2.edf", verbose=1)
	print rec
	data = rec.get_data(start=rec.start, duration=dur, channels=ch)
	print data

	pylab.plot(data[0])
	pylab.plot(data[1]+50.)
	pylab.show()


	del rec
