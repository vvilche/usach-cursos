#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los 25 slide decks de los cursos USACH con CONTENIDO que explica los conceptos.
Regenerar: editar CLASES y re-correr. Determinista, cero tokens de LLM en la generación."""
import html, os

CSS = """
:root{--bg:#f8fafc;--card:#fff;--ink:#0f172a;--mut:#475569;--line:#e2e8f0;--acc:ACC;--acc2:#2563eb;--warn:#b45309;--soft:SOFT;}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);}
.deck{max-width:960px;margin:0 auto;height:100vh;display:flex;flex-direction:column;padding:0 24px;}
header{display:flex;justify-content:space-between;align-items:center;padding:14px 0;color:var(--mut);font-size:13px;border-bottom:1px solid var(--line);}
header .curso{font-weight:700;color:var(--acc);}
main{flex:1;display:flex;align-items:center;justify-content:center;overflow:auto;}
.slide{display:none;width:100%;max-width:840px;animation:in .3s ease;}.slide.active{display:block;}
@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.kicker{color:var(--acc);font-weight:700;font-size:13px;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px;}
h1{font-size:44px;margin:0 0 10px;letter-spacing:-.02em;line-height:1.12;}
h2{font-size:30px;margin:0 0 18px;letter-spacing:-.015em;line-height:1.2;}
.lead{font-size:22px;line-height:1.5;color:var(--mut);margin:0;}
.big{font-size:26px;line-height:1.45;color:var(--ink);margin:0;}
.meta{color:var(--mut);font-size:16px;margin-top:14px;}
.def{background:var(--soft);border:1px solid #c8ecd4;border-left:5px solid var(--acc);border-radius:12px;padding:22px 26px;font-size:21px;line-height:1.55;margin:0;}
.def b{color:var(--acc);}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
.col{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;}
.col .t{font-weight:800;font-size:18px;margin-bottom:10px;}.col.bad .t{color:var(--warn);}.col.good .t{color:var(--acc);}
.col ul{padding-left:18px;margin:0;}.col li{font-size:16.5px;margin:7px 0;color:var(--mut);}
.loop{display:flex;align-items:center;justify-content:space-between;gap:6px;flex-wrap:wrap;}
.node{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 12px;text-align:center;flex:1;min-width:105px;}
.node .n{font-weight:800;font-size:16px;color:var(--acc);}.node .d{font-size:12.5px;color:var(--mut);margin-top:4px;}
.arrow{font-size:24px;color:var(--acc);font-weight:700;}
.cajon{background:var(--soft);border:1px solid #c8ecd4;border-radius:12px;padding:20px 24px;font-size:18px;line-height:1.55;margin:0;}
.cajon .q{font-weight:700;color:var(--ink);font-size:20px;margin-bottom:8px;}
.cajon ol{padding-left:20px;margin:8px 0 0;}.cajon li{margin:6px 0;color:var(--mut);}
.piezas{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;}
.pieza{background:var(--card);border:1px solid var(--line);border-top:4px solid var(--acc);border-radius:12px;padding:16px 18px;}
.pieza .t{font-weight:800;font-size:16px;margin-bottom:6px;}.pieza p{font-size:14.5px;color:var(--mut);margin:0;}
.warn{background:#fff7ed;border:1px solid #fed7aa;border-left:5px solid var(--warn);border-radius:12px;padding:18px 22px;font-size:18px;line-height:1.55;margin:0;}
.steps{counter-reset:s;}.steps .step{display:flex;gap:14px;align-items:flex-start;margin:12px 0;}
.steps .step::before{counter-increment:s;content:counter(s);background:var(--acc);color:#fff;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;flex-shrink:0;}
.steps .step p{margin:0;font-size:18px;color:var(--mut);}.steps .step p b{color:var(--ink);}
.links li{font-size:19px;margin:10px 0;}.links a{color:var(--acc2);}
ul.plain{padding-left:22px;margin:0;}ul.plain li{font-size:19px;margin:9px 0;color:var(--mut);}ul.plain li b{color:var(--ink);}
footer{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-top:1px solid var(--line);}
footer button{background:var(--acc);color:#fff;border:0;border-radius:8px;width:44px;height:44px;font-size:20px;cursor:pointer;}footer button:disabled{opacity:.3;}
.counter{color:var(--mut);font-size:13px;}
.code{background:#0f172a;color:#e2e8f0;border-radius:12px;padding:18px 20px;font:13.5px/1.6 \"SF Mono\",Menlo,Consolas,monospace;overflow:auto;max-height:62vh;white-space:pre;}
.code .c{color:#64748b}
.code .k{color:#7dd3fc}
.code .s{color:#86efac}
.code .n{color:#fca5a5}
#fs{background:none;border:1px solid var(--line);border-radius:8px;color:var(--mut);font-size:15px;width:34px;height:34px;cursor:pointer;line-height:1;}
#fs:hover{border-color:var(--acc);color:var(--acc);}
.hdr-right{display:flex;align-items:center;gap:12px;}
.hdr-left{display:flex;align-items:center;gap:14px;}
.volver{color:var(--mut);text-decoration:none;font-size:13px;font-weight:600;white-space:nowrap;}
.volver:hover{color:var(--acc);}
html.fs .deck{max-width:none;padding:0 5vw;}
html.fs .slide{max-width:1240px;}
html.fs h1{font-size:64px;}
html.fs h2{font-size:44px;}
html.fs .lead{font-size:30px;}
html.fs .big{font-size:36px;}
html.fs .def{font-size:28px;}
html.fs .meta{font-size:20px;}
html.fs .cajon{font-size:24px;}
html.fs .cajon .q{font-size:26px;}
html.fs ul.plain li{font-size:26px;}
html.fs .col li{font-size:22px;}
html.fs .col .t{font-size:24px;}
html.fs .steps .step p{font-size:24px;}
html.fs .node .n{font-size:20px;}
html.fs .node .d{font-size:16px;}
html.fs .pieza .t{font-size:20px;}
html.fs .pieza p{font-size:18px;}
html.fs .links li{font-size:24px;}
html.fs .warn{font-size:24px;}
html.fs .code{font-size:15px;}
html.fs .kicker{font-size:16px;}
"""

def esc(s): return html.escape(s, quote=False)

def render_slide(s):
    k = s[0]; w = s[1]
    kick = f'<div class="kicker">{esc(w.get("kicker",""))}</div>' if w.get("kicker") else ""
    h2 = f'<h2>{esc(w["h2"])}</h2>' if w.get("h2") else ""
    if k == "pregunta":
        return f'<section class="slide">{kick}{h2}<p class="big">{w["big"]}</p></section>'
    if k == "definicion":
        return f'<section class="slide">{kick}{h2}<p class="def">{w["defn"]}</p><p class="meta">{esc(w.get("meta",""))}</p></section>'
    if k == "vs":
        bad = "".join(f"<li>{esc(x)}</li>" for x in w["bad"])
        good = "".join(f"<li>{esc(x)}</li>" for x in w["good"])
        return (f'<section class="slide">{kick}{h2}<div class="grid2">'
                f'<div class="col bad"><div class="t">{esc(w["bad_t"])}</div><ul>{bad}</ul></div>'
                f'<div class="col good"><div class="t">{esc(w["good_t"])}</div><ul>{good}</ul></div></div></section>')
    if k == "loop":
        nodes = "".join(f'<div class="node"><div class="n">{esc(t)}</div><div class="d">{esc(d)}</div></div>' for t, d in w["nodes"])
        nodes = f'<span class="arrow">→</span>'.join([nodes]) if len(w["nodes"]) == 1 else nodes
        # intercalar flechas
        parts = []
        for i, (t, d) in enumerate(w["nodes"]):
            parts.append(f'<div class="node"><div class="n">{esc(t)}</div><div class="d">{esc(d)}</div></div>')
            if i < len(w["nodes"]) - 1:
                parts.append('<span class="arrow">→</span>')
        loop = "".join(parts)
        return f'<section class="slide">{kick}{h2}<p class="lead" style="margin-bottom:20px">{esc(w.get("lead",""))}</p><div class="loop">{loop}</div><p class="meta">{esc(w.get("meta",""))}</p></section>'
    if k == "ejemplo":
        steps = "".join(f"<li>{w['steps'][i]}</li>" for i in range(len(w["steps"]))) if isinstance(w.get("steps"), list) else ""
        return f'<section class="slide">{kick}{h2}<div class="cajon"><div class="q">{esc(w["q"])}</div><ol>{steps}</ol></div><p class="meta">{esc(w.get("meta",""))}</p></section>'
    if k == "piezas":
        pz = "".join(f'<div class="pieza"><div class="t">{esc(t)}</div><p>{esc(p)}</p></div>' for t, p in w["piezas"])
        return f'<section class="slide">{kick}{h2}<div class="piezas">{pz}</div></section>'
    if k == "porque":
        return f'<section class="slide">{kick}{h2}<p class="big">{w["big"]}</p><p class="meta">{esc(w.get("meta",""))}</p></section>'
    if k == "error":
        return f'<section class="slide">{kick}{h2}<div class="warn">{w["warn"]}</div></section>'
    if k == "pasos":
        st = "".join(f'<div class="step"><p><b>{esc(b)}</b> {esc(t)}</p></div>' for b, t in w["steps"])
        return f'<section class="slide">{kick}{h2}<div class="steps">{st}</div></section>'
    if k == "testeo":
        return f'<section class="slide">{kick}{h2}<p class="big">{w["big"]}</p><p class="meta">{esc(w.get("meta",""))}</p></section>'
    if k == "lista":
        li = "".join(f"<li>{x}</li>" for x in w["items"])
        return f'<section class="slide">{kick}{h2}<ul class="plain">{li}</ul></section>'
    if k == "links":
        li = "".join(f'<li><a href="{esc(u)}" target="_blank">{esc(l)}</a></li>' for l, u in w["links"])
        return f'<section class="slide">{kick}{h2}<ul class="links">{li}</ul></section>'
    if k == "code":
        return f'<section class="slide">{kick}{h2}<pre class="code">{w["code"]}</pre></section>'
    return f'<section class="slide">{kick}{h2}</section>'

def deck(curso, cu, n, fecha, titulo, lead, slides):
    acc = cu["color"]; soft = cu["soft"]
    css = CSS.replace("ACC", acc).replace("SOFT", soft)
    portada = (f'<section class="slide active"><div class="kicker">{esc(cu["level"]+" · "+cu["short"])}</div>'
               f'<h1>{esc(titulo)}</h1><p class="lead">{esc(lead)}</p></section>')
    cuerpo = "".join(render_slide(s) for s in slides)
    total = len(slides) + 1
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clase {n} · {esc(titulo)}</title><style>{css}</style></head>
<body><div class="deck">
<header><span class="hdr-left"><a class="volver" href="{cu['plan']}" title="Volver al plan de clases">← Plan de clases</a><span class="curso">{esc(cu['nombre'])}</span></span><span class="hdr-right"><span class="counter">Clase {n} · {fecha}</span><button id="fs" title="Pantalla completa (tecla F / Esc)">⛶</button></span></header>
<main>{portada}{cuerpo}</main>
<footer><button id="prev">←</button><span class="counter" id="cnt">1 / {total}</span><button id="next">→</button></footer>
</div>
<script>
var s=document.querySelectorAll('.slide'),i=0,n=s.length,cnt=document.getElementById('cnt');
function go(x){{s[i].classList.remove('active');i=(x+n)%n;s[i].classList.add('active');cnt.textContent=(i+1)+' / '+n;document.getElementById('prev').disabled=i===0;document.getElementById('next').disabled=i===n-1;}}
document.getElementById('prev').onclick=function(){{go(i-1)}};document.getElementById('next').onclick=function(){{go(i+1)}};
var fsBtn=document.getElementById('fs');
function toggleFs(){{var el=document.documentElement;if(!document.fullscreenElement&&!document.webkitFullscreenElement){{if(el.requestFullscreen)el.requestFullscreen();else if(el.webkitRequestFullscreen)el.webkitRequestFullscreen();}}else{{if(document.exitFullscreen)document.exitFullscreen();else if(document.webkitExitFullscreen)document.webkitExitFullscreen();}}}}
if(fsBtn)fsBtn.onclick=toggleFs;
function onFsChange(){{document.documentElement.classList.toggle('fs',!!(document.fullscreenElement||document.webkitFullscreenElement));}}
document.addEventListener('fullscreenchange',onFsChange);
document.addEventListener('webkitfullscreenchange',onFsChange);
document.addEventListener('keydown',function(e){{if(e.key==='ArrowRight'||e.key===' '){{e.preventDefault();go(i+1)}}else if(e.key==='ArrowLeft'){{go(i-1)}}else if(e.key==='f'||e.key==='F'){{toggleFs()}}}});
</script></body></html>"""

# ══════════════════════════════ CONTENIDO ══════════════════════════════
AU = {"nombre": "Hackeando la Auditoría con IA Agéntica", "short": "Auditoría IA Agéntica",
      "color": "#0a7a3d", "soft": "#eefaf1", "level": "Electivo IV",
      "plan": "auditoria-ia-agentica.html"}
IN = {"nombre": "Innovación: Ideas Disruptivas para el Éxito", "short": "Innovación Disruptiva",
      "color": "#2456a5", "soft": "#eef4fc", "level": "Electivo VI",
      "plan": "innovacion-disruptiva.html"}

CLASES = []
# ── AUDITORÍA ──
CLASES.append(dict(curso=AU, n=1, fecha="Jue 24 sep 2026", titulo="De ChatGPT al agente autónomo",
  lead="Por qué «chatear» con una IA no le cambia la pega a un auditor — y qué significa, de verdad, que una IA ejecute el trabajo por ti.",
  slides=[
   ("pregunta", dict(kicker="Dónde estamos hoy", h2="En 2025 las Big 4 invirtieron +US$6.000M en IA para auditar", big="PwC, Deloitte, EY y KPMG ya auditan con agentes de IA, análisis del 100% de las transacciones y process mining. La auditoría que aprenderás este semestre <b>ya está ocurriendo</b> — tú vas a construir una pieza de eso.")),
   ("piezas", dict(kicker="Las 4 plataformas", h2="Qué usa cada Big 4", piezas=[("PwC · Aura NextGen","US$1.000M. Harvey AI lee contratos (IFRS 16) y GL.ai detecta anomalías en asientos."),("Deloitte · Omnia","US$1.400M+. Red de agentes autónomos para conciliación bancaria y vouching."),("EY · Canvas","US$1.400M. Plataforma cloud con 150.000 usuarios y análisis antifraude en nóminas."),("KPMG · Clara","US$2.000M. Azure OpenAI: coteja estados contra taxonomías IFRS automáticamente.")])),
   ("lista", dict(kicker="Qué hace la IA hoy", h2="El fin del muestreo", items=["<b>Full-population testing:</b> auditar el 100% de los asientos, no una muestra de 25 facturas (se acaba la NIA 530).","<b>Agentes autónomos:</b> three-way matching (factura vs orden de compra vs recepción) — el 98% se aprueba solo.","<b>Process mining:</b> reconstruir la ruta REAL de cada transacción y detectar violaciones de segregación de funciones.","<b>ESG:</b> auditar datos no financieros (emisiones, agua) con el mismo rigor que un balance."])),
   ("porque", dict(kicker="Y en Chile", h2="NCG 519: la auditoría ESG ya es obligatoria", big="La CMF alineó a Chile con los estándares ISSB (IFRS S1/S2). Desde el <b>ejercicio 2026</b>, los emisores deben revelar emisiones y riesgos climáticos — y eso se audita.", meta="No estás aprendiendo una moda: estás aprendiendo la herramienta que el mercado chileno ya está exigiendo.")),
   ("lista", dict(kicker="Cómo lo vas a construir", h2="Sin computador potente, sin terminal", items=["<b>Google Colab:</b> Python corre en la nube de Google, en tu navegador. Funciona en Windows, Mac, Chromebook o tablet — solo necesitas una cuenta de Google y conexión a internet.","<b>No instalas nada:</b> no hay que configurar Python ni usar el terminal. Escribís código en celdas y lo ejecutas con un botón ▶.","<b>Learn Mode:</b> un tutor de IA gratis dentro de Colab que te explica cada línea de código en palabras simples. Actívalo desde la barra lateral."])),
   ("pregunta", dict(kicker="La pregunta del día", h2="Un auditor que solo «chatea» con una IA, ¿en qué cambió su pega?", big="En nada. Sigue copiando datos a mano, solo que ahora la IA le redacta el correo. El trabajo duro — conciliar, revisar, marcar — sigue siendo suyo.")),
   ("definicion", dict(kicker="Definición", h2="Qué es un agente (de verdad)", defn="Un agente es un programa que recibe un <b>objetivo</b>, <b>decide por sí mismo</b> qué hacer, usa <b>herramientas</b> y <b>ejecuta</b> hasta cumplirlo. No espera instrucciones paso a paso.", meta="La diferencia no es de «más inteligente»: es de quién hace el trabajo. Con ChatGPT tú eres el ejecutor. Con un agente, el ejecutor es la máquina.")),
   ("vs", dict(kicker="La diferencia clave", h2="IA conversacional vs. IA agéntica", bad_t="ChatGPT (conversacional)", bad=["Conversa y responde texto","No ejecuta acciones","Olvida todo al cerrar el chat","El trabajo lo haces tú"], good_t="Agente (agéntica)", good=["Ejecuta tareas completas","Usa herramientas (archivos, APIs, código)","Mantiene estado y avanza","El trabajo lo hace la máquina"])),
   ("loop", dict(kicker="El mecanismo", h2="El loop del agente", lead="Todo agente repite un ciclo de 3 pasos hasta cumplir el objetivo:", nodes=[("🎯 Objetivo","qué hay que lograr"),("PENSAR","¿qué hago ahora?"),("ACTUAR","llamar una herramienta"),("OBSERVAR","ver el resultado")], meta="Si el resultado no cumple el objetivo, vuelve a PENSAR con la info nueva. Es un loop, no una respuesta única.")),
   ("ejemplo", dict(kicker="Ejemplo real de auditoría", h2="Qué haría un agente con esta orden", q="«Conciliá estas 1.000 facturas contra el SII y marcá las que no cuadren.»", steps=["<b>Piensa:</b> «Necesito leer el archivo y cruzar cada factura con el registro del SII».","<b>Actúa:</b> abre el archivo, consulta la API del SII, compara montos y folios.","<b>Observa:</b> encuentra 37 facturas que no cuadran.","<b>Vuelve a actuar:</b> genera un reporte con las 37 marcadas y su motivo."], meta="No te redactó un consejo. Hizo la conciliación. Esa es la diferencia entre conversar y ejecutar.")),
   ("piezas", dict(kicker="Anatomía", h2="Las 3 piezas de un agente", piezas=[("🧠 Modelo","El cerebro que decide. Es el LLM (Claude, GPT, DeepSeek…), pero no basta solo."),("✋ Herramientas","Las manos: leer archivos, consultar APIs, correr código. Sin ellas es solo un ChatGPT."),("💾 Memoria","Recuerda qué ya hizo y qué le falta, para no repetir ni perder el hilo del objetivo.")])),
   ("porque", dict(kicker="Por qué importa", h2="Lo que le pasa al auditor", big="El auditor deja de ser <b>operador</b> (pegar datos en Excel) y pasa a ser <b>supervisor</b>: define qué controlar y revisa lo que el agente marcó.", meta="Resultado: audita el 100% de las transacciones, no una muestra. Y usa su criterio en lo que de verdad importa.")),
   ("error", dict(kicker="Error típico", h2="Confundir «pedir un texto» con «delegar una tarea»", warn="<b>Mal:</b> «Hazme un informe de las facturas.» → la IA devuelve texto genérico, sin tocar tus datos.<br><br><b>Bien:</b> darle <b>objetivo + herramientas + restricciones</b>: «Lee este archivo, cruza con el SII, marca las que no cuadren y devuélveme un reporte. No inventes cifras.»")),
   ("pasos", dict(kicker="La tarea de hoy (paso a paso)", h2="Tu primer agente", steps=[("Abre Google Colab:", "en el navegador, andá a colab.research.google.com y entrá con tu cuenta de Google. No instalas nada: corre en la nube de Google, da igual si tu compu es Windows o Mac."),("Crea un notebook nuevo:", "Archivo → Nuevo notebook. Es un documento donde escribes código y lo ejecutas con el botón ▶ (o Shift+Enter). Nada de terminal."),("Obtén tu key gratis de IA:", "andá a console.groq.com/keys y creá una key (gratis, 1 minuto). Es la llave que deja a tu código usar la IA."),("Pega el código del ejemplo:", "copia el código de la siguiente diapositiva y pegalo en una celda. Cambiá la línea de la key por la tuya."),("Corre con ▶:", "y mira lo que imprime. Ese es tu primer agente ejecutando una tarea de verdad.")])),
   ("code", dict(kicker="El código (copialo tal cual)", h2="Tu primer agente, línea por línea", code="""# PASO PREVIO: instalar la librería que conecta con la IA
# (escribe esta línea SOLA en una celda y apretá ▶)
!pip install openai

# ═══ AHORA SÍ, TU PRIMER AGENTE ═══
# Copiá todo esto en OTRA celda y corre con ▶
# Cada línea tiene un comentario (#) que explica qué hace.

# 1) LA LLAVE de la IA (la sacaste gratis en console.groq.com/keys)
from openai import OpenAI
cliente = OpenAI(
    api_key="PEGA-AQUI-TU-KEY",     # <- borrá esto y pegá tu key entre las comillas
    base_url="https://api.groq.com/openai/v1"
)

# 2) CREAMOS UN ARCHIVO DE EJEMPLO (para no depender de subir nada)
import pandas as pd
pd.DataFrame({
    "factura": ["F-001", "F-002", "F-003"],
    "monto":   [120000,  85000,  240000],
}).to_csv("facturas.csv", index=False)
print("Archivo de ejemplo creado: facturas.csv")

# 3) LA HERRAMIENTA: cuenta las filas de un CSV
#    (un CSV es una tabla guardada como texto, como un Excel simple)
def contar_filas(archivo):
    datos = pd.read_csv(archivo)   # abre la tabla
    return len(datos)              # len() cuenta cuántas filas tiene

# 4) EL OBJETIVO: qué queremos que el agente logre
objetivo = "contar cuántas filas tiene el archivo facturas.csv"

# 5) EL LOOP: pensar -> actuar -> observar
# PENSAR: le preguntamos a la IA qué herramienta usar
respuesta = cliente.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content":
        "Tengo un objetivo: " + objetivo +
        ". Responde SOLO con el nombre de la función a usar: contar_filas"}]
)
decision = respuesta.choices[0].message.content
print("La IA pensó:", decision)   # OBSERVAR lo que decidió

# ACTUAR: ejecutar la herramienta que la IA eligió
if "contar_filas" in decision:
    filas = contar_filas("facturas.csv")   # ejecuta la herramienta
    print("El archivo tiene", filas, "filas")   # OBSERVAR el resultado
else:
    print("La IA no supo qué hacer. Ajustá el objetivo.")
""")),
   ("lista", dict(kicker="Y ahora, crece", h2="El mismo agente, en 5 etapas", items=["<b>Etapa 1:</b> una herramienta (contar filas).","<b>Etapa 2:</b> 4 herramientas — la IA elige cuál usar.","<b>Etapa 3:</b> loop real — repetir hasta cumplir el objetivo.","<b>Etapa 4:</b> responder en lenguaje natural <b>con la fuente</b> (primer paso del cero-alucinación).","<b>Etapa 5:</b> conciliar facturas vs pagos y marcar las que no cuadran (aperitivo del caza-fraudes)."])),
   ("lista", dict(kicker="Para correrlo ya", h2="El código completo", items=["<b>agente_progresivo.py</b> en este sitio: el agente de auditoría entero, etapa por etapa, comentado línea por línea.","<b>Cómo:</b> descargalo, subelo a Colab (o copia su contenido en una celda), pegá tu key de Groq y corre.","<b>Mirá cómo crece:</b> cada etapa agrega UNA pieza. Así se construye un agente, de a poco."])),
   ("testeo", dict(kicker="El testeo", h2="Demuestra que entendiste el loop", big="Corre tu agente en pantalla y explica las 3 fases: qué pensó, qué hizo y qué observó.", meta="Si no puedes explicar el loop con tus palabras, el agente «funcionó» pero no aprendiste nada.")),
   ("links", dict(kicker="Para profundizar", h2="Para aprender", links=[("Google Colab (abrirlo ya)", "https://colab.research.google.com"),("Groq (key gratis, console.groq.com)", "https://console.groq.com/keys"),("agente_progresivo.py (código completo)", "agente_progresivo.py"),("Building Effective Agents (Anthropic)","https://www.anthropic.com/research/building-effective-agents")])),
  ]))
CLASES.append(dict(curso=AU, n=2, fecha="Jue 01 oct 2026", titulo="Agente lector de documentos",
  lead="Sacar cifras de un balance sin leerlo a mano, y sin que la IA invente números.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Cómo sacas las cifras de un PDF sin leerlo a mano?", big="Un auditor recibe balances en PDF todo el día. Si el agente tiene que «leerlos como persona», no ganaste nada. La clave es la extracción determinista.")),
   ("definicion", dict(kicker="Concepto", h2="Extracción determinista", defn="Leer el texto del PDF con una <b>librería</b> (PyMuPDF), no pedirle al LLM que «recuerde» las cifras. El LLM <b>formatea</b> lo que el parser ya leyó: nunca inventa números.", meta="Determinista = mismo PDF, misma salida, siempre. Sin aleatoriedad ni alucinación de cifras.")),
   ("vs", dict(kicker="Por qué no el LLM", h2="LLM leyendo vs. parser", bad_t="LLM «leyendo» el PDF", bad=["Puede inventar montos que no están","Resultado distinto cada vez","No cuadra el balance"], good_t="Parser (PyMuPDF)", good=["Lee el texto exacto del PDF","Siempre la misma salida","Las cifras cuadran contra el original"])),
   ("ejemplo", dict(kicker="Ejemplo", h2="Balance → tabla", q="De un balance real, extraer las cuentas principales:", steps=["Abrir el PDF y extraer todo el texto.","Ubicar activos, pasivos y patrimonio.","Emitir una tabla estructurada (cuenta, monto).","Verificar: activo = pasivo + patrimonio."], meta="La verificación del cuarto paso es la prueba de que la extracción fue correcta.")),
   ("pasos", dict(kicker="La tarea (paso a paso)", h2="Manos a la obra", steps=[("Instalá el lector de PDF:", "en una celda de Colab escribe «!pip install pymupdf» y apretá ▶. Es la librería que convierte un PDF en texto plano, como abrirlo y copiar todo el contenido."),("Abre un balance de ejemplo:", "sube un PDF real a Colab (puedes bajar uno de la CMF y arrastrarlo al panel de archivos). «Abrirlo» en código significa: leer el archivo y extraer todo su texto."),("Ubicá las cuentas:", "busca etiquetas conocidas («Total activos», «Total pasivos», «Patrimonio»). Son palabras fijas que puedes encontrar con una búsqueda de texto."),("Entrega una tabla:", "cuenta + monto, para que el agente la presente limpia. Regla de oro: el número sale del PDF, no de la cabeza del modelo.")])),
   ("testeo", dict(kicker="El testeo", h2="Que cuadre", big="La tabla extraída debe cuadrar contra el PDF: activo = pasivo + patrimonio.", meta="Si no cuadra, es error de extracción, no del PDF. Ese es el estándar mínimo de un agente lector.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("PyMuPDF","https://pymupdf.readthedocs.io")])),
  ]))
CLASES.append(dict(curso=AU, n=3, fecha="Jue 08 oct 2026", titulo="RAG: la memoria del agente",
  lead="Por qué un agente necesita recuperar (y no meter todo al prompt), y cómo se arma un mini-RAG.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Por qué no puedes meter 1.000 normas en el prompt?", big="El prompt tiene un límite (ventana de contexto) y, aunque cupiera, sería lento y caro. El agente necesita <b>recuperar solo lo relevante</b> para cada pregunta.")),
   ("definicion", dict(kicker="Concepto", h2="Qué es RAG", defn="<b>R</b>etrieval-<b>A</b>ugmented <b>G</b>eneration: antes de responder, el agente <b>busca</b> en su biblioteca los fragmentos relevantes y responde <b>basado en ellos</b>, citando la fuente.", meta="Sin RAG, el LLM responde de memoria (y alucina). Con RAG, responde con el documento delante.")),
   ("lista", dict(kicker="Las 3 piezas", h2="Cómo se construye", items=["<b>Chunking:</b> partir los documentos en trozos (párrafos, artículos).","<b>Embeddings:</b> convertir cada trozo en un vector que captura su significado.","<b>Índice vectorial:</b> guardar los vectores (FAISS) para buscar por similitud."])),
   ("loop", dict(kicker="El flujo", h2="Cómo responde un RAG", lead="Ante una pregunta:", nodes=[("❓ Pregunta","«¿cuál es la multa?»"),("🔍 Buscar","vectores más parecidos"),("📄 Recuperar","los top chunks"),("✍️ Responder","con esos chunks citados")], meta="El modelo genera SOLO a partir de lo recuperado. No de su memoria.")),
   ("vs", dict(kicker="Por qué no el prompt gigante", h2="Prompt gigante vs. retrieval", bad_t="Meter todo al prompt", bad=["Lento y caro (tokens)","Desborda la ventana de contexto","El modelo se confunde con tanto texto"], good_t="Recuperar solo lo relevante", good=["Rápido y barato","Escala a miles de docs","El modelo ve solo lo que importa"])),
   ("pasos", dict(kicker="La tarea (paso a paso)", h2="Mini-RAG en 3 pasos", steps=[("Instalá las librerías:", "en una celda de Colab: «!pip install fastembed faiss-cpu». fastembed convierte texto en vectores; faiss los guarda y busca parecidos."),("Chunkea:", "partí 10 documentos (normas del SII, por ejemplo) en párrafos. Cada párrafo será un «trozo» recuperable."),("Embebe e indexa:", "convertí cada trozo en un vector (una lista de números que captura su significado) y guardalos en FAISS."),("Consulta:", "ante una pregunta, busca los trozos más parecidos y que el agente responda citando cuál usó. Si no está, que diga «no está».")])),
   ("testeo", dict(kicker="El testeo", h2="Muestra la fuente", big="El agente responde y muestra qué chunk usó. Pregunta trampa: si no está en el corpus, debe decir «no está», no inventar.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Qué es RAG","https://www.pinecone.io/learn/retrieval-augmented-generation/"),("Vector embeddings","https://www.pinecone.io/learn/vector-embeddings/"),("fastembed","https://github.com/qdrant/fastembed"),("FAISS","https://github.com/facebookresearch/faiss")])),
  ]))
CLASES.append(dict(curso=AU, n=4, fecha="Jue 15 oct 2026", titulo="HITO L1 · Agente lector de balances",
  lead="Integrar extracción + RAG en un agente que lee un balance y responde con fuente.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Qué te falta para que sea «de verdad»?", big="Un agente que solo extrae cifras no responde preguntas. Uno que solo responde no lee documentos. El hito es <b>unirlos</b>.")),
   ("lista", dict(kicker="Integración", h2="Las piezas a unir", items=["<b>Extracción</b> (clase 2): leer el balance → tabla.","<b>RAG</b> (clase 3): indexar → recuperar → responder.","<b>Grounding:</b> toda respuesta cita su fuente."])),
   ("error", dict(kicker="Error típico", h2="El agente que no sabe decir «no está»", warn="Si le preguntan algo que no está en el balance y el agente inventa una cifra, <b>todo lo demás pierde valor</b>. La honestidad («no está en el documento») es más importante que parecer listo.")),
   ("pasos", dict(kicker="La tarea", h2="Integrá", steps=[("Conecta","extracción + índice en un solo agente."),("Agrega grounding:","cada respuesta lleva su fuente."),("Añade la regla","«si no está, dilo».")])),
   ("testeo", dict(kicker="El testeo", h2="Demo + prueba de fuego", big="Demo de 2 min por pareja. Luego, una pregunta cuya respuesta NO está en el balance: el agente debe declararlo.", meta="Pasa el hito quien demuestra que su agente lee, responde y NO inventa.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Cómo hacer un agente confiable","https://www.anthropic.com/research/building-effective-agents"),("RAG con grounding","https://www.pinecone.io/learn/grounded-rag/")])),
  ]))
