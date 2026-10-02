# Informe de Auditoría — Lote 2: acciones del checklist (O5), importación de cronograma (O6) y acta de conformidad (O7)

> Auditor: rol Auditor (solo lectura). Escribe únicamente este informe; no edita código, flujos, plan, progreso ni evidencia. Formato: `06-informe-auditoria.md`. Fecha: 2026-10-02.

## Alcance auditado

Lote 2 del plan [`2026-10-02-observaciones-victor-lote-2-plan.md`](../01-planes/2026-10-02-observaciones-victor-lote-2-plan.md) sobre el Spec [`2026-10-02-observaciones-victor.md`](../01-planes/2026-10-02-observaciones-victor.md): (O5) acción por grupo en cada fila del checklist, (O7) «Acta de conformidad» fuera de la lista y del gate de cierre, y (O6) importación de cronograma de punta a punta con motivo específico y log en servidor. Se auditan las fases A (carril `local-worker-1`), B (carril `local-worker-2`) y D (documentación), la Punch List A1–A8 / B1–B7 / C1 / D1–D4, el libro de hallazgos y las fuentes de verdad declaradas afectadas (flujos 12, 08, 15, 14 y el índice de `04-flujos-de-negocio`).

Este informe se emitió **antes del Gate 2** y **antes del merge a `main`**; se **actualiza tras el Gate 2 autorizado por Victor y el merge ya ejecutado** por el Orquestador. Verificación post-merge: `main` pasó de `ce5623e` a **`5e8420b`**, con dos merges — `b9d0e2b` (Merge `local-worker-1`: checklist O5/O7 + `089` documentada) y `5e8420b` (Merge `local-worker-2`: cronograma O6) —, `main` = `origin/main` y `0 0` en `git rev-list --left-right --count origin/main...main`, árbol limpio. Los cinco commits de los carriles (`c219069`, `af60e85`, `3a393d5`, `c502122`, `a53ce5b`) son ahora ancestros de `main`.

## Material revisado

- Spec `2026-10-02-observaciones-victor.md`; Plan `2026-10-02-observaciones-victor-lote-2-plan.md`; Progreso `02-progreso/2026-10-02-observaciones-victor-lote-2.md`; Evidencia `03-evidencia/2026-10-02-observaciones-victor-lote-2.md`.
- Resultados de tanda: `...-lote-2-briefs/resultados/A.md` y `.../B.md`.
- Flujos: `12-checklist.md`, `08-programa-portafolio-proyecto.md`, `15-cronograma.md`, `14-accesos-y-restricciones.md`, `04-flujos-de-negocio/README.md`.
- Aprendizaje: `03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md` y el índice de `03-aprendizaje-continuo/README.md`.
- Plantilla `06-plantillas/02-plan.md`; estándar `04-flujo-sdd-y-planes.md`; plan del Lote 1 (`2026-10-02-observaciones-victor-plan.md`) para OP3.
- Código en `py_control_proyectos_web`: `local-worker-1` (`.worktrees/local-worker-1`), `local-worker-2` (`.worktrees/local-worker-2`) y `main`. Archivos: `db/089_checklist_grupos.sql`, `db/README.md`, `src/lib/checklist/acciones-checklist.ts` (+ test), `src/app/(workspace)/proyectos/[id]/page.tsx`, `src/middleware.ts`, `src/lib/errores/traducir-error.ts` (+ test), `src/components/ui/FormularioSubirRdt.tsx`, `src/components/ui/FormularioPlanMaestro.tsx`.

## Verificación de rama

