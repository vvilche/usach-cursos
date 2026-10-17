# -*- coding: utf-8 -*-
"""Genera tarea-innovacion-clases-1-4.html

Tarea de bloque para Innovación (electivo VI), clases 1 a 4, en grupos de hasta 2 personas.
Contenido derivado SOLO de las clases 1-4 de gen_ppts.py: no se inventan criterios.
CSS y motor de quiz se toman de tarea-innovacion-clases-2-3.html (la tarea ya publicada).
El quiz se balancea con cuota exacta por posicion, no al azar, para que no sea adivinable.

Determinista, cero tokens de LLM.
"""
import json
import re

BASE = "tarea-innovacion-clases-2-3.html"
SALIDA = "tarea-innovacion-clases-1-4.html"
PLAN = "innovacion-disruptiva.html"
CATALOGO = "patrones-modelo-negocio.html"

_src = open(BASE, encoding="utf-8").read()
_m_css = re.search(r"<style>(.*?)</style>", _src, re.S)
_m_js = re.search(r"<script>(.*?)</script>\s*</body>", _src, re.S)
assert _m_css and _m_js, "no se encontro <style> o <script> en la tarea base"
CSS = _m_css.group(1)
_SCRIPT = _m_js.group(1)
# el motor = todo el script menos el bloque de preguntas original
MOTOR = re.sub(r"const QS\s*=\s*\[.*?\n\];\s*", "", _SCRIPT, flags=re.S)

QS = [
 dict(q="Tu grupo escribe: «nuestra idea es disruptiva porque el producto es mejor que el del líder, "
        "con más funciones y mejor terminación». Según la clase 1, ¿qué está mal en ese argumento?",
      opts=["Mejorar lo mismo para el mismo cliente es innovación incremental (sustaining), no "
            "disruptiva: no ataca un segmento que el líder ignora",
            "Nada: tener más funciones es exactamente lo que define una disrupción",
            "Que no menciona el precio final del producto",
            "Que la disrupción solo la pueden hacer empresas grandes"],
      ok=0,
      why="La clase 1 separa los tres tipos: sustaining mejora el producto para los MEJORES clientes "
          "actuales. Ser «mejor» para el mismo cliente es la vía por la que el líder te copia rápido. "
          "La disrupción entra por un segmento que el líder ignora, con algo más simple y barato."),
 dict(q="Identifican el «job» de su usuario y escriben: «el trabajo es sacar un crédito de consumo». "
        "¿Qué le falta para ser un job to be done bien planteado?",
      opts=["Nada, un job es la tarea concreta que el cliente quiere hacer",
            "Las tres dimensiones: la funcional (qué tarea resuelve), la emocional (cómo lo hace "
            "sentir) y la social (qué dice de él ante los demás)",
            "Poner el precio que estaría dispuesto a pagar",
            "Nombrar al competidor que hoy resuelve ese trabajo"],
      ok=1,
      why="«Sacar un crédito» es solo la dimensión funcional. Un job completo describe también qué "
          "tensión emocional resuelve y qué dice del cliente ante otros. Sin las tres, la idea se "
          "queda pegada al producto y no al trabajo que el cliente necesita hacer."),
 dict(q="Su curva de valor se ve igual a la del competidor, solo que un poco más arriba en todos los "
        "factores. Según la clase 2, ¿en qué océano están?",
      opts=["En un océano azul, porque están por encima de la competencia",
            "En un océano azul, porque la curva es distinta a la del líder",
            "En un océano rojo: una curva desplazada sigue compitiendo por los mismos factores",
            "No se puede saber sin tener el Canvas completo"],
      ok=2,
      why="La clase 2 es explícita: si la curva es una copia desplazada de la competencia, sigues en "
          "océano rojo. Innovar es CAMBIAR LA FORMA de la curva con EREC, no subirla entera."),
 dict(q="Aplican EREC y escriben: «eliminamos la atención en tienda física y creamos una app de "
        "autoservicio». ¿Qué movimiento del método están usando al crear la app?",
      opts=["Reducir, porque la app reemplaza al vendedor de la tienda",
            "Elevar, porque la app es más moderna que la tienda",
            "Crear: un factor que la industria nunca ofreció, distinto de eliminar o reducir uno "
            "que ya existía",
            "Ninguno: una app es un canal, no un factor de la curva"],
      ok=2,
      why="EREC son cuatro movimientos distintos. Quitar la atención en tienda es ELIMINAR; la app "
          "que no existía en la industria es CREAR. Los dos movimientos conviven en una misma idea: "
          "por eso hay que nombrar cuál es cuál."),
 dict(q="En el Canvas escriben primero canales, recursos clave y costos, y al final intentan definir "
        "el segmento. Según la clase 3, ¿cuál es el problema?",
      opts=["Ninguno: el Canvas no tiene un orden obligatorio y las 9 cajas valen igual",
            "El orden invertido hace que el resto de las cajas quede vacío de sentido: se empieza "
            "SIEMPRE por segmento y propuesta de valor",
            "Que los costos deben ir en la columna de los ingresos",
            "Que faltó incluir la fórmula de utilidad de Johnson dentro del Canvas"],
      ok=1,
      why="La clase 3 lo señala como error típico: las 9 cajas se llenan solas y quedan sin sustento. "
          "Segmento y propuesta de valor primero; canales, recursos y costos se DERIVAN de ahí."),
 dict(q="Su modelo cobra por hora de asesoría. Para generar un modelo alternativo aplican el patrón "
        "«Suscripción» y pasan a una cuota mensual fija. ¿Es cambio de lógica o es cosmético?",
      opts=["Cosmético: el servicio que entregan es exactamente el mismo",
            "Cambio de lógica: cambia cómo se captura el valor —de ingreso transaccional a recurrente",
            "Es cosmético, porque el patrón Suscripción ya lo usa todo el mundo",
            "No se puede determinar sin conocer el precio de la hora"],
      ok=1,
      why="La clase 4 define lo cosmético como cambiar color o precio sin tocar la lógica. Acá cambia "
          "la forma de capturar el valor: transaccional (pago por uso) pasa a recurrente (pago "
          "periódico). Que otros usen el patrón no lo vuelve cosmético."),
 dict(q="Para la clase 4 eligen tres patrones: Freemium, Suscripción y Cola larga. Al presentarlos, "
        "los tres terminan siendo «lo básico gratis y el resto pagado». ¿Qué falló?",
      opts=["Nada: son tres patrones del catálogo, así que son tres modelos válidos",
            "Eligieron mal: Cola larga no existe en el Business Model Navigator",
            "Aplicaron los tres con la misma lógica de Freemium: hay que poder decir qué patrón generó "
            "cada modelo y que la lógica de captura de valor sea distinta",
            "Faltó agregar los 10 tipos de innovación de Doblin"],
      ok=2,
      why="El testeo de la clase 4 pide dos cosas: que los modelos sean genuinamente distintos y poder "
          "decir qué patrón los generó. Si los tres desembocan en la misma captura de valor, es una "
          "variación cosmética repetida tres veces."),
 dict(q="El grupo concluye: «como el líder nos va a copiar igual, no tiene sentido apuntar a un "
        "segmento pequeño». Según la clase 1, ¿qué está olvidando?",
      opts=["Que el líder ignora ese segmento por una razón racional —márgenes malos y sus clientes "
            "actuales no quieren el producto simple— y ahí es justamente donde crece el disruptor",
            "Que el líder nunca copia a nadie porque es una empresa grande",
            "Que el segmento pequeño deja de serlo apenas el producto se abarata",
            "Que la copia solo importa en mercados regulados"],
      ok=0,
      why="El dilema del innovador: el líder ve el segmento bajo, calcula márgenes malos y decide "
          "racionalmente no entrar. Ese cálculo correcto para hoy es lo que le deja el espacio al "
          "disruptor. El grupo está usando la lógica del líder para descartar su propia oportunidad."),
]


