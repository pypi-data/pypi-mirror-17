/*-
 * Copyright (c) 1991, 1993
 *	The Regents of the University of California.  All rights reserved.
 *
 * This code is derived from software contributed to Berkeley by
 * David Hitz of Auspex Systems, Inc.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. All advertising materials mentioning features or use of this software
 *    must display the following acknowledgement:
 *	This product includes software developed by the University of
 *	California, Berkeley and its contributors.
 * 4. Neither the name of the University nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

 /* 1999-02-22 Arkadiusz Mi¶kiewicz <misiek@pld.ORG.PL>
  * - added Native Language Support
  */

/*
This code hacked by Markus Demleitner to make it into a Python
Extension type.
*/

#undef DEBUG

/*
 * look -- find lines in a sorted list.
 * 
 * The man page said that TABs and SPACEs participate in -d comparisons.
 * In fact, they were ignored.  This implements historic practice, not
 * the manual page.
 */

#include <sys/types.h>
#include <sys/mman.h>
#include <sys/stat.h>

#include <limits.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>
#include <getopt.h>
#include <locale.h>

#include <Python.h>

#define	EQUAL		0
#define	GREATER		1
#define	LESS		(-1)

staticforward PyTypeObject Lookertype;

typedef struct {
	PyObject_HEAD
	int dflag, fflag;
	int stringlen;
	char *string;
	char *comparbuf;
	char *g_front,*g_back;
	int fd;
	int searchcount;
} lookerobject;

/* 
----------- Program logic, mostly taken from the original source -----------
*/

#define	SKIP_PAST_NEWLINE(p, back) \
	while (p < back && *p++ != '\n');

/*
 * Return LESS, GREATER, or EQUAL depending on how  string  compares with
 * string2 (s1 ??? s2).
 * 
 * 	o Matches up to len(s1) are EQUAL. 
 *	o Matches up to len(s2) are GREATER.
 * 
 * Compare understands about the -f and -d flags, and treats comparisons
 * appropriately.
 * 
 * The string "string" is null terminated.  The string "s2" is '\n' terminated
 * (or "s2end" terminated).
 *
 * We use strcasecmp etc, since it knows how to ignore case also
 * in other locales.
 */
static int
compare(lookerobject *self,char *s2, char *s2end) {
	int i;
	char *p;

	/* copy, ignoring things that should be ignored */
	p = self->comparbuf;
	i = self->stringlen;
	while(s2 < s2end && *s2 != '\n' && i--) {
		if (!self->dflag || isalnum(*s2))
			*p++ = *s2;
		s2++;
	}
	*p = 0;
	/* and compare */
	if (self->fflag) {
		i = strncasecmp(self->comparbuf, self->string, self->stringlen);
	} else {
		i = strncmp(self->comparbuf, self->string, self->stringlen);
	}
# ifdef DEBUG
	printf("Compared %20.20s and %20.20s: %d\n", self->comparbuf, 
			self->string, i);
#	endif
	return ((i > 0) ? LESS : (i < 0) ? GREATER : EQUAL);
}

/*
 * Find the first line that starts with string, linearly searching from front
 * to back.
 * 
 * Return NULL for no such line.
 * 
 * This routine assumes:
 * 
 * 	o front points at the first character in a line. 
 *	o front is before or at the first line to be printed.
 */
static char *
linear_search(lookerobject *self, char *front, char *back)
{
#	ifdef DEBUG
	printf("Switching to linear search.\n");
#	endif
	while (front < back) {
		switch (compare(self, front, back)) {
		case EQUAL:		/* Found it. */
			return (front);
			break;
		case LESS:		/* No such string. */
			return (NULL);
			break;
		case GREATER:		/* Keep going. */
			break;
		}
		SKIP_PAST_NEWLINE(front, back);
	}
	return (NULL);
}

/*
 * Binary search for "string" in memory between "front" and "back".
 * 
 * This routine is expected to return a pointer to the start of a line at
 * *or before* the first word matching "string".  Relaxing the constraint
 * this way simplifies the algorithm.
 * 
 * Invariants:
 * 	front points to the beginning of a line at or before the first 
 *	matching string.
 * 
 * 	back points to the beginning of a line at or after the first 
 *	matching line.
 * 
 * Base of the Invariants.
 * 	front = NULL; 
 *	back = EOF;
 * 
 * Advancing the Invariants:
 * 
 * 	p = first newline after halfway point from front to back.
 * 
 * 	If the string at "p" is not greater than the string to match, 
 *	p is the new front.  Otherwise it is the new back.
 * 
 * Termination:
 * 
 * 	The definition of the routine allows it return at any point, 
 *	since front is always at or before the line to print.
 * 
 * 	In fact, it returns when the chosen "p" equals "back".  This 
 *	implies that there exists a string is least half as long as 
 *	(back - front), which in turn implies that a linear search will 
 *	be no more expensive than the cost of simply printing a string or two.
 * 
 * 	Trying to continue with binary search at this point would be 
 *	more trouble than it's worth.
 */
static char *
binary_search(lookerobject *self, char *front, char *back)
{
	char *p;

	p = front + (back - front) / 2;
	SKIP_PAST_NEWLINE(p, back);

	/*
	 * If the file changes underneath us, make sure we don't
	 * infinitely loop.
	 */
	while (p < back && back > front) {

		if (compare(self, p, back) == GREATER)
			front = p;
		else
			back = p;
		p = front + (back - front) / 2;
		SKIP_PAST_NEWLINE(p, back);
	}
	return (front);
}

