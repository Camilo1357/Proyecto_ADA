
import heapq


def distancias_desde(grafo: dict[int, list[tuple[int, float]]],origen: int) -> dict[int, float]:
    """
    Calcula la distancia mínima desde el origen hasta cada nodo alcanzable.

    grafo: conexiones dirigidas y sus longitudes en metros.
    origen: nodo desde el que comienza el recorrido.

    Retorna un diccionario {nodo: distancia_minima}.
    """

    # La distancia desde el origen hasta sí mismo es cero.
    distancias: dict[int, float] = {origen: 0.0}

    # La cola de prioridad almacena pares (distancia, nodo).
    cola: list[tuple[float, int]] = [(0.0, origen)]

    # Exploramos mientras haya caminos pendientes.
    while cola:

        # Extraemos el camino con menor distancia acumulada.
        distancia_actual, nodo_actual = heapq.heappop(cola)

        # Ignoramos una entrada si ya existe una distancia mejor.
        if distancia_actual > distancias[nodo_actual]:
            continue

        # Recorremos las conexiones que salen del nodo actual.
        for vecino, longitud in grafo[nodo_actual]:

            # Calculamos la distancia al vecino.
            nueva_distancia: float = distancia_actual + longitud

            # Actualizamos si encontramos una ruta mejor.
            if (
                vecino not in distancias
                or nueva_distancia < distancias[vecino]
            ):

                distancias[vecino] = nueva_distancia

                # Añadimos la nueva posibilidad a la cola.
                heapq.heappush(cola, (nueva_distancia, vecino))

    # Los nodos inalcanzables no aparecen en el resultado.
    return distancias
