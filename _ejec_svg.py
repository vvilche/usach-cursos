# -*- coding: utf-8 -*-
"""SVG de la seccion 0 ejecutiva: diagramas propios, en la paleta del curso (cobre).

No duplica el SVG de los 7 subsistemas que ya existe en clase-harness-contabilidad.html:
ese se enlaza. Acá van los que faltan:

  svg_ciclo()      el bucle pensar -> actuar -> observar (Acto 1)
  svg_brecha()     las dos barras que resumen el Acto 1 (88% vs 6%)
  svg_siete()      los 7 subsistemas con la decision de negocio de cada uno (Acto 3b)
  svg_pesos()      las dos palancas: modelo vs harness (Acto 3)

Verificado a ojo: viewBox fijo, sin coordenadas fuera del marco, texto con text-anchor
y sin solapes (el SVG se audita despues con un chequeo de geometria).
"""

C = "#7a2e0e"          # cobre del curso
C2 = "#a16207"         # cobre claro
SOFT = "#fdf3ec"
INK = "#0f172a"
MUT = "#475569"
LINE = "#e2e8f0"
OK = "#0a7a3d"


def svg_ciclo():
    """El ciclo del agente: 4 nodos en circulo con flechas."""
    return '''<svg viewBox="0 0 760 340" role="img" aria-label="El ciclo del agente: objetivo, pensar, actuar, observar, y vuelta al pensar" style="width:100%;height:auto;max-width:760px">
<defs><marker id="fa" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#a16207"/></marker></defs>
<circle cx="380" cy="170" r="112" fill="none" stroke="#e8d5c8" stroke-width="2" stroke-dasharray="6 6"/>
<rect x="300" y="26" width="160" height="58" rx="12" fill="#7a2e0e"/>
<text x="380" y="50" text-anchor="middle" fill="#fff" font-size="15" font-weight="800" font-family="sans-serif">OBJETIVO</text>
<text x="380" y="70" text-anchor="middle" fill="#f0d9c8" font-size="11.5" font-family="sans-serif">qué hay que lograr</text>

<rect x="560" y="141" width="150" height="58" rx="12" fill="#fff" stroke="#7a2e0e" stroke-width="2"/>
<text x="635" y="165" text-anchor="middle" fill="#7a2e0e" font-size="14" font-weight="800" font-family="sans-serif">PENSAR</text>
<text x="635" y="184" text-anchor="middle" fill="#475569" font-size="11.5" font-family="sans-serif">¿qué hago ahora?</text>

<rect x="305" y="256" width="150" height="58" rx="12" fill="#fff" stroke="#0a7a3d" stroke-width="2"/>
<text x="380" y="280" text-anchor="middle" fill="#0a7a3d" font-size="14" font-weight="800" font-family="sans-serif">ACTUAR</text>
<text x="380" y="299" text-anchor="middle" fill="#475569" font-size="11.5" font-family="sans-serif">usar una herramienta</text>

<rect x="50" y="141" width="150" height="58" rx="12" fill="#fff" stroke="#7a2e0e" stroke-width="2"/>
<text x="125" y="165" text-anchor="middle" fill="#7a2e0e" font-size="14" font-weight="800" font-family="sans-serif">OBSERVAR</text>
<text x="125" y="184" text-anchor="middle" fill="#475569" font-size="11.5" font-family="sans-serif">leer el resultado</text>

<path d="M470 84 Q560 105 585 139" fill="none" stroke="#a16207" stroke-width="2.5" marker-end="url(#fa)"/>
<path d="M635 201 Q600 250 460 272" fill="none" stroke="#a16207" stroke-width="2.5" marker-end="url(#fa)"/>
<path d="M303 278 Q180 255 148 203" fill="none" stroke="#a16207" stroke-width="2.5" marker-end="url(#fa)"/>
<path d="M172 139 Q205 100 296 72" fill="none" stroke="#a16207" stroke-width="2.5" marker-end="url(#fa)"/>
<text x="380" y="170" text-anchor="middle" fill="#a16207" font-size="12" font-weight="700" font-family="sans-serif">si no cumple,</text>
<text x="380" y="187" text-anchor="middle" fill="#a16207" font-size="12" font-weight="700" font-family="sans-serif">vuelve a pensar</text>
</svg>'''