/* Return a Python list of all matching strings behind front.
This used to be print_from */
static PyObject*
collect_from(lookerobject *self, char *front, char *back, int maxMatches)
{	
	int eol;
	char *strbeg;
	int numMatches=0;

	strbeg = front;
	while (front < back && compare(self, front, back) == EQUAL) {
		if (compare(self, front, back) == EQUAL) {
			eol = 0;
			while (front < back && !eol) {
				if (*front++ == '\n')
					eol = 1;
			}
		} else
			SKIP_PAST_NEWLINE(front, back);
		numMatches++;
		if (maxMatches && numMatches>=maxMatches) {
			break;
		}
	}
	return PyString_FromStringAndSize(strbeg, front-strbeg);
}

/* A hacked version of the old C look function, to be called directly
from the python wrapper looker_look */
static PyObject*
look(lookerobject *self, int maxMatches)
{
	int ch;
	char *readp, *writep;
	char *front=self->g_front;
	char *back=self->g_back;

	/* Reformat string string to avoid doing it multiple times later. */
	if (self->dflag) {
		for (readp = writep = self->string; (ch = *readp++) != 0;) {
			if (isalnum(ch))
				*(writep++) = ch;
		}
		*writep = '\0';
		self->stringlen = writep - self->string;
	} else {
		self->stringlen = strlen(self->string);
	}

	self->comparbuf = realloc(self->comparbuf, self->stringlen+1);
	if (self->comparbuf == NULL) {	
		return PyErr_NoMemory();
	}
	front = binary_search(self, front, back);
	front = linear_search(self, front, back);
		
	return (front ?  collect_from(self, front, back, maxMatches) : 
		PyString_FromString("") );
}

/*
-------------------- Python interface, Type definition -------------------
*/

static PyObject*
looker_look(lookerobject *self, PyObject *args)
{
	int maxMatches=0;

	if (!PyArg_ParseTuple(args, "s|i", &(self->string), &maxMatches)) {
		return NULL;
	}
	return look(self, maxMatches);
}

/* Method table for the Looker class, for getattr */
static struct PyMethodDef looker_methods[]={
{"look", (PyCFunction)looker_look, METH_VARARGS, 
	"Looks for string given in argument"},
{NULL,NULL, 0, NULL},
};

/* getattr is just a dispatcher here */
static PyObject *looker_getattr(lookerobject *self, char *name)
{	
	return Py_FindMethod(looker_methods, (PyObject*)self, name);
}

/* the destructor needs to free all C allocated memory */
static void looker_destroy(lookerobject *self)
{ 
	munmap(self->g_front, self->g_back-self->g_front);
	close(self->fd);
	if (self->comparbuf) {
		free(self->comparbuf);
	}
	PyObject_Del(self);
}

static PyTypeObject Lookertype = {
	PyObject_HEAD_INIT(&PyType_Type)
	0,  /* never mind */
	"Looker", /* Name */
	sizeof(lookerobject),
	0,  /* never mind */
	(destructor)looker_destroy,
	(printfunc)0,
	(getattrfunc)looker_getattr,
	(setattrfunc)0,
	(cmpfunc)0,
	(reprfunc)0,
	0, /* as number */
	0, /* as sequence */
	0, /* as mapping */
};

/*
-------------------- Python interface, Module logic -------------------
*/

/* an auxillary function for the constructor that does the real work */
static PyObject *fillLookerObjectStruct(char *fname, int fflag, int dflag)
{	struct stat sb;
	lookerobject *self;

	self = PyObject_New(lookerobject, &Lookertype);
	if (!self) { /* If this fails, we're too hosed to even bother */
		return NULL; /* setting an error string */
	}

	if ((self->fd = open(fname, O_RDONLY, 0)) < 0 || fstat(self->fd, &sb)) {
		PyErr_SetFromErrno(PyExc_IOError);
		return NULL;
	}
	if ((void *)(self->g_front = mmap(NULL,
				  (size_t)sb.st_size,
				  PROT_READ,
				  MAP_FILE|MAP_SHARED,
				  self->fd,
				  (off_t)0)) <= (void *)0) {
		PyErr_SetFromErrno(PyExc_IOError);
		return NULL;
	}
	self->g_back = self->g_front + sb.st_size;
	self->dflag = dflag;
	self->fflag = fflag;
	self->comparbuf = NULL;
	self->string = NULL;
	self->searchcount = 0;
	return (PyObject*)self;
}

/* The constructor for our new looker type */
static PyObject *looker_new(PyObject *self, PyObject *args)
{	char *fname;
	int fflag=1, dflag=0;

	if (!PyArg_ParseTuple(args, "s|ii", &fname, &fflag, &dflag)) {
		return NULL;
	}
	return fillLookerObjectStruct(fname, fflag, dflag);
}

static PyMethodDef lookerMethods[] = {
	{"Looker", looker_new, METH_VARARGS, "Creates a new looker instance."},
	{NULL, NULL, 0, NULL},
};

void initLooker(void)
{
	Py_InitModule("Looker", lookerMethods);
}
