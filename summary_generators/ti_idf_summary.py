import math

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import re
nltk.download('averaged_perceptron_tagger')

stop_words = set(stopwords.words("english"))


def clean_reviews(reviews, should_remove_signs):
    cleaned_reviews = []
    for review in reviews:
        cleaned_review = get_cleaned_text(review, should_remove_signs)
        cleaned_reviews.append(cleaned_review)

    return cleaned_reviews


def get_cleaned_text(text, should_remove_signs):
    # Remove Unicode
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Remove Mentions
    cleaned_text = re.sub(r'@\w+', '', cleaned_text)
    # Lowercase the numbers
    cleaned_text = re.sub(r'[0-9]', '', cleaned_text)
    # Remove the doubled space
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)

    if should_remove_signs:
        cleaned_text = re.sub(r'\?', ' ', cleaned_text)
        cleaned_text = re.sub(r'\.', ' ', cleaned_text)
        cleaned_text = re.sub(r'\\', ' ', cleaned_text)
        cleaned_text = re.sub(r'-', ' ', cleaned_text)
        cleaned_text = re.sub(r'/', ' ', cleaned_text)
        cleaned_text = re.sub(r'!', ' ', cleaned_text)
        cleaned_text = re.sub(r'\\u.{4}', '', cleaned_text)
        cleaned_text = re.sub(r'\\n', '', cleaned_text)

    return cleaned_text


def get_frequency_matrix(reviews, should_process):
    frequency_matrix = {}
    ps = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    for review in reviews:
        freq_table = {}
        words = word_tokenize(review)
        for word in words:
            word = word.lower()
            if should_process:
                word = lemmatizer.lemmatize(word)
                word = ps.stem(word)
            if word in freq_table:
                freq_table[word] += 1
            elif word not in stop_words:
                freq_table[word] = 1

        frequency_matrix[review] = freq_table

    return frequency_matrix


def get_tf_matrix(freq_matrix):
    tf_matrix = {}

    for review, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[review] = tf_table

    return tf_matrix


def get_global_frequency_table(freq_matrix):
    word_encounters = {}

    for review, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_encounters:
                word_encounters[word] += count
            else:
                word_encounters[word] = count

    return word_encounters


def get_word_count_in_all_documents(freq_matrix):
    word_encounters = {}

    for review, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_encounters:
                word_encounters[word] += 1
            else:
                word_encounters[word] = 1

    return word_encounters


def get_idf_matrix(freq_matrix, words_encoutners, total_documents):
    idf_matrix = {}

    for review, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(words_encoutners[word]))

        idf_matrix[review] = idf_table

    return idf_matrix


def get_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (review1, f_table1), (review2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[review1] = tf_idf_table

    return tf_idf_matrix


def get_adjusted_score_to_elements_of_speech_contained(words) -> float:
    total_score_per_sentence = 0
    bigrams = list(nltk.ngrams(words, 2))
    for entry in bigrams:
        tagged_bigram = nltk.pos_tag(entry)
        if tagged_bigram[0][1] == 'JJ' and (tagged_bigram[1][1] == 'NN' or tagged_bigram[1][1] == 'NNS'):
            total_score_per_sentence += 0.5
        elif tagged_bigram[0][1] == 'NNP' or tagged_bigram[1][1] == 'NNP':  # Add hotel name as exception
            total_score_per_sentence -= 0.5

    return total_score_per_sentence


def get_non_stop_words_count(words) -> int:
    count_words_in_sentence = 0
    for word in words:
        if word not in stop_words:
            count_words_in_sentence += 1

    if(count_words_in_sentence == 0):
        count_words_in_sentence = 200

    return count_words_in_sentence


def get_sentences_score(tf_idf_matrix) -> dict:
    sentence_scores = {}

    review_counter = 0
    for review, f_table in tf_idf_matrix.items():
        if review_counter < 4000:
            sentences = nltk.sent_tokenize(review)
            for sentence in sentences:
                total_score_per_sentence = 0
                words = nltk.word_tokenize(sentence)

                total_score_per_sentence = get_adjusted_score_to_elements_of_speech_contained(words)
                if '?' in sentence or len(words) < 6:
                    total_score_per_sentence -= 1
                count_words_in_sentence = get_non_stop_words_count(words)

                for word, score in f_table.items():
                    total_score_per_sentence += score

                sentence_scores[sentence] = total_score_per_sentence / count_words_in_sentence
        print(review_counter)
        review_counter += 1

    return sentence_scores


def generate_summary(sentence_scores):
    summary = ''
    sentence_scores = dict(sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True))

    counter = 0
    for sentence in sentence_scores.keys():
        if counter < 30:
            counter += 1
            summary += " " + sentence

    return summary


def generate_tf_idf_summary(file):
    file = open(file, 'r',  encoding="utf-8-sig")

    reviews = file.readlines()

    reviews = clean_reviews(reviews, False)

    total_documents = len(reviews)
    # print(sentences)

    freq_matrix = get_frequency_matrix(reviews, True)
    # print(freq_matrix)

    tf_matrix = get_tf_matrix(freq_matrix)
    # print(tf_matrix)

    word_encounters = get_word_count_in_all_documents(freq_matrix)
    # print(count_doc_per_words)

    idf_matrix = get_idf_matrix(freq_matrix, word_encounters, total_documents)
    # print(idf_matrix)

    tf_idf_matrix = get_tf_idf_matrix(tf_matrix, idf_matrix)
    # print(tf_idf_matrix)
    
    sentence_scores = get_sentences_score(tf_idf_matrix)
    #print(sentence_scores)
    
    summary = generate_summary(sentence_scores)
    print(summary)
    #print(pos_tagging((summary)))


def get_most_used_phrases(file):
    file = open(file, 'r', encoding="utf-8-sig")
    reviews = file.readlines()
    reviews = clean_reviews(reviews, True)
    freq_matrix = get_frequency_matrix(reviews, False)
    freq_table = get_global_frequency_table(freq_matrix)
    phrases_map = {}
    for review in reviews:
        words = word_tokenize(review)
        bigrams = list(nltk.ngrams(words, 2))
        for bigram in bigrams:
            tagged_bigram = nltk.pos_tag(bigram)
            if tagged_bigram[0][1] == 'JJ' and (tagged_bigram[1][1] == 'NN' or tagged_bigram[1][1] == 'NNS'):
                first_bigram_element = bigram[0].lower()
                second_bigram_element = bigram[1].lower()
                if len(bigram[0]) > 2 and bigram[0] in freq_table.keys() and bigram[1] in freq_table.keys():
                    phrase_score = freq_table[first_bigram_element] + freq_table[second_bigram_element]
                    lowercased_bigram = (first_bigram_element, second_bigram_element)
                    if lowercased_bigram not in phrases_map.keys():
                        phrases_map[lowercased_bigram] = phrase_score

    sorted_phrases = dict(sorted(phrases_map.items(), key=lambda item: item[1] and item[0][1] != 'hotel', reverse=True))

    for phrase in list(sorted_phrases.keys())[:15]:
        print(f'{phrase[0]} {phrase[1]}')

