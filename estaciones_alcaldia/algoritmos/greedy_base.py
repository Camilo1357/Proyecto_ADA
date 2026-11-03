
from typing import Any

from algoritmos.cobertura import (
    evaluar_lote,
    calcular_valor_adicional
)


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

    # Presupuesto total disponible.
    presupuesto: int = int(parametros["presupuesto_millones"])

    # Resultados de la propuesta.
    estaciones_seleccionadas: list[dict[str, Any]] = []

    # Incidentes que ya están cubiertos por alguna estación elegida.
    incidentes_ya_cubiertos: set[int] = set()

    # Lotes que ya tienen una estación.
    lotes_utilizados: set[str] = set()

    # Orden de tipos establecido por el profesor para desempatar.
    orden_tipos: list[str] = [
        "hurto",
        "accidente",
        "incendio"
    ]

    # Calculamos las alternativas de cada lote una sola vez.
    alternativas_por_lote: dict[str, dict[str, dict[str, Any]]] = {}

    for lote in lotes:
        id_lote: str = lote["lote"]

        alternativas_por_lote[id_lote] = evaluar_lote(grafo,lote,parametros,incidentes)

    # Ordenamos los lotes para resolver correctamente los empates.
    lotes_ordenados: list[dict[str, str]] = sorted(lotes,key=lambda lote: lote["lote"])

    # Repetimos mientras exista una estación que aporte valor.
    while True:

        mejor_alternativa: dict[str, Any] | None = None
        mayor_valor_adicional: int = 0

        # Recorremos los lotes en orden de código.
        for lote in lotes_ordenados:

            id_lote: str = lote["lote"]

            # No podemos construir más de una estación en el mismo lote.
            if id_lote in lotes_utilizados:
                continue

            alternativas: dict[str, dict[str, Any]] = (alternativas_por_lote[id_lote])

            # Recorremos los tipos en el orden oficial de desempate.
            for tipo in orden_tipos:

                # Si el tipo no está disponible en los parámetros, lo omitimos.
                if tipo not in alternativas:
                    continue

                alternativa: dict[str, Any] = alternativas[tipo]
                costo: int = alternativa["costo"]

                # La estación debe caber en el presupuesto restante.
                if costo > presupuesto:
                    continue

                # Convertimos los incidentes cubiertos a conjunto.
                incidentes_cubiertos: set[int] = set(alternativa["incidentes_cubiertos"])

                # Calculamos el valor que todavía no está cubierto.
                valor_adicional: int = calcular_valor_adicional(incidentes_cubiertos,incidentes_ya_cubiertos,incidentes,parametros)

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

        # Unimos los nuevos incidentes con los que ya estaban cubiertos.
        incidentes_ya_cubiertos.update(mejor_alternativa["incidentes_cubiertos"])

    # Calculamos el valor total de la propuesta.
    valor_total: int = calcular_valor_adicional(
        incidentes_ya_cubiertos,
        set(),
        incidentes,
        parametros
    )

    # Devolvemos el mismo formato general de resultados de la heurística propia.
    return {
        "estaciones_seleccionadas": estaciones_seleccionadas,
        "incidentes_cubiertos": incidentes_ya_cubiertos,
        "costo_total": sum(
            estacion["costo"]
            for estacion in estaciones_seleccionadas
        ),
        "presupuesto_restante": presupuesto,
        "valor_total": valor_total
    }
