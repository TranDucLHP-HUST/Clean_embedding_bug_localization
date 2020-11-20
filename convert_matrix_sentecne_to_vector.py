import pickle
import numpy as np
import tf_idf
import time

# define name file
INPUT_SOURCE = 'data/AspectJ_matrix_source.pickle'
INPUT_BUG = 'data/AspectJ_matrix_bug.pickle'
OUTPUT_SOURCE = 'data/AspectJ_vector_source.pickle'
OUTPUT_BUG = 'data/AspectJ_vector_bug.pickle'

BUG_STEMMING = 'data/AspectJ_bug_stemming.pickle'
SOURCE_STEMMING = 'data/AspectJ_source_stemming.pickle'


def for_source():
    file = open(INPUT_SOURCE, 'rb')
    matrix_input = pickle.load(file)

    # find the max sentences
    max_sentences = 0
    for each_source in matrix_input:
        max_sentences = max(max_sentences, len(each_source))
    print('Max number of sentences in source file: ', max_sentences)

    matrix_result = []
    for each_source in matrix_input:
        matrix_source = np.zeros(shape=(max_sentences, 300))
        ind = -1
        for matrix_sentence in each_source:
            ind += 1
            middle = np.zeros(300)
            if len(matrix_sentence) == 0:
                matrix_source[ind] = np.asarray(middle)
            else:
                for word in matrix_sentence:
                    middle += np.asarray(word)
                matrix_source[ind] = np.asarray(middle) / len(matrix_sentence)

        matrix_result.append(matrix_source)

    file = open(OUTPUT_SOURCE, 'wb')
    pickle.dump(matrix_result, file)
    print("After compute vector sentences, shape of matrix sources: ", np.asarray(matrix_result).shape)
    file.close()
    return matrix_result


def for_bug():
    file = open(INPUT_BUG, 'rb')
    matrix_input = pickle.load(file)

    # find the max sentences
    max_sentences = 0
    for each_source in matrix_input:
        max_sentences = max(max_sentences, len(each_source))
    print('Max number of sentences in bug reports: ', max_sentences)

    matrix_tfidf = tf_idf.compute_tfidf()

    matrix_result = []
    for each_bug in range(len(matrix_input)):
        matrix_bug = np.zeros(shape=(max_sentences, 300))
        ind = -1
        for matrix_sentence in range(len(matrix_input[each_bug])):
            ind += 1
            middle = np.zeros(300)
            if len(matrix_input[each_bug][matrix_sentence]) == 0:
                matrix_bug[ind] = np.asarray(middle)
            else:
                for word in range(len(matrix_input[each_bug][matrix_sentence])):
                    tfidf_value = matrix_tfidf[each_bug][matrix_sentence][word]  # get the tf-idf value of each word
                    middle += np.asarray(matrix_input[each_bug][matrix_sentence][word]) * tfidf_value
                matrix_bug[ind] = np.asarray(middle) / len(matrix_input[each_bug][matrix_sentence])

        matrix_result.append(matrix_bug)

    file = open(OUTPUT_BUG, 'wb')
    pickle.dump(matrix_result, file)
    print("After comput vector sentences, shape of matrix bugs: ", np.asarray(matrix_result).shape)
    file.close()
    return matrix_result


for_source()
for_bug()
