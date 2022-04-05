<!-- 

1
Contar como hice el boolean.
Contar como hice el vectorial.
Mejorar lo escrito. Usando el script


Cual es la ventaja de usar TF-IDF que solo TF?

Punto 1
Asumo que la query esta unida con or? Osea, ENERGY-METABOLIS or LIVER-CIRRHOSIS or VITAMIN-A
Porque si las uno con and, no recupero ningun documento

Como puede ser que la palabra 142, PANCREATIC-JUICE no está en ningun documento? SWEATING lo mismo.

Los demás terminos de la query, tienen frequencia 0, log(0)??

Cuando calculo la longitud normalizada del documento, lo hago usando el vector cuyo peso es TF-iDF?

Query 2: (1, 4, 6, 9, 14, 17, 19, 21, 23, 29, 36, 37, 38, 147, 195, 196) Tiene 3 documentos incorrectos

Si fueran todos tweets, no debería normalizar los vectores, no? Que formual uso

Resuletas: 
En el 1 de modelo vectorial, lo hacemos con TF, con IDF, o TFIDF? CON TF-IDF

Como el termino 142 no está en ningun documento, cuando hago el DF para hacer el IDF, me da error, division por 0. Igual despues use el idf que nos dan, y no lo calculé









Borrador:

Eliminando la palabra "PATIENTS" de la query, se mejora la precisión, dado que esta hace que se recuperen 4 documentos que ninguno es relevante.

Podría seguir indicando que terminos se podrían agregar o quitar de la query para mejorar la precision o recall o ambos. El problema es que este analisis es facil hacerlo viendo los documentos relevantes, los terminos que tienen estos documentos, el valor que aporta cada uno de los términos de la query al conjunto de resultados, etc. Pero me resulta poco valioso indicar cómo mejorar los resultados, haciéndolo de esta forma, dado que es como "hacer trampa".
Por ejemplo, para la query 2, los términos que resultan intuitivos para traducir de la 

Podría mejorar la eficiencia de la query realizando un analisis utilizando los diferentes archivos de input que tengo. Este analisis es facil hacerlo viendo los documentos relevantes, los terminos que tienen estos documentos, el valor que aporta cada uno de los términos de la query al conjunto de resultados, etc. El problema, es que no se llegan a resultados reales, al que un usuario podría llegar. Es decir, hay documentos que no son recuperados debido a que no contienen ninguno de los términos de la query, podría agregar uno de los términos del documento a la query, y así lograr que lo recupere, pero este término, sería imposible de adivinar para el usuario, por lo tanto no sería un documento que está al alcance del usuario recuperarlo.


-->