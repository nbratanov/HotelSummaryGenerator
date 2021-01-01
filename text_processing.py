import re
import string
from os import listdir
from os.path import isfile, join
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


def process_documents():
    documents_clean = []
    documents = get_documents()
    for d in documents:
        cleaned_document = clean_document(d)
        documents_clean.append(cleaned_document)

    return documents_clean


def get_tokens_for_documents():
    tokens_for_documents = []
    clean_documents = process_documents()
    for document in clean_documents:
        tokens = get_document_tokens(document)
        filtered_tokens = get_filtered_document_tokens(tokens)
        normalized_tokens = get_normalized_tokens(filtered_tokens)
        tokens_for_documents.append(normalized_tokens)

    return tokens_for_documents


def clean_document(document):
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', document)
    # Remove Mentions
    document_test = re.sub(r'@\w+', '', document_test)
    # Lowercase the document
    document_test = document_test.lower()
    # Remove punctuations
    document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
    # Lowercase the numbers
    document_test = re.sub(r'[0-9]', '', document_test)
    # Remove the doubled space
    document_test = re.sub(r'\s{2,}', ' ', document_test)

    return document_test


def get_documents():
    directory_path = './data'
    return [f for f in listdir(directory_path) if isfile(join(directory_path, f))]


def get_document_tokens(document):
    tweet_tokenizer = TweetTokenizer()
    return tweet_tokenizer.tokenize(document)


def get_normalized_tokens(tokens):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    normalized_tokens = []
    for token in tokens:
        normalized_token = lemmatizer.lemmatize(token)
        normalized_token = stemmer.stem(token)

        normalized_tokens.append(normalized_token)

    return normalized_tokens


def get_filtered_document_tokens(tokens):
    stop_words = set(stopwords.words('english'))
    return [w for w in tokens if w not in stop_words]
