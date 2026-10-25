#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los 12 decks del curso "IA agentica para ejecutivos" + su plan de clases.

Publico: ejecutivos C-level de empresas grandes (Arauco, Sonepar, ese nivel), no tecnicos.
EJE: no "que es un agente" en abstracto, sino USAR un agente (Hermes y equivalentes)
para el trabajo de un ejecutivo: investigar, decidir, delegar, controlar.

Determinista, cero tokens de LLM. Reusa CSS/deck()/render_slide() de gen_ppts.py para
que la familia visual sea la del sitio.

ADVERTENCIA CONOCIDA: importar gen_ppts EJECUTA su bloque __main__ y reescribe los 25
decks de Auditoria/Innovacion (porque escribe antes del guard). Por eso este generador:
  1. fotografia `git status --porcelain` ANTES del import,
  2. importa,
  3. si el import modifico archivos que no son nuestros, lo dice y sale con error
     (los archivos se restauran con git checkout: son contenido generado, sin trabajo manual).
"""
import hashlib
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

AJENOS = ("auditoria-", "innovacion-", "auditoria-big4")


def git(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def huella_html():
    return {f: hashlib.md5(open(f, "rb").read()).hexdigest()
            for f in os.listdir(".") if f.endswith(".html")}


antes = huella_html()
sys.path.insert(0, BASE)
from gen_ppts import CSS, deck, render_slide  # noqa: E402

from _curso_ejec_clases import CLASES_EJEC  # noqa: E402

# ── control: el import de gen_ppts reescribio decks ajenos? ──
despues = huella_html()
tocados = [f for f in despues
           if despues[f] != antes.get(f) and f.startswith(AJENOS)]
if tocados:
    print("ERROR: el import de gen_ppts reescribio decks que NO son del curso nuevo:")
    for f in tocados:
        print("  ", f)
    print("Restaurando con git checkout (contenido generado, sin trabajo manual):")
    print(git("git checkout -- " + " ".join(tocados)))
    sys.exit(1)

# ── curso ──
EJ = {"nombre": "IA Agéntica para Ejecutivos",
      "short": "IA Agéntica Ejecutivos",
      "color": "#7a2e0e",     # cobre: distinto del verde de Auditoria y el azul de Innovacion
      "soft": "#fdf3ec",
      "level": "Curso ejecutivo",
      "plan": "ejecutivos-ia-agentica.html"}

hechos = 0
for n, titulo, lead, slides in CLASES_EJEC:
    fn = f"ejecutivos-{n:02d}.html"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(deck(EJ, EJ, n, f"Clase {n} de 12", titulo, lead, slides))
    hechos += 1
    print(f"  {fn}  ({len(slides)+1} slides)")

print(f"\n{hechos} decks generados.")
assert hechos == 12, f"esperaba 12 decks, salieron {hechos}"
