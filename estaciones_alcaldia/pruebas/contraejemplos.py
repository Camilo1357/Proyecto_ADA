
from typing import Any
import csv
import json
import sys
from pathlib import Path

# Permite ejecutar el archivo directamente desde VS Code.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from algoritmos.greedy_base import greedy_base
from algoritmos.heuristica_propia import greedy_eficiencia
from algoritmos.exacto import fuerza_bruta


def main() -> None:

    # Ubicación de las carpetas con las instancias de prueba.
    carpeta_instancias: Path = Path(__file__).resolve().parent / "instancias"

    nombres_instancias: list[str] = [
        "contraejemplo_greedy",
        "contraejemplo_propia"
    ]

    # Ejecutamos los dos contraejemplos.
    for nombre in nombres_instancias:

        carpeta: Path = carpeta_instancias / nombre

        # -----------------------------------------------------
        # 1. Leer los archivos CSV
        # -----------------------------------------------------

        with (carpeta / "nodos.csv").open(
            "r", encoding="utf-8", newline=""
        ) as archivo:
            nodos: list[dict[str, str]] = list(
                csv.DictReader(archivo)
            )

        with (carpeta / "aristas.csv").open(
            "r", encoding="utf-8", newline=""
        ) as archivo:
            aristas: list[dict[str, str]] = list(
                csv.DictReader(archivo)
            )

        with (carpeta / "lotes.csv").open(
            "r", encoding="utf-8", newline=""
        ) as archivo:
            lotes: list[dict[str, str]] = list(
                csv.DictReader(archivo)
            )

        with (carpeta / "incidentes.csv").open(
            "r", encoding="utf-8", newline=""
        ) as archivo:
            incidentes: list[dict[str, str]] = list(
                csv.DictReader(archivo)
            )

        # -----------------------------------------------------
        # 2. Leer los parámetros JSON
        # -----------------------------------------------------

        with (carpeta / "parametros.json").open(
            "r", encoding="utf-8"
        ) as archivo:
            parametros: dict[str, Any] = json.load(archivo)

        # -----------------------------------------------------
        # 3. Construir el grafo dirigido
        # -----------------------------------------------------

        grafo: dict[int, list[tuple[int, int]]] = {}

        # Inicializamos todos los nodos.
        for nodo in nodos:
            id_nodo: int = int(nodo["id"])
            grafo[id_nodo] = []

        # Agregamos las aristas respetando su dirección.
        for arista in aristas:

            origen: int = int(arista["origen"])
            destino: int = int(arista["destino"])
            longitud: int = int(arista["longitud_m"])

            grafo[origen].append((destino, longitud))

        # -----------------------------------------------------
        # 4. Ejecutar las tres estrategias
        # -----------------------------------------------------

        resultado_base: dict[str, Any] = greedy_base(
            grafo, lotes, incidentes, parametros
        )

        resultado_propio: dict[str, Any] = greedy_eficiencia(
            grafo, lotes, incidentes, parametros
        )

        resultado_exacto: dict[str, Any] = fuerza_bruta(
            grafo, lotes, incidentes, parametros
        )

        # -----------------------------------------------------
        # 5. Mostrar resultados
        # -----------------------------------------------------

        print("\n" + "=" * 55)
        print("INSTANCIA:", nombre)
        print("=" * 55)

        print("\nGREEDY BASE")
        print("Valor:", resultado_base["valor_total"])
        print("Costo:", resultado_base["costo_total"])
        print(
            "Estaciones:",
            resultado_base["estaciones_seleccionadas"]
        )

        print("\nHEURÍSTICA PROPIA")
        print("Valor:", resultado_propio["valor_total"])
        print("Costo:", resultado_propio["costo_total"])
        print(
            "Estaciones:",
            resultado_propio["estaciones_seleccionadas"]
        )

        print("\nSOLUCIÓN EXACTA")
        print("Valor:", resultado_exacto["valor_total"])
        print("Costo:", resultado_exacto["costo_total"])
        print(
            "Estaciones:",
            resultado_exacto["estaciones_seleccionadas"]
        )

        # -----------------------------------------------------
        # 6. Verificar que cada heurística tenga un contraejemplo
        # -----------------------------------------------------

        if nombre == "contraejemplo_greedy":

            assert resultado_base["valor_total"] == 10
            assert resultado_exacto["valor_total"] == 12

            assert (
                resultado_base["valor_total"]
                < resultado_exacto["valor_total"]
            )

        if nombre == "contraejemplo_propia":

            assert resultado_propio["valor_total"] == 9
            assert resultado_exacto["valor_total"] == 10

            assert (
                resultado_propio["valor_total"]
                < resultado_exacto["valor_total"]
            )

    # Si llegamos aquí, las dos pruebas fueron exitosas.
    print("\n" + "=" * 55)
    print("TODAS LAS COMPROBACIONES FUERON EXITOSAS")
    print("=" * 55)


if __name__ == "__main__":
    main()
