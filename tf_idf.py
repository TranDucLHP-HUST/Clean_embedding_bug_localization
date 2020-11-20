import numpy as np
import math
import pickle

# define name file
BUG_STEMMING = 'data/AspectJ_bug_stemming.pickle'


def computeTF(words):
    words_set = set(words)
    wordDict = dict.fromkeys(words_set, 0)
    for word in words:
        wordDict[word] += 1

    tf_result = []
    for w in words:
        for word, count in wordDict.items():
            if word == w:
                tf_result.append(math.log10(count) + 1)
                break
    return tf_result


def computeIDF(document, doc_list):
    idf_result = []

    for word in document:
        count = 0
        for doc in doc_list:
            if word in doc:
                count += 1
        idf_result.append(math.log10(len(doc_list) / count))

    return idf_result


def compute_tfidf():
    file = open(BUG_STEMMING, 'rb')
    bug_words = pickle.load(file)
    data = []
    for bug in bug_words:
        for sentence in bug:
            data.append(sentence)

    tfidf_result = []
    for bug in bug_words:
        bug_tfidf = []
        for sentence in bug:
            bug_tfidf.append(np.asarray(computeTF(sentence)) * np.asarray(computeIDF(sentence, data)))
        tfidf_result.append(bug_tfidf)

    return tfidf_result


print(compute_tfidf())