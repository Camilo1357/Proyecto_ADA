
import csv
import json
from pathlib import Path
from typing import Any


# Ruta absoluta de la raíz del proyecto.
# parents[0] = datos, parents[1] = estaciones_alcaldia,
# parents[2] = carpeta raíz del repositorio.
RAIZ_PROYECTO: Path = Path(__file__).resolve().parents[2]

# Carpeta que contiene pequena, comuna y ciudad.
CARPETA_INSTANCIAS: Path = RAIZ_PROYECTO / "instancias"


def leer_csv(ruta: Path) -> list[dict[str, str]]:
    """Lee un CSV y devuelve sus filas como una lista de diccionarios."""

    # Abrimos el archivo con la codificación adecuada.
    with open(ruta, encoding="utf-8", newline="") as archivo:
        # Cada fila usa los encabezados del CSV como claves.
        return list(csv.DictReader(archivo))


def cargar_instancia(nombre: str = "pequena") -> dict[str, Any]:
    """Carga los CSV y los parámetros JSON de una instancia."""

    # Solo permitimos los nombres de las instancias disponibles.
    nombres_validos: set[str] = {"pequena", "comuna", "ciudad"}

    if nombre not in nombres_validos:
        raise ValueError(
            f"Instancia desconocida: {nombre}. "
            "Usa pequena, comuna o ciudad."
        )

    # Construimos la ruta a la instancia seleccionada.
    carpeta: Path = CARPETA_INSTANCIAS / nombre

    # Comprobamos que la carpeta exista.
    if not carpeta.is_dir():
        raise FileNotFoundError(
            f"No se encontró la carpeta de datos: {carpeta}"
        )

    # Leemos los cuatro archivos CSV.
    datos: dict[str, Any] = {
        "nodos": leer_csv(carpeta / "nodos.csv"),
        "calles": leer_csv(carpeta / "aristas.csv"),
        "lotes": leer_csv(carpeta / "lotes.csv"),
        "incidentes": leer_csv(carpeta / "incidentes.csv"),
    }

    # Leemos los parámetros generales desde el archivo JSON.
    with open(
        carpeta / "parametros.json",
        encoding="utf-8"
    ) as archivo:
        datos["parametros"] = json.load(archivo)

    # Devolvemos todos los datos reunidos.
    return datos
