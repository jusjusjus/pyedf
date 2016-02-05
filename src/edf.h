#ifndef EDF_INCLUDED
#define EDF_INCLUDED

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


extern int files_open;
extern struct edfhdrblock *hdrlist[EDFLIB_MAXFILES];


struct my_param_struct {         /* this structure contains all the relevant EDF-signal parameters of one signal */
	char   *label;              /* label (name) of the signal, null-terminated string */
	long long smp_in_file;         /* number of samples of this signal in the file */
	double phys_max;               /* physical maximum */
	double phys_min;               /* physical minimum */
	int    dig_max;                /* digital maximum */
	int    dig_min;                /* digital minimum */
	int    smp_in_datarecord;      /* number of samples of this signal in a datarecord */
	char   *physdimension;       /* physical dimension (uV, bpm, mA, etc.), null-terminated string */
	char   *prefilter;          /* null-terminated string */
	char   *transducer;         /* null-terminated string */
};


struct my_annotation_struct {   /* this structure is used for annotations */
        long long onset;        /* onset time of the event, expressed in units of 100 nanoSeconds */
        char *duration;         /* duration time, this is a null-terminated ASCII text-string */
        char *annotation; 	/* description of the event in UTF-8, this is a null terminated string */
};


struct my_hdr_struct {                     	/* this structure contains all the relevant EDF header info and will be filled when calling the function edf_open_file_readonly() */
	int       handle;                       /* a handle (identifier) used to distinguish the different files */
	int       filetype;                     /* 0: EDF, 1: EDFplus, 2: BDF, 3: BDFplus, a negative number means an error */
	int       edfsignals;                   /* number of EDF signals in the file, annotation channels are NOT included */
	long long file_duration;                /* duration of the file expressed in units of 100 nanoSeconds */
	int       startdate_day;
	int       startdate_month;
	int       startdate_year;
	long long starttime_subsecond;		/* starttime offset expressed in units of 100 nanoSeconds. Is always less than 10000000 (one second). Only used by EDFplus and BDFplus */
	int       starttime_second;
	int       starttime_minute;
	int       starttime_hour;
	char      *patient;			/* null-terminated string, contains patientfield of header, is always empty when filetype is EDFPLUS or BDFPLUS */
	char      *recording;			/* null-terminated string, contains recordingfield of header, is always empty when filetype is EDFPLUS or BDFPLUS */
	char      *patientcode;			/* null-terminated string, is always empty when filetype is EDF or BDF */
	char      *gender;			/* null-terminated string, is always empty when filetype is EDF or BDF */
	char      *birthdate;			/* null-terminated string, is always empty when filetype is EDF or BDF */
	char      *patient_name;		/* null-terminated string, is always empty when filetype is EDF or BDF */
	char      *patient_additional;		/* null-terminated string, is always empty when filetype is EDF or BDF */
	char      *admincode;			/* null-terminated string, is always empty when filetype is EDF or BDF */
	char      *technician;			/* null-terminated string, is always empty when filetype is EDF or BDF */
	char      *equipment;			/* null-terminated string, is always empty when filetype is EDF or BDF */
	char      *recording_additional;	/* null-terminated string, is always empty when filetype is EDF or BDF */
	long long datarecord_duration;		/* duration of a datarecord expressed in units of 100 nanoSeconds */
	long long datarecords_in_file;		/* number of datarecords in the file */
	long long annotations_in_file;		/* number of annotations in the file */
	struct my_param_struct *signalparam;	/* array of structs which contain the relevant signal parameters */
};

struct my_param_struct *alloc_params(void);
void free_params(struct my_param_struct*);

void read_my_header(char *filename, struct my_hdr_struct *myhdr);
void read_physical_samples(const int hdl, int *channels, const int CHANNELS, const int START, const int SIZE, double *buf);
int close_edf(const int);
void edftomy_hdr_test(struct edf_hdr_struct *hdr, struct my_hdr_struct *myhdr);
void edftomy_hdr(struct edf_hdr_struct *hdr, struct my_hdr_struct *myhdr);
void mytoedf_hdr(struct my_hdr_struct *hdr, struct edf_hdr_struct *myhdr);

#endif
