import os.path

import pandas as pd
from openpyxl import load_workbook

import benchmarks.benchmark as bm
from py_stringmatching.similarity_measure.affine import Affine
from py_stringmatching.similarity_measure.bag_distance import BagDistance
from py_stringmatching.similarity_measure.editex import Editex
from py_stringmatching.similarity_measure.hamming_distance import HammingDistance
from py_stringmatching.similarity_measure.jaro import Jaro
from py_stringmatching.similarity_measure.jaro_winkler import JaroWinkler
from py_stringmatching.similarity_measure.levenshtein import Levenshtein
from py_stringmatching.similarity_measure.needleman_wunsch import NeedlemanWunsch
from py_stringmatching.similarity_measure.smith_waterman import SmithWaterman
# token based similarity measures
from py_stringmatching.similarity_measure.cosine import Cosine
from py_stringmatching.similarity_measure.dice import Dice
from py_stringmatching.similarity_measure.jaccard import Jaccard
from py_stringmatching.similarity_measure.overlap_coefficient import OverlapCoefficient
from py_stringmatching.similarity_measure.soft_tfidf import SoftTfIdf
from py_stringmatching.similarity_measure.tfidf import TfIdf
from py_stringmatching.similarity_measure.tversky_index import TverskyIndex
# hybrid similarity measures
from py_stringmatching.similarity_measure.generalized_jaccard import GeneralizedJaccard
from py_stringmatching.similarity_measure.monge_elkan import MongeElkan
#phonetic similarity measures
from py_stringmatching.similarity_measure.soundex import Soundex

df1 = pd.read_csv('Short_benchmark.csv', encoding='latin')
df2 = pd.read_csv('Medium_benchmark.csv', encoding='latin')
df3 = pd.read_csv('Long_benchmark.csv', encoding='latin')

short_setA = df1['SET A']
short_setB = df1['SET B']
medium_setA = df2['SET A']
medium_setB = df2['SET B']
long_setA = df3['SET A']
long_setB = df3['SET B']




measures = {
# sequence based similarity measures
#     'Affine' : Affine,
    # 'BagDistance' : BagDistance,
    # 'Editex' : Editex,
    # 'HammingDistance' : HammingDistance,
    # 'Jaro': Jaro,
    'JaroWinkler' : JaroWinkler,
    # 'Levenshtein' : Levenshtein,
    # 'NeedlemanWunsch' : NeedlemanWunsch,
    # 'SmithWaterman' : SmithWaterman,
# # token based similarity measures
#     'Cosine' : Cosine,
#     'Dice' : Dice,
#     'Jaccard' : Jaccard,
#     'OverlapCoefficient': OverlapCoefficient,
#     'SoftTfIdf' : SoftTfIdf,
#     'TfIdf' : TfIdf,
#     'TverskyIndex' : TverskyIndex,
# # hybrid similarity measures
#     'GeneralizedJaccard' : GeneralizedJaccard,
#     'MongeElkan' : MongeElkan,
# #phonetic similarity measures
#     'Soundex' : Soundex

}

bm_size = [10, 20, 40, 80, 160]
# bm_size = [10]

new_index = ['short_short', 'short_medium', 'short_long', 'medium_medium', 'medium_long', 'long_long']
writer = pd.ExcelWriter('benchmark.xlsx')
if os.path.isfile('benchmark.xlsx'):
    book = load_workbook('benchmark.xlsx')
    writer.book = book

for measure in measures.items():
    # print(str(measure[0]))
    df = pd.DataFrame()
    for size in bm_size:

        bm_list = []
        x = bm.benchmark()
        x.set_bm_pairs(size)
        # l.append(x.get_benchmark(Jaro(), short_setA, short_setB)[0])
        # Benchmark for short-short
        bm_list.append(x.get_benchmark(measure[1](), short_setA, short_setB)[0])

        # Benchmark for short-medium
        bm_list.append(x.get_benchmark(measure[1](), short_setA, medium_setA)[0])

        # Benchmark for short-long
        bm_list.append(x.get_benchmark(measure[1](), short_setA, long_setA)[0])

        # Benchmark for medium-medium
        bm_list.append(x.get_benchmark(measure[1](), medium_setA, medium_setB)[0])

        # Benchmark for medium-long
        bm_list.append(x.get_benchmark(measure[1](), medium_setA, long_setA)[0])

        # Benchmark for long-long
        bm_list.append(x.get_benchmark(measure[1](), long_setA, long_setB)[0])

        temp_df = pd.DataFrame({str(size): bm_list}, index=new_index)
        # print(temp_df)
        df = pd.concat([df, temp_df], axis=1)
        # print(df)

    # print(df)
    df.to_excel(writer, str(measure[0])+'.xlsx')
    writer.save()
    #
