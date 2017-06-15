# cython: boundscheck=False

from __future__ import division

from py_stringmatching.similarity_measure.cython.cython_jaro import jaro



cdef inline int int_min(int a,int b):
    """Finds the minimum integer of the given two integers.

    Args:
        integer1,integer2 (int): Input integers.

    Returns:
        Minimum integer (int).

    """
    if a > b : return b
    else: return a

def jaro_winkler(unicode string1, unicode string2, float prefix_weight):
    """Function to find the Jaro Winkler distance between two strings.

    Args:string1,string2 (unicode), prefix_weight (float): Input strings and prefix weight.

    Returns: Jaro Winkler distance score (float)


    """
    cdef int i = 0
    cdef float jw_score = jaro(string1,string2)
    cdef int min_len = int_min(len(string1),len(string2))
    cdef int j = int_min(min_len,4)

    #Finding the jaro winkler distance between two strings
    while i < j and string1[i] == string2[i] and string1[i]:
        i += 1
    if i!=0:
        jw_score += i* prefix_weight * (1-jw_score)

    return jw_score

