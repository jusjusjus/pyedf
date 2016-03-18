#!/usr/bin/python

import pyedf
import os

THISPATH = os.path.dirname(__file__)
if THISPATH == '': THISPATH = '.'

score = pyedf.score(score_file=THISPATH+'/sample.csv', verbose=2)

rec = pyedf.recording(filename=THISPATH+'/sample.edf')

sampling_rate, X = rec.get_data(state_of_interest=score.states[0], channels=[0])

print 'sampling rate :', sampling_rate
print 'X.shape :', X.shape
