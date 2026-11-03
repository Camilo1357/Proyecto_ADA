import time
from typing import Any

from datos.lector_datos import cargar_instancia
from algoritmos.grafo import construir_grafo
from algoritmos.cobertura import (
    evaluar_lote,
    calcular_valor,
    calcular_valor_adicional
)
from algoritmos.greedy_base import greedy_base
from algoritmos.heuristica_propia import greedy_eficiencia
from algoritmos.exacto import fuerza_bruta


def main() -> None:

    # -------------------------------------------------
    # 1. CARGA DE DATOS
    # -------------------------------------------------

    # Cambia "pequena" por "comuna" o "ciudad" para
    # ejecutar los algoritmos sobre otra instancia.
    nombre_instancia: str = "comuna"

    datos: dict[str, Any] = cargar_instancia(nombre_instancia)

    parametros: dict[str, Any] = datos["parametros"]

    # -------------------------------------------------
    # 2. CONSTRUCCIÓN DEL GRAFO
    # -------------------------------------------------

    grafo = construir_grafo(datos["calles"])

    print("\n========== INFORMACIÓN DEL GRAFO ==========")
    print("Instancia:", nombre_instancia)
    print("Cantidad de nodos:", len(grafo))
    print(
        "Cantidad de tramos:",
        sum(len(vecinos) for vecinos in grafo.values())
    )

    # -------------------------------------------------
    # 3. EVALUACIÓN DE LOS LOTES (PARTE 1)
    # -------------------------------------------------

    for lote in datos["lotes"]:

        resultados = evaluar_lote(
            grafo,
            lote,
            parametros,
            datos["incidentes"]
        )

        print(f"\nLote {lote['lote']} (nodo {lote['nodo']}):")

        for tipo, resultado in resultados.items():

            print(f"\n  Tipo: {tipo}")
            print(f"  Estación: {resultado['estacion']}")
            print(f"  Costo: {resultado['costo']} millones")
            print(
                "  Incidentes cubiertos:",
                sorted(resultado["incidentes_cubiertos"])
            )

    # -------------------------------------------------
    # 4. PRUEBA DEL CÁLCULO DEL VALOR
    # -------------------------------------------------

    incidentes_cubiertos: set[int] = {1, 2, 4, 6}

    valor = calcular_valor(
        incidentes_cubiertos,
        datos["incidentes"],
        parametros
    )

    print("\n========== PRUEBA DEL CÁLCULO DEL VALOR ==========")
    print("Incidentes cubiertos:", sorted(incidentes_cubiertos))
    print("Valor obtenido:", valor)

    # Esta prueba de referencia utiliza IDs de la instancia pequeña.
    if nombre_instancia == "pequena":
        print("Valor esperado: 12")

    # -------------------------------------------------
    # 5. PRUEBA DEL VALOR ADICIONAL
    # -------------------------------------------------

    incidentes_ya_cubiertos: set[int] = {1, 2, 4}
    incidentes_nueva_estacion: set[int] = {2, 4, 6}

    valor_adicional = calcular_valor_adicional(
        incidentes_nueva_estacion,
        incidentes_ya_cubiertos,
        datos["incidentes"],
        parametros
    )

    print("\n========== PRUEBA DEL VALOR ADICIONAL ==========")
    print("Ya estaban cubiertos:", sorted(incidentes_ya_cubiertos))
    print("Nueva estación cubre:", sorted(incidentes_nueva_estacion))
    print("Valor adicional obtenido:", valor_adicional)

    if nombre_instancia == "pequena":
        print("Valor esperado: 3")

    # -------------------------------------------------
    # 6. EJECUCIÓN DEL GREEDY BASE DEL PROFESOR
    # -------------------------------------------------

    inicio_base = time.perf_counter()

    resultado_base = greedy_base(
        grafo,
        datos["lotes"],
        datos["incidentes"],
        parametros
    )

    tiempo_base = time.perf_counter() - inicio_base

    print("\n========== RESULTADO GREEDY BASE ==========")

    for estacion in resultado_base["estaciones_seleccionadas"]:

        print("\nLote:", estacion["lote"])
        print("Tipo:", estacion["tipo"])
        print("Estación:", estacion["estacion"])
        print("Costo:", estacion["costo"], "millones")
        print("Valor adicional:", estacion["valor_adicional"])
        print(
            "Incidentes cubiertos:",
            sorted(estacion["incidentes_cubiertos"])
        )

    print("\n========== RESUMEN GREEDY BASE ==========")
    print("Costo total:", resultado_base["costo_total"], "millones")
    print(
        "Presupuesto restante:",
        resultado_base["presupuesto_restante"],
        "millones"
    )
    print("Valor total:", resultado_base["valor_total"])
    print("Tiempo:", round(tiempo_base, 6), "segundos")
    print(
        "Incidentes cubiertos:",
        sorted(resultado_base["incidentes_cubiertos"])
    )

    # -------------------------------------------------
    # 7. EJECUCIÓN DE NUESTRA HEURÍSTICA PROPIA
    # -------------------------------------------------

    inicio_eficiencia = time.perf_counter()

    resultado_eficiencia = greedy_eficiencia(
        grafo,
        datos["lotes"],
        datos["incidentes"],
        parametros
    )

    tiempo_eficiencia = time.perf_counter() - inicio_eficiencia

    print("\n========== RESULTADO HEURÍSTICA PROPIA ==========")

    for estacion in resultado_eficiencia["estaciones_seleccionadas"]:

        print("\nLote:", estacion["lote"])
        print("Tipo:", estacion["tipo"])
        print("Estación:", estacion["estacion"])
        print("Costo:", estacion["costo"], "millones")
        print("Valor adicional:", estacion["valor_adicional"])
        print("Eficiencia:", round(estacion["eficiencia"], 6))
        print(
            "Incidentes cubiertos:",
            sorted(estacion["incidentes_cubiertos"])
        )

    print("\n========== RESUMEN HEURÍSTICA PROPIA ==========")
    print("Costo total:", resultado_eficiencia["costo_total"], "millones")
    print(
        "Presupuesto restante:",
        resultado_eficiencia["presupuesto_restante"],
        "millones"
    )
    print("Valor total:", resultado_eficiencia["valor_total"])
    print("Tiempo:", round(tiempo_eficiencia, 6), "segundos")
    print(
        "Incidentes cubiertos:",
        sorted(resultado_eficiencia["incidentes_cubiertos"])
    )

    # -------------------------------------------------
    # 8. EJECUCIÓN DEL ALGORITMO EXACTO
    # -------------------------------------------------

    inicio_exacto = time.perf_counter()

    resultado_exacto = fuerza_bruta(
        grafo,
        datos["lotes"],
        datos["incidentes"],
        parametros
    )

    tiempo_exacto = time.perf_counter() - inicio_exacto

    print("\n========== RESULTADO ALGORITMO EXACTO ==========")

    for estacion in resultado_exacto["estaciones_seleccionadas"]:

        print("\nLote:", estacion["lote"])
        print("Tipo:", estacion["tipo"])
        print("Estación:", estacion["estacion"])
        print("Costo:", estacion["costo"], "millones")
        print(
            "Incidentes cubiertos:",
            sorted(estacion["incidentes_cubiertos"])
        )

    print("\n========== RESUMEN ALGORITMO EXACTO ==========")
    print("Costo total:", resultado_exacto["costo_total"], "millones")
    print(
        "Presupuesto restante:",
        resultado_exacto["presupuesto_restante"],
        "millones"
    )
    print("Valor total:", resultado_exacto["valor_total"])
    print(
        "Incidentes cubiertos:",
        sorted(resultado_exacto["incidentes_cubiertos"])
    )
    print(
        "Combinaciones evaluadas:",
        resultado_exacto["combinaciones_evaluadas"]
    )
    print("Tiempo:", round(tiempo_exacto, 6), "segundos")

    # -------------------------------------------------
    # 9. COMPARACIÓN DE LOS TRES ALGORITMOS
    # -------------------------------------------------

    print("\n========== COMPARACIÓN DE RESULTADOS ==========")

    print(
        f"{'Métrica':<25}"
        f"{'Greedy base':>15}"
        f"{'Eficiencia':>15}"
        f"{'Exacto':>15}"
    )

    print("-" * 70)

    print(
        f"{'Valor total':<25}"
        f"{resultado_base['valor_total']:>15}"
        f"{resultado_eficiencia['valor_total']:>15}"
        f"{resultado_exacto['valor_total']:>15}"
    )

    print(
        f"{'Costo total':<25}"
        f"{resultado_base['costo_total']:>15}"
        f"{resultado_eficiencia['costo_total']:>15}"
        f"{resultado_exacto['costo_total']:>15}"
    )

    print(
        f"{'Presupuesto restante':<25}"
        f"{resultado_base['presupuesto_restante']:>15}"
        f"{resultado_eficiencia['presupuesto_restante']:>15}"
        f"{resultado_exacto['presupuesto_restante']:>15}"
    )

    print(
        f"{'Tiempo (segundos)':<25}"
        f"{tiempo_base:>15.6f}"
        f"{tiempo_eficiencia:>15.6f}"
        f"{tiempo_exacto:>15.6f}"
    )


if __name__ == "__main__":
    main()