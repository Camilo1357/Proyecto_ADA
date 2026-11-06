
from typing import Any

from algoritmos.cobertura import (evaluar_lote,calcular_valor_adicional)

#Seleccionar la estación que aporte el mayor valor adicional absoluto.
def greedy_base(grafo: dict[int, list[tuple[int, int]]],lotes: list[dict[str, str]],incidentes: list[dict[str, str]],parametros: dict[str, Any]) -> dict[str, Any]:
    """
    Selecciona estaciones usando la heurística base del profesor.

    Criterio:
        Elegir la estación que agregue el mayor valor adicional
        absoluto, sin dividirlo por el costo.

    Desempates:
        1. Menor código de lote.
        2. Orden de tipo: hurto, accidente, incendio.

    Respeta el presupuesto y permite máximo una estación por lote.
    """


    # V = cantidad de nodos del grafo.
    # E = cantidad de aristas del grafo.
    # L = cantidad de lotes.
    # I = cantidad de incidentes.
    # K = cantidad de tipos de estación 

    # Presupuesto total disponible.
    presupuesto: int = int(parametros["presupuesto_millones"])

    # Resultados de la propuesta.
    estaciones_seleccionadas: list[dict[str, Any]] = []

    # Incidentes que ya están cubiertos por alguna estación elegida.
    incidentes_ya_cubiertos: set[int] = set()

    # Lotes que ya tienen una estación.
    lotes_utilizados: set[str] = set()

    # Orden de tipos establecido por el profesor para desempatar.
    orden_tipos: list[str] = ["hurto","accidente","incendio"] # O(1)

    # Calculamos las alternativas de cada lote una sola vez.
    alternativas_por_lote: dict[str, dict[str, dict[str, Any]]] = {}

    for lote in lotes: #O(L) T1
        id_lote: str = lote["lote"]

        alternativas_por_lote[id_lote] = evaluar_lote(grafo,lote,parametros,incidentes) # O(E logE + I) T2

    # Ordenamos los lotes para resolver correctamente los empates.
    lotes_ordenados: list[dict[str, str]] = sorted(lotes,key=lambda lote: lote["lote"]) # O(L LogL) T3

    # Repetimos mientras exista una estación que aporte valor.
    while True: # O(L) T4

        mejor_alternativa: dict[str, Any] | None = None
        mayor_valor_adicional: int = 0

        # Recorremos los lotes en orden de código.
        for lote in lotes_ordenados: # O(L) T5

            id_lote: str = lote["lote"]

            # No podemos construir más de una estación en el mismo lote.
            if id_lote in lotes_utilizados:
                continue

            alternativas: dict[str, dict[str, Any]] = (alternativas_por_lote[id_lote])

            # Recorremos los tipos en el orden oficial de desempate.
            for tipo in orden_tipos: # O(1)

                # Si el tipo no está disponible en los parámetros, lo omitimos.
                if tipo not in alternativas:
                    continue

                alternativa: dict[str, Any] = alternativas[tipo]
                costo: int = alternativa["costo"]

                # La estación debe caber en el presupuesto restante.
                if costo > presupuesto:
                    continue

                # Convertimos los incidentes cubiertos a conjunto.
                incidentes_cubiertos: set[int] = set(alternativa["incidentes_cubiertos"]) # O(I) T6

                # Calculamos el valor que todavía no está cubierto.
                valor_adicional: int = calcular_valor_adicional(incidentes_cubiertos,incidentes_ya_cubiertos,incidentes,parametros) # O(I) T7

                # No seleccionamos estaciones que no agreguen valor.
                if valor_adicional == 0:
                    continue

                # Solo reemplazamos si encontramos un valor estrictamente mayor.
                # Así conservamos el primer candidato en caso de empate:
                # primero el menor lote y luego el orden de tipos.
                if valor_adicional > mayor_valor_adicional:

                    mayor_valor_adicional = valor_adicional

                    mejor_alternativa = {
                        "lote": id_lote,
                        "tipo": tipo,
                        "estacion": alternativa["estacion"],
                        "costo": costo,
                        "valor_adicional": valor_adicional,
                        "incidentes_cubiertos": incidentes_cubiertos
                    }

        # Si no encontramos una estación que agregue valor, terminamos.
        if mejor_alternativa is None:
            break

        # Agregamos la estación a la propuesta.
        estaciones_seleccionadas.append(mejor_alternativa)

        # Descontamos su costo del presupuesto.
        presupuesto -= mejor_alternativa["costo"]

        # Marcamos el lote como utilizado.
        lotes_utilizados.add(mejor_alternativa["lote"])
        #agrega un valor

        # Unimos los nuevos incidentes con los que ya estaban cubiertos.
        incidentes_ya_cubiertos.update(mejor_alternativa["incidentes_cubiertos"]) # O(I) T8
        #agrega un conjunto

    # Calculamos el valor total de la propuesta.
    valor_total: int = calcular_valor_adicional(incidentes_ya_cubiertos,set(),incidentes,parametros) # O(I) T9

    # Devolvemos el mismo formato general de resultados de la heurística propia.
    return {
        "estaciones_seleccionadas": estaciones_seleccionadas,
        "incidentes_cubiertos": incidentes_ya_cubiertos,
        "costo_total": sum(estacion["costo"]for estacion in estaciones_seleccionadas),
        "presupuesto_restante": presupuesto,
        "valor_total": valor_total
    }


