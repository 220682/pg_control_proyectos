# 2026-10-02 — Plan: lote 2 — acciones del checklist (O5), importación de cronograma (O6) y acta de conformidad (O7)

> Plan del **Planner** sobre el Spec aprobado [`2026-10-02-observaciones-victor.md`](2026-10-02-observaciones-victor.md) (Gate Spec: aprobado por Victor, 2026-10-02). Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. **2 Workers** con propiedad de archivos disjunta. Briefs por tanda en `2026-10-02-observaciones-victor-lote-2-briefs/` (se crea al lanzar la Fase A).

## Identificación y estado

- Tema: Lote 2 de observaciones de Victor — (O5) acción por grupo en cada fila del checklist, (O6) importación de cronograma de punta a punta con mensaje de error específico, (O7) «Acta de conformidad» fuera de la lista.
- Fecha: 2026-10-02.
- Estado: **Cerrada** — fases A, B, C y D completas; Gate 2 aprobado; merge a `main` y push hechos (2026-10-02).

Puertas:

- Gate Spec: `aprobado por Victor (2026-10-02)`
- Gate 1: `aprobado por Victor (2026-10-02)` — respuestas completas abajo
- Gate 2: `aprobado por Victor (2026-10-02)` — autoriza el merge de ambos carriles, el mensaje de cierre y la actualización de índices

## Referencia al Spec aprobado

| Spec | Estado |
|---|---|
| [`2026-10-02-observaciones-victor.md`](2026-10-02-observaciones-victor.md) | Aprobado (Gate Spec, 2026-10-02) — filas O5, O6, O7 y sección «Grupos de acción del checklist (O5)» |

## Objetivo, alcance y no alcance

- **Resultado esperado:** ver «Resultado esperado (Lote 2)» del Spec (O5, O6, O7).
- **Alcance:** O5, O6, O7.
- **No alcance:** construir las pantallas de OT, Recursos del servicio y 3WLA (botones muertos hasta que Victor las haga en otro plan); generación automática de «Recursos del servicio» desde el DP; fusión de chips; permisos por rol (ninguna observación cambia la matriz); cualquier observación futura.
- **Validación esperada:** vitest, `tsc`, lint, build, **smoke real de importación de cronograma con éxito y con fallo** (lo que faltó en el Lote 1), navegación manual de Victor.

## Entorno, repositorios, ramas y worktrees

- Modo: local. Documentación en `pg_control_proyectos` (`main`, directo). Código en `py_control_proyectos_web`.
- **Verificado (2026-10-02):** docs: `main` = `origin/main` (`3577f53`), 0/0; único cambio pendiente sin commitear: `docs/06-material-de-apoyo/Informacion para pruebas/PPTO-prueba N°01.xlsx` (deuda del Lote 1, ver Gate 1 (i)). Código: `main` = `origin/main` = `ce5623e`, árbol limpio; `local-worker-1` = `ce5623e` (igual que `main`), `local-worker-2` = `9ad0640` (3 commits detrás), `local-worker-3`/`local-worker-4` atrás y limpias (sin usar; limpieza propuesta en planes futuros).
- **2 carriles** (ramas/worktrees existentes, sin crear infraestructura — fast-forward de `local-worker-2` pendiente de autorización, Gate 1 (iv)):

| Carril | Rama | Worktree | Observaciones |
|---|---|---|---|
| 1 · Checklist (O5 + O7) | `local-worker-1` | `.worktrees/local-worker-1` | Ya está en `main` |
| 2 · Cronograma (O6) | `local-worker-2` | `.worktrees/local-worker-2` | Sync a `main` antes de arrancar |

- Merge a `main` **solo tras el Gate 2** (lo hace el Orquestador vía Worker git).
- Protocolo de migraciones aplicable (copia en `2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-protocolo-migraciones.md`, autorizado por Victor 2026-09-30): la `089` es aditiva e idempotente; se aplica de una en una con candado; si el clasificador deniega el script, **no se rodea**: se deja listo, se anota el comando exacto y se marca «pendiente de aplicar» (aprendizaje [`2026-10-01-clasificador-bloquea-scripts-de-migracion.md`](../../03-aprendizaje-continuo/2026-10-01-clasificador-bloquea-scripts-de-migracion.md)).

## Skills aplicables

Skills de `.claude/skills/` de `pg_control_proyectos` (el repo de código no tiene carpeta de Skills):

| Skill | Quién | Dónde |
|---|---|---|
| `seguir-flujo-de-planes` | Orquestador | Al lanzar cada carril y antes del mensaje de cierre |
| `cerrar-tanda` | Worker | Al final de cada tanda (A y B) |
| `trasladar-hallazgos` | Documentador | Tanda final (traslado de hallazgos) |
| `verificar-permisos-por-rol` | — | **No aplica**: ninguna observación cambia permisos por rol ni la matriz; O5 solo consume los `puedeVer*` ya existentes. Si en la implementación aparece un cambio en `permisos.ts` o `registro-accesos.ts`, se detiene y se registra como observación para consultar a Victor antes de tocarlo. |

## Fases y dependencias

| Fase | Qué | Worker | Depende de |
|---|---|---|---|
| A | Migración `089` + acciones del checklist (O5) + acta fuera de la lista (O7) | Worker 1 | — |
| B | Diagnóstico, corrección y smoke de importación de cronograma (O6) | Worker 2 | — |
| C | Integración (`db/README.md`, verificación cruzada, merge) | Orquestador/Worker git | A, B (tras Gate 2) |
| D | Documentación (flujos 12, 15 y 08, deuda del Lote 1, traslado de hallazgos) | Documentador | A, B |

A y B son independientes (matriz de propiedad disjunta): corren en paralelo.

## Matriz de propiedad de archivos

