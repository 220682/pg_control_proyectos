# F5B-B · Economía: DP, Plan Maestro, Curva S y Dashboard del portafolio (rol + alcance)

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5B · **Depende de:** F5B-A cerrada (funciones nuevas en `permisos.ts`).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-91 | DP (ver): ídem PL-89 en `/proyectos/<SV1>/dp`, con el supervisor de oficina técnica dentro y el planner fuera; el botón de importar sigue la fila "Importar DP" de la tabla 2 (PL-134) | Capturas |
| PL-122 | Dashboard del portafolio (`app/programas/…/dashboard`, fuera del shell): los roles de la tabla 1 lo ven; los demás reciben "No tienes acceso…" con enlace de vuelta a la grilla del portafolio, sin datos y sin error 500 | Capturas por rol + respuesta |
| PL-123 | Plan Maestro (ver) y Curva S: Plan Maestro para los roles de economía más el planner; Curva S solo economía (el rol Asistente ya no entra por la excepción del código vigente); gestionar Plan Maestro no cambia | Capturas por rol + API |
| PL-153 | Exportar DP (`…/dp/exportar`): solo los roles que ven el DP (economía más supervisor de oficina técnica, supuesto A12); cualquier otro rol recibe 403; hoy no tiene guardia de rol | Respuestas por rol (13 roles) |
| PL-176 | Dashboard del portafolio (`app/programas/…/dashboard`, fuera del shell): mismo patrón; el mensaje enlaza de vuelta a la grilla del portafolio | Capturas + SVX |
| PL-177 | DP (ver): mismo patrón en `/proyectos/[id]/dp` y en `…/dp/exportar` | Capturas + respuesta de la API |
| PL-178 | Plan Maestro (ver): mismo patrón en `/plan-maestro?proyectoId=` y en `GET /api/plan-maestro`; el planner (excepción de la tabla 1) también queda sujeto al alcance | Capturas + respuesta de la API |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **DP** `proyectos/[id]/dp/page.tsx`: hoy sin guardia para ver (~101 `puedeImportar` usa `puedeSubirDocumento(..., 'supervisor_oficina_tecnica')`: eso es F5C-B, no lo cambies aquí). `api/proyectos/[id]/dp/exportar/route.ts`: **sin guardia** → `puedeVerDp` + alcance (PL-153, PL-177). El supervisor de oficina técnica ve el DP; el planner no.
- **Plan Maestro:** `(workspace)/plan-maestro/page.tsx` (lee `?proyectoId=`) y `api/plan-maestro/route.ts` GET ~31 (`puedeVerPlanMaestro`; POST ~127 y PUT ~297 usan `puedeGestionarPlanMaestro` y ya llaman `exigirAlcance`). Añade alcance a la lectura; el planner (excepción de la tabla 1) también queda sujeto.
- **Curva S:** página y `api/curva-s/route.ts` ~33 ya usan rol + alcance; solo cambia el rol a `puedeVerCurvaS` = economía (el rol Asistente ya no entra por la excepción vigente). No cambia el alcance.
- **Dashboard del portafolio** (`src/app/programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx`, 239 líneas; **fuera del shell y sin guardia ni alcance**; usa `crearClienteServidor`, lee `portafolios`, `proyectos` y `pr_*`): añade guardia de rol antes de leer datos con «No tienes acceso…» y enlace de vuelta a la grilla del portafolio (`/programas/[id]/portafolios/[portafolioId]`), sin datos ni error 500 (PL-122). Alcance en un portafolio (agrupa varios servicios): el plan dice «mismo patrón». **Duda de negocio si no es evidente:** cómo aplicar alcance por OT a un portafolio (recomendación del Planner: mostrar solo las OT del portafolio con alcance; administrador todas). Si no puedes resolverlo con el código y el plan, devuélvela al Orquestador antes de implementar esa parte (PL-176).
- Con «Ver como» el alcance sigue siendo el del usuario real (R28): distingue rechazo por rol de rechazo por alcance por el mensaje.
- No muevas ninguna página. Solo se añade guardia.

## Qué NO hacer

- No toques `src/lib/dp`, `plan-maestro`, `curva-s` ni `dashboard`. No muevas el dashboard del portafolio al shell.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