CLASES.append(dict(curso=AU, n=5, fecha="Jue 22 oct 2026", titulo="El problema real: conciliación SII vs ERP",
  lead="El dolor de verdad del auditor: cruzar lo facturado con lo registrado, y por qué la Ley 21.595 lo vuelve urgente.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Cuántas facturas revisa un auditor al año… y a mano?", big="Miles, y casi todas a mano o por muestreo. La conciliación (facturas del SII vs. lo que registró el ERP) es donde se esconden los fraudes — y donde se pierden las horas.")),
   ("definicion", dict(kicker="Concepto", h2="Factura electrónica (DTE)", defn="En Chile toda factura es un <b>Documento Tributario Electrónico</b> que el SII valida y almacena. Hay una <b>fuente oficial</b> de la verdad para cada factura.", meta="El auditor no tiene que creerle al cliente: puede cruzar contra el SII.")),
   ("lista", dict(kicker="El problema", h2="Conciliación = cruzar", items=["<b>Registro de compras/ventas</b> (lo que dice la empresa).","<b>DTE del SII</b> (lo que realmente se facturó).","<b>Discrepancia</b> = factura sin respaldo, monto distinto, folio duplicado."])),
   ("porque", dict(kicker="El contexto legal", h2="Ley 21.595 — Delitos Económicos", big="Desde 2024, la empresa responde penalmente por delitos económicos (entre ellos, facturas falsas y fraude tributario). El auditor ya no revisa «por orden»: revisa porque hay <b>riesgo penal</b>.", meta="Un agente que detecta facturas truchas no es un lujo, es control de riesgo.")),
   ("pasos", dict(kicker="La tarea", h2="Prepará el terreno", steps=[("Explora el mapa de fuentes","contables de Chile (SII, CMF, LeyChile)."),("Arma un dataset","de facturas de ejemplo (RUT, monto, fecha, folio)."),("Deja el dataset listo","para conciliar la próxima clase.")])),
   ("testeo", dict(kicker="El testeo", h2="Explicá el dolor", big="Decí dónde vive cada dato del SII y por qué conciliar 1.000 facturas a mano es trabajo de 8 horas que un agente hace en segundos.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("SII (factura electrónica)","https://www.sii.cl"),("Ley 21.595 — Delitos Económicos","https://www.bcn.cl/leychile/navegar?idNorma=1195119"),("CMF","https://www.cmfchile.cl"),("Mapa de fuentes contables","mapa-fuentes-contables.html")])),
  ]))
