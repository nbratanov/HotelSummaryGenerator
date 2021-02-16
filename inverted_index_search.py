import pickle
from operator import itemgetter
from string import punctuation

import numpy as np
from nltk.tokenize import sent_tokenize, TweetTokenizer

from hotel_information.database.database_connector import DatabaseConnector
from utilities import get_cleaned_text

tokenizer = TweetTokenizer()
database = DatabaseConnector()


def preprocess_document(document):
    cleaned_text = get_cleaned_text(document, True)
    sentences = sent_tokenize(cleaned_text)
    tokens_list = []
    for sentence in sentences:
        sent_tokens = tokenizer.tokenize(sentence)
        sent_tokens = [single_token.lower() for single_token in sent_tokens if single_token not in punctuation]
        tokens_list += sent_tokens
    return tokens_list


def get_token_doc_id_pairs():
    token_docid_pair = []
    doc_ids = {}

    # documents = get_documents()
    """TODO refactor"""
    database = DatabaseConnector()
    hotels_information = database.get_hotels_information()
    hotels_information_as_strings = []
    for hotel_information in hotels_information:
        hotel_information_as_string = ""
        for info in hotel_information:
            hotel_information_as_string += str(info) + " "

        hotels_information_as_strings.append(hotel_information_as_string)

    for i, document in enumerate(hotels_information_as_strings):
        doc_ids[i] = document
        document_tokens = preprocess_document(document)
        token_docid_pair += [(token, i) for token in document_tokens]

    return sorted(token_docid_pair, key=itemgetter(0))


def get_merge_token_in_doc(sorted_token_docid_pairs):
    merged_tokens_in_doc = []
    for token, doc_id in sorted_token_docid_pairs:
        if merged_tokens_in_doc:
            prev_tok, prev_doc_id, prev_freq = merged_tokens_in_doc[-1]
            if prev_tok == token and prev_doc_id == doc_id:
                merged_tokens_in_doc[-1] = (token, doc_id, prev_freq + 1)
            else:
                merged_tokens_in_doc.append((token, doc_id, 1))
        else:
            merged_tokens_in_doc.append((token, doc_id, 1))
    return merged_tokens_in_doc


def get_dictionary():
    dictionary = {}
    sorted_token_id_pairs = get_token_doc_id_pairs()
    merged_tokens_in_doc = get_merge_token_in_doc(sorted_token_id_pairs)
    for token, doc_id, doc_freq in merged_tokens_in_doc:
        num_encounters = 1
        frequency = doc_freq
        if token in dictionary.keys() and dictionary[token][0]:
            num_encounters = dictionary[token][0] + 1
            frequency = dictionary[token][0] + doc_freq

        dictionary[token] = (num_encounters, frequency)
    return dictionary


def get_postings():
    postings = {}
    sorted_token_id_pairs = get_token_doc_id_pairs()
    merged_tokens_in_doc = get_merge_token_in_doc(sorted_token_id_pairs)
    for token, doc_id, doc_freq in merged_tokens_in_doc:
        if token in postings.keys():
            postings[token].append((doc_id, doc_freq))
        else:
            postings[token] = [(doc_id, doc_freq)]

    return postings


def create_and_save_dictionary_and_postings():
    dictionary = get_dictionary()
    postings = get_postings()
    with open('inverted_index/dictionary.pkl', 'wb') as f:
        pickle.dump(dictionary, f, pickle.HIGHEST_PROTOCOL)
    with open('inverted_index/postings.pkl', 'wb') as f:
        pickle.dump(postings, f, pickle.HIGHEST_PROTOCOL)


def load_dictionary():
    with open('inverted_index/dictionary.pkl', 'rb') as f:
        return pickle.load(f)


def load_postings():
    with open('inverted_index/postings.pkl', 'rb') as f:
        return pickle.load(f)


def and_query(word1, word2):
    postings = load_postings()
    if word1 in postings.keys() and word2 in postings.keys():
        postings_word1 = postings[word1]
        postings_word2 = postings[word2]
    else:
        return []

    return get_matching_documents_from_postings(postings_word1, postings_word2)


