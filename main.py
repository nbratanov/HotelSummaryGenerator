# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from text_processing import process_documents, get_sentences_score, \
    get_summary_for_documents
from tf_idf_summary import generate_tf_idf_summary
from ti_idf_alternative import generate_tf_idf_summary_alternative
import nltk
nltk.download('averaged_perceptron_tagger')


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = 'from wheelchair watermelons'
    pos_tag = nltk.pos_tag(text.split())
    print(pos_tag)
    # print('Ordinary')
    # get_summary_for_documents()
    # print()
    print('TF-IDF summary')
    generate_tf_idf_summary_alternative()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
