#!/usr/bin/python

from .edf_param_struct import edf_param_struct

EEG_Channels = ['EEG',
        'FP1',
        'FP2',
        'Fp1',
        'Fp2',
        'F3', 'F3A2',
        'F4', 'F4A1',
        'F7',
        'F8',
        'T3',
        'T4',
        'T5',
        'T6',
        'C3', 'C3-A2', 'C3A2',
        'C4', 'C4A1', 'C4-A1',
        'P3',
        'P4',
        'O1', 'O1A2',
        'O2', 'O2-A1', 'O2A1',
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
        'F1-F3',
        'F3-C3',
        'C3-P3',
        'P3-O1',
        'F7-T3',
        'T3-T5']

EOG_Channels = ['EOG', 'EOG dx',
        'ROC-LOC', 'LOC-ROC',
        'ROC', 'ROC-A2', 'EOG-R',
        'LOC', 'LOC-A1', 'EOG-L']

ECG_Channels = ['ECG', 'EKG', 'ekg',
        'ECG1',
        'ECG2',
        'ECG1-ECG2']

HR_Channels = ['HR',
           'Heart Rate Varia']

Resp_Channels = ['PLETH', 'Pleth',
        'TORACE', 'Torace', 'toracico',
        'ADDDOME', 'ADDOME', 'Abdo', 'abdomen'
        'Flusso', 'Canula', 'cannula', 'Flow', 'flow',
        'TERMISTORE']

BloodGas_Channels = ['SAO2', 'SpO2', 'Ox Status']

Leg_Channels = ['TIB', 'Leg', 'TIB Dx', 'TIB Sx', 'tib sin', 'tib dx',
        'DX1-DX2', 'Dx1-DX2',
        'DX1', 'DX2',
        'SX1', 'SX2',
        'SX1-SX2']

EMG_Channels = ['EMG', 'EMG1-EMG2', 'EMG-EMG',
        'EMG1', 'CHIN1',
        'EMG2', 'CHIN2',
        'deltoide', 'EMG']

Position_Channels = ['Position', 'Posizione',
             'STAT']

Snore_Channels = ['MIC', 'Sound']


Types = dict(EEG=EEG_Channels, EOG=EOG_Channels, ECG=ECG_Channels,
        Resp=Resp_Channels, Leg=Leg_Channels, EMG=EMG_Channels,
        BloodGas=BloodGas_Channels, HR=HR_Channels, Position=Position_Channels,
        Snore=Snore_Channels) 



def get_type(channel):

    if type(channel) == edf_param_struct:
        label = channel.label_b.decode('utf-8').strip(" ")
    else:
        label = channel

    for t in Types:

        if t in label:    # Example:  label="EEG left channel", t="EEG".  returns true :)
            return t

        for ch in Types[t]:
            if label == ch:
                return t

    return 'unknown'


def is_channeltype(string):    # type : return True

    for t in Types:
        if string == t:
            return True

    return False




if __name__=="__main__":

    print(get_type("T3-T5"))
