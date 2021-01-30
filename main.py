# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from text_processing import process_documents, get_tokenized_sentences_for_documents, get_sentences_score, \
    get_summary_for_documents


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    cleaned_documents = process_documents()
    #print (get_tokenized_sentences_for_documents())
    #print (get_sentences_score())
    sentences = get_tokenized_sentences_for_documents()
    get_summary_for_documents(sentences)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
