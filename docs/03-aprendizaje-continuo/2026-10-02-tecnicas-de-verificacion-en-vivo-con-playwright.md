# Técnicas de verificación en vivo con Playwright: archivo, «Ver como» y estado entre evaluate

**Fecha:** 2026-10-02
**Origen:** Worker 1, tandas T2 y T3 (mejoras M5, M6 y M8) del plan dashboard-economia-y-curva-s
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s.md` (mejoras M5, M6 y M8)
**Categoría:** `playwright/verificacion`

## Origen

Plan `2026-10-01-dashboard-economia-y-curva-s`, tandas T2 y T3 (verificación en vivo con login real sobre el proyecto de prueba PS-0009).

## Observación

Tres workarounds de herramienta que ahorraron iteraciones, todos del mismo tipo (técnicas de Playwright en verificación en vivo); se agrupan aquí por ser pequeños y de la misma clase:

1. **Subida de archivos** (M5): `playwright_browser_file_upload` no era fiable; se usó `page.setInputFiles` con el fixture copiado a Temp con nombre ASCII (el original trae `N°`).
2. **Suplantación «Ver como»** (M6): fue más barato forzar el rol con `POST /api/ver-como` + `page.reload` que con el combobox de la interfaz; se restaura con `DELETE /api/ver-como`.
3. **Estado entre `evaluate`** (M8): los `window.*` guardados vía `browser_evaluate` se pierden entre llamadas tras ciertos renders; conviene re-`fetch` los catálogos/plan dentro de cada evaluate de escritura en vez de depender de estado guardado.

## Evidencia

- `tanda-T2.md` § Mejoras (subida de archivos y «Ver como»); V03/V04 cerrados Conforme con ese método.
- `tanda-T3.md` § Mejoras (estado entre evaluate) y § Método: «Ver como» por `POST /api/ver-como` + recarga, restaurado con `DELETE /api/ver-como`.

## Clasificación

Mejora de trabajo (workarounds de herramienta). No es una regla de negocio.

## Etiqueta de categoría

`playwright/verificacion`

## Destino propuesto

Queda como aprendizaje; candidato a nota en el brief base de Workers para tandas con Playwright y en las notas de verificación en vivo del repositorio.

## Cambio propuesto

Documentar en el brief de tandas con navegador: usar `page.setInputFiles` con fixture en Temp de nombre ASCII si la subida falla; forzar «Ver como» por `POST/DELETE /api/ver-como` + recarga; re-`fetch`ar dentro de cada evaluate de escritura y no confiar en `window.*` entre llamadas.

## Estado

`Borrador` — pendiente de revisión del Auditor.

## Referencia a la aprobación

Pendiente (Gate 2 de Victor).
