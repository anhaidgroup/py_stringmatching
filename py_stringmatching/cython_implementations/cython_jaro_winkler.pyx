# cython: boundscheck=False

from __future__ import division
cimport cython

import numpy as np
cimport numpy as np

from py_stringmatching.similarity_measure.jaro import Jaro

@cython.boundscheck(False)
@cython.wraparound(False)

def jaro_winkler(unicode string1, unicode string2, float prefix_weight):
    cdef int i = 0
    cdef int min_len = 0
    cdef float jw_score = Jaro().get_raw_score(string1,string2)
    min_len = min(len(string1),len(string2))
    cdef int j = min(min_len,4)
    while i < j and string1[i] == string2[i] and string1[i]:
        i += 1
    if(i==1):
        jw_score += i* prefix_weight * (1-jw_score)

    return jw_score