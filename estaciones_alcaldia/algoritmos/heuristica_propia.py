
from typing import Any

from algoritmos.cobertura import (evaluar_lote,calcular_valor_adicional)


def greedy_eficiencia(grafo: dict[int, list[tuple[int, int]]],lotes: list[dict[str, str]],incidentes: list[dict[str, str]],parametros: dict[str, Any]) -> dict[str, Any]:
    """
    Selecciona estaciones usando el criterio de eficiencia:

        valor adicional / costo

    Respeta el presupuesto y permite máximo una estación por lote.
    """

    # Obtenemos el presupuesto total disponible.
    presupuesto: int = int(parametros["presupuesto_millones"])

    # Guardaremos las estaciones que finalmente seleccionemos.
    estaciones_seleccionadas: list[dict[str, Any]] = []

    # Guardamos los identificadores de incidentes ya cubiertos.
    incidentes_ya_cubiertos: set[int] = set()

    # Registramos los lotes que ya tienen una estación.
    lotes_utilizados: set[str] = set()

    # Calculamos las alternativas disponibles en cada lote.
    alternativas_por_lote: dict[str, dict[str, dict[str, Any]]] = {}

    for lote in lotes:
        id_lote: str = lote["lote"]

        alternativas_por_lote[id_lote] = evaluar_lote(grafo,lote,parametros,incidentes)

    # Repetimos mientras podamos encontrar una estación conveniente.
    while True:

        mejor_alternativa: dict[str, Any] | None = None
        mejor_eficiencia: float = -1.0

        # Revisamos todos los lotes disponibles.
        for lote in lotes:

            id_lote: str = lote["lote"]

            # Un lote no puede tener más de una estación.
            if id_lote in lotes_utilizados:
                continue

            alternativas: dict[str, dict[str, Any]] = (alternativas_por_lote[id_lote])

            # Revisamos cada tipo de estación posible.
            for tipo, alternativa in alternativas.items():

                costo: int = alternativa["costo"]

                # Descartamos estaciones que superan el presupuesto restante.
                if costo > presupuesto:
                    continue

                # Convertimos la cobertura en un conjunto.
                incidentes_cubiertos: set[int] = set(alternativa["incidentes_cubiertos"])

                # Calculamos el valor que aporta esta estación.
                valor_adicional: int = calcular_valor_adicional(incidentes_cubiertos,incidentes_ya_cubiertos,incidentes,parametros)

                # No elegimos estaciones que no aportan valor nuevo.
                if valor_adicional == 0:
                    continue

                # Calculamos la eficiencia de la alternativa.
                eficiencia: float = valor_adicional / costo

                # Conservamos la alternativa con mayor eficiencia.
                if eficiencia > mejor_eficiencia:
                    mejor_eficiencia = eficiencia

                    mejor_alternativa = {
                        "lote": id_lote,
                        "tipo": tipo,
                        "estacion": alternativa["estacion"],
                        "costo": costo,
                        "valor_adicional": valor_adicional,
                        "eficiencia": eficiencia,
                        "incidentes_cubiertos": incidentes_cubiertos
                    }

        # Si no encontramos ninguna alternativa, terminamos.
        if mejor_alternativa is None:
            break

        # Seleccionamos la mejor alternativa encontrada.
        estaciones_seleccionadas.append(mejor_alternativa)

        # Descontamos su costo del presupuesto disponible.
        presupuesto -= mejor_alternativa["costo"]

        # Registramos el lote para no volver a utilizarlo.
        lotes_utilizados.add(mejor_alternativa["lote"])

        # Actualizamos los incidentes cubiertos.
        incidentes_ya_cubiertos.update(mejor_alternativa["incidentes_cubiertos"]) #Añade una lista a lo q ya tenemos, no reemplaza a los que ya existen

    # Calculamos el valor total de todos los incidentes cubiertos.
    valor_total: int = calcular_valor_adicional(incidentes_ya_cubiertos,set(),incidentes,parametros)

    # Devolvemos los resultados de la solución.
    return {
        "estaciones_seleccionadas": estaciones_seleccionadas,
        "incidentes_cubiertos": incidentes_ya_cubiertos,
        "costo_total": sum(
            estacion["costo"]
            for estacion in estaciones_seleccionadas),
        "presupuesto_restante": presupuesto,
        "valor_total": valor_total
    }

# ============================================================
# COMPLEJIDAD TEMPORAL DE greedy_eficiencia
# ============================================================

# Definiciones:
# L = número de lotes
# E = número de aristas del grafo
# I = número de incidentes
# A = número de tipos de estación (A = 3)


# 1. PRECALCULAR ALTERNATIVAS:

# T1: evaluar_lote para cada lote:
# O(E log E + I)

# Se ejecuta una vez por cada uno de los L lotes:
# O(L * (E log E + I))


# 2. ORDENAR LOS LOTES:

# T2: ordenar los lotes por código:
# O(L log L)


# 3. CICLO VORAZ (WHILE):

# El while puede ejecutarse como máximo L veces,
# porque cada iteración selecciona un lote diferente.

# En cada iteración:
# T3: recorrer los L lotes y sus A alternativas:
# O(L * A)

# T4: calcular el valor adicional de cada alternativa:
# O(I)

# Por tanto, en cada iteración:
# O(L * A * I)

# Como el while puede ejecutarse como máximo L veces:
# O(L * L * A * I)

# Como A = 3 es constante:
# O(L² * I)

# T5: actualizar el conjunto de incidentes cubiertos:
# O(I) por iteración, como máximo L iteraciones.
# O(L * I)

# Este costo ya queda incluido en O(L² * I).


# 4. CÁLCULOS FINALES:

# T6: calcular el valor total revisando los incidentes:
# O(I)

# T7: sumar los costos de las estaciones seleccionadas:
# O(L)


# 5. COMPLEJIDAD TEMPORAL TOTAL:

# Sumamos todas las partes:

# O(L * (E log E + I))
# + O(L log L)
# + O(L² * I)
# + O(L * I)
# + O(I)
# + O(L)

# Desarrollando:

# TEMPORAL = O(LE log E + LI + L log L + L²I + LI + I + L)

# Simplificando:

# TEMPORAL = O(LE log E + L²I)


# ============================================================
# COMPLEJIDAD ESPACIAL DE greedy_eficiencia
# ============================================================

# 1. ALMACENAMIENTO DEL GRAFO:

# El grafo almacena V nodos y E aristas:
# O(V + E)


# 2. ALTERNATIVAS PRECALCULADAS:

# Se almacenan las alternativas de cada lote.
# Cada lote tiene A alternativas y cada alternativa
# puede almacenar hasta I incidentes cubiertos.

# O(L * A * I)

# Como A = 3 es constante:
# O(L * I)


# 3. CONJUNTOS Y LISTAS AUXILIARES:

# incidentes_ya_cubiertos:
# O(I)

# lotes_utilizados:
# O(L)

# estaciones_seleccionadas:
# O(L)


# 4. COMPLEJIDAD ESPACIAL TOTAL:

# Sumamos todas las estructuras:

# O(V + E + LI + I + L)

# Simplificando:

# ESPACIAL = O(V + E + LI)