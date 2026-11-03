
from typing import Any

from algoritmos.cobertura import (
    evaluar_lote,
    construir_valores_incidentes,
    calcular_valor_rapido
)


def fuerza_bruta(
    grafo: dict[int, list[tuple[int, int]]],
    lotes: list[dict[str, str]],
    incidentes: list[dict[str, str]],
    parametros: dict[str, Any]
) -> dict[str, Any]:
    """
    Busca la combinación óptima de estaciones mediante backtracking.

    Maximiza el valor de los incidentes cubiertos sin superar
    el presupuesto y respetando la restricción de una estación
    como máximo por lote.

    Incluye:
    - Poda por presupuesto.
    - Poda por valor máximo posible.
    - Cálculo rápido del valor de incidentes.
    """

    # ---------------------------------------------------------
    # 1. Preparar los datos
    # ---------------------------------------------------------

    # Construimos una sola vez el diccionario de valores.
    valores_incidentes: dict[int, int] = construir_valores_incidentes(
        incidentes,
        parametros
    )

    presupuesto: int = int(parametros["presupuesto_millones"])

    # ---------------------------------------------------------
    # 2. Construir las alternativas de cada lote
    # ---------------------------------------------------------

    alternativas_por_lote: list[list[dict[str, Any] | None]] = []

    for lote in lotes:

        resultados: dict[str, dict[str, Any]] = evaluar_lote(
            grafo,
            lote,
            parametros,
            incidentes
        )

        # None representa no construir una estación.
        alternativas: list[dict[str, Any] | None] = [None]

        for tipo, resultado in resultados.items():

            alternativas.append({
                "lote": lote["lote"],
                "tipo": tipo,
                "estacion": resultado["estacion"],
                "costo": resultado["costo"],
                "incidentes_cubiertos": set(
                    resultado["incidentes_cubiertos"]
                )
            })

        alternativas_por_lote.append(alternativas)

    # Usamos la cantidad real de listas de alternativas.
    cantidad_lotes: int = len(alternativas_por_lote)

    # ---------------------------------------------------------
    # 3. Preparar los límites superiores de valor
    # ---------------------------------------------------------

    # valor_maximo_restante[i] contiene todos los incidentes
    # que podrían cubrirse utilizando los lotes desde i en adelante.
    valor_maximo_restante: list[set[int]] = [
        set() for _ in range(cantidad_lotes + 1)
    ]

    for indice in range(cantidad_lotes - 1, -1, -1):

        incidentes_posibles: set[int] = (
            valor_maximo_restante[indice + 1].copy()
        )

        for alternativa in alternativas_por_lote[indice]:

            if alternativa is not None:
                incidentes_posibles.update(
                    alternativa["incidentes_cubiertos"]
                )

        valor_maximo_restante[indice] = incidentes_posibles

    # ---------------------------------------------------------
    # 4. Variables para guardar la mejor solución
    # ---------------------------------------------------------

    mejor_valor: int = -1
    mejor_costo: int = 0

    mejores_estaciones: list[dict[str, Any]] = []
    mejores_incidentes: set[int] = set()

    combinaciones_evaluadas: int = 0
    ramas_podadas: int = 0

    # ---------------------------------------------------------
    # 5. Backtracking con podas
    # ---------------------------------------------------------

    def explorar_combinaciones(indice_lote: int,costo_actual: int,incidentes_actuales: set[int],estaciones_actuales: list[dict[str, Any]]) -> None:

        nonlocal mejor_valor
        nonlocal mejor_costo
        nonlocal mejores_estaciones
        nonlocal mejores_incidentes
        nonlocal combinaciones_evaluadas
        nonlocal ramas_podadas

        # Poda 1: presupuesto.
        if costo_actual > presupuesto:
            ramas_podadas += 1
            return

        # Poda 2: valor máximo que todavía podría alcanzarse.
        # La unión incluye los incidentes actuales y todos los
        # que podrían cubrirse con los lotes pendientes.
        incidentes_posibles: set[int] = (incidentes_actuales |valor_maximo_restante[indice_lote])

        valor_posible: int = calcular_valor_rapido(incidentes_posibles,valores_incidentes)

        # Si no puede superar la mejor solución, descartamos.
        # Usamos < y no <= para permitir desempatar por menor costo.
        if valor_posible < mejor_valor:
            ramas_podadas += 1
            return

        # Si ya procesamos todos los lotes, evaluamos la solución.
        if indice_lote == cantidad_lotes:

            combinaciones_evaluadas += 1

            valor_actual: int = calcular_valor_rapido(incidentes_actuales,valores_incidentes)

            # Maximizamos el valor.
            # En empate, preferimos menor costo.
            if (valor_actual > mejor_valor or (valor_actual == mejor_valor and costo_actual < mejor_costo)):

                mejor_valor = valor_actual
                mejor_costo = costo_actual

                mejores_estaciones = estaciones_actuales.copy()
                mejores_incidentes = incidentes_actuales.copy()
            return

        # -----------------------------------------------------
        # 6. Explorar las alternativas del lote actual
        # -----------------------------------------------------

        alternativas: list[dict[str, Any] | None] = (alternativas_por_lote[indice_lote])

        for alternativa in alternativas:

            # Opción 1: no instalar estación.
            if alternativa is None:
                explorar_combinaciones(indice_lote + 1,costo_actual,incidentes_actuales,estaciones_actuales)
                continue

            # Obtenemos el costo de la estación.
            costo_nuevo: int = int(alternativa["costo"])

            # Si supera el presupuesto, descartamos la alternativa.
            if costo_actual + costo_nuevo > presupuesto:
                ramas_podadas += 1
                continue

            # Unimos los incidentes sin duplicar sus identificadores.
            nuevos_incidentes: set[int] = (
                incidentes_actuales |
                alternativa["incidentes_cubiertos"]
            )

            # Agregamos la estación a la solución parcial.
            nuevas_estaciones: list[dict[str, Any]] = (
                estaciones_actuales + [alternativa]
            )

            # Continuamos con el siguiente lote.
            explorar_combinaciones(indice_lote + 1,costo_actual + costo_nuevo,nuevos_incidentes,nuevas_estaciones)


    # ---------------------------------------------------------
    # 7. Iniciar la búsqueda
    # ---------------------------------------------------------

    explorar_combinaciones(0,0,set(),[])

    # ---------------------------------------------------------
    # 8. Devolver los resultados
    # ---------------------------------------------------------

    return {
        "estaciones_seleccionadas": mejores_estaciones,
        "incidentes_cubiertos": mejores_incidentes,
        "costo_total": mejor_costo,
        "presupuesto_restante": presupuesto - mejor_costo,
        "valor_total": mejor_valor,
        "combinaciones_evaluadas": combinaciones_evaluadas,
        "ramas_podadas": ramas_podadas
    }
