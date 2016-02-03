#! /usr/bin/python

from my_param_struct import my_param_struct
import channeltypes
import ctypes as ct
import numpy as np
import datetime
import os



try: lib = ct.cdll.LoadLibrary( os.path.dirname(__file__)+'/lib/_edf.so' )
except: lib = ct.cdll.LoadLibrary( 'lib/_edf.so' )


EDFLIB_MAXSIGNALS = 256



def STRING(size):
	return ct.cast( ct.create_string_buffer(size+1), ct.POINTER(ct.c_char*(size+1)) )



class my_hdr_struct(ct.Structure):					# this structure contains all the relevant EDF header info and will be filled when calling the function edf_open_file_readonly()

	_fields_ = [("handle", ct.c_int),				# a handle (identifier) used to distinguish the different files
		("filetype", ct.c_int),					# 0 : EDF, 1 : EDFplus, 2 : BDF, 3 : BDFplus.  Negative numbers indicate errors.
		("edfsignals", ct.c_int),				# number of EDF signals in the file, annotation channels are NOT included
		("file_duration", ct.c_longlong),			# duration of the file expressed in units of 100 nanoSeconds
		("startdate_day", ct.c_int),       
		("startdate_month", ct.c_int),       
		("startdate_year", ct.c_int),       
		("starttime_subsecond", ct.c_longlong),			# starttime offset expressed in units of 100 nanoSeconds. Is always less than 10000000 (one second). Only used by EDFplus and BDFplus
		("starttime_second", ct.c_int),       
		("starttime_minute", ct.c_int),       
		("starttime_hour", ct.c_int),       
		("patient", ct.POINTER(ct.c_char*81)),			# null-terminated string, contains patientfield of header, is always empty when filetype is EDFPLUS or BDFPLUS
		("recording", ct.POINTER(ct.c_char*81)),		# null-terminated string, contains recordingfield of header, is always empty when filetype is EDFPLUS or BDFPLUS
		("patientcode", ct.POINTER(ct.c_char*81)),		# null-terminated string, is always empty when filetype is EDF or BDF
		("gender", ct.POINTER(ct.c_char*16)),                   # null-terminated string, is always empty when filetype is EDF or BDF
		("birthdate", ct.POINTER(ct.c_char*16)),                # null-terminated string, is always empty when filetype is EDF or BDF
		("patient_name", ct.POINTER(ct.c_char*81)),		# null-terminated string, is always empty when filetype is EDF or BDF
		("patient_additional", ct.POINTER(ct.c_char*81)),       # null-terminated string, is always empty when filetype is EDF or BDF
		("admincode", ct.POINTER(ct.c_char*81)),                # null-terminated string, is always empty when filetype is EDF or BDF
		("technician", ct.POINTER(ct.c_char*81)),               # null-terminated string, is always empty when filetype is EDF or BDF
		("equipment", ct.POINTER(ct.c_char*81)),                # null-terminated string, is always empty when filetype is EDF or BDF
		("recording_additional", ct.POINTER(ct.c_char*81)),     # null-terminated string, is always empty when filetype is EDF or BDF
		("datarecord_duration", ct.c_longlong),			# duration of a datarecord expressed in units of 100 nanoSeconds
		("datarecords_in_file", ct.c_longlong),			# number of datarecords in the file
		("annotations_in_file", ct.c_longlong),			# number of annotations in the file
		("signalparam", ct.POINTER(my_param_struct))] 		# array of structs which contain the relevant signal parameters


	def __init__(self, filename):

		hdr = ct.Structure.__init__(self, 0, 0, 0, 0l, 0, 0, 0, 0l, 0, 0, 13, STRING(80), STRING(80), STRING(80), STRING(15), STRING(15), STRING(80), STRING(80), STRING(80), STRING(80), STRING(80), STRING(80),   0l, 0l, 0l, lib.alloc_params(EDFLIB_MAXSIGNALS) )

		lib.read_my_header(filename, self)

		self.fields = dict(patient=self.patient.contents.value,
				patient_name=self.patient_name.contents.value,
				admincode=self.admincode.contents.value)

		self.fields['patient'] = self.fields['patient'].strip(' ')

		self.start = datetime.datetime(year=self.startdate_year, month=self.startdate_month, day=self.startdate_day,
						hour=self.starttime_hour, minute=self.starttime_minute, second=self.starttime_second, microsecond=self.starttime_subsecond)
		
		self.channelnames = np.asarray([self.signalparam[i].label.contents.value.strip(' ') for i in xrange(self.edfsignals)])
		self.samplingrates = np.asarray([self.signalparam[i].smp_in_datarecord for i in xrange(self.edfsignals)])
		self.channeltypes = np.asarray([channeltypes.get_type(self.signalparam[i]) for i in xrange(self.edfsignals)])


	def read_physical_samples(self, channels, start, size):

		channels = np.asarray(channels)

		if not channels.dtype == int:
			print "edf_file : channels.dtype has to be integer."
			return None

		channels = np.asarray(channels, dtype=np.int32)			# By default, it's int64 which will be converted to a long by ansi-c.

		data = np.zeros((channels.size, size), float)
		lib.read_physical_samples(self.handle, channels.ctypes.data_as(ct.POINTER(ct.c_int)), channels.size, start, size, data.ctypes.data_as(ct.POINTER(ct.c_double)))

		return data


	def close(self):
		lib.free_params(self.signalparam)
		lib.edf_close(self.handle)
	

	def __del__(self):
		self.close()







lib.read_my_header.argtypes = [ct.c_char_p, ct.POINTER(my_hdr_struct)]

lib.read_physical_samples.argtypes = [ct.c_int, ct.POINTER(ct.c_int), ct.c_int, ct.c_int, ct.c_int, ct.POINTER(ct.c_double)]

lib.edf_close.argtypes = [ct.c_int]
lib.edf_close.restype = ct.c_int

lib.alloc_params.argtypes = [ct.c_int]
lib.alloc_params.restype = ct.POINTER(my_param_struct)

lib.free_params.argtypes = [ct.POINTER(my_param_struct)]






if __name__ == "__main__":

	import pylab

	f = my_hdr_struct(filename="example/sample.edf")
	

	START = 0
	SIZE = 100000
	ch = [0]

	data = f.read_physical_samples(ch, START, SIZE)

	print data

	pylab.plot(data[0])

	pylab.show()

	del f

	print 'exiting ..'


















