/* 
 *  File:     ctrigramodule.c
 * 
 *  Project:  ADS reference handling
 *
 *  Description: 
 *     Functions to handle a trigram index
 *
 *  Author:   Markus Demleitner
 *
 */

/*
 * $Log:$
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Python.h>

#define MAX_CHAR 255
#define INDL_CHUNKSIZE 400
#define maxlen  151

typedef struct {   
   unsigned short ind;
   float          hits;
} trighit_t;

/*
 * Static Globals
 *  ( it would good if they dissapear from module ) 
 */
static trighit_t       *trighits;
static unsigned short   numstrings=0;
static unsigned short **theindex;

static char           **stringlist;
static char            *indexchars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 &";
static int              usedchars;

static unsigned char    charind[MAX_CHAR+1];


/*
 * Function declaration
 */
static int         WLD           (char *word, char *sample, int limit);
static void        buildcharind  (void) ;
static int         trigind       (unsigned char *trig);
static int         ind_add       (unsigned short **indlist,
                                      unsigned short stringind) ;
static int         trig_add      (char *str,unsigned short **theindex,
                                      unsigned short stringind);
static PyObject *  buildind      (PyObject *self,PyObject *args);
static int         addhits       (unsigned short *hitlist) ;
static int         hitcompare    (const void* a,const void* b);
PyObject *         lookup        (PyObject *self,PyObject *args);
void               initctrigram  (void);

/*
 * Python module exported methods
 */
static PyMethodDef TrigramMethods[]=
{   
   {"buildindex",  buildind, METH_VARARGS},
   {"lookup",      lookup,   METH_VARARGS},
   {NULL, NULL}
};


/*
 *  Function:     WLD
 *
 *  Description:  from ldw module
 *                
 *
 ***********************************************/
static int 
WLD(char *word, char *sample, int limit)
{
   register int spmin,
              p,q,r,
              lm,lw,
              d1,d2,
              i,k,
              x1,x2,x3;
   char c;
  
   int  d[maxlen];

   lw = strlen (word);
   lm = strlen (sample);
   if (lw >= maxlen) lw = (maxlen-1);
   if (lm >= maxlen) lm = (maxlen-1);

   /*
    * Calculate initial values
    */
   if (*sample == '*') {
      for (k=0; k<=lw; k++) {
         d[k] = 0;
      }
   } else {
      d[0] = (*sample == 0) ? 0 : 1;
      i = (*sample == '?') ? 0 : 1;
      for (k=1; k<=lw; k++) {
         if (*sample == *(word+k-1)) {
             i = 0;
          }
          d[k] = k-1 + i;
      }
   }

   spmin = (d[0] == 0  ||  lw == 0) ?  d[0] : d[1];
   if (spmin > limit) {
       return (maxlen);
   }

  /*
   * Calculate distance matrix
   */
   for (i=2; i<=lm; i++) {
       c = *(sample+i-1);
       p = (c == '*'  ||  c == '?') ?  0 : 1;
       q = (c == '*') ?  0 : 1;
       r = (c == '*') ?  0 : 1;
       d2 = d[0];
       d[0] = d2 + q;
       spmin = d[0];

       for (k=1; k<=lw; k++) {
       /****  d[k] = Minimum of three numbers  ****/
           d1 = d2;
           d2 = d[k];
           x1 = d1 + ((c == *(word+k-1)) ?  0 : p);
           x2 = d2 + q;
           x3 = d[k-1] + r;

           if (x1 < x2) {
              x2 = x1;
           }
           d[k] = (x2 < x3) ?  x2 : x3;  
    
           if (d[k] < spmin) {
              spmin = d[k];
           }
      }

      if (spmin > limit) {
          return (maxlen);
      }
   } 
   return ((d[lw] <= limit) ?  d[lw] : maxlen); 
}


/* 
 *  Function:    buildcharind()
 *
 *  Description: fill out charind with the index of the 
 *               index in indexchars :-) 
 *
 *************************************************************/
static void 
buildcharind(void) 
{   

   int   i;
   char *ind;

   usedchars = strlen(indexchars)+1;

   for(i=0;i<MAX_CHAR;i++) {   
       ind = strchr(indexchars,i);
       if (ind) {
          charind[i] = ind-indexchars;
       } else {
          charind[i] = MAX_CHAR;
       }
   }
   
}


