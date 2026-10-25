# -*- coding: utf-8 -*-
"""Historia "Cómo llegamos hasta acá" — seccion 0 del curso ejecutivo.

5 actos, dictados ANTES de la clase 1. Storytelling para C-level: cada afirmacion con
fuente primaria y fecha. NO es material tecnico.

EJE: no es la historia de un producto, es la historia de una disciplina. El ejecutivo
tiene que salir sabiendo POR QUE hoy se compra un harness y no un modelo.

FUENTES VERIFICADAS (oct 2026), citadas en el deck de fuentes:
- arXiv 2609.00006 (harness engineering, 15 jul 2026): 11 harnesses de produccion,
  Hermes y OpenClaw incluidos. 7 subsistemas, 29 patrones, 2 ausencias, 18 recomendaciones.
- arXiv 2608.05201 (ASTELD, 5 ago 2026): 8 plataformas, caso OpenClaw, 50+ derivados,
  y la region vacia: ningun sistema evaluado combina local-first con seguridad empresarial.
- OpenClaw: Clawdbot (nov 2025) -> Moltbot (27 ene 2026) -> OpenClaw (30 ene 2026).
  Fuente: docs.openclaw.ai/start/lore + TechCrunch 30 ene 2026 (100.000 estrellas en 2 meses).
- Cifras del harness: cambio de harness 13 pts vs cambio de modelo 2,5-5 pts (SWE-bench
  Verified); GLM-5.2 23% vs 52%; LFM2.5-2.6B 42%->54% entrenando en 4 harness, -31% llamadas.
- Zhipu GLM-5.3: "la dificultad de escalar se mueve del modelo al entorno".
- LIBRO_ERRORES.md (local): 1.464 sesiones, 39.752 mensajes, 4.012 crudas -> ~922 unicas.
- McKinsey 2026 + grafico dic 2025: 88% usa IA, 6% impacto significativo, 37% algun impacto.
- RAG: OmniRetrieval arXiv 2605.29250. El "73% de RAG fallan" NO tiene estudio primario
  localizado -> se presenta como afirmacion de blogs de industria, no como dato.

VOCABULARIO: C-level no tecnico. Se permite "harness" SOLO despues de definirlo en el Acto 3
(antes se dice "el programa que envuelve al modelo"). Prohibido: LLM, token, prompt, API,
RAG (se dice "memoria documental"), embedding, sandbox, MCP, CLI, Colab, Python.
"""

HISTORIA = []

