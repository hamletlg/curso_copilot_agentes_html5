#!/usr/bin/env python3
"""Extrae componentes de un content.xml real de eXeLearning (v3/v4) y muestra su estructura.

Utilidad de apoyo al montaje: los paquetes oficiales de ejemplo traen un componente real de
CADA tipo de iDevice, con el estado interno exacto (htmlView + jsonProperties). Sirve para
copiar la estructura correcta al generar el paquete del curso por código.

Los paquetes de ejemplo se descargan del repositorio oficial, por ejemplo:

  curl -sLO https://raw.githubusercontent.com/exelearning/exelearning/main/test/fixtures/todos-los-idevices_dos_informes.elpx
  unzip -o todos-los-idevices_dos_informes.elpx content.xml -d fixture

Uso:
  python3 extraer_componentes_elpx.py <content.xml> [tipos_separados_por_coma] [salida.txt]

Ejemplo:
  python3 extraer_componentes_elpx.py fixture/content.xml quick-questions,text

Notas:
  - Los iDevices de tipo juego/cuestionario guardan su estado en un <div class="...DataGame js-hidden">
    codificado: XOR de cada carácter con la clave 146 y despues escape() (percent-encoding).
    Ver /app/public/app/common/common.js (función encrypt) dentro del contenedor.
  - El resto de iDevices usan JSON normal en <jsonProperties> (patrón «Standard JSON»).
"""
import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

NS = "{http://www.intef.es/xsd/ode}"
XOR_KEY = 146


def xor_decode(payload: str) -> str:
    """Deshace el 'cifrado' de los iDevices de juego: escape() + XOR 146."""
    raw = urllib.parse.unquote_to_bytes(payload)
    return "".join(chr(b ^ XOR_KEY) for b in raw)


def txt(el, tag):
    e = el.find(NS + tag)
    return (e.text or "") if e is not None else None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    path = sys.argv[1]
    tipos = sys.argv[2].split(",") if len(sys.argv) > 2 else ["quick-questions"]
    out = open(sys.argv[3], "w", encoding="utf-8") if len(sys.argv) > 3 else sys.stdout

    root = ET.parse(path).getroot()
    for comp in root.iter(NS + "odeComponent"):
        tipo = txt(comp, "odeIdeviceTypeName") or ""
        if tipo not in tipos:
            continue
        print("=" * 78, file=out)
        print("TIPO:", tipo, file=out)
        ids = {t: txt(comp, t) for t in ("odePageId", "odeBlockId", "odeIdeviceId", "odeComponentsOrder")}
        print("IDS:", ids, file=out)

        jp = txt(comp, "jsonProperties") or ""
        if jp:
            try:
                d = json.loads(jp)
                print("claves jsonProperties:", sorted(d.keys()), file=out)
                for k, v in d.items():
                    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
                    if isinstance(s, str) and len(s) < 300:
                        print(f"   {k} = {s}", file=out)
                    else:
                        print(f"   {k}: len={len(s)}", file=out)
            except Exception as e:
                print("!! jsonProperties no es JSON válido:", e, file=out)

        hv = txt(comp, "htmlView") or ""
        print(f"htmlView: {len(hv)} caracteres", file=out)
        for m in re.finditer(r'<div class="([^"]*DataGame[^"]*)"[^>]*>([^<]*)</div>', hv):
            dec = xor_decode(m.group(2))
            print(f"--- DataGame '{m.group(1)}' | codificado={len(m.group(2))} | claro={len(dec)}", file=out)
            try:
                print(json.dumps(json.loads(dec), ensure_ascii=False, indent=1)[:8000], file=out)
            except Exception as e:
                print("NO JSON:", e, dec[:800], file=out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
