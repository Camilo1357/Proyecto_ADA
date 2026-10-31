
from typing import Any

from algoritmos.cobertura import (
    evaluar_lote,
    calcular_valor_adicional
)


def greedy_base(grafo: dict[int, list[tuple[int, int]]],lotes: list[dict[str, str]],incidentes: list[dict[str, str]],parametros: dict[str, Any]) -> dict[str, Any]:
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
