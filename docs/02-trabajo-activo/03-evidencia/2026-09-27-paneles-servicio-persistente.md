# Evidencia — Paneles: servicio persistente

## Referencia al plan

`docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente.md` (v8).

## Entorno y fecha

Worktree `py_control_proyectos_web/.worktrees/local-worker-1`, rama `local-worker-1` (desde `main` `1942b01`). Inicio: 2026-09-29.

## Rol / usuario y datos autorizados

Cuentas de prueba A y B (credenciales fuera del repositorio). Solo lectura sobre datos reales. Sin secretos.

## Punch List ejecutada

Evidencia por ítem, añadida al final por cada Worker (append).

## Enlace al artifact de checklist visual

Matriz de permisos: https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT

## Resultados de pruebas técnicas

## Regresiones verificadas

## Limitaciones o casos no verificables

---

## Evidencia por tanda


---

## F0-A · Línea base, descargas y funciones de permisos (Worker local-3, 2026-09-29)

Worktree `.worktrees/local-worker-1`, HEAD `1942b01` (= `main`), árbol limpio antes y después de medir.

### LB-01 · Línea base técnica (sin tocar código)

| Comando | Resultado |
|---|---|
| `npm test` (`vitest run`) | 60 archivos pasaron de 60; **528 pruebas pasadas, 0 falladas** |
| `npm run lint` (`eslint`) | **27 problemas: 9 errores y 18 advertencias** (resumen del runner; coincide con el baseline del 2026-09-23). 1 error corregible con `--fix` |
| `npx next build --webpack` | Compila; termina con la lista de rutas sin error |

Referencia para PL-74 a PL-76 (F6-E): tests 528/528, lint 9 errores + 18 advertencias.

### PL-127 · Inventario de descargas (código `1942b01` contra artefacto «Matriz de permisos», sección Descargas, y flujo 14)

Descargas por API con `Content-Disposition` (9 rutas) y su guardia actual:

| Ruta | Guardia hoy | En el artefacto (Descargas) | En flujo 14 |
|---|---|---|---|
| `GET proyectos/[id]/registro-costos` | `puedeDescargarRegistroCostosServicio` (JP) | Sí, «Descargar registro de costos» (admin, JP) | Sí (tabla 2) |
| `POST logistica/requerimientos/exportar-004` | `puedeDescargarConsolidadoRq` (alias de `puedeVerConsolidadoRq`) | Sí, consolidado RQ PROM-GP-004 | Sí (tabla 2, nota 5) |
| `GET proyectos/[id]/dp/exportar` | Solo sesión iniciada (403 si no hay usuario; sin rol ni alcance) | Sí, «Exportar DP» (propuesta a revisar) | No (pendiente, ítem 1 de «por decidir») |
| `GET rdts/exportar` (ZIP y PDF PROM-GP-0006) | `puedeVerRdts` | Sí, «Descargar RDTs… y listado» (propuesta: 13 roles) | No (pendiente) |
| `GET rdts/partes/[id]/pdf` | `puedeVerRdts` | Sí, «PDF de un RDT estructurado» (13 roles) | No |
| `GET rdts/[id]/archivo` | `puedeVerRdts` | Sí, «archivo de un RDT subido» (13 roles) | No |
| `GET proyectos/[id]/requerimientos/exportar` (`tipo` = vacio, detalle o registro) | Solo sesión (401 si no hay usuario); sin rol ni alcance | Sí, «listado RQ según filtro» (registro) y «PDF individual de un RQ» (detalle) | No |
| `GET requerimientos/formato-vacio` | Solo sesión (401) | Sí, «formato vacío PROM-GP-008» | No |
| `GET cronograma/plantilla` | `puedeSubirCronograma` (admin, JP, planner) | Sí, «plantilla de cronograma» (admin, JP, planner; guardia igual) | No |

`BotonDescargarPdf` (`components/ui/BotonDescargarPdf.tsx`, hace `fetch(url)` + enlace `download`) se usa en `DetalleRqNotificacion`, `FormularioRequerimiento` y `PanelVerRq`; sus URL apuntan a `proyectos/[id]/requerimientos/exportar` (detalle) y `requerimientos/formato-vacio`, ya inventariadas arriba. No añade rutas nuevas.

Descargas por almacenamiento (Storage): `admin.storage...download(` aparece en `registro-costos` (GET), `rdts/[id]/archivo`, `rdts/exportar` (arma el ZIP) y `requerimientos/exportar` (`cargarImagenesAdjuntos`: incrusta las imágenes adjuntas de cada línea del RQ dentro del PDF; no las entrega sueltas). No hay `createSignedUrl`, `getPublicUrl` ni URL de Storage en ninguna pantalla.

Puntos por verificar del brief:
- Adjuntos de RQ (`…/lineas/[lineaId]/adjuntos/route.ts`): **solo POST (subida)**; no hay ruta de descarga. Guardia de la subida: `puedeCrearRequerimiento` o administrador, más alcance por OT. Los adjuntos solo salen embebidos como imágenes en el PDF de `requerimientos/exportar`.
- Documentos del checklist (`…/documentos/[documentoId]/route.ts`): **solo POST (subida)**; guardia `puedeSubirDocumentoAsignado` + alcance. **No existe descarga** de documentos del checklist ni del DP subido en el código de `1942b01`.

**Lista para Victor (entrada de PL-155, F7-B)**
1. Ninguna descarga del código falta en el artefacto: las 9 rutas están en su sección «Descargas» (cinco añadidas allí como «ya existen en el código»). Las que **aún no están en el flujo 14** son las propuestas a revisar (exportar DP, RDTs y listado, listado RQ, plantilla de cronograma, PDF de RDT, archivo de RDT, PDF individual de RQ, formato vacío).
2. Hallazgo a reportar: `dp/exportar`, `requerimientos/exportar` y `requerimientos/formato-vacio` **no tienen guardia de rol ni de alcance por OT** (solo sesión); el artefacto propone que sigan a «ver», pero hoy cualquier usuario autenticado puede llamarlas con cualquier `proyectoId`. No se cambió nada (A13).
3. No hay descarga de adjuntos ni de documentos del checklist: no falta nada en el artefacto por ese lado (descargarlos sería una función nueva, no un cambio de guardia).

### PL-146 · Funciones de `permisos.ts` que cambian: tabla del plan contra el código `1942b01`

Verificado con Grep de cada función en `src/` (excluyendo `permisos.ts` y pruebas). Usos: P = página, A = API, C = componente o lib. Las variables locales `puedeEditar`, `puedeEliminar`, `puedeCorregir`, `puedeValidar`, `puedeSubir`, `puedeDescargar`, `puedeComentar`, `puedeManipular`, `puedeDerivar`, `puedeActualizarEstado`, `puedeEditarTipo`, `puedeImportar`, `puedeGestionar` son **derivados en props o estado** de las funciones de la tabla, no funciones propias.

| Función (hoy en código) | Alias / dependencias | Usos (páginas, APIs, componentes) | Contra la tabla del plan |
|---|---|---|---|
| `puedeAdjudicarProyecto` (solo JOT, l.32) | Base de `puedeCrearPrograma` y `puedeCrearPortafolio`; hoy también la usan dashboard (toggle) y editar servicio | P: `programas/[id]/portafolios/[portafolioId]` (+`/proyectos/nuevo`), `proyectos/[id]/{page,dashboard,editar}`. A: `proyectos` (POST), `proyectos/siguiente-ot`, `proyectos/[id]/datos`, `proyectos/[id]/tipo-dashboard`. C: `ToggleTipoDashboard` | Confirmada |
| `puedeCrearPrograma`, `puedeCrearPortafolio` | Alias de `puedeAdjudicarProyecto` (l.122, 126) | P: `programas`, `programas/[id]`. A: `programas`, `programas/[id]`, `portafolios`, `portafolios/[id]` | Confirmada |
| `puedeConfirmarTransicionEstado` (solo JOT, l.36) | — | P: `proyectos/[id]/page`. A: `confirmar-transicion` | Confirmada |
| `puedeArchivarProyecto`, `puedeEliminarProyecto` (admin, JOT) | — | P: `proyectos/[id]/page`, `portafolios/[portafolioId]/{page,archivados}`. A: `proyectos/[id]` | Confirmada |
| `puedeEliminarContenedor` (admin) | — | P: `programas`, `programas/[id]`. A: `programas/[id]`, `portafolios/[id]` | Confirmada |
| `puedeModificarChecklist` (admin, JOT) | — | P: `checklist/editar`, `proyectos/[id]/page`. A: `checklist` | Confirmada |
| `puedeEditarPerfilExtendido` (admin, JOT, JP) | — | **Sin usos en `src/` fuera de `permisos.ts` y pruebas** | **Corrige**: la columna «Usos» del plan dice «Perfil (página y API)»; hoy no se referencia. Ubicar la guardia real del perfil antes de tocarla |
| `puedeSubirDocumento(roles, rolResponsable)` (admin o rol responsable) | Base de `puedeSubirDocumentoAsignado` | P: `proyectos/[id]/dp/page` (l.101, con `'supervisor_oficina_tecnica'`). A: `proyectos/[id]/dp` (POST, l.28) | Confirmada; `puedeImportarDp` reemplaza estos dos usos |
| `puedeSubirDocumentoAsignado` | -> `puedeSubirDocumento` | P: `proyectos/[id]/page` (l.150). A: `documentos/[documentoId]` (POST, l.85) | **Añadir a «Sin cambio»** (no figuraba con su nombre) |
| `puedeVerCurvaS` (todos menos asistente) | — | P: `proyectos/[id]/curva-s`. A: `api/curva-s` | Confirmada |
| `puedeVerPlanMaestro` (todos menos asistente) | — | P: `plan-maestro`, `proyectos/[id]/page` (l.97). A: `api/plan-maestro`. C: `lib/notificaciones/grupo-proceso.ts` (l.188) | Confirmada; **añadir** `grupo-proceso.ts` |
| `puedeVerCronograma` (todos menos asistente) | — | P: `cronograma`. A: `cronograma`, `cronograma/hitos`. C: `grupo-proceso.ts` (l.181) | Confirmada; **añadir** `grupo-proceso.ts` |
| `puedeVerPaquetesTrabajo` (todos menos asistente) | — | P: `paquetes-trabajo`. A: `api/paquetes-trabajo` | Confirmada |
| `puedeVerRdts` (admin, JP, JOT, SAdm, RRHH, asistente, SOp) | — | P: `rdts`, `rdts/{consolidado,listado,status}`. A: `rdts` (GET), `rdts/consolidado`, `rdts/exportar`, `rdts/[id]/archivo`, `rdts/partes` (GET), `rdts/partes/[id]/{historial,pdf}`. C: `grupo-proceso.ts` (l.123) | Confirmada; **añadir** `rdts/consolidado`, `partes/[id]/historial` y `grupo-proceso.ts` |
| `puedeVerConsolidadoRq` (slog, JP, admin, JOT) | `puedeDescargarConsolidadoRq` la usa como alias | P: `logistica/consolidado-rq`. A: `logistica/requerimientos` (GET). C: `grupo-proceso.ts` (l.174) | Confirmada; **añadir** `api/logistica/requerimientos` y `grupo-proceso.ts` |
| `puedeDescargarConsolidadoRq` | Alias de `puedeVerConsolidadoRq` (l.350) | P: `logistica/consolidado-rq`. A: `logistica/requerimientos/exportar-004` (POST) | Confirmada |
| `puedeVerApartadoProyectos` (admin, JP) | Base de `puedeVerRecursos` | C: `(workspace)/layout.tsx` (l.45-46), `WorkspaceShell` (l.47, 204) | **Añadir a la tabla** (alias raíz del panel izquierdo y de Recursos; no figuraba) |
| `puedeVerRecursos` | Alias de `puedeVerApartadoProyectos` (l.197, verificado) | P: `recursos/{cargos,equipos,personal}`. A: `api/recursos` (GET), `api/recursos/personal`. C: `layout.tsx` (l.48), `WorkspaceShell` (l.49, 162) | Confirmada |
| `puedeGestionarCatalogoCnc` (admin, JP) | Mismo conjunto que `puedeVerApartadoProyectos` | P: `recursos/causas-cnc`. A: `recursos/catalogo-cnc` (+`[id]`). C: `layout.tsx` (l.49-50), `WorkspaceShell` (l.51, 194) | Confirmada (sin cambio); relación con la nueva `puedeGestionarRecursos` a resolver en F5D |
| `puedeCrearRequerimiento` (12 roles: todos menos admin) | — | P: `mi-entorno`, `proyectos/[id]/requerimientos/nuevo`. A: `…/requerimientos` (POST), `…/siguiente-codigo`, `…/lineas/[lineaId]/adjuntos` (POST; esta ruta acepta además al administrador por fuera de la función) | Confirmada; **añadir** `siguiente-codigo` y `adjuntos` |
| `puedeActualizarEstadoRequerimiento` (slog) | — | P: `logistica/consolidado-rq`, `mi-entorno`, `notificaciones`, `requerimientos`. A: `…/[rqId]/estado` | Confirmada |
| `puedeDerivarRequerimientoLogistica` (admin, JOT, JP) | — | P: `mi-entorno`, `notificaciones`, `requerimientos`. A: `notificaciones/[id]/atender`, `…/[rqId]/estado` | Confirmada (sin cambio) |
| `puedeComentarRequerimiento` (JP, admin, slog) | — | P: `logistica/consolidado-rq`. A: `…/[rqId]/comentarios` | Confirmada (sin cambio) |
| `puedeEliminarRequerimiento` (admin) | — | P: `requerimientos`. A: `…/requerimientos/[rqId]` (DELETE) | Confirmada |
| `puedeSubirRdt` (SOp, admin, JP, JOT) | — | P: `mi-entorno`. A: `api/rdts` (POST). C: `grupo-proceso.ts` (l.206) | Confirmada (sin cambio) |
| `puedeCrearRdtEstructurado` (SOp, admin, JP) | — | P: `rdts/crear`, `rdts/status`. A: `rdts/catalogos`, `rdts/plantillas`, `rdts/partes` (POST), `rdts/partes/[id]` (PUT, l.62). C: `grupo-proceso.ts` (l.197) | Confirmada; **añadir** `grupo-proceso.ts`. Hoy `puedeCorregir` (derivado en `rdts/status`) sigue a esta función |
| `puedeValidarRdt` (admin, JP) | — | P: `rdts/status`. A: `rdts/partes/[id]` (PATCH, l.151) | Confirmada |
| `puedeEliminarRdt` (admin) | — | P: `rdts/listado`. A: `rdts/[id]` (DELETE), `rdts/partes/[id]` (DELETE, l.315-321) | Confirmada |
| `puedeSubirCronograma` (JP, admin, planner) | — | P: `cronograma`. A: `cronograma`, `cronograma/hitos`, `cronograma/plantilla` | Confirmada (sin cambio; la plantilla la usa como guardia de descarga) |
| `puedeGestionarPlanMaestro` (admin, JP, planner) | Base de `puedeGestionarPaquetesTrabajo` | P: `plan-maestro`. A: `api/plan-maestro` | Confirmada (sin cambio) |
| `puedeGestionarPaquetesTrabajo` | Alias de `puedeGestionarPlanMaestro` (l.287) | P: `paquetes-trabajo`. A: `api/paquetes-trabajo` | Confirmada (sin cambio) |
| `puedeSubirRegistroCostosServicio` (slog) | — | P: `registro-costos`. A: `registro-costos` (POST) | Confirmada |
| `puedeDescargarRegistroCostosServicio` (JP) | — | P: `registro-costos`. A: `registro-costos` (GET) | Confirmada |
| `puedeGestionarUsuarios`, `puedeAsignarRolAdministrador`, `puedeSimularRol` | — | Layout, shell, `admin/usuarios`, `ver-como`, `lib/auth/ver-como.ts` | Sin cambio (regresión PL-145) |

Funciones nuevas que **no existen** en el código (confirmado): `puedeVerEconomia`, `puedeVerDashboard`, `puedeVerDashboardPortafolio`, `puedeVerPr`, `puedeVerDp`, `puedeVerRegistroCostos`, `puedeVerStatusRequerimiento`, `puedeEditarServicio`, `puedeImportarDp`, `puedeCorregirRdt`, `puedeRechazarRdtValidado`, `puedeGestionarRecursos`.

Pantallas económicas hoy **sin guardia de rol en el código** (la reciben en F1): Dashboard del servicio (solo el toggle usa `puedeAdjudicarProyecto`), PR, Dashboard del portafolio, DP (ver; la página solo usa `puedeSubirDocumento` para importar). `dp/exportar` y `requerimientos/exportar` tampoco tienen guardia de rol (ver PL-127).

Hallazgos de PL-146:
1. `puedeEditarPerfilExtendido` no tiene usos en `src/` fuera de `permisos.ts` y pruebas. Ubicar la guardia real del perfil (Grep de `perfil` en `api/` y `PerfilEntorno`) en la tanda que la cambie.
2. La tabla omite `puedeVerApartadoProyectos`, `puedeSubirDocumentoAsignado` y los usos en `lib/notificaciones/grupo-proceso.ts` (`puedeVerRdts`, `puedeVerConsolidadoRq`, `puedeVerCronograma`, `puedeVerPlanMaestro`, `puedeCrearRdtEstructurado`, `puedeSubirRdt`). Cambiar esas funciones altera a quién se le arman notificaciones de proceso: revisarlo en la tanda que las cambie.
3. Alias confirmados: `puedeVerRecursos` -> `puedeVerApartadoProyectos`; `puedeCrearPrograma` y `puedeCrearPortafolio` -> `puedeAdjudicarProyecto`; `puedeDescargarConsolidadoRq` -> `puedeVerConsolidadoRq`; `puedeGestionarPaquetesTrabajo` -> `puedeGestionarPlanMaestro`. `puedeCrearRequerimiento` da 12 roles (todos menos administrador), coherente con el plan.

## F0-B (parcial, bloqueada en el login) - LB-02 a LB-05

Estado: LB-03 derivado del codigo (sin confirmar en navegador); LB-02, LB-04, LB-05 y la confirmacion en navegador de LB-03 NO ejecutados. Motivo: al escribir las credenciales de la cuenta A en el formulario con Playwright, el clasificador de permisos denego la accion por "Credential Leakage". No se reintento por otra via. Servidor dev en el puerto 3111 iniciado y detenido. Sin capturas.

### LB-03 (derivado del codigo en 1942b01, sin verificar en navegador)
Servicio: resolverProyectoId lo reconoce solo en /proyectos/[id]/... y con ?proyectoId= en /mi-entorno y /plan-maestro. Chip = enlace si hrefItemPanel devuelve href; si no, span sin enlace.

| Chip / item | Con servicio | Sin servicio | Habilitado |
|---|---|---|---|
| Accesos rapidos tareo-moi, pets, acta-conformidad, status-servicios | sin ruta | sin ruta | No (span) |
| Requerimiento (status-requerimiento) | /requerimientos | /requerimientos | Si |
| Consolidado RQ | /logistica/consolidado-rq | igual | Si |
| Subir RDTs | /mi-entorno?proyectoId=id&accion=subir-rdt | /mi-entorno?accion=subir-rdt | Si |
| Crear RQ | /mi-entorno?proyectoId=id&accion=crear-rq | /mi-entorno?accion=crear-rq | Si |
| Crear RDTs, Status RDTs, Archivo RDTs, Consolidado RDTs | /rdts/crear, /rdts/status, /rdts/listado, /rdts/consolidado | igual | Si |
| Notificaciones (8 grupos) | /notificaciones | igual | Si |
| Plan Maestro | /plan-maestro?proyectoId=id | /plan-maestro | Si |
| Cronograma, Paquetes de Trabajo | /cronograma?proyectoId=id, /paquetes-trabajo?proyectoId=id | null | Solo con servicio |
| PR, Dashboard, Curva S, Registro de costos | /proyectos/id/pr, dashboard, curva-s, registro-costos | null | Solo con servicio |
| Items sin ruta (capacitaciones, Informe, Acta, Consolidado MOI, Pets, 3WLA, Programacion diaria) | - | - | No |

