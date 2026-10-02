# Evidencia — Observaciones de Victor (Lote 2: acciones del checklist O5, cronograma O6 y acta de conformidad O7)

> **Archivo final** (creado el 2026-10-02 en la Tanda D del Lote 2, ítems D1/D2/D3; completado al cierre con la tanda B y C1). Recoge la evidencia real de las tandas A, B y D.

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
| B1 | Reproducir el fallo con `scripts/smoke-cronograma.mjs` y `soloAnalizar=true` en los dos archivos | Ejecución real contra `npm run dev -- --webpack -p 3112` sobre PS-0007 | Los dos archivos reales devuelven **HTTP 200** con propuesta completa (PDF: 3 niveles/74 filas; XLSX: 2 niveles/13 filas); las variantes inválidas imprimen la pantalla real con `traducirErrorApi` | Conforme | `briefs/resultados/B.md` § «Evidencia de smokes» | Worker 2 |
| B2 | Aislar la causa raíz con `exceljs` y `PDFParse` sobre los archivos reales | Diagnóstico escrito (formato, fase y mensaje) | Parsers **sanos** (XLSX 14 act., PDF 78 act., 0 incompletas); el fallo estaba en 3 fases ajenas al parser: sesión caducada (HTML sin `error`), prefijo técnico en `traducir-error` y 500 por uuid inválido | Conforme | `briefs/resultados/B.md` § «Diagnóstico de causa raíz» | Worker 2 |
| B3 | Corregir la causa raíz | Diff + `tsc` | `esIdProyectoValido` en el POST → 400 «El N° OT del servicio no es válido» (antes 500 crudo de Postgres); prefijo técnico quitado en `traducir-error.ts`; detección de respuesta no JSON en el formulario | Conforme | `briefs/resultados/B.md` §§ B3/B5 | Worker 2 |
| B4 | Loguear **todos** los caminos de fallo con formato, nombre y mensaje | Salida del log en la prueba de fallo | `logFalloImportacion` en **17 caminos** del POST + `catch` de lectura y global, con etapa + formato + nombre de archivo + mensaje; salida real del `dev-3112.log` | Conforme | `briefs/resultados/B.md` § «log en servidor» | Worker 2 |
| B5 | `traducir-error.ts` sin fallback genérico + fallback real en `FormularioCronograma.tsx` + test | `npm test` + smoke de fallo | `traducir-error.ts:26-27` quita el prefijo técnico y conserva el motivo; `FormularioCronograma.tsx:151,186` con fallback real; test nuevo `traducir-error.test.ts` 4/4 | Conforme | `briefs/resultados/B.md` § B5 | Worker 2 |
| B6 | Smoke de éxito de punta a punta + smoke de fallo con motivo en pantalla y log | Salidas de ambos smokes | Sobre **PS-0007** (creado con R7): éxito XLSX 14 act. y PDF 78 act. con `extraccionCompleta: true` y persistencia verificada; 6 fallos con motivo específico y log; **PS-0004/PS-0006 sin escrituras** | Conforme | `briefs/resultados/B.md` §§ «Evidencia de smokes» y B4 | Worker 2 |
| B7 | `npm test` / `tsc` / `lint` / build verdes en el carril 2 | Ejecución en el carril | **100 archivos / 1030 tests OK · `tsc` exit 0 · lint 27 (9E/18W) = baseline, 0 en archivos propios · `npx next build --webpack` exit 0** | Conforme | `briefs/resultados/B.md` § B7 | Worker 2 |
| C1 | `db/README.md` con la fila `089`; ramas integradas; `git status` limpio | Diff + git | Fila `089` en `db/README.md` (commit `3a393d5`, carril 1); ambos carriles mergeados a `main` tras el Gate 2; `git status` limpio y `main` = `origin/main` (`0/0`) | Conforme | Mensaje de cierre del plan | Integración (Orquestador) |
| D1 | Fila del Lote 2 («En ejecución») en `01-planes/README.md` | Diff | Fila añadida arriba de la del Lote 1, en la tabla «En ejecución» | Conforme | Commit de esta tanda | Documentador |
| D2 | Flujos 12, 08, 15 (+14 aprobado) e índices según la tabla del Gate 1 | Diff + casilla «aplicado» | Escritos: `12-checklist.md` (columna «Grupo / acción», sección «Grupos de acción (O5)», RB1–RB3, acta fuera de la lista), `08-…` (CIERRE no cuenta), `15-cronograma.md` (RB4), `14-…` (fila 74, nota 4, actualización Gate 1; **artefacto «Matriz de permisos»: lo edita Victor**), índice `04-flujos-de-negocio/README.md`. La casilla «aplicado» del plan se marca al cerrar D2/D4 | Conforme (edición hecha; casilla del plan pendiente de marcar) | Diff de esta tanda | Documentador |
| D3 | Progreso y evidencia del Lote 1 con su contenido real + nota del smoke de O4 | Dos archivos nuevos | `02-progreso/2026-10-02-observaciones-victor.md` y `03-evidencia/2026-10-02-observaciones-victor.md` creados: estado Cerrada, commits, SQL aplicados por Victor, decisiones, y la nota de que **el smoke de O4 nunca se hizo** (su evidencia vive en la homónima del Lote 2) | Conforme | Los dos archivos nuevos | Documentador |
| D4 | Trasladar el libro de hallazgos + `verificar-referencias.py` sin rotos | Traslado por filas (Skill `trasladar-hallazgos`) + ejecución del verificador | **MB1–MB3** → archivo nuevo [`03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md`](../../03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md) (3 secciones, una por hallazgo, con origen y fecha) + fila en el índice de `03-aprendizaje-continuo/README.md`, commit `903033e`. **RB1–RB4** → `Trasladada` con enlace y commit `7100179`, texto **verificado abriendo el destino**: `12-checklist.md` (columna «Grupo / acción», Grupos de acción, «Ítems sin pantalla todavía (RB2)», acta fuera de la lista), `08-programa-portafolio-proyecto.md` (CIERRE no cuenta), `15-cronograma.md` (regla RB4). **OP1–OP5 sin tocar** (`Registrada`, las clasifica el Auditor); huérfanos: ninguno. Verificador: por defecto **44 archivos, 0 huérfanos, 0 enlaces rotos, exit 0**; alcance Lote 2 (plan + briefs + homónimos) **0/0 exit 0**; alcance `03-aprendizaje-continuo` **0/0**. Punch D4 → `Conforme` | Conforme | Archivo de aprendizaje + índice; estados en el plan; salidas del verificador (recogidas en el plan D4 y en el handoff del progreso) | Documentador (tanda D4) |

