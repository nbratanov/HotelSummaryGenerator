import heapq

import nltk
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TweetTokenizer

from utilities import get_reviews_collection, get_cleaned_text

nltk.download('stopwords')
nltk.download('wordnet')

""" Generate summary for single document """


def get_summary_for_documents(hotel_id):
    reviews = get_reviews_collection(hotel_id)
    document_text = ""
    for review in reviews:
        document_text += review[0] + "\n"

    processed_documents = process_documents(document_text, True)
    word_frequencies = get_weighted_word_frequencies(get_document_tokens(processed_documents[0]))

    document_sentences = sent_tokenize(processed_documents[0])
    sentence_scores = get_sentences_score(document_sentences, word_frequencies)
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)

    frequency_summary = ""
    for sentence_index in summary_sentences:
        print(document_sentences[sentence_index])
        frequency_summary += document_sentences[sentence_index] + "\n"

    return frequency_summary


def process_documents(document_text, should_clean_document=True):
    documents_clean = []
    text_to_append = document_text
    if should_clean_document:
        text_to_append = get_cleaned_text(document_text, False)
    documents_clean.append(text_to_append)

    return documents_clean


def get_longest_sentence(document_tokenized_sentences):
    longest_sentence_length = 0
    for sentence in document_tokenized_sentences:
        if len(sentence) > longest_sentence_length:
            longest_sentence_length = len(sentence)
    return longest_sentence_length


def get_sentences_score(document_sentences, word_frequencies):
    sentence_scores = {}
    longest_sentence_length = get_longest_sentence(document_sentences)
    for index, sentence in enumerate(document_sentences):
        tokenized_sentence = get_tokenized_sentence(sentence)

        single_sentence_score = (longest_sentence_length - len(tokenized_sentence)) * 0.5
        if tokenized_sentence:
            for word in tokenized_sentence[0]:
                if word in word_frequencies.keys():
                    single_sentence_score += word_frequencies[word]
        sentence_scores[index] = single_sentence_score

    return sentence_scores


def get_tokenized_sentence(sentence):
    tokenized_sentence = []
    if '?' not in sentence and len(sentence) > 4:
        tokens = get_document_tokens(sentence)
        filtered_tokens = get_filtered_document_tokens(tokens)
        normalized_tokens = get_normalized_tokens(filtered_tokens)
        tokenized_sentence.append(normalized_tokens)

    return tokenized_sentence


def get_word_frequencies(tokens):
    filtered_tokens = get_filtered_document_tokens(tokens)
    normalized_tokens = get_normalized_tokens(filtered_tokens)
    token_frequencies = {}
    for token in normalized_tokens:
        if token not in token_frequencies.keys():
            token_frequencies[token] = 1
        else:
            token_frequencies[token] += 1

    return token_frequencies


def get_weighted_word_frequencies(tokens):
    word_frequencies = get_word_frequencies(tokens)
    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    return word_frequencies


def get_document_tokens(document):
    tweet_tokenizer = TweetTokenizer()
    return tweet_tokenizer.tokenize(document)


def get_normalized_tokens(tokens):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    normalized_tokens = []
    for token in tokens:
        lemmatized_token = lemmatizer.lemmatize(token)
        normalized_token = stemmer.stem(lemmatized_token)

        normalized_tokens.append(normalized_token)

    return normalized_tokens


def get_filtered_document_tokens(tokens):
    stop_words = set(stopwords.words('english'))
    return [w for w in tokens if w not in stop_words]
