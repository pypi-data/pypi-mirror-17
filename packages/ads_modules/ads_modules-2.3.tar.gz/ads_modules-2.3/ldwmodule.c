/* Levenstein-Distance of two strings.  Adapted from a program by
   Jörg Michael with the following header: */
/****  Einfache Levenshtein-Distanz (p0=q0=r0=1) ****/
/****  mit Berücksichtigung von Wildcards        ****/
/****  (geschwindigkeitsoptimiertes C-Programm)  ****/
/****  Autor :  Jörg Michael, Hannover           ****/
/****  Datum :  22. Dezember 1993                ****/

/* adapted for python by msdemlei@ari.uni-heidelberg.de, Sept 98 */

#include <string.h>
#include <Python.h>

#define  maxlen  151

static int WLD (char *wort, char *muster, int limit)
{
 register int spmin,
              p,q,r,
              lm,lw,
              d1,d2,
              i,k,
              x1,x2,x3;
	char c;
	/* mm[maxlen],
	ww[maxlen];
	*/
	int  d[maxlen];

 lw = strlen (wort);
 lm = strlen (muster);
 if (lw >= maxlen) lw = (maxlen-1);
 if (lm >= maxlen) lm = (maxlen-1);

 /****  Anfangswerte berechnen ****/
 if (*muster == '*')
   {
    for (k=0; k<=lw; k++)
      {
       d[k] = 0;
      }
   }
 else
   {
    d[0] = (*muster == 0) ? 0 : 1;
    i = (*muster == '?') ? 0 : 1;
    for (k=1; k<=lw; k++)
      {
       if (*muster == *(wort+k-1))
         {
          i = 0;
         }
       d[k] = k-1 + i;
      }
   }

 spmin = (d[0] == 0  ||  lw == 0) ?  d[0] : d[1];
 if (spmin > limit)
   {
    return (maxlen);
   }

 /****  Distanzmatrix durchrechnen  ****/
 for (i=2; i<=lm; i++)
   {
    c = *(muster+i-1);
    p = (c == '*'  ||  c == '?') ?  0 : 1;
    q = (c == '*') ?  0 : 1;
    r = (c == '*') ?  0 : 1;
    d2 = d[0];
    d[0] = d2 + q;
    spmin = d[0];

    for (k=1; k<=lw; k++)
      {
       /****  d[k] = Minimum dreier Zahlen  ****/
       d1 = d2;
       d2 = d[k];
       x1 = d1 + ((c == *(wort+k-1)) ?  0 : p);
       x2 = d2 + q;
       x3 = d[k-1] + r;

       if (x1 < x2)
         {
          x2 = x1;
         }
       d[k] = (x2 < x3) ?  x2 : x3;  

       if (d[k] < spmin)
         {
          spmin = d[k];
         }
      }

    if (spmin > limit)
      {
       return (maxlen);
      }
   } 
 return ((d[lw] <= limit) ?  d[lw] : maxlen); 
}

/* compute distances between a string and a list of strings, return
a list of integer distances */
static PyObject *list_ldws(char *str,PyObject *strlist)
{	int listlen=PyList_Size(strlist);
	PyObject *intlist=PyList_New(listlen);
	int i,dist;
	char *str2;

	for (i=0;i<listlen;i++)
	{	str2 = PyString_AsString(PyList_GetItem(strlist,i));
		dist = WLD(str,str2,40);
		PyList_SetItem(intlist,i,PyInt_FromLong(dist));
	}
	return intlist;
}

	
static PyObject * ldw_ldw(PyObject *self,PyObject *args)
{ char *str1,*str2;
	PyObject *strlist;
	int dist;

	if (!PyArg_ParseTuple(args,"ss",&str1,&str2))
	{	if (!PyArg_ParseTuple(args,"sO",&str1,&strlist))
		{	PyErr_SetString(PyExc_ValueError,"Invalid arguments");
			return NULL;
		}
		else
		{	PyErr_Clear();
			return list_ldws(str1,strlist);
		}
	}
	dist = WLD(str1,str2,40);
	return Py_BuildValue("i",dist);
}

static PyMethodDef LdwMethods[]=
{	{"ldw",ldw_ldw,METH_VARARGS},
	{NULL, NULL}
};

void initldw(void)
{ Py_InitModule("ldw",LdwMethods);
}
