import pandas as pd
import re
import pickle
from gensim.models import KeyedVectors
from nltk.stem import PorterStemmer
import numpy as np

ps = PorterStemmer()

# Define constance
BUG_CSV = "data/AspectJ_csv_not_trace.csv"
BUG_PROCESS = "data/AspectJ_process.csv"
SOURCE_PROCESS = 'data/AspectJ_source_process.csv'
MATRIX_SOURCE = 'data/AspectJ_matrix_source.pickle'
MATRIX_BUG = 'data/AspectJ_matrix_bug.pickle'
MODEL = 'data/wiki-news-300d-1M.vec'
BUG_STEMMING = 'data/AspectJ_bug_stemming.pickle'
SOURCE_STEMMING = 'data/AspectJ_source_stemming.pickle'


def bug_word_embedding(summary, description, model):
    bug_stemming = []   # save word stemming for tf-idf
    matrix_bug = []
    for index in range(len(summary)):
        matrix = []
        matrix_stemming = []

        # for summary
        if type(summary[index]) == str:
            matrix_sentence = []
            sentence_stemming = []
            for word in summary[index].split():
                if len(word) > 1:
                    try:
                        matrix_sentence.append(model[word])
                        sentence_stemming.append(ps.stem(word))
                    except:
                        continue
            matrix.append(matrix_sentence)
            matrix_stemming.append(sentence_stemming)

        # for description
        if type(description[index]) == str:
            for sentence in description[index].split('.'):
                if sentence != '':  # different null string
                    matrix_sentence = []
                    sentence_stemming = []
                    for word in sentence.split():
                        if len(word) > 1:
                            try:
                                matrix_sentence.append(model[word])
                                sentence_stemming.append(ps.stem(word))
                            except:
                                continue
                    matrix.append(matrix_sentence)
                    matrix_stemming.append(sentence_stemming)
        matrix_bug.append(matrix)
        bug_stemming.append(matrix_stemming)

    # dump word stemming
    file = open(BUG_STEMMING, 'wb')
    pickle.dump(bug_stemming, file)
    file.close()

    return matrix_bug


def source_word_embedding(data, model):
    source_stemming = []
    matrix_source = []
    for each_source in data:
        matrix = []
        matrix_stemming = []

        # for each line in source
        list_sentence = []
        for sentence in each_source:
            if sentence not in list_sentence:   # set the list sentence, not repeat
                list_sentence.append(sentence)
                matrix_sentence = []
                sentence_stemming = []
                for word in sentence.split():
                    if len(word) > 1:
                        try:
                            matrix_sentence.append(model[word])
                            sentence_stemming.append(ps.stem(word))
                        except:
                            continue
                matrix.append(matrix_sentence)
                matrix_stemming.append(sentence_stemming)

        matrix_source.append(matrix)
        source_stemming.append(matrix_stemming)

    # dump word stemming
    file = open(SOURCE_STEMMING, 'wb')
    pickle.dump(source_stemming, file)
    file.close()

    return matrix_source


def word_embedding():
    # load model fasttext
    model_ft = KeyedVectors.load_word2vec_format(MODEL, binary=False)

    # for bug report
    file = pd.read_csv(BUG_PROCESS)
    summary = file['summary'].values
    description = file['description'].values

    matrix_bug = bug_word_embedding(summary, description, model_ft)
    print("Shape of bug embedding: ", np.asarray(matrix_bug).shape)

    # for source
    file = pd.read_csv(SOURCE_PROCESS)
    classes = file['classes'].values
    methods = file['methods'].values
    data = []
    for index in range(len(classes)):
        # clean data source in file csv
        tg = []
        words = re.sub(r"\W", ' ', classes[index])
        words = re.sub(r"\d", '', words)
        tg.append(words)

        line = methods[index].replace("', '", '---')
        for i in line.split('---'):
            words = re.sub(r"\W", ' ', i)
            words = re.sub(r"\d", '', words)
            tg.append(words)
        data.append(tg)

    matrix_source = source_word_embedding(data, model_ft)
    print("Shape of source embedding: ", np.asarray(matrix_source).shape)

    # save in file pickle
    file = open(MATRIX_BUG, 'wb')
    pickle.dump(matrix_bug, file)
    file.close()

    file = open(MATRIX_SOURCE, 'wb')
    pickle.dump(matrix_source, file)
    file.close()

    print("Dump successfully")
