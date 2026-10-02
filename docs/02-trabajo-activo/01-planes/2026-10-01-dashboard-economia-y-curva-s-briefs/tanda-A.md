# Brief — Tanda A · Permisos y accesos (Dashboard 13 roles · Curva S dos modos)

## Rol, modelo y tanda

Worker 1 (código) · modelo **DeepSeek V4.1 Flash** (`opencode/deepseek-v4.1-flash`) · tanda **A**, ola única, carril único `local-worker-5`. Se lanza como subagente «Worker 1 · A».

## Ítems de la tanda (Punch List del plan)

| ID | Ítem | Evidencia mínima |
|---|---|---|
| F01 | Chip «Dashboard» habilitado para los 13 roles (`puedeVerDashboard` + `registro-accesos`), con alcance por OT; sin permiso, deshabilitado con título y sin enlace | Tests + captura/inspección del chip por rol |
| F02 | Chip «Curva S» habilitado para los 13 roles; `puedeVerCurvaSEconomica` devuelve true solo a los 5 con economía | Tests |
| P01 | `permisos.ts`: `puedeVerDashboard` y `puedeVerCurvaS` a los 13 roles; nuevo `puedeVerCurvaSEconomica` = 5; sin rol conocido → false; `puedeVerEconomia` intacto | `npm test` (`permisos.test.ts`) |
| P02 | `registro-accesos.ts` y `matriz-base-flujo14.ts` coherentes: matriz derivada vs base con 0 diferencias | `matriz-accesos.test.ts` |
| P03 | Las pruebas que leen la tabla 1 del flujo 14 por ruta absoluta quedan coherentes con el flujo 14 (Fase E). **En A no edites el flujo 14**: deja anotado en tu resultado cómo queda el test y si quedará rojo hasta E | Nota + `npm test` |
| P04 | Alcance por OT intacto en Dashboard y Curva S (pantalla y API), con bypass del administrador como hoy | Prueba con OT ajena y admin |
| V03 | La página del Dashboard valida rol y alcance en servidor; el PATCH de `tipo-dashboard` sigue exigiendo `puedeVerEconomia` (sin cambio) | Prueba forzando la ruta + revisión del PATCH |
| V04 | Sin sesión o sin alcance: rechazo igual que antes (los guards no se debilitan) | Prueba sin sesión y con OT ajena |
| F06 (parte A) | Interruptor Parcial/Completo: se ve en ambos casos; para rol sin economía queda **deshabilitado con `title`** (D3) | Inspección DOM/captura |
| U02 (parte A) | Opciones deshabilitadas **visibles** con `title` que explica el permiso | Inspección DOM |

Decisiones ya resueltas que afectan a A: **D1** (chip Curva S a 13 roles), **D3** (interruptor visible pero deshabilitado), **PD3** (permisos y Parcial forzado en servidor), **PD4** (selector al patrón de `ToggleTipoDashboard`, `disabled` + `title`, nunca oculto).

## Rama, worktree y puerto

- Rama `local-worker-5`; worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-5`; puerto dev 3115 (en A **no** se usa navegador).
- `node_modules` = junction al repo principal (dev/build con `--webpack`). `.env.local` ya copiado: no lo leas ni muestres.

## Qué leer, y qué no

1. Este brief y `00-reglas-de-contexto.md`.
2. App: `AGENTS.md` y `CLAUDE.md` enteros.
3. `docs/04-flujos-de-negocio/14-accesos-y-restricciones.md` — solo tablas 1 y 2 y notas ¹ y 9–10 (una vez).
4. Código: `src/lib/permisos/permisos.ts` y `permisos.test.ts`; `src/lib/config/registro-accesos.ts` y `registro-accesos.test.ts`; `src/lib/config/matriz-base-flujo14.ts` y `matriz-accesos.test.ts`; `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`; `src/components/dashboard/ToggleTipoDashboard.tsx`.
5. Del plan (`../2026-10-01-dashboard-economia-y-curva-s.md`): solo ítems por **Grep de su ID**.

**No leer**: el plan completo, progreso/evidencia completos, ni los flujos 11/16/21 (son de B–E).

## Qué puede trabajar

Editar **solo** esos archivos. Crear: `...-dashboard-economia-y-curva-s-briefs/resultados/tanda-A.md`.
**No tocar**: `docs/04-flujos-de-negocio/**` (Fase E), `docs/02-trabajo-activo/**`, `db/**`, `evm.ts`, `dashboard.ts`, `curva-s.ts` (motor) ni componentes de gráficos (fases B/C).

## Dónde deja entrega y evidencia

- Código: commit en `local-worker-5` (`git add` explícito; **sin push ni merge**).
- Resumen: `...-briefs/resultados/tanda-A.md` (plantilla `12-resumen-de-cierre-de-tanda.md`): estados de tus ítems, handoff ≤15 líneas, número de llamadas, hallazgos (mejoras, reglas de negocio, huérfanos).

## Contrato técnico verificado (2026-10-02, `main` = `5e8420b`)

- `src/lib/permisos/permisos.ts`: `puedeVerEconomia` (l.246); `puedeVerDashboard` (l.256) hoy `return puedeVerEconomia(rolesUsuario)`; `puedeVerCurvaS` (l.414) hoy `return puedeVerEconomia(rolesUsuario)`; `puedeVerDashboardPortafolio` (l.260). El arreglo de roles es `Rol[]` (léelo arriba del archivo). Los 5 con economía (confirmar nombres exactos en el código): administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos, jefe de costos.
- `registro-accesos.ts`, `matriz-base-flujo14.ts` y sus pruebas existen (verificado).
- `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx` y `src/components/dashboard/ToggleTipoDashboard.tsx` existen (verificado).

## Skills que debe usar

- `cerrar-tanda` al final.
- `verificar-permisos-por-rol` en **modo estático** (esperado vs código + pruebas), porque A no usa navegador.

## Límites

~80 llamadas (a las ~60 cierra lo que tiene y escribe el handoff). Sin navegador. Sin migraciones. Sin push/merge. Una captura por ítem si aplica.

## Cómo registra hallazgos y preguntas

Todo va a `resultados/tanda-A.md` en los grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos). Conflicto con un flujo o un permiso no decidido → **detente y devuélvelo al Orquestador**; no sigas con el conflicto abierto.

## Criterios de salida

- `puedeVerDashboard` y `puedeVerCurvaS` = 13 roles; `puedeVerCurvaSEconomica` = 5; `puedeVerEconomia` sin cambio.
- Registro de accesos y matriz coherentes (0 diferencias); pruebas de los módulos tocados verdes; `npx tsc --noEmit` = 0; lint igual al de `main` (línea base medida, no cero).
- Dashboard fuerza Parcial en servidor si el rol no tiene economía; PATCH de `tipo-dashboard` sin cambio; guards sin debilitar.
- Interruptor Parcial/Completo visible y deshabilitado con `title` para rol sin economía.
- Commit en la rama y `resultados/tanda-A.md` escrito.
