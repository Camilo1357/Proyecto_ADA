
def construir_grafo(
    filas_calles: list[dict[str, str]]
) -> dict[int, list[tuple[int, int]]]:
    """
    Convierte las filas de aristas.csv en un diccionario de adyacencia.

    Cada clave es un nodo.
    Cada conexión contiene (nodo_destino, distancia_en_metros).
    """

    # Diccionario donde cada nodo tendrá sus conexiones salientes.
    grafo: dict[int, list[tuple[int, int]]] = {}

    # Recorremos todas las filas del archivo de calles.
    for calle in filas_calles:

        # Convertimos los textos del CSV en números enteros.
        origen: int = int(calle["origen"])
        destino: int = int(calle["destino"])
        distancia: int = int(calle["longitud_m"])

        # Creamos la lista de conexiones del origen si hace falta.
        if origen not in grafo:
            grafo[origen] = []

        # Agregamos la conexión dirigida del origen al destino.
        grafo[origen].append((destino, distancia))

        # Registramos el destino aunque no tenga salidas.
        if destino not in grafo:
            grafo[destino] = []

    # Devolvemos el grafo completo.
    return grafo
