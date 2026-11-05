# Dónde construir: estaciones para una alcaldía nueva

## 1. Descripción del proyecto

Este proyecto busca determinar en qué lotes conviene construir estaciones de atención de incidentes para una alcaldía nueva, considerando un presupuesto limitado.

El objetivo es seleccionar estaciones que maximicen el valor de los incidentes cubiertos, respetando las restricciones de ubicación, tipo de estación y presupuesto.

La red vial se representa mediante un grafo dirigido. Se comparan tres estrategias:

1. Greedy base del profesor.
2. Heurística propia basada en eficiencia.
3. Algoritmo exacto mediante fuerza bruta con Backtracking y podas.

## 2. Objetivo

Desarrollar y comparar los tres algoritmos anteriores en las instancias Pequeña, Comuna y Ciudad. La comparación considera el valor total de los incidentes cubiertos, el costo, el presupuesto restante, el tiempo de ejecución y las limitaciones de cada estrategia.

Además, se construyen contraejemplos manuales de máximo seis nodos para mostrar que las dos heurísticas voraces no garantizan encontrar la solución óptima.

## 3. Datos de entrada

Cada instancia contiene los siguientes archivos:

| Archivo | Contenido |
|---|---|
| `nodos.csv` | Identificadores y coordenadas de los nodos. |
| `aristas.csv` | Conexiones dirigidas entre nodos y longitud de cada tramo. |
| `lotes.csv` | Lotes disponibles, nodo asociado y factor de zona. |
| `incidentes.csv` | Incidentes registrados, nodo, tipo y fecha. |
| `parametros.json` | Presupuesto y parámetros de cada tipo de estación. |

### Tipos de incidentes y parámetros base

| Tipo | Estación | Costo base (millones) | Radio de cobertura | Peso |
|---|---|---:|---:|---:|
| Hurto | CAI | 1.000 | 1.000 m | 1 |
| Accidente | Tránsito / grúas | 2.000 | 2.000 m | 3 |
| Incendio | Bomberos | 5.000 | 3.000 m | 5 |

El costo de una estación se calcula multiplicando el costo base por el factor de zona del lote y aplicando el redondeo implementado en `calcular_costo()`.

## 4. Reglas del problema

- Se puede construir como máximo una estación por lote.
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

```text
Proyecto_ADA - copia/
├── estaciones_alcaldia/
│   ├── main.py
│   ├── requirements.txt
│   ├── resultados_ciudad.json
│   ├── resultados_comuna.json
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
│   │   ├── contraejemplos.py
│   │   └── instancias/
│   │       ├── contraejemplo_greedy/
│   │       └── contraejemplo_propia/
│   ├── visualizaciones/
│   │   ├── mapas.py
│   │   └── resultados_visualizacion/
│   └── README.md
└── instancias/
    ├── pequena/
    ├── comuna/
    └── ciudad/
```

Las instancias se encuentran fuera de la carpeta `estaciones_alcaldia`, dentro de la carpeta `instancias`.

Los archivos JSON de resultados se guardan dentro de `estaciones_alcaldia`.

## 7. Instalación y ejecución

### Requisitos

- Python 3.
- Conexión a Internet durante la primera instalación de dependencias.
- Las carpetas de instancias con sus archivos CSV y JSON.

### Dependencias externas

El archivo `requirements.txt`, ubicado al mismo nivel que `main.py`, contiene:

```text
folium>=0.20.0,<1.0.0
```

Las demás herramientas utilizadas para leer archivos, medir tiempos y ejecutar los algoritmos pertenecen a la biblioteca estándar de Python.

### Instalación automática

La versión integrada de `main.py` comprueba si Folium está instalado. Si no lo encuentra, utiliza el intérprete de Python que está ejecutando el programa para instalar las dependencias declaradas en `requirements.txt`.

Por tanto, no se debe escribir una ruta fija a Spyder ni a otra instalación de Python. `sys.executable` permite utilizar el intérprete activo, ya sea desde Spyder, VS Code, PyCharm o una terminal.

La primera ejecución necesita conexión a Internet si faltan dependencias. Si Folium ya está instalado, el programa continúa sin reinstalarlo.

### Ejecución

Desde el entorno de Python elegido, ejecutar:

```bash
python main.py
```

El programa presenta el menú de selección de instancia:

- Ciudad.
- Comuna.
- Pequeña.
- Todas.

La opción Todas procesa las instancias secuencialmente. Las visualizaciones se generan para Ciudad y Comuna; Pequeña presenta sus resultados en la terminal.

