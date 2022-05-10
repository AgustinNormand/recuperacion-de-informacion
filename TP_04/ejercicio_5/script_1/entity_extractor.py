import re
from normalizer import Normalizer
class Entity_Extractor():
    def __init__(self, STEMMING_LANGUAGE):
        self.normalizer = Normalizer(STEMMING_LANGUAGE)
        self.regular_expressions = [
            [r'(?:[0-9]{1,2}[\-/][0-9]{1,2}[\-/][0-9]{2,4})|(?:[0-9]{2,4}[\-/][0-9]{1,2}[\-/][0-9]{1,2})', "date"],
            [r'(\b[\w\.]+@[A-Za-z0-9\-]+\.[\.|A-Z|a-z]{2,}\b)', "mail"],
            [r'(?:[A-Z][bcdfghj-np-tvxz]\.)|(?:[A-Z][a-z]{2}\.)', "abbreviation"], #Dr. Lic.
            [r'([A-Z]{2}\.[A-Z]{2})', "abbreviation"], #EE.UU
            [r'(\b(?:[A-Z]\.?){2,})', "abbreviation"], #Poco checkeado. S.A S.A. U.S.A D.A.S.M.I N.A.S.A
            #[r'(?:\b[A-Z]\.[A-Z]\.[A-Z]\.[A-Z]\b)|(?:\b[A-Z]\.[A-Z]\.[A-Z]\b)|(?:\b[A-Z]\.[A-Z]\.)', "abbreviation"], #U.S.A N.A.S.A S.A.
            [r'(?:\b[A-Z]{2}\b)|(?:\b[A-Z]{3}\b)|(?:\b[A-Z]{4}\b)|(?:\b[A-Z]{5}\b)', "abbreviation"], #EJ FIFA USA
            [r'((?:\b[a-z]{2,3}\.\s)|(?:\s[a-z]{2,3}\.\s))', "abbreviation"], # lic. nac. ing. dra. etc.
            [r"((?:(?:https?://)|(?:www\.)|(?:ftps?://))(?:[a-zA-Z./0-9-_?=]+))", "url"],
            [r'((?:\b[0-9]+[\.,][0-9]+\b)|(?:\b[0-9]+\b))', "number"],
            #[r'((?:(?:\b[A-ZÁÉÍÚÓ][a-záéíóú]+\s?){2,})|(?:(?!\A)[A-ZÁÉÍÚÓ][a-záéíóú]+))', "proper_name"], # El Quinto, Agustin Normand
            [r'((?:\b[A-ZÁÉÍÚÓ][a-záéíóú]+\s?){2,})', "proper_name"]
        ]

    def extract_entities(self, actual_line):
        entities = []

        for regular_expression, re_type in self.regular_expressions:
            m = re.findall(regular_expression, actual_line)
            actual_line = re.sub(regular_expression, "", actual_line)

            if m != []:
                for value in m:
                    value = value.strip()
                    
                    if re_type == "abbreviation":
                        value = self.normalizer.normalize_abbreviation(value)

                    if re_type == "date":
                        value = self.normalizer.normalize_date(value)
                        
                    entities.append(value)
                        
        return [actual_line, entities]