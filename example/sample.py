
import os
import pyedf
from pyedf.recording import edf_hdr_struct, read_md5

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

assert os.path.exists(sample_edf)
assert os.path.exists(sample_score)
assert os.path.exists(sample_md5)

print("\n###############")
print("TEST : read_md5")
print("###############\n")
md5sum = read_md5(filename=sample_md5)
print(TEST_PASSED)

print("#####################")
print("TEST : edf_hdr_struct")
print("#####################\n")
hdr = edf_hdr_struct.edf_hdr_struct(filename=sample_edf, md5checksum=md5sum['sample.edf'])
print("Some samples :", hdr.read_physical_samples([0], 0, 10))
hdr.close()
print(TEST_PASSED)

print("\n############")
print("TEST : score")
print("############\n")
score = pyedf.score(filename=sample_score, verbose=0)
print(score.states[0])
print(TEST_PASSED)

print("\n################")
print("TEST : recording")
print("###############\n")
rec = pyedf.recording(filename=sample_edf)
print(rec.patient)
sampling_rate, X = rec.get_data(state_of_interest=score.states[0], channels=['C4-P4', 0])
print('sampling rate :', sampling_rate)
print('X.shape :', X.shape)
print(TEST_PASSED)
