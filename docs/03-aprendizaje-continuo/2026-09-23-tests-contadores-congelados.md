# Tests con contadores congelados y atribución errónea de fallos en vitest

**Fecha:** 2026-09-23  
**Origen:** Worker Fase 1 de Paquetes de Trabajo (chat `local_3`)  
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-09-23-paquetes-de-trabajo.md`

## Hallazgo 1: Contadores congelados

`nav-proyecto.test.ts` congelaba el total de ítems del nav (`toHaveLength(40)`). Al agregar el chip "Paquetes de Trabajo", la suite completa falló, pero el fallo **no** apareció al correr solo el test del módulo tocado (el contador 41 solo se detecta en la suite completa de todos los test files).

**Práctica:** al agregar un ítem a una lista con un test de conteo:
- Actualizar el contador del test existente (`40` → `41`, `39` → `40`, etc.).
- Añadir un test específico que fije la ubicación y el comportamiento del nuevo ítem (aquí: entre Cronograma y Plan Maestro, sin servicio no es link muerto).

## Hallazgo 2: Atribución errónea del fallo con grep

Al leer la salida de vitest por consola filtrada con `Select-String -Pattern "FAIL"`, la salida envuelta por la terminal (line wrap) produjo líneas que parecían de `vinculos.test.ts` pero eran artefactos de la envoltura del nombre largo del archivo real. El fallo estaba en `nav-proyecto.test.ts`, que sí pasaba limpio al correrlo aislado.

**Práctica:**
- Guiarse por la **sección `Failed Tests`** y el conteo del resumen, no por un filtro de `FAIL`.
- Antes de "arreglar" un archivo que aparece en el grep, correr ese archivo aislado (`vitest run src/lib/x.test.ts`) para confirmar que realmente es el que falla.