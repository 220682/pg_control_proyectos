# F6-B · Servidor: URL directa, APIs, sesión cerrada, bypass del administrador y prueba de humo en vivo

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F6 · **Depende de:** F6-A cerrada.
**Punto de commit:** Ninguno (el cambio de humo se revierte).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-44 | **Ver no es acceder.** Cuenta B, por URL directa (con `?proyectoId=`), a cada pantalla cuyo chip esté deshabilitado para su rol según la matriz base (con la cuenta B, típicamente las interfaces con economía, Editar servicio y Editar checklist): el servidor responde con la guardia de la pantalla (redirección o mensaje) y no muestra datos | URL, resultado y captura de cada una |
| PL-45 | Cuenta B, por URL directa, a las interfaces con economía (PR, Dashboard, DP, Curva S, Plan Maestro, Registro de costos y dashboard del portafolio): rechazo según la matriz base; detalle en PL-89 a PL-91 y PL-122 a PL-124 | Remite a esos ítems |
| PL-46 | Cuenta B, desde el navegador con la sesión iniciada, llama a `GET /api/cronograma`, `/api/rdts/consolidado` y `/api/curva-s` con `proyectoId` de SV1, de SVX y con un id inexistente: las dos primeras responden según la matriz base (los 13 roles) y `/api/curva-s` rechaza a un rol fuera de la matriz; con id inexistente, respuesta 4xx clara y nunca 500 ni datos de un servicio sin alcance | Respuestas registradas |
| PL-54 | Prueba de humo en vivo: añadir una entrada de prueba **solo en el registro** (sin commitearla) y comprobar con Playwright, con las dos cuentas, que aparece en los paneles correspondientes, conserva el servicio, se habilita o deshabilita por permiso y sale en la matriz, sin tocar ningún otro archivo; se revierte y el diff final no la contiene | Captura + `git status` con un solo archivo modificado, luego limpio |
| PL-73 | Con sesión cerrada, cualquier ruta del workspace con `?proyectoId=` lleva a `/login` (el middleware sigue igual) | Captura |
| PL-180 | El administrador salta el alcance en las seis pantallas (bypass ya resuelto por el helper existente); se comprueba que sigue entrando a SVX sin ser miembro | Captura |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **PL-44/PL-45:** cuenta B, por URL directa con `?proyectoId=`, a cada pantalla cuyo chip esté deshabilitado para su rol (típicamente economía, Editar servicio, Editar checklist): el servidor muestra la guardia (redirección o mensaje) sin datos. Interfaces con economía y dashboard del portafolio: detalle en PL-89 a PL-91 y PL-122 a PL-124 (ya cerrados; remite).
- **PL-46:** cuenta B, desde el navegador con sesión, `GET /api/cronograma`, `/api/rdts/consolidado` y `/api/curva-s` con `proyectoId` de SV1, de SVX y con id inexistente: las dos primeras según la matriz (13 roles), `/api/curva-s` rechaza a un rol fuera de la tabla 1; con id inexistente, 4xx claro y nunca 500 ni datos de un servicio sin alcance.
- **PL-73:** con la sesión cerrada, cualquier ruta del workspace con `?proyectoId=` lleva a `/login` (`src/middleware.ts` no se modifica).
- **PL-180:** el administrador entra a SVX sin ser miembro en las seis pantallas con economía (bypass de `tieneAlcanceSobreProyecto`).
- **PL-54 (prueba de humo en vivo):** añade una entrada de prueba **solo en `src/lib/config/registro-accesos.ts`** (sin commitear), comprueba con las dos cuentas que aparece en los paneles correspondientes, conserva el servicio, se habilita o deshabilita por permiso y sale en la matriz, sin tocar ningún otro archivo; revierte tu propio cambio y confirma con `git status` (un solo archivo modificado, luego limpio).

## Qué NO hacer

- No commitees la entrada de prueba. No modifiques el middleware ni datos.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
