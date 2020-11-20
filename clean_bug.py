from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pandas as pd
import re
from nltk.tokenize import word_tokenize

# Define constance
BUG_CSV = "data/AspectJ_csv_not_trace.csv"
BUG_PROCESS = "data/AspectJ_process.csv"

stop_words = set(stopwords.words('english'))


def Start(data, check):
    inp = data

    # combine word, eg. AbcDef --> Abc & Def
    def combined_word(word):
        if word.isupper():
            return word.lower()
        else:
            char = []
            for i in range(0, len(word)):
                if word[i].islower():
                    char.append(word[i])
                else:
                    char.append(' ')
                    char.append(word[i].lower())
            words = []
            for word in word_tokenize(''.join(char)):
                words.append(word)
            result = ''
            for i in words:
                if i not in stop_words:
                    result += i + ' '
            return result

    # Tokenize sentences for description
    def tokenize_sentences(corpus):
        line = str(corpus)
        n = len(line)
        i = 0
        line_token = []
        lline = ''
        while i < n:
            lline += line[i]

            if i < n - 2:
                if (line[i] == '.') and (line[i + 2] == line[i + 2].upper()) and (line[i + 1].isdigit() == False):
                    line_token.append(lline)
                    lline = ''
            i += 1
        if lline != '':
            line_token.append(lline)
        return line_token

    # Data pre-processing
    # process the summary text
    text = inp['summary'].values
    text1_save = []
    index = -1
    for y1 in text:
        index += 1
        if check[index] in ['resolved fixed', 'verified fixed', 'closed fixed']:
            line_after = ''
            y1 = re.sub(r'\W', ' ', y1)  # remove puntuaction
            y1 = re.sub(r'\d', ' ', y1)  # remove digits
            words = y1.split()
            line = ''
            for word in words:
                word1 = word.lower()
                if word1 not in stop_words:
                    if word.islower():
                        word = word.capitalize()
                    line += combined_word(word)
                    line += ' '
            words = line.split()
            for w1 in words:
                if len(w1) != 1:  # if w1 is a character then delete
                    line_after += ' '
                    line_after += w1
            text1_save.append(line_after.lower())

    # precess the description text
    text = inp['description'].values
    text2_save = []
    index = -1
    for row in text:
        index += 1
        if check[index] in ['resolved fixed', 'verified fixed', 'closed fixed']:
            if type(row) == str:
                x = tokenize_sentences(row)
                line_after = ''
                for y1 in x:
                    y1 = re.sub(r'\W', ' ', y1)  # remove puntuaction
                    y1 = re.sub(r'\d', ' ', y1)  # remove digits
                    line = ''
                    words = y1.split()
                    line = ''
                    for word in words:
                        word1 = word.lower()
                        if word1 not in stop_words:
                            if word.islower():
                                word = word.capitalize()
                            line += combined_word(word)
                            # line+=word
                            line += ' '

                    words = line.split()

                    for w1 in words:
                        if len(w1) != 1:  # if w1 is a character then delete
                            line_after += ' '
                            line_after += w1
                    line_after += '.'
                text2_save.append(line_after.lower())
            else:
                text2_save.append('')

    x = pd.DataFrame({'summary': text1_save, 'description': text2_save})
    print("Number of bugs: ", len(text1_save), len(text2_save))
    x.to_csv(BUG_PROCESS)
