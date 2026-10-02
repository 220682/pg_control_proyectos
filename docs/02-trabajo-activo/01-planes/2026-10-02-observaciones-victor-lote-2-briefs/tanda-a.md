# Tanda A · Worker 1 — Acciones del checklist (O5) y acta fuera de la lista (O7)

Carril **1 · Checklist** · rama `local-worker-1` en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-1` (ya en `main` `ce5623e`, limpia) · puerto 3111. Lanzamiento: subagente «Worker 1 · tanda A».

Lee primero `00-contratos-comunes.md` y `00-indice-de-tandas.md`.

## Ítems de la tanda (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| A1 | `db/089_checklist_grupos.sql` (nuevo): columnas `grupo_accion` (`ARCHIVO`/`PANTALLA`, default `ARCHIVO`), `ruta_accion` (nullable), `etiqueta_accion` (nullable) en `catalogo_documentos`; `PANTALLA` en las 9 claves del Grupo B; `ruta_accion` en `cronograma`, `paquete_trabajo`, `plan_maestro`, `requerimiento`; `etiqueta_accion='Crear / Ver'` en las 7 no estructuradas (`dp`/`pr` con etiqueta nula). Aditiva, idempotente, con comentario de reversa. **La aplica tú** (protocolo en `00-contratos-comunes.md`). | SQL + lectura crítica + conteos antes/después + registro en tu resultado |
| A2 | `src/lib/checklist/acciones-checklist.ts` (nuevo, + test): función pura con la regla de render (D3), en este orden — ad-hoc (sin catálogo) → Archivo; `tipo_captura='ESTRUCTURADO'` → enlace DP/PR con sus etiquetas dinámicas actuales; `grupo_accion='ARCHIVO'` → «Seleccionar archivo»; `grupo_accion='PANTALLA'` → enlace con `etiqueta_accion ?? 'Crear / Ver'` y **botón muerto** (`title="Sin pantalla todavía"`, patrón del flujo 16) si `ruta_accion` es nula. El agregado `?proyectoId=<id>` solo para rutas reales (D4) y el gateo por permiso de su pantalla (D5: `puedeVerCronograma`, `puedeVerPaquetesTrabajo`, `puedeVerPlanMaestro`, `puedeVerStatusRequerimiento`, igual que hoy DP/PR). | `npm test` + `tsc` (los 4 caminos y las rutas) |
| A3 | `page.tsx` (`proyectos/[id]`): el select añade `fase`, `grupo_accion`, `ruta_accion`, `etiqueta_accion`; **oculta las filas de fase `CIERRE`** (filtrado en JS, conservando los ítems ad-hoc); el render delega en `acciones-checklist`; siguen `ToggleCompletado` y `SubirDocumento` para el Grupo A (y personalizados); casilla y responsable intactos en todos. | `tsc` + build + salida del `GET` del checklist como evidencia de la lista (sin navegador) |
| A4 | Gate de cierre: `confirmar-transicion/route.ts` selecciona `catalogo_documentos(fase)` y solo evalúa «checklist completo» con filas de fase ≠ `CIERRE` (o sin catálogo). **Sin tocar** el CAS de la transición ni el bootstrap. Verifica ambos sentidos con una prueba del filtrado (función pura en tu archivo o test existente): todo lo demás completo **sí** cierra; un ítem de AL_INICIO pendiente **no** cierra. **No ejecutes la transición real en PS-0006.** | Lectura crítica + prueba verde de los dos sentidos |
| A5 | `editor-checklist.tsx`: no ofrece los ítems de fase `CIERRE` (lista de catálogo y `agregarCatalogo`); el badge «Cierre» deja de verse. `checklist/route.ts` solo si hace falta filtrar en servidor. | `tsc` + build |
| A6 | `documentos/[documentoId]` (POST): rechaza la subida a ítems de `grupo_accion='PANTALLA'` con **400** y mensaje claro, siguiendo el patrón ya existente para `ESTRUCTURADO` (líneas 62–71 del archivo). | Smoke de fallo 400 (sesión en `00-contratos-comunes.md`; script temporal **fuera** del repo) + `tsc` |
| A7 | Consulta de **solo lectura** a la base: ¿hay `proyecto_documentos` de claves del Grupo B con `archivo_ruta` no nula? **Solo reportas** lo que encuentres; si los hay, **los elimina Victor** (Gate 1, Q2) — tú no borras nada. | Salida de la consulta en tu resultado |
| A8 | `npm test`, `npx tsc --noEmit`, `npm run lint` (sin deuda nueva; compara con el total de `main`), `npx next build --webpack` verdes en el carril. | Salida de comandos |

## Reglas de negocio ya resueltas (Gate 1 + Spec)

- **Grupo A (Archivo, «Seleccionar archivo»):** 2 Alcance, 3 Presupuesto, 12 Listado de personal nuevo, 13 Listado de pets (+ ítems personalizados, que suben como hoy).
- **Grupo B (Pantalla propia, enlace Crear/Ver):** 1 OT, 4 Cronograma, 5 Recursos del servicio, 6 DP, 7 Paquetes de trabajo, 8 Plan maestro, 9 PR, 10 3WLA, 11 Requerimientos. Rutas: `/cronograma`, `/paquetes-trabajo`, `/plan-maestro`, `/requerimientos` (siempre con `?proyectoId=<id>`); DP y PR conservan sus etiquetas y lógica actuales. **OT, Recursos del servicio y 3WLA: botón muerto** (sin ruta) hasta que Victor haga esas pantallas en otro plan.
- **O7:** «Acta de conformidad» y todo documento de fase `CIERRE` no aparecen en la lista ni en el editor, y no cuentan para el checklist completo. Las filas y el bootstrap **no se tocan** (ocultado, no borrado).
- La subida (POST) solo aplica a Grupo A y personalizados; el servidor rechaza el Grupo B (A6).

## Qué leer

`AGENTS.md` y `CLAUDE.md` de la app (enteros); de este plan **solo** tus ítems por ID y del Spec la sección «Grupos de acción del checklist (O5)»; flujos: `04-flujos-de-negocio/12-checklist.md`, `08-programa-portafolio-proyecto.md` y `14-accesos-y-restricciones.md` (solo la nota de «Subir documento»); `design.md` solo si necesitas el patrón de chips/enlaces (nunca entero). **No leas** el plan completo, el brief B, la evidencia ni el progreso.

## Qué puedes y qué no

- **Puedes crear/editar:** los archivos dueño de tu fila en `00-indice-de-tandas.md`, más `db/089_*.sql` y un script temporal fuera del repositorio para A6/A7.
- **No tocas:** `src/lib/checklist/checklist.ts`, `db/README.md`, `permisos.ts`/`registro-accesos.ts` (si algo exige tocarlos: **detente y devuelve la pregunta**), cualquier archivo del carril 2, flujos de negocio, estándar, plan, progreso o evidencia.

## Skills

Al empezar: lista `.claude/skills/` de `pg_control_proyectos` y comprueba que la app no tiene carpeta de Skills; anota «Skills revisados» en tu resultado (`verificar-permisos-por-rol` **no aplica**: ningún cambio de permisos). Al terminar: **usa `cerrar-tanda`** (sus pasos 1, 3 y 4 van en `resultados/A.md`).

## Criterios de salida

A1–A8 `Conforme` con su evidencia; 089 aplicada y verificada (o denuncia exacta si el clasificador la bloqueó); tests/tsc/lint/build verdes; `resultados/A.md` escrito con handoff, hallazgos de los cinco grupos y número de llamadas; commit (y push) en `local-worker-1`. Una tanda no se cierra con un ítem a medias.
