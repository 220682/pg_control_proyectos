# Resumen de cierre — Tanda P (RDT: formulario, borrador, PDF y consolidado)

## Tanda, rol y modelo

Tanda P, Worker 3, Sonnet 5.5, esfuerzo medio. Rama `local-worker-3`.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| P1 | Observado | Código: columnas «HH extra» y «HH normales» (total menos extra, calculado) por persona; «HM stand-by» y desplegable «Estado» por equipo; error visible en rojo (extra mayor que el total, negativos). `erroresDelParte` (O) bloquea el guardado. `tsc` y lint sin errores nuevos. | Capturas de escritorio y 390 px no hechas: sin cuentas de prueba en esta sesión. Pasa a la tanda L. |
| P2 | Conforme (prueba) / captura Observada | `plantilla.test.ts`: el borrador guarda y restaura `horasExtra`, `horasStandby`, `estado`; un borrador viejo abre con 0, 0 y vacío. `aplicarDatosPlantilla` ya lo hacía (P32 confirmado), no se tocó `borrador.ts` ni `tipos.ts`. | Captura pendiente en L. |
| P3 | Conforme | PDF generado en prueba y leído con `pdftotext`: tareo con TOTAL, EXTRA, NORMAL; equipos con HM OPER., STAND-BY, ESTADO; mismo formato PROM-GP-002, sin dinero. Rutas `partes/[id]/pdf` y `pdf-borrador` pasan los campos. Prueba `exportador-pdf.test.ts` (también con un RDT sin los campos). | — |
| P4 | Conforme | `consolidado.test.ts` (2 pruebas nuevas): las filas de HH ya incluyen la extra; las filas de HM suman operativas + stand-by; grupos nuevos «Desglose del total de HH» (normales, extra) y «Desglose del total de HM» (operativas, stand-by), sin total propio para no duplicar. Ruta `api/rdts/consolidado` lee `horas_extra` y `horas_standby`. | — |
| P5 | Conforme (código) / captura Observada | El GET de `partes/[id]` (O) ya devuelve los campos y el formulario los carga en corrección y solo lectura; los listados no muestran tareo. | Captura en L. |
| P6 | Conforme | `npm test`: 124 archivos, 1247 pruebas en verde. | — |
| P7 | Observado | No se intentó iniciar sesión ni aplicar migraciones (100 y 102 sin aplicar en esta sesión). | Recorrido Playwright y permisos, a la tanda L. |

## Rama, commits y archivos tocados

`local-worker-3`: 2d4b3e8 (P1-P3) y 1247100 (P4-P6), con push. `git branch --contains` los muestra solo en `local-worker-3`. Árbol limpio. Tocados: `FormularioCrearRdt.tsx`, `exportador-parte-pdf.ts`, `consolidado.ts`, rutas `partes/[id]/pdf`, `partes/pdf-borrador`, `consolidado`, y pruebas de `plantilla`, `exportador-pdf`, `consolidado`.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| P-H1 | archivo o carpeta huérfano | El `node_modules` del repo principal quedó a medias (50 entradas, `vitest` vacío) y existe un enlace `.worktrees/_node_modules_bloqueado_w4` hacia él: otro trabajador lo borró o lo renombró. Sin tocar nada del principal, se reemplazó el enlace de este worktree por un `node_modules` propio con `npm ci`. | Victor: reparar el principal; revisar el enlace `_node_modules_bloqueado_w4`. |
| P-H2 | mejora de trabajo | En worktrees, un `node_modules` compartido por enlace es frágil: una limpieza en otro worktree lo rompe para todos. | `docs/03-aprendizaje-continuo/` |
| P-H3 | mejora de trabajo | `npm test` vuelve a cambiar el snapshot de Curva S por fin de línea; se restauró con `git checkout`. | Mejora de trabajo ya conocida. |
| P-H4 | regla de negocio acordada | Decisión mía a validar: en el Consolidado el desglose de HH/HM va como grupo aparte sin total, y las filas de HM incluyen el stand-by. | Flujo 06 y 18 (Victor confirma). |

## Traspaso

Hecho: P1-P6 en código y pruebas. Falta: capturas de P1, P2, P5 y el recorrido P7 (L, con migraciones 100 y 102 aplicadas y cuentas de prueba). Verificación: `npm test` 1247 verdes; `npx tsc --noEmit` sin errores; `npm run lint` 9 errores y 22 avisos (los preexistentes); `npx next build --webpack` en verde.

## Llamadas y contexto

Unas 45 llamadas.

## Skills revisados

`cerrar-tanda` (usado, sin commit de documentación). Los demás no aplican.

## Fuentes de verdad revisadas

Ninguna editada. Pendientes: flujo `06-rdt.md` (columnas del formulario y del PDF) y flujo de Consolidado, a cargo del Documentador.
