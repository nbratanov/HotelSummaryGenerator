from os import listdir
from os.path import isfile, join
import re


def get_reviews_collection(hotel_id):
    return []


def get_documents():
    directory_path = './data'
    return [f for f in listdir(directory_path) if isfile(join(directory_path, f))]


def get_cleaned_text(text, should_remove_signs):
    # Remove Unicode
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Remove Mentions
    cleaned_text = re.sub(r'@\w+', '', cleaned_text)
    # Lowercase the numbers
    cleaned_text = re.sub(r'[0-9]', '', cleaned_text)
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


