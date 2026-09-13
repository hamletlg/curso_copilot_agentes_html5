#!/usr/bin/env python3
"""Prueba de interacción del curso exportado (CDP contra Chrome headless).

 1) Acordeón (página 7): clic en la sección 1 y comprobación de que el contenido se despliega.
 2) Cuestionario (página 24): iniciar, leer la primera pregunta, responder la opción correcta
    y comprobar que aparece el feedback.
"""
import asyncio
import json
import subprocess
import time

import requests
import websockets

BASE = "file:///mnt/DATA/trabajo_hermes/articulate_hermes/entregables/html5_preview/"
PUERTO = 9333
fallos = []


def check(nombre, cond, detalle=""):
    print(f"  [{'OK  ' if cond else 'FALLO'}] {nombre}" + (f" -> {detalle}" if detalle else ""))
    if not cond:
        fallos.append(nombre)


async def main():
    proc = subprocess.Popen(
        ["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
         f"--remote-debugging-port={PUERTO}", "--user-data-dir=/tmp/chrome-cdp2"],
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

        async def js(expr):
            r = await cmd("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
            try:
                return r["result"]["result"].get("value")
            except Exception:
                return f"ERROR: {json.dumps(r)[:200]}"

        async def ir(url, espera=3.0):
            await cmd("Page.navigate", url=BASE + url)
            await asyncio.sleep(espera)

        await cmd("Page.enable")
        await cmd("Runtime.enable")

        print("=== 0) UN SOLO BLOQUE POR PÁGINA, SIN ETIQUETA «Texto» ===")
        for pagina, esperado in (("html/13-crear-tu-propio-agente-con-agent-builder.html", 1),
                                 ("html/7-los-5-componentes-del-agente.html", 1),
                                 ("html/24-evaluacion-final.html", 1)):
            await ir(pagina)
            d0 = json.loads(await js("""(() => {
                const cajas = document.querySelectorAll('article.box');
                return JSON.stringify({cajas: cajas.length,
                    titulos: document.querySelectorAll('.box-title').length,
                    sinCabecera: document.querySelectorAll('article.box.no-header').length,
                    cajasDeTexto: document.querySelectorAll('.exe-text').length,
                    menuActivo: (document.querySelector('#siteNav a.active') || {}).textContent});
            })()"""))
            check(f"{pagina}: {esperado} bloque", d0["cajas"] == esperado, f"cajas={d0['cajas']}")
            check(f"{pagina}: sin titulo «Texto»", d0["titulos"] == 0, f"titulos={d0['titulos']}")
            print(f"     menu activo: {str(d0['menuActivo']).strip()!r}")

        print("\n=== 0b) NAVEGACIÓN «ANTERIOR / SIGUIENTE» AL PIE ===")
        await ir("html/13-crear-tu-propio-agente-con-agent-builder.html")
        dn = json.loads(await js("""(() => {
            const caja = document.querySelector('.nav-buttons');
            const der = document.querySelector('.nav-buttons .nav-button-right');
            const izq = document.querySelector('.nav-buttons .nav-button-left');
            const main = document.querySelector('main.page');
            const cont = document.querySelector('.page-content');
            const r = e => { const x = e.getBoundingClientRect();
                return {top: Math.round(x.top + window.scrollY), bottom: Math.round(x.bottom + window.scrollY),
                        left: Math.round(x.left), right: Math.round(x.right)}; };
            if (!caja || !der || !izq) return JSON.stringify({falta: true});
            return JSON.stringify({
                falta: false, dentroDeMain: main.contains(caja),
                posDer: getComputedStyle(der).position,
                caja: r(caja), texto: r(cont),
                etiquetas: [izq.textContent.trim(), der.textContent.trim()],
                hrefDer: der.getAttribute('href'),
                anchoDer: Math.round(der.getBoundingClientRect().width)});
        })()"""))
        if dn.get("falta"):
            check("nav: bloque .nav-buttons presente", False)
        else:
            check("nav: el bloque vive dentro de <main> (hereda la maquetación del tema)", dn["dentroDeMain"])
            check("nav: ya no está fijo arriba (position: static)", dn["posDer"] == "static", dn["posDer"])
            check("nav: misma caja que la columna de texto",
                  abs(dn["caja"]["left"] - dn["texto"]["left"]) <= 1
                  and abs((dn["caja"]["right"] - dn["caja"]["left"])
                          - (dn["texto"]["right"] - dn["texto"]["left"])) <= 1,
                  f'caja={dn["caja"]} texto={dn["texto"]}')
            check("nav: va después del contenido (al pie)",
                  dn["caja"]["top"] >= dn["texto"]["bottom"],
                  f'top={dn["caja"]["top"]} vs fin del texto={dn["texto"]["bottom"]}')
            check("nav: Anterior/Siguiente con sus etiquetas",
                  dn["etiquetas"] == ["Anterior", "Siguiente"], str(dn["etiquetas"]))
            check("nav: «Siguiente» apunta a la página siguiente",
                  (dn["hrefDer"] or "").endswith("14-el-inventario-de-ia-de-tu-empresa.html"),
                  dn["hrefDer"] or "")
        await js("window.scrollTo(0, document.documentElement.scrollHeight)")
        await asyncio.sleep(0.8)
        d2 = json.loads(await js("""(() => {
            const b = document.querySelector('.nav-buttons .nav-button-right');
            const x = b.getBoundingClientRect();
            return JSON.stringify({visible: x.top >= 0 && x.bottom <= window.innerHeight,
                margenInferior: Math.round(window.innerHeight - x.bottom),
                scrollY: Math.round(window.scrollY)});
        })()"""))
        check("nav: visible al llegar al final de la página (sin scroll up)",
              d2["visible"], f'margen inferior={d2["margenInferior"]}px, scrollY={d2["scrollY"]}')

        print("\n=== 0c) PORTADA: TEXTO SOBRE LA IMAGEN (OVERLAY) ===")
        PORTADA_JS = """(() => {
            const img = document.querySelector('.portada > img');
            const t = document.querySelector('.portada-texto');
            const tit = document.querySelector('.portada-titulo');
            if (!img || !t || !tit) return JSON.stringify({falta: true});
            const ri = img.getBoundingClientRect(), rt = t.getBoundingClientRect();
            return JSON.stringify({falta: false, alt: img.getAttribute('alt') || '',
                modo: getComputedStyle(t).position === 'absolute' ? 'overlay' : 'debajo',
                colorTitulo: getComputedStyle(tit).color,
                sombra: getComputedStyle(tit).textShadow,
                columna: Math.round(document.querySelector('.portada').getBoundingClientRect().width),
                dentro: Math.round(rt.top - ri.top) >= 0 && Math.round(ri.bottom - rt.bottom) >= -1,
                desborda: rt.height > ri.height + 2});
        })()"""
        for etiqueta, w, h, esperado in (("escritorio 1280", 1280, 900, "overlay"),
                                         ("movil 420", 420, 900, "debajo")):
            await cmd("Emulation.setDeviceMetricsOverride", width=w, height=h,
                      deviceScaleFactor=1, mobile=False)
            await ir("index.html", 3.0)
            dp = json.loads(await js(PORTADA_JS))
            if dp.get("falta"):
                check(f"portada ({etiqueta}): estructura .portada presente", False)
                continue
            check(f"portada ({etiqueta}, columna {dp['columna']}px): modo {esperado}",
                  dp["modo"] == esperado, dp["modo"])
            check(f"portada ({etiqueta}): texto alternativo de la imagen",
                  len(dp["alt"]) > 30, dp["alt"][:40])
            if esperado == "overlay":
                check(f"portada ({etiqueta}): sombra en el título (sobre la foto)",
                      "rgb" in (dp["sombra"] or ""), (dp["sombra"] or "")[:60])
                check(f"portada ({etiqueta}): el texto cabe dentro de la imagen",
                      dp["dentro"] and not dp["desborda"])
                check(f"portada ({etiqueta}): título en blanco sobre el degradado",
                      dp["colorTitulo"] == "rgb(255, 255, 255)", dp["colorTitulo"])
            else:
                check(f"portada ({etiqueta}): sin sombra (texto sobre fondo claro)",
                      (dp["sombra"] or "none") == "none", (dp["sombra"] or "")[:40])
                check(f"portada ({etiqueta}): título en color oscuro (texto debajo)",
                      dp["colorTitulo"] not in ("rgb(255, 255, 255)",), dp["colorTitulo"])
        await cmd("Emulation.setDeviceMetricsOverride", width=1280, height=900,
                  deviceScaleFactor=1, mobile=False)

        print("\n=== 1) ACORDEÓN (página 7: los 5 componentes) ===")
        await ir("html/7-los-5-componentes-del-agente.html")
        antes = await js("""(() => {
            const c = document.querySelectorAll('.fx-accordion-content');
            const t = document.querySelectorAll('.fx-accordion-title');
            return JSON.stringify({titulos: t.length, contenidos: c.length,
                alturas: Array.from(c).map(x => x.offsetHeight),
                href: t[0] ? t[0].getAttribute('href') : null});
        })()""")
        print("  antes:", antes)
        await js("document.querySelectorAll('.fx-accordion-title')[0].click()")
        await asyncio.sleep(1.2)
        d1 = json.loads(await js("""(() => {
            const c = document.querySelectorAll('.fx-accordion-content');
            const t = document.querySelectorAll('.fx-accordion-title');
            return JSON.stringify({alturas: Array.from(c).map(x => x.offsetHeight),
                texto: (c[0].textContent || '').trim().slice(0, 70),
                activo: t[0].classList.contains('active')});
        })()"""))
        check("acordeón: se despliega la sección 1", d1["alturas"][0] > 0, f"alturas={d1['alturas']}")
        check("acordeón: marcada como activa", d1["activo"])
        print(f"     contenido visible: {d1['texto']!r}")
        await js("document.querySelectorAll('.fx-accordion-title')[0].click()")
        await asyncio.sleep(1.2)
        d2 = json.loads(await js("""(() => { const c = document.querySelectorAll('.fx-accordion-content');
            return JSON.stringify({alturas: Array.from(c).map(x => x.offsetHeight)}); })()"""))
        check("acordeón: se vuelve a plegar al segundo clic", d2["alturas"][0] == 0, f"alturas={d2['alturas']}")

        print("\n=== 2) CUESTIONARIO (página 24) ===")
        await ir("html/24-evaluacion-final.html", 4.0)
        await js("""(() => {
            const c = Array.from(document.querySelectorAll('a,button,div,span,p'))
                .filter(e => /Pulse aquí para jugar/i.test(e.textContent || '') && e.offsetParent !== null);
            c[c.length-1].click();
        })()""")
        await asyncio.sleep(2.5)
        p1 = json.loads(await js("""(() => {
            const q = document.querySelector('.QXTP-Question');
            const ops = Array.from(document.querySelectorAll('[class^=QXTP-Option]:not([class*=Div])'))
                .filter(e => e.offsetParent !== null);
            return JSON.stringify({pregunta: q ? q.textContent.trim().slice(0,110) : null,
                n: ops.length, opciones: ops.map(o => o.textContent.trim().replace(/\\s+/g,' ').slice(0,55))});
        })()"""))
        check("cuestionario: carga la primera pregunta", bool(p1["pregunta"]), p1["pregunta"] or "")
        check("cuestionario: 4 opciones visibles", p1["n"] == 4, f"{p1['n']}")
        for o in p1["opciones"]:
            print(f"     - {o}")

        # responde la opción correcta de la P1 (b = índice 1, orden fijo)
        await js("""(() => {
            const ops = Array.from(document.querySelectorAll('[class^=QXTP-Option]:not([class*=Div])'))
                .filter(e => e.offsetParent !== null);
            ops[1].click();
        })()""")
        await asyncio.sleep(2.0)
        r1 = json.loads(await js("""(() => {
            const html = document.body.innerHTML;
            const score = document.querySelector('.QXTP-GameScores, .QXTP-DataScore');
            const q = document.querySelector('.QXTP-Question');
            return JSON.stringify({
                feedbackOk: html.includes('Has entendido el concepto')
                            || html.includes('Repasa el contenido del nodo'),
                marcador: score ? score.textContent.trim().replace(/\\s+/g,' ').slice(0,60) : null,
                siguiente: q ? q.textContent.trim().slice(0,80) : null});
        })()"""))
        check("cuestionario: aplica el feedback por pregunta", r1["feedbackOk"])
        check("cuestionario: registra el acierto", "Aciertos: 1" in (r1["marcador"] or ""), r1["marcador"] or "")
        print(f"     marcador: {r1['marcador']!r}")
        print(f"     siguiente pregunta: {r1['siguiente']!r}")

    proc.terminate()
    print("\n" + ("INTERACCIONES OK" if not fallos else f"FALLOS: {fallos}"))


asyncio.run(main())