# ══════════════════════════════════════════════════════ ACTO 1
HISTORIA.append((1, "La promesa que no se cumplió",
  "2022-2024. La IA llegó a todas las empresas y a casi ninguna cuenta de resultados. Esta es la historia de por qué, y de por qué la explicación no es la que se dio en los directorios.",
  [
   ("pregunta", dict(kicker="Acto 1 de 5 · La promesa", h2="Todos compraron. Casi nadie cobró.",
     big="Entre 2023 y 2025 las empresas del mundo adoptaron IA más rápido que cualquier tecnología anterior. Al cierre de 2025, <b>88% de las empresas la usaba</b> en al menos una función. Pero solo <b>6%</b> podía atribuirle un impacto significativo al resultado.",
     meta="Fuentes: McKinsey, gráfico oficial 'AI at work but not at scale' (dic 2025; 1.993 encuestados, jun-jul 2025) para el 88%; McKinsey Global Survey 2026 (ago 2026) para el 6%.")),

   ("vs", dict(kicker="La brecha, medida", h2="Lo que crecía y lo que no",
     bad_t="Lo que subió",
     bad=["88% de las empresas usa IA en al menos una función",
          "79% usa IA generativa (era 33% en 2023)",
          "80% de las personas dice que mejoró su productividad",
          "40% de las empresas grandes ya escala agentes (era 27% el año anterior)"],
     good_t="Lo que se quedó plano",
     good=["37% atribuye algún impacto al resultado operativo — igual que el año anterior",
           "Solo 6% puede atribuirle 5% o más y llamarlo significativo",
           "1 de cada 5 pilotos no llegó a demostrar retorno (MIT, ago 2025)",
           "La productividad individual sube; el resultado de la empresa no"])),

   ("porque", dict(kicker="La explicación que se dio", h2="«Es que el modelo todavía no es suficientemente bueno»",
     big="Fue el diagnóstico de 2023 y 2024. Y era cómodo: no exigía cambiar nada de la empresa, solo esperar la próxima versión. <b>Era falso</b>, y el curso entero existe porque era falso.",
     meta="El dato que lo desmiente viene del Acto 3: el mismo modelo, en dos programas distintos, acierta 62% o 33%. El modelo no era el problema.")),

   ("pregunta", dict(kicker="Y el costo de creerlo", h2="Seis años comprando la cosa equivocada",
     big="Con ese diagnóstico, las empresas compraron licencias, capacitaciones y chatbots. Todo eso mejora al individuo que lo usa — y por eso las encuestas de productividad se ven bien. <b>Pero no cambia cómo trabaja el proceso</b>, y el resultado vive en el proceso.",
     meta="Es la diferencia entre el 80% de productividad individual y el 6% de impacto significativo: la misma tecnología, dos lugares donde se mide.")),

   ("definicion", dict(kicker="Lo que este curso propone", h2="La pregunta correcta no es «¿qué modelo?»",
     defn="La pregunta que separa a la empresa que cobra de la que solo compró es: <b>¿qué rodea al modelo?</b> Qué datos ve, qué puede ejecutar, qué recuerda, qué límites tiene y quién revisa lo que hizo.",
     meta="Eso es lo que en 2026 se llamó 'harness' y lo que se explica en el Acto 3. Los tres primeros actos existen para que esa palabra no suene a jerga: es la respuesta a por qué el 6%.")),

   ("testeo", dict(kicker="El testeo del acto", h2="Nombra tu propia brecha",
     big="En una frase: ¿en qué proceso de tu empresa la IA ya mejoró la vida de las personas, y en cuál cambió el resultado del negocio? Si solo tienes la primera, ya sabes dónde estás.",
     meta="No hay respuesta correcta. Hay honestidad: la mayoría de las empresas grandes solo puede nombrar la primera.")),

   ("links", dict(kicker="Fuentes del acto", h2="Para verificar",
     links=[("McKinsey — AI at work but not at scale (el 88%, dic 2025)", "https://www.mckinsey.com/featured-insights/charts/ai-at-work-but-not-at-scale"),
            ("McKinsey — The state of AI: Global Survey 2026 (el 6%, ago 2026)", "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"),
            ("MIT / NANDA — los pilotos sin retorno (ago 2025, resumen con cifras)", "https://www.salesforce.com/news/stories/why-ai-pilots-fail/")])),
  ]))

