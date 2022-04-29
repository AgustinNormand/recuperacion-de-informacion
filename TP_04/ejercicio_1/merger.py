import math


def merge_vocabulary(final_vocabulary, thread_vocabulary):
    for key in thread_vocabulary:
        try:
            final_vocabulary[key] += thread_vocabulary[key]
        except:
            final_vocabulary[key] = thread_vocabulary[key]


def merge_inverted_index(final_inverted_index, thread_inverted_index):
    for key in thread_inverted_index:
        try:
            final_inverted_index[key].extend(thread_inverted_index[key])
        except:
            final_inverted_index[key] = thread_inverted_index[key]


def sort_inverted_index(final_inverted_index):
    for key in final_inverted_index:
        final_inverted_index[key] = sorted(
            final_inverted_index[key], key=lambda tup: tup[0])


def merge_document_vectors(final_document_vectors, thread_documents_vectors):
    for key in thread_documents_vectors:
        final_document_vectors[key] = thread_documents_vectors[key]


def process_results(results):
    final_vocabulary = {}
    final_inverted_index = {}
    final_documents_vectors = {}
    for result in results:
        print(result[0])
        merge_vocabulary(final_vocabulary, result[0])
        merge_inverted_index(final_inverted_index, result[1])
        merge_document_vectors(final_documents_vectors, result[2])

    sort_inverted_index(final_inverted_index)

    return [final_vocabulary, final_inverted_index, final_documents_vectors]
