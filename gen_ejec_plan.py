#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera ejecutivos-ia-agentica.html — plan de clases del curso ejecutivo.

Toma el <style> del plan de Auditoria (misma familia visual) y lo reescribe con la
paleta cobre del curso nuevo. NO hereda CSS de banners ni de piezas que no aplican
(se cortan por clase antes de usarse).

Determinista, cero tokens de LLM.
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)

FUENTE = "auditoria-ia-agentica.html"
SALIDA = "ejecutivos-ia-agentica.html"

src = open(FUENTE, encoding="utf-8").read()
m = re.search(r"<style>(.*?)</style>", src, re.S)
assert m, "no se encontro <style> en el plan fuente"
CSS = m.group(1)

# paleta: el plan hereda el verde de Auditoria; este curso usa cobre
CSS = CSS.replace("--acc:#2563eb;--acc2:#0a7a3d", "--acc:#7a2e0e;--acc2:#7a2e0e")
CSS = CSS.replace("background:#eefaf1;color:var(--acc2);border:1px solid #c8ecd4",
                  "background:#fdf3ec;color:var(--acc2);border:1px solid #f0d9c8")
# cortar reglas huerfanas de piezas que este plan no tiene
CSS = "\n".join(l for l in CSS.splitlines() if "banner-" not in l and "tag-insumo" not in l)

