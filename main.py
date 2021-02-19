import nltk

from inverted_index_search import create_and_save_dictionary_and_postings, load_postings, load_dictionary, and_query, \
    or_query, multiple_and_operation
from summary_generators.frequency_summary import get_summary_for_documents
from summary_generators.tf_idf_summary import generate_tf_idf_summary, get_most_used_phrases
from hotel_information.common.domain.hotel_summary import HotelSummary

from hotel_information.database.database_util import DatabaseUtil
from hotel_information.database.database_connector import DatabaseConnector

nltk.download('averaged_perceptron_tagger')


def setup_database():
    DatabaseUtil().setup_database()
    DatabaseUtil().setup_tables()


def generate_review(hotel_id):
    print("FREQUENCY SUMMARY \n-----------")
    frequency_summary = get_summary_for_documents(hotel_id)
    print("FREQUENCY SUMMARY \n-----------")

    print("TF-IDF SUMMARY \n-----------")
    tf_idf_summary = generate_tf_idf_summary(hotel_id)
    print("TF-IDF SUMMARY \n-----------")

    print("MOST USED PHRASES \n-----------")
    frequent_phrases = get_most_used_phrases(hotel_id)
    print("MOST USED PHRASES \n-----------")

    hotel_summary = HotelSummary(hotel_id, frequency_summary, tf_idf_summary, frequent_phrases)

    database = DatabaseConnector()
    database.store_generated_summaries(hotel_summary)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #hotel_id = "16830408"
    hotel_id = "1674691"
    generate_review(hotel_id)

    print("EXAMPLE SEARCH \n-----------")
    create_and_save_dictionary_and_postings()
    result = multiple_and_operation(['free', 'internet'])
    print(result)