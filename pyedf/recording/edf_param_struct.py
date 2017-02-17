#!/usr/bin/python

import ctypes as ct

class edf_param_struct(ct.Structure):                    # this structure contains all the relevant EDF-signal parameters of one signal

    _fields_ = [("label_b", ct.c_char*17),        # label (name) of the signal, null-terminated string
        ("smp_in_file", ct.c_longlong),             # number of samples of this signal in the file
        ("phys_max", ct.c_double),                  # physical maximum
        ("phys_min", ct.c_double),                  # physical minimum
        ("dig_max", ct.c_int),                         # digital maximum
        ("dig_min", ct.c_int),                        # digital minimum
        ("smp_in_datarecord", ct.c_int),            # number of samples of this signal in a datarecord
        ("physdimension_b", ct.c_char*9),        # physical dimension (uV, bpm, mA, etc.), null-terminated string
        ("prefilter_b", ct.c_char*81),        # null-terminated string
        ("transducer_b", ct.c_char*81)]        # null-terminated string
