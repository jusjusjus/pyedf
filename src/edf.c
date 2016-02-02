

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "edflib.h"
#include "edf.h"


//extern struct edfhdrblock *hdrlist[EDFLIB_MAXFILES];
//extern files_open;


struct my_param_struct *alloc_params(int n)
{
	int i;
	struct my_param_struct* paramslist;

       	paramslist = (struct my_param_struct*)calloc(n, sizeof(struct my_param_struct)*EDFLIB_MAXSIGNALS);

	for(i=0; i<EDFLIB_MAXSIGNALS; i++)
	{
		paramslist[i].label = (char*)calloc(17, sizeof(char));
		paramslist[i].physdimension = (char*)calloc(9, sizeof(char));
		paramslist[i].prefilter = (char*)calloc(81, sizeof(char));
		paramslist[i].transducer = (char*)calloc(81, sizeof(char));
	}
	return paramslist;
}



void free_params(struct my_param_struct *paramslist)
{
	int i;
	for(i=0; i<EDFLIB_MAXSIGNALS; i++)
	{
		free(paramslist[i].label);
		free(paramslist[i].physdimension);
		free(paramslist[i].prefilter);
		free(paramslist[i].transducer);
	}
	free(paramslist);
}



void read_my_header(char *filename, struct my_hdr_struct *myhdr)
{
	struct edf_hdr_struct hdr;

	if( edfopen_file_readonly(filename, &hdr, EDFLIB_READ_ALL_ANNOTATIONS) )	// Open the file and read out the hdr info.
	{
		switch(hdr.filetype)
		{
			case EDFLIB_MALLOC_ERROR                : printf("\nmalloc error\n\n"); break;
			case EDFLIB_NO_SUCH_FILE_OR_DIRECTORY   : printf("\nI cannot open file %s.\n\n", filename); break;
			case EDFLIB_FILE_CONTAINS_FORMAT_ERRORS : printf("\nThe file is not EDF(+) or BDF(+) compliant.\n" "It contains format errors\n\n"); break;
			case EDFLIB_MAXFILES_REACHED            : printf("\nToo many files have been opened.\n\n"); break;
			case EDFLIB_FILE_READ_ERROR             : printf("\na read error occurred\n\n"); break;
			case EDFLIB_FILE_ALREADY_OPENED         : printf("\nfile has already been opened\n\n"); break;
			default                                 : printf("\nUnknown error.\n\n"); break;
		}
	}
	edftomy_hdr(&hdr, myhdr);
}



void read_physical_samples(const int hdl, int *channels, const int CHANNELS, const int START, const int SIZE, double *buf)
{
	int j;

	for(j=0; j<CHANNELS; j++)
	{
		printf("channels(%i) %i ..\n", j, channels[2*j]);			// It's quite fishy that channels[2*j] is valid.  Every second one is zero.
		edfseek(hdl, channels[2*j], START, EDFSEEK_SET);				// Reel the file to START.
		edfread_physical_samples(hdl, channels[2*j], SIZE, &(buf[SIZE*j]));	// Read physical samples into buffer.
	}
}


int edf_close(const int handle)
{
	return edfclose_file(handle);
}