# ══════════════════════════════════════════════════════ ACTO 2
HISTORIA.append((2, "La guerra de los agentes",
  "Noviembre 2025 - marzo 2026. En cinco meses nació, se rebautizó tres veces, explotó en popularidad y mostró su talón de Aquiles. Es el episodio que enseñó al mercado que un agente sin límites es un riesgo.",
  [
   ("pregunta", dict(kicker="Acto 2 de 5 · La guerra", h2="Un fin de semana de 2025 cambió la conversación",
     big="Un desarrollador austríaco retirado, Peter Steinberger, armó en un fin de semana un asistente que corría en el computador de la persona y trabajaba desde WhatsApp. Lo llamó <b>Clawdbot</b>. En dos meses llegó a <b>100.000 estrellas</b> — una de las explosiones más rápidas que ha visto el software libre.",
     meta="Fuente: TechCrunch, 30 de enero de 2026. Clawdbot lanzado en noviembre de 2025.")),

   ("pasos", dict(kicker="La cronología, con fechas", h2="Tres nombres en cinco días",
     steps=[("Noviembre 2025:", "nace como Clawdbot. Un asistente personal que vive en tu computador y obedece desde el chat que ya usas."),
            ("27 de enero de 2026:", "Anthropic —la empresa de Claude— envía un correo pidiendo el cambio de nombre por marca. La comunidad vota en Discord: gana 'Moltbot'."),
            ("30 de enero de 2026:", "tercer y definitivo nombre: OpenClaw. 'La langosta mudó de caparazón por última vez'."),
            ("La misma semana:", "bots automáticos roban el usuario @openclaw en X y el usuario personal de GitHub del creador. Hubo que llamar a los directivos de ambas plataformas.")],
     meta="Fuente: la propia documentación del proyecto (docs.openclaw.ai/start/lore) y TechCrunch, 30 ene 2026. Los nombres son reales; el relato del proyecto los cuenta así.")),

   ("porque", dict(kicker="Por qué esto no es una anécdota de frikis", h2="Lo que se demostró en 90 días",
     big="Que <b>un agente personal, corriendo en el computador de alguien y conectado a sus chats, es lo que la gente quería</b>. No un chat en una pestaña: algo que actúa. Esa demanda existía y estaba insatisfecha.",
     meta="En marzo de 2026 ya se hablaba de 'claws' como categoría de producto: agentes personales que corren en tu máquina y ejecutan tareas por ti.")),

   ("error", dict(kicker="El talón de Aquiles", h2="«Seguridad confiando en una langosta»",
     warn="Su propia documentación cita, con humor, la frase del creador: <b>«security by trusting a lobster»</b>. Y registra un incidente real: el agente ejecutando una orden que listaba todo el directorio del usuario y lo compartía en un chat de grupo.<br><br>TechCrunch fue explícito en enero de 2026: mientras no madurara la seguridad, <b>no era aconsejable darle acceso a tu Slack o WhatsApp principal</b>.")),

   ("definicion", dict(kicker="El paper que lo estudió", h2="50 derivados y una región vacía",
     defn="Un paper de agosto de 2026 (ASTELD) clasificó <b>ocho plataformas de agentes</b> y más de <b>50 derivados de OpenClaw</b>. Conclusión incómoda para el mercado: <b>ninguno de los sistemas evaluados combina despliegue local con seguridad de nivel empresarial</b>.",
     meta="arXiv 2608.05201 (5 ago 2026). Esa 'región vacía' es exactamente el espacio donde una empresa seria puede jugar: local, pero con gobierno.")),

   ("vs", dict(kicker="La lección para un directorio", h2="Popularidad y confiabilidad son ejes distintos",
     bad_t="Lo que la adopción viral premia",
     bad=["Que sea fácil de instalar y usar", "Que se conecte a todo el chat y el correo",
          "Que ejecute sin pedir permiso", "Que la comunidad crezca rápido"],
     good_t="Lo que una empresa necesita",
     good=["Que se pueda auditar qué hizo y cuándo", "Que se le pueda limitar el acceso por área",
           "Que pida aprobación en lo irreversible", "Que si sube el precio o se va, el trabajo quede"])),

   ("porque", dict(kicker="Lo que pasó después", h2="El mercado se separó en dos",
     big="Por un lado, los agentes virales y gratuitos que corren donde el usuario quiera. Por el otro, los que se pueden poner en una empresa: con registro, permisos y reglas. <b>Hermes pertenece al segundo grupo</b>, y por eso aparece en el estudio académico junto a los grandes.",
     meta="En el Acto 3: el paper de harness engineering analizó once sistemas de producción, y Hermes es uno de ellos.")),

   ("testeo", dict(kicker="El testeo del acto", h2="La pregunta que salva un proyecto",
     big="Antes de conectar un agente a un sistema de la empresa, pregúntate: ¿si esto se equivoca, quién responde y qué queda registrado? Si no hay respuesta, no es un agente listo para producción.",
     meta="Es la misma pregunta que el paper ASTELD respondió con datos: la seguridad y la facilidad se mueven en direcciones opuestas.")),

   ("links", dict(kicker="Fuentes del acto", h2="Para verificar",
     links=[("TechCrunch — el tercer nombre y las 100.000 estrellas (30 ene 2026)", "https://techcrunch.com/2026/01/30/openclaws-ai-assistants-are-now-building-their-own-social-network"),
            ("OpenClaw — la historia oficial del proyecto (docs.openclaw.ai)", "https://docs.openclaw.ai/start/lore"),
            ("arXiv 2608.05201 — ASTELD: ocho plataformas y la región vacía (5 ago 2026)", "https://arxiv.org/abs/2608.05201")])),
  ]))

