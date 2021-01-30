import re
import string
from os import listdir
from os.path import isfile, join
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import sent_tokenize
import heapq
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')


def process_documents(should_clean_document=True):
    documents_clean = []
    documents = get_documents()
    for d in documents:
        with open('./data/' + d, 'r', encoding="utf-8-sig") as document_text:
            text_to_append = document_text.read()
            if should_clean_document:
                text_to_append = clean_document(text_to_append)
            documents_clean.append(text_to_append)

    return documents_clean


def get_summary_for_documents(sentences):
    sentence_scores = get_sentences_score()
    print(sentence_scores)
    summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
    print(summary_sentences)
    for sentence_index in summary_sentences:
        for word in sentences[sentence_index]:
            print(word, end=" ", flush=True)


def get_longest_sentence(document_tokenized_sentences):
    longest_sentence_length = 0
    for sentence in document_tokenized_sentences:
        if len(sentence) > longest_sentence_length:
            longest_sentence_length = len(sentence)
    return longest_sentence_length


def get_sentences_score():
    sentence_scores = {}
    with open('./data/hotel amira istanbul.txt', 'r', encoding="utf-8-sig") as document_text:
        word_frequencies = get_weightened_word_frequency(get_document_tokens(document_text.read()))
        document_tokenized_sentences = get_tokenized_sentences_for_documents()
        longest_sentence_length = get_longest_sentence(document_tokenized_sentences)
        print(word_frequencies)
        for index, sentence in enumerate(document_tokenized_sentences):
            single_sentence_score = 0
            if len(sentence) < longest_sentence_length:
                single_sentence_score = 0.1

            for word in sentence:
                if word in word_frequencies.keys():
                    # if sentence not in sentence_scores.keys():
                    #     single_sentence_score = word_frequencies[word]
                    # else:
                    single_sentence_score += word_frequencies[word]
            sentence_scores[index] = single_sentence_score

    #TO DO: Create a map of sentences and scores here

    return sentence_scores


def get_tokenized_sentences_for_documents():
    document_senteces = []
    processed_documents = process_documents(True)
    for document in processed_documents:
        document_sentences = sent_tokenize(document)
        for sentence in document_sentences:
            tokens = get_document_tokens(sentence)
            filtered_tokens = get_filtered_document_tokens(tokens)
            #normalized_tokens = get_normalized_tokens(filtered_tokens)
            document_senteces.append(filtered_tokens)

    return document_senteces


def get_word_frequencies(tokens):
    token_frequencies = {}
    for token in tokens:
        if token not in token_frequencies.keys():
            token_frequencies[token] = 1
        else:
            token_frequencies[token] += 1

    return token_frequencies


def get_weightened_word_frequency(tokens):
    word_frequencies = get_word_frequencies(tokens)
    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    return word_frequencies


def clean_document(document):
    # Remove Unicode
    document_test = re.sub(r'[^\x00-\x7F]+', ' ', document)
    # Remove Mentions
    document_test = re.sub(r'@\w+', '', document_test)
    # Lowercase the document
    document_test = document_test.lower()
    # Remove punctuations
    #document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
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