Comandos reales ejecutados en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` (no de memoria).

Punteros:

```
git rev-parse main            -> ce5623e765b8ad1719a4f6734c30679370a416f5
git rev-parse local-worker-1  -> 3a393d5f5329c13fbd8fc81fbec82c963f74718e
git rev-parse local-worker-2  -> a53ce5b318a51741ffa1ed202de00cc0b9f811f4
git rev-parse origin/main     -> ce5623e765b8ad1719a4f6734c30679370a416f5
```

Commits del carril 1 no presentes en `main` (`git log --oneline main..local-worker-1`):

```
3a393d5 docs(db): documenta 089_checklist_grupos en el README
af60e85 feat(checklist): gate de cierre sin fase CIERRE, editor sin items de cierre y rechazo de subida al Grupo B
c219069 feat(checklist): grupos de accion del catalogo (O5) y render delegado en la lista
```

Commits del carril 2 no presentes en `main` (`git log --oneline main..local-worker-2`):

```
a53ce5b tanda B (O6): motivo especifico en pantalla y log de todos los fallos de la importacion de cronograma
c502122 tanda B (O6): smoke de importacion de cronograma con sesion Supabase sin navegador
```

Pertenencia (`git branch --contains <sha>`):

```
c219069  -> + local-worker-1
af60e85  -> + local-worker-1
3a393d5  -> + local-worker-1
c502122  -> + local-worker-2
a53ce5b  -> + local-worker-2
```

Comprobación de ancestría contra `main` (verificación **previa** al Gate 2):

```
git merge-base --is-ancestor c219069 main  -> exit 1 (NO era ancestro de main antes del merge)
git status -sb (código)                     -> ## main...origin/main   (árbol limpio)
```

**Conclusión de rama (previa al Gate 2, confirmada con git):** al emitirse el informe, los cinco commits de los dos carriles estaban **solo** en sus ramas de Worker (`local-worker-1`, `local-worker-2`) y **ninguno en `main`**, que entonces era `ce5623e` = `origin/main` (el merge es posterior al Gate 2). Los worktrees estaban alineados con sus ramas (`local-worker-1` en `3a393d5`, `local-worker-2` en `a53ce5b`).

### Actualización post-merge

Victor autorizó el Gate 2 y el Orquestador ejecutó el merge. Verificado con git tras el merge:

```
git rev-parse main              -> 5e8420bef6476cf65511e5ab48e6e02c43b45e73
git rev-parse origin/main       -> 5e8420bef6476cf65511e5ab48e6e02c43b45e73
git rev-list --left-right --count origin/main...main
                                -> 0	0
git status -sb                  -> ## main...origin/main   (árbol limpio)

git log --oneline -6 main
5e8420b Merge local-worker-2: cronograma O6 (smoke, validacion uuid, log de fallos y motivo especifico)
b9d0e2b Merge local-worker-1: checklist O5/O7 (grupos de accion, acta fuera de la lista, gate de cierre) y 089 documentada
3a393d5 docs(db): documenta 089_checklist_grupos en el README
a53ce5b tanda B (O6): motivo especifico en pantalla y log de todos los fallos de la importacion de cronograma
c502122 tanda B (O6): smoke de importacion de cronograma con sesion Supabase sin navegador
af60e85 feat(checklist): gate de cierre sin fase CIERRE, editor sin items de cierre y rechazo de subida al Grupo B

