#ifndef EDF_INCLUDED
#define EDF_INCLUDED

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


extern int files_open;
extern struct edfhdrblock *hdrlist[EDFLIB_MAXFILES];


void read_my_header(char *filename, struct edf_hdr_struct *myhdr);
void read_physical_samples(const int hdl, int *channels, const int CHANNELS, const int START, const int SIZE, double *buf);
int close_edf(const int);

#endif