def balancear(qs):
    """Cuota exacta N/K por posición: mueve la correcta a la posición objetivo, sin perder opciones."""
    n, k = len(qs), 4
    objetivo = [i for i in range(k) for _ in range(n // k)]
    while len(objetivo) < n:
        objetivo.append(len(objetivo) % k)
    out = []
    for q, pos in zip(qs, objetivo):
        opts = list(q["opts"])
        correcta = opts.pop(q["ok"])
        opts.insert(pos, correcta)
        out.append(dict(q=q["q"], opts=opts, ok=pos, why=q["why"]))
    return out


QS_BAL = balancear(QS)


def main():
    dist = [sum(1 for q in QS_BAL if q["ok"] == p) for p in range(4)]
    assert dist == [2, 2, 2, 2], f"distribucion no planchada: {dist}"
    assert len({len(q["opts"]) for q in QS_BAL}) == 1 and len(QS_BAL[0]["opts"]) == 4

    html = open("templates_tarea_1_4.txt", encoding="utf-8").read()
    html = (html.replace("@@CSS@@", CSS)
                .replace("@@QS@@", "const QS = " + json.dumps(QS_BAL, ensure_ascii=False, indent=2) + ";\n")
                .replace("@@MOTOR@@", MOTOR)
                .replace("@@PLAN@@", PLAN)
                .replace("@@CATALOGO@@", CATALOGO))
    assert "@@" not in html, "quedaron marcadores sin reemplazar"
    open(SALIDA, "w", encoding="utf-8").write(html)
    print(f"OK -> {SALIDA} ({len(html)} bytes) | {len(QS_BAL)} preguntas | distribucion {dist}")


if __name__ == "__main__":
    main()
