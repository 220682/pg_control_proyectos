# Evidencia — Observaciones de Victor (Lote 2: acciones del checklist O5, cronograma O6 y acta de conformidad O7)

> **Archivo en actualización** (creado el 2026-10-02 en la Tanda D del Lote 2, ítems D1/D2/D3). Recoge la evidencia real disponible hasta hoy; los ítems de la tanda B se completarán al reanudarla.

## Referencia al plan

[`docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-2-plan.md`](../01-planes/2026-10-02-observaciones-victor-lote-2-plan.md) — Gate 1 aprobado por Victor (2026-10-02); Gate 2 pendiente. Evidencia de cada tanda, en el momento: [`briefs/resultados/A.md`](../01-planes/2026-10-02-observaciones-victor-lote-2-briefs/resultados/A.md) y [`briefs/resultados/B.md`](../01-planes/2026-10-02-observaciones-victor-lote-2-briefs/resultados/B.md).

## Entorno y fecha

- Código: `py_control_proyectos_web`; carril 1 = `local-worker-1` en `.worktrees/local-worker-1` (base `ce5623e`, dev server 3111); carril 2 = `local-worker-2` en `.worktrees/local-worker-2` (fast-forward a `main` autorizado, dev server 3112). **`main` = `origin/main` = `ce5623e`** (merge de A y B solo tras Gate 2).
- Documentación: `pg_control_proyectos`, rama `main`.
- Migración `089`: aplicada por el Worker con credenciales autorizadas (Q3) vía script temporal fuera del repo (protocolo de migraciones).
- Proyecto de prueba: **`PS-0006` — «PRUEBA-F5B Servicio de verificacion»** (Gate 1 (i)). Fecha de ejecución: 2026-10-02.

## Rol / usuario y datos autorizados

Cuentas de prueba A/B (credenciales solo con `Read` en el archivo de cuentas de prueba de la app, fuera de este repositorio; nunca impresas). Login del smoke sin navegador (password grant de Supabase → cookie `sb-…-auth-token` `base64-` troceada, formato verificado contra `@supabase/ssr`). Escrituras solo en el proyecto de prueba; consultas de solo lectura donde el brief lo pide (A7). Sin secretos en el repositorio.

## Punch List ejecutada

Estados tomados de `briefs/resultados/A.md` (tanda A) y `briefs/resultados/B.md` (tanda B), y de la fase D de esta sesión.

