import json
import subprocess
import sys
import time
import webbrowser
from typing import Any
import importlib.util
import subprocess
import sys
from pathlib import Path
from datos.lector_datos import cargar_instancia
from algoritmos.grafo import construir_grafo
from algoritmos.cobertura import evaluar_lote
from algoritmos.greedy_base import greedy_base
from algoritmos.heuristica_propia import greedy_eficiencia
from algoritmos.exacto import fuerza_bruta


def main() -> None:

    # ---------------------------------------------------------
    # 0. VERIFICAR E INSTALAR DEPENDENCIAS
    # ---------------------------------------------------------

    print("\nVerificando dependencias del proyecto...")

    # Ubicación del archivo requirements.txt.
    carpeta_proyecto = Path(__file__).resolve().parent
    ruta_requirements = carpeta_proyecto / "requirements.txt"

    # Verificar que exista el archivo de dependencias.
    if not ruta_requirements.exists():
        raise FileNotFoundError(    f"No se encontró el archivo: {ruta_requirements}")

    # Comprobar si Folium está instalado.
    if importlib.util.find_spec("folium") is None:

        print("Folium no está instalado.")
        print("Instalando dependencias del proyecto...")

        # Asegurar que pip esté disponible.
        subprocess.run(
            [
                sys.executable,
                "-m",
                "ensurepip",
                "--upgrade",
            ],
            check=True,
        )

        # Instalar las dependencias del requirements.txt.
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                str(ruta_requirements),
            ],
            check=True,
        )

        print("Dependencias instaladas correctamente.")

    else:
        print("Todas las dependencias están instaladas.")
    """Menú principal para ejecutar una o todas las instancias."""

    carpeta = Path(__file__).resolve().parent
    ruta_mapas = carpeta / "visualizaciones" / "mapas.py"
    carpeta_html = carpeta / "visualizaciones" / "resultados_visualizacion"

    while True:
        print("\n" + "=" * 62)
        print("       ESTACIONES PARA UNA ALCALDÍA NUEVA")
        print("=" * 62)
        print("\nSeleccione la instancia que desea ejecutar:\n")
        print("1. Ciudad")
        print("2. Comuna")
        print("3. Pequeña")
        print("4. Todas las instancias")
        print("0. Salir")

        opcion = input("\nIngrese una opción: ").strip()

        if opcion == "0":
            print("\nPrograma finalizado.")
            break
        elif opcion == "1":
            instancias = ["ciudad"]
        elif opcion == "2":
            instancias = ["comuna"]
        elif opcion == "3":
            instancias = ["pequena"]
        elif opcion == "4":
            instancias = ["ciudad", "comuna", "pequena"]
        else:
            print("\nOpción no válida. Intente nuevamente.")
            continue

        for nombre_instancia in instancias:
            print("\n" + "=" * 62)
            print(f"PROCESAMIENTO: {nombre_instancia.upper()}")
            print("=" * 62)

            inicio_total = time.perf_counter()
            datos: dict[str, Any] = cargar_instancia(nombre_instancia)
            parametros: dict[str, Any] = datos["parametros"]

            print("\nInformación de la instancia")
            print("Lotes:", len(datos["lotes"]))
            print("Incidentes:", len(datos["incidentes"]))
            print("Tramos:", len(datos["calles"]))

            inicio = time.perf_counter()
            grafo = construir_grafo(datos["calles"])
            tiempo_grafo = time.perf_counter() - inicio

            print("\nConstrucción del grafo")
            print("Nodos:", len(grafo))
            print("Tramos:", sum(len(vecinos) for vecinos in grafo.values()))
            print(f"Tiempo: {tiempo_grafo:.6f} segundos")

            # La evaluación requerida en la Parte 1 se mide para Ciudad.
            if nombre_instancia == "ciudad":
                inicio = time.perf_counter()
                cantidad_alternativas = 0

                for lote in datos["lotes"]:
                    alternativas = evaluar_lote(
                        grafo,
                        lote,
                        parametros,
                        datos["incidentes"],
                    )
                    cantidad_alternativas += len(alternativas)

                tiempo_evaluacion = time.perf_counter() - inicio
                print("\nEvaluación de lotes (Parte 1)")
                print("Lotes evaluados:", len(datos["lotes"]))
                print("Alternativas evaluadas:", cantidad_alternativas)
                print(f"Tiempo: {tiempo_evaluacion:.6f} segundos")
                print(
                    "¿Cumple el límite de 60 segundos?:",
                    "SÍ" if tiempo_evaluacion < 60 else "NO",
                )

            # Ejecutar Greedy base.
            inicio = time.perf_counter()
            resultado_base = greedy_base(
                grafo,
                datos["lotes"],
                datos["incidentes"],
                parametros,
            )
            tiempo_base = time.perf_counter() - inicio

            # Ejecutar la heurística propia.
            inicio = time.perf_counter()
            resultado_propia = greedy_eficiencia(
                grafo,
                datos["lotes"],
                datos["incidentes"],
                parametros,
            )
            tiempo_propia = time.perf_counter() - inicio

            # El exacto se ejecuta en Pequeña y Comuna, nunca en Ciudad.
            resultado_exacto = None
            tiempo_exacto = None

            if nombre_instancia in ("pequena", "comuna"):
                inicio = time.perf_counter()
                resultado_exacto = fuerza_bruta(
                    grafo,
                    datos["lotes"],
                    datos["incidentes"],
                    parametros,
                )
                tiempo_exacto = time.perf_counter() - inicio

            # Comparación de algoritmos.
            print("\n" + "-" * 72)
            print("COMPARACIÓN DE ALGORITMOS")
            print("-" * 72)
            print(
                f"{'Algoritmo':<22}{'Valor':>10}{'Costo':>14}"
                f"{'Cubiertos':>14}{'Tiempo (s)':>14}"
            )

            comparaciones = [
                ("Greedy base", resultado_base, tiempo_base),
                ("Heurística propia", resultado_propia, tiempo_propia),
            ]

            if resultado_exacto is not None:
                comparaciones.append(
                    ("Exacto", resultado_exacto, tiempo_exacto)
                )

            for nombre, resultado, duracion in comparaciones:
                print(
                    f"{nombre:<22}"
                    f"{resultado['valor_total']:>10}"
                    f"{resultado['costo_total']:>14}"
                    f"{len(resultado['incidentes_cubiertos']):>14}"
                    f"{duracion:>14.6f}"
                )

            # Seleccionar la propuesta oficial de cada instancia.
            if nombre_instancia == "ciudad":
                elegido = resultado_propia
                algoritmo_elegido = "greedy_eficiencia"
            else:
                elegido = resultado_exacto
                algoritmo_elegido = "fuerza_bruta"

            print("\n" + "-" * 72)
            print(f"SOLUCIÓN SELECCIONADA: {algoritmo_elegido}")
            print("-" * 72)
            print("Estaciones:", len(elegido["estaciones_seleccionadas"]))
            print("Costo total:", elegido["costo_total"], "millones")
            print("Presupuesto restante:", elegido["presupuesto_restante"], "millones")
            print("Valor total:", elegido["valor_total"])
            print("Incidentes cubiertos:", len(elegido["incidentes_cubiertos"]))

            print("\nDetalle de estaciones:")
            if not elegido["estaciones_seleccionadas"]:
                print("No se seleccionaron estaciones.")

            for estacion in elegido["estaciones_seleccionadas"]:
                ids = sorted(
                    estacion["incidentes_cubiertos"],
                    key=lambda identificador: int(identificador),
                )
                print(
                    f"- Lote {estacion['lote']} | {estacion['tipo']} | "
                    f"Costo: {estacion['costo']} millones | "
                    f"Incidentes cubiertos: {len(ids)}"
                )
                print("  IDs:", ids)

            # Pequeña se presenta en terminal; Ciudad y Comuna generan HTML.
            if nombre_instancia in ("ciudad", "comuna"):
                resultado_json = {
                    "instancia": nombre_instancia,
                    "algoritmo": algoritmo_elegido,
                    "estaciones_seleccionadas": [],
                    "incidentes_cubiertos": sorted(
                        elegido["incidentes_cubiertos"],
                        key=lambda identificador: int(identificador),
                    ),
                    "costo_total": elegido["costo_total"],
                    "presupuesto_restante": elegido["presupuesto_restante"],
                    "valor_total": elegido["valor_total"],
                }

                for estacion in elegido["estaciones_seleccionadas"]:
                    resultado_json["estaciones_seleccionadas"].append({
                        "lote": estacion["lote"],
                        "tipo": estacion["tipo"],
                        "estacion": estacion["estacion"],
                        "costo": estacion["costo"],
                        "incidentes_cubiertos": sorted(
                            estacion["incidentes_cubiertos"],
                            key=lambda identificador: int(identificador),
                        ),
                    })

                ruta_json = carpeta / f"resultados_{nombre_instancia}.json"
                with open(ruta_json, "w", encoding="utf-8") as archivo:
                    json.dump(
                        resultado_json,
                        archivo,
                        ensure_ascii=False,
                        indent=4,
                    )

                print(f"\nJSON guardado: {ruta_json}")

                # Ejecutar el generador de HTML para esta instancia.
                subprocess.run(
                    [sys.executable, str(ruta_mapas), nombre_instancia],
                    check=True,
                )

                ruta_html = carpeta_html / f"{nombre_instancia}.html"
                if ruta_html.exists():
                    webbrowser.open(ruta_html.as_uri())
                    print(f"Visualización abierta: {ruta_html}")
                else:
                    print(f"No se encontró el HTML esperado: {ruta_html}")

            tiempo_total = time.perf_counter() - inicio_total
            print(f"\nTiempo total de {nombre_instancia}: {tiempo_total:.6f} segundos")

        print("\n" + "=" * 62)
        print("PROCESAMIENTO SOLICITADO FINALIZADO")
        print("=" * 62)


if __name__ == "__main__":
    main()
