# Emular viewport móvil con CDP cuando la herramienta de resize no lo aplica

**Fecha:** 2026-10-02
**Origen:** Worker 1, tanda D (hallazgo M3) del plan dashboard-economia-y-curva-s
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s.md` (mejora M3)
**Categoría:** `playwright/viewport`

## Origen

Plan `2026-10-01-dashboard-economia-y-curva-s`, tanda D, verificación responsive (escritorio 1440 y móvil 390).

## Observación

`browser_resize` no aplicaba el viewport: la ventana seguía reportándose en 1440 css px. Para la evidencia móvil de 390 px hubo que usar el protocolo CDP con `Emulation.setDeviceMetricsOverride`. Es un workaround de herramienta, no un cambio de la app.

## Evidencia

- Capturas móviles `R05-U05-*` y `R05-*` en `docs/02-trabajo-activo/03-evidencia/capturas/dashboard-economia-y-curva-s/`.
- Confirmación del viewport efectivo en la propia sesión de Playwright.

## Clasificación

Mejora de trabajo (workaround de herramienta). No es una regla de negocio.

## Etiqueta de categoría

`playwright/viewport`

## Destino propuesto

Queda como aprendizaje; candidato a nota en el brief base de Workers si la verificación responsive por 390 px se repite.

## Cambio propuesto

Documentar en el brief que, si `browser_resize` no surte efecto, se use CDP `Emulation.setDeviceMetricsOverride` y se compruebe el viewport antes de tomar la captura.

## Estado

`Borrador` — pendiente de revisión del Auditor.

## Referencia a la aprobación

Pendiente (Gate 2 de Victor).