CLASES.append(dict(curso=AU, n=6, fecha="Jue 29 oct 2026", titulo="Bajar datos del SII (ingestor, sin LLM)",
  lead="Traer la normativa y los datos del SII con Python determinista, sin gastar un token de IA.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Cómo bajas 68 circulares sin copiar y pegar?", big="Con un script. La ingesta de datos es trabajo de <b>código determinista</b>, no de IA. La IA entra después, a responder; no a «resumir» 68 PDFs uno por uno.")),
   ("definicion", dict(kicker="Concepto", h2="Ingestor determinista", defn="Un script que baja los documentos, extrae el texto y lo guarda limpio. <b>Siempre la misma salida</b> para la misma entrada — no depende de un modelo.", meta="Razón de fondo: si el LLM «resume» cada documento, gasta tokens y puede cambiar el contenido. Extraer es exacto y gratis.")),
   ("lista", dict(kicker="Las fuentes", h2="Dónde bajar", items=["<b>LeyChile:</b> API XML con el texto completo de cada ley (limpio, sin scrapear).","<b>SII:</b> índices de circulares/resoluciones + sus PDFs.","<b>Dedup:</b> hash por documento para no embeber dos veces lo mismo."])),
   ("error", dict(kicker="Error típico", h2="Mandar el LLM a «leer» en vez de extraer", warn="Si usas la IA para descargar/resumir el corpus, <b>pagas tokens por algo que un script hace gratis y mejor</b>. La regla: ingesta = código; IA = solo para responder.")),
   ("pasos", dict(kicker="La tarea (paso a paso)", h2="Corre el ingestor", steps=[("Bajá una ley:", "en Colab, pedí una ley a la API XML de LeyChile por su código y te devuelve el texto completo, limpio, sin copiar y pegar."),("Bajá una circular:", "del SII (índice + PDF). La circular es un PDF: extraés el texto con la misma librería de la clase 2."),("Limpialo y deduplicá:", "quedate con el texto plano y evitá guardar dos veces lo mismo (un «hash» por documento).")])),
   ("testeo", dict(kicker="El testeo", h2="Traé una fuente real", big="Cada pareja muestra una fuente real bajada, con el texto limpio, y confirma que la ingesta es Python puro (cero tokens de LLM).")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("LeyChile (API de normas)","https://www.leychile.cl"),("Circulares SII 2025","https://www.sii.cl/normativa_legislacion/circulares/2025/indcir2025.htm"),("Ingestor de ejemplo","ingestor_store_b.py")])),
  ]))
