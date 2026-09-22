#!/usr/bin/env python3
"""Capturas de pantalla del curso exportado (Chrome headless por CDP), para el README y el historial.

Captura página completa de las páginas más representativas (portada, fundamentos, uso responsable,
marco legal, ejercicios y evaluación) en escritorio, y una en móvil.

Uso:
    python3 herramientas/capturar_pantallas.py            # -> entregables/capturas/rev6/
"""
import asyncio
import base64
import json
import pathlib
import subprocess
import time

import requests
import websockets

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PREVIEW = RAIZ / "entregables" / "html5_preview"
DESTINO = RAIZ / "entregables" / "capturas" / "rev7"
PUERTO = 9334

# (nombre, ruta, ancho, alto, qué desplegar antes de capturar)
#   "acordeon" -> abre la primera sección
#   "respuesta" -> pulsa el botón de retroalimentación de la actividad abierta
PAGINAS = [
    ("01_portada", "index.html", 1280, 900, ""),
    ("02_de_la_ia_al_agente", "html/3-que-es-la-ia-de-la-ia-al-agente.html", 1280, 900, ""),
    ("03_inventario_ia", "html/14-el-inventario-de-ia-de-tu-empresa.html", 1280, 900, ""),
    ("04_sobreexposicion_permisos", "html/18-permisos-sobreexposicion-y-shadow-ai.html",
     1280, 900, "acordeon"),
    # revisión VII: el recuadro de ideas clave, en su sitio y con el CSS propio aplicado
    ("05_recuadro_ideas_clave", "html/19-politica-de-uso-y-protocolo-de-incidentes.html",
     1280, 900, ""),
    # revisión VII: la página de ejercicios, con la respuesta modelo desplegada
    ("06_ejercicios", "html/23-ejercicios-practicos.html", 1280, 900, "respuesta"),
    ("07_evaluacion_final", "html/24-evaluacion-final.html", 1280, 900, ""),
    ("08_portada_movil", "index.html", 420, 900, ""),
]


async def main():
    DESTINO.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        ["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         f"--remote-debugging-port={PUERTO}", "--user-data-dir=/tmp/chrome-capturas"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    ws_url = None
    for _ in range(60):
        try:
            datos = requests.get(f"http://127.0.0.1:{PUERTO}/json/list", timeout=1).json()
            paginas = [d for d in datos if d.get("type") == "page"]
            if paginas:
                ws_url = paginas[0]["webSocketDebuggerUrl"]
                break
        except Exception:
            pass
        time.sleep(0.5)
    if not ws_url:
        raise SystemExit("No se pudo conectar a Chrome por CDP")

    async with websockets.connect(ws_url, max_size=None) as ws:
        contador = {"i": 0}

        async def cmd(metodo, **params):
            contador["i"] += 1
            mid = contador["i"]
            await ws.send(json.dumps({"id": mid, "method": metodo, "params": params}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == mid:
                    return msg

        await cmd("Page.enable")
        for nombre, ruta, ancho, alto, desplegar in PAGINAS:
            await cmd("Emulation.setDeviceMetricsOverride", width=ancho, height=alto,
                      deviceScaleFactor=1, mobile=(ancho < 600))
            await cmd("Page.navigate", url=f"file://{PREVIEW}/{ruta}")
            await asyncio.sleep(2.5)
            # despliega lo que corresponda antes de capturar, para que se vea la interacción
            if desplegar == "acordeon":
                await cmd("Runtime.evaluate", expression="""
                    (() => { const t = document.querySelectorAll('.fx-accordion-title');
                             if (t.length) t[0].click(); return t.length; })()""")
                await asyncio.sleep(1.0)
            elif desplegar == "respuesta":
                await cmd("Runtime.evaluate", expression="""
                    (() => { const b = document.querySelector('input.feedbacktooglebutton');
                             if (b) b.click(); return !!b; })()""")
                await asyncio.sleep(1.2)
            m = await cmd("Page.getLayoutMetrics")
            alto_real = int(m["result"]["cssContentSize"]["height"]) + 40
            ancho_real = int(m["result"]["cssContentSize"]["width"])
            r = await cmd("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                          clip={"x": 0, "y": 0, "width": ancho_real,
                                "height": min(alto_real, 6000), "scale": 1})
            datos = base64.b64decode(r["result"]["data"])
            salida = DESTINO / f"{nombre}.png"
            salida.write_bytes(datos)
            print(f"  {salida.name}: {ancho_real}x{min(alto_real, 6000)} px ({len(datos)//1024} KB)")

    proc.terminate()
    print(f"\nCapturas en {DESTINO}")


asyncio.run(main())
