Tutorial
========
Once the package has been installed, you can import the package as follows:

.. ipython:: python
   
   import py_stringmatching as sm
   
Computing a similarity score between two given strings **x** and **y** then typically consists of four steps: (1) selecting a similarity measure type, (2) selecting a tokenizer type, (3) creating a tokenizer object (of the selected type) and using it to tokenize the two given strings **x** and **y**, and (4) creating a similarity measure object (of the selected type) and applying it to the output of the tokenizer to compute a similarity score. We now elaborate on these steps. 

1. Selecting a Similarity Measure
----------------------------------
First, you must select a similarity measure. The package py_stringmatching currently provides a set of different measures (with plan to add more). Examples of such measures are Jaccard, Levenshtein, TF/IDF, etc. To understand more about these measures, a good place to start is the string matching chapter of the book "Principles of Data Integration". (This chapter is available on the package's homepage.)

A major group of similarity measures treats input strings as **sequences** of characters (e.g., Levenshtein, Smith Waterman). Another group treats input strings as **sets** of tokens (e.g., Jaccard). Yet another group treats input strings as **bags** of tokens (e.g., TF/IDF). A bag of tokens is a collection of tokens such that a token can appear multiple times in the collection (as opposed to a set of tokens, where each token can appear only once).

The currently implemented similarity measures include: 
  * sequence-based measures: affine gap, bag distance, editex, Hamming distance, Jaro, Jaro Winkler, Levenshtein, Needleman Wunsch, partial ratio, partial token sort, ratio, Smith Waterman, token sort.
  * set-based measures: cosine, Dice, Jaccard, overlap coefficient, Tversky Index.
  * bag-based measures: TF/IDF.
  * phonetic-based measures: soundex.
  
(There are also hybrid similarity measures: Monge Elkan, Soft TF/IDF, and Generalized Jaccard. They are so called because each of these measures uses multiple similarity measures. See their descriptions in this user manual to understand what types of input they expect.)

At this point, you should know if the selected similarity measure treats input strings as sequences, bags, or sets, so that later you can set the parameters of the tokenizing function properly (see Steps 2-3 below). 

2. Selecting a Tokenizer Type
-----------------------------
If the above selected similarity measure treats input strings as sequences of characters, then you do not need to tokenize the input strings **x** and **y**, and hence do not have to select a tokenizer type. 

Otherwise, you need to select a tokenizer type. The package py_stringmatching currently provides a set of different tokenizer types: alphabetical tokenizer, alphanumeric tokenizer, delimiter-based tokenizer, qgram tokenizer, and whitespace tokenizer (more tokenizer types can easily be added).

A tokenizer will convert an input string into a set or a bag of tokens, as discussed in Step 3. 

3. Creating a Tokenizer Object and Using It to Tokenize the Input Strings
-------------------------------------------------------------------------
If you have selected a tokenizer type in Step 2, then in Step 3 you create a tokenizer object of that type. If the intended similarity measure (selected in Step 1) treats the input strings as **sets** of tokens, then when creating the tokenizer object, you must set the flag return_set to True. Otherwise this flag defaults to False, and the created tokenizer object will tokenize a string into a **bag** of tokens. 

The following examples create tokenizer objects where the flag return_set is not mentioned, thus defaulting to False. So these tokenizer objects will tokenize a string into a bag of tokens. 

.. ipython:: python

   # create an alphabetical tokenizer that returns a bag of tokens
   alphabet_tok = sm.AlphabeticTokenizer()
    
   # create an alphanumeric tokenizer
   alnum_tok = sm.AlphanumericTokenizer()
    
   # create a delimiter tokenizer using comma as a delimiter
   delim_tok = sm.DelimiterTokenizer(delim_set=[','])
    
   # create a qgram tokenizer using q=3
   qg3_tok = sm.QgramTokenizer(qval=3)
    
   # create a whitespace tokenizer
   ws_tok = sm.WhitespaceTokenizer()

Given the string "up up and away", the tokenizer alphabet_tok (defined above) will convert it into a bag of tokens ['up', 'up', 'and', 'away'], where the token 'up' appears twice. 

The following examples create tokenizer objects where the flag return_set is set to True. Thus these tokenizers will tokenize a string into a set of tokens. 

.. ipython:: python

   # create an alphabetical tokenizer that returns a set of tokens
   alphabet_tok_set = sm.AlphabeticTokenizer(return_set=True)

   # create a whitespace tokenizer that returns a set of tokens
   ws_tok_set = sm.WhitespaceTokenizer(return_set=True)

   # create a qgram tokenizer with q=3 that returns a set of tokens
   qg3_tok_set = sm.QgramTokenizer(qval=3, return_set=True)
   
So given the same string "up up and away", the tokenizer alphabet_tok_set (defined above) will convert it into a set of tokens ['up', 'and', 'away']. 
    
All tokenizers have a **tokenize** method which tokenizes a given input string into a set or bag of tokens (depending on whether the flag return_set is True or False), as these examples illustrate:

.. ipython:: python

   test_string = ' .hello, world!! data, science, is    amazing!!. hello.'

   # tokenize into a bag of alphabetical tokens
   alphabet_tok.tokenize(test_string)

   # tokenize into alphabetical tokens (with return_set set to True)
   alphabet_tok_set.tokenize(test_string)

   # tokenize using comma as the delimiter
   delim_tok.tokenize(test_string)

   # tokenize using whitespace as the delimiter
   ws_tok.tokenize(test_string)
   
Thus, once you have created the tokenizer, you can use the **tokenize** method to tokenize the two input strings **x** and **y** (see more in Step 4 below). 

.. note::

     The **tokenize** method returns a **Python list** which represents a set of tokens or a bag of tokens, depending on whether the flag return_set is True or False. 

4. Creating a Similarity Measure Object and Using It to Compute a Similarity Score
-----------------------------------------------------------------------------------
Recall that in Step 1 you have selected a similarity measure (e.g., Jaccard, Levenshtein). In this step you start by creating a similarity measure object of the selected type, as illustrated by these examples:
 
.. ipython:: python

   # create a Jaccard similarity measure object
   jac = sm.Jaccard()
    
   # create a Levenshtein similarity measure object
   lev = sm.Levenshtein()

There are two main types of similarity measures. 

(1) Those that when given two input strings will compute a true similarity score, which is a number in the range [0,1] such that the higher this number, the more similar the two input strings are. 

(2) Those that when given two input strings will compute a distance score, which is a number such that the higher this number, the more **dissimilar** the two input strings are (this number is often not in the range [0,1]). Clearly, Type-2 measures (also known as distance measures), are the reverse of Type-1 measures. 

For example, Jaccard similarity measure will compute a true similarity score in [0,1] for two input strings. Levenshtein similarity measure, on the other hand, is really a distance measure, which computes the edit distance between the two input strings (see for example Wikipedia or the string matching chapter in the book "Principles of Data Integration"). It is easy to convert a distance score into a true similarity score (again, see examples in the above book chapter). 

Given the above, each similarity measure object in py_stringmatching is supplied with two methods: **get_raw_score** and **get_sim_score**. The first method will compute the raw score as defined by that type of similarity measures, be it similarity score or distance score. For example, for Jaccard this method will return a true similarity score, whereas for Levenshtein it will return an edit distance score. 

The method **get_sim_score** normalizes the raw score to obtain a true similarity score (a number in [0,1], such that the higher this number the more similar the two strings are). For Jaccard, **get_sim_score** will simply call **get_raw_score**. For Levenshtein, however, **get_sim_score** will normalize the edit distance to return a true similarity score in [0,1].

Here are some examples of using the **get_raw_score** method:

.. ipython:: python

   # input strings
   x = 'string matching package'
   y = 'string matching library'

   # compute Jaccard score over sets of tokens of x and y, tokenized using whitespace
   jac.get_raw_score(ws_tok_set.tokenize(x), ws_tok_set.tokenize(y))

   # compute Jaccard score over sets of tokens of x and y, tokenized into qgrams (with q=3)
   jac.get_raw_score(qg3_tok_set.tokenize(x), qg3_tok_set.tokenize(y))
    
   # compute Levenshtein distance between x and y
   lev.get_raw_score(x, y)
    
Note that in the above examples, the Jaccard measure treats the input strings as sets of tokens. And indeed, the two tokenizers ws_tok_set and qg3_tok_set as defined earlier would tokenize a string into a set of tokens. The Levenshtein measure, on the other hand, treats the input strings as sequences of characters. Hence when using it we do not have to tokenize the two strings **x** and **y**.

Here are some example of using the **get_sim_score** method:

.. ipython:: python

   # get normalized Levenshtein similarity score between x and y
   lev.get_sim_score(x, y)
    
   # get normalized Jaccard similarity score (this is the same as the raw score)
   jac.get_sim_score(ws_tok_set.tokenize(x), ws_tok_set.tokenize(y))
   
So depending on what you want, you can call **get_raw_score** or **get_sim_score**. Note, however, that certain measures such as affine gap, Monge-Elkan, Needleman-Wunsch, Smith-Waterman and Soft TF/IDF do not have a **get_sim_score** method, because there is no straightforward way to normalize the raw scores of these measures into similarity scores in [0,1] (see the Developer Manual for further explanation).

Handling a Large Number of String Pairs
---------------------------------------
Steps 1-4 above discuss the case where you want to compute the similarity score of only a single string pair. 

There are however cases where you need to compute the similarity scores of many string pairs. For example, given a table A of 10K strings and a table B of 10K strings, you may need to compute the string similarity scores for all 100M string pairs in the Cartesian product of the two tables. 

In such cases, you should avoid tokenizing the same string repeatedly, such as calling jac.get_sim_score(ws_tok_set.tokenize(x), ws_tok_set.tokenize(y)) for all pairs (x,y) in the Cartesian product. If you do this, a string x in table A will be tokenized 10K times, since it will appear in 10K pairs. This is clearly unnecessary and very expensive. 

Instead, you should tokenize all strings in tables A and B only once, store the output of tokenizing in some Python structure, then call the similarity measure on these structures to compute similarity scores. This will avoid repeated tokenizing of the same strings.

Handling Missing Values
------------------------
By "missing values" we mean cases where the values of one or more strings are missing (e.g., represented as None or NaN in Python). For example, given a row "David,,36" in a CSV file, the value of the second cell of this row is missing. So when this file is read into a data frame, the corresponding cell in the data frame will have the value NaN. Note that missing values are different from empty string values, which are represented as "". 

Handling missing values is tricky and application dependent (see the Developer Manual for a detailed discussion). For these reasons, the tokenizers and similarity measures in the package py_stringmatching do not handle missing values. If one of their input arguments is missing, they will stop, raising an error. Put differently, they expect non-missing input arguments.

Adding Prefix and Suffix to the Input String for Qgram Tokenizers
-----------------------------------------------------------------
Consider computing a similarity score between two strings "mo" and "moo" using 3gram tokenizing followed by Jaccard scoring. Tokenizing "mo" returns an empty set, because "mo" contains no 3gram. Tokenizing "moo" returns the set {"moo"}. As a result, the Jaccard score between "mo" and "moo" is 0. This is somewhat counterintuitive, because the two strings are similar. 

To address such cases, in practice it is common to add a prefix of (q-1) characters (using #) and a suffix of (q-1) characters (using $) to the input string, before generating qgram tokens. For example, "moo" will be padded to be "##moo$$", before tokenizing. The flag "padding" in qgram tokenizers can be set for this purpose (the default is True, in which case the string will be padded). 

Class Hierarchy for Tokenizers and Similarity Measures
-------------------------------------------------------
The current version implements the following class hierarchy for tokenizers:

Tokenizer                                                                       
  * DefinitionTokenizer                                                         
      * AlphabeticTokenizer                                                     
      * AlphanumericTokenizer                                                   
      * QgramTokenizer                                                          
  * DelimiterTokenizer                                                          
      * WhitespaceTokenizer 

The version implements the following class hierarchy for similarity measures: 

SimilarityMeasure                                                               
  * SequenceSimilarityMeasure                                                   
      * Affine
      * BagDistance
      * Editex                                                                  
      * HammingDistance                                                         
      * Jaro                                                                    
      * JaroWinkler                                                             
      * Levenshtein                                                             
      * NeedlemanWunsch
      * PartialRatio
      * PartialTokenSort
      * Ratio                                                         
      * SmithWaterman
      * TokenSort                                                           
  * TokenSimilarityMeasure                                                      
      * Cosine                                                                  
      * Dice                                                                    
      * Jaccard                                                                 
      * OverlapCoefficient                                                      
      * TfIdf
      * TverskyIndex                                                                   
  * HybridSimilarityMeasure
      * GeneralizedJaccard                                                     
      * MongeElkan                                                              
      * SoftTfIdf
  * PhoneticSimilarityMeasure
      * Soundex  

 
References
-----------
AnHai Doan, Alon Halevy, Zachary Ives, "Principles of Data Integration", Morgan Kaufmann, 2012. Chapter 4 "String Matching" (available on the package's homepage).
