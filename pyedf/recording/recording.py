#! /usr/bin/python

import numpy as np

from .edf_hdr_struct import edf_hdr_struct, read_md5
from .channeltypes import is_channeltype
import pyedf.score as score
import datetime
import logging


if not hasattr(__builtins__, 'xrange'):
    xrange = range


class Recording(edf_hdr_struct):

    logger = logging.getLogger(name='recording')

    def __init__(self, filename, md5checksum=None, verbose=0):
        edf_hdr_struct.__init__(self, filename, md5checksum=md5checksum)

        self.verbose = verbose

        if self.verbose:
            print("recording: Opening edf file", filename)



    def select_channels_from_int(self, i):
        assert i < self.edfsignals
        return [i]


    def select_channels_from_str(self, name):
        if is_channeltype(name):
            return np.arange(self.edfsignals)[self.channeltypes == name].tolist()
        else:
            return [self.channelnames.index(name)]


    def select_channels(self, channels=None):
        self.logger.debug('select_channels({})'.format(channels))

        if channels is None:    # Select all channels.
            return range(self.edfsignals)
        elif not np.iterable(channels) or type(channels) == str or type(channels) == np.typeDict['str']: # Wenn channels nicht indizierbar oder ein String ist, ..
            channels = [channels]       #                .. dann mach ne Liste draus.

        channelindices = []
        for channel in channels:
            dtype = type(channel)
            if   dtype in [np.typeDict['int'], int]:
                channelindices.extend(self.select_channels_from_int(channel))
            elif dtype in [np.typeDict['str'], str]:
                channelindices.extend(self.select_channels_from_str(channel))
            else:
                print("Channel '{}' not understood.".format(channel))
                print("Possible Channels: {}".format(self.channelnames))
                exit(0)

        if len(channelindices) == 0:
            self.logger.debug("Channels '{}' not understood.".format(channels))
            self.logger.debug("Possible Channels: {}".format(self.channelnames))

        return channelindices


        # Setup the channel information ..
        if not (channels is None or np.iterable(channels)):
            print("recording : Parameter 'channels' not understood.", channels)
            raise AttributeError


    def get_samplingrate(self, channels):

        channels = self.select_channels(channels)

        samplingrate = self.samplingrates[channels]

        if np.iterable(samplingrate):

            if not all(samplingrate == samplingrate[0]*np.ones((samplingrate.size), dtype=int)):    # If sampling rates are unqual ..
                print("recording : Unqual sampling rates.", samplingrate)
                return None

            samplingrate = samplingrate[0]

        return samplingrate


    def get_data(self, state_of_interest=None, start=None, end=None, duration=None, channels=None):

        channels = self.select_channels(channels)

        # Check if all channels have the same sampling rate ..
        samplingrate = recording.get_samplingrate(self, channels)
                    

        # Load the time information ..
        # Start
        if isinstance(state_of_interest, score.state):
            start = state_of_interest
            duration = state_of_interest.duration

        if isinstance(start, datetime.datetime):    # start is a datetime object
            n_start = int((start-self.start).total_seconds() * samplingrate)

        elif isinstance(start, float):    # start is in seconds
            n_start = int(start * samplingrate)

        else:
            raise ValueError("# start is not defined:", start)

        # n_duration
        if isinstance(end, datetime.datetime):    # end is a datetime object
            n_duration = int((end-self.start).total_seconds() * samplingrate) - n_start

        if isinstance(duration, float):    # duration is given in seconds
            n_duration = int(duration * float(samplingrate))

        if self.verbose: print("# Loading from", start, "(= datapoint", n_start, "), ", n_duration, "datapoints of channels", channels)

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



recording = Recording




if __name__ == "__main__":

    import pylab

    START = 0
    SIZE = 100000
    ch = pylab.array([1, 15, 1], dtype=long)
    dur = 200.


    rec = recording(filename="/home/jus/Data/capslpdb/n4/n4.edf", verbose=0)
    fs, data = rec.get_data(start=rec.start, duration=dur, channels='EEG')
    t = np.arange(data.shape[1])/float(fs)
    print(fs)
    exit(0)

    offset = 80
    for (j, dat_j) in enumerate(data):
        pylab.plot(t, dat_j-offset*j, 'k-')

    pylab.show()


    del rec