# T1: recorrer los L lotes:
# O(L)
#
# T2: ejecutar evaluar_lote() para cada lote:
# O(E log E + I)
#
# 
# T1 * T2 = O(L * (E log E + I))
#
# T3: ordenar los L lotes:
# O(L log L)
#
#
# 3. CICLO WHILE:
#
# T4: el while realiza como máximo L selecciones exitosas,
# porque no se puede utilizar un lote más de una vez.
# Su complejidad es O(L).
#
# T5: recorrer los L lotes:
# O(L)
#
# Recorrer los K tipos de estación:
# O(K) = O(1)
#
# T6: convertir los incidentes cubiertos en conjunto:
# O(I)
#
# T7: calcular el valor adicional:
# O(I)
#
# Por tanto, el recorrido de lotes y tipos en una iteración cuesta:
# 
# (T5 * K * (T6 + T7)) = O(L * K * (I + I))
#
# Como K = 3 = O(1):
#
# O(L * I)
#
# El while puede ejecutarse como máximo L veces:
#
# T4 * (T5 * K * (T6 + T7)) = O(L * L * I)
#
# Resultado:
# O(L² * I)
#
# T8: actualizar el conjunto de incidentes cubiertos:
# O(I) por iteración, como máximo L iteraciones.
#
# O(L * I)
#
# Este costo ya queda incluido en O(L² * I).
#
# T9: calcular el valor total revisando los incidentes:
# O(I)
#
# Sumar los costos de las estaciones seleccionadas:
# O(L)
#
#
# 5. COMPLEJIDAD TEMPORAL TOTAL:
#
# Sumamos todas las partes:
#
# O(L * (E log E + I))
# + O(L log L)
# + O(L² * I)
# + O(L * I)
# + O(I)
# + O(L)
#
# Desarrollando:
#
# TEMPORAL = O(LE log E + LI + L log L + L²I + LI + I + L)
#
# simplificado:
# # O(LE log E + L²I)


# ============================================================
# ANALISIS DE COMPLEJIDAD ESPACIAL
# ============================================================
#
#
#grafo
# En el grafo almacenamos V nodos y E aristas:
#
# O(V + E)
#
#
# estaciones_seleccionadas
# Se pueden seleccionar como máximo L estaciones.
# Cada estación almacena también un conjunto de incidentes
# cubiertos, que puede contener hasta I identificadores.
#
# O(L * I)
#
#
# incidentes_ya_cubiertos
# El conjunto almacena como máximo I identificadores:
#
# O(I)
#
#
# lotes_utilizados
#
# El conjunto almacena como máximo L identificadores:
#
# O(L)
#
#
# orden_tipos
#
# Se almacenan K = 3 tipos de estación:
#
# O(1)
#
#
# alternativas_por_lote
#
# Se almacenan las alternativas de los L lotes.
# Cada lote puede tener hasta I incidentes cubiertos.
#
# O(L * I)
#
#
# lotes_ordenados
#
# Se almacena una lista con los L lotes:
#
# O(L)
#
# 9. COMPLEJIDAD ESPACIAL TOTAL:
#
# O(V + E)
# + O(L * I)
# + O(I)
# + O(L)
# + O(1)
# + O(L * I)
# + O(L)
#
# O(V + E + 2LI + I + 2L)
#
# COMPLEJIDAD ESPACIAL FINAL:
#
# O(V + E + LI + L + I)
#
# simplificado: 
#
# O(V + E + LI)
# ============================================================




