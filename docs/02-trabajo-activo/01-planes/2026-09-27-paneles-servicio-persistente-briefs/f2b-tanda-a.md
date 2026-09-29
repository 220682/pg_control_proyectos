# F2B-A · Interfaces sin economía abiertas a los 13 roles: funciones, páginas y APIs de ver

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F2B · **Depende de:** F2-E cerrada (fin de F2).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-92 | Status de Requerimiento: los 13 roles (con "Ver como") abren `/requerimientos` y cada rol que crea RQ ve su lista; sin sesión lleva a `/login`; un usuario sin ningún rol conocido es rechazado (prueba unitaria) | Tabla 13 roles + captura |
| PL-94 | `GET /api/proyectos/<SV1>/partidas` no se restringió: con "Ver como" rol Asistente, Crear RQ carga las partidas y abre su formulario (sin guardar) | Captura |
| PL-119 | Cronograma, Paquetes de Trabajo, RDTs (status, archivo de subidos, consolidado) y consolidado RQ (ver) abren para los 13 roles, incluido el rol Asistente; las acciones dentro de cada pantalla siguen la tabla 2 | Tabla rol × pantalla con "Ver como" + capturas |
| PL-120 | Recursos de empresa (Personal, Cargos, Equipos, Causas CNC en consulta) abren para los 13 roles, en páginas y APIs de lectura; gestionar Causas CNC (alta y baja) sigue solo con las filas de la tabla 2, en pantalla y en API | Capturas + respuestas de la API |

## Entregable sin ID: parte F2B de PL-88
Implementa y prueba (recorriendo `ROLES`) las funciones de ver de las interfaces sin economía. PL-88 se **cierra en F5B-A** (misma prueba, ampliada a economía).

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Fuente única de roles: tabla 1 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md` (léela del archivo; no la copies). En `src/lib/permisos/permisos.ts` (líneas de 1942b01): `puedeVerCronograma` ~265, `puedeVerPaquetesTrabajo` ~291, `puedeVerRdts` ~239, `puedeVerConsolidadoRq` ~331, `puedeVerRecursos` ~197 (hoy alias de `puedeVerApartadoProyectos`) → los **13 roles**; **nueva** `puedeVerStatusRequerimiento` (13 roles; un usuario sin rol conocido es rechazado: PL-92). `puedeGestionarCatalogoCnc` ~234 sigue siendo de gestión (admin y JP): separa consulta de gestión.
Guardias a abrir (Grep verificado):
- Páginas (`src/app/(workspace)/`): `cronograma` ~14, `paquetes-trabajo` ~14, `rdts/{consolidado,listado,status}` y `rdts/page.tsx`, `logistica/consolidado-rq` ~15, `recursos/{cargos,equipos,personal}`, `recursos/causas-cnc` (hoy exige gestionar: la consulta pasa a `puedeVerRecursos`), `requerimientos/page.tsx` (hoy solo sesión: añade `puedeVerStatusRequerimiento`).
- APIs (`src/app/api/`): `cronograma/route.ts` ~26, `cronograma/hitos/route.ts` ~15, `paquetes-trabajo/route.ts` ~62, `rdts/route.ts` ~55, `rdts/consolidado/route.ts` ~31, `rdts/partes/route.ts` ~55 (GET), `rdts/partes/[id]/historial/route.ts` ~34, `logistica/requerimientos/route.ts` ~11, `recursos/route.ts` ~21, `recursos/personal/route.ts` ~15 (GET; el POST ~42 no cambia aquí), `recursos/catalogo-cnc/route.ts` GET ~14 (consulta), y `GET proyectos/[id]/requerimientos/route.ts`.
- **No restrinjas** `GET proyectos/[id]/partidas` (lo usa Crear RQ; PL-94: con «Ver como» asistente, Crear RQ carga partidas y abre su formulario, sin guardar).
- `grupo-proceso.ts` (`chipsRdts` ~123; `comunes` ~174/181) usa estas funciones para `habilitado`: con 13 roles quedan habilitados; corrige los `tituloDeshabilitado` obsoletos («Solo Geren…», «Asistentes no tienen acceso…»). `(workspace)/layout.tsx` pasa `puedeVerRecursos` al shell (el panel izquierdo se rehace en F3).
- Las **acciones** dentro de las pantallas siguen con sus funciones actuales (F5C). Pruebas: `permisos.test.ts` recorre los 13 roles contra la tabla 1. Verificación de roles: un `browser_evaluate` que recorre los 13 roles con `POST /api/ver-como` y hace `fetch` a las rutas (R28).

## Qué NO hacer

- No cambies las funciones de acción (F5C). No muestres ni añadas dinero en pantalla.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
