
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


def evaluar_lote(grafo: dict[int, list[tuple[int, int]]],lote: dict[str, str], parametros: dict[str, Any], incidentes: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    """
    Evalúa los tres tipos de estación para un lote.

    Devuelve, por tipo, el costo, el radio y los incidentes cubiertos.
    """

    # Extraemos el nodo y el factor de zona del lote.
    nodo_lote: int = int(lote["nodo"])
    factor_zona: float = float(lote["factor_zona"])

    # Aquí guardaremos los resultados de cada tipo de estación.
    resultados: dict[str, dict[str, Any]] = {}

    # Recorremos los tipos definidos en parametros.json.
    for tipo, configuracion in parametros["tipos"].items():

        # Calculamos el costo específico de esta estación y este lote.
        costo: int = calcular_costo(factor_zona, int(configuracion["costo_base"]))

        # Buscamos qué incidentes del tipo correcto quedan cubiertos.
        cubiertos: list[int] = calcular_cobertura(grafo, nodo_lote, tipo, incidentes, int(configuracion["radio_m"]))

        # Guardamos la información para usarla en los algoritmos.
        resultados[tipo] = {
            "estacion": configuracion["estacion"],
            "costo": costo,
            "radio_m": int(configuracion["radio_m"]),
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
