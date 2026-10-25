
from datos.lector_datos import cargar_instancia
from algoritmos.grafo import construir_grafo
from algoritmos.cobertura import evaluar_lote, calcular_valor

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



if __name__ == "__main__":
    main()