# ══════════════════════════════════════════════════════ ACTO 3
HISTORIA.append((3, "El descubrimiento del harness",
  "2026. Un paper de 83 páginas desarmó once agentes de producción y encontró lo que nadie estaba midiendo: el modelo pesa menos que el programa que lo envuelve. Esta es la tesis del curso.",
  [
   ("pregunta", dict(kicker="Acto 3 de 5 · El hallazgo", h2="El experimento que ordena todo",
     big="Mismos pesos del modelo, mismas preguntas, el mismo día. Solo cambia el programa que lo envuelve. Resultado: <b>62% de acierto en un programa y 33% en otro</b>. El mismo cerebro, la mitad del resultado.",
     meta="Medición sobre SWE-bench Verified, 2026. El programa que envuelve al modelo es lo que la industria bautizó 'harness'.")),

   ("definicion", dict(kicker="La definición, en simple", h2="Qué es un harness",
     defn="Si el modelo es el <b>motor</b>, el harness es <b>el auto completo</b>: el bucle que lo hace trabajar, las herramientas que le da, la memoria que le entrega, los límites que le pone y las extensiones con que crece. El motor solo no lleva a nadie a ninguna parte.",
     meta="Definición adaptada del paper arXiv 2609.00006: 'un agente es un modelo más un harness'. La analogía es nuestra, no del paper.")),

   ("vs", dict(kicker="Las cifras del hallazgo", h2="Qué mueve más la aguja",
     bad_t="Cambiar el modelo",
     bad=["Dentro del mismo programa: mueve 2,5 a 5 puntos", "Es lo que todos discuten en la reunión",
          "Cuesta más plata por consulta", "Se nota poco en el resultado final"],
     good_t="Cambiar el harness",
     good=["El mismo modelo: mueve 13 puntos", "No requiere cambiar de proveedor",
           "Se puede mejorar sin gastar más", "Explica la mitad de la varianza del resultado"])),

   ("piezas", dict(kicker="La evidencia, tres veces", h2="Tres mediciones del mismo fenómeno",
     piezas=[("GLM-5.2", "23% en un harness y 52% en otro. Mismo modelo, mismos pesos, más del doble de acierto."),
             ("Claude Opus", "El ranking se invierte según el harness: el que gana en uno pierde en otro. No hay un 'mejor' universal."),
             ("LFM2.5 chico", "Un modelo de 2.600 millones de parámetros pasó de 42% a 54% entrenándolo dentro de cuatro harness reales, con 31% menos consultas.")])),

   ("porque", dict(kicker="La frase que lo resume", h2="«La dificultad se movió del modelo al entorno»",
     big="Lo dijo Zhipu, la empresa detrás de la familia GLM, en su informe de 2026: <b>«a medida que mejora la capacidad del agente, la mayor parte de la dificultad de escalar se traslada del modelo al entorno»</b>. No es una opinión de un curso: es el reporte técnico de quien construye uno de los modelos.",
     meta="Informe de GLM-5.3 (2026), citado por Hugging Face en su repaso de los reportes de laboratorio (sep 2026).")),

   ("lista", dict(kicker="El paper de referencia", h2="Once agentes desarmados, y las dos ausencias",
     items=["<b>Qué es:</b> 'Harness Engineering', 83 páginas, publicado el 15 de julio de 2026. Estudia el código de once agentes de producción.",
            "<b>Cuáles:</b> Claude Code, Codex CLI, Gemini CLI, Mistral Vibe, OpenHands, Aider, Mini-SWE-Agent, <b>Hermes</b>, Pi, OpenCode y <b>OpenClaw</b>.",
            "<b>Qué mapea:</b> siete subsistemas canónicos, trece observaciones transversales, 29 patrones recurrentes y 18 recomendaciones de diseño.",
            "<b>La primera ausencia:</b> en unos cuatro millones de líneas de código, <b>ningún runtime de agente importa un framework de agentes</b>. Se lo hacen a mano.",
            "<b>La segunda ausencia:</b> <b>ninguno recupera código con vectores</b>. El campo corre con bucles propios y recuperación determinista."],
     meta="arXiv 2609.00006 (15 jul 2026), segunda edición ampliada de un estudio de abril 2026. Es la base del capítulo de harness del curso.")),

   ("porque", dict(kicker="Por qué le importa a un directorio", h2="Cambia qué se compra",
     big="Si el harness pesa más que el modelo, entonces <b>la decisión de compra no es 'contratemos el modelo más caro'</b>. Es: ¿tiene herramientas para tocar nuestros sistemas? ¿recuerda lo de la empresa? ¿deja registro? ¿puede ponerle límites? Todo eso es harness, y todo eso es negociable con un proveedor.",
     meta="Y es la razón por la que las dos ausencias del paper importan: no existe un framework que resuelva esto por ti. Se arma.")),

   ("testeo", dict(kicker="El testeo del acto", h2="Reescribe tu conversación de compra",
     big="Toma la última propuesta de IA que evaluaste. ¿Cuántas líneas hablaban del modelo y cuántas del harness? Si es 90/10, la decisión estaba mirando el eje que pesa menos.",
     meta="Se evalúa que la respuesta distinga el motor del auto completo, con ejemplos de su propia propuesta.")),

   ("links", dict(kicker="Fuentes del acto", h2="Los papers, para que TI los lea",
     links=[("arXiv 2609.00006 — Harness Engineering: 11 sistemas (15 jul 2026)", "https://arxiv.org/abs/2609.00006"),
            ("Hugging Face — cómo entrenan los laboratorios a los agentes en 2026", "https://huggingface.co/blog/sergiopaniego/rl-environments-2026"),
            ("Clase 0b del curso de Auditoría — el mismo modelo, otra herramienta (este sitio)", "clase-harness-multientorno.html"),
            ("Clase 0 del curso de Auditoría — los 7 subsistemas y el glosario (este sitio)", "clase-harness-contabilidad.html")])),
  ]))

