#! /usr/bin/python


import numpy as np
from pyedf.recording import recording, read_md5
from .montages import montage
import xml.etree.ElementTree as xml



class derivation(recording):

    def __init__(self, edf_filename, montage_filename, md5checksum=None, verbose=0):
        recording.__init__(self, edf_filename, md5checksum=md5checksum, verbose=verbose)
        self.mtg = montage(montage_filename)

        self.channelindices = np.asarray([self.channelnames.index(channel)
                            for channel in self.mtg.channels])            # Find the recording index of channels in the montage

        self.mixer = self.mtg.mixing_matrix(self.mtg.channels)


    def get_samplingrate(self):

        return super(derivation, self).get_samplingrate(self.channelindices)


    def get_data(self, state_of_interest=None, start=None, end=None, duration=None, channels=None):

        sampling_rate, X = super(derivation, self).get_data(state_of_interest, start, end, duration, self.channelindices)

        Y = np.dot(np.transpose(self.mixer[0]), X)

        return sampling_rate, Y     # Y[derivation, time]






if __name__ == "__main__":

    import matplotlib.pyplot as plt

    md5 = read_md5(filename="../../../example/md5sum.txt")
    dx = derivation('../../../example/sample.edf', '../../../example/sample.mtg', md5checksum=md5)


    samplingrate, x = dx.get_data(start=0., duration=100.)
    t = np.arange(x.shape[1])/float(samplingrate)

    for i in xrange(x.shape[0]):
        plt.plot(t, x[i]-30.*i)

    plt.show()






