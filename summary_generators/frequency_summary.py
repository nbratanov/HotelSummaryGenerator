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


def get_summary_for_documents(filePath):
    with open('./data/hotel_amira_istanbul.txt', 'r', encoding="utf-8-sig") as document_text:
        parsed_text = document_text.read()
        word_frequencies = get_weightened_word_frequency(get_document_tokens(parsed_text))
        processed_documents = process_documents(parsed_text, True)
        for document in processed_documents:
            document_sentences = sent_tokenize(document)
    print(document_sentences[9001])
    print(document_sentences[12562])
    sentence_scores = get_sentences_score(document_sentences, word_frequencies)
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    for sentence_index in summary_sentences:
        print(document_sentences[sentence_index])


def process_documents(document_text, should_clean_document=True):
    documents_clean = []
    documents = get_documents()
    for d in documents:
        if should_clean_document:
            text_to_append = clean_document(document_text)
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
        single_sentence_score = 0
        if len(tokenized_sentence) < longest_sentence_length:
            single_sentence_score = 0.000005
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


def get_weightened_word_frequency(tokens):
    word_frequencies = get_word_frequencies(tokens)
    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

    return word_frequencies


def clean_document(document):
    # Remove Unicode
    cleaned_document = re.sub(r'[^\x00-\x7F]+', ' ', document)
    # Remove Mentions
    cleaned_document = re.sub(r'@\w+', '', cleaned_document)
    cleaned_document = re.sub(r'\\u.{4}', '', cleaned_document)
    cleaned_document = re.sub(r'\\n', '', cleaned_document)
    cleaned_document = re.sub(r'\\', ' ', cleaned_document)

    # Lowercase the document
    cleaned_document = cleaned_document.lower()
    # Remove punctuations
    #cleaned_document = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', cleaned_document)
    # Lowercase the numbers
    cleaned_document = re.sub(r'[0-9]', '', cleaned_document)
    # Remove the doubled space
    cleaned_document = re.sub(r'\s{2,}', ' ', cleaned_document)

    return cleaned_document


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
        lemmatized_token = lemmatizer.lemmatize(token)
        normalized_token = stemmer.stem(lemmatized_token)

        normalized_tokens.append(normalized_token)

    return normalized_tokens


def get_filtered_document_tokens(tokens):
    stop_words = set(stopwords.words('english'))
    return [w for w in tokens if w not in stop_words]
