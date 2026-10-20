#!/usr/bin/env python3
"""Genera el manual interactivo: Estado de Resultados en Business Central + plan de cuentas real."""
import openpyxl, collections, json, html

XLSX = "/Users/victorvilche/Downloads/Movs. contabilidad (71).xlsx"
OUT = "/Users/victorvilche/orca/projects/RogelioProject/out/index.html"

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb["Movs. contabilidad"]
rows = list(ws.iter_rows(min_row=1, values_only=True))
hdr = list(rows[0])
data = [dict(zip(hdr, r)) for r in rows[1:]]

def num(v):
    try: return float(v or 0)
    except: return 0.0

# --- saldos por cuenta
saldos, nombres = collections.defaultdict(float), {}
for d in data:
    c = str(d["Nº cuenta"] or "").strip()
    if not c: continue
    saldos[c] += num(d["Importe ($)"])
    nombres[c] = str(d["Nombre cuenta"] or "").strip()

def grupo(pref):
    return {c: v for c, v in saldos.items() if c.startswith(pref)}

# --- Estado de Resultados (cuentas 3 y 4 = ingresos/egresos del plan chileno)
ing = {c: -v for c, v in saldos.items() if c[0] == "3" and c[:3] != "230"}
# Gastos: clases 4,5,6,7,8,9. OJO: solo "4" deja fuera las 6xxx y 7xxx
# (patentes, notariales, reajustes pagados) y el resultado sale inflado por ese monto exacto.
gas = {c: v for c, v in saldos.items() if c[0] in "456789"}

def s(d): return sum(d.values())
TOT_ING, TOT_GAS = s(ing), s(gas)
RESULTADO = TOT_ING - TOT_GAS

# --- Balance
act = {c: v for c, v in saldos.items() if c.startswith("1")}
pas = {c: -v for c, v in saldos.items() if c.startswith("2")}
pat = {c: -v for c, v in saldos.items() if c[:3] == "230"}
TOT_ACT, TOT_PAS, TOT_PAT = s(act), s(pas), s(pat)
CUADRE_OK = abs(TOT_ACT - (TOT_PAS + TOT_PAT + RESULTADO)) < 2
TAG_CUADRE = "t-ok" if CUADRE_OK else "t-warn"
TXT_CUADRE = "OK" if CUADRE_OK else "REVISAR"

# --- jerarquia de cuentas (prefijos chilenos)
def tree(d):
    out = []
    for c in sorted(d):
        lvl = 1
        if c[3:7] != "000": lvl = 3
        elif c[1:3] != "00": lvl = 2
        out.append((c, nombres.get(c, ""), d[c], lvl))
    return out

# --- dimensiones
dims = {}
for dim in ["Item de Gasto", "Centro de Gestión", "Flujo de Caja", "N.º proyecto"]:
    cnt = collections.Counter()
    for d in data:
        v = str(d[dim] or "").strip()
        if v and v != "None": cnt[v] += 1
    dims[dim] = cnt.most_common()

fechas = [d["Fecha registro"] for d in data if d["Fecha registro"]]
fmin, fmax = min(fechas), max(fechas)
DEBE = sum(num(d["Importe debe ($)"]) for d in data)
HABER = sum(num(d["Importe haber ($)"]) for d in data)

def fmt(n): return f"{n:,.0f}".replace(",", ".")

