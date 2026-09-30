# Resultados F4-A · RDT: datos, catálogo desde el Plan Maestro y real por clave

Carril 4 · rama `local-worker-4` · commit `a037e98`. Sin push ni merge.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada en la secuencia de cierre), verificar-permisos-por-rol y seguir-flujo-de-planes (no aplican: sin cambio de permisos; el segundo lo usa el Orquestador). Repo de la app: sin carpeta de Skills.

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F4A-1 | Observado | `db/082` (paquete_trabajo_id en `rdt_actividades` y `rdt_actividad_partidas`), `db/083` (`es_derivada`, `declaracion_id`, `metrado_derivado` + check), `db/084` (índices). Aditivas, idempotentes, con comentario de deshacer. **No aplicadas**: el sistema denegó el script (ver Handoff). |
| F4A-2 | Conforme | `src/lib/rdts/declaracion-paquete.ts` (reutiliza `repartirAvanceDelPaquete` por import relativo, sin editarlo; `validarDeclaracionPaquete`, `repartirDeclaracionPaquete`, `claveReporte`, `validarClaveEnPlanMaestro`). Pruebas en `rdt-paquetes.test.ts`. |
| F4A-3 | Conforme | `GET /api/rdts/catalogos` añade `estadoPlanMaestro`, `lineasPlanMaestro` (por clave, líneas de una clave sumadas, con modo y guía) y `mensajePlanMaestro`; lógica en `catalogo-plan-maestro.ts`. Probado con Supabase simulado (con y sin plan). |
| F4A-4 | Conforme | `src/lib/rdts/real-por-clave.ts`: `realPorClaveReporte(admin, proyectoId)` + `agregarRealPorClave` pura. Solo partes VALIDADO, metrado solo de `D`, horas de tareo `es_moi=false` (D, C y NC), por clave y día. Probado. |
| F4A-5 | Conforme | Prueba «clave estable entre versiones»: un real `P:X` y dos versiones del plan con distinto id de línea dan la misma clave `P:X`. |

Verificación (Bash, `VITE_CONFIG_NATIVE_IGNORE_WARNING=true`, en el worktree): `npm test` 71 archivos, 689 pruebas verdes (14 nuevas); `npx tsc --noEmit` sin errores; `npx eslint src` 27 problemas (9 errores), igual que `main`, ninguno en archivos tocados.

## Handoff (migraciones 082 a 084: NO aplicadas)
- No se comprobó si ya estaban: el clasificador denegó `python migrar_F4-A.py check` (sin explicación). No lo rodeé ni lo partí. No se creó candado; no se leyó `entorno_variable.txt`.
- Script listo, fuera del repo, sin credenciales dentro (lee `PR_DB_URL` en el proceso): `C:\Users\BRANDY\AppData\Local\Temp\claude\D--VICTOR-CLAUDE-CODE-pg-control-proyectos\3a959253-7780-4b11-9071-ae185aa5ef45\scratchpad\migrar_F4-A.py`. Se dejó sin borrar porque Victor lo necesita; borrarlo tras aplicar.
- Comandos exactos (Victor los aprueba o los corre con `!`): `python "<ruta>" check` (select 1, conteos de `rdt_actividades`, `rdt_actividad_partidas`, `rdt_partes`, `paquetes_trabajo`, `dp_partidas`, `plan_maestro_partidas`, y existencia de columnas/índices) y luego `python "<ruta>" apply` (aplica 082, 083, 084 una a una en transacción y repite conteos). Antes de `apply`, crear el candado `resultados/CANDADO-MIGRACIONES.txt` y borrarlo al terminar. Tras aplicar: conteos antes = después.
- Dependencia: `GET /api/rdts/catalogos` lee columnas de `plan_maestro_partidas` que crea el carril 2 (076–078: `metrado_linea`, `clave_reporte`, `paquete_*`); hasta que se apliquen, con plan aprobado el catálogo devuelve `lineasPlanMaestro: []` y el error en `erroresParciales`. `rdt_*` ya necesita 082–084 para `real-por-clave`.

## Decisiones técnicas (a confirmar con Victor)
- Nombres de los campos derivados: el plan no los dejó fijados; se usaron `declaracion_id` y `es_derivada`, más `metrado_derivado` (añadido: el metrado repartido a cada partida derivada no cabe en `rdt_actividades.metrado_ejecutado`). **Por confirmar con Victor.**
- **Riesgo para F4-B/F4-C:** `recalcular_pr_desde_rdt` (`db/053`, no modificable) suma `a.metrado_ejecutado` de la actividad por cada vínculo de partida. Una actividad con filas derivadas contaría su metrado declarado en cada partida derivada, en vez de `metrado_derivado`. Hay que decidir cómo se guardan las derivadas (p. ej. actividades derivadas propias con su metrado) o autorizar un ajuste a 053. Devuelto al Orquestador.
- Clave de reporte = `(paquete|'DIRECTA'):dpPartidaId` (contrato C2), implementada localmente en `declaracion-paquete.ts`; no se importó del carril 3 (no existe aún en esta rama). Unificar en F5-A.
- Se conservaron `partidas` y `subpresupuestos` en el catálogo para no romper `FormularioCrearRdt` hasta F4-C; «sin plan aprobado no se puede crear RDT» solo se aplica en la respuesta (`estadoPlanMaestro`, `mensajePlanMaestro`); el bloqueo al crear lo implementa F4-B/C.
- Horas repartidas a partes iguales entre vínculos no derivados de una actividad (caso legado con varios); las derivadas no duplican horas.
- Las pruebas de ruta usan `vi.doMock('@/…')` porque `vitest.config.ts` no define alias.

## Mejoras de trabajo
- Heredoc de Bash con varios archivos TypeScript falló por comillas; usar Write para archivos de código.
- El clasificador denegó el script `migrar_*.py` (igual que en F2-A); la regla de permiso de Victor no se aplicó o no lo reconoce.

## Reglas de negocio detectadas
Ninguna nueva.

## Huérfanos
Ninguno.

## Llamadas
Aproximadamente 31.
