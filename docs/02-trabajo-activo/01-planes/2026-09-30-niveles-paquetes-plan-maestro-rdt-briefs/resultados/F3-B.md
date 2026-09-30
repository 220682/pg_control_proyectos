# Resultados F3-B · Plan Maestro: datos y API

Carril 2 · rama `local-worker-2` · commit `35bcf07` (sobre F3-A `72aace7`). Sin push ni merge.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada), verificar-permisos-por-rol (usada para `puedeCrearVersionPlanMaestro`, ver F3B-6), seguir-flujo-de-planes (no aplica: lo usa el Orquestador). Repo de la app: sin carpeta de Skills.

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F3B-1 | Conforme | `db/076` (quita `plan_maestro_partidas_plan_maestro_id_wbs_key`, deja índice normal), `db/077` (8 columnas nulas en `plan_maestro_partidas`), `db/078` (`motivo_version`). Aditivas, idempotentes, con comentario de deshacer. **Aplicadas y verificadas** (ver Migraciones). |
| F3B-2 | Conforme | `POST /api/plan-maestro`: BORRADOR sin paquetes, líneas desde `cronograma_actividad_partidas` (metrado > 0; en paquete si está en `paquete_trabajo_vinculos` de un paquete no archivado, si no directa), no lee `paquete_trabajo_programacion`; con aprobada parte de sus asignaciones (misma actividad y WBS) y exige `motivo` (`motivo_version`). `plan-maestro-api.test.ts` (datos simulados). |
| F3B-3 | Conforme | `GET` → `{ plan, lineas, asignaciones, semanas, reales }`; `reales` sale de `src/lib/plan-maestro/real-adaptador.ts` (`leerRealPorClave`, devuelve `[]`). Probado. |
| F3B-4 | Conforme | `PATCH` guardar/aprobar: `validarAprobacion` (Σ días = `metradoLinea` por línea, Σ líneas = contractual por partida, partidas del DP sin línea) con mensajes que nombran WBS y cantidades; reemplaza la aprobada y llama `recalcular_pr_planificado`. Probado, incluido que un 400 no cambia nada. |
| F3B-5 | Conforme | `lineas.test.ts` § F3B-5: `calcularPvAlCorte`, `calcularIndicadoresPartida`/`Proyecto` (mismo mapeo que `pr/page.tsx` y `dashboard/page.tsx`) suman las líneas repetidas de un WBS; espejo JS de los `group by` de `db/061` y `db/070`. Lectura del SQL y de `pr/page.tsx` ~205-209, `dashboard/page.tsx` ~133-137, `api/curva-s/route.ts` (solo min/max de fecha): todos agregan por línea y luego por WBS o por fecha. **Nada que reportar: todo suma.** Limitación: el SQL no se ejecutó en vitest (espejo en JS). |
| F3B-6 | Conforme (API con datos simulados) / Observado (en vivo) | `puedeCrearVersionPlanMaestro` (administrador y jefe de proyectos) en `permisos.ts` con prueba para los 13 roles (`permisos.test.ts`). `plan-maestro-api.test.ts`: 13 roles × POST/PATCH/GET (gestionar = admin/JP/planner; ver = 5 de economía + planner), 13 roles en versión nueva con aprobada (solo admin y JP pasan, el resto 403), 403 por alcance, 400 servicio inexistente. La comprobación en vivo con «Ver como» queda `Observado — pendiente de F5-C` (no se usó servidor). |

Comandos (Bash, `VITE_CONFIG_NATIVE_IGNORE_WARNING=true`): `npx vitest run` 73 archivos, 726 pruebas verdes; `npx tsc --noEmit` sin errores; `npx eslint .` en el worktree: 27 problemas (9 errores, 18 avisos), idéntico con y sin mis cambios (= los 27 de `main`).