void edftomy_hdr(struct edf_hdr_struct *hdr, struct my_hdr_struct *myhdr)
{
	int j;

	myhdr->handle = hdr->handle;                     
        myhdr->filetype = hdr->filetype;                   
        myhdr->edfsignals = hdr->edfsignals;                 
        myhdr->file_duration = hdr->file_duration;              
        myhdr->startdate_day = hdr->startdate_day;
        myhdr->startdate_month = hdr->startdate_month;
        myhdr->startdate_year = hdr->startdate_year;
        myhdr->starttime_subsecond = hdr->starttime_subsecond;        
        myhdr->starttime_second = hdr->starttime_second;
        myhdr->starttime_minute = hdr->starttime_minute;
        myhdr->starttime_hour = hdr->starttime_hour;
        strncpy(myhdr->patient, hdr->patient, 81);
        strncpy(myhdr->recording, hdr->recording, 81);              
        strncpy(myhdr->patientcode, hdr->patientcode, 81);
        strncpy(myhdr->gender, hdr->gender, 16);    
        strncpy(myhdr->birthdate, hdr->birthdate, 16);              
        strncpy(myhdr->patient_name, hdr->patient_name, 81);           
        strncpy(myhdr->patient_additional, hdr->patient_additional, 81);     
        strncpy(myhdr->admincode, hdr->admincode, 81);
        strncpy(myhdr->technician, hdr->technician, 81);             
        strncpy(myhdr->equipment, hdr->equipment, 81);              
        strncpy(myhdr->recording_additional, hdr->recording_additional, 81);   
	myhdr->datarecord_duration = hdr->datarecord_duration;
        myhdr->datarecords_in_file = hdr->datarecords_in_file;
        myhdr->annotations_in_file = hdr->annotations_in_file;

	for(j=0; j<hdr->edfsignals; j++)
	{
        	strncpy(myhdr->signalparam[j].label, hdr->signalparam[j].label, 17);
        	strncpy(myhdr->signalparam[j].physdimension, hdr->signalparam[j].physdimension, 9);   
        	strncpy(myhdr->signalparam[j].prefilter, hdr->signalparam[j].prefilter, 81);
        	strncpy(myhdr->signalparam[j].transducer, hdr->signalparam[j].transducer, 81);
		myhdr->signalparam[j].smp_in_file = hdr->signalparam[j].smp_in_file;
		myhdr->signalparam[j].phys_max = hdr->signalparam[j].phys_max;
		myhdr->signalparam[j].phys_min = hdr->signalparam[j].phys_min;
		myhdr->signalparam[j].dig_max = hdr->signalparam[j].dig_max;
		myhdr->signalparam[j].dig_min = hdr->signalparam[j].dig_min;
		myhdr->signalparam[j].smp_in_datarecord = hdr->signalparam[j].smp_in_datarecord;	
	}
	return;
}



void mytoedf_hdr(struct my_hdr_struct *hdr, struct edf_hdr_struct *myhdr)
{
	int j;
	hdr->handle = myhdr->handle;                     
        hdr->filetype = myhdr->filetype;                   
        hdr->edfsignals = myhdr->edfsignals;                 
        hdr->file_duration = myhdr->file_duration;              
        hdr->startdate_day = myhdr->startdate_day;
        hdr->startdate_month = myhdr->startdate_month;
        hdr->startdate_year = myhdr->startdate_year;
        hdr->starttime_subsecond = myhdr->starttime_subsecond;        
        hdr->starttime_second = myhdr->starttime_second;
        hdr->starttime_minute = myhdr->starttime_minute;
        hdr->starttime_hour = myhdr->starttime_hour;
        strncpy(hdr->patient, myhdr->patient, 81);
        strncpy(hdr->recording, myhdr->recording, 81);
        strncpy(hdr->patientcode, myhdr->patientcode, 81);
        strncpy(hdr->gender, myhdr->gender, 16);                 
        strncpy(hdr->birthdate, myhdr->birthdate, 16);              
        strncpy(hdr->patient_name, myhdr->patient_name, 81);           
        strncpy(hdr->patient_additional, myhdr->patient_additional, 81);     
        strncpy(hdr->admincode, myhdr->admincode, 81);              
        strncpy(hdr->technician, myhdr->technician, 81);             
        strncpy(hdr->equipment, myhdr->equipment, 81);              
        strncpy(hdr->recording_additional, myhdr->recording_additional, 81);   
	hdr->datarecord_duration = myhdr->datarecord_duration;
        hdr->datarecords_in_file = myhdr->datarecords_in_file;
        hdr->annotations_in_file = myhdr->annotations_in_file;

	for(j=0; j<hdr->edfsignals; j++)
	{
        	strncpy(hdr->signalparam[j].label, myhdr->signalparam[j].label, 16);   
        	strncpy(hdr->signalparam[j].physdimension, myhdr->signalparam[j].physdimension, 9);
        	strncpy(hdr->signalparam[j].prefilter, myhdr->signalparam[j].prefilter, 81);
        	strncpy(hdr->signalparam[j].transducer, myhdr->signalparam[j].transducer, 81);
		hdr->signalparam[j].smp_in_file = myhdr->signalparam[j].smp_in_file;	
		hdr->signalparam[j].phys_max = myhdr->signalparam[j].phys_max;	
		hdr->signalparam[j].phys_min = myhdr->signalparam[j].phys_min;	
		hdr->signalparam[j].dig_max = myhdr->signalparam[j].dig_max;	
		hdr->signalparam[j].dig_min = myhdr->signalparam[j].dig_min;	
		hdr->signalparam[j].smp_in_datarecord = myhdr->signalparam[j].smp_in_datarecord;	
	}
	return;
}

