import pickle
from collections import defaultdict
from nltk.tokenize import sent_tokenize, TweetTokenizer
from string import punctuation
from operator import itemgetter
from utilities import get_documents, get_cleaned_text


tokenizer = TweetTokenizer()


def preprocess_document(document):
    cleaned_text = get_cleaned_text(document, True)
    sentences = sent_tokenize(cleaned_text)
    tokens = []
    for _sent in sentences:
        sent_tokens = tokenizer.tokenize(_sent)
        sent_tokens = [_tok.lower() for _tok in sent_tokens if _tok not in punctuation]
        tokens += sent_tokens
    return tokens


def get_token_doc_id_pairs():
    token_docid = []
    doc_ids = {}

    documents = get_documents()
    for i, document in enumerate(documents):
        doc_ids[i] = document
        with open('./data/' + document) as f:
            document_tokens = preprocess_document(f.read())
            token_docid += [(token, i) for token in document_tokens]

    return sorted(token_docid, key=itemgetter(0))


def get_merge_token_in_doc(sorted_token_docid):
    merged_tokens_in_doc = []
    for token, doc_id in sorted_token_docid:
        if merged_tokens_in_doc:
            prev_tok, prev_doc_id, prev_freq = merged_tokens_in_doc[-1]
            if prev_tok == token and prev_doc_id == doc_id:
                merged_tokens_in_doc[-1] = (token, doc_id, prev_freq+1)
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
            postings[token] = []
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


def or_query(word1, word2):
    postings = load_postings()
    if word1 not in postings.keys() and word2 not in postings.keys():
        return []

    postings_word1 = postings[word1]
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


