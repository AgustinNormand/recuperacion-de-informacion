# Análisis de Texto
##### Fecha entrega: 25/03/2021

###### Normand Agustín

###### Legajo: 156649

Para la entrega del TP resuelto arme un único archivo comprimido (.tar.gz) y envielo a través del siguiente formulario:
https://forms.gle/enizkPdDeA25AotC7 el cual se encontrará habilitado hasta la fecha de entrega establecida.

Bibliografı́a sugerida: MIR [1] Capı́tulo 7, TOL [5] Capı́tulo 3, MAN [4] Capı́tulo 6, Grefenstette et al. [2], Ha et al. [3].

### 1. Escriba un programa que realice análisis léxico sobre la colección RI-tknz-data. El programa debe recibir como parámetros el directorio donde se encuentran los documentos y un argumento que indica si se deben eliminar las palabras vacı́as (y en tal caso, el nombre del archivo que las contiene). Defina, además, una longitud mı́nima y máxima para los términos. Como salida, el programa debe generar:
### a) Un archivo (terminos.txt) con la lista de términos a indexar (ordenado), su frecuencia en la colección y su DF (Document Frequency). Formato de salida: < termino > [ESP ] < CF > [ESP ] < DF >.
### Ejemplo:
casa 238 3
perro 644 6
...
zorro 12 1

Para resolver este ejercicio cree las siguientes clases:

* Document
* Collection
* Normalizer
* Tokenizer
* Exporter

Dichas clases se encuentran en el directorio ejercicio_1. Junto con el archivo emptywords.csv donde cargué las palabras vacías. Y además, también podemos encontrar los archivos de salida del programa: 

* terminos.txt
* estadisticas.txt
* frecuencias.txt

Para correr el programa, python3 tokenizer.py path_coleccion path_archivo_palabras_vacias

En caso de no querer utilizar un archivo de palabras vacias, simplemente correr python3 tokenizer.py path_coleccion

### b) Un segundo archivo (estadisticas.txt) con los siguientes datos (un punto por lı́nea y separados por espacio cuando sean más de un valor) :

1) Cantidad de documentos procesados
2) Cantidad de tokens y términos extraı́dos
3) Promedio de tokens y términos de los documentos
4) Largo promedio de un término
5) Cantidad de tokens y términos del documento más corto y del más largo
6) Cantidad de términos que aparecen sólo 1 vez en la colección

### c) Un tercer archivo (frecuencias.txt, con un término y su CF por lı́nea) con:

1) La lista de los 10 términos más frecuentes y su CF (Collection Frequency)
2) La lista de los 10 términos menos frecuentes y su CF.

<!-- 

Contar de donde saque las palabras vacias
Por arriba como reslvi el codigo??
Decisiones que tome.

 -->



### 2. Tomando como base el programa anterior, escriba un segundo T okenizer que implemente los criterios del artı́culo de Grefenstette y Tapanainen para definir qué es una “palabra” (o término) y cómo tratar números y signos de puntuación. Además, extraiga en listas separadas utilizando en cada caso una función especı́fica.

<!-- 

Falta terminar 

-->

<!-- 

a) Abreviaturas tal cual están escritas (por ejemplo, Dr., Lic., S.A., NASA, etc.)

Si quiero matchear abreviaturas como NASA, es inevitable que la expresión regular tambien matchee:

* JEFE
* FOTO
* SPAM
* UEFA
* AYER
* ANSA

Abreviaturas con 3 letras mayusculas:

* PDF
* AFA
* CIA
* UBA
* USB
* VIH
* HIV
* DNI
* OMS

No validas

* SON
* DEL
* MAS
* MIL
* LOS
* RIO

b) Direcciones de correo electrónico y URLs
c) Números (por ejemplo, cantidades, teléfonos)
d ) Nombres propios (por ejemplo, Villa Carlos Paz, Manuel Belgrano, etc.) y los trate como un único
token.
Genere y almacene la misma información que en el caso anterior.
-->




### 3. A partir del programa del ejercicio 1, incluya un proceso de stemming, use la librerı́a NLTK (Natural Language Toolkit) y revise qué algoritmos soporta para español e inglés.

