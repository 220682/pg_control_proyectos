# Resumen — Limpieza de datos de prueba (script preparado, sin aplicar)

Worker de datos · 2026-10-18 · orden de Victor «borra todo de prueba». Solo lectura (GET con la sesión del administrador); no se borró ni escribió nada en producción; sin commits.

Entregables en `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/limpieza/`:
- `respaldo-antes-de-limpiar.json` — 3 RQ (ítems y comentarios), 2 RDT (nombre y DNI del personal redactados), ficha y checklist de PS-0005, 28 avisos visibles (36 filas) con id.
- `limpieza-datos-prueba.sql` — `begin; … commit;` con guardas, conteo antes, borrados por id exacto (cada uno con filas esperadas), comprobación que revierte si queda algo y `select` final antes/después. Dos secciones opcionales comentadas (RDT validado del 17-10 con recálculo del PR; celular de Logística 1).
- `limpieza-notas.md` — qué borra y qué no, filas por tabla, riesgos, Storage, ids.

Qué borra: servicio PS-0005 «PRUEBA T7» (`e15799ae-…`) en cascada; en PS-0000 los RQ SO-001/002/003 (3 + 4 ítems + 5 comentarios), el RDT rechazado del 14-10 (`dcf5e7b8-…`) con su historial, y los avisos de prueba (30 por id exacto + los de otras personas por referencia o código exacto, entre 7 y 20 que el administrador no puede ver).

Qué no borra: PS-0000, sus otros 35 RDT, las cuentas de prueba, avisos reales (`informe.emitido`, «hola», «falta subir» de PS-0001 a PS-0004, checklist del 07-10) y el RDT validado del 17-10 (opcional aparte).

Respuesta sobre el RDT validado del 17-10: sí altera PS-0000. El PR se reconstruye entero desde los RDT VALIDADO; borrarlo quita 8 HH reales y su costo (AC) del acumulado, PR, curva S y dashboard; el avance físico no cambia (metrado 0). Exige recalcular el PR (la sección opcional lo hace). Por eso queda comentado. El rechazado no afecta al PR.

Hallazgos para Victor: (1) el RDT del 18-10 cargado por Victor (`c0c665e0-…`, 40 HH, REGISTRADO) NO se toca: no es de T7B; (2) no se pudieron listar los avisos de otras personas (no se usaron sus cuentas); el SQL los borra por referencia y la guarda aborta si algo no encaja; (3) falta quitar de Storage la carpeta `e15799ae-…/` de `documentos-proyecto` (incluye `PRUEBA-T7-plano.txt`); (4) tras borrar PS-0005 el próximo N° OT debería volver a PS-0005.

Navegador cerrado. Snapshots nuevos de `.playwright-mcp/` por este Worker: ninguno (no se tomó snapshot; solo un log de consola `console-2026-10-18T23-14-46-545Z.log`, sin claves). Se buscó la clave del administrador en los snapshots y logs de las 23:00 UTC en adelante y en los entregables: no aparece. Unas 50 llamadas.
