# Verificar maquetas y medir el lint sin crear infraestructura nueva

**Fecha:** 2026-10-01
**Origen:** Workers F0-B, F0-R, F0-T, F0-V, F1-A, F3-C y F5-A del plan niveles-paquetes-plan-maestro-rdt
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`
**Categoría:** `maquetas` y `lint`

## Hallazgo

- **Maquetas HTML sin navegador del repositorio:** el navegador de pruebas bloquea `file:` y `python -m http.server` no respondió en el entorno; un servidor Node mínimo local sí. Exponer el cálculo en `window.__maqueta` permitió comparar número a número contra el anexo. Sin navegador, el script se valida con `new Function`; para comprobar clics conviene tener jsdom en el repositorio de la app.
- **Reutilizar una maqueta aprobada:** reemplazar solo el marco (shell) con un script de cortes verificados evita regresiones en el lienzo; contar el balance de `<div>` tras cada corte (un corte mal anclado dejó un `</div>` de más).
- **Color en tablas:** una clase utilitaria (`.pct-ej`) pierde contra reglas de fila (`tr.real td`); calificar el selector (`tr.real td.pct-ej`) y probar la cascada, no solo que la clase se aplique.
- **Medidas de la maqueta junto a la comprobación:** si se anota «Observado — pendiente de F5» con medidas calculadas a ojo (`top-5`, `pl-5`), dejar escrita la medida de la maqueta al lado.
- **Lint de `main`:** `npm run lint` en el repositorio principal cuenta también los worktrees (24 585 problemas); medir la base dentro de un worktree limpio, o extrayendo `git archive <commit>` a una carpeta temporal con un enlace a `node_modules` (sin crear worktree, que requiere autorización); quitar el enlace con `rmdir` antes de borrar la carpeta.

## Destino propuesto

Aprendizaje; el último punto complementa `2026-09-23-eslint-baseline-vs-cero.md` (ya promovido).