| ID | Esperado | Método | Observado | Estado | Evidencia/ruta/enlace | Responsable |
|---|---|---|---|---|---|---|
| A1 | Migración `db/089_checklist_grupos.sql`: columnas `grupo_accion`/`ruta_accion`/`etiqueta_accion`; 9 `PANTALLA`; 4 rutas; 7 etiquetas; aditiva, idempotente, con reversa | SQL + conteos antes/después tras el apply | 80 líneas; `catalogo_documentos` 14→14, `proyecto_documentos` 7→7, con archivo 1→1; después: `grupo PANTALLA: 9`, `con ruta_accion: 4`, `etiqueta 'Crear / Ver': 7`, claves del Grupo B presentes: 9 | Conforme | `db/089_checklist_grupos.sql` (app, commit `c219069`) | Worker 1 |
| A2 | `acciones-checklist.ts` pura (regla D3 + permisos D4/D5) con test de los 4 caminos y rutas | `npm test` + `npx tsc --noEmit` | 100 archivos / **1043 tests OK** (17 del archivo nuevo: 4 caminos, `?proyectoId` en las 4 rutas, gateo D5, ambos sentidos del gate de cierre); `tsc` exit 0 | Conforme | `src/lib/checklist/acciones-checklist.ts` + `.test.ts` | Worker 1 |
| A3 | `page.tsx`: select con `fase`/`grupo_accion`/`ruta_accion`/`etiqueta_accion`; oculta fase `CIERRE`; render delegado | `tsc` + build + SSR real sin navegador | `GET /api/proyectos/51f5905b…/checklist` → 200 con 13 ítems; HTML SSR de `GET /proyectos/51f5905b…` → 200, 95 181 bytes, sección checklist 5 477 bytes, **9 comprobaciones OK** (input solo en Grupo A, enlace cronograma con `?proyectoId=`, botón muerto de OT `title="Sin pantalla todavía"`, «Crear / Ver», casilla presente, sin acta en la lista) | Conforme | Salida en `briefs/resultados/A.md` § estados | Worker 1 |
| A4 | O7 en `confirmar-transicion/route.ts`: solo evalúan fase ≠ `CIERRE`; sin tocar CAS ni bootstrap | Lectura crítica + prueba en ambos sentidos (sin transición real) | `filasQueGatean` filtra `fase !== 'CIERRE'`; todo lo demás completo → **cierra**; un ítem de AL_INICIO pendiente → **no cierra**. **No se ejecutó la transición real en PS-0006** | Conforme | Test en `acciones-checklist.test.ts`; lectura de `confirmar-transicion/route.ts` | Worker 1 |
| A5 | Editor sin ítems de fase `CIERRE`; `checklist/route.ts` filtra si hace falta | `tsc` + build + consulta real con el acta creada | `editor-checklist.tsx` filtra `fase !== 'CIERRE'`; GET con `.neq('fase','CIERRE')`, PATCH rechaza agregar ítems de cierre con 400; con `acta_conformidad` en la base: **`items de fase CIERRE en el editor = 0`**; ocultado, no borrado | Conforme | Salida en `briefs/resultados/A.md` § estados | Worker 1 |
| A6 | POST `documentos/[documentoId]` rechaza `grupo_accion='PANTALLA'` con 400 | Smoke con sesión sin navegador (script fuera del repo) | Subida a `cronograma` → **400** «Este documento se completa en la pantalla de su módulo, no subiendo un archivo»; `ot` (botón muerto) → **400** mismo mensaje; **control** Grupo ARCHIVO sin archivo → 400 «Falta el archivo» (el corte no bloquea el Grupo A) | Conforme | Salida en `briefs/resultados/A.md` § estados | Worker 1 |
| A7 | Consulta de solo lectura: ítems del Grupo B con `archivo_ruta` no nula | SQL de solo lectura | **0 filas** → nada que Victor elimine (Q2); no se borró nada | Conforme | Salida en `briefs/resultados/A.md` § estados | Worker 1 |
| A8 | `npm test`, `tsc`, `lint`, build verdes | Ejecución en el carril | **100 archivos / 1043 tests OK · `tsc` exit 0 · lint 27 (9E/18W) = baseline de `main` · `npx next build --webpack` exit 0** (el `next build` con Turbopack falla por entorno: hallazgo MB1) | Conforme | `briefs/resultados/A.md` § traspaso | Worker 1 |
| B1 | Reproducir el fallo con `scripts/smoke-cronograma.mjs` y `soloAnalizar=true` en los dos archivos | Ejecución real contra `npm run dev -- --webpack -p 3112` | Script creado, lint OK y ejecutado; **ambas llamadas devuelven 409 antes del parser** (Plan Maestro aprobado): `bloqueadoPorPlanAprobado: true`, `perderia: {vinculos: 48, paquetes: 4, planMaestroBorrador: true}`. Cero escrituras | **Observado** | `briefs/resultados/B.md` (salida completa del 409) | Worker 2 |
| B2 | Aislar la causa raíz con `exceljs` y `PDFParse` sobre los archivos reales | — | No alcanzado: el 409 corta antes del parser | Pendiente (bloqueado por R7) | `briefs/resultados/B.md` § estados | Worker 2 |
| B3 | Corregir la causa raíz | — | Sin cambio de código (sin causa raíz diagnosticada). Incluye el 500 crudo de `POST /api/cronograma` sin `esIdProyectoValido`, **autorizado** por el Orquestador | Pendiente | Plan § Registro de decisiones | Worker 2 |
| B4 | Loguear **todos** los caminos de fallo con formato, nombre y mensaje | — | Hoy solo el `console.error` de lectura (`route.ts:314`) | Pendiente | `briefs/resultados/B.md` | Worker 2 |
| B5 | `traducir-error.ts` sin fallback genérico + fallback real en `FormularioCronograma.tsx:133,164` + test | — | `traducir-error.ts:23` sigue devolviendo el fallback para mensajes con prefijo técnico; `??` muerto en las dos líneas; no existe `traducir-error.test.ts` | Pendiente | `briefs/resultados/B.md` | Worker 2 |
| B6 | Smoke de éxito de punta a punta + smoke de fallo con motivo en pantalla y log | — | **Imposible sobre PS-0006/PS-0004** (PM aprobado): ambos servicios vigentes bloqueados; los archivados responden «OT no vigente». Pendiente sobre el servicio de prueba nuevo (R7) | **Observado** | `briefs/resultados/B.md` § «Qué se importó» (nada; cero escrituras) | Worker 2 |
| B7 | `npm test` / `tsc` / `lint` / build verdes en el carril 2 | — | Solo `npx eslint scripts/smoke-cronograma.mjs` → OK; corrida completa al reanudar | Pendiente | `briefs/resultados/B.md` | Worker 2 |
| C1 | `db/README.md` con la fila `089`; ramas integradas; `git status` limpio | Diff + git | **`db/README.md` aún sin la fila `089`**; merge pendiente (solo tras Gate 2) | Sin verificar | — | Integración (Orquestador) |
| D1 | Fila del Lote 2 («En ejecución») en `01-planes/README.md` | Diff | Fila añadida arriba de la del Lote 1, en la tabla «En ejecución» | Conforme | Commit de esta tanda | Documentador |
| D2 | Flujos 12, 08, 15 (+14 aprobado) e índices según la tabla del Gate 1 | Diff + casilla «aplicado» | Escritos: `12-checklist.md` (columna «Grupo / acción», sección «Grupos de acción (O5)», RB1–RB3, acta fuera de la lista), `08-…` (CIERRE no cuenta), `15-cronograma.md` (RB4), `14-…` (fila 74, nota 4, actualización Gate 1; **artefacto «Matriz de permisos»: lo edita Victor**), índice `04-flujos-de-negocio/README.md`. La casilla «aplicado» del plan se marca al cerrar D2/D4 | Conforme (edición hecha; casilla del plan pendiente de marcar) | Diff de esta tanda | Documentador |
| D3 | Progreso y evidencia del Lote 1 con su contenido real + nota del smoke de O4 | Dos archivos nuevos | `02-progreso/2026-10-02-observaciones-victor.md` y `03-evidencia/2026-10-02-observaciones-victor.md` creados: estado Cerrada, commits, SQL aplicados por Victor, decisiones, y la nota de que **el smoke de O4 nunca se hizo** (su evidencia vive en la homónima del Lote 2) | Conforme | Los dos archivos nuevos | Documentador |
| D4 | Trasladar el libro de hallazgos + `verificar-referencias.py` sin rotos | — | **Fuera de esta tanda** (no ejecutado) | Sin verificar | — | Documentador (D4) |