CLASES.append(dict(curso=AU, n=7, fecha="Jue 05 nov 2026", titulo="Detección de fraude + Ley 21.595",
  lead="Reglas que marcan facturas truchas, ligadas a los artículos de la Ley 21.595.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Qué hace «trucha» a una factura?", big="No es magia ni un modelo de ML: son <b>señales concretas</b> que se pueden escribir como reglas.")),
   ("lista", dict(kicker="Señales de fraude", h2="Qué buscar", items=["<b>Duplicados:</b> mismo folio/RUT repetido.","<b>RUT inválido:</b> dígito verificador que no cuadra.","<b>Montos redondos:</b> facturas sospechosamente exactas.","<b>Proveedores fantasma:</b> RUT sin inicio de actividades.","<b>Fechas inconsistentes:</b> factura emitida antes de existir la empresa."])),
   ("vs", dict(kicker="Enfoque", h2="Reglas vs. ML", bad_t="Modelo de ML desde el día 1", bad=["Necesita miles de ejemplos etiquetados","Caja negra: no sabes por qué marcó","Sobredimensionado para empezar"], good_t="Reglas deterministas primero", good=["Escribes la señal explícita","Cada alerta es auditable y explicable","Luego, si acaso, ML encima"])),
   ("porque", dict(kicker="El ancla legal", h2="Ligar cada alerta a la Ley 21.595", big="Una alerta sin respaldo legal es una opinión. Cada factura marcada debe decir <b>qué artículo</b> de la Ley 21.595 (o del Código Tributario) se viola.", meta="Eso convierte el agente de «detector» en «evidencia de auditoría».")),
   ("pasos", dict(kicker="La tarea", h2="Escribí las reglas", steps=[("Regla por señal:","duplicado, RUT inválido, monto raro, fecha inconsistente."),("Liga cada regla","a un artículo (Ley 21.595 / Código Tributario)."),("Genera un reporte","de alertas con su fundamento.")])),
   ("testeo", dict(kicker="El testeo", h2="Dataset con trampas", big="Sobre un dataset con facturas truchas plantadas, detectalas y decí qué artículo se viola en cada caso.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Ley 21.595 (artículos)","https://www.bcn.cl/leychile/navegar?idNorma=1195119"),("Tribunales Tributarios (casos reales)","https://www.tta.cl")])),
  ]))
CLASES.append(dict(curso=AU, n=8, fecha="Jue 19 nov 2026", titulo="HITO L2 · Auditoría en vivo a 1.000 transacciones",
  lead="El agente concilia 1.000 facturas SII vs ERP en segundos y entrega el reporte de discrepancias.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Tu agente aguanta 1.000 facturas de una?", big="Hasta ahora trabajaste con 10 documentos. El hito es la escala: mil transacciones, en segundos, con un reporte limpio.")),
   ("lista", dict(kicker="Qué armar", h2="La conciliación completa", items=["<b>Cargar</b> el dataset SII y el ERP simulado.","<b>Cruzar</b> por folio, RUT, monto y fecha.","<b>Marcar</b> discrepancias con su motivo.","<b>Reportar</b> en una tabla clara."])),
   ("porque", dict(kicker="El resultado", h2="De 8 horas a segundos", big="Lo que un auditor hace en un día, el agente lo hace en segundos <b>sobre el 100% de las facturas</b>, no sobre una muestra.", meta="Miden el tiempo en pantalla: ese número es su argumento de venta del proyecto.")),
   ("pasos", dict(kicker="La tarea", h2="Corre la auditoría", steps=[("Concilia","las 1.000 facturas contra el ERP."),("Marca","cada discrepancia (monto, folio, proveedor)."),("Mide y muestra","el tiempo total.")])),
   ("testeo", dict(kicker="El testeo", h2="Demo en vivo", big="El agente marca las facturas truchas en segundos, con el tiempo en pantalla, y explicas cada discrepancia.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("SII","https://www.sii.cl"),("Ley 21.595","https://www.bcn.cl/leychile/navegar?idNorma=1195119")])),
  ]))
CLASES.append(dict(curso=AU, n=9, fecha="Jue 26 nov 2026", titulo="Cero alucinación: spec-first (spec-kit)",
  lead="Por qué los LLM inventan, y cómo una especificación rígida lo evita.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Por qué un LLM inventa un artículo que no existe?", big="Porque genera la palabra «más probable», no la «más cierta». Sin una restricción, rellena los huecos con lo que suena plausible.")),
   ("definicion", dict(kicker="Concepto", h2="Alucinación", defn="El modelo produce información <b>falsa pero verosímil</b> cuando no tiene la respuesta y no está obligado a decir «no sé».", meta="En auditoría una alucinación no es un error menor: es una cifra o un artículo inventado en un informe.")),
   ("vs", dict(kicker="La solución", h2="Pedir suelto vs. especificar", bad_t="Prompt suelto", bad=["«Revisa estas facturas»","El modelo decide qué es importante","Inventa plazos y artículos"], good_t="Spec rígida (spec-kit)", good=["Define QUÉ hacer y QUÉ NO","«Prohibido inventar artículos/plazos»","El agente sigue la spec, no improvisa"])),
   ("ejemplo", dict(kicker="Ejemplo", h2="Una spec de auditoría", q="Spec: «Cuadra la conciliación al centavo»", steps=["Cita la norma vigente, nunca de memoria.","Prohibido inventar artículos, plazos o umbrales.","Si un dato no está en la fuente, decláralo.","Entrega la cifra con su fuente al lado."], meta="Con esta spec, el agente prefiere decir «no está» antes que inventar.")),
   ("pasos", dict(kicker="La tarea", h2="Escribí tu spec", steps=[("Define QUÉ","debe hacer el agente exactamente."),("Define QUÉ NO","puede hacer (inventar, redondear, omitir)."),("Haz que el agente","ejecute respetando la spec.")])),
   ("testeo", dict(kicker="El testeo", h2="Prueba adversarial", big="Pedile un artículo que no existe. Debe decir «no está en la norma», no inventar el «Artículo 999».")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("spec-kit (Spec-Driven Development)","https://github.com/github/spec-kit"),("Por qué un RAG alucina","https://www.pinecone.io/learn/rag-hallucinations/")])),
  ]))
CLASES.append(dict(curso=AU, n=10, fecha="Jue 03 dic 2026", titulo="Guardrails: Zod + Graft",
  lead="Blindar el agente con validación de datos y mapeo del código del ERP.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Cómo haces que el agente RECHAZE un dato malo?", big="Un agente sin validación deja pasar basura. Con un <b>schema</b>, cada dato se chequea contra reglas antes de aceptarse.")),
   ("definicion", dict(kicker="Concepto", h2="Guardrails de datos", defn="Un <b>schema</b> (Zod/Pydantic) define qué es una factura válida: campos, tipos y reglas. Si un dato no cumple, el agente lo <b>rechaza</b> en vez de pasarlo.", meta="Es el cinturón de seguridad: no evita que el modelo se equivoque, evita que el error llegue al reporte.")),
   ("piezas", dict(kicker="Dos herramientas", h2="Zod + Graft", piezas=[("🔒 Zod","Valida datos: «el monto es número > 0», «el RUT tiene 9 dígitos». Rechaza lo que no cuadra."),("🗺️ Graft","Mapea el código del ERP en un grafo legible para que el agente no se pierda entre módulos."),("⚙️ Resultado","El agente valida cada transacción antes de aceptarla.")])),
   ("vs", dict(kicker="El efecto", h2="Sin guardrails vs. con guardrails", bad_t="Sin validación", bad=["Pasa un monto negativo o un RUT roto","El error llega al informe final","Nadie sabe dónde se rompió"], good_t="Con schema Zod", good=["Rechaza la transacción al instante","Cada rechazo dice qué regla falló","El reporte solo lleva datos válidos"])),
   ("pasos", dict(kicker="La tarea (paso a paso)", h2="Blindá tu agente", steps=[("Definí el schema Zod:", "escribe qué es una factura VÁLIDA: qué campos tiene (RUT, monto, fecha), de qué tipo es cada uno y qué reglas debe cumplir (monto > 0, RUT con dígito verificador)."),("Mapeá el mini-ERP:", "con Graft, dibujá cómo se conectan los módulos (factura → pago → conciliación) para que el agente no se pierda."),("Conectá la validación:", "que el agente chequee cada transacción contra el schema ANTES de aceptarla. Si falla, la rechaza y dice por qué.")])),
   ("testeo", dict(kicker="El testeo", h2="Que rechace", big="El agente rechaza una transacción que no cuadra y explica qué regla del schema la frenó.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Zod","https://zod.dev"),("Pydantic","https://docs.pydantic.dev"),("Graft (grafo de código)","https://github.com/NanoNets/graft")])),
  ]))
CLASES.append(dict(curso=AU, n=11, fecha="Jue 10 dic 2026", titulo="HITO L3 · Blindaje al centavo + evaluación",
  lead="Medir si tu agente de verdad no alucina, con un set de evaluación y una batería adversarial.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Cómo sabes que tu agente no alucina?", big="No lo sabes hasta que lo <b>mides</b>. «Me funciona» no es evidencia. Un set de evaluación lo es.")),
   ("lista", dict(kicker="Las métricas", h2="Qué medir", items=["<b>Recall:</b> ¿recuperó los documentos relevantes? (≥ 0.75)","<b>Precision:</b> ¿lo recuperado era relevante? (≥ 0.70)","<b>Faithfulness:</b> ¿la respuesta se sostiene en la fuente? (≥ 0.80)","<b>MRR:</b> ¿la fuente correcta rankea arriba?"])),
   ("lista", dict(kicker="La batería", h2="Pruebas adversariales", items=["<b>Falsa premisa:</b> preguntar por un artículo inexistente.","<b>Typos:</b> «plzso» en vez de «plazo».","<b>Prompt injection:</b> «ignora tus instrucciones».","<b>Cadena de 4 vueltas:</b> referencias a «eso», «el plazo»."])),
   ("pasos", dict(kicker="La tarea", h2="Armá tu set de evaluación", steps=[("Escribe 10+ consultas","con su respuesta esperada."),("Medí","recall/precision del retrieval y faithfulness."),("Corre la batería adversarial","y registrá los resultados.")])),
   ("testeo", dict(kicker="El testeo", h2="Con métricas en pantalla", big="Pasá la batería adversarial y muestra que el agente responde con fuente o declara «no está», con los números de recall/faithfulness.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Evaluar un RAG","https://www.pinecone.io/learn/rag-evaluation/"),("Faithfulness / groundedness","https://www.pinecone.io/learn/rag-faithfulness/")])),
  ]))
