# Estado de Resultados en Business Central — material de la clase

Material del módulo contable del electivo. Todo derivado de un export **real** de Business Central
(`Movs. contabilidad`), no de ejemplos de manual.

## Qué hay acá

```
business-central-estado-resultados.html   Entregable: manual + ER/Balance sobre datos reales (abrir en navegador)
skills/
  business-central-er/
    SKILL.md                Cómo se construye un ER en BC y cómo diagnosticar que no cuadre
    scripts/audita_movs.py  Auditoría determinística de un export (sin LLM)
    gen_er_html.py          Generador del HTML a partir del xlsx
  contabilidad-chile-niif/
    SKILL.md                Taxonomía NIIF + normativa chilena vigente + mapeo de planes de cuenta
datos/                      (vacío; acá van los exports, no se versionan)
```

## Cómo usarlo

Auditar cualquier export de movimientos contables:

```bash
python3 skills/business-central-er/scripts/audita_movs.py "/ruta/Movs. contabilidad.xlsx"
python3 skills/business-central-er/scripts/audita_movs.py archivo.xlsx --json   # para otro programa
```

Imprime cuadratura debe/haber, activo, pasivo, patrimonio, resultado y los hallazgos.

## Las tres capas normativas (resumen)

1. **NIIF / IFRS** — estructura del estado. Taxonomía 2024: `210000` balance, `310000` ER por función,
   `320000` ER por naturaleza, `510000`/`520000` flujos, `610000` patrimonio.
2. **SII** — el resultado tributario se determina con los arts. 29-33 de la LIR, **no** con NIIF.
   Son dos resultados distintos y ambos deben cuadrar.
3. **CMF** — exige NIIF a las entidades fiscalizadas.

## Vigencia — verificar antes de usar

- **IFRS 18** reemplaza a NIC 1 desde ejercicios que empiecen el **1-ene-2027**. Exige subtotales nuevos
  (resultado operativo, resultado antes de financiamiento e impuestos).
- **Ley 21.850** (publicada 17-10-2026) baja el IDPC: 2026 = 27% · 2027 = 25,5% · 2028 = 24% · 2029+ = 23%.
  Pro Pyme: 12,5% (2026-27), 15% (2028). Integración total restablecida desde 2029.

## Dos trampas que cuestan caro

- **Sumar solo las cuentas `4xxx` como gasto.** El plan chileno usa también `5/6/7`. Omitirlas infla el
  resultado exactamente en su monto. Sumar `4,5,6,7,8,9`.
- **`startswith("23")` para patrimonio.** No matchea `2301001`. Usar `c[:3] == "230"`.

Y el chequeo fuerte no es `A = P + PN` sino **`Activo − Pasivo = Resultado`**: si el patrimonio viene de una
apertura de otro ejercicio sin cierre intermedio, la primera identidad no da y no es un error.
