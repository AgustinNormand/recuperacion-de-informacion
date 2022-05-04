FILE_PATH = "./queries_2y3t.txt"

AND_SYMBOL = "&"
OR_SYMBOL = "|"
NOT_SYMBOL = "!"

SYMBOLS = [AND_SYMBOL, OR_SYMBOL, NOT_SYMBOL]

def build_two_term_querys(term0, term1):
    querys = []
    for symbol in SYMBOLS:
        querys.append("{}{}{}".format(term0, symbol, term1))
    return querys

def build_tree_term_querys(term0, term1, term2):
    querys = []
    querys.append("{}{}{}{}{}".format(term0, AND_SYMBOL, term1, AND_SYMBOL, term2))
    querys.append("({}{}{}){}{}".format(term0, OR_SYMBOL, term1, NOT_SYMBOL, term2))
    querys.append("({}{}{}){}{}".format(term0, AND_SYMBOL, term1, OR_SYMBOL, term2))
    return querys

with open(FILE_PATH, "r") as f:
    two_term_and_querys = []
    two_term_or_querys = []
    two_term_not_querys = []
    tree_term_querys = []

    for line in f.readlines():
        line = line.replace("\n", "")
        terms = line.split(" ")
        if len(terms) == 2:
            and_query, or_query, not_query = build_two_term_querys(terms[0], terms[1])
            two_term_and_querys.append(and_query)
            two_term_or_querys.append(or_query)
            two_term_not_querys.append(not_query)
        else:
            if len(terms) == 3:
                tree_term_querys.extend(build_tree_term_querys(terms[0], terms[1], terms[2]))
    #print(tree_term_querys)

for two_term_and_query in two_term_and_querys:
    #print(two_term_and_query)
    


