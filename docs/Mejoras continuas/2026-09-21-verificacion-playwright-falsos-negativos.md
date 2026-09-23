# Mejora de trabajo — falsos negativos en verificación con Playwright

> Origen: tarea [2026-09-21-dashboard-fase-3-agente-c.md](../Tareas%20de%20implementacion/2026-09-21-dashboard-fase-3-agente-c.md) (vueltas 1 y 2 del loop de verificación). Extraído el 2026-09-23.

## Lección 1 — texto en mayúsculas por CSS (`uppercase`) da falso negativo

Varias etiquetas de la interfaz usan la clase `uppercase` de Tailwind (transformación visual, no cambia el texto real). Un script de verificación que lee `body.innerText()` recibe el texto **ya transformado a mayúsculas** por el navegador; si la aserción busca el texto en minúscula/mixto original, falla aunque la pantalla esté correcta.

**Cómo evitarlo:** leer con `body.textContent()` en scripts de verificación — no está afectado por CSS. No tocar el producto (el `uppercase` es una convención visual válida ya usada en el resto de la app).

## Lección 2 — timeout fijo en vez de esperar la condición real

Un script que espera un tiempo fijo (`waitForTimeout(1000)`) tras una acción que dispara un ciclo `PATCH → router.refresh() → nuevo RSC` puede fallar si ese ciclo tarda más de lo esperado en el servidor de desarrollo (hasta ~3s visto en un caso real), aunque el guardado en base de datos ya haya funcionado.

**Cómo evitarlo:** esperar la condición real (ej. un atributo `aria-pressed="true"` con el texto correcto, o el parámetro esperado en la URL) en vez de un tiempo fijo arbitrario.

## Por qué importa

Ambas son causas de "FAIL" en una Punch List que en realidad son un problema del script de verificación, no del producto — confundirlas con hallazgos reales hace perder tiempo re-investigando la pantalla en vez del script.
