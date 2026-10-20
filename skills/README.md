# Skills del módulo contable

Dos skills que son **el procedimiento del ejercicio de clase**, escritas para que un agente las ejecute
sin el profesor. El caso completo —qué se preguntó, qué se midió y en qué nos equivocamos— está en
`caso-estado-resultados.html` en la raíz del repo.

## Qué hay acá

```
business-central-er/
  SKILL.md                       Cómo se construye un ER/balance en BC y cómo diagnosticar descuadres
  scripts/audita_movs.py         Auditoría determinística de un export (sin LLM)
  gen_caso_paso_a_paso.py        Generador del caso HTML a partir del xlsx
contabilidad-chile-niif/
  SKILL.md                       Taxonomía NIIF + normativa chilena vigente + mapeo de planes de cuenta
datos/                           (vacío; acá van los exports, no se versionan)
```

## Qué es una skill (y por qué esto no es un informe)

Un informe se lee una vez. Una skill es un **procedimiento que se ejecuta para siempre**. La diferencia
práctica: este mismo ejercicio, hecho de nuevo con otro cliente, corre con

```bash
python3 skills/business-central-er/scripts/audita_movs.py "Movs. contabilidad.xlsx"
python3 skills/business-central-er/scripts/audita_movs.py archivo.xlsx --json   # para otro programa
```

y devuelve cuadratura debe/haber, activo, pasivo, patrimonio, resultado y los hallazgos, sin volver a
pensar el método.

## Cómo se usó en clase

1. Preguntar qué hay antes de buscar.
2. Definir el alcance (ER y Balance son estados distintos; el segundo obliga al cierre).
3. Ubicar la norma y **verificar su vigencia**.
4. Inspeccionar el dato real antes de calcular.
5. Calcular por dos caminos y exigir que coincidan.
6. Recién ahí entregar.

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

## Los dos errores del ejercicio (y por qué se enseñan)

- **Sumar solo las cuentas `4xxx` como gasto.** El plan chileno usa también `5/6/7`. Omitirlas infla el
  resultado exactamente en su monto: en el caso real, $130M sobre $3.795M de gasto. Sumar `4,5,6,7,8,9`.
- **`startswith("23")` para patrimonio.** No matchea `2301001`. Usar `c[:3] == "230"`.

Y el chequeo fuerte no es `A = P + PN` sino **`Activo − Pasivo = Resultado`**: si el patrimonio viene de una
apertura de otro ejercicio sin cierre intermedio, la primera identidad no da y **no es un error**.

Se enseñan porque un error bien diagnosticado enseña más que diez fórmulas correctas.
