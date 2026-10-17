# -*- coding: utf-8 -*-
"""Balancea el quiz de los borradores de tarea y los publica en la raiz del repo.

- Reordena las opciones con CUOTA EXACTA por posicion (N/K). No cambia enunciados,
  ni opciones, ni explicaciones: solo mueve la correcta a su posicion objetivo.
- Copia el archivo a la raiz con el mismo nombre (el enlace no cambia entre
  borrador y version publicada, como dice REVISAR.html).
- Agrega el boton .detalle al plan del electivo en el bloque de cada clase.

Se ejecuta una vez por tanda:  python3 publica_tareas.py 5 6 7
"""
import json
import os
import re
import sys

BORR = "_tareas-borrador/borradores"
PLAN = "innovacion-disruptiva.html"

MAPEO = {
    5: "tarea-innovacion-clase-5-propuesta-de-valor-customer-development.html",
    6: "tarea-innovacion-clase-6-lean-startup-mvp.html",
    7: "tarea-innovacion-clase-7-hito-mitad-presenta-tu-modelo-disruptivo.html",
}


def extrae_qs(txt):
    m = re.search(r"const QS\s*=\s*(\[.*?\n\]);", txt, re.S)
    if not m:
        raise SystemExit("no encontre const QS")
    return m


def js_a_py(bloque):
    """Extrae las preguntas del literal JS sin reinterpretarlo como JSON.

    Formato por pregunta:  q: "...", opts: ["...", ...], ok: N, why: "..."
    Los strings usan comillas dobles; las internas van como «» o \\".
    """
    preguntas = []
    for m in re.finditer(
        r'\{\s*q:\s*"(?P<q>(?:[^"\\]|\\.)*)"\s*,\s*'
        r'opts:\s*\[(?P<opts>(?:[^\[\]]|\[(?:[^\[\]]|\\.)*\])*)\]\s*,\s*'
        r'ok:\s*(?P<ok>\d+)\s*,\s*'
        r'why:\s*"(?P<why>(?:[^"\\]|\\.)*)"\s*\}',
        bloque, re.S,
    ):
        opts = [o for o in re.findall(r'"((?:[^"\\]|\\.)*)"', m.group("opts"))]
        if len(opts) != 4:
            raise SystemExit(f"pregunta con {len(opts)} opciones: {m.group('q')[:50]}")
        preguntas.append(dict(q=m.group("q"), opts=opts, ok=int(m.group("ok")), why=m.group("why")))
    if not preguntas:
        raise SystemExit("no pude extraer preguntas del bloque QS")
    return preguntas


def balancea(qs):
    n, k = len(qs), 4
    objetivo = [i for i in range(k) for _ in range(n // k)]
    while len(objetivo) < n:
        objetivo.append(len(objetivo) % k)
    for q, pos in zip(qs, objetivo):
        opts = list(q["opts"])
        correcta = opts.pop(q["ok"])
        opts.insert(pos, correcta)
        q["ok"] = pos
    return qs


def main(clases):
    for n in clases:
        origen = os.path.join(BORR, MAPEO[n])
        txt = open(origen, encoding="utf-8").read()
        m = extrae_qs(txt)
        # el bloque QS es JS: lo evaluamos como JSON tras normalizar claves
        bloque = m.group(1)
        qs = js_a_py(bloque)
        antes = {p: sum(1 for q in qs if q["ok"] == p) for p in range(4)}
        qs = balancea(qs)
        despues = {p: sum(1 for q in qs if q["ok"] == p) for p in range(4)}
        nuevo = "const QS = " + json.dumps(qs, ensure_ascii=False, indent=2) + ";"
        txt = txt[:m.start()] + nuevo + txt[m.end():]
        assert "@@" not in txt
        destino = MAPEO[n]
        open(destino, "w", encoding="utf-8").write(txt)
        print(f"clase {n}: {destino}")
        print(f"   ok antes {list(antes.values())} -> despues {list(despues.values())} "
              f"| max marca-una-letra {max(despues.values())}/{len(qs)}")
    return 0


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]] or [5, 6, 7]
    sys.exit(main(args))
