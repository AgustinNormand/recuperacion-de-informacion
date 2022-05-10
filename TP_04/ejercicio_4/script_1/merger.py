def merge_vocabulary(final_vocabulary, thread_vocabulary):
    for key in thread_vocabulary:
        try:
            final_vocabulary[key] += thread_vocabulary[key]
        except:
            final_vocabulary[key] = thread_vocabulary[key]

def process_results(results):
    final_vocabulary = {}
    for result in results:
        merge_vocabulary(final_vocabulary, result[0])

    return final_vocabulary
