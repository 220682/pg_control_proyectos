# 2026-10-21 — Los esperados de una prueba se fijan antes y se calculan desde el presupuesto, no desde la app

## Origen

Plan [`2026-10-21-correcciones-prueba-rdt-ps0001.md`](../02-trabajo-activo/01-planes/2026-10-21-correcciones-prueba-rdt-ps0001.md), apartado «Mejoras (de trabajo)», fila M1. Nace de la verificación de la prueba del RDT en PS-0001 (19.10.2026) hecha con el calculador de esperados [`scripts/esperados_rdt_ps0001.py`](../../scripts/esperados_rdt_ps0001.py). Es método de trabajo, no regla del sistema.

## Observación

En la prueba funcional del RDT, desde la segunda tanda los «esperados» se recalcularon con las reglas que la app mostraba (tarifas sin resolver, materiales en 5.389,32, HH con la transversal) y los cuadros dijeron «OK». Eso comprueba que la app acumula de forma consistente, no que la regla sea la correcta. Además se sustituyeron personas del guion (un CAPATAZ por un OPERARIO, etc.), de modo que la prueba nunca ejercitó las tarifas previstas. El informe final concluyó «los cálculos cuadran», cierto solo para avance, valor ganado y metrados.

Al recalcular con un calculador independiente de la app, desde el presupuesto y el cronograma, aparecieron cuatro vacíos reales: costo real (AC) con 1.790,10 de horas a costo 0 por cargos sin tarifa, HH reales e IP con las HH de la transversal, SPI con el PV al 19.10 contra EV hasta el 23.10, y un RDT con fecha futura aceptado.

## Evidencia

- Tabla «Verificación de la prueba anterior» del plan de correcciones (esperado original contra mostrado: EV 1.284,44 / 2.978,37 / 4.827,61 / 6.549,78 / 8.287,52 coinciden; AC de D5 esperado 9.167 a 9.528 contra 7.754,89 mostrado; HH 290,72 e IP 0,76 contra 268 y 0,788).
- Calculador independiente: `scripts/esperados_rdt_ps0001.py`.

## Clasificación

Mejora de trabajo (método de verificación). Candidata a procedimiento reusable.

## Etiqueta de categoría

`método`, `verificación`, `pruebas`

## Destino propuesto

Este archivo y, si se repite en otra prueba, la guía de pruebas de `01-contexto-repositorio/04-pruebas-y-evidencia.md` o un Skill.

## Cambio propuesto

1. **Fijar los esperados antes de empezar** la prueba, calculados desde las fuentes (presupuesto, cronograma, Plan Maestro) con un calculador independiente de la app, y guardarlos en el plan de la prueba.
2. **No recalcular los esperados durante la prueba** con lo que la app muestra. Toda diferencia entre lo esperado y lo mostrado es un hallazgo: se decide si falla la app o el esperado, con Victor, y se registra.
3. **No sustituir a las personas, cargos ni equipos del guion.** Si hace falta cambiarlos, se anota como desviación del guion, porque deja de ejercitar lo previsto.
4. El veredicto de un informe de prueba dice qué familias de cifras se verificaron de forma independiente y cuáles solo por consistencia.

## Estado

`Pendiente` (nuevo, 2026-10-21, plan Correcciones de la prueba del RDT en PS-0001, M1).

## Referencia a la aprobación

Sin aprobación de promoción todavía; Victor ordenó la guía v2 con esperados fijados antes de empezar (Registro de decisiones del plan, 2026-10-21).
