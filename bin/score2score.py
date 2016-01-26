#!/usr/bin/python

from pylab import *
import numpy as np
import sys
import time
import pyedf.score as sc
import pyedf.event
import datetime
import re




def getFilename():

	infile = None
	outfile = None

	if len(sys.argv) < 2:
		print 'no file provided.'
		print 'score2score.py <input> (<output>)'
		exit(1)
	
	else:
		infile = sys.argv[1]
		if len(sys.argv) > 2: outfile = sys.argv[2]

	return infile, outfile



stages = ['W', 'S1', 'S2', 'S3', 'S4', 'REM', 'R']
def interpret_stage(stage):

	try:
		stages.index(stage)
	except:
		print 'stage %s unknown.'% (stage)
		return None

	return stage



def interpret_time(timestring):
	timestring = timestring.replace('.', ':')
	if len(timestring.split(':') == 3):
		return timestring
	else:
		return None



def interpret_event(event):

	if eventlist.has_key(event):	return eventlist[event]
	else:				return None



def interpret_duration(duration):

	try:	return float(duration) 
	except:	return None


###



delimiter = '\t'
keys1 = ['sleep_stage', 'position', 'time', 'event', 'duration', 'location']
keys2 = ['sleep_stage', 'time', 'event', 'duration', 'location']




###


eventlist = dict()
eventlist['SLEEP-S0'] = 'Wake'
eventlist['SLEEP-S1'] = 'S1'
eventlist['SLEEP-S2'] = 'S2'
eventlist['SLEEP-S3'] = 'S3'
eventlist['SLEEP-S4'] = 'S4'
eventlist['SLEEP-REM'] = 'REM'

interpret = dict()
interpret['sleep_stage'] = interpret_stage
interpret['position'] = lambda x: 1
interpret['time'] = lambda x: x
interpret['event'] = interpret_event
interpret['duration'] = interpret_duration
interpret['location'] = lambda x: 1



###



infile, outfile = getFilename()


fin = open(infile, 'r')
score = sc.score()




### determine date
for line in fin:

	if re.search('Date', line):
		(day, month, year) = re.findall("[0-9]+", line)

		date = "%s-%s-%s" % (year, month, day)
### determine date

fin.seek(0) # it's necessary to reopen? (rwinds pointer)

### read all states
previous_time = None
one_day = datetime.timedelta(hours=24)
for line in fin:

	y = line.split(delimiter)

	if len(y) == len(keys1):	keys = keys1
	elif len(y) == len(keys2):	keys = keys2
	else:				continue

	yitp = dict({ (key, interpret[key](y[k])) for (k, key) in enumerate(keys) })

	if any([yi == None for yi in yitp.values()]):
		continue	# check if valid readout

	yitp['time'] = yitp['time'].replace('.', ':')

	start = date+'T'+yitp['time']
	time = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S") 

	if previous_time:
		if time < previous_time:
			time = time + one_day
			start = datetime.datetime.isoformat(time)


	score.append(start=start, duration=yitp['duration'], annot=yitp['event'])
	previous_time = time

### read all states

	
### clean up
fin.close()

if outfile == None:	print score
else:			score.save(outfile)
### clean up










