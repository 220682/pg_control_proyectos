# F2-D · Redirects y salidas que pierden el servicio; validación en servidor

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F2 · **Depende de:** F2-A, F2-B y F2-C cerradas.
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-19 | Redirección del servidor por falta de permiso: la cuenta B abre por URL una pantalla que no puede usar con `?proyectoId=SV1` y aterriza en Mi entorno conservando SV1 | URL final + captura |
| PL-20 | Las salidas tras guardar (Crear RDTs a Status de RDTs, Crear RQ a Status de Requerimiento) y `CabeceraPagina` conservan el servicio | Prueba unitaria del helper + revisión de código (sin guardar datos reales) |
| PL-21 | El chip "Salir a Mi entorno" se comporta según la decisión 4 aprobada (con servicio, va a `/mi-entorno?proyectoId=…`) | Captura antes y después de hacer clic |
| PL-70 | El parámetro `?proyectoId=` nunca se usa en servidor sin validar pertenencia: las pantallas y APIs que lo reciben validan autenticación, rol y acceso al servicio como antes | Revisión de código + PL-46 |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Las 14 páginas con `redirect('/mi-entorno')` (Grep verificado), bajo `src/app/(workspace)/`: `cronograma`, `logistica/consolidado-rq`, `mi-perfil`, `paquetes-trabajo`, `plan-maestro`, `rdts/consolidado`, `rdts/crear`, `rdts/listado`, `rdts/page.tsx`, `rdts/status`, `recursos/cargos`, `recursos/causas-cnc`, `recursos/equipos`, `recursos/personal`. Cada redirect conserva `?proyectoId=` con el helper (lee `searchParams` donde la página aún no lo haga).
- Salidas tras guardar: `FormularioCrearRdt.tsx` ~572 y `FormularioRequerimiento.tsx` ~177. Se prueban con la prueba unitaria del helper y revisión de código (no se guardan datos reales).
- `CabeceraPagina` (`src/components/ui/CabeceraPagina.tsx`, 45 líneas, componente de servidor): `volverHref = '/mi-entorno'`, `volverEtiqueta = 'Salir a Mi entorno'`, `mostrarVolver`. Decisión 4 (recomendación B vigente): mismo texto; con servicio va a `/mi-entorno?proyectoId=…`, sin servicio a `/mi-entorno`. Usada por unas 20 pantallas: decide cómo recibe el servicio sin volverla cliente sin necesidad.
- También revisa los redirects que hoy pasan el servicio por otro parámetro o lo pierden: `proyectos/[id]/mi-entorno/page.tsx`, `proyectos/[id]/entorno/[grupo]/page.tsx`, `proyectos/[id]/requerimientos/page.tsx`.
- **PL-19:** con la cuenta B (o «Ver como» de un rol sin permiso) abre por URL una pantalla que hoy no puede usar (p. ej. `/recursos/personal?proyectoId=<SV1>`) y verifica el aterrizaje en Mi entorno conservando SV1. **PL-70:** revisión de código: ninguna página ni API que reciba `proyectoId` lo usa sin validar autenticación, rol y acceso (`src/lib/auth/guard-proyecto.ts`, `usuario-actual.ts`).

## Qué NO hacer

- No cambies quién puede abrir cada pantalla. La prueba de fuente contra redirects es de F5-A (PL-57).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