## Enlace al artifact de checklist visual

**https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd** — «El checklist de cada lote de implementación» (estado vivo de los ítems). Coexiste con este archivo: el artefacto guarda el estado mientras se prueba; este `.md` y la Punch List del plan registran el resultado en texto y en git.

## Resultados de pruebas técnicas

- Carril 1 (`local-worker-1`): `npm test` **100 / 1043 OK** · `npx tsc --noEmit` **exit 0** · `npm run lint` **27 (9E/18W) = baseline** · `npx next build --webpack` **exit 0**.
- Carril 2 (`local-worker-2`): `npm test` **100 / 1030 OK** · `npx tsc --noEmit` **exit 0** · `npm run lint` **27 (9E/18W)**, 0 en archivos propios · `npx next build --webpack` **exit 0**.
- Migración `089`: aplicada y verificada con conteos antes/después (A1).
- Evidencia SSR/API **sin navegador** (patrón password grant + cookie Supabase) para A3, A5 y A6.
- Verificador de referencias (tanda D4): `python scripts/verificar-referencias.py` → **0 huérfanos / 0 enlaces rotos, exit 0** (44 archivos del núcleo); mismos 0/0 en el alcance del Lote 2 (plan + briefs + homónimos) y en `docs/03-aprendizaje-continuo`.

## Verificación en PRODUCCIÓN (2026-10-02, tras el despliegue)

La evidencia de arriba es de smokes **locales** (`npm run dev`). Victor probó después en la app desplegada (`py-control-proyectos-web.vercel.app`, proyecto real PS-0008, PDF `CRON-PROMCOSER-AESA-001.pdf`) y reportó que **seguía sin importar** («El servidor respondió sin JSON (HTTP 500)») → observación **O8** en el Spec. El riesgo R6 («Smoke local ≠ Vercel») se materializó: el parser estaba sano pero la **ruta entera** crasgaba al cargar el módulo en la función serverless.

### Diagnóstico en producción (sin navegador, mismo mecanismo MB2)

- Con credencial de prueba, `GET https://…/api/cronograma?proyectoId=<uuid>` → **HTTP 500, `content-length: 0`, sin `content-type`** (no es el `error` JSON de la ruta: la ruta no llegó a ejecutarse).
- `GET …/api/cronograma/plantilla` (solo `exceljs`, **sin** `pdf-parse`) → **200** con el .xlsx. El único importador que distingue a la ruta rota es `import { PDFParse } from 'pdf-parse'`.
- Conclusión: fallo **al cargar el módulo**, no al leer el archivo. Por eso afectaba igual a Excel y a PDF, y al GET de lectura.

### Cadena de causa raíz

`pdf-parse@2.4.5` → `pdfjs-dist/legacy/build/pdf.mjs`: para polifillar `globalThis.DOMMatrix` hace `createRequire(import.meta.url)("@napi-rs/canvas")`. `@napi-rs/canvas` carga su binario nativo por plataforma con `require` **dinámico** (`js-binding.js` → `@napi-rs/canvas-linux-x64-gnu`, ~31 MB). El trazador de archivos de Vercel no ve ese `require` dinámico → el binario queda **fuera** de la función → el polifill no carga → `pdf.mjs` ejecuta `new DOMMatrix()` **sin guarda a nivel de módulo** → `ReferenceError: DOMMatrix is not defined` al importar. Con `pdf-parse` importado arriba del todo, esto mataba la ruta completa (GET + Excel + PDF). Idéntico patrón al de `pdfkit` (`.afm`), ya comentado en `next.config.ts`.

