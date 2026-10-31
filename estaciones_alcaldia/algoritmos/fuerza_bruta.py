
from typing import Any

from algoritmos.cobertura import evaluar_lote, calcular_valor


def fuerza_bruta(grafo: dict[int, list[tuple[int, int]]],lotes: list[dict[str, str]],incidentes: list[dict[str, str]],parametros: dict[str, Any]) -> dict[str, Any]:
    """
    Examina todas las combinaciones posibles de estaciones.

    Selecciona la combinación factible que maximiza el valor
    total de los incidentes cubiertos.

    Cada lote puede tener cero o una estación.
    """

    # IMPORTANTE: el JSON real utiliza presupuesto_millones.
    presupuesto: int = int(parametros["presupuesto_millones"])

    # Guardamos todas las alternativas disponibles por lote.
    alternativas_por_lote: list[list[dict[str, Any] | None]] = []

    for lote in lotes:

        resultados: dict[str, dict[str, Any]] = evaluar_lote(grafo,lote,parametros,incidentes)

        # La opción None representa no instalar una estación.
        alternativas: list[dict[str, Any] | None] = [None]

        # Agregamos los tres tipos de estación disponibles.
        for tipo, resultado in resultados.items():

            alternativas.append({
                "lote": lote["lote"],
                "tipo": tipo,
                "estacion": resultado["estacion"],
                "costo": resultado["costo"],
                "incidentes_cubiertos": set(resultado["incidentes_cubiertos"])})

        alternativas_por_lote.append(alternativas)

    # Variables para guardar la mejor solución encontrada.
    mejor_valor: int = -1
    mejor_costo: int = 0
    mejores_estaciones: list[dict[str, Any]] = []
    mejores_incidentes: set[int] = set()

    # Contamos las combinaciones examinadas.
    combinaciones_evaluadas: int = 0

    def explorar_combinaciones(indice_lote: int,costo_actual: int,incidentes_actuales: set[int],estaciones_actuales: list[dict[str, Any]]) -> None:

        nonlocal mejor_valor
        nonlocal mejor_costo
        nonlocal mejores_estaciones
        nonlocal mejores_incidentes
        nonlocal combinaciones_evaluadas

        # Si superamos el presupuesto, descartamos esta rama.
        if costo_actual > presupuesto:
            return

        # Si ya procesamos todos los lotes, evaluamos la solución.
        if indice_lote == len(lotes):

            combinaciones_evaluadas += 1

            valor_actual: int = calcular_valor(incidentes_actuales,incidentes,parametros)

            # Buscamos el mayor valor total.
            # En caso de empate, preferimos menor costo.
            if (valor_actual > mejor_valor or (valor_actual == mejor_valor and costo_actual < mejor_costo)):
                mejor_valor = valor_actual
                mejor_costo = costo_actual
                mejores_estaciones = estaciones_actuales.copy()
                mejores_incidentes = incidentes_actuales.copy()

            return

        # Obtenemos las alternativas del lote actual.
        alternativas = alternativas_por_lote[indice_lote]

        # Probamos no instalar o instalar cada tipo de estación.
        for alternativa in alternativas:

            # Opción 1: no instalar una estación en este lote.
            if alternativa is None:
                explorar_combinaciones(indice_lote + 1,costo_actual,incidentes_actuales,estaciones_actuales)
                continue

            # Obtenemos el costo de la estación.
            costo_nuevo: int = alternativa["costo"]

            # Si no cabe en el presupuesto, la descartamos.
            if costo_actual + costo_nuevo > presupuesto:
                continue

            # Creamos una copia de los incidentes cubiertos. El operador | une los dos conjuntos y elimina automáticamente los elementos repetidos.
            nuevos_incidentes: set[int] = (incidentes_actuales | alternativa["incidentes_cubiertos"])

            # Agregamos la estación a la selección actual.
            nuevas_estaciones: list[dict[str, Any]] = (estaciones_actuales + [alternativa])

            # Exploramos las decisiones del siguiente lote.
            explorar_combinaciones(indice_lote + 1,costo_actual + costo_nuevo,nuevos_incidentes,nuevas_estaciones)

    # Iniciamos la exploración desde el primer lote.
    explorar_combinaciones(0,0,set(),[])

    # Devolvemos la mejor solución encontrada.
    return {
        "estaciones_seleccionadas": mejores_estaciones,
        "incidentes_cubiertos": mejores_incidentes,
        "costo_total": mejor_costo,
        "presupuesto_restante": presupuesto - mejor_costo,
        "valor_total": mejor_valor,
        "combinaciones_evaluadas": combinaciones_evaluadas
    }