De la librería NLTK utilicé el módulo nltk.stem.snowball, ya que tiene soporte tanto para español como para inglés.

Los cambios realizados en el código del ejercicio 3, respecto al del ejercicio 1, se enfocan en las condiciones para que un token sea o no un término.

Especificamente, dado un token, este es sometido a un proceso de Stemming.
Luego, el token y el resultado del proceso mencionado anteriormente, no deben estar en la lista de palabras vacias.

Por otro lado, el resultado del proceso de Stemming, debe tener una longitud válida para ser un término.

Finalmente si las condiciones mencionadas anteriormente se cumplen, se incrementa la Collection Frecuency del término, que es el resultado del processo de Stemming.

Además, se guarda en un diccionario para cada raiz obtenida con el Stemmer, de que tokens fue obtenida, para para poder realizar un debug a futuro. 

Ejemplo: competent->{'competencia': 22, 'competencias': 44, 'competente': 9, 'competentes': 1}
La raiz "competent", fue obtenida de los tokens: "competencia" 22 veces, "competencias" 44 veces, "competente" 9 veces y "competentes" 1 vez.

### Luego de modificar su programa, corra nuevamente el proceso del ejercicio 1 y analice los cambios en la colección. ¿Qué implica este resultado?

Luego de correr el programa del ejercicio 1, y el del ejercicio 3, ambos con el mismo archivo de palabras vacías y la misma longitud minima y máxima permitida para los términos, noté las siguientes diferencias:

* El programa del ejercicio 1 extrajo 32279 términos y el del ejercicio 3, 23028 términos.
    * Concretamente 9251 términos menos extraidos por el programa del ejercicio 3. Esto tiene sentido ya que estoy contando la cantidad de terminos diferentes extraidos. En el ejercicio 1, los tokens "universidad" y "universidades", son dos términos diferentes, pero sin embargo, en el ejercicio 3, son el mismo término.

* En el ejercicio 1, el promedio de términos extraidos por documentos es de 64.81726907630522, mientras que en el ejercicio 3, es de 46.24096385542169.
    * Al igual que el item anterior, este comportamiento era de esperarse, ya que tokens con la misma raiz, pero diferentes, en el ejercicio 1, son tratados como términos distintos, por lo que el promedio de términos que se van a extrar de cada documento, es mayor que en el ejercicio 3.

* En las estadisticas del ejercicio 1, el largo promedio de un término es de 9.15722296229747 caracteres, mientras que en las del ejercicio 3, es de 8.346013548723294 caracteres.
    * Este comportamiento puede ser explicado debido a que, los términos del ejercicio 1, son los token que son univocos en la colección, luego de haber sido normalizados. Pero en el ejercicio 3, los términos son la raiz de los token, que obviamente es de longitud inferior que el token del que se extrae. Por lo tanto la longitud promedio de los términos del ejercicio 3 va a ser inferior a la del ejercicio 1.

* La cantidad de términos del documento mas largo en el ejercicio 1 es de 7581, mientras que en el ejercicio 3 es de 4890. La explicación es similar a la del primer y segundo item de esta lista, los documentos tienen menos términos, debido al proceso de stemming.

* La cantidad de términos que aparecen una sola vez en la colección, en el ejercicio 1 es de 16898, mientras que en el ejercicio 3 es de 11730. Esto tiene sentido, dado que por ejemplo, en el ejercicio 1, un término que aparece una sola vez en toda la colección es "robot", por lo tanto, este hace que se incremente el contador. Mientras que en el ejercicio 3, el token "robot" y el token "robotica" tienen la misma raiz, por lo que el término que los agrupa a ambos es "robot", y la CF de este término, es de 3 (1 vez  por el token "robot" y 2 veces por el token "robotica") por lo que ya no produce un incremento en el contador de los términos que aparecen una sola vez en la colección. 
Esto explica por qué el contador del ejercicio 3 es inferior al contador del ejercicio 1.