# ══════════════════════════════════════════════════════ ACTO 4
HISTORIA.append((4, "Lo que aprendimos de nosotros mismos",
  "2026. Mientras el mercado discutía modelos, acá se hizo algo que casi nadie hace: auditar el propio trabajo. Miles de sesiones minadas, errores contados, y las reglas que salieron de ahí. Este es el capítulo que ningún proveedor puede contar.",
  [
   ("pregunta", dict(kicker="Acto 4 de 5 · La evidencia propia", h2="¿Y cómo se usa esto sin que salga mal?",
     big="Todo lo anterior explica por qué un agente puede trabajar. No explica por qué <b>no va a inventar una cifra</b>. Para eso no alcanza con doctrina: hay que mirar los errores reales. Y los nuestros están medidos, contados y escritos.",
     meta="Este acto usa datos propios de CONECTA sobre trabajo con agentes durante 2026. Van con su metodología, incluida la parte incómoda.")),

   ("vs", dict(kicker="El corpus", h2="Qué se auditó",
     bad_t="La escala del trabajo",
     bad=["1.464 sesiones de trabajo real", "39.752 mensajes", "18.196 errores de herramienta",
          "9 entornos: Mac, servidor y siete perfiles de área"],
     good_t="Lo que se encontró (después de deduplicar)",
     good=["4.012 correcciones directas del usuario",
           "Solo el 18% de esos textos era único: la misma corrección se repetía hasta 20 veces",
           "Correcciones distintas reales: ~922",
           "Y al minar aparecieron credenciales en el texto: se construyó un filtro que las enmascara"])),

   ("porque", dict(kicker="La nota metodológica honesta", h2="Por qué publicamos el número chico",
     big="El primer conteo daba 4.012 correcciones. Al revisar, <b>la misma frase aparecía hasta veinte veces</b> por sesiones duplicadas. Decidimos publicar las <b>~922 reales</b>: un número grande y falso no sirve para decidir nada.",
     meta="Es la primera lección del material y se aplica a todo lo demás: si un número no se puede reproducir, no es un número. Fuente: LIBRO_ERRORES.md de CONECTA (2026).")),

   ("lista", dict(kicker="El ranking de errores", h2="Dónde falla un agente, medido",
     items=["<b>32,5% respondió otra cosa / se fue por las ramas.</b> Hizo algo distinto de lo pedido.",
            "<b>24,4% no pidió permiso / se apuró.</b> Se adelantó en algo que no le correspondía.",
            "<b>14,8% no usó la herramienta que tenía.</b> Improvisó teniendo el recurso.",
            "<b>14,6% no verificó / reportó sin ejecutar.</b> Dijo que estaba hecho y no estaba.",
            "<b>7,9% formato equivocado · 2,3% pérdida de datos · 0,9% inventó datos.</b> La invención existe, pero no es el error más frecuente."],
     meta="Sobre las ~922 correcciones distintas. Dato contraintuitivo para un directorio: el riesgo número uno no es que invente, es que haga otra cosa de la que se le pidió.")),

   ("piezas", dict(kicker="Las reglas que salieron", h2="Las cuatro que cambiaron el resultado",
     piezas=[("El entregable es la salida real", "No la descripción de lo que hizo. Si no se ejecutó, no está hecho. Ataca el 14,6%."),
             ("Releer la pregunta textual", "Responder exactamente lo preguntado; lo agregado va marcado aparte. Ataca el 32,5%."),
             ("Actuar en lo reversible, pedir permiso en lo irreversible", "Ataca el 24,4%, el error que más caro sale en una empresa."),
             ("Ninguna cifra sin fuente", "Se marca el origen de cada número o no se dice. Es el 0,9%, pero es el que termina en un directorio.")])),

   ("porque", dict(kicker="Por qué esto es un activo y no un paper", h2="La diferencia entre teoría y operación",
     big="Cualquier empresa puede leer el paper del harness. Muy pocas pueden mostrar <b>1.464 sesiones auditadas de su propio trabajo</b>, con el ranking de sus errores y las reglas que cambiaron. Eso es lo que separa a un adoptante de un operador.",
     meta="Y es transferible: las reglas no dependen del modelo ni del proveedor. Sobreviven al cambio de versión.")),

   ("testeo", dict(kicker="El testeo del acto", h2="Elige tu error más caro",
     big="De los cinco patrones del ranking, ¿cuál le costaría más a tu área si lo cometiera un agente todos los días? Y ¿qué regla escrita lo bloquearía?",
     meta="Se evalúa que elija por costo real, no por frecuencia: el más frecuente (irse por las ramas) y el más caro (actuar sin permiso) no son el mismo.")),

   ("links", dict(kicker="Fuentes del acto", h2="Para profundizar",
     links=[("LIBRO_ERRORES — manual de errores medido (material de CONECTA, 2026)", "https://vvilche.github.io/usach-cursos/"),
            ("Directrices del agente — las reglas y las pruebas para saber si funcionan (este sitio)", "directrices-hermes.html"),
            ("Caso: cómo se construyó un Estado de Resultados, con los dos errores cometidos (este sitio)", "caso-estado-resultados.html")])),
  ]))