/* 
 * Function:    trigind(unsigned char *trig)
 *
 * Description: compute the index of the trigram trig 
 *
 * Returns:     int 
 *
 ********************************************************/
static int 
trigind(unsigned char *trig) 
{   

   int i;
   int ind = 0;
   
   for (i=0;i<3;i++) {
      if (charind[(unsigned int)trig[i]] != MAX_CHAR)
      {   
         ind *= usedchars;
         ind += charind[(unsigned int)trig[i]];
      } else {
         return -1;
      }
   }
   return ind;
}


/* 
 *  Function:    ind_add  (unsigned short **indlist,unsigned short stringind) 
 *
 *  Description: Add stringind to the index list 
 *               (an extensible array) indlist 
 *
 ********************************************************/
static int 
ind_add(unsigned short **indlist,unsigned short stringind) 
{   

   unsigned short *indp;
   int i;

   if (!*indlist) {   
       *indlist     = (unsigned short*)malloc(INDL_CHUNKSIZE*sizeof(unsigned short));
      (*indlist)[0] = INDL_CHUNKSIZE-1;
      (*indlist)[1] = stringind;
      for (i=2;i<INDL_CHUNKSIZE;i++) {
         (*indlist)[i] = 0;
      }
      return 0;
   }

   /* 
    * We only do this on initialisation, so we can take our time 
    */
   for (indp=(*indlist)+1;*indp;indp++) {
      if (*indp==stringind) {
         return 0;
      }
   }

   if (indp-*indlist==(*indlist)[0]) {   
         *indlist = (unsigned short *) realloc (*indlist,
                            ((*indlist)[0]+1+INDL_CHUNKSIZE)*sizeof(unsigned short));
        (*indlist)[0] += INDL_CHUNKSIZE;
          indp = (*indlist)+1;

          while (*indp++);

          while (indp-*indlist<=(*indlist)[0]) *indp++ = 0;

          return ind_add(indlist,stringind);
   }

   *indp = stringind;

   return 0;
}



/* 
 *  Function:      trig_add(char *str,unsigned short **theindex,
 *                        unsigned short stringind)
 *
 *  Description:  add the trigrams found in str to trigind 
 *
 *******************************************************************/
static int 
trig_add(char *str,unsigned short **theindex,unsigned short stringind)
{   
   char *cp=str,
        *ep=str;

   int   i,ind;
   
   for (i=0;i<2;i++,ep++) {
      if (!*ep) return 1;
   }

   while (*ep) {   
      ind = trigind(cp);

      if (ind>=0) ind_add(theindex+ind,stringind);

      ep++;
      cp++;
   }

   return 0;
}


/* 
 *  Function:      buildind (PyObject *self,PyObject *args) 
 * 
 *  Description:   build the index 
 * 
 ************************************************************/
static PyObject *
buildind(PyObject *self,PyObject *args)
{   
    int       i;
    char    **curstr;
    unsigned short     stringind;
    PyObject *strlist;

    if (!PyArg_ParseTuple(args,"O",&strlist)) {   
          PyErr_SetString(PyExc_ValueError,"Invalid Arguments");
          return NULL;
    }

    numstrings = PyList_Size(strlist);
    stringlist = (char **) malloc ((numstrings + 1) * sizeof(char*));

    for (i=0; i<numstrings; i++) {   
         Py_INCREF(PyList_GetItem(strlist,i));
         stringlist[i] = PyString_AsString(PyList_GetItem(strlist,i));
    }   

    stringlist[numstrings] = NULL;

    theindex = (unsigned short **) malloc ( (usedchars+1) *
                                            (usedchars+1) *
                                            (usedchars+1) *
                                            sizeof(unsigned short*));

    for (i=0; i<usedchars*usedchars*usedchars; i++) {
        theindex[i] = NULL;
    }

    stringind = 1;  /* 0 is a marker */
    curstr    = stringlist;

    while (*curstr) {   
         trig_add(*curstr,theindex,stringind);
         stringind++;
         curstr++;
    }

    trighits = malloc((numstrings+1)*sizeof(trighit_t));


    /*
    printf("Index build\n");

    for (i=0;i<numstrings;i++) {
         printf("String %d (%s) contains:\n",i,stringlist[i]);
         printf("\n");
    } 
    */

    Py_INCREF(Py_None);
    return Py_None;
}


/* 
 * Function:    addhits(unsigned short *hitlist) 
 *
 * Description: Add hits
 *
 **********************************************************/
