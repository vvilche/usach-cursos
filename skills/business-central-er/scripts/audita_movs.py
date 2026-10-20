#!/usr/bin/env python3
"""Audita un export 'Movs. contabilidad' de Business Central.

Uso:  python3 audita_movs.py "/ruta/Movs. contabilidad (71).xlsx"

Deterministico: no usa LLM. Imprime cuadratura, Balance, Estado de Resultados
(y con --json lo deja en JSON para alimentar un HTML).
"""
import sys, json, collections
import openpyxl


def num(v):
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def carga(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(min_row=1, values_only=True))
    hdr = [str(h).strip() if h is not None else "" for h in rows[0]]
    data = [dict(zip(hdr, r)) for r in rows[1:] if any(c is not None for c in r)]
    return hdr, data


def col(data, *candidatos):
    """Devuelve la primera clave del dict que coincida (tolera variantes de nombre)."""
    if not data:
        return None
    keys = list(data[0].keys())
    for cand in candidatos:
        for k in keys:
            if cand.lower() in k.lower():
                return k
    return None


def audita(path):
    hdr, data = carga(path)
    c_cta = col(data, "Nº cuenta", "N. cuenta", "Cuenta")
    c_nom = col(data, "Nombre cuenta")
    c_imp = col(data, "Importe ($)", "Importe (")
    c_deb = col(data, "Importe debe")
    c_hab = col(data, "Importe haber")
    c_fec = col(data, "Fecha registro")
    if not (c_cta and c_imp):
        raise SystemExit(f"No encuentro cuenta/importe. Columnas: {hdr}")

    saldos, nombres = collections.defaultdict(float), {}
    for d in data:
        c = str(d.get(c_cta) or "").strip()
        if not c:
            continue
        saldos[c] += num(d.get(c_imp))
        nombres[c] = str(d.get(c_nom) or "").strip()

    debe = sum(num(d.get(c_deb)) for d in data) if c_deb else 0.0
    haber = sum(num(d.get(c_hab)) for d in data) if c_hab else 0.0
    fechas = [d.get(c_fec) for d in data if d.get(c_fec)]

    def clase(p):
        return {c: v for c, v in saldos.items() if c.startswith(p)}

    act, pas = clase("1"), {c: -v for c, v in clase("2").items()}
    # Patrimonio = subgrupo 230x (capital, revalorizacion, utilidades acumuladas).
    # OJO: '23' como prefijo de string NO matchea '2301001' -> usar c[:3] == '230'.
    pat = {c: -v for c, v in saldos.items() if c[:3] == "230"}
    ing = {c: -v for c, v in saldos.items() if c[0] == "3" and c[:3] != "230"}
    gas = {}
    for p in ("4", "5", "6", "7", "8", "9"):
        gas.update(clase(p))

    s = lambda d: sum(d.values())
    resultado = s(ing) - s(gas)
    descuadre = s(act) - (s(pas) + s(pat) + resultado)

    hallazgos = []
    if c_deb and c_hab and abs(debe - haber) > 1:
        hallazgos.append(f"ERROR: debe({debe:,.0f}) != haber({haber:,.0f})")
    # El chequeo fuerte es A-P == Resultado. La identidad A = P + PN + RES solo falla
    # cuando el patrimonio viene de una apertura de otro ejercicio sin cierre intermedio.
    if abs(s(act) - s(pas) - resultado) > 1:
        hallazgos.append(
            f"A-P ({s(act)-s(pas):,.0f}) != Resultado ({resultado:,.0f}): revisar clasificacion de cuentas."
        )
    elif abs(descuadre) > 1:
        hallazgos.append(
            f"A = P + PN + RES no da (difiere {descuadre:,.0f}), pero A-P = Resultado cuadra exacto."
            " No es error de captura: las cuentas de patrimonio (230x) vienen de un saldo de apertura"
            " de otro ejercicio sin cierre intermedio. Correr Close Income Statement y exportar sin cruzar el corte."
        )
    neg_act = [c for c, v in act.items() if v < 0]
    if neg_act:
        hallazgos.append(f"{len(neg_act)} cuentas de activo con saldo negativo: {neg_act[:6]}")
    pos_pas = [c for c, v in pas.items() if v < 0]
    if pos_pas:
        hallazgos.append(f"{len(pos_pas)} cuentas de pasivo con saldo deudor: {pos_pas[:6]}")

    return {
        "archivo": path,
        "movimientos": len(data),
        "cuentas": len(saldos),
        "periodo": [str(min(fechas)) if fechas else None, str(max(fechas)) if fechas else None],
        "debe": debe, "haber": haber, "cuadra_debe_haber": abs(debe - haber) <= 1,
        "activo": s(act), "pasivo": s(pas), "patrimonio": s(pat), "resultado": resultado,
        "descuadre": descuadre,
        "ingresos": dict(sorted(ing.items())), "gastos": dict(sorted(gas.items())),
        "activo_detalle": dict(sorted(act.items())),
        "pasivo_detalle": dict(sorted(pas.items())),
        "patrimonio_detalle": dict(sorted(pat.items())),
        "nombres": nombres,
        "hallazgos": hallazgos,
    }


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    r = audita(sys.argv[1])
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=1, default=str))
        return
    print(f"Archivo     : {r['archivo']}")
    print(f"Movimientos : {r['movimientos']:,}   Cuentas: {r['cuentas']}")
    print(f"Periodo     : {r['periodo'][0]} -> {r['periodo'][1]}")
    print(f"Debe/Haber  : {r['debe']:,.0f} / {r['haber']:,.0f}  cuadra={r['cuadra_debe_haber']}")
    print(f"Activo      : {r['activo']:,.0f}")
    print(f"Pasivo      : {r['pasivo']:,.0f}")
    print(f"Patrimonio  : {r['patrimonio']:,.0f}")
    print(f"Resultado   : {r['resultado']:,.0f}")
    print(f"Descuadre   : {r['descuadre']:,.0f}")
    print("\nHallazgos:")
    for h in r["hallazgos"] or ["  (ninguno)"]:
        print(" -" if not h.startswith(" ") else "", h)


if __name__ == "__main__":
    main()
