#!/usr/bin/python

from my_param_struct import my_param_struct

EOG_Channels = ['ROC-LOC', 'LOC-ROC',
		'ROC',
		'LOC']

EEG_Channels = ['FP1',
		'FP2',
		'Fp1',
		'Fp2',
		'F3',
		'F4',
		'F7',
		'F8',
		'T3',
		'T4',
		'T5',
		'T6',
		'C3',
		'C4',
		'P3',
		'P4',
		'O1',
		'O2',
		'A1',
		'A2',
		'Fp2-F4', 'FP2-F4',
		'F2-F4',
		'F4-C4',
		'C4-P4',
		'P4-O2',
		'F8-T4',
		'T4-T6',
		'Fp1-F3', 'FP1-F3',
		'F3-C3',
		'C3-P3',
		'P3-O1',
		'F7-T3',
		'T3-T5',
		'C4-A1']

ECG_Channels = ['ECG1-ECG2',
		'ECG1',
		'ECG2']

HR_Channels = ['HR']

Resp_Channels = ['PLETH', 'Pleth',
		'TORACE', 'Torace',
		'ADDDOME', 'ADDOME', 'Abdo',
		'Flusso', 'Canula',
		'TERMISTORE']

BloodGas_Channels = ['SAO2', 'SpO2', 'Ox Status']

Leg_Channels = ['SX1-SX2',
		'DX1-DX2', 'Dx1-DX2',
		'DX1', 'DX2',
		'SX1', 'SX2',
		'TIB Dx', 'TIB Sx']

EMG_Channels = ['EMG1-EMG2',
		'EMG1',
		'EMG2']

Position_Channels = ['Posizione', 'Position',
			'STAT']

Snore_Channels = ['Sound', 'MIC']


Types = dict(EEG=EEG_Channels, EOG=EOG_Channels, ECG=ECG_Channels,
		Resp=Resp_Channels, Leg=Leg_Channels, EMG=EMG_Channels,
		BloodGas=BloodGas_Channels, HR=HR_Channels, Position=Position_Channels,
		Snore=Snore_Channels) 



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
