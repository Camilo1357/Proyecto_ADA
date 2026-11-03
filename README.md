# Dónde construir: estaciones para una alcaldía nueva

## 1. Descripción del proyecto

Este proyecto busca determinar en qué lotes conviene construir estaciones de atención de incidentes para una alcaldía nueva, considerando un presupuesto limitado.

El objetivo es seleccionar estaciones que maximicen el valor de los incidentes cubiertos, respetando las restricciones de ubicación, tipo de estación y presupuesto.

El proyecto utiliza un grafo dirigido para representar la red vial y algoritmos de optimización para comparar diferentes estrategias de selección de estaciones.

## 2. Objetivo

Desarrollar y comparar tres algoritmos para seleccionar estaciones:

1. Greedy base del profesor.
2. Heurística propia basada en eficiencia.
3. Algoritmo exacto mediante fuerza bruta con poda por presupuesto.

Se busca analizar la calidad de las soluciones, el costo, el tiempo de ejecución y las limitaciones de cada estrategia.

## 3. Datos de entrada

El proyecto utiliza cuatro archivos de datos y un archivo de parámetros.

| Archivo | Contenido |
|---|---|
| `nodos.csv` | Identificadores y coordenadas de los nodos. |
| `aristas.csv` | Conexiones dirigidas entre nodos y longitud de cada tramo. |
| `lotes.csv` | Lotes disponibles, nodo asociado y factor de zona. |
| `incidentes.csv` | Incidentes registrados, nodo, tipo y fecha. |
| `parametros.json` | Presupuesto y parámetros de cada tipo de estación. |

### Tipos de incidentes

- Hurto.
- Accidente.
- Incendio.

### Parámetros base

| Tipo | Costo base (millones) | Radio de cobertura | Peso |
|---|---:|---:|---:|
| Hurto | 1.000 | 1.000 m | 1 |
| Accidente | 2.000 | 2.000 m | 3 |
| Incendio | 5.000 | 3.000 m | 5 |

El costo de una estación se calcula multiplicando el costo base por el factor de zona del lote y aplicando el redondeo definido por la implementación.

## 4. Reglas del problema

- Se puede construir máximo una estación por lote.
- Se pueden construir varias estaciones del mismo tipo en lotes diferentes.
- Una estación solo cubre incidentes de su mismo tipo.
- Un incidente queda cubierto si la distancia mínima dirigida desde el nodo de la estación hasta el nodo del incidente no supera el radio de cobertura.
- Si varias estaciones cubren el mismo incidente, este se cuenta una sola vez.
- La suma de los costos de las estaciones no puede superar el presupuesto.
- Los incidentes de un mismo tipo tienen la misma prioridad.
- La fecha y hora del incidente no modifica su peso.
- Se permite que los vehículos utilicen los carriles de Metroplús, según los supuestos del problema.

## 5. Instancias disponibles

| Instancia | Nodos | Aristas | Incidentes | Lotes | Presupuesto (millones) |
|---|---:|---:|---:|---:|---:|
| Pequeña | 9 | 22 | 18 | 5 | 6.000 |
| Comuna | 2.893 | 6.782 | 913 | 15 | 12.000 |
| Ciudad | 27.568 | 67.330 | 5.300 | 80 | 40.000 |

## 6. Estructura del proyecto

La estructura de carpetas reportada para el desarrollo es:

```text
Proyecto_ADA - copia/
├── estaciones_alcaldia/
│   ├── main.py
│   ├── datos/
│   │   └── lector_datos.py
│   ├── algoritmos/
│   │   ├── grafo.py
│   │   ├── distancias.py
│   │   ├── cobertura.py
│   │   ├── greedy_base.py
│   │   ├── heuristica_propia.py
│   │   └── exacto.py
│   ├── pruebas/
│   └── README.md
└── instancias/
    ├── pequena/
    ├── comuna/
    └── ciudad/
```

Las instancias se encuentran fuera de la carpeta `estaciones_alcaldia`, dentro de la carpeta `instancias`.

## 7. Implementación

### 7.1. Construcción del grafo

Archivo: `algoritmos/grafo.py`

Se construye un grafo dirigido a partir de las conexiones de la red vial.

Cada arista contiene:

- Nodo de origen.
- Nodo de destino.
- Longitud del tramo.

Las longitudes se manejan como valores numéricos de tipo `float`.

### 7.2. Cálculo de distancias

Archivo: `algoritmos/distancias.py`

Se utiliza el algoritmo de Dijkstra implementado con `heapq` para calcular las distancias mínimas desde un nodo de origen.

El grafo es dirigido, por lo que las distancias se calculan respetando el sentido de las conexiones.

### 7.3. Cálculo de costos y cobertura

Archivo: `algoritmos/cobertura.py`

Este módulo contiene las operaciones para:

- Calcular el costo de una estación según el factor de zona.
- Identificar los incidentes cubiertos por una estación.
- Evaluar las alternativas de estación para cada lote.
- Calcular el valor total de los incidentes cubiertos.
- Calcular el valor adicional aportado por una nueva estación.

