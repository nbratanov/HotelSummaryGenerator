# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import nltk

from summary_generators.frequency_summary import get_summary_for_documents
from summary_generators.ti_idf_summary import generate_tf_idf_summary, get_most_used_phrases

nltk.download('averaged_perceptron_tagger')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_summary_for_documents('./data/kempinski hotel grand arena.txt')
    print("FREQUENCY SUMMARY \n-----------")
    generate_tf_idf_summary('./data/kempinski hotel grand arena.txt')
    print("TF-IDF SUMMARY \n-----------")
    get_most_used_phrases('./data/kempinski hotel grand arena.txt')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