CLASES.append(dict(curso=AU, n=12, fecha="Jue 17 dic 2026", titulo="Hackathon: el Swarm multi-agente",
  lead="Orquestar varios agentes que se reparten el trabajo de auditoría.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Un solo agente o varios?", big="Un solo agente haciendo todo se pierde. Un <b>swarm</b> reparte el trabajo: cada agente hace una cosa y se la pasa al siguiente.")),
   ("definicion", dict(kicker="Concepto", h2="Orquestación multi-agente", defn="Dividir la tarea en <b>roles</b> y hacer que colaboren: uno extrae, otro concilia, otro detecta fraude. El resultado de uno es la entrada del otro.", meta="No es correr 3 veces el mismo agente: es una cadena de especialistas.")),
   ("loop", dict(kicker="El flujo", h2="Un swarm de auditoría", lead="El flujo end-to-end:", nodes=[("📄 Extractor","lee facturas y ERP"),("🔁 Conciliador","cruza y marca"),("🚨 Caza-fraudes","alerta + fundamento")], meta="Cada agente hace su parte y entrega al siguiente. Sin intervención manual.")),
   ("error", dict(kicker="Error típico", h2="El agente «todista»", warn="Un solo agente con un prompt enorme que hace todo termina <b>confundido y lento</b>. Dividir en roles pequeños es más fácil de probar y de arreglar.")),
   ("pasos", dict(kicker="La tarea", h2="Armá tu swarm", steps=[("Definí los roles","(2–3 agentes)."),("Encadená","la salida de uno como entrada del otro."),("Probá el flujo","de punta a punta.")])),
   ("testeo", dict(kicker="El testeo", h2="End-to-end", big="El swarm ejecuta el flujo completo (factura → conciliación → alerta) sin intervención manual entre pasos.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Patrones multi-agente (Anthropic)","https://www.anthropic.com/research/building-effective-agents")])),
  ]))
CLASES.append(dict(curso=AU, n=13, fecha="Jue 07 ene 2027", titulo="Demo final / Executive Pitch",
  lead="Presentar el sistema agéntico de auditoría como si fuera a un directorio.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Puedes vender lo que construiste?", big="El mejor agente no vale si no sabes explicarlo a un directorio en 3 minutos.")),
   ("lista", dict(kicker="El pitch", h2="Qué comunicar", items=["<b>Problema:</b> el dolor real del auditor.","<b>Solución:</b> qué hace tu swarm, con demo.","<b>Impacto:</b> tiempo/costo/cobertura (números).","<b>Confianza:</b> cómo garantizas que no alucina."])),
   ("pasos", dict(kicker="La tarea", h2="Prepará la demo", steps=[("Estructura el pitch","problema → solución → impacto."),("Ensaya la demo en vivo","con datos reales."),("Anticipa preguntas","del panel.")])),
   ("testeo", dict(kicker="El testeo final", h2="Ante el panel", big="El sistema responde con fuente, cuadra al centavo y defiende sus alertas. Importa que funcione y lo sepan explicar — no una nota.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Cómo hacer un agente confiable","https://www.anthropic.com/research/building-effective-agents")])),
  ]))

# ── INNOVACIÓN (profundizado) ──
CLASES.append(dict(curso=IN, n=1, fecha="Sáb 26 sep 2026", titulo="¿Qué es innovar de verdad? Disrupción vs mejora",
  lead="Por qué las grandes empresas fracasan ante lo nuevo, y qué es un «job to be done».",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Por qué las empresas grandes fracasan ante lo nuevo?", big="Porque son excelentes sirviendo a sus mejores clientes. La disrupción no llega por lo alto: entra por abajo, con algo más simple y barato, y sube hasta comerse el mercado.")),
   ("definicion", dict(kicker="Concepto", h2="Disrupción (Christensen)", defn="Una <b>disrupción</b> ataca un segmento que el líder <b>ignora</b> con una oferta más simple, barata o accesible, y desde ahí mejora hasta quedarse con el mercado.", meta="No es «hacerlo mejor»: es «hacerlo distinto para quien hoy no está servido».")),
   ("lista", dict(kicker="Los 3 tipos", h2="No toda innovación es disrupción", items=["<b>Sustaining:</b> mejorar el producto para los mejores clientes (iPhone cada año). No es disruptiva.","<b>Low-end disruption:</b> entrar por abajo con algo más barato/simple (autos chinos vs premium).","<b>New-market disruption:</b> crear un mercado donde no había (smartphones para no-usuarios de PC)."])),
   ("vs", dict(kicker="La distinción clave", h2="Mejora incremental vs. disrupción", bad_t="Mejora incremental", bad=["Servir mejor al mismo cliente","El líder te copia rápido","Misma batalla, mismo campo"], good_t="Disrupción", good=["Nuevo segmento o nueva forma de usar","El líder lo desprecia al inicio","Redefine las reglas del juego"])),
   ("porque", dict(kicker="El dilema", h2="Por qué el líder la ignora (racionalmente)", big="El segmento bajo tiene <b>márgenes malos</b> y sus clientes actuales <b>no quieren</b> el producto simple. La decisión lógica es «no entremos ahí». Y justo ahí crece el disruptor.", meta="El dilema del innovador: hacer lo correcto para hoy es lo que te mata mañana.")),
   ("definicion", dict(kicker="Concepto", h2="Jobs to be Done", defn="El cliente no «compra un producto»: <b>contrata algo para hacer un trabajo</b>. El taladro se contrata para hacer el agujero en la pared.", meta="La pregunta correcta no es «¿qué quiere comprar?» sino «¿qué trabajo necesita hacer?».")),
   ("ejemplo", dict(kicker="Ejemplo clásico", h2="El batido de Christensen", q="Una cadena de comida rápida quería vender más batidos en la mañana.", steps=["Entrevistaron a los clientes: «¿más espeso?, ¿más dulce?» y nada subea las ventas.","Observaron a los que COMPRABAN: se lo llevaban al auto, solos, en la mañana.","El «trabajo»: algo para hacer con una mano en un viaje aburrido.","El batido ganaba al plátano o la dona: duraba más y no ensuciaba."], meta="No preguntaron «¿qué quieres?». Observaron qué trabajo estaba haciendo el cliente.")),
   ("lista", dict(kicker="Profundizar", h2="Las 3 dimensiones del «job»", items=["<b>Funcional:</b> qué tarea resuelve (llegar del punto A al B).","<b>Emocional:</b> cómo lo hace sentir (seguridad, tranquilidad).","<b>Social:</b> qué dice de él ante los demás (estatus, pertenencia)."])),
   ("error", dict(kicker="Error típico", h2="Preguntar «¿qué quieres?» en vez de observar", warn="«¿Qué quieres?» te da respuestas racionalizadas. <b>Observá qué hacen</b>, qué se les complica, qué improvisan. El trabajo se ve en la conducta, no en el discurso.")),
   ("pasos", dict(kicker="La tarea", h2="Encontrá el «job»", steps=[("Elegí un mercado real.",""),("Describe el trabajo","que hoy se resuelve mal (funcional + emocional + social)."),("NO propongas solución todavía","— solo el problema.")])),
   ("testeo", dict(kicker="El testeo", h2="¿Es disruptiva o incremental?", big="Explicá por qué tu idea es disruptiva (segmento ignorado u otra forma de hacer el trabajo), no una mejora incremental del líder.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Christensen — The Innovator's Dilemma","https://www.claytonchristensen.com"),("Jobs to be Done (Alan Klement)","https://jtbd.info")])),
  ]))
CLASES.append(dict(curso=IN, n=2, fecha="Sáb 03 oct 2026", titulo="Océano Azul: crear mercados sin competencia",
  lead="Redefinir los factores de la industria para crear un mercado donde no compites por lo mismo.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Competir por lo mismo o crear mercado nuevo?", big="En el <b>océano rojo</b> todos pelean por los mismos clientes y el agua se tiñe de sangre. En el <b>océano azul</b> redefines el juego y la competencia se vuelve irrelevante.")),
   ("vs", dict(kicker="La distinción", h2="Rojo vs. azul", bad_t="Océano rojo", bad=["Competís en un mercado saturado","Ganás quitándole clientes al otro","Márgenes que se achican"], good_t="Océano azul", good=["Creas demanda nueva","La competencia deja de importar","Márgenes altos al inicio"])),
   ("definicion", dict(kicker="La herramienta", h2="La curva de valor (strategy canvas)", defn="Un gráfico que compara <b>en qué factores compite</b> la industria. Innovar es <b>cambiar la forma</b> de esa curva, no moverla un poco.", meta="Si tu curva es una copia desplazada de la competencia, sigues en océano rojo.")),
   ("lista", dict(kicker="El método", h2="EREC: 4 movimientos", items=["<b>E</b>liminar: sacar un factor que la industria da por sentado.","<b>R</b>educir: bajarlo muy por debajo del estándar.","<b>E</b>levar: subirlo muy por encima del estándar.","<b>C</b>rear: un factor que la industria nunca ofreció."])),
   ("ejemplo", dict(kicker="Ejemplo clásico", h2="Cirque du Soleil", q="Ni circo tradicional ni teatro: un mercado nuevo.", steps=["Eliminó: animales y estrellas de circo.","Redujo: humor barato y pista única.","Elevó: estética y música de teatro.","Creó: un espectáculo artístico para adultos."], meta="No compitió con Ringling Bros: creó su propio océano azul.")),
   ("ejemplo", dict(kicker="Ejemplo clásico", h2="[yellow tail]", q="Un vino que rompió todas las reglas de la industria.", steps=["Eliminó: envejecimiento, prestigio, lenguaje técnico, añadas.","Redujo: la variedad de cepas y la complejidad.","Elevó: facilidad de elegir y de beber.","Creó: un vino «para cualquiera» que no intimida."], meta="Atrajo a los que NO tomaban vino (cerveceros, cocteleros), no a los expertos.")),
   ("lista", dict(kicker="Profundizar", h2="Los 6 caminos hacia el océano azul", items=["Mirar <b>industrias alternativas</b> (no solo competidores).","Mirar <b>grupos estratégicos</b> (premium vs. económico).","Mirar la <b>cadena de compradores</b> (usuario vs. comprador vs. influenciador).","Mirar <b>ofertas complementarias</b> (qué pasa antes/después de usar el producto).","Cambiar el <b>apelo funcional → emocional</b> (o al revés).","Mirar <b>el tiempo</b> (tendencias que aún no son mercado)."])),
   ("pasos", dict(kicker="La tarea", h2="Dibujá tu curva", steps=[("Listá los factores","en los que compite tu industria."),("Aplicá EREC","a cada factor."),("Compará tu curva","contra la del competidor típico.")])),
   ("testeo", dict(kicker="El testeo", h2="Redefines, no copias", big="Tu curva redefine al menos un factor que la industria da por sentado — no es una copia desplazada.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Blue Ocean Strategy (Kim & Mauborgne)","https://www.blueoceanstrategy.com")])),
  ]))