CLASES = [
 # (n, titulo, objetivo, bloques, tarea, testeo)
 (1, "Qué es un agente (y qué no)",
  "Distinguir IA conversacional de IA agéntica, con las cifras del mercado sobre la mesa: por qué el 88% de las empresas usa IA y solo un 6% puede atribuirle un impacto significativo al resultado.",
  [("20'", "Apertura: el dato que incomoda — 88% usa IA, 6% ve el impacto, 95% de los pilotos sin retorno", ""),
   ("35'", "Concepto: objetivo, herramientas, memoria y el ciclo del agente", ""),
   ("60'", "TAREA: mapear qué tareas de su cargo son delegables y cuáles no", "tarea"),
   ("30'", "TESTEO: distinguir conversación de ejecución, en vivo", "testeo"),
   ("15'", "Cierre: el mapa de las 12 clases", "")],
  "Cada participante elige tres tareas de su propio cargo y las clasifica: (a) la hace una persona, (b) la puede preparar un agente y la firma una persona, (c) la puede ejecutar un agente solo. Debe justificar el criterio de cada una. Los datos del mapeo son de su trabajo real — la base del plan de 90 días de la clase 12.",
  "Demostrar que distingue los tres tipos de tarea y que el criterio de clasificación es explícito, no intuitivo."),

 (2, "Quién ya lo está usando en Chile",
  "Ver casos chilenos con nombre, cifra y fuente — ARAUCO, Copec, Vida Cámara, Entel Connect — y traducir uno a la propia operación.",
  [("15'", "Apertura: ¿esto ya funciona en empresas como la nuestra?", ""),
   ("45'", "Concepto: los cuatro casos de ARAUCO (gerencia de IA, Calidad de Cosecha, multiagente en celulosa, legal/compras/finanzas)", ""),
   ("60'", "TAREA: traducir un caso ajeno al proceso equivalente propio", "tarea"),
   ("25'", "TESTEO: el caso y su equivalente, con valor en cifra o decisión", "testeo"),
   ("15'", "Cierre: el patrón — todos partieron por el dolor, no por la herramienta", "")],
  "Elegir uno de los cuatro casos de la clase y nombrar el proceso equivalente en su empresa: qué se mide hoy por muestreo o por impresión, quién decide con esa información, y cuánto valdría medirlo completo. Con el nombre del proceso real, no de una idea.",
  "Se evalúa que el caso y el proceso propio sean comparables, y que el valor esté en una cifra o en una decisión concreta — no en «eficiencia»."),

 (3, "Hermes: el agente que usas tú",
  "Entender qué es Hermes, de quién es, cómo está armado y por qué un ejecutivo puede tener el suyo — incluido el argumento de riesgo de proveedor.",
  [("15'", "Apertura: «¿otro ChatGPT?» — la diferencia es la envoltura", ""),
   ("40'", "Concepto: las cinco piezas (memoria, herramientas, reglas, perfil, registro)", ""),
   ("20'", "Concepto: riesgo de proveedor — por qué abierto y propio", ""),
   ("55'", "TAREA: definir las cinco piezas de su propio agente (en papel, sin instalar)", "tarea"),
   ("20'", "TESTEO: nombrar recuerda / ejecuta / pide permiso", "testeo"),
   ("10'", "Cierre: qué hace falta para la clase 4", "")],
  "Escribir la ficha de su agente antes de instalarlo: qué tareas va a tomar, qué información necesita ver, qué reglas de calidad debe respetar, y qué acciones nunca hará sin aprobación. Una página. Es el contrato que se usa en la clase 4.",
  "Se evalúa que la ficha tenga las cinco piezas y que las reglas sean verificables (no «ser cuidadoso», sino «toda cifra con fuente»)."),

 (4, "Tu primer agente, andando esta semana",
  "La única clase técnica: instalar Hermes, conectar un modelo y ejecutar la primera tarea real. Cada participante sale con un agente corriendo.",
  [("15'", "Apertura: «yo no instalo software» — por qué aquí sí", ""),
   ("40'", "Demostración guiada: instalar, conectar el modelo, verificar", ""),
   ("65'", "TAREA: instalar y ejecutar la primera tarea propia", "tarea"),
   ("25'", "TESTEO: el agente respondiendo sobre un archivo propio", "testeo"),
   ("15'", "Cierre: qué información puede y qué no puede tocar ese agente", "")],
  "Instalar Hermes en su equipo, conectar un modelo con la guía del sitio, y ejecutar la primera tarea con la estructura de encargo de la clase 4 (objetivo, fuente, criterio, restricciones, entrega). Si la tarea usa información sensible, se hace con datos de ejemplo.",
  "El agente corre en el equipo del participante y responde sobre un archivo propio, con la fuente a la vista."),

 (5, "Darle lo que sabe tu empresa",
  "Conectar fuentes de conocimiento con criterio: hechos estables en memoria, procedimientos en la biblioteca de tareas, y el patrón puente —nunca copia— para los sistemas.",
  [("15'", "Apertura: por qué el agente no sabe nada de tu empresa", ""),
   ("40'", "Concepto: memoria vs biblioteca de tareas; las cuatro fuentes", ""),
   ("20'", "Concepto: puente, no copia — un solo origen por cifra", ""),
   ("60'", "TAREA: conectar una fuente y definir cinco hechos estables", "tarea"),
   ("25'", "TESTEO: una pregunta que hoy exige abrir tres archivos", "testeo"),
   ("15'", "Cierre: qué información NO se conecta y por qué", "")],
  "Conectar una fuente real de su área (carpeta de informes, actas, contratos) y escribir los cinco a diez hechos estables que el agente debe saber siempre. Probar con una pregunta que hoy obliga a abrir tres archivos y comparar la respuesta del agente con la propia.",
  "La respuesta es verificable: se ve de qué archivo salió cada parte. Una respuesta correcta sin fuente no acredita."),

 (6, "Ponerlo a producir",
  "Del encargo de chat al encargo de trabajo: producir un entregable completo —informe, comparación, análisis— y revisarlo con criterio.",
  [("15'", "Apertura: «ya me responde» no es «ya me sirve»", ""),
   ("40'", "Concepto: las cinco partes de un encargo", ""),
   ("90'", "TAREA: producir un entregable recurrente completo", "tarea"),
   ("25'", "TESTEO: producto + encargo + verificación de una cifra en vivo", "testeo"),
   ("15'", "Cierre: qué cambia en el trabajo del gerente", "")],
  "Elegir un entregable que ya produce cada mes y encargarlo completo con las cinco partes, dejando el encargo escrito para reutilizarlo. Verificar una cifra al azar contra el archivo original y comprobar que el anexo explica el cálculo.",
  "El producto sirve para decidir, y el encargo se puede reutilizar. Un buen resultado sin encargo reutilizable no escala."),

 (7, "Cuando la IA inventa: el riesgo de las cifras",
  "Entender por qué un agente inventa una cifra con seguridad total, cómo se detecta y cuáles son los cuatro controles que lo bloquean.",
  [("15'", "Apertura: la IA no miente, completa", ""),
   ("35'", "Concepto: las tres formas del invento y los dos tipos de respuesta", ""),
   ("25'", "Concepto: los cuatro controles (fuente, extractor, cruce, muestra)", ""),
   ("50'", "TAREA: encontrar el dato falso plantado en un informe", "tarea"),
   ("25'", "TESTEO: hallazgo en menos de diez minutos, solo con el original", "testeo"),
   ("10'", "Cierre: qué exige el comité de riesgo", "")],
  "Se entrega un informe producido por un agente con un dato falso plantado. El grupo debe encontrarlo en menos de diez minutos usando solo el archivo original, y luego escribir la regla que faltaba para que no hubiera pasado.",
  "Si no encuentran el dato falso, el problema no es el ejercicio: no hay proceso de verificación. Se evalúa la regla escrita, no solo el hallazgo."),

 (8, "Fuente o no se usa",
  "Escribir y comprobar la regla de trazabilidad: cada cifra con archivo y línea, o norma y artículo. Y distinguir «no lo resuelve» de «no lo revisé».",
  [("15'", "Apertura: ¿con qué criterio se acepta un dato que trajo un agente?", ""),
   ("35'", "Concepto: trazabilidad y los tres estados de un dato", ""),
   ("70'", "TAREA: auditar el entregable de la clase 6, cifra por cifra", "tarea"),
   ("25'", "TESTEO: cero cifras «no revisables»", "testeo"),
   ("15'", "Cierre: así cambia el registro de la reunión de comité", "")],
  "Tomar el entregable propio de la clase 6 y verificar cada cifra contra su fuente: archivo y línea, o norma y artículo. Marcar cada una como verificada, faltante o no revisada, y escribir la regla que faltaba en el encargo (no corregir el número a mano).",
  "Entregable con todas sus cifras marcadas y cero «no revisables». Un informe feo con todas las fuentes se defiende; uno elegante sin fuentes no."),

 (9, "Los límites: permisos, datos y firmas",
  "Decidir por escrito qué puede hacer el agente solo, qué debe preguntar y qué nunca toca — con el criterio reversible / irreversible y el marco de la Ley 21.719.",
  [("15'", "Apertura: ¿qué puede hacer tu agente sin pedirte permiso?", ""),
   ("35'", "Concepto: reversible vs irreversible; las tres decisiones (datos, acciones, registro)", ""),
   ("20'", "Marco legal: Ley 21.719, régimen pleno desde el 1 de diciembre de 2026", ""),
   ("60'", "TAREA: la matriz de atribuciones del propio agente", "tarea"),
   ("20'", "TESTEO: defender por qué cada acción está en su columna", "testeo"),
   ("10'", "Cierre: las cinco preguntas para el abogado y para TI", "")],
  "Escribir la matriz de atribuciones del agente propio: qué hace solo (reversible), qué exige aprobación (irreversible o con efecto externo) y qué nunca toca. Responder por escrito las cinco preguntas de la clase: qué datos ve, dónde corren, qué ejecuta sin aprobación, quién revisa y cómo se revoca.",
  "Una acción irreversible en la columna «solo» reprueba el ejercicio completo, aunque funcione."),

 (10, "Varios agentes, un proceso",
  "Cuándo el trabajo se divide entre varios agentes, cómo se reparte (paralelo, cadena, coordinador) y qué se vuelve más difícil de controlar.",
  [("15'", "Apertura: el cierre de mes no cabe en un encargo", ""),
   ("40'", "Concepto: las tres formas de repartir y el rol del coordinador", ""),
   ("20'", "Caso real: por qué el sistema de celulosa es multiagente", ""),
   ("60'", "TAREA: diseñar el reparto de un proceso propio", "tarea"),
   ("25'", "TESTEO: el proceso completo con los cruces a la vista", "testeo"),
   ("15'", "Cierre: cuándo NO vale la pena tener varios agentes", "")],
  "Diseñar el reparto de un proceso propio en tres partes: qué va en paralelo, qué en cadena, quién junta y en qué puntos se cruzan los números críticos. Incluir qué se registra de cada agente para poder reconstruir cualquier conclusión.",
  "Las contradicciones se detectan antes del resultado final. Un proceso que entrega limpio porque nadie cruzó nada no es un proceso."),

 (11, "Gobernar la IA sin frenar la empresa",
  "Las cuatro decisiones escritas que el directorio debe tomar —rol, límites, registro, métrica— y qué exigirle a un proveedor.",
  [("15'", "Apertura: ¿quién responde cuando un agente se equivoca?", ""),
   ("35'", "Concepto: las cuatro decisiones y la regla de la firma humana", ""),
   ("25'", "Concepto: plataforma cerrada vs agente propio; pilotos vs capacidades", ""),
   ("60'", "TAREA: el acta de gobernanza de una página", "tarea"),
   ("20'", "TESTEO: un acta que se pueda firmar hoy", "testeo"),
   ("10'", "Cierre: el checklist de seis preguntas anuales", "")],
  "Redactar el acta de gobernanza de un agente: qué agente, de quién depende, qué datos ve, qué requiere aprobación, cómo se mide y cómo se apaga. Una página, firmable hoy.",
  "Un acta con «por definir» no es gobernanza: es una intención. Se evalúa que esté completa y firmable."),

 (12, "El plan de 90 días",
  "Cierre: cada participante se va con un plan escrito y con la primera tarea ejecutada. Presentación ante panel.",
  [("10'", "Apertura: ¿qué cambia el lunes?", ""),
   ("25'", "Concepto: el plan 30/60/90 y los indicadores de resultado", ""),
   ("15'", "Concepto: los cinco errores que se repiten", ""),
   ("70'", "TESTEO FINAL: presentación del plan por participante o grupo", "testeo"),
   ("40'", "Panel de preguntas y cierre del curso", "")],
  "Presentar el plan de 90 días: el proceso elegido, el indicador de resultado, quién responde y cómo se apaga — con la primera tarea ya ejecutada, no prometida.",
  "El plan es defendible frente al área que lo va a recibir. Lo que importa: que mañana alguien pueda empezar."),
]

