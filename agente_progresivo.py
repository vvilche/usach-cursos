# ═══════════════════════════════════════════════════════════════════
#  AGENTE PROGRESIVO — cómo se construye un agente de auditoría
#  Etapa por etapa. Cada etapa agrega UNA pieza sobre la anterior.
#  Corre todo de arriba a abajo en Google Colab (una celda = todo).
#
#  Antes de empezar, en OTRA celda:
#     !pip install openai
#  Y en la línea de abajo pegá tu key gratis de Groq (console.groq.com/keys)
# ═══════════════════════════════════════════════════════════════════

from openai import OpenAI

cliente = OpenAI(
    api_key="PEGA-AQUI-TU-KEY",     # <- pegá tu key entre las comillas
    base_url="https://api.groq.com/openai/v1"
)

import pandas as pd

# Datos de ejemplo: facturas (lo que se facturó) y pagos (lo que entró)
pd.DataFrame({
    "folio":  ["F-001", "F-002", "F-003", "F-004"],
    "monto":  [120000,  85000,   240000,  50000],
}).to_csv("facturas.csv", index=False)

pd.DataFrame({
    "folio":  ["F-001", "F-002", "F-003", "F-005"],   # ojo: F-004 no aparece, F-005 no existe en facturas
    "monto":  [120000,  85000,   240000,  99999],
}).to_csv("pagos.csv", index=False)

print("Archivos de ejemplo creados: facturas.csv y pagos.csv\n")


# ═══════════════════════════════════════════════════════════════════
#  ETAPA 1 — Un agente con UNA herramienta
#  Un agente = objetivo + herramienta + loop (pensar → actuar → observar)
# ═══════════════════════════════════════════════════════════════════
print("════ ETAPA 1 · Una sola herramienta ════")

def contar_filas(archivo):
    """Cuenta cuántas filas tiene un CSV."""
    return len(pd.read_csv(archivo))

objetivo = "contar cuántas filas tiene facturas.csv"

respuesta = cliente.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content":
        "Objetivo: " + objetivo +
        ". Responde SOLO con el nombre de la función a usar: contar_filas"}]
)
decision = respuesta.choices[0].message.content.strip()
print("La IA decidió usar:", decision)

if "contar_filas" in decision:
    resultado = contar_filas("facturas.csv")
    print("Resultado:", resultado, "filas\n")


# ═══════════════════════════════════════════════════════════════════
#  ETAPA 2 — Múltiples herramientas: la IA ELIGE cuál usar
#  Ahora el agente tiene 4 herramientas. El objetivo cambia, y el
#  modelo decide cuál de las 4 sirve. Eso es "agente" de verdad.
# ═══════════════════════════════════════════════════════════════════
print("════ ETAPA 2 · Cuatro herramientas, la IA elige ════")

def sumar_columna(archivo, columna):
    """Suma los valores de una columna numérica."""
    return pd.read_csv(archivo)[columna].sum()

def buscar_mayor(archivo, columna):
    """Devuelve el valor más alto de una columna."""
    return pd.read_csv(archivo)[columna].max()

def detectar_duplicados(archivo, columna):
    """Devuelve los valores que aparecen más de una vez."""
    datos = pd.read_csv(archivo)
    return list(datos[datos.duplicated(columna)][columna])

# El menú de herramientas se lo describimos a la IA en texto
menu_herramientas = (
    "Herramientas disponibles:\n"
    "- contar_filas(archivo): cuenta filas de un CSV\n"
    "- sumar_columna(archivo, columna): suma una columna\n"
    "- buscar_mayor(archivo, columna): el valor más alto\n"
    "- detectar_duplicados(archivo, columna): valores repetidos\n"
)

objetivo = "¿cuánto facturé en total?"

respuesta = cliente.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content":
        menu_herramientas +
        "\nObjetivo: " + objetivo +
        "\nResponde SOLO con: nombre_funcion(archivo, columna)"}]
)
decision = respuesta.choices[0].message.content.strip()
print("La IA decidió:", decision)

# Traducimos lo que decidió la IA a una llamada real
if "sumar_columna" in decision:
    print("Total facturado: $", sumar_columna("facturas.csv", "monto"))
elif "buscar_mayor" in decision:
    print("Factura más cara: $", buscar_mayor("facturas.csv", "monto"))
elif "detectar_duplicados" in decision:
    print("Duplicados:", detectar_duplicados("facturas.csv", "folio"))
print()


# ═══════════════════════════════════════════════════════════════════
#  ETAPA 3 — El LOOP real: repetir hasta cumplir el objetivo
#  Hasta ahora era una pasada. Un agente REPITE (pensar→actuar→observar)
#  hasta que el objetivo se cumple. Acá el loop con límite de intentos.
# ═══════════════════════════════════════════════════════════════════
print("════ ETAPA 3 · El loop real (repetir hasta cumplir) ════")

