# Brief — Tanda C · Curva S con selector de dos modos (económica USD / avance físico %)

## Rol, modelo y tanda

Worker 1 (código) · modelo **DeepSeek V4.1 Flash** (`opencode-go/deepseek-v4.1-flash`) · tanda **C**, carril único `local-worker-5`. «Worker 1 · C». Depende de A (hecha) y B (hecha: commit `94a5f79`).

## Ítems de la tanda (Punch List del plan)

| ID | Ítem | Evidencia mínima |
|---|---|---|
| F09 | El selector de dos modos se ve siempre; «Económica (USD)» deshabilitada con `title` para rol sin economía; los dos activos para rol con economía | Inspección/captura (en vivo en D) |
| F10 | La curva física dibuja % planificado (PV/BAC) y % real (EV/BAC) con unidad rotulada, sin USD en eje, tooltips, tarjetas ni tabla | Inspección |
| F11 | Sin Plan Maestro aprobado: % planificado «Pendiente» (D5); % real dibujado con los RDT validados existentes | Inspección |
| D03 | Serie física en lógica pura con tests: PV/BAC y EV/BAC, BAC = 0 → sin serie, recorte al corte conservado, agrupación semanal intacta | `npm test` |
| D04 | Curva S sigue leyendo, no recalculando: sin cambios en `evm.ts`, `dashboard.ts` ni funciones SQL | Diff |
| U01 | Selector con `role="group"` y `aria-label`; opción no permitida accesible por teclado con `title` (no oculta, `aria-disabled`) | Inspección DOM |
| U04 | Un solo eje Y por modo con unidad rotulada; nunca % y USD en el mismo eje | Inspección (captura en D) |
| E01 | Sin PM: «Pendiente» en % planificado, sin curva PV inventada; sin RDT validados: serie real vacía con su nota | Inspección |
| E03 | Carga atenuada sin salto de layout; error de API con mensaje claro (patrón existente) | Revisión (D) |
| E04 | `modo=economica` sin permiso vía URL/API → 403 con mensaje; la interfaz nunca ofrece el modo | Llamada directa |
| V01 | `GET /api/curva-s?modo=economica` con rol sin economía → 403 aunque se fuerce; sin `modo` la respuesta es determinista por permiso | Llamada directa con las dos cuentas |
| V02 | La respuesta de `modo=fisica` no incluye montos USD ni `bac` | Cuerpo JSON revisado |

Decisiones que aplican: **PD2** (contrato `modo=`), **PD4** (selector al patrón `ToggleTipoDashboard`), **D5** (sin PM → «Pendiente»).

## Contrato `GET /api/curva-s` (PD2)

- Parámetro `modo=economica|fisica`.
- Sin `modo`: el servidor deriva `economica` si `puedeVerEconomia`, si no `fisica`.
- `modo=economica` exige `puedeVerCurvaSEconomica` (5 roles); si no, **403** (criterio 6).
- `modo=fisica` **no devuelve montos USD ni `bac`** (solo series en % y brecha en puntos porcentuales). No confiar en la query del navegador.

## Serie física (D03)

- `% planificado = PV / BAC` y `% real = EV / BAC`, sobre lo ya existente (`curva_s_proyecto`, `pr_partidas`, `plan_maestro_asignaciones`, RDT validado). Sin migración.
- `BAC = 0` → sin serie (no se divide).
- Recorte al corte y agrupación semanal intactos.
- Sin PM aprobado: la serie planificada muestra «Pendiente» (no se dibuja PV inventado); la real se dibuja con los RDT validados que existan.

## Rama, worktree y puerto

- Rama `local-worker-5`; worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-5`; puerto 3115 (C **no** usa navegador).

## Qué leer, y qué no

1. Este brief y `00-reglas-de-contexto.md`.
2. App: `AGENTS.md` y `CLAUDE.md`.
3. `docs/04-flujos-de-negocio/21-curva-s.md` (reglas y endpoint) y la fila de Curva S del flujo 14.
4. `docs/05-diseno-y-referencias/design.md` solo las secciones de selector/gráficos que uses.
5. Código: `src/components/curva-s/{PantallaCurvaS,GraficoCurvaS}.tsx`; `src/lib/curva-s/*`; `src/app/api/curva-s/route.ts`; `src/app/(workspace)/proyectos/[id]/curva-s/page.tsx`; `src/lib/permisos/permisos.ts` (solo leer `puedeVerCurvaSEconomica`).
6. Del plan: solo ítems por Grep de su ID.

**No leer**: el plan completo, progreso/evidencia completos, ni los flujos 11/16 completos.

## Qué puede trabajar

Editar: los cinco archivos de código de arriba. Crear: pruebas nuevas si hacen falta.
**No tocar**: `src/lib/evm.ts`, `src/lib/dashboard/dashboard.ts` (motor) · `src/lib/permisos/**` y `src/lib/config/**` (ya cerrados en A) · `db/**` · `docs/04-flujos-de-negocio/**` (E) · `docs/02-trabajo-activo/**`.

## Contrato técnico verificado (2026-10-02)

- Existen: `src/components/curva-s/GraficoCurvaS.tsx`, `PantallaCurvaS.tsx`; `src/lib/curva-s/curva-s.ts` (+test); `src/app/api/curva-s/route.ts`; `src/app/(workspace)/proyectos/[id]/curva-s/page.tsx`.
- `puedeVerCurvaSEconomica` ya existe (Fase A) y es igual a `puedeVerEconomia` (5 roles).

## Skills que debe usar

- `cerrar-tanda` al final.

## Límites

~80 llamadas. Sin navegador. Sin migraciones. Sin push/merge. Commit solo en `local-worker-5` (`git add` explícito).

## Cómo registra hallazgos y preguntas

A `resultados/tanda-C.md` en los grupos. Conflicto de negocio o permiso no decidido → detente y devuélvelo.

## Criterios de salida

- Selector visible en los dos casos; económica deshabilitada con `title` sin economía.
- Serie física en % (PV/BAC, EV/BAC) sin USD; sin PM → «Pendiente»; BAC=0 sin serie.
- `GET /api/curva-s?modo=economica` sin permiso → 403; `fisica` sin USD ni `bac`; sin `modo` determinista.
- `npm test` de los módulos tocados verde; `tsc` 0; lint igual al baseline de `main`.
- Commit en la rama y `resultados/tanda-C.md` escrito.
