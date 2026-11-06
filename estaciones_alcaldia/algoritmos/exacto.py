
from typing import Any

from algoritmos.cobertura import (
    evaluar_lote,
    construir_valores_incidentes
)


def fuerza_bruta(grafo: dict[int, list[tuple[int, float]]],lotes: list[dict[str, str]],incidentes: list[dict[str, str]],parametros: dict[str, Any]) -> dict[str, Any]:
    """
    Encuentra la solución óptima mediante fuerza bruta con Backtracking.

    Optimizaciones:
    - Ordenamiento de lotes por potencial de cobertura.
    - Ordenamiento de alternativas por valor potencial.
    - Poda por presupuesto.
    - Poda por valor máximo restante.
    - Modificación y restauración de conjuntos durante la recursión.

    No utiliza Greedy ni soluciones iniciales heurísticas.
    """

    # ---------------------------------------------------------
    # 1. Preparar los datos
    # ---------------------------------------------------------

    valores_incidentes: dict[int, int] = construir_valores_incidentes(incidentes, parametros)

    presupuesto: int = int(parametros["presupuesto_millones"])

    # ---------------------------------------------------------
    # 2. Construir las alternativas de cada lote
    # ---------------------------------------------------------

    alternativas_por_lote: list[list[dict[str, Any]]] = []

    for lote in lotes:

        resultados = evaluar_lote(grafo, lote, parametros, incidentes)

        alternativas: list[dict[str, Any]] = []

        for tipo, resultado in resultados.items():

            ids_cubiertos: set[int] = set(resultado["incidentes_cubiertos"])

            valor_potencial: int = sum(
                valores_incidentes.get(id_incidente, 0)
                for id_incidente in ids_cubiertos
            )

            alternativas.append({
                "lote": lote["lote"],
                "tipo": tipo,
                "estacion": resultado["estacion"],
                "costo": int(resultado["costo"]),
                "incidentes_cubiertos": ids_cubiertos,
                "valor_potencial": valor_potencial
            })

        alternativas_por_lote.append(alternativas)

    cantidad_lotes: int = len(alternativas_por_lote)

    # ---------------------------------------------------------
    # 3. Ordenar los lotes por potencial de cobertura
    # ---------------------------------------------------------

    alternativas_por_lote.sort(
        key=lambda alternativas: max(
            (alternativa["valor_potencial"]
             for alternativa in alternativas),
            default=0),
        reverse=True
    )

    # ---------------------------------------------------------
    # 4. Ordenar las alternativas de cada lote
    # ---------------------------------------------------------

    for alternativas in alternativas_por_lote:

        alternativas.sort(
            key=lambda alternativa: alternativa["valor_potencial"],
            reverse=True
        )

    # ---------------------------------------------------------
    # 5. Preparar la mejor solución conocida
    # ---------------------------------------------------------

    # Empezamos con la solución vacía.
    # No se construye ninguna solución mediante Greedy.

    mejor_valor: int = 0
    mejor_costo: int = 0

    mejores_estaciones: list[dict[str, Any]] = []
    mejores_incidentes: set[int] = set()

    # ---------------------------------------------------------
    # 6. Calcular los incidentes posibles desde cada posición
    # ---------------------------------------------------------

    valor_maximo_restante: list[set[int]] = [
        set() for _ in range(cantidad_lotes + 1)
    ]

    for indice in range(cantidad_lotes - 1, -1, -1):

        posibles: set[int] = (valor_maximo_restante[indice + 1].copy())

        for alternativa in alternativas_por_lote[indice]:

            posibles.update(alternativa["incidentes_cubiertos"])

        valor_maximo_restante[indice] = posibles

    # ---------------------------------------------------------
    # 7. Variables de seguimiento
    # ---------------------------------------------------------

    combinaciones_evaluadas: int = 0
    nodos_visitados: int = 0

    ramas_podadas_presupuesto: int = 0
    ramas_podadas_valor: int = 0

    incidentes_actuales: set[int] = set()
    estaciones_actuales: list[dict[str, Any]] = []

    # ---------------------------------------------------------
    # 8. Backtracking
    # ---------------------------------------------------------

    def explorar_combinaciones(indice_lote: int,costo_actual: int,valor_actual: int) -> None:

        nonlocal mejor_valor
        nonlocal mejor_costo
        nonlocal mejores_estaciones
        nonlocal mejores_incidentes
        nonlocal combinaciones_evaluadas
        nonlocal nodos_visitados
        nonlocal ramas_podadas_presupuesto
        nonlocal ramas_podadas_valor

        nodos_visitados += 1

        # -----------------------------------------------------
        # Poda 1: presupuesto
        # -----------------------------------------------------

        if costo_actual > presupuesto:

            ramas_podadas_presupuesto += 1
            return

        # -----------------------------------------------------
        # Poda 2: valor máximo restante
        # -----------------------------------------------------

        incidentes_pendientes: set[int] = (valor_maximo_restante[indice_lote] - incidentes_actuales)

        valor_adicional_maximo: int = sum(
            valores_incidentes.get(id_incidente, 0)
            for id_incidente in incidentes_pendientes
        )

        valor_posible: int = (valor_actual + valor_adicional_maximo)

        # Si esta rama no puede superar la mejor solución,
        # no tiene sentido continuar explorándola.

        if (valor_posible < mejor_valor or (valor_posible == mejor_valor and costo_actual >= mejor_costo)):
            ramas_podadas_valor += 1
            return

        # -----------------------------------------------------
        # Caso base: todos los lotes fueron procesados
        # -----------------------------------------------------

        if indice_lote == cantidad_lotes:

            combinaciones_evaluadas += 1

            if (valor_actual > mejor_valor or (valor_actual == mejor_valor and costo_actual < mejor_costo)):

                mejor_valor = valor_actual
                mejor_costo = costo_actual

                mejores_estaciones = (estaciones_actuales.copy())

                mejores_incidentes = (incidentes_actuales.copy())

            return

        # -----------------------------------------------------
        # 9. Explorar las alternativas del lote actual
        # -----------------------------------------------------

        alternativas: list[dict[str, Any]] = (alternativas_por_lote[indice_lote])

        for alternativa in alternativas:

            nuevo_costo: int = (costo_actual + alternativa["costo"])

            # Descartar si supera el presupuesto.

            if nuevo_costo > presupuesto:

                ramas_podadas_presupuesto += 1
                continue

            # Identificar únicamente los incidentes nuevos.

            nuevos_incidentes: set[int] = (alternativa["incidentes_cubiertos"] - incidentes_actuales)

            # No instalar una estación que no aporte cobertura.

            if not nuevos_incidentes:
                continue

            ganancia: int = sum(valores_incidentes.get(id_incidente, 0) for id_incidente in nuevos_incidentes)

            # Agregar temporalmente la alternativa.

            incidentes_actuales.update(nuevos_incidentes)
            estaciones_actuales.append(alternativa)

            explorar_combinaciones(indice_lote + 1,nuevo_costo,valor_actual + ganancia)

            # Restaurar el estado para explorar otra alternativa.

            estaciones_actuales.pop()

            incidentes_actuales.difference_update(nuevos_incidentes)

        # -----------------------------------------------------
        # 10. Explorar la opción de no instalar estación
        # -----------------------------------------------------

        explorar_combinaciones(indice_lote + 1,costo_actual,valor_actual)

    # ---------------------------------------------------------
    # 11. Ejecutar la búsqueda
    # ---------------------------------------------------------

    explorar_combinaciones(0, 0, 0)

    # Ordenar la solución por código de lote.

    mejores_estaciones.sort(key=lambda estacion: estacion["lote"])

    # ---------------------------------------------------------
    # 12. Preparar la salida
    # ---------------------------------------------------------

    estaciones_resultado: list[dict[str, Any]] = []

    for alternativa in mejores_estaciones:

        estaciones_resultado.append({
            "lote": alternativa["lote"],
            "tipo": alternativa["tipo"],
            "estacion": alternativa["estacion"],
            "costo": alternativa["costo"],
            "incidentes_cubiertos": (
                alternativa["incidentes_cubiertos"].copy()
            )
        })

    ramas_podadas: int = (
        ramas_podadas_presupuesto
        + ramas_podadas_valor
    )

    return {
        "estaciones_seleccionadas": estaciones_resultado,
        "incidentes_cubiertos": mejores_incidentes,
        "costo_total": mejor_costo,
        "presupuesto_restante": presupuesto - mejor_costo,
        "valor_total": mejor_valor,
        "combinaciones_evaluadas": combinaciones_evaluadas,
        "nodos_visitados": nodos_visitados,
        "ramas_podadas": ramas_podadas,
        "ramas_podadas_presupuesto": ramas_podadas_presupuesto,
        "ramas_podadas_valor": ramas_podadas_valor
    }