NIVELES = [
 ("Etapa 1 · Clases 1–3 — Entender", "qué es un agente, quién lo usa en Chile y qué es Hermes"),
 ("Etapa 2 · Clases 4–6 — Usar", "instalarlo, darle el conocimiento de la empresa y ponerlo a producir"),
 ("Etapa 3 · Clases 7–9 — Controlar", "cifras verificables, fuente obligatoria y límites de permiso"),
 ("Etapa 4 · Clases 10–12 — Escalar y gobernar", "varios agentes, acta de gobernanza y plan de 90 días"),
]


def clase_html(n, titulo, objetivo, bloques, tarea, testeo):
    bl = "".join(
        f'<span class="bloque{" tarea" if cls == "tarea" else " testeo" if cls == "testeo" else ""}">'
        f'<span class="min">{m}</span> {t}</span>'
        for m, t, cls in bloques)
    return f'''<div class="clase">
  <h3>{n} · {titulo}</h3>
  <div class="fecha">Clase {n} de 12</div><details class="deck"><summary>▶ Ver presentación</summary><iframe loading="lazy" src="ejecutivos-{n:02d}.html" title="Clase {n}"></iframe></details>
  <div class="obj"><b>Al salir sabes:</b> {objetivo}</div>
  <div class="bloques">{bl}</div>
  <h4>Tarea</h4>
  <div class="tarea"><p>{tarea}</p></div>
  <h4>Testeo</h4>
  <div class="testeo"><p><b>Demostrar:</b> {testeo}</p></div>
  <div class="links"><b>Para profundizar:</b>
    <a href="ejecutivos-{n:02d}.html">Abrir presentación</a>
    {('<a href="ejecutivos-guion-video.html">Guion del screencast de la clase 1</a>' if n == 1 else '')}
  </div>
</div>'''


