
from datos.lector_datos import cargar_instancia
from algoritmos.grafo import construir_grafo
from algoritmos.distancias import distancias_desde


def main() -> None:
    # Seleccionamos la instancia con la que estamos trabajando.
    nombre_instancia: str = "pequena"

    # Cargamos los datos del profesor.
    datos = cargar_instancia(nombre_instancia)

    # Construimos el grafo a partir de las calles.
    grafo = construir_grafo(datos["calles"])

    print("Grafo construido correctamente.")
    print("Cantidad de nodos:", len(grafo))

    # Calculamos las distancias mínimas desde el nodo 0.
    origen: int = 0
    distancias: dict[int, int] = distancias_desde(grafo, origen)

    # Mostramos la distancia mínima a cada nodo alcanzable.
    print(f"\nDistancias mínimas desde el nodo {origen}:")

    for nodo in sorted(distancias):
        print(f"Hasta el nodo {nodo}: {distancias[nodo]} metros")


# Ejecutamos main() cuando este archivo se ejecuta directamente.
if __name__ == "__main__":
    main()
