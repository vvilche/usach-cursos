#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera clase-harness-multientorno.html — deck para el Electivo IV (Auditoría).

Tema: por qué el mismo modelo rinde distinto según la herramienta que lo envuelve,
y cómo se entrena un modelo DENTRO de esas herramientas.

Fuentes (verificadas en primaria, 6 oct 2026):
- "The ultimate guide to multi-harness RL" — Adithya S Kolavi / FineEnvs, HF Space.
  https://huggingface.co/spaces/AdithyaSK/multi-harness-rl
- Checkpoint FineEnvs/LFM2.5-2.6B-multiharness-RL (54.2% pass@1, step 1000)
- Post de @ClementDelangue (5 oct 2026) y @NousResearch (5 oct 2026)
- Paper citado en el articulo: Agent Lightning v1.0 / harnessed agentic RL

Reutiliza la plantilla del curso importando desde gen_ppts (idempotente).
"""
from gen_ppts import CSS, deck, AU

OUT = "clase-harness-multientorno.html"

TITULO = "El mismo modelo, otra herramienta"
LEAD = ("Por qué un agente rinde distinto según el programa que lo envuelve — y cómo se entrena "
        "un modelo de IA para que funcione bien en cualquier herramienta, no solo en la suya.")

SLIDES = [

    ("pregunta", dict(
        kicker="La pregunta de hoy",
        h2="¿Por qué el mismo modelo acierta 62% en una herramienta y 33% en otra?",
        big="Mismos pesos, mismas preguntas, mismo día. Solo cambia el programa que lo envuelve. "
            "Ese programa tiene nombre: <b>harness</b>. Y explica más del resultado que el modelo mismo.")),

    ("definicion", dict(
        kicker="Recordatorio del bloque 1",
        h2="Qué es el harness, otra vez",
        defn="El harness es <b>todo lo que no es el modelo</b>: el bucle, las herramientas que le da, "
             "el contexto que le escribe, cómo interpreta lo que devuelve, y cuándo lo detiene.",
        meta="Ya lo vimos en la Clase 0. Hoy vamos a ver cuánto pesa, medido.")),

    ("pregunta", dict(
        kicker="El hallazgo",
        h2="El harness mueve la aguja más que el modelo",
        big="Estudio de 2026 sobre SWE-bench Verified: cambiar el harness movió el resultado "
            "<b>13 puntos</b>. Cambiar el modelo dentro del mismo harness lo movió <b>2,5 a 5 puntos</b>.")),

    ("lista", dict(
        kicker="Cómo se ve en la práctica",
        h2="Tres mediciones del mismo fenómeno",
        items=[
            "GLM-5.2: <b>23%</b> en un harness y <b>52%</b> en otro — mismo modelo, mismos pesos.",
            "Claude Opus 4.5: <b>45,9%</b> en un leaderboard público y <b>55,4%</b> dentro de Claude Code.",
            "GLM-5.1, GPT-5.4 y Kimi K2.6 (3 puntos de diferencia entre sí): <b>cada uno gana bajo una configuración de harness distinta</b>.",
        ])),

    ("pregunta", dict(
        kicker="Y lo incómodo",
        h2="El ranking no se traslada entre modelos",
        big="Un harness puede ser el 2º mejor de diez para un modelo y el 9º para otro. "
            "No existe «el mejor harness»: existe el mejor <b>para este modelo en esta tarea</b>.")),

    ("porque", dict(
        kicker="Por qué importa para la pega",
        h2="Una nota de benchmark no describe al modelo: describe al modelo <i>en ese harness</i>",
        big="Cuando alguien te dice «este modelo saca 62%», la pregunta correcta es: "
            "¿62% con qué herramienta?",
        meta="Es la misma pregunta que hacerse con un dato contable sin su fuente.")),

    ("error", dict(
        kicker="El error que hay que evitar",
        h2="«Ya lo probé con ChatGPT y no sirve»",
        warn="<b>Mal:</b> descartar la IA porque la probaste en una herramienta y no dio resultado.<br><br>"
             "<b>Bien:</b> entender que probaste <b>una combinación</b> de modelo + herramienta + instrucciones. "
             "Cambiar cualquiera de las tres cambia el resultado.")),

    ("pregunta", dict(
        kicker="La segunda parte",
        h2="¿Y si entrenamos al modelo dentro de la herramienta?",
        big="Hasta ahora: se elige un modelo y se lo mete en la herramienta, y hay que aguantarse lo que salga. "
            "Lo nuevo: <b>entrenar al modelo dentro de la herramienta real</b>, con refuerzo.")),

    ("definicion", dict(
        kicker="Concepto nuevo",
        h2="Qué es el aprendizaje por refuerzo, en una frase",
        defn="Se le da al modelo una tarea y una <b>recompensa</b>. Lo intenta muchas veces. "
             "A las respuestas que salen bien se les sube la probabilidad, a las que salen mal se les baja. "
             "Nadie le dice cómo hacerlo: lo descubre intentando.",
        meta="Es la misma lógica del aprendizaje supervisado de un junior, pero automatizada y a escala de miles de intentos.")),

    ("vs", dict(
        kicker="La distinción que importa",
        h2="Enseñarle a imitar vs. dejarlo intentar",
        bad_t="Ajuste supervisado (SFT) · imitar",
        bad=[
            "Se le muestran los aciertos de un modelo mayor y se le pide copiarlos",
            "Aprende del <b>éxito ajeno</b>",
            "No puede aprender a hacer menos intentos",
            "En la medición: llegó a 47,5%",
        ],
        good_t="Refuerzo (RL) · intentar",
        good=[
            "Lo intenta él, se le premia el acierto",
            "Aprende de <b>su propio intento</b>",
            "Se puede premiar que acierte con <b>menos intentos</b>",
            "En la medición: llegó a 54% y con 31% menos llamadas",
        ])),

    ("loop", dict(
        kicker="Cómo funciona por dentro",
        h2="El problema técnico: el harness no deja mirar adentro",
        lead="El modelo vive dentro del harness. Para entrenarlo hay que ver exactamente qué generó, y el harness no lo muestra.",
        nodes=[
            ("Modelo", "el que queremos entrenar"),
            ("Harness", "no deja ver qué genera"),
            ("Entrenador", "necesita verlo para corregir"),
        ],
        meta="La solución no fue reescribir el harness. Fue poner un intermediario.")),

    ("piezas", dict(
        kicker="La solución, en tres piezas",
        h2="Un intermediario que el harness cree que es el modelo",
        piezas=[
            ("1 · Proxy de captura", "Se pone entre el harness y el modelo. El harness cree que le habla a la API. En realidad le habla al intermediario, que anota absolutamente todo."),
            ("2 · Traductor", "El harness habla cuatro idiomas distintos según cuál sea. El intermediario los entiende todos y los unifica en uno solo."),
            ("3 · Entrenador", "Con el registro exacto de lo que el modelo generó, el entrenador ya puede corregirlo y mejorarlo."),
        ])),

    ("porque", dict(
        kicker="Lo elegante",
        h2="Ninguna de las 10 herramientas se modificó",
        big="Claude Code, Codex, Hermes, Pi, OpenCode y otras cinco pasan por el intermediario "
            "<b>tal como se instalan</b>. No se les tocó una línea de código.",
        meta="No hubo que reimplementar cada herramienta como un simulador: se las usó de verdad, las reales.")),

    ("lista", dict(
        kicker="El experimento",
        h2="Qué midieron, en concreto",
        items=[
            "Modelo chico y abierto: <b>LFM2.5-2.6B</b> (2.600 millones de parámetros).",
            "<b>1.000 tareas</b> de análisis de datos, sacadas de notebooks reales.",
            "<b>250 tareas reservadas</b> que el modelo nunca vio, para medir.",
            "Dos corridas: entrenado en <b>una sola herramienta</b> vs. entrenado en <b>cuatro a la vez</b>.",
        ])),

    ("vs", dict(
        kicker="El resultado",
        h2="Entrenar en una vs. entrenar en cuatro",
        bad_t="Solo en OpenCode",
        bad=[
            "Mejora mucho donde entrenó: <b>34% → 58%</b>",
            "Casi no mejora en las otras tres herramientas",
            "Promedio final: 52%",
            "Aprendió las mañas de <b>esa</b> herramienta",
        ],
        good_t="En las cuatro a la vez",
        good=[
            "Mejora en <b>las cuatro</b>, incluida donde no entrenó",
            "<b>42% → 54%</b> de promedio",
            "Promedio final: 54%",
            "Aprendió a resolver la tarea, no el trámite de una herramienta",
        ])),

    ("pregunta", dict(
        kicker="El detalle que sorprende",
        h2="31% menos llamadas a la herramienta",
        big="En las tareas que ya resolvía, el modelo entrenado pasó a hacer <b>un 31% menos de consultas</b>. "
            "Se le premió acierto <i>y</i> economía: acertar rápido vale más que acertar dando vueltas.")),

    ("error", dict(
        kicker="El otro resultado",
        h2="Imitar sirvió menos que intentar",
        warn="El modelo entrenado <b>imitando</b> los aciertos de uno mucho mayor (27B contra 2,6B) llegó a "
             "<b>47,5%</b>. El entrenado <b>intentando</b> llegó a <b>54%</b>.<br><br>"
             "Y el de imitación escondía el daño: subía en tres herramientas y <b>caía 17 puntos</b> en la cuarta. "
             "El promedio parecía bien; el detalle estaba mal. <b>Es exactamente lo que no debe pasar en una auditoría.</b>")),

    ("porque", dict(
        kicker="Para qué te sirve saberlo",
        h2="Tres cosas que puedes usar mañana",
        big="1 · Antes de descartar una IA, cambia de herramienta antes que de modelo.<br>"
            "2 · Un resultado sin decir con qué herramienta se midió no es un dato.<br>"
            "3 · Los modelos abiertos y chicos ya se pueden adaptar a tu flujo.",
        meta="El modelo de este experimento pesa 2.600 millones de parámetros: cabe en un notebook. No es un modelo de frontera.")),

    ("testeo", dict(
        kicker="Lo que hay que llevarse",
        h2="El harness pesa más que el modelo",
        big="Cambiar la herramienta mueve el resultado 13 puntos. Cambiar el modelo, 2,5 a 5. "
            "La conclusión práctica: <b>el problema casi nunca es «la IA es mala»; es que está mal ensamblada</b>.",
        meta="Y ahora se sabe que también se le puede enseñar a trabajar bien en cualquier herramienta, no solo en una.")),

    ("links", dict(
        kicker="Para profundizar",
        h2="Las fuentes, todas abiertas",
        links=[
            ("La guía completa de multi-harness RL (Hugging Face)", "https://huggingface.co/spaces/AdithyaSK/multi-harness-rl"),
            ("El modelo entrenado (LFM2.5-2.6B multi-harness)", "https://huggingface.co/FineEnvs/LFM2.5-2.6B-multiharness-RL"),
            ("Training Agents — curso de Hugging Face (TRL + OpenEnv)", "https://huggingface.co/blog/sergiopaniego/rl-environments-2026"),
        ])),
]


def main():
    html = deck(AU, AU, 14, "Material de apoyo · 6 oct 2026", TITULO, LEAD, SLIDES)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK ->", OUT, "|", len(SLIDES) + 1, "slides")


if __name__ == "__main__":
    main()