git merge-base --is-ancestor <sha> main
c219069 -> exit=0   af60e85 -> exit=0   3a393d5 -> exit=0
c502122 -> exit=0   a53ce5b -> exit=0
```

**Conclusión post-merge:** los cinco commits de los dos carriles son **ancestros de `main`** (los cinco `merge-base --is-ancestor` devuelven `exit 0`), `main` = `origin/main` = `5e8420b`, `0 0` y árbol limpio. La integración quedó completa.

## Cumplimiento de SDD, plan, Punch List y evidencia

### Verificación de la Punch List (contra evidencia y código)

**Worker 1 — Checklist (O5 + O7): A1–A8 `Conforme`.** Verificado en código y evidencia:
- A1: `db/089_checklist_grupos.sql` existe; añade `grupo_accion`/`ruta_accion`/`etiqueta_accion` con `add column if not exists`, constraint `grupo_accion in ('ARCHIVO','PANTALLA')`, 9 `PANTALLA`, 4 rutas (`/cronograma`, `/paquetes-trabajo`, `/plan-maestro`, `/requerimientos`) y `'Crear / Ver'` en 7 claves; reversa comentada. Aditiva e idempotente. **Conforme**.
- A2: `src/lib/checklist/acciones-checklist.ts` implementa la regla D3 (ad-hoc → Archivo; `ESTRUCTURADO` → enlace DP/PR; `ARCHIVO` → seleccionar archivo; `PANTALLA` → enlace con `etiquetaAccion ?? 'Crear / Ver'` y botón muerto `title: 'Sin pantalla todavía'` sin `ruta_accion`), gateo D5 por permiso de cada pantalla y helper `conProyectoId`. Test presente. **Conforme**.
- A3: `page.tsx` amplía el select con `fase, grupo_accion, ruta_accion, etiqueta_accion` (línea 45), oculta fase `CIERRE` (línea 51-56) y delega el render. **Conforme** (evidencia SSR 9 comprobaciones).
- A4: `confirmar-transicion` filtra fase ≠ `CIERRE` para el checklist completo, sin tocar CAS ni bootstrap. **Conforme** (prueba en ambos sentidos; transición real no ejecutada, declarado).
- A5: editor sin ítems de fase `CIERRE` (`fase !== 'CIERRE'`). **Conforme**.
- A6: POST `documentos/[documentoId]` rechaza `grupo_accion='PANTALLA'` con 400 y mensaje claro; control Grupo A no se bloquea. **Conforme**.
- A7: consulta de solo lectura → 0 filas del Grupo B con `archivo_ruta`; nada que borrar. **Conforme**.
- A8: `npm test` 100/1043 · `tsc` 0 · lint 27 = baseline · `next build --webpack` 0. **Conforme**.

**Worker 2 — Cronograma (O6): B1–B7 `Conforme`.** Verificado en código y evidencia:
- B1/B2/B6: diagnóstico y smokes reales (XLSX 14 act., PDF 78 act., `extraccionCompleta: true`, persistencia verificada) sobre PS-0007; 6 fallos con motivo y log. **Conforme**.
- B3: `esIdProyectoValido` → 400 «El N° OT del servicio no es válido»; prefijo técnico eliminado en `traducirErrorApi`. **Conforme** (código leído: `traducir-error.ts:26-27`).
- B4: `logFalloImportacion` en 17 caminos + 2 `catch`. **Conforme** (salida real del log en `resultados/B.md`).
- B5: fallback real en `FormularioCronograma.tsx` y test nuevo `traducir-error.test.ts` 4/4. **Conforme**.
- B7: `npm test` 100/1030 · `tsc` 0 · lint 27, 0 propios · build 0. **Conforme**.

**Integración/documentación — C1 y D1–D4: `Conforme` (post-merge).**
- **C1: `Conforme`.** La fila `089` está en `db/README.md` (`3a393d5`) y el merge de ambos carriles a `main` ya se ejecutó (merges `b9d0e2b` y `5e8420b`); `main` = `origin/main` = `5e8420b`, `0 0`, árbol limpio. La afirmación de la evidencia homónima («ambos carriles mergeados a `main`… `0/0`») **queda confirmada por git** tras el Gate 2.
- **D1–D4: `Conforme`.** D2 (flujos 12/08/15/14 + índice) y D3 (homónimos del Lote 1) están en `7100179`; D4 (traslado MB1–MB3 y RB1–RB4) está respaldado por `903033e` y por los flujos. **D1:** el índice `01-planes/README.md` aún muestra el Lote 2 «En ejecución»; su actualización al estado final corresponde a la tanda de cierre del Orquestador (ver «Pendientes»).

### Sobre el cierre documental (resuelto por el merge)

La **versión de trabajo** de `02-progreso/` y `03-evidencia/` declaraba, antes del merge, «Estado: Cerrada», «Gate 2 aprobado», «merge a `main` hecho», «Auditoría emitida» y C1 `Conforme`. En el momento de la auditoría previa al Gate 2 esos enunciados **no estaban respaldados por git** (`main` era `ce5623e` y los commits solo estaban en las ramas de Worker), lo que motivó la recomendación original. **Tras la autorización del Gate 2 por Victor y el merge ejecutado por el Orquestador (main `5e8420b`, cinco commits ancestrales, `0 0`), esos enunciados quedan satisfechos** y la discrepancia se resuelve. El cierre real (mensaje de cierre del plan, actualización del índice y verificación final de Victor en producción) lo ejecuta el Orquestador.

### Punch List: tabla de estados

| Bloque | Estado auditado |
|---|---|
| A1–A8 | `Conforme` |
| B1–B7 | `Conforme` |
| C1 | `Conforme` (fila `089` + merge a `main` ejecutado, `main` = `origin/main` = `5e8420b`, `0 0`) |
| D1 | `Conforme` (fila del índice presente; su estado final lo actualiza la tanda de cierre del Orquestador) |
| D2–D4 | `Conforme` |

## Verificación de la revisión de fuentes de verdad por fase

Se abrieron las fuentes dueñas y se contrastaron con lo aprobado en Gate 1:

- **`12-checklist.md`** — ✓ refleja O5/O7: columna «Grupo / acción» (13 ítems), sección «Grupos de acción (O5)» con Grupo A (4) / Grupo B (9), «Sin subida en el Grupo B» con rechazo 400, «Ítems sin pantalla todavía (RB2)» (OT, Recursos, 3WLA con «Sin pantalla todavía»), y «Acta de conformidad» fuera de la lista/editor/checklist completo (línea 31, deroga D5). Incluye RB1, RB2 y RB3.
- **`08-programa-portafolio-proyecto.md`** — ✓ el checklist completo para cerrar «no cuenta los documentos de fase CIERRE desde O7» (línea 11); coherente con A4 y RB3.
- **`15-cronograma.md`** — ✓ regla RB4 (motivo específico en pantalla + log en servidor con formato, nombre y mensaje; nunca solo «error») (línea 7).
- **`14-accesos-y-restricciones.md`** — ✓ fila «Subir documento del proyecto (catálogo AL_INICIO, Grupo A y personalizados)» (línea 78) y nota 4 reescrita al alcance del Grupo A + personalizados, con rechazo 400 y acta CIERRE fuera; actualización fechada 2026-10-02 (línea 17) con la nota de que el artefacto «Matriz de permisos» lo edita **solo Victor**. Correcto: el artefacto no es verificable en el repo y no se editó por un agente.
- **`04-flujos-de-negocio/README.md`** — ✓ fila del Lote 2 con los flujos y reglas que actualiza (línea 43). Dice «(en ejecución)»; su paso a «cerrado» corresponde a la tanda de cierre del Orquestador (no es un defecto del contenido de las reglas).
- **Observación menor en flujo 12:** la línea 38 describe las etiquetas de DP/PR como «Crear/Ver DP, Cargar/Ver PR», mientras el Spec pidió «Crear DP / Ver DP» y «Crear PR / Ver PR». No es una regla nueva ni un cambio de alcance; se anota como precisión de redacción, no bloquea.

**Aprendizaje MB1–MB3:** el archivo `03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md` existe y contiene las tres secciones (MB1 build `--webpack` en worktrees; MB2 evidencia SSR/API sin navegador; MB3 UTF-8 en PowerShell 5.1) con su origen y fecha, y tiene fila en `03-aprendizaje-continuo/README.md` (línea 42). **Conforme.**

**RB1–RB4:** escritas en los flujos dueños (12, 08 y 15) según lo verificado arriba. **Conforme.**

**Libro de hallazgos:** MB1–MB3 y RB1–RB4 en estado `Trasladada` con destino y commit (`903033e` y `7100179`). **No queda ninguna fila `Registrada` de MB/RB.** OP1–OP5 siguen `Registrada` a propósito (las clasifica el Auditor, abajo) y su destino declarado es «Clasificación del Auditor; Victor decide en el Gate 2». **Conforme.**

**Skills citados:** `seguir-flujo-de-planes` (Orquestador; consta su uso declarado, sin evidencia mecánica), `cerrar-tanda` (Workers A y B; aplicado, con estados/evidencia/traspaso por fila), `trasladar-hallazgos` (Documentador D4; sus efectos son verificables: MB a aprendizaje + índice, RB en flujos, filas cerradas) y `verificar-permisos-por-rol` (**no aplica**: ninguna observación cambia la matriz; `acciones-checklist.ts` solo consume `puedeVer*` existentes, confirmado en código). **Conforme.**

## Clasificación de hallazgos

### `APLICAR AHORA`

- **Ninguno.** El único ítem de la emisión previa al Gate 2 —la declaración de cierre de `02-progreso/` y `03-evidencia` sin respaldo en git— quedó **resuelto por el Gate 2 autorizado por Victor y el merge ejecutado**: `main` = `origin/main` = `5e8420b`, con los cinco commits de A/B como ancestros (`merge-base --is-ancestor` exit 0 en todos) y `0 0` en `rev-list --left-right --count`. Los enunciados («Gate 2 aprobado», «merge hecho», «C1 `Conforme`») ahora se corresponden con el estado real.

### `PROPONER A RESPONSABLE`

1. **OP1** — Un plan pudo cerrarse sin sus homónimos `02-progreso/`/`03-evidencia/` y con enlaces a una carpeta `-briefs/` inexistente. Es un hueco del proceso de cierre, no un defecto de este plan. Destino: regla en `04-flujo-sdd-y-planes.md` / checklist de cierre (que existan los homónimos y los enlaces internos resuelvan).
2. **OP2** — O6 reabrió O4: se cerró O4 sin la evidencia de smoke que su propia evidencia pedía. Hueco del proceso (permitir cerrar una corrección sin la evidencia mínima exigida). Destino: endurecer el Gate 2 (no cerrar con ítem `APLICAR AHORA` de un informe previo pendiente).
3. **OP3** — Nivel de sección inconsistente: `06-plantillas/02-plan.md` define los cuatro apartados del libro de hallazgos con `##` (nivel 2); el plan del Lote 1 los usó con `###` (nivel 3); el plan del Lote 2 siguió la plantilla (`##`). Verificado en los tres archivos. Destino: decidir el nivel canónico y alinear plantilla/verificador/planes históricos.
4. **OP4** — El brief fijó PS-0006 para el smoke sin chequear antes el 409 por Plan Maestro aprobado; el chequeo previo (análisis sin escribir) debería ser paso del brief o del Gate 1. Destino: añadir el precheck al brief base de tandas que usan datos de prueba.
5. **OP5** — `src/middleware.ts:33-37` redirige a `/login` (HTML) también `/api/*` con sesión caducada, de modo que la API no devuelve `error` JSON y el usuario ve un mensaje genérico. La mitigación quedó en `FormularioCronograma`, pero el patrón afecta a todas las APIs. Toca autenticación → decide Victor: excepción `/api/*` con 401 JSON o dejarlo como está.