def svg_brecha():
    """Las dos barras del Acto 1: uso 88% vs impacto significativo 6%."""
    return '''<svg viewBox="0 0 720 250" role="img" aria-label="88 por ciento de las empresas usa IA, solo 6 por ciento puede atribuirle un impacto significativo" style="width:100%;height:auto;max-width:720px">
<text x="20" y="34" fill="#475569" font-size="13" font-family="sans-serif">Empresas que usan IA en al menos una función</text>
<rect x="20" y="44" width="616" height="40" rx="6" fill="#7a2e0e"/>
<text x="648" y="71" fill="#7a2e0e" font-size="20" font-weight="800" font-family="sans-serif">88%</text>

<text x="20" y="126" fill="#475569" font-size="13" font-family="sans-serif">Empresas que pueden atribuirle 5% o más del resultado y llamarlo significativo</text>
<rect x="20" y="136" width="42" height="40" rx="6" fill="#a16207"/>
<text x="74" y="163" fill="#a16207" font-size="20" font-weight="800" font-family="sans-serif">6%</text>

<line x1="20" y1="200" x2="700" y2="200" stroke="#e2e8f0" stroke-width="1"/>
<text x="20" y="224" fill="#94a3b8" font-size="11.5" font-family="sans-serif">Fuente: McKinsey, gráfico oficial dic-2025 (uso) y Global Survey 2026 (impacto significativo). Medido, no estimado.</text>
</svg>'''


def svg_pesos():
    """Las dos palancas: cambiar el modelo vs cambiar el harness."""
    return '''<svg viewBox="0 0 720 230" role="img" aria-label="Cambiar el modelo mueve 2,5 a 5 puntos; cambiar el harness mueve 13 puntos" style="width:100%;height:auto;max-width:720px">
<text x="20" y="30" fill="#475569" font-size="13.5" font-weight="600" font-family="sans-serif">Cambiar el MODELO (mismos harness)</text>
<rect x="20" y="40" width="120" height="36" rx="6" fill="#cbd5e1"/>
<text x="152" y="65" fill="#475569" font-size="15" font-weight="700" font-family="sans-serif">2,5 a 5 puntos</text>

<text x="20" y="118" fill="#7a2e0e" font-size="13.5" font-weight="600" font-family="sans-serif">Cambiar el HARNESS (mismo modelo)</text>
<rect x="20" y="128" width="312" height="36" rx="6" fill="#7a2e0e"/>
<text x="344" y="153" fill="#7a2e0e" font-size="18" font-weight="800" font-family="sans-serif">13 puntos</text>

<line x1="20" y1="188" x2="700" y2="188" stroke="#e2e8f0" stroke-width="1"/>
<text x="20" y="210" fill="#94a3b8" font-size="11.5" font-family="sans-serif">Medición sobre SWE-bench Verified, 2026. La barra del harness es 2,6 a 5,2 veces más larga: la escala es proporcional al efecto.</text>
</svg>'''


def svg_siete():
    """Los 7 subsistemas con la decision de negocio que abre cada uno."""
    items = [
        ("1", "Bucle", "cuándo sigue solo y cuándo se detiene"),
        ("2", "Modelo conectado", "cuánto cuesta cada tarea"),
        ("3", "Herramientas", "a qué sistemas llega y en qué modo"),
        ("4", "Memoria", "qué papeles de trabajo quedan"),
        ("5", "Seguridad", "qué corre solo y qué pide permiso"),
        ("6", "Orquestación", "si puede crear otros agentes"),
        ("7", "Extensibilidad", "cómo se le agrega capacidad"),
    ]
    filas = []
    y = 22
    for num, nom, dec in items:
        filas.append(f'<rect x="18" y="{y}" width="660" height="46" rx="8" fill="#fff" stroke="#e8d5c8" stroke-width="1.2"/>')
        filas.append(f'<rect x="18" y="{y}" width="46" height="46" rx="8" fill="#7a2e0e"/>')
        filas.append(f'<text x="41" y="{y+29}" text-anchor="middle" fill="#fff" font-size="16" font-weight="800" font-family="sans-serif">{num}</text>')
        filas.append(f'<text x="82" y="{y+22}" fill="#0f172a" font-size="14.5" font-weight="700" font-family="sans-serif">{nom}</text>')
        filas.append(f'<text x="82" y="{y+38}" fill="#475569" font-size="12.5" font-family="sans-serif">{dec}</text>')
        y += 54
    return ('<svg viewBox="0 0 700 402" role="img" aria-label="Los siete subsistemas del harness y la decision de negocio que abre cada uno" '
            'style="width:100%;height:auto;max-width:700px">' + "".join(filas) + '</svg>')