# ══════════════════════════════════════════════════════ ACTO 5
HISTORIA.append((5, "Hasta dónde podríamos llegar",
  "2026 en adelante. Qué está resuelto, qué no, y dónde está el espacio vacío que el mercado todavía no llenó. Cierre de la sección 0, sin promesas.",
  [
   ("pregunta", dict(kicker="Acto 5 de 5 · El horizonte", h2="Lo que ya no es una promesa",
     big="Un agente personal que corre en tu computador, lee tus archivos, recuerda tus reglas y deja registro de lo que hizo <b>ya existe y ya se usa</b>. No es una demo de laboratorio: once sistemas de producción fueron estudiados por código.",
     meta="Es el punto de partida del curso, no el final. La pregunta ya no es '¿se puede?', es '¿qué le ponemos adentro?'.")),

   ("porque", dict(kicker="El espacio vacío", h2="Nadie combina local con seguridad empresarial",
     big="El paper de agosto de 2026 fue explícito: <b>ninguno de los ocho sistemas evaluados combina despliegue local con seguridad de nivel empresarial</b>. Ahí está la oportunidad — y el riesgo, porque lo que no existe tampoco está resuelto por nadie.",
     meta="arXiv 2608.05201. Es la frontera: la empresa que resuelva eso primero con reglas claras, tiene ventaja sobre la que compre la plataforma cerrada más grande.")),

   ("vs", dict(kicker="El estado del arte, sin adornos", h2="Lo resuelto y lo no resuelto",
     bad_t="Resuelto",
     bad=["Un agente puede leer archivos, consultar sistemas y ejecutar tareas",
          "Puede recordar entre sesiones y aprender reglas",
          "Se puede limitar, registrar y auditar lo que hizo",
          "Corre en un notebook o en un servidor de la empresa"],
     good_t="No resuelto (y no se promete acá)",
     good=["Que no invente nunca: se controla, no se elimina",
           "Que decida bien sin supervisión en procesos críticos",
           "Que combine local y seguridad empresarial de fábrica",
           "Que el resultado llegue solo al número: hay que rediseñar el proceso"])),

   ("lista", dict(kicker="Dónde se puede jugar", h2="Cuatro jugadas con sustento",
     items=["<b>1. El agente del ejecutivo:</b> tu propio agente sobre tus archivos, con tus reglas. Es lo que se construye en este curso, y no depende de TI.",
            "<b>2. El proceso con fuente obligatoria:</b> un entregable que hoy tarda días y que sale con todas las cifras trazables. Ataca el 6% del Acto 1.",
            "<b>3. La memoria documental de la empresa:</b> el conocimiento disperso hoy en carpetas, actas y correos, consultable. La tecnología existe (OmniRetrieval, mayo 2026); el trabajo es de la empresa, no del proveedor.",
            "<b>4. La gobernanza antes que la escala:</b> acta, permisos y métrica desde el primer día. Es lo que separa al 6% del 94%, y no cuesta tecnología: cuesta decidirlo."],
     meta="Las cuatro son reversibles y se pueden empezar sin proyecto de transformación. Ninguna exige comprar una plataforma nueva.")),

   ("error", dict(kicker="Lo que no vamos a decir", h2="Tres promesas que este curso no hace",
     warn="<b>No:</b> 'esto reemplaza personas'. El ranking del Acto 4 muestra que un agente sin supervisión se equivoca en algo distinto de lo que se le pidió, casi un tercio de las veces.<br><br><b>No:</b> 'esto se paga solo'. El 95% de los pilotos no demostró retorno.<br><br><b>No:</b> 'hay que hacerlo ya o quedas fuera'. La ventaja no es la velocidad: es el proceso que se rediseña bien.")),

   ("definicion", dict(kicker="El cierre de la sección 0", h2="La historia completa en una frase",
     defn="2022-2024: <b>se compró la IA equivocada</b>. 2025: <b>se descubrió que el agente existe y que sin límites es un riesgo</b>. 2026: <b>se aprendió que pesa más el harness que el modelo, y que sin reglas escritas el resultado no llega</b>. 2027: <b>gana quien ponga el conocimiento de su empresa adentro de un agente que se pueda auditar</b>.",
     meta="De ahí en adelante el curso es práctico: nueve clases para construir eso, tres para controlarlo.")),

   ("testeo", dict(kicker="El testeo del acto", h2="Tu tesis en tres líneas",
     big="En tres líneas, escritas por ti: qué cambia en tu empresa, qué número lo va a probar, y qué no vas a hacer. Ese texto es el borrador del plan de 90 días de la clase 12.",
     meta="Se evalúa que las tres líneas sean contradictorias con nada de la sección 0: si prometes que no habrá errores, no se aprendió la historia.")),

   ("links", dict(kicker="Fuentes del acto", h2="Y el material del curso",
     links=[("arXiv 2608.05201 — la región vacía: local con seguridad empresarial (5 ago 2026)", "https://arxiv.org/abs/2608.05201"),
            ("arXiv 2605.29250 — OmniRetrieval: consultar fuentes distintas (28 may 2026)", "https://arxiv.org/abs/2605.29250"),
            ("Plan de clases del curso ejecutivo (este sitio)", "ejecutivos-ia-agentica.html"),
            ("Instalar Hermes — guía paso a paso (este sitio)", "guia-instalar-hermes.html")])),
  ]))