Panel izquierdo (WorkspaceShell): grupo Proyecto solo con proyectoId y puedeVerApartadoProyectos; solo DP tiene ruta (/proyectos/id/dp), el resto son span. Recursos (Personal, Cargos, Equipos) con puedeVerRecursos; Causas CNC con puedeGestionarCatalogoCnc; Materiales es span.
Asistente (codigo): ChatPlaceholder en WorkspaceShell ~464 dentro de proyectoId + hidden lg:block, y en la pagina del portafolio. Diferencias entre cuenta A y B: no determinadas (requiere navegador).

## F0-B (continuacion, navegador) - LB-02, LB-04, LB-05 y confirmacion de LB-03 (2026-09-29)

Login con browser_fill_form en el formulario de login, sin bloqueo. Servidor dev `-p 3111` en el worktree local-worker-1. Solo lectura. Capturas en `capturas/paneles-servicio-persistente/` (JPEG; 1440 de ancho en escritorio, 390 en movil).

**LB-05 Servicios de prueba**
- SV1 = PS-0004 Movimiento de tierra e instalacion de bancoductos (Ejecucion, Aesa, OC-213432; con DP, Cronograma, Paquetes y Plan Maestro en su panel).
- SV2 = PS-0005 TIE - IN (otro servicio del mismo portafolio Servicios Marcobre, programa Promcoser). Es el unico otro servicio visible.
- SVX (cuenta B no es miembro): no determinable ni existente. El portafolio solo tiene PS-0004 y PS-0005; la cuenta B ve y abre ambos (200) y Mi entorno con cualquiera de los dos no muestra "No tienes esta OT a cargo". La UI no muestra `proyecto_miembros` y el MCP postgresql no conecto. Declarado: sin SVX (pregunta devuelta al Orquestador).
- Rol de la cuenta B en el pie del panel: **Supervisor Operativo** (Lopez Caceres Loayza). Cuenta A: Administrador (Victor Perez Contreras).

**LB-02 Capturas de paneles (7 de 12)**
| Archivo | Contenido |
|---|---|
| LB-02-1-cuentaA-con-servicio.jpg | A en SV1: panel izquierdo (Recursos, Proyecto, Ver como), centro y panel derecho (Accesos rapidos, Grupos) |
| LB-02-2-cuentaB-con-servicio.jpg | B en SV1 |
| LB-02-3-cuentaA-sin-servicio.jpg | A en /notificaciones (sin servicio) |
| LB-02-4-mi-entorno-cuentaA.jpg | A en /mi-entorno |
| LB-02-5-movil-cajon-izquierdo.jpg | 390 px, A, SV1, cajon "Abrir menu" |
| LB-02-6-movil-cajon-derecho.jpg | 390 px, A, SV1, cajon "Abrir herramientas" |
| LB-02-7-mi-entorno-cuentaB.jpg | B en /mi-entorno |

**LB-04 Asistente actual (4 capturas)**
- LB-04-1-asistente-escritorio-con-servicio.jpg: barra "Pregúntale algo al asistente…" al pie, con servicio en escritorio.
- LB-04-2-asistente-sin-servicio.jpg: /recursos/personal (A), no aparece; tambien comprobado por texto en /notificaciones.
- LB-04-3-asistente-movil-con-servicio.jpg: 390 px con servicio, no aparece (oculta por `hidden lg:block`, comprobado por DOM).
- LB-04-4-asistente-portafolio.jpg: copia del placeholder en la pantalla del portafolio Servicios Marcobre.

**LB-03 confirmacion en navegador (fetch de destinos sin seguir redirect; 200 = la pagina responde)**
- Cuenta A con SV1: 17 de 17 destinos 200 (recursos personal/cargos/equipos/causas-cnc, notificaciones, dp, pr, dashboard, curva-s, requerimientos, logistica/consolidado-rq, mi-entorno?proyectoId&accion=subir-rdt, cronograma, paquetes-trabajo, plan-maestro, editar, checklist/editar). Los hrefs del DOM coinciden con la tabla derivada: con servicio `?proyectoId=id` en Cronograma, Paquetes, Plan Maestro y Subir RDTs, y `/proyectos/id/dp|pr|dashboard|curva-s`; Requerimiento y Consolidado RQ sin id. Sin servicio (/notificaciones): Subir RDTs -> `/mi-entorno?accion=subir-rdt`, Plan Maestro -> `/plan-maestro`, y no hay chips de PR, Dashboard, Curva S, Cronograma ni Paquetes. Coincide.
- Cuenta A en /mi-entorno: 12 enlaces (Gestionar -> /admin/usuarios, Ver todas, Crear RQ, Status RQ, Consolidado RQ, Cronograma, Plan Maestro, Status de RDTs -> /rdts/listado, Consolidado RDTs, Crear RDTs, Subir RDTs, mas el vinculo a portafolio).
- Cuenta B (Supervisor Operativo) con SV1: el panel izquierdo NO muestra Recursos ni grupo Proyecto; la pagina no muestra Editar servicio ni Editar checklist; el panel derecho conserva Requerimiento, Consolidado RQ, Subir RDTs, Notificaciones, Cronograma, Paquetes, Plan Maestro, PR, Dashboard, Curva S y Ver DP. En /mi-entorno B ve 9 enlaces de herramientas (sin Gestionar, Consolidado RQ ni el resto que ve A).
- **Hallazgo de linea base (F1/F2):** B recibe 200 por URL directa en /recursos/personal, cargos, equipos, causas-cnc, /admin/usuarios, /proyectos/SV1/editar, checklist/editar, dp, pr, dashboard, curva-s, cronograma, paquetes, plan-maestro y /rdts/crear; en las tres inspeccionadas (/admin/usuarios, editar, cargos) el HTML no trae texto de "No autorizado". Hoy la visibilidad se controla ocultando chips y paneles. 200 no prueba que el contenido cargue funcional.
- Diferencia codigo vs navegador: el chip Status de RDTs apunta a `/rdts/listado` en el DOM (la tabla derivada decia `/rdts/status`); la tabla se lee `/rdts/listado`.



## F0-C - PL-147 - Linea base «antes» por rol de las tablas 1 y 2 del flujo 14 (Worker local-3, 2026-09-29)

Metodo: (a) prueba vitest temporal `src/lib/permisos/_lb-f0.test.ts` (borrada; no se commitea) que evalua cada funcion `puede*` de `permisos.ts` (`1942b01`) con los 13 roles de `ROLES`; (b) Grep de guardias de paginas y APIs en `src/app`; (c) muestra en navegador con «Ver como» (asistente, supervisor_operativo, supervisor_logistica) con `fetch` sin efecto. Lectura: `✓` hoy si y objetivo si; `—` hoy no y objetivo no; `✓→—` hoy puede pero el flujo 14 (objetivo) dice que no; `—→✓` hoy no puede pero el objetivo dice que si. «Objetivo» = celdas de las tablas 1 y 2 aprobadas 2026-09-28 (no se copian: se marca solo la diferencia). Roles en orden: Admin, JP, JOT, SOT, Plnr, SCo, JCo, SOp, SLog, SAdm, SSO, Asist, RRHH.

### Tabla 1 rol x interfaz - hoy (UI y servidor)

| Fila | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH | Guardia hoy (UI / servidor) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dashboard del servicio (Parcial/Completo) | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | UI: chip visible a todos. Servidor: pagina sin guardia de rol (solo el toggle usa `puedeAdjudicarProyecto`). Objetivo: Completo con economia; Parcial 13 roles (brecha, nota 1 del flujo) |
| Dashboard del portafolio | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | Sin guardia de rol |
| PR | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | Chip visible a todos; pagina sin guardia |
| DP, ver | ✓ | ✓ | ✓ | ✓ | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | Chip «Ver DP» visible a todos; pagina sin guardia (solo `puedeSubirDocumento` para importar) |
| Curva S | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | — | ✓→— | `puedeVerCurvaS`: la pagina muestra mensaje de sin acceso (no redirige) y `GET /api/curva-s` 403; chip visible a todos |
| Plan Maestro, ver | ✓ | ✓ | ✓ | ✓→— | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | — | ✓→— | `puedeVerPlanMaestro`: pagina redirige a /mi-entorno; API 403 |
| Registro de costos, ver | —→✓ | ✓ | —→✓ | — | — | —→✓ | —→✓ | — | ✓→— | — | — | — | — | Pagina: entra quien sube o descarga (JP, SLog); redirige al servicio al resto; el GET del archivo solo `puedeDescargarRegistroCostosServicio` (JP) |
| Cronograma, ver | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | —→✓ | ✓ | Pagina redirige a /mi-entorno; API 403 |
| Paquetes de trabajo, ver | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | —→✓ | ✓ | Igual |
| RDTs status / archivo / consolidado | ✓ | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | ✓ | —→✓ | ✓ | —→✓ | ✓ | ✓ | `puedeVerRdts`: paginas /rdts, status, listado, consolidado redirigen; APIs 403 |
| RQ status | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | `/requerimientos` sin guardia de rol (alcance por OT); `GET /api/proyectos/[id]/requerimientos` sin guardia de rol |
| RQ consolidado | ✓ | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | Pagina redirige; `GET /api/logistica/requerimientos` 403 |
| Recursos: Personal, Cargos, Equipos | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | `puedeVerRecursos` (=`puedeVerApartadoProyectos`): panel oculta Recursos; pagina redirige a /mi-entorno; API 403 |
| Recursos: Causas CNC | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | Igual; API `catalogo-cnc` 403 |
| Ficha del servicio y grilla del portafolio | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Sin guardia de rol |
| Panel izquierdo del servicio | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | Grupos Proyecto y Recursos solo con `puedeVerApartadoProyectos` (Admin, JP); el resto de roles ve el panel sin ellos |
| Notificaciones y Mi entorno | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Sin guardia de rol (Mi entorno usa funciones solo para mostrar bloques) |

Extra (no esta en la tabla 1): `/admin/usuarios` = `puedeGestionarUsuarios` (Admin, JP); la pagina redirige a /programas.

### Tabla 2 rol x accion - hoy (UI y servidor)

| Fila | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH | Guardia hoy (UI / servidor) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Adjudicar proyecto / crear programa / portafolio | —→✓ | —→✓ | ✓ | — | — | — | — | — | — | — | — | — | — | `puedeAdjudicarProyecto`, `puedeCrearPrograma`, `puedeCrearPortafolio` (solo JOT); UI oculta botones y API 403 |
| Confirmar transicion de estado | —→✓ | —→✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Solo JOT; API 403 |
| Archivar proyecto | ✓ | —→✓ | ✓→— | — | — | — | — | — | — | — | — | — | — | Admin, JOT |
| Eliminar proyecto | ✓ | —→✓ | ✓→— | — | — | — | — | — | — | — | — | — | — | Admin, JOT; `DELETE /api/proyectos/[id]` (el GET de esa ruta usa la misma guardia) |
| Eliminar contenedor | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — | Solo Admin; API 403 «Solo el administrador…» |
| Editar servicio | —→✓ | —→✓ | ✓→— | — | — | — | — | — | — | — | — | — | — | Reusa `puedeAdjudicarProyecto` (solo JOT); pagina /editar redirige; API `/datos` 403 |
| Editar checklist | ✓ | —→✓ | ✓→— | — | — | — | — | — | — | — | — | — | — | Admin, JOT; pagina redirige; API 403 |
| Importar DP | ✓ | —→✓ | — | ✓→— | — | — | — | — | — | — | — | — | — | `puedeSubirDocumento(roles,"supervisor_oficina_tecnica")`: Admin y SOT; `POST /dp` 403 |
| Gestionar usuarios | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Admin, JP; API 403 |
| Editar perfil extendido (propio) | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | `puedeEditarPerfilExtendido` (Admin, JP, JOT) no se usa en ninguna guardia; `PATCH /api/perfil` solo pide sesion: los 13 roles pasan (400 «Nada que actualizar» con cuerpo vacio en la muestra) |
| Asignar rol administrador | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | Solo Admin |
| «Ver como» | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | Solo Admin real (`POST /api/ver-como` 403 para no admin; comprobado con la cuenta B) |
| Subir documento del proyecto (rol responsable = `*`, no incluido) | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — | `puedeSubirDocumentoAsignado`: Admin + rol responsable del documento (`*`) + usuario asignado; JP hoy solo si es responsable |
| Crear personal | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | `POST /api/recursos/personal` usa `puedeVerRecursos` |
| Editar / eliminar personal | —→✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — | No existe pantalla ni API (por construir) |
| Crear / editar / eliminar cargo | —→✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — | No existe (Cargos solo lectura) (por construir) |
| Crear / editar / eliminar equipo | —→✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — | No existe (Equipos solo lectura) (por construir) |
| Crear causa CNC | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | `POST /api/recursos/catalogo-cnc` |
| Activar / desactivar causa CNC | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | `PATCH /api/recursos/catalogo-cnc/[id]` |
| Editar descripcion de causa CNC | —→✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — | No existe (por construir) |
| Subir RDT (PDF o foto) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | `puedeSubirRdt`; `POST /api/rdts` |
| Crear RDT estructurado | ✓ | ✓ | —→✓ | — | — | — | — | ✓ | — | — | — | — | — | `puedeCrearRdtEstructurado` (Admin, JP, SOp); JOT no |
| Validar / rechazar RDT | ✓ | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | `puedeValidarRdt` (Admin, JP): `PATCH /api/rdts/partes/[id]` accion VALIDAR o RECHAZAR |
| Corregir RDT rechazado | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | — | Sin funcion propia: sigue a `puedeCrearRdtEstructurado` |
| Rechazar un RDT ya validado | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Misma guardia que Validar (`PATCH` RECHAZAR sobre VALIDADO); sin funcion propia |
| Eliminar RDT | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — | Solo Admin; `DELETE /api/rdts/[id]` y `/partes/[id]` |
| Subir / reemplazar cronograma | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Igual al objetivo |
| Gestionar Plan Maestro | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Igual al objetivo |
| Gestionar paquetes de trabajo | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Igual al objetivo |
| Crear RQ | —→✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | `puedeCrearRequerimiento` excluye a Admin: `POST .../requerimientos` da 403 al Admin; `siguiente-codigo` y `adjuntos` si lo dejan pasar (guardia aparte) |
| Comentar RQ | ✓ | ✓ | — | — | — | — | — | — | ✓ | — | — | — | — | Igual al objetivo |
| Actualizar estado de RQ | —→✓ | — | — | — | — | — | — | — | ✓ | — | — | — | — | Solo SLog; API 403 |
| Derivar RQ a logistica | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Igual al objetivo |
| Eliminar RQ | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — | Solo Admin |
| Descargar consolidado RQ | ✓ | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | Igual al objetivo (`exportar-004` POST) |
| Subir registro de costos | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | Solo SLog; API 403 |
| Descargar registro de costos | —→✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Solo JP hoy; falta Admin |

Sin guardia de rol hoy y fuera de las tablas: `GET /api/proyectos/[id]/dp/exportar` y `GET .../requerimientos/exportar` (PL-127); `GET /api/proyectos/[id]/partidas` (debe seguir asi, lo usa Crear RQ).

### Muestra en navegador con «Ver como» (PL-147)

Servidor dev `-p 3111` en el worktree local-worker-1; solo lectura (`fetch` en un `browser_evaluate`; escrituras con cuerpo vacio o id inexistente `0000…`). La sesion que encontre abierta era la cuenta B (Supervisor Operativo, no admin): `POST /api/ver-como` dio 403 con los tres roles, lo que confirma `puedeSimularRol` solo Admin y sirvio de muestra del rol SOp real. Cerre sesion e inicie con la cuenta A (admin real) para simular; al terminar `DELETE /api/ver-como` = 200 (rol propio restaurado). Servicio de prueba SV1 = PS-0004.

Resultado (P = pagina: `200` + `[REDIR destino]` si el HTML trae `NEXT_REDIRECT`, es decir el servidor redirige; A = API, codigo HTTP). Asistente / SOp / SLog:

| Ruta | Asistente | SOp | SLog | Coincide con la tabla calculada |
|---|---|---|---|---|
| P recursos personal, cargos, equipos, causas-cnc | REDIR /mi-entorno | REDIR /mi-entorno | REDIR /mi-entorno | Si |
| P /admin/usuarios | REDIR /programas | REDIR /programas | REDIR /programas | Si |
| P cronograma, paquetes-trabajo, plan-maestro | REDIR /mi-entorno | 200 | 200 | Si (asistente sin acceso) |
| P /rdts, status, listado, consolidado | 200 | 200 | REDIR /mi-entorno | Si (`puedeVerRdts`) |
| P /rdts/crear | REDIR | 200 | REDIR | Si |
| P /logistica/consolidado-rq | REDIR | REDIR | 200 | Si |
| P editar servicio, checklist/editar | REDIR al servicio | REDIR | REDIR | Si |
| P registro-costos | REDIR al servicio | REDIR | 200 | Si (JP/SLog) |
| P dp, pr, dashboard, curva-s, requerimientos/nuevo, programas, notificaciones, mi-entorno | 200 | 200 | 200 | pr, dashboard, dp: sin guardia (brecha vs objetivo). curva-s: 200 con mensaje «sin acceso» para asistente (no redirige) |
| A recursos (GET/POST personal, catalogo-cnc GET/POST/PATCH) | 403 | 403 | 403 | Si |
| A admin/usuarios GET/POST/DELETE | 403 | 403 | 403 | Si |
| A programas/portafolios POST | 403 | 403 | 403 | Si (solo JOT) |
| A DELETE programas, portafolios, requerimientos, rdts, rdts/partes | 403 | 403 | 403 | Si |
| A proyectos POST, siguiente-ot, [id] GET/PATCH/DELETE, confirmar-transicion, datos, tipo-dashboard, checklist, dp POST | 403 | 403 | 403 | Si |
| A registro-costos GET | 403 | 403 | 403 | Si (solo JP) |
| A registro-costos POST | 403 | 403 | 403 «No tienes esta OT a cargo» | Si: SLog pasa la guardia de rol y frena el alcance (R28) |
| A logistica/requerimientos GET / exportar-004 POST | 403 | 403 | 200 / 400 | Si |
| A comentarios POST | 403 | 403 | 400 (paso el rol) | Si |
| A rdts GET | 200 | 200 | 403 | Si |
| A rdts POST | 403 | 500 (paso el rol; cuerpo JSON no es formulario) | 403 | Si (`puedeSubirRdt` SOp, no asistente ni SLog). El 500 es solo por el cuerpo vacio |
| A rdts/catalogos, plantillas | 403 | 200 | 403 | Si (`puedeCrearRdtEstructurado`) |
| A rdts/consolidado | 400 (paso el rol) | 400 | 403 | Si |
| A cronograma, plan-maestro, paquetes GET | 403 | 200 | 200 | Si |
| A cronograma, plan-maestro, paquetes POST | 403 | 403 | 403 | Si |
| A curva-s GET | 403 | 200 | 200 | Si |
| A `PATCH /api/perfil` | 400 | 400 | 400 | Sin guardia de rol (hallazgo) |
| A `POST /api/proyectos/[id]/requerimientos` | 403 «No tienes esta OT a cargo» | igual | igual | Con id inexistente la guardia de alcance se evalua antes que la de rol; no prueba el rol |
| A dp/exportar, requerimientos siguiente-codigo, partidas | 400 / 200 / 200 | igual | igual | Sin guardia de rol (dp/exportar; PL-127) |

Correcciones a F0-B: en el HTML de Next el `redirect()` de servidor llega con estado HTTP 200 (la respuesta ya empezo a transmitirse) y un marcador `NEXT_REDIRECT`. Por eso el «200 por URL directa» de la cuenta B en Recursos, /admin/usuarios, editar servicio y checklist/editar **no** es acceso: son redirecciones del servidor (comprobado aqui con la cuenta A simulando). El 200 sin marcador (PR, Dashboard, DP, Curva S con mensaje) si es contenido sin guardia de rol.

