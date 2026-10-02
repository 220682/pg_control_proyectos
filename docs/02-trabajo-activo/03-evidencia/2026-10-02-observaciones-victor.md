# Evidencia — Observaciones de Victor (Lote 1: checklist, área Jefatura y error de cronograma)

> **Deuda documental saldada el 2026-10-02** por el Documentador del Lote 2 (Tanda D, ítem D3). La evidencia no se guardó en su momento (no hubo carpeta de briefs ni archivo homónimo — OP1); este archivo la reconstruye con los resultados reales del plan, del informe de auditoría y de la historia de git. **El único caso nunca verificado (smoke de O4) se declara abajo y su evidencia vive en la homónima del Lote 2.**

## Referencia al plan

[`docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-plan.md`](../01-planes/2026-10-02-observaciones-victor-plan.md) — cerrado con Gate 2 aprobado por Victor (2026-10-02). Informe del Auditor: [`docs/02-trabajo-activo/04-auditoria/2026-10-02-observaciones-victor.md`](../04-auditoria/2026-10-02-observaciones-victor.md).

## Entorno y fecha

- Código: `py_control_proyectos_web`, worktrees `.worktrees/local-worker-1` y `.worktrees/local-worker-2`, rama `local-worker-1` desde `647999a`; merge a `main` tras el Gate 2 → `main` = `origin/main` = `ce5623e`.
- Documentación: `pg_control_proyectos`, rama `main` (commits `5f1ed31`, `cd3465b`, `a006081`, `9573dd2`, `2700ad8`).
- Migraciones: `087` y `088` **aplicadas por Victor en Supabase el 2026-10-02** y verificadas en el Gate 2.
- Fechas de ejecución: 2026-10-02. Reconstrucción de esta evidencia: 2026-10-02 (Documentador, Tanda D del Lote 2).

## Rol / usuario y datos autorizados

Cuentas de prueba (credenciales fuera del repositorio; nunca impresas). Solo lectura sobre datos reales y escrituras de prueba del propio plan. Sin secretos. Las migraciones las aplicó Victor.

## Punch List ejecutada

Estados según el plan (Punch List embebida) contrastados con el informe de Auditoría y con la verificación de código; «Método» = lo que realmente se ejecutó.

| ID | Esperado | Método | Observado | Estado | Evidencia/ruta/enlace | Responsable |
|---|---|---|---|---|---|---|
| A1 | Migración `087`: 3 inserts, 3 renombres, delete de AL_INICIO no listados, `orden` 1–13, idempotente | Lectura crítica del SQL por el Auditor + aplicación y verificación de Victor | SQL correcto: limpia `proyecto_documentos` de `materiales_con_costo` antes del delete, agrega `completado` y vuelve `rol_responsable_id` nullable; **aplicada y verificada en Supabase (2026-10-02)** | Conforme | Informe de auditoría § Revisión técnica O3; plan, Gate 2 | Worker 1 |
| A2 | `lista-usuarios.ts` ordena por rol y luego nombre | Prueba unitaria + `tsc` + revisión de código | Orden por `PRIORIDAD_ROL_PRINCIPAL` y luego nombre, reflejado en `etiquetaSelector`; vitest completo verde | Conforme | Auditoría O1 ✓ | Worker 1 |
| A3 | `SelectorUsuario.tsx` sin filtro por rol | `tsc` + build + revisión de código | Los 3 usos del editor van sin `filtrarPorRolClave`; **matiz:** el prop quedó declarado sin uso (clasificado NO PROMOVER) | Conforme | Auditoría O1 ✓ | Worker 1 |
| A4 | `editor-checklist.tsx`: responsable con todos los usuarios para todo ítem | `tsc` + build | Sin filtro por rol en los selectores del editor | Conforme | Auditoría O1 ✓ | Worker 1 |
| A5 | `checklist.ts`: completar por check manual para todos, revisando consumidores | Prueba unitaria + grep de consumidores | `documentoCompleto` = flag `completado`; grep: solo `checklist.ts`/su test y las 4 rutas de API, todas coherentes; `proyectoTieneDp` queda solo para etiquetas Ver/Cargar DP/PR | Conforme | Auditoría O3 ✓ | Worker 1 |
| A6 | `registro-accesos.ts`: «Personal NUEVO» → «Listado de personal nuevo» | Lectura de código (verificación puntual del Documentador, 2026-10-02) | `registro-accesos.ts:281`: chip `personal-nuevo` con el nombre «Listado de personal nuevo» | Conforme | Código de `main` de la app | Worker 1 |
| A7 | `npm test`, `npx tsc --noEmit`, `npm run lint`, `npm run build` verdes | Ejecución en el carril; re-contada por el Auditor (salvo build) | **99 archivos / 1026 tests OK**; `tsc` sin errores; lint **27 problemas (9E/18W)** = baseline en archivos ajenos al plan; build verde **reportado por los Workers** (el Auditor no lo re-ejecutó) | Conforme | Comandos del Auditor § Comandos de verificación | Worker 1 |
| B1 | Migración `088`: `PR`/«Proyecto» → `JF`/«Jefatura», conservando `perfiles.area_id` | Lectura crítica + aplicación y verificación de Victor | Idempotente (guarda contra `JF` existente), conserva `id`; `area-usuario.ts` mapea administrador y jefe de proyectos a `JF`; sin `PR` residual como código de área | Conforme | Auditoría O2 ✓; plan, Gate 2 | Worker 2 |
| B2 | Loguear el error de lectura/parseo en servidor con contexto | Lectura crítica + build | `console.error('[cronograma] No se pudo leer/parsear el archivo', { formato, archivo, error })` en la ruta de lectura; `respuestaErrorInesperado` loguea y devuelve el mensaje. **Alcance:** hoy solo ese `catch` (el resto de caminos de fallo se loguea en el Lote 2, ítem B4) | Conforme | Auditoría O4 ✓ | Worker 2 |
| B3 | Restaurar el mensaje específico en pantalla | Smoke con fallo forzado + revisión de código | `FormularioCronograma` muestra `traducirErrorApi(body.error)`; los mensajes en español pasan a pantalla. **Matiz:** `traducir-error.ts` devuelve el fallback cuando el mensaje empieza por identificador (`Error: …`) y el `?? 'No se pudo leer el cronograma'` es código muerto — confirmado al reabrir O6 en el Lote 2 | Conforme (con matiz del Auditor; la corrección completa queda en O6) | Auditoría O4 ✓ con matiz; Spec O6 | Worker 2 |
| B4 | Reproducir y **corregir** el error de lectura/parseo con los archivos de prueba (éxito real) | Smoke con importación exitosa — **nunca ejecutado** | Solo se corrigió la detección de formato (MIME con fallback por extensión); los parsers (`parser-excel`/`parser-pdf`) no cambiaron y **el éxito end-to-end nunca se verificó**. El informe de Auditoría lo dejó «APLICAR AHORA» y el plan cerró igual | **Observado** | Auditoría, hallazgo APLICAR AHORA 2; reabierto como O6 en el Lote 2 | Worker 2 |
| B5 | `npm test`, `npx tsc --noEmit`, `npm run lint`, `npm run build` verdes | Ejecución en el carril + revisión del Auditor | Mismos números que A7 (1026 tests OK, `tsc` 0, lint 27 = baseline; build reportado) | Conforme | Comandos del Auditor | Worker 2 |
| C1 | `db/README.md` con las filas `087` y `088`; ramas integradas | Diff + `git status` | Commit de integración `ce5623e` (incluye `db/README.md`); merge a `main` verificado `origin/main…main` = `0 0` con árbol limpio | Conforme | Mensaje de cierre del plan (16a) | Integración |
| D1 | Flujos `12-checklist.md` y `02-usuarios.md` según la tabla del Gate 1 | Diff + verificación del Auditor en el libro de hallazgos | RB1 → flujo 12 (13 ítems, completar por check) y RB2 → flujo 02 (área `JF`), commit `5f1ed31` | Conforme | Auditoría § Segundo chequeo | Documentador (Lote 1) |
| D2 | Trasladar RB1/RB2 a su destino y `verificar-referencias.py` sin enlaces rotos | Diff + commits del libro de hallazgos | Filas RB1/RB2 cerradas como `Trasladada` con destino y commit (`cd3465b`); **la salida del verificador no constó en ese cierre**, se ejecutó de nuevo al saldar esta deuda (2026-10-02, Tanda D del Lote 2): sin referencias rotas | Conforme | Plan, libro de hallazgos; verificador en la raíz del repo | Documentador (Lote 1) |

