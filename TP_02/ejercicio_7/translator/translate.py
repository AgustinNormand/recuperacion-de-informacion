from pathlib import Path

terrier_docnames = {}
with open("terrier_docnames_ids.txt", "r") as f:
    for line in f.readlines():
        doc_id = line.split(",")[0]
        p = Path(line.replace("{}, ".format(doc_id), "").replace("../../ejercicio_6/", "").strip())
        #doc_name = p.name
        terrier_docnames[doc_id] = str(p)

mis_docnames = {}
with open("mis_docnames_ids.txt", "r") as f:
    for line in f.readlines():
        path, doc_id = line.strip().split()
        mis_docnames[path] = doc_id

with open("translated_file.res", "w") as translated_file:
    with open("output_ejercicio_5/TF_IDF.res", "r") as f:
        for line in f.readlines():
            query_id, q0, doc_id, count, score, model = line.strip().split()
            translated_doc_id = mis_docnames[terrier_docnames[doc_id]]
            translated_file.write("{} Q0 d{} {} {} {}\r\n".format(query_id, translated_doc_id, count, score, model))
            #break


#print(mis_docnames)
#print(terrier_docnames)