Los incidentes se almacenan en conjuntos para evitar contar varias veces un mismo identificador.

### 7.4. Greedy base del profesor

Archivo: `algoritmos/greedy_base.py`

Este algoritmo selecciona en cada iteración la estación que aporta el mayor valor adicional absoluto.

No divide el valor adicional por el costo.

Criterios de desempate:

1. Menor código de lote.
2. Orden de tipo: hurto, accidente e incendio.

El algoritmo respeta el presupuesto y evita seleccionar más de una estación en el mismo lote.

### 7.5. Heurística propia: eficiencia

Archivo: `algoritmos/heuristica_propia.py`

La heurística propia utiliza una relación entre el valor adicional y el costo de cada estación.

Su criterio es:

**Eficiencia = valor adicional / costo**

En cada iteración se selecciona la alternativa factible con mayor eficiencia.

Después de seleccionar una estación:

- Se descuenta su costo del presupuesto.
- Se marca su lote como utilizado.
- Se actualiza el conjunto de incidentes cubiertos.

Esta estrategia busca obtener un mayor aprovechamiento del presupuesto.

### 7.6. Algoritmo exacto: fuerza bruta con poda

Archivo: `algoritmos/exacto.py`

La función `fuerza_bruta()` examina las alternativas de estación de cada lote.

Para cada lote considera cuatro posibilidades:

1. No construir una estación.
2. Construir una estación de hurto.
3. Construir una estación de accidentes.
4. Construir una estación de incendios.

El algoritmo combina las alternativas de todos los lotes y calcula el valor total de cada solución factible.

Se utiliza una poda por presupuesto: cuando el costo acumulado supera el presupuesto disponible, se descarta esa rama de búsqueda.

El algoritmo garantiza encontrar una solución óptima porque examina todas las combinaciones factibles.

En caso de empate en valor, se prefiere la solución de menor costo.

## 8. Resultados obtenidos

### 8.1. Instancia pequeña

Se realizaron pruebas de costos, cobertura y valor de incidentes.

Algunos resultados de referencia:

| Lote | Tipo | Costo (millones) | Incidentes cubiertos |
|---|---|---:|---|
| L1 | Hurto | 1.100 | 7, 8, 12, 13 |
| L1 | Accidente | 2.200 | 1, 2, 3, 4 |
| L1 | Incendio | 5.500 | 16, 17, 18 |
| L2 | Hurto | 1.500 | 9, 10, 11, 12, 13 |
| L3 | Accidente | 2.800 | 1, 2, 4, 6 |
| L4 | Hurto | 1.500 | 9, 10, 11, 14 |
| L5 | Hurto | 1.500 | 14, 15 |

#### Resultados de los algoritmos

| Algoritmo | Valor total | Costo total (millones) |
|---|---:|---:|
| Greedy base | 15 | 5.500 |
| Heurística propia | 19 | 5.100 |
| Exacto | 20 | 5.400 |

La heurística propia obtiene un valor superior al Greedy base en esta instancia.

El algoritmo exacto encuentra la solución óptima:

| Lote | Tipo | Costo (millones) |
|---|---|---:|
| L1 | Hurto | 1.100 |
| L3 | Accidente | 2.800 |
| L4 | Hurto | 1.500 |
| **Total** | | **5.400** |

Resultado del algoritmo exacto:

- Valor total: 20.
- Costo total: 5.400 millones.
- Presupuesto restante: 600 millones.
- Incidentes cubiertos: 12.
- Combinaciones completas evaluadas: 97.

El resultado coincide con el valor óptimo de referencia de la instancia pequeña.

#### Tiempos de ejecución

Se midió el tiempo de ejecución de cada algoritmo utilizando `time.perf_counter()`.

| Algoritmo | Tiempo (segundos) |
|---|---:|
| Greedy base | 0,000200 |
| Heurística propia | 0,000232 |
| Exacto | 0,000775 |

En la instancia pequeña, el Greedy base presentó el menor tiempo de ejecución, seguido de la heurística propia y el algoritmo exacto.

El algoritmo exacto tardó aproximadamente 3,9 veces más que el Greedy base, pero encontró la solución óptima, con un valor total de 20.

La heurística propia obtuvo un buen equilibrio entre calidad de solución y tiempo de ejecución: alcanzó un valor de 19, superior al Greedy base, con un tiempo de ejecución cercano al de este.

Estos resultados corresponden únicamente a la instancia pequeña. No deben generalizarse a las instancias comuna y ciudad.

### 8.2. Instancia comuna

Resultados obtenidos en las ejecuciones reportadas:

| Algoritmo | Valor total | Costo total (millones) | Presupuesto restante |
|---|---:|---:|---:|
| Greedy base | 1.529 | 11.950 | 50 |
| Heurística propia | 1.492 | 11.600 | 400 |

El Greedy base obtiene 37 puntos más de valor que la heurística propia en esta instancia.

La heurística propia utiliza 350 millones menos de presupuesto, pero obtiene un valor total inferior.

El resultado del Greedy base coincide con la referencia oficial reportada para la instancia comuna.

