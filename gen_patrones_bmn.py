# -*- coding: utf-8 -*-
"""Genera patrones-modelo-negocio.html: catálogo ES de los 60 Business Model Patterns.

Fuente de los datos: businessmodelnavigator.com/explore (extraído 2026-10-17).
Texto en español en _patrones_bmn_es.py. Determinista, cero tokens de LLM.

NO toca gen_ppts.py (ese regenera los 28 decks del curso).
"""
import html as _html
from _patrones_bmn_es import PATRONES

SALIDA = "patrones-modelo-negocio.html"
PLAN = "innovacion-disruptiva.html"

CSS = """
:root{--bg:#f8fafc;--ink:#0f172a;--muted:#5b6878;--line:#dbe3ec;--card:#fff;
      --acc:#0a7a3d;--acc-soft:#e7f4ec;--acc2:#7c3aed;--acc2-soft:#f2ecfd}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
     font-family:"Inter","Helvetica Neue",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
     font-size:16px;line-height:1.62;-webkit-font-smoothing:antialiased}
header{background:#0f172a;color:#fff;padding:22px 32px;display:flex;align-items:center;
       justify-content:space-between;gap:16px;flex-wrap:wrap}
header h1{margin:0;font-size:1.16rem;font-weight:650;letter-spacing:.01em}
header .back{color:#a7f3c9;text-decoration:none;font-size:.87rem;border:1px solid rgba(167,243,201,.35);
             padding:7px 13px;border-radius:7px;white-space:nowrap}
header .back:hover{background:rgba(167,243,201,.12)}
main{max-width:1120px;margin:0 auto;padding:34px 26px 70px}
.lead{font-size:1.02rem;color:#334155;max-width:76ch;margin:0 0 10px}
.note{background:var(--acc-soft);border-left:3px solid var(--acc);border-radius:0 7px 7px 0;
      padding:13px 17px;font-size:.9rem;color:#14532d;margin:20px 0 26px;max-width:88ch}
.note b{color:#0a5f30}
.bar{display:flex;gap:12px;align-items:center;flex-wrap:wrap;position:sticky;top:0;z-index:20;
     background:var(--bg);padding:12px 0 14px;border-bottom:1px solid var(--line);margin-bottom:22px}
#q{flex:1;min-width:230px;padding:11px 15px;font-size:.95rem;border:1px solid #c7d2de;
   border-radius:9px;background:#fff;font-family:inherit;color:var(--ink)}
#q:focus{outline:none;border-color:var(--acc);box-shadow:0 0 0 3px rgba(10,122,61,.12)}
#cuenta{font-size:.83rem;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:15px}
.card{background:var(--card);border:1px solid var(--line);border-radius:11px;padding:17px 19px 16px;
      display:flex;flex-direction:column;transition:box-shadow .15s,border-color .15s}
.card:hover{border-color:#b9cadb;box-shadow:0 3px 14px rgba(15,23,42,.07)}
.card .top{display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;margin-bottom:3px}
.card .num{font-size:.72rem;color:#94a3b8;font-variant-numeric:tabular-nums;font-weight:600;
           min-width:20px}
.card h2{margin:0;font-size:1.02rem;font-weight:660;letter-spacing:-.005em;line-height:1.32}
.card .en{font-size:.75rem;color:var(--acc2);background:var(--acc2-soft);border-radius:5px;
          padding:2px 7px;font-weight:600;white-space:nowrap}
.card p{margin:8px 0 12px;font-size:.895rem;color:#3d4a5c;line-height:1.58;flex:1}
.card .src{font-size:.765rem;color:var(--muted);text-decoration:none;border-top:1px solid #eef2f7;
           padding-top:9px}
.card .src:hover{color:var(--acc)}
.vacio{padding:40px 0;text-align:center;color:var(--muted);font-size:.92rem;display:none}
footer{max-width:1120px;margin:0 auto;padding:0 26px 60px;font-size:.82rem;color:var(--muted);
       border-top:1px solid var(--line);padding-top:20px}
footer a{color:var(--acc)}
@media(max-width:560px){main{padding:22px 15px 50px}.grid{grid-template-columns:1fr}
  header{padding:16px 18px}}
"""

JS = """
(function(){
  var q=document.getElementById('q'), cards=[].slice.call(document.querySelectorAll('.card')),
      cta=document.getElementById('cuenta'), vacio=document.getElementById('vacio');
  function normalize(s){return (s||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');}
  cards.forEach(function(c){c.dataset.buscar=normalize(c.dataset.nombre+' '+c.dataset.en+' '+c.textContent);});
  function filtrar(){
    var t=normalize(q.value.trim()), n=0;
    cards.forEach(function(c){
      var ok = !t || c.dataset.buscar.indexOf(t)>-1;
      c.style.display = ok ? '' : 'none';
      if(ok) n++;
    });
    cta.textContent = n+' de '+cards.length+' patrones';
    vacio.style.display = n ? 'none' : 'block';
  }
  q.addEventListener('input',filtrar);
  filtrar();
})();
"""