static int 
addhits(unsigned short *hitlist) 
{   
   unsigned short *hp=hitlist;

   if (!hp) return 0;

   hp++;

   while (*hp) { 
      trighits[*hp++-1].hits++;
   }

   return 0;
}


/* 
 * Function:    hitcompare(const void* a,const void* b)
 *
 * Description: Compare hits
 *
 **********************************************************/
static int 
hitcompare(const void* a,const void* b)
{   
   if (((trighit_t*)b)->hits<((trighit_t*)a)->hits)
      return -1;
   return 1;
}


/* 
 * Function:    lookup (PyObject *self,PyObject *args)
 *
 * Description: Look up a word in the index 
 *
 **********************************************************/
PyObject *
lookup(PyObject *self,PyObject *args)
{   
   char      *cp,
             *ep;
   int        i;
   char      *str;
   int        ind;
   int        nummatches=10;

   int        origlen,
              maxtrigs,
              numsuspect,
              minhits;

   double     delta;
   trighit_t *curhit;
   PyObject  *reslist;

   if (!PyArg_ParseTuple(args,"si",&str,&nummatches)) {   
        PyErr_SetString(PyExc_ValueError,"Invalid arguments");
        return NULL;
   }

   cp = ep = str;

   /* Trighits will contain how many trigrams from the corresponding
	 template string are found in the lookup string.  We initialize them
	 all to zero so we can add into them later. */
   for (i=0;i<=numstrings;i++) {   
        trighits[i].ind = i;
        trighits[i].hits = 0;
   }

   /* We can't do strings shorter than three characters.  ep points
	 to the end of the current trigram */
   for (i=0;i<2;i++,ep++) {
      if (!*ep) {   
          PyErr_SetString(PyExc_ValueError,"Short string");
          return NULL;
      }
   }

   /* For each trigram until the end of the string, add one to
	 each template string hit counter that contains the trigram */
   while (*ep) {
       ind = trigind(cp);
       if (ind>=0) addhits(theindex[ind]);
       ep++;
       cp++;
   }

   /* Sort the trighits array.  Shortly we will nuke all hopeless cases,
	 and that's why we need the array sorted. */
   qsort(trighits,numstrings,sizeof(trighit_t),hitcompare);

   /* If we have no hits at all, we give up */
   if (trighits[0].hits<0.1) return Py_BuildValue("");

   minhits = trighits[0].hits/2;

   if (0==minhits) minhits = 1;

   curhit   = trighits;
   origlen  = strlen(str);
   maxtrigs = strlen(str);

   /* Normalize the number of hits to the number of trigrams in 
	 the lookup string and the length of the respective template 
	 string (because longer template strings will of course have
	 more trigrams and thus would yield higher scores) */
   while (curhit->hits>=minhits) { 
      delta = abs((strlen(stringlist[curhit->ind])-origlen)) / maxtrigs;

      if (delta<0) delta = 0;

      curhit->hits = curhit->hits/maxtrigs-delta;
      curhit++;
   }

   numsuspect = curhit-trighits;

   /* Now sort again, pushing up the templates with the best
	 normalized scores */
   qsort(trighits,numsuspect,sizeof(trighit_t),hitcompare);

   /* Now compute a normalized levenshtein distance for the numsuspect
	 best hits and combine that with the number of hits.  This is
	 complete bullshit in theory but works quite well in practice */
   curhit = trighits;
   for (i=0;i<numsuspect;i++) { 
       curhit->hits = 1-(1-curhit->hits) *
                 (float) WLD(stringlist[curhit->ind],str,maxlen/3)/origlen;

       if (curhit->hits<0) curhit->hits = 0;

       curhit++;
   }

   qsort(trighits,numsuspect,sizeof(trighit_t),hitcompare);

   if (numsuspect>nummatches) numsuspect = nummatches;

   /* Finally, get the indices of the best matching templates from
	 the trighit_ts, build python strings from them and return the
	 result. */
   reslist = PyList_New(nummatches);

   for (i=0;i<nummatches;i++) {
     PyList_SetItem(reslist,i,Py_BuildValue("sf",
       stringlist[trighits[i].ind],trighits[i].hits));
   }

   return reslist;
}


/*
 * Init python module
 */
void 
initctrigram(void)
{ 
    Py_InitModule("ctrigram",TrigramMethods);
    buildcharind();
}