def get_matching_documents_from_postings(postings_word1, postings_word2):
    documents_results = []
    postings_ind1, postings_ind2 = 0, 0
    while postings_ind1 < len(postings_word1) and postings_ind2 < len(postings_word2):
        doc_id1, doc_id2 = postings_word1[postings_ind1][0], postings_word2[postings_ind2][0]
        if doc_id1 == doc_id2:
            documents_results.append(postings_word1[postings_ind1][0])
            postings_ind1 += 1
            postings_ind2 += 1
        elif doc_id1 < doc_id2:
            postings_ind1 += 1
        elif doc_id1 > doc_id2:
            postings_ind2 += 1
    return documents_results


def merge_result_with_posting(result, posting):
    documents_results = []
    postings_ind1, postings_ind2 = 0, 0
    while postings_ind1 < len(result) and postings_ind2 < len(posting):
        doc_id1, doc_id2 = result[postings_ind1], posting[postings_ind2][0]
        if doc_id1 == doc_id2:
            documents_results.append(result[postings_ind1])
            postings_ind1 += 1
            postings_ind2 += 1
        elif doc_id1 < doc_id2:
            postings_ind1 += 1
        elif doc_id1 > doc_id2:
            postings_ind2 += 1
    return documents_results


def multiple_and_operation(words_list):
    postings = load_postings()
    not_terms = {}
    postings_for_query_words = {}
    for word in words_list:
        if word[0] == '!':
            word = word[1:]
            not_terms[word] = word
        if word in postings.keys():
            postings_for_query_words[word] = postings[word]
        elif word not in not_terms.keys():
            return []

    sorted_postings = sorted(postings_for_query_words, key=lambda k: len(postings_for_query_words[k]), reverse=False)
    documents_results = get_matching_documents_from_postings(postings_for_query_words[sorted_postings[0]],
                                                             postings_for_query_words[sorted_postings[1]])
    if sorted_postings[0] in not_terms.keys() and sorted_postings[1] in not_terms.keys():
        documents_results = []
        for key in postings.keys:
            for i in range(len(postings[key])):
                documents_results.append(postings[key][i][0])

    elif sorted_postings[0] in not_terms.keys():
        encounters_list = [x[0] for x in postings[sorted_postings[1]]]
        documents_results = np.setdiff1d(encounters_list, documents_results)
    elif sorted_postings[1] in not_terms.keys():
        encounters_list = [x[0] for x in postings[sorted_postings[0]]]
        documents_results = np.setdiff1d(encounters_list, documents_results)

    i = 2
    while i < len(sorted_postings):
        result_documents_results = merge_result_with_posting(documents_results,
                                                             postings_for_query_words[sorted_postings[i]])
        if sorted_postings[i] in not_terms:
            documents_results = np.setdiff1d(documents_results, result_documents_results)
        else:
            documents_results = result_documents_results
        i += 1

    return documents_results


def or_query(word1, word2):
    postings = load_postings()
    if word1 not in postings.keys() and word2 not in postings.keys():
        return []

    postings_word1 = []
    postings_word2 = []

    if word1 in postings.keys():
        postings_word1 = postings[word1]

    if word2 in postings.keys():
        postings_word2 = postings[word2]

    documents_results = []
    postings_ind1, postings_ind2 = 0, 0
    while postings_ind1 < len(postings_word1):
        documents_results.append(postings_word1[postings_ind1][0])
        postings_ind1 += 1

    while postings_ind2 < len(postings_word2):
        documents_results.append(postings_word2[postings_ind2][0])
        postings_ind2 += 1

    return documents_results


def multiple_or_operation(words_list):
    postings = load_postings()
    should_return_empty_list = True
    postings_for_words = []
    for word in words_list:
        if word in postings.keys():
            postings_for_words[word] = postings[word]
            should_return_empty_list = False

    if should_return_empty_list:
        return []

    documents_results = []
    for key in range(len(postings_for_words)):
        postings_ind1 = 0
        while postings_ind1 < len(postings_for_words[key]):
            documents_results.append(postings_for_words[key][0])
            postings_ind1 += 1

    return documents_results