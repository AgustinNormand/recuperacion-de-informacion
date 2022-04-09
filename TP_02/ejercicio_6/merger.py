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


def calculate_idf(final_vocabulary, document_count):
    for key in final_vocabulary:
        df = final_vocabulary[key]
        final_vocabulary[key] = [df, math.log(document_count/df)]


def calculate_document_norm(document_vector, vocabulary):
    acum = 0
    for term in document_vector:
        tf = document_vector[term]
        idf = vocabulary[term][1]
        acum += math.pow(tf*idf, 2)

    return math.sqrt(acum)


def calculate_documents_norm(documents_norm, final_documents_vectors, vocabulary):
    for key in final_documents_vectors:
        documents_norm[key] = calculate_document_norm(
            final_documents_vectors[key], vocabulary)


def process_results(results):
    final_vocabulary = {}
    final_inverted_index = {}
    final_documents_vectors = {}
    documents_norm = {}
    for result in results:
        merge_vocabulary(final_vocabulary, result[0])
        merge_inverted_index(final_inverted_index, result[1])
        merge_document_vectors(final_documents_vectors, result[2])

    sort_inverted_index(final_inverted_index)
    calculate_idf(final_vocabulary, len(final_documents_vectors))
    calculate_documents_norm(
        documents_norm, final_documents_vectors, final_vocabulary)

    return [final_vocabulary, final_inverted_index, final_documents_vectors, documents_norm]