> Nota de implementación: para que la instalación automática funcione, el bloque de comprobación e instalación de dependencias debe estar incorporado al inicio de `main()`. El archivo `requirements.txt` por sí solo no instala paquetes.

## 8. Implementación

### 8.1. Construcción del grafo

**Archivo:** `algoritmos/grafo.py`

Se construye un grafo dirigido a partir de las conexiones de la red vial. Cada arista contiene el nodo de origen, el nodo de destino y la longitud del tramo. Las longitudes se manejan como valores numéricos.

### 8.2. Cálculo de distancias

**Archivo:** `algoritmos/distancias.py`

Se utiliza Dijkstra implementado con `heapq` para calcular las distancias mínimas desde un nodo de origen. El grafo es dirigido, por lo que las distancias respetan el sentido de las conexiones. La implementación requiere longitudes de arista no negativas. Los nodos inalcanzables no aparecen en el diccionario de distancias.

### 8.3. Cálculo de costos y cobertura

**Archivo:** `algoritmos/cobertura.py`

Este módulo contiene las operaciones para:

- Calcular el costo de una estación según el factor de zona.
- Identificar los incidentes cubiertos por una estación.
- Evaluar las alternativas de estación para cada lote.
- Calcular el valor total de los incidentes cubiertos.
- Calcular el valor adicional aportado por una nueva estación.
- Construir un diccionario que asocia cada ID de incidente con su peso.

La evaluación de un lote calcula las distancias una sola vez y reutiliza ese resultado para evaluar los distintos tipos de estación. Los incidentes se identifican mediante conjuntos para evitar contar dos veces un mismo ID.

### 8.4. Greedy base del profesor

**Archivo:** `algoritmos/greedy_base.py`

Este algoritmo selecciona en cada iteración la estación que aporta el mayor valor adicional absoluto. No divide el valor adicional por el costo.

Criterios de desempate:

1. Menor código de lote.
2. Orden de tipo: hurto, accidente e incendio.

El algoritmo respeta el presupuesto y evita seleccionar más de una estación en el mismo lote.

### 8.5. Heurística propia: eficiencia

**Archivo:** `algoritmos/heuristica_propia.py`

La heurística propia utiliza la relación:

**Eficiencia = valor adicional / costo**

En cada iteración se selecciona la alternativa factible con mayor eficiencia. Después de seleccionar una estación, se descuenta su costo del presupuesto, se marca su lote como utilizado y se actualiza el conjunto de incidentes cubiertos.

Esta estrategia busca obtener un mayor aprovechamiento del presupuesto, pero no garantiza encontrar la solución óptima.

### 8.6. Algoritmo exacto: fuerza bruta con Backtracking y podas

**Archivo:** `algoritmos/exacto.py`

La función `fuerza_bruta()` resuelve el problema mediante búsqueda exhaustiva con Backtracking. No utiliza Greedy ni construye una solución inicial heurística.

Para cada lote considera cuatro posibilidades:

1. No construir una estación.
2. Construir una estación de hurto.
3. Construir una estación de accidentes.
4. Construir una estación de incendios.

El algoritmo explora las combinaciones de alternativas y mantiene el conjunto de incidentes cubiertos para contar cada incidente una sola vez.

Para reducir el espacio de búsqueda utiliza:

- **Ordenamiento de lotes y alternativas:** modifica el orden de exploración, pero no elimina opciones ni determina por sí solo la solución.
- **Poda por presupuesto:** descarta una rama cuando el costo acumulado supera el presupuesto.
- **Poda por valor máximo restante:** calcula una cota superior optimista del valor que todavía podría alcanzarse. Si esa cota no puede mejorar la mejor solución conocida —considerando también el desempate por costo—, descarta la rama.
- **Estado reversible:** agrega temporalmente los incidentes y las estaciones de una decisión y restaura el estado al retroceder, evitando copias innecesarias.

El criterio de optimización es:

1. Maximizar el valor total de los incidentes cubiertos.
2. En caso de empate en valor, minimizar el costo total.

Bajo las condiciones del modelo —alternativas completas por lote, costos y pesos no negativos e identificadores únicos de incidentes—, las podas conservan la optimalidad.

## 9. Resultados experimentales

Los siguientes resultados corresponden a las ejecuciones reportadas. Los tiempos pueden variar según el equipo y el entorno de ejecución.

### 9.1. Instancia Pequeña

| Métrica | Greedy base | Heurística propia | Exacto |
|---|---:|---:|---:|
| Valor total | 15 | 19 | **20** |
| Costo total (millones) | 5.500 | 5.100 | 5.400 |
| Presupuesto restante (millones) | 500 | 900 | 600 |
| Tiempo (segundos) | 0,000426 | 0,000729 | 0,002632 |

