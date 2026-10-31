# Dónde construir: estaciones para una alcaldía nueva

## 1. Objetivo

Seleccionar estaciones de atención de emergencias en lotes disponibles
para maximizar el valor de los incidentes cubiertos sin exceder el
presupuesto. El escenario usa una red vial de Medellín y datos simulados
de incidentes, lotes, factores de zona y costos.

La especificación oficial está en el [notebook del
proyecto](https://github.com/callejohnathan/udem_analisis_y_diseno_de_algoritmos/blob/main/material_de_apoyo/proyectos_finales/20262_estaciones/practica_estaciones.ipynb).
Si este resumen difiere de una versión posterior del notebook, prevalece
el documento oficial.

## 2. Datos de entrada

Cada instancia contiene:

  -----------------------------------------------------------------------
  Archivo                             Contenido
  ----------------------------------- -----------------------------------
  `nodos.csv`                         Identificador, latitud y longitud
                                      de cada nodo.

  `aristas.csv`                       Tramos dirigidos: origen, destino,
                                      longitud en metros y nombre de vía.

  `lotes.csv`                         Código de lote, nodo asociado y
                                      factor de zona.

  `incidentes.csv`                    ID, nodo, tipo y fecha/hora del
                                      incidente.

  `parametros.json`                   Presupuesto y parámetros de cada
                                      tipo de estación.
  -----------------------------------------------------------------------

Cada fila de `aristas.csv` representa un tramo dirigido. Una vía de
doble sentido aparece como dos aristas, una en cada dirección. No se
debe inferir que existe la arista inversa. El grafo es dirigido y
ponderado por `longitud_m`.

### Instancias

  -----------------------------------------------------------------------------
  Instancia          Nodos      Aristas   Incidentes        Lotes   Presupuesto
                              dirigidas                              (millones)
  ----------- ------------ ------------ ------------ ------------ -------------
  `pequena`              9           22           18            5         6.000

  `comuna`           2.893        6.782          913           15        12.000

  `ciudad`          27.568       67.330        5.300           80        40.000
  -----------------------------------------------------------------------------

El programa debe cargar cualquier instancia con el mismo formato; no
puede depender de IDs, cantidades o valores particulares.

## 3. Parámetros y reglas del problema

En la instancia pequeña se verificaron estos parámetros:

  Tipo          Estación                         Costo base (millones)   Radio (m)   Peso
  ------------- ------------------------------ ----------------------- ----------- ------
  `hurto`       CAI                                              1.000       1.000      1
  `accidente`   Estación de tránsito y grúas                     2.000       2.000      3
  `incendio`    Estación de bomberos                             5.000       3.000      5

Los valores efectivos deben leerse desde `parametros.json`, no
codificarse para una sola instancia.

-   Se puede construir como máximo una estación por lote; un lote puede
    quedar sin usar.
-   Se permiten estaciones del mismo tipo en lotes diferentes.
-   El costo es el costo base del tipo multiplicado por el factor de
    zona del lote, redondeado al millón más cercano.
-   Debe verificarse la regla de redondeo en empates: `round()` de
    Python usa redondeo al par.
-   Un incidente solo queda cubierto si coincide el tipo, existe una
    ruta dirigida desde el nodo de la estación al nodo del incidente y
    la distancia mínima es menor o igual al radio.
-   La dirección importa: se calcula desde la estación hacia el
    incidente. No se usa distancia en línea recta.
-   Un incidente inaccesible en esa dirección no queda cubierto.
-   El valor de la solución es la suma de los pesos de los incidentes
    cubiertos. Cada ID se cuenta una sola vez, aunque lo cubran varias
    estaciones.
-   Supuestos del enunciado: los vehículos pueden usar carriles de
    Metroplús; incidentes del mismo tipo tienen igual prioridad; la
    fecha/hora no pondera la importancia.

Formalmente, una estación de tipo `t` ubicada en `s` cubre un incidente
de tipo `t` en `v` si:

\[ d\_{`\text{dirigida}`{=tex}}(s,v) `\leq `{=tex}R(t) \]

El valor de una solución es:

\[ V(S)=`\sum`{=tex}\_{i`\in `{=tex}I(S)}
w(`\operatorname{tipo}`{=tex}(i)) \]

donde `I(S)` contiene los IDs únicos cubiertos.

## 4. Entregables del enunciado

### Parte 1: costos y coberturas

Para cada lote y tipo de estación, calcular el costo y la lista ordenada
de IDs cubiertos. La instancia `ciudad` debe procesarse en menos de un
minuto. Es importante no ejecutar Dijkstra repetidamente para el mismo
lote si sus distancias pueden reutilizarse entre tipos de estación.

### Parte 2: heurísticas

**2.1. Greedy base del profesor.** Selecciona iterativamente la estación
con mayor valor adicional absoluto, respetando presupuesto y un máximo
de una estación por lote. Desempata por código de lote y luego por tipo
en el orden `hurto`, `accidente`, `incendio`.

**2.2. Heurística propia.** El equipo debe diseñar una heurística que
construya la solución seleccionando una estación a la vez y supere el
valor del Greedy base en al menos una de las tres instancias. Debe
aplicarse a pequeña, comuna y ciudad.

La propuesta propia que se ha venido desarrollando es un **Greedy por
eficiencia**:

1.  Calcular el valor adicional de cada candidata respecto de los
    incidentes ya cubiertos.
2.  Dividir el valor adicional entre el costo.
3.  Elegir la candidata factible con mayor relación valor/costo.
4.  Actualizar estaciones seleccionadas, lotes ocupados, presupuesto e
    IDs cubiertos.
5.  Repetir mientras haya candidatas factibles que aporten valor.

\[ E(l,t)=`\frac{\text{valor adicional}(l,t)}{\text{costo}(l,t)}`{=tex}
\]

El valor adicional excluye incidentes ya cubiertos. Se debe definir y
documentar un desempate determinista. Esta heurística es la propuesta
del equipo; no es el Greedy base. En código debe tener un nombre
inequívoco, por ejemplo `greedy_eficiencia` o `heuristica_eficiencia`.

**Contraejemplos.** Para cada heurística que pide el enunciado,
construir manualmente una instancia de máximo seis nodos en la que no
encuentre la mejor propuesta posible y explicar la decisión local que
conduce al resultado inferior.

### Parte 3: óptimo y comparación

Se solicita obtener una solución de mayor valor garantizada para pequeña
y comuna. Esto exige un método exacto; una heurística no garantiza
optimalidad.

Se está considerando **búsqueda exhaustiva mediante Backtracking con
poda por presupuesto**. Solo se pueden podar ramas que no puedan
producir una solución factible. Debe medirse su rendimiento y
conservarse la garantía de optimalidad.

Para cada instancia se comparan valor y tiempo de: - Greedy base del
profesor. - Heurística propia. - Óptimo, cuando corresponda.

Para ciudad se debe justificar con un cálculo y análisis de complejidad
por qué no se reporta el óptimo si no es computacionalmente viable.

La solución óptima de pequeña y comuna debe informar estaciones
ordenadas por lote, costo total, casos cubiertos por tipo, valor y
tiempo.

**Advertencia:** con 15 lotes y cuatro alternativas por lote (no
instalar o instalar uno de tres tipos), comuna tiene hasta
(4\^{15}=1.073.741.824) asignaciones. Backtracking sencillo podría ser
demasiado lento. Se deben evaluar podas más fuertes o un método exacto
alternativo, sin perder la garantía.

### Parte 4: mapas y propuesta

Para ciudad, elegir una propuesta heurística y mostrar un mapa que
distinga lotes sin usar, estaciones por tipo e incidentes cubiertos/no
cubiertos. Acompañar con tabla de estación, lote, tipo, costo y casos
cubiertos; costo total frente al presupuesto; casos por tipo; valor y
justificación.

Repetir mapa y tabla para la mejor propuesta posible de comuna (óptimo
de la Parte 3). Los mapas son obligatorios. Una GUI adicional para la
feria es opcional si el equipo decide competir.

## 5. Arquitectura algorítmica

### Algoritmos de soporte

-   **Construcción del grafo:** lista de adyacencia dirigida.
-   **Dijkstra:** distancias mínimas dirigidas desde el nodo de cada
    lote.
-   **Cobertura:** filtra incidentes por tipo y radio.
-   **Costo:** aplica costo base y factor de zona.
-   **Valor:** suma pesos de IDs únicos cubiertos.

Dijkstra no selecciona estaciones: es el componente de caminos mínimos
que permite calcular coberturas.

### Algoritmos de optimización

1.  **Greedy base del profesor:** referencia requerida para comparación.
2.  **Greedy propio por eficiencia:** heurística del equipo.
3.  **Algoritmo exacto:** Backtracking con poda u otro método exacto que
    garantice el óptimo en pequeña y comuna.

## 6. Restricciones técnicas

Implementación en Python. El enunciado permite `csv`, `json` y `pandas`
para lectura; `heapq` para la cola de prioridad; y herramientas como
`folium`, `matplotlib`, `streamlit` o `tkinter` para visualización,
siempre que no calculen rutas, distancias en grafos o combinaciones.

No utilizar `networkx`, `osmnx`, `scipy`, `itertools` ni otras librerías
que resuelvan por el equipo los cálculos de rutas, distancias o
combinaciones. La lógica algorítmica central debe ser propia.

## 7. Estructura local de trabajo conocida

``` text
Proyecto_ADA - copia/
├── estaciones_alcaldia/
│   ├── main.py
│   ├── datos/
│   │   └── lector_datos.py
│   ├── algoritmos/
│   │   ├── grafo.py
│   │   ├── distancias.py
│   │   ├── cobertura.py
│   │   ├── greedy.py
│   │   └── fuerza_bruta.py
│   ├── pruebas/
│   └── README.md
└── instancias/
    ├── pequena/
    ├── comuna/
    └── ciudad/
```

Es la estructura local conocida durante el desarrollo; verificar los
archivos reales antes de afirmar que todos existen o están terminados.

## 8. Implementación conocida y observaciones

-   `datos/lector_datos.py`: carga CSV y JSON, valida `pequena`,
    `comuna` o `ciudad` y devuelve nodos, calles, lotes, incidentes y
    parámetros. La clave de presupuesto es `presupuesto_millones`.
-   `algoritmos/grafo.py`: construye lista de adyacencia dirigida; no
    agrega aristas inversas que no estén en los datos.
-   `algoritmos/distancias.py`: Dijkstra con `heapq`, devuelve
    `nodo -> distancia mínima`; presupone longitudes no negativas.
-   `algoritmos/cobertura.py`: calcula costos, coberturas y valores. La
    cobertura se mide desde el nodo de estación hacia el incidente.
-   `algoritmos/greedy.py`: una versión que se probó seleccionaba por
    valor adicional/costo, por lo que era nuestra heurística propia
    aunque la función se llamara `greedy_base`. Corregir el nombre para
    no confundirla con la base del profesor.
-   `fuerza_bruta.py`: se propuso una búsqueda recursiva con
    Backtracking, unión de conjuntos para evitar duplicados y poda por
    presupuesto. Su existencia y ejecución satisfactoria deben
    confirmarse; no asumir que ya está validada.

**Optimización pendiente:** calcular Dijkstra una sola vez por lote y
reutilizar el mapa de distancias para los tres tipos de estación. Cambia
el radio y el filtro de tipo, no el nodo de origen. Esto evita hasta
tres ejecuciones redundantes por lote y ayuda a cumplir el límite de
ciudad.

## 9. Resultados de la instancia pequeña registrados

### Costos y coberturas por lote

  Lote     Nodo   Factor Tipo          Costo (millones) IDs cubiertos
  ------ ------ -------- ----------- ------------------ -------------------
  L1          1      1,1 hurto                    1.100 7, 8, 12, 13
  L1          1      1,1 accidente                2.200 1, 2, 3, 4
  L1          1      1,1 incendio                 5.500 16, 17, 18
  L2          3      1,5 hurto                    1.500 9, 10, 11, 12, 13
  L2          3      1,5 accidente                3.000 3, 4, 5
  L2          3      1,5 incendio                 7.500 16, 17, 18
  L3          5      1,4 hurto                    1.400 8, 15
  L3          5      1,4 accidente                2.800 1, 2, 4, 6
  L3          5      1,4 incendio                 7.000 16, 17, 18
  L4          6      1,5 hurto                    1.500 9, 10, 11, 14
  L4          6      1,5 accidente                3.000 3, 5, 6
  L4          6      1,5 incendio                 7.500 17, 18
  L5          8      1,5 hurto                    1.500 14, 15
  L5          8      1,5 accidente                3.000 3, 5, 6
  L5          8      1,5 incendio                 7.500 17, 18

Dos pruebas oficiales coinciden con estos resultados: L3 accidente
cuesta 2.800 y cubre `[1, 2, 4, 6]`; L2 hurto cuesta 1.500 y cubre
`[9, 10, 11, 12, 13]`.

### Heurística propia por eficiencia: ejecución registrada

-   L1 accidente: costo 2.200, valor adicional 12, IDs `[1, 2, 3, 4]`.
-   L2 hurto: costo 1.500, valor adicional 5, IDs `[9, 10, 11, 12, 13]`.
-   L3 hurto: costo 1.400, valor adicional 2, IDs `[8, 15]`.
-   Costo total: 5.100 millones; presupuesto restante: 900 millones.
-   Valor total: 19.
-   IDs únicos cubiertos: `[1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 15]`.

Es un resultado local registrado y debe repetirse con la versión final
del código.

### Greedy base del profesor: resultados de referencia identificados

**Pequeña:** L1 incendio; costo 5.500 millones; tres incendios
cubiertos; valor 15.

**Comuna:** L05 accidente, L06 hurto, L08 accidente, L09 incendio, L13
hurto, L14 hurto y L15 accidente; costo 11.950 millones; 486 hurtos, 296
accidentes y 31 incendios; valor 1.529.

Verificar estos resultados con el notebook vigente antes de la entrega.

### Óptimo conocido de pequeña

-   Estaciones: L1 hurto, L3 accidente y L4 hurto.
-   Costo: 5.400 millones.
-   Cobertura: 8 hurtos, 4 accidentes y 0 incendios.
-   Valor: 20.

El algoritmo exacto debe encontrar ese valor o una solución distinta
empatada en el óptimo.

## 10. Validaciones necesarias

1.  Carga correcta de las tres instancias.
2.  Dirección de las aristas preservada.
3.  Distancias mínimas de Dijkstra correctas.
4.  Coincidencia del tipo de estación e incidente.
5.  Radio inclusivo: `distancia <= radio_m`.
6.  Incidentes no alcanzables en la dirección correcta no se cubren.
7.  IDs repetidos se cuentan una sola vez.
8.  Presupuesto nunca excedido.
9.  Máximo una estación por lote.
10. Algoritmo exacto devuelve valor 20 en pequeña.
11. Parte 1 para ciudad termina en menos de un minuto.
12. Tiempos comparativos medidos y reproducibles.

## 11. Complejidad y análisis

Sean `V` nodos, `E` aristas dirigidas, `L` lotes e `I` incidentes.
Dijkstra con `heapq` tiene complejidad aproximada
(O((V+E)`\log `{=tex}V)) por origen. Ejecutándolo una vez por lote, el
costo de distancias es aproximadamente (O(L(V+E)`\log `{=tex}V)), más el
trabajo de evaluar incidentes y tipos.

La heurística debe analizarse según sus iteraciones, candidatas y costo
de calcular valores adicionales. El algoritmo exacto tiene un espacio de
búsqueda exponencial: hasta (4\^L) asignaciones (no instalar o elegir
uno de tres tipos por lote). La poda reduce ramas, pero no elimina en
general el crecimiento exponencial.

## 12. Rúbrica compartida

  Criterio                          Peso
  ------------------------------- ------
  Modelado del grafo                10 %
  Implementación de algoritmos      10 %
  Comparación de algoritmos         10 %
  Visualización geográfica           5 %
  Calidad técnica                    5 %
  Explicación de algoritmos         15 %
  Uso de técnicas algorítmicas      10 %
  Análisis de complejidad           10 %
  Análisis de trade-offs            15 %
  Claridad y dominio conceptual     10 %

Explicación de algoritmos, trade-offs y claridad/dominio conceptual
suman 45 % de la rúbrica.

## 13. Sustentación

En la sustentación el equipo recibirá una nueva distribución de lotes y
un nuevo histórico de incidentes con el mismo formato. El código debe
procesarlos sin depender de las instancias actuales ni de resultados
precalculados. El equipo debe poder explicar modelado, algoritmos,
garantías, complejidad, decisiones y compromisos entre calidad de
solución y tiempo.

## 14. Lista de trabajo pendiente

-   [x] Lectura inicial de CSV y JSON.
-   [x] Construcción inicial del grafo dirigido.
-   [x] Implementación inicial de Dijkstra.
-   [x] Cálculo inicial de costos y coberturas.
-   [x] Pruebas de cobertura pequeña contrastadas con el notebook.
-   [x] Primera ejecución registrada de la heurística propia por
    eficiencia.
-   [ ] Implementar y validar el Greedy base del profesor para
    reproducir la referencia.
-   [ ] Diferenciar nombres de Greedy base y heurística propia.
-   [ ] Reutilizar una ejecución de Dijkstra por lote.
-   [ ] Construir contraejemplos manuales para las heurísticas.
-   [ ] Implementar y validar el óptimo de pequeña.
-   [ ] Medir y optimizar el método exacto para comuna.
-   [ ] Ejecutar base y heurística propia en las tres instancias.
-   [ ] Registrar tiempos reproducibles y completar la tabla
    comparativa.
-   [ ] Generar mapas y tablas de ciudad y comuna.
-   [ ] Documentar complejidad, trade-offs y justificación.
-   [ ] Probar con una instancia nueva antes de la sustentación.

**Regla de mantenimiento:** actualizar este documento cuando cambien la
estructura real, los nombres de funciones, los resultados medidos o las
decisiones de diseño. No marcar como terminado un componente que solo
esté propuesto o que no se haya ejecutado y validado.