**Pendiente:** ejecutar y medir el algoritmo exacto en comuna. No se ha validado todavía su resultado ni su tiempo de ejecución.

### 8.3. Instancia ciudad

La instancia ciudad contiene 80 lotes.

La búsqueda exhaustiva tiene un máximo teórico de:

4^80 combinaciones.

Por su crecimiento exponencial, la fuerza bruta no resulta práctica para esta instancia.

Se deben ejecutar y comparar las dos estrategias voraces en ciudad, y justificar la inviabilidad del algoritmo exacto mediante el análisis de complejidad y las mediciones disponibles.

**Pendiente:** consolidar los resultados de los tres algoritmos y las mediciones de tiempo de ciudad.

## 9. Complejidad y análisis

### Dijkstra

La implementación utiliza una cola de prioridad mediante `heapq`.

Su complejidad habitual con listas de adyacencia y cola de prioridad es:

O((V + E) log V)

donde:

- V es la cantidad de nodos.
- E es la cantidad de aristas.

### Greedy base

En cada iteración se revisan las alternativas de los lotes que todavía no han sido utilizados.

La cantidad de iteraciones está limitada por el número de lotes, porque se selecciona máximo una estación por lote.

### Heurística propia

Tiene una estructura de búsqueda voraz similar a la del Greedy base, pero cambia el criterio de selección: maximiza la relación entre valor adicional y costo.

### Algoritmo exacto

Con L lotes y tres tipos de estación, existen hasta:

4^L combinaciones.

La poda por presupuesto reduce la cantidad de ramas exploradas, pero no elimina el crecimiento exponencial.

Por esto, el algoritmo exacto es apropiado para instancias pequeñas y puede resultar inviable para instancias grandes.

## 10. Restricciones técnicas

La implementación utiliza Python y las herramientas permitidas para el proyecto.

Se utilizan:

- `csv` y `json` para lectura de datos.
- `pandas` para manipulación de datos cuando corresponde.
- `heapq` para la cola de prioridad de Dijkstra.
- `time` para medir tiempos de ejecución.

No se utilizan librerías externas para resolver rutas, distancias o combinaciones de optimización.

Se deben respetar las restricciones del enunciado respecto a librerías como `networkx`, `osmnx`, `scipy` e `itertools`.

## 11. Visualización

Está pendiente completar:

- Mapa de la instancia ciudad.
- Identificación de lotes utilizados y no utilizados.
- Ubicación de las estaciones seleccionadas por tipo.
- Visualización de incidentes cubiertos y no cubiertos.
- Tabla de estaciones con lote, tipo, costo y casos cubiertos.
- Resumen de presupuesto, valor y cobertura por tipo de incidente.
- Mapa y tabla de la mejor solución de la instancia comuna.

## 12. Pruebas pendientes

- [x] Construcción del grafo en pequeña y comuna.
- [x] Manejo de longitudes decimales en las aristas.
- [x] Pruebas de cobertura y costos en pequeña.
- [x] Verificación de resultados de cobertura con la referencia disponible.
- [x] Ejecución del Greedy base.
- [x] Ejecución de la heurística propia.
- [x] Comparación de Greedy base y heurística propia en pequeña y comuna.
- [x] Ejecución del algoritmo exacto en pequeña.
- [x] Validación del valor óptimo de 20 en pequeña.
- [ ] Medición y registro de tiempos de los tres algoritmos en las instancias.
- [ ] Evaluación del algoritmo exacto en comuna.
- [ ] Ejecución y comparación final en ciudad.
- [ ] Contraejemplo manual de máximo seis nodos para cada heurística.
- [ ] Mapas y tablas de resultados para ciudad y comuna.
- [ ] Pruebas de procesamiento de nuevos lotes e incidentes sin depender de IDs fijos.

## 13. Consideraciones para la sustentación

Durante la sustentación se debe explicar:

1. Cómo se representa la red vial mediante un grafo dirigido.
2. Cómo se calculan las distancias mínimas.
3. Cómo se determina la cobertura de una estación.
4. Cómo se calcula el valor adicional de una alternativa.
5. En qué se diferencia el Greedy base de la heurística propia.
6. Cómo funciona la búsqueda exacta y la poda por presupuesto.
7. Por qué el algoritmo exacto no es práctico para la instancia ciudad.
8. Qué ventajas y limitaciones tiene cada estrategia.
9. Cómo se procesan nuevos datos sin depender de identificadores o valores fijos.

## 14. Estado general del proyecto

El proyecto ya cuenta con la construcción del grafo, el cálculo de distancias, la evaluación de costos y cobertura, dos algoritmos voraces y un algoritmo exacto mediante fuerza bruta con poda.

El algoritmo exacto fue validado en la instancia pequeña y encontró el valor óptimo esperado de 20, con un costo de 5.400 millones.

Los resultados de Greedy base y de la heurística propia ya fueron obtenidos para pequeña y comuna.

Todavía falta completar las mediciones de tiempo, evaluar la viabilidad del exacto en comuna, consolidar los resultados de ciudad y terminar las visualizaciones requeridas.