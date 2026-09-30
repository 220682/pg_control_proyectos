# Resultados F1-B · Niveles: datos, importación del DP y del cronograma, bloqueo de recarga

Rama `local-worker-1` (app), commit `2652116`. **Migraciones 073-075 escritas pero NO aplicadas: el sistema denegó el script (ver Handoff).**

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda, seguir-flujo-de-planes, verificar-permisos-por-rol. App: sin carpeta de Skills. Se usó `cerrar-tanda` (adaptado: estados, evidencia y traspaso en este archivo). Los otros no aplican (no hay permisos por rol ni recorrido del flujo de planes).

## Estado de los ítems
| ID | Estado | Evidencia |
|---|---|---|
| F1B-1 | Observado | `db/073` (`servicio_niveles`), `db/074` (`servicio_encabezados` + función `niveles_dp_por_defecto` + mapa por defecto pendiente para lo ya importado), `db/075` (`reemplazar_dp`, misma firma de 13 parámetros, reconstruye niveles y encabezados). Releídas críticamente; aditivas e idempotentes; `dp_subpresupuestos` y `dp_paquetes` se siguen poblando. **Observado porque aún no están aplicadas ni verificadas en la base** (denegación del sistema). |
| F1B-2 | Conforme | `leerEstructuraCD` (`src/lib/dp/parser-cd.ts`) lee encabezados de cualquier nivel; `parsearWorkbookDP` devuelve `estructura`. `parser*.test.ts` siguen verdes; `niveles-dp.test.ts`: 3 niveles produce el mismo mapa y las mismas listas que hoy (subpresupuestos `1,2`, paquete `2.1`), 4 y 5 niveles, nivel 1 = Servicio, partida directa del subpresupuesto sin marcarla error. `npm test` |
| F1B-3 | Conforme (lógica) | `POST /api/proyectos/[id]/dp`: `soloAnalizar=true` devuelve `{ propuesta: { nivelesDetectados, mapa, encabezados, filasParaRevisar } }` sin guardar; `mapaNiveles` (JSON) se valida (`validarMapaDP`: orden fijo, Servicio y Partida obligatorios, Partida en el último nivel, consecutivos) y se guarda `confirmado: true`; sin él se guarda el propuesto `confirmado: false`. Pruebas en `niveles-dp.test.ts`. **Limitación:** `vitest.config.ts` no tiene alias `@/` (archivo congelado), así que no hay prueba que ejecute el `route.ts` completo; la lógica está en funciones puras probadas (`proponerNivelesDP`, `resolverMapaDP`, `construirParametroEstructura`). La ruta queda Observado en vivo hasta F5. |
| F1B-4 | Conforme (lógica) | `src/lib/cronograma/niveles.ts` (roles propios Servicio/Área/Fase/Actividad resumen/Tarea; mapa pendiente o confirmado por `mapaNiveles`; se guardan en `servicio_niveles` y `servicio_encabezados` con origen `CRONOGRAMA`, y en `informe.niveles`). Enlace por EDT y `recalcular_pr_fechas_base` intactos. `PATCH /api/cronograma`: acepta vínculos sin metrado; si viene, >0; se eliminó el 100 % por partida (`hayVinculoInvalido` en `vinculos.ts`, probado). `sumarMetradoPorPartida` y `partidasConMetradoIncompleto` se conservan (ya sin uso en la ruta; F3 las puede reutilizar). Mismo límite de prueba de ruta que F1B-3. |
| F1B-5 | Conforme (lógica) | `src/lib/proyectos/bloqueo-recarga.ts`: `evaluarRecarga` (contrato C1) y `decidirRecarga`. Usado en `POST` del DP y `POST` del cronograma. Tres casos probados con cliente simulado: plan APROBADO → 409 sin confirmar (`bloqueadoPorPlanAprobado`); sin aprobado y con algo que perder → 409 `requiereConfirmacion` con la lista, pasa con `confirmarPerdida=true`; borrador no bloquea. Sin nada que perder, carga libre. **Por verificar en vivo:** la consulta de vínculos usa un `select` con unión `cronograma_actividades!inner(proyecto_id)` de PostgREST (no se pudo probar sin la base). |
| F1B-6 | Conforme | Las guardias de rol (`puedeImportarDp`, `puedeSubirCronograma`), de alcance (`exigirAlcance`) y de servicio inexistente no se tocaron. `npm test`: 75 archivos, 723 pruebas verdes. `npx tsc --noEmit`: limpio. Lint del worktree: 27 problemas (9 errores, 18 avisos) = igual que `main`; 0 en los archivos nuevos. |

