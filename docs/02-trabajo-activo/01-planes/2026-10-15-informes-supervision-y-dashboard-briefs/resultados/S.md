# Resultado — Tanda S: AC con materiales y subcontratos en las pantallas

## Tanda, rol y modelo

Tanda S, Worker 2, Sonnet 5.5.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| S1 | Conforme (no probado en base) | `cargarDatosDashboard` lee `costo_materiales_acum` y `costo_subcontratos_acum`; helper `datosAcDesdeCabecera` usado por PR, Dashboard y descarga PDF/Excel. `cargar-dashboard.test.ts`: AC PR = AC Dashboard = 100. | Las columnas existen solo cuando Victor aplique la 102. |
| S2 | Conforme (no probado en base) | `TipoRecursoCosto` suma `material` y `subcontrato`; el Dashboard filtra los cuatro tipos; `CostoRealRecursos` los rotula. `costo-recursos.test.ts`: con las cuatro clases «Sin resolver» = 0. | Falta ver el bloque con datos reales tras aplicar la 102. |
| S3 | Observado | Código: `desgloseAc` (personal, equipos, materiales, subcontratos, sin resolver) en una franja sobre el pie; fila «Materiales y subcontratos (sin partida)» con AC en las columnas 16 y 21; pie corregido. Prueba unitaria `desgloseAc`. | Sin captura: no se inició sesión (regla de la tanda). Se cierra en L con las dos cuentas, escritorio y 390 px. |
| S4 | Observado | Prueba con el cargador real: AC PR = AC Dashboard y bloque de recursos cuadrado. El último punto de la Curva S se arma con el mismo valor: la Curva S es SQL (`curva_s_proyecto`), la prueba de texto de R5 ya asegura que llama a la misma función. | La igualdad real con la Curva S y con Costos (C5) se comprueba en L7 con base. Sin captura. |

## Rama, commits y archivos tocados

Rama `local-worker-2`, commit 1d7c338, subido (`git branch -r --contains` muestra `origin/local-worker-2`). Archivos: `pr/page.tsx`, `dashboard/page.tsx`, `cargar-dashboard.ts` (+test), `costo-recursos.ts` (+test), `CostoRealRecursos.tsx`, `datos-descarga.ts` (solo usa el helper; fuera de la lista del brief, necesario para que el PDF/Excel tengan el mismo AC).

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| S-H1 | conflicto con un flujo o pregunta | `datos-descarga.ts` también arma el AC; lo toqué para que PDF/Excel coincidan con la pantalla. | Confirmar o aceptar. |
| S-H2 | observación sobre la política | El PR no tiene «KPI AC» como tarjeta: puse una franja de desglose sobre el pie. Confirmar el diseño en L. | Gate 2 / L. |
| S-H3 | mejora de trabajo | Correr `npm test` reescribe el snapshot de `curva-s-route` (solo fin de línea); se restauró con `git checkout`. | Aprendizaje continuo. |
| S-H4 | regla de negocio acordada | BAC: `evm.ts` usa Σ `pr_partidas.bac`, `calcularBac` de `dashboard.ts` suma recursos (P21). No se midió diferencia ni se corrigió. | Anotado, sin acción. |

## Traspaso

Hecho S1 a S4 en código y pruebas. Falta: capturas y verificación en base (L). `npm test` 132 archivos / 1292 pruebas verdes; `tsc` limpio; lint 9 errores y 22 avisos (iguales a los preexistentes); `next build --webpack` correcto. Árbol limpio salvo `db/095*` y sin seguimiento.

## Llamadas y contexto

Unas 25 llamadas.

## Skills revisados

`cerrar-tanda` (secuencia seguida a mano). Los demás no aplican.

## Fuentes de verdad revisadas

Sin edición. Pendiente para el flujo 10 (PR): mencionar el desglose del AC y la fila «sin partida»; flujo 11 (Dashboard): el bloque de recursos incluye materiales y subcontratos.