El algoritmo exacto obtuvo el mayor valor de cobertura: 20 puntos, con un costo de 5.400 millones y 600 millones de presupuesto restante.

La solución exacta reportada selecciona:

| Lote | Tipo de estación | Costo (millones) |
|---|---|---:|
| L1 | Hurto | 1.100 |
| L3 | Accidente | 2.800 |
| L4 | Hurto | 1.500 |
| **Total** | | **5.400** |

La ejecución reportó 12 incidentes cubiertos. El resultado exacto supera en 5 puntos al Greedy base y en 1 punto a la heurística propia.

### 9.2. Instancia Comuna

| Métrica | Greedy base | Heurística propia | Exacto |
|---|---:|---:|---:|
| Valor total | 1.529 | 1.492 | **1.574** |
| Costo total (millones) | 11.950 | 11.600 | 11.700 |
| Presupuesto restante (millones) | 50 | 400 | 300 |
| Tiempo (segundos) | 0,100222 | 0,102936 | 19,454549 |

El algoritmo exacto obtuvo el mayor valor de cobertura: 1.574 puntos, con un costo de 11.700 millones y 300 millones de presupuesto restante.

En comparación con las otras estrategias:

- Supera al Greedy base en 45 puntos.
- Supera a la heurística propia en 82 puntos.
- Su tiempo de ejecución fue de aproximadamente 19,45 segundos, por debajo del objetivo de un minuto establecido para Comuna.

El resultado exacto reportó 850 incidentes cubiertos: 519 hurtos, 300 accidentes y 31 incendios.

### 9.3. Instancia Ciudad

La instancia Ciudad contiene 80 lotes. Si cada lote tiene tres tipos de estación posibles y la opción de no construir, el espacio teórico de decisiones es:

\[
4^{80} \approx 1,46 \times 10^{48}
\]

combinaciones.

Este número representa el espacio máximo teórico antes de aplicar las podas. Las podas pueden reducir la búsqueda efectiva, pero no eliminan el crecimiento exponencial del peor caso. En las pruebas realizadas, la ejecución del algoritmo exacto no terminó en un tiempo práctico, por lo que se interrumpió y no se reporta una solución óptima para Ciudad. Esto es coherente con el alcance del enunciado, que no exige obtener el óptimo exacto de esta instancia.

Los resultados de las dos heurísticas voraces son:

| Métrica | Greedy base | Heurística propia |
|---|---:|---:|
| Valor total | 7.591 | **7.706** |
| Costo total (millones) | 39.850 | 39.950 |
| Presupuesto restante (millones) | 150 | 50 |
| Incidentes cubiertos | 3.301 | **3.738** |
| Tiempo (segundos) | 6,801294 | 7,422654 |

La heurística propia obtuvo 115 puntos más de valor que Greedy base (aproximadamente 1,51 % de mejora) y cubrió 437 incidentes adicionales (aproximadamente 13,24 % más). Para conseguirlo utilizó 100 millones adicionales y tardó aproximadamente 0,62 segundos más. Ambas propuestas respetaron el presupuesto de 40.000 millones.

Por valor y cantidad de incidentes cubiertos, la heurística propia es la propuesta voraz recomendada para Ciudad. Su costo fue de 39.950 millones, por lo que dejó 50 millones de presupuesto disponible.

### 9.4. Evaluación de alternativas de la Parte 1

Para Ciudad se evaluaron los 80 lotes y sus tres tipos de estación, es decir, 240 alternativas.

| Operación | Tiempo medido |
|---|---:|
| Construcción del grafo | 0,069222 s |
| Evaluación de los lotes y tipos | 3,561515 s |

La evaluación de alternativas quedó por debajo del límite de un minuto establecido para la Parte 1.

## 10. Contraejemplos de las heurísticas

Se construyeron dos instancias manuales, ambas con máximo seis nodos. Los datos se guardan en archivos CSV y JSON y se ejecutan mediante `pruebas/contraejemplos.py`.

### 10.1. Contraejemplo para Greedy base

- 6 nodos.
- 3 lotes.
- 12 incidentes de hurto.
- Presupuesto: 2.000 millones.

Resultados:

| Algoritmo | Valor | Costo | Decisión |
|---|---:|---:|---|
| Greedy base | 10 | 2.000 | L1: hurto; cubre 10 incidentes |
| Heurística propia | 12 | 2.000 | L2 y L3: hurto; cubren 12 incidentes |
| Exacto | **12** | 2.000 | L2 y L3: hurto; cubren 12 incidentes |

