
import time
from typing import Any

from datos.lector_datos import cargar_instancia
from algoritmos.grafo import construir_grafo
from algoritmos.cobertura import evaluar_lote
from algoritmos.greedy_base import greedy_base
from algoritmos.heuristica_propia import greedy_eficiencia


def main() -> None:

    # -------------------------------------------------
    # 1. CARGA DE DATOS
    # -------------------------------------------------

    nombre_instancia: str = "ciudad"

    datos: dict[str, Any] = cargar_instancia(nombre_instancia)
    parametros: dict[str, Any] = datos["parametros"]

    print("\n========== INFORMACIÓN DE LA INSTANCIA ==========")
    print("Instancia:", nombre_instancia)
    print("Cantidad de lotes:", len(datos["lotes"]))
    print("Cantidad de incidentes:", len(datos["incidentes"]))
    print("Cantidad de tramos:", len(datos["calles"]))

    # -------------------------------------------------
    # 2. CONSTRUCCIÓN DEL GRAFO
    # -------------------------------------------------

    inicio_grafo = time.perf_counter()

    grafo = construir_grafo(datos["calles"])

    tiempo_grafo = time.perf_counter() - inicio_grafo

    print("\n========== CONSTRUCCIÓN DEL GRAFO ==========")
    print("Cantidad de nodos:", len(grafo))
    print(
        "Cantidad de tramos:",
        sum(len(vecinos) for vecinos in grafo.values())
    )
    print("Tiempo:", round(tiempo_grafo, 6), "segundos")

    # -------------------------------------------------
    # 3. EVALUACIÓN DE LOTES (PARTE 1)
    # -------------------------------------------------

    inicio_evaluacion = time.perf_counter()

    cantidad_alternativas = 0

    for lote in datos["lotes"]:

        resultados = evaluar_lote(
            grafo,
            lote,
            parametros,
            datos["incidentes"]
        )

        cantidad_alternativas += len(resultados)

    tiempo_evaluacion = time.perf_counter() - inicio_evaluacion

    print("\n========== EVALUACIÓN DE LOTES (PARTE 1) ==========")
    print("Lotes evaluados:", len(datos["lotes"]))
    print("Alternativas evaluadas:", cantidad_alternativas)
    print("Tiempo total:", round(tiempo_evaluacion, 6), "segundos")
    print(
        "¿Cumple el límite de 60 segundos?:",
        "SÍ" if tiempo_evaluacion < 60 else "NO"
    )

    # -------------------------------------------------
    # 4. EJECUCIÓN DEL GREEDY BASE
    # -------------------------------------------------

    inicio_base = time.perf_counter()

    resultado_base = greedy_base(
        grafo,
        datos["lotes"],
        datos["incidentes"],
        parametros
    )

    tiempo_base = time.perf_counter() - inicio_base

    print("\n========== RESUMEN GREEDY BASE ==========")
    print(
        "Estaciones seleccionadas:",
        len(resultado_base["estaciones_seleccionadas"])
    )
    print("Costo total:", resultado_base["costo_total"], "millones")
    print(
        "Presupuesto restante:",
        resultado_base["presupuesto_restante"],
        "millones"
    )
    print("Valor total:", resultado_base["valor_total"])
    print(
        "Incidentes cubiertos:",
        len(resultado_base["incidentes_cubiertos"])
    )
    print("Tiempo:", round(tiempo_base, 6), "segundos")

    # -------------------------------------------------
    # 5. EJECUCIÓN DE LA HEURÍSTICA PROPIA
    # -------------------------------------------------

    inicio_eficiencia = time.perf_counter()

    resultado_eficiencia = greedy_eficiencia(
        grafo,
        datos["lotes"],
        datos["incidentes"],
        parametros
    )

    tiempo_eficiencia = time.perf_counter() - inicio_eficiencia

    print("\n========== RESUMEN HEURÍSTICA PROPIA ==========")
    print(
        "Estaciones seleccionadas:",
        len(resultado_eficiencia["estaciones_seleccionadas"])
    )
    print(
        "Costo total:",
        resultado_eficiencia["costo_total"],
        "millones"
    )
    print(
        "Presupuesto restante:",
        resultado_eficiencia["presupuesto_restante"],
        "millones"
    )
    print("Valor total:", resultado_eficiencia["valor_total"])
    print(
        "Incidentes cubiertos:",
        len(resultado_eficiencia["incidentes_cubiertos"])
    )
    print("Tiempo:", round(tiempo_eficiencia, 6), "segundos")

    # -------------------------------------------------
    # 6. COMPARACIÓN DE RESULTADOS
    # -------------------------------------------------

    print("\n========== COMPARACIÓN DE RESULTADOS ==========")

    print(
        f"{'Métrica':<30}"
        f"{'Greedy base':>18}"
        f"{'Heurística propia':>22}"
    )

    print("-" * 70)

    print(
        f"{'Valor total':<30}"
        f"{resultado_base['valor_total']:>18}"
        f"{resultado_eficiencia['valor_total']:>22}"
    )

    print(
        f"{'Costo total':<30}"
        f"{resultado_base['costo_total']:>18}"
        f"{resultado_eficiencia['costo_total']:>22}"
    )

    print(
        f"{'Presupuesto restante':<30}"
        f"{resultado_base['presupuesto_restante']:>18}"
        f"{resultado_eficiencia['presupuesto_restante']:>22}"
    )

    print(
        f"{'Incidentes cubiertos':<30}"
        f"{len(resultado_base['incidentes_cubiertos']):>18}"
        f"{len(resultado_eficiencia['incidentes_cubiertos']):>22}"
    )

    print(
        f"{'Tiempo (segundos)':<30}"
        f"{tiempo_base:>18.6f}"
        f"{tiempo_eficiencia:>22.6f}"
    )

    print("\n========== FIN DE LA EJECUCIÓN ==========")


if __name__ == "__main__":
    main()