def ejecutar_agente(objetivo, max_intentos=5):
    """Loop del agente: pide a la IA qué hacer, ejecuta, observa, repite.

    Le pasamos el historial de lo ya hecho para que sepa qué le falta y
    pueda decir 'listo' cuando terminó. Así no repite pasos ni se cuelga.
    """
    historial = []   # acá guardamos lo que ya se hizo

    for intento in range(1, max_intentos + 1):
        # PENSAR (con memoria de lo ya hecho)
        hecho = "\n".join(historial) if historial else "(nada todavía)"
        respuesta = cliente.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content":
                menu_herramientas +
                "\nObjetivo: " + objetivo +
                "\nYa se hizo:\n" + hecho +
                "\nResponde SOLO con UNA acción: nombre_funcion(archivo, columna)." +
                "\nSi ya está todo resuelto, responde SOLO la palabra: listo"}]
        )
        decision = respuesta.choices[0].message.content.strip().lower()
        print(f"  Intento {intento}: la IA decidió «{decision}»")

        # ACTUAR + OBSERVAR
        if "listo" in decision:
            print("  → Objetivo cumplido.\n")
            return
        elif "sumar_columna" in decision:
            r = sumar_columna("facturas.csv", "monto")
            print("  → Total facturado:", r)
            historial.append(f"- Total facturado: {r}")
        elif "buscar_mayor" in decision:
            r = buscar_mayor("facturas.csv", "monto")
            print("  → Factura más cara:", r)
            historial.append(f"- Factura más cara: {r}")
        elif "detectar_duplicados" in decision:
            r = detectar_duplicados("facturas.csv", "folio")
            print("  → Duplicados:", r)
            historial.append(f"- Duplicados: {r}")
        elif "contar_filas" in decision:
            r = contar_filas("facturas.csv")
            print("  → Filas:", r)
            historial.append(f"- Filas: {r}")
    print("  → Se acabaron los intentos.\n")

ejecutar_agente("decime cuántas filas tiene facturas.csv y cuál es la factura más cara")


# ═══════════════════════════════════════════════════════════════════
#  ETAPA 4 — Respuesta en lenguaje natural, CON la fuente
#  En vez de devolver solo la cifra, la IA explica el resultado y
#  cita de dónde salió. Eso es el primer paso del "grounding"
#  (no inventar cifras) que veremos en la clase 3 (RAG).
# ═══════════════════════════════════════════════════════════════════
print("════ ETAPA 4 · Respuesta con fuente ════")

total = sumar_columna("facturas.csv", "monto")
filas = contar_filas("facturas.csv")

respuesta = cliente.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content":
        "Datos reales (NO los inventes): " +
        f"total facturado = ${total}, filas = {filas}, fuente = facturas.csv. " +
        "Responde en una frase para un auditor, mencionando la cifra y la fuente."}]
)
print("El agente responde:", respuesta.choices[0].message.content.strip())
print()


# ═══════════════════════════════════════════════════════════════════
#  ETAPA 5 — La conciliación: facturas vs pagos
#  El trabajo real del auditor: cruzar dos fuentes y marcar
#  discrepancias. Acá el agente compara facturas.csv contra pagos.csv.
#  Esto es el aperitivo del caza-fraudes (clase 7).
# ═══════════════════════════════════════════════════════════════════
print("════ ETAPA 5 · Conciliación facturas vs pagos ════")

facturas = pd.read_csv("facturas.csv")
pagos = pd.read_csv("pagos.csv")

# Cruzamos por folio: juntamos ambas tablas y vemos qué falta o no cuadra
cruce = facturas.merge(pagos, on="folio", how="outer", suffixes=("_factura", "_pago"))

# Una factura sin pago = monto_pago vacío
sin_pago = cruce[cruce["monto_pago"].isna()]
# Un pago sin factura = monto_factura vacío
sin_factura = cruce[cruce["monto_factura"].isna()]
# Montos distintos
no_cuadra = cruce[
    cruce["monto_factura"].notna() & cruce["monto_pago"].notna() &
    (cruce["monto_factura"] != cruce["monto_pago"])
]

print("Facturas SIN pago:")
print(sin_pago[["folio", "monto_factura"]].to_string(index=False))
print("\nPagos SIN factura (posible factura trucha):")
print(sin_factura[["folio", "monto_pago"]].to_string(index=False))
print("\nMontos que NO cuadran:")
print(no_cuadra[["folio", "monto_factura", "monto_pago"]].to_string(index=False))

# La IA lo explica para un auditor
respuesta = cliente.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content":
        f"Resultado de la conciliación (real, no inventes): " +
        f"{len(sin_pago)} factura(s) sin pago, " +
        f"{len(sin_factura)} pago(s) sin factura (folio {list(sin_factura['folio'])}), " +
        f"{len(no_cuadra)} monto(s) que no cuadran. " +
        "Escribí un párrafo corto para un auditor explicando qué encontró la auditoría."}]
)
print("\nEl agente concluye:", respuesta.choices[0].message.content.strip())

print("\n\n═══ FIN — Acabás de construir un agente de auditoría en 5 etapas ═══")
print("Etapa 1: una herramienta · Etapa 2: elige entre varias · Etapa 3: loop real")
print("Etapa 4: responde con fuente · Etapa 5: concilia facturas vs pagos")