| Archivo | Worker 1 (checklist) | Worker 2 (cronograma) |
|---|---|---|
| `db/089_checklist_grupos.sql` (nuevo) | Dueño | — |
| `src/app/(workspace)/proyectos/[id]/page.tsx` | Dueño | — |
| `src/lib/checklist/acciones-checklist.ts` (nuevo, + test) | Dueño | — |
| `src/app/(workspace)/proyectos/[id]/checklist/editar/editor-checklist.tsx` | Dueño | — |
| `src/app/api/proyectos/[id]/checklist/route.ts` | Dueño (solo si hace falta filtrar en servidor) | — |
| `src/app/api/proyectos/[id]/documentos/[documentoId]/route.ts` | Dueño | — |
| `src/app/api/proyectos/[id]/confirmar-transicion/route.ts` | Dueño | — |
| `src/app/api/cronograma/route.ts` | — | Dueño |
| `src/lib/cronograma/*` (parsers, solo si la causa raíz lo exige) | — | Dueño |
| `src/lib/errores/traducir-error.ts` (+ test nuevo) | — | Dueño |
| `src/components/ui/FormularioCronograma.tsx` | — | Dueño |
| `scripts/smoke-cronograma.mjs` (nuevo, fuera de `src/`) | — | Dueño |
| `db/README.md` | — (integración C) | — (integración C) |

**Sin archivos compartidos entre carriles.** `src/lib/checklist/checklist.ts` **no se toca** (`checklistCompleto` conserva su contrato; el filtro de fase se hace en quien lo llama). `db/README.md` lo actualiza la integración (C), no los Workers.

## Equipo del plan

| Rol | Modelo | Sesión/tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|
| Orquestador | Sonnet | esta sesión | `main` (docs) | N/A | Activo |
| Planner | Sonnet | este plan | `main` (docs) | N/A | Plan entregado |
| Worker 1 | Sonnet | tanda A | `local-worker-1` | `.worktrees/local-worker-1` | Tanda A en curso |
| Worker 2 | Sonnet | tanda B | `local-worker-2` | `.worktrees/local-worker-2` | Tanda B en curso |
| Documentador | Sonnet | tanda final | `main` (docs) | N/A | Pendiente |
| Worker git | Haiku | a pedido | opera sobre las demás | — | Pendiente |
| Auditor | Sonnet | | `main` (docs) | N/A | Pendiente |

### Brief de cada Worker

Los briefs viven en [`2026-10-02-observaciones-victor-lote-2-briefs/`](2026-10-02-observaciones-victor-lote-2-briefs/) (plantilla `13-brief-de-tanda.md`), uno por tanda (A y B), con su `resultados/<tanda>.md`.

### Prompt del Auditor

> Audita el Lote 2 del plan `2026-10-02-observaciones-victor-lote-2` (O5, O6, O7) contra el Spec `2026-10-02-observaciones-victor.md`. Revisa: (a) que cada fila del checklist muestre la acción de su grupo según la tabla del Spec («Seleccionar archivo» solo en los 4 ítems del Grupo A; enlace Crear/Ver en los 9 del Grupo B; botones muertos con título «Sin pantalla todavía» en OT, Recursos y 3WLA; casilla y responsable intactos en todos); (b) que «Acta de conformidad» no aparezca en la lista ni en el editor y que el gate de cierre siga exigiendo todo lo demás (sin falsos positivos de «checklist completo»); (c) que la importación de cronograma tenga **evidencia de smoke real con éxito y con fallo** (salidas del script, mensaje específico en pantalla y log en servidor), no solo tests; (d) que la `089` sea aditiva, idempotente y documentada en `db/README.md`; (e) trazabilidad de la tabla de flujos del Gate 1 y del libro de hallazgos. Formato: `06-informe-auditoria.md` en `02-trabajo-activo/04-auditoria/`.

## Archivos / componentes afectados

Ver «Matriz de propiedad». Nuevo: `db/089_checklist_grupos.sql`, `src/lib/checklist/acciones-checklist.ts` (+ test), `src/lib/errores/traducir-error.test.ts` (si no existe), `scripts/smoke-cronograma.mjs`. Fuentes de verdad que se actualizan en la Fase D: `04-flujos-de-negocio/12-checklist.md`, `15-cronograma.md`, `08-programa-portafolio-proyecto.md` (y `14-accesos-y-restricciones.md` solo si Victor lo aprueba en el Gate 1).

## Decisiones de diseño del Planner (delegadas por el Spec)

| # | Decisión | Por qué |
|---|---|---|
| D1 | **O5 por columnas en `catalogo_documentos`** (opción i del Spec): `grupo_accion` (`ARCHIVO`/`PANTALLA`, default `ARCHIVO`), `ruta_accion` (nullable) y `etiqueta_accion` (nullable), sembradas por clave en la migración `089`. | La columna es la fuente de verdad: mover un ítem de grupo no toca código. |
| D2 | **O7 por ocultado, sin migración destructiva** (Opción A): el `page.tsx` y el editor dejan de mostrar los ítems de fase `CIERRE`; `confirmar-transicion` excluye esas filas del «checklist completo»; las filas existentes se conservan y el bootstrap de CIERRE **no se toca**. | Mantiene los datos, es reversible y no toca el flujo con CAS/revert de la transición. La opción alternativa (borrar filas y catálogo) es destructiva y necesitaría autorización expresa. |
| D3 | **Regla de render** en `acciones-checklist.ts`, en este orden: ad-hoc (sin catálogo) → Archivo; `tipo_captura='ESTRUCTURADO'` → enlace DP/PR con las etiquetas dinámicas actuales; `grupo_accion='ARCHIVO'` → «Seleccionar archivo»; `grupo_accion='PANTALLA'` → enlace con `etiqueta_accion ?? 'Crear / Ver'`, y **botón muerto** (`title="Sin pantalla todavía"`, patrón del flujo 16) si `ruta_accion` es nula. | Conserva la casilla y el responsable de todos los ítems (O3/D2) y la lógica viva de DP/PR. |
| D4 | **Los enlaces del Grupo B llevan `?proyectoId=<id>`** en las cuatro pantallas (`/cronograma`, `/paquetes-trabajo`, `/plan-maestro`, `/requerimientos`). | Las cuatro leen `proyectoId` del query y, sin él, rebotan a `/mi-entorno`. El Spec muestra la ruta base; el plan añade el parámetro. |
| D5 | **Cada enlace del Grupo B se gatea por el permiso de su pantalla** (`puedeVerCronograma`, `puedeVerPaquetesTrabajo`, `puedeVerPlanMaestro`, `puedeVerStatusRequerimiento`) y por el alcance por OT, igual que hoy DP/PR (flujo 14). | «Solo a quien la pantalla no va a rechazar»: ya es el criterio del propio `page.tsx`. |