* En las frecuencias de cada uno de los programas, en el ejercicio 1, "argentina" es un término que tiene una CF de 774, sin embargo "argentina" tiene una CF de 921 en el ejercicio 3.
    * Dado que en este ultimo ejercicio, este termino incluye a los tokens: "argentina" 774 veces, "argentino" 89 veces, "argentine" 1 vez, "argentinas" 30 veces y "argentinos" 27 veces.


### Busque ejemplos de pares de términos que tienen la misma raı́z pero que el stemmer los trató diferente y términos que son diferentes y se los trató igual.

En cuanto a ejemplos donde el stemmer trato de igual forma a términos que son diferentes, encontré:
* Para uno de los términos más frecuentes "univers" con una CF de 2416.
    * 2239 veces, el stemmer paso de "universidad" a "univers".
    * 171 veces, de "universidades" a "univers".
    * 3 veces, de "universo" a "univers"

* Para el término "mart"
    * 87 veces, el stemmer pasó de martes a "mart"
    * 12 veces, de "marta" a "mart"

Podemos ver que trató de igual forma a términos que son diferentes.

Por otro lado, para dar ejemplos con terminos con la misma raiz pero que el stemmer trató diferente:

* Los términos: "cientifico", "cientificos", "cientificas", "cientificamente". 
Fueron tratados de forma distinta que los términos: "ciencias" y "ciencia".

* El término: "libreria" fué tratado de forma diferente que los términos: "libros", "libro".

* El término "enamorado" fué tratado de forma distinta que el los términos: "amor", "amorosas" y "amorosamente"

### 4. Sobre la colección CISI3 , ejecute los stemmers de Porter y Lancaster provistos en el módulo nltk.stem. Compare: cantidad de tokens resultantes, resultado 1 a 1 y tiempo de ejecución para toda la colección. Qué conclusiones puede obtener de la ejecución de uno y otro?

La cantidad de términos del stemmer Lancaster es 17251. Mientras que la cantidad del Porter es de 18074. Este último tiene 823 términos más.


Sometiendo a cada token a un procesamiento, eliminando acentos y caracteres no alfanumericos, la cantidad de términos obtenidos por Lancaster es de 8890, mientras que la de porter es de 9962. Una cantidad de términos significativamente menor, pero mayor diferencia entre los diferentes Stemmers, concretamente 1072 términos.

Como era de esperarse, ambos stemmers tratan de igual forma a los numeros, no realizan ninguna modificación.

En cuanto a palabras que los stemmers tratan de igual forma:

* in -> in
* of -> of
* the -> the
* wich -> wich
* to -> to
* as -> as

* suggested -> suggest
* participated -> particip
* produced -> produc

* dealing -> deal
* representing -> repres

* information -> inform
* importance -> import

* eight -> eight
* seventeen -> seventeen
* four -> four

Las palabras que los stemmers tratan de manera diferente:

* Palabra: specifying
    * Porter: specifi
    * Lancaster: spec

* Palabra: balancing
    * Porter: balanc
    * Lancaster: bal

* Palabra: water
    * Porter: water
    * Lancaster: wat
    
* Palabra: fifth
    * Porter: fifth
    * Lancaster: fif

* Palabra: seventies
    * Porter: seventi
    * Lancaster: seventy

* Palabra: preclassified
    * Porter: preclassifi
    * Lancaster: preclass

* Palabra: queried
    * Porter: queri
    * Lancaster: query

Vemos que en ambos casos, tanto en palabras que tratan de igual forma, como de manera diferente, hay palabras con "ing", hay palabras terminadas con "ed", hay palabras que hacen referencia a numeros.


Simplifiqué el tokenizador con respecto a los puntos anteriores para no agregar tiempos de procesamiento adicionales y ver reflejado lo mejor posible los tiempos de cada Stemmer.

Unicamente leyendo linea a linea cada uno de los archivos de la colección, separando estas por espacios, aplicando solamente el proceso de stem a estas palabras sin ningún otro tratamiento, los tiempos de ejecución de cada uno de los stemmers son:
* Porter: 8.350780248641968 segundos.
* Lancaster: 4.523569583892822 segundos.

