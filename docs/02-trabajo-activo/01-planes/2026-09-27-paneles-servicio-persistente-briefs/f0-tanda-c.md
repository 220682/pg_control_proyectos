# F0-C · Línea base por rol: quién puede hoy cada interfaz y cada acción

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F0 · **Depende de:** F0-A cerrada (usa su lista de funciones y guardias).
**Punto de commit:** Ninguno (solo evidencia).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-147 | Línea base "antes" por rol de la **tabla 1 y la tabla 2 completas** (no solo de las interfaces con economía): quién puede hoy cada interfaz y cada acción, en UI y servidor | Tablas rol × interfaz y rol × acción |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Fuente de las filas: tablas 1 y 2 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md` (19,7 KB; léelo una vez, no lo copies al plan ni a los briefs).
- Cómo calcular «hoy» sin 13 sesiones de navegador: crea un archivo de prueba **temporal** de vitest (p. ej. `src/lib/permisos/_lb-f0.test.ts`; `include` es `src/**/*.test.ts`), que importe `ROLES` (`src/lib/permisos/permisos.ts` ~16, `readonly Rol[]`, 13 roles) y cada función `puede*` y escriba la tabla rol × función; bórralo al terminar (no se commitea). Para la guardia de servidor de cada página o API usa `Grep` (páginas sin guardia de rol hoy: `proyectos/[id]/pr`, `dashboard`, `dp` para ver, `requerimientos`, dashboard del portafolio `src/app/programas/[id]/portafolios/[portafolioId]/dashboard`).
- Muestra en navegador (3 roles: `asistente`, `supervisor_operativo`, `supervisor_logistica`) con «Ver como»: `POST /api/ver-como` con `{ "rol": "<rol>" }` (`src/app/api/ver-como/route.ts`; solo administrador real; fija la cookie `COOKIE_VER_COMO`). Confirma que la tabla calculada coincide con lo que ocurre. Un solo `browser_evaluate` puede recorrer rutas con `fetch` y devolver los códigos; al terminar, restaura tu rol (revisa la ruta para ver cómo se quita la simulación).
- R28: «Ver como» cambia los roles pero el alcance por OT (`proyecto_miembros`) sigue siendo el del usuario real; distingue `{"error":"No autorizado"}` (rol) de `{"error":"No tienes esta OT a cargo"}` (alcance) (`src/lib/auth/guard-proyecto.ts`).
- Entrega: tabla rol × interfaz (tabla 1) y rol × acción (tabla 2), «antes», con UI y servidor. Es la base de PL-97 (F6-A).

## Qué NO hacer

- No cambies permisos. No escribas datos: solo lectura y llamadas sin efecto.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