El Greedy base selecciona primero L1 porque aporta 10 puntos inmediatos. Esa decisión consume todo el presupuesto e impide construir estaciones en L2 y L3, que juntas cubren 12 incidentes. Por tanto, la elección de mayor valor adicional inmediato no necesariamente conduce a la mejor combinación global.

### 10.2. Contraejemplo para la heurística propia

- 5 nodos.
- 2 lotes.
- 3 incidentes de accidentes y 10 de hurto.
- Presupuesto: 3.000 millones.

Resultados:

| Algoritmo | Valor | Costo | Decisión |
|---|---:|---:|---|
| Greedy base | 9 | 2.000 | L1: accidente |
| Heurística propia | 9 | 2.000 | L1: accidente |
| Exacto | **10** | 3.000 | L1 y L2: hurto |

La heurística propia prioriza la eficiencia de la estación de accidentes en L1 (9/2.000 = 0,0045). Sin embargo, esa decisión bloquea la posibilidad de instalar estaciones de hurto en ambos lotes. La solución exacta instala dos estaciones de hurto y obtiene 10 puntos.

Estos ejemplos muestran que ni maximizar el valor adicional absoluto ni maximizar la relación valor/costo garantiza encontrar el óptimo global.

### 10.3. Ejecución de las pruebas

Desde la carpeta `estaciones_alcaldia`, ejecutar:

```bash
python pruebas/contraejemplos.py
```

El script lee las instancias de prueba, ejecuta Greedy base, heurística propia y algoritmo exacto, y verifica los valores esperados mediante aserciones. La ejecución confirmada finaliza con el mensaje:

```text
TODAS LAS COMPROBACIONES FUERON EXITOSAS
```

## 11. Complejidad y análisis

### Dijkstra

Con listas de adyacencia y cola de prioridad, la complejidad habitual es:

\[
O((V+E)\log V)
\]

donde \(V\) es la cantidad de nodos y \(E\) la cantidad de aristas.

### Greedy base

En cada iteración se revisan las alternativas de los lotes que todavía no han sido utilizados. La cantidad de iteraciones está limitada por el número de lotes, porque se selecciona como máximo una estación por lote.

### Heurística propia

Tiene una estructura de búsqueda voraz similar a la del Greedy base, pero cambia el criterio de selección: maximiza la relación entre valor adicional y costo.

### Algoritmo exacto

Con \(L\) lotes y tres tipos de estación, existen hasta:

\[
4^L
\]

combinaciones teóricas, contando la opción de no construir.

El Backtracking explora este espacio y utiliza podas por presupuesto y por valor máximo restante para reducir las ramas examinadas. Estas podas preservan la optimalidad bajo los supuestos del modelo, pero no eliminan el crecimiento exponencial del peor caso.

Los resultados experimentales muestran que el método es viable para Pequeña y Comuna en los tiempos medidos. Para Ciudad, cuyo espacio teórico alcanza \(4^{80}\), no se reporta una solución exacta.

## 12. Visualización

El módulo `visualizaciones/mapas.py` genera una página HTML para cada instancia visualizada. Cada página contiene dos pestañas:

1. **Mapa interactivo:** muestra lotes no utilizados, estaciones construidas e incidentes cubiertos y no cubiertos. Las capas se pueden activar o desactivar.
2. **Tabla de estaciones:** presenta lote, tipo de estación, costo, cantidad de incidentes cubiertos e IDs de los incidentes. También muestra el costo total, presupuesto, presupuesto restante, valor y cobertura por tipo.

Las visualizaciones se generan para Ciudad y Comuna. Se guardan en:

```text
estaciones_alcaldia/
└── visualizaciones/
    └── resultados_visualizacion/
        ├── ciudad.html
        ├── mapa_ciudad.html
        ├── comuna.html
        └── mapa_comuna.html
```

Los archivos `ciudad.html` y `comuna.html` son las páginas principales. Cada una carga su correspondiente archivo `mapa_*.html`, por lo que ambos deben permanecer en la misma carpeta.

El mapa utiliza un proveedor externo de mosaicos cartográficos. Por esta razón, la visualización del mapa base requiere conexión a Internet y puede depender de la disponibilidad y condiciones de uso del proveedor. Los marcadores, capas y tablas se generan localmente a partir de los datos de la instancia y del JSON de resultados.

**Estado de validación:** la generación de las tablas HTML está funcionando. Se está verificando la carga del mapa base en los navegadores y redes utilizados; no se debe considerar cerrada esta validación hasta comprobar que los mapas de Ciudad y Comuna se visualizan correctamente.

