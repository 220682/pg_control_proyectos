# Brief — Tanda D: Informes, API

## Rol, modelo y tanda

Worker 1, Sonnet, esfuerzo medio. Tanda D, Ola 2, carril W1 (después de C). Subagente «Worker 1 · D». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **D1**: `GET/POST /api/proyectos/[id]/informes`. GET: emitidos y reemplazados de todos más borradores **propios**; los de formato `COSTOS` solo con `puedeVerInformeCostos`; filtros tipo, estado, autor, fecha. POST: crear con período; copia «Restricciones y pendientes» y «Próximas actividades» del último emitido; `COSTOS` sin economía = 403. Código con `siguiente_codigo_informe(p_proyecto, p_tipo, p_ot)`: **recibe el N° OT** (P31); léelo del servicio y verifica el nombre real con `grep` en `db/098` y en el proyecto.
- **D2**: `GET/PATCH/DELETE informes/[informeId]`. Borrador ajeno = 404; PATCH guarda bloques o cambia el período (mismas validaciones de `periodo.ts`); PATCH sobre `EMITIDO` = 409; DELETE solo borrador propio; `COSTOS` sin economía = 403.
- **D3**: `POST informes/[informeId]/emitir` (arma la foto fija con `congelar.ts` de la tanda C y llama a la RPC `emitir_informe`) y `POST .../nueva-version` (borrador versión +1 desde un emitido; autor, administrador, jefe de proyectos). Al emitir, notificación tipo `MENSAJE` a los miembros del servicio menos el autor (R9; sin cambiar el check de `db/012`), visible en `/notificaciones`: usa los helpers de `src/lib/notificaciones/`.
- **D4**: `GET/POST informes/formatos-usuario` (cada usuario sobre lo suyo; un formato con bloques de Costos no se crea ni se usa sin economía).
- **D5**: `fotos-campo`: `POST` (JPEG por sus primeros bytes, tope 3 MB, descripción obligatoria, GPS opcional válido, `wbs` debe pertenecer al servicio), `GET ?fecha=` (banco del día), `PATCH/GET/DELETE fotos-campo/[fotoId]` (asignar a bloque de borrador propio; GET devuelve URL firmada de 60 s tras comprobar permisos; DELETE solo foto propia sin informe emitido). Se guardan en el bucket `documentos-proyecto`, ruta `informes/{proyectoId}/fotos/{uuid}.jpg`, con `admin.storage` (sin bucket nuevo).
- **D6**: campo `avisos` de la respuesta: semanal que se cruza con otro emitido (se permite) y días sin diario.
- **D7**: pruebas de ruta: 401, 403 por rol, 404 de borrador ajeno, 409 al editar un emitido, 400 de período fuera de límites **por llamada directa**, 403 de `COSTOS`. **Es obligatorio leer y aplicar el Skill** `verificar-permisos-por-rol` (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/verificar-permisos-por-rol/SKILL.md`) y entregar su **tabla esperado contra observado** para los 13 roles. Si no se puede suplantar en vivo porque las migraciones (098 a 102) no están aplicadas, la tabla se arma con **pruebas de ruta por rol** (rutas con la sesión simulada) y queda «Observado» para la tanda L.

Punto de corte: D1–D4 / D5–D7.

## Rama, worktree y puerto

Rama `local-worker-1`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-1`, continuando tras C (verifica con `git log --oneline -5` que C está). Trabaja solo ahí. Puerto 3011 si levantas la app.

## Qué leer, y qué no

1. `src/lib/informes/tipos.ts` (**contrato congelado**), `periodo.ts`, `formatos.ts`, `estados.ts`, lo de C (`congelar.ts`, `armar-datos-*.ts`) y `db/098_informes_supervision.sql`.
2. `src/lib/auth/guard-proyecto.ts` (`validarEscrituraProyecto`), `src/lib/permisos/permisos.ts` (`puedeVerInformes`, `puedeCrearInforme`, `puedeEmitirInforme`, `puedeTomarFotoCampo`, `puedeCrearInformeCostos`, `puedeEmitirInformeCostos`, `puedeVerInformeCostos`, `puedeNuevaVersionInformeAjeno`, `puedeDescargarInforme`), `src/lib/notificaciones/`, y una ruta existente con `admin.storage` (RDT) como patrón.
3. Flujo `14-accesos-y-restricciones.md` en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`.

**Crear y emitir `COSTOS` = `puedeCrearInformeCostos` / `puedeEmitirInformeCostos`: los 5 roles con economía** (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos, jefe de costos); no los restrinjas a 3 (P30). **No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `src/app/api/proyectos/[id]/informes/**`, `src/app/api/proyectos/[id]/fotos-campo/**`, `src/lib/informes/**` (menos `tipos.ts`) y sus pruebas.

**No toca:** `src/lib/informes/tipos.ts`, `db/**`, `db/095*` (sin seguimiento: no lo agregues a ningún commit), `permisos.ts` salvo que falte una función (entonces pregunta), `next.config.ts`, `package.json`, `src/lib/rdts/**`, `api/rdts/**`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.** Toda ruta valida en servidor: sesión, rol y alcance sobre el servicio.

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-1` (nunca a `main`) al cerrar D1–D4 y al cerrar D5–D7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/D.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos) e incluye la tabla del Skill. No hagas commit en el repositorio de documentación.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador) y `verificar-permisos-por-rol` (obligatorio). Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees por el symlink de `node_modules`). `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

D1–D7 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen con la tabla de permisos. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
