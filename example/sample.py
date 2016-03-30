#!/usr/bin/python

import os

from pyedf.recording import edf_hdr_struct, read_md5
import pyedf


TEST_FAILED = """
##############
TEST : failed.
##############
"""
TEST_PASSED = """
##############
TEST : passed.
##############
"""

THISPATH = os.path.dirname(__file__)
if THISPATH == '': THISPATH = '.'








sample_edf   = THISPATH+'/sample.edf'
sample_score = THISPATH+'/sample-epochs.csv'
sample_md5   = THISPATH+'/sample.md5'

try:
	assert os.path.exists(sample_edf)
	assert os.path.exists(sample_score)
	assert os.path.exists(sample_md5)

except:
	print "Module test impossible:"
	print "Critical files not available."
	print "File necessary :\n%s\n%s\n%s" % (sample_edf, sample_score, sample_md5)
	print "exiting .."
	exit(-1)


###

print "\n###############"
print "TEST : read_md5"
print "###############\n"

try:
	md5sum = read_md5(filename=sample_md5)
	print TEST_PASSED
except:
	print TEST_FAILED

print "#####################"
print "TEST : edf_hdr_struct"
print "#####################\n"

#hdr = edf_hdr_struct.edf_hdr_struct(filename=sample_edf, md5checksum=md5sum['sample.edf'])
#print hdr.read_physical_samples([0], 0, 10)
#exit(0)

try:
	hdr = edf_hdr_struct.edf_hdr_struct(filename=sample_edf, md5checksum=md5sum['sample.edf'])
	print "Some samples :", hdr.read_physical_samples([0], 0, 10)
	hdr.close()
	print TEST_PASSED
except:
	print TEST_FAILED

print "\n############"
print "TEST : score"
print "############\n"

try:
	score = pyedf.score(filename=sample_score, verbose=2)
	print score
	print TEST_PASSED
except:
	print TEST_FAILED

print "\n################"
print "TEST : recording"
print "###############\n"


try:
	rec = pyedf.recording(filename=sample_edf)
	sampling_rate, X = rec.get_data(state_of_interest=score.states[0], channels=[0])
	print 'sampling rate :', sampling_rate
	print 'X.shape :', X.shape
	print TEST_PASSED
except:
	print TEST_FAILED
