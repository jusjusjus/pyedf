#!/usr/bin/python

import pyedf
import os

THISPATH = os.path.dirname(__file__)
if THISPATH == '': THISPATH = '.'


rec = pyedf.recording(filename=THISPATH+'/sample.edf')

score = pyedf.score(score_file=THISPATH+'/sample.csv', verbose=2)

print rec.get_data(state_of_interest=score.states[0], channels=[0])