Sin efecto sobre datos: ninguna llamada creo ni borro registros (todas con cuerpo vacio o id inexistente; la unica en pasar guardia con efecto potencial fue `POST /api/rdts` con JSON vacio, que fallo con 500 sin escribir).

### Hallazgos de PL-147 (para F1 a F6)

1. **Diferencias hoy contra objetivo (36 celdas marcadas `→`)**: Dashboard, portafolio, PR y DP sin guardia; Curva S y Plan Maestro solo excluyen al asistente; Registro de costos visible a JP y SLog; `puedeAdjudicarProyecto` solo JOT (falta Admin y JP; Editar servicio la reusa); Archivar/Eliminar proyecto y Editar checklist Admin+JOT (falta JP, sobra JOT); Confirmar transicion solo JOT; Importar DP hoy Admin+SOT (falta JP, sobra SOT); Editar perfil hoy 13 roles; Subir doc proyecto no incluye JP; Crear RQ excluye Admin; Actualizar estado RQ sin Admin; Eliminar RQ/RDT/contenedor sin JP; Descargar registro de costos sin Admin; Crear RDT sin JOT; Validar RDT sin JOT; Recursos: panel/CNC solo Admin+JP (objetivo: consulta para los 13) y sin edicion/borrado.
2. `puedeEditarPerfilExtendido` no se usa; el perfil propio se edita sin guardia de rol (13 roles).
3. Los roles admitidos por «Ver como» coinciden con `ROLES` (13); DELETE de ver-como disponible para quien tenga sesion.
4. Filas de las tablas que hoy se calculan con una misma funcion (alias): Editar servicio = Adjudicar; Corregir RDT = Crear estructurado; Rechazar validado = Validar; Crear personal = Ver Recursos; Activar/desactivar CNC = Gestionar CNC.
5. Sin cambio previsto (igual al objetivo): Subir RDT, Cronograma, Plan Maestro, Paquetes (gestion), Comentar RQ, Derivar RQ, Descargar consolidado RQ, Subir registro de costos, Asignar rol admin, Ver como, Gestionar usuarios.

## F1-A · PL-51 y registro base (2026-09-29) — Conforme

- Commit `06f40f3` en `local-worker-1`: `src/lib/config/registro-accesos.ts` (+ `.test.ts`), `nav-proyecto.ts` reescrito como derivación pura, `nav-proyecto.test.ts` reescrito por ubicación.
- Registro: 41 accesos con id, etiqueta, grupo, tipo, ruta, requiereServicio (`si`/`opcional`/`no`), permiso (obligatorio; `PERMISO_LIBRE` explícito si no hay función vigente), visibilidad por panel, icono, color, orden. `validarRegistro()` detecta ids duplicados, permiso omitido, grupo desconocido, visibilidad incompleta y `si` sin ruta; probada con registro defectuoso.
- `NAV_PROYECTO`, `CHIPS_ACCESO_RAPIDO`, `encontrarItemNavProyecto`, `clavesConRutaEntorno`, `hrefItemPanel` derivan del registro; `hrefItemPanel` generaliza las 9 excepciones por clave a `requiereServicio`. Cronograma sigue `si` (C20). Sin cambio visible, sin tocar WorkspaceShell/PanelSecciones/grupo-proceso.
- `npm test`: 61 archivos, 540 pruebas verdes (antes 508). `npm run lint`: 9 errores, 18 advertencias (= línea base). `npx tsc --noEmit`: sin errores.


## F1-B - PL-50 y PL-52 (2026-09-29, commit 2d6c9d9 en local-worker-1)
**Que se hizo.** Mi entorno (`herramientasPorGrupo`), Accesos rapidos (`CHIPS_ACCESO_RAPIDO`, etiqueta corta `Requerimiento`), `hrefItemPanel` y las 4 rutas fijas de Recursos (`derivarRecursos()` en `WorkspaceShell`) derivan de `REGISTRO_ACCESOS`. Registro: 46 entradas = 41 del nav + `enviar-notificacion` (grupo Mi entorno, accion de pagina, sin ruta) + 4 de Recursos de empresa (`recursos-personal/cargos/equipos/causas-cnc`, permiso = `puedeVerRecursos` / `puedeGestionarCatalogoCnc`). Los dos grupos nuevos viven en `GRUPOS_FUERA_DE_NAV` y no entran en `NAV_PROYECTO` (sigue con 41). Campos nuevos en `visible`: `centroOrden`, `centroEtiqueta`, `centroConServicio` (transitorio: solo Crear RQ y Subir RDTs enviaban `?proyectoId=`; F2-A lo generaliza), `centroSiempreHabilitado` (transitorio: Crear RQ estaba siempre habilitado, aunque `puedeCrearRequerimiento` diga otra cosa; se conserva para no cambiar quien puede), `accesoRapidoEtiqueta`. Materiales queda como `span` inerte en el panel izquierdo (no se migra; F3 lo retira).
**PL-50 - busqueda de codigo.** Grep de `NAV_PROYECTO|herramientasPorGrupo|CHIPS_ACCESO_RAPIDO|hrefItemPanel|RUTA_PERSONAL|RUTA_CARGOS|RUTA_EQUIPOS|RUTA_CAUSAS_CNC` en `src` (sin tests): ya no hay listas propias; `grupo-proceso.ts` no tiene `chipsRdts` ni listas de chips, `WorkspaceShell` ya no declara `RUTA_*` ni `COLOR_RECURSOS` propio, `PanelSecciones` ya no tiene `ETIQUETA_CHIP`. Ver diff del commit.
**PL-52 - tabla clave anterior -> id nuevo (Mi entorno, 10 chips, sin perdidas).** enviar-notificacion -> enviar-notificacion; crear-requerimiento-servicios -> igual; status-requerimiento -> igual; consolidado-rq -> igual; cronograma -> igual; plan-maestro -> igual; **listado-rdts -> status-rdts** (E3); consolidado-rdts -> igual; crear-rdt -> igual; **subir-rdt -> rdt** (union). Accesos rapidos (7): mismos ids del nav (tareo-moi, pets, acta-conformidad, status-servicios, status-requerimiento, consolidado-rq, rdt). NAV_PROYECTO (41): ids sin cambio (identidad). Recursos: Personal, Cargos, Equipos, Causas CNC -> `recursos-*`; Materiales no se migra.
**Diferencias visibles declaradas.** (1) E3: el chip «Status de RDTs» de Mi entorno va ahora a `/rdts/status` (antes `/rdts/listado`, lo que F0-B/LB-03 marcaba como diferencia con el panel derecho); «Archivo de RDTs subidos» = `/rdts/listado` en el panel derecho (ya lo era). (2) Union `rdt`/`subir-rdt`: la clave interna cambia; etiqueta y ruta iguales. Sin otra diferencia (etiquetas, orden, hrefs con y sin servicio, `habilitado` y `tituloDeshabilitado` para los 13 roles y sin rol, mismo conjunto en los 8 grupos).
**Prueba de equivalencia.** `src/lib/config/equivalencia-f1b.test.ts` (8 pruebas) contra la linea base congelada de 1942b01. Sin navegador: no hizo falta, la equivalencia se comprueba sobre las funciones que la interfaz consume.
**Tests actualizados (R12).** `registro-accesos.test.ts` (46 entradas, 41 en el nav, izquierdo incluye los 4 de Recursos), `grupo-proceso.test.ts` (claves `status-rdts`/`rdt`, ruta `/rdts/status`).
**Resultados.** `npm test`: 62 archivos, 548 pruebas verdes (antes 61/540). `npm run lint`: 9 errores, 18 advertencias (= base). `npx tsc --noEmit`: sin errores.

## F2-A - Servicio persistente en el shell (Worker local-3, 2026-09-30)

Codigo: helper `src/lib/config/servicio-contexto.ts` (+ test, 31 casos), `WorkspaceShell.tsx`, `(workspace)/layout.tsx` (lista de servicios vigentes visibles por RLS -> shell), `registro-accesos.ts` (retirado `centroConServicio`), `grupo-proceso.ts` (Mi entorno envia `?proyectoId=` segun `requiereServicio` si/opcional), `equivalencia-f1b.test.ts` (diferencia F2-A declarada). npm test 590/590; tsc limpio; lint 9 errores y 18 advertencias (= baseline). Navegador (Playwright, dev -p 3111, solo lectura): sesion A = Administrador, B = Supervisor Operativo (Lopez Caceres). Capturas 1440 en `capturas/paneles-servicio-persistente/PL-01, 15, 16, 37, 47, 66.jpg`. Consola sin errores en las corridas de A y B.

- PL-01 (A, 1440): tras elegir SV1 en el portafolio, URL `/proyectos/dc850536-...` ; panel izquierdo "SERVICIO ACTUAL PS-0004 Movimiento de tierra, e instalacion de bancoductos"; panel derecho sin "Selecciona un servicio", chips con href: Subir RDTs, Cronograma, Paquetes, Plan Maestro con `?proyectoId=<SV1>`, PR/Dashboard/Curva S en `/proyectos/<SV1>/...`; inertes (sin ruta, igual que la linea base): Tareo MOI, Pets, Acta de conformidad, Status de servicios. Movil 390: cajon izquierdo muestra PS-0004 y el derecho los mismos hrefs.
- PL-15: Todos los servicios -> SV2: izquierdo "PS-0005 TIE - IN"; todos los hrefs del derecho llevan el id de SV2, ninguno el de SV1.
- PL-16: en el portafolio (tras "Todos los servicios") sin bloque de servicio, aparece "Selecciona un servicio...", chips con servicio ausentes (Cronograma, Paquetes, PR, Dashboard, Curva S) y los que funcionan sin servicio como en LB-03: Requerimiento `/requerimientos`, Consolidado RQ `/logistica/consolidado-rq`, Subir RDTs `/mi-entorno?accion=subir-rdt`, Plan Maestro `/plan-maestro`, Notificaciones `/notificaciones`. Status de RDTs no cambio (requiereServicio no; sin tocar).
- PL-37: SV1 -> PS-0004 y SV2 -> PS-0005 con id de la URL; la ficha (`/proyectos/<SV2>/dp`) abre con "PS-0005 — TIE - IN". B (Supervisor Operativo) ve lo mismo en ambos.
- PL-47: `?proyectoId=` con uuid inexistente, texto basura (`abc'<script>`) y `../../admin`: sin bloque de servicio, sin nombre ni N° OT en el panel, "Selecciona un servicio" mostrado, sin errores de consola, con A y con B. El caso "archivado" no se pudo probar con dato real (no hay servicio archivado; no se archiva ni escribe): usa la misma ruta de codigo (la lista del layout filtra `archivado=false`, igual que `/api/proyectos/vigentes`), verificado por el caso inexistente y por la prueba unitaria `resolverServicioVisible`. Sin acceso: la lista viene de la consulta con RLS del usuario.
- PL-66: `/notificaciones` sin servicio (A y B): izquierdo con Recursos de empresa visible para A (Personal, Cargos, Equipos, Materiales, Causas CNC), derecho con "Selecciona un servicio", sin errores. Movil 390 igual.
- PL-72: prueba unitaria del helper: `esIdServicio` (solo uuid), `esRutaInterna` (rechaza `//host`, `/\host`, `https:`, `javascript:`, saltos de linea, backslash), `conServicio`/`sinServicio` devuelven `/` ante ruta no interna y no anaden servicio invalido. Alcance: el helper esta listo; su uso en los redirects del servidor es F2-D.
- Persistencia (A2): con servicio activo, los enlaces de Recursos, Usuarios, Notificaciones, Configuraciones y Mi entorno del panel izquierdo llevan `?proyectoId=`; "Todos los servicios" y el logo no. Notificaciones del grupo Proyecto y los accesos `requiereServicio: no` no lo envian (segun brief: solo si/opcional).
- `centroSiempreHabilitado` NO se retiro: quitarlo dejaria Crear RQ deshabilitado para los roles sin `puedeCrearRequerimiento` (cambia quien puede). Se deja y se registra.


## F2-B (Worker local-3, 2026-09-30) - cuenta A (Administrador), escritorio 1440, dev :3111
Criterio de "ambos paneles con SV": panel izquierdo muestra SERVICIO ACTUAL con el numero; en el derecho, todos los enlaces con servicio (7/7) llevan el id. SV1 = PS-0004 (dc850536-...), SV2 = PS-0005 (3b869b75-...). Codigo: `useServicioEnUrl.ts` (nuevo) + los tres formularios (`router.replace` con `conServicio`, sin apilar historial; sincroniza URL a selector solo cuando cambia la URL).
- PL-02 Conforme: `/cronograma?proyectoId=<SV1>`, selector = SV1, izq PS-0004, der 7/7. Captura `capturas/paneles-servicio-persistente/PL-02.jpg`.
- PL-03 Conforme: `/paquetes-trabajo?proyectoId=<SV1>` idem (selector = SV1 tras cargar la lista). Captura PL-03.jpg.
- PL-04 Conforme: `/plan-maestro?proyectoId=<SV1>` idem. Captura PL-04.jpg.
- PL-14 Conforme: en las tres pantallas, selectOption SV2 -> URL pasa de `?proyectoId=<SV1>` a `?proyectoId=<SV2>`, izq PS-0005, der 7/7, selector = SV2 (history +1 por la navegacion inicial, sin bucle). Captura PL-14.jpg (Cronograma tras el cambio).
- PL-11 Conforme: con `?proyectoId=<SV1>` en `/notificaciones`, `/mi-entorno&accion=crear-rq`, `/mi-entorno&accion=subir-rdt`, `/recursos/personal`, `/recursos/cargos`, `/recursos/equipos`: izq PS-0004, der 7/7. Enlaces de Recursos en el panel llevan el servicio. Captura PL-11.jpg (Mi entorno crear-rq). Nota: el enlace "Notificaciones" del grupo Proyecto no lleva servicio (hallazgo de F2-A, `requiereServicio: no`); el del pie si.
- PL-12 Observado: SV1 y SV2 en `/proyectos/<id>/dp`, `pr`, `dashboard`, `curva-s`: izq y der 7/7 (regresion OK). `registro-costos` con cuenta A redirige a `/proyectos/<id>` por la guardia (solo supervisor_logistica sube, jefe_de_proyectos descarga) con paneles en el servicio; no se vio la pantalla (habria que probar con esos roles). Captura PL-12.jpg (Dashboard SV1).
- Defecto previo corregido: `/api/cronograma` sin cronograma no devuelve `partidasDp` y el formulario fallaba (`undefined.filter`) al elegir PS-0005; ahora `?? []`.
- Comandos: npm test 590/590, tsc limpio, lint 9 errores y 18 advertencias (= baseline).


## Evidencia F2-C (2026-09-30, cuenta A, escritorio 1440, dev :3111; SV1 = PS-0004, SV2 = PS-0005)

Capturas en `capturas/paneles-servicio-persistente/PL-xxx.jpg`. Datos reales: solo lectura; PL-05 no guardo nada.

| ID | Resultado | URL / dato observado |
|---|---|---|
| PL-05 | Conforme | `/rdts/crear?proyectoId=<SV1>`: selector = PS-0004; panel con "Servicio actual PS-0004". Cambiar el selector a SV2 actualizo la URL a SV2 y el panel a PS-0005 (E1 editable). |
| PL-06 | Conforme | `/rdts/status?proyectoId=<SV1>`: filtro N° OT = PS-0004, 71 filas, todas PS-0004; panel PS-0004. Con SV2 (sin partes) el filtro queda en PS-0005 en el estado y la tabla vacia. |
| PL-07 | Observado | `/rdts/listado?proyectoId=<SV1>`: panel PS-0004; el archivo esta vacio (0), no hay filas ni opciones para leer el filtro; mismo codigo que Status de RDTs. |
| PL-08 | Conforme | `/rdts/consolidado?proyectoId=<SV1>`: selector = PS-0004 y consolidado cargado (2 tablas) sin clic; al elegir SV2 la URL y el panel pasan a SV2. |
| PL-09 | Conforme | `/requerimientos?proyectoId=<SV1>`: filtro N° OT = PS-0004 (leido de props de React; no hay RQ en ningun servicio), panel PS-0004. Con `&ots=<SV2>`: filtro = PS-0005 y panel sigue en PS-0004. |
| PL-10 | Conforme | `/logistica/consolidado-rq?proyectoId=<SV1>`: filtro N° OT = PS-0004, panel PS-0004 (0 materiales: no hay RQ). |
| PL-13 | Conforme | `/proyectos/<SV1>/requerimientos` -> `/requerimientos?ots=<SV1>&proyectoId=<SV1>`; filtro PS-0004, panel PS-0004. |

Prueba de equivalencia (declarada): Status RQ, Consolidado RQ, Status/Archivo/Consolidado de RDTs y Crear RDTs pasan de `requiereServicio: 'no'` a `'opcional'` y su ruta envia `?proyectoId=`; no cambia `habilitado` (los 13 roles siguen igual, prueba F1-B verde). Resultados: npm test 591/591, tsc limpio, lint 9 errores / 18 avisos (= baseline).

### F2-D (Worker local-3)

