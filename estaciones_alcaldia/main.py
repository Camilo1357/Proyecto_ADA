
from datos.lector_datos import cargar_instancia
from algoritmos.grafo import construir_grafo
from algoritmos.cobertura import evaluar_lote, calcular_valor, calcular_valor_adicional
from algoritmos.greedy import greedy_base
def main() -> None:
    # Cargamos la instancia pequeña.
    datos = cargar_instancia("pequena")

    # Construimos la red vial dirigida.
    grafo = construir_grafo(datos["calles"])

    # Obtenemos los parámetros de costos, radios y pesos.
    parametros = datos["parametros"]

    # Evaluamos cada tipo de estación en cada lote.
    for lote in datos["lotes"]:
        resultados = evaluar_lote(
            grafo,
            lote,
            parametros,
            datos["incidentes"]
        )

        print(f"\nLote {lote['lote']} (nodo {lote['nodo']}):")

        for tipo, resultado in resultados.items():
            print(f"  Tipo: {tipo}")
            print(f"  Estación: {resultado['estacion']}")
            print(f"  Costo: {resultado['costo']} millones")
            print(
                "  Incidentes cubiertos:",
                resultado["incidentes_cubiertos"]
            )
    
    # Cargamos los datos de la instancia pequeña.
    datos = cargar_instancia("pequena")

    # Obtenemos los parámetros de los tipos de incidentes.
    parametros = datos["parametros"]

    # Prueba: los incidentes 1, 2, 4 y 6 están cubiertos.
    # Son cuatro accidentes, y cada accidente vale 3 puntos.
    incidentes_cubiertos = {1, 2, 4, 6}

    # Calculamos el valor total de esos incidentes.
    valor = calcular_valor(
        incidentes_cubiertos,
        datos["incidentes"],
        parametros
    )

    print("\nPrueba de cálculo del valor:")
    print("Incidentes cubiertos:", sorted(incidentes_cubiertos))
    print("Valor total:", valor)
    print("Valor esperado: 12")

    
    # -----------------------------------------
    # PRUEBA DEL VALOR ADICIONAL
    # -----------------------------------------

    # Simulamos los incidentes que ya cubren
    # las estaciones seleccionadas anteriormente.
    incidentes_ya_cubiertos: set[int] = {1, 2, 4}

    # Simulamos los incidentes que cubre una nueva estación.
    incidentes_nueva_estacion: set[int] = {2, 4, 6}

    # Calculamos cuánto valor nuevo aporta esa estación.
    valor_adicional: int = calcular_valor_adicional(
        incidentes_nueva_estacion,
        incidentes_ya_cubiertos,
        datos["incidentes"],
        datos["parametros"]
    )

    print("\nPrueba del valor adicional:")
    print("Ya estaban cubiertos:", sorted(incidentes_ya_cubiertos))
    print("La nueva estación cubre:", sorted(incidentes_nueva_estacion))
    print("Valor adicional:", valor_adicional)
    print("Valor esperado: 3")

    
    # -----------------------------------------
    # EJECUCION DEL ALGORITMO GREEDY BASE
    # -----------------------------------------

    # Construimos el grafo vial con los datos cargados.
    grafo = construir_grafo(datos["calles"])

    # Ejecutamos Greedy con la instancia pequeña.
    resultado_greedy = greedy_base(
        grafo,
        datos["lotes"],
        datos["incidentes"],
        datos["parametros"]
    )

    # Mostramos las estaciones seleccionadas.
    print("\n========== RESULTADO GREEDY ==========")

    for estacion in resultado_greedy["estaciones_seleccionadas"]:
        print("\nLote:", estacion["lote"])
        print("Tipo:", estacion["tipo"])
        print("Estacion:", estacion["estacion"])
        print("Costo:", estacion["costo"], "millones")
        print("Valor adicional:", estacion["valor_adicional"])
        print("Eficiencia:", round(estacion["eficiencia"], 6))
        print("Incidentes cubiertos:", sorted(estacion["incidentes_cubiertos"]))

    # Mostramos el resumen general.
    print("\n========== RESUMEN ==========")
    print("Costo total:", resultado_greedy["costo_total"], "millones")
    print("Presupuesto restante:", resultado_greedy["presupuesto_restante"], "millones")
    print("Valor total:", resultado_greedy["valor_total"])
    print("Incidentes cubiertos:", sorted(resultado_greedy["incidentes_cubiertos"]))



if __name__ == "__main__":
    main()
