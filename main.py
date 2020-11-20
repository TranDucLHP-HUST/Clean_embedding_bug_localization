import pandas as pd
import clean_bug
import clean_source
import word_embedding
import convert_matrix_sentecne_to_vector

# Define constance
BUG_CSV = "data/AspectJ_csv_not_trace.csv"
SOURCE = 'data/sourceFile_aspectj'

if __name__ == '__main__':
    # Read file csv and Extract summary and description
    inp = pd.read_csv(BUG_CSV)
    x = inp[['summary', 'description']]
    check = inp['status']
    # Bug pre-processing
    clean_bug.Start(x,check)
    print("Ok, cleaned bug!")

    # Extract AST for source and clean
    clean_source.preprocessing_source(SOURCE)
    print("Ok, cleaned source!")

    # Word embedding with fasttext pretrain
    word_embedding.word_embedding()

    # using tfidf to vectorized sentence
    convert_matrix_sentecne_to_vector.for_bug()
    convert_matrix_sentecne_to_vector.for_source()