ACTOS_S0 = [
 ("a", "Acto 1 · La promesa que no se cumplió", "2022–2024",
  "Por qué el 88% de las empresas usa IA y solo el 6% puede atribuirle un impacto significativo. La explicación que se dio en los directorios era falsa.",
  "8 diapositivas · 25 min con discusión"),
 ("b", "Acto 2 · La guerra de los agentes", "nov 2025 – mar 2026",
  "OpenClaw: tres nombres en cinco días, 100.000 estrellas en dos meses, y el episodio de seguridad que enseñó que un agente sin límites es un riesgo.",
  "10 diapositivas · 30 min"),
 ("c", "Acto 3 · El descubrimiento del harness", "2026",
  "El paper de 83 páginas que desarmó once agentes de producción: el modelo pesa 2,5–5 puntos, el harness pesa 13. La tesis del curso.",
  "10 diapositivas · 35 min"),
 ("cb", "Acto 3b · Cómo se arma un agente (arquitectura agéntica)", "2026",
  "Las siete piezas del harness, la forma mínima y máxima de cada una, la decisión de uno o varios agentes, y cómo auditar una propuesta técnica en siete preguntas.",
  "10 diapositivas · 30 min"),
 ("d", "Acto 5 · Lo que aprendimos de nosotros mismos", "2026",
  "1.464 sesiones auditadas, 39.752 mensajes, ~922 correcciones reales. El ranking de errores y las cuatro reglas que cambiaron el resultado.",
  "9 diapositivas · 30 min"),
 ("e", "Acto 6 · Hasta dónde podríamos llegar", "2026 en adelante",
  "Qué está resuelto, qué no, y la región vacía del mercado: nadie combina despliegue local con seguridad empresarial. Cierre sin promesas.",
  "9 diapositivas · 25 min"),
]