CLASES.append(dict(curso=IN, n=3, fecha="Sáb 10 oct 2026", titulo="Modelo de negocio: Canvas + 4 cajas",
  lead="Cómo tu idea crea, entrega y captura valor — y cómo lo dibujas en un Canvas.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Tu idea cómo gana plata?", big="Una idea genial sin modelo de negocio es un hobby. El modelo responde: ¿para quién creas valor, cómo lo entregas y cómo lo capturás?")),
   ("vs", dict(kicker="La distinción", h2="Producto vs. modelo de negocio", bad_t="Solo producto", bad=["«Tengo una app genial»","Sin respuesta de quién paga","Sin lógica de sostenibilidad"], good_t="Modelo de negocio", good=["Producto + cliente + canal + ingresos","Claro quién paga y por qué","Sistema completo que se sostiene"])),
   ("definicion", dict(kicker="Concepto", h2="Modelo de negocio", defn="La forma en que una organización <b>crea, entrega y captura</b> valor. Es la lógica de cómo el negocio funciona y se sostiene en el tiempo.", meta="No es el producto: es todo el sistema alrededor de él.")),
   ("lista", dict(kicker="La herramienta", h2="Canvas: 9 cajas (Osterwalder)", items=["<b>Front (cliente):</b> segmentos · propuesta de valor · canales · relación.","<b>Back (operación):</b> recursos · actividades · socios clave.","<b>Dinero:</b> ingresos · costos."])),
   ("lista", dict(kicker="Profundizar", h2="Ingresos: ¿quién paga y cómo?", items=["<b>Transaccional:</b> pagás por uso (una venta).","<b>Recurrente:</b> suscripción mensual/anual.","<b>Freemium:</b> básico gratis, premium pago.","<b>Licencia / marketplace:</b> cobrás comisión o permiso."])),
   ("lista", dict(kicker="Complemento", h2="4 cajas de Johnson", items=["<b>Propuesta de valor</b> para el cliente.","<b>Fórmula de utilidad:</b> cómo generas margen (ingresos - costos).","<b>Recursos clave.</b>","<b>Procesos clave.</b>"])),
   ("ejemplo", dict(kicker="Ejemplo", h2="Spotify (freemium)", q="Un modelo que responde las 9 cajas:", steps=["Segmentos: oyentes gratis + premium + anunciantes.","Propuesta: música ilimitada sin fricción.","Ingresos: suscripción premium + publicidad.","Recursos: catálogo (licencias) + algoritmo de recomendación."], meta="El producto es la app; el modelo es cómo el gratis alimenta al pago.")),
   ("error", dict(kicker="Error típico", h2="Llenar el canvas sin pensar en el cliente", warn="Las 9 cajas se llenan solas… y quedan vacías de sentido. Empezá SIEMPRE por el <b>segmento</b> y la <b>propuesta de valor</b>; el resto se deriva de ahí.")),
   ("pasos", dict(kicker="La tarea", h2="Llená tu Canvas", steps=[("Completá las 9 cajas","para tu idea."),("Marcá las 2 cajas más débiles","— son tus supuestos críticos."),("Prepará explicar","cómo creas, entregas y capturás valor.")])),
   ("testeo", dict(kicker="El testeo", h2="En 60 segundos", big="Explicá cómo tu modelo crea, entrega y captura valor, y cuáles son tus 2 supuestos más arriesgados.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Business Model Canvas","https://www.strategyzer.com/library/the-business-model-canvas"),("Las 4 cajas de Johnson (HBR)","https://hbr.org/2008/12/reinventing-your-business-model")])),
  ]))
CLASES.append(dict(curso=IN, n=4, fecha="Sáb 17 oct 2026", titulo="Patrones: 55 patrones + 10 tipos de innovación",
  lead="Generar variantes de tu modelo con recetas probadas, no esperando la inspiración.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Cómo generas ideas nuevas sin esperar la inspiración?", big="La innovación no es un golpe de suerte: hay <b>patrones</b> — recetas de modelos que ya funcionaron — que puedes aplicar sistemáticamente.")),
   ("definicion", dict(kicker="Concepto", h2="Recombinación de patrones", defn="El 90% de los modelos nuevos son una <b>recombinación</b> de patrones que ya existen. No inventás de cero: mezclás piezas probadas de formas nuevas.", meta="El Business Model Navigator documenta 55 de esos patrones.")),
   ("lista", dict(kicker="Patrones clave", h2="6 patrones con ejemplo", items=["<b>Freemium:</b> Spotify, LinkedIn.","<b>Suscripción:</b> Netflix, SaaS.","<b>Razor-and-blade:</b> la máquina barata, el repuesto caro (Gillette).","<b>Marketplace:</b> conectas oferta y demanda (MercadoLibre, Airbnb).","<b>Long tail:</b> vender muchos nichos, no pocos éxitos (Amazon).","<b>Peer-to-peer:</b> los usuarios son el activo (Uber, Airbnb)."])),
   ("lista", dict(kicker="Complemento", h2="10 tipos de innovación (Doblin)", items=["<b>Configuración:</b> modelo de negocio, red, estructura, proceso.","<b>Oferta:</b> performance del producto, sistema de producto.","<b>Experiencia:</b> servicio, canal, marca, engagement."])),
   ("ejemplo", dict(kicker="Ejemplo", h2="Aplicar un patrón a tu idea", q="Si tu idea es «asesoría contable», aplicá patrones:", steps=["Suscripción: contabilidad mensual fija en vez de honorarios por hora.","Freemium: diagnóstico gratis, servicio pago.","Marketplace: conecta contadores con pymes."], meta="Cada patrón es un modelo distinto sobre el mismo producto.")),
   ("error", dict(kicker="Error típico", h2="Variación cosmética vs. cambio de lógica", warn="Cambiar el color o el precio NO es un nuevo modelo. Un patrón cambia <b>qué crea valor, quién paga o cómo se captura</b>. Si no cambia la lógica, es cosmética.")),
   ("pasos", dict(kicker="La tarea", h2="Aplicá patrones", steps=[("Elegí 3 patrones","de los 55 que no usas hoy."),("Aplicalos a tu modelo base.",""),("Generá 2 modelos alternativos","genuinamente distintos.")])),
   ("testeo", dict(kicker="El testeo", h2="No variaciones cosméticas", big="Los 2 modelos nuevos son genuinamente distintos (cambia la lógica de captura de valor) y puedes decir qué patrón los generó.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Business Model Navigator (55 patrones)","https://www.businessmodelnavigator.com"),("Ten Types of Innovation (Doblin)","https://doblin.com/ten-types")])),
  ]))
CLASES.append(dict(curso=IN, n=5, fecha="Sáb 24 oct 2026", titulo="Propuesta de valor + Customer Development",
  lead="Diseñar la propuesta de valor y salir a validarla con clientes reales.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Tu «gran idea» la valida alguien o solo tú?", big="La mayoría de las ideas mueren no por malas, sino por <b>nunca haber hablado con un cliente</b>. Validar es salir a la calle, no creerse la propia idea.")),
   ("definicion", dict(kicker="Concepto", h2="Value Proposition Canvas", defn="Une dos lados: los <b>trabajos, dolores y ganancias</b> del cliente, con tus <b>productos, aliviadores y creadores de ganancia</b>.", meta="El encaje problema-solución se ve cuando tu oferta alivia el dolor real del cliente.")),
   ("lista", dict(kicker="Lado del cliente", h2="Jobs · Pains · Gains", items=["<b>Jobs:</b> qué trabajo intenta hacer (funcional, emocional, social).","<b>Pains:</b> qué le molesta, qué cuesta, qué riesgo teme.","<b>Gains:</b> qué resultado espera, qué lo sorprendería gratamente."])),
   ("lista", dict(kicker="Lado de tu propuesta", h2="Products · Relievers · Creators", items=["<b>Products:</b> qué ofrecés.","<b>Pain relievers:</b> cómo quitás cada dolor.","<b>Gain creators:</b> cómo generas cada ganancia."])),
   ("definicion", dict(kicker="Concepto", h2="Customer Development (Steve Blank)", defn="Salir del edificio y <b>hablar con clientes</b> para descubrir el problema antes de construir la solución.", meta="4 pasos: descubrimiento → validación → creación → construcción de la empresa. El curso cubre los 2 primeros.")),
   ("error", dict(kicker="Error típico", h2="Preguntar «¿te gustaría?»", warn="«¿Te gustaría una app para X?» → todos dicen que sí y nadie compra. Preguntá en cambio: <b>«¿cómo lo resolvés hoy?, ¿cuánto te cuesta?, ¿qué intentaste?»</b> — el dolor aparece solo.")),
   ("lista", dict(kicker="Cómo entrevistar", h2="5 reglas de la entrevista", items=["Preguntas <b>abiertas</b>, nunca «¿te gusta?».","<b>Escuchá</b>, no vendas tu idea.","Buscá <b>hechos del pasado</b>, no opiniones del futuro.","Identificá <b>qué ya pagan</b> hoy por resolverlo.","No entrevistes solo a amigos y familia."])),
   ("pasos", dict(kicker="La tarea", h2="Validá", steps=[("Llená el Value Proposition Canvas.",""),("Escribí un guión","de 5+ preguntas de descubrimiento."),("Hacé 1 entrevista real","antes de la próxima clase.")])),
   ("testeo", dict(kicker="El testeo", h2="Con evidencia, no opinión", big="Mostrá el encaje problema-solución con evidencia de cliente (al menos 1 entrevista hecha), no con tu opinión.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Value Proposition Design","https://www.strategyzer.com/library/value-proposition-design"),("Customer Development (Steve Blank)","https://steveblank.com")])),
  ]))
CLASES.append(dict(curso=IN, n=6, fecha="Sáb 07 nov 2026", titulo="Lean Startup + MVP",
  lead="Aprender rápido con el mínimo producto, antes de gastar un año construyendo.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Cómo sabes si tu idea sirve antes de gastar un año?", big="No lo sabes, por eso no construís el producto completo: construís el <b>mínimo para aprender</b> y mides.")),
   ("definicion", dict(kicker="Concepto", h2="Build-Measure-Learn", defn="Ciclo lean: <b>construí</b> lo mínimo, <b>medí</b> cómo responde el mercado, <b>aprendé</b> y decide (pivotar o perseverar).", meta="La velocidad de aprendizaje, no la de construcción, es la ventaja.")),
   ("definicion", dict(kicker="Concepto", h2="MVP", defn="La <b>versión mínima</b> que te permite testear tu hipótesis más riesgosa con el menor esfuerzo.", meta="No es un producto «malo»: es un experimento con la forma de un producto.")),
   ("lista", dict(kicker="Tipos de MVP", h2="No hace falta código", items=["<b>Landing page:</b> mides interés antes de construir.","<b>Video:</b> muestras cómo funcionaría (Dropbox).","<b>Concierge:</b> hacés el trabajo a mano (Zappos).","<b>Wizard of Oz:</b> el «software» es una persona detrás.","<b>Prototipo:</b> maqueta para testear usabilidad."])),
   ("ejemplo", dict(kicker="Ejemplo clásico", h2="Dropbox (video)", q="Antes de escribir una línea de producto:", steps=["Hicieron un video de 3 min mostrando cómo funcionaría.","El video generó lista de espera de 75.000 personas.","Eso validó la demanda antes de construir."], meta="Un video fue el MVP. No hace falta código para validar interés.")),
   ("ejemplo", dict(kicker="Ejemplo clásico", h2="Zappos (concierge)", q="Antes de montar el e-commerce de zapatos:", steps=["El fundador fue a tiendas, sacó fotos y las subió a un sitio.","Cuando alguien compraba, él compraba el zapato y lo enviaba.","Eso validó que la gente compraría zapatos online."], meta="Cero inventario, cero sistema: solo validar la demanda.")),
   ("error", dict(kicker="Error típico", h2="Métricas de vanidad vs. accionables", warn="«10.000 visitas» no te dice nada si nadie compra. Medí lo que <b>cambia tu decisión</b>: % de conversión, retención, N de pedidos. Una métrica es útil solo si te hace decidir.")),
   ("lista", dict(kicker="La decisión", h2="Pivotar o perseverar", items=["<b>Perseverar:</b> la hipótesis se validó, sigue optimizando.","<b>Pivotar:</b> cambia un componente (segmento, canal, pricing) y re-testea.","Pivotar NO es fracasar: es aprender con datos."])),
   ("pasos", dict(kicker="La tarea", h2="Diseñá tu experimento", steps=[("Definí la hipótesis más riesgosa.",""),("Diseñá el MVP mínimo","para testearla."),("Definí la métrica","y el umbral de éxito/fracaso.")])),
   ("testeo", dict(kicker="El testeo", h2="Que sea refutable", big="Explicá qué métrica validaría o refutaría la hipótesis. Si nada puede refutarla, el experimento está mal diseñado.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("The Lean Startup (Ries)","http://theleanstartup.com"),("Running Lean (Maurya)","https://leanstack.com")])),
  ]))
