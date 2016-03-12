

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "edflib.h"
#include "edf.h"


//extern struct edfhdrblock *hdrlist[EDFLIB_MAXFILES];
//extern files_open;



void read_my_header(char *filename, struct edf_hdr_struct *hdr, const char *md5checksum)
{
	if( edfopen_file_readonly(filename, hdr, EDFLIB_READ_ALL_ANNOTATIONS, md5checksum) )	// Open the file and read out the hdr info.
	{
		switch(hdr->filetype)
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
}



void read_physical_samples(const int hdl, int *channels, const int CHANNELS, const int START, const int SIZE, double *buf)
{
	int j;

	for(j=0; j<CHANNELS; j++)
	{
		edfseek(hdl, channels[j], START, EDFSEEK_SET);				// Reel the file to START.
		edfread_physical_samples(hdl, channels[j], SIZE, &(buf[SIZE*j]));	// Read physical samples into buffer.
	}
}


int edf_close(const int handle)
{
	return edfclose_file(handle);
}


