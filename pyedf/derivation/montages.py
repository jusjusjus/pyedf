#! /usr/bin/python

import numpy as np
import xml.etree.ElementTree as xml


MONTAGES_PATH = '/home/jus/.EDFView/Montages/'

FILE_TYPES = ['mtg', 'avg']



class montage(object):

    def __init__(self, file_name=None):
        
        self.file_name = file_name

        if not file_name == None:

            file_type = file_name.split('.')[-1] 
            FILE_TYPES.index(file_type)

            if file_type == 'mtg':
                self.__load_mtg(file_name)

            if file_type == 'avg':
                self.__load_avg(file_name)


    def __load_mtg(self, file_name):

        try:    self.tree = xml.parse(MONTAGES_PATH+self.file_name.split('/')[-1])    # load xml-file with montage
        except:    self.tree = xml.parse(self.file_name)

        root = self.tree.getroot()
        self.derivations = []                    # List of [[channelname 1, weight in derivation], [channelname 2, weight in derivation], ..]
        self.channels = []                    # Contains individual channel names
        self.derivation_names = []                # Contains derivation names

        for signalcomposition in root.iter('signalcomposition'):
            self.derivations.append([])
            self.derivation_names.append('')

            for signal in signalcomposition.iter('signal'):
                signal_label = signal.find('label').text.strip()
                self.derivations[-1].append([signal_label, float(signal.find('factor').text)])        # derivation[i] = [...[channel, weight]...]
                
                self.derivation_names[-1] += '-'+signal_label

                try:    self.channels.index(signal_label)
                except:    self.channels.append(signal_label)

            self.derivation_names[-1] = self.derivation_names[-1][1:]


    def __load_avg(self, file_name):
        self.channel_file = open(file_name, 'r')
        self.channels = []

        for line in self.channel_file:
            self.channels.append(line[:-1])

        mfactor = -1./float(len(self.channels))

        self.derivations = []
        self.derivation_names = []

        for channel in self.channels:
            self.derivation_names.append(channel)
            self.derivations.append([[channel, 1.]])        # channel name, weight

            for other_channel in self.channels:

                if other_channel == channel:
                    continue

                self.derivations[-1].append([other_channel, mfactor])    # derivation[i] = [...[channel, weight]...]


    def mixing_matrix(self, channel_names):

        N, M = len(channel_names), len(self.derivations)     # input-, output- dimension
        ch_dict = {}

        try:        # check if all necessary channels, stored in 'self.channels' are available
                # and also store the corresponding index in order to make derivation
            for ch in self.channels:        # create hash table.
                ch_dict[ch] = channel_names.index(ch)

        except:
            print("mixing_matrix:  Not enough channels available for derivation", self.file_name)
            print("\tAvailable channels:\t", channel_names)
            print("\n\tMissing channel:\t", ch)
            exit(-1)

        mixer = np.zeros((N, M), float)

        for j in xrange(len(self.derivations)):

            for signal in self.derivations[j]:
                mixer[ch_dict[signal[0]], j] = signal[1]

        return mixer, self.derivation_names







if __name__ == "__main__":

    mtg = montage('S001-IV-bipolar.mtg')
    chNames = []

    for ch in mtg.channels:
        chNames.append(ch)

    chNames.pop(chNames.index('O2'))
    print(mtg.mixing_matrix(chNames))









