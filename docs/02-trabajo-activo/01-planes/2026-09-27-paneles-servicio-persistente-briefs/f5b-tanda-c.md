# F5B-C · Economía: Registro de costos «solo subir», enlaces internos, APIs y cierre de F5B

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5B · **Depende de:** F5B-A y F5B-B cerradas.
**Punto de commit:** Al cerrar la fase F5B (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-124 | Registro de costos, ver: según la tabla 1 (la descarga es una acción, PL-126); logística entra a la pantalla en modo "solo subir" (sin descarga, sin fecha ni contenido del archivo); la pantalla no rechaza a quien deba subir | Capturas por rol |
| PL-179 | Registro de costos: mismo patrón en `/proyectos/[id]/registro-costos` y en su API; logística (modo "solo subir") también queda sujeta al alcance para esa OT | Capturas + respuesta de la API |
| PL-93 | APIs, desde el navegador con la sesión iniciada: las de interfaces sin economía (`GET /api/proyectos/<SV1>/requerimientos` y su exportación, `/api/logistica/requerimientos`, `/api/recursos*`, `/api/paquetes-trabajo`) responden a los 13 roles; las de economía (`…/dp/exportar`, `GET /api/curva-s`, `GET /api/plan-maestro`, `…/registro-costos`) responden 403 a un rol fuera de la tabla 1 | Respuestas registradas |
| PL-95 | Los chips de interfaces sin economía están activos para los 13 roles (F2B); los de economía usan las funciones nuevas como `permiso` del registro: para un rol fuera de la tabla 1 aparecen deshabilitados con título en los tres paneles y en Accesos rápidos, y para uno dentro, activos | Tabla chip × rol + captura |
| PL-98 | Enlaces internos: la ficha del servicio, su checklist de documentos (que enlaza a PR y DP) y la grilla del portafolio (enlace al dashboard) no muestran a un rol fuera de la tabla 1 un enlace que lleve a una pantalla rechazada | Captura con "Ver como" |
| PL-99 | La referencia de F5B y F5C es la versión aprobada del flujo 14 (commit 8027037, artefacto versión 17); el Worker anota en el progreso el commit del flujo 14 contra el que verifica y, si cambia durante la tarea, lo comunica al Orquestador antes de seguir | Nota en el progreso |
| PL-101 | La guardia se evalúa antes de leer datos del servicio: para un rol fuera de la tabla 1 no se ejecutan consultas de datos de PR, DP, Dashboard, Curva S, Plan Maestro ni Registro de costos y la respuesta no revela nombre ni datos del servicio | Revisión de código + captura |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **Registro de costos:** `proyectos/[id]/registro-costos/page.tsx` ~18-23 hoy abre si `puedeSubir || puedeDescargar` y si no hace `redirect('/proyectos/${id}')`; `PanelRegistroCostos.tsx` (subir/descargar). API `api/proyectos/[id]/registro-costos/route.ts`: GET ~20 (`puedeDescargarRegistroCostosServicio`) y POST ~56 (`validarEscrituraProyecto(id, puedeSubirRegistroCostosServicio)`). Ver = `puedeVerRegistroCostos` (economía) + alcance (PL-179, también para logística). **Modo «solo subir»:** logística entra con solo el control de subir: sin descarga, sin fecha ni contenido del archivo (PL-124). La descarga (administrador y JP) es F5C-C.
- **Enlaces internos (PL-98, R17):** ficha `proyectos/[id]/page.tsx` («Ver Dashboard» y los enlaces a PR y DP del checklist de documentos; ya oculta el de Plan Maestro según permiso: mismo patrón) y el enlace al dashboard desde la grilla del portafolio (`programas/[id]/portafolios/[portafolioId]/page.tsx`): no se muestra a un rol fuera de la tabla 1 un enlace que lleve a una pantalla rechazada.
- **PL-93 (APIs, desde el navegador con sesión, 13 roles con «Ver como»):** sin economía responden a los 13 (`GET proyectos/<SV1>/requerimientos` y su exportación, `logistica/requerimientos`, `recursos*`, `paquetes-trabajo`); economía responden 403 a un rol fuera de la tabla 1 (`dp/exportar`, `curva-s`, `plan-maestro`, `registro-costos`). `partidas` no se restringe.
- **PL-95:** los chips de economía usan las funciones nuevas como `permiso` en los tres paneles y Accesos rápidos (deshabilitados con título fuera de la tabla 1, activos dentro).
- **PL-99:** anota en el progreso el commit del flujo 14 contra el que verificas: `git -C "D:\VICTOR\CLAUDE CODE\pg_control_proyectos" log -1 --format=%h -- docs/04-flujos-de-negocio/14-accesos-y-restricciones.md`; si cambia durante la tarea, avisa al Orquestador. **PL-101:** la guardia se evalúa antes de leer datos (revisión de código de las seis pantallas).

## Qué NO hacer

- No cambies permisos de acciones ni descargas (F5C). No restrinjas `partidas`.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
