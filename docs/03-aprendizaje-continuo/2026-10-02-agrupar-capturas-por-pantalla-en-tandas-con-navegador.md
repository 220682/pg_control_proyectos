# Agrupar capturas por pantalla en tandas con navegador (no una por ítem)

**Fecha:** 2026-10-02
**Origen:** Worker 1, tanda D (hallazgo M2 / B-H3 de presupuesto) del plan dashboard-economia-y-curva-s
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s.md` (mejora M2)
**Categoría:** `playwright/evidencia`

## Origen

Plan `2026-10-01-dashboard-economia-y-curva-s`, tanda D (Fase D + Fase T) con Playwright y login real.

## Observación

Con 22+ ítems que exigen navegador, «una captura por ítem» no cabe en el presupuesto de llamadas de una tanda. El Worker agrupó varias capturas en un solo archivo por pantalla (por ejemplo `F03-F04-F05-U05-*`, `U03-F08-F13-*`, `F10-U04-*`), lo que cubrió varios IDs con una sola imagen y dejó evidencia suficiente ítem por ítem sin multiplicar llamadas.

## Evidencia

- Capturas en `docs/02-trabajo-activo/03-evidencia/capturas/dashboard-economia-y-curva-s/` (9 archivos para ~20 ítems visuales).
- Tanda D: ~108 llamadas, por encima del objetivo ~80; F12 quedó sin ejecutar.

## Clasificación

Mejora de trabajo (método de evidencia). No es una regla de negocio.

## Etiqueta de categoría

`playwright/evidencia`

## Destino propuesto

Queda como aprendizaje; candidato a nota en el brief base de Workers (plantilla `13-brief-de-tanda.md`) y en `docs/01-contexto-repositorio/04-pruebas-y-evidencia.md`.

## Cambio propuesto

En el brief de una tanda con navegador, indicar explícitamente «agrupar capturas por pantalla desde el inicio» y estimar las llamadas por pantalla, no por ítem.

## Estado

`Borrador` — pendiente de revisión del Auditor.

## Referencia a la aprobación

Pendiente (Gate 2 de Victor).