Si bien se puede observar que el stemmer Porter corre casi en el doble de tiempo que Lancaster, este útlimo es un altorimo de stemming muy agresivo, que resulta en una longitud menor del vocabulario, dado que muchos tokens terminan correspondiendo al mismo término debido a la gran poda que hace en las palabras.

Por otro lado, Porter es un algoritmo computacionalmente más intensivo que la otra alternativa, pero que nos brinda mas precisión en el proceso de stemming. Es razonable que sea el algoritmo más utilizado para esta finalidad.


### 5. Escriba un programa que realice la identificación del lenguaje de un texto a partir de un conjunto de entrenamiento. Pruebe dos métodos sencillos:

### a) Uno basado en la distribución de la frecuencia de las letras.

Cree un diccionario para cada uno de los archivos de train y las claves de este, son las letras de la "a" a la  "z". Lo inicialicé en 0, y luego conté la frecuencia de caracteres para cada uno de los 3 archivos.
Por ultimo, leí linea a linea el archivo de test, contando la frecuencia de caracteres en cada una de estas, y verificando con cuales de los diciccionarios de train, tenia mayor coeficiente de correlación, siendo este el idioma estimado de la linea leida.

Utilizando este método la precision del modelo es de 0.87.
De 300 lineas, solo estimó de forma erronea 39.


### b) El segundo, basado en calcular la probabilidad de que una letra x preceda a una y (calcule una  matriz de probabilidades con todas las combinaciones).

Para este otro método, conté como válidas unicamente las combinaciones de caracteres donde ambos eran letras, o, una letra con un espacio, es decir, descarté numeros y simbolos.

Lei los 3 archivos de train para obtener todos los posibles pares de letras, usando estas combinaciones, cree 3 diccionarios inicializados en 0. Lei cada uno de los archivos de train, contando la frecuencia de aparición del duo de caracteres, en los diccionarios.
Finalmente, lei cada una de las lineas del archivo de test, agrupando de a 2 caracteres, contando la frecuencia de aparición, y verificando el coeficiente de correlación con los diccionarios.

La precision del modelo es de 0.9833333333333333.
De la totalidad de las lineas de test, unicamente el idioma de 5 fueron estimados de forma incorrecta.

Hay un grupo de caracteres que fué leido en el conjunto de test, que no había aparecido en el conjunto de train: "rj". No fué incorporado como clave en los diccionarios de frecuencias.

Una aclaración que tiene valor para ambos modelos, además de la ventaja de su sencillez, tienen muy buena precision para realizar la identificacion del lenguaje de un texto, más teniendo en cuenta que el largo promedio de las lineas del conjunto de test, es de unicamente 164 caracteres.

### Compare los resultados contra el módulo Python langdetect y la solución provista.

El accuracy de langdetect es de 0.99, de 300 lineas del conjunto de test, el idioma de 3 fué detectado de forma incorrecta. Tan solo 2 lineas más del conjunto de test debemos estimar de forma correcta para igualar la solución de langdetect.

## Propiedades del Texto (En notebook Jupyter).

### 6. En este ejercicio se propone verificar la predicción de ley de Zipf. Para ello, descargue desde Project Gutenberg el texto del Quijote de Cervantes y escriba un programa que extraiga los términos y calcule sus frecuencias (el programa debe generar la lista ordenada por frecuencia descencente). Calcule la curva de ajuste utilizando la función Polyfit del módulo NumPy. Con los datos crudos y los estimados grafique en la notebook ambas distribuciones (haga 2 gráficos, uno en escala lineal y otro en log-log). ¿Cómo se comporta la predicción? ¿Qué conclusiones puede obtener?

En primer lugar, eliminé una sección en inglés que tenía el quijote, probablemente agregada por la página de la cual fué descargado el libro.

Luego procesé linea a linea, palabra a palabra el texto, transformandolas a minusculas, removiendo acentos y caracteres no alfanumericos, para luego, en un diccionario, contar las ocurrencias de cada uno de los tokens, obteniendo de esta forma los términos, con su collection frecuency.

Una vez finalizado este procesamiento, obtuve a partir del diccionario una lista ordenada por frecuencia de forma descendente. Con esta, y la lista de rankings, calculé la curva de ajuste usando Polyfit.

