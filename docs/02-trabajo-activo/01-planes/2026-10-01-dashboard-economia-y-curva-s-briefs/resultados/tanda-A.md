# Cierre de tanda — Tanda A · Permisos y accesos

## Tanda, rol y modelo

- Tanda **A**, ola única, carril único `local-worker-5`.
- Worker 1 (código), modelo **DeepSeek V4.1 Flash** (`opencode/deepseek-v4.1-flash`).
- Repo de código: `py_control_proyectos_web`, worktree `...\.worktrees\local-worker-5`.

## Estado de los ítems

| ID | Estado (`Conforme` / `Observado` / `No aplica`) | Evidencia: comando o pantalla y resultado real | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| F01 | Observado | `npm test` verde: `puedeVerDashboard` = 13 roles y false sin rol conocido (`permisos.test.ts`). El chip del panel deriva del registro (`panel-derecho.ts`/`panel-izquierdo.ts` usan `acceso.permiso`). | Falta la captura/inspección del chip por rol, que exige navegador: **Fase D**. Checklist D: chip Dashboard activo para los 13 roles; sin rol conocido, chip deshabilitado con título y sin `href`. |
| F02 | Observado | `puedeVerCurvaS` = 13 roles; `puedeVerCurvaSEconomica` = solo los 5 con economía (`permisos.test.ts`). Chip Curva S deriva de `puedeVerCurvaS`. | Captura del chip por rol → **Fase D**. Checklist D: chip activo 13 roles; `puedeVerCurvaSEconomica` en la pantalla (C). |
| P01 | Conforme | `npx vitest run src/lib/permisos/permisos.test.ts …` → 108/108; suite completa 1051/1051. `puedeVerEconomia` intacta (5 roles). | — |
| P02 | Conforme | `matriz-accesos.test.ts`: `derivarMatrizAccesos()` vs `MATRIZ_BASE_FLUJO14` = 0 diferencias (base `dashboard` y `curva-s` → 13 roles). | — |
| P03 | Observado | Flujo 14 **no** se editó (Fase E). En `permisos.test.ts` se retiraron `Dashboard del servicio` y `Curva S` del mapa que compara contra el archivo (7→5 filas, 65 celdas) y se añadieron pruebas explícitas del modo físico/económico. | La comparación fila-por-fila contra el archivo para esas dos filas se recupera en **Fase E**, cuando el flujo 14 tenga la semántica Parcial/Completo. Resuelve: Fase E. |
| P04 | Conforme | `permissions.test.ts` prueba alcance por OT para Dashboard y Curva S física (OT ajena = false, OT propia = true, admin salta el alcance). La API `GET /api/curva-s` sigue usando `validarEscrituraProyecto(proyectoId, …)` sin debilitar el alcance. | — |
| V03 | Observado | Revisión del PATCH `src/app/api/proyectos/[id]/tipo-dashboard/route.ts`: sigue exigiendo `puedeVerEconomia` (sin cambio). La página fuerza Parcial en servidor (`tipo_dashboard==='COMPLETO' && puedeEditarTipo`). | La prueba "rol sin economía forzando la ruta" es en vivo → **Fase D**. Checklist D: con BD en `COMPLETO`, rol sin economía abre Parcial y el PATCH responde 403. |
| V04 | Observado | Guards intactos: `validarEscrituraProyecto` (401 sin sesión, 403 sin rol, 403 sin OT) sin cambios; la página conserva el rechazo sin sesión/sin alcance. Solo cambia la función de permiso de Dashboard a 13 roles (por diseño D1). | Prueba sin sesión y con OT ajena en vivo → **Fase D**. Checklist D: 401 sin sesión, 403 con OT ajena, en Dashboard y API de Curva S. |
| F06 (parte A) | Observado | `ToggleTipoDashboard.tsx`: el interruptor se renderiza siempre; para rol sin economía cada opción va `disabled` con `title` ("Solo los roles con datos económicos pueden alternar…"). Ya no hay etiqueta fija. | Inspección DOM/captura → **Fase D**. Checklist D: control visible en ambos casos; no clickeable sin economía; `title` presente. |
| U02 (parte A) | Observado | Mismo cambio: opciones deshabilitadas **visibles** con `title` que explica el permiso (nunca ocultas). | Inspección DOM → **Fase D**. Checklist D: opciones visibles y deshabilitadas con título en rol sin economía. |

## Rama, commits y archivos tocados

