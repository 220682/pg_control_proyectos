# Resumen de cierre — Tanda R

## Tanda, rol y modelo

Tanda R (AC con materiales y subcontratos), Ola 1, Worker 3, Sonnet 5.5, esfuerzo medio.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| R1 | Observado | `db/102_ac_materiales_subcontratos.sql` + línea en `db/README.md`; revisada y probada con modelo TS, no en base | No se aplica la migración (la aplica el Orquestador); sin base indicada |
| R2 | Observado | `recalcular_pr_desde_rdt` reescrita desde el cuerpo de 100; caso a mano 1 000 / 200 al 30 % -> 300 y 60 en `ac-equivalencia.test.ts` | Igual que R1: sin ejecución en base |
| R3 | Observado | `curva_s_proyecto` reescrita desde el cuerpo de 100; `ac_acum` = HH+HM + función con el `ev_acum` de cada día | Igual que R1 |
| R4 | Conforme | `evm.ts` + prueba en `evm.test.ts` (AC 1 250 -> 1 610 con 300 + 60; AC/CPI por partida iguales); `npm test` verde | — |
| R5 | Conforme (a-e en TS/texto SQL) | `src/lib/pr/ac-equivalencia.test.ts` (a-e en verde) + `db/pruebas/102_comparacion_ac.sql` (solo lectura, para correr en base) | La parte (c) contra el cargador del Dashboard es estructural/numérica; la comparación en base queda pendiente |
| R6 | Observado | No probado en base: Victor no indicó ninguna | Orquestador/Victor: indicar PS-0011 u otro y correr `db/pruebas/102_comparacion_ac.sql` tras aplicar 102 |

Delta por componente (caso a mano, avance 30 %): materiales +300, subcontratos +60; con monto manual 150 el delta del subcontrato es 150 - 60 = +90; EV sin cambio.

## Rama, commits y archivos tocados

Rama `local-worker-3`. Commits: `a8f7089` (R1-R3) y `2bbeb62` (R4-R5), ambos pusheados y comprobados con `git branch --contains` (solo `local-worker-3`). Archivos: `db/102_ac_materiales_subcontratos.sql`, `db/README.md`, `db/pruebas/102_comparacion_ac.sql`, `src/lib/pr/evm.ts`, `src/lib/pr/evm.test.ts`, `src/lib/pr/ac-equivalencia.test.ts`.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| R-H1 | conflicto con un flujo o pregunta | `ac_materiales_subcontratos_al_corte` es `security definer` (fija `search_path = public`): `pr_subcontrato_medicion` tiene RLS sin política y la Curva S corre con la sesión del usuario; sin esto el monto manual se ignoraría en la Curva S. Cualquier autenticado podría pedir los dos totales de cualquier proyecto por RPC. Pregunta: ¿se acepta, o se pasa la Curva S al cliente de servicio? | Victor/Orquestador, Gate 2 |
| R-H2 | observación sobre la política | El brief habla de `ProyectoEvmDatos` con campos nuevos; `pr/page.tsx` y `dashboard/page.tsx` (tanda S) construyen ese objeto. Los dos campos se dejaron **opcionales** (`?: number`, 0 si faltan) para no romper compilación; la tanda S debe cargarlos desde `proyecto_pr.costo_materiales_acum/costo_subcontratos_acum` o el AC mostrado no cambia | Tanda S |
| R-H3 | regla de negocio acordada | Documentar en flujos 10 y 11: AC = HH + HM + legacy + materiales + subcontratos; avance físico sin tope; manual desde el día (Lima) de `actualizado_en`. Los flujos no se editaron | Documentador |
| R-H4 | conflicto con un flujo o pregunta | El avance físico usa `pr_partidas.bac` (columna nullable, rellenada por 060/063); el brief P21 compara con el BAC del Dashboard (suma de recursos): no se pudo medir sin base | R6, cuando Victor indique base |
| R-H5 | mejora de trabajo | Los heredocs con `\r`/`\n` en Bash se corrompen; los archivos `db/*.sql` existentes unos van en LF y otros en CRLF (la 102 quedó en CRLF); las pruebas que leen SQL deben normalizar `\r\n` | Aprendizaje continuo |
| R-H6 | mejora de trabajo | `npm test` deja modificado `curva-s-route.test.ts.snap` solo por fin de línea; se restauró con `git checkout` | Aprendizaje continuo |

## Traspaso

Hecho: migración 102 escrita (no aplicada), `evm.ts`, pruebas R5 y script SQL de comparación. Falta: aplicar 102 (Orquestador), que la tanda S cargue los dos campos nuevos en PR/Dashboard, y R6 con una base indicada. Verificación: `npm test` 124 archivos / 1 241 pruebas verdes; `npx tsc --noEmit` sin errores; `npm run lint` 9 errores y 22 avisos (los preexistentes); `npx next build --webpack` correcto. Árbol limpio.

## Llamadas y contexto

Unas 30 llamadas.

## Skills revisados

`cerrar-tanda` (usado). Los demás no aplican: no toca permisos por rol ni diseño.

## Fuentes de verdad revisadas

No se editó ninguna. Pendientes de actualizar: flujos `10-generacion-pr.md` y `11-*` (Dashboard) con la cuenta del AC (R-H3).

## R-fix (respuesta al hallazgo R-H1)

Commit `34b8bbf` en `local-worker-3`: `ac_materiales_subcontratos_al_corte` y `curva_s_proyecto` con `revoke` a public/anon/authenticated y `grant` a service_role (db/102); unico llamador de la Curva S es `api/curva-s/route.ts`, que valida sesion, rol y alcance antes, y ahora llama con `crearClienteAdmin()`. Tocados por permiso del Orquestador: `src/app/api/curva-s/route.ts` y su prueba (mock del cliente); `cargar-curva-s.ts` no cambio. Prueba de texto en `ac-equivalencia.test.ts`. `npm test` 1242 verdes, `tsc` sin errores.
