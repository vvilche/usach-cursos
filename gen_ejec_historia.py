#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la seccion 0 del curso ejecutivo:

  ejecutivos-00a.html .. ejecutivos-00e.html   los 5 actos de la historia (decks)
  ejecutivos-glosario.html                     glosario de datos para no tecnicos
  ejecutivos-timeline.html                     linea de tiempo 2022 -> 2026

Determinista, cero tokens de LLM. Reusa CSS/deck() de gen_ppts.py.
El import de gen_ppts reescribe los decks ajenos (trampa conocida); se verifica y se
restaura si toco algo que no es nuestro.
"""
import hashlib
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
AJENOS = ("auditoria-", "innovacion-", "auditoria-big4", "ejecutivos-0", "ejecutivos-glosario", "ejecutivos-timeline")


def huella():
    return {f: hashlib.md5(open(f, "rb").read()).hexdigest()
            for f in os.listdir(".") if f.endswith(".html")}


antes = huella()
sys.path.insert(0, BASE)
import gen_ppts  # noqa: E402
from gen_ppts import CSS, deck  # noqa: E402
render_slide = gen_ppts.render_slide  # referencia al original, para el fallback
from _curso_ejec_historia import HISTORIA  # noqa: E402

despues = huella()
tocados = [f for f in despues if despues[f] != antes.get(f) and f.startswith(AJENOS)]
if tocados:
    print("ERROR: gen_ppts reescribio decks ajenos:", tocados)
    subprocess.run("git checkout -- " + " ".join(tocados), shell=True)
    sys.exit(1)


CSS_FIG = """
.fig{background:#fff;border:1px solid #e8d5c8;border-radius:12px;padding:10px 14px;display:flex;justify-content:center;}
.tw{overflow-x:auto;margin:0;}
table{border-collapse:collapse;width:100%;font-size:14.5px;background:#fff;}
th,td{border:1px solid #e2e8f0;padding:9px 12px;text-align:left;vertical-align:top;}
th{background:#fdf3ec;color:#7a2e0e;font-size:13.5px;}
tbody tr:nth-child(even){background:#fcfdfe;}
"""


# ── tipos de slide propios: svg crudo y tabla ────────────────────────────────
# render_slide de gen_ppts escapa todo el contenido; para un diagrama y una tabla
# necesitamos HTML crudo. No se toca gen_ppts: se envuelve.
_render_base = render_slide


def esc_(s):
    import html as _h
    return _h.escape(str(s), quote=True)


def render_slide(s):
    k, w = s[0], s[1]
    if k == "svg":
        kick = f'<div class="kicker">{esc_(w.get("kicker",""))}</div>' if w.get("kicker") else ""
        h2 = f'<h2>{esc_(w["h2"])}</h2>' if w.get("h2") else ""
        cap = f'<p class="meta">{esc_(w["cap"])}</p>' if w.get("cap") else ""
        return f'<section class="slide">{kick}{h2}<div class="fig">{w["svg"]}</div>{cap}</section>'
    if k == "tabla":
        kick = f'<div class="kicker">{esc_(w.get("kicker",""))}</div>' if w.get("kicker") else ""
        h2 = f'<h2>{esc_(w["h2"])}</h2>' if w.get("h2") else ""
        head = "".join(f"<th>{esc_(c)}</th>" for c in w["cols"])
        filas = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in w["rows"])
        cap = f'<p class="meta">{esc_(w["cap"])}</p>' if w.get("cap") else ""
        return (f'<section class="slide">{kick}{h2}<div class="tw"><table><thead><tr>{head}</tr></thead>'
                f'<tbody>{filas}</tbody></table></div>{cap}</section>')
    return _render_base(s)


# deck() llama a gen_ppts.render_slide (su global), no a la nuestra: se la reemplazamos.
# Es un monkeypatch local al proceso de generacion; no toca gen_ppts.py en disco.
gen_ppts.render_slide = render_slide

EJ = {"nombre": "IA Agéntica para Ejecutivos",
      "short": "Sección 0 · La historia",
      "color": "#7a2e0e", "soft": "#fdf3ec",
      "level": "Sección 0 · Historia",
      "plan": "ejecutivos-ia-agentica.html"}

# sufijo de archivo por acto: el 3b entra entre el 3 y el 4 sin renumerar los ya publicados
SUFIJOS = {1: "a", 2: "b", 3: "c", 4: "cb", 5: "d", 6: "e"}
ACTOS = ["La promesa", "La guerra de los agentes", "El harness", "La arquitectura agéntica",
         "Lo nuestro", "El horizonte"]
hechos = 0
for n, titulo, lead, slides in HISTORIA:
    suf = SUFIJOS[n]
    etiqueta = "3b" if n == 4 else str(n)
    fn = f"ejecutivos-00{suf}.html"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(deck(EJ, EJ, f"0.{etiqueta}", f"Sección 0 · Acto {etiqueta} de 6", titulo, lead, slides)
                  .replace("</style>", CSS_FIG + "</style>"))
    hechos += 1
    print(f"  {fn}  Acto {etiqueta} · {ACTOS[n-1]}  ({len(slides)+1} slides)")
assert hechos == 6, hechos

# ══════════════════════════════════════════════════ GLOSARIO
GLOSARIO = [
 ("Agente", "Un programa que recibe un objetivo, decide por sí mismo qué hacer, usa herramientas y ejecuta hasta cumplirlo. La diferencia con un chatbot es quién hace el trabajo: con el chatbot eres tú; con el agente, es la máquina y tú revisas.",
  "No es 'una IA más inteligente'. Es una IA conectada a herramientas y con permiso para actuar."),
 ("Modelo", "El motor: la red entrenada que produce texto, cálculos y decisiones. Es una pieza, no el sistema completo. Se cambia sin rehacer el trabajo.",
  "Cuando alguien dice 'usamos GPT' o 'usamos Claude', está hablando del motor, no del auto."),
 ("Harness", "El auto completo alrededor del motor: el ciclo de trabajo, las herramientas que le da, la memoria que le entrega, los límites que le pone y cómo se extiende. Pesa más que el modelo: cambiar de harness mueve 13 puntos el resultado; cambiar de modelo, 2,5 a 5.",
  "Palabra en inglés, sin traducción de uso. En el curso se explica con la analogía motor / auto."),
 ("Herramienta", "Lo que el agente puede hacer en el mundo: leer un archivo, consultar un sistema, buscar en internet, hacer un cálculo. Sin herramientas, un agente es solo un chat.",
  "La pregunta de compra correcta: ¿a qué sistemas de la empresa puede llegar y en qué modo (leer o escribir)?"),
 ("Memoria", "Lo que el agente conserva entre una sesión y otra: quién eres, cómo se llaman las cosas en tu empresa, qué se decidió. Es lo que separa una consulta suelta de un colaborador.",
  "La regla sana: en memoria, los hechos estables; los procedimientos complejos van aparte."),
 ("Regla de comportamiento", "Un archivo de instrucciones propias que el agente lee en cada sesión: qué verificar, qué no afirmar, cuándo pedir permiso. Es lo que convierte un agente en uno auditable.",
  "En Hermes vive en un archivo llamado SOUL. Sin reglas, el agente inventa — es exactamente lo contrario de lo que pide un comité de riesgo."),
 ("Trazabilidad", "Poder responder, para cada cifra de un entregable, de qué archivo salió, en qué línea está y qué cálculo se aplicó. Si la cadena se corta, el número no es un dato: es una afirmación.",
  "Es el mismo principio de la contabilidad y de la auditoría, aplicado a una herramienta nueva."),
 ("Alucinación", "Un dato inventado que el sistema entrega con seguridad total, porque su trabajo es producir la continuación más plausible y no decir 'no sé'.",
  "No se elimina: se controla. Con fuente obligatoria, extractor determinista, verificación cruzada y muestra humana."),
 ("Memoria documental de la empresa", "El conocimiento disperso en carpetas, actas, contratos y correos, puesto a disposición del agente para que consulte cuando la tarea lo pide, en vez de tenerlo todo cargado siempre.",
  "El proveedor probablemente lo llame 'solución de conocimiento empresarial'. Da igual el nombre: el concepto es éste, y el ejecutivo necesita el concepto, no la sigla."),
 ("Puente, no copia", "El agente consulta la fuente original (el ERP, el sistema, el archivo oficial) en vez de trabajar sobre una copia propia. Si existe una copia, al día siguiente dos números compiten y nadie sabe cuál gana.",
  "Es la regla que evita el clásico 'la planilla dice una cosa y el sistema otra'."),
 ("Irreversible", "El criterio que ordena los permisos de un agente. Reversible: leer, calcular, preparar un borrador — lo hace solo. Irreversible: enviar un correo, modificar un registro, publicar, pagar — pide aprobación.",
  "No es un criterio de tamaño, es de si se puede deshacer. Ahí se decide qué puede hacer el agente sin que nadie mire."),
 ("Registro", "Queda escrito lo que el agente hizo, con qué fuente y cuándo. Sin registro no hay auditoría posible: solo confianza.",
  "La pregunta que hay que responder antes de conectar un agente: ¿dónde queda el registro y quién lo revisa?"),
 ("Perfil", "Una separación del agente y su información: el perfil de una persona o de un área, aislado del resto. Se usa para que lo delicado no comparta espacio con el trabajo general.",
  "Resuelve el 80% de las conversaciones de seguridad sin comprar nada nuevo."),
 ("Evaluación", "Medir si el agente cumple: contra casos conocidos, no contra una impresión. Es la diferencia entre 'funciona' y 'funciona en este caso'.",
  "En el curso se hace con la muestra humana: una cifra al azar contra el original, en cada entrega."),
]

def glosario_html():
    items = "\n".join(
        f'''  <div class="g" id="g{i}">
    <div class="gt">{t}</div>
    <div class="gd">{d}</div>
    <div class="gn"><b>Por qué importa:</b> {n}</div>
  </div>''' for i, (t, d, n) in enumerate(GLOSARIO, 1))
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glosario de datos — IA Agéntica para Ejecutivos</title>
<style>
:root{{--bg:#f8fafc;--card:#fff;--ink:#0f172a;--mut:#475569;--line:#e2e8f0;--acc:#7a2e0e;--soft:#fdf3ec;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}}
.wrap{{max-width:900px;margin:0 auto;padding:32px 22px 90px;}}
header{{border-bottom:2px solid var(--acc);padding-bottom:18px;margin-bottom:8px;}}
h1{{font-size:28px;margin:0 0 6px;letter-spacing:-.02em;}}
.sub{{color:var(--mut);font-size:14px;margin:0;}}
.aviso{{background:var(--soft);border:1px solid #f0d9c8;border-left:5px solid var(--acc);border-radius:10px;padding:14px 18px;font-size:14.5px;color:#5b2b14;margin:20px 0 8px;}}
.buscador{{margin:22px 0 6px;}}
.buscador input{{width:100%;padding:12px 14px;font-size:16px;border:1px solid var(--line);border-radius:10px;background:#fff;}}
.g{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 22px;margin:12px 0;border-left:4px solid var(--acc);}}
.gt{{font-weight:800;font-size:18px;color:var(--acc);margin-bottom:6px;}}
.gd{{font-size:15.5px;color:var(--ink);}}
.gn{{font-size:14px;color:var(--mut);margin-top:10px;padding-top:10px;border-top:1px dashed var(--line);}}
.gn b{{color:var(--acc);}}
a{{color:#2563eb;}}
footer{{margin-top:40px;padding-top:14px;border-top:1px solid var(--line);color:var(--mut);font-size:13px;}}
</style></head>
<body><div class="wrap">
<header>
  <h1>Glosario de datos</h1>
  <p class="sub">Los {len(GLOSARIO)} conceptos que un ejecutivo necesita para autorizar, comprar o frenar un proyecto de IA agéntica · Sección 0 del curso</p>
</header>
<div class="aviso"><b>Por qué existe:</b> el mismo concepto tiene tres nombres —el de la industria en inglés, el del proveedor y el de la jerga interna— y esas diferencias se cobran en las reuniones. Acá va cada uno con su definición operativa y con la razón por la que le importa a quien decide.</div>
<div class="buscador"><input id="q" type="search" placeholder="Buscar un concepto (por ejemplo: trazabilidad, permiso, memoria)…" aria-label="Buscar concepto"></div>
{items}
<footer>
  <a href="ejecutivos-ia-agentica.html">← Volver al plan de clases</a> ·
  <a href="ejecutivos-timeline.html">La línea de tiempo 2022–2026 →</a> ·
  Fuente de las definiciones: el material del curso y las fuentes citadas en cada acto de la sección 0.
</footer>
</div>
<script>
const q=document.getElementById('q');
const gs=[...document.querySelectorAll('.g')];
const norm=s=>s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
q.addEventListener('input',()=>{{
  const v=norm(q.value.trim());
  gs.forEach(g=>{{g.style.display = !v || norm(g.textContent).includes(v) ? '' : 'none';}});
  const vis=gs.filter(g=>g.style.display!=='none').length;
  q.setAttribute('aria-label','Buscar concepto — '+vis+' de '+gs.length+' visibles');
}});
</script>
</body></html>'''


# ══════════════════════════════════════════════════ TIMELINE
HITOS = [
 ("2022", "nov", "Llega ChatGPT", "La IA generativa entra a la conversación de las empresas. Todos los directorios preguntan por ella.", ""),
 ("2023", "todo", "Primera ola de adopción", "Licencias, capacitaciones, chatbots internos. La métrica es 'cuántas personas lo usan'.", ""),
 ("2024", "todo", "La decepción", "Los pilotos no llegan al resultado. El diagnóstico de moda: 'el modelo todavía no es suficientemente bueno'. Es falso.", ""),
 ("2025", "jun-jul", "Encuesta que fija la escala", "1.993 respondentes: 88% de las empresas usa IA en al menos una función. Solo 7% dice haberla escalado del todo.", ""),
 ("2025", "ago", "El dato incómodo", "Un estudio del MIT encuentra que 95% de los pilotos de IA generativa no llegó a demostrar retorno.", "https://www.salesforce.com/news/stories/why-ai-pilots-fail/"),
 ("2025", "nov", "Nace Clawdbot", "Un desarrollador austríaco publica un asistente personal que corre en el computador y obedece desde WhatsApp. Se hace viral.", "https://techcrunch.com/2026/01/30/openclaws-ai-assistants-are-now-building-their-own-social-network"),
 ("2025", "dic", "El gráfico del 88%", "McKinsey publica la serie de adopción: 20% en 2017 → 88% en 2025. Y solo 7% con despliegue completo.", "https://www.mckinsey.com/featured-insights/charts/ai-at-work-but-not-at-scale"),
 ("2026", "ene 27", "Primer cambio de nombre", "Anthropic pide el cambio por marca. La comunidad vota: el proyecto pasa a llamarse Moltbot.", "https://docs.openclaw.ai/start/lore"),
 ("2026", "ene 30", "OpenClaw", "Tercer y último nombre. 100.000 estrellas en dos meses. TechCrunch advierte: no darle acceso al Slack o WhatsApp principal todavía.", "https://docs.openclaw.ai/start/lore"),
 ("2026", "abr", "Primera edición del estudio de harness", "Un estudio analiza el código de ocho agentes de producción y encuentra que el entorno pesa más que el modelo.", "https://arxiv.org/abs/2609.00006"),
 ("2026", "may 28", "OmniRetrieval", "Se publica el método para consultar fuentes heterogéneas (texto, tablas, grafos) sin aplanarlas en un solo formato.", "https://arxiv.org/abs/2605.29250"),
 ("2026", "jul 15", "El paper de referencia", "83 páginas: once harnesses de producción —incluidos Hermes y OpenClaw—, siete subsistemas, 29 patrones y dos ausencias. El harness quedó de plataforma.", "https://arxiv.org/abs/2609.00006"),
 ("2026", "ago 5", "La región vacía", "ASTELD clasifica ocho plataformas y 50+ derivados de OpenClaw. Hallazgo: ninguno combina despliegue local con seguridad empresarial.", "https://arxiv.org/abs/2608.05201"),
 ("2026", "ago 25", "El número que duele", "McKinsey 2026: el impacto significativo sigue en 6%. 80% dice que mejoró su productividad individual. La brecha entre individuo y proceso.", "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"),
 ("2026", "oct", "Este curso", "Doce clases para construir el agente propio, darle el conocimiento de la empresa, controlarlo con fuente obligatoria y gobernarlo con acta y métrica.", ""),
]

def timeline_html():
    filas = []
    for anio, cuando, titulo, texto, url in HITOS:
        link = f'<a href="{url}" target="_blank">fuente ↗</a>' if url else ''
        filas.append(f'''  <article class="h">
    <div class="hv"><span class="hy">{anio}</span><span class="hc">{cuando}</span></div>
    <div class="hb"><h3>{titulo}</h3><p>{texto}</p>{f'<p class="hs">{link}</p>' if link else ''}</div>
  </article>''')
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Línea de tiempo 2022–2026 — IA Agéntica para Ejecutivos</title>
<style>
:root{{--bg:#f8fafc;--card:#fff;--ink:#0f172a;--mut:#475569;--line:#e2e8f0;--acc:#7a2e0e;--soft:#fdf3ec;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}}
.wrap{{max-width:920px;margin:0 auto;padding:32px 22px 90px;}}
header{{border-bottom:2px solid var(--acc);padding-bottom:18px;margin-bottom:20px;}}
h1{{font-size:28px;margin:0 0 6px;letter-spacing:-.02em;}}
.sub{{color:var(--mut);font-size:14px;margin:0;}}
.tl{{position:relative;padding-left:26px;}}
.tl::before{{content:"";position:absolute;left:7px;top:6px;bottom:6px;width:2px;background:#e8d5c8;}}
.h{{position:relative;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:14px 0;}}
.h::before{{content:"";position:absolute;left:-19px;top:22px;width:12px;height:12px;border-radius:50%;background:var(--acc);border:2px solid #fff;}}
.hv{{display:flex;gap:10px;align-items:baseline;margin-bottom:4px;}}
.hy{{font-weight:800;color:var(--acc);font-size:15px;}}
.hc{{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.06em;}}
.hb h3{{margin:0 0 4px;font-size:16.5px;}}
.hb p{{margin:0;font-size:14.5px;color:var(--mut);}}
.hs{{margin-top:6px !important;font-size:12.5px !important;}}
a{{color:#2563eb;}}
footer{{margin-top:36px;padding-top:14px;border-top:1px solid var(--line);color:var(--mut);font-size:13px;}}
</style></head>
<body><div class="wrap">
<header>
  <h1>Línea de tiempo 2022–2026</h1>
  <p class="sub">Cómo pasamos de «el modelo no es suficientemente bueno» a saber que el harness pesa más · cada hito con su fuente</p>
</header>
<div class="tl">
{chr(10).join(filas)}
</div>
<footer>
  <a href="ejecutivos-ia-agentica.html">← Volver al plan de clases</a> ·
  <a href="ejecutivos-glosario.html">Glosario de datos →</a> ·
  Fechas verificadas en las fuentes citadas en cada hito (octubre 2026).
</footer>
</div></body></html>'''


open("ejecutivos-glosario.html", "w", encoding="utf-8").write(glosario_html())
open("ejecutivos-timeline.html", "w", encoding="utf-8").write(timeline_html())
print(f"  ejecutivos-glosario.html   ({len(GLOSARIO)} conceptos)")
print(f"  ejecutivos-timeline.html   ({len(HITOS)} hitos)")
