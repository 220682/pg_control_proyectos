# F5B-A · Economía: funciones de permiso, PR y Dashboard del servicio (rol + alcance por OT)

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5B · **Depende de:** F5-A cerrada.
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-88 | `permisos.ts`: las funciones de ver de las interfaces sin economía permiten a los 13 roles (F2B); `puedeVerEconomia` cubre los cinco roles de la regla 2 como único punto de cambio y las específicas delegan en ella, con las excepciones del planner (Plan Maestro) y el supervisor de oficina técnica (DP) (F5B); `puedeVerRecursos` ya no es alias de `puedeVerApartadoProyectos`. Las pruebas unitarias recorren los 13 roles y comparan con la tabla 1 leída del flujo 14 | `npm test` + salida de la comparación |
| PL-89 | PR: los roles de la tabla 1 abren `/proyectos/<SV1>/pr` con datos; con "Ver como" un rol fuera (por ejemplo supervisor operativo) ve "No tienes acceso…" sin datos y sin error 500 | Capturas de los tres casos |
| PL-90 | Dashboard del servicio (Parcial y Completo): ídem PL-89 en `/proyectos/<SV1>/dashboard`; el interruptor Parcial/Completo (`ToggleTipoDashboard` y `PATCH /api/proyectos/[id]/tipo-dashboard`) sigue a `puedeVerEconomia`: lo activan los roles con datos económicos de la matriz y se comprueba por los dos lados (C35 resuelta por Victor el 2026-09-29; que los demás roles vean un Parcial sin economía es del plan futuro de `planes-futuros.md`) | Capturas |
| PL-125 | Las excepciones acotadas se aplican tal como quedaron aprobadas, en un solo lugar (`puedeVerEconomia` y las específicas): planner solo en Plan Maestro; supervisor de oficina técnica solo en DP (y sin importar); jefe de costos con economía; se comprueban por los dos lados con "Ver como" | Tabla por rol |
| PL-174 | PR (`/proyectos/[id]/pr`): un rol con permiso de economía pero sin esa OT asignada ve "No tienes acceso…" sin datos, igual que Curva S; con la OT asignada, abre normalmente | Capturas de los dos casos + SVX |
| PL-175 | Dashboard del servicio: mismo patrón que PL-174 en `/proyectos/[id]/dashboard` | Capturas + SVX |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Fuente de roles: tabla 1 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md` (leer del archivo). En `permisos.ts` crea (nombres propuestos): `puedeVerEconomia` = administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos (**único punto de cambio**), y las específicas que delegan en ella: `puedeVerDashboard`, `puedeVerDashboardPortafolio`, `puedeVerPr`, `puedeVerCurvaS` (hoy ~296 excluye al rol Asistente), `puedeVerDp` (economía + supervisor de oficina técnica), `puedeVerPlanMaestro` (hoy ~278; economía + planner), `puedeVerRegistroCostos` (economía; logística entra solo a subir). El registro usa estas funciones como `permiso`. PL-88 cierra aquí con pruebas de los 13 roles (incluye lo de F2B-A).
- **Patrón a copiar (Curva S):** `src/app/(workspace)/proyectos/[id]/curva-s/page.tsx` ~12: `if (!usuario || !puedeVerCurvaS(usuario.roles) || !tieneAlcanceSobreProyecto(usuario, id))` muestra «No tienes acceso a la Curva S de este servicio.» dentro del shell, sin leer datos. API: `validarEscrituraProyecto(proyectoId, permitido)` y `exigirAlcance(usuario, proyectoId)` en `src/lib/auth/guard-proyecto.ts` (403 `No autorizado` por rol; 403 `No tienes esta OT a cargo` por alcance); `tieneAlcanceSobreProyecto` en `src/lib/permisos/alcance-proyecto.ts` (el administrador salta el alcance).
- **PR** (`proyectos/[id]/pr/page.tsx`) y **Dashboard** (`proyectos/[id]/dashboard/page.tsx`): hoy sin guardia. Añade **solo** la guardia (rol + alcance), **antes** de cualquier consulta de datos; no toques `src/lib/pr` ni `src/lib/dashboard`.
- **Interruptor Parcial/Completo (C35 resuelta por Victor, 2026-09-29):** `ToggleTipoDashboard` (`dashboard/page.tsx` ~264; `puedeEditarTipo` ~97 usa `puedeAdjudicarProyecto`) y `PATCH api/proyectos/[id]/tipo-dashboard/route.ts` (~12, `validarEscrituraProyecto(id, puedeAdjudicarProyecto)`) pasan a `puedeVerEconomia`; verifica por los dos lados. Lo demás del Parcial sin economía es del plan futuro.
- PL-125: excepciones acotadas en un solo lugar (planner solo Plan Maestro; supervisor de oficina técnica solo DP y sin importar; jefe de costos con economía), por los dos lados con «Ver como». SVX: usa el servicio sin alcance de la cuenta B (LB-05).

## Qué NO hacer

- No modifiques cálculos ni datos (`src/lib/pr`, `dashboard`, `curva-s`, `plan-maestro`, `dp`). No cambies permisos de acciones (F5C).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
