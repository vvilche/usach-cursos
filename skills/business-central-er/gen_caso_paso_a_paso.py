#!/usr/bin/env python3
"""Genera el material de clase: CÓMO SE HIZO este ejercicio, paso a paso.

No es un manual de Business Central: es el registro del proceso real —qué preguntamos,
qué medimos, en qué nos equivocamos y cómo lo detectamos— para que el alumno lo repita.

Uso:  python3 gen_caso_paso_a_paso.py "/ruta/Movs. contabilidad.xlsx"
Salida: caso-estado-resultados.html
"""
import sys, json, subprocess, os

AUDITOR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts", "audita_movs.py")

ETAPAS = [
    {
        "n": 1,
        "titulo": "Qué nos pidieron (y qué respondimos)",
        "pregunta": "«Busca todo lo que te permita convertirte en experto en Estado de Resultados, tengo Business Central»",
        "que_hice": "Antes de buscar en la web, revisamos qué había en el disco. Un proyecto vacío y una carpeta contable sin contenido: no había nada previo.",
        "aprendizaje": "El primer reflejo no es buscar: es ver qué ya existe. Nos ahorró construir sobre arena.",
        "error": None,
    },
    {
        "n": 2,
        "titulo": "La pregunta que cambió el ejercicio",
        "pregunta": "«Mientras buscas material de cómo se construyen los balances»",
        "que_hice": "Se amplió de Estado de Resultados a Balance. Son dos estados distintos y el segundo obliga a entender el cierre de ejercicio.",
        "aprendizaje": "Un pedido de una línea puede redefinir el alcance. Repetir el objetivo en voz alta antes de seguir evitó horas perdidas.",
        "error": None,
    },
    {
        "n": 3,
        "titulo": "La taxonomía: ¿qué norma rige esto?",
        "pregunta": "«Puede ser el SII o alguna normativa IFRS»",
        "que_hice": "Se identificaron TRES capas que conviven y colisionan: NIIF (estructura del estado, IFRS Foundation), tributaria (SII, arts. 29-33 LIR) y regulatoria (CMF).",
        "aprendizaje": "Un contador puede tener utilidad NIIF y pérdida tributaria el mismo año. Son dos resultados y ambos deben reconciliarse. Colapsarlos en una sola cifra es el error de base.",
        "error": None,
    },
    {
        "n": 4,
        "titulo": "Verificar vigencia — no citar de memoria",
        "pregunta": "«Checa que sean las normas vigentes, po weón»",
        "que_hice": "Se consultó IFRS Foundation (IFRS 18 reemplaza a NIC 1 desde el 1-ene-2027) y el SII. Apareció la Ley 21.850, publicada el 17-oct-2026 — tres días antes de la clase: el IDPC baja a 25,5% en 2027, 24% en 2028 y 23% desde 2029.",
        "aprendizaje": "La norma cambió mientras preparábamos la clase. Citar «27%» de memoria habría sido un error de $ millones en cualquier proyección.",
        "error": None,
    },
    {
        "n": 5,
        "titulo": "El dato real: la sábana de movimientos",
        "pregunta": "«Con esta sábana de datos se debe trabajar»",
        "que_hice": "4.550 movimientos, 98 cuentas, export `Movs. contabilidad` de Business Central. Se inspeccionaron las 23 columnas antes de calcular nada.",
        "aprendizaje": "`Importe ($)` ya viene con signo (debe positivo / haber negativo): es la columna que se suma para saldos. Usar `debe` o `haber` por separado obliga a reconstruir el signo y ahí se cuelan los errores.",
        "error": None,
    },
    {
        "n": 6,
        "titulo": "El error que casi se publica",
        "pregunta": "— (este paso no lo pidieron: lo encontramos al verificar)",
        "que_hice": "El primer cálculo sumó solo las cuentas `4xxx` como gasto y dio resultado $132.877.213. Al cruzar con el balance apareció un «descuadre» de $130.079.797 — que era EXACTAMENTE el total de las clases `6xxx` y `7xxx` omitidas.",
        "aprendizaje": "El plan de cuentas chileno usa clases 4, 5, 6 y 7 para gastos. Sumar solo `4` infla el resultado en el monto exacto de las otras clases. Resultado real: $2.797.416.",
        "error": True,
    },
    {
        "n": 7,
        "titulo": "Cómo se detectó: el segundo camino",
        "pregunta": "— (control interno)",
        "que_hice": "Se calculó el total de gastos por dos métodos independientes: (a) suma de clases 4-9, (b) negativos de clase 3. Si no coinciden, hay un error. Coincidieron recién al corregir.",
        "aprendizaje": "Nunca dar por bueno un número que sale por un solo camino. Dos métodos que deben coincidir convierten un error silencioso en un error visible.",
        "error": None,
    },
    {
        "n": 8,
        "titulo": "La segunda trampa: el prefijo",
        "pregunta": "— (control interno)",
        "que_hice": "El patrimonio salía $0 porque se filtró con `startswith(\"23\")`, que en Python NO matchea `2301001`. Corregido a `c[:3] == \"230\"`.",
        "aprendizaje": "El patrimonio es el subgrupo `230x` (capital, revalorización, utilidades acumuladas). Una comparación de prefijo mal puesta devuelve cero en silencio, sin lanzar error.",
        "error": True,
    },
    {
        "n": 9,
        "titulo": "El chequeo fuerte no es el que uno cree",
        "pregunta": "— (control interno)",
        "que_hice": "`Activo = Pasivo + Patrimonio + Resultado` NO daba: faltaban $400.568.938. Pero `Activo − Pasivo = Resultado` cuadraba exacto.",
        "aprendizaje": "El patrimonio venía de una apertura del ejercicio anterior (documento BCEAPERTURAVT, 31-05-2025) sin cierre intermedio: el archivo mezcla dos ejercicios. No es un error de captura y no hay que «arreglarlo»: hay que correr el cierre y exportar sin cruzar el corte.",
        "error": None,
    },
    {
        "n": 10,
        "titulo": "Entregar a otro: convertirlo en skill",
        "pregunta": "«Pásales a los alumnos cómo hicimos este ejercicio»",
        "que_hice": "El proceso se congeló en dos skills: `business-central-er` (la mecánica y los controles, con el script que audita automáticamente) y `contabilidad-chile-niif` (la norma y su vigencia). Un skill es un procedimiento que otro puede ejecutar sin vos.",
        "aprendizaje": "Un informe se lee una vez. Una skill se ejecuta para siempre. Lo que se repite, se escribe como procedimiento; lo que pasó una vez, se documenta como caso.",
        "error": None,
    },
]


