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





Punto 6. Desprolijo
Falta lo de las postings.
Falta ponderar terminos del query.
Cambiar a indice invertido.
Dejar de buscar si el doc id leído es mayor, habiendo ordenado los docid.

Justificar porque use bf4
Documentar mejor como correr el programa?

	# Leer de disco palabras vacias una sola vez. Mejora menor.

	#Verificar si en algun momento no inserta desordenado en una posting.



5
./terrier batchretrieve -t ../../ejercicio_5/query-text.trec -w TF_IDF

Terrier model list http://terrier.org/docs/current/javadoc/org/terrier/matching/models/package-summary.html



-->