def seccion0_html():
    actos = "\n".join(f'''<div class="clase">
  <h3>{t}</h3>
  <div class="fecha">{f} · {d}</div><details class="deck"><summary>▶ Ver presentación</summary><iframe loading="lazy" src="ejecutivos-00{k}.html" title="{t}"></iframe></details>
  <div class="obj">{o}</div>
  <div class="links"><b>Material de apoyo:</b>
    <a href="ejecutivos-00{k}.html">Abrir presentación</a>
    <a href="ejecutivos-glosario.html">Glosario de datos</a>
  </div>
</div>''' for k, t, f, o, d in ACTOS_S0)
    return f'''<div class="nivel">Sección 0 · La historia <small>se dicta antes de la clase 1 · 6 actos · 175 min</small></div>
<p class="progtext"><b>Por qué existe:</b> un ejecutivo no necesita aprender a instalar un agente: necesita saber <b>por qué hoy se compra un harness y no un modelo</b>. Los cinco actos construyen esa historia con fuentes primarias, fechas y cifras — desde la promesa incumplida de 2022 hasta la región del mercado que todavía nadie llenó.</p>
<p class="progtext"><b>Material de referencia de la sección:</b> <a href="ejecutivos-glosario.html">glosario de datos (14 conceptos, buscable)</a> · <a href="ejecutivos-timeline.html">línea de tiempo 2022–2026 (15 hitos con fuente)</a></p>
{actos}
<div class="clase">
  <h3>0g · Instalar Hermes, paso a paso</h3>
  <div class="fecha">Taller de la sección 0 · se hace antes de la clase 4</div>
  <div class="bloques">
    <span class="bloque"><span class="min">10'</span> Qué vamos a instalar y dónde</span>
    <span class="bloque"><span class="min">25'</span> Abrir la terminal y pegar el instalador</span>
    <span class="bloque tarea"><span class="min">30'</span> TAREA: conseguir la llave y conectar el modelo</span>
    <span class="bloque testeo"><span class="min">15'</span> TESTEO: el agente responde sobre un archivo propio</span>
    <span class="bloque"><span class="min">10'</span> Cierre: qué puede y qué no puede tocar</span>
  </div>
  <h4>Qué se instala</h4>
  <div class="tarea"><p>Hermes en el computador de cada participante, con el modelo de IA que cada uno elija. Son <b>dos líneas en una ventana negra</b> y una llave de acceso. No se programa: se copia y se pega. Todo el detalle, con los comandos exactos y los cuatro errores típicos de cada paso, está en la <a href="guia-instalar-hermes.html">guía de instalación</a> de este sitio.</p></div>
  <h4>Testeo</h4>
  <div class="testeo"><p><b>Demostrar:</b> el agente corre en el equipo del participante y responde sobre un archivo propio, con la fuente a la vista. Si la tarea usa información sensible, se demuestra con datos de ejemplo.</p></div>
  <div class="links"><b>Material paso a paso:</b>
    <a href="guia-instalar-hermes.html">Guía de instalación de Hermes</a>
    <a href="directrices-hermes.html">Reglas del agente (SOUL)</a>
  </div>
</div>'''