### `NO PROMOVER`

- Ninguna. Todos los hallazgos revisados (A-H1, `??` muerto, `/api/*`, OP1–OP5) tienen valor de follow-up; ninguno se descarta.

### `PROPONER SKILL`

1. **MB1** — El fallo de `next build` (Turbopack) en worktrees por junction de `node_modules` se repite (ya estaba en `2026-09-23-turbopack-worktree-junction.md`, promovido a `01-contexto-repositorio/03-entorno-git-y-worktrees.md`, y volvió a ocurrir en este plan). Propuesta: elevarlo a nota obligatoria del brief base de Workers o a un Skill de arranque de carril (usar `--webpack`).
2. **MB2** — El patrón de evidencia SSR/API sin navegador (password grant + cookie `sb-<ref>-auth-token` troceada) es reutilizable y ya se usó en A3, A5, A6 y los smokes de B. Propuesta: Skill/nota de evidencia para cuando Playwright no está autorizado.

## Pendientes técnicos y documentales

1. **A-H1 (decisión de Victor, Gate 2).** En `local-worker-1` `src/app/(workspace)/proyectos/[id]/page.tsx:163`: `(doc.roles as unknown as { clave: string } | null)?.clave ?? catalogo?.roles.clave`. Es nulo-safe sobre `doc.roles` pero **no** sobre `catalogo.roles`: si `catalogo` existe y su `roles` es `null` (claves `cronograma`/`paquete_trabajo`/`plan_maestro` con `rol_responsable_id` nulo), el SSR revienta con `TypeError … reading 'clave'`. Hoy inalcanzable porque el editor siempre guarda responsable concreto + rol. Corregir a `catalogo?.roles?.clave` (una línea) ahora o en plan futuro.
2. **`??` muerto (decisión de Victor, Gate 2).** `traducirErrorApi` tiene firma `(mensaje: string | undefined, fallback = 'Ocurrió un error'): string` y **siempre** devuelve string, por lo que el `??` nunca se aplica en: `FormularioSubirRdt.tsx:55` y `FormularioPlanMaestro.tsx:244` y `:269` (confirmado en `local-worker-2`). No se tocaron por ser de carriles ajenos. Limpiar (pasar el fallback como 2.º argumento, como se hizo en `FormularioCronograma`) o dejar.
3. **Excepción `/api/*` en `middleware.ts:33-37` (decisión de Victor, Gate 2).** Misma ruta que OP5; exige tocar autenticación, por eso no se aplicó. Devolver 401 JSON a APIs o mantener la redirección.
4. **C1 resuelto:** fila `089` documentada (`3a393d5`) y merge a `main` ejecutado (`b9d0e2b`, `5e8420b`); `main` = `origin/main` = `5e8420b`, `0 0`, árbol limpio. `Conforme`.
5. **D1 (a cargo de la tanda de cierre del Orquestador):** `01-planes/README.md` aún muestra el Lote 2 «En ejecución»; actualizarlo al estado final junto con el mensaje de cierre del plan. `04-flujos-de-negocio/README.md` tiene la misma salvedad.
6. **Menor (flujo 12):** alinear la redacción «Cargar/Ver PR» con lo aprobado («Crear PR / Ver PR»), si Victor lo considera.

