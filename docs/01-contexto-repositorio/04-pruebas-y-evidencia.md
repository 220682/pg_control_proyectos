# Pruebas y evidencia

## Verificación en vivo — Punch List de Mejoras

El checklist de cada lote **no es una tabla estática en el .md** — es un artifact interactivo, con guardado en la nube:

**https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd**

Cada lote (tab) tiene sus ítems con estado **Conforme / Observado / Sin verificar**, comentario y capturas de pantalla pegadas (Ctrl+V). Victor lo usa mientras prueba en la app real. Al crear un nuevo lote de implementación, se agrega ahí como checklist nuevo. El archivo de evidencia local (`02-trabajo-activo/03-evidencia/<tema>.md`) enlaza a este artifact y registra el resultado en texto — los dos lugares coexisten, uno no reemplaza al otro (ver `02-trabajo-activo/03-evidencia/README.md`).

## Cuándo es obligatorio Playwright

Para cualquier cambio de interfaz o comportamiento en `py_control_proyectos_web`, el Worker corre un script de verificación con Playwright **antes** de reportar un ítem de la Punch List como listo. Es autoverificación del Worker; no reemplaza la prueba final de Victor en la Punch List interactiva.

### Falsos negativos conocidos (verificado en la Fase 3 del dashboard, 2026-09-21)

- **Texto en mayúsculas por CSS (`uppercase`):** leer con `body.textContent()`, no con `innerText()` — `innerText()` devuelve el texto ya transformado visualmente por CSS, y una aserción que busca el texto original (minúscula/mixto) falla aunque la pantalla esté correcta. No se toca el producto por esto: `uppercase` es una convención visual válida.
- **Timeout fijo en vez de esperar la condición real:** un ciclo `PATCH → router.refresh() → nuevo RSC` puede tardar más que un `waitForTimeout` fijo (hasta ~3s visto en un caso real) sin que el guardado real haya fallado. Esperar la condición real (un atributo, un parámetro en la URL) en vez de un tiempo arbitrario.

Ambas son causas de "FAIL" que en realidad son un problema del script de verificación, no del producto — confundirlas con hallazgos reales hace perder tiempo re-investigando la pantalla en vez del script.

## Lint: contra `main`, no contra cero

`npx eslint src` en `py_control_proyectos_web` puede tener deuda preexistente (errores/warnings ya presentes en `main`, no introducidos por la tarea en curso). Criterio de verificación:

1. Comparar el total contra `main` antes de reclamar un archivo — si el conteo es idéntico, la deuda es previa.
2. Lintear solo los archivos tocados por la tarea. Si salen limpios, el trabajo no introdujo deuda nueva.
3. Reportar en la evidencia: "eslint: N errores/M warnings, idéntico conteo al de `main`; archivos tocados: limpios" (o el conteo real si cambió).

## Tests: contadores congelados y atribución de fallos

- **Contadores congelados:** un test que fija el largo de una lista (`toHaveLength(N)`) falla en la suite completa cuando se agrega un ítem, aunque el módulo tocado pase aislado — el contador solo se detecta corriendo todos los test files juntos. Al agregar un ítem a una lista con test de conteo: actualizar el contador existente y añadir un test específico que fije la ubicación y el comportamiento del nuevo ítem.
- **Atribución errónea con filtros de consola:** filtrar la salida de test runners con un patrón de texto (ej. `grep`/`Select-String -Pattern "FAIL"`) puede mezclar líneas envueltas por la terminal (line wrap) de un archivo con el nombre de otro. Guiarse por la sección de tests fallidos y el conteo del resumen del runner, no por un filtro de texto. Antes de "arreglar" un archivo que aparece en el filtro, correrlo aislado para confirmar que es el que realmente falla.

## Capturas, login y datos

- No se usan credenciales ni datos reales sin autorización explícita (ver `../00-estandar-agentes/01-principios-y-seguridad.md`).
- Las capturas de pantalla de evidencia se pegan en el artifact de Punch List interactivo, no como archivos sueltos en el repositorio.

## Si un caso no puede verificarse

Se documenta la limitación explícitamente en el archivo de evidencia (sección "Limitaciones o casos no verificables") — nunca se afirma que un ítem quedó Conforme sin haberlo verificado.
