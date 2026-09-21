#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte los links 'Ver presentación' en decks EMBEBIDOS (details + iframe) dentro de la página."""
import re

CSS_DECK = """
.deck{margin-top:12px;}
.deck summary{cursor:pointer;display:inline-block;background:var(--acc2);color:#fff;padding:9px 18px;border-radius:8px;font-weight:700;font-size:13px;list-style:none;user-select:none;}
.deck summary::-webkit-details-marker{display:none;}
.deck summary:hover{opacity:.9;}
.deck iframe{display:block;width:100%;height:560px;border:1px solid var(--line);border-radius:10px;margin-top:12px;background:#fff;}
"""

def embed(filename, key, color_var):
    with open(filename, encoding="utf-8") as f:
        h = f.read()
    # reemplazar cada <a class="ppt" href="KEY-NN.html">Ver presentación →</a>
    pat = re.compile(r'<a class="ppt" href="%s-\d+\.html">Ver presentación →</a>' % key)
    def repl(m):
        n = re.search(r'%s-(\d+)\.html' % key, m.group(0)).group(1)
        return (f'<details class="deck"><summary>▶ Ver presentación</summary>'
                f'<iframe loading="lazy" src="{key}-{n}.html" title="Clase {n}"></iframe></details>')
    h2, cnt = pat.subn(repl, h)
    assert cnt > 0, f"{filename}: no se encontraron links .ppt"
    # color del botón según el curso (--acc2 en auditoría, --acc en innovación)
    css = CSS_DECK.replace("var(--acc2)", color_var)
    # inyectar CSS .deck
    if ".deck{margin-top" not in h2:
        h2 = h2.replace("a:hover{text-decoration:underline;}", "a:hover{text-decoration:underline;}\n" + css)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(h2)
    print(f"  {filename}: {cnt} decks embebidos")

embed("auditoria-ia-agentica.html", "auditoria", "var(--acc2)")
embed("innovacion-disruptiva.html", "innovacion", "var(--acc)")
print("listo")