- Rama `local-worker-5` (worktree `.worktrees/local-worker-5`). Commit de la tanda: **`d40cd74`** (padre `5e8420b`).
- Verificación de rama: `git branch --contains d40cd74` → `* local-worker-5` (solo esa). Sin push ni merge. `git status` limpio tras el commit.
- Archivos tocados (todos con `git add <ruta>` explícito):
  - `src/lib/permisos/permisos.ts`
  - `src/lib/permisos/permisos.test.ts`
  - `src/lib/config/matriz-base-flujo14.ts`
  - `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`
  - `src/components/dashboard/ToggleTipoDashboard.tsx`
  - `registro-accesos.ts`: **sin cambio**: los chips Dashboard y Curva S derivan de `puedeVerDashboard`/`puedeVerCurvaS`, que ya se actualizaron; por eso F01/F02 se cumplen sin tocarlo.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| A-H1 | mejora de trabajo | `permisos.test.ts` compara la tabla 1 del flujo 14 leyendo el archivo por ruta absoluta; al mover los permisos antes que el doc, esa comparación quedaba roja entre A y E. Se separó: mapa reducido a las filas que siguen rigiéndose por la columna económica + pruebas explícitas de los dos modos. | `docs/03-aprendizaje-continuo/` (nota de método) + recordatorio a Fase E para re-añadir las filas. |
| A-H2 | observación sobre la política | P03/R2 anticipan un carril con `npm test` rojo entre A y E, mientras las 00-reglas exigen tests verdes. La tensión se resolvió ajustando el mapa de la prueba en A (permitido por R2) sin tocar el flujo. | Lo clasifica el Auditor; decide Victor en Gate 2. |
| A-H3 | archivo o carpeta huérfano | Ninguno detectado en esta tanda. | — |
| A-H4 | conflicto con un flujo o pregunta | Ninguno: las tablas 1 y 2 del flujo 14 no deciden las filas nuevas (Parcial físico 13 / Completo económico 5); esa redacción es la Fase E, ya decidida (D1/D3/PD3), no una duda abierta. | Fase E / Documentador. |

## Traspaso

- P01/P02/P04 Conforme. F01/F02/V03/V04/F06-A/U02-A con permiso y código listos; la verificación en vivo (capturas, DOM, 401/403, forzar ruta) es de **Fase D**.
- P03: el flujo 14 no se tocó (Fase E). La prueba quedó verde; en E se re-añaden Dashboard y Curva S al mapa fila-por-fila con semántica Parcial/Completo.
- Entre A y C la API `GET /api/curva-s` sirve la serie económica a los 13 roles (el contrato `?modo=` + 403 es PD2, Fase C). Estado intermedio **previsto por el plan**; no se tocó por no estar en el alcance de A.
- `puedeVerCurvaSEconomica` queda exportada sin consumidores hasta la Fase C (selector/API).
- Comandos: `npx vitest run` = 101 archivos / 1051 tests verdes; `npx tsc --noEmit` = 0; `npm run lint` = 27 problemas (9 error / 18 warning) = igual al baseline medido en `main`.
- Pendiente de D: capturas por rol, DOM del interruptor, 401/403 en vivo.
- Pendiente de E: reescribir las filas Dashboard/Curva S del flujo 14 y devolver esas filas al mapa de `permisos.test.ts`.

## Llamadas y contexto

- Llamadas aproximadas: **~52** (lectura, edición, verificación y cierre).

## Skills revisados

- `pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`, `trasladar-hallazgos`. Usados: `cerrar-tanda` (secuencia de cierre) y `verificar-permisos-por-rol` en **modo estático** (esperado = tablas/D1/PD3 vs `permisos.ts` + pruebas; la verificación en vivo con «Ver como» es de Fase D).
- Repo de la app (`py_control_proyectos_web`): **no tiene** carpeta `.claude/skills` (comprobado). No aplica.
- `seguir-flujo-de-planes` y `trasladar-hallazgos`: del Orquestador/Documentador, no de esta tanda.

## Fuentes de verdad revisadas

- Revisadas (solo lectura, sin editar): `docs/04-flujos-de-negocio/14-accesos-y-restricciones.md` (tablas 1 y 2, notas ¹ y 9–10), plan `2026-10-01-dashboard-economia-y-curva-s.md` (ítems por ID) y `00-reglas-de-contexto.md`.
- Pendientes de actualización (no las edita el Worker): filas «Dashboard del servicio (Parcial y Completo)» y «Curva S» de la tabla 1 del flujo 14 → **Fase E**; artefacto «Matriz de permisos» → lo actualiza Victor.
- `permisos.ts` ↔ flujo 14: coincidencia fila por fila salvo Dashboard/Curva S (objetivo del plan, no brecha).