CLASES.append(dict(curso=IN, n=7, fecha="Sáb 21 nov 2026", titulo="HITO · Presentá tu modelo disruptivo",
  lead="Defender tu modelo ante pares y convertí la crítica en iteración.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Tu modelo resiste una crítica?", big="La mitad del curso fue construir. Ahora viene la prueba: presentarlo y defenderlo ante pares que no te deben nada.")),
   ("lista", dict(kicker="Qué presentar", h2="Los 3 bloques", items=["<b>Canvas</b> completo (9 cajas).","<b>Curva de valor</b> (por qué es disruptiva).","<b>Hipótesis</b> y cómo pensás validarla."])),
   ("lista", dict(kicker="Estructura", h2="Una buena presentación de 4 min", items=["<b>Problema</b> (el job no resuelto).","<b>Insight</b> (qué descubriste del cliente).","<b>Solución</b> (tu modelo).","<b>Pedido</b> (qué feedback buscas)."])),
   ("error", dict(kicker="Error típico", h2="Defender en vez de escuchar", warn="La crítica no es un ataque: es <b>data gratis</b>. El que defiende su idea con uñas no aprende; el que anota el feedback, itera.")),
   ("pasos", dict(kicker="La tarea", h2="Presentá (4 min)", steps=[("Presentá","Canvas + curva + hipótesis."),("Recibí crítica","estructurada de los pares."),("Anotá por escrito","qué vas a cambiar.")])),
   ("testeo", dict(kicker="El testeo", h2="Iterá, no defiendas", big="Defiende el modelo ante preguntas duras y explicitá qué feedback vas a incorporar — no solo presentar, iterar.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Business Model Canvas","https://www.strategyzer.com/library/the-business-model-canvas")])),
  ]))
CLASES.append(dict(curso=IN, n=8, fecha="Sáb 28 nov 2026", titulo="Portafolio: Tres Horizontes + Ambition Matrix",
  lead="Organizar tus ideas en un portafolio equilibrado entre el hoy y el mañana.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Todas tus ideas son de hoy, o tienes apuestas de futuro?", big="Un portafolio sano mezcla lo que <b>hoy</b> da plata, lo <b>adyacente</b> y las <b>apuestas</b> de largo plazo. Todo de un solo tipo es un riesgo.")),
   ("definicion", dict(kicker="Concepto", h2="Tres Horizontes (McKinsey)", defn="<b>H1</b> core: defender y extender el negocio actual. <b>H2</b> emergente: construir el siguiente motor. <b>H3</b> transformacional: apostar a lo que aún no existe.", meta="Las empresas mueren cuando solo invierten en H1.")),
   ("lista", dict(kicker="Cada horizonte", h2="En detalle", items=["<b>H1 (hoy):</b> optimizar, defender margen, mejorar lo que ya funciona.","<b>H2 (1-3 años):</b> escalar lo que ya mostró tracción.","<b>H3 (3+ años):</b> explorar opciones, aceptar que la mayoría fallará."])),
   ("definicion", dict(kicker="Concepto", h2="Ambition Matrix", defn="Clasifica las iniciativas por <b>qué tan nuevo</b> es el producto y el mercado: core, adyacente o transformacional.", meta="La matriz deja ver si tu portafolio está desbalanceado.")),
   ("ejemplo", dict(kicker="Ejemplo", h2="Portafolio desbalanceado vs. sano", q="Dos casos:", steps=["Desbalanceado: 90% core, 10% adyacente, 0% transformacional → muere lento.","Sano: 70/20/10 (core/adyacente/transformacional).","El 10% transformacional es el que te salva en 5 años."], meta="No se trata de abandonar el core: se trata de no depender solo de él.")),
   ("pasos", dict(kicker="La tarea", h2="Ubicá tus ideas", steps=[("Poné cada idea","en la Ambition Matrix."),("Proyectala","en los Tres Horizontes."),("Detectá","si el portafolio está desbalanceado.")])),
   ("testeo", dict(kicker="El testeo", h2="El balance", big="Explicá el balance de tu portafolio y por qué tu idea es la apuesta transformacional correcta para el horizonte elegido.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Three Horizons (McKinsey)","https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/enduring-ideas-the-three-horizons-of-growth"),("Innovation Ambition Matrix (HBR)","https://hbr.org/2012/05/managing-your-innovation-portfolio")])),
  ]))
CLASES.append(dict(curso=IN, n=9, fecha="Sáb 05 dic 2026", titulo="Design Thinking + 101 Design Methods",
  lead="Idear de forma estructurada: empatizar, definir, idear, prototipar, testear.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Cómo idear sin quedarte con la primera idea obvia?", big="La primera idea casi siempre es la más mediocre. El design thinking fuerza <b>divergir</b> (muchas ideas) antes de <b>converger</b>.")),
   ("definicion", dict(kicker="Concepto", h2="Design Thinking", defn="Un método <b>centrado en el humano</b> para resolver problemas: entender al usuario antes de diseñar la solución.", meta="No es «hacer las cosas bonitas»: es asegurarse de resolver el problema correcto.")),
   ("loop", dict(kicker="El ciclo", h2="Las 5 fases", lead="No necesariamente lineales, se iteran:", nodes=[("💙 Empatizar","entender al usuario"),("🎯 Definir","el problema real"),("💡 Idear","divergir"),("🛠️ Prototipar","algo tangible"),("🧪 Testear","con usuario")], meta="El corazón es el test: un prototipo rápido que te enseña qué funciona.")),
   ("lista", dict(kicker="El doble diamante", h2="Divergir y converger", items=["<b>Divergir:</b> abrir (muchas ideas, sin juzgar).","<b>Converger:</b> cerrar (elegir con criterio).","El error clásico: converger demasiado pronto, con la primera idea."])),
   ("lista", dict(kicker="Cada fase", h2="En detalle", items=["<b>Empatizar:</b> entrevistas, observación, «un día en la vida de».","<b>Definir:</b> el insight en una frase («el usuario necesita X porque Y»).","<b>Idear:</b> cantidad sobre calidad, aplazar el juicio.","<b>Prototipar:</b> rápido y barato (papel, maqueta, sketch).","<b>Testear:</b> con usuario real, a aprender no a validar."])),
   ("error", dict(kicker="Error típico", h2="Prototipo bonito, aprendizaje cero", warn="No construyas un prototipo para impresionar: construilo para <b>aprender</b>. Un prototipo feo que te enseña algo vale más que uno pulido que no responde ninguna pregunta.")),
   ("pasos", dict(kicker="La tarea", h2="Un ciclo completo", steps=[("Empatizá","(entrevista u observación)."),("Definí","el problema en una frase."),("Ideá + prototipá","en baja fidelidad."),("Testeá","con un usuario real.")])),
   ("testeo", dict(kicker="El testeo", h2="Qué aprendiste", big="Mostrá el prototipo y qué aprendiste del test con un usuario real. Lo importante no es el prototipo, es lo que te enseñó.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Design Thinking (IDEO)","https://designthinking.ideo.com")])),
  ]))
CLASES.append(dict(curso=IN, n=10, fecha="Sáb 12 dic 2026", titulo="Von Hippel: fuentes de innovación + lead users",
  lead="La innovación no nace solo dentro de la empresa: los usuarios líderes la anticipan.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿De dónde vienen las mejores ideas?", big="No siempre del laboratorio. Muchas innovaciones nacen en los <b>usuarios</b> que sufren el problema antes que nadie y se arman su propia solución.")),
   ("definicion", dict(kicker="Concepto", h2="Lead users (usuarios líderes)", defn="Usuarios que enfrentan una necesidad <b>antes</b> que el mercado masivo y que, para resolverla, <b>ya improvisan soluciones</b>. Son tu radar.", meta="Si encuentras al lead user, encuentras la demanda futura antes que nadie.")),
   ("lista", dict(kicker="Características", h2="Cómo reconocer a un lead user", items=["Sufre el problema <b>hoy</b> (no en el futuro).","Ya <b>inventó</b> una solución casera o un parche.","Se <b>beneficia</b> mucho si el problema se resuelve bien.","Está <b>adelantado</b> a la tendencia del mercado."])),
   ("lista", dict(kicker="El proceso", h2="Lead User Method (4 pasos)", items=["<b>Identificar la tendencia</b> clave del mercado.","<b>Encontrar lead users</b> (foros, comunidades, power users).","<b>Workshop</b> con ellos para co-diseñar.","<b>Testear</b> el concepto resultante con el mercado."])),
   ("ejemplo", dict(kicker="Ejemplo", h2="La innovación nace en el usuario", q="Casos reales:", steps=["Mountain bike: ciclistas que modificaban sus bicis para el barro.","Surf: los surfistas inventaron mejoras antes que la industria.","Medicina: pacientes crónicos que diseñan sus propios dispositivos."], meta="La empresa llega DESPUÉS, a industrializar lo que el usuario ya improvisó.")),
   ("definicion", dict(kicker="Concepto", h2="Democratización (toolkits)", defn="Darle al usuario <b>herramientas</b> para que diseñe su propia solución (impresoras 3D, plataformas low-code).", meta="Cuando el costo de innovar baja, el usuario deja de ser solo consumidor: se vuelve co-creador.")),
   ("pasos", dict(kicker="La tarea", h2="Buscá tu lead user", steps=[("Identificá","quién sufre tu problema HOY y se arma soluciones propias."),("Describe","su perfil concreto (no «los jóvenes»)."),("Diseñá","cómo co-crear con ellos.")])),
   ("testeo", dict(kicker="El testeo", h2="Perfil real, no abstracción", big="Explicá quién es tu lead user concreto y cómo lo incorporás al desarrollo.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Eric von Hippel (MIT)","https://evhippel.mit.edu")])),
  ]))
CLASES.append(dict(curso=IN, n=11, fecha="Sáb 19 dic 2026", titulo="NABC pitch: vender la idea disruptiva",
  lead="Estructurar la idea en un pitch de 3 minutos que responda Need, Approach, Benefit, Competition.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Podés vender tu idea en 3 minutos?", big="Un directorio no te da media hora. Si no puedes explicar el valor en 3 minutos, no tienes clara la idea.")),
   ("definicion", dict(kicker="El método", h2="NABC (SRI International)", defn="Un pitch estructurado en 4 partes que obliga a ir al grano.", meta="Usado para evaluar ideas de inversión en SRI International, Stanford y Silicon Valley.")),
   ("lista", dict(kicker="Las 4 letras", h2="NABC", items=["<b>N</b>eed — la necesidad (el job no resuelto).","<b>A</b>pproach — tu abordaje distinto.","<b>B</b>enefit — el beneficio <b>cuantificable</b>.","<b>C</b>ompetition — por qué les ganas."])),
   ("lista", dict(kicker="Profundizar", h2="Cada letra bien hecha", items=["<b>Need:</b> un dolor concreto, no «mejorar la eficiencia».","<b>Approach:</b> en qué SOS distinto, no en qué sos bueno.","<b>Benefit:</b> números (tiempo, plata, cobertura).","<b>Competition:</b> qué hará el otro y por qué no le alcanza."])),
   ("error", dict(kicker="Error típico", h2="Beneficio sin números", warn="«Mejora la eficiencia» no vende nada. «Reduce 8 horas a 3 segundos y audita el 100%» sí. <b>El beneficio va en números.</b>")),
   ("lista", dict(kicker="Estructura", h2="El pitch de 3 min", items=["<b>0:00 Hook</b> — una frase que engancha.","<b>0:30 Need</b> — el dolor.","<b>1:00 Approach</b> — tu solución distinta.","<b>2:00 Benefit</b> — los números.","<b>2:30 Competition</b> — por qué ganas.","<b>3:00 Cierre</b> — qué pedís."])),
   ("pasos", dict(kicker="La tarea", h2="Armá tu pitch", steps=[("Escribí las 4 letras","en una frase cada una."),("Ensaya el pitch de 3 min.",""),("Que el beneficio","tenga números.")])),
   ("testeo", dict(kicker="El testeo", h2="Pitch de 3 min", big="Pitch que responde las 4 letras sin muletillas y con el beneficio en números.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Método NABC (SRI International)","https://www.sri.com")])),
  ]))