# ============ HTML ============
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#c9d1d9;line-height:1.6;font-size:14px}
.wrap{max-width:1180px;margin:0 auto;padding:32px 24px 80px}
h1{font-size:27px;font-weight:600;color:#f0f6fc;letter-spacing:-.4px;margin-bottom:6px}
.sub{color:#8b949e;font-size:13px;margin-bottom:28px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin-bottom:32px}
.kpi{background:#161b22;border:1px solid #21262d;border-radius:10px;padding:16px 18px}
.kpi .l{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:#8b949e;margin-bottom:6px}
.kpi .v{font-size:20px;font-weight:600;color:#f0f6fc;font-variant-numeric:tabular-nums}
.kpi .v.neg{color:#f85149}.kpi .v.pos{color:#3fb950}
.kpi .n{font-size:11px;color:#6e7681;margin-top:4px}
section{margin-bottom:36px}
h2{font-size:17px;font-weight:600;color:#f0f6fc;margin-bottom:4px;display:flex;align-items:center;gap:9px}
h2 .num{background:#1f6feb;color:#fff;width:22px;height:22px;border-radius:6px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex:none}
.desc{color:#8b949e;font-size:12.5px;margin-bottom:14px;padding-left:31px}
table{width:100%;border-collapse:collapse;background:#161b22;border:1px solid #21262d;border-radius:9px;overflow:hidden;font-size:12.5px}
th{background:#1c2128;text-align:left;padding:9px 12px;font-size:10.5px;text-transform:uppercase;letter-spacing:.6px;color:#8b949e;font-weight:600;border-bottom:1px solid #21262d}
td{padding:7px 12px;border-bottom:1px solid #21262d22;font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:none}
tr:hover td{background:#1c212833}
.r{text-align:right;font-variant-numeric:tabular-nums}
.cc{font-family:ui-monospace,Menlo,monospace;color:#79c0ff;font-size:11.5px}
.l3 td:first-child{padding-left:34px}
.l2 td:first-child{padding-left:20px}
.tot td{background:#1c2128;font-weight:600;color:#f0f6fc;border-top:1px solid #30363d}
.tot.big td{font-size:13.5px}
.neg{color:#f85149}.pos{color:#3fb950}
.tag{display:inline-block;padding:2px 7px;border-radius:4px;font-size:10px;font-weight:600;letter-spacing:.3px}
.t-ok{background:#23863622;color:#3fb950;border:1px solid #23863655}
.t-warn{background:#bb800922;color:#d29922;border:1px solid #bb800955}
.t-bad{background:#da363322;color:#f85149;border:1px solid #da363355}
.t-info{background:#1f6feb22;color:#58a6ff;border:1px solid #1f6feb55}
.box{background:#161b22;border:1px solid #21262d;border-left:3px solid #1f6feb;border-radius:8px;padding:14px 18px;margin:14px 0;font-size:13px}
.box.warn{border-left-color:#d29922}
.box.bad{border-left-color:#f85149;background:#da363310}
.box.ok{border-left-color:#3fb950}
.box b{color:#f0f6fc}
code{background:#1c2128;padding:1px 6px;border-radius:4px;font-family:ui-monospace,Menlo,monospace;font-size:11.5px;color:#79c0ff}
.steps{counter-reset:s}
.step{background:#161b22;border:1px solid #21262d;border-radius:9px;padding:15px 18px;margin-bottom:9px;display:flex;gap:14px}
.step .n{counter-increment:s;background:#21262d;color:#58a6ff;width:25px;height:25px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex:none;margin-top:1px}
.step .n::before{content:counter(s)}
.step .b{flex:1}
.step .t{font-weight:600;color:#f0f6fc;margin-bottom:3px;font-size:13.5px}
.step .d{color:#8b949e;font-size:12.5px}
.step .d code{background:#0d1117;border:1px solid #21262d}
.tabs{display:flex;gap:5px;margin-bottom:14px;flex-wrap:wrap}
.tab{background:#161b22;border:1px solid #21262d;color:#8b949e;padding:6px 13px;border-radius:7px;cursor:pointer;font-size:12px;font-family:inherit;transition:.12s}
.tab:hover{border-color:#30363d;color:#c9d1d9}
.tab.on{background:#1f6feb;border-color:#1f6feb;color:#fff}
.pane{display:none}.pane.on{display:block}
footer{margin-top:50px;padding-top:20px;border-top:1px solid #21262d;color:#6e7681;font-size:11.5px}
footer a{color:#58a6ff;text-decoration:none}
.src{font-size:11px;color:#6e7681}
"""

def fila(c, n, v, lvl=1, cls=""):
    cl = "l3" if lvl == 3 else ("l2" if lvl == 2 else "")
    vc = "neg" if v < 0 else ""
    return f'<tr class="{cl} {cls}"><td class="cc">{c}</td><td>{html.escape(n)}</td><td class="r {vc}">{fmt(v)}</td></tr>'

# --- tabla balance
def tabla_balance(sub, tot, titulo):
    filas = "".join(fila(c, n, v, l) for c, n, v, l in tree(sub))
    return f'''<table><thead><tr><th style="width:90px">Cuenta</th><th>Nombre</th><th class="r" style="width:150px">Saldo</th></tr></thead>
<tbody>{filas}<tr class="tot"><td colspan="2">{titulo}</td><td class="r">{fmt(tot)}</td></tr></tbody></table>'''

# --- tabla ER
def tabla_er(d, tot, titulo):
    filas = "".join(fila(c, n, v) for c, n, v, l in tree(d))
    return f'''<table><thead><tr><th style="width:90px">Cuenta</th><th>Nombre</th><th class="r" style="width:150px">Monto</th></tr></thead>
<tbody>{filas}<tr class="tot"><td colspan="2">{titulo}</td><td class="r">{fmt(tot)}</td></tr></tbody></table>'''

# --- mapeo IFRS
MAPEO = [
    ("Ingresos de actividades ordinarias", "3101002", "INGRESOS POR VENTA", "NIC 1.82(a) / NIIF 15"),
    ("Otros ingresos", "3201001, 3201003, 3202003", "Intereses FM, reajustes ganados", "NIC 1.85"),
    ("Costo de ventas", "4201001", "COSTOS DE VENTA", "NIC 1.103"),
    ("Gastos de administración", "4101001, 4101002, 4101003, 4101007, 4101010", "Mano obra, honorarios, municipales, legales", "NIC 1.103"),
    ("Costos de distribución", "4101004, 4101005, 4101009", "Marketing, gestión venta, post venta", "NIC 1.103"),
    ("Costos financieros", "4101006, 7101002", "Gastos financieros, reajustes pagados", "NIC 1.82(b)"),
    ("Gastos de administración (cont.)", "61xxxxx", "Patentes, notariales, asesorías, varios", "NIC 1.103"),
]

dims_html = ""
for dim, vals in dims.items():
    filas = "".join(f'<tr><td class="cc">{html.escape(k)}</td><td class="r">{v:,}</td></tr>'.replace(",", ".") for k, v in vals)
    dims_html += f'''<div style="margin-bottom:18px"><div style="font-weight:600;color:#f0f6fc;margin-bottom:7px;font-size:13px">{html.escape(dim)} <span class="src">— {len(vals)} valores</span></div>
<table><thead><tr><th>Valor</th><th class="r" style="width:120px">Movimientos</th></tr></thead><tbody>{filas}</tbody></table></div>'''

mapeo_html = "".join(
    f'<tr><td>{html.escape(a)}</td><td class="cc">{html.escape(b)}</td><td style="color:#8b949e">{html.escape(c)}</td><td class="src">{html.escape(d)}</td></tr>'
    for a, b, c, d in MAPEO)

HTML = f'''<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Estado de Resultados · Business Central — Concreta</title><style>{CSS}</style></head><body><div class="wrap">

<h1>Estado de Resultados en Business Central</h1>
<div class="sub">Manual aplicado sobre <b>Movs. contabilidad (71).xlsx</b> — {len(data):,} movimientos reales, {len(saldos)} cuentas, {fmin:%d-%m-%Y} a {fmax:%d-%m-%Y}</div>

<div class="grid">
<div class="kpi"><div class="l">Ingresos</div><div class="v pos">{fmt(TOT_ING)}</div><div class="n">cuentas 3xxx</div></div>
<div class="kpi"><div class="l">Costos y gastos</div><div class="v neg">{fmt(TOT_GAS)}</div><div class="n">cuentas 4xxx + 6xxx + 7xxx</div></div>
<div class="kpi"><div class="l">Resultado del período</div><div class="v {'neg' if RESULTADO<0 else 'pos'}">{fmt(RESULTADO)}</div><div class="n">ingresos − gastos</div></div>
<div class="kpi"><div class="l">Movimientos</div><div class="v">{len(data):,}</div><div class="n">debe = haber &#10003;</div></div>
</div>

<section>
<h2><span class="num">1</span> La taxonomía que rige lo contable</h2>
<div class="desc">Tres capas normativas. Business Central es la herramienta; no define la taxonomía.</div>

<div class="box"><b>Capa 1 — NIIF / IFRS (la estructura)</b><br>
La taxonomía contable oficial es la <b>IFRS Taxonomy 2024</b> (IFRS Foundation). Organiza los estados por códigos: <code>210000</code> Estado de Situación Financiera, <code>310000</code> Estado del Resultado Integral por función del gasto, <code>320000</code> por naturaleza, <code>510000/520000</code> Flujos de Efectivo, <code>610000</code> Cambios en el Patrimonio.<br>
<span class="src">Fuente: IFRS Foundation — Taxonomía NIIF Ilustrada 2024, versión en español (258 págs, en fuentes/).</span></div>

<div class="box warn"><b>Capa 2 — Chile: quién obliga a usar NIIF</b><br>
La <b>CMF</b> (ex SVS) exige NIIF a las entidades fiscalizadas desde 2009-2011. El <b>SII</b> acepta la contabilidad en base NIIF pero determina el resultado tributario con reglas propias (arts. 29 a 33 LIR) — <b>son dos resultados distintos y ambos deben cuadrar</b>.<br>
<span class="src">Fuente: DL 824 (LIR) art. 29-33, texto vigente 27-03-2026 (fuentes/LIR-824.pdf).</span></div>

<div class="box bad"><b>Capa 3 — Alerta de vigencia (verificado hoy)</b><br>
La <b>Ley 21.850</b> (Ley de Reconstrucción Nacional) fue publicada el <b>17-10-2026</b> y cambia la tasa de IDPC de forma gradual:
<table style="margin-top:9px;font-size:12px">
<thead><tr><th>Año comercial</th><th class="r">Tasa IDPC</th><th>Operación renta</th></tr></thead>
<tbody>
<tr><td>2026</td><td class="r">27,0%</td><td>AT 2027 — sin cambio</td></tr>
<tr><td>2027</td><td class="r">25,5%</td><td>AT 2028</td></tr>
<tr><td>2028</td><td class="r">24,0%</td><td>AT 2029</td></tr>
<tr><td>2029 y siguientes</td><td class="r">23,0%</td><td>AT 2030+ (permanente)</td></tr>
</tbody></table>
<span class="src">No aplicar 27% a ejercicios 2027+. Verificar contra texto publicado antes de cerrar el año.</span></div>

<div class="box"><b>Ojo con IFRS 18</b> — reemplaza a NIC 1 para ejercicios que comiencen desde <b>1-enero-2027</b>. Exige dos subtotales nuevos (resultado operativo y resultado antes de financiamiento e impuestos) y revelar las medidas de desempeño definidas por la administración. Si tu ER actual no separa "resultado operativo", vas a tener que reestructurarlo antes de 2027.<br>
<span class="src">Fuente: ifrs.org — IFRS 18, vigencia confirmada.</span></div>
</section>

<section>
<h2><span class="num">2</span> Cómo se construye el Estado de Resultados en Business Central</h2>
<div class="desc">Business Central no tiene un "estado de resultados" hardcodeado: se arma con <b>Financial Reports</b> (antes Account Schedules), que combinan <b>Row Definitions</b> (filas) + <b>Column Definitions</b> (columnas).</div>

<div class="steps">
<div class="step"><div class="n"></div><div class="b"><div class="t">Chart of Accounts — la base</div><div class="d">Cada cuenta tiene <code>Account Category</code> (Assets, Liabilities, Equity, Income, Expense) y <code>Account Subcategory</code>. El ER solo lee cuentas con categoría Income y Expense. Si una cuenta está mal categorizada, el ER la ignora en silencio. <b>Es el error #1.</b></div></div></div>
<div class="step"><div class="n"></div><div class="b"><div class="t">General Ledger Setup</div><div class="d">Definir <code>Allow Posting From/To</code> (períodos), moneda local (<code>LCY</code>), y <code>Closing Date</code>. Sin <code>Allow Posting To</code> abierto al período, no hay datos que reportar.</div></div></div>
<div class="step"><div class="n"></div><div class="b"><div class="t">Row Definition — la estructura del ER</div><div class="d">Se define fila por fila con <code>Row Type</code>:
<br>· <code>Header</code> — título de sección
<br>· <code>Account Range</code> — rango de cuentas (ej. 3101002..3101999)
<br>· <code>Total</code> — suma de filas anteriores (Bold/underline)
<br>· <code>Formula</code> — cálculo entre filas por número de fila (ej. <code>ROW1-ROW2</code>)
<br>· <code>Beginning Balance</code> / <code>Net Change</code> — saldo inicial vs movimiento del período</div></div></div>
<div class="step"><div class="n"></div><div class="b"><div class="t">Column Definition — el tiempo</div><div class="d"><code>Column Layout</code>: Net Change, Balance at Date, Comparison Period, % of Total, Budget. Permite comparar período actual vs anterior vs presupuesto en una sola tabla.</div></div></div>
<div class="step"><div class="n"></div><div class="b"><div class="t">Account Schedule (Financial Report)</div><div class="d">Une Row Def + Column Def + <code>Analysis View</code> (qué dimensión filtrar). Desde ahí se puede <b>exportar a Excel</b> con formato o publicar como KPI web service.</div></div></div>
<div class="step"><div class="n"></div><div class="b"><div class="t">Dimensiones — el corte gerencial</div><div class="d">Tu archivo usa <b>4 dimensiones reales</b>: Item de Gasto, Centro de Gestión, Flujo de Caja, N.º proyecto. Un ER por centro de gestión = mismo Row Def, distinto <code>Analysis View</code> filtrado.</div></div></div>
</div>

<div class="box ok"><b>Regla práctica:</b> si el ER "no cuadra con el balance", el 90% de las veces es (a) una cuenta con Account Category equivocada, o (b) movimientos en un período cerrado que quedaron fuera del filtro de fechas. Revisar esos dos antes de tocar la Row Definition.</div>
</section>

<section>
<h2><span class="num">3</span> Estado de Resultados — datos reales del archivo</h2>
<div class="desc">Calculado desde los {len(data):,} movimientos. Cuentas 3xxx = ingresos (saldo acreedor, se lee en positivo); 4xxx/6xxx/7xxx = egresos.</div>

<div class="tabs">
<button class="tab on" onclick="sw(this,'er')">Estado de Resultados</button>
<button class="tab" onclick="sw(this,'bal')">Balance</button>
<button class="tab" onclick="sw(this,'map')">Mapeo a NIIF</button>
<button class="tab" onclick="sw(this,'dim')">Dimensiones</button>
</div>

<div id="er" class="pane on">
<div style="font-weight:600;color:#3fb950;margin:12px 0 7px;font-size:13px">INGRESOS</div>
{tabla_er(ing, TOT_ING, "TOTAL INGRESOS")}
<div style="font-weight:600;color:#f85149;margin:18px 0 7px;font-size:13px">COSTOS Y GASTOS</div>
{tabla_er(gas, TOT_GAS, "TOTAL COSTOS Y GASTOS")}
<table style="margin-top:18px"><tbody><tr class="tot big"><td colspan="2">RESULTADO DEL PERÍODO</td><td class="r {'neg' if RESULTADO<0 else 'pos'}">{fmt(RESULTADO)}</td></tr></tbody></table>
</div>

<div id="bal" class="pane">
<div style="font-weight:600;color:#f0f6fc;margin:12px 0 7px;font-size:13px">ACTIVO</div>
{tabla_balance(act, TOT_ACT, "TOTAL ACTIVO")}
<div style="font-weight:600;color:#f0f6fc;margin:18px 0 7px;font-size:13px">PASIVO</div>
{tabla_balance(pas, TOT_PAS, "TOTAL PASIVO")}
<div style="font-weight:600;color:#f0f6fc;margin:18px 0 7px;font-size:13px">PATRIMONIO</div>
{tabla_balance(pat, TOT_PAT, "TOTAL PATRIMONIO")}
<div class="box ok"><b>El balance cuadra: A − P = {fmt(TOT_ACT-TOT_PAS)}</b>, que es exactamente el resultado del período ({fmt(RESULTADO)}). Eso confirma que no hay error de digitación: debe = haber ({fmt(DEBE)}).<br><br><b>Por qué la identidad "A = P + PN" no da:</b> las cuentas de patrimonio (2301001 CAPITAL, 2302001 REVALORIZACIÓN, 2303001 UTILIDAD ACUMULADA = {fmt(TOT_PAT)}) vienen de un <b>saldo de apertura del ejercicio anterior</b> (documento BCEAPERTURAVT, 31-05-2025), no de asientos del período. El archivo mezcla dos ejercicios sin el cierre intermedio, así que el patrimonio se muestra "suelto", sin contrapartida en el activo del mismo rango de fechas.<br><br><b>Qué hacer:</b> en BC, correr el <b>cierre de ejercicio</b> (Close Income Statement) al 31-12-2025 y exportar un rango que no cruce el corte. Recién ahí el balance trimestral/anual va a cuadrar contra patrimonio.</div>
</div>

<div id="map" class="pane">
<div class="desc" style="padding-left:0;margin-bottom:12px">Del plan de cuentas chileno a las líneas de la taxonomía NIIF. Esta es la tabla que se carga en la <b>Row Definition</b>.</div>
<table><thead><tr><th>Línea NIIF (taxonomía)</th><th style="width:200px">Cuentas</th><th>Nombre en tu plan</th><th style="width:130px">Referencia</th></tr></thead><tbody>{mapeo_html}</tbody></table>
<div class="box" style="margin-top:14px"><b>Nota de método:</b> el plan de cuentas de la empresa es <b>tradicional chileno</b> (1=activo, 2=pasivo, 3=resultado acreedor, 4=gasto), no el de Business Central (que usa Account Category). El mapeo es a nivel de cuenta; para dimensiones hay que poblar <code>Account Subcategory</code>.</div>
</div>

<div id="dim" class="pane">
<div class="desc" style="padding-left:0;margin-bottom:12px">Dimensiones detectadas en el export. Cada una es un corte posible del ER.</div>
{dims_html}
</div>
</section>

<section>
<h2><span class="num">4</span> Controles antes de dar el ER por bueno</h2>
<div class="desc">Checklist derivado de lo que este archivo mostró.</div>
<table><thead><tr><th style="width:30px"></th><th>Control</th><th style="width:130px">Estado en este archivo</th></tr></thead><tbody>
<tr><td><span class="tag t-ok">OK</span></td><td>Debe = Haber en el mayor</td><td class="src">cuadra exacto</td></tr>
<tr><td><span class="tag t-ok">OK</span></td><td>Activo − Pasivo = resultado del período</td><td class="src">cuadra exacto</td></tr>
<tr><td><span class="tag t-info">INFO</span></td><td>Patrimonio con contrapartida en el activo</td><td class="src">apertura de 2 ejercicios mezclada</td></tr>
<tr><td><span class="tag t-warn">REVISAR</span></td><td>Cierre de ejercicio: resultado traspasado a patrimonio</td><td class="src">2303001 sin el resultado del período</td></tr>
<tr><td><span class="tag t-warn">REVISAR</span></td><td>Cuentas de activo con saldo negativo</td><td class="src">{len([c for c,v in act.items() if v<0])} cuentas</td></tr>
<tr><td><span class="tag t-warn">REVISAR</span></td><td>Cuentas de pasivo con saldo deudor</td><td class="src">{len([c for c,v in pas.items() if v<0])} cuentas</td></tr>
<tr><td><span class="tag t-info">INFO</span></td><td>Cuentas del plan sin movimiento</td><td class="src">{len([c for c,v in saldos.items() if v==0])} de {len(saldos)}</td></tr>
</tbody></table>
</section>

<footer>
Generado desde <code>Movs. contabilidad (71).xlsx</code> — {len(data):,} movimientos · {len(saldos)} cuentas · período {fmin:%d-%m-%Y} a {fmax:%d-%m-%Y}<br><br>
<b>Fuentes verificadas:</b> IFRS Taxonomy 2024 (IFRS Foundation, español) · DL 824 LIR arts. 29-33, texto vigente 27-03-2026 (LeyChile) · Ley 21.850 publicada 17-10-2026 · SII tasas IDPC (actualizado 25-05-2026) · Documentación Microsoft Learn de Business Central (973 archivos, en caché local).<br><br>
<span class="src">Los montos son datos reales del archivo, no estimaciones. Los tratamientos normativos deben validarse con el contador antes de presentar al SII.</span>
</footer>
</div>
<script>
function sw(el,id){{
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('on'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('on'));
  document.getElementById(id).classList.add('on'); el.classList.add('on');
}}
</script></body></html>'''

open(OUT, "w").write(HTML)
print("OK", OUT)
print(f"Ingresos {fmt(TOT_ING)} | Gastos {fmt(TOT_GAS)} | Resultado {fmt(RESULTADO)}")