## Verificación
- `VITE_CONFIG_NATIVE_IGNORE_WARNING=true npx vitest run` (Bash): 75 archivos, 723 pruebas verdes (698 previas + 25 nuevas).
- `npx tsc --noEmit`: sin salida. `npx eslint .` en el worktree: 27 problemas, igual que la base.

## Handoff (máx. 15 líneas)
1. **Migraciones 073-075 sin aplicar.** Al lanzar `python ...\scratchpad\migrar_F1-B.py` el clasificador del sistema respondió «Credential Exploration» y denegó. No lo rodeé. Se borró el candado que había creado (no apliqué nada). El script queda listo, fuera del repositorio.
2. Comando exacto: `python "C:/Users/BRANDY/AppData/Local/Temp/claude/D--VICTOR-CLAUDE-CODE-pg-control-proyectos/3a959253-7780-4b11-9071-ae185aa5ef45/scratchpad/migrar_F1-B.py"` (Victor lo aprueba o lo corre con el prefijo `!`). Antes crear el candado: `cd "D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/resultados" && (set -o noclobber; echo "F1-B $(date +%H:%M)" > CANDADO-MIGRACIONES.txt)` y borrarlo al terminar.
3. El script lee `PR_DB_URL` de `entorno_variable.txt` dentro del proceso (sin imprimirla), aplica 073, 074 y 075 cada una en su transacción, e imprime: `select 1`, conteos de 8 tablas antes y después, número de firmas de `reemplazar_dp` (debe ser 1, `pronargs` 13), existencia de tablas y función, y cuántos servicios recibieron el mapa por defecto. No imprime credenciales. Hay que borrarlo al terminar.
4. **Orden crítico:** el código de esta rama llama a `reemplazar_dp` con el objeto nuevo en `p_subpresupuestos`; sin 075 aplicada, importar un DP falla. No desplegar ni probar la importación antes de aplicar las tres.
5. El backfill de 074 escribe filas nuevas en las tablas nuevas para cada servicio con DP de profundidad 2 o 3; no cambia ningún dato existente. Con profundidad distinta queda sin mapa (se propone al reimportar).
6. Decisión técnica: para no cambiar la firma de 13 parámetros, `p_subpresupuestos` admite arreglo (forma histórica) u objeto `{subpresupuestos, paquetes, niveles, encabezados, confirmado}`. F1-C debe enviar desde pantalla: `soloAnalizar`, `mapaNiveles`, `confirmarPerdida` (DP y cronograma).
7. Cuerpos 409 para F1-C: `bloqueadoPorPlanAprobado: true` (sin confirmar) o `requiereConfirmacion: true` con `perderia {vinculos, paquetes, planMaestroBorrador}`. El 409 de conciliación del DP (`pendienteConciliacion`) es distinto; al reenviar con resoluciones hay que reenviar también `confirmarPerdida`.
8. Pendiente en vivo (F5): `evaluarRecarga` (unión PostgREST) y los dos `POST`.

## Mejoras de trabajo
- El clasificador de permisos bloquea los scripts `migrar_*.py` aunque el protocolo los autorice; conviene que Victor compruebe la regla de permiso antes de lanzar Workers con migraciones.
- `vitest.config.ts` sin alias `@/` impide probar rutas de API: sacar la lógica a funciones puras de `src/lib` fue la vía.
- Los heredocs largos con `'EOF'` en Bash fallaron dos veces por el analizador de comandos; usar la herramienta Write para los archivos.

## Reglas de negocio acordadas en esta tarea
Ninguna nueva. Interpretación aplicada (a confirmar en F5-D): el aviso de pérdida solo se exige si hay algo que perder; la lista de lo que se perdería es la misma para DP y cronograma.

## Carpetas/archivos huérfanos
Ninguno nuevo. `sumarMetradoPorPartida` y `partidasConMetradoIncompleto` (`src/lib/cronograma/vinculos.ts`) quedaron sin uso en la ruta; se conservan con sus pruebas.

## Llamadas
Aprox. 40.