## 13. Restricciones técnicas

La implementación utiliza Python y las herramientas permitidas para el proyecto.

Se utilizan:

- `csv` y `json` para lectura de datos.
- `heapq` para la cola de prioridad de Dijkstra.
- `time` para medir tiempos de ejecución.
- `folium` para la visualización de mapas interactivos.

No se utilizan librerías externas para resolver rutas, distancias o combinaciones de optimización. Se respetan las restricciones del enunciado respecto a librerías como `networkx`, `osmnx`, `scipy` e `itertools`.

Los archivos CSV y JSON se utilizan como fuentes de lectura de datos.

## 14. Pruebas y estado de avance

- [x] Construcción del grafo en las instancias.
- [x] Manejo de longitudes decimales en las aristas.
- [x] Pruebas de cobertura y costos en Pequeña.
- [x] Verificación de resultados de cobertura con la referencia disponible.
- [x] Ejecución del Greedy base.
- [x] Ejecución de la heurística propia.
- [x] Comparación de Greedy base y heurística propia en las tres instancias.
- [x] Ejecución del algoritmo exacto en Pequeña.
- [x] Obtención del valor 20 para el algoritmo exacto en Pequeña.
- [x] Ejecución del algoritmo exacto en Comuna.
- [x] Obtención del valor 1.574 para el algoritmo exacto en Comuna.
- [x] Medición de tiempos de los tres algoritmos en Pequeña y Comuna.
- [x] Ejecución y comparación de Greedy base y heurística propia en Ciudad.
- [x] Evaluación de las 240 alternativas de Ciudad en 3,561515 segundos.
- [x] Contraejemplo manual de máximo seis nodos para Greedy base.
- [x] Contraejemplo manual de máximo seis nodos para la heurística propia.
- [x] Ejecución de las pruebas de contraejemplos con comprobaciones exitosas.
- [x] Generación de las páginas HTML y tablas para Ciudad y Comuna.
- [ ] Verificar que los mapas base de Ciudad y Comuna carguen correctamente en el entorno de ejecución.
- [ ] Ejecutar pruebas de procesamiento con una nueva distribución de lotes e histórico de incidentes, sin depender de IDs fijos.
- [ ] Confirmar la instalación automática de dependencias desde `main.py` en un entorno limpio.

## 15. Consideraciones para la sustentación

Durante la sustentación se debe explicar:

1. Cómo se representa la red vial mediante un grafo dirigido.
2. Cómo se calculan las distancias mínimas.
3. Cómo se determina la cobertura de una estación.
4. Cómo se calcula el valor adicional de una alternativa.
5. En qué se diferencia el Greedy base de la heurística propia.
6. Cómo funciona la búsqueda exacta con Backtracking y sus podas.
7. Por qué el algoritmo exacto no es práctico para la instancia Ciudad.
8. Qué ventajas y limitaciones tiene cada estrategia.
9. Cómo se procesan nuevos datos sin depender de identificadores o valores fijos.
10. Cómo se interpretan los mapas, las capas y las tablas de las propuestas para Ciudad y Comuna.

## 16. Estado general del proyecto

El proyecto cuenta con la construcción del grafo dirigido, el cálculo de distancias mediante Dijkstra, la evaluación de costos y cobertura, dos algoritmos voraces y un algoritmo exacto mediante fuerza bruta con Backtracking y podas.

Los tres algoritmos se ejecutaron en Pequeña y Comuna. En Pequeña, el algoritmo exacto obtuvo un valor de 20 y un costo de 5.400 millones, con un tiempo medido de 0,002632 segundos. En Comuna, obtuvo un valor de 1.574 y un costo de 11.700 millones, con un tiempo medido de 19,454549 segundos.

En Ciudad, Greedy base obtuvo un valor de 7.591 y la heurística propia un valor de 7.706. Esta última cubrió 3.738 incidentes, frente a 3.301 de Greedy base, con un costo de 39.950 millones dentro del presupuesto de 40.000 millones. La evaluación de las alternativas de Ciudad tomó 3,561515 segundos. No se reporta una solución exacta para Ciudad porque la ejecución no terminó en un tiempo práctico y el enunciado no exige obtener el óptimo exacto para esta instancia.

También se completaron los dos contraejemplos manuales de máximo seis nodos y sus pruebas automatizadas. Las páginas HTML con tablas para Ciudad y Comuna se generan; la carga de los mapas base todavía debe verificarse en el entorno de ejecución. La instalación automática de dependencias debe quedar habilitada en `main.py` mediante la lectura de `requirements.txt`.