## Migraciones (076 a 078)
- Vía directa (`PR_DB_URL`), 2026-09-30 18:26. Script temporal `migrar_F3-B.py` (modos `check`/`apply`), ya borrado; candado creado y borrado. `check` previo: la restricción existía y ninguna columna nueva, o sea, no estaban aplicadas.
- Aplicadas una a una en transacción: 076, 077, 078.
- Verificación posterior: restricción `unique (plan_maestro_id, wbs)` ya no existe; las 8 columnas de 077 y `motivo_version` existen.
- Conteos antes = después: `plan_maestro_partidas` 240, `proyecto_plan_maestro` 5, `plan_maestro_asignaciones` 260, `paquetes_trabajo` 0, `dp_partidas` 48.
- **Requiere autorización expresa de Victor: cambio de restricción (076)**. Victor ya la dio para esta relajación (WBS único), según el protocolo; queda constancia.
- Las 240 líneas existentes quedan con columnas nuevas nulas; el lector usa `metrado_contractual` cuando `metrado_linea` es null y deriva la clave (`DIRECTA:<partida>`).

## Handoff
- Falta para F3-C (pantalla): consumir la nueva forma de `GET` (`lineas` en lugar de `partidas`) y enviar `lineaId` en `PATCH` (se sigue aceptando `partidaId`). `FormularioPlanMaestro.tsx` (pantalla actual) lee `partidas` y dejará de funcionar contra esta API; es de F3-C. `POST` acepta `{ proyectoId, motivo? }`.
- F5-A: sustituir el cuerpo de `real-adaptador.ts` por `realPorClaveReporte(admin, proyectoId)` (C4, carril 4). Sin cambio de contrato: la firma de `leerRealPorClave(proyectoId)` es mía; ajustar si la de C4 necesita el cliente.
- F5-A/F5-D: registrar en la tabla del flujo 14 la fila **«Crear versión nueva del Plan Maestro cuando ya hay una aprobada: administrador y jefe de proyectos»** (más estricta que gestionar) y en el artefacto de la Matriz de permisos (política del repositorio).
- Decisión técnica a confirmar: la restricción de versión nueva se aplica solo a `POST`. **Aprobar** un borrador (que reemplaza la aprobada) sigue con `puedeGestionarPlanMaestro` (el planner podría aprobar un borrador creado por admin/JP). El brief solo pide restringir la creación.
- Decisión técnica: `metodo_distribucion` del borrador es `MANUAL` (primera versión) o `MIXTA` (desde una aprobada), ya que no hay distribución automática desde paquetes.
- Decisión técnica: `POST` exige al menos un vínculo con metrado; no exige el 100 % (se valida al aprobar, incluidas partidas del DP sin línea).
- En vivo (F5-B/C): crear BORRADOR real requiere las tablas de 079 (ya aplicadas por el carril 3) y vínculos con metrado; no se probó contra la base (solo simulado).

## Mejoras de trabajo
- Un heredoc grande de Bash con comillas simples sin cerrar dentro del texto no se ejecutó (ni falló limpio): para archivos con apóstrofes usar Write.
- El mock de Supabase de `paquetes-api.test.ts` (rama 3) se adapta bien: hay que hacer que `insert` asigne ids y los guarde en la tabla para encadenar `select` posteriores.

## Reglas de negocio detectadas
- Versión nueva del Plan Maestro con una aprobada: solo administrador y jefe de proyectos, con motivo obligatorio (ya aprobada en el Spec; llega al flujo 20 y 14 vía F5-D).
- Una partida puede repetirse en varias líneas del Plan Maestro; PV, planificado del PR y Curva S suman todas (probado).

## Huérfanos
`paquete_trabajo_partidas` y `paquete_trabajo_programacion` siguen sin uso (por contrato). `src/lib/plan-maestro/plan-maestro.ts` (`generarPropuestaDiaria`, `validarAsignacionesPartida`, etc.) queda sin uso desde la ruta; decidir en F3-C/F5-A si se retira.

## Llamadas
Aproximadamente 45.