## Enlace al artifact de checklist visual

**https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd** — «El checklist de cada lote de implementación» (estado vivo de los ítems). Coexiste con este archivo: el artefacto guarda el estado mientras se prueba; este `.md` y la Punch List del plan registran el resultado en texto y en git.

## Resultados de pruebas técnicas

- Carril 1 (`local-worker-1`): `npm test` **100 / 1043 OK** · `npx tsc --noEmit` **exit 0** · `npm run lint` **27 (9E/18W) = baseline** · `npx next build --webpack` **exit 0**.
- Carril 2 (`local-worker-2`): pendiente de corrida completa (B7); solo `npx eslint scripts/smoke-cronograma.mjs` → OK.
- Migración `089`: aplicada y verificada con conteos antes/después (A1).
- Evidencia SSR/API **sin navegador** (patrón password grant + cookie Supabase) para A3, A5 y A6.

## Regresiones verificadas

- Gate de cierre probado en **ambos sentidos** (no cierra con ítem de AL_INICIO pendiente; cierra con todo lo demás completo), sin ejecutar transición real.
- El Grupo A siguió subiendo (control 400 «Falta el archivo») después del rechazo al Grupo B.
- `checklist.ts` **no se tocó** (`checklistCompleto` conserva su contrato); el filtro de fase está en quien lo llama.
- Cero escrituras en servicios reales durante la tanda B (solo GET y `soloAnalizar=true`).

## Limitaciones o casos no verificables

1. **Tanda B incompleta:** no existe salida de smoke de éxito ni de fallo (B1/B6 `Observado`, B2–B5/B7 `Pendiente`); bloqueo 409 documentado, mitigación R7 aprobada pero aún no ejecutada.
2. La transición real de fase (A4) no se ejecutó en PS-0006 (solo prueba de ambos sentidos en test).
3. El build con Turbopack (por defecto) no funciona en worktrees (MB1); se usó `--webpack`.
4. El merge a `main`, `db/README.md` (089) y la verificación final en la app desplegada (R6) quedan para el cierre.
5. `resultados/B.md` aún registra «DETENIDA» con la pregunta de PS-0006: no refleja todavía la decisión R7 del Orquestador (se actualizará al reanudar la tanda).