CLASES.append(dict(curso=IN, n=12, fecha="Sáb 09 ene 2027", titulo="Demo final: pitch + portafolio",
  lead="Presentar la idea disruptiva final con evidencia, ante un panel.",
  slides=[
   ("pregunta", dict(kicker="La pregunta", h2="¿Listo para defenderla ante un panel?", big="Cierre del curso: presentás la idea completa — no la idea «de la primera clase», sino la que sobrevivió a validación, feedback e iteración.")),
   ("lista", dict(kicker="Qué presentar", h2="El paquete completo", items=["<b>NABC</b> (pitch de 3 min).","<b>Modelo de negocio</b> (Canvas).","<b>Evidencia de validación</b> (entrevistas, prototipo, experimento).","<b>Portafolio</b> (dónde encaja tu idea)."])),
   ("error", dict(kicker="Error típico", h2="Presentar la idea de la clase 1", warn="Si tu idea final es la misma que tuviste en la clase 1, no aprendiste a iterar. El panel quiere ver <b>qué cambió</b> y por qué — qué mató la validación, qué sobrevivió.")),
   ("pasos", dict(kicker="La tarea", h2="Prepará la defensa", steps=[("Estructurá","NABC + Canvas + evidencia."),("Ensaya","el pitch final."),("Anticipá","las preguntas del panel.")])),
   ("testeo", dict(kicker="El testeo final", h2="Con evidencia real", big="Defiende la idea con evidencia real de cliente, no suposiciones. Importa que esté validada y sepan argumentarla — no una nota.")),
   ("links", dict(kicker="Para aprender", h2="Links", links=[("Método NABC (SRI International)","https://www.sri.com")])),
  ]))

os.chdir(os.path.dirname(os.path.abspath(__file__)))
hechos = 0
for c in CLASES:
    cu = c["curso"]
    key = "auditoria" if cu is AU else "innovacion"
    fn = f"{key}-{c['n']:02d}.html"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(deck(cu, cu, c["n"], c["fecha"], c["titulo"], c["lead"], c["slides"]))
    hechos += 1
    print(f"  {fn}  ({len(c['slides'])+1} slides)")
print(f"\n{hechos} decks con contenido generados.")

# ── DEEP DIVE: estado del arte Big 4 ──
B4 = {"nombre": "Hackeando la Auditoría con IA Agéntica", "short": "Auditoría IA Agéntica",
      "color": "#0a7a3d", "soft": "#eefaf1", "level": "Electivo IV",
      "plan": "auditoria-ia-agentica.html"}
B4_SLIDES = [
 ("pregunta", dict(kicker="La tesis", h2="¿Por qué las Big 4 invirtieron +US$10.000M en IA?", big="Porque el paradigma de la auditoría murió: revisar una muestra de 25 facturas ya no es auditar. Hoy se audita el <b>100% de las transacciones</b> con agentes de IA.")),
 ("definicion", dict(kicker="El cambio de paradigma", h2="El fin del muestreo selectivo (NIA 530)", defn="Durante un siglo, auditar fue <b>muestrear</b>: revisar 25 a 50 transacciones por cuenta y suponer que el resto estaba bien. Con millones de asientos, el <b>99,99% quedaba a ciegas</b>.", meta="Enron, Wirecard y Parmalat explotaron exactamente ese punto ciego.")),
 ("vs", dict(kicker="Dos mundos", h2="Auditoría tradicional vs. Big 4 de frontera", bad_t="Tradicional (siglo XX)", bad=["Post-mortem: revisión 3 meses después del cierre","Muestra de 25-60 facturas (5% de los datos)","Junior dedica 70% del tiempo a «ticking & tying»","Solo cifras contables históricas"], good_t="Big 4 (2025-2030)", good=["Auditoría continua, 100% del General Ledger en tiempo real","Agentes de IA cotejan contratos (IFRS 15/16) y bancos","Process Mining reconstruye el 100% de P2P y O2C","Triple aseguramiento: financiero + IA + ESG"])),
 ("piezas", dict(kicker="Las 4 plataformas", h2="El mapa tecnológico de las Big 4", piezas=[("PwC · Aura NextGen","Harvey AI + GL.ai. US$1.000M con OpenAI/Microsoft. 120.000 auditores."),("Deloitte · Omnia","Connected Agentic Intelligence. US$1.400M+ con NVIDIA/AWS/GCP."),("EY · Canvas","EY.ai + Canvas Analyzer. US$1.400M sobre Azure. 150 países."),("KPMG · Clara","Financial Report Analyzer + Substantive Agents. US$2.000M con Microsoft.")])),
 ("lista", dict(kicker="El detalle", h2="Qué hace cada plataforma", items=["<b>PwC:</b> Harvey lee miles de contratos (IFRS 16/15) y GL.ai detecta anomalías en miles de millones de asientos.","<b>Deloitte:</b> redes de agentes autónomos: conciliación bancaria, revisión documental y revelaciones (DART + GenAI).","<b>EY:</b> Canvas Analyzer visualiza el riesgo por división/país; Virtual Analytics vigila pagos, nómina y fraude.","<b>KPMG:</b> FRA compara estados financieros contra taxonomías IFRS al instante; dashboards Power BI todo el año."])),
 ("lista", dict(kicker="El corazón", h2="Las 6 innovaciones disruptivas", items=["<b>1. Full-population testing:</b> auditar el 100% del ledger, no una muestra.","<b>2. Agentes sustantivos:</b> three-way matching autónomo + extracción de contratos.","<b>3. Process mining:</b> reconstruir el 100% de los flujos P2P/O2C (SOX 404).","<b>4. ESG:</b> aseguramiento CSRD/ISSB y NCG 461/519.","<b>5. Forense con grafos:</b> partes relacionadas ocultas y deepfakes.","<b>6. Auditar la IA:</b> gobernanza de algoritmos (EU AI Act / NIST RMF)."])),
 ("definicion", dict(kicker="Innovación 1", h2="Full-population testing", defn="Se extrae el <b>100% de los asientos</b> del ERP (SAP, Oracle, Dynamics). Cada asiento recibe un <b>Anomaly Score</b>: hora rara (3 AM), usuario inusual (el CFO contabilizando directo), pagos justo bajo el umbral (smurfing) o contrapartidas cruzadas.", meta="El auditor ya no muestrea: filtra el 0,1% más anómalo y lo investiga a fondo.")),
 ("loop", dict(kicker="Innovación 2", h2="El agente sustantivo (three-way matching)", lead="Lo que hacía un junior en horas, un agente lo hace en segundos:", nodes=[("📄 Extraer","factura + OC + recepción + cartola"),("⚖️ Validar","cantidad, precio, impuestos al 100%"),("🚨 Escalar","98% conforme · 2% al senior"),("🧾 Registrar","papel de trabajo con evidencia")], meta="98% de transacciones conformes se archivan solas; el 2% sube con hallazgo detallado.")),
 ("ejemplo", dict(kicker="Innovación 3", h2="Process mining (SOX 404)", q="En vez de entrevistar al contador y probar 2 transacciones:", steps=["<b>Reconstruye</b> el 100% de P2P y O2C desde los event logs del ERP.","<b>Revela</b> +300 variaciones reales del proceso (no las 5 del manual).","<b>Detecta</b> segregación de funciones violada y maverick buying.","<b>Alerta</b> cambio de cuenta bancaria de proveedor + pago millonario en 48h."])),
 ("porque", dict(kicker="Innovación 4", h2="ESG: auditar carbono, agua y derechos", big="La auditoría ya no es solo dinero. Con <b>NCG 519</b>, desde el <b>ejercicio 2026</b> los emisores chilenos reportan IFRS S1/S2 (emisiones, clima) — y eso se audita.", meta="Doble materialidad: impacto del clima en la empresa Y de la empresa en el ambiente.")),
 ("lista", dict(kicker="Innovación 5", h2="Forense: grafos y deepfakes", items=["<b>Grafos:</b> cruzan direcciones, teléfonos, correos y cuentas para destapar empresas fantasma y conflictos de interés.","<b>Deepfake del CEO:</b> clonan voz y video del gerente para ordenar transferencias millonarias.","<b>Control:</b> verificación criptográfica fuera de banda para pagos extraordinarios."])),
 ("lista", dict(kicker="Innovación 6", h2="Auditar la IA (AI Governance)", items=["<b>Bias:</b> ¿el scoring de crédito discrimina por género o código postal?","<b>Explicabilidad:</b> ¿puedes explicar por qué el algoritmo rechazó un crédito?","<b>Alucinación:</b> guardrails para que la IA no invente cifras en reportes.","<b>Prompt injection:</b> ¿el sistema puede ser engañado para liberar pagos?","<b>Privacidad:</b> ¿el modelo filtra datos personales?"])),
 ("porque", dict(kicker="En Chile", h2="El calendario que te toca a ti", big="<b>NCG 461</b> (memorias integradas) ya rige. <b>NCG 519</b> obliga a converger con ISSB (IFRS S1/S2) desde el <b>ejercicio 2026</b>, reportes en 2027.", meta="Las empresas IPSA ya contratan aseguramiento ESG voluntario para inversionistas como BlackRock.")),
 ("lista", dict(kicker="El negocio", h2="ROI: de 2.380 a 1.020 horas (-57%)", items=["<b>Planificación y mapeo:</b> 250 → 90 HH (-64%)","<b>Pruebas de control:</b> 400 → 120 HH (-70%)","<b>Vouching mecánico:</b> 900 → 150 HH (-83%)","<b>Confirmaciones:</b> 180 → 30 HH (-83%)","<b>Contratos IFRS 15/16:</b> 350 → 80 HH (-77%)","<b>Juicio profesional:</b> 300 → 550 HH (+83%: más valor, menos mecánica)"])),
 ("lista", dict(kicker="El retorno", h2="Los 4 ROI para la empresa auditada", items=["<b>Menos «audit fatigue»:</b> -75% de interrupción al equipo contable.","<b>Fugas y fraude:</b> el 100% del ledger detecta lo que la muestra de 25 no veía.","<b>Menos restatements:</b> -80% de probabilidad de corregir balances públicos.","<b>Comité de auditoría:</b> dashboards de calor, no PDF de 80 páginas."])),
 ("pasos", dict(kicker="La gobernanza", h2="Tres líneas de defensa (IIA)", steps=[("1ª línea — Gerencia:","responsable de la calidad del data lake y del monitoreo continuo."),("2ª línea — Riesgo/Cumplimiento:","aprueba y supervisa controles y reportabilidad ESG."),("3ª línea — Auditoría Interna:","aseguramiento de algoritmos e IA del negocio."),("Big 4 — Asegurador externo:","full-population testing y opinión de auditoría.")])),
 ("porque", dict(kicker="La conclusión", h2="Qué significa para ti", big="El auditor deja de ser <b>operador</b> (pegar datos, muestrear) y pasa a ser <b>supervisor de sistemas agénticos</b>: define qué controlar, revisa lo que el agente marcó y aporta juicio donde importa.", meta="Eso es exactamente lo que vas a construir en las próximas clases.")),
 ("testeo", dict(kicker="El testeo", h2="Demuestra que entendiste el cambio", big="Explica en 60 segundos: por qué el muestreo murió, qué hace un agente sustantivo y qué cambia con la NCG 519 en Chile.", meta="Si puedes explicarlo sin leer, entendiste el mapa de la auditoría que viene.")),
 ("links", dict(kicker="Para profundizar", h2="Links", links=[("Dashboard interactivo Big 4 (simulador ROI)","https://vvilche.github.io/auditoria-big4-innovacion/"),("Informe completo (Estado del Arte)","https://github.com/vvilche/auditoria-big4-innovacion"),("Plan de clases del curso","auditoria-ia-agentica.html"),("Ley 21.595 — Delitos Económicos","https://www.bcn.cl/leychile/navegar?idNorma=1195119")])),
]
with open("auditoria-big4.html", "w", encoding="utf-8") as f:
    f.write(deck(B4, B4, 0, "Estado del arte · Deep dive",
                 "El estado del arte: la revolución de las Big 4",
                 "PwC, Deloitte, EY y KPMG redefinieron la auditoría con IA agéntica, process mining y ESG. Este es el mapa de lo que vas a construir este semestre.",
                 B4_SLIDES))
print(f"  auditoria-big4.html  ({len(B4_SLIDES)+1} slides, deep dive)")
