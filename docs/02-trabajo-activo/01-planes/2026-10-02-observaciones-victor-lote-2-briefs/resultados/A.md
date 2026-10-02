# Resultado · Tanda A — Worker 1 (carril 1 · Checklist)

## Tanda, rol y modelo

- **Tanda:** A — «Acciones del checklist (O5) y acta fuera de la lista (O7)».
- **Rol:** subagente «Worker 1 · tanda A» (código), dentro del flujo con Orquestador.
- **Modelo:** `opencode/mimo-v2.6-flash-free`.
- **Rama y entorno:** `local-worker-1` en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-1` (base `ce5623e`); puerto 3111 para el dev server.

## Estado de los ítems

| ID | Estado (`Conforme` / `Observado` / `No aplica`) | Evidencia: comando o pantalla y resultado real | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| A1 | Conforme | `db/089_checklist_grupos.sql` (80 líneas, aditiva e idempotente con reversa comentada). Aplicada con script temporal **fuera** del repo (protocolo de `00-contratos-comunes.md`) y verificada: conteos antes/después iguales — `catalogo_documentos` 14→14, `proyecto_documentos` 7→7, con archivo 1→1; después del apply: `grupo PANTALLA: 9 (esperado 9)`, `con ruta_accion: 4 (esperado 4)`, `etiqueta 'Crear / Ver': 7 (esperado 7)`, `claves del Grupo B presentes: 9 (esperado 9)`. | — |
| A2 | Conforme | `src/lib/checklist/acciones-checklist.ts` + `acciones-checklist.test.ts`: `npm test` → **100 archivos / 1043 tests OK** (de ellos los 17 del archivo nuevo, que cubren los 4 caminos, `?proyectoId` en las 4 rutas reales, el gateo D5 y ambos sentidos del gate de cierre); `npx tsc --noEmit` → exit 0. | — |
| A3 | Conforme | `page.tsx` con select ampliado y render delegado. `npx tsc --noEmit` exit 0; `npx next build --webpack` exit 0; `GET /api/proyectos/51f5905b…/checklist` → 200, 13 ítems; HTML SSR de `GET /proyectos/51f5905b…` (status 200, 95 181 bytes, sección de checklist 5 477 bytes) con las 9 comprobaciones **OK**: input de archivo solo en el Grupo A (2 en PS-0006), enlace real de cronograma con `?proyectoId=`, botón muerto de OT con `title="Sin pantalla todavía"`, etiqueta «Crear / Ver», casilla (`ToggleCompletado`) presente, sin «Acta de conformidad» en la lista, y sin enlaces a `/paquetes-trabajo` ni `/plan-maestro` fuera del checklist. | — |
| A4 | Conforme | `confirmar-transicion/route.ts` selecciona `catalogo_documentos(fase)` y gatea con `filasQueGatean`; comentarios obsoletos corregidos; CAS de la transición y bootstrap sin tocar. Lectura crítica del archivo + prueba verde de los dos sentidos en `acciones-checklist.test.ts` (todo lo demás completo → cierra; un ítem de AL_INICIO pendiente → no cierra). **No se ejecutó la transición real en PS-0006.** | — |
| A5 | Conforme | `editor-checklist.tsx` filtra `fase !== 'CIERRE'` en el fetch; `checklist/route.ts` GET con `.neq('fase','CIERRE')` y PATCH que rechaza agregar ítems de cierre con 400. Evidencia real con la fila `acta_conformidad` **creada en la base**: `GET …/checklist/editar` → `items de fase CIERRE en el editor = 0` (la fila existía y no se ofrece), `personalizados=0, usuarios=3`; `tsc` y `build` verdes. | — |
| A6 | Conforme | `documentos/[documentoId]` (POST) rechaza `grupo_accion='PANTALLA'` con 400. Smoke con script temporal **fuera** del repo y sesión sin navegador: subida a `cronograma` → **400** «Este documento se completa en la pantalla de su módulo, no subiendo un archivo»; botón muerto (`ot`) → **400** con el mismo mensaje; **control** grupo ARCHIVO sin archivo → 400 «Falta el archivo» (el corte nuevo no bloquea el Grupo A). | — |
| A7 | Conforme | Consulta de solo lectura: `A7 filas del Grupo B con archivo_ruta: 0` → **no hay nada que Victor elimine en el Gate 1 (Q2)**. No se borró nada. | — |
| A8 | Conforme | En el carril: `npm test` → 100 archivos / **1043 tests OK**; `npx tsc --noEmit` → **exit 0**; `npm run lint` → **27 problems (9 errors, 18 warnings)**, idéntico al baseline de `main` (sin deuda nueva); `npx next build --webpack` → **exit 0** (incluye `/proyectos/[id]`, `/proyectos/[id]/checklist/editar` y las rutas API). `next build` con Turbopack (por defecto) **falla por entorno** — ver hallazgo A-H2. | — |

## Rama, commits y archivos tocados

- **Rama:** `local-worker-1` (base `ce5623e`), no `main`.
- **Commits:** `c219069` — grupos de acción del catálogo (O5) y render delegado en la lista (`db/089_checklist_grupos.sql`, `page.tsx`, `acciones-checklist.ts`, `acciones-checklist.test.ts`); `af60e85` — gate de cierre sin fase CIERRE, editor sin ítems de cierre y rechazo de subida al Grupo B (`confirmar-transicion/route.ts`, `documentos/[documentoId]/route.ts`, `checklist/route.ts`, `editor-checklist.tsx`).
- **Verificación de rama:** `git branch --contains af60e85` → `* local-worker-1`; `git log --oneline -6` muestra los dos commits sobre `ce5623e`.
- **Archivos tocados:** los 8 dueños de la fila de `00-indice-de-tandas.md`. Ningún archivo prohibido.
- **Estado final:** `git status --short` limpio (solo ignorados: `.env.local`, `.next/`, `node_modules/`, `tsconfig.tsbuildinfo`).
- **Push:** `git push -u origin local-worker-1` → exit 0 (rama nueva en `origin`, sin tocar `main`).
- **Limpieza:** dev server 3111 detenido; script temporal de migración/smoke y HTML de evidencia borrados; candado de migraciones (`resultados/CANDADO-MIGRACIONES.txt`) borrado; semillas de prueba retiradas — PS-0006 volvió a sus 4 filas originales (`alcance`, `presupuesto_proyecto`, `dp`, `pr`), ninguna con archivo.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| A-H1 | conflicto con un flujo o pregunta para el Responsable humano | En `page.tsx` (línea de `doc.roles as {clave}\|null ?? catalogo?.roles.clave`) falta la segunda interrogation de cadena: si una fila de `cronograma`/`paquete_trabajo`/`plan_maestro` no trae `rol_responsable_id`, el catálogo de esas 3 claves lo tiene `NULL` (desde la 087) y el SSR de `/proyectos/[id]` revienta con `TypeError: Cannot read properties of null (reading 'clave')` (lo vi al sembrar filas sin responsable; el editor, en cambio, siempre guarda responsable concreto + rol, y el bootstrap de CIERRE solo crea el acta, cuyo rol de catálogo sí es `7`). Hoy **no es alcanzable por la aplicación**, pero la página se caería entera si algún día aparece una fila así. | Pregunta a Victor: ¿hacemos nulo-safe esa expresión en esta misma tanda (cambio de una línea en un archivo dueño) o lo dejamos para otro plan? No lo toqué sin su visto bueno. |
| A-H2 | mejora de trabajo | En un worktree `next build` (Turbopack, por defecto en Next 16) falla con `Symlink [project]/node_modules is invalid, it points out of the filesystem root` porque el `node_modules` vive en la raíz del repo, fuera del worktree; `next build --webpack` sí compila. | Al cerrar el plan: archivo nuevo en `docs/03-aprendizaje-continuo/` con el workaround (usar `--webpack` en worktrees). |
| A-H3 | mejora de trabajo | Para evidenciar SSR/API sin navegador: login por `POST /auth/v1/token?grant_type=password` y cookie `sb-…-auth-token` armada como la hace `@supabase/ssr` (`base64-` + base64url + `createChunks`), en un script temporal fuera del repo; sirve para A3, A5 y A6 de una sola corrida. | Al cerrar el plan: mismo archivo de aprendizaje de A-H2 (técnicas de evidencia sin navegador). |
| A-H4 | archivo o carpeta huérfano | No se detectaron archivos ni carpetas huérfanos en los archivos que toqué. | — |

## Traspaso

- Hecho: A1–A8 todos `Conforme`; 089 aplicada y verificada en producción de la app; código en `local-worker-1` con 2 commits y **push a `origin/local-worker-1`**.
- Verificación final: `npm test` 100/1043 OK · `npx tsc --noEmit` exit 0 · `npm run lint` 27 (9E/18W) = baseline de `main` · `npx next build --webpack` exit 0.
- Queda limpio: PS-0006 sin filas de prueba, sin candado de migraciones, sin dev server, sin scripts temporales.
- Pendiente de decisión: A-H1 (nulo-safe en `page.tsx`) — esperando a Victor.
- No toqué (por estar prohibido): `db/README.md` (queda documentar la 089), flujos 12/14, matriz de permisos, plan, progreso y evidencia.
- El Orquestador pasa A-H1…A-H3 al libro de hallazgos del plan y mide llamadas/contexto con su script.

## Llamadas y contexto

Aproximadamente 70 llamadas de herramientas en la sesión completa de la tanda (de ellas ~18 en esta última continuación de cierre). Las cifras exactas las mide el Orquestador con el script de medición.

## Skills revisados

- `pg_control_proyectos/.claude/skills/`: **`cerrar-tanda`** — usado en este cierre (pasos 1, 3 y 4 volcados en este archivo: estado de ítems, evidencia y traspaso); **`seguir-flujo-de-planes`** — referencia del flujo y de las puertas (Gate 1 aprobado antes de empezar); **`trasladar-hallazgos`** — no aplica (es el cierre de documentación de un plan, no la tanda de un Worker; los hallazgos los traslada el Orquestador); **`verificar-permisos-por-rol`** — no aplica: ningún cambio de permisos, menús ni accesos (D5 reutiliza permisos existentes).
- App hermana: **no tiene carpeta `.claude/skills`** (verificado).

## Fuentes de verdad revisadas

- **Actualizadas:** ninguna fuente central (este rol no edita flujos, estándar ni matriz de permisos). Se actualizaron solo archivos dueños de la tanda.
- **Pendientes de decisión:** documentar la migración 089 en `db/README.md` (archivo prohibido para este rol); registrar en el flujo 12 la regla de O7 (fase `CIERRE` oculta, no borrada) y que la subida en servidor solo aplica al Grupo A (A6); confirmar si la D5 (gateo por permiso de pantalla) exige alguna nota en el flujo 14 — hoy no cambia la matriz porque reutiliza permisos existentes; resolver A-H1.