### Corrección (Worker, 2026-10-02, autorizada por Victor para llegar a producción)

| Commit | Qué | Evidencia |
|---|---|---|
| `00a161b` | `await import('pdf-parse')` **perezoso** dentro de la rama PDF (fuera del import estático de cabecera). Aísla el fallo: deja vivos GET y Excel, y si el import volviera a fallar cae en el `catch` y devuelve **400 con motivo** (RB4) en vez de un 500 vacío. | `src/app/api/cronograma/route.ts:378` |
| `35ac5dd` | `outputFileTracingIncludes` para `pdf-parse` (cjs+esm, sin `.map`), `pdfjs-dist/legacy/build/pdf.mjs`+`pdf.worker.mjs` y **`@napi-rs/canvas*`** (los paquetes por plataforma son `optionalDependencies`: en el build de Vercel solo existe el `-linux-x64-gnu`). | `next.config.ts:22-45` |
| — | `scripts/smoke-cronograma.mjs`: opción `--base` (poder golpear la URL desplegada) y volcado del cuerpo crudo cuando la respuesta no es JSON. | salida abajo |

### Verificación tras el despliegue automático de Vercel

Comandos contra `--base https://py-control-proyectos-web.vercel.app`:

| Prueba | Resultado |
|---|---|
| `GET /api/cronograma?proyectoId=<PS-0008>` | **200** `application/json` (antes 500 vacío) |
| PDF `CRON-PROMCOSER-AESA-001.pdf`, `soloAnalizar` (PS-0008, real, **sin guardar**) | **200** · propuesta 3 niveles / 74 filas de encabezado |
| XLSX `Cron-prueba N°01.xlsx`, `soloAnalizar` (PS-0008, real, sin guardar) | **200** · propuesta 2 niveles / 13 filas |
| Guardado real XLSX (PS-0007 «PRUEBA-CRONO», servicio de prueba) | **200** · informe `totalActividades=14 tareas=10 resumenes=4 hitos=0` |
| Lectura devuelta PS-0007 | «Cron-prueba_N_01.xlsx (excel), 14 actividades» — persistencia confirmada |
| PDF `CRON-PROMCOSER-AESA-001.pdf`, `soloAnalizar` (PS-0007, prueba) | **200** · propuesta 3 niveles / 74 filas, servicio mostrado «PRUEBA-CRONO Importacion de cronograma» |

**Cero escrituras en servicios reales** (PS-0008 solo con `soloAnalizar=true`); las escrituras de prueba van a PS-0007 (servicio dedicado `PRUEBA-CRONO`, igual que la tanda B). Suite verde local: `npm test` **101 / 1047 OK**, `tsc` exit 0, build exit 0; `eslint` exit 0 en los archivos tocados.

> **Regla que deja O8 (para el traslado):** un smoke local **no** valida una función serverless de Vercel cuando hay dependencias con `require` dinámico o binarios por plataforma (`@napi-rs/canvas`, `pdfkit`, `pdfjs-dist`). Antes de cerrar cualquier cosa que toque parser/binario, hay que (a) ejecutar el smoke contra `--base` **desplegado** y (b) confirmar el trazado con `outputFileTracingIncludes` o `npx vercel build`. La verificación de Victor en la app desplegada pasa a ser **obligatoria**, no un "pendiente de R6".

## Regresiones verificadas

- Gate de cierre probado en **ambos sentidos** (no cierra con ítem de AL_INICIO pendiente; cierra con todo lo demás completo), sin ejecutar transición real.
- El Grupo A siguió subiendo (control 400 «Falta el archivo») después del rechazo al Grupo B.
- `checklist.ts` **no se tocó** (`checklistCompleto` conserva su contrato); el filtro de fase está en quien lo llama.
- Cero escrituras en servicios reales durante la tanda B (solo GET y `soloAnalizar=true`).

## Limitaciones o casos no verificables

1. La transición real de fase (A4) no se ejecutó en ningún proyecto (solo prueba de ambos sentidos en test).
2. El build con Turbopack (por defecto) no funciona en worktrees (MB1); se usó `--webpack`.
3. La verificación final en la app desplegada (R6) queda a cargo de Victor tras el push del merge.
6. **Reportado sin tocar (tanda D4):** corrido sobre el alcance completo `docs/02-trabajo-activo` (163 archivos), el verificador devuelve 15 huérfanos y 20 enlaces rotos **preexistentes** de planes antiguos (2026-09-20/21, rutas `../Flujos de trabajo/…` de antes de la reestructuración documental) más 194 menciones sin archivo — ninguno pertenece a este plan; no se modificó ningún archivo ajeno.
