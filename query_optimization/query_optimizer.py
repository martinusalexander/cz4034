from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from spelling import correction as spell_correction

# Locate the nltk data in the project folder
import os
import nltk
nltk_data_folder = os.path.join(os.path.join(os.getcwd(), 'query_optimization'), 'nltk_data')
nltk.data.path.append(nltk_data_folder)


def optimize(original_query, do_spell_correction=True):
    # Tokenize
    query_tokens = tokenize(original_query)
    # Correct the spelling
    if do_spell_correction:
        for i in range(len(query_tokens)):
            query_tokens[i] = spell_correction(query_tokens[i])
    # Remove stopwords
    query_tokens_no_stopwords = remove_stopwords(query_tokens)
    optimized_query = ' '.join(query_tokens_no_stopwords)
    return optimized_query

def tokenize(query):
    return word_tokenize(query, language='english')

def remove_stopwords(tokens):
    cleaned_tokens = [token for token in tokens if token not in stopwords.words('english')]
    return cleaned_tokens
