# - Recorrer todos los archivos de un directorio y contar frecuencias de palabras
# - Eliminar del análisis a aquellas palabras que pertecen al grupo de "palabras vacías"
# - Pasar a minúsculas y eliminar las tildes de las palabras procesadas
# - Crear bar chart de frecuencias

import sys
import pathlib
import re
import matplotlib.pyplot as plt

palabras_vacias = [] # algunas palabras a ignorar

should_delete_stop_words = False

def process_dir(filepath):
    frequencies = count_frequencies(filepath)
    print(frequencies)
    save_frequencies(frequencies)
    plot_frequencies(frequencies)

def count_frequencies(dirpath):
    frequencies = {}
    corpus_path = pathlib.Path(dirpath)
    for in_file in corpus_path.iterdir():
        with open(in_file, "r") as f:
            for line in f.readlines():
                tokens_list =  filter(lambda x: should_include_word(x), [normalize(x) for x in line.strip().split()])
                for token in tokens_list:
                    if token in frequencies.keys():
                        frequencies[token] += 1 
                    else:
                        frequencies[token] = 1
    return frequencies

def should_include_word(word): 
    if (len(word) > MIN_LENGTH and len(word) < MAX_LENGTH):
        return word not in palabras_vacias        
    return False

def translate(to_translate):
	tabin = u'áéíóú'
	tabout = u'aeiou'
	tabin = [ord(char) for char in tabin]
	translate_table = dict(zip(tabin, tabout))
	return to_translate.translate(translate_table)


def normalize(token):
    result = token.lower()
    result = translate(result)

    #re module doc: https://docs.python.org/3/library/re.html
    
	#result = re.sub('[-\[!\"\$%&\(\)=\']', '', result) # encierro la expresion entre [] para dar opciones
    
    is_number = re.search('^[0-9]*$',result)
    if (is_number):
        print('Numero encontrado: ' + is_number.group()+ "\n")
    #re.findall('([\w\.-]+)@([\w\.-]+)', 'juan@unlu mail universidad pepe@gmail')
    mails = re.search("([a-z]+@[a-z]+.com)", result)
    if mails:
        print(f'Mail encontrado {mails.group()}\n')
    
    return result

def save_frequencies(frequencies):
	# guardar en un archivo frecuencias ordenadas por valor
	with open("dir_frequencies.txt", "w") as f:
        # sorted retorna lista de keys ordenadas por valor
		for key in sorted(frequencies, key=frequencies.get, reverse=True):
			f.write(f'{key} {frequencies[key]}\n')

def plot_frequencies(frequencies, sort_values=True):
    if sort_values:
        # sorted retorna diccionario ordenado por valor
        frequencies = {k: v for k, v in sorted(frequencies.items(), key=lambda item: item[1], reverse=True)}
    plt.plot(frequencies.keys(), frequencies.values())
    plt.show()


def load_stop_words(path):
    with open(path, "w") as f:
        
# -------------------------------------

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Es necesario pasar como argumento un path a un directorio')
		sys.exit(0)
	dirpath = sys.argv[1]
    if len(sys.argv) == 3:
        stop_words_path = sys.argv[2]
        palabras_vacias = load_stop_words(stop_words_path)
        
	process_dir(dirpath)





