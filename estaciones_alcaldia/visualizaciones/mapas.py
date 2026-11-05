import csv
import html
import json
import sys
from pathlib import Path

import folium


def main() -> None:
    """
    Genera una visualización HTML por instancia.

    Cada visualización principal contiene dos pestañas:
    - Mapa interactivo.
    - Tabla de estaciones.

    El mapa de Folium se guarda en un archivo HTML independiente.
    Esto evita incrustarlo como data URL, mecanismo que puede fallar
    cuando el mapa contiene muchos elementos (por ejemplo, Ciudad).
    """

    # ---------------------------------------------------------
    # 1. PREPARAR RUTAS
    # ---------------------------------------------------------

    raiz = Path(__file__).resolve().parents[1]
    carpeta_instancias = raiz.parent / "instancias"

    carpeta_salida = (
        raiz / "visualizaciones" / "resultados_visualizacion"
    )
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    instancias = (
        sys.argv[1:]
        if len(sys.argv) > 1
        else ["ciudad", "comuna"]
    )

    colores = {
        "hurto": "blue",
        "accidente": "orange",
        "incendio": "red",
    }

    # ---------------------------------------------------------
    # 2. PROCESAR CADA INSTANCIA
    # ---------------------------------------------------------

    for instancia in instancias:

        carpeta_datos = carpeta_instancias / instancia
        ruta_resultado = raiz / f"resultados_{instancia}.json"

        if not carpeta_datos.exists():
            print(f"No existe la instancia: {carpeta_datos}")
            continue

        if not ruta_resultado.exists():
            print(f"No existe el resultado: {ruta_resultado}")
            continue

        # -----------------------------------------------------
        # 3. LEER COORDENADAS
        # -----------------------------------------------------

        coordenadas = {}

        with open(
            carpeta_datos / "nodos.csv",
            encoding="utf-8",
            newline="",
        ) as archivo:
            for fila in csv.DictReader(archivo):
                coordenadas[int(fila["id"])] = (
                    float(fila["lat"]),
                    float(fila["lon"]),
                )

        if not coordenadas:
            print(f"La instancia {instancia} no tiene nodos.")
            continue

        # -----------------------------------------------------
        # 4. LEER LOTES
        # -----------------------------------------------------

        lotes = []

        with open(
            carpeta_datos / "lotes.csv",
            encoding="utf-8",
            newline="",
        ) as archivo:
            for fila in csv.DictReader(archivo):
                lotes.append({
                    "lote": str(fila["lote"]),
                    "nodo": int(fila["nodo"]),
                })

        lotes_por_id = {
            lote["lote"]: lote
            for lote in lotes
        }

        # -----------------------------------------------------
        # 5. LEER INCIDENTES
        # -----------------------------------------------------

        incidentes = []

        with open(
            carpeta_datos / "incidentes.csv",
            encoding="utf-8",
            newline="",
        ) as archivo:
            for fila in csv.DictReader(archivo):
                incidentes.append({
                    "id": str(fila["id"]),
                    "nodo": int(fila["nodo"]),
                    "tipo": fila["tipo"],
                })

        # -----------------------------------------------------
        # 6. LEER PARÁMETROS Y RESULTADOS
        # -----------------------------------------------------

        with open(
            carpeta_datos / "parametros.json",
            encoding="utf-8",
        ) as archivo:
            parametros = json.load(archivo)

        with open(
            ruta_resultado,
            encoding="utf-8",
        ) as archivo:
            resultado = json.load(archivo)

        estaciones = resultado["estaciones_seleccionadas"]

        ids_cubiertos = {
            str(identificador)
            for identificador in resultado["incidentes_cubiertos"]
        }

        lotes_usados = {
            str(estacion["lote"])
            for estacion in estaciones
        }

        # -----------------------------------------------------
        # 7. CALCULAR CENTRO Y CREAR MAPA
        # -----------------------------------------------------

        centro = (
            sum(punto[0] for punto in coordenadas.values())
            / len(coordenadas),
            sum(punto[1] for punto in coordenadas.values())
            / len(coordenadas),
        )

        # Se usa CartoDB Positron en lugar de los mosaicos estándar
        # de OpenStreetMap que estaban devolviendo error 403.
        # Crear el mapa sin mosaicos predeterminados.
        mapa = folium.Map(
            location=centro,
            zoom_start=13,
            control_scale=True,
            tiles=None,
        )

        # Agregar Esri World Street Map como mapa base.
        folium.TileLayer(
            tiles=(
                "https://server.arcgisonline.com/ArcGIS/rest/services/"
                "World_Street_Map/MapServer/tile/{z}/{y}/{x}"
            ),
            attr="Tiles © Esri",
            name="Esri World Street Map",
            overlay=False,
            control=True,
        ).add_to(mapa)
        # -----------------------------------------------------
        # 8. LOTES NO UTILIZADOS
        # -----------------------------------------------------

        capa_lotes = folium.FeatureGroup(
            name="Lotes no utilizados",
            show=True,
        )

        for lote in lotes:
            if lote["lote"] in lotes_usados:
                continue

            nodo_lote = lote["nodo"]

            if nodo_lote not in coordenadas:
                continue

            lat, lon = coordenadas[nodo_lote]

            folium.CircleMarker(
                location=(lat, lon),
                radius=6,
                color="gray",
                fill=True,
                fill_color="gray",
                fill_opacity=0.8,
                tooltip=f'Lote no utilizado: {lote["lote"]}',
            ).add_to(capa_lotes)

        capa_lotes.add_to(mapa)

        # -----------------------------------------------------
        # 9. ESTACIONES CONSTRUIDAS Y TABLA
        # -----------------------------------------------------

        capa_estaciones = folium.FeatureGroup(
            name="Estaciones construidas",
            show=True,
        )

        filas_tabla = []

        for estacion in estaciones:
            lote_id = str(estacion["lote"])

            if lote_id not in lotes_por_id:
                print(f"Advertencia: lote desconocido {lote_id}")
                continue

            lote = lotes_por_id[lote_id]
            nodo_lote = lote["nodo"]

            if nodo_lote not in coordenadas:
                print(
                    f"Advertencia: el nodo {nodo_lote} del lote "
                    f"{lote_id} no tiene coordenadas."
                )
                continue

            lat, lon = coordenadas[nodo_lote]

            tipo_original = str(estacion["tipo"])
            tipo_clave = tipo_original.strip().lower()

            if "hurto" in tipo_clave or "cai" in tipo_clave:
                tipo = "hurto"

            elif any(
                palabra in tipo_clave
                for palabra in (
                    "accidente",
                    "tránsito",
                    "transito",
                    "grúa",
                    "grua",
                )
            ):
                tipo = "accidente"

            elif (
                "incendio" in tipo_clave
                or "bombero" in tipo_clave
            ):
                tipo = "incendio"

            else:
                tipo = tipo_clave

            ids_estacion = [
                str(identificador)
                for identificador in estacion["incidentes_cubiertos"]
            ]

            folium.Marker(
                location=(lat, lon),
                tooltip=f"{lote_id}: {tipo_original}",
                popup=(
                    f"<b>Lote:</b> {html.escape(lote_id)}<br>"
                    f"<b>Tipo:</b> {html.escape(tipo_original)}<br>"
                    f"<b>Costo:</b> {estacion['costo']} millones<br>"
                    f"<b>Incidentes cubiertos:</b> {len(ids_estacion)}"
                ),
                icon=folium.Icon(
                    color=colores.get(tipo, "purple"),
                    icon="info-sign",
                ),
            ).add_to(capa_estaciones)

            filas_tabla.append({
                "lote": lote_id,
                "tipo": tipo_original,
                "costo": estacion["costo"],
                "cantidad": len(ids_estacion),
                "ids": ", ".join(
                    sorted(
                        ids_estacion,
                        key=lambda valor: int(valor),
                    )
                ),
            })

        capa_estaciones.add_to(mapa)

        # -----------------------------------------------------
        # 10. INCIDENTES CUBIERTOS Y NO CUBIERTOS
        # -----------------------------------------------------

        capa_cubiertos = folium.FeatureGroup(
            name="Incidentes cubiertos",
            show=True,
        )

        capa_no_cubiertos = folium.FeatureGroup(
            name="Incidentes no cubiertos",
            show=True,
        )

        conteo_tipo = {
            "hurto": 0,
            "accidente": 0,
            "incendio": 0,
        }

        for incidente in incidentes:
            nodo_incidente = incidente["nodo"]

            if nodo_incidente not in coordenadas:
                continue

            lat, lon = coordenadas[nodo_incidente]
            cubierto = incidente["id"] in ids_cubiertos

            tipo_incidente = incidente["tipo"].strip().lower()

            if "hurto" in tipo_incidente:
                tipo_normalizado = "hurto"

            elif "accidente" in tipo_incidente:
                tipo_normalizado = "accidente"

            elif "incendio" in tipo_incidente:
                tipo_normalizado = "incendio"

            else:
                tipo_normalizado = None

            if cubierto and tipo_normalizado is not None:
                conteo_tipo[tipo_normalizado] += 1

            marcador = folium.CircleMarker(
                location=(lat, lon),
                radius=3,
                color="green" if cubierto else "gray",
                fill=True,
                fill_color="green" if cubierto else "gray",
                fill_opacity=0.7,
                popup=(
                    f"<b>Incidente:</b> "
                    f"{html.escape(incidente['id'])}<br>"
                    f"<b>Tipo:</b> "
                    f"{html.escape(incidente['tipo'])}<br>"
                    f"<b>Estado:</b> "
                    f"{'Cubierto' if cubierto else 'No cubierto'}"
                ),
            )

            if cubierto:
                marcador.add_to(capa_cubiertos)

            else:
                marcador.add_to(capa_no_cubiertos)

        capa_cubiertos.add_to(mapa)
        capa_no_cubiertos.add_to(mapa)

        folium.LayerControl(
            collapsed=False
        ).add_to(mapa)

        # -----------------------------------------------------
        # 11. GUARDAR EL MAPA EN UN HTML INDEPENDIENTE
        # -----------------------------------------------------

        ruta_mapa = carpeta_salida / f"mapa_{instancia}.html"

        mapa.save(str(ruta_mapa))

        # -----------------------------------------------------
        # 12. CONSTRUIR TABLA Y RESUMEN
        # -----------------------------------------------------

        filas_html = ""

        for fila in filas_tabla:
            filas_html += f"""
            <tr>
                <td>{html.escape(fila["lote"])}</td>
                <td>{html.escape(fila["tipo"])}</td>
                <td>{fila["costo"]:,}</td>
                <td>{fila["cantidad"]}</td>
                <td class="ids">{html.escape(fila["ids"])}</td>
            </tr>
            """

        presupuesto = parametros.get(
            "presupuesto_millones",
            parametros.get(
                "presupuesto",
                resultado["costo_total"]
                + resultado["presupuesto_restante"],
            ),
        )

        # El iframe carga un archivo local independiente.
        # No se usa data:text/html;base64, por los problemas
        # de carga que se presentaban en mapas grandes.
        nombre_mapa = ruta_mapa.name

        pagina_html = f"""<!DOCTYPE html>
<html lang="es">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Propuesta de estaciones - {html.escape(instancia.title())}</title>

<style>

body {{
    margin: 0;
    font-family: Arial, sans-serif;
    color: #222;
}}

header {{
    background: #17365d;
    color: white;
    padding: 18px 24px;
}}

.tabs {{
    display: flex;
    gap: 8px;
    padding: 12px 20px;
    background: #edf1f5;
}}

button {{
    border: 0;
    padding: 11px 18px;
    cursor: pointer;
    border-radius: 5px;
    font-weight: bold;
}}

button.active {{
    background: #245a86;
    color: white;
}}

.panel {{
    display: none;
    padding: 18px 22px;
}}

.panel.active {{
    display: block;
}}

iframe {{
    display: block;
    width: 100%;
    height: calc(100vh - 175px);
    min-height: 520px;
    border: 1px solid #ccc;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin-top: 18px;
}}

th, td {{
    border: 1px solid #ccc;
    padding: 9px;
    text-align: left;
    vertical-align: top;
}}

th {{
    background: #17365d;
    color: white;
}}

tr:nth-child(even) {{
    background: #f2f2f2;
}}

.ids {{
    max-width: 550px;
    overflow-wrap: anywhere;
}}

.resumen {{
    margin-top: 24px;
    padding: 16px;
    background: #f2f2f2;
    border-radius: 6px;
}}

</style>

</head>

<body>

<header>
    <h1>Propuesta de estaciones: {html.escape(instancia.title())}</h1>
</header>

<div class="tabs">

    <button
        class="active"
        onclick="mostrarPestana('mapa', this)"
    >
        Mapa interactivo
    </button>

    <button
        onclick="mostrarPestana('tabla', this)"
    >
        Tabla de estaciones
    </button>

</div>

<section id="mapa" class="panel active">

    <iframe
        id="mapFrame"
        title="Mapa interactivo"
        src="{html.escape(nombre_mapa, quote=True)}"
    ></iframe>

</section>

<section id="tabla" class="panel">

    <h2>Estaciones seleccionadas</h2>

    <table>

        <thead>
            <tr>
                <th>Lote</th>
                <th>Tipo de estación</th>
                <th>Costo (millones)</th>
                <th>Incidentes cubiertos</th>
                <th>IDs de incidentes</th>
            </tr>
        </thead>

        <tbody>
            {filas_html}
        </tbody>

    </table>

    <div class="resumen">

        <h2>Resumen de la propuesta</h2>

        <p><b>Estaciones construidas:</b> {len(estaciones)}</p>

        <p><b>Costo total:</b> {resultado["costo_total"]:,} millones</p>

        <p><b>Presupuesto:</b> {presupuesto:,} millones</p>

        <p>
            <b>Presupuesto restante:</b>
            {resultado["presupuesto_restante"]:,} millones
        </p>

        <p><b>Valor total:</b> {resultado["valor_total"]}</p>

        <p><b>Incidentes cubiertos:</b> {len(ids_cubiertos)}</p>

        <h3>Incidentes cubiertos por tipo</h3>

        <ul>
            <li>Hurtos: {conteo_tipo["hurto"]}</li>
            <li>Accidentes: {conteo_tipo["accidente"]}</li>
            <li>Incendios: {conteo_tipo["incendio"]}</li>
        </ul>

    </div>

</section>

<script>

function mostrarPestana(nombre, boton) {{

    document.querySelectorAll(".panel").forEach(
        panel => panel.classList.remove("active")
    );

    document.querySelectorAll(".tabs button").forEach(
        tab => tab.classList.remove("active")
    );

    document.getElementById(nombre).classList.add("active");

    boton.classList.add("active");

    if (nombre === "mapa") {{

        setTimeout(() => {{

            const frame = document.getElementById("mapFrame");

            frame.contentWindow.dispatchEvent(
                new Event("resize")
            );

        }}, 150);

    }}

}}

</script>

</body>
</html>
"""

        # -----------------------------------------------------
        # 13. GUARDAR LA PÁGINA PRINCIPAL
        # -----------------------------------------------------

        ruta_html = carpeta_salida / f"{instancia}.html"

        with open(
            ruta_html,
            "w",
            encoding="utf-8",
        ) as archivo:
            archivo.write(pagina_html)

        print(f"\nMapa generado: {ruta_mapa}")
        print(f"Visualización generada: {ruta_html}")

    print("\nProceso de visualización finalizado.")


if __name__ == "__main__":
    main()