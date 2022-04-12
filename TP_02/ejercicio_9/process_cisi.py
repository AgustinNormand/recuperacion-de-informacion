import pathlib
import sys
from tokenizer import Tokenizer
from normalizer import Normalizer
import re

tn = Tokenizer("emptywords.txt")
n = Normalizer()

def normalize(text):
    words = text.split()
    final_text = []
    for word in words:
        #word = re.sub(r'[^a-zA-Z0-9]', '', word)
        final_text.append(n.normalize(word))

    return " ".join(final_text)

def tokenize(text, frequency = False):
    tokenized_query = tn.tokenize_query(text)
    keys = tokenized_query.keys()
    if frequency:
        keys = []
        for key in tokenized_query:
            for i in range(tokenized_query[key]):
                keys.append(key)

    return " ".join(keys)


def process_documents(dirpath):
    with open("doc-text.trec", "w") as trec_file:
        corpus_path = pathlib.Path(dirpath)
        for file_name in corpus_path.rglob("*.ALL"):
            with open(file_name, "r") as f:
                text_section = False
                for line in f.readlines():
                    #if ".I" in line:
                    if re.findall(r'(\.I\s[0-9]+)', line):
                        doc_number = int(line.split(".I")[1].strip())
                        trec_file.write("<DOC>\r\n")
                        trec_file.write("<DOCNO>{}</DOCNO>\r\n".format(doc_number))
                    
                    if re.findall(r'(\.W\b)', line):
                        text_section = True
                        continue

                    if re.findall(r'(\.X\b)', line):
                        text_section = False
                        trec_file.write("</DOC>\r\n")

                    if text_section:
                        trec_file.write(normalize(line))
                        trec_file.write("\r\n")


"""def process_querys(dirpath):
    with open("query-text.trec", "w") as trec_file:
        corpus_path = pathlib.Path(dirpath)
        for file_name in corpus_path.rglob("*.BLN"):
            with open(file_name, "r") as f:
                for line in f.readlines():
                    if re.findall(r'(#q[0-9]+=)', line):
                        query_number = int(line.split("=")[0].split("#q")[1])
                        trec_file.write("<TOP>\r\n")
                        trec_file.write("<NUM>{}<NUM>\r\n".format(query_number))
"""

def process_relevants(dirpath):
    with open("qrels", "w") as trec_file:
        corpus_path = pathlib.Path(dirpath)
        for file_name in corpus_path.rglob("*.REL"):
            with open(file_name, "r") as f:
                for line in f.readlines():
                    query_id, document_id, _, _ = line.split()
                    trec_file.write("{} {} {} {}\n".format(query_id, 0, document_id, 1))

def process_information_needs(dirpath):
    with open("query-text.trec", "w") as trec_file:
        corpus_path = pathlib.Path(dirpath)
        for file_name in corpus_path.rglob("*.QRY"):
            with open(file_name, "r") as f:
                text_section = False
                text = ""
                for line in f.readlines():
                    if re.findall(r'(\.B\b)', line) or re.findall(r'(\.A\b)', line) or re.findall(r'(\.I\s[0-9]+)', line):
                        text_section = False
                        if text != "":
                            trec_file.write("<TOP>\r\n")
                            trec_file.write("<NUM>{}</NUM>\r\n".format(information_need_number))
                            trec_file.write("<TITLE>{}</TITLE>\r\n".format(tokenize(text, True)))
                            trec_file.write("</TOP>\r\n")
                            text = ""

                    if re.findall(r'(\.I\s[0-9]+)', line):
                        information_need_number = int(line.split(".I")[1].strip())

                    if re.findall(r'(\.W\b)', line):
                        text_section = True
                        continue

                    if text_section:
                        text += line + " "


if len(sys.argv) > 1:
    dirpath = sys.argv[1]
    process_documents(dirpath)
    process_relevants(dirpath)
    process_information_needs(dirpath)