cuerpo = []
for nombre, sub in NIVELES:
    cuerpo.append(f'<div class="nivel">{nombre} <small>{sub}</small></div>')
    lo = int(nombre.split("Clases ")[1].split("–")[0])
    hi = int(nombre.split("–")[1].split(" ")[0])
    for c in CLASES:
        if lo <= c[0] <= hi:
            cuerpo.append(clase_html(*c))

HTML = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IA Agéntica para Ejecutivos — Plan de clases</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>IA Agéntica para Ejecutivos</h1>
  <p class="sub">Del dato al directorio: cómo un ejecutivo usa un agente para investigar, decidir, delegar y controlar · 12 clases · 160 min/clase · curso ejecutivo</p>
  <span class="badge">12 clases · 4 etapas</span>
  <span class="badge">Sin programar</span>
  <span class="badge">Objetivo: un agente propio funcionando y un plan de 90 días</span>
</header>

<p style="color:var(--mut);max-width:860px;margin:14px 0 0;">Curso para <b>ejecutivos y profesionales de empresa</b>, no técnicos. No se enseña a programar: se enseña a <b>dirigir un agente</b> — darle un objetivo, entregarle el conocimiento de la empresa, exigirle fuente y ponerle límites. El eje es Hermes y herramientas equivalentes, aplicadas al trabajo real de cada participante.</p>
<p style="color:var(--mut);max-width:860px;margin:6px 0 0;"><b>Los casos son de empresas chilenas de este tamaño</b>, con cifra y fuente citada en cada deck: ARAUCO (gerencia de IA, Calidad de Cosecha con +37% de calidad de faenas, sistema multiagente en celulosa), Copec, Vida Cámara, Entel Connect. Las cifras de mercado (McKinsey, MIT) están fechadas en el deck de la clase que las usa.</p>
<p style="color:var(--mut);max-width:860px;margin:6px 0 0;"><b>Única clase técnica:</b> la 4, instalar el agente. Una tarde, una vez, con guía paso a paso. Todo lo demás es criterio, no comandos.</p>

{seccion0_html()}\n{chr(10).join(cuerpo)}

<footer>
  Objetivo del curso (no notas): cada participante egresa con <b>un agente funcionando en una tarea real</b>, un <b>encargo escrito</b> reutilizable cada mes, y un <b>acta de gobernanza</b> con dueño y métrica. Material complementario en este sitio: <a href="guia-instalar-hermes.html">guía de instalación</a> · <a href="directrices-hermes.html">directrices del agente</a>.
</footer>
</div>
</body>
</html>'''

with open(SALIDA, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"{SALIDA}: {len(HTML)} bytes, {len(CLASES)} clases, {len(NIVELES)} etapas")
