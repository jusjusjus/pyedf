#!/usr/bin/python

from my_param_struct import my_param_struct

EOG_Channels = ['ROC-LOC', 'LOC-ROC']

EEG_Channels = ['Fp2-F4',
		'F4-C4',
		'C4-P4',
		'P4-O2',
		'F8-T4',
		'T4-T6',
		'Fp1-F3',
		'FP1-F3',
		'F3-C3',
		'C3-P3',
		'P3-O1',
		'F7-T3',
		'T3-T5',
		'C4-A1']

ECG_Channels = ['ECG1-ECG2']


Types = dict(EEG=EEG_Channels, EOG=EOG_Channels, ECG=ECG_Channels) 



def get_type(channel):

	if type(channel) == my_param_struct:
		label = channel.label.contents.value.strip(" ")
	else:
		label = channel

	for t in Types:
		for ch in Types[t]:
			if label == ch:
				return t

	return 'unknown'


if __name__=="__main__":

	print get_type("T3-T5")
