#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep dive: Modelos de IA vs Agentes de IA + contextos de entrenamiento.
Reutiliza el CSS y el template `deck()` de gen_ppts.py (mismo design system).
Regenerar: python3 gen_modelos_agentes.py  — determinista, cero tokens de LLM.
"""
import html as _html
from gen_ppts import CSS, deck, render_slide, AU, IN

esc = _html.escape

# Curso contenedor (usa el branding de Auditoría, pero es transversal a ambos electivos)
DD = {"nombre": "Deep dive transversal · Modelos, agentes y contexto",
      "short": "Modelos vs Agentes",
      "color": "#0a7a3d", "soft": "#eefaf1", "level": "Clase 0 · Deep dive",
      "plan": "index.html"}

SLIDES = [
 ("pregunta", dict(
   kicker="La pregunta que abre todo",
   h2="¿Es lo mismo «usar una IA» que «tener un agente»?",
   big="No. Y la diferencia no es de potencia, es de <b>quién hace el trabajo</b>. Al final de esta clase vas a poder mirar cualquier herramienta de IA y decir en qué categoría cae — y por qué eso cambia lo que puedes delegar.")),

 ("piezas", dict(
   kicker="Las dos categorías",
   h2="Los dos tipos que vas a ver todo el semestre",
   piezas=[
     ("🧠 MODELO de IA", "Un cerebro sin manos. Recibe un texto, devuelve un texto. Sabe muchísimo, pero no puede actuar."),
     ("🤖 AGENTE de IA", "El modelo + herramientas + memoria + un bucle de decisión. Decide qué hacer, lo hace, y vuelve a decidir."),
     ("🔑 La clave", "Todo agente TIENE un modelo adentro. Ningún modelo solo es un agente. Es una relación de «contiene», no de competencia.")])),

 ("definicion", dict(
   kicker="Definición 1",
   h2="Qué es un modelo de IA",
   defn="Un modelo es una <b>función matemática</b>: entra algo, sale algo. Le das un texto y predice la continuación; le das una imagen y devuelve una etiqueta; le das una serie de datos y detecta una anomalía.",
   meta="Tres propiedades que lo definen: (1) no recuerda entre consultas, (2) no decide nada por su cuenta, (3) no ejecuta acciones. Le preguntas dos veces lo mismo y no sabe que ya te respondió antes.")),

 ("definicion", dict(
   kicker="Definición 2",
   h2="Qué es un agente de IA",
   defn="Un agente es un programa que recibe un <b>objetivo</b>, <b>decide por sí mismo</b> qué hacer, usa <b>herramientas</b> (archivos, internet, código, APIs) y repite hasta cumplirlo.",
   meta="El agente no espera que le digas cada paso. Le das la meta y él arma el camino. Ahí está toda la diferencia práctica.")),

 ("vs", dict(
   kicker="La comparación directa",
   h2="Modelo vs. agente, lado a lado",
   bad_t="MODELO (solo responde)",
   bad=["Le mandas texto, te devuelve texto",
        "No recuerda nada entre consultas",
        "No ejecuta ninguna acción",
        "Tú haces el trabajo; él aconseja",
        "No sabe si su respuesta sirvió"],
   good_t="AGENTE (ejecuta el trabajo)",
   good=["Recibe un objetivo, no una pregunta",
         "Recuerda lo que ya hizo y qué falta",
         "Usa herramientas: archivos, APIs, código",
         "La máquina hace el trabajo; tú supervisas",
         "Verifica el resultado y corrige el rumbo"])),

 ("loop", dict(
   kicker="El mecanismo",
   h2="Cómo funciona un agente por dentro",
   lead="Todo agente, sin excepción, repite este ciclo hasta cumplir el objetivo:",
   nodes=[("🎯 Objetivo", "qué hay que lograr"),
          ("PENSAR", "¿qué hago ahora?"),
          ("ACTUAR", "usar una herramienta"),
          ("OBSERVAR", "ver qué pasó")],
   meta="Si el resultado no cumple el objetivo, vuelve a PENSAR con la información nueva. Es un bucle, no una respuesta única. Esa repetición es lo que lo hace autónomo.")),

 ("ejemplo", dict(
   kicker="Ejemplo real de todos los días",
   h2="La misma tarea, dos mundos",
   q="«Necesito saber cuántos clientes nuevos tuve este mes.»",
   steps=[
     "<b>Con un modelo (chat):</b> le describes tu problema, te explica cómo hacerlo en Excel, y te dice «deberías revisar tu base de datos». El trabajo lo haces tú.",
     "<b>Con un agente:</b> le das el objetivo. Abre tu base de datos, filtra por fecha, cuenta los clientes nuevos, hace el gráfico y te devuelve el reporte listo.",
     "<b>La diferencia:</b> el modelo te dio un consejo. El agente te dio el resultado. Uno te ahorró tiempo de pensar; el otro te ahorró la pega completa."],
   meta="Ojo: el agente usa un modelo adentro para decidir cada paso. El modelo es el motor; el agente es el auto completo.")),

 ("vs", dict(
   kicker="La analogía que sirve",
   h2="El consultor encerrado vs. el consultor con acceso",
   bad_t="Modelo = consultor sin teléfono",
   bad=["Sabe muchísimo de su tema",
        "Está encerrado en una pieza",
        "Solo te habla cuando le preguntas",
        "No puede tocar tus archivos",
        "No puede llamar a nadie"],
   good_t="Agente = el mismo consultor con todo",
   good=["El mismo conocimiento experto",
         "Con computador y acceso a tus datos",
         "Con permiso para actuar solo",
         "Puede buscar, calcular, escribir",
         "Y reportarte cuando terminó"])),

 ("error", dict(
   kicker="Error típico",
   h2="Creer que un modelo «más grande» se vuelve agente",
   warn="<b>No.</b> Cambiar de un modelo bueno a uno mejor no lo convierte en agente: sigue siendo un cerebro sin manos.<br><br>Lo que convierte un modelo en agente no es su tamaño, sino <b>agregarle herramientas, memoria y un bucle de decisión</b>. Un modelo chico con buenas herramientas hace más trabajo real que un modelo enorme que solo conversa.")),

 ("pregunta", dict(
   kicker="Cambio de tema",
   h2="Ahora la segunda pregunta: ¿cómo «aprendió» lo que sabe?",
   big="Cuando hablamos de «contexto» nos referimos a <b>tres cosas distintas</b> que se confunden todo el tiempo. Si las separas, entiendes por qué una IA te puede hablar de la Segunda Guerra Mundial pero no sabe nada de tu empresa.")),

 ("piezas", dict(
   kicker="Los tres contextos",
   h2="Tres cosas que se llaman «contexto»",
   piezas=[
     ("1️⃣ Contexto de ENTRENAMIENTO", "Con qué datos se formó el modelo. Ocurre UNA VEZ, antes de que exista. Después no cambia."),
     ("2️⃣ Contexto = VENTANA", "Cuánto texto cabe a la vez en su «mente». Es memoria de trabajo, no permanente."),
     ("3️⃣ Contexto INYECTADO", "La información que le das al momento de preguntar: el prompt, un documento, un RAG.")])),

 ("definicion", dict(
   kicker="Contexto 1",
   h2="Contexto de entrenamiento: con qué se formó",
   defn="Son los datos con los que el modelo aprendió a hablar y razonar. Ocurre <b>una sola vez</b>, antes de que el modelo exista, y se «hornea» en sus parámetros internos.",
   meta="Los modelos grandes se entrenan con billones de palabras: páginas web, libros, artículos, código. Es un proceso que cuesta millones de dólares y semanas de cómputo.")),

 ("lista", dict(
   kicker="Contexto 1 · Consecuencias",
   h2="Tres consecuencias que debes entender",
   items=[
     "<b>No se puede consultar.</b> Nadie puede preguntarle al modelo «¿de qué libro sacaste esa frase?». El conocimiento quedó mezclado, no guardado como una biblioteca.",
     "<b>Tiene fecha de corte.</b> Todo lo que pasó después de esa fecha, el modelo no lo sabe. Por eso puede afirmar cosas desactualizadas con total seguridad.",
     "<b>No sabe nada de ti.</b> Tu empresa, tus datos, tus clientes nunca estuvieron en el entrenamiento. Si el modelo te habla de ellos, los está inventando."])),

 ("definicion", dict(
   kicker="Contexto 2",
   h2="Ventana de contexto: cuánto cabe a la vez",
   defn="Es la cantidad máxima de texto que el modelo puede «tener presente» en una sola interacción. Se mide en <b>tokens</b> (aprox. 1 token = ¾ de palabra en español).",
   meta="Es memoria de trabajo, como el escritorio donde apoyas los papeles. Si algo no está en el escritorio, el modelo no lo ve — aunque «lo sepa» de otras conversaciones o del entrenamiento.")),

 ("ejemplo", dict(
   kicker="Contexto 2 · En la práctica",
   h2="Qué significa una ventana de 128.000 tokens",
   q="Una ventana grande: ¿para qué sirve realmente?",
   steps=[
     "<b>Ventana chica:</b> cabe una conversación corta. Si le pasas un informe largo, se queda con el principio y el final — el medio desaparece.",
     "<b>Ventana grande (128k):</b> cabe un libro completo. Puedes darle todo el contrato, todas las normas del semestre, y razona sobre el conjunto.",
     "<b>Pero atención:</b> ventana grande no es memoria permanente. Al cerrar la conversación, se vacía. Para que recuerde de verdad, hay que guardar afuera y volver a inyectar."],
   meta="Por eso existe el RAG: en vez de meter 1.000 documentos al escritorio, guardas los documentos afuera y le traes solo los 5 pedazos que necesita para esta pregunta.")),

 ("definicion", dict(
   kicker="Contexto 3",
   h2="Contexto inyectado: lo que le das al preguntar",
   defn="Es la información que le entregas <b>en el momento</b> de la consulta. No cambia el modelo: solo cambia lo que el modelo ve en esta interacción.",
   meta="Es la forma real en que le enseñas algo nuevo a una IA hoy. Tres técnicas, de menor a mayor esfuerzo: prompt directo, RAG, y fine-tuning.")),

 ("piezas", dict(
   kicker="Contexto 3 · Las tres técnicas",
   h2="Cómo se le da conocimiento nuevo a una IA",
   piezas=[
     ("📋 Prompt", "Le pegas el texto en la consulta. Cabe lo que quepa en la ventana. Simple, inmediato, pero manual."),
     ("🔍 RAG", "Buscas los fragmentos relevantes en tus documentos y se los inyectas. Así funciona un buscador inteligente sobre tus propios archivos."),
     ("🎓 Fine-tuning", "Reentrenas el modelo con tus datos. Cambia el modelo mismo. Es caro, lento, y casi nunca necesario si tienes RAG.")])),

 ("porque", dict(
   kicker="Por qué esto importa en tu carrera",
   h2="El modelo es commodity; el contexto es el activo",
   big="Cualquier empresa puede contratar el mismo modelo que tú. Es un insumo que se compra, como la luz eléctrica. <b>Lo que no se puede comprar son tus datos, tu corpus y las herramientas que armaste alrededor.</b>",
   meta="Por eso el valor no está en «usar IA», sino en tener información propia que la IA no tiene, y un agente que la explote. Ahí no hay competencia: es tuyo.")),

 ("ejemplo", dict(
   kicker="El caso que lo cierra",
   h2="Dos empresas, el mismo modelo, resultados opuestos",
   q="Las dos pagan la misma API. ¿Por qué una gana?",
   steps=[
     "<b>Empresa A:</b> usa el modelo para redactar correos. Buen modelo, cero contexto propio. Cualquiera la iguala mañana.",
     "<b>Empresa B:</b> usa el mismo modelo, pero le inyecta por RAG su normativa interna, sus contratos y su historial de casos. El agente decide con información que nadie más tiene.",
     "<b>La conclusión:</b> el modelo es idéntico. La diferencia es el contexto propietario y el agente que lo usa. Eso no se copia."],
   meta="Regla para recordar: <b>no compites por el modelo (se compra), compites por el contexto (se construye).</b>")),

 ("lista", dict(
   kicker="Resumen para llevarte",
   h2="Las tres ideas de hoy",
   items=[
     "<b>1. Modelo ≠ agente.</b> El modelo responde; el agente ejecuta. Todo agente contiene un modelo, pero ningún modelo solo es un agente.",
     "<b>2. «Contexto» son tres cosas.</b> El entrenamiento (una vez, no cambia), la ventana (memoria de trabajo, se llena y se vacía) y lo inyectado (lo que le das al preguntar).",
     "<b>3. El activo no es el modelo.</b> Es información propietaria + herramientas. El modelo es el motor; lo que te diferencia es qué le das de comer y qué le dejas hacer."])),

 ("testeo", dict(
   kicker="El testeo",
   h2="Demuestra que lo entendiste",
   big="Explícale a tu compañero, en 60 segundos y sin leer: (1) la diferencia entre un modelo y un agente, con un ejemplo de tu vida, (2) los tres significados de «contexto», y (3) por qué el contexto propio vale más que el modelo.",
   meta="Si puedes hacerlo con tus palabras, entendiste el concepto más importante de todo el semestre. Si no, vuelve a las diapositivas 5 y 12.")),

 ("links", dict(
   kicker="Para profundizar",
   h2="Lecturas y recursos",
   links=[("Building Effective Agents (Anthropic)", "https://www.anthropic.com/research/building-effective-agents"),
          ("Google Colab (para probar ya)", "https://colab.research.google.com"),
          ("Groq — key gratis de IA", "https://console.groq.com/keys"),
          ("Plan de clases del curso", "auditoria-ia-agentica.html")])),
]

if __name__ == "__main__":
    for nombre, curso in [("modelos-vs-agentes.html", DD),
                          ("modelos-vs-agentes-innovacion.html", dict(DD, color=IN["color"], soft=IN["soft"],
                                                                       nombre="Deep dive transversal · Modelos, agentes y contexto",
                                                                       plan="innovacion-disruptiva.html"))]:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(deck(curso, curso, 0, "Deep dive transversal",
                         "Modelos de IA vs. Agentes de IA",
                         "Dos conceptos que se confunden todo el tiempo, y los tres significados de «contexto» que necesitas separar para entender por qué una IA sabe de historia pero no sabe nada de tu empresa.",
                         SLIDES))
        print(f"  {nombre}  ({len(SLIDES)+1} slides)")