def leer_metricas(path):
    out = subprocess.run([sys.executable, AUDITOR, path, "--json"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(out.stderr)
    return json.loads(out.stdout)


CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#c9d1d9;line-height:1.65;font-size:14px}
.wrap{max-width:960px;margin:0 auto;padding:34px 24px 90px}
h1{font-size:26px;font-weight:600;color:#f0f6fc;letter-spacing:-.4px;margin-bottom:6px}
.sub{color:#8b949e;font-size:13px;margin-bottom:26px}
.anon{background:#bb800915;border:1px solid #bb800955;border-radius:8px;padding:10px 14px;margin-bottom:26px;font-size:12.5px;color:#d29922}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:32px}
.kpi{background:#161b22;border:1px solid #21262d;border-radius:9px;padding:13px 15px}
.kpi .l{font-size:10.5px;text-transform:uppercase;letter-spacing:.7px;color:#8b949e;margin-bottom:5px}
.kpi .v{font-size:17px;font-weight:600;color:#f0f6fc;font-variant-numeric:tabular-nums}
.kpi .v.pos{color:#3fb950}.kpi .v.neg{color:#f85149}
.etapa{background:#161b22;border:1px solid #21262d;border-radius:11px;margin-bottom:13px;overflow:hidden}
.etapa.err{border-left:3px solid #f85149}
.etapa.norm{border-left:3px solid #1f6feb}
.hd{display:flex;gap:13px;padding:15px 18px;cursor:pointer;align-items:flex-start;user-select:none}
.hd:hover{background:#1c212833}
.num{background:#21262d;color:#58a6ff;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex:none;margin-top:1px}
.etapa.err .num{background:#da363333;color:#f85149}
.tt{font-weight:600;color:#f0f6fc;font-size:14px}
.preg{color:#8b949e;font-style:italic;font-size:12.5px;margin-top:3px}
.bd{padding:0 18px 16px 57px;display:none}
.etapa.open .bd{display:block}
.lbl{font-size:10.5px;text-transform:uppercase;letter-spacing:.7px;color:#6e7681;margin:12px 0 4px;font-weight:600}
.lbl.ap{color:#3fb950}
.txt{font-size:13.2px;color:#c9d1d9}
.txt code{background:#0d1117;border:1px solid #21262d;padding:1px 6px;border-radius:4px;font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:#79c0ff}
.ap{background:#23863612;border:1px solid #23863640;border-radius:7px;padding:10px 13px;font-size:13px;color:#b7e4c7;margin-top:6px}
.ap b{color:#56d364}
footer{margin-top:44px;padding-top:18px;border-top:1px solid #21262d;color:#6e7681;font-size:11.5px}
table{width:100%;border-collapse:collapse;background:#161b22;border:1px solid #21262d;border-radius:9px;overflow:hidden;font-size:12.5px;margin-top:10px}
th{background:#1c2128;text-align:left;padding:8px 12px;font-size:10.5px;text-transform:uppercase;letter-spacing:.6px;color:#8b949e;border-bottom:1px solid #21262d}
td{padding:7px 12px;border-bottom:1px solid #21262d22}
td.r{text-align:right;font-variant-numeric:tabular-nums}
.cc{font-family:ui-monospace,Menlo,monospace;color:#79c0ff;font-size:11.5px}
.tot td{background:#1c2128;font-weight:600;color:#f0f6fc;border-top:1px solid #30363d}
"""


def fmt(n):
    return f"{n:,.0f}".replace(",", ".")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    m = leer_metricas(path) if path else None

    if m:
        kpis = f"""<div class="grid">
<div class="kpi"><div class="l">Movimientos</div><div class="v">{m['movimientos']:,}</div></div>
<div class="kpi"><div class="l">Cuentas</div><div class="v">{m['cuentas']}</div></div>
<div class="kpi"><div class="l">Ingresos</div><div class="v pos">{fmt(sum(m['ingresos'].values()))}</div></div>
<div class="kpi"><div class="l">Gastos</div><div class="v neg">{fmt(sum(m['gastos'].values()))}</div></div>
<div class="kpi"><div class="l">Resultado</div><div class="v {'neg' if m['resultado']<0 else 'pos'}">{fmt(m['resultado'])}</div></div>
</div>"""
        # tabla de gastos por clase: la evidencia del paso 6
        clases = {}
        for c, v in m["gastos"].items():
            clases.setdefault(c[0], 0.0)
            clases[c[0]] += v
        filas = "".join(
            f'<tr><td class="cc">{k}xxx</td><td class="r">{fmt(v)}</td></tr>'
            for k, v in sorted(clases.items()))
        filas += f'<tr class="tot"><td>Total gastos</td><td class="r">{fmt(sum(clases.values()))}</td></tr>'
        tabla = f"""<table><thead><tr><th>Clase de cuenta</th><th class="r" style="width:170px">Monto</th></tr></thead>
<tbody>{filas}</tbody></table>
<div class="lbl">El chequeo que falla si te falta una clase</div>"""
    else:
        kpis, tabla = "", ""

    partes = []
    for e in ETAPAS:
        cls = "etapa" + (" err" if e.get("error") else "")
        cuerpo = f'<div class="lbl">Qué hicimos</div><div class="txt">{e["que_hice"]}</div>'
        if e["n"] == 6 and tabla:
            cuerpo += f'<div class="lbl">Evidencia — gasto por clase de cuenta</div>{tabla}'
        cuerpo += f'<div class="lbl ap">Aprendizaje</div><div class="ap"><b>→</b> {e["aprendizaje"]}</div>'
        partes.append(f'''<div class="{cls}">
<div class="hd" onclick="this.parentElement.classList.toggle('open')">
<div class="num">{e["n"]}</div>
<div><div class="tt">{e["titulo"]}</div><div class="preg">{e["pregunta"]}</div></div>
</div>
<div class="bd">{cuerpo}</div></div>''')

    html = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cómo se construyó el Estado de Resultados — paso a paso</title>
<style>{CSS}</style></head><body><div class="wrap">

<h1>Cómo se construyó este Estado de Resultados</h1>
<div class="sub">El registro del proceso real: qué se preguntó, qué se midió, en qué nos equivocamos y cómo se detectó.</div>

<div class="anon"><b>Datos anonimizados.</b> Las cifras provienen de un export real de Business Central, pero los nombres de empresas, bancos y contrapartes fueron reemplazados. Las cifras se mantienen porque el ejercicio es sobre la mecánica contable.</div>

{kpis}

<div class="lbl">El proceso, en orden</div>
{''.join(partes)}

<footer>
Material del electivo de Auditoría con IA Agéntica — FAE USACH.<br><br>
El procedimiento completo está en las skills <code>business-central-er</code> y <code>contabilidad-chile-niif</code> del repositorio:
son el mismo proceso, escritos para que un agente los ejecute sin vos.<br><br>
Para reproducirlo: <code>python3 skills/business-central-er/scripts/audita_movs.py "Movs. contabilidad.xlsx"</code>
</footer>
</div>
<script>
document.querySelectorAll('.etapa')[0].classList.add('open');
</script>
</body></html>'''

    with open("caso-estado-resultados.html", "w") as f:
        f.write(html)
    print("OK caso-estado-resultados.html")


if __name__ == "__main__":
    main()
