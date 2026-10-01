# Resultados F4-B · RDT: API de partes (crear, validar, modo por avance del paquete)

Carril 4 · rama `local-worker-4` · commit `14bae8d`. Sin push ni merge. Sin migraciones nuevas (082-084 de F4-A, ya aplicadas; `db/053` intacta).

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada), verificar-permisos-por-rol y seguir-flujo-de-planes (no aplican: permisos sin cambio; el segundo es del Orquestador). Repo de la app: sin carpeta de Skills.

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F4B-1 | Conforme | `POST /api/rdts/partes`: sin plan aprobado 400 con mensaje (`SIN_PLAN_MAESTRO`); cada actividad D (y C/NC y `materialesClaves` si vienen) debe estar en el plan aprobado; el servidor impone el `wbs` del plan y guarda `paquete_trabajo_id`. Pruebas: válido, sin plan, fuera del plan (`partes-paquetes.test.ts`). |
| F4B-2 | Conforme | `PATCH` VALIDAR: exige plan aprobado, acepta `asignaciones` opcionales (actividad → clave) del validador, exige clave a toda actividad con descripción (D, C, NC) y reescribe `rdt_actividad_partidas` con partida + paquete (`sincronizarParte`). Prueba de vínculos e idempotencia. Limitación: los materiales son texto libre en `rdt_partes.materiales` (sin tabla), por eso solo se validan sus claves, no se persisten por separado. |
| F4B-3 | Conforme | Paquete en `AVANCE_PAQUETE`: solo se declara la guía (otra partida del paquete: 400); el servidor calcula el mismo % con `repartirDeclaracionPaquete` y guarda cada derivada como **actividad propia** (`metrado_ejecutado` = repartido, un vínculo, `es_derivada=true`, `declaracion_id` = actividad declarada, `metrado_derivado`). El cliente no puede mandar derivadas (se descartan campos extra y se rechaza declarar no-guía). Prueba espejo de 053: PR = {cama 5, exc 15, rell 15}, sin doble conteo; `agregarRealPorClave` da lo mismo por clave sin duplicar. `GET partes/[id]` no devuelve derivadas como filas editables (`filasDerivadas` aparte, solo lectura). |
| F4B-4 | Conforme | `PATCH accion=REASIGNAR_PAQUETE` (mismo permiso que validar): solo `REGISTRADO`/`REVISADO`; recalcula derivadas; revierte si falla. El PR suma por partida (prueba sobre espejo de 053; motor no editado). |
| F4B-5 | Conforme | Prueba de las funciones de permiso para los 13 roles (crear, validar/rechazar, rechazar validado, corregir) sin cambios. `npm test` 72 archivos / 709 pruebas verdes; `npx tsc --noEmit` limpio; `npx eslint src` 27 problemas (9 errores) = igual que `main`. |

## Handoff
- Para F4-C (pantalla): `POST` espera por actividad `claveReporte` (`paquete|DIRECTA:partidaId`, del catálogo F4-A) y opcional `materialesClaves[]`; `PATCH` acepta `asignaciones:[{actividadId, claveReporte}]` en VALIDAR y REASIGNAR_PAQUETE; `GET partes/[id]` añade `paquetesActividades` y `filasDerivadas`. «Met. acum.» (`metradosAcumulados` en catálogos) ya incluye las derivadas, total del servicio por partida.
- Archivos nuevos: `src/lib/rdts/partes-paquetes.ts` (lógica pura), `partes-paquetes-servidor.ts` (plan aprobado, sincronización, asignaciones), prueba `partes-paquetes.test.ts`.
- Comandos: `npx vitest run src/lib/rdts`, `npx tsc --noEmit`, `npx eslint src`.
- Pendiente de F5 (navegador/datos reales): creación real con plan aprobado; 076-078 del carril 2 deben estar aplicadas para leer `plan_maestro_partidas`.

## Decisiones técnicas (a confirmar con Victor)
- Derivadas como actividad propia (propuesta de Victor): 053 no cambia. Efecto colateral: `actividades_acum` (PPC) cuenta cada derivada como una actividad D de su partida; lo ve F5.
- Reasignar usa el permiso de validar (administrador, jefe de proyectos, jefe de oficina técnica); el supervisor que crea corrige reemplazando el parte. Si Victor quiere que el supervisor también reasigne, es cambio de permisos (tabla 2 flujo 14).
- Creación no atómica con el RPC `guardar_rdt_parte` (sin tocar la función): si falla el paso de paquete, se borra el parte recién creado. Un RDT antiguo sin paquete se valida solo si su partida está como directa en el plan aprobado.
- Al fallar una validación el historial ya registró la acción (comportamiento previo, no cambiado).

## Mejoras de trabajo
- Heredoc de Bash con archivos TypeScript vuelve a fallar por comillas: usar Write.
- En pruebas con base simulada, copiar los valores previos antes de revertir (los objetos son referencias); un bug real de reversión salió así.

## Reglas de negocio detectadas
Ninguna nueva (se aplicó el criterio de Victor del brief: real por partida en DP/PR; acumulado de paquete solo en Plan Maestro).

## Huérfanos
Ninguno.

## Llamadas
Aproximadamente 45 en total (sesión cortada y retomada).
