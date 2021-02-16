# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import nltk

from inverted_index_search import create_and_save_dictionary_and_postings, load_postings, load_dictionary, and_query, \
    or_query, multiple_and_operation
from summary_generators.frequency_summary import get_summary_for_documents
from summary_generators.tf_idf_summary import generate_tf_idf_summary, get_most_used_phrases
from trip_advisor_crawler.common.domain.hotel_summary import HotelSummary

from trip_advisor_crawler.database.database_util import DatabaseUtil
from trip_advisor_crawler.database.database_connector import DatabaseConnector

nltk.download('averaged_perceptron_tagger')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_and_save_dictionary_and_postings()
    postings = load_postings()
    print(postings)
    # dictionary = load_dictionary()
    # result = and_query('recommend', 'famous')
    # print(result)
    # result = or_query('pesho', 'udriebace')
    # print(result)

    # get_summary_for_documents("16830408")
    # print("FREQUENCY SUMMARY \n-----------")
    # generate_tf_idf_summary("16830408")
    # print("TF-IDF SUMMARY \n-----------")
    # get_most_used_phrases("16830408")

    # DatabaseUtil().setup_database()
    # DatabaseUtil().setup_tables()

    # hotel_id = "16830408"
    # hotel_id = "8147345"
    # frequency_summary = get_summary_for_documents(hotel_id)
    # tf_idf_summary = generate_tf_idf_summary(hotel_id)
    # frequent_phrases = get_most_used_phrases(hotel_id)
    # hotel_summary = HotelSummary(hotel_id, frequency_summary, tf_idf_summary, frequent_phrases)
    #
    #database = DatabaseConnector()
    # database.store_generated_summaries(hotel_summary)
    #database.get_hotels_information()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