**Posterior al cierre y verificado aquí:** la contradicción del flujo 14 que encontró el Auditor (nota 4 «según `catalogo_documentos.rol_responsable_id`», desactualizada tras O3) se resolvió con el commit `9573dd2` (nota 4 reescrita con el responsable concreto por proyecto), antes del Gate 2.

## Enlace al artifact de checklist visual

**https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd** — Punch List de Mejoras (checklist visual vivo, con estados y comentarios de Victor). Coexiste con este archivo: el artefacto guarda el estado mientras se prueba; este `.md` registra el resultado en texto y en git.

## Resultados de pruebas técnicas

- `npx vitest run` → **99 archivos, 1026 tests, todos pasan** (re-ejecutado por el Auditor).
- `npx tsc --noEmit` → sin errores.
- `npm run lint` → 27 problemas (9 errores, 18 warnings), todos preexistentes en archivos ajenos al plan; único aviso en archivo tocado: `checklist.ts:32` (parámetro `_` intencional).
- `npm run build` → reportado verde por los Workers; **no re-ejecutado por el Auditor** (declarado en su informe).
- Migraciones `087`/`088`: aplicadas por Victor en Supabase (2026-10-02) y verificadas en el Gate 2.

## Regresiones verificadas

- Grep de consumidores de `documentoCompleto`/`checklistCompleto`/`documentosPendientes`: solo `checklist.ts` y su test, más las 4 rutas de API (`dp`, `confirmar-transicion`, `documentos/[documentoId]`, checklist) — todas coherentes con el completado por check.
- El editor del checklist sigue operativo tras `087` (responsable concreto por proyecto; `rol_responsable_id` informativo).
- El área `PR` no queda como código de área residual (solo `pr` como clave de documento, que es correcto).

## Limitaciones o casos no verificables

1. **El smoke real de O4 (importación de cronograma con éxito y con fallo) nunca se hizo.** No hay capturas ni salidas de esa prueba en este plan: esa evidencia vive desde el Lote 2, en [`docs/02-trabajo-activo/03-evidencia/2026-10-02-observaciones-victor-lote-2.md`](../03-evidencia/2026-10-02-observaciones-victor-lote-2.md) (ítems B1/B6 del plan del Lote 2, observación O6).
2. `npm run build` no fue re-ejecutado por el Auditor (solo reportado por los Workers).
3. No hubo briefs ni evidencia en vivo durante la tarea (la carpeta `-briefs/` nunca existió): la tabla de arriba es una reconstrucción documental, no un volcado de salidas en el momento.
4. El prop `filtrarPorRolClave` quedó sin uso en `SelectorUsuario.tsx` (NO PROMOVER; limpieza opcional en plan futuro).