## Recomendación

`Listo para Gate 2`.

La implementación de O5 y O6 está respaldada por evidencia real y verificada en los carriles de Worker (tests, smokes y código leídos), los flujos 12/08/15/14 reflejan lo aprobado en Gate 1, y MB1–MB3 y RB1–RB4 están correctamente trasladados. El único ítem de la emisión previa al Gate 2 (declaración de cierre sin respaldo en git) quedó resuelto: Victor autorizó el Gate 2 y el merge ya está ejecutado (`main` = `origin/main` = `5e8420b`; los cinco commits de A/B son ancestros de `main`; `0 0`; árbol limpio), por lo que C1 y D1 pasan a `Conforme` y no queda nada en `APLICAR AHORA`.

**Cierre real a cargo del Orquestador:** redactar el mensaje de cierre del plan, actualizar el estado final del índice `01-planes/README.md` (hoy «En ejecución») y del índice `04-flujos-de-negocio/README.md`, y coordinar la verificación final de Victor en la app desplegada (riesgo R6). Quedan las decisiones de Victor para planes futuros (A-H1, `??` muerto en `FormularioSubirRdt`/`FormularioPlanMaestro`, excepción `/api/*` en `middleware.ts`) y las clasificaciones `PROPONER A RESPONSABLE` (OP1–OP5) y `PROPONER SKILL` (MB1, MB2). El Auditor no hace merge ni aprueba en nombre del Responsable humano.
