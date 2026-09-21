#!/usr/bin/env python3
"""Ingestor Store B — normativa tributaria Chile (leyes de impuesto + SII).

Fase 0: bajar + extraer + deduplicar. Salida JSONL con chunks (parent-child:
cada chunk lleva su norma + url + fecha de la fuente). Pensado para correr en
el VPS con `nice -n 15`, y en la Mac para pruebas.

Fuentes implementadas:
  - LeyChile API XML  (obtxml?opt=7&idNorma=N)  -> leyes completas, texto limpio
  - SII circulares    (indcir<anio>.htm)         -> índice de circulares del año
"""
import re, sys, json, hashlib, html, argparse
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (compatible; conta-rag/0.1; +https://hermes-agent.nousresearch.com)"}

LEYES = [
    ("6374",    "Código Tributario (DL 830/1974)",              "codigo-tributario"),
    ("6368",    "Ley de Impuesto a la Renta (DL 824/1974)",     "ley-renta"),
    ("6369",    "Ley de IVA (DL 825/1974)",                     "ley-iva"),
    ("1207746", "Ley 21.713 Cumplimiento Tributario (2024)",    "ley-21713"),
]


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    return re.sub(r"\s+", " ", s).lower().strip()


def fetch_ley(idnorma, nombre, slug):
    xml = get(f"https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma={idnorma}")
    m = re.search(r"<TituloNorma[^>]*>(.*?)</TituloNorma>", xml, re.DOTALL)
    titulo = clean(m.group(1)) if m else nombre
    mf = re.search(r'fechaVersion="([^"]+)"', xml)
    version = mf.group(1) if mf else ""
    textos = re.findall(r"<Texto[^>]*>(.*?)</Texto>", xml, re.DOTALL)
    chunks = []
    for i, t in enumerate(textos):
        txt = clean(t)
        if len(txt) < 15:
            continue
        h = hashlib.md5(norm(txt).encode()).hexdigest()
        chunks.append({
            "id": h, "fuente": "leychile", "norma": slug, "norma_nombre": titulo,
            "idnorma": idnorma, "version": version, "chunk_i": i,
            "url": f"https://www.bcn.cl/leychile/navegar?idNorma={idnorma}", "texto": txt,
        })
    return chunks


def fetch_circulares(anio):
    url = f"https://www.sii.cl/normativa_legislacion/circulares/{anio}/indcir{anio}.htm"
    page = get(url)
    base = "https://www.sii.cl/normativa_legislacion/circulares/%s/" % anio
    items = []
    for href, num, fecha in re.findall(
            r"<a[^>]+href=['\"]([^'\"]+)['\"][^>]*>\s*Circular\s+N(?:&deg;|[°º])\s*(\d+)\s+del\s+([^<]+)</a>",
            page, re.IGNORECASE):
        link = href if href.startswith("http") else base + href.lstrip("./")
        items.append({"numero": num, "fecha": clean(fecha), "url": link})
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fuente", choices=["leyes", "circulares", "all"], default="all")
    ap.add_argument("--out", default="store_b.jsonl")
    ap.add_argument("--anios", default="2024,2025,2026")
    args = ap.parse_args()

    seen = set()
    out = []

    if args.fuente in ("leyes", "all"):
        for idn, nombre, slug in LEYES:
            try:
                ch = fetch_ley(idn, nombre, slug)
            except Exception as e:
                print(f"[leyes] ERROR {slug}: {e}", file=sys.stderr)
                continue
            nuevos = [c for c in ch if c["id"] not in seen]
            seen.update(c["id"] for c in nuevos)
            out += nuevos
            total_txt = sum(len(c["texto"]) for c in ch)
            print(f"[leyes] {slug}: {len(ch)} chunks ({len(nuevos)} únicos), "
                  f"{total_txt:,} chars, v.{ch[0]['version'] if ch else '?'}")

    if args.fuente in ("circulares", "all"):
        for anio in args.anios.split(","):
            anio = anio.strip()
            try:
                items = fetch_circulares(anio)
            except Exception as e:
                print(f"[circ] ERROR {anio}: {e}", file=sys.stderr)
                continue
            print(f"[circ] {anio}: {len(items)} circulares en índice")
            for it in items:
                out.append({
                    "id": hashlib.md5(norm(f"circular {anio} {it['numero']}").encode()).hexdigest(),
                    "fuente": "sii-circulares", "norma": f"circular-{anio}-{it['numero']}",
                    "norma_nombre": f"Circular N° {it['numero']} ({it['fecha']})",
                    "anio": anio, "url": it["url"], "texto": "",
                })

    with open(args.out, "w", encoding="utf-8") as f:
        for c in out:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"\n[total] {len(out)} registros -> {args.out}")


if __name__ == "__main__":
    main()