## Punch List embebida

Formato `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. Evidencia en el archivo homónimo.

### Worker 1 — Checklist (O5 + O7)

| ID | Ítem | Evidencia mínima | Estado |
|---|---|---|---|
| A1 | Migración `db/089_checklist_grupos.sql`: `grupo_accion`, `ruta_accion`, `etiqueta_accion` en `catalogo_documentos`; `grupo_accion='PANTALLA'` en las 9 claves del Grupo B; `ruta_accion` en `cronograma`, `paquete_trabajo`, `plan_maestro`, `requerimiento`; `etiqueta_accion='Crear / Ver'` en las 7 no estructuradas (`dp`/`pr` quedan con `etiqueta_accion` nula). Aditiva, idempotente, con comentario de reversa. | SQL + lectura crítica + conteo de filas por clave antes/después | Conforme (089 aplicada y verificada: 14/7/1, 9 PANTALLA, 4 rutas, 7 etiquetas) |
| A2 | `acciones-checklist.ts`: función pura con la regla D3 y el mapa de permisos D4/D5 (incluye el agregado `?proyectoId=`); prueba unitaria de los cuatro caminos y de las rutas. | `npm test` + `tsc` | Conforme (tests verdes) |
| A3 | `page.tsx`: el select añade `fase`, `grupo_accion`, `ruta_accion`, `etiqueta_accion`; **oculta las filas de fase `CIERRE`** (filtrado en JS, conservando los ítems ad-hoc); el render delega en `acciones-checklist`; se conservan `ToggleCompletado` y `SubirDocumento` para el Grupo A. | `tsc` + build + captura de la lista | Conforme (SSR de `/proyectos/[id]` con 9 comprobaciones OK) |
| A4 | O7 en el gate de cierre: `confirmar-transicion/route.ts` selecciona `catalogo_documentos(fase)` y solo evalúa para «checklist completo» las filas con fase ≠ `CIERRE` (o sin catálogo). **Sin tocar** el CAS de la transición ni el bootstrap. | Lectura crítica + prueba/verificación de que un proyecto con todo lo demás completo **sí** cierra y con un ítem de AL_INICIO pendiente **no** cierra | Conforme (prueba de ambos sentidos verde; sin transición real) |
| A5 | `editor-checklist.tsx`: no ofrece los ítems de fase `CIERRE` (lista de catálogo y `agregarCatalogo`); el badge «Cierre» deja de ser visible. `checklist/route.ts` solo si hace falta filtrar en servidor. | `tsc` + build + captura | Conforme (editor con 0 ítems de CIERRE existiendo `acta_conformidad`; ocultado, no borrado) |
| A6 | `documentos/[documentoId]` (POST): rechaza la subida a ítems de `grupo_accion='PANTALLA'` con 400 y mensaje claro, siguiendo el patrón ya existente para `ESTRUCTURADO` (líneas 62–71). | Smoke con fallo 400 + `tsc` | Conforme (400 con mensaje claro; Grupo A sin bloquearse) |
| A7 | Comprobación de datos: consulta de **solo lectura** para ver si hay ítems del Grupo B con `archivo_ruta` no nula (archivos ya subidos que quedarían sin acceso desde la lista). Si los hay, **se reportan y los elimina Victor** (Gate 1, Q2); el Worker no borra nada. | Salida de la consulta | Conforme (**0 filas**: no hay archivos que eliminar) |
| A8 | `npm test`, `npx tsc --noEmit`, `npm run lint`, `npm run build` verdes en el carril. | Salida de comandos | Conforme (100 archivos/1043 tests OK · tsc exit 0 · lint 27 = baseline · build exit 0) |

### Worker 2 — Cronograma (O6)

| ID | Ítem | Evidencia mínima | Estado |
|---|---|---|---|
| B1 | Reproducir el fallo: `scripts/smoke-cronograma.mjs` (fuera de `src/`) contra `npm run dev` local, con `soloAnalizar=true` y **cada archivo de prueba** (`CRON-PROMCOSER-AESA-001.pdf` y `Cron-prueba N°01.xlsx`); registra el cuerpo HTTP y el **string exacto** que vería Victor en pantalla. | Salida completa del script | Conforme (200 con propuesta completa en ambos; variantes inválidas imprimen la pantalla real con `traducirErrorApi`) |
| B2 | Aislar la causa raíz: carga del XLSX real con `exceljs` → `parsearExcelCronograma(hoja)`, y del PDF real con `PDFParse.getText()` → `parsearTextoPdfCronograma(texto)` (el camino que hoy solo se prueba con el fixture `.txt`); comparar con los tests verdes actuales. Diagnóstico escrito (formato, fase y mensaje del fallo). | Diagnóstico + salida | Conforme (parsers sanos: 14 y 78 act.; fallo en 3 fases ajenas al parser — sesión caducada, prefijo técnico, 500 por uuid) |
| B3 | Corregir la causa raíz en la ruta de importación (`api/cronograma/route.ts` y/o `lib/cronograma/*`). | Diff + tests | Conforme (uuid validado → 400; prefijo técnico quitado en `traducir-error.ts`; respuesta no JSON detectada en el formulario) |
| B4 | Loguear en servidor **todos** los caminos de fallo de la importación (hoy solo el `catch` de lectura, línea 314) con formato, nombre del archivo y mensaje. | Salida del log en la prueba de fallo | Conforme (`logFalloImportacion` en 17 caminos + 2 `catch`; salida real en `resultados/B.md`) |
| B5 | Mensaje específico en pantalla: `traducir-error.ts` deja de devolver el fallback genérico para mensajes que ya traen motivo (quitar el prefijo técnico `Error: …` y conservar el resto) y `FormularioCronograma.tsx` pasa su fallback real en las líneas 133 y 164 (hoy el `??` es código muerto). Prueba unitaria de `traducirErrorApi`. | `npm test` + smoke de fallo mostrando el motivo | Conforme (test nuevo `traducir-error.test.ts` 4/4; smokes muestran motivo específico) |
| B6 | Smoke de **éxito de punta a punta** (análisis + guardado) con los dos archivos sobre un proyecto de prueba, verificando el informe de extracción; y smoke de **fallo** (archivo inválido) con motivo específico en pantalla y log en servidor. | Salidas de ambos smokes (contadores de actividades) | Conforme (éxito XLSX 14 act. y PDF 78 act. con persistencia verificada; 6 fallos con motivo + log; sobre **PS-0007** creado por el Worker — R7) |
| B7 | `npm test`, `npx tsc --noEmit`, `npm run lint`, `npm run build` verdes en el carril. | Salida de comandos | Conforme (100 archivos/1030 tests OK · tsc exit 0 · lint 27 = baseline, 0 en archivos propios · build `EXIT=0`) |

### Integración y documentación

| ID | Ítem | Evidencia mínima | Estado |
|---|---|---|---|
| C1 | `db/README.md` con la fila `089`; ramas integradas sin conflictos; `git status` limpio. | Diff + git status | Conforme (fila `089` en `db/README.md`; `local-worker-1` mergeada con `b9d0e2b` y `local-worker-2` con `5e8420b`; `main` = `origin/main` = `5e8420b`, `0/0`, árbol limpio) |
| D1 | Índice de `01-planes/README.md`: fila del Lote 2 («En ejecución») y, al cerrar, su estado final. | Diff | Conforme (fila del Lote 2 en `7100179`; estado final «Cerrada» y fila del Lote 1 corregida en la tanda de cierre) |
| D2 | Flujos `12-checklist.md` (grupos de acción + acta fuera de la lista + «subir» solo Grupo A), `15-cronograma.md` (regla de mensaje específico y log) y `08-programa-portafolio-proyecto.md` (qué es «checklist completo» para cerrar) según la tabla del Gate 1; índices actualizados. `14-accesos-y-restricciones.md` + artefacto «Matriz de permisos» **solo** si Victor lo aprueba. | Diff + casilla «aplicado» | Conforme (flujos 12, 08, 15 y 14 + índice, commit `7100179`; el artefacto «Matriz de permisos» lo edita Victor) |
| D3 | **Deuda documental del Lote 1:** crear `02-progreso/2026-10-02-observaciones-victor.md` y `03-evidencia/2026-10-02-observaciones-victor.md` con su contenido real (estado, commits, SQL aplicados por Victor, decisiones) y la nota de que el smoke de O4 nunca se hizo y su evidencia vive ahora en la homónima del Lote 2. | Dos archivos nuevos + diff | Conforme (dos archivos creados con contenido real, commit `7100179`) |
| D4 | Trasladar el libro de hallazgos a su destino; `python scripts/verificar-referencias.py` sin referencias rotas (incluidos los enlaces a los homónimos del Lote 1 y al mapa de briefs). | Salida del verificador | Conforme (MB1–MB3 → [`2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md`](../../03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md) + fila en su índice, commit `903033e`; RB1–RB4 → flujos 12/08/15, commit `7100179`; verificador por defecto: 44 archivos, 0 huérfanos, 0 enlaces rotos, exit 0; alcance Lote 2 (plan + briefs + homónimos): 0/0, exit 0; alcance `03-aprendizaje-continuo`: 0/0) |

## Riesgos y bloqueos

| # | Riesgo | Mitigación |
|---|---|---|
| R1 | La causa raíz de O6 sigue desconocida (el commit `9ad0640` solo añadió detección de formato, `console.error` y mensaje; los parsers no cambiaron y el éxito end-to-end nunca se verificó) | B1 reproduce antes de tocar nada; B2 aísla el camino (exceljs vs `PDFParse`) sin depender del fixture `.txt`; B3 corrige; B6 cierra con evidencia |
| R2 | El cambio del gate de cierre (A4) podría cerrar un proyecto con el checklist incompleto o, al revés, bloquear cierres | Filtrar **solo** fase `CIERRE`; prueba explícita en ambos sentidos; no tocar CAS ni bootstrap |
| R3 | Archivos ya subidos a ítems del Grupo B quedan sin acceso desde la lista | A7 consulta de solo lectura + consulta a Victor antes de ocultarlos |
| R4 | `local-worker-2` está 3 commits detrás de `main` | Fast-forward autorizado en el Gate 1 (iv) antes de arrancar la Fase B |
| R5 | El clasificador puede denegar la aplicación de la `089` | Protocolo de migraciones: si se deniega, SQL listo + comando exacto anotado + «pendiente de aplicar»; no se rodea la regla |
| R6 | Smoke local ≠ Vercel (Victor probó en la app desplegada) | Evidencia local obligatoria (B6) + verificación final de Victor en producción tras el push, como punto del mensaje de cierre |
| R7 | El smoke necesita un proyecto de prueba **sin Plan Maestro aprobado y sin cronograma previo**, o el bloqueo de recarga lo frena | Se especifica en el Gate 1 (i); si no existe, se crea con el rol adecuado |

## Consultas para el Gate 1

Además de los cuatro bloques estándar de más abajo, el Planner deja estas consultas:

| # | Consulta | Por qué importa |
|---|---|---|
| Q1 | ¿Existe un **proyecto de prueba** para O5/O7 (y para el smoke de O6, sin Plan Maestro aprobado)? ¿Se crea uno nuevo o se usa uno existente? | El smoke y las capturas no pueden tocar datos reales |
| Q2 | Si A7 encuentra archivos ya subidos a ítems del Grupo B: ¿mostrar además un enlace «Ver archivo subido» junto al del módulo, o ignorarlos? | Decide si la Fase A oculta el acceso a esos archivos |
| Q3 | ¿Quién aplica la `089` en Supabase (Victor, como en el Lote 1, o el Worker con las credenciales ya autorizadas)? | Sin ella, A1/A3 no tienen efecto |
| Q4 | Si se aprueba la fila 3 de la tabla de flujos: ¿quién actualiza el artefacto «Matriz de permisos» (solo Victor puede editarlo)? | Política de AGENTS.md: artefacto y flujo 14 se actualizan en la misma tarea |

## Gate 1 — respuestas de Victor (2026-10-02)

**Aprobación general:** plan + Punch List + decisiones D1–D5 **aprobados**; implementación autorizada sin aprobaciones intermedias hasta el Gate 2.

### (i) Datos de prueba

- Archivos de cronograma confirmados: `CRON-PROMCOSER-AESA-001.pdf` y `Cron-prueba N°01.xlsx` (los del Lote 1). Confirmados además `PPTO-prueba N°01.xlsx` (adjuntado por Victor).
- **Q1 (proyecto de prueba):** se usa el proyecto existente señalado por Victor — **`PS-0006` — «PRUEBA-F5B Servicio de verificacion»** — para capturas de O5/O7 y el smoke de O6.
- **Deuda del Lote 1:** `PPTO-prueba N°01.xlsx` → **commitear** (decisión de Victor).

### (ii) Pre-autorizaciones — **autorizadas en bloque**

- `npm run dev` local (worktrees y repo raíz) con `.env.local` (copiar al worktree si falta).
- `npm test`, `npx tsc --noEmit`, `npm run lint`, `npm run build` en los dos carriles.
- Credenciales de prueba para el login del smoke, sin mostrar ni copiar ningún secreto.
- Script nuevo `scripts/smoke-cronograma.mjs` (fuera de `src/`).
- Consulta de solo lectura a la base para A7.
- Playwright **no** se usa (si hiciera falta, se pide aparte).

### (iii) Tabla de reglas escritas — **aprobada en su totalidad** (filas 1–5)

- Fila 3 (`14-accesos-y-restricciones.md` + artefacto «Matriz de permisos»): **aprobada**. El Documentador actualiza el flujo 14; **el artefacto «Matriz de permisos» lo edita solo Victor** (solo él puede).

| # | Documento | Qué dice hoy | Qué pasaría a decir | Quién lo edita |
|---|---|---|---|---|
| 1 | `04-flujos-de-negocio/12-checklist.md` (línea 29, decisión D5 del Lote 1) | «El "Acta de conformidad" (CIERRE) se mantiene fuera de este catálogo y no se modifica.» | «La "Acta de conformidad" no figura en la lista del checklist del proyecto: los documentos de fase CIERRE se ocultan de la lista y del editor y no cuentan para el checklist completo.» — **deroga D5** | Documentador (D2) |
| 2 | `12-checklist.md` (tabla de 13 ítems y línea 5) | La tabla no declara qué acción muestra cada fila; «Subir un documento del catálogo lo puede además el rol responsable…» | Nueva columna «Grupo / acción»: «Seleccionar archivo» solo en Alcance, Presupuesto, Listado de personal nuevo y Listado de pets; «Crear / Ver» en los 9 de pantalla propia; **subir aplica solo a esos 4 más los personalizados** | Documentador (D2) |
| 3 | `14-accesos-y-restricciones.md` (fila «Subir documento del proyecto (catálogo AL_INICIO/CIERRE)», nota 4) | La acción «Subir documento» cubre el catálogo AL_INICIO/CIERRE completo | La acción cubre solo los ítems del Grupo A y los personalizados; el servidor rechaza subir a ítems del Grupo B y el acta sale del alcance → **aprobada por Victor (Q4)** | Documentador (D2); artefacto «Matriz de permisos»: Victor |
| 4 | `08-programa-portafolio-proyecto.md` (línea 11) | «la transición en sí solo valida en servidor el Plan Maestro `APROBADO` y el checklist completo» | «…y el checklist completo (los documentos de fase CIERRE no cuentan desde O7)». **Sin este cambio, ningún proyecto podría cerrarse**: el acta siempre quedaría pendiente | Documentador (D2) |
| 5 | `04-flujos-de-negocio/15-cronograma.md` | No dice nada sobre el mensaje de error de importación (solo informe de extracción y niveles) | Regla nueva: «si la importación falla, la pantalla muestra el motivo específico (sin mensaje genérico) y el error queda logueado en servidor con formato, nombre del archivo y mensaje» | Documentador (D2) |
| 6 | `04-flujos-de-negocio/16-paneles.md` (línea 62) | Define el chip inerte con título «Sin pantalla todavía» | **No cambia:** ese mismo patrón se reutiliza para los botones muertos de OT, Recursos del servicio y 3WLA en el checklist (fila informativa, sin edición) | — |

### (iv) Ramas y worktrees — **autorizado**

- Reutilizar `local-worker-1` y `local-worker-2` (existentes, limpias) y **hacer fast-forward de `local-worker-2` a `main`** antes de arrancar la Fase B.
- No se crea, borra ni renombra ninguna rama ni worktree; `local-worker-3`/`local-worker-4` quedan como están.
- Merge a `main` solo tras el Gate 2.

### (v) Consultas Q1–Q4 — resueltas

| # | Respuesta de Victor |
|---|---|
| Q1 | Proyecto existente: **`PS-0006` — «PRUEBA-F5B Servicio de verificacion»** |
| Q2 | Si A7 encuentra archivos ya subidos a ítems del Grupo B: **los elimina Victor él mismo** («elimino todo lo que exista para que no haya confusión»). El Worker **solo consulta y reporta**; no borra nada. |
| Q3 | La `089` **la aplica el Worker con las credenciales autorizadas** (protocolo de migraciones). |
| Q4 | Cubierta por la aprobación de la fila 3: Documentador edita el flujo 14; el artefacto «Matriz de permisos» lo edita Victor. |

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-02 | Gate Spec aprobado (O5, O6, O7) | Victor |
| 2026-10-02 | Dos grupos de acción: A Archivo (4 ítems) y B Pantalla propia (9 ítems) | Victor |
| 2026-10-02 | OT, Recursos del servicio y 3WLA quedan en el Grupo B con botones **muertos**; las pantallas vienen en otro plan | Victor |
| 2026-10-02 | O7 reabre y deroga la decisión D5 del Lote 1; el mecanismo lo define el Planner | Victor |
| 2026-10-02 | D1: O5 se implementa con columnas en `catalogo_documentos` (migración `089`) | Planner (delegado por el Spec) |
| 2026-10-02 | D2: O7 se implementa por **ocultado** (lista + editor + gate de cierre), sin migración destructiva y sin tocar el bootstrap | Planner (delegado por el Spec) |
| 2026-10-02 | D3–D5: regla de render, `?proyectoId=` en los enlaces y gateo por permiso de cada pantalla | Planner |
| 2026-10-02 | **Gate 1 aprobado:** plan, Punch List, tabla de reglas (filas 1–5), pre-autorizaciones (bloque completo) y ramas con fast-forward de `local-worker-2` | Victor |
| 2026-10-02 | Proyecto de prueba: **PS-0006 «PRUEBA-F5B Servicio de verificacion»** (existente) | Victor |
| 2026-10-02 | Archivos subidos a ítems del Grupo B (si A7 los encuentra): **los elimina Victor**; el Worker solo consulta y reporta | Victor |
| 2026-10-02 | La migración `089` **la aplica el Worker** con las credenciales autorizadas (protocolo de migraciones) | Victor |
| 2026-10-02 | Deuda del Lote 1: **commitear** `PPTO-prueba N°01.xlsx` | Victor |
| 2026-10-02 | Fila 3 (flujo 14 + artefacto «Matriz de permisos»): cambio aprobado; el artefacto lo edita Victor | Victor |
| 2026-10-02 | **Tanda A cerrada:** A1–A8 `Conforme`; código en `local-worker-1` (`c219069`, `af60e85`, pusheado); 089 aplicada y verificada | Orquestador (consolidación) |
| 2026-10-02 | **Bloqueo de B resuelto con la mitigación R7 aprobada en Gate 1:** PS-0006 y PS-0004 tienen Plan Maestro aprobado (409 previo al parser) → Worker 2 **crea un servicio de prueba nuevo** (marcado `PRUEBA-…`, sin PM, sin cronograma, sin datos reales) por el flujo normal de la app con cuenta A, sin tocar PS-0004/PS-0006; si la creación no es posible sin navegador, devuelve la pregunta con las opciones 1–3 del `resultados/B.md` (nada destructivo sin Victor) | Orquestador (R7; autonomía delegada por Victor) |
| 2026-10-02 | Autorizado a Worker 2: corregir dentro de B3/B4 el **500 crudo** de `POST /api/cronograma` cuando `proyectoId` no es uuid válido (falta `esIdProyectoValido`) → 400 limpio (carril propio, alineado con RB4) | Orquestador |
| 2026-10-02 | **A-H1** (expresión no nulo-safe en `page.tsx`, inalcanzable hoy) queda **Pendiente de decisión** para el Gate 2: nulo-safe ahora (una línea, archivo dueño) u otro plan | Victor (Gate 2) |
| 2026-10-02 | **Tanda B cerrada:** B1–B7 `Conforme`; código en `local-worker-2` (`c502122`, `a53ce5b`, pusheado); causa raíz en 3 sitios ajenos al parser; 1030 tests · build verdes | Orquestador (consolidación) |
| 2026-10-02 | Servicio de prueba creado por R7: **PS-0007 «PRUEBA-CRONO Importacion de cronograma»** (`479e9671-…`, portafolio «Portafolio Practica»); único dato escrito: su propio cronograma (estado final PDF, 78 act.). PS-0004 y PS-0006 **intactos** | Orquestador (R7) / Worker 2 |
| 2026-10-02 | **O7 aplicada:** el gate de cierre evalúa solo fase ≠ `CIERRE`; D5 del Lote 1 derogada (acta fuera de la lista, editor y checklist completo) | Victor (Spec/Gate 1) |
| 2026-10-02 | **C1 parcial:** `db/README.md` actualizado con la fila `089` en `local-worker-1` (commit `3a393d5`, pusheado); el merge a `main` sigue **postergado al Gate 2** (iv) | Orquestador (Fase C) |
| 2026-10-02 | **Pendiente de decisión para el Gate 2:** el mismo `??` muerto (`traducirErrorApi(x) ?? '…'`) está en `FormularioSubirRdt.tsx:55` y `FormularioPlanMaestro.tsx:244,269` (carriles ajenos; no se tocaron) — corregirlos ahora u otro plan | Victor (Gate 2) |
| 2026-10-02 | **Pendiente de decisión para el Gate 2:** `middleware.ts:33-37` redirige también las rutas `/api/*` a `/login` HTML (sesión caducada → mensaje genérico); la mitigación ya está en el formulario, pero corregirlo en origen exige tocar autenticación — excepción `/api/*` con 401 JSON ahora, o dejarlo así | Victor (Gate 2) |
| 2026-10-02 | **Gate 2 aprobado:** merge de `local-worker-1` (`b9d0e2b`) y `local-worker-2` (`5e8420b`) a `main`, push, mensaje de cierre e índices | Victor |
| 2026-10-02 | **A-H1**, el `??` muerto en dos formularios y la excepción `/api/*` del middleware: enviados a planes futuros (ninguno bloquea el cierre) | Victor (autorización de cierre) |
| 2026-10-02 | **Skills MB1/MB2** (propuestos por el Auditor): no se crean en este plan | Victor (autorización de cierre) |
| 2026-10-02 | **Auditoría emitida:** [`04-auditoria/2026-10-02-observaciones-victor-lote-2.md`](../04-auditoria/2026-10-02-observaciones-victor-lote-2.md), `Listo para Gate 2` tras el merge | Auditor |

## Enlaces a progreso y evidencia homónimos

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-10-02-observaciones-victor-lote-2.md`
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-02-observaciones-victor-lote-2.md`
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-10-02-observaciones-victor-lote-2.md`

## Libro de hallazgos

Formato de fila: `| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |`. Estados: `Registrada` → `Trasladada` (con enlace y commit) · `Descartada` (con motivo) · `Pendiente de decisión` (con quién decide). Los Workers no editan este archivo: dejan sus hallazgos en su resumen de cierre y el Orquestador los pasa aquí.

## Mejoras (de trabajo)

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| MB1 | 2026-10-02 | Worker 1 (tanda A, A-H2) | En worktrees, `next build` (Turbopack) falla por symlink de `node_modules` fuera del worktree; usar `npx next build --webpack` | `03-aprendizaje-continuo/` (archivo nuevo) | `Trasladada` | [`2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md`](../../03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md) § 1 (commit `903033e`) |
| MB2 | 2026-10-02 | Worker 1 (A-H3) y Worker 2 (B, hallazgo 1) | Evidenciar SSR/API **sin navegador**: password grant de Supabase → cookie `sb-<ref>-auth-token` (`base64-` troceada a 3180, verificada en `@supabase/ssr`); script temporal fuera del repo | `03-aprendizaje-continuo/` (archivo nuevo) | `Trasladada` | [`2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md`](../../03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md) § 2 (commit `903033e`) |
| MB3 | 2026-10-02 | Worker 2 (B, hallazgo 2) | En Windows PowerShell 5.1, `Get-Content -Raw` + `Set-Content` corrompe UTF-8 con acentos; usar la herramienta de edición de archivos | `03-aprendizaje-continuo/` (archivo nuevo) | `Trasladada` | [`2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md`](../../03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md) § 3 (commit `903033e`) |

## Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| RB1 | 2026-10-02 | Victor (Spec) | Cada fila del checklist muestra la acción de su grupo: «Seleccionar archivo» solo en los 4 ítems del Grupo A; enlace «Crear / Ver» a la pantalla propia en los 9 del Grupo B; sin subida en el Grupo B | `04-flujos-de-negocio/12-checklist.md` | `Trasladada` | [`12-checklist.md`](../../04-flujos-de-negocio/12-checklist.md) (columna «Grupo / acción» + «Grupos de acción», commit `7100179`) |
| RB2 | 2026-10-02 | Victor (Spec) | OT, Recursos del servicio y 3WLA quedan con botón muerto (título «Sin pantalla todavía») hasta que exista su pantalla | `04-flujos-de-negocio/12-checklist.md` | `Trasladada` | [`12-checklist.md`](../../04-flujos-de-negocio/12-checklist.md) («Ítems sin pantalla todavía (RB2)», commit `7100179`) |
| RB3 | 2026-10-02 | Victor (Spec) | «Acta de conformidad» no figura en la lista del checklist; los documentos de fase CIERRE no cuentan para el checklist completo (deroga D5) | `04-flujos-de-negocio/12-checklist.md` + `08-programa-portafolio-proyecto.md` | `Trasladada` | [`12-checklist.md`](../../04-flujos-de-negocio/12-checklist.md) (acta fuera de la lista) + [`08-programa-portafolio-proyecto.md`](../../04-flujos-de-negocio/08-programa-portafolio-proyecto.md) (CIERRE no cuenta), commit `7100179` |
| RB4 | 2026-10-02 | Victor (Spec) | Si la importación de cronograma falla, la pantalla muestra el motivo específico y el error queda logueado en servidor con formato, nombre de archivo y mensaje | `04-flujos-de-negocio/15-cronograma.md` | `Trasladada` | [`15-cronograma.md`](../../04-flujos-de-negocio/15-cronograma.md) (regla RB4 de fallo de importación, commit `7100179`) |

## Observaciones sobre la política

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| OP1 | 2026-10-02 | Planner | El plan del Lote 1 enlaza `02-progreso/`, `03-evidencia/` y una carpeta `-briefs/` que **no existen**: un plan puede quedar «Cerrada» sin sus homónimos y con enlaces rotos. En este plan se cierra la deuda (D3) | Clasificación del Auditor; Victor decide en el Gate 2 | `Trasladada` | [Informe de Auditoría Lote 2](../04-auditoria/2026-10-02-observaciones-victor-lote-2.md) (clasificada `PROPONER A RESPONSABLE`) |
| OP2 | 2026-10-02 | Planner | O6 **reabre O4**: se aprobó y cerró O4 (Gate 2 del Lote 1) sin evidencia de smoke, pese a que el informe del Auditor lo dejó como «APLICAR AHORA». El flujo permitió cerrar una corrección sin la evidencia mínima que su propia evidencia pedía | Clasificación del Auditor; Victor decide en el Gate 2 | `Trasladada` | [Informe de Auditoría Lote 2](../04-auditoria/2026-10-02-observaciones-victor-lote-2.md) (clasificada `PROPONER A RESPONSABLE`) |
| OP3 | 2026-10-02 | Planner | La plantilla `02-plan.md` presenta los cuatro apartados del libro de hallazgos como secciones de nivel 2, mientras el plan aprobado del Lote 1 los usa como nivel 3; el lector/verificador puede buscarlos en el nivel equivocado | Auditor y `06-plantillas/02-plan.md` | `Trasladada` | [Informe de Auditoría Lote 2](../04-auditoria/2026-10-02-observaciones-victor-lote-2.md) (clasificada `PROPONER A RESPONSABLE`) |
| OP4 | 2026-10-02 | Worker 2 (tanda B) | El brief fija PS-0006 para el smoke **sin chequear antes** si el servicio está bloqueado por Plan Maestro aprobado (409 previo al parser): el chequeo previo (llamada de análisis sin escribir) debería ser un paso del brief o del Gate 1 para no gastar la tanda | Clasificación del Auditor; Victor decide en el Gate 2 | `Trasladada` | [Informe de Auditoría Lote 2](../04-auditoria/2026-10-02-observaciones-victor-lote-2.md) (clasificada `PROPONER A RESPONSABLE`) |
| OP5 | 2026-10-02 | Worker 2 (tanda B) | `src/middleware.ts:33-37` redirige a `/login` (HTML) también para rutas `/api/*` con sesión caducada: la API no puede devolver un `error` JSON y cualquier forma pinta «Ocurrió un error»; la mitigación quedó en `FormularioCronograma` pero el patrón afecta a **todas** las APIs | Clasificación del Auditor; Victor decide en el Gate 2 (toca autenticación) | `Trasladada` | [Informe de Auditoría Lote 2](../04-auditoria/2026-10-02-observaciones-victor-lote-2.md) (clasificada `PROPONER A RESPONSABLE`) |

## Carpetas/archivos huérfanos

Ninguno detectado en la revisión de inicio ni en las tandas A y B (A-H4 y hallazgo 6 de B: ninguno). Si durante la Fase D o la auditoría aparece alguno, se reporta aquí sin borrar nada.

## Informe de Auditoría

[`2026-10-02-observaciones-victor-lote-2.md`](../04-auditoria/2026-10-02-observaciones-victor-lote-2.md) — recomendación **`Listo para Gate 2`** (informe emitido antes del Gate 2 y actualizado tras el merge autorizado). Clasificación: `APLICAR AHORA` ninguno; `PROPONER A RESPONSABLE` OP1–OP5; `NO PROMOVER` ninguno; `PROPONER SKILL` MB1 y MB2 (no creados en este plan). Pendientes técnicos para decisión futura: A-H1, el `??` muerto en dos formularios y la excepción `/api/*` del middleware.

## Mensaje de cierre

### Alcance completado y no completado

- **Completado:** O5 (migración `089` + acción por grupo en cada fila del checklist), O7 (acta de conformidad fuera de la lista, del editor y del gate de cierre, derogando D5 del Lote 1) y O6 (importación de cronograma de punta a punta: causa raíz en tres sitios ajenos al parser, validación de uuid, `logFalloImportacion` en 17 caminos, `traducir-error` sin fallback genérico y smokes reales de éxito y fallo), más toda la Fase D (flujos 12/08/15/14, deuda documental del Lote 1 y traslado del libro de hallazgos).
- **No completado (fuera de alcance, a planes futuros):** pantallas de OT, Recursos del servicio y 3WLA (hoy con botones muertos); A-H1 (expresión no nulo-safe en `page.tsx`, inalcanzable); el `??` muerto en `FormularioSubirRdt.tsx:55` y `FormularioPlanMaestro.tsx:244,269`; la excepción `/api/*` (401 JSON) en `middleware.ts:33-37`; los Skills MB1/MB2 propuestos.

### Estado final de la Punch List

A1–A8 `Conforme` · B1–B7 `Conforme` · C1 `Conforme` · D1–D4 `Conforme`.

### Evidencia

[`03-evidencia/2026-10-02-observaciones-victor-lote-2.md`](../03-evidencia/2026-10-02-observaciones-victor-lote-2.md), con `resultados/A.md` y `resultados/B.md`. Smoke real sobre PS-0007: XLSX 14 act. y PDF 78 act. con persistencia verificada; 6 fallos con motivo específico en pantalla y log en servidor. Comandos: carril 1 **100/1043 tests**, carril 2 **100/1030 tests**, `tsc` 0, lint 27 = baseline, `next build --webpack` 0.

### Auditoría y decisiones del Gate 2

Informe `Listo para Gate 2`. Victor aprobó el Gate 2 (2026-10-02) y autorizó el merge. A-H1, el `??` muerto y la excepción `/api/*` del middleware quedan enviados a planes futuros (ninguno bloquea el cierre). Los Skills propuestos (MB1, MB2) no se crean en este plan.

### Consumo total del plan

`python scripts/medir.py` **no encontró las sesiones del 2026-10-02**: los registros locales de Claude Code que lee el script no contienen esas sesiones (la sesión de este cierre corre en otro harness). **No se estiman cifras**; la fila queda pendiente de medir con el script cuando las sesiones estén disponibles.

| Rol o Worker | Sesiones | Llamadas | Entrada | Caché creada | Caché leída | Salida |
|---|---|---|---|---|---|---|
| **Total del plan** | pendiente | — | — | — | — | — |

### Hallazgos trasladados

MB1–MB3 → aprendizaje nuevo; RB1–RB4 → flujos 12/08/15; OP1–OP5 → informe de Auditoría (clasificadas `PROPONER A RESPONSABLE`). **Ninguna fila queda `Registrada`.** Verificador de referencias: **0 huérfanos / 0 enlaces rotos** (exit 0) en el núcleo de 44 archivos; alcance del Lote 2, 0/0.

### Documentos promovidos

Flujos `12-checklist.md`, `08-programa-portafolio-proyecto.md`, `15-cronograma.md` y `14-accesos-y-restricciones.md`; índices `01-planes/README.md` y `04-flujos-de-negocio/README.md`. Aprendizaje nuevo `03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md`.

### Aprendizajes registrados

MB1 (build `--webpack` en worktrees), MB2 (evidencia SSR/API sin navegador), MB3 (UTF-8 en PowerShell 5.1).

### Pendientes enviados a planes futuros

Ver «Elementos postergados propuestos para planes futuros» al final.

### Merge / fuentes de verdad / Skill

- **16a Merge:** `local-worker-1` → `main` (`b9d0e2b`) y `local-worker-2` → `main` (`5e8420b`); `main` = `origin/main` = `5e8420b`.
- **16b Fuentes de verdad:** actualizadas en la Fase D (commits `7100179`, `903033e`); índices actualizados en la tanda de cierre.
- **16c Skill:** no aplica (MB1/MB2 propuestos por el Auditor y no aprobados para crear en este plan).

### Confirmación de 100% pusheado

`pg_control_proyectos`: `main` = `origin/main`, `git rev-list --left-right --count` = `0 0`, sin cambios propios pendientes (el árbol conserva cambios de otros planes activos, ajenos a este). `py_control_proyectos_web`: `main` = `origin/main` = `5e8420b`, `0 0`, árbol limpio.

### Autorización de cierre

Gate 2 aprobado y cierre autorizado por Victor (2026-10-02). Queda la verificación final de Victor en la app desplegada (riesgo R6).

## Elementos postergados propuestos para planes futuros

- Pantallas de OT, Recursos del servicio y 3WLA (hoy con botones muertos).
- Generación automática de «Recursos del servicio» desde los datos del DP.
- Limpieza de ramas/worktrees `local-worker-3` y `local-worker-4` (atrás de `main`).
- **A-H1:** expresión no nulo-safe en `page.tsx:163` (`catalogo?.roles.clave`); inalcanzable hoy.
- **`??` muerto** en `FormularioSubirRdt.tsx:55` y `FormularioPlanMaestro.tsx:244,269` (pasar el fallback como 2.º argumento).
- **Excepción `/api/*` en `middleware.ts:33-37`** (401 JSON en vez de redirección a `/login` HTML); toca autenticación.
- **Skills MB1/MB2** propuestos por el Auditor (build en worktrees; evidencia sin navegador), no creados.
