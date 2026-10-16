# Brief — Tanda B: Informes, base de datos, permisos y reglas puras

## Rol, modelo y tanda

Worker 1, Sonnet, esfuerzo medio. Tanda B, Ola 1, carril W1. Subagente «Worker 1 · B». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **B1**: `db/098_informes_supervision.sql` y una línea en `db/README.md`. Sigue la forma de `db/096`. Aditiva, reversa en comentario, RLS activado **sin política** (solo el servidor). Contenido:
  - `informes`: `id`, `proyecto_id`, `tipo` (`DIARIO`/`SEMANAL`), `formato` (`TECNICO`, `EJECUTIVO`, `FOTOGRAFICO`, `COSTOS`, `PERSONALIZADO`), `formato_usuario_id` opcional, `fecha_desde`, `fecha_hasta`, `codigo`, `version`, `estado` (`BORRADOR`/`EMITIDO`/`REEMPLAZADO`), `autor_id`, `bloques jsonb`, `foto_fija jsonb`, `emitido_en`, `emitido_por`, `reemplaza_a`, `creado_en`, `actualizado_en`. `unique (proyecto_id, codigo, version)`; checks `desde <= hasta` y tope duro de 93 días (los límites finos los valida el servidor).
  - `informes_contadores (proyecto_id, tipo) -> ultimo` y `siguiente_codigo_informe` con `insert ... on conflict do update ... returning`: **sin repetidos por carrera**. Código `{N° OT}-ID-{n}` (diario) o `-IS-{n}` (semanal).
  - `fotos_campo`: `id`, `proyecto_id`, `autor_id`, `tomada_en`, `lat`, `lng` (nulos), `wbs`/`paquete_id` (nulos), `descripcion`, `ruta_storage`, `bytes`, `informe_id`, `bloque_id` (nulos).
  - `formatos_usuario`: `id`, `dueno_id`, `nombre`, `bloques jsonb`; `unique (dueno_id, nombre)`.
  - `emitir_informe(p_id, p_usuario, p_foto_fija)`: **una transacción atómica**: valida `BORRADOR`, pasa a `EMITIDO`, guarda la foto fija y marca la versión anterior `REEMPLAZADO`.
  - **Trigger de inmutabilidad**: rechaza `update` de contenido sobre `EMITIDO`/`REEMPLAZADO` (solo permite `EMITIDO` -> `REEMPLAZADO`).
- **B2**: en `src/lib/permisos/permisos.ts`: ver informes (los 13 roles); crear, emitir y tomar foto (los 4 roles de `puedeCrearRdtEstructurado`); crear y ver `COSTOS` (`puedeVerEconomia` y crear); nueva versión de informe ajeno (administrador y jefe de proyectos); descargar (quien lo ve). Prueba unitaria por rol.
- **B3**: `src/lib/informes/tipos.ts`: **contrato congelado** (informe, bloque, formato, estado, foto, foto fija). Lo usará W3 desde la Ola 3: nómbralo con cuidado, no lo cambies después.
- **B4**: `periodo.ts`: atajos (semana en curso, anterior, últimas 2 semanas, mes anterior), validación de límites (`desde >= fecha_real_inicio`, `hasta <= hoy` en fecha Lima, `desde <= hasta`, máximo 3 meses), columnas por día (<= 10 días) o por semana, título «Informe del período» (> 7 días), cruce con semanales emitidos (se permite, devuelve `avisos`). Prueba unitaria con bordes (10/11 días, 3 meses, hoy, inicio).
- **B5**: `formatos.ts` (cinco formatos con bloques distintos y marca `soloEconomia`) y `estados.ts` (transiciones y visibilidad: borrador solo del autor, emitido congelado). Prueba: ningún formato distinto de `COSTOS` contiene bloques económicos.

Punto de corte: B1–B2 / B3–B5.

## Rama, worktree y puerto

Rama `local-worker-1`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-1` (con la Tanda A cerrada: commits `e65dcae` y `c0dd874`). Trabaja **solo** ahí. Puerto 3011 si necesitas la app. Al empezar, `git status`: si hay cambios sin commit que no sean tuyos, avísalo al Orquestador antes de seguir.

## Qué leer, y qué no

1. `db/096_rdt_borradores_e_inasistencias.sql` (forma de migración, RLS), `db/013_requerimientos.sql`, `db/README.md`.
2. `src/lib/permisos/permisos.ts` (`puedeVerEconomia`, `puedeCrearRdtEstructurado`, `puedeMedirSubcontratos`, `puedeVerInasistencias`).
3. Flujo `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/14-accesos-y-restricciones.md`.
4. En el plan, solo el Spec «Alcance» A.8 y A.16 (búscalos con Grep).

**No leas** el plan completo, maquetas ni otros flujos.

## Qué puede trabajar

Crear o editar: `db/098*`, una línea en `db/README.md`, `src/lib/informes/**` (solo `tipos.ts`, `periodo.ts`, `formatos.ts`, `estados.ts` y sus pruebas), `src/lib/permisos/permisos.ts` y su prueba.

**No toca:** `src/lib/pdf/hoja.ts`, `src/lib/rdts/**`, `api/rdts/**`, `registro-accesos.ts`, `next.config.ts`, `package.json`, `db/095*` (sin seguimiento, de otra tarea: **no lo agregues a ningún commit**), `db/099*` ni lo de la Tanda A, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica la migración** a ninguna base: solo escribe el archivo (la aplica el Orquestador).

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-1` (nunca a `main`) al cerrar B1–B2 y al cerrar B3–B5; nunca a medias de un ítem. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español, con la línea `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/B.md`, con la plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` de ese repositorio (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Primera migración libre para esta tanda: **098** (097 y 099 ya existen). Re-verifica con `ls db/` y `git log --oneline -3 main`.
- Funciones vigentes en `permisos.ts` (verificadas): `puedeVerEconomia`, `puedeCrearRdtEstructurado`, `puedeMedirSubcontratos`, `puedeVerInasistencias`.
- Guardia de escritura de las rutas futuras: `validarEscrituraProyecto` (`src/lib/auth/guard-proyecto.ts`); aquí no se crean rutas.
- Base de prueba: Victor no indicó ninguna: la migración queda «revisada, no probada en base».

## Skills que debe usar

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`: léelo y sigue su secuencia; el commit de documentación lo hace el Orquestador) y `verificar-permisos-por-rol` (`.../.claude/skills/verificar-permisos-por-rol/SKILL.md`) para contrastar B2 contra la tabla de permisos.

## Verificación

`npm test`; `npx tsc --noEmit`; `npm run lint`: tiene 9 errores y 22 avisos **preexistentes**, el criterio es no agregar errores nuevos (anota el conteo antes y después). Build: `npm run build` con Turbopack falla en los worktrees (`node_modules` es un symlink); usa `npx next build --webpack`.

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra el ítem en curso, haz commit y push y escribe el traspaso.

## Cómo registra hallazgos y preguntas

Los hallazgos van a tu resumen, en los cinco grupos. Si encuentras un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador** en tu respuesta final; no lo decidas tú.

## Criterios de salida

B1–B5 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits en `local-worker-1` comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
