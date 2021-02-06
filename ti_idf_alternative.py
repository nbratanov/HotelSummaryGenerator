import math

from nltk import sent_tokenize, word_tokenize, PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('averaged_perceptron_tagger')


def pos_tagging(text):
    pos_tag = nltk.pos_tag(text.split())
    pos_tagged_noun_verb = []
    for word,tag in pos_tag:
        if tag == "NN" or tag == "NNP" or tag == "NNS" or tag == "RB" or tag == "JJ" or tag == "VB" or tag == "VBD" or tag == "VBG" or tag == "VBN" or tag == "VBP" or tag == "VBZ":
             pos_tagged_noun_verb.append(word)
    return pos_tagged_noun_verb


def get_frequency_matrix(sentences):
    frequency_matrix = {}
    stop_words = set(stopwords.words("english"))
    ps = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    for sent in sentences:
        if '?' not in sent:
            freq_table = {}
            words = word_tokenize(sent)
            if len(words) > 4:
                for word in words:
                    word = word.lower()
                    word = lemmatizer.lemmatize(word)
                    word = ps.stem(word)
                    if word in freq_table:
                        freq_table[word] += 1
                    elif word not in stop_words:
                        freq_table[word] = 1

                frequency_matrix[sent] = freq_table

    return frequency_matrix


def get_tf_matrix(freq_matrix):
    tf_matrix = {}

    for sent, f_table in freq_matrix.items():
        tf_table = {}

        count_words_in_sentence = len(f_table)
        for word, count in f_table.items():
            tf_table[word] = count / count_words_in_sentence

        tf_matrix[sent] = tf_table

    return tf_matrix


def create_documents_per_words(freq_matrix):
    word_per_doc_table = {}

    for sent, f_table in freq_matrix.items():
        for word, count in f_table.items():
            if word in word_per_doc_table:
                word_per_doc_table[word] += 1
            else:
                word_per_doc_table[word] = 1

    return word_per_doc_table


def get_idf_matrix(freq_matrix, count_doc_per_words, total_documents):
    idf_matrix = {}

    for sent, f_table in freq_matrix.items():
        idf_table = {}

        for word in f_table.keys():
            idf_table[word] = math.log10(total_documents / float(count_doc_per_words[word]))

        idf_matrix[sent] = idf_table

    return idf_matrix


def get_tf_idf_matrix(tf_matrix, idf_matrix):
    tf_idf_matrix = {}

    for (sent1, f_table1), (sent2, f_table2) in zip(tf_matrix.items(), idf_matrix.items()):

        tf_idf_table = {}

        for (word1, value1), (word2, value2) in zip(f_table1.items(),
                                                    f_table2.items()):
            tf_idf_table[word1] = float(value1 * value2)

        tf_idf_matrix[sent1] = tf_idf_table

    return tf_idf_matrix


def get_longest_sentence_length(sentences):
    longest_sentence_length = 0
    for sent in sentences:
        words = word_tokenize(sent)
        if len(words) > longest_sentence_length:
            longest_sentence_length = len(words)
    return longest_sentence_length


def get_sentences_score(tf_idf_matrix, max_sentence_length) -> dict:
    sentenceValues = {}

    for sentence, f_table in tf_idf_matrix.items():
        total_score_per_sentence = 0
        token = nltk.word_tokenize(sentence)
        bigrams = list(nltk.ngrams(token, 2))
        for entry in bigrams:
            tagged_bigram = nltk.pos_tag(entry)
            if tagged_bigram[0][1] == 'JJ' and (tagged_bigram[1][1] == 'NN' or tagged_bigram[1][1] == 'NNP' or tagged_bigram[1][1] == 'NNS'):
                total_score_per_sentence += 1


        count_words_in_sentence = len(f_table)
        for word, score in f_table.items():
            total_score_per_sentence += score

        print(sentence)
        print(f'score: {total_score_per_sentence}')
        print(f'length: {count_words_in_sentence}')
        print(f_table)


        sentenceValues[sent] = total_score_per_sentence / count_words_in_sentence

   # print(sentenceValues)
    return sentenceValues


def get_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    average = (sumValues / len(sentenceValue))

    return average


def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if '?' not in sentence and sentence in sentenceValue and sentenceValue[sentence] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary


def generate_tf_idf_summary_alternative():
    file = './data/hotel amira istanbul.txt'
    file = open(file, 'r', encoding="utf8")
    text = file.read()
    #text = remove_special_characters(str(text))
    #text = re.sub(r'\d+', '', text)
    sentences = sent_tokenize(text)
    total_documents = len(sentences)
    # print(sentences)

    max_sent_length = get_longest_sentence_length(sentences)

    freq_matrix = get_frequency_matrix(sentences)
    # print(freq_matrix)

    tf_matrix = get_tf_matrix(freq_matrix)
    # print(tf_matrix)

    count_doc_per_words = create_documents_per_words(freq_matrix)
    # print(count_doc_per_words)

    idf_matrix = get_idf_matrix(freq_matrix, count_doc_per_words, total_documents)
    # print(idf_matrix)

    tf_idf_matrix = get_tf_idf_matrix(tf_matrix, idf_matrix)
    # print(tf_idf_matrix)

    sentence_scores = get_sentences_score(tf_idf_matrix, max_sent_length)
    #print(sentence_scores)

    threshold = get_average_score(sentence_scores)
    # print(threshold)

    summary = generate_summary(sentences, sentence_scores, 2.5 * threshold)
    print(summary)
    #print(pos_tagging((summary)))