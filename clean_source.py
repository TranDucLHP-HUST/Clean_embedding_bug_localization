import javalang
import ntpath
import nltk
import glob
import csv
import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

nltk.download("punkt")
stop_words = set(stopwords.words('english'))

# define name file
SOURCE_PROCESS = 'data/AspectJ_source_process.csv'


def getName(file):
    return ntpath.basename(file)


def get_name_not_commit(file):
    name = ntpath.basename(file)
    return name.split(' ')[1]


# function read folder
def openFolder(path, files, agr):
    files.extend(glob.glob(os.path.join(path, agr)))
    for file in os.listdir(path):
        fullpath = os.path.join(path, file)
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            openFolder(fullpath, files, agr)


def clean(link):
    path = os.path.normpath(link)
    token = path.split(os.sep)
    return link.replace()


def combined_word(words):
    # clean the methods, classes
    y1 = re.sub(r'\W', ' ', words)  # remove puntuaction
    y1 = re.sub(r'_', ' ', y1)  # remove puntuaction
    word = re.sub(r'\d', ' ', y1)  # remove digits

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


def process_link(link):
    link = link.replace('\\', '/')
    path = os.path.normpath(link)
    token = path.split(os.sep)
    link = link.replace(token[0], '')
    link = link[1:]
    path = os.path.normpath(link)
    token = path.split(os.sep)
    link = link.replace(token[0], '')
    return link[1:]


def preprocessing_source(source):
    name_source = []
    with open(SOURCE_PROCESS, 'w') as csv_file:
        fieldnames = ['name_file', 'classes', 'methods']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        name_files = []
        openFolder(source, name_files, "*.java")

        for name_file in name_files:
            if 'Test' not in get_name_not_commit(name_file):
                try:
                    classes = []
                    methods = []
                    with open(name_file, 'r') as f:
                        source = f.readlines()
                    f.close()
                    if len(source) == 0:
                        continue
                    source = ' '.join(source)
                    source += '\n'
                    try:
                        tree = javalang.parse.parse(source)
                    except javalang.parser.JavaSyntaxError:
                        continue
                    for x, y in tree.filter(javalang.tree.ClassDeclaration):
                        classes.append(combined_word(y.name))
                    for a, b in tree.filter(javalang.tree.MethodDeclaration):
                        if b.name not in methods:
                            methods.append(combined_word(b.name))
                    name_source.append(process_link(name_file))

                    name = getName(name_file)
                    writer.writerow({'name_file': name, 'classes': classes, 'methods': methods})
                except UnicodeDecodeError:
                    continue
    f = open('data/Aspectj_name_full_link.pickle', 'wb')
    print("Number of sources: ", len(name_source))
    pickle.dump(name_source, f)


