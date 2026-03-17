import os.path
from math import floor

import pandas as pd
from openpyxl import load_workbook

import benchmarks.custom_benchmarks.benchmark as bm
from py_stringmatching.similarity_measure.affine import Affine
from py_stringmatching.similarity_measure.bag_distance import BagDistance
# token based similarity measures
from py_stringmatching.similarity_measure.cosine import Cosine
from py_stringmatching.similarity_measure.dice import Dice
from py_stringmatching.similarity_measure.editex import Editex
# hybrid similarity measures
from py_stringmatching.similarity_measure.generalized_jaccard import GeneralizedJaccard
from py_stringmatching.similarity_measure.hamming_distance import HammingDistance
from py_stringmatching.similarity_measure.jaccard import Jaccard
from py_stringmatching.similarity_measure.jaro import Jaro
from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler
from py_stringmatching.similarity_measure.levenshtein import Levenshtein
from py_stringmatching.similarity_measure.monge_elkan import MongeElkan
from py_stringmatching.similarity_measure.needleman_wunsch import NeedlemanWunsch
from py_stringmatching.similarity_measure.overlap_coefficient import OverlapCoefficient
from py_stringmatching.similarity_measure.smith_waterman import SmithWaterman
from py_stringmatching.similarity_measure.soft_tfidf import SoftTfIdf
# phonetic similarity measures
from py_stringmatching.similarity_measure.soundex import Soundex
from py_stringmatching.similarity_measure.tfidf import TfIdf
from py_stringmatching.similarity_measure.tversky_index import TverskyIndex

# User input for dataset path and reading the csv file
df1 = pd.read_csv(str(input('Enter the short strings data set path: ')))
df2 = pd.read_csv(str(input('Enter the medium strings data set path: ')))
df3 = pd.read_csv(str(input('Enter the long strings data set path: ')))

# Converting each column in dataset to separate sets
short_setA = df1['SET A']
short_setB = df1['SET B']
medium_setA = df2['SET A']
medium_setB = df2['SET B']
long_setA = df3['SET A']
long_setB = df3['SET B']

# Dict of Current Measures
present_measures = {
    # sequence based similarity measures
    'Affine': Affine,
    'BagDistance': BagDistance,
    'Editex': Editex,
    'HammingDistance': HammingDistance,
    'Jaro': Jaro,
    'JaroWinkler': JaroWinkler,
    'Levenshtein': Levenshtein,
    'NeedlemanWunsch': NeedlemanWunsch,
    'SmithWaterman': SmithWaterman,
    # token based similarity measures
    'Cosine': Cosine,
    'Dice': Dice,
    'Jaccard': Jaccard,
    'OverlapCoefficient': OverlapCoefficient,
    'SoftTfIdf': SoftTfIdf,
    'TfIdf': TfIdf,
    'TverskyIndex': TverskyIndex,
    # hybrid similarity measures
    'GeneralizedJaccard': GeneralizedJaccard,
    'MongeElkan': MongeElkan,
    # phonetic similarity measures
    'Soundex': Soundex

}

# User input to select the measure to be benchmarked
bench_measure = input('Choose one measure to benchmark among the following available measures: Affine, BagDistance,\n' \
                      ' Editex, HammingDistance, Jaro, JaroWinkler,Levenshtein,\n\
                      NeedlemanWunsch, SmithWaterman, Cosine, Dice, Jaccard, OverlapCoefficient, SoftTfIdf, TfIdf,\n \
                      TverskyIndex, GeneralizedJaccard, MongeElkan, Soundex ')

# User input for the size of dataset to be benchmarked
if present_measures.keys().__contains__(bench_measure):
    bench_measure = present_measures.get(bench_measure)
    bm_size =input('Enter the size of the dataset to be benchmarked: ')

# Changing the index in dataframe
    new_index = ['short_short', 'short_medium', 'short_long', 'medium_medium', 'medium_long', 'long_long']
    writer = pd.ExcelWriter('benchmark.xlsx')
    if os.path.isfile('benchmark.xlsx'):
        book = load_workbook('benchmark.xlsx')
        writer.book = book

    df = pd.DataFrame()
    bm_list = []
    bench_object = bm.Benchmark()
    size = floor(bm_size/11000)
    bench_object.set_bm_pairs(size)
    # Benchmark for short-short
    bm_list.append(bench_object.get_benchmark(bench_measure(), short_setA, short_setB)[0])

    # Benchmark for short-medium
    bm_list.append(bench_object.get_benchmark(bench_measure(), short_setA, medium_setA)[0])

    # Benchmark for short-long
    bm_list.append(bench_object.get_benchmark(bench_measure(), short_setA, long_setA)[0])

    # Benchmark for medium-medium
    bm_list.append(bench_object.get_benchmark(bench_measure(), medium_setA, medium_setB)[0])

    # Benchmark for medium-long
    bm_list.append(bench_object.get_benchmark(bench_measure(), medium_setA, long_setA)[0])

    # Benchmark for long-long
    bm_list.append(bench_object.get_benchmark(bench_measure(), long_setA, long_setB)[0])

    temp_df = pd.DataFrame({str(size): bm_list}, index=new_index)
    df = pd.concat([df, temp_df], axis=1)

df.to_excel(writer, str(bench_measure[0]) + '.xlsx')
writer.save()
#
