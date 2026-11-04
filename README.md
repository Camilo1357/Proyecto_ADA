**# Dónde construir: estaciones para una alcaldía nueva**



**## 1. Descripción del proyecto**



Este proyecto busca determinar en qué lotes conviene construir

estaciones de atención de incidentes para una alcaldía nueva,

considerando un presupuesto limitado.



El objetivo es seleccionar estaciones que maximicen el valor de los

incidentes cubiertos, respetando las restricciones de ubicación, tipo de

estación y presupuesto.



El proyecto representa la red vial mediante un grafo dirigido y compara

tres estrategias: Greedy base, una heurística propia basada en

eficiencia y un algoritmo exacto mediante fuerza bruta con Backtracking

y podas.



**## 2. Objetivo**



Desarrollar y comparar tres algoritmos:



1\.  Greedy base del profesor.

2\.  Heurística propia basada en eficiencia.

3\.  Algoritmo exacto mediante fuerza bruta con Backtracking.



La comparación considera el valor total de los incidentes cubiertos, el

costo, el presupuesto restante, el tiempo de ejecución y las

limitaciones de cada estrategia.



**## 3. Datos de entrada**



**&#xA0; -----------------------------------------------------------------------**

  Archivo                             Contenido

**&#xA0; ----------------------------------- -----------------------------------**

  \`nodos.csv\`                         Identificadores y coordenadas de

                                      los nodos.



  \`aristas.csv\`                       Conexiones dirigidas entre nodos y

                                      longitud de cada tramo.



  \`lotes.csv\`                         Lotes disponibles, nodo asociado y

                                      factor de zona.



  \`incidentes.csv\`                    Incidentes registrados, nodo, tipo

                                      y fecha.



  \`parametros.json\`                   Presupuesto y parámetros de cada

                                      tipo de estación.

  -----------------------------------------------------------------------



**### Tipos de incidentes**



\-   Hurto.

\-   Accidente.

\-   Incendio.



**### Parámetros base**



  Tipo          Costo base (millones)   Radio de cobertura   Peso

**&#xA0; ----------- ----------------------- -------------------- ------**

  Hurto                         1.000              1.000 m      1

  Accidente                     2.000              2.000 m      3

  Incendio                      5.000              3.000 m      5



El costo de una estación se calcula multiplicando el costo base por el

factor de zona del lote y aplicando el redondeo implementado en

\`calcular_costo()\`.



**## 4. Reglas del problema**



\-   Se puede construir como máximo una estación por lote.

\-   Se pueden construir varias estaciones del mismo tipo en lotes

    diferentes.

\-   Una estación solo cubre incidentes de su mismo tipo.

\-   Un incidente queda cubierto si la distancia mínima dirigida desde el

    nodo de la estación hasta el nodo del incidente no supera el radio

    de cobertura.

\-   Si varias estaciones cubren el mismo incidente, este se cuenta una

    sola vez.

\-   La suma de los costos de las estaciones no puede superar el

    presupuesto.

\-   Los incidentes de un mismo tipo tienen la misma prioridad.

\-   La fecha y hora del incidente no modifica su peso.

\-   Se permite que los vehículos utilicen los carriles de Metroplús,

    según los supuestos del problema.



**## 5. Instancias disponibles**



**&#xA0; -----------------------------------------------------------------------------**

  Instancia          Nodos      Aristas   Incidentes        Lotes   Presupuesto

                                                                     (millones)

**&#xA0; ----------- ------------ ------------ ------------ ------------ -------------**

  Pequeña                9           22           18            5         6.000



  Comuna             2.893        6.782          913           15        12.000



  Ciudad            27.568       67.330        5.300           80        40.000

  -----------------------------------------------------------------------------



**## 6. Estructura del proyecto**



\`\`\` text

Proyecto_ADA - copia/

├── estaciones_alcaldia/

│   ├── main.py

│   ├── datos/

│   │   └── lector_datos.py

│   ├── algoritmos/

│   │   ├── grafo.py

│   │   ├── distancias.py

│   │   ├── cobertura.py

│   │   ├── greedy_base.py

│   │   ├── heuristica_propia.py

│   │   └── exacto.py

│   ├── pruebas/

│   └── README.md

└── instancias/

    ├── pequena/

    ├── comuna/

    └── ciudad/

\`\`\`



Las instancias se encuentran fuera de la carpeta \`estaciones_alcaldia\`,

dentro de la carpeta \`instancias\`.



**## 7. Implementación**



**### 7.1. Construcción del grafo**



**\*\*Archivo:\*\*** \`algoritmos/grafo.py\`



Se construye un grafo dirigido a partir de las conexiones de la red

vial. Cada arista contiene el nodo de origen, el nodo de destino y la

longitud del tramo. Las longitudes se manejan como valores numéricos.



**### 7.2. Cálculo de distancias**



**\*\*Archivo:\*\*** \`algoritmos/distancias.py\`



Se utiliza Dijkstra implementado con \`heapq\` para calcular las

distancias mínimas desde un nodo de origen. El grafo es dirigido, por lo

que las distancias respetan el sentido de las conexiones. La

implementación requiere longitudes de arista no negativas. Los nodos

inalcanzables no aparecen en el diccionario de distancias.



**### 7.3. Cálculo de costos y cobertura**



**\*\*Archivo:\*\*** \`algoritmos/cobertura.py\`



Este módulo contiene las operaciones para:



\-   Calcular el costo de una estación según el factor de zona.

\-   Identificar los incidentes cubiertos por una estación.

\-   Evaluar las alternativas de estación para cada lote.

\-   Calcular el valor total de los incidentes cubiertos.

\-   Calcular el valor adicional aportado por una nueva estación.

\-   Construir un diccionario que asocia cada ID de incidente con su

    peso.



La evaluación de un lote calcula las distancias una sola vez y reutiliza

ese resultado para evaluar los distintos tipos de estación. Los

incidentes se identifican mediante conjuntos para evitar contar dos

veces un mismo ID.



**### 7.4. Greedy base del profesor**



**\*\*Archivo:\*\*** \`algoritmos/greedy_base.py\`



Este algoritmo selecciona en cada iteración la estación que aporta el

mayor valor adicional absoluto. No divide el valor adicional por el

costo.



Criterios de desempate:



1\.  Menor código de lote.

2\.  Orden de tipo: hurto, accidente e incendio.



El algoritmo respeta el presupuesto y evita seleccionar más de una

estación en el mismo lote.



**### 7.5. Heurística propia: eficiencia**



**\*\*Archivo:\*\*** \`algoritmos/heuristica_propia.py\`



La heurística propia utiliza la relación:



**\*\*Eficiencia = valor adicional / costo\*\***



En cada iteración se selecciona la alternativa factible con mayor

eficiencia. Después de seleccionar una estación, se descuenta su costo

del presupuesto, se marca su lote como utilizado y se actualiza el

conjunto de incidentes cubiertos.



Esta estrategia busca obtener un mayor aprovechamiento del presupuesto,

pero no garantiza encontrar la solución óptima.



**### 7.6. Algoritmo exacto: fuerza bruta con Backtracking y podas**



**\*\*Archivo:\*\*** \`algoritmos/exacto.py\`



La función \`fuerza_bruta()\` resuelve el problema mediante búsqueda

exhaustiva con Backtracking. No utiliza Greedy ni construye una solución

inicial heurística.



Para cada lote considera cuatro posibilidades:



1\.  No construir una estación.

2\.  Construir una estación de hurto.

3\.  Construir una estación de accidentes.

4\.  Construir una estación de incendios.



El algoritmo explora las combinaciones de alternativas y mantiene el

conjunto de incidentes cubiertos para contar cada incidente una sola

vez.



Para reducir el espacio de búsqueda utiliza:



\-   **\*\*Ordenamiento de lotes y alternativas:\*\*** modifica el orden de

    exploración, pero no elimina opciones ni determina por sí solo la

    solución.

\-   **\*\*Poda por presupuesto:\*\*** descarta una rama cuando el costo

    acumulado supera el presupuesto.

\-   **\*\*Poda por valor máximo restante:\*\*** calcula una cota superior

    optimista del valor que todavía podría alcanzarse. Si esa cota no

    puede mejorar la mejor solución conocida ---considerando también el

    desempate por costo---, descarta la rama.

\-   **\*\*Estado reversible:\*\*** agrega temporalmente los incidentes y las

    estaciones de una decisión y restaura el estado al retroceder,

    evitando copias innecesarias.



El criterio de optimización es:



1\.  Maximizar el valor total de los incidentes cubiertos.

2\.  En caso de empate en valor, minimizar el costo total.



Bajo las condiciones del modelo ---alternativas completas por lote,

costos y pesos no negativos e identificadores únicos de incidentes---,

las podas conservan la optimalidad.



**## 8. Resultados experimentales**



Los siguientes resultados corresponden a las ejecuciones reportadas para

Pequeña y Comuna. Los tiempos pueden variar según el equipo y el entorno

de ejecución.



**### 8.1. Instancia pequeña**



  Métrica                             Greedy base   Heurística propia     Exacto

**&#xA0; --------------------------------- ------------- ------------------- ----------**

  Valor total                                  15                  19     **\*\*20\*\***

  Costo total (millones)                    5.500               5.100      5.400

  Presupuesto restante (millones)             500                 900        600

  Tiempo (segundos)                      0.000426            0.000729   0.002632



El algoritmo exacto obtuvo el mayor valor de cobertura: 20 puntos, con

un costo de 5.400 millones y 600 millones de presupuesto restante.



La solución exacta reportada selecciona:



  Lote        Tipo de estación     Costo (millones)

**&#xA0; ----------- ------------------ ------------------**

  L1          Hurto                           1.100

  L3          Accidente                       2.800

  L4          Hurto                           1.500

  **\*\*Total\*\***                               **\*\*5.400\*\***



La ejecución reportó 12 incidentes cubiertos. El resultado exacto supera

en 5 puntos al Greedy base y en 1 punto a la heurística propia.



**### 8.2. Instancia comuna**



  Métrica                             Greedy base   Heurística propia      Exacto

**&#xA0; --------------------------------- ------------- ------------------- -----------**

  Valor total                               1.529               1.492   **\*\*1.574\*\***

  Costo total (millones)                   11.950              11.600      11.700

  Presupuesto restante (millones)              50                 400         300

  Tiempo (segundos)                      0.100222            0.102936   19.454549



El algoritmo exacto obtuvo el mayor valor de cobertura: 1.574 puntos,

con un costo de 11.700 millones y 300 millones de presupuesto restante.



En comparación con las otras estrategias:



\-   Supera al Greedy base en 45 puntos.

\-   Supera a la heurística propia en 82 puntos.

\-   Su tiempo de ejecución fue de aproximadamente 19,45 segundos, por

    debajo del objetivo de un minuto establecido para Comuna.



El resultado muestra el costo computacional adicional de la búsqueda

exacta frente a las estrategias voraces. En esta instancia, el

Backtracking con podas encuentra una propuesta de mayor valor y cumple

el límite de tiempo esperado.



**### 8.3. Instancia ciudad**



La instancia Ciudad contiene 80 lotes. Si cada lote tiene tres tipos de
estación posibles y la opción de no construir, el espacio teórico de
decisiones es:



\[ 4^{80} pprox 1,46 	imes 10^{48} \]



combinaciones.



Este número representa el espacio máximo teórico antes de aplicar las
podas. Las podas pueden reducir la búsqueda efectiva, pero no eliminan
el crecimiento exponencial del peor caso. En las pruebas realizadas,
la ejecución del algoritmo exacto no terminó en un tiempo práctico,
por lo que se interrumpió y no se reporta una solución óptima para
Ciudad. Esto es coherente con el alcance del enunciado, que no exige
obtener el óptimo exacto de esta instancia.



Los resultados de las dos heurísticas voraces son:



| Métrica | Greedy base | Heurística propia |
|---|---:|---:|
| Valor total | 7.591 | **7.706** |
| Costo total (millones) | 39.850 | 39.950 |
| Presupuesto restante (millones) | 150 | 50 |
| Incidentes cubiertos | 3.301 | **3.738** |
| Tiempo (segundos) | 7,380910 | 7,722432 |



La heurística propia obtuvo 115 puntos más de valor que Greedy base
(aproximadamente 1,51 % de mejora) y cubrió 437 incidentes adicionales
(aproximadamente 13,24 % más). Para conseguirlo utilizó 100 millones
adicionales y tardó aproximadamente 0,34 segundos más. Ambas propuestas
respetaron el presupuesto de 40.000 millones.



Por valor y cantidad de incidentes cubiertos, la heurística propia es
la propuesta voraz recomendada provisionalmente para Ciudad. Su costo
fue de 39.950 millones, por lo que dejó 50 millones de presupuesto
disponible.



El tiempo de evaluación de todos los lotes y tipos de estación de la
Parte 1 debe reportarse por separado del tiempo de ejecución de las
heurísticas. Ese dato todavía debe incorporarse cuando se confirme la
medición correspondiente.



**## 9. Complejidad y análisis**



**### Dijkstra**



Con listas de adyacencia y cola de prioridad, la complejidad habitual

es:



\\[ O((V+E)\`\log \`{=tex}V) \\]



donde (V) es la cantidad de nodos y (E) la cantidad de aristas.



**### Greedy base**



En cada iteración se revisan las alternativas de los lotes que todavía

no han sido utilizados. La cantidad de iteraciones está limitada por el

número de lotes, porque se selecciona como máximo una estación por lote.



**### Heurística propia**



Tiene una estructura de búsqueda voraz similar a la del Greedy base,

pero cambia el criterio de selección: maximiza la relación entre valor

adicional y costo.



**### Algoritmo exacto**



Con (L) lotes y tres tipos de estación, existen hasta:



\\[ 4\\^L \\]



combinaciones teóricas, contando la opción de no construir.



El Backtracking explora este espacio y utiliza podas por presupuesto y

por valor máximo restante para reducir las ramas examinadas. Estas podas

preservan la optimalidad, pero no eliminan el crecimiento exponencial

del peor caso.



Los resultados experimentales muestran que el método es viable para

Pequeña y Comuna en los tiempos medidos. Para Ciudad, cuyo espacio

teórico alcanza (4\\^{80}), no se reporta una solución exacta.



**## 10. Restricciones técnicas**



La implementación utiliza Python y las herramientas permitidas para el

proyecto.



Se utilizan:



\-   \`csv\` y \`json\` para lectura de datos.

\-   \`pandas\` para manipulación de datos cuando corresponde.

\-   \`heapq\` para la cola de prioridad de Dijkstra.

\-   \`time\` para medir tiempos de ejecución.



No se utilizan librerías externas para resolver rutas, distancias o

combinaciones de optimización. Se respetan las restricciones del

enunciado respecto a librerías como \`networkx\`, \`osmnx\`, \`scipy\` e

\`itertools\`.



**## 11. Visualización**



Está pendiente completar:



\-   Mapa de la instancia Ciudad.

\-   Identificación de lotes utilizados y no utilizados.

\-   Ubicación de las estaciones seleccionadas por tipo.

\-   Visualización de incidentes cubiertos y no cubiertos.

\-   Tabla de estaciones con lote, tipo, costo e incidentes cubiertos.

\-   Resumen de presupuesto, valor y cobertura por tipo de incidente.

\-   Mapa y tabla de la solución de la instancia Comuna.



**## 12. Pruebas y estado de avance**



\-   [x] Construcción del grafo en Pequeña y Comuna.

\-   [x] Manejo de longitudes decimales en las aristas.

\-   [x] Pruebas de cobertura y costos en Pequeña.

\-   [x] Verificación de resultados de cobertura con la referencia

    disponible.

\-   [x] Ejecución del Greedy base.

\-   [x] Ejecución de la heurística propia.

\-   [x] Comparación de Greedy base y heurística propia en Pequeña y

    Comuna.

\-   [x] Ejecución del algoritmo exacto en Pequeña.

\-   [x] Obtención del valor 20 para el algoritmo exacto en Pequeña.

\-   [x] Ejecución del algoritmo exacto en Comuna.

\-   [x] Obtención del valor 1.574 para el algoritmo exacto en Comuna.

\-   [x] Medición de tiempos de los tres algoritmos en Pequeña y Comuna.

\-   [x] Ejecución y comparación de Greedy base y heurística propia en Ciudad.

\-   [ ] Registrar y verificar el tiempo de evaluación de lotes y tipos de estación de la Parte 1 en Ciudad (límite: menos de 60 segundos).

\-   [ ] Contraejemplo manual de máximo seis nodos para cada heurística.

\-   [ ] Mapas y tablas de resultados para Ciudad y Comuna.

\-   [ ] Pruebas de procesamiento de nuevos lotes e incidentes sin

    depender de IDs fijos.



**## 13. Consideraciones para la sustentación**



Durante la sustentación se debe explicar:



1\.  Cómo se representa la red vial mediante un grafo dirigido.

2\.  Cómo se calculan las distancias mínimas.

3\.  Cómo se determina la cobertura de una estación.

4\.  Cómo se calcula el valor adicional de una alternativa.

5\.  En qué se diferencia el Greedy base de la heurística propia.

6\.  Cómo funciona la búsqueda exacta con Backtracking y sus podas.

7\.  Por qué el algoritmo exacto no es práctico para la instancia Ciudad.

8\.  Qué ventajas y limitaciones tiene cada estrategia.

9\.  Cómo se procesan nuevos datos sin depender de identificadores o

    valores fijos.



**## 14. Estado general del proyecto**



El proyecto cuenta con la construcción del grafo dirigido, el cálculo de

distancias mediante Dijkstra, la evaluación de costos y cobertura, dos

algoritmos voraces y un algoritmo exacto mediante fuerza bruta con

Backtracking y podas.



Los tres algoritmos se ejecutaron en las instancias Pequeña y Comuna. En
Pequeña, el algoritmo exacto obtuvo un valor de 20 y un costo de 5.400
millones, con un tiempo medido de 0,002632 segundos. En Comuna, obtuvo
un valor de 1.574 y un costo de 11.700 millones, con un tiempo medido de
19,454549 segundos.



En ambas instancias, el algoritmo exacto obtuvo el mayor valor de
cobertura entre las tres estrategias comparadas. En Comuna, además,
cumplió el objetivo de ejecución inferior a un minuto.



En Ciudad, Greedy base obtuvo un valor de 7.591 y la heurística propia
un valor de 7.706. Esta última cubrió 3.738 incidentes, frente a 3.301
de Greedy base, con un costo de 39.950 millones dentro del presupuesto
de 40.000 millones. No se reporta una solución exacta para Ciudad
porque la ejecución no terminó en un tiempo práctico y el enunciado no
exige obtener el óptimo exacto para esta instancia.



Permanecen pendientes el tiempo de evaluación de la Parte 1 en Ciudad,
los contraejemplos manuales de las heurísticas, las visualizaciones y
tablas de Ciudad y Comuna, y las pruebas con nuevos datos sin depender
de identificadores fijos.