def esc(s):
    return _html.escape(s, quote=True)


def tarjeta(p):
    pid, es, en, texto = p
    num = "%%NUM%%" if pid == 1 else ""
    return (
        f'<article class="card" data-nombre="{esc(es)}" data-en="{esc(en)}">\n'
        f'  <div class="top"><span class="num">{pid}</span><h2>{esc(es)}</h2>'
        f'<span class="en">{esc(en)}</span></div>\n'
        f'  <p>{esc(texto)}</p>\n'
        f'  <a class="src" href="https://www.businessmodelnavigator.com/pattern?id={pid}" '
        f'target="_blank" rel="noopener">Ficha original en inglés →</a>\n'
        f'</article>'
    )


def main():
    assert len(PATRONES) == 60, f"se esperaban 60 patrones, hay {len(PATRONES)}"
    ids = [p[0] for p in PATRONES]
    assert ids == list(range(1, 61)), f"ids no consecutivos 1..60: {ids}"

    tarjetas = "\n".join(tarjeta(p) for p in PATRONES)
    html = (
        '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>60 patrones de modelo de negocio · en español</title>\n'
        '<meta name="description" content="Catálogo en español de los patrones de modelo de '
        'negocio del Business Model Navigator (Universidad de St. Gallen).">\n'
        f'<style>@@CSS@@</style>\n</head>\n<body>\n'
        '<header>\n'
        '  <h1>60 patrones de modelo de negocio</h1>\n'
        f'  <a class="back" href="{PLAN}">← Plan de clases</a>\n'
        '</header>\n<main>\n'
        '<p class="lead">Los <b>patrones de modelo de negocio</b> son recetas probadas: la forma en '
        'que una empresa crea, entrega y captura valor. Más del 90% de los modelos de negocio '
        'nuevos son recombinaciones de patrones que ya existen — no inventos desde cero. Esta es '
        'la lista del <b>Business Model Navigator</b> (Universidad de St. Gallen), traducida al '
        'español.</p>\n'
        '<div class="note">\n'
        '  <b>Nota sobre el conteo:</b> el libro y el sitio hablan de <b>55 patrones</b>. Al '
        'revisar la lista publicada el <b>17 de octubre de 2026</b> aparecen <b>60</b>: el sitio '
        'agregó después los cinco últimos (Sensor como servicio, Virtualización, Objeto con '
        'autoservicio, Objeto como punto de venta y Prosumidor). Están los 60 aquí, y las 55 '
        'fichas del libro original quedan identificadas por su número.\n'
        '</div>\n'
        '<div class="bar">\n'
        '  <input id="q" type="search" placeholder="Buscar patrón… (ej: suscripción, licencia, '
        'gratis)" autocomplete="off" aria-label="Buscar patrón">\n'
        '  <span id="cuenta">60 de 60 patrones</span>\n'
        '</div>\n'
        '<div class="grid">\n@@TARJETAS@@\n</div>\n'
        '<p class="vacio" id="vacio">Ningún patrón coincide con esa búsqueda. Prueba con otra '
        'palabra.</p>\n'
        '</main>\n'
        '<footer>\n'
        '  <p><b>Fuente:</b> Business Model Navigator, Universidad de St. Gallen — '
        '<a href="https://www.businessmodelnavigator.com/explore" target="_blank" rel="noopener">'
        'businessmodelnavigator.com/explore</a>. Patrones descritos en '
        '<i>The Business Model Navigator</i> (Gassmann, Frankenberger &amp; Csik).<br>\n'
        '  Textos traducidos al español para el electivo <i>Innovación: Ideas Disruptivas para el '
        'Éxito</i> (FAE USACH). La traducción sigue el sentido del original; el enlace a cada '
        f'ficha en inglés está en cada tarjeta.</p>\n'
        f'  <p><a href="{PLAN}">← Volver al plan del electivo</a></p>\n'
        '</footer>\n'
        '<script>@@JS@@</script>\n</body>\n</html>\n'
    )
    html = html.replace("@@CSS@@", CSS).replace("@@TARJETAS@@", tarjetas).replace("@@JS@@", JS)

    with open(SALIDA, "w", encoding="utf-8") as f:
        f.write(html)
    tarjetas_n = html.count('class="card"')
    marcadores = html.count("@@")
    print(f"OK -> {SALIDA} ({len(html)} bytes, {tarjetas_n} tarjetas, marcadores: {marcadores})")


if __name__ == "__main__":
    main()
