#! /usr/bin/python

from .edf_param_struct import edf_param_struct
from .channeltypes import get_type
from pyedf.score import State
import ctypes as ct
import numpy as np
import datetime
import sys
import os

if not hasattr(__builtins__, 'xrange'):
    xrange = range


# Set up the path to the foreign library
THISPATH = os.path.dirname(__file__)

if len(THISPATH) == 0:
    THISPATH = '.'

libname = dict()
v = sys.version_info
if v >= (3, 0):
    libname['linux'] = THISPATH+'/lib/_edf.cpython-{}{}m-x86_64-linux-gnu.so'.format(v[0], v[1])
    libname['linux2'] = libname['linux']
else:
    libname['linux'] = THISPATH+'/lib/_edf.so'
    libname['linux2'] = libname['linux']

libname['darwin'] = libname['linux']
libname['win32'] = THISPATH+'/edf.dll' 


# Load the library
if os.path.exists( libname[sys.platform] ):
    lib = ct.cdll.LoadLibrary( libname[sys.platform] )

else:
    raise ImportError('Unable to load library {}.'.format(libname[sys.platform]))


###


EDFLIB_MAXSIGNALS = 256
MD5_DIGEST_LENGTH = 16


class edf_hdr_struct(ct.Structure):                    # this structure contains all the relevant EDF header info and will be filled when calling the function edf_open_file_readonly()

    _fields_ = [("handle", ct.c_int),                # a handle (identifier) used to distinguish the different files
        ("filetype", ct.c_int),                    # 0 : EDF, 1 : EDFplus, 2 : BDF, 3 : BDFplus.  Negative numbers indicate errors.
        ("edfsignals", ct.c_int),                # number of EDF signals in the file, annotation channels are NOT included
        ("file_duration", ct.c_longlong),            # duration of the file expressed in units of 100 nanoSeconds
        ("startdate_day", ct.c_int),       
        ("startdate_month", ct.c_int),       
        ("startdate_year", ct.c_int),       
        ("starttime_subsecond", ct.c_longlong),            # starttime offset expressed in units of 100 nanoSeconds. Is always less than 10000000 (one second). Only used by EDFplus and BDFplus
        ("starttime_second", ct.c_int),       
        ("starttime_minute", ct.c_int),       
        ("starttime_hour", ct.c_int),       
        ("patient_b", ct.c_char*81),            # null-terminated string, contains patientfield of header, is always empty when filetype is EDFPLUS or BDFPLUS
        ("recording", ct.c_char*81),        # null-terminated string, contains recordingfield of header, is always empty when filetype is EDFPLUS or BDFPLUS
        ("patientcode", ct.c_char*81),        # null-terminated string, is always empty when filetype is EDF or BDF
        ("gender", ct.c_char*16),                   # null-terminated string, is always empty when filetype is EDF or BDF
        ("birthdate", ct.c_char*16),                # null-terminated string, is always empty when filetype is EDF or BDF
        ("patient_name", ct.c_char*81),        # null-terminated string, is always empty when filetype is EDF or BDF
        ("patient_additional", ct.c_char*81),       # null-terminated string, is always empty when filetype is EDF or BDF
        ("admincode", ct.c_char*81),                # null-terminated string, is always empty when filetype is EDF or BDF
        ("technician", ct.c_char*81),               # null-terminated string, is always empty when filetype is EDF or BDF
        ("equipment", ct.c_char*81),                # null-terminated string, is always empty when filetype is EDF or BDF
        ("recording_additional", ct.c_char*81),     # null-terminated string, is always empty when filetype is EDF or BDF
        ("datarecord_duration", ct.c_longlong),            # duration of a datarecord expressed in units of 100 nanoSeconds
        ("datarecords_in_file", ct.c_longlong),            # number of datarecords in the file
        ("annotations_in_file", ct.c_longlong),            # number of annotations in the file
        ("signalparam", edf_param_struct*EDFLIB_MAXSIGNALS)]         # array of structs which contain the relevant signal parameters

    def __init__(self, filename, md5checksum=None):
        self.opened = True
        assert os.path.exists(filename), "File '{}' does not exist.".format(filename)
        if md5checksum is not None:
            md5checksum = md5checksum.encode('utf-8')
        lib.read_my_header(filename.encode('utf-8'), self, md5checksum)
        self.patient = self.patient_b.decode('utf-8').strip(' ')

        self.channelnames  = [self.signalparam[i].label_b.decode('utf-8').strip(' ') for i in xrange(self.edfsignals)]
        self.samplingrates = np.asarray([int(self.signalparam[i].smp_in_datarecord / (self.datarecord_duration*100.*10**-9)) for i in xrange(self.edfsignals)])
        self.channeltypes  = np.asarray([get_type(self.signalparam[i]) for i in xrange(self.edfsignals)])

        start = datetime.datetime(
            year        = self.startdate_year,
            month       = self.startdate_month,
            day         = self.startdate_day,
            hour        = self.starttime_hour,
            minute      = self.starttime_minute,
            second      = self.starttime_second,
            microsecond = self.starttime_subsecond
        )
        duration = self.datarecord_duration/10**7 * self.datarecords_in_file
        self.start = State(start=start, duration=duration, annot='recording')


    def read_physical_samples(self, channels, start, size):

        channels = np.asarray(channels)

        if not channels.dtype == int:
            print("edf_file : channels.dtype has to be integer.")
            return None

        channels = np.asarray(channels, dtype=np.int32)            # By default, it's int64 which will be converted to a long by ansi-c.

        data = np.zeros((channels.size, size), float)
        lib.read_physical_samples(self.handle, channels.ctypes.data_as(ct.POINTER(ct.c_int)), channels.size, start, size, data.ctypes.data_as(ct.POINTER(ct.c_double)))

        return data


    def close(self):

        if self.opened:
            exitcode = lib.edf_close(self.handle)
            self.opened = False

            if exitcode < 0:
                print("edf_hdr_struct : problems closing file.")


    def __del__(self):
        self.close()




def read_md5(filename, separator=' '):

    f = open(filename, 'r')
    md5dict = dict()

    for line in f:
        line = line.split(separator)

        md5sum = line[0].strip(' ')
        filename_j = line[-1].strip('\n').strip(' ')
        md5dict[filename_j] = md5sum

    f.close()

    return md5dict




lib.read_my_header.argtypes = [ct.c_char_p, ct.POINTER(edf_hdr_struct), ct.c_char_p]

lib.read_physical_samples.argtypes = [ct.c_int, ct.POINTER(ct.c_int), ct.c_int, ct.c_int, ct.c_int, ct.POINTER(ct.c_double)]

lib.edf_close.argtypes = [ct.c_int]
lib.edf_close.restype = ct.c_int




if __name__ == "__main__":

    import pylab

    filename_md5 = THISPATH + "/../../example/sample.md5"
    filename_edf = THISPATH + "/../../example/sample.edf"

    #md5 = read_md5(filename=filename_md5)
    f = edf_hdr_struct(filename=filename_edf, md5checksum=None)
    

    START = 0
    SIZE = 100000
    ch = [0]

    data = f.read_physical_samples(ch, START, SIZE)

    print(data)

    pylab.plot(data[0])

    pylab.show()

    del f

    print('exiting ..')


















