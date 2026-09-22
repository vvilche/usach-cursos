# Estoy dictando un curso donde alumnos de Contabilidad construyen sus propios agentes de IA

Este semestre arranqué un electivo en la FAE USACH que no enseña a "usar ChatGPT". Enseña a construir lo que hay detrás.

**"Hackeando la Auditoría con IA Agéntica"** — 13 clases, una vez por semana, para alumnos de Contabilidad y Auditoría que llegan sin saber programar. Al terminar, cada uno habrá construido su propio agente de auditoría, desde cero.

---

¿Por qué un curso así?

Porque la auditoría está cambiando a una velocidad que la formación no está siguiendo. Las Big 4 ya invirtieron más de US$6.000 millones en IA para auditar, y la NCG 519 volvió obligatorio auditar ESG con trazabilidad sobre el 100% de los datos, no sobre un muestreo. El auditor que solo sabe Excel está quedando fuera de ese juego.

Lo que el curso NO es: un taller de prompts ni un demo de herramienta.

Lo que SÍ es: los alumnos construyen, clase a clase, un sistema real —

- Un agente que lee balances y EE.FF. y responde citando la fuente (sin alucinar).
- Un ingestor que baja datos del SII automáticamente, sin LLM.
- Un caza-fraudes que cruza lo declarado contra lo registrado (SII vs ERP), con la Ley 21.595 como marco.
- Blindaje con spec-first y guardrails para que el agente no invente cifras.

Y lo cierran con un executive pitch: le venden su agente a un "directorio" como si fuera un cliente.

---

Tres decisiones de diseño que creo que marcan la diferencia:

1. **Sin frameworks pesados.** Python puro + API gratuita (Groq). Nada de instalar 40 dependencias. El alumno entiende el loop pensar→actuar→observar porque lo escribe con sus manos, no porque un framework se lo esconda.

2. **Desde cero, de verdad.** Asumo que nunca programaron y que muchos no tienen Mac ni computador potente. Todo corre en Google Colab, en el navegador, gratis. La primera tarea es un agente de 15 líneas que cuenta filas de un CSV — y cada clase le agrega una pieza.

3. **Cero alucinación como hábito, no como tema avanzado.** Desde la clase 1 el agente responde con la fuente citada. Para un auditor, una cifra inventada es peor que no tener cifra.

---

La tesis de fondo: la normativa es la puerta de entrada, pero lo que se vende es la capa de datos de toda la empresa, lista para que cada área actúe en tiempo real. Un auditor que construye agentes no solo "audita mejor": se convierte en el que habilita eso.

El plan de clases, las presentaciones y el código están públicos:

👉 https://vvilche.github.io/usach-cursos/

#IA #Auditoría #Contabilidad #AgentesDeIA #Educación #USACH #RAG #Fintech
