import re
from os import listdir
from os.path import isfile, join

from crawlers.database.database_connector import DatabaseConnector


# def store_hotel_summaries(hotel_id):
#     frequency_summary = get_summary_for_documents(hotel_id)
#     tf_idf_summary = generate_tf_idf_summary(hotel_id)
#     frequent_phrases = get_most_used_phrases(hotel_id)
#     hotel_summary = HotelSummary(hotel_id, frequency_summary, tf_idf_summary, frequent_phrases)
#
#     database = DatabaseConnector()
#     database.store_generated_summaries(hotel_summary)


def get_reviews_collection(hotel_id):

    database = DatabaseConnector()
    reviews = database.get_review_by_hotel_id(hotel_id)

    return reviews


def get_documents():
    directory_path = './data'
    return [f for f in listdir(directory_path) if isfile(join(directory_path, f))]


def get_cleaned_text(text, should_remove_signs):
    # Remove Unicode
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Remove Mentions
    cleaned_text = re.sub(r'@\w+', '', cleaned_text)
    # Remove the numbers
    #cleaned_text = re.sub(r'[0-9]', '', cleaned_text)
    # Remove the doubled space
    cleaned_text = re.sub(r'\s{2,}', ' ', cleaned_text)
    # Remove newlines and bad escape symbols
    cleaned_text = re.sub(r'\\u.{4}', '', cleaned_text)
    cleaned_text = re.sub(r'\\n', '', cleaned_text)
    # Remove unnecessary plus symbols
    cleaned_text = re.sub(r'\+', '. ', cleaned_text)
    cleaned_text = re.sub(r'#', '', cleaned_text)
    cleaned_text = re.sub(r'\(', '', cleaned_text)
    cleaned_text = re.sub(r'\)', '', cleaned_text)
    cleaned_text = re.sub(r':', '', cleaned_text)
    cleaned_text = re.sub(r';', '', cleaned_text)
    cleaned_text = re.sub(r'_', '', cleaned_text)
    cleaned_text = re.sub(r'\\', ' ', cleaned_text)
    cleaned_text = re.sub(r'-', ' ', cleaned_text)
    cleaned_text = re.sub(r'/', ' ', cleaned_text)
    cleaned_text = re.sub(r'\'', '', cleaned_text)
    cleaned_text = re.sub(r'\"', '', cleaned_text)

    if should_remove_signs:
        cleaned_text = re.sub(r'\?', ' ', cleaned_text)
        cleaned_text = re.sub(r'\.', ' ', cleaned_text)
        cleaned_text = re.sub(r'!', ' ', cleaned_text)

    return cleaned_text


