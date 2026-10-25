# -*- coding: utf-8 -*-
"""Contenido de las 12 clases del curso "IA agentica para ejecutivos".

Cada entrada: (n, titulo, lead, slides). Los slides usan los tipos de gen_ppts.py:
pregunta, definicion, vs, loop, ejemplo, piezas, porque, error, pasos, testeo, lista, links.
Campos RAW (aceptan <b>): big, defn, warn, items, steps(pasos), code.
Campos ESCAPED (sin HTML): h2, lead, meta, vs todo, piezas, links.

REGLA DE VOCABULARIO (publico C-level, no tecnico):
- "Hermes" solo, nunca "Hermes Agent".
- Se dice "asistente con IA", "agente", "le da datos a la IA", "conectar".
  Prohibido: LLM, token, prompt, API, RAG, sandbox, embedding, fine-tuning, MCP, CLI.

REGLA DE CIFRAS: toda cifra de estos decks sale de una fuente citada en el propio deck
(ver el slide "Fuentes" de cada clase). Fecha de medicion: oct 2026.
"""

CLASES_EJEC = []

# ══════════════════════════════════════════════════ CLASE 1
CLASES_EJEC.append((1, "Qué es un agente (y qué no)",
  "El 88% de las empresas ya usa IA, pero solo un 6% puede atribuirle un impacto significativo al resultado. La diferencia entre esas dos cifras es el tema completo del curso.",
  [
   ("pregunta", dict(kicker="Dónde estamos hoy", h2="Todos tienen IA. Casi nadie tiene resultados.",
     big="El 88% de las empresas usa IA en al menos una función del negocio. Pero solo <b>6%</b> puede atribuirle al menos un 5% de su resultado operativo y calificar el impacto de significativo. <b>Tener herramientas no es tener resultados.</b>",
     meta="Cifras: McKinsey Global Survey on the state of AI. Uso 88% (gráfico oficial, dic 2025; 1.993 encuestados, jun-jul 2025). El 6% de alto desempeño, informe 2026 (ago 2026), sin cambio respecto de 2025.")),

   ("pregunta", dict(kicker="Y el dato que incomoda", h2="95% de los pilotos de IA no entrega retorno",
     big="Un estudio del MIT (agosto 2025) revisó pilotos de IA generativa en empresas y encontró que <b>95% no llegó a demostrar retorno</b>. No falló el modelo: falló la forma en que la empresa lo puso a trabajar.",
     meta="Cifra citada por múltiples medios sobre el informe del MIT (NANDA, ago 2025). El detalle importa: el 70% de los usuarios reportó que la herramienta no aprende de sus correcciones.")),

   ("vs", dict(kicker="Dónde está la brecha", h2="Uso individual alto, escala empresarial baja",
     bad_t="Lo que crece",
     bad=["80% de las personas dice que la IA mejoró su productividad individual",
          "50% dice que le ayuda a tomar mejores decisiones",
          "40% de las empresas grandes ya está escalando agentes (era 27% el año anterior)"],
     good_t="Lo que no crece",
     good=["37% atribuye algún impacto en el resultado operativo (igual que el año anterior)",
           "Solo 6% puede atribuirle 5% o más y llamarlo significativo",
           "39% espera reducir dotación por IA; las reducciones reales van muy por detrás"])),
   ("porque", dict(kicker="Por qué fallan", h2="Nadie le dio a la IA acceso a lo que la empresa sabe",
     big="Un chatbot no conoce tu planta, tus contratos, tu planilla de costos ni lo que decidiste el martes pasado en el comité. <b>Sin acceso a los datos y sin memoria de lo decidido, la IA solo puede opinar.</b>",
     meta="Ese es exactamente el hueco que llena un agente: no es una IA más inteligente, es una IA conectada a tu realidad.")),

   ("definicion", dict(kicker="La definición", h2="Qué es un agente",
     defn="Un agente es un programa que recibe un <b>objetivo</b>, <b>decide por sí mismo</b> qué hacer, usa <b>herramientas</b> (leer archivos, consultar sistemas, buscar en internet, correr cálculos) y <b>ejecuta</b> hasta cumplirlo.",
     meta="La diferencia con ChatGPT no es de inteligencia: es de quién hace el trabajo. Con un chatbot, el ejecutor eres tú.")),

   ("loop", dict(kicker="El mecanismo", h2="El ciclo que repite un agente",
     lead="Todo agente, sin excepción, repite este ciclo hasta cumplir el objetivo:",
     nodes=[("🎯 Objetivo", "qué hay que lograr"), ("PENSAR", "¿qué hago ahora?"),
            ("ACTUAR", "usar una herramienta"), ("OBSERVAR", "leer el resultado")],
     meta="Si el resultado no cumple el objetivo, vuelve a PENSAR con la información nueva. Es un ciclo, no una respuesta única.")),

   ("vs", dict(kicker="La diferencia que importa", h2="Chatbot vs. agente",
     bad_t="ChatGPT / Gemini (conversacional)",
     bad=["Responde texto cuando le preguntas", "No toca tus archivos ni tus sistemas",
          "Olvida todo al cerrar la ventana", "El trabajo lo sigues haciendo tú"],
     good_t="Agente (Hermes y equivalentes)",
     good=["Recibe un objetivo y lo persigue hasta cumplirlo", "Lee tus archivos, consulta tus sistemas, busca datos",
           "Recuerda lo hecho y lo decidido entre sesiones", "El trabajo lo hace la máquina; tú revisas"])),

   ("piezas", dict(kicker="Anatomía", h2="Las 3 piezas de un agente",
     piezas=[("🧠 Modelo", "El cerebro que decide. Es lo de menos: hay decenas disponibles y se cambian sin reconstruir nada."),
             ("✋ Herramientas", "Las manos: leer archivos, entrar a un sistema, buscar en internet, hacer cálculos. Sin ellas no hay agente."),
             ("💾 Memoria", "Lo que recuerda entre una sesión y otra: tus datos, tus reglas, lo que ya se hizo. Es lo que convierte una consulta en un colaborador.")])),

   ("ejemplo", dict(kicker="Ejemplo a nivel directorio", h2="La misma orden, dos mundos",
     q="«Necesito saber cuánto nos costó el paro de la línea 3 el mes pasado.»",
     steps=["<b>Chatbot:</b> explica cómo podría calcularse, redacta una metodología, pide los datos. Vuelves al lunes siguiente.",
            "<b>Agente:</b> abre los registros de producción, cruza las horas detenidas con el costo por hora de cada línea, revisa los contratos con el cliente para ver si hay penalidad, y devuelve una cifra con su fuente.",
            "<b>Agente, parte 2:</b> deja el resultado en un archivo y un resumen de 5 líneas para el comité, con la fecha y el origen de cada dato."],
     meta="Lo que cambió no es la calidad de la redacción: es que alguien (algo) hizo el trabajo completo.")),

   ("error", dict(kicker="Error típico de la primera semana", h2="Pedir un texto cuando lo que se necesita es una tarea",
     warn="<b>Mal:</b> «Hazme un análisis del costo del paro.» → devuelve un texto genérico y elegante, sin haber mirado un solo dato tuyo.<br><br><b>Bien:</b> dar <b>objetivo + dónde están los datos + qué restricciones respetar + cómo quieres la salida</b>: «Lee los registros de producción de septiembre, cruza con el costo por hora de la línea 3, revisa si el contrato con el cliente tiene penalidad, y devuélveme una tabla con la cifra, el cálculo y la fuente de cada dato.»")),

   ("porque", dict(kicker="La buena noticia", h2="Un ejecutivo puede tener su propio agente",
     big="No hace falta un proyecto de transformación digital para empezar. Un agente personal corre en tu computador, con tu cuenta, y trabaja sobre <b>los archivos que tú le das</b>.",
     meta="Ese es el experimento de este curso: cada participante termina con un agente propio, usándolo en su trabajo real, sin depender del área de tecnología.")),

   ("lista", dict(kicker="El mapa del curso", h2="Las 4 etapas",
     items=["<b>Etapas 1-3:</b> entender qué es un agente, quién lo está usando en Chile y qué es Hermes. Instalarlo y darle tu primera tarea real.",
            "<b>Etapas 4-6:</b> darle lo que sabe tu empresa (datos, documentos, reglas) y ponerlo a producir: informes, análisis y comparaciones.",
            "<b>Etapas 7-9:</b> volverlo confiable: que no invente cifras, que sepa decir «no lo sé», que todo dato tenga fuente.",
            "<b>Etapas 10-12:</b> escalar y gobernar: varios agentes a la vez, permisos, riesgo, y qué exigirle a TI o a un proveedor."])),

   ("testeo", dict(kicker="El testeo", h2="Distingue la conversación de la ejecución",
     big="Frente a dos pantallas —una de un chatbot y una de un agente trabajando— señala qué hace cada una, quién ejecuta y dónde está el trabajo humano de control.",
     meta="Si no puedes nombrar qué está haciendo el agente y qué estás haciendo tú, todavía no tienes un criterio para comprar, autorizar o frenar un proyecto de IA.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Verificar lo que no te creas",
     links=[("McKinsey — The state of AI: Global Survey 2026 (informe vigente, ago 2026)", "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"),
            ("McKinsey — AI at work but not at scale (el gráfico del 88%, dic 2025)", "https://www.mckinsey.com/featured-insights/charts/ai-at-work-but-not-at-scale"),
            ("Hermes Agent — características (documentación oficial)", "https://hermes-agent.nousresearch.com/docs/user-guide/features/overview"),
            ("Instalar Hermes — guía paso a paso de este sitio", "guia-instalar-hermes.html")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 2
CLASES_EJEC.append((2, "Quién ya lo está usando en Chile",
  "No es una promesa de Silicon Valley: empresas chilenas de este tamaño ya tienen agentes trabajando en operaciones críticas. Qué hacen, qué ganaron y qué les costó.",
  [
   ("pregunta", dict(kicker="La pregunta del directorio", h2="¿Esto ya funciona en empresas como la nuestra?",
     big="Sí, y no en un piloto de laboratorio: en faenas, plantas y equipos legales. Lo que sigue son casos chilenos con nombre, cifra y fuente — para que el comité no discuta una idea, sino una realidad medida.",
     meta="Todas las cifras de esta clase salen de la revista corporativa de Empresas Copec (abril 2026) y de Forbes Chile (oct 2025). Fuente y fecha al pie de cada dato.")),

   ("definicion", dict(kicker="Caso 1 · ARAUCO", h2="Una gerencia dedicada a la IA, no un proyecto suelto",
     defn="ARAUCO creó una <b>gerencia de AI y Advanced Analytics</b> para pasar de esfuerzos aislados a adopción con escala. Su argumento: la IA es <b>sinérgica</b>; sin una visión común se pierden las economías de escala.",
     meta="Fuente: Revista Empresas Copec, abril 2026. Declaración de Juan Pablo Barros, gerente de AI y Advanced Analytics de ARAUCO.")),

   ("ejemplo", dict(kicker="Caso 2 · Calidad de Cosecha", h2="Del muestreo visual a medir el 100% de la faena",
     q="Cómo un dron cambió una decisión de operación",
     steps=["Drones capturan imágenes de alta resolución sobre la faena forestal.",
            "Modelos de visión identifican, dimensionan y clasifican <b>cada trozo de madera individual</b>.",
            "Se estima su volumen y se clasifica por valor comercial.",
            "El cruce con el inventario forestal identifica madera no aprovechada y estima la pérdida."],
     meta="Resultado publicado: 37% de mejora en la calidad promedio de las faenas. Pasó a operar automatizado en el primer trimestre de 2024. Ganó el Premio Nacional de Inteligencia Artificial Chile, PotencIA. Fuente: Revista Empresas Copec, abril 2026.")),

   ("porque", dict(kicker="Por qué ese caso es el interesante", h2="No reemplazó al experto: le cambió la pregunta",
     big="Antes, un jefe de faena discutía <b>una muestra</b> y una impresión visual. Ahora discute <b>todo el volumen cosechado</b>, con indicador objetivo. Lo que cambia no es el modelo: es que la conversación de margen ahora tiene evidencia completa.",
     meta="Declaración de José Miguel Echeverría, jefe de Procesamiento, Teledetección y Geomática de ARAUCO, en la misma fuente.")),

   ("lista", dict(kicker="Caso 3 · Celulosa", h2="El agente que diagnostica fallas en minutos, no en semanas",
     items=["<b>El problema:</b> una falla operacional compleja exige semanas de trabajo altamente especializado para encontrar la causa raíz.",
            "<b>Lo que hicieron:</b> un sistema de IA <b>multiagente</b> que integra manuales, bitácoras y datos de proceso.",
            "<b>Lo que entrega:</b> hipótesis de causa raíz y recomendaciones para acelerar la resolución.",
            "<b>Por qué importa:</b> en una planta, el tiempo de diagnóstico es directamente continuidad operacional y costo.",
            "<b>El otro salto:</b> gemelos digitales que replican el comportamiento de sistemas críticos con datos en tiempo real, para estabilizar procesos."],
     meta="Fuente: Revista Empresas Copec, abril 2026 (declaración de Juan Pablo Barros).")),

   ("piezas", dict(kicker="Caso 4 · Lo transversal", h2="Donde un ejecutivo lo ve primero: el trabajo de oficina",
     piezas=[("⚖️ Legal", "Agentes para procesos y análisis complejos: abogados con hasta 8 agentes armados según su propia necesidad, para optimizar flujos y ahorrar tiempo."),
             ("💰 Compras y Finanzas", "Sistemas de agentes orientados a agilizar procesos y abrir nuevas eficiencias."),
             ("🌲 Incendios", "165 cámaras robotizadas propias, visión artificial, apoyo satelital y simuladores de propagación en tiempo real.")])),

   ("vs", dict(kicker="El resto del mercado chileno", h2="Lo que otras empresas del país ya pusieron a andar",
     bad_t="Chat para adentro (productividad)",
     bad=["Copec: más de la mitad de sus 1.600 colaboradores usa IA en su rutina; 20.000 interacciones mensuales.",
          "Caja Los Andes: IA integrada para la productividad de sus más de 2.000 colaboradores."],
     good_t="Agentes en el proceso (resultado)",
     good=["Vida Cámara: agente experto en pólizas con arquitectura de agentes y subagentes — 15% de mejora en tiempos de atención.",
           "Entel Connect: 500.000 interacciones al mes, +30% de ventas promedio y propuestas duplicadas.",
           "diio: -80% de tiempo en tareas manuales de venta, con más de 20% de tasa de cierre."])),

   ("error", dict(kicker="Lo que la fuente dice que cuesta", h2="El cuello de botella no fue la tecnología",
     warn="ARAUCO declara que su principal desafío fue <b>la gestión del cambio y la adopción de las personas</b>: habilidades técnicas y una cultura que integre estas capacidades en el trabajo diario.<br><br>Si tu comité cree que el problema será elegir el modelo, el proyecto ya partió mirando el lugar equivocado.")),

   ("porque", dict(kicker="La lectura para tu empresa", h2="El patrón que se repite en todos los casos",
     big="Ninguno de estos casos partió por «adoptar IA». Todos partieron por un <b>problema que dolía</b> —una pérdida de madera, un diagnóstico tardío, un tiempo de atención— y la IA fue el instrumento. El que parte por la herramienta, termina con una licencia y un curso.",
     meta="Patrón observado en las cuatro fuentes de esta clase; es lectura propia, no una cita de las empresas.")),

   ("testeo", dict(kicker="El testeo", h2="Traduce un caso ajeno a tu propia operación",
     big="Toma uno de estos cuatro casos y nombra en tu empresa el proceso equivalente: qué se mide hoy por muestreo o por impresión, y cuánto valdría medirlo completo.",
     meta="Se evalúa que el caso elegido y el proceso propio sean comparables, y que el valor esté en una cifra o en una decisión concreta — no en «eficiencia».")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Las fuentes, para que TI y Auditoría las revisen",
     links=[("ARAUCO — Del futuro al presente: la IA en el negocio forestal (Empresas Copec, abr 2026)", "https://revista.empresascopec.cl/desde-adentro/arauco-del-futuro-al-presente-la-ia-en-el-negocio-forestal/"),
            ("Forbes Chile — Cómo están usando las empresas chilenas la IA (oct 2025)", "https://forbes.cl/ia/2025-10-09/como-estan-usando-las-empresas-chilenas-la-inteligencia-artificial"),
            ("Cómo usa Arauco la IA para optimizar el uso de la madera (ago 2026)", "https://www.cualestuhuella.cl/noticia/noticias/2026/08/arauco-inteligencia-artificial-madera-cosecha-forestal"),
            ("McKinsey — The state of AI (informe vigente 2026)", "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 3
CLASES_EJEC.append((3, "Hermes: el agente que usas tú",
  "No es un chatbot más: es un trabajador con memoria, herramientas y reglas. Qué es Hermes, de quién es, y por qué un ejecutivo puede tener el suyo sin depender de TI.",
  [
   ("pregunta", dict(kicker="La pregunta honesta", h2="¿Otro ChatGPT? ¿Por qué no usar lo que ya pagamos?",
     big="Porque ChatGPT te responde y se olvida. Hermes <b>trabaja sobre tus archivos, recuerda tus reglas y ejecuta</b>. La diferencia no es el modelo —que también puede ser el mismo— sino todo lo que hay alrededor.",
     meta="Hermes puede usar distintos modelos (incluidos los de pago que ya tienes). Lo que cambia es la envoltura: memoria, herramientas, reglas y registro.")),

   ("definicion", dict(kicker="La definición", h2="Qué es Hermes",
     defn="Hermes es un <b>agente abierto</b> creado por Nous Research que corre en tu propio computador (o en un servidor), usa el modelo de IA que tú elijas, y trabaja con <b>memoria persistente</b>, herramientas reales y reglas que tú escribes.",
     meta="Abierto = el código se puede auditar, y no quedas amarrado a un proveedor ni a un precio. Es la condición que un comité de riesgo pide antes de decir sí.")),

   ("piezas", dict(kicker="Con qué está armado", h2="Las cinco piezas que un ejecutivo debe saber nombrar",
     piezas=[("Memoria", "Recuerda entre sesiones: tus datos, tus convenciones, lo decidido. No hay que reexplicarle el contexto cada mañana."),
             ("Herramientas", "Lee y escribe archivos, busca en internet, corre cálculos, consulta sistemas, opera el navegador."),
             ("Reglas", "Un archivo de instrucciones propias: qué verificar, qué no afirmar, cuándo pedir permiso antes de actuar."),
             ("Perfil", "Una carpeta con lo que sabe de ti y de tu área, separable del resto: información delicada en un perfil, trabajo general en otro."),
             ("Registro", "Todo lo que hizo queda escrito y revisable. Es la pieza que permite auditarlo después.")])),

   ("loop", dict(kicker="Cómo trabaja", h2="De la orden al resultado, en cuatro pasos",
     lead="Le das un objetivo en lenguaje normal. Esto es lo que pasa después:",
     nodes=[("Tú escribes", "«arma el resumen de costos»"), ("Busca", "lee tus archivos y sistemas"),
            ("Calcula y verifica", "no inventa la cifra"), ("Entrega", "resultado + fuente de cada dato")],
     meta="En el medio puede corregirse solo: si un archivo no está o un dato no cuadra, vuelve atrás y lo busca, en vez de rellenar el hueco con algo plausible.")),

   ("vs", dict(kicker="Comparación honesta", h2="Hermes frente a las alternativas",
     bad_t="Herramientas cerradas",
     bad=["Tus datos salen a la nube del proveedor", "No puedes ver ni limitar lo que hace por dentro",
          "Precio y reglas cambian cuando el proveedor quiere", "Si el proveedor se cae, se cae tu proceso"],
     good_t="Hermes (abierto y propio)",
     good=["Corre donde tú decidas; el dato no sale si no lo autorizas",
           "Código auditable y reglas editables por ti",
           "Cambia de modelo sin rehacer el trabajo",
           "Queda el registro de todo lo que hizo"])),

   ("porque", dict(kicker="Por qué esto le importa a un directorio", h2="Riesgo de proveedor",
     big="Con un agente propio, la inteligencia es un insumo sustituible. Con una plataforma cerrada, la inteligencia es un proveedor del que dependes — con contratos, aumentos de precio y salida difícil.",
     meta="Es la misma pregunta que su comité hace por la nube o por el ERP: ¿qué pasa si mañana el proveedor sube el precio, cambia las condiciones o se retira del país?")),

   ("error", dict(kicker="Error típico", h2="Evaluar Hermes como si fuera un buscador",
     warn="<b>Mal:</b> sentarse a probarlo con preguntas de trivia. «¿Quién ganó el mundial?» — eso lo hace cualquier buscador.<br><br><b>Bien:</b> darle una tarea real y completa de tu trabajo: un archivo de verdad, un criterio de negocio, un formato de entrega. La prueba de un agente no es lo que sabe, es <b>lo que logra con lo que le das</b>.")),

   ("lista", dict(kicker="Qué NO es Hermes", h2="Para que la expectativa quede clara",
     items=["<b>No es un reemplazo de tu ERP ni de tu equipo:</b> es un ejecutor de tareas al que hay que dirigir y supervisar.",
            "<b>No es infalible:</b> puede equivocarse; el curso dedica tres clases a controlarlo. Lo que sí hace es dejar rastro de lo que hizo.",
            "<b>No se instala solo:</b> requiere instalar software en un computador y conseguir una llave de acceso a un modelo. Es la única parte técnica del curso, y se ve en la próxima clase.",
            "<b>No decide por ti:</b> investiga, calcula, redacta y alerta. La decisión —y la firma— siguen siendo humanas."])),

   ("ejemplo", dict(kicker="Ejemplo de esta misma semana", h2="Lo que Hermes hizo para un ejecutivo, en una sesión",
     q="Un caso real de uso, con las herramientas que tiene",
     steps=["Recibió una instrucción amplia: «rehacer este curso para otro público».",
            "Buscó el material existente en el disco antes de escribir nada: encontró el programa, el repositorio y el curso largo de referencia.",
            "Verificó los datos que iba a citar en fuentes primarias y descartó los titulares sin respaldo.",
            "Detectó que un requisito no definido cambiaba el resultado, y en vez de adivinar, preguntó."],
     meta="La última línea es la que decide si un agente sirve en una empresa: la diferencia entre «no sé» y una respuesta inventada con seguridad.")),

   ("testeo", dict(kicker="El testeo", h2="Nombra las cinco piezas",
     big="Un agente hace tres cosas distintas y tú debes poder decir cuál es cuál: recuerda, ejecuta, y pide permiso.",
     meta="Si confundes las tres, cualquier vendedor de IA te vende las que le convengan.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Para leer la fuente, no el resumen",
     links=[("Hermes Agent — características (documentación oficial)", "https://hermes-agent.nousresearch.com/docs/user-guide/features/overview"),
            ("Hermes Agent — repositorio del proyecto", "https://github.com/NousResearch/hermes-agent"),
            ("Nous Research — proyectos y modelos", "https://nousresearch.com"),
            ("Directrices del agente — cómo hacer que trabaje bien (este sitio)", "directrices-hermes.html")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 4
CLASES_EJEC.append((4, "Tu primer agente, andando esta semana",
  "La única clase técnica del curso — y aun así es de una tarde. Instalar Hermes, conectarle un modelo y darle la primera tarea real: la tuya.",
  [
   ("pregunta", dict(kicker="La objeción razonable", h2="«Yo no instalo software»",
     big="No hay que programar, pero sí hay que <b>escribir dos líneas en una ventana negra</b> y pegar una llave. Una tarde, una vez. La alternativa —esperar que TI lo haga— es un proyecto de tres meses para una prueba que se hace hoy.",
     meta="Es el mismo esfuerzo que instalar una impresora, con la diferencia de que aquí no hay un menú: hay que copiar y pegar.")),

   ("pasos", dict(kicker="El procedimiento", h2="Instalar Hermes, en cinco pasos",
     steps=[("Abre la Terminal:", "en Mac es una aplicación más (búscala en Launchpad). En Windows, PowerShell. No se rompe nada: es una ventana para dar órdenes escritas."),
            ("Pega el instalador:", "copia el comando de la guía de instalación de este sitio y pégalo en la ventana. Baja solo lo necesario y lo deja dentro de tu usuario."),
            ("Consigue una llave de acceso:", "es la credencial que conecta tu agente con un modelo de IA. Hay opciones gratuitas sin tarjeta: la guía trae cuáles y cómo se piden."),
            ("Conecta el modelo:", "tu agente te pide la llave la primera vez y la guarda. Desde ahí puede pensar, leer y ejecutar."),
            ("Verifica:", "pídele un diagnóstico de sí mismo. Si algo falta, el propio agente lo dice y explica cómo arreglarlo.")],
     meta="La guía paso a paso, con los comandos exactos y los errores típicos de cada paso: guia-instalar-hermes.html")),

   ("vs", dict(kicker="Dos caminos", h2="Tu agente, o un agente compartido por la empresa",
     bad_t="Instalación por persona",
     bad=["Cada ejecutivo instala en su equipo", "Control total de tus archivos y tus reglas",
          "No depende de una autorización de TI", "Requiere una tarde de cada uno"],
     good_t="Agente en un servidor, acceso por navegador",
     good=["Nadie instala nada: se entra por el navegador", "Un solo lugar que mantener y actualizar",
           "Sirve para un grupo grande de una sola vez", "La información queda en un servidor: exige gobernanza"]),
   ),

   ("error", dict(kicker="Error típico", h2="Instalarlo en la máquina equivocada",
     warn="<b>Mal:</b> instalarlo en el notebook que se lleva a la casa, con las credenciales de la cuenta corporativa del correo corporativo.<br><br><b>Bien:</b> decidir primero <b>qué información va a tocar</b> ese agente. Si va a ver información financiera o de personas, el equipo lo define el área de riesgo, no la costumbre. Un agente con acceso a todo es un problema de gobierno, no una comodidad.")),

   ("porque", dict(kicker="Antes de empezar", h2="Escoge la tarea por el dolor, no por la moda",
     big="La primera tarea no se elige por lo que suena innovador, sino por lo que hoy te quita <b>tres horas y no exige decidir</b>: consolidar un reporte, comparar dos propuestas, resumir 40 correos que nadie quiere leer.",
     meta="Es la misma lógica de los casos de la clase 2: se parte del problema que duele, no de la herramienta.")),

   ("ejemplo", dict(kicker="La primera tarea, bien formulada", h2="De «ayúdame con los costos» a una orden ejecutable",
     q="Cómo se le da una tarea a un agente",
     steps=["<b>Objetivo:</b> consolidar el gasto del mes por centro de costo.",
            "<b>Fuente:</b> el archivo de la planilla que exportas todos los meses (se lo entregas o le indicas la carpeta).",
            "<b>Criterio:</b> agrupar por centro de costo, comparar contra el mes anterior, marcar variaciones sobre 10%.",
            "<b>Restricciones:</b> no inventar cifras; si falta un dato, decirlo; no tocar el archivo original.",
            "<b>Entrega:</b> una tabla y un resumen de cinco líneas para el comité."],
     meta="Esa estructura —objetivo, fuente, criterio, restricciones, entrega— es reutilizable para el 90% de lo que le vas a pedir.")),

   ("testeo", dict(kicker="El testeo", h2="El agente corre en tu equipo",
     big="Muestra el agente respondiendo sobre un archivo tuyo, con la fuente a la vista. Corre en tu equipo, no en una diapositiva.",
     meta="Sube al curso solo lo que no sea sensible. Si la tarea usa información confidencial, demuéstralo con datos de ejemplo.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Los materiales de esta clase",
     links=[("Instalar Hermes — paso a paso (este sitio)", "guia-instalar-hermes.html"),
            ("Hermes Agent — instalación (documentación oficial)", "https://hermes-agent.nousresearch.com/docs/getting-started/installation"),
            ("Directrices del agente — el archivo de reglas (este sitio)", "directrices-hermes.html")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 5
CLASES_EJEC.append((5, "Darle lo que sabe tu empresa",
  "Un agente sin tus datos opina. Con tus datos, informa. Cómo se le entrega el conocimiento de la empresa sin copiarlo a mano ni exponer lo que no corresponde.",
  [
   ("pregunta", dict(kicker="La pregunta clave", h2="¿Por qué mi agente no sabe nada de mi empresa?",
     big="Porque no le has dado nada. El modelo sabe de libros y de internet, no de tu planta ni de tus contratos. <b>Tu contexto es el activo</b>: la IA es lo que lo aprovecha.",
     meta="Es la razón por la que dos empresas con el mismo modelo y los mismos proveedores obtienen resultados distintos.")),

   ("definicion", dict(kicker="Concepto", h2="Memoria: lo que el agente conserva entre sesiones",
     defn="La memoria de Hermes es un conjunto de <b>hechos estables</b> que se cargan en cada sesión: quién eres, cómo se llaman las cosas en tu empresa, qué convenciones hay. Se escribe una vez y sirve para todo lo que venga después.",
     meta="La regla sana: en memoria, hechos del entorno que aplican siempre. Procedimientos y pasos, en la biblioteca de tareas. Mezclarlos es lo que vuelve inservible a un agente.")),

   ("vs", dict(kicker="La distinción que ordena todo", h2="Dos tipos de conocimiento, dos lugares",
     bad_t="Hechos estables → memoria",
     bad=["Es política uso siempre el cierre de mes calendario", "Los centros de costo se nombran «NNNN-00»",
          "Mi comité se reúne el segundo martes", "El informe va en el formato X"],
     good_t="Procedimientos → biblioteca de tareas",
     good=["Cómo se cierra el mes, paso a paso", "Cómo se calcula el costo por tonelada",
           "Cómo se prepara el informe de comité", "Cómo se revisa un contrato de suministro"])),

   ("error", dict(kicker="El error que cuesta caro", h2="Meter todo en la memoria",
     warn="<b>Mal:</b> pegar el manual de la empresa completo en la memoria del agente. Se carga en <b>cada</b> consulta, aunque no tenga nada que ver, y el agente se vuelve lento, caro y confuso.<br><br><b>Bien:</b> memoria corta con los hechos de siempre, y los procedimientos en una biblioteca que se consulta cuando la tarea lo pide.")),

   ("piezas", dict(kicker="Las cuatro fuentes de conocimiento", h2="Qué le puedes conectar a un agente",
     piezas=[("Archivos", "Planillas, informes, contratos, minutas. Lo más rápido de empezar y lo que ya tienes en el disco."),
             ("Correo", "El hilo de una negociación, las aprobaciones. Alto valor y alto riesgo: exige permiso explícito."),
             ("Sistemas", "El ERP, el sistema de mantenimiento, el de personas. Es lo más potente: el dato sale de la fuente y no de una copia."),
             ("Internet", "Normativa, prensa, licitaciones, precios de referencia. Con la condición de la clase 8: fuente o no se usa.")])),

   ("ejemplo", dict(kicker="El patrón correcto", h2="Puente, no copia",
     q="Por qué no exportar el ERP a una planilla y darle esa planilla al agente",
     steps=["<b>La copia envejece el día que se hace.</b> Al día siguiente dos números distintos compiten: el del sistema y el de la copia.",
            "<b>Si discrepan, ¿cuál gana?</b> Nadie lo sabe, y esa discusión cuesta más que el ahorro.",
            "<b>El patrón correcto:</b> el agente consulta la fuente (o recibe el export oficial del proceso que ya existe).",
            "<b>Resultado:</b> un solo origen para la cifra, y la trazabilidad que Auditoría y el directorio exigen."],
     meta="Aplica igual a cualquier sistema: si el dato vive en el ERP, se pregunta ahí. La copia propia es un problema nuevo, no una solución.")),

   ("porque", dict(kicker="Por qué aquí gana una empresa grande", h2="El dato es la ventaja, no el modelo",
     big="Cualquier competidor puede contratar el mismo modelo mañana. Lo que no puede copiar es <b>tu historia de costos, tus bitácoras de planta y tus 20 años de decisiones</b>. La ventaja competitiva está en esa base, no en la IA.",
     meta="Es el mismo argumento del caso de ARAUCO en celulosa: el agente integra manuales, bitácoras y datos de proceso — activos que solo ellos tienen.")),

   ("pasos", dict(kicker="La tarea de esta clase", h2="Conectar una fuente de conocimiento, con criterio",
     steps=[("Elige una fuente:", "una carpeta de documentos de tu área que uses de verdad (informes mensuales, actas, contratos)."),
            ("Define los hechos estables:", "cinco a diez convenciones que el agente debe saber siempre (cómo se nombran las cosas, qué formato, qué se considera normal)."),
            ("Déjalos en la memoria:", "no el manual completo: los hechos que aplican siempre."),
            ("Prueba con una pregunta que hoy te cuesta:", "algo que hoy obliga a abrir tres archivos."),
            ("Compara contra tu respuesta:", "el agente y tú, por separado, la misma pregunta. Ahí se ve si la fuente sirve.")])),

   ("testeo", dict(kicker="El testeo", h2="Del archivo disperso a la respuesta con fuente",
     big="Muestra al agente respondiendo una pregunta que hoy exige abrir tres archivos, y señala de qué archivo salió cada parte.",
     meta="Se evalúa que la respuesta sea verificable. Una respuesta correcta sin fuente no acredita: en un comité no se puede defender.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Material de esta clase",
     links=[("Directrices del agente — qué va en las reglas y qué no (este sitio)", "directrices-hermes.html"),
            ("Hermes Agent — memoria y contexto (documentación oficial)", "https://hermes-agent.nousresearch.com/docs/user-guide/features/overview"),
            ("Cómo ARAUCO integra manuales y bitácoras con agentes (Empresas Copec)", "https://revista.empresascopec.cl/desde-adentro/arauco-del-futuro-al-presente-la-ia-en-el-negocio-forestal/")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 6
CLASES_EJEC.append((6, "Ponerlo a producir",
  "De la consulta suelta al trabajo delegado: cómo se le encarga un producto completo —un informe, un análisis, una comparación— y cómo se revisa lo que entrega.",
  [
   ("pregunta", dict(kicker="El salto de nivel", h2="«Ya me responde» no es «ya me sirve»",
     big="Responder preguntas es la mitad del camino. El valor real aparece cuando el agente <b>produce el entregable entero</b>: el informe de comité, la comparación de tres proveedores, el análisis de la desviación.",
     meta="Y ahí cambia lo que tienes que saber hacer: ya no es escribir preguntas, es definir el encargo y revisar el producto.")),

   ("definicion", dict(kicker="Concepto", h2="Encargo de trabajo, no instrucción de chat",
     defn="Un <b>encargo</b> tiene cinco partes: resultado esperado, fuentes que puede usar, reglas de calidad, qué hacer cuando falta información, y formato de entrega. Sin las cinco, el agente improvisa — y una improvisación en un informe de comité se paga caro.",
     meta="La diferencia práctica: con instrucción de chat obtienes un borrador; con encargo obtienes un producto que puedes firmar o rechazar con criterio.")),

   ("vs", dict(kicker="Dos formas de pedir", h2="Instrucción vs. encargo",
     bad_t="Instrucción de chat",
     bad=["«Hazme un análisis de las desviaciones del trimestre»", "El agente elige qué mirar y cómo",
          "Resultado distinto cada vez que lo pides", "No puedes defenderlo frente a nadie"],
     good_t="Encargo",
     good=["Qué entregable, para quién, con qué fuentes", "Qué se considera bien hecho, escrito de antemano",
           "Mismo encargo, mismo procedimiento, resultado comparable", "Cada cifra con su origen: se puede auditar"])),

   ("ejemplo", dict(kicker="Ejemplo real", h2="El informe de desviación, encargado bien",
     q="Encargo típico de un gerente de operaciones",
     steps=["<b>Entregable:</b> informe de desviación del trimestre, máximo 2 páginas, para el comité.",
            "<b>Fuentes:</b> el reporte de producción del trimestre y el presupuesto aprobado. Nada más.",
            "<b>Regla de calidad:</b> toda variación sobre 5% explicada con su causa; si no hay causa en la fuente, se marca «por confirmar».",
            "<b>Si falta información:</b> preguntar antes de escribir, no rellenar con supuestos.",
            "<b>Formato:</b> tabla de cifras + tres conclusiones + un anexo con el cálculo de cada número."],
     meta="Compara con el informe que hoy se arma a mano: el contenido es el mismo trabajo, pero las reglas quedaron escritas antes de empezar.")),

   ("error", dict(kicker="Error típico", h2="Aceptar el resultado porque está bien escrito",
     warn="<b>Mal:</b> una respuesta impecable en la forma se aprueba sin abrir la fuente. El estilo fluido no es evidencia de haber leído los datos.<br><br><b>Bien:</b> revisar <b>una cifra al azar contra el archivo original</b>. Si esa cuadra y el anexo explica cómo se calculó, el resto es revisable. Si no cuadra, el informe entero está en duda.")),

   ("porque", dict(kicker="Dónde está tu valor", h2="Tu trabajo se mueve, no desaparece",
     big="Antes: <b>producir</b> el informe. Después: <b>definir</b> qué significa «bien hecho» y <b>revisar</b> lo que llegó. Es un trabajo más chico en horas y más grande en criterio — y es exactamente el que un directorio espera de un gerente.",
     meta="Y es lo que un agente no puede hacer: definir el estándar es una decisión de negocio, no de software.")),

   ("lista", dict(kicker="Qué se puede delegar hoy", h2="Tareas de oficina que rinden de inmediato",
     items=["<b>Consolidaciones:</b> un número único a partir de cinco planillas que nadie mantiene igual.",
            "<b>Comparaciones:</b> tres propuestas de proveedor contra los mismos criterios, con la diferencia señalada.",
            "<b>Resúmenes de comité:</b> minutas de 40 páginas convertidas en decisiones, responsables y fechas.",
            "<b>Barridos de riesgo:</b> contratos revisados contra una cláusula que siempre debe estar.",
            "<b>Investigación de mercado:</b> prensa, licitaciones y competencia sobre un tema puntual — con las reglas de la clase 8."])),

   ("pasos", dict(kicker="La tarea de esta clase", h2="Encargar un producto completo",
     steps=[("Elige un entregable recurrente:", "uno que ya produzcas cada mes y que puedas mostrar (con datos de ejemplo si es sensible)."),
            ("Escribe las cinco partes:", "resultado, fuentes, regla de calidad, qué hacer ante faltantes, formato."),
            ("Ejecútalo con el agente:", "y guarda el encargo escrito: lo vas a reutilizar todos los meses."),
            ("Verifica una cifra al azar:", "contra el archivo original, y revisa que el anexo explique el cálculo."),
            ("Ajusta el encargo, no el resultado:", "si algo sale mal, el arreglo va en la instrucción, no en corregir a mano cada vez.")])),

   ("testeo", dict(kicker="El testeo", h2="Entrega el producto y su encargo",
     big="Presenta el informe terminado junto al encargo escrito con que se pidió, y verifica una cifra contra la fuente en vivo.",
     meta="Se evalúa que el producto sirva para tomar la decisión, y que el encargo se pueda reutilizar. Un buen resultado sin encargo reutilizable no escala.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Material de esta clase",
     links=[("Anthropic — Building effective agents (el patrón de encargo y verificación)", "https://www.anthropic.com/research/building-effective-agents"),
            ("Directrices del agente — reglas para que no invente (este sitio)", "directrices-hermes.html"),
            ("McKinsey — The state of AI, informe 2026 (qué separa a los que capturan valor)", "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 7
CLASES_EJEC.append((7, "Cuando la IA inventa: el riesgo de las cifras",
  "El riesgo que mata proyectos en un directorio no es que el agente sea lento: es que entregue un número falso con seguridad total. Cómo se detecta y cómo se bloquea.",
  [
   ("pregunta", dict(kicker="El riesgo real", h2="La IA no miente: completa",
     big="Un modelo de lenguaje no tiene una tabla de verdades: tiene una habilidad entrenada para <b>producir la continuación más plausible</b>. Cuando no sabe un dato, la continuación plausible es un dato inventado que parece correcto.",
     meta="No es un defecto que se arregle con una versión mejor del modelo. Es cómo funciona, y por eso se controla por diseño.")),

   ("vs", dict(kicker="Dónde es más peligroso", h2="Los dos tipos de respuesta",
     bad_t="Respuesta de opinión (riesgo bajo)",
     bad=["«¿Qué deberíamos priorizar este trimestre?»", "«¿Cómo se estructura un comité de riesgo?»",
          "No hay una única respuesta correcta", "El error se detecta discutiendo"],
     good_t="Respuesta de hecho (riesgo alto)",
     good=["«¿Cuánto gastamos en mantención en 2025?»", "«¿Qué dice la cláusula 12 del contrato?»",
           "Hay UNA respuesta correcta y es verificable", "El error se descubre en el comité, o no se descubre"])),

   ("ejemplo", dict(kicker="Cómo se ve el invento", h2="Tres formas en que un dato falso entra a un informe",
     q="Las tres se ven igual de creíbles",
     steps=["<b>El dato desplazado:</b> la cifra existe en el archivo, pero es de otro mes o de otra faena.",
            "<b>El dato completado:</b> falta un valor, y el agente pone el promedio «para que el cuadro cierre».",
            "<b>La fuente fantasma:</b> cita un informe, una norma o un estudio que no existe, con nombre y año verosímiles."],
     meta="Los tres pasan cualquier revisión de forma. Solo se detectan yendo al archivo original, y por eso el control tiene que ser de proceso.")),

   ("piezas", dict(kicker="Los cuatro controles", h2="Cómo se bloquea, en orden de eficacia",
     piezas=[("Fuente obligatoria", "Regla escrita: toda cifra sin archivo de origen se marca «por confirmar», nunca se completa."),
             ("Extractor, no memoria", "Que la cifra la lea un programa del archivo, y el agente solo la ordene y la explique."),
             ("Verificación cruzada", "Dos caminos independientes para el mismo número: si no coinciden, no se publica."),
             ("Muestra humana", "Una cifra al azar contra el original, en cada entrega. Barato y detecta casi todo.")])),

   ("error", dict(kicker="Error típico en la organización", h2="Confiar en la revisión de forma",
     warn="<b>Mal:</b> el informe se revisa por ortografía, formato y coherencia interna. Un dato inventado es perfectamente coherente consigo mismo.<br><br><b>Bien:</b> la revisión es <b>contra la fuente</b>, en puntos muestreados. Es la misma lógica que la auditoría de toda la vida: no se revisa todo, se revisa bien elegido.")),

   ("porque", dict(kicker="Por qué esto es un tema de directorio", h2="Un dato falso en un informe firmado tiene dueño",
     big="Si un gerente firma un informe construido con un agente y una cifra es falsa, la responsabilidad no es del modelo. <b>La cadena de responsabilidad es la misma de siempre</b>: la firma es humana, y por eso el proceso de verificación también.",
     meta="Es la razón por la que la clase 9 (gobernanza) existe en este curso: sin reglas escritas, el agente es un pasivo, no un activo.")),

   ("lista", dict(kicker="Qué exigirle al proveedor", h2="Las cinco preguntas del comité de riesgo",
     items=["<b>¿De dónde saca cada cifra?</b> Que muestre el archivo y la línea, no solo el número.",
            "<b>¿Qué hace cuando falta un dato?</b> La respuesta correcta es «lo dice», nunca «lo estima».",
            "<b>¿Se puede repetir la misma consulta y obtener lo mismo?</b> Si no, no es un proceso: es una anécdota.",
            "<b>¿Queda registro de lo que hizo?</b> Sin registro no hay auditabilidad.",
            "<b>¿Quién responde si un dato es falso?</b> Si la respuesta es el proveedor, mal: la responsabilidad es de la empresa."])),

   ("definicion", dict(kicker="La regla que ordena todo", h2="«No lo resuelve» no es lo mismo que «no lo revisé»",
     defn="En toda entrega de un agente hay tres estados posibles de un dato: <b>verificado con fuente</b>, <b>marcado como faltante</b>, o <b>no revisado</b>. El único inaceptable es el tercero presentado como el primero.",
     meta="Es también el criterio con que se evalúa a las personas en este trabajo: distinguir lo que no se pudo resolver de lo que no se revisó.")),

   ("testeo", dict(kicker="El testeo", h2="Encuentra el invento",
     big="Se entrega un informe con un dato falso plantado. El grupo debe encontrarlo en menos de diez minutos, usando solo el archivo original.",
     meta="Si no lo encuentran, el problema no es el ejercicio: es que la organización no tiene proceso de verificación, y un agente sin ese proceso es un riesgo, no una herramienta.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Material de esta clase",
     links=[("Directrices del agente — las reglas que evitan el invento (este sitio)", "directrices-hermes.html"),
            ("MIT — por qué el 70% de los usuarios dice que la herramienta no aprende de sus correcciones", "https://www.salesforce.com/news/stories/why-ai-pilots-fail/"),
            ("Caso del curso de Auditoría — cómo se construyó un Estado de Resultados, con los dos errores cometidos (este sitio)", "caso-estado-resultados.html")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 8
CLASES_EJEC.append((8, "Fuente o no se usa",
  "El mismo estándar que se le exige a un analista se le exige al agente: cada afirmación con su origen. Cómo se escribe esa regla y cómo se comprueba que se cumple.",
  [
   ("pregunta", dict(kicker="La regla del comité", h2="¿Con qué criterio se acepta un dato que trajo un agente?",
     big="El mismo con que se acepta el de un analista nuevo: <b>que se pueda rastrear</b>. La ventaja del agente es que puede dejar el rastro completo, archivo y línea, de cada número que usó — si se le exige.",
     meta="Sin esa exigencia, un agente es más rápido pero no más confiable que una persona que improvisa.")),

   ("definicion", dict(kicker="Concepto", h2="Trazabilidad: el rastro que hace defendible una cifra",
     defn="Trazabilidad es poder responder, para cada número de un entregable, <b>de qué archivo salió, en qué línea está y qué cálculo se aplicó</b>. Si esa cadena se corta en algún punto, el número no es un dato: es una afirmación.",
     meta="No es un requisito de tecnología: es el mismo principio que la empresa ya aplica en contabilidad y en auditoría.")),

   ("vs", dict(kicker="Los dos estándares", h2="Lo que se acepta y lo que no",
     bad_t="No sirve",
     bad=["«Según los datos, el costo bajó 12%»", "Cita un informe sin nombre, fecha ni página",
          "Un dato «aproximado» sin decir de dónde viene", "Un resumen perdido sin enlace al original"],
     good_t="Sirve",
     good=["«Costo unitario: 12.400 (archivo costos_sep2026.xlsx, hoja L3, fila 47)»",
           "«Norma N° 21.595, artículo 3, texto vigente al [fecha]»",
           "«No hay dato en la fuente para septiembre: se marca por confirmar»",
           "«Fuente primaria: revista corporativa, abril 2026»"])),

   ("ejemplo", dict(kicker="Ejemplo verificado", h2="Cómo se cita bien, con un caso real de este curso",
     q="La misma afirmación, tres niveles de respaldo",
     steps=["<b>Nivel 0 (no sirve):</b> «Arauco mejoró su cosecha con drones.»",
            "<b>Nivel 1 (mejor):</b> «Arauco mejoró 37% la calidad de sus faenas con un sistema de drones y visión artificial.»",
            "<b>Nivel 2 (defendible):</b> «+37% de calidad promedio de faenas; proyecto reconocido con el Premio Nacional de IA Chile PotencIA; operando automatizado desde el primer trimestre de 2024. Fuente: Revista Empresas Copec, abril 2026.»"],
     meta="Solo el nivel 2 se le puede entregar a un directorio. Un dato con fuente, fecha y autor se puede defender; sin eso, se discute.")),

   ("error", dict(kicker="Error típico", h2="Confundir el resumen con la fuente",
     warn="<b>Mal:</b> citar lo que dijo un medio sobre un informe. Muchas veces el medio agrega una interpretación que el informe no dice.<br><br><b>Bien:</b> llegar al documento original —el informe, el repositorio, la norma, la ficha del producto— y citar de ahí. Si solo existe el resumen, decirlo: «según X, que cita Y».")),

   ("porque", dict(kicker="Por qué esto sube el nivel de la conversación", h2="Sin fuente, la reunión es de opiniones",
     big="La reunión que discute <b>cifras con origen</b> termina en decisiones. La que discute impresiones necesita otra reunión. Un agente que entrega fuente cambia el registro de la conversación, no solo la velocidad.",
     meta="Y cambia quién puede participar: el que tiene el dato puede discutir con el que tiene el cargo.")),

   ("lista", dict(kicker="Cómo se escribe la regla", h2="Las reglas mínimas que van en el agente",
     items=["<b>Toda cifra lleva su fuente</b> (archivo y ubicación, o norma y artículo, o documento y fecha).",
            "<b>Sin fuente, se marca como faltante.</b> No se estima, no se completa, no se «aproxima».",
            "<b>Distinguir dato de interpretación:</b> «el costo bajó 12%» es dato; «la causa fue la mantención» es interpretación y va marcada como tal.",
            "<b>Fecha de medición:</b> toda cifra lleva cuándo se midió, porque el dato de hace seis meses ya no describe la operación.",
            "<b>Fuente primaria primero:</b> el documento original antes que el resumen de terceros."])),

   ("pasos", dict(kicker="La tarea de esta clase", h2="Auditar un entregable del propio agente",
     steps=[("Toma un entregable de la clase 6:", "el informe que produjo el agente."),
            ("Abre cada cifra:", "verifica archivo y línea, o norma y artículo. Marca cada uno como verificado, faltante o no revisado."),
            ("Cuenta:", "cuántas verificaron, cuántas no tenían fuente y cuántas estaban mal."),
            ("Escribe el arreglo:", "la regla concreta que faltaba en el encargo (no la corrección manual del número)."),
            ("Reejecuta:", "con la regla nueva, y compara la tasa de cifras con fuente.")])),

   ("testeo", dict(kicker="El testeo", h2="Cada cifra con su rastro",
     big="Entregable con todas sus cifras marcadas: verificada con fuente, faltante, o no revisable. El número de «no revisable» debe ser cero.",
     meta="Se evalúa la trazabilidad, no la belleza del informe. Un informe feo con todas las fuentes se defiende; uno elegante sin fuentes no.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Las fuentes primarias de este curso",
     links=[("Revista Empresas Copec — ARAUCO y la IA (abr 2026)", "https://revista.empresascopec.cl/desde-adentro/arauco-del-futuro-al-presente-la-ia-en-el-negocio-forestal/"),
            ("McKinsey — The state of AI, Global Survey 2026 (informe original)", "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"),
            ("Hermes Agent — documentación oficial", "https://hermes-agent.nousresearch.com/docs")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 9
CLASES_EJEC.append((9, "Los límites: permisos, datos y firmas",
  "Un agente con acceso a todo es un riesgo con buena redacción. Qué puede hacer solo, qué debe preguntar y qué nunca debe tocar — decidido antes, no después del incidente.",
  [
   ("pregunta", dict(kicker="La pregunta de control", h2="¿Qué puede hacer tu agente sin pedirte permiso?",
     big="Esa respuesta no la puede dar el proveedor: es una <b>decisión de la empresa</b>. Si nadie la escribió, la respuesta por defecto es «todo lo que técnicamente pueda» — y eso es exactamente el problema.",
     meta="Es el mismo ejercicio de siempre: definir atribuciones. La diferencia es que aquí el que las recibe no es un empleado, es un programa que no tiene miedo ni sentido común.")),

   ("vs", dict(kicker="El criterio que ordena los permisos", h2="Reversible o irreversible",
     bad_t="Hacer solo (reversible)",
     bad=["Leer archivos y buscar información", "Calcular y preparar borradores",
          "Resumir, comparar, ordenar", "Consultar sistemas en modo lectura"],
     good_t="Pedir permiso (irreversible o con efecto externo)",
     good=["Enviar un correo o un mensaje", "Escribir o modificar un registro en un sistema",
           "Publicar o compartir un documento", "Gastar dinero o comprometer un proveedor"])),

   ("piezas", dict(kicker="Las tres decisiones que van por escrito", h2="Qué se define antes de soltarlo",
     piezas=[("Datos", "Qué información puede ver: la de su área, la de la empresa, la de personas. Se resuelve con perfiles separados y carpetas, no con confianza."),
             ("Acciones", "Qué puede ejecutar solo y qué requiere aprobación explícita. Regla dura: lo irreversible siempre pregunta."),
             ("Registro", "Qué queda escrito de lo que hizo, y quién lo revisa. Sin registro no hay control posible, solo fe.")])),

   ("ejemplo", dict(kicker="Ejemplo de la frontera", h2="El mismo agente, dos decisiones distintas",
     q="Por qué la frontera no es «la IA sí o no», sino «qué acción»",
     steps=["<b>Preparar el correo al proveedor pidiendo la cotización revisada:</b> reversible, sin efecto externo → lo hace solo y lo deja en borrador.",
            "<b>Enviarlo firmado por la gerencia:</b> efecto externo, compromete a la empresa → pide aprobación y la deja registrada.",
            "<b>Cambiar el precio en el sistema:</b> modifica el dato maestro → nunca solo, y con doble control.",
            "<b>Archivar el contrato vencido:</b> reversible pero afecta a terceros → avisa y espera."],
     meta="Ninguna de estas cuatro respuestas la puede dar el proveedor de IA: son decisiones de la empresa sobre sus propias atribuciones.")),

   ("error", dict(kicker="El error que se paga con una denuncia", h2="Darle acceso a todo «para que sirva mejor»",
     warn="<b>Mal:</b> conectar el correo completo, la carpeta de personas y el ERP «para que tenga contexto».<br><br><b>Bien:</b> el mínimo necesario para la tarea, con perfiles separados. La información de personas, las negociaciones abiertas y los datos financieros no auditados tienen dueño y no se conectan por comodidad.")),

   ("porque", dict(kicker="Por qué la ley ya lo pide", h2="La protección de datos no es un trámite nuevo",
     big="La nueva ley de datos personales (N° 21.719) ya está publicada, y el régimen completo rige desde el <b>1 de diciembre de 2026</b>. Crea una agencia con facultades sancionatorias. Si el agente trata datos de clientes o de trabajadores, la empresa es <b>responsable</b> igual que si lo hiciera una persona.",
          meta="El agente no crea una excepción a la ley: obliga a aplicar la que ya existe. Fuente: Ley N° 21.719 (D.O. 13.12.2024), texto vigente desde el 1 de diciembre de 2026.")),

   ("lista", dict(kicker="La conversación con el abogado y con TI", h2="Las cinco preguntas que hay que responder por escrito",
     items=["<b>1. ¿Qué datos ve el agente?</b> Enumerados, no «los necesarios».",
            "<b>2. ¿Dónde corren esos datos?</b> En un equipo de la empresa, en un servidor propio o en la nube de un proveedor.",
            "<b>3. ¿Qué acciones ejecuta sin aprobación?</b> Con el criterio reversible / irreversible.",
            "<b>4. ¿Quién revisa lo que hizo, y con qué frecuencia?</b> Un nombre y una cadencia, no un área.",
            "<b>5. ¿Cómo se revoca?</b> Si mañana hay un incidente, cómo se apaga en minutos, no en semanas."])),

   ("testeo", dict(kicker="El testeo", h2="La matriz de atribuciones",
     big="Cada grupo presenta su agente con la lista de lo que hace solo, lo que pregunta y lo que nunca toca — y defiende por qué cada acción está en esa columna.",
     meta="Se evalúa el criterio, no la lista: una acción irreversible en la columna «solo» reprueba el ejercicio completo, aunque funcione.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Material de esta clase",
     links=[("Hermes Agent — perfiles separados y permisos (documentación oficial)", "https://hermes-agent.nousresearch.com/docs/user-guide/features/overview"),
            ("Directrices del agente — la regla de pedir permiso en lo irreversible (este sitio)", "directrices-hermes.html"),
            ("Ley 21.719 — nueva ley de protección de datos personales (BCN)", "https://www.bcn.cl/leychile/navegar?idNorma=1209272")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 10
CLASES_EJEC.append((10, "Varios agentes, un proceso",
  "Cuando una tarea es demasiado grande para un solo agente: cómo se divide el trabajo entre varios, qué gana la empresa y qué se vuelve más difícil de controlar.",
  [
   ("pregunta", dict(kicker="El caso", h2="El cierre de mes no cabe en un solo encargo",
     big="Un cierre exige conciliar bancos, revisar provisiones, calcular variaciones, redactar el informe y contestar las observaciones del comité. Un agente puede hacer cada parte; <b>varios agentes pueden hacer el proceso completo</b>, en paralelo.",
     meta="Es la diferencia entre tener un ayudante y tener un equipo. Y un equipo, igual que en la vida real, exige coordinación.")),

   ("definicion", dict(kicker="Concepto", h2="Qué es un proceso de varios agentes",
     defn="Es un <b>reparto de trabajo</b> entre agentes especializados, cada uno con su tarea y su fuente, más un agente que coordina, junta los resultados y verifica que no se contradigan entre sí.",
     meta="No es más inteligencia: es división del trabajo. Lo que se gana es paralelismo; lo que se pierde es simplicidad.")),

   ("piezas", dict(kicker="Cómo se reparte", h2="Tres formas de dividir, según el problema",
     piezas=[("En paralelo", "Tareas independientes al mismo tiempo: conciliación, provisiones y variaciones. El más rápido y el más fácil de controlar."),
             ("En cadena", "Una tarea alimenta la siguiente: extraer, calcular, redactar, revisar. Aquí un error se propaga: hay que verificar en cada eslabón."),
             ("Coordinador", "Un agente reparte, junta y detecta contradicciones. Obligatorio cuando hay más de tres piezas o cuando el resultado se firma.")])),

   ("vs", dict(kicker="La comparación honesta", h2="Uno o varios",
     bad_t="Un agente solo",
     bad=["Simple de entender y de auditar", "Un solo punto de falla, fácil de ubicar",
          "Se satura con tareas largas: pierde el hilo", "Barato y rápido de montar"],
     good_t="Varios agentes",
     good=["Procesa en paralelo: el cierre en horas, no en semanas", "Cada parte con su fuente y su responsable",
           "Necesita coordinador o los resultados se contradicen", "Más caro, más complejo, más difícil de auditar"])),

   ("ejemplo", dict(kicker="Ejemplo real de la fuente", h2="El caso de celulosa: por qué multiagente",
     q="Cómo se explica que un sistema así resuelva en minutos lo que tomaba semanas",
     steps=["El diagnóstico de una falla exige leer manuales, bitácoras y datos de proceso: tres fuentes distintas, con lenguajes distintos.",
            "Un solo agente tendría que cargar todo junto y se perdería; el sistema <b>integra</b> las fuentes con agentes especializados.",
            "El resultado es una hipótesis de causa raíz con recomendaciones, no un volcado de información.",
            "Beneficio medido por la empresa: lo que requería semanas de trabajo especializado se resuelve en minutos."],
     meta="Fuente: Revista Empresas Copec, abril 2026. Es el argumento más claro de por qué la arquitectura importa: no es más IA, es mejor reparto.")),

   ("error", dict(kicker="Error típico", h2="Multiplicar agentes sin multiplicar control",
     warn="<b>Mal:</b> cinco agentes trabajando y un solo control al final. Si dos se contradicen, nadie sabe cuál tiene razón y hay que rehacer todo.<br><br><b>Bien:</b> verificación en cada unión — cuando dos ramas se juntan, se cruzan los números. La regla: <b>el que coordina no produce, verifica</b>.")),

   ("porque", dict(kicker="Cuándo NO vale la pena", h2="La decisión de arquitectura, en simple",
     big="Si la tarea cabe en un encargo y se ejecuta en minutos, un agente alcanza. Varios agentes se justifican cuando el trabajo tiene <b>partes independientes, volumen alto o fuentes muy distintas</b>. Lo demás es complicarse por moda.",
     meta="La pregunta correcta no es «¿cuántos agentes puedo tener?» sino «¿cuál es el cuello de botella real?».")),

   ("lista", dict(kicker="El diseño del proceso", h2="Qué se define antes de repartir trabajo",
     items=["<b>Qué partes son independientes:</b> esas van en paralelo, y son la ganancia real de tiempo.",
            "<b>Qué partes dependen de otras:</b> ahí va verificación al final de cada eslabón, sin excepción.",
            "<b>Quién junta:</b> un solo responsable del resultado final, con nombre. El resto son proveedores internos.",
            "<b>Dónde se cruzan los números:</b> en cada unión, dos fuentes distintas para la misma cifra crítica.",
            "<b>Qué se registra:</b> qué hizo cada agente y con qué fuente, para poder reconstruir cualquier conclusión."])),

   ("testeo", dict(kicker="El testeo", h2="El proceso completo, en vivo",
     big="Mostrar el proceso de tres partes corriendo: qué hizo cada agente, dónde se cruzaron los números y qué se detectó al juntar.",
     meta="Se evalúa que las contradicciones se hayan detectado <b>antes</b> del resultado final. Un proceso que entrega limpio porque nadie cruzó nada no es un proceso: es una suma de opiniones.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Material de esta clase",
     links=[("ARAÚCO — sistema multiagente en celulosa (Empresas Copec, abr 2026)", "https://revista.empresascopec.cl/desde-adentro/arauco-del-futuro-al-presente-la-ia-en-el-negocio-forestal/"),
            ("Anthropic — patrones de trabajo con varios agentes", "https://www.anthropic.com/research/building-effective-agents"),
            ("Clase 0 del curso de Auditoría — cómo se construye un agente (este sitio)", "clase-harness-contabilidad.html")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 11
CLASES_EJEC.append((11, "Gobernar la IA sin frenar la empresa",
  "El comité no necesita entender de modelos: necesita cuatro decisiones escritas. Qué rol tiene la empresa, qué exige a un proveedor y cómo se mide si esto sirve.",
  [
   ("pregunta", dict(kicker="La pregunta del directorio", h2="¿Quién responde cuando un agente se equivoca?",
     big="La empresa, siempre. Ningún contrato traslada la responsabilidad de una decisión de negocio a un proveedor de software. Por eso <b>el gobierno de la IA es gobierno de la empresa</b>, no del área de tecnología.",
     meta="Y por eso esta clase no es técnica: son cuatro decisiones que se toman una vez y se revisan una vez al año.")),

   ("piezas", dict(kicker="Las cuatro decisiones", h2="Lo mínimo que debe estar escrito",
     piezas=[("Rol", "Quién es el dueño de cada agente en producción. Un nombre por proceso, no un área. Y quién puede apagarlo."),
             ("Límites", "Qué datos ve, qué acciones ejecuta solo y qué exige aprobación. La matriz de la clase 9, firmada."),
             ("Registro", "Qué queda de lo que hizo, dónde, por cuánto tiempo y quién lo revisa. Sin esto no hay auditoría posible."),
             ("Métrica", "Qué número tiene que mover para seguir pagándolo. Si no está definido antes, se defiende con anécdotas.")])),

   ("vs", dict(kicker="Cómo se compra esto", h2="Plataforma cerrada vs. agente propio",
     bad_t="Plataforma cerrada",
     bad=["Rápido de implementar y sin instalar nada", "Tus datos y tu contexto viven en el proveedor",
          "Cambia el precio y la política cuando él decide", "Salir es caro: el conocimiento quedó adentro"],
     good_t="Agente propio (abierto)",
     good=["Corre donde la empresa decida", "El conocimiento queda en casa y es reutilizable",
           "Se cambia de modelo sin rehacer el trabajo", "Exige capacidades internas: alguien que lo mantenga"])),

   ("error", dict(kicker="El error de gobernanza más común", h2="Comprar pilotos en vez de construir capacidades",
     warn="<b>Mal:</b> un piloto por área, cada uno con su proveedor, sin registro común ni criterio compartido. A los seis meses hay doce pilotos y ninguna capacidad.<br><br><b>Bien:</b> pocas iniciativas, todas con el mismo estándar de fuente, registro y permisos, y una capacidad interna que queda cuando el proveedor se va.")),

   ("porque", dict(kicker="Lo que dicen los números", h2="El valor no llega solo",
     big="El 88% de las empresas usa IA, pero solo 6% puede atribuirle un impacto significativo al resultado. Y el 95% de los pilotos del MIT no demostró retorno. <b>La diferencia entre esas cifras no es el modelo: es el gobierno.</b>",
     meta="Cifras: McKinsey (uso 88%, dic 2025; 6% de alto desempeño, informe 2026) y el informe del MIT (NANDA, ago 2025). Las dos están en el slide de fuentes.")),

   ("lista", dict(kicker="El checklist del directorio", h2="Seis preguntas, una vez al año",
     items=["<b>1.</b> ¿Tenemos una lista de los agentes que hoy están en producción, con dueño y función?",
            "<b>2.</b> ¿Cada uno tiene definido qué datos ve y qué puede ejecutar sin aprobación?",
            "<b>3.</b> ¿Queda registro de lo que hicieron y alguien lo revisa con cadencia?",
            "<b>4.</b> ¿Sabemos cuánto costó y qué número movió?",
            "<b>5.</b> ¿Podemos apagar cualquiera de ellos en minutos?",
            "<b>6.</b> ¿Si el proveedor de IA sube el precio o se va, el trabajo sigue? (Capacidad interna, no contrato.)"])),

   ("definicion", dict(kicker="La regla que evita el desastre", h2="La firma sigue siendo humana",
     defn="Ningún entregable que salga de la empresa —un informe, una cotización, un pago, una comunicación a un cliente— se emite sin <b>un responsable humano con nombre</b> que lo haya revisado. El agente prepara; la persona responde.",
     meta="Es la misma regla de siempre, aplicada a una herramienta nueva. Y es lo que permite usar agentes en procesos críticos sin que el directorio asuma un riesgo que no entiende.")),

   ("testeo", dict(kicker="El testeo", h2="El acta de gobernanza",
     big="Cada grupo redacta el acta de una página: qué agente, de quién depende, qué datos ve, qué requiere aprobación, cómo se mide y cómo se apaga.",
     meta="Se evalúa que se pueda firmar hoy. Un acta con «por definir» no es gobernanza: es una intención.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Material de esta clase",
     links=[("McKinsey — The state of AI, informe 2026 (dónde está la brecha de valor)", "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"),
            ("MIT / NANDA — por qué fallan los pilotos (resumen con las cifras)", "https://www.salesforce.com/news/stories/why-ai-pilots-fail/"),
            ("Ley 21.719 — protección de datos personales (BCN)", "https://www.bcn.cl/leychile/navegar?idNorma=1209272")])),
  ]))

# ══════════════════════════════════════════════════ CLASE 12
CLASES_EJEC.append((12, "El plan de 90 días",
  "Cierre: cada participante se va con un plan escrito y aprobado por su propia área — no con una idea. Qué se hace en 30, 60 y 90 días, y cómo se sabe si funcionó.",
  [
   ("pregunta", dict(kicker="La pregunta de cierre", h2="¿Qué cambia el lunes en tu empresa?",
     big="Un curso que termina en «fue muy interesante» es un gasto. Este termina con <b>un plan escrito, con dueño, fecha y número</b> — y la primera tarea ejecutada hoy, no la próxima semana.",
     meta="Es el mismo criterio que el testeo de la clase 1: distinguir una conversación de una ejecución, ahora aplicado al cierre.")),

   ("pasos", dict(kicker="El plan", h2="30, 60 y 90 días",
     steps=[("Días 1-30 — el experimento:", "un agente, una tarea, una persona. Elige el proceso que hoy quita tres horas y no exige decidir. Sin integración, sin proveedor, sin comité."),
            ("Días 31-60 — el control:", "aplica las reglas de fuente (clase 8) y la matriz de permisos (clase 9) a ese experimento. Mide cuántas cifras tenían origen y cuántas no."),
            ("Días 61-90 — la decisión:", "con los números del experimento, decide escalar, rediseñar o cerrar. Documenta la decisión y su porqué.")],
     meta="El orden importa: primero el valor, después el control, y solo entonces la escala. Al revés, el proyecto muere en el comité de riesgo antes de mostrar nada.")),

   ("vs", dict(kicker="Cómo se mide", h2="Indicador de esfuerzo vs. indicador de resultado",
     bad_t="Esfuerzo (no sirve para decidir)",
     bad=["Cuántas personas lo usan", "Cuántas consultas se hicieron", "Cuántas horas de capacitación",
          "Cuántos agentes se construyeron"],
     good_t="Resultado (sí sirve)",
     good=["Horas liberadas en un proceso concreto", "Cifras verificadas contra la fuente, y su tasa de error",
           "Días entre el cierre y el informe disponible", "Observaciones del comité que bajan porque el dato estaba bien"])),

   ("error", dict(kicker="Error típico del cierre", h2="Presentar el piloto como transformación",
     warn="<b>Mal:</b> «implementamos IA en la compañía». Nadie sabe qué significa, nadie puede medirlo, y a los seis meses el presupuesto se corta.<br><br><b>Bien:</b> «redujimos el informe de desviación de 3 días a 4 horas en la línea 3, con 100% de las cifras verificadas contra el ERP, en 90 días». Eso se defiende en cualquier comité.")),

   ("porque", dict(kicker="Lo que se llevan", h2="Tres activos, no una idea",
     big="Al terminar, cada participante tiene: <b>un agente funcionando</b> en una tarea real, <b>un encargo escrito</b> reutilizable cada mes, y <b>un acta de gobernanza</b> con dueño y métrica. Eso es lo que queda cuando el entusiasmo se va.",
     meta="Y son activos de la empresa, no del asistente al curso: se pueden entregar, auditar y heredar.")),

   ("lista", dict(kicker="Los cinco errores que se repiten", h2="Lo que las empresas ya aprendieron",
     items=["<b>Partir por la herramienta.</b> Todos los casos de la clase 2 partieron por un problema que dolía.",
            "<b>No medir antes.</b> Sin la línea base, ningún resultado es demostrable al final.",
            "<b>Dejar el cambio para TI.</b> La adopción la hace el gerente del proceso, no el área de sistemas.",
            "<b>Confundir piloto con capacidad.</b> Un piloto que se apaga no deja nada; una capacidad queda.",
            "<b>Ignorar a las personas.</b> ARAUCO declaró que su principal desafío fue la gestión del cambio, no la tecnología."])),

   ("testeo", dict(kicker="El testeo final", h2="Presenta y defiende el plan",
     big="Cada grupo presenta su plan de 90 días: el proceso elegido, el indicador de resultado, quién responde y cómo se apaga. Con la primera tarea ya ejecutada.",
     meta="Se evalúa que el plan sea defendible frente al área que lo va a recibir — no la calidad de la presentación. Lo que importa: que mañana alguien pueda empezar.")),

   ("links", dict(kicker="Fuentes y para profundizar", h2="Para seguir solo",
     links=[("Hermes Agent — documentación oficial", "https://hermes-agent.nousresearch.com/docs"),
            ("Instalar Hermes — guía de este sitio", "guia-instalar-hermes.html"),
            ("Directrices del agente — reglas para que trabaje bien (este sitio)", "directrices-hermes.html"),
            ("McKinsey — The state of AI 2025", "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai"),
            ("Revista Empresas Copec — ARAUCO y la IA", "https://revista.empresascopec.cl/desde-adentro/arauco-del-futuro-al-presente-la-ia-en-el-negocio-forestal/")])),
  ]))
