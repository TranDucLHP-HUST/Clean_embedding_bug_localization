import pandas as pd
import clean_bug
import pickle
import re
import numpy as np
import time
import math

# define name file
INPUT_SOURCE = 'data/AspectJ_matrix_source.pickle'
INPUT_BUG = 'data/AspectJ_matrix_bug.pickle'
OUTPUT_SOURCE = 'data/AspectJ_vector_source.pickle'
OUTPUT_BUG = 'data/AspectJ_vector_bug.pickle'
CSV_SOURCE = 'data/AspectJ_source_process.csv'
BUG_STEMMING = 'data/AspectJ_bug_stemming.pickle'
SOURCE_STEMMING = 'data/AspectJ_source_stemming.pickle'

file = open(OUTPUT_BUG, 'rb')
matrix = pickle.load(file)
for bug in matrix:
    for i in bug:
        for j in i:
            tg = j
            if math.isnan(tg):
                print('has nan')
                exit()
