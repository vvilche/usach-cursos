#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inyecta: (1) botón 'Ver presentación' en cada clase, (2) sección 'Programa de asignatura'."""
import re

CSS_PPT = ".ppt{display:inline-block;margin-left:10px;font-size:12px;font-weight:700;color:var(--acc);}"
CSS_PROG = ".prog{margin-top:36px;}.progtext{font-size:13.5px;color:var(--mut);margin:6px 0;max-width:860px;}"

PROG_AUD = """<h2 class="prog">Programa de asignatura</h2>
<p class="progtext"><b>Objetivo general:</b> el alumno entiende la IA agéntica y egresa con un sistema de auditoría propio — lector de balances, caza-fraudes SII vs ERP y blindaje cero-alucinación — más portafolio en GitHub.</p>
<p class="progtext"><b>4 niveles:</b> L1 Unboxing Agentic AI · L2 Caza-Fraudes Digital (Ley 21.595) · L3 Armadura Cero Alucinación (spec-kit / Graft / Zod) · L4 Hackathon Swarm UFAS.</p>
<p class="progtext"><b>Stack:</b> spec-kit · Graft · Zod/Pydantic · eve · CrewAI · fastembed + FAISS.</p>
<p class="progtext"><b>Evaluación (aprender &gt; notas):</b> laboratorios en parejas · proyecto capstone · demo/pitch final.</p>
"""

PROG_INN = """<h2 class="prog">Programa de asignatura</h2>
<p class="progtext"><b>Objetivo general:</b> el alumno desarrolla y valida una idea disruptiva — modelo de negocio + evidencia de cliente + pitch NABC.</p>
<p class="progtext"><b>2 fases:</b> F1 diseñar la disrupción (Christensen, Océano Azul, Canvas, patrones, value prop, lean) · F2 escalar y vender (portafolio, design thinking, lead users, NABC, pitch).</p>
<p class="progtext"><b>Evaluación (aprender &gt; notas):</b> ejercicios en parejas · presentaciones intermedias · pitch final.</p>
"""

def inject(curso_key, filename, n_clases, proghtml, anchor):
    with open(filename, encoding="utf-8") as f:
        h = f.read()
    # CSS
    h = h.replace("a:hover{text-decoration:underline;}",
                  "a:hover{text-decoration:underline;}\n  " + CSS_PPT + "\n  " + CSS_PROG)
    # PPT links
    fechas = list(re.finditer(r'<div class="fecha">[^<]*</div>', h))
    assert len(fechas) == n_clases, f"{filename}: {len(fechas)} fechas, esperaba {n_clases}"
    off = 0
    for i, m in enumerate(fechas, 1):
        link = f'<a class="ppt" href="{curso_key}-{i:02d}.html">Ver presentación →</a>'
        pos = m.end() + off
        h = h[:pos] + link + h[pos:]
        off += len(link)
    # Programa section
    assert anchor in h, f"{filename}: ancla no encontrada"
    h = h.replace(anchor, proghtml + anchor, 1)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(h)
    print(f"  {filename}: {n_clases} links + programa OK")

inject("auditoria", "auditoria-ia-agentica.html", 13, PROG_AUD, '<div class="nivel">LEVEL 1')
inject("innovacion", "innovacion-disruptiva.html", 12, PROG_INN, '<div class="fase">FASE 1')
print("listo")
