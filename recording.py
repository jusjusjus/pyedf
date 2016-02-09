#! /usr/bin/python

import numpy as np

from edf_hdr_struct import edf_hdr_struct
import state
import montages
import datetime




class recording(edf_hdr_struct):

	def __init__(self, filename, verbose=0):
		edf_hdr_struct.__init__(self, filename)

		self.verbose = verbose

		if self.verbose:
			print "recording: Opening edf file", filename


	def get_samplingrate(self, channels):

		samplingrate = self.samplingrates[channels]
		if np.iterable(samplingrate):
			if not all(samplingrate == samplingrate[0]*np.ones((samplingrate.size), dtype=int)):	# If sampling rates are unqual ..
				print "recording : Unqual sampling rates.", samplingrate
				return None

			samplingrate = samplingrate[0]

		return samplingrate


	def get_data(self, state_of_interest=None, start=None, end=None, duration=None, channels=None):

		# Setup the channel information ..
		if not (channels == None or np.iterable(channels)):
			print "recording : Parameter 'channels' not understood.", channels
			return None

		theType = channels

		if type(theType) == str:			# Load only those channels of type 'theType'.
			channels = np.arange(self.edfsignals)[self.channeltypes == theType]

		# Check if all channels have the same sampling rate ..
		samplingrate = self.get_samplingrate(channels)
					

		# Load the time information ..
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

		return samplingrate, self.read_physical_samples(channels, start=n_start, size=n_duration)


	def __str__(self):
		string = '\n############## %s ################\n' % (self.patient)

		string +='start : %s\n' % (str(self.start))
		string +='edfsignals : %i\n' % (self.edfsignals)

		string += '\nSignal Information\n'
		string += '------------------\n' 
		for i in xrange(self.edfsignals):
			string += 'Signal %i\n'				% (i)
			string += 'Name : %s\n'				% (self.channelnames[i])
			string += 'Type : %s\n'				% (self.channeltypes[i])
			string += 'Sampling rate : %i Hz\n' 		% (self.samplingrates[i])

			string += '\n'
		string += '------------------\n'
		

		string += '############## %s ################\n' % ('#'*len(self.patient))

		return string








if __name__ == "__main__":

	import pylab

	START = 0
	SIZE = 100000
	ch = pylab.array([1, 15, 1], dtype=long)
	dur = 200.


	rec = recording(filename="/home/jus/Data/capslpdb/n5/n5.edf", verbose=0)
	fs, data = rec.get_data(start=rec.start, duration=dur, channels='EEG')
	t = np.arange(data.shape[1])/float(fs)

	offset = 80
	for (j, dat_j) in enumerate(data):
		pylab.plot(t, dat_j-offset*j, 'k-')

	pylab.show()


	del rec
