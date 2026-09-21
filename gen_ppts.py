#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los slide decks (PPT embebidas en HTML) de los cursos USACH desde una data declarativa.
Regla (skill curso-ppt-html): todo curso = una PPT por clase, HTML autocontenido en GitHub Pages.
Regenerar: editar CLASES y re-correr. Determinista, cero tokens.
"""
import html, os

CURSOS = {
    "auditoria":  {"nombre": "Hackeando la Auditoría con IA Agéntica", "short": "Auditoría IA Agéntica", "color": "#0a7a3d"},
    "innovacion": {"nombre": "Innovación: Ideas Disruptivas para el Éxito", "short": "Innovación Disruptiva", "color": "#2456a5"},
}

# n, fecha, titulo, objetivo, conceptos[], tarea, testeo, links[(label,url)]
CLASES = [
# ── AUDITORÍA ────────────────────────────────────────────────────────────────
dict(curso="auditoria", n=1, fecha="Jue 24 sep 2026", titulo="De ChatGPT al agente autónomo",
  objetivo="Distinguir IA conversacional de agéntica y correr tu primer agente que ejecuta una tarea de verdad.",
  conceptos=["IA conversacional vs agéntica", "El loop: pensar → actuar → observar", "Un agente ejecuta; no solo responde"],
  tarea="En parejas: crear venv, instalar el stack y correr un agente mínimo (CrewAI o eve) que recibe un CSV y ejecuta una acción (contar filas, sumar una columna).",
  testeo="El agente corre en pantalla y la pareja explica las 3 fases del loop: qué pensó, qué hizo, qué observó.",
  links=[("Building Effective Agents (Anthropic)", "https://www.anthropic.com/research/building-effective-agents"),
         ("eve — framework de agentes (Vercel)", "https://github.com/vercel/eve"),
         ("CrewAI docs", "https://docs.crewai.com")]),
dict(curso="auditoria", n=2, fecha="Jue 01 oct 2026", titulo="Agente lector de documentos",
  objetivo="Hacer que tu agente lea un PDF (un balance) y extraiga cifras estructuradas sin inventarlas.",
  conceptos=["Extracción determinista (no LLM para las cifras)", "PyMuPDF para leer PDFs", "El LLM formatea; no inventa números"],
  tarea="El agente abre un balance real (PDF), extrae las cuentas principales y las entrega en una tabla.",
  testeo="La tabla cuadra contra el PDF (activo = pasivo + patrimonio). Si no cuadra, es error de extracción.",
  links=[("PyMuPDF", "https://pymupdf.readthedocs.io"),
         ("CrewAI — tools", "https://docs.crewai.com")]),
dict(curso="auditoria", n=3, fecha="Jue 08 oct 2026", titulo="RAG: la memoria del agente",
  objetivo="Entender por qué el agente necesita recuperación (y no meter todo al prompt) y armar un mini-RAG.",
  conceptos=["Embeddings + búsqueda vectorial", "Chunking: partir el texto en trozos", "Índice FAISS + dedup"],
  tarea="Chunkear 10 documentos, embeber con fastembed, indexar en FAISS y consultar: el agente responde solo con lo recuperado.",
  testeo="El agente responde y muestra la fuente (qué chunk usó). Si no está en el corpus, dice «no está».",
  links=[("Qué es RAG", "https://www.pinecone.io/learn/retrieval-augmented-generation/"),
         ("Vector embeddings", "https://www.pinecone.io/learn/vector-embeddings/"),
         ("fastembed", "https://github.com/qdrant/fastembed"),
         ("FAISS", "https://github.com/facebookresearch/faiss")]),
dict(curso="auditoria", n=4, fecha="Jue 15 oct 2026", titulo="HITO L1 · Agente lector de balances",
  objetivo="Integrar extracción + RAG en un agente que lee un balance y responde con fuente.",
  conceptos=["Integración: extracción + índice + respuesta", "Grounding: citar la fuente", "El agente dice «no está» cuando no tiene la respuesta"],
  tarea="Integrar las clases 1–3 en un solo agente: lee un balance, lo indexa y responde preguntas citando la fuente.",
  testeo="Demo de 2 min por pareja + prueba de fuego: una pregunta cuya respuesta NO está en el balance → el agente debe declararlo.",
  links=[("Cómo hacer un agente confiable", "https://www.anthropic.com/research/building-effective-agents"),
         ("RAG con grounding", "https://www.pinecone.io/learn/grounded-rag/")]),
dict(curso="auditoria", n=5, fecha="Jue 22 oct 2026", titulo="El problema real: conciliación SII vs ERP",
  objetivo="Entender el dolor real del auditor (conciliar facturas vs registro) y dónde viven los datos del SII.",
  conceptos=["Factura electrónica del SII", "Conciliación: facturas vs registro", "Ley 21.595 de Delitos Económicos"],
  tarea="Recorrer el mapa de fuentes contables chilenas (SII, CMF, LeyChile) y armar un dataset de facturas de ejemplo listo para conciliar.",
  testeo="Explicar dónde vive cada dato del SII y por qué conciliar 1.000 facturas a mano es trabajo de 8 horas que un agente hace en segundos.",
  links=[("SII (factura electrónica)", "https://www.sii.cl"),
         ("Ley 21.595 — Delitos Económicos", "https://www.bcn.cl/leychile/navegar?idNorma=1195119"),
         ("CMF", "https://www.cmfchile.cl"),
         ("Mapa de fuentes contables", "mapa-fuentes-contables.html")]),
dict(curso="auditoria", n=6, fecha="Jue 29 oct 2026", titulo="Bajar datos del SII (ingestor, sin LLM)",
  objetivo="Construir un ingestor en Python que baja normativa del SII de forma determinista (cero tokens de LLM).",
  conceptos=["Ingesta determinista vs resumir con IA", "API XML de LeyChile", "Deduplicar por hash antes de embeber"],
  tarea="Correr el ingestor de ejemplo: bajar una ley vía API XML de LeyChile y una circular del SII, extraer texto limpio y deduplicar.",
  testeo="Cada pareja trae una fuente real bajada y muestra el texto limpio + confirma que la ingesta es Python puro.",
  links=[("LeyChile (API de normas)", "https://www.leychile.cl"),
         ("Circulares SII 2025", "https://www.sii.cl/normativa_legislacion/circulares/2025/indcir2025.htm"),
         ("Ingestor de ejemplo", "ingestor_store_b.py")]),
dict(curso="auditoria", n=7, fecha="Jue 05 nov 2026", titulo="Detección de fraude + Ley 21.595",
  objetivo="Construir reglas de detección de facturas truchas y alertas automáticas.",
  conceptos=["Reglas deterministas (no ML)", "Señales: duplicados, RUT inválido, montos raros", "Cada alerta ligada a un artículo de la Ley 21.595"],
  tarea="Escribir reglas que marquen facturas duplicadas, montos sospechosos, RUT inválido y fechas inconsistentes. Ligar cada alerta a un artículo.",
  testeo="Sobre un dataset con trampas plantadas, detectar las facturas truchas y decir qué artículo de la Ley 21.595 se viola en cada caso.",
  links=[("Ley 21.595 (artículos)", "https://www.bcn.cl/leychile/navegar?idNorma=1195119"),
         ("Tribunales Tributarios (casos reales)", "https://www.tta.cl")]),
dict(curso="auditoria", n=8, fecha="Jue 19 nov 2026", titulo="HITO L2 · Auditoría en vivo a 1.000 transacciones",
  objetivo="Tu agente concilia 1.000 facturas SII vs ERP en segundos y marca las discrepancias.",
  conceptos=["Conciliación masiva", "Reporte de discrepancias (monto, folio, proveedor)", "Medir el tiempo total"],
  tarea="Correr la conciliación completa: dataset SII vs ERP simulado, marcar discrepancias y generar reporte. Medir el tiempo.",
  testeo="En vivo, el agente marca las facturas truchas en segundos, con el tiempo en pantalla, y la pareja explica cada discrepancia.",
  links=[("SII", "https://www.sii.cl"),
         ("Ley 21.595", "https://www.bcn.cl/leychile/navegar?idNorma=1195119")]),
dict(curso="auditoria", n=9, fecha="Jue 26 nov 2026", titulo="Cero alucinación: spec-first (spec-kit)",
  objetivo="Escribir una especificación rígida de QUÉ debe hacer el agente antes de codificar.",
  conceptos=["Por qué los LLM alucinan", "Spec-first: definir antes de codificar", "La spec prohíbe inventar artículos/plazos"],
  tarea="Escribir la spec de una tarea («cuadrar la conciliación al centavo, citando la norma vigente, prohibido inventar») y que el agente la ejecute.",
  testeo="Prueba adversarial: pedir un artículo que no existe → el agente dice «no está en la norma», no inventa el «Artículo 999».",
  links=[("spec-kit (Spec-Driven Development)", "https://github.com/github/spec-kit"),
         ("Por qué un RAG alucina", "https://www.pinecone.io/learn/rag-hallucinations/")]),
dict(curso="auditoria", n=10, fecha="Jue 03 dic 2026", titulo="Guardrails: Zod + Graft",
  objetivo="Blindar el agente con validación de datos (Zod) y mapeo del ERP (Graft).",
  conceptos=["Guardrails de datos", "Schema Zod de la factura", "Graft: grafo de código para no perderse"],
  tarea="Definir el schema Zod de una factura (campos, tipos, reglas) y mapear la estructura del ERP con Graft.",
  testeo="El agente rechaza una transacción que no cuadra y explica qué regla del schema la frenó.",
  links=[("Zod", "https://zod.dev"),
         ("Pydantic", "https://docs.pydantic.dev"),
         ("Graft (grafo de código)", "https://github.com/NanoNets/graft")]),
dict(curso="auditoria", n=11, fecha="Jue 10 dic 2026", titulo="HITO L3 · Blindaje al centavo + evaluación",
  objetivo="Tu agente cuadra al centavo sin alucinar y sabes MEDIRLO con un set de evaluación.",
  conceptos=["Recall / precision / MRR", "Faithfulness / groundedness", "Batería adversarial"],
  tarea="Armar un set de evaluación (10+ consultas con respuesta esperada) y medir recall/precision del retrieval + faithfulness.",
  testeo="Pasar la batería adversarial (falsas premisas, typos, prompt injection) y que el agente responda con fuente o declare «no está».",
  links=[("Evaluar un RAG", "https://www.pinecone.io/learn/rag-evaluation/"),
         ("Faithfulness / groundedness", "https://www.pinecone.io/learn/rag-faithfulness/")]),
dict(curso="auditoria", n=12, fecha="Jue 17 dic 2026", titulo="Hackathon: el Swarm multi-agente",
  objetivo="Orquestar varios agentes (extractor, conciliador, caza-fraudes) que colaboran en un flujo.",
  conceptos=["Orquestación multi-agente", "División de tareas entre agentes", "Flujo end-to-end"],
  tarea="En equipos, orquestar 2–3 agentes que se pasan el trabajo: uno extrae, otro concilia, otro detecta fraude y alerta.",
  testeo="El swarm ejecuta el flujo completo (factura → conciliación → alerta) sin intervención manual entre pasos.",
  links=[("Patrones multi-agente (Anthropic)", "https://www.anthropic.com/research/building-effective-agents"),
         ("CrewAI — crews multi-agente", "https://docs.crewai.com")]),
dict(curso="auditoria", n=13, fecha="Jue 07 ene 2027", titulo="Demo final / Executive Pitch",
  objetivo="Presentar tu sistema agéntico de auditoría como si fuera a un directorio.",
  conceptos=["Pitch ejecutivo: problema, solución, impacto", "Demo en vivo", "Defender el sistema ante preguntas"],
  tarea="Cada equipo presenta su Swarm UFAS: pitch + demo en vivo del sistema auditando.",
  testeo="Ante panel, el sistema responde con fuente, cuadra al centavo y defiende sus alertas. Importa que funcione y lo sepan explicar.",
  links=[("eve (deploy del swarm)", "https://github.com/vercel/eve"),
         ("CrewAI", "https://docs.crewai.com")]),
# ── INNOVACIÓN ───────────────────────────────────────────────────────────────
dict(curso="innovacion", n=1, fecha="Sáb 26 sep 2026", titulo="¿Qué es innovar de verdad? Disrupción vs mejora",
  objetivo="Distinguir disrupción de mejora incremental e identificar un «job to be done» no satisfecho.",
  conceptos=["El dilema del innovador (Christensen)", "Jobs to be Done", "Disrupción ≠ mejora incremental"],
  tarea="En parejas, elegir un mercado real y redactar el «job to be done» que hoy se resuelve mal. No proponer solución todavía.",
  testeo="Explicar por qué su idea es disruptiva (segmento ignorado u otra forma de hacer el trabajo), no una mejora incremental del líder.",
  links=[("Christensen — The Innovator's Dilemma", "https://www.claytonchristensen.com"),
         ("Jobs to be Done (Alan Klement)", "https://jtbd.info")]),
dict(curso="innovacion", n=2, fecha="Sáb 03 oct 2026", titulo="Océano Azul: crear mercados sin competencia",
  objetivo="Usar la curva de valor (eliminar-reducir-elevar-crear) para redefinir un mercado.",
  conceptos=["Estrategia del Océano Azul", "La curva de valor", "Eliminar · Reducir · Elevar · Crear"],
  tarea="Dibujar la curva de valor de su idea y compararla contra la del competidor típico.",
  testeo="Su curva redefine los factores (al menos uno que la industria da por sentado), no es una copia desplazada.",
  links=[("Blue Ocean Strategy (Kim & Mauborgne)", "https://www.blueoceanstrategy.com")]),
dict(curso="innovacion", n=3, fecha="Sáb 10 oct 2026", titulo="Modelo de negocio: Canvas + 4 cajas",
  objetivo="Diseñar el modelo de negocio con el Canvas (9 cajas) y las 4 cajas de Johnson.",
  conceptos=["Business Model Canvas (9 cajas)", "Las 4 cajas de Johnson", "Crear, entregar y capturar valor"],
  tarea="Llenar las 9 cajas del Canvas para su idea e identificar las 2 cajas más débiles (supuestos críticos).",
  testeo="Explicar en 60 segundos cómo su modelo crea, entrega y captura valor, y cuáles son sus 2 supuestos más arriesgados.",
  links=[("Business Model Canvas", "https://www.strategyzer.com/library/the-business-model-canvas"),
         ("Las 4 cajas de Johnson (HBR)", "https://hbr.org/2008/12/reinventing-your-business-model")]),
dict(curso="innovacion", n=4, fecha="Sáb 17 oct 2026", titulo="Patrones: 55 patrones + 10 tipos de innovación",
  objetivo="Generar variantes de tu modelo usando patrones sistemáticos, no solo inspiración.",
  conceptos=["55 patrones (Gassmann)", "10 tipos de innovación (Doblin)", "Patrones → modelos alternativos"],
  tarea="Aplicar al menos 3 patrones a su modelo base y producir 2 modelos alternativos (no variaciones cosméticas).",
  testeo="Los 2 modelos nuevos son genuinamente distintos y pueden decir qué patrón los generó.",
  links=[("Business Model Navigator (55 patrones)", "https://www.businessmodelnavigator.com"),
         ("Ten Types of Innovation (Doblin)", "https://doblin.com/ten-types")]),
dict(curso="innovacion", n=5, fecha="Sáb 24 oct 2026", titulo="Propuesta de valor + Customer Development",
  objetivo="Diseñar la propuesta de valor y salir a validar el dolor del cliente real.",
  conceptos=["Value Proposition Canvas", "Customer Development", "Entrevistas de descubrimiento"],
  tarea="Llenar el Value Proposition Canvas y redactar un guión de entrevista (mínimo 5 preguntas que validen el dolor).",
  testeo="El encaje problema-solución con evidencia de cliente (al menos 1 entrevista hecha), no con opinión propia.",
  links=[("Value Proposition Design", "https://www.strategyzer.com/library/value-proposition-design"),
         ("Customer Development (Steve Blank)", "https://steveblank.com")]),
dict(curso="innovacion", n=6, fecha="Sáb 07 nov 2026", titulo="Lean Startup + MVP",
  objetivo="Diseñar un MVP y un experimento medible para validar tu hipótesis más riesgosa.",
  conceptos=["Build-Measure-Learn", "MVP mínimo viable", "Hipótesis falsable"],
  tarea="Definir la hipótesis más riesgosa, el MVP mínimo para testearla y el experimento (métrica, plazo, umbral).",
  testeo="Explicar qué métrica validaría o refutaría la hipótesis. Si nada puede refutarla, el experimento está mal diseñado.",
  links=[("The Lean Startup (Ries)", "http://theleanstartup.com"),
         ("Running Lean (Maurya)", "https://leanstack.com")]),
dict(curso="innovacion", n=7, fecha="Sáb 21 nov 2026", titulo="HITO mitad · Presenta tu modelo disruptivo",
  objetivo="Presentar tu modelo disruptivo a pares y defenderlo ante crítica constructiva.",
  conceptos=["Presentación en 4 min", "Crítica estructurada", "Iterar con feedback"],
  tarea="Presentar el modelo (Canvas + curva de valor + hipótesis) en 4 min y anotar qué van a cambiar.",
  testeo="Defender el modelo ante preguntas duras y explicitar qué feedback van a incorporar — no solo presentar, iterar.",
  links=[("Business Model Canvas", "https://www.strategyzer.com/library/the-business-model-canvas")]),
dict(curso="innovacion", n=8, fecha="Sáb 28 nov 2026", titulo="Portafolio: Tres Horizontes + Ambition Matrix",
  objetivo="Organizar tus ideas en un portafolio de innovación (core / adyacente / transformacional).",
  conceptos=["Tres horizontes de crecimiento", "Innovation Ambition Matrix", "Balance del portafolio"],
  tarea="Ubicar sus ideas en la Ambition Matrix y los Tres Horizontes, e identificar si el portafolio está desbalanceado.",
  testeo="Explicar el balance de su portafolio y por qué su idea es la apuesta transformacional correcta.",
  links=[("Three Horizons (McKinsey)", "https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/enduring-ideas-the-three-horizons-of-growth"),
         ("Innovation Ambition Matrix (HBR)", "https://hbr.org/2012/05/managing-your-innovation-portfolio")]),
dict(curso="innovacion", n=9, fecha="Sáb 05 dic 2026", titulo="Design Thinking + 101 Design Methods",
  objetivo="Idear de forma estructurada (empatizar → definir → idear → prototipar → testear).",
  conceptos=["Ciclo de design thinking", "Métodos de Kumar (101 Design Methods)", "Prototipo de baja fidelidad"],
  tarea="Aplicar un ciclo completo de design thinking a un sub-problema: empatizar, definir, idear y prototipar.",
  testeo="El prototipo + qué aprendieron del test con un usuario real. Importa lo que enseñó, no que sea bonito.",
  links=[("Design Thinking (IDEO)", "https://designthinking.ideo.com")]),
dict(curso="innovacion", n=10, fecha="Sáb 12 dic 2026", titulo="Von Hippel: fuentes de innovación + lead users",
  objetivo="Identificar usuarios líderes y fuentes de innovación fuera de la empresa.",
  conceptos=["Lead users", "Democratización de la innovación", "Co-creación con usuarios"],
  tarea="Identificar los lead users de su mercado (los que ya sufren el problema y se arman soluciones propias) y diseñar la co-creación.",
  testeo="Explicar quién es su lead user concreto y cómo lo incorporan — un perfil real, no una abstracción.",
  links=[("Eric von Hippel (MIT)", "https://evhippel.mit.edu")]),
dict(curso="innovacion", n=11, fecha="Sáb 19 dic 2026", titulo="NABC pitch: vender la idea disruptiva",
  objetivo="Estructurar tu idea en un pitch NABC (Need-Approach-Benefit-Competition) y ensayarlo.",
  conceptos=["Need — la necesidad", "Approach — el abordaje distinto", "Benefit — beneficio cuantificable", "Competition — por qué ganas"],
  tarea="Armar el pitch NABC y ensayar el pitch de 3 min.",
  testeo="Pitch de 3 min que responde las 4 letras sin muletillas y con el beneficio en números.",
  links=[("Método NABC (SRI International)", "https://www.sri.com")]),
dict(curso="innovacion", n=12, fecha="Sáb 09 ene 2027", titulo="Demo final: pitch + portafolio",
  objetivo="Presentar tu idea disruptiva final ante un panel, con el portafolio completo.",
  conceptos=["Pitch final", "Evidencia de validación", "Portafolio de innovación"],
  tarea="Cada equipo presenta: NABC + modelo de negocio + evidencia de validación (entrevistas, prototipo, experimento) + portafolio.",
  testeo="Defender la idea con evidencia real de cliente, no suposiciones. Importa que esté validada y sepan argumentarla.",
  links=[("Método NABC (SRI International)", "https://www.sri.com")]),
]

def esc(s):
    return html.escape(s, quote=False)

def deck(c):
    cu = CURSOS[c["curso"]]
    color = cu["color"]
    conceptos = "".join(f"<li>{esc(x)}</li>" for x in c["conceptos"])
    links = "".join(f'<li><a href="{esc(l[1])}" target="_blank">{esc(l[0])}</a></li>' for l in c["links"])
    titulo = esc(c["titulo"])
    objetivo = esc(c["objetivo"])
    tarea = esc(c["tarea"])
    testeo = esc(c["testeo"])
    fecha = esc(c["fecha"])
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Clase {c['n']} · {titulo}</title>
<style>
:root{{--bg:#f8fafc;--card:#fff;--ink:#0f172a;--mut:#475569;--line:#e2e8f0;--acc:{color};}}
*{{box-sizing:border-box}}
html,body{{margin:0;height:100%}}
body{{font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--ink);}}
.deck{{max-width:920px;margin:0 auto;height:100vh;display:flex;flex-direction:column;padding:0 20px;}}
header{{display:flex;justify-content:space-between;align-items:center;padding:14px 2px;color:var(--mut);font-size:13px;border-bottom:1px solid var(--line);}}
header .curso{{font-weight:700;color:var(--acc);}}
main{{flex:1;display:flex;align-items:center;justify-content:center;}}
.slide{{display:none;width:100%;max-width:760px;animation:in .25s ease;}}
.slide.active{{display:block;}}
@keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.kicker{{color:var(--acc);font-weight:700;font-size:14px;text-transform:uppercase;letter-spacing:.06em;}}
.slide h1{{font-size:40px;margin:10px 0 6px;letter-spacing:-.02em;line-height:1.15;}}
.slide h2{{font-size:26px;margin:0 0 16px;letter-spacing:-.01em;}}
.curso-name{{color:var(--mut);font-size:16px;}}
.big{{font-size:24px;line-height:1.4;color:var(--ink);}}
.slide p{{font-size:19px;line-height:1.5;color:var(--mut);margin:0;}}
.slide ul{{padding-left:22px;margin:0;}}
.slide li{{font-size:19px;line-height:1.6;margin:8px 0;color:var(--mut);}}
.slide .links li a{{color:var(--acc);font-size:19px;}}
footer{{display:flex;justify-content:space-between;align-items:center;padding:14px 2px;border-top:1px solid var(--line);}}
footer button{{background:var(--acc);color:#fff;border:0;border-radius:8px;width:44px;height:44px;font-size:20px;cursor:pointer;}}
footer button:disabled{{opacity:.3;cursor:default;}}
.counter{{color:var(--mut);font-size:13px;}}
</style></head>
<body><div class="deck">
<header><span class="curso">{esc(cu['short'])}</span><span class="counter">Clase {c['n']} · {fecha}</span></header>
<main>
  <section class="slide active"><div class="kicker">Clase {c['n']} · {fecha}</div><h1>{titulo}</h1><p class="curso-name">{esc(cu['nombre'])}</p></section>
  <section class="slide"><h2>Al salir sabes…</h2><p class="big">{objetivo}</p></section>
  <section class="slide"><h2>Conceptos clave</h2><ul>{conceptos}</ul></section>
  <section class="slide"><h2>La tarea</h2><p>{tarea}</p></section>
  <section class="slide"><h2>El testeo</h2><p>{testeo}</p></section>
  <section class="slide"><h2>Para aprender</h2><ul class="links">{links}</ul></section>
  <section class="slide"><h2>A practicar</h2><p>En parejas: deja funcionando la tarea de hoy y anota una duda para la próxima clase.</p></section>
</main>
<footer><button id="prev">←</button><span class="counter" id="cnt">1 / 7</span><button id="next">→</button></footer>
</div>
<script>
var s=document.querySelectorAll('.slide'),i=0,n=s.length,cnt=document.getElementById('cnt');
function go(x){{s[i].classList.remove('active');i=(x+n)%n;s[i].classList.add('active');cnt.textContent=(i+1)+' / '+n;document.getElementById('prev').disabled=i===0;document.getElementById('next').disabled=i===n-1;}}
document.getElementById('prev').onclick=function(){{go(i-1)}};
document.getElementById('next').onclick=function(){{go(i+1)}};
document.addEventListener('keydown',function(e){{if(e.key==='ArrowRight'||e.key===' '){{go(i+1)}}else if(e.key==='ArrowLeft'){{go(i-1)}}}});
</script>
</body></html>"""

os.chdir(os.path.dirname(os.path.abspath(__file__)))
hechos = 0
for c in CLASES:
    fn = f"{c['curso']}-{c['n']:02d}.html"
    with open(fn, "w", encoding="utf-8") as f:
        f.write(deck(c))
    hechos += 1
    print(f"  {fn}")
print(f"\n{hechos} decks generados.")
