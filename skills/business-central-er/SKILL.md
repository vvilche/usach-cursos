---
name: business-central-er
description: "Use al armar ER o balance en Business Central."
version: 1.0.0
license: MIT
---

# Estado de Resultados y Balance en Business Central

## When to Use

Cuando Victor (o un cliente) pide armar, revisar o explicar un **Estado de Resultados**, un **Balance** o
un cierre en **Microsoft Dynamics 365 Business Central**, o cuando entrega un export
`Movs. contabilidad (NN).xlsx` para analizar. No usar para contabilidad sin BC (ver `contabilidad-chile-rag`)
ni para cotizaciones.

## Regla de oro: el dato sale del archivo, no del LLM

Ningún número se escribe sin calcularlo de la sábana real con Python. El LLM **no suma**. Si no hay archivo,
se dice que no hay archivo; no se estima un resultado.

## Anatomía del export "Movs. contabilidad"

Export estándar de BC (Contabilidad → Movimientos de contabilidad → exportar). Columnas reales observadas:

```
Fecha registro | Tipo documento | Id. usuario | Nº documento | Nº cuenta | Nombre cuenta | Descripción |
N.° tarea proyecto | Item de Gasto | Centro de Gestión | N.º proyecto | Flujo de Caja | Cód. divisa origen |
Importe divisa origen | Importe IVA divisa origen | Importe de IVA no deducible de moneda de origen |
Importe debe ($) | Importe haber ($) | Importe ($) | Tipo contrapartida | Cta. contrapartida | Nº mov. |
N° de Factura|Rut Prov
```

- `Item de Gasto`, `Centro de Gestión`, `Flujo de Caja`, `N.º proyecto` son **dimensiones de BC** (Analysis Views).
- `Importe ($)` ya viene con signo: debe positivo / haber negativo. **Es la columna que se suma para saldos**,
  no `debe` ni `haber` por separado.
- Ojo con tildes y `$` en los nombres de columna: usar `dict(zip(hdr,row))` y nunca índices fijos.

## Cómo se construye el ER en BC (Financial Reports)

BC no trae un ER hardcodeado. Se arma con **Financial Reports** (antes *Account Schedules*):

1. **Chart of Accounts** — cada cuenta necesita `Account Category` (Assets/Liabilities/Equity/Income/Expense)
   y `Account Subcategory`. **El ER solo lee Income y Expense.** Una cuenta mal categorizada se omite en silencio.
   Es el error #1 y no genera ningún mensaje de error.
2. **General Ledger Setup** — `Allow Posting From/To` abre el período; sin eso no hay datos que reportar.
   `Closing Date` bloquea el ejercicio cerrado.
3. **Row Definition** — la estructura. Tipos de fila: `Header`, `Account Range` (ej. `3101002..3101999`),
   `Total`, `Formula` (referencia por número de fila, ej. `ROW1-ROW2`), `Beginning Balance`, `Net Change`.
4. **Column Definition** — el tiempo: `Net Change`, `Balance at Date`, `Comparison Period`, `% of Total`, `Budget`.
5. **Account Schedule** — Row Def + Column Def + `Analysis View` (qué dimensión cortar). Exporta a Excel o
   publica como KPI web service.
6. **Dimensiones** — mismo Row Def, distinto Analysis View, da el ER por centro de gestión o proyecto.

## Diagnóstico: "el ER no cuadra con el balance"

**Primero descartar el error propio.** Medido en un caso real: se reportó un "descuadre de $130.079.797
por falta de cierre de ejercicio" cuando en realidad el script de cálculo solo sumaba las cuentas de gasto
`4xxx` y **omitía las `6xxx` y `7xxx`**. La diferencia era exactamente el total de esas cuentas
($216.546.7 + $127.914.330 = $130.079.797). Antes de culpar al archivo, verificar que el cálculo separe
bien ingresos de gastos.

Orden de revisión, del más probable al menos:

1. **Bug en el propio cálculo:** clases de gasto incompletas (chileno usa 4, 5, 6, 7).
2. Cuenta con `Account Category` equivocada → el ER la ignora sin avisar.
3. Movimientos fuera del rango de fechas / período cerrado.
4. Cierre de ejercicio no corrido: las cuentas de resultado arrastran saldo y el patrimonio no incorpora la utilidad.
5. Dimensión obligatoria sin valor → el movimiento no aparece en el Analysis View.

**Chequeo obligatorio antes de entregar** (`scripts/audita_movs.py`):
- `sum(debe) == sum(haber)` → si falla, hay error de digitación.
- **Gastos = clases 4,5,6,7,8,9. Usar `c[0] in "456789"`, NUNCA `startswith("4")`.**
- **Patrimonio = subgrupo `230x`: `c[:3] == "230"`. NUNCA `startswith("23")`** (no matchea `2301001`).
- `Activo − Pasivo == Resultado` → este sí es el chequeo fuerte.
- Si hay patrimonio de apertura de otro ejercicio, `A = P + PN` no da y **no es un error**: el archivo mezcla
  ejercicios sin cierre intermedio. Decirlo así, no inventar un "descuadre".
- Cuentas de activo con saldo negativo / pasivo con saldo deudor → revisar signo o naturaleza.

## Plan de cuentas chileno vs. BC

El plan chileno tradicional usa el primer dígito como clase (`1` activo, `2` pasivo, `3` resultado acreedor,
`4` gasto). BC **no** usa eso: usa `Account Category`.
Consecuencia: hay que poblar `Account Category`/`Subcategory` cuenta por cuenta. Al mapear, la clasificación
correcta es de **naturaleza contable**, no del prefijo numérico.

## Entregable con Victor

- HTML (SVG/tablas), nunca .md suelto.
- Un solo archivo con pestañas (ER / Balance / Mapeo NIIF / Dimensiones), no varios archivos sueltos.
- Cada cifra marcada como MEDIDO (del archivo) y cada norma con fuente y fecha de vigencia.
- Abrir con `open -a "Google Chrome" <ruta absoluta>`.

## Pitfalls

- El export puede traer el encabezado con BOM/espacios: limpiar `str(h).strip()`.
- Los nombres de columna cambian entre localizaciones (`Importe (I$)I`, etc.). Validar contra `hdr` impreso.
- No confundir `Importe ($)` (movimiento con signo) con `Importe debe ($)` (columna bruta).
- Fechas vienen como `datetime`, incluidas las de apertura con hora `23:59:59`.
- Un mismo `Nº documento` con varias filas = un asiento; no sumar por documento sin agrupar.
- **Nunca afirmar un diagnóstico contable sin probar el cálculo contra un segundo camino.** Calcular el total
de gastos por dos métodos distintos (suma de negativos de clase 3 y suma de clases 4-9) y verificar que coincidan
antes de escribir la conclusión en el entregable.
- El repo de trabajo real de USACH es el que tiene remoto a `vvilche/usach-cursos`; hay copias vacías (ver `usach-cursos`).

## Archivos

- `scripts/audita_movs.py` — cuadratura debe/haber, balance, ER y hallazgos. Determinístico, sin LLM.
