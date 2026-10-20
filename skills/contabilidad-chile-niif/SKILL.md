---
name: contabilidad-chile-niif
description: "Use al mapear un plan de cuentas chileno a NIIF."
version: 1.0.0
license: MIT
---

# Taxonomía contable: NIIF + normativa chilena vigente

## When to Use

Cuando hay que decidir **qué norma rige** un estado financiero en Chile, mapear un plan de cuentas chileno a las
líneas NIIF, o verificar si una tasa/plazo/umbral está vigente antes de usarlo. Complementa a `business-central-er`
(que cubre la herramienta BC); esta skill cubre la **norma**.

## Las tres capas (no colapsarlas)

La contabilidad chilena no es una sola normativa. Conviven y colisionan:

1. **NIIF / IFRS** — la estructura del estado financiero. Fuente: IFRS Foundation.
2. **Tributaria (SII)** — el resultado tributario. Se determina con reglas propias (arts. 29-33 LIR),
   **no** con NIIF. Una empresa puede tener utilidad NIIF y pérdida tributaria, o al revés.
3. **Regulatoria sectorial** — CMF, Superintendencias, BCCh, según el tipo de entidad.

Error clásico: usar el resultado NIIF como base imponible. Son dos resultados y ambos deben reconciliarse.

## Estructura NIIF: códigos de la taxonomía

IFRS Taxonomy 2024 (versión español, 258 págs) organiza por estado:

| Código | Estado |
|---|---|
| `210000` | Situación financiera, corriente/no corriente |
| `220000` | Situación financiera, orden de liquidez |
| `310000` | Resultado integral **por función del gasto** |
| `320000` | Resultado integral **por naturaleza del gasto** |
| `410000`/`420000` | Componentes ORI (netos / antes de impuestos) |
| `510000`/`520000` | Flujos de efectivo (directo / indirecto) |
| `610000` | Cambios en el patrimonio |

Líneas del ER por función (`310000`), en orden: Ingresos de actividades ordinarias → Costo de ventas →
**Ganancia bruta** → Otros ingresos → Costos de distribución → Gastos de administración → Otros gastos →
Otras ganancias (pérdidas) → **Ganancia por actividades de operación** → Ingresos/costos financieros →
Participación en asociadas → Impuesto → Resultado del período.

Cada línea trae su referencia normativa (ej. `NIC 1.82(a)`, `NIC 1.103`). Esa referencia es la que se audita.

## Cambios de vigencia que hay que verificar SIEMPRE

**No citar una norma sin confirmar que está vigente hoy.** Dos que cambian pronto:

- **IFRS 18** reemplaza a NIC 1 para ejercicios que comiencen desde **1-enero-2027**. Exige dos subtotales
  nuevos: *resultado operativo* y *resultado antes de financiamiento e impuestos*, y revelar las medidas de
  desempeño definidas por la administración. Un ER que no separa "resultado operativo" hay que reestructurarlo.
- **Ley 21.850** (Reconstrucción Nacional, publicada 17-10-2026) baja el IDPC gradualmente:
  2026 = 27% · 2027 = 25,5% · 2028 = 24% · 2029+ = 23%. Además restablece la integración total
  (restitución del crédito: 35% en 2026, 30% en 2027, 20% en 2028, 0% desde 2029).
  Régimen Pro Pyme (14 D N°3): 12,5% en 2026-2027, 15% en 2028.

Verificar en: `sii.cl` (FAQ tasas IDPC, actualizada) y el texto de la ley en LeyChile. La página de FAQ del SII
sobre tasas de primera categoría es la fuente más rápida y confiable para esto.

## Mapeo plan chileno → NIIF

El plan chileno tradicional usa el primer dígito como clase: `1` activo, `2` pasivo, `3` resultado acreedor,
`4` gasto, y `5/6/7` según la empresa (gastos de administración, operacionales, financieros).

**Trampa medida:** al sumar gastos, tomar solo `4` deja fuera `6xxx` y `7xxx`. En un caso real eso omitió
$130M de $3.795M de gasto y el resultado salió inflado en ese monto exacto. Sumar siempre `4,5,6,7,8,9`.

**Trampa de prefijo:** patrimonio es el subgrupo `230x` (capital, revalorización, utilidades acumuladas).
`startswith("23")` **no** matchea `2301001` — hay que usar `c[:3] == "230"`.

El mapeo a NIIF es por **naturaleza contable**, no por prefijo numérico: una cuenta "GASTOS LEGALES" puede ser
administración o distribución según el caso, y hay que preguntarlo.

## Cómo obtener las fuentes (los sitios chilenos bloquean)

- **SII y CMF bloquean** `web_extract` y a veces por IP. Usar el navegador real, o `curl` con User-Agent.
- **LeyChile**: la página carga el articulado por JS. El texto completo se baja con el exportador oficial:
  `https://nuevo.leychile.cl/servicios/Consulta/Exportar?radioExportar=Normas&exportar_formato=pdf&nombrearchivo=<NOMBRE>&hddResultadoExportar=<IDNORMA>.<FECHA>.0.0%23`
  (los parámetros exactos salen del enlace "descargar" de la propia página de la norma).
- **IFRS Foundation** sí responde a `web_extract`: la página de cada norma trae la fecha de vigencia.
- Guardar los PDF en `fuentes/` del proyecto con el nombre de la norma, no en /tmp.

## Entregable

HTML con las tres capas separadas, cada afirmación normativa con su fuente y fecha de vigencia, y un cuadro
visible de "qué cambia y cuándo" cuando haya reforma en trámite o recién publicada.