Utilizando los datos crudos y los estimados, cree el siguente gráfico en escala lineal:

![lineal](https://raw.githubusercontent.com/AgustinNormand/recuperacion-de-informacion/main/TP_01/ejercicio_6/lineal.png)

Y otro en escala log-log:

![log-log](https://raw.githubusercontent.com/AgustinNormand/recuperacion-de-informacion/main/TP_01/ejercicio_6/log-log.png)

Para poder indicar con una medida estadistica como se comporta la predicción utilicé el coeficiente de determinacion, dado que este se utiliza en contextos de modelos estadisticos cuyo principal proposito es predecir futuros resultados.

Aplicandolo en los datos reales y los estimados en escala lineal, utilizando una curva como función de ajuste, el valor resultante es de 0.9236733223632114.

Mientras que en escala logaritmica, utilizando una recta como funcion de ajuste el valor de este coeficiente es 0.9776427799102992.

A modo de conclusion, apoyandonos sobre los valores de los coeficientes, podemos afirmar que este no se trata de un contraejemplo a la ley de Zipf, hay muy pocos terminos con una ocurrencia muy alta, y muchos términos que ocurren pocas veces.

Si en una escala lineal, ajustamos un modelo que sea recta vemos que este resulta en el siguiente gráfico:

![recta](https://raw.githubusercontent.com/AgustinNormand/recuperacion-de-informacion/main/TP_01/ejercicio_6/recta.png)

Por lo que confirma lo dicho anteriormente, muy pocos términos tienen una frecuencia muy alta, dado que la recta se ajustó a los términos que ocurren pocas veces.


### 7. Usando los datos del ejercicios anterior y de acuerdo a la ley de Zipf, calcule la proporción del total de términos para aquellos que tienen frecuencia f = {100, 1000, 10000}. Verifique respecto de los valores reales. ¿Qué conclusión puede obtener?

Valores reales:

* Proporción de terminos con frecuencia >= a 100 = 0.01720643408512657
* Proporción de terminos con frecuencia >= a 1000 = 0.002069946957609211
* Proporción de terminos con frecuencia >= a 10000 = 0.0001724955798007676

Valores estimados curve_fit, curva, escala lineal:

* Proporción de terminos con frecuencia >= a 100 = 0.04187330199663634
* Proporción de terminos con frecuencia >= a 1000 = 0.0024580620121609385
* Proporción de terminos con frecuencia >= a 10000 = 0.0001293716848505757

Valores estimados polyfit, recta, escala logaritmica:

* Proporción de terminos con frecuencia >= a 100 = 0.0170339385053258
* Proporción de terminos con frecuencia >= a 1000 = 0.00250118590711113
* Proporción de terminos con frecuencia >= a 10000 = 0.0003449911596015352


Se puede observar que la estimación realizada por curve_fit, estima de forma aceptable los términos con frecuencias bajas, pero sitúa en frecuencias altas una gran proporción de términos, (0.418), alejandose de lo planteado por la ley de Zipf, que los términos con frecuencias altas, ocurren una cantidad reducida de veces.

Tal vez por este motivo el modelo de polyfit haya sido el más exitoso para este experimento, ajustando los términos en las 3 frecuencias diferentes, con una muy buena precisión.

### 8. Codifique un script que reciba como parámetro el nombre de un archivo de texto, tokenize y calcule y escriba a un archivo los pares (#términos totales procesados, #términos únicos). Verifique en qué medida satisface la ley de Heaps. Grafique en la notebook los ajustes variando los parámetros de la expresión. Puede inicialmente probar con los archivos de los puntos anteriores.


Utilice el Quijote para hacer el experimento, lo leí linea a linea y extraje terminos y tokens. 
Además, agregue dos listas, para ir guardando la cantidad de terminos en un momento determindo, y la otra, para guardar el "step" actual. Definí una variable "step", que indica, cada cuantos tokens encontrados, debe agregar a la lista la cantidad de términos actuales. 
Si el step es de 1, por cada token que encuentra, va a agregar a la lista, la cantidad de términos encontrados hasta el momento, el step actual, e incrementa el step en 1.

Escribí el archivo de pares, que para el Quijote es de 384260 tokens y 23201 términos.

Luego, ajusté una curva utilizando la funcion de ajuste de la ley de Heaps, utilizando los dos arrays comentados anteriormente, el de steps, y el de cantidad de términos. Graficando la recta ajustada, y los valores originales, obtuve el siguiente gráfico:

![heaps-uno](https://raw.githubusercontent.com/AgustinNormand/recuperacion-de-informacion/main/TP_01/ejercicio_8/heaps_original.png)

Vemos al final un incremento significativo de tokens que llama la atención, que se desvía significativamente de lo estimado por la ley de Heaps. Lo que significa es que al final del texto, encuentra muchos términos nuevos.
Si observamos el final del texto, efectivamente vemos que hay un gran texto escrito en idioma ingés, de 2665 palabras, que al estar en un idioma diferente, el tokenizer encuentra muchos términos en esa seccion de texto.

Eliminando lo comentado anteriormente, y corriendo el código nuevamente, obtenemos el siguiente gráfico:

![heaps-dos](https://raw.githubusercontent.com/AgustinNormand/recuperacion-de-informacion/main/TP_01/ejercicio_8/heaps.png)

En donde vemos que este pico al final desapareció, logrando que la recta se ajuste aun mejor a la distribución de los datos crudos.

Por ultimo, para verificar en que medida se satisface la ley de Heaps, calculé el coeficiente de determinación, dado que al igual que en casos anteriores, seguimos en un contexto de predicción de datos futuros. 

Este coeficiente tiene el valor de 0.9991511720407505, confirmando lo que se ve en el gráfico, que la ley de Heaps se satisface ampliamente. La longitud del vocabulario, está en funcion de la longitud del documento, cuanto más avancemos en el procesamiento del texto, mayor dificultad tendremos en encontrar nuevos términos.

<!---

Pasar todos los archivos por el formatter que pidieron. Back,

Agregar allgun plot??

Si no es ninguna expresion regular, lo paso por el filtro de longitud de caracteres.

REGULAR EXPR

Email
distanciapedenfermeria@gmail.com0351-4334028/4043

URL
http://www.youtube.comhttp://www.youtube.com
'http://www.kennedy.edu.ar/';//window.location.href
'http://csi.gstatic.com/csi');


Abrebiation de Dr. Lic. Mg.
Estero.
Estero.
Campos.
Vegas.
Porta.
Quinteros.
Sandes.
Grippo.

Abrebiation de etc.
dr.
dr.
dr.
dra.
prof.
ed.
pag.
(Estos están bastante bien, pero mezclados con basura.)

familia.
biopolitica.
exclusion.
filosofia.
estado.
nazismo.
amor.
muerte.
razón.
occidente.
(estos son fin de parrafos? tendría que ver si la palabra siguiente arranca con mayuscula)

Abrebiation ([A-Z]\.)
DyN.
VIH.
AIRES.-
DT.
HABANA.
MADRID.-
W.
W.
CIA.
W.
UBA.
AIRES.-
M.
C.
YAKARTA.-
IDESA.
SPAM.









Notas: 

* Las palabras vacias, siguen siendo tokens en el documento? O no son ni tokens ni terminos?

* Los documentos se procesan linea a linea. Nombre propio separado en 2 lineas?
Si las parseo, como me fijo los nombres propios? Ya lo pregunte

Lo del largo del termino, debería ser despues de haber normaliado, traducido, etc. Ya lo pregunte

academicasfcfmnfchficesipaudedainformesdepartamentosareascargosdedicacioncaracterinscripcionresolucion
Porque no se limito ese termino? Resuelto



Elegir longitud minima y maxima tokens, documentar porque esa decision.

Cantidad de terminos es cantidaad univoca de terminos? Sería como las claves del diccionario?

Promedio de terminos de los documentos? Sumo todas las frecuencias de terminos y las divido por la cantida de documentoss? O es la cantidad de claves del diccionario dividido la cantidad de documentos?












Quijote:
Elimine la primera parte en inglés, hasta el titulo.
-->



