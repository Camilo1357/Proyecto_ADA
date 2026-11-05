
from typing import Any

from algoritmos.distancias import distancias_desde


def calcular_costo(factor_zona: float,costo_base: int) -> int:
    """
    Calcula el costo de construir una estación en un lote.

    El costo base se multiplica por el factor de zona
    y se redondea al millón de pesos más cercano.
    """

    costo: int = round(costo_base * factor_zona)

    return costo


def calcular_cobertura(grafo: dict[int, list[tuple[int, int]]], nodo_estacion: int, tipo_estacion: str, incidentes: list[dict[str, str]], radio_m: int) -> list[int]:
    """
    Devuelve los identificadores de los incidentes cubiertos
    por una estación ubicada en un nodo determinado.

    Solo cubre incidentes del mismo tipo y dentro del radio.
    Las distancias respetan las direcciones de las calles.
    """

    # Calculamos las distancias mínimas desde el nodo de la estación.
    distancias: dict[int, int] = distancias_desde(grafo,nodo_estacion)

    # Aquí guardaremos los IDs de los incidentes cubiertos.
    incidentes_cubiertos: list[int] = []

    # Revisamos todos los incidentes registrados.
    for incidente in incidentes:

        # Convertimos los campos del CSV a los tipos necesarios.
        id_incidente: int = int(incidente["id"])
        nodo_incidente: int = int(incidente["nodo"])
        tipo_incidente: str = incidente["tipo"]

        # Una estación solo atiende incidentes de su propio tipo.
        if tipo_incidente != tipo_estacion:
            continue

        # Si el nodo no aparece, no es alcanzable desde la estación.
        if nodo_incidente not in distancias:
            continue

        # Obtenemos la distancia mínima hasta el nodo del incidente.
        distancia: int = distancias[nodo_incidente]

        # El incidente se cubre si está dentro del radio permitido.
        if distancia <= radio_m:
            incidentes_cubiertos.append(id_incidente)

    # Devolvemos los IDs, no los puntos, porque los puntos
    # dependen del peso asociado a cada tipo de incidente.
    return incidentes_cubiertos


def evaluar_lote(grafo: dict[int, list[tuple[int, int]]],lote: dict[str, str],parametros: dict[str, Any],incidentes: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    """
    Evalúa los tres tipos de estación para un lote.

    Calcula las distancias una sola vez y las reutiliza
    para evaluar los diferentes tipos de estación.
    """

    nodo_lote: int = int(lote["nodo"])
    factor_zona: float = float(lote["factor_zona"])

    # Una sola ejecución de Dijkstra para este lote.
    distancias: dict[int, float] = distancias_desde(grafo, nodo_lote)

    resultados: dict[str, dict[str, Any]] = {}

    for tipo, configuracion in parametros["tipos"].items():

        costo: int = calcular_costo(factor_zona,int(configuracion["costo_base"]))
  
        radio_m: int = int(configuracion["radio_m"])

        cubiertos: list[int] = []

        # Reutilizamos las distancias para cada tipo.
        for incidente in incidentes:

            if incidente["tipo"] != tipo:
                continue

            id_incidente: int = int(incidente["id"])
            nodo_incidente: int = int(incidente["nodo"])

            if nodo_incidente not in distancias:
                continue

            if distancias[nodo_incidente] <= radio_m:
                cubiertos.append(id_incidente)

        resultados[tipo] = {
            "estacion": configuracion["estacion"],
            "costo": costo,
            "radio_m": radio_m,
            "peso": int(configuracion["peso"]),
            "incidentes_cubiertos": cubiertos
        }

    return resultados


def calcular_valor(incidentes_cubiertos: set[int], incidentes: list[dict[str, str]], parametros: dict[str, Any]) -> int:
    """
    Calcula el valor total de los incidentes cubiertos.

    Cada incidente se cuenta una sola vez, aunque varias
    estaciones puedan cubrirlo.

    El valor de cada incidente depende de su tipo:
    - Hurto: 1 punto.
    - Accidente: 3 puntos.
    - Incendio: 5 puntos.
    """
    valor_total: int = 0

    # Recorremos los incidentes registrados en los datos.
    for incidente in incidentes:
        # Convertimos el identificador a entero para compararlo
        # con los identificadores del conjunto de cubiertos.
        id_incidente: int = int(incidente["id"])

        # Si el incidente no está cubierto, no aporta valor.
        if id_incidente not in incidentes_cubiertos:
            continue

        # Consultamos el tipo de incidente.
        tipo: str = incidente["tipo"]

        # Obtenemos el peso que corresponde a ese tipo.
        peso: int = int(parametros["tipos"][tipo]["peso"])

        # Sumamos el peso una sola vez por incidente.
        valor_total += peso

    return valor_total


def calcular_valor_adicional(incidentes_cubiertos: set[int], incidentes_ya_cubiertos: set[int], incidentes: list[dict[str, str]], parametros: dict[str, Any]) -> int:
    """
    Calcula el valor de los incidentes nuevos que aporta una estación.

    Los incidentes que ya están cubiertos no suman valor otra vez.
    """
    # Restamos los incidentes que ya estaban cubiertos.
    incidentes_nuevos: set[int] = (incidentes_cubiertos - incidentes_ya_cubiertos)

    # Calculamos el valor únicamente de los incidentes nuevos.
    return calcular_valor(incidentes_nuevos,incidentes,parametros)


def construir_valores_incidentes(incidentes: list[dict[str, str]],parametros: dict[str, Any]) -> dict[int, int]:
    """
    Construye un diccionario que relaciona cada ID de incidente
    con su valor, según el tipo de incidente.
    """

    valores: dict[int, int] = {}

    for incidente in incidentes:
        id_incidente: int = int(incidente["id"])
        tipo: str = incidente["tipo"]

        peso: int = int(parametros["tipos"][tipo]["peso"])

        valores[id_incidente] = peso

    return valores

def calcular_valor_rapido(incidentes_cubiertos: set[int],valores_incidentes: dict[int, int]) -> int:
    """
    Calcula el valor de los incidentes cubiertos consultando
    directamente el diccionario de pesos.
    """

    valor_total: int = 0

    for id_incidente in incidentes_cubiertos:
        valor_total += valores_incidentes.get(id_incidente, 0)

    return valor_total