| ID | Estado | Evidencia |
|---|---|---|
| PL-19 | Conforme | Cuenta B, escritorio 1440: `/recursos/causas-cnc?proyectoId=<SV1>` (pantalla que B no puede usar) aterriza en `/mi-entorno?proyectoId=<SV1>`. Las 14 paginas con `redirect('/mi-entorno')` usan `conServicio('/mi-entorno', proyectoId)` (mi-perfil, rdts, recursos/* ahora leen `searchParams`). Captura `capturas/paneles-servicio-persistente/PL-19.jpg`. |
| PL-20 | Conforme | Pruebas unitarias nuevas (servicio-contexto.test.ts, ots-seleccion.test.ts). Codigo: `FormularioCrearRdt` -> `conServicio('/rdts/status', parte.proyectoId)`; `FormularioRequerimiento` -> `rutaStatusRq({ proyectoId })`; `CabeceraPagina` sigue siendo componente de servidor y delega el chip al cliente `SalirAMiEntorno`. Redirects de `proyectos/[id]/mi-entorno`, `entorno/[grupo]` y `requerimientos` ya conservaban el id (revisados). No se guardaron datos. |
| PL-21 | Conforme | Cuenta B en `/rdts/status?proyectoId=<SV1>`: chip "Salir a Mi entorno" con href `/mi-entorno?proyectoId=<SV1>`; clic aterriza en esa URL. Capturas `PL-21-antes.jpg` y `PL-21-despues.jpg`. Sin servicio el chip va a `/mi-entorno` (prueba unitaria). |
| PL-70 | Conforme | Revision de codigo: paginas que reciben `proyectoId` lo usan solo tras `obtenerUsuarioActual` + guardia de rol; `servicioDePagina` valida formato uuid + RLS + no archivado; los redirects solo reflejan ids con formato uuid (`conServicio`). APIs con `?proyectoId=` (cronograma, hitos, plantilla, paquetes-trabajo, plan-maestro, rdts/catalogos|consolidado|partes|exportar, curva-s, notificaciones): auth + rol; lecturas por cliente RLS; escrituras con `exigirAlcance`/`validarEscrituraProyecto`. Nota: `rdts/exportar` y `notificaciones` usan admin solo para storage/N° OT, sin proyectoId. El alcance por OT al leer es C21 (fase posterior). PL-46 no era de esta tanda. |

Nota: por error el servicio usado en la verificacion fue PS-0005 (SV2) y no PS-0004; el comportamiento es identico (id de servicio visible para B).
Resultados: npm test 596/596, tsc limpio, lint 9 errores / 18 avisos (= baseline).


## F2-E · PL-17, PL-18, PL-67, PL-69 (2026-09-29, worker F2-E, dev 3111, escritorio 1440, cuentas A y B, solo lectura)

SV1 = PS-0004 (dc850536…), SV2 = PS-0005 (3b869b75…, sin DP). Sin cambios de codigo en F2-E.

**PL-18 y PL-67 (Conforme).** Un script de Playwright (`page.goto` por ruta + `MutationObserver` sobre `document` y `PerformanceObserver layout-shift` inyectados con `addInitScript`, es decir activos desde el primer render) recorrio 23 rutas con `?proyectoId=SV1`, con cuenta B y con cuenta A. En las 46 cargas: el texto "Selecciona un servicio" nunca aparecio (ni al final ni en ningun instante de la carga; conteo del observador = 0); desplazamiento de layout acumulado maximo 0.007 (umbral CLS bueno: 0.1). Control positivo: `/cronograma` sin servicio si activa el observador (mensaje visible y contador > 0), asi que el observador funciona. Rutas: cronograma, paquetes-trabajo, plan-maestro, rdts/crear|status|listado|consolidado, requerimientos, logistica/consolidado-rq, notificaciones, mi-entorno (+`accion=crear-rq`, `accion=subir-rdt`), recursos/personal|cargos|equipos|causas-cnc, proyectos/SV1/dp|pr|dashboard|curva-s|registro-costos|requerimientos. Cuenta A: todas conservan la URL con SV1 (15 enlaces con id en los paneles; 14 en `/proyectos/<id>/…`); registro-costos redirige a `/proyectos/SV1` (guardia de rol, ya visto en PL-12) y `/proyectos/SV1/requerimientos` a `/requerimientos?ots=SV1&proyectoId=SV1`. Cuenta B (Supervisor Operativo): consolidado-rq y las 4 rutas de recursos aterrizan en `/mi-entorno?proyectoId=SV1` (PL-19), sin mensaje "Selecciona…". Captura de la pantalla cargada: `capturas/paneles-servicio-persistente/PL-18.jpg` (PL-67.jpg es la misma imagen; la prueba de PL-67 es el observador, no la imagen).

**PL-17 (Conforme, cuenta A).** Secuencia: `/cronograma?proyectoId=SV1` -> clic chip Plan Maestro `/plan-maestro?proyectoId=SV1` -> Atras `/cronograma?proyectoId=SV1` -> Adelante `/plan-maestro?proyectoId=SV1` -> F5 igual -> pestana nueva con esa URL igual. En cada paso: PS-0004 en los paneles, 15 enlaces con `proyectoId=SV1`, sin el mensaje "Selecciona…". Captura `PL-17.jpg`.

**PL-69 (Conforme con observacion cosmetica, cuenta A).** SV2 = PS-0005 sin DP (DP muestra "Todavia no se importo DP"; Paquetes "Este servicio todavia no tiene paquetes de trabajo"). En 11 pantallas: panel con PS-0005, 14-15 chips con `proyectoId=SV2`, 0 elementos `aria-disabled`, sin mensaje "Selecciona…", sin errores; Status de RDTs y Status RQ con 0 filas, Dashboard y Curva S renderizan. Observacion (misma que F2-C): en Paquetes, Crear RDTs y Consolidado RDTs el selector de OT queda en el placeholder ("Seleccione…", "Elige el servicio…", "Elige el N° OT…") y en Status de RDTs los selects dicen "Todos", porque sus opciones salen de datos (servicios con DP/partidas o RDTs) y PS-0005 no esta entre ellas; las pantallas ya conocen el servicio (mensajes de estado vacio propios). No se considera fallo de PL-18/PL-69 (cosmetico, no afecta paneles ni chips). Captura `PL-69.jpg` (Status de RDTs con SV2).

### Resumen de F2 (PL-01 a PL-21 y PL-66/67/69/70/72)

| ID | Estado | ID | Estado |
|---|---|---|---|
| PL-01 | Conforme | PL-13 | Conforme |
| PL-02 | Conforme | PL-14 | Conforme |
| PL-03 | Conforme | PL-15 | Conforme |
| PL-04 | Conforme | PL-16 | Conforme |
| PL-05 | Conforme | PL-17 | Conforme |
| PL-06 | Conforme | PL-18 | Conforme |
| PL-07 | Observado (archivo RDTs vacio; a F6) | PL-19 | Conforme |
| PL-08 | Conforme | PL-20 | Conforme |
| PL-09 | Conforme | PL-21 | Conforme |
| PL-10 | Conforme | PL-66 | Conforme |
| PL-11 | Conforme | PL-67 | Conforme |
| PL-12 | Observado (Registro de costos exige rol; a F6) | PL-69 | Conforme (cosmetico anotado) |
| PL-70 | Conforme | PL-72 | Conforme |

## F2B-A · PL-92, PL-94, PL-119, PL-120 y parte F2B de PL-88 (Worker local-3, 2026-09-30) — Conforme (PL-88 sigue abierto hasta F5B-A)

Entorno: dev :3111 en el worktree local-worker-1, cuenta A (admin real) con «Ver como» recorriendo los 13 roles con un solo `browser_evaluate` (POST /api/ver-como por rol, `fetch`; DELETE al final, 200). SV1 = PS-0004. Solo lectura: las escrituras se probaron con cuerpo `{}` o id `0000…` (400 = pasó la guardia de rol, 403 = rechazado por rol). Vitest: 599/599 (`permisos.test.ts` recorre `ROLES`); tsc sin errores; lint 9 errores / 18 advertencias (igual al baseline).

Cambios: `puedeVerRdts`, `puedeVerCronograma`, `puedeVerPaquetesTrabajo`, `puedeVerConsolidadoRq`, `puedeVerRecursos` y la nueva `puedeVerStatusRequerimiento` = los 13 roles (un usuario sin rol conocido: rechazado). `puedeDescargarConsolidadoRq` deja de ser alias y conserva su conjunto (admin, JP, JOT, SLog). `POST /api/recursos/personal` pasa a `puedeVerApartadoProyectos` (mismo conjunto de antes: admin, JP). Causas CNC: página y `GET catalogo-cnc` con `puedeVerRecursos`; alta/baja siguen con `puedeGestionarCatalogoCnc`; la tabla oculta «Nueva causa» y «Activar/Desactivar» a quien no gestiona; Personal oculta el formulario de alta a quien no puede crear. Guardia nueva en `/requerimientos` y `GET proyectos/[id]/requerimientos`. Textos `tituloDeshabilitado` obsoletos retirados; panel izquierdo muestra Causas CNC a quien ve Recursos.

Tabla 13 roles (orden Admin, JP, JOT, SOT, Plnr, SCo, JCo, SOp, SLog, SAdm, SSO, Asist, RRHH). Resultado idéntico en los 13 roles en cada fila:
| Ruta | 13 roles |
|---|---|
| Páginas cronograma, paquetes-trabajo, rdts, rdts/status, rdts/listado, rdts/consolidado, logistica/consolidado-rq, recursos/{personal,cargos,equipos,causas-cnc}, requerimientos | abren (sin NEXT_REDIRECT) |
| GET cronograma, cronograma/hitos, paquetes-trabajo, rdts, rdts/consolidado, rdts/partes, logistica/requerimientos, recursos, recursos/personal, recursos/catalogo-cnc, proyectos/SV1/requerimientos, proyectos/SV1/partidas | 200 |
| GET rdts/partes/{id inexistente}/historial | 404 (pasó la guardia) |
| POST catalogo-cnc `{}`, PATCH catalogo-cnc/{id} `{}`, POST recursos/personal `{}` | Admin 400, JP 400; los otros 11 roles 403 |

Ninguna respuesta dio «No tienes esta OT a cargo» (la cuenta A ve todas las OT).
- PL-92 Conforme: 13 roles abren `/requerimientos` y su API; función nueva probada por vitest con `[]` y rol ajeno (rechazo). Sin sesión → `/login`: guardia `if (!usuario) redirect('/login')` sin cambios, verificada por lectura de código, no en navegador. Captura PL-092.jpg.
- PL-94 Conforme: con «Ver como» asistente, `/proyectos/SV1/requerimientos/nuevo` carga el formulario (24 controles, desplegable de partidas con 15 opciones, botones «Ver partidas», «Agregar ítem», «Crear requerimiento de servicios»); no se guardó nada. `GET partidas` 200 en los 13 roles. Captura PL-094.jpg.
- PL-119 Conforme: tabla anterior; asistente abre Cronograma. Las acciones dentro de cada pantalla no se tocaron (F5C). Captura PL-119.jpg (Cronograma como asistente).
- PL-120 Conforme: consulta abierta a 13 roles en páginas y API; alta/baja CNC solo admin/JP (403 en los otros 11 con cuerpo/id inválido). Como asistente la pantalla muestra 12 filas sin «Nueva causa» ni «Activar/Desactivar». Captura PL-120.jpg.
- PL-88 (parte F2B): funciones de ver sin economía implementadas y probadas recorriendo `ROLES`.

Nota: `rdts/exportar`, `rdts/partes/[id]/pdf` y `rdts/[id]/archivo` usan `puedeVerRdts`, por lo que ahora quedan abiertas a los 13 roles (coincide con la propuesta del artefacto en PL-127; sigue «por decidir» en el flujo 14).


## F2B-B parte 1 · PL-121 (2026-09-29) — Observado
- Método: Grep de dinero (USD, S/, precio, costo, tarifa, monto, importe, moneda, currency) sobre TablaConsolidadoRdts, FormularioPaquetesTrabajo, TablaStatusRdts, TablaListadoRdts, ListadoRequerimientos, TablaConsolidadoRq, TablaRecursos, TablaPersonal, GrillaProyectosReales y proyectos/[id]/page.tsx; más escaneo de texto renderizado en pantalla (cuenta A y cuenta B, PS-0004/PS-0005): consolidado RDTs, paquetes, status, listado RDTs, RQ, consolidado RQ, personal, cargos, equipos, causas CNC, ficha, portafolio.
- Resultado en pantalla: ninguna muestra USD, S/ ni importes. Coincidencias de texto sin dinero: menú lateral («Supervisor de Costos», «Jefe de Costos», «Costos»), «Recursos hh, hm, mat. (s/c)» y el recurso de prueba «CARGO INVENTADO SIN TARIFA» (nombre de dato).
- HALLAZGO (R25, no editado): `src/app/api/paquetes-trabajo/route.ts` línea ~72 (GET) selecciona `precio_unitario` de `dp_partidas` y lo devuelve en `partidasDp`; `FormularioPaquetesTrabajo.tsx` línea 23 lo declara en el tipo `PartidaDp`, pero no lo renderiza. Comprobado con cuenta B: la respuesta 200 de `GET /api/paquetes-trabajo?proyectoId=…` contiene `precio_unitario` (visible en la pestaña Red). No se ve en pantalla; sí se expone en el payload a los 13 roles al abrir Paquetes. Decisión pendiente de Victor: quitar el campo del select/tipo (no se usa) o aceptarlo.
- Captura: capturas/paneles-servicio-persistente/PL-121.jpg (consolidado RDTs PS-0004, cuenta A). Sin capturas adicionales por ítem.
- Nota: el formulario de login aparece con las credenciales de la cuenta A ya escritas (autocompletado del navegador de prueba); no se investigó.


## F2B-B parte 2 (2026-09-29) — PL-121, PL-152, PL-154

- PL-121 Conforme: quitado `precio_unitario` del select de `api/paquetes-trabajo/route.ts` y del tipo `PartidaDp` (no se usaba). Re-verificado con cuenta B (Supervisor Operativo): GET para PS-0004 (48 partidas) y PS-0005, 200, claves de partidasDp = id, wbs, descripcion, unidad, metrado_contractual; el payload no contiene «precio». Barrido de dinero en las 9 pantallas + ficha: sin coincidencias monetarias (solo metrados). Captura: capturas/paneles-servicio-persistente/PL-121.jpg.
- PL-152 Conforme: `requerimientos/exportar` ahora exige `puedeVerStatusRequerimiento` (403 «No autorizado») tras el 401; alcance por OT conservado. Un usuario sin rol conocido es rechazado por `tieneRolConocido` (pruebas de permisos, 599 verdes). Sin sesión, el middleware redirige al login.
- PL-154 Conforme: botones «Descargar RDTs (según filtro)» y «Descargar listado RDTs (según filtro)» visibles (cuenta A) y APIs abiertas a los 13 roles. Captura: PL-154.jpg.

Tabla 13 roles × descarga (cuenta A con «Ver como»; código de estado; no se bajó archivo; sin RDTs con el filtro activo la API responde 400 tras pasar la guardia; id inexistente 404 = pasó la guardia; ningún 403):

| Rol | rdts/exportar zip | rdts/exportar listado | partes/[id]/pdf | rdts/[id]/archivo | RQ exportar SV1 | RQ exportar SV2 |
|---|---|---|---|---|---|---|
| administrador | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| jefe_de_proyectos | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| jefe_de_oficina_tecnica | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| supervisor_oficina_tecnica | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| planner | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| supervisor_costos | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| jefe_de_costos | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| supervisor_operativo | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| supervisor_logistica | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| supervisor_administracion | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| supervisor_ssoma | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| asistente | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |
| rrhh | 400 (pasó guardia) | 400 (pasó guardia) | 404 | 404 | 200 pdf | 200 pdf |

No tocadas (A13): cronograma/plantilla, requerimientos/formato-vacio, exportar-004, registro-costos, dp/exportar. «Ver como» restaurado (DELETE 200).

## F3-A · Panel izquierdo con servicio (commit b84211b en local-worker-1)

Verificado en dev (puerto 3111, cuenta A, SV1=PS-0004, SV2=PS-0005), 604 pruebas verdes, tsc limpio, lint 9 errores/18 advertencias (igual al baseline).
- PL-22 Conforme: 27 chips en 7 grupos (Alcance y presupuesto, Planificación, Recursos del servicio, Documentación, Reportes, Acciones, Servicio); acciones separadas de informativos. Prueba unitaria para los 13 roles (panel-izquierdo.test.ts). Captura capturas/paneles-servicio-persistente/PL-22.jpg.
- PL-23 Conforme: 17 chips con pantalla; cada href lleva SV1 y la pantalla responde 200 mostrando PS-0004 (DP, Paquetes, Cronograma, Plan Maestro, Consolidado RDTs, Requerimiento, PR, Dashboard, Curva S, Registro de costos, Generar RQ, Crear RDT, Subir RDT, Crear paquete, Ficha, Editar servicio, Editar checklist).
- PL-24 Conforme: 10 chips inertes (OT, Alcance, Presupuesto, Cargos HH, Equipos HM, Materiales c/c, Personal NUEVO, Planos, PETS, Consolidado de servicio) sin href; clic en Planos y Cargos (HH) no cambia la URL; 0 errores de consola.
- PL-25 Conforme: hrefs de Generar RQ (?accion=crear-rq), Crear RDT, Subir RDT (?accion=subir-rdt) y Crear paquete (?accion=crear, formulario de paquete nuevo abierto, sin guardar) con SV1.
- PL-26 Conforme: en Crear paquete con SV1 se cambió el servicio a SV2 dentro del formulario: URL pasó a SV2, «Servicio actual» a PS-0005 y los chips del panel siguen a SV2. Captura PL-26.jpg.
- Observación: con el permiso vigente, «Generar RQ» sale deshabilitado para roles sin puedeCrearRequerimiento (p. ej. administrador solo); en Mi entorno ese chip sigue siempre habilitado (transitorio F1). La cuenta A tenía activo el resto de acciones.


## F3-B (commit c51a99e en local-worker-1)

- PL-27 / PL-62: sin servicio, el botón «Recursos de empresa» (aria-expanded=true, lista visible); con servicio (ruta /proyectos/<id>), aria-expanded=false y lista hidden. Clic alterna en ambos casos; abrir Personal (enlace del panel) mantiene el servicio y el estado. Botón nativo, foco por teclado y Enter/Space alternan (true a false a true). Secciones con `<nav aria-labelledby>` y `<h2>`. Cuenta A y cuenta B (Supervisor Operativo) ven los 4 chips activos.
- PL-28: 4 enlaces (Personal, Cargos, Equipos, Causas CNC); texto «Materiales» ausente del panel. El catálogo de datos no se tocó.
- PL-29: con servicio, Usuarios, Notificaciones, Configuraciones, Mi entorno y Cerrar sesión presentes con `?proyectoId=`; «Ver como» presente para A. El pie es ahora shrink-0 fuera del área con scroll: siempre visible aunque el panel tenga 1629 px de contenido (clientHeight 332 en el contenedor). No se pulsó Cerrar sesión salvo para cambiar de cuenta (funciona).
- PL-49: cuenta A y B (rol leído del pie: Supervisor Operativo): chips activos y las 4 páginas /recursos/* responden 200 para B. CNC con cuenta B: POST 403, PATCH 403, GET 200; sin botones de alta en la página. Con «Ver como» y nombres de rol válidos (asistente, residente, supervisor, logistica, solo_lectura): 403/403/200. Los nombres que usé para administrador, jefe y planificación no eran los del enum (jefe_de_proyectos), por lo que devolvieron 400 como el administrador real; ese tramo no cuenta como prueba: los 13 roles quedan cubiertos por la prueba unitaria de permisos.test.ts (solo administrador y jefe_de_proyectos gestionan CNC), que sigue verde. Captura PL-49.jpg.
- PL-59: 390 px: cajón izquierdo con mismo contenido (27 enlaces, Recursos, pie, servicio actual), cajón derecho con «Accesos rápidos» y «Grupos del servicio»; ambos cierran al navegar (el derecho tras la compilación de la ruta); sin scroll horizontal. Captura PL-59.jpg.
- PL-60: escritorio 1440: scroll interno en el contenedor del panel, pie visible tras scrollTop máximo; con Recursos oculto queda compacto. Captura PL-60.jpg.
- Pruebas: 604 verdes, tsc limpio, lint 9 errores/18 advertencias (igual al baseline). Console: los 403 esperados de las pruebas de API.

### F3-C (2026-09-29, commit 0819483 en local-worker-1; SV1 = PS-0004)

- PL-38: cuenta A (Administrador): los 27 chips activos salvo 10 inertes (sin pantalla). Diferencias contra la matriz del flujo 14, LISTADAS y no corregidas: (a) dp, pr, dashboard, curva-s, costos-servicios, plan-maestro abiertos a roles sin economía (lo cierra F5B); (b) editar-servicio usa `puedeAdjudicarProyecto` (JOT sí, JP no) y editar-checklist Admin+JOT, la matriz dice Admin+JP para ambos (F5C); títulos de esos dos chips desactualizados («Solo el Jefe de oficina técnica…»); (c) Generar RQ no incluye a administrador con rol único (la cuenta A lo ve activo por tener más roles) (F5C). Coinciden con la matriz: crear-rdt, rdt, crear-paquete.
- PL-39: cuenta B (Supervisor Operativo): panel visible (192 px, 7 grupos). Deshabilitados con `opacity-40`, `cursor-not-allowed`, título: Crear paquete, Editar servicio, Editar checklist. Activos: el resto de pantallas y Generar RQ, Crear RDT, Subir RDT. Captura PL-39.jpg.
- PL-40: clic real y sintético en chips deshabilitados: URL sin cambio, 0 errores de consola.
- PL-48: cuenta B: sin botón crear personal, sin crear paquete; POST /api/paquetes-trabajo, /api/recursos/personal y /api/recursos/catalogo-cnc con `{}`: 403 «No autorizado». Comparación completa con F0-C solo para B; las acciones de A quedan a F5C.
- PL-61: chip deshabilitado: `SPAN aria-disabled="true"`, tabIndex -1, título, texto legible. Corrección: los chips deshabilitados de Mi entorno (panel derecho) no tenían aria-disabled ni título por defecto; ahora sí. Verificado con «Ver como» asistente: plan-maestro, crear-rdt, rdt con aria-disabled y título.
- PL-63: panel izquierdo separa informativos y «Acciones» con rótulo de texto; panel derecho no tenía marca: se añade insignia de texto «Acción» (campo `tipo` en `HerramientaEntorno`, test nuevo). Captura PL-63.jpg.
- PL-64: diff contra main sin `max-w` nuevo, sin cambios en package.json; se reusa el `CHIP` de EntornoTrabajoGrupo.
- PL-71: `git diff main -- permisos.ts` solo contiene F2B-A (funciones de ver, `puedeVerStatusRequerimiento`, `puedeDescargarConsolidadoRq` con sus roles previos); `npm test` 604 verdes (+1 nueva), tsc limpio, lint 9/18 igual al baseline. «Ver como» restaurado (DELETE) y servidor detenido.


## F4-A Panel derecho estandarizado (PL-30 a PL-34, PL-41, PL-42) - 2026-09-30
Codigo: `panel-derecho.ts` (derivacion del registro: estado activo/deshabilitado/inerte, servicio en toda ruta, incluidas Notificaciones), `PanelSecciones.tsx` y `WorkspaceShell.tsx` consumen los chips; marca Accion y titulo en deshabilitados; Mi entorno "Ver todas" con servicio. Prueba `panel-derecho.test.ts` (6 casos, 13 roles). Navegador: cuenta A (Administrador) con SV1=PS-0004 en :3111; recorrido de los 7 grupos y Accesos rapidos por evaluate; luego Ver como asistente; cuenta B una vez.
- PL-30/31/32/33: con SV1, todos los chips con pantalla activos con `proyectoId=SV1` (o `/proyectos/SV1/...`): Crear RDTs, Subir RDTs, Crear RQ, Consolidado RDTs, Cronograma, Paquetes, Plan Maestro (selector); Status RDTs, Archivo RDTs, Requerimiento, Consolidado RQ (filtro); PR, Dashboard, Curva S, Registro de costos (ruta); las 7 Notificaciones y los accesos rapidos tambien. Sin pantalla: inertes con titulo "Sin pantalla todavia". DP y su href de SV1 verificados en el panel izquierdo (esta en el grupo Proyecto). Cronograma abre con "PS-0004" preseleccionado en el selector; Status RDTs con el filtro N° OT = PS-0004.
- PL-34: Cronograma, selector PS-0004 -> PS-0005: URL pasa a SV2, cronograma_PS-0004 desaparece. Status RDTs: filtro pasa de PS-0004 a Todos (solo PS-0004 tiene RDTs, mismas 71 filas). Captura: capturas/paneles-servicio-persistente/PL-34.jpg (solo despues).
- PL-41: la cuenta B es Supervisor Operativo y con SV1 no tiene chips deshabilitados (todos sus permisos pasan): el mecanismo se comprobo con Ver como = asistente: deshabilitados Plan Maestro ("Asistentes no tienen acceso al Plan Maestro"), Curva S, Crear RDTs, Subir RDTs (rapido y grupo), todos con aria-disabled y titulo; sin enlace. Captura PL-41.jpg. Ver como restaurado (DELETE 200).
- PL-42: Mi entorno con SV1: 9 chips de la matriz + Enviar mensaje; cuenta B todos activos con `proyectoId=SV1`; asistente: Plan Maestro, Crear RDTs y Subir RDTs deshabilitados con titulo. Mismo conjunto que la base (LB-03); no se cambio ningun permiso.
Suite: 611 pruebas, tsc limpio, lint 9 errores/18 advertencias (igual que baseline). Servidor dev detenido. No se repitieron credenciales fuera del login.

## F4B-A · Asistente como icono (PL-102 a PL-107) · 2026-09-29 · commit 7c9c6ca
Cuenta: B (Supervisor Operativo), escritorio 1440 y movil 390, dev en puerto 3111. Conteo por `aria-label="Asistente"` y `[data-asistente]`.
- PL-102: 23 rutas con SV1 (PS-0004: cronograma, paquetes, plan maestro, rdts crear/status/listado/consolidado, requerimientos, consolidado-rq, mi-entorno, notificaciones, recursos x4, configuraciones, mi-perfil, dp, pr, dashboard, curva-s, registro-costos, ficha) -> icono 1|1|visible, esquina (1160,884).
- PL-103: sin servicio (programas, programa, portafolio, mi-entorno, notificaciones, recursos/personal, configuraciones, mi-perfil, admin/usuarios) -> 1 icono visible.
- PL-104: movil 390 en cronograma con SV1, programas, mi-perfil, recursos: 1 icono visible (374,828), sin scroll horizontal (scrollWidth 390); panel abierto dentro del viewport (16..374). Captura PL-104.jpg. Nota: el indicador de Next Dev Tools (solo desarrollo) tapa el icono en movil; no existe en produccion.
- PL-105: clic abre (aria-expanded=true, aviso de vista previa, campo y Enviar); segundo clic, boton Cerrar y Escape repliegan y el foco queda en el icono. Captura PL-105.jpg (abierto).
- PL-106: sin texto "Pregúntale algo"; contenedor central = main (900 px a 900). Linea base F0 inferida del marcado anterior (banda border-t+py-4), sin captura "antes".
- PL-107: exactamente 1 instancia en todas las pantallas anteriores (copia del portafolio y del shell retiradas). Ejemplo "¿Cuántos proyectos...?" eliminado (A10).
- Pruebas: 611 verdes, tsc sin errores, lint 9 errores/18 advertencias (baseline). "Ver como" no se uso: el asistente no depende del rol.

## F4B-B (PL-108 a PL-111) — commit 4310953 en local-worker-1, cuenta de la sesion ya abierta, Playwright 1440 y 390 px

Cambios: `ChatPlaceholder.tsx` (aria-controls con id del panel siempre presente y `hidden` al cerrar, rol dialog no modal, max-h calc(100dvh-10rem) con scroll interno, icono 48 px, boton cerrar 40 px) y `WorkspaceShell.tsx` (padding inferior 4.5rem + zona segura en el contenedor de scroll para que el icono no tape el final de tablas).
- PL-108 Conforme: icono 1112-1160 x 836-884 (48x48), dentro de `main`; paneles laterales 0-240 y 1184-1440, sin solape. `elementFromPoint` en 5 puntos internos del icono = el boton. /rdts/status: la tabla larga (scrollHeight 2382) termina en y=824 y el icono empieza en 836. /rdts/consolidado, /plan-maestro y /proyectos/<id>/pr sin desbordamiento con los datos actuales. Formularios largos no medidos (sin datos que los desborden): cubiertos por el mismo margen inferior.
- PL-109 Conforme: 390 px, icono 326-374 x 716-764 (16 px sobre el borde inferior); cabecera 0-57 con menu (12,8,40x40) y herramientas (338,8,40x40) libres. Con cajon Menu o Herramientas abierto (z-50), `elementFromPoint` en icono y en panel devuelve el cajon: el asistente queda por debajo. Escritorio: overlay fixed z-50 de prueba inyectado cubre icono y panel. Modales reales (PanelVerRq, etc.) no abiertos: Observado, misma capa z-50 que el cajon. Captura PL-109.jpg.
- PL-110 Conforme: escritorio panel 776-1160 x 624-828, entre los laterales; movil 390x780 panel 16-374 x 504-708 bajo la cabecera, boton cerrar visible 40x40; a 390x420 cabe (144-348) con scroll interno disponible. Capturas PL-110.jpg y PL-110-movil.jpg.
- PL-111 Conforme: nombre "Asistente", aria-expanded true/false, aria-controls -> panel (role dialog, aria-label "Conversacion con el asistente"). Foco al boton, Enter abre, Escape cierra y el foco vuelve al icono, Espacio abre. Objetivo 48 px (cerrar 40).
- Notas: el indicador de Next Dev Tools tapa el icono solo en desarrollo (oculte `nextjs-portal`). Con un cajon abierto, Escape cierra tambien el panel del asistente (listener global); inofensivo. En PL-110-movil.jpg tome una captura previa con el panel cerrado y la reemplace (2 tomas). Pruebas 611 verdes, tsc limpio, lint 9/18 (baseline). "Ver como" no usado.

## F4B-C · Asistente: estado, red, reutilización, roles y pantallas fuera del shell (2026-09-29)

- **PL-112 Conforme.** Con el panel abierto en `/rdts`, navegación por enlaces del shell a `/recursos/personal`, `/plan-maestro` y `/requerimientos` (navegación SPA, sin recarga: marca `window.__marca` viva) conserva `aria-expanded=true` y el diálogo visible; tras `reload` vuelve a icono (`aria-expanded=false`). Comportamiento decidido: el estado vive en el shell y no persiste al recargar; R23 no se materializa. Captura: `capturas/paneles-servicio-persistente/PL-112.jpg`. Pendiente F7: escribirlo en el flujo 17.
- **PL-113 Conforme.** `ChatPlaceholder.tsx` no contiene `fetch` ni `/api`. En `/recursos/cargos`, abrir, escribir y pulsar Enviar no cambia la URL ni el campo (`preventDefault`) y el texto «todavía no está conectado a ningún dato» sigue visible. Las únicas llamadas `/api` son `recursos?tipo=cargos` y `notificaciones/count` cada 5 s (RefrescoDatos), con la misma cadencia con o sin asistente (sin tocarlo: mismos ticks periódicos; ninguna llamada extra por abrir o Enviar).
- **PL-114 Conforme.** Diff contra `main`: `ChatPlaceholder.tsx` modificado, sin componente paralelo; `package.json` sin cambios; tokens y clases existentes; Escape y foco al icono como el cajón móvil del shell. Los dos `max-w-*` nuevos (`max-w-[calc(100%-2rem)]` del flotante y `max-w-[85%]` de la burbuja) son del propio asistente, ninguno en contenedor de página.
- **PL-115 Conforme.** Icono presente (`[data-asistente]` = 1) con cuenta A, cuenta B (Supervisor Operativo, leído del pie) y «Ver como» en los 13 roles; «Ver como» restaurado (DELETE 200). El asistente no aparece en `registro-accesos.ts`, `permisos.ts` ni en la matriz del flujo 14 (solo existe el rol «asistente», que no es el chat). Captura: `PL-115.jpg`. Pendiente F7: nota en flujos 14/17.
- **PL-116 Conforme (excepción declarada).** Sin sesión, `/login` y `/auth/activar` (redirige a login) no tienen asistente. `programas/[id]/portafolios/[portafolioId]/dashboard` (fuera de `(workspace)`) no tiene asistente ni paneles (`aside`=0): excepción a reportar a Victor (R13, R21, V4); no se mueve. Captura: `PL-116.jpg`.
- Hallazgo menor: `/login` con sesión activa muestra el formulario con «Cerrar sesión» en vez de redirigir. Cierre: `npm test` 611 verdes, `tsc` limpio, lint 9 errores/18 advertencias (baseline).

## F5-A (2026-09-29) — commit `0e16648` en `local-worker-1`

- **PL-53 Conforme.** `src/lib/config/registro-humo.test.ts`: un registro con UNA entrada nueva (`prueba-humo`, solo planner) aparece en panel izquierdo, panel derecho (con `?proyectoId=` y sin él), accesos rápidos, Mi entorno y como fila de la matriz derivada (13 celdas, solo planner true); el estado por permiso da `activo`/`deshabilitado`. Para poder pasarle el registro, `construirPanelIzquierdo`, `construirPanelDerecho`, `construirAccesosRapidos` y `herramientasPorGrupo` reciben ahora `registro` opcional (por defecto el real; sin cambio de comportamiento). El panel izquierdo se sigue armando por estructura explícita (`ESTRUCTURA_IZQUIERDA`): la prueba añade la entrada a esa estructura.
- **PL-55 Conforme.** `cobertura-pantallas.ts/.test.ts` recorre `src/app/**/page.tsx` con `fs` (incluye la de fuera de `(workspace)`), cruza con las rutas del registro y con `EXCEPCIONES_PANTALLAS` (18, cada una con motivo; incluye PL-116 y `/programas/**`). Rojo demostrado con `src/app/(workspace)/_prueba-cobertura/page.tsx`: 2 pruebas fallaron (`['/_prueba-cobertura']` sin cobertura); página borrada, no commiteada. Verde: 6/6.
- **PL-56 Conforme.** `matriz-accesos.ts` (roles × accesos derivada del registro), `matriz-base-flujo14.ts` (tablas 1 y 2 transcritas por id de acceso) y `matriz-accesos.test.ts`, que fija las diferencias y falla si aparece una nueva o se salda una sin retirarla. **Diferencias registro vs matriz base (no corregidas):**
  - F5B, chips con economía abiertos a roles que la matriz excluye: `dashboard`, `pr`, `costos-servicios` (SOT, Plnr, SOp, SLog, SAdm, SSO, Asist, RRHH); `curva-s` (igual sin Asist, que ya no lo ve); `dp` (Plnr, SOp, SLog, SAdm, SSO, Asist, RRHH; SOT sí es correcto); `plan-maestro` (SOT, SOp, SLog, SAdm, SSO, RRHH; Plnr sí es correcto).
  - F5C, acciones: `editar-servicio` usa `puedeAdjudicarProyecto` (solo JOT): la matriz pide Admin+JP y excluye JOT (3 celdas); `editar-checklist` = Admin+JOT, la matriz Admin+JP (JP falta, JOT sobra); `crear-rdt` (Crear RDT estructurado): falta JOT (la matriz lo da); `crear-requerimiento-servicios` (`puedeCrearRequerimiento`): falta Admin. Nota: la diferencia de `crear-rdt` y la de `editar-servicio` para Admin/JP son más amplias que las conocidas al lanzar la tanda; se informan al Orquestador.
  - Filas de la base sin par en el registro (no comparadas): archivar/eliminar, importar DP, subir documento, validar RDT, descargas, gestión de Recursos, etc.
- **PL-57 Conforme.** `fuente-servicio.test.ts` escanea `src/app/(workspace)` y `src/components` (no `.test`): ningún `redirect(`, `href`, `router.push/replace` ni `volverHref` con ruta literal a Mi entorno o a pantallas que aceptan `?proyectoId=`. Encontró dos pérdidas reales y se corrigieron con `conServicio` (no cambian permisos): `requerimientos/page.tsx` (`redirect('/mi-entorno')` → conserva `proyectoIdRaw`) y `FormularioRequerimiento` (enlace «Ver status del servicio» a `/requerimientos`). Excepciones con motivo (3): `CabeceraPagina` (`volverHref` por defecto, `SalirAMiEntorno` agrega el servicio), `PanelDiagnostico` `/rdts/status` (Dashboard: solo cambia la guardia) y `FormularioCrearRdt` `/rdts/status` (Volver a Status en solo lectura; pendiente decidir). Rojo/verde de la función con casos sintéticos dentro de la prueba.
- Cierre: `npm test` 69 archivos, 631 verdes (611 + 20 nuevas), `tsc` limpio, lint 9 errores/18 advertencias (baseline).

## F5B-A — Economía: permisos, PR y Dashboard del servicio (2026-09-29)

Verificado con `npm test` (637 verdes), `tsc` limpio, lint 9 errores/18 advertencias (igual al baseline) y en vivo (dev en 3111, cuenta A con «Ver como», SV1=PS-0004; `fetch` a páginas y APIs por los 13 roles).

- **PL-88 Conforme.** `puedeVerEconomia` (admin, JP, JOT, SCo, JCo) es el único punto de cambio; `puedeVerDashboard`, `puedeVerDashboardPortafolio`, `puedeVerPr`, `puedeVerCurvaS`, `puedeVerRegistroCostos` delegan; `puedeVerDp` = economía + supervisor OT; `puedeVerPlanMaestro` = economía + planner. `permisos.test.ts` recorre los 13 roles y compara 7 filas x 13 roles con la tabla 1 leída del archivo del flujo 14 (91 celdas). Retiradas de `matriz-accesos.test.ts` las diferencias económicas (la matriz derivada coincide con la base en esas filas). Registro: dp, pr, dashboard y costos-servicios usan las nuevas funciones.
- **PL-89 Conforme.** Por «Ver como» sobre SV1: admin, JP, JOT, SCo, JCo abren `/pr` con datos (`US$`); los otros 8 roles ven «No tienes acceso al PR de este servicio.» sin datos, HTTP 200, sin error 500. Captura del caso negado (supervisor operativo): `capturas/paneles-servicio-persistente/PL-89.jpg`.
- **PL-90 Conforme.** Igual en `/dashboard` (5 con datos, 8 negados). Interruptor: `PATCH tipo-dashboard` con cuerpo inválido da 400 (pasó guardia) para los 5 roles con economía y 403 para los otros 8; el botón Parcial/Completo queda activo para jefe de costos (antes no). Captura: `PL-90.jpg`.
- **PL-125 Conforme.** Tabla por rol (pr | dashboard | curva-s | PATCH | API curva-s | API plan-maestro): SOT niega todo (la excepción DP es solo de `puedeVerDp`, probada en unidad); planner niega PR/Dashboard/Curva y su API plan-maestro devuelve 200 (403 en los otros sin economía); jefe de costos y supervisor de costos con economía completa; asistente y el resto, 403/negado.
- **PL-174 y PL-175 Observado.** Código: ambas páginas evalúan rol y `tieneAlcanceSobreProyecto` antes de leer datos (patrón de Curva S); prueba unitaria `economia por OT` para los 4 roles con economía no admin (sin OT: fuera; con OT: dentro; admin salta). No hay prueba en vivo: la cuenta B es Supervisor Operativo (sin economía; ve NEG en SV1 y SV2 por rol, no por alcance), el administrador salta el alcance, no existe SVX y el MCP postgresql no conecta. Queda por confirmar manualmente con un usuario de rol económico sin la OT.

## F5B-B — DP, Plan Maestro, Curva S, Dashboard del portafolio (2026-09-29)

Verificación en vivo (Playwright, dev en 3111, cuenta A con «Ver como» a los 13 roles sobre PS-0004/PS-0005; cuenta B = Supervisor Operativo). Sin escrituras; «Ver como» restaurado (DELETE).
- PL-91/PL-177 DP (página): con rol de economía y supervisor de oficina técnica se muestra; planner y los otros 6 roles ven «No tienes acceso al DP de este servicio.» sin leer datos. Alcance añadido (`tieneAlcanceSobreProyecto`); no probado en vivo (sin SVX).
- PL-153 `GET …/dp/exportar`: 200/404 (sin DP) para administrador, jefe proyectos, jefe oficina técnica, supervisor oficina técnica, supervisor costos, jefe costos; 403 para planner, operativo, logística, administración, SSOMA, asistente, RRHH. Ahora con `puedeVerDp` + `exigirAlcance`.
- PL-123 `GET /api/plan-maestro`: 200 economía + planner; 403 resto. `GET /api/curva-s`: 200 solo economía (planner y asistente 403). Curva S ya usaba `puedeVerCurvaS` desde F5B-A; sin cambios.
- PL-178 Plan Maestro: `exigirAlcance` en GET y en la página (`?proyectoId=`, mensaje «No tienes esta OT a cargo.»); el planner queda sujeto. Sin prueba en vivo del rechazo por alcance.
- PL-122/PL-176 Dashboard del portafolio: guardia de rol antes de leer datos; 13 roles: economía ve datos, los otros 8 ven «No tienes acceso al dashboard de este portafolio.» con enlace a la grilla (captura `capturas/paneles-servicio-persistente/PL-122.jpg`, cuenta B). **Decisión pendiente de confirmación de Victor (PL-176):** se muestran solo las OT del portafolio con alcance del usuario; administrador todas; sin ninguna OT con alcance, mensaje «No tienes acceso…».
- Suite: 637 pruebas verdes, tsc limpio, lint 9 errores/18 advertencias (igual a la base).
- Fuera de tanda: `registro-costos` (página y API) siguen abiertos por URL; el plan lo cubre en PL-124/PL-179 (F5B) y PL-126/PL-143 (F5C) — no se tocó.

## F5B-C (Registro de costos, enlaces internos, APIs, cierre F5B)
- Flujo 14 vigente al verificar: commit 68fc0e6 (posterior al 8027037 citado en PL-99; sin cambios de tablas 1/2 que afecten F5B) — PL-99 Conforme.
- PL-124/PL-179 Registro de costos: página con guardia antes de leer datos: ver = economía (`puedeVerRegistroCostos`) o Logística en modo «solo subir» (sin leer el registro: sin fecha ni existencia ni descarga), más alcance por OT; el resto ve «No tienes acceso…» sin datos propios de la página. API GET: rol (economía + descarga de jefe de proyectos, F5C-C) y alcance vía `validarEscrituraProyecto`; POST ya tenía alcance. Vivo con «Ver como» (cuenta A, 13 roles, SV1=PS-0004): página OK (economía), SOLO_SUBIR (supervisor_logistica), DENY (los otros 7); GET API 403 a todos salvo jefe de proyectos (404 sin archivo). Captura PL-124.jpg (logística). PL-179 Observado: el rechazo por alcance («No tienes esta OT a cargo») no se probó en vivo con cuenta B (comparte código con las otras pantallas, verificado ya en PR/DP).
- PL-93 APIs (13 roles): requerimientos, logística, recursos/personal, catalogo-cnc, paquetes-trabajo 200 a los 13; `dp/exportar`, `curva-s`, `plan-maestro`, `registro-costos` 403 fuera de la tabla 1 (excepciones: supervisor OT en DP, planner en Plan Maestro). Los 400 en exportar/recursos son parámetros faltantes (pasaron la guardia).
- PL-98 enlaces: ficha del servicio oculta Ver Dashboard, Ver/Cargar PR y Ver/Crear DP según rol y alcance; grilla/cabecera del portafolio oculta «Ver Dashboard». Verificado sobre el HTML de los 13 roles: economía ve los 3 enlaces; supervisor OT solo DP; resto ninguno; portafolio con enlace solo para economía.
- PL-95 Observado: los chips usan las funciones nuevas en el registro (pruebas unitarias verdes); no se recorrió la tabla chip × rol en vivo.
- PL-101 Observado: las seis pantallas evalúan la guardia antes de consultar datos (revisión de código), pero el panel izquierdo del layout muestra «Servicio actual» (número y nombre) a cualquier rol con la ficha, también en pantallas denegadas; no es dato económico. Pendiente de decisión del Orquestador.
- Suite: 637 pruebas verdes, tsc limpio, lint 9 errores/18 advertencias (igual a base).

## F5C-A · Acciones de ciclo de vida (PL-128 a PL-133, PL-135)

Verificado contra flujo 14 tabla 2 (commit de docs 68fc0e6) y código local-worker-1 (commit 69011c3). Sin escrituras reales: ids inexistentes o cuerpos inválidos.
- Pruebas unitarias: las 10 funciones (adjudicar, crear programa/portafolio, confirmar transición, archivar, eliminar proyecto, eliminar contenedor, editar servicio [nueva `puedeEditarServicio`], editar checklist, editar perfil) con los 13 roles; 647 pruebas verdes, tsc limpio, lint 9 errores/18 advertencias (igual al baseline).
- API con «Ver como» (cuenta A, 13 roles; luego DELETE /api/ver-como): 403 por rol para los 10 roles sin permiso en todas las acciones; administrador y JP pasan la guardia (400/200 con id inexistente); JP y JOT en acciones «Requiere OT» reciben 403 de alcance («No tienes esta OT a cargo»); JOT pasa la guardia solo en adjudicar/programa/portafolio/proyecto y transición, y recibe 403 de rol en archivar, eliminar, contenedor, servicio, checklist, perfil.
- Precondición Plan Maestro aprobado en confirmar-transicion: revisada en el código (400 al destino EJECUCION sin plan APROBADO), sin cambios.
- Perfil: PATCH /api/perfil ahora exige puedeEditarPerfilExtendido (antes sin guardia de rol); GET devuelve puedeEditar y la interfaz oculta el chip «Editar mi perfil». JOT: puedeEditar=false; JP: true (verificado por API; el chip se renderiza en cliente, sin captura).
- Chips del panel: prueba panel-izquierdo (JP activo, JOT deshabilitado en Editar servicio); títulos corregidos.

## F5C-B (commit 81d57d4 en local-worker-1) - acciones de RDT e importar DP
Verificado contra la tabla 2 del flujo 14 (ultimo commit 68fc0e6). Dev en puerto 3111, cuenta A con «Ver como» para los 13 roles (restaurado con DELETE /api/ver-como; servidor detenido). Ninguna prueba guardo, importo ni borro: ids inexistentes (UUID cero) y cuerpos invalidos.
- Pruebas unitarias: 13 roles por funcion (importar DP, crear, validar/rechazar, corregir, rechazar validado, eliminar). Suite: 653 verdes; tsc limpio; lint 9 errores / 18 advertencias (igual al baseline).
- PL-134 Conforme: POST /api/proyectos/<id>/dp: JP pasa la guardia de rol (403 «No tienes esta OT a cargo» = alcance); JOT y supervisor de OT «No autorizado»; admin 404. Boton y POST usan puedeImportarDp; el DP sigue visible al supervisor de OT (puedeVerDp intacto).
- PL-136 Conforme: POST /api/rdts/partes: admin 400; JP, JOT y supervisor operativo pasan la guardia de rol (403 de alcance); los otros 9 «No autorizado». /rdts/crear con JOT: 200 sin redireccion; chip activo por prueba del registro (crear-rdt ya no es diferencia en matriz-accesos.test). Sin captura (solo lectura).
- PL-137 Observado: PATCH accion invalida: admin, JP, JOT 400; los otros 10 403. Las ramas «rechazar VALIDADO sin JOT» y «corregir sin JOT» (POST reemplazar) exigen un RDT existente: solo verificadas por prueba unitaria y lectura de codigo, no por API en vivo.
- PL-138 Conforme: DELETE /api/rdts/partes/<inexistente> y /api/rdts/<inexistente>: admin y JP 404 (pasan guardia); los otros 11 403. Recalculo PR: DELETE de parte ya llama recalcularPr tras borrar (con alcance por OT); sin cambios ahi.

## F5C-C: acciones de RQ, registro de costos y descargas (2026-09-29)

Verificado contra flujo 14 tabla 2 (ultimo commit 68fc0e6). Cuenta A con «Ver como» en los 13 roles; ids inexistentes, sin subir, descargar ni borrar nada; «Ver como» restaurado (DELETE) al terminar. Pruebas: 654 verdes, tsc limpio, lint 9 errores/18 advertencias (igual al baseline). Sin capturas de imagen: se verifico con DOM y API (limitacion; el formulario de PL-139 se leyo por DOM).

- PL-139 Conforme: `puedeCrearRequerimiento` = 13 roles (prueba unitaria). POST `/requerimientos` con cuerpo `{}`: administrador 400 (paso la guardia); los otros 12 roles 403 «No tienes esta OT» (paso el rol, frena el alcance). El formulario `/proyectos/<id>/requerimientos/nuevo` abre en los 13 roles; como administrador lleva el servicio PS-0004 preseleccionado y no guarda. Retirado `centroSiempreHabilitado` (chip Crear RQ ahora sigue a la funcion).
- PL-140 Conforme: `puedeActualizarEstadoRequerimiento` = administrador + logistica (no JP; decision de Victor). PATCH `/estado` con id inexistente: 404 para todos, porque la ruta busca el RQ antes del rol; el rechazo por rol queda cubierto por la prueba unitaria de 13 roles. Botones del consolidado, Status y notificaciones usan la misma funcion. En Status, la columna «Acción» aparece para administrador, JP (por derivar) y logistica, y no para jefe de costos.
- PL-141 Conforme: `puedeEliminarRequerimiento` = administrador + JP. DELETE con id inexistente: administrador 404; JP 403 «No tienes esta OT» (paso el rol); los otros 11 roles 403 por rol. Se anadio la guardia de alcance por OT a esta ruta (`validarEscrituraProyecto`), como en las demas escrituras. Columna «Eliminar» visible en administrador y JP, ausente en jefe de costos y logistica.
- PL-142 Conforme: `puedeDescargarConsolidadoRq` conserva administrador, JP, JOT y logistica. Botón «Descargar PROM-GP-004» presente solo en esos 4 de 13; POST exportar-004 con id inexistente: 400 en esos 4, 403 en los otros 9. Los 13 ven el consolidado.
- PL-126 Conforme: `puedeDescargarRegistroCostosServicio` = administrador + JP. GET `registro-costos` con servicio inexistente: administrador 404 (paso), JP 403 «No tienes esta OT» (paso el rol), JOT, supervisor de costos, jefe de costos, logistica y demas 403 por rol. En pantalla: administrador y JP ven «No hay archivo para descargar» (control de descarga); jefe de costos no.
- PL-143 Conforme: logistica ve «Puedes subir el registro…» y «Subir registro», sin descarga ni contenido; el resto no ve el control de subir. POST sin archivo: logistica pasa la guardia de rol (frena el alcance), los otros 12 roles 403 (administrador incluido). No se subio nada.

### F5C-D (PL-144, PL-145, PL-148, PL-151), 2026-09-30, commit 8240c55 en local-worker-1
- PL-144 Conforme: unitaria (13 roles) `puedeAsignarRolAdministrador` y `puedeSimularRol` solo administrador. Cuenta B (Supervisor Operativo): sin selector «Ver como»; POST `/api/ver-como` 403 «Solo el administrador puede simular». Con «Ver como» de los 12 roles no administrador: POST y PATCH `/api/admin/usuarios` asignando rol administrador 403 (JP incluido; en el JP se comprobo que llega a la guardia de asignar, no a la de gestionar). Nada escrito.
- PL-145 Conforme: pruebas unitarias 13 roles para subir RDT, subir cronograma, Plan Maestro, paquetes, catalogo CNC, usuarios, comentar RQ, derivar RQ y subir documento; API en vivo con cuerpo invalido y ids inexistentes, 13 roles: cada rol pasa (400/404) o es rechazado (403 rol) exactamente segun la tabla 2. Hallazgo corregido: `puedeSubirDocumento` no daba paso al JP (la tabla 2 fila 4 lo marca sin condicion); ahora admin y JP siempre, y el resto solo si es el responsable.
- PL-148 Conforme: pruebas unitarias por funcion (editar servicio, importar DP, corregir RDT, rechazar RDT validado, descargar consolidado RQ) con el conjunto exacto de la tabla 2; el JOT gana crear/validar RDT sin ganar corregir, rechazar validado, editar servicio ni importar DP. Ningun alias arrastra un rol.
- PL-151 Conforme: mensajes por caso (servicio inexistente; «Ver como» aplica el proyecto_miembros del usuario real, no lo salta): JP simulado 403 «No tienes esta OT a cargo» en confirmar transicion, editar servicio, archivar, eliminar proyecto, checklist, importar DP, crear RQ, eliminar RQ; JOT simulado: confirmar transicion y crear RQ dan OT, el resto (servicio, archivar, eliminar, checklist, DP, cronograma, eliminar RQ) da `{"error":"No autorizado"}` por rol; JP en registro de costos: rol. Administrador: pasa (400) sin OT. Cuenta B (miembro de PS-0004/PS-0005): crear RQ con cuerpo vacio en ambos da 400 (pasa OT) y en un id ajeno 403 OT. Cronograma con cuerpo sin vinculos da 400 antes del alcance (orden de la ruta, sin cambio).
- Hallazgos de F5C-C cerrados: PATCH `/estado` valida el rol antes de buscar el RQ (id inexistente: derivar admin/JP/JOT 404, logistica 403; actualizar estado admin/logistica 404, JP y demas 403). PATCH `/checklist` con `{}` ahora 400 «Cuerpo inválido» (antes 500); el editor envia los 4 arreglos, sin cambio de permisos.
- Suite: 669 verdes, tsc limpio, lint 9 errores/18 advertencias (baseline).


## F5D-A (2026-09-30) - PL-157 a PL-162: Conforme
- PL-157: `puedeGestionarRecursos` (administrador y JP) en permisos.ts; `puedeGestionarCatalogoCnc` delega en ella; POST Personal la usa. `npm test` 670 verdes (13 roles), tsc limpio, lint 9 errores/18 advertencias (igual al baseline).
- Cuenta B (Supervisor Operativo): pagina Personal sin formulario ni columna Acciones; POST/PATCH personal y POST/PATCH catalogo-cnc = 403.
- Cuenta A + matriz «Ver como» de los 13 roles (POST personal `{}` / PATCH personal id inexistente / POST CNC `{}` / PATCH CNC id inexistente): administrador y jefe_de_proyectos = 400/404/400/400 (pasan la guardia); los otros 11 = 403/403/403/403. DELETE /api/ver-como = 200 (restaurado).
- PL-158/161/162 en UI (cuenta A): crear, editar (nombre) y desactivar Personal funcionan; la fila no se borra (queda Inactivo); `/api/rdts/catalogos` incluye al trabajador activo y deja de incluirlo al desactivarlo. Captura: capturas/paneles-servicio-persistente/PL-161.jpg.
- PL-159/160: Causa CNC creada, desactivada, activada y desactivada por API (200); estado final activo=false.
- Registros de prueba (todos activo=false): Personal DNI 99999901 «PRUEBA-PL Trabajador Uno EDIT» (cargo AYUDANTE TOPOGRAFO); catalogo_cnc id 68287d9a-803e-43c4-a6c5-d11e7e32a07f «PRUEBA-PL causa CNC». No se tocaron registros reales.
- Limite: control visible con «Ver como» JP no se comprobo en UI (misma funcion que la matriz API, que es 400/404 para JP).

## F5D-B (PL-163 a PL-169) - Cargos, Equipos y Causa CNC

Verificado con Playwright (cuenta A, servidor dev 3111, worktree local-worker-1). Captura: capturas/paneles-servicio-persistente/PL-163.jpg. Commit d87fa26.
- PL-163/164/165 (Cargo, UI): alta con `POST /api/recursos` (origen MANUAL), editar unidad/categoria con `PATCH /api/recursos/[id]` (fila queda DIA/PRUEBA), desactivar (`activo=false`). Cargo inactivo ya no aparece en `cargos` de `/api/recursos/personal` y crear Personal con ese cargo devuelve 400 "no es un cargo del catalogo". Cargo de prueba id `3f33340d-dddb-4b83-8609-27b680580867` (PRUEBA-PL cargo F5D-B), dejado Inactivo.
- PL-166/167/168 (Equipo, UI): alta, editar (unidad MES, categoria PRUEBA) y desactivar. Equipo de prueba id `4595f1f6-f744-4cbb-a579-cb285113afce` (PRUEBA-PL equipo F5D-B), dejado Inactivo.
- PL-169: lapiz por fila en Causas CNC; se reactivo la causa `68287d9a-803e-43c4-a6c5-d11e7e32a07f`, se edito a "PRUEBA-PL causa CNC editada", aparecio en `causasCnc` de `/api/rdts/catalogos` (fuente del desplegable de Crear RDT) y se dejo Inactiva.
- Permisos (Ver como, 13 roles, id inexistente/cuerpo vacio): administrador y jefe_de_proyectos pasan la guardia (400/404/400); los otros 11 roles 403 en POST /api/recursos, PATCH /api/recursos/[id] y PATCH catalogo-cnc. Rol asistente: sin formulario ni columna Acciones. "Ver como" restaurado (DELETE 200).
- Decision: la descripcion no se edita (PATCH responde 400): recursos_personal.cargo, rdt_tareo.cargo, consolidado (MOI/maquinaria) y precios DP la referencian por texto; equivalencias usan id (FK). Editables: unidad, categoria, activo.
- Suite: 670 pruebas verdes, tsc limpio, lint 9 errores/18 advertencias (baseline).


## F6-A · PL-43, PL-96, PL-97 (2026-09-30) — Conforme

Metodo. Prueba vitest temporal (borrada, no commiteada) que lee las tablas 1 y 2 **del propio archivo** `14-accesos-y-restricciones.md` y la linea base «antes» **de esta misma evidencia (F0-C)**, evalua las funciones de `permisos.ts` con los 13 roles y compara celda a celda (702 celdas: 17 filas de tabla 1 y 43 de tabla 2 agrupadas, x 13 roles). Resultado: **0 celdas donde `permisos.ts` difiera del flujo 14; 0 celdas donde el objetivo de F0-C difiera del flujo 14 actual**. Vivo: cuenta A (admin real) con «Ver como», dev :3111, SV1 = PS-0004, solo lectura (APIs con id inexistente o cuerpo vacio); al final `DELETE /api/ver-como` = 200.

**PL-43 Conforme.** Para cada uno de los 13 roles se cargaron `/mi-entorno?proyectoId=SV1`, `/mi-entorno` y la ficha del servicio y se leyo el estado de cada chip (`data-chip` / `data-herramienta`: deshabilitado o `aria-disabled` frente a activo/inerte) en panel izquierdo, panel derecho y Mi entorno: **79 chips por rol, 79/79 coinciden con la matriz** (13 x 79 = 1027 comprobaciones, 0 diferencias; 19 ids distintos visibles en esas pantallas). Los chips sin restriccion o inertes (ot, materiales, planos, cargos-hh, etc.) no se deshabilitan para ningun rol, como pide la tabla 1 (panel izquierdo: 13 roles). Patron esperado por chip, derivado del registro y contrastado con la fila del flujo 14: economia (dashboard, pr, curva-s, costos-servicios) = Admin, JP, JOT, SCo, JCo; dp = economia + SOT; plan-maestro = economia + Plnr; crear-rdt y rdt = Admin, JP, JOT, SOp; editar-servicio y editar-checklist = Admin, JP; crear-paquete = Admin, JP, Plnr; el resto, 13 roles. Limite: no se vieron en vivo todos los ids del registro (por ejemplo `enviar-notificacion`, siempre habilitado); la matriz del registro contra el flujo 14 si se comparo completa (sin diferencias).

**PL-96 Conforme.** Servidor vs tablas 1 y 2 para los 13 roles (`pasa` = no recibe 403 por rol; `403 No tienes esta OT a cargo` cuenta como «paso el rol»; la cuenta A real no tiene la OT, asi que los roles simulados que pasan el rol frenan en el alcance, R28). 45 llamadas de API y 21 paginas por rol: **coinciden todas salvo 2 filas que son explicables y no son diferencias:**
- `/proyectos/SV1/registro-costos`: entra tambien SLog, en modo «solo subir» (puede subir, no ve ni descarga; F5B-C). Coincide con la tabla 2 (SLog sube) y la tabla 1 (SLog no ve el registro).
- `POST /api/rdts/partes` con cuerpo vacio da 400 a los 13 porque valida `proyectoId` antes de la guardia; con `proyectoId` inexistente: Admin 400, JP/JOT/SOp «No tienes esta OT a cargo» (pasaron el rol), los otros 9 «No autorizado». Orden ya existente, sin escritura.
(La pagina `/rdts/crear` se clasifica a mano: Admin, JP, JOT y SOp la ven; los otros 9 roles son redirigidos.)
Paginas (redirige o «No tienes acceso»): dashboard, PR, curva-s = economia; DP = economia + SOT; Plan Maestro = economia + Plnr; registro de costos = economia + SLog solo subir; editar servicio, checklist/editar, /admin/usuarios = Admin, JP; /rdts/crear = Admin, JP, JOT, SOp; cronograma, paquetes, status/listado/consolidado RDTs, RQ status, consolidado RQ y las 4 pantallas de Recursos = 13 roles. APIs: GET curva-s, plan-maestro, admin/usuarios, rdts/catalogos y registro-costos; POST programas, portafolios, proyectos, confirmar-transicion, dp, admin/usuarios, recursos, recursos/personal, catalogo-cnc y sus PATCH, rdts, rdts/partes, cronograma, plan-maestro, paquetes-trabajo, requerimientos, exportar-004, registro-costos; PATCH rq/estado y rdts/partes (VALIDAR); comentarios; DELETE programas, portafolios, proyectos, rdts, rdts/partes, requerimientos: todas con el conjunto de roles de su fila. `GET .../partidas` sin guardia (debe seguir asi) da 200 a los 13; `PATCH /api/perfil` con cuerpo vacio: 400 solo a Admin y JP, 403 al resto (antes lo pasaban los 13; ahora sigue la fila «Editar perfil extendido»). Unitario: `permisos.ts` = flujo 14 en todas las filas para los 13 roles (incluye `puedeSubirDocumento`: Admin y JP siempre; el resto solo como rol responsable).

**PL-97 Conforme (informe para revision de Victor).** Notacion: `✓` puede antes y despues; `—` no puede ni antes ni despues; `—→✓` antes no podia, ahora si; `✓→—` antes podia, ahora no. Celdas cambiadas: **142 de 702 (20 %)**; cada una coincide con la marca `→` de la linea base F0-C, es decir con lo que decide el flujo 14. **Ninguna celda cambio fuera del flujo 14 (0 hallazgos de permisos).** Brecha ya conocida (nota 1 del flujo): el Dashboard del servicio sigue sin separar Parcial (13 roles) de Completo (economia); hoy la pagina entera es economia.

Resumen por rol (gana = `—→✓`; pierde = `✓→—`):

| Rol | Gana | Pierde |
|---|---|---|
| Administrador | ver registro de costos; adjudicar/crear programa y portafolio; confirmar transicion; editar servicio; editar/eliminar Personal; crear/editar/eliminar Cargos y Equipos; editar texto CNC; crear RQ; actualizar estado RQ; descargar registro de costos | nada |
| Jefe de proyectos | adjudicar/crear programa y portafolio; confirmar transicion; archivar y eliminar proyecto; eliminar contenedor; editar servicio y checklist; importar DP; subir documento del proyecto; gestion completa de Recursos (Personal, Cargos, Equipos, texto CNC); eliminar RDT; eliminar RQ | nada |
| Jefe de oficina tecnica | ver registro de costos; ver Recursos y panel izquierdo completo; crear RDT; validar/rechazar RDT | archivar y eliminar proyecto; editar servicio y checklist; perfil extendido |
| Supervisor OT | ver RDTs, consolidado RQ, Recursos, panel izquierdo | Dashboard, portafolio, PR, Curva S, Plan Maestro; importar DP; perfil extendido |
| Planner | ver RDTs, consolidado RQ, Recursos, panel izquierdo | Dashboard, portafolio, PR, DP, Curva S; perfil extendido |
| Supervisor de costos | ver registro de costos, RDTs, consolidado RQ, Recursos, panel izquierdo | perfil extendido |
| Jefe de costos | igual que supervisor de costos | perfil extendido |
| Supervisor operativo | ver consolidado RQ, Recursos, panel izquierdo | Dashboard, portafolio, PR, DP, Curva S, Plan Maestro; perfil extendido |
| Supervisor de logistica | ver RDTs, Recursos, panel izquierdo | Dashboard, portafolio, PR, DP, Curva S, Plan Maestro; ver registro de costos (sigue pudiendo subirlo); perfil extendido |
| Supervisor de administracion | ver consolidado RQ, Recursos, panel izquierdo | Dashboard, portafolio, PR, DP, Curva S, Plan Maestro; perfil extendido |
| Supervisor SSOMA | ver RDTs, consolidado RQ, Recursos, panel izquierdo | Dashboard, portafolio, PR, DP, Curva S, Plan Maestro; perfil extendido |
| Asistente | ver Cronograma, Paquetes, consolidado RQ, Recursos, panel izquierdo | Dashboard, portafolio, PR, DP; perfil extendido |
| RRHH | ver consolidado RQ, Recursos, panel izquierdo | Dashboard, portafolio, PR, DP, Curva S, Plan Maestro; perfil extendido |

Tabla completa (antes → despues), una fila por interfaz o accion de las tablas 1 y 2; las sub-acciones con el mismo resultado (adjudicar/programa/portafolio; archivar/eliminar; crear/editar/eliminar Cargos o Equipos) se agrupan o se listan juntas. Columnas: Admin, JP, JOT, SOT, Plnr, SCo, JCo, SOp, SLog, SAdm, SSO, Asist, RRHH.

| Fila (tabla) | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| T1 · dashboard | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— |
| T1 · portafolio | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— |
| T1 · pr | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— |
| T1 · dp-ver | ✓ | ✓ | ✓ | ✓ | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— |
| T1 · curva-s | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | — | ✓→— |
| T1 · plan-maestro-ver | ✓ | ✓ | ✓ | ✓→— | ✓ | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | — | ✓→— |
| T1 · registro-costos-ver | —→✓ | ✓ | —→✓ | — | — | —→✓ | —→✓ | — | ✓→— | — | — | — | — |
| T1 · cronograma-ver | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | —→✓ | ✓ |
| T1 · paquetes-ver | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | —→✓ | ✓ |
| T1 · rdts-ver | ✓ | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | ✓ | —→✓ | ✓ | —→✓ | ✓ | ✓ |
| T1 · rq-status | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| T1 · rq-consolidado | ✓ | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ |
| T1 · recursos-personal-cargos-equipos | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ |
| T1 · recursos-cnc | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ |
| T1 · ficha | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| T1 · panel-izq | ✓ | ✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ | —→✓ |
| T1 · notificaciones | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| T2 · adjudicar | —→✓ | —→✓ | ✓ | — | — | — | — | — | — | — | — | — | — |
| T2 · transicion | —→✓ | —→✓ | ✓ | — | — | — | — | — | — | — | — | — | — |
| T2 · archivar | ✓ | —→✓ | ✓→— | — | — | — | — | — | — | — | — | — | — |
| T2 · eliminar-proyecto | ✓ | —→✓ | ✓→— | — | — | — | — | — | — | — | — | — | — |
| T2 · eliminar-contenedor | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · editar-servicio | —→✓ | —→✓ | ✓→— | — | — | — | — | — | — | — | — | — | — |
| T2 · editar-checklist | ✓ | —→✓ | ✓→— | — | — | — | — | — | — | — | — | — | — |
| T2 · importar-dp | ✓ | —→✓ | — | ✓→— | — | — | — | — | — | — | — | — | — |
| T2 · usuarios | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · perfil-ext | ✓ | ✓ | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— | ✓→— |
| T2 · rol-admin | ✓ | — | — | — | — | — | — | — | — | — | — | — | — |
| T2 · ver-como | ✓ | — | — | — | — | — | — | — | — | — | — | — | — |
| T2 · subir-doc | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · personal-crear | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · personal-editar-elim | —→✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · cargo-cee | —→✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · equipo-cee | —→✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · cnc-crear | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · cnc-activar | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · cnc-editar | —→✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · rdt-subir | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — |
| T2 · rdt-crear | ✓ | ✓ | —→✓ | — | — | — | — | ✓ | — | — | — | — | — |
| T2 · rdt-validar | ✓ | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — |
| T2 · rdt-corregir | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | — |
| T2 · rdt-rechazar-validado | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · rdt-eliminar | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · cronograma-subir | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — |
| T2 · plan-gestionar | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — |
| T2 · paquetes-gestionar | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — |
| T2 · rq-crear | —→✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| T2 · rq-comentar | ✓ | ✓ | — | — | — | — | — | — | ✓ | — | — | — | — |
| T2 · rq-estado | —→✓ | — | — | — | — | — | — | — | ✓ | — | — | — | — |
| T2 · rq-derivar | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — |
| T2 · rq-eliminar | ✓ | —→✓ | — | — | — | — | — | — | — | — | — | — | — |
| T2 · rq-desc-consolidado | ✓ | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — |
| T2 · costos-subir | — | — | — | — | — | — | — | — | ✓ | — | — | — | — |
| T2 · costos-descargar | —→✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — |


Hallazgos de F6-A: (1) Ninguno exige cambiar permisos mas alla del flujo 14. (2) F0-C contaba 36 filas con diferencia; el conteo por celda de esta tabla es 142. (3) `POST /api/rdts/partes` valida el cuerpo antes de la guardia de rol (pre-existente; sin escritura). (4) El «Servicio actual» del panel izquierdo se muestra a cualquier rol (PL-101, ya registrado). Sin escrituras de datos en esta tanda; sin cambios de codigo.


## F6-B (2026-09-30) - servidor: URL directa, APIs, sesion cerrada, bypass admin, humo en vivo

Servicios: SV1=PS-0004, SV2=PS-0005. Cuenta B leida del pie del panel: Supervisor Operativo. No existe SVX (solo hay 2 servicios; MCP postgresql no conecto).
- PL-44 Conforme. B por URL directa a SV1: `/proyectos/SV1/{dp,pr,dashboard,curva-s,registro-costos}` muestran el mensaje «No tienes acceso al <X> de este servicio» sin datos; `/editar`, `/checklist/editar` redirigen a la ficha `/proyectos/SV1`; `/plan-maestro?proyectoId=SV1` redirige a `/mi-entorno?proyectoId=SV1`. Captura: capturas/paneles-servicio-persistente/PL-44.jpg (PR).
- PL-45 Conforme (remite a PL-89 a 91 y 122 a 124). Repetido en vivo con B: DP, PR, Dashboard, Curva S, Registro de costos y dashboard del portafolio = mensaje de rechazo; Plan Maestro = redireccion.
- PL-46 Conforme con correccion. Antes: con B, `GET /api/cronograma` y `/api/rdts/consolidado` con `proyectoId=zzz` = 500 (`invalid input syntax for type uuid`) y con uuid inexistente = 200 vacio; `/api/curva-s` con admin igual (500 / 200 vacio); B en `/api/curva-s` = 403 en todos los ids. Despues (commit b4d3a4a): no-uuid = 400, uuid inexistente = 404 «Servicio no encontrado», vacio = 400; SV1 y SV2 = 200 (B) en las dos primeras y 403 (B) / 200 (admin) en curva-s. Los 13 roles de las dos primeras: `puedeVerCronograma`/`puedeVerRdts` = tieneRolConocido (permisos.test.ts). Parte SVX: Observada (no existe SVX; no hay alcance por OT en cronograma ni consolidado, solo rol, igual que antes; no decidido).
- PL-54 Conforme. Entrada `prueba-humo-vivo` (grupo Logistica, permiso `puedeVerCurvaS`) anadida solo en `registro-accesos.ts`: con A (admin) el chip aparece en Mi entorno > Logistica, activo, con `?proyectoId=SV1` en el href; con B aparece deshabilitado («Tu rol no tiene acceso a esta pantalla»); `derivarMatrizAccesos` la incluye como fila (prueba temporal, borrada) y `validarRegistro` = []. `git status` con un solo archivo modificado, luego revertido (limpio). Captura: PL-54.jpg (cuenta A).
- PL-73 Conforme. Con la sesion cerrada, 11 rutas del workspace con `?proyectoId=` (cronograma, plan-maestro, rdts/consolidado, mi-entorno, paquetes-trabajo, pr, dashboard, curva-s, dp, registro-costos, editar) terminan en `/login` (conserva `?proyectoId=` en las de query). Middleware sin cambios. Captura: PL-73.jpg.
- PL-180 Observado. Cuenta A (administrador) entra a las 6 pantallas (dp, pr, dashboard, curva-s, registro-costos, plan-maestro) de SV1 y SV2 con 200 y datos, sin mensaje de guardia; captura PL-180.jpg. No hay SVX donde A no sea miembro, asi que el «sin ser miembro» se cubre con `alcance-proyecto.test.ts` (admin con alcance sobre cualquier proyecto; no admin sin la OT en su lista, no).

## F6-C (2026-09-30) · PL-65, PL-117, PL-170, PL-171, PL-172

Cuenta A con «Ver como»; servidor dev :3111 en local-worker-1 (HEAD b4d3a4a, sin código nuevo). Sin migraciones.

**PL-172 · Conforme.** Tabla 13 roles × 12 acciones (crear/editar/desactivar × Personal, Cargos, Equipos, Causas CNC), llamadas sin efecto (id `0000…`/cuerpo vacío): administrador y jefe_de_proyectos = 400/404 (pasan la guardia: crear 400, editar y desactivar 404); los otros 11 roles = 403 en las 12 acciones. Interfaz (HTML servido por rol): «Agregar» y columna «Acciones» solo con administrador y JP; los demás 11 roles no ven ningún control de mutación. Camino feliz con registros marcados (autorización de Victor 2026-09-30), como administrador y como JP: crear, editar y desactivar en los 4 recursos = 200. Registros creados (todos dejados inactivos, ninguno borrado): Cargos `PRUEBA-PL cargos A` y `J`, Equipos `PRUEBA-PL equipos A` y `J`, Personal DNI 99999902 y 99999903 (`PRUEBA-PL persona A/J`, cargo OFICIAL), Causas CNC `PRUEBA-PL causa A editada` y `PRUEBA-PL causa J editada`. Cargos/Equipos quedaron con unidad UND y categoría «PRUEBA-PL editada». No se reutilizaron los registros de prueba previos (99999901 y los ids anteriores siguen inactivos, sin tocar). No se tocaron registros reales ni Materiales.

**PL-170 · Conforme.** Cargos y Equipos, 13 roles: «Personalizar campos» (4 y 5 campos), «Limpiar filtros», 8 y 10 selectores de filtro «Todos» y cabeceras de orden presentes en los 13; los controles de alta/edición añaden solo «Agregar» y «Acciones» para administrador y JP (cabeceras 10/12 frente a 8/10 sin gestión).

**PL-171 · Conforme.** Personal: DNI duplicado responde 400 «Ya existe un trabajador con DNI …» y un cargo fuera del catálogo 400 «no es un cargo del catálogo de la empresa» (administrador y JP); el alta usa el selector «Elige un cargo…» del catálogo activo; editar y desactivar funcionan tras el alta.

**PL-65 · Observado.** Capturas en `capturas/paneles-servicio-persistente/PL-65-*.jpg` (consolidado-rdts, status-rdts, consolidado-rq, pr). Medido a 1440 px: Status de RDTs (71 filas, 26 celdas sticky, 1 contenedor con scroll horizontal) y PR (9 filas, 68 celdas sticky, scroll horizontal) conformes; Consolidado RDTs y Consolidado RQ no tienen datos en PS-0004/PS-0005 (0 filas), por lo que el scroll con columnas fijas no se pudo ver con filas (el código de TablaConsolidadoRdts conserva `sticky`; Consolidado RQ sin `sticky` en la línea base 1942b01). Requiere revisión manual con datos.

**PL-117 · Observado.** Con el asistente como icono, ancho de página sin desborde (scrollWidth − clientWidth = 0) en 17 pantallas a 1440 y 390 px (RDTs, RQ, PR, portafolio, Mi entorno, Cronograma, Plan Maestro, Recursos, etc.); tablas largas con scroll interno. Sin comparación numérica de filas contra LB-02/LB-04 (no se releyeron); revisión visual de «como antes salvo la barra» queda al Responsable humano.

Hallazgo: consola con 150+ errores 403 durante la matriz de roles (esperados: son las respuestas rechazadas). «Ver como» restaurado (DELETE = 200).

## F6-D - PL-68, PL-77, PL-78, PL-80 (Worker, 2026-09-30, HEAD b4d3a4a, solo lectura, sin codigo nuevo)

Servidor dev -p 3111 (detenido al cerrar). Capturas: `capturas/paneles-servicio-persistente/PL-78.jpg`, `PL-80.jpg`.

- **PL-68 Conforme.** Cuenta A: 42 rutas (SV1 y SV2: /proyectos/id y dp, pr, dashboard, curva-s, editar, checklist/editar; mi-entorno con y sin accion; cronograma, paquetes, plan-maestro con proyectoId; y las pantallas sin servicio, RDTs, Recursos, admin/usuarios): 200 todas, 0 errores de consola (console.error/pageerror), 0 respuestas 4xx, 0 requestfailed. Cuenta B (Supervisor Operativo): 41 rutas, 0 errores JS, 0 4xx. Barrido «Ver como» 12 roles x 6 rutas: 0 errores JS, 0 4xx (POST 200 en los 12; DELETE 200). Los avisos son los de la linea base (Fast Refresh, HMR, React DevTools, preload de layout.css). Consola errores: 0 de recursos/JS y 0 de 4xx esperados (esta tanda no llamo a APIs de escritura).
- **PL-77 Conforme.** Sin servicio, cuenta A: los destinos coinciden con LB-03: Subir RDTs -> `/mi-entorno?accion=subir-rdt`, Plan Maestro -> `/plan-maestro`, Requerimiento `/requerimientos`, Consolidado RQ `/logistica/consolidado-rq`; no hay chips de PR, Dashboard, Curva S, Cronograma ni Paquetes; /notificaciones, /cronograma, /paquetes-trabajo, /requerimientos, /rdts/* y /recursos/* responden 200 sin redirect. Cuenta B: mismos chips sin servicio. Diferencias respecto de F0 en B, todas efecto esperado del flujo 14 aplicado en F1-F5 (no regresion): /plan-maestro y /proyectos/id/editar redirigen (a /mi-entorno y /proyectos/id; en F0 daban 200 sin guardia) y en SV1 tambien /checklist/editar; el panel izquierdo de B muestra Recursos de empresa (consulta abierta a los 13 roles, tabla 1 fila 41; en F0 no se mostraba).
- **PL-78 Observado.** Cuenta A y B: chip Crear RQ desde Mi entorno (SV1) abre la seccion «Crear RQ» (URL con accion=crear-rq, sin guardar); Status de requerimiento abre con 8 filtros y «Limpiar filtros» funciona, pero no hay requerimientos en los servicios de prueba (0), asi que el efecto de filtrar sobre filas no se pudo observar; Consolidado RDTs: selector con PS-0004 y PS-0005, elegir PS-0004 carga la grilla (70 dias cargados) en A y B; Plan Maestro y Cronograma abren con y sin proyectoId en A; en B Cronograma abre con y sin servicio y Plan Maestro redirige a Mi entorno (guardia flujo 14). Pendiente manual: filtrar sobre un servicio que tenga requerimientos.
- **PL-80 Conforme.** Escritorio 1440: panel izquierdo con Recursos, «Ver como» (solo A; B no lo tiene) y pie con usuarios y rol (A: Administrador; B: Supervisor Operativo). Movil 390: botones «Abrir menu» y «Abrir herramientas» presentes, sin desborde horizontal, cajon izquierdo con Menu, servicio actual, Recursos, Ver como (A) y pie; cajon derecho con Herramientas, Accesos rapidos, Grupos del servicio; B igual sin Ver como. Igual a LB-02 (LB-02-5 y LB-02-6).
- «Ver como» restaurado (DELETE /api/ver-como = 200) y sesion cerrada por borrado de cookies antes de entrar como B; datos no escritos.

## F6-E — Cierre técnico (2026-09-30, local-worker-1 `b4d3a4a` vs main `1942b01`)

- **PL-35 Conforme.** `git diff --stat main...local-worker-1 -- db/` vacío; ningún `.sql`, migración, `package*.json` ni archivo de entorno en el diff (103 archivos, 4304+/1024-).
- **PL-36 Conforme.** `git diff --stat` sobre `src/lib/pr`, `dashboard`, `curva-s`, `plan-maestro`, `dp` vacío (cálculos EVM intactos). Páginas PR, Dashboard servicio, Dashboard portafolio, DP, Plan Maestro y Registro de costos: solo guardia rol+alcance por OT (y `puedeEditarTipo = puedeVerEconomia` por C35; DP: `puedeImportarDp`; Registro de costos: modo `soloSubir` sin leer el registro para Logística). Hallazgos a declarar: (a) `api/curva-s` añade validación de id (400) y servicio inexistente (404), sin tocar `lib/curva-s`; (b) `api/plan-maestro`, `dp/exportar` y `registro-costos` API sumaron guardia de rol/alcance; (c) Paquetes de Trabajo retiró `precio_unitario` del select (regla de Victor: ningún rol sin economía recibe precios).
- **PL-74 Conforme.** `npm test`: Test Files 70 passed (70); Tests 672 passed (672); 3,29 s. Pruebas específicas nuevas: cobertura-pantallas, equivalencia-f1b, fuente-servicio, matriz-accesos, panel-derecho, panel-izquierdo, registro-accesos, registro-humo, servicio-contexto, id-proyecto, permisos (13 roles), nav-proyecto, ots-seleccion, grupo-proceso.
- **PL-75 Conforme.** `npm run lint`: worktree 27 problemas (9 errores, 18 advertencias) = baseline `main` (9/18). `eslint` sobre los archivos modificados da 11 problemas (3 errores, 8 advertencias) idénticos a los que da `main` sobre los mismos archivos (preexistentes, no introducidos); archivos nuevos sin problemas.
- **PL-76 Conforme.** `npx next build --webpack` en el worktree: exit 0, todas las rutas listadas; sin artefactos añadidos a git (árbol limpio).
- **PL-79 Conforme, con declaración.** Revisados los handoffs de todas las tandas: no hubo escritura sobre datos reales. Victor autorizó (2026-09-30) registros de prueba marcados `PRUEBA-PL` en Recursos (F5D-A/B y F6-C), todos `activo=false`, ninguna fila borrada: Personal DNI 99999901, 99999902, 99999903; Cargo 3f33340d-dddb-4b83-8609-27b680580867 y `PRUEBA-PL cargos A/J`; Equipo 4595f1f6-f744-4cbb-a579-cb285113afce y `PRUEBA-PL equipos A/J`; Causa CNC 68287d9a-803e-43c4-a6c5-d11e7e32a07f y `PRUEBA-PL causa A/J editada`. Las demás pruebas de acciones fueron con id inexistente o cuerpo inválido; «Ver como» siempre restaurado (DELETE 200).
- **PL-87 Conforme (limitaciones declaradas).** Sin SVX real en la BD; cuenta B = Supervisor Operativo; Observados: PL-07, PL-12, PL-65, PL-78, PL-95, PL-101, PL-117, PL-137, PL-174 a PL-180. Decisiones de negocio pendientes de Victor: (1) dashboard del portafolio solo con OT con alcance; (2) perfil extendido editable solo por admin+JP (los otros 11 roles ya no editan su celular); (3) descripción de Cargo/Equipo no editable (cascada en personal, rdt_tareo, DP); (4) `GET /api/cronograma` y `/api/rdts/consolidado` sin alcance por OT en lectura; además `dp/exportar`, `requerimientos/exportar` y `formato-vacio` sin rol/alcance según nota de F0 (revisar contra el estado actual en F7-B). Sin artefacto de checklist visual.

## F7-A (2026-09-30) — documentación de paneles, política de interfaz, asistente y design.md

Consulta: Victor aprobó el 2026-09-30 reescribir los flujos según las resoluciones C1 a C11, C22, C28, V1, V3, V4, V7 (V2 en flujo 17), E1 y la decisión 4 del plan. Solo lectura sobre el código de `local-worker-1` para reflejar el estado real (27 chips, 7 grupos, `ChatPlaceholder` 48 px, `z-40`, `aria-disabled`).

| Ítem | Estado | Sección actualizada (base de PL-150) |
|---|---|---|
| PL-58 | Conforme | `docs/04-flujos-de-negocio/16-paneles.md` § «Política de interfaz nueva»; `docs/01-contexto-repositorio/05-diseno-y-ui.md` § «Política de interfaz nueva (instrucción para el Worker y el Planner)» con la plantilla de 7 ítems |
| PL-84 | Conforme | `docs/05-diseno-y-referencias/design.md` §5 «Chip de acceso deshabilitado y registro de accesos»; historial 1.4.0 |
| PL-118 | Conforme | flujo 16 § «Asistente: elemento del shell fuera de los tres paneles»; flujo 01 (apartado Proyectos, enlace al 16); flujo 17 (aclaración V2); `design.md` §3 «Asistente flotante» |

Contradicciones cerradas en `16-paneles.md`: C1, C2 (reglas 2 y 3), C3 y C4 (panel izquierdo, Recursos de empresa), C5 (regla 7), C6 (árbol de 7 grupos), C7 (estado de implementación consolidado; se eliminó el bloque duplicado y el texto cortado «tablas con scrol»), C8 (E1), C9 y C28 (regla 10, «Tabla de accesos»), C10 (`requiere servicio` con «opcional»), C22, V1, V3, V4, V7. C11 en flujo 01. Flujos 14 y artefacto sin tocar (F7-B). Sin commit.

## F7-B (2026-09-30) · Flujo 14, artefacto «Matriz de permisos» y descargas

Respuestas de Victor (2026-09-30): (A) las 5 descargas de A13 valen para los 13 roles, con rechazo a quien no tenga rol conocido; A12 confirmado (RDTs zip/PDF/uno/archivo subido y listado RQ: 13 roles; exportar DP sigue a «ver DP»). (B) Autoriza actualizar el artefacto para que quede igual que el flujo 14, sin cambiar el estado «En revisión».

- **PL-83 · Conforme.** Comparación registro vs base del flujo 14, repetible con: `cd D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-1; npx vitest run src/lib/config/matriz-accesos.test.ts` (prueba «matriz derivada del registro vs flujo 14 (PL-56)»; base transcrita en `src/lib/config/matriz-base-flujo14.ts`, derivación en `matriz-accesos.ts`). Resultado 2026-09-30 sobre HEAD b4d3a4a: 4/4 verdes y `DIFERENCIAS_CONOCIDAS = {}` (cero diferencias). No se reescribió la base; las filas de descargas nuevas no tienen id en el registro, así que la base no las cubre (ver hallazgo).
- **PL-100 · Conforme.** Diff de `docs/04-flujos-de-negocio/14-accesos-y-restricciones.md`: solo la decisión de Victor (descargas, nota 7, punto por decidir 1 cerrado), la nota del asistente y la aclaración de fecha; tablas 1 y 2 aprobadas intactas, sin dos versiones conviviendo (el consolidado RQ y el registro de costos siguen en sus filas de 2026-09-28).
- **PL-173 · Conforme.** Retiradas las 9 marcas «(por construir)» del grupo Recursos en el flujo 14 (y la nota 6 lo explica) y en el artefacto. Es coherente porque Victor aprobó la gestión total de Recursos y las 9 acciones existen (F5D); quién puede ejecutarlas no cambia.
- **PL-155 · Conforme.** Lista confirmada con el código (HEAD b4d3a4a), por ruta de API y guardia real:
  - Plantilla de cronograma `api/cronograma/plantilla`: `puedeSubirCronograma` (admin, JP, planner). **NO cumple** «13 roles» (hallazgo).
  - PDF de un RDT estructurado `api/rdts/partes/[id]/pdf`, archivo de RDT subido `api/rdts/[id]/archivo`, ZIP/PDF `api/rdts/exportar`: `puedeVerRdts` = rol conocido. Cumple (A12).
  - PDF individual de RQ y listado RQ `api/proyectos/[id]/requerimientos/exportar` (`tipo=detalle|registro|vacio`): `puedeVerStatusRequerimiento` = rol conocido. Cumple.
  - Formato vacío PROM-GP-008: `.../exportar?tipo=vacio` cumple; `api/requerimientos/formato-vacio` solo exige sesión (401 sin sesión, sin comprobar rol). **NO cumple** (hallazgo).
  - Exportar DP `api/proyectos/[id]/dp/exportar`: `puedeVerDp` (economía + SOT), igual que el flujo.
  - Adjuntos de RQ y documentos del checklist (por verificar en el brief): solo existe `POST` (subida) en sus rutas; no hay descarga por API. Quedan fuera de la matriz de descargas.
- **PL-156 · Observado.** «Descargas» del artefacto y tabla 2 del flujo 14 alineadas (mismas 10 filas de descarga incluidas registro de costos y consolidado RQ). El estado del artefacto sigue «En revisión»: solo Victor lo cambia. Falta una captura del artefacto (no tomada: verificación por lectura del HTML publicado).
- **PL-149 · Observado.** Trazabilidad: Ficha del servicio, Editar servicio, Editar checklist, gestión de Recursos (9 acciones), «solo subir» del registro de costos y las descargas figuran en artefacto y flujo 14; el registro único de entradas coincide con la tabla 1 (PL-83). El asistente del shell se anotó como excepción sin fila (el flujo 16 dice que no figura en la matriz; no se crea fila con permiso). Artefacto publicado en la versión 7 (`https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT`, version id 1790781681-a76d), con `read` previo. Pendiente: captura del artefacto y comprobación del Auditor.
- **Hallazgos para el Orquestador (no corregidos):** (1) `api/cronograma/plantilla` solo admite administrador, JP y planner, y Victor decidió 13 roles; (2) `api/requerimientos/formato-vacio` solo exige sesión; ambos requieren `tieneRolConocido` (y, si se quiere que la prueba los cubra, ids en el registro de accesos y base). (3) Las casillas guardadas en la base de datos del artefacto (estado de Victor) no se tocaron; solo cambió el HTML de la propuesta.

## F6-R1 · PL-155 (parte de código) — Conforme (2026-09-30)

- Commit `0690c81` en `local-worker-1`: `puedeDescargarPlantillaCronograma` y `puedeDescargarFormatoRequerimientoVacio` (ambas con `tieneRolConocido`, 13 roles; rol desconocido rechazado). `/api/cronograma/plantilla` usa la primera (antes `puedeSubirCronograma`, que no se tocó); `/api/requerimientos/formato-vacio` añade 403 por rol.
- Pruebas: 675 verdes (3 nuevas: 13 roles, rol vacío/inventado, subir cronograma sin cambio); tsc limpio; lint 9 errores/18 advertencias (baseline).
- Verificación en vivo (dev :3111, cuenta A, «Ver como» los 13 roles): `formato-vacio` = 200 `application/pdf` en los 13; `plantilla` con id inexistente = 400 en los 13 (pasó la guardia de rol; ninguno 403). Sin escrituras. «Ver como» restaurado (DELETE 200). No se probó el 403 de rol desconocido en vivo (no hay cuenta sin rol); lo cubre la prueba unitaria.

## PL-82 (F7-C, 2026-09-30) — Observado
- Reescritos, integrados en su estructura, según C16-C36 y V6 aprobadas por Victor el 2026-09-30: flujos 03, 05, 06, 08, 09, 11, 12, 15, 20, 21 y `04-flujos-de-negocio/README.md` (regla «Borrado administrador» con citas en 05, 06 y 08 enlazadas). Contraste con `registro-accesos.ts`, `grupo-proceso.ts`, `permisos.ts` y páginas de RDT/RQ/Dashboard en `local-worker-1` (0690c81): 10 chips de Mi entorno iguales en los 8 grupos, `/rdts/status` y `/rdts/listado` (borrado solo ahí), interruptor con `puedeVerEconomia`.
- Diff: `git diff -- docs/04-flujos-de-negocio` en `pg_control_proyectos`. Grep de residuos («solo admin», «Jefe de oficina técnica adjudica», «todos menos asistente», `puedeAdjudicarProyecto` como regla): sin restos.
- Observado (no editable en esta tanda): flujo 14 (a) nota ¹ y «Puntos por decidir» 3 y 5 siguen diciendo que 02/05/06/08/12/13 contradicen y que el interruptor «queda por confirmar» (ya resuelto, C35); (b) flujos «Revisados» 02 y 13 no releídos: pueden citar al JOT con ciclo de vida.

## PL-82 (F7-C2, cierre) — Conforme

- Flujo 14: nota ¹ ahora recoge C35 (Victor, 2026-09-29: alternan Parcial/Completo los roles con `puedeVerEconomia`; los demás lo verían fijo en Parcial, plan futuro). «Puntos por decidir» 3, 4 y 5 marcados «Cerrado» con fecha y decisión (3: flujos reescritos 2026-09-30, 02 y 13 sin citas; 4 y la frase «por confirmar» de la lista de diferencias: solo logística, 2026-09-29; 5: C35). Ninguna celda de las tablas 1 y 2 cambió.
- Flujos 02 (`02-usuarios.md`) y 13: Grep de oficina técnica / solo administrador / eliminar / archivar / adjudicar / borrar: sin citas del ciclo de vida ni de borrados; no se tocan.
- `git status`: 16, 01, 17 y 14 modificados sin commitear (esperado); sin reglas duplicadas.
- Decisiones 2026-09-30 (dashboard del portafolio con alcance, perfil extendido, R30) figuran en el Registro como «provisionales»; no afectan al texto del flujo 14.

## PL-81, PL-85, PL-86, PL-150 (F7-D, 2026-09-30)

- **PL-81 — Conforme.** Consulta en bloque, pregunta y respuesta «APROBADO» de Victor (2026-09-30) registradas en el progreso, sección «Consulta en bloque previa a la edición de flujos».
- **PL-150 — Conforme.** Tabla «Trazabilidad por flujo» completada en el progreso (consulta, tanda que actualizó y enlace a la sección) para los 21 flujos, README, artefacto, `05-diseno-y-ui.md`, `design.md` y `03-entorno-git-y-worktrees.md`. Búsqueda de referencias a la versión anterior sin restos (solo menciones históricas explicadas en el flujo 14).
- **PL-85 — Conforme.** Diff: archivo nuevo `docs/03-aprendizaje-continuo/2026-09-30-plan-paneles-servicio-persistente-tandas.md`; fila nueva en `docs/03-aprendizaje-continuo/README.md`; estado del plan en `docs/02-trabajo-activo/01-planes/README.md`; tabla «Resultados por tanda» de `medicion.md` (salida de `medir.py 60`); sección «Pool real de ramas y worktrees» de `03-entorno-git-y-worktrees.md`. Reglas de negocio: verificadas en los flujos. Huérfanos reportados a Victor sin borrar: `hist_nucleo/.env.local`, `hist_local-worker`, los dos `git stash` de `py_control_proyectos_web` y los 12 registros PRUEBA-PL de Recursos (activo=false).
- **PL-86 — Observado.** Búsqueda en memoria (script temporal, ya borrado) de los valores de `cuentas-prueba.md` sobre el árbol de trabajo de ambos repositorios (sin `node_modules`, `.next` ni `.git`) y sobre `git diff HEAD` y `git log -p -n 40`. Solo conteos: `pg_control_proyectos`: 84 líneas en 51 archivos (83 líneas en 50 archivos de `.playwright-mcp/`, carpeta ignorada por git y no versionada; 1 línea en `docs/02-trabajo-activo/01-planes/2026-09-20-sub-lote-2-alcance-proyecto.md`, línea 233, coincide con el correo de una cuenta, no con una contraseña; plan cerrado); `git diff HEAD` y `git log -p -n 40`: 0. `py_control_proyectos_web`: 0 en el árbol (incluido `.worktrees/local-worker-1`), 0 en `git diff HEAD`; `git log -p -n 40` de `local-worker-1`: 37 líneas, todas cabeceras `Author:` (coincide un valor con el correo del autor de los commits), 0 en contenido. Ningún valor se imprimió ni se guardó.

## F6-R2 (2026-09-30) - servicio de prueba SVX y reprueba en vivo

**SVX creado (autorizado por Victor):** OT `PS-0006`, uuid `5769ee50-f49c-4aab-9968-65ad56fe7c07`, nombre `PRUEBA-PL SVX servicio de prueba F6-R2` (cliente/area/OC con prefijo `PRUEBA-PL SVX`), portafolio "Servicios Marcobre" (programa Promcoser). Cuenta A, flujo real: `/programas/.../proyectos/nuevo` con los 11 documentos del checklist marcados, sin supervisor operativo. Importado por la UI: DP con `PPTO-prueba N°01.xlsx` (POST `/api/proyectos/[id]/dp` 200; observacion: partida 03.01 sin mano de obra) y cronograma con `Cron-prueba N°01.xlsx` en `/cronograma` (extraccion completa: 14 actividades, 11 enlazadas al DP). Membresia resultante (`api/proyectos/route.ts`): solo el creador (cuenta A), y el supervisor si se elige. No se tocaron PS-0004, PS-0005 ni datos reales. Ver como restaurado (DELETE /api/ver-como).

**Hecho en vivo (con alcance, A con Ver como):** jefe_de_proyectos abre PR, Dashboard, dashboard del portafolio, DP, Plan Maestro `?proyectoId=`, registro de costos de SVX (200); `dp/exportar?formato=xlsx` 200 (xlsx), `/api/plan-maestro` 200, `/api/proyectos/SVX/registro-costos` 404 "No hay registro" (paso la guardia). planner, supervisor_logistica y supervisor_operativo: paginas de economia "No tienes acceso al ... de este servicio" (rol), APIs 403 "No autorizado"; logistica abre registro-costos (solo subir) y Plan Maestro solo para planner. Captura: `capturas/paneles-servicio-persistente/PL-175-SVX-dashboard-con-alcance.jpg`.

**PL-46 (parte SVX), cuenta B (Supervisor Operativo):** SVX y SV1: `/api/cronograma` 200, `/api/rdts/consolidado` 200, `/api/curva-s` 403; id inexistente: 404 "Servicio no encontrado" (cronograma, consolidado), curva-s 403; id basura: 400 "El N° OT del servicio no es valido". Nunca 500. Ya figuraba Conforme.

**PL-95 (tabla chip x rol, `aria-disabled` en HTML de `/proyectos/SVX`, `/programas`, portafolio, `/mi-entorno` con los 13 roles):** panel del servicio: administrador, JP, JOT, sup. costos y jefe de costos con los 6 chips de economia activos; planner solo Plan Maestro; sup. OT solo DP; los otros 8 roles, todo deshabilitado. En panel de portafolio, inicio y mi-entorno los chips de economia solo se ven deshabilitados para roles fuera de la tabla 1; para roles dentro no hay servicio elegido ("Elige un servicio"). No se verifico Accesos rapidos para roles con economia con servicio activo. Sigue Observado.

**BLOQUEO (PL-174 a PL-180): no se pudo producir "OT sin alcance".** La cuenta A es miembro de PS-0004, PS-0005 y PS-0006 (JP con Ver como abre todo), asi que nunca hay caso negativo por alcance. Unico camino: quitar a A de PS-0006 (PATCH `/api/admin/usuarios/[id]` con `quitarProyectos`, fila de `proyecto_miembros` solo del servicio de prueba). El clasificador automatico de permisos denego esa llamada; no se intento eludir. La cuenta B no sirve (no tiene rol con economia, cualquier rechazo seria por rol). PL-180 (admin entra a SVX sin ser miembro) exige el mismo paso. Queda Observado con esta causa.

## F6-R3 (2026-09-30) - alcance por OT en vivo (PL-174 a PL-180, PL-95)

Con autorizacion explicita de Victor se quito a la cuenta A de PS-0006 (`PATCH /api/admin/usuarios/<A>` con `quitarProyectos`, 200) y al terminar se re-asigno (`asignarProyectos`, 200). Con A fuera de PS-0006, sondeo por fetch autenticado con Ver como a `jefe_de_proyectos`, `jefe_de_oficina_tecnica`, `supervisor_costos`, `jefe_de_costos`, `planner` y `supervisor_logistica` sobre PS-0006 (sin alcance) frente a las otras dos OT del portafolio (con alcance).
- Sin alcance (PS-0006): paginas PR, Dashboard, DP y registro de costos "No tienes acceso al ... de este servicio" (las paginas usan un solo texto para rol y alcance, igual que Curva S; se distingue porque el mismo rol abre en las otras OT); Plan Maestro pagina y `GET /api/plan-maestro` 403 "No tienes esta OT a cargo" (incluido planner); `dp/exportar` 403 "No tienes esta OT a cargo"; `registro-costos` API 403 "No tienes esta OT a cargo" para JP. Rechazo por rol ("No autorizado") en registro-costos API para JOT, costos, planner y logistica en las tres OT.
- Con alcance: todas 200 (dp/exportar 404 si la OT no tiene DP; registro-costos API 404 "No hay registro").
- Dashboard del portafolio: administrador 3 servicios, JP con Ver como 2 (sin PS-0006).
- Administrador sin Ver como (A fuera de PS-0006): las seis pantallas y las APIs de PS-0006 en 200 (PL-180).
- PL-179 logistica: registro de costos rechazado en PS-0006 y abierto en las otras dos.
- PL-95: `/mi-entorno?proyectoId=<uuid>`: administrador y JP economia activa; planner solo Plan Maestro; sup. operativo y SSOMA todo deshabilitado. Accesos rapidos (Tareo MOI, Pets, Acta, Status, Requerimiento, Consolidado RQ, Subir RDTs) no lleva chips de economia.
- Captura: `capturas/paneles-servicio-persistente/PL-175-SVX-dashboard-sin-alcance.jpg`. Sin cambios de codigo. Ver como restaurado. Servidor 3111 detenido.
