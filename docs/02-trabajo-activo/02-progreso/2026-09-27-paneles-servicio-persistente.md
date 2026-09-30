# Progreso — Paneles: servicio persistente

## Referencia al plan

`docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente.md` (v8). Briefs, índice de tandas y medición: `2026-09-27-paneles-servicio-persistente-briefs/`.

## Estado general y fase actual

Ejecución iniciada el 2026-09-29 (Victor: «implementemos el plan… continua»). Fase F0, tanda F0-A.

## Tabla de roles / Workers y estado

| Rol | Etiqueta | Rama | Estado |
|---|---|---|---|
| Orquestador | sesión principal | `main` (solo docs) | Activo |
| Worker | `local_3.worker_paneles-servicio-persistente-<tanda>` | `local-worker-1` | Ver índice de tandas |

## Avances terminados

Ninguno aún.

## Trabajo actual

F0-A.

## Pendientes

Las 38 tandas del índice.

## Commits, ramas y worktrees usados

Worktree `py_control_proyectos_web/.worktrees/local-worker-1`, rama `local-worker-1` desde `main` `1942b01`.

## Hallazgos registrados en el momento

Ninguno.

## Bloqueos, riesgos y decisiones requeridas

Puntos de pausa: antes de F5D-A, antes de F7-A y después de F6-E (ver índice).

## Próximo paso verificable

Cerrar F0-A con evidencia de LB-01, PL-127 y PL-146.

## Última actualización y responsable

2026-09-29 · Orquestador.

## Handoffs



### Handoff F0-A (Worker local-3, 2026-09-29)
- Conforme: PL-127 (inventario de 9 rutas de descarga + BotonDescargarPdf + Storage), PL-146 (tabla de funciones de permisos contra el código, con alias y usos). LB-01 medido.
- LB-01 en `1942b01`: `npm test` 60 archivos, 528/528 pasan; `npm run lint` 27 problemas (9 errores, 18 advertencias); `npx next build --webpack` compila. Árbol limpio, sin cambios de código.
- Para Victor (entrada de PL-155/F7-B): `dp/exportar`, `requerimientos/exportar` y `requerimientos/formato-vacio` solo exigen sesión (sin rol ni alcance por OT); guardia no cambiada (A13). Adjuntos de RQ y documentos del checklist solo tienen subida, no descarga: nada faltante en el artefacto.
- Hallazgos para F1: `puedeEditarPerfilExtendido` no tiene usos en `src/` (ubicar la guardia real del perfil); `lib/notificaciones/grupo-proceso.ts` usa 6 funciones de permisos que cambian; la tabla del plan omite `puedeVerApartadoProyectos` y `puedeSubirDocumentoAsignado`.
- Sin preguntas devueltas. Siguiente: F0-B (navegador, lo lanza el Orquestador). Sin commit de código; evidencia y progreso quedan modificados en pg_control_proyectos sin commitear.

### Handoff F0-B (final, 2026-09-29)
- Conforme: LB-02 (7 capturas), LB-03 (derivado del codigo y confirmado en navegador), LB-04 (4 capturas), LB-05 (SV1=PS-0004, SV2=PS-0005; cuenta B = Supervisor Operativo). Detalle en evidencia. Sin commit ni cambios de codigo/db.
- Login con browser_fill_form funciono sin bloqueo (cuentas A y B).
- Observado: SVX (B sin membresia) no existe ni se puede comprobar: solo hay 2 servicios y B ve ambos; proyecto_miembros no es visible en la UI y el MCP postgresql no conecto. Pregunta al Orquestador: aceptar "sin SVX" o indicar una OT/consulta para probar "No tienes esta OT a cargo".
- Hallazgo de linea base: B (Supervisor Operativo) recibe 200 por URL directa en Recursos, /admin/usuarios, editar servicio, checklist/editar, DP, PR, Dashboard, Curva S, Cronograma, Plan Maestro y /rdts/crear; hoy solo se ocultan chips y paneles. El chip Status de RDTs es /rdts/listado (no /rdts/status).
- Asistente: barra solo en escritorio con servicio (oculta en movil por hidden lg:block, ausente sin servicio) y copia en portafolio.
- Servidor 3111 iniciado por este Worker y detenido al cerrar; worktree sin cambios.

### Handoff F0-C (final, 2026-09-29)
- Conforme: PL-147. Tablas 1 y 2 «antes» (13 roles, UI y servidor) en la evidencia (seccion «F0-C»), con las celdas que difieren del flujo 14 marcadas (`✓→—`, `—→✓`; 36 celdas). Base de PL-97 (F6-A).
- Metodo: vitest temporal `_lb-f0.test.ts` (borrado; worktree limpio) + Grep de guardias + muestra «Ver como» (asistente, SOp, SLog) con `fetch` en un solo `browser_evaluate`; coincide con la tabla calculada. Rol restaurado (`DELETE /api/ver-como` 200). Servidor 3111 iniciado y detenido por este Worker.
- Hallazgo: la sesion abierta al inicio era la cuenta B (SOp); se cerro y se entro con A. El `redirect()` de servidor llega con HTTP 200 + `NEXT_REDIRECT`: el «200 por URL directa» de B en Recursos, /admin/usuarios, editar servicio y checklist/editar (F0-B) es redireccion, no acceso. PR, Dashboard, DP siguen sin guardia (200 real); Curva S del asistente muestra mensaje sin acceso.
- Hallazgo: `puedeEditarPerfilExtendido` sin uso; `PATCH /api/perfil` sin guardia de rol (13 roles).
- Limite: con id inexistente `POST .../requerimientos` evalua alcance antes que rol, y SVX sigue sin existir; el alcance por OT (R28) solo se vio en registro-costos POST (SLog).
- Sin preguntas devueltas, sin commit de codigo, sin db/. Pendiente para el Orquestador: commit de evidencia, progreso y plan en pg_control_proyectos.

## Handoff F1-A (2026-09-29)
- Conforme: PL-51 + registro base. Commit `06f40f3` en `local-worker-1`. Pendiente: nada de F1-A. Siguiente: F1-B.
- Retomar: `cd .worktrees/local-worker-1; npm test; npm run lint; npx tsc --noEmit` (540 pruebas; lint 9/18 = base).
- Decisión técnica: `permiso` declara la función vigente de permisos.ts solo donde el nombre coincide con el destino (cronograma, paquetes, plan-maestro, curva-s, rdt, crear-rdt, status/listado/consolidado-rdts, consolidado-rq, crear-rq); el resto `PERMISO_LIBRE`. La interfaz aún NO filtra por `permiso` (F1-B+). Conviene contrastarlo con flujo 14 tabla 1 antes de aplicarlo.
- Decisión: `visible.accesoRapido` es número (posición) para conservar el orden de chips. `visible.centro` = false en todos (aún no hay chips en el centro).
- `tipo: 'accion'` en crear-rdt, rdt, crear-requerimiento-servicios; el resto `informativo`.
- Trampa: `encontrarItemNavProyecto` debe tener UN solo parámetro (PanelSecciones lo usa en `map`); la variante con nav es `encontrarItemEn`.
- Vitest no resuelve el alias `@/`: en `src/lib/config` usar rutas relativas.
- `ItemNavProyecto` ahora incluye `requiereServicio`. Sin unión rdt/subir-rdt (E3 = F1-B).


## Handoff F1-B (2026-09-29)
- Conforme: PL-50, PL-52. Commit `2d6c9d9` en `local-worker-1`. Pendiente: nada de F1-B. Fase F1 completa.
- Retomar: `cd .worktrees/local-worker-1; npm test; npm run lint; npx tsc --noEmit` (548 pruebas; lint 9/18 = base).
- Decision E3 aplicada: `status-rdts` = `/rdts/status` en Mi entorno; `listado-rdts` = Archivo de RDTs subidos (`/rdts/listado`, solo panel derecho). Claves de Mi entorno: `listado-rdts`->`status-rdts`, `subir-rdt`->`rdt`.
- Registro: 46 entradas (41 nav + `enviar-notificacion` + 4 `recursos-*`); grupos `Mi entorno` y `Recursos de empresa` en `GRUPOS_FUERA_DE_NAV` (fuera de NAV_PROYECTO).
- Transitorios a retirar: `visible.centroConServicio` (F2-A, ?proyectoId= a todos los chips) y `visible.centroSiempreHabilitado` (Crear RQ estaba siempre habilitado en Mi entorno aunque `puedeCrearRequerimiento` sea mas estricta; decidir en la fase que aplique permisos por panel; flujo 14).
- WorkspaceShell: el guardia de Recursos sigue con los flags `puedeVerRecursos`/`puedeGestionarCatalogoCnc` del layout (misma funcion que `permiso`); el `span` Materiales se inserta por id (`recursos-causas-cnc`); F3 rehace el panel.
- Hallazgo: la prueba de equivalencia congela LB-03; si F2+ cambia hrefs, actualizar `equivalencia-f1b.test.ts`.

## Handoff F2-A (Worker local-3, 2026-09-30)
- Conforme: PL-01, PL-15, PL-16, PL-37, PL-47, PL-66, PL-72 (PL-72 = helper; el uso en redirects es F2-D). Observado: ninguno. Falta: nada de F2-A.
- Codigo (rama local-worker-1): `src/lib/config/servicio-contexto.ts` (+test), WorkspaceShell (bloque "Servicio actual", validacion contra servicios visibles, enlaces de Recursos/pie con servicio), layout (lista de servicios), registro (retirado `centroConServicio`), grupo-proceso, equivalencia-f1b.test.
- Decision: servicio validado contra `proyectos` no archivados visibles por RLS pasados desde el layout; URL = unica fuente (`/proyectos/<id>` o `?proyectoId=` en cualquier ruta; `/programas/**` no).
- Cambio visible declarado: Mi entorno ahora envia `?proyectoId=` tambien en Cronograma y Plan Maestro (antes solo Crear RQ y Subir RDTs), por el brief (si/opcional).
- `centroSiempreHabilitado` se conserva (retirarlo cambiaria permisos de Crear RQ): decision pendiente para la fase de permisos por panel.
- Hallazgos: los accesos `requiereServicio: no` (Notificaciones del grupo Proyecto, Status RQ, Consolidado RQ, RDTs) no llevan servicio al navegar, asi que en esas paginas el panel queda sin servicio; A2 pide conservarlo solo en pie y Recursos. Archivado no probado con dato real (no hay servicio archivado).
- Comandos: `npm test` (590 ok), `npx tsc --noEmit`, `npm run lint` (9 err/18 warn = baseline), `npm run dev -- --webpack -p 3111`.


## Handoff F2-B (Worker local-3, 2026-09-30)
- Conforme: PL-02, PL-03, PL-04, PL-11, PL-14. Observado: PL-12 (solo Registro de costos: la cuenta A no pasa la guardia de rol; DP/PR/Dashboard/Curva S conformes). Falta: nada de F2-B.
- Codigo (rama local-worker-1): `src/components/ui/useServicioEnUrl.ts` (hooks `useCambiarServicioEnUrl` y `useSincronizarServicio`) usados en FormularioCronograma, FormularioPaquetesTrabajo y FormularioPlanMaestro; el selector hace router.replace con `conServicio` y sigue a la URL cuando esta cambia.
- Defecto previo: FormularioCronograma fallaba con servicios sin cronograma (API sin `partidasDp`); corregido con `?? []`.
- Decision: la sincronizacion URL a selector solo actua al cambiar el id de la URL (sin bucle, R11); si la URL no trae servicio, el formulario sigue eligiendo el primero sin escribir la URL.
- Hallazgo: para PL-12 completo hace falta probar registro-costos con supervisor_logistica o jefe_de_proyectos (ver-como).
- Comandos: `npm test` (590), `npx tsc --noEmit`, `npm run lint` (9/18 = baseline), `npm run dev -- --webpack -p 3111`.


## Handoff F2-C (Worker local-3, 2026-09-30)
- Conforme: PL-05, PL-06, PL-08, PL-09, PL-10, PL-13. Observado: PL-07 (archivo de RDTs vacio: filtro no legible en pantalla; paneles ok). Falta: nada de F2-C.
- Codigo (rama local-worker-1): registro-accesos (6 accesos a `opcional` con `?proyectoId=`), `src/lib/servicios/servicio-pagina.ts` (valida el servicio con RLS y no archivado), 6 paginas leen `searchParams.proyectoId`; Tabla Status/Listado RDTs y Consolidado RQ con prop `numeroOtInicial` (sigue a la URL sin efectos); TablaConsolidadoRdts y FormularioCrearRdt con `proyectoIdInicial` + hooks de F2-B; `rutaStatusRq` acepta `proyectoId`, el redirect de `/proyectos/<id>/requerimientos` lo conserva.
- Decision: `ots` sigue siendo solo la seleccion de la tabla; `proyectoId` es el contexto de paneles y preselecciona el filtro si no viene `ots`. R3 no aplica: N° OT tiene formato PS-####, sin colision de prefijos.
- Diferencia declarada: chips/accesos de esas pantallas ahora llevan `?proyectoId=` (tests de equivalencia y nav actualizados). Permisos sin cambios.
- Hallazgo menor: en Status de RDTs, si el servicio de la URL no tiene partes, el select del filtro muestra "Todos" (sus opciones salen de los datos) aunque el estado filtra por el servicio.
- Comandos: `npm test` (591), `npx tsc --noEmit`, `npm run lint` (9/18), `npm run dev -- --webpack -p 3111`.


## Handoff F2-D (Worker local-3, 2026-09-30)
- Conforme: PL-19, PL-20, PL-21, PL-70. Observado: ninguno. Falta: nada de F2-D.
- Codigo (rama local-worker-1): 13 paginas con redirect por permiso usan `conServicio('/mi-entorno', proyectoId)` (mi-perfil, rdts, recursos/* leen ahora `searchParams`); `FormularioCrearRdt` y `FormularioRequerimiento` conservan el servicio al guardar; nuevo `src/components/ui/SalirAMiEntorno.tsx` (cliente) usado por `CabeceraPagina` (sigue de servidor).
- Decision: el chip lee el servicio de la URL (no hay prop en 20 pantallas); tras guardar se usa el servicio del formulario.
- Pruebas: +5 unitarias. Comandos: `npm test` (596), `npx tsc --noEmit`, `npm run lint` (9/18 = baseline), `npm run dev -- --webpack -p 3111`.
- Hallazgo: `fetch` a una pagina que redirige no muestra la URL final (redireccion por streaming); verificar con navegacion real.


## Handoff F2-E (cierra F2)
- Conforme: PL-17, PL-18, PL-67, PL-69. Sin cambios de codigo, sin commit en local-worker-1 (ultimo 73f22fc). F2 completa: solo PL-07 y PL-12 Observados (para F6).
- Metodo: `addInitScript` con MutationObserver + PerformanceObserver desde el primer render, 23 rutas x cuentas A y B; "Selecciona un servicio" 0 veces, CLS max 0.007; control positivo sin servicio.
- Hallazgo cosmetico (PL-69/F2-C): con un servicio sin DP (PS-0005) los selectores de OT de Paquetes, Crear RDTs, Consolidado RDTs y los filtros de Status de RDTs muestran placeholder/"Todos" porque sus opciones salen de datos. Paneles y chips correctos. Decidir en F6 si se quiere incluir el servicio actual en las opciones.
- Servicios: SV1 = PS-0004 (dc850536…), SV2 = PS-0005 (3b869b75…, sin DP). Dev: `npm run dev -- --webpack -p 3111` en el worktree.
- Capturas PL-17/18/67/69 en `03-evidencia/capturas/paneles-servicio-persistente/` (PL-18 y PL-67 son copia de PL-17).

## Handoff F2B-A (Worker local-3, 2026-09-30)
- Conforme: PL-92, PL-94, PL-119, PL-120. PL-88 parte F2B hecha; se cierra en F5B-A (misma prueba con economía).
- Sin pendientes de la tanda. Observación: «sin sesión → /login» de PL-92 verificado solo por código.
- Decisiones técnicas: helper `tieneRolConocido` (13 roles; lista vacía o rol ajeno = rechazado); `puedeDescargarConsolidadoRq` desacoplada para no ampliar la descarga; `POST recursos/personal` usa `puedeVerApartadoProyectos` (mismo conjunto admin/JP) hasta F5D; Causas CNC y Personal reciben `puedeGestionar`/`puedeCrear` para ocultar acciones.
- Hallazgo: `rdts/exportar`, `partes/[id]/pdf` y `[id]/archivo` quedan abiertas a 13 roles al ampliar `puedeVerRdts` (descargas por decidir en flujo 14).
- Verificado: npm test 599 verdes, tsc limpio, lint 9 errores/18 advertencias (baseline). Dev :3111 detenido; «Ver como» restaurado.
- Retomar: `git log -1` en local-worker-1; siguiente tanda según `00-indice-de-tandas.md`.


## Handoff F2B-B parte 1 (PL-121)
- PL-121: Observado. Sin dinero visible en pantallas (cuentas A y B). Hallazgo R25: `precio_unitario` viaja en `GET /api/paquetes-trabajo` (route.ts ~72) sin mostrarse; no editado, a Victor vía Orquestador.
- PL-152 y PL-154: sin tocar, pendientes de la respuesta de Victor sobre A12; se lanzan como continuación.
- Sin commit de código en esta parte (solo lectura). Dev :3111 detenido. Sesión del navegador de prueba quedó con la cuenta B.
- Retomar: `git log -1` en local-worker-1 debe seguir en fb6ae56.


## Handoff F2B-B parte 2 (2026-09-29)
- Conforme: PL-121, PL-152, PL-154. Observado: ninguno.
- Código (local-worker-1): quitado `precio_unitario` de api/paquetes-trabajo y del tipo PartidaDp; guardia `puedeVerStatusRequerimiento` en requerimientos/exportar.
- Pruebas: npm test 599 verdes; tsc limpio; lint 9 errores/18 advertencias (igual al baseline).
- Hallazgo para F5B: `plan-maestro` (api y FormularioPlanMaestro), `dp`, `pr` y `dashboard` también devuelven `precio_unitario` a roles sin economía (no tocados por restricción).
- Sin prueba unitaria nueva: la guardia reutiliza puedeVerStatusRequerimiento (cubierta para los 13 roles). Un rechazo por rol desconocido no se pudo probar en vivo (Ver como solo admite los 13); vitest lo cubre.
- Regla de Victor registrada en el plan (Reglas de negocio acordadas).
- Retomar: `git log -1` en local-worker-1; siguiente tanda F2B cerrada, seguir el índice de tandas.
- Navegador de prueba quedó con la cuenta A; dev :3111 detenido.

## Handoff F3-A (commit b84211b, local-worker-1)
- Conforme: PL-22 a PL-26. Pendiente de la fase F3: F3-B (Recursos de empresa y pie).
- Decisiones técnicas: 7 accesos nuevos en el registro (grupo `Servicio`, fuera de NAV_PROYECTO: ficha, editar servicio, editar checklist, crear paquete, Cargos HH, Equipos HM, Planos); estructura del panel en `src/lib/config/panel-izquierdo.ts`; componente `PanelServicioIzquierdo.tsx` (3 estados: activo, deshabilitado con título, inerte). `usuario.roles` se pasa al shell desde el layout (Ver como incluido).
- Sin servicio el panel izquierdo ya no muestra el bloque «Proyecto» (queda para F3-B); `puedeVerApartadoProyectos` ya no gobierna el bloque con servicio.
- `?accion=crear` en Paquetes de Trabajo abre el formulario solo si el rol puede gestionar.
- Hallazgo: Generar RQ deshabilitado para administrador puro (permiso vigente); decidir si el transitorio `centroSiempreHabilitado` se retira en otra fase.
- Retomar: `cd .worktrees/local-worker-1; npm run dev -- --webpack -p 3111`. Servidor detenido, «Ver como» restaurado.


## Handoff F3-B (commit c51a99e)
- Conforme: PL-27, 28, 29, 49, 59, 60, 62. Nada Observado; F3 completa.
- Cambio único: src/components/ui/WorkspaceShell.tsx: nuevo RecursosEmpresa (botón aria-expanded, nav+h2, ul hidden), Materiales eliminado, panel izquierdo con área de scroll interna y pie shrink-0.
- Decisión: la elección manual del botón vale por modo (con/sin servicio); por defecto visible sin servicio y oculto con servicio; no persiste al recargar.
- Nota: en CNC, la API con Ver como se probó con 5 roles sin permiso (403); el resto de los 13 los cubre la prueba unitaria.
- Retomar: cd .worktrees/local-worker-1; npm run dev -- --webpack -p 3111. Servidor detenido, Ver como restaurado (DELETE).

## Handoff F3-C (2026-09-29) — commit 0819483
- Conforme: PL-38, 39, 40, 48, 61, 63, 64, 71. Pendiente: nada de la tanda; F3 queda cerrada.
- Cambio de código: `tipo` en `HerramientaEntorno`; chips de Mi entorno con `aria-disabled`, título por defecto y insignia «Acción» (EntornoTrabajoGrupo.tsx, grupo-proceso.ts + test).
- Hallazgos para F5B/F5C: economía sin restringir en chips (dp, pr, dashboard, curva-s, costos, plan-maestro); editar-servicio/editar-checklist no coinciden con la matriz (Admin+JP) y sus títulos están desactualizados; el texto «Cree uno» de Paquetes se muestra también a roles sin permiso de gestionar.
- Comprobación de PL-48 solo con B (Supervisor Operativo); acciones de A y de otros roles se revalidan en F5C.
- Retomar: `npm run dev -- --webpack -p 3111` en local-worker-1; `npm test`; lint baseline 9 errores/18 advertencias.


## Handoff F4-A (2026-09-30)
- Conforme: PL-30, 31, 32, 33, 34, 41, 42. Pendiente: nada de esta tanda.
- Cambios (local-worker-1): nuevo `src/lib/config/panel-derecho.ts` (+test); `PanelSecciones.tsx` recibe chips ya resueltos (`AccesosRapidos chips=`, `GruposAccordion grupos=`); `WorkspaceShell` pasa `roles`; "Ver todas" de Mi entorno lleva el servicio.
- Decision tecnica: el estado deshabilitado se aplica tambien sin servicio; Notificaciones (requiereServicio 'no') recibe el servicio via `conServicio` en el panel, sin tocar el registro.
- Hallazgos: la cuenta B (Supervisor Operativo) no ve deshabilitados con SV1; el administrador tiene Crear RQ deshabilitado con las funciones vigentes (F5B lo decide). Solo PS-0004 tiene RDTs, asi que el filtro de Status RDTs no cambia filas.
- Retomar: `npm test`, `npx tsc --noEmit`, `npx eslint` en local-worker-1; dev `npm run dev -- --webpack -p 3111`.

## Handoff F4B-A (2026-09-29) · commit 7c9c6ca en local-worker-1
- Conforme: PL-102 a PL-107. Sin pendientes de la tanda.
- Decision tecnica: ChatPlaceholder pasa a icono flotante `absolute bottom-4 right-4 z-40` dentro de `<main>` (contenedor `relative`), una sola instancia en WorkspaceShell; estado abierto en el propio componente (el shell no remonta). Panel con cabecera, aviso, campo y Enviar; Escape/cerrar devuelven el foco al icono.
- Hallazgo: en movil el indicador de Next Dev Tools (solo dev) intercepta el clic del icono; en la verificacion se oculto `nextjs-portal`.
- Verificado solo con cuenta B (sesion ya abierta) y sin «Ver como»; el asistente no depende del rol.
- F4B-B: mediciones finas de posicion/a11y (aria-live, z-index vs modales y cabeceras z-20/z-30 no probado con modal abierto).
- Retomar: `npm run dev -- --webpack -p 3111` en el worktree; servidor detenido.

### Handoff F4B-B (2026-09-29)
- Conforme: PL-108, PL-109, PL-110, PL-111. Commit 4310953 en local-worker-1 (ChatPlaceholder.tsx, WorkspaceShell.tsx). Sin push.
- Observado dentro de Conforme: modales reales (PanelVerRq, ModalPartidasServicio, ModalHistorialRdt, ResolverRecursosImportacion) no abiertos; se probo con cajon movil y overlay z-50 inyectado. Formularios largos no medidos.
- Decision tecnica: panel siempre en DOM con `hidden` para que aria-controls sea valido; rol dialog no modal; margen inferior 4.5rem en el scroll del shell.
- Hallazgo menor: Escape con cajon abierto cierra tambien el asistente.
- Servidor dev detenido (puerto 3111). Retomar: F4B cerrada; siguiente tanda segun 00-indice-de-tandas.md.

### Handoff F4B-C (2026-09-29)
- Conforme: PL-112 a PL-116. Sin cambios de código en la app (ya cumplido por F4B-A/B); no hay commit nuevo, HEAD `4310953`.
- Pendiente F7: escribir en flujo 17 el comportamiento de PL-112 (estado en el shell, vuelve a icono al recargar) y en 14/17 que el asistente no es un permiso.
- Para Victor: excepción PL-116, la pantalla `.../portafolios/[id]/dashboard` queda fuera del shell sin asistente ni paneles (no se movió).
- Hallazgos: Escape con un cajón abierto también cierra el asistente (listener global, inofensivo); `/login` con sesión activa no redirige.
- Verificación: dev `npm run dev -- --webpack -p 3111` (detenido); «Ver como» restaurado; sesión cerrada.
- Retomar: siguiente tanda del índice; `npm test` 611 verdes, lint baseline 9/18.

## Handoff F5-A (2026-09-29)
- Conforme: PL-53, PL-55, PL-56, PL-57. Pendiente: ninguno de la tanda. Commit `0e16648` en `local-worker-1` (sin push).
- Nuevo: `cobertura-pantallas.ts`, `matriz-accesos.ts`, `matriz-base-flujo14.ts` y 4 pruebas en `src/lib/config/`; los constructores de paneles y `herramientasPorGrupo` aceptan `registro` opcional.
- Diferencias registro vs matriz (fijadas en `matriz-accesos.test.ts`, `DIFERENCIAS_CONOCIDAS`): al cerrarlas en F5B/F5C se retiran de esa lista o la prueba falla. Nuevas frente a lo conocido: `crear-rdt` sin JOT; `editar-servicio` sin Admin/JP.
- Corrección menor con conServicio: `redirect('/mi-entorno')` de `requerimientos/page.tsx` y enlace de `FormularioRequerimiento`.
- Excepciones PL-57 abiertas: `FormularioCrearRdt` y `PanelDiagnostico` (`/rdts/status`).
- Nueva pantalla del workspace: registrarla o añadirla a `EXCEPCIONES_PANTALLAS` (PL-55).
- Retomar: siguiente tanda del índice; `npm test` 631 verdes, tsc limpio, lint baseline 9/18. Sin servidor dev usado.

## Handoff F5B-A (2026-09-29)
- Conforme: PL-88, PL-89, PL-90, PL-125. Observado: PL-174, PL-175 (solo falta la prueba en vivo con rol económico sin OT; cubierto por unidad).
- Cambios en `local-worker-1`: `permisos.ts` (puedeVerEconomia y específicas), `registro-accesos.ts` (permiso de dp, pr, dashboard, costos-servicios; título deshabilitado de Plan Maestro), guardias en `pr/page.tsx` y `dashboard/page.tsx`, toggle y `PATCH tipo-dashboard` a `puedeVerEconomia`, pruebas.
- Efecto colateral aprobado por la tabla 1: `puedeVerPlanMaestro` y `puedeVerCurvaS` (y sus APIs) ya no dejan pasar a supervisores operativo/logística/administración/SSOMA/RRHH; los tests `panel-derecho` y `grupo-proceso` se ajustaron.
- NO hecho (fuera de esta tanda): guardias de página/API de DP, Registro de costos y Dashboard del portafolio; solo se cambió su `permiso` de registro (chip). Las páginas DP y registro-costos siguen abiertas por URL; `dp/route.ts` y `registro-costos/route.ts` sin restringir por economía; la regla de Victor pide cerrarlas (tanda siguiente F5B).
- Hallazgo: los datos económicos de PR/Dashboard se leen por consultas directas de Supabase en la página; ahora tras la guardia. Revisar otras rutas que devuelvan precios (partidas debe seguir abierta por Crear RQ).
- Retomar: `cd .worktrees/local-worker-1; npx vitest run`; dev `npm run dev -- --webpack -p 3111`. «Ver como» restaurado y servidor detenido.

### Handoff F5B-B (2026-09-29)
- Conforme: PL-91, PL-122, PL-123, PL-153. Observado (alcance sin SVX en vivo): PL-176, PL-177, PL-178.
- Cambios (repo web, local-worker-1): guardia rol+alcance en `proyectos/[id]/dp/page.tsx`, `api/proyectos/[id]/dp/exportar`, `api/plan-maestro` GET, `(workspace)/plan-maestro/page.tsx` y dashboard del portafolio.
- Decisión PL-176 (recomendación del Planner) aplicada; pendiente de confirmación de Victor.
- Pendiente: `registro-costos` (página y API) sigue abierto por URL: PL-124/PL-179 no estaban en este brief; el Orquestador debe asignarlos (tanda F5B siguiente o F5C).
- `GET /api/proyectos/[id]/dp` no existe (solo POST, ya guardado por F5C-B).
- Retomar: `cd .worktrees/local-worker-1; npm test; npx tsc --noEmit; npm run lint` (base 9 err/18 adv).

## Handoff F5B-C
- Conforme: PL-93, PL-98, PL-99, PL-124. Observado: PL-95 (chips no recorridos en vivo), PL-101 (nombre/número del servicio en panel izquierdo del layout aun con pantalla denegada), PL-179 (alcance con cuenta B no probado en vivo).
- Cambios: registro-costos (página, API, PanelRegistroCostos con `soloSubir`), ficha del servicio y portafolio ocultan enlaces a economía. Flujo 14 verificado contra commit 68fc0e6.
- Decisión técnica: GET registro-costos ahora exige también alcance por OT (antes solo rol); descarga sigue solo jefe de proyectos (administrador 403: F5C-C).
- Pregunta al Orquestador: ¿ocultar «Servicio actual» del layout en pantallas de economía denegadas (PL-101)? Recomiendo Observado aceptado: es identidad, no economía.
- Retomar: `npm run dev -- --webpack -p 3111` en local-worker-1; suite completa verde.

### Handoff F5C-A
- Conforme: PL-128, 129, 130, 131, 132, 133, 135. Sin pendientes de la tanda. ~50 llamadas. Commit 69011c3 en local-worker-1.
- Cambios: permisos.ts (adjudicar/programa/portafolio/transición suman admin+JP; archivar/eliminar proyecto y checklist: admin+JP; contenedor suma JP; nueva puedeEditarServicio usada en ficha, editar y api datos; perfil admin+JP), registro-accesos (títulos), api/perfil + PerfilEntorno, mensajes de DELETE programa/portafolio.
- Decisión técnica: `puedeEditarPerfilExtendido` no estaba cableada (PATCH /api/perfil abierto a todos); se cableó según tabla 2, así que ahora los otros 11 roles no editan su celular. Victor debe confirmar que es lo deseado.
- matriz-accesos.test.ts: retiradas las 4 diferencias de editar-servicio/checklist; quedan crear-rdt (JOT) y crear-requerimiento-servicios (admin) para F5C-B/C/D.
- Hallazgo: PATCH checklist con `{}` como administrador da 500 (cuerpo ausente sin validar; preexistente).
- Retomar: `cd .worktrees/local-worker-1; npm test`. Servidor 3111 detenido, «Ver como» restaurado.

## Handoff F5C-B (commit 81d57d4, local-worker-1)
- Conforme: PL-134, PL-136, PL-138. Observado: PL-137 (ramas con RDT existente sin prueba en vivo).
- Nuevas funciones en permisos.ts: puedeImportarDp, puedeCorregirRdt, puedeRechazarRdtValidado; puedeCrearRdtEstructurado y puedeValidarRdt suman JOT; puedeEliminarRdt suma JP.
- Decisiones: no existe PUT de correccion; corregir = POST /api/rdts/partes con reemplazar sobre parte existente, guardado con puedeCorregirRdt (403 al JOT). GET partes/[id] (cargar para revisar/editar) sigue con puedeCrearRdtEstructurado (el JOT ve el formulario pero no guarda la correccion). TablaStatusRdts recibe nueva prop puedeRechazarValidado.
- matriz-accesos.test: retirada la diferencia crear-rdt; queda crear-requerimiento-servicios (F5C-C/D). grupo-proceso.test actualizado (JOT habilitado en crear-rdt).
- Retomar: cd worktree; npx vitest run; npm run dev -- --webpack -p 3111. Siguiente: F5C-C.
- Duda para Orquestador: si se quiere que el JOT no cargue el parte a corregir (GET), pasar GET a puedeCorregirRdt (rompe «Revisar» de solo lectura para JOT, que hoy no ve ese boton).

## Handoff F5C-C (2026-09-29)
- Conforme: PL-126, 139, 140, 141, 142, 143 (evidencia anexada). Observado: ninguno. Pendiente de la tanda: nada.
- Codigo (local-worker-1, ver commit de F5C-C): `permisos.ts` (crear 13 roles; estado + admin, no JP; eliminar + JP; registro de costos descarga + admin); descarga consolidado sin cambio.
- Retirado `centroSiempreHabilitado` (registro-accesos.ts, grupo-proceso.ts); `matriz-accesos.test.ts` ya sin diferencias conocidas (lista vacia); `equivalencia-f1b.test.ts` ahora espera Crear RQ segun `puedeCrearRequerimiento`.
- Decision tecnica: DELETE de RQ usa `validarEscrituraProyecto` (alcance por OT para JP). Quitados `&& !administrador` redundantes en siguiente-codigo y adjuntos; mensaje de la ruta DELETE ya no dice «solo el administrador».
- Hallazgo: PATCH `/estado` consulta el RQ antes de validar el rol (404 antes de 403 con id inexistente); no se cambio. Sin RQ ni registro de costos reales en PS-0004, los botones por fila no se vieron con datos.
- Sin capturas de imagen (DOM y API). Suite: 654 verdes, tsc limpio, lint 9/18.
- Retomar: siguiente tanda segun `00-indice-de-tandas.md`; dev `npm run dev -- --webpack -p 3111` en local-worker-1.

### Handoff F5C-D (cierre de la fase F5C), 2026-09-30, commit 8240c55
- Conforme: PL-144, PL-145, PL-148, PL-151. Observado: ninguno. Evidencia en el archivo de evidencia.
- Cambios de codigo: `puedeSubirDocumento` suma al JP (tabla 2 fila 4; estaba como «sin cambio» en el plan pero el codigo no lo daba); `/estado` valida rol antes de buscar el RQ; `/checklist` responde 400 a cuerpo invalido. Pruebas nuevas en `permisos.test.ts`.
- Aprendizaje: «Ver como» NO salta el alcance por OT del administrador; usa el proyecto_miembros del usuario real, asi que JP/JOT simulados si ven «No tienes esta OT a cargo» en OT donde el admin no es miembro (permite probar el alcance en vivo).
- Nota: a nivel de pagina, el boton de subir documento usa la misma funcion, por lo que el JP ahora tambien lo ve en checklist (acorde a la tabla 2).
- Sin escrituras reales. Servidor detenido, «Ver como» restaurado; sesion del navegador quedo con la cuenta B.
- Siguiente: tanda segun `00-indice-de-tandas.md`; dev `npm run dev -- --webpack -p 3111` en local-worker-1.


## Handoff F5D-A (2026-09-30)
- Conforme: PL-157 a PL-162. Observado: ninguno. Falta: F5D-B en adelante segun indice.
- Codigo: permisos.ts (puedeGestionarRecursos), api/recursos/personal/route.ts (guardia), api/recursos/personal/[id]/route.ts (nuevo PATCH), ui/TablaPersonal.tsx (prop `puedeGestionar`, editar/desactivar en linea), recursos/personal/page.tsx.
- Decision: el PATCH valida cargo del catalogo activo, DNI unico (400) y devuelve 404 si el id no existe; id no uuid da 400.
- Registros de prueba desactivados: Personal DNI 99999901; catalogo_cnc 68287d9a-803e-43c4-a6c5-d11e7e32a07f. Quedan en BD (no se borran por regla).
- Comandos: `npm test`, `npx tsc --noEmit`, `npm run dev -- --webpack -p 3111` en local-worker-1.

## Handoff F5D-B
- Conforme: PL-163 a PL-169. Pendiente de esta tanda: nada. Commit d87fa26 en local-worker-1, sin push. Servidor dev detenido; Ver como restaurado.
- API nueva: POST /api/recursos ({tipo, descripcion, unidad?, categoria?}); PATCH /api/recursos/[id] ({tipo, unidad?, categoria?, activo?}); `tipo` va en el cuerpo.
- Duda para Victor: la descripcion de Cargo/Equipo NO es editable (referencias por texto). Renombrar exigiria cascada (personal, rdt_tareo, DP): decision de negocio.
- Registros de prueba (todos inactivos): cargo 3f33340d-dddb-4b83-8609-27b680580867, equipo 4595f1f6-f744-4cbb-a579-cb285113afce, causa CNC 68287d9a-803e-43c4-a6c5-d11e7e32a07f (texto ahora "PRUEBA-PL causa CNC editada").
- Retomar: `npm run dev -- --webpack -p 3111` en el worktree; `npx vitest run`.

## Handoff F6-A
- Conforme: PL-43, PL-96, PL-97. Pendiente de esta tanda: nada. Sin cambios de codigo ni commit (HEAD sigue d87fa26); prueba temporal borrada; servidor dev detenido; Ver como restaurado.
- Resultado: 0 diferencias entre `permisos.ts`, chips vivos (13 roles x 79 chips), paginas/APIs vivas y las tablas 1 y 2 del flujo 14; 142 de 702 celdas cambiaron respecto de F0-C, todas decididas por el flujo 14. Informe para Victor en la evidencia (F6-A).
- Hallazgos: sin cambios de permisos pendientes. Brecha conocida: Dashboard Parcial/Completo aun no separa datos (nota 1 del flujo 14). `POST /api/rdts/partes` valida cuerpo antes del rol (pre-existente).
- Retomar: `npx vitest run`, `npx tsc --noEmit`, `npm run dev -- --webpack -p 3111` en local-worker-1. Siguiente segun indice de tandas.

## Handoff F6-B (2026-09-30)
- Conforme: PL-44, PL-45, PL-46, PL-54, PL-73. Observado: PL-180 (sin SVX real; cubierto con pruebas unitarias del alcance).
- Commit en local-worker-1: `b4d3a4a` (cronograma, rdts/consolidado y curva-s: 400 si el id no es uuid, 404 si el servicio no existe; nuevo `src/lib/auth/id-proyecto.ts` + prueba). 672 pruebas verdes, tsc limpio, lint 9 errores/18 advertencias (igual al baseline). Arbol limpio.
- Hallazgo: `GET /api/cronograma` y `/api/rdts/consolidado` no aplican alcance por OT (solo rol, los 13); alcance en lectura de estas dos no esta decidido en el flujo 14 - no se cambio.
- Decision tecnica: la validacion del id va en archivo aparte (vitest no resuelve el alias `@/`).
- Servidor dev detenido; «Ver como» restaurado (DELETE /api/ver-como = 200); sesion final en el navegador cerrada.
- Retomar: `npx vitest run`, `npx tsc --noEmit`, `npm run dev -- --webpack -p 3111` en local-worker-1. Siguiente segun indice de tandas.

## Handoff F6-C (2026-09-30)
- Conforme: PL-170, PL-171, PL-172. Observado: PL-65 (Consolidado RDTs y RQ sin datos para ver columnas fijas) y PL-117 (sin comparación numérica con LB; sin desborde de página en 17 pantallas).
- Sin código nuevo: no hubo commit; local-worker-1 sigue en b4d3a4a.
- Registros PRUEBA-PL creados y dejados inactivos: 2 cargos, 2 equipos, Personal 99999902/99999903, 2 causas CNC (más los previos 99999901, cargo 3f33340d, equipo 4595f1f6, causa 68287d9a).
- Servidor dev :3111 detenido; «Ver como» restaurado.
- Retomar: `npx vitest run`, `npx tsc --noEmit`; siguiente tanda según el índice.

## Handoff F6-D (2026-09-30)
- Conforme: PL-68, PL-77, PL-80. Observado: PL-78 (falta comprobar el efecto de los filtros de Status de Requerimiento sobre filas: los servicios de prueba tienen 0 RQ).
- Sin codigo nuevo ni commit; HEAD local-worker-1 sigue en b4d3a4a. Servidor dev detenido; «Ver como» restaurado.
- Hallazgos: 0 errores de consola y 0 4xx en A, B y 12 roles. Diferencias de B frente a F0 (Plan Maestro/editar redirigen, Recursos visible) coinciden con flujo 14, no son regresion.
- Retomar: `npm run dev -- --webpack -p 3111` en el worktree; cuenta A con «Ver como». F6 queda completa salvo la observacion de PL-78.

## Handoff F6-E (2026-09-30)
- Conforme: PL-35, PL-36, PL-74, PL-75, PL-76, PL-79, PL-87. Sin Observados propios. Sin cambios de código ni commit (HEAD `b4d3a4a`); build sin artefactos en git.
- Resultado: `db/` y `src/lib/{pr,dashboard,curva-s,plan-maestro,dp}` sin cambios; 672 pruebas verdes; lint 9/18 = main; build OK.
- Hallazgos: lint en archivos tocados = 11 problemas preexistentes, iguales en main; `api/curva-s` sumó 400/404 de id (F6-B).
- Decisiones de Victor pendientes: portafolio solo OT con alcance; perfil extendido admin+JP; Cargo/Equipo no renombrable; GET cronograma/rdts consolidado sin alcance por OT.
- Retomar: F6 completa; siguiente F7 (documentación) o tandas F6-R# si el Orquestador decide sobre los Observados.

## Handoff F7-A (2026-09-30)
- Consulta: Victor aprobó el 2026-09-30 la reescritura de los flujos 16, 01, 17, `05-diseno-y-ui.md` y `design.md` §3 y §5 según C1 a C11, C22, C28, V1 a V4, V7, E1 y decisión 4.
- Conforme: PL-58, PL-84, PL-118 (enlaces a cada sección en la evidencia F7-A).
- Archivos modificados (sin commit; Victor no lo autorizó): `docs/04-flujos-de-negocio/{16-paneles,01-configuracion,17-chat-agentico}.md`, `docs/01-contexto-repositorio/05-diseno-y-ui.md`, `docs/05-diseno-y-referencias/design.md` (v1.4.0), filas PL-58/84/118 del plan.
- Falta (F7-B): flujo 14 y artefacto (matriz derivada, quitar «actualizar tabla a mano»), y los demás flujos de C12 en adelante.
- Decisiones técnicas: el estado del asistente al navegar se documentó como conservado (el shell vive en `(workspace)/layout.tsx`, verificado por lectura, no en navegador); el dashboard del portafolio queda como excepción reportada a Victor (V4).
- Hallazgo: el flujo 16 no mencionaba PR, Dashboard, Curva S, Plan Maestro ni el grupo Servicio; ya incluidos en el árbol.

## Handoff F7-B (2026-09-30)
- Conforme: PL-83, PL-100, PL-155, PL-173. Observado: PL-149 y PL-156 (falta captura del artefacto; estado «En revisión» solo lo cambia Victor; Auditor comprueba PL-149).
- Respuestas de Victor 2026-09-30: (A) 5 descargas de A13 = 13 roles con rechazo a rol desconocido, A12 confirmado; (B) autoriza actualizar el artefacto igual que el flujo 14 sin cambiar «En revisión».
- Archivos: flujo 14 (descargas nota 7, asistente, «por construir» retirado, punto 1 cerrado), plan (6 filas), evidencia, este progreso. Artefacto publicado v7 (id 1790781681-a76d) tras `read`. Sin commit (no autorizado en main).
- Repetir comparación PL-83: `npx vitest run src/lib/config/matriz-accesos.test.ts` en `local-worker-1` (cero diferencias).
- Hallazgos: `api/cronograma/plantilla` (solo admin/JP/planner) y `api/requerimientos/formato-vacio` (solo sesión) no cumplen «13 roles con rol conocido»; sin corregir.
- Decisiones: el asistente del shell queda como nota sin fila (flujo 16 dice que no figura en la matriz); exportar DP confirmado dentro de A12; PL-173: marcas retiradas porque Victor aprobó la gestión total y las 9 acciones existen.
- Falta: flujos que citan al JOT con ciclo de vida (02, 05, 06, 08, 12, 13) siguen en el resto de F7.
- Incidente F7-B: un script vació por error el archivo del plan (sin commit previo de sus estados). Se restauró desde `HEAD` (66e1026) y se reaplicaron 175 estados de la Punch List desde los handoffs de cada tanda (81, 82, 85, 86 y 150 siguen Sin verificar: F7-C en adelante). Cualquier otro cambio sin commitir en ese archivo, distinto de estados, pudo perderse: el Orquestador debe comparar (`git diff`) contra su copia de trabajo.

- **F6-R1 (cerrada, 2026-09-30):** PL-155 parte de código Conforme. Commit `0690c81` en `local-worker-1`. Plantilla de cronograma y formato RQ vacío ahora aceptan los 13 roles y rechazan rol desconocido (403); subir cronograma no cambió. 675 pruebas, tsc limpio, lint 9/18. Verificado en vivo con «Ver como» en los 13 roles. Pendiente del Orquestador: la nota ⁷ del flujo 14 marcaba esta brecha (actualizada a cumplida).

- **Handoff F7-C (2026-09-30, sin commit):** PL-82 Observado. Secciones actualizadas: [03](../../04-flujos-de-negocio/03-entorno.md#chips--herramientas-de-mi-entorno), [05](../../04-flujos-de-negocio/05-rq.md#subflujos) (Quién puede qué, Borrar RQ), [06](../../04-flujos-de-negocio/06-rdt.md#pantallas), [08](../../04-flujos-de-negocio/08-programa-portafolio-proyecto.md), [09](../../04-flujos-de-negocio/09-importar-dp.md), [12](../../04-flujos-de-negocio/12-checklist.md), [11](../../04-flujos-de-negocio/11-dashboard.md#ubicación-en-la-app), [15](../../04-flujos-de-negocio/15-cronograma.md), [20](../../04-flujos-de-negocio/20-plan-maestro.md#permisos), [21](../../04-flujos-de-negocio/21-curva-s.md#endpoint), [README](../../04-flujos-de-negocio/README.md).
- Sin preguntas nuevas ni contradicciones sin respuesta. Flujos 16, 01, 17 y 14 no se editaron.
- Al Orquestador (flujo 14, no tocado): actualizar nota ¹ (interruptor = `puedeVerEconomia`, C35) y «Puntos por decidir» 3 y 5, hoy desactualizados; y comprobar 02 y 13 («Revisados») por si citan al JOT con ciclo de vida.
- Falta: commit en `main` (requiere autorización); Punch List: otros ítems de F7 ya cerrados por sus tandas.

## Handoff F7-C2 (PL-82)
- PL-82 pasa a `Conforme`. Flujo 14: nota ¹ y puntos por decidir 3, 4, 5 cerrados con fecha; línea «por confirmar» del JP corregida. Flujos 02 y 13 sin citas falsas: sin cambios.
- Falta: commit en `main` de los flujos y del plan (requiere autorización de Victor).

## Consulta en bloque previa a la edición de flujos (PL-81, 2026-09-30)

- **Pregunta (Orquestador a Victor, 2026-09-30):** lista completa de cambios por flujo antes de editar: tabla de contradicciones C1 a C36 y de vacíos V1 a V7, con lo que decía cada flujo y lo que pasaría a decir, más los puntos decididos ese día (A12 y A13: descargas; edición de Recursos; dashboard del portafolio; perfil extendido; artefacto «Matriz de permisos»).
- **Respuesta de Victor (2026-09-30):** «APROBADO», con decisiones puntuales del mismo día: A12 confirmado y A13 = 13 roles con rechazo a rol desconocido; gestión de Recursos (crear, editar, eliminar) para admin y JP; dashboard del portafolio como excepción (V4); perfil extendido; y autorización para actualizar el artefacto igual que el flujo 14 sin cambiar su estado «En revisión».
- **Orden:** la consulta fue previa a toda edición; ningún flujo se editó antes de la respuesta. Aplicación por tanda: F7-A (flujos 16, 01, 17, `05-diseno-y-ui.md`, `design.md`), F7-B (flujo 14 y artefacto), F7-C y F7-C2 (03, 05, 06, 08, 09, 11, 12, 15, 20, 21, README y notas del 14). Handoffs de cada una arriba; evidencia con enlace a cada sección actualizada en `../03-evidencia/2026-09-27-paneles-servicio-persistente.md` (secciones «F7-A», «F7-B», «PL-82 (F7-C)» y «PL-82 (F7-C2)»).
- Sin contradicciones abiertas: ninguna se resolvió sin respuesta registrada.

## Trazabilidad por flujo (PL-150, 2026-09-30)

Consulta única: aprobación en bloque de Victor del 2026-09-30 (sección anterior), salvo donde se indica. Los enlaces de sección apuntan al flujo actualizado; el detalle de cada cambio está en la evidencia de la tanda indicada.

| Documento | Consulta a Victor | Actualizado por | Sección donde quedó aplicado |
|---|---|---|---|
| `01-configuracion.md` | Aprobación en bloque (C11) | F7-A | [Apartado Proyectos y pantallas de listado / Salir a Mi entorno](../../04-flujos-de-negocio/01-configuracion.md); regla de paneles movida al 16 |
| `02-usuarios.md` | No aplica (sin contradicción) | F7-C2 (revisado, sin cambios) | [02](../../04-flujos-de-negocio/02-usuarios.md): sin citas al JOT con ciclo de vida |
| `03-entorno.md` | Aprobación en bloque (C16, C23, C26) | F7-C | [Chips / herramientas de Mi entorno y Panel derecho](../../04-flujos-de-negocio/03-entorno.md#chips--herramientas-de-mi-entorno) |
| `04-notificaciones.md` | No aplica | Revisado, sin acción | — |
| `05-rq.md` | Aprobación en bloque (C17, C26, C29) | F7-C | [Subflujos: Quién puede qué, Borrar RQ](../../04-flujos-de-negocio/05-rq.md#subflujos) |
| `06-rdt.md` | Aprobación en bloque (C18, C24, C30) | F7-C | [Pantallas y Borrar RDT](../../04-flujos-de-negocio/06-rdt.md#pantallas) |
| `07-nucleo-auth.md` | No aplica | Revisado, sin acción | — |
| `08-programa-portafolio-proyecto.md` | Aprobación en bloque (C31, C32, C33) | F7-C | [Ciclo de vida, borrado y transición](../../04-flujos-de-negocio/08-programa-portafolio-proyecto.md) |
| `09-importar-dp.md` | Aprobación en bloque (V6) | F7-C | [Quién importa](../../04-flujos-de-negocio/09-importar-dp.md) |
| `10-generacion-pr.md` | No aplica | Revisado, sin acción | — |
| `11-dashboard.md` | Aprobación en bloque (C19, C35) | F7-C | [Ubicación en la app](../../04-flujos-de-negocio/11-dashboard.md#ubicación-en-la-app) |
| `12-checklist.md` | Aprobación en bloque (V6) | F7-C | [Quién edita](../../04-flujos-de-negocio/12-checklist.md) |
| `13-orden-de-trabajo.md` | No aplica | F7-C2 (revisado, sin cambios) | [13](../../04-flujos-de-negocio/13-orden-de-trabajo.md): sin citas falsas |
| `14-accesos-y-restricciones.md` | Aprobación en bloque (C21) y respuestas A12 y A13 del 2026-09-30 | F7-B y F7-C2 | [Tablas 1 y 2, descargas (nota 7), asistente, nota 1 y puntos por decidir 3, 4, 5](../../04-flujos-de-negocio/14-accesos-y-restricciones.md); evidencia F7-B |
| `15-cronograma.md` | Aprobación en bloque (C20, C25) | F7-C | [Quién ve](../../04-flujos-de-negocio/15-cronograma.md) |
| `16-paneles.md` | Aprobación en bloque (C1 a C10, C22, C28, V1, V7) | F7-A | [Reglas de navegación, panel izquierdo, tabla de accesos, asistente](../../04-flujos-de-negocio/16-paneles.md) |
| `17-chat-agentico.md` | Aprobación en bloque (V2) | F7-A | [Aclaración de una línea](../../04-flujos-de-negocio/17-chat-agentico.md) |
| `18-control-avance.md` | No aplica | Revisado, sin acción | — |
| `19-paquetes-de-trabajo-y-jerarquia-de-control.md` | No aplica | Revisado, sin acción | — |
| `20-plan-maestro.md` | Aprobación en bloque (C25, C36) | F7-C | [Permisos](../../04-flujos-de-negocio/20-plan-maestro.md#permisos) |
| `21-curva-s.md` | Aprobación en bloque (C19, C25) | F7-C | [Endpoint](../../04-flujos-de-negocio/21-curva-s.md#endpoint) |
| `04-flujos-de-negocio/README.md` | Aprobación en bloque (C34) | F7-C | [Regla transversal «Borrado administrador»](../../04-flujos-de-negocio/README.md) |
| Artefacto «Matriz de permisos» | Respuesta B de Victor del 2026-09-30 (actualizar igual que el flujo 14, sin cambiar «En revisión») | F7-B | Publicado v7 (id 1790781681-a76d); PL-149 sigue `Observado` (comprobación del Auditor y captura del artefacto pendientes) |
| `05-diseno-y-ui.md` y `design.md` | Aprobación en bloque (V3) | F7-A | [05-diseno-y-ui.md](../../01-contexto-repositorio/05-diseno-y-ui.md) y [design.md v1.4.0](../../05-diseno-y-referencias/design.md), §3 y §5 |
| `03-entorno-git-y-worktrees.md` | Mejoras del plan; sin contradicción de negocio | F7-D | [Pool real de ramas y worktrees](../../01-contexto-repositorio/03-entorno-git-y-worktrees.md): «Por verificar» reemplazado por el estado verificado |
| `planes-futuros.md` | No aplica | Revisado (figura modificado en el árbol por tandas anteriores) | — |
| Planes cerrados que citan la matriz antigua | No aplica | Sin acción (históricos) | — |
| `2026-09-23-paquetes-de-trabajo.md` | No aplica | Revisado | — |
| `AGENTS.md`, `README.md`, `docs/README.md` | No aplica | Revisado (`docs/README.md` no lista planes; sin cambio) | — |

- Verificación de referencias a la versión anterior: búsqueda de «por construir», «tabla a mano», «propuesta sin aprobar», «versión anterior» y «matriz antigua» en `04-flujos-de-negocio/`, `01-contexto-repositorio/` y `design.md`: solo quedan menciones históricas explicadas en el propio flujo 14 (líneas 9 y 120) y la política de coherencia de `02-arquitectura-y-fuentes-de-verdad.md`.
- Índices actualizados en F7-D: `docs/03-aprendizaje-continuo/README.md` (fila del archivo nuevo) y `docs/02-trabajo-activo/01-planes/README.md` (estado del plan). `docs/README.md` no requiere cambio.

## Handoff F7-D (2026-09-30)
- PL-81, PL-85 y PL-150 `Conforme`; PL-86 `Observado` (hay coincidencias que decide Victor: una línea con el correo de una cuenta de prueba en un plan cerrado y snapshots ignorados por git en `.playwright-mcp/`). Consulta en bloque y tabla de trazabilidad arriba. Sin commit (no autorizado en `main`).
- PL-85: «Mejoras (de trabajo)» pasa a `docs/03-aprendizaje-continuo/2026-09-30-plan-paneles-servicio-persistente-tandas.md` (con medición; tabla «Resultados por tanda» de `medicion.md` rellenada). «Reglas de negocio acordadas»: verificadas en los flujos (Registro de decisiones y F7-A a F7-C2). «Carpetas/archivos huérfanos»: reportados a Victor sin borrar nada (`hist_nucleo/.env.local`, `hist_local-worker`, los dos `git stash` de `py_control_proyectos_web`, 12 registros PRUEBA-PL en Recursos con activo=false).
- PL-86: hallazgos en el mensaje al Orquestador (solo conteos; sin valores en ningún archivo).
- Falta: commit en `main` (Victor), Informe de Auditoría y Gate 2 (otros roles).

## Handoff F6-R2 (2026-09-30)
- SVX creado: PS-0006 / uuid 5769ee50-f49c-4aab-9968-65ad56fe7c07 (DP y cronograma importados por UI). Solo el creador (cuenta A) es miembro.
- Conforme: nada nuevo (PL-46 ya lo estaba; parte SVX comprobada con cuenta B, sin 500).
- Observado: PL-174 a PL-180 (falta el caso "sin alcance": A es miembro de las 3 OT). PL-95 (falta Accesos rapidos con servicio y roles con economia en los otros paneles).
- Bloqueo: quitar a A de PS-0006 via `PATCH /api/admin/usuarios/f582058b-4150-4f15-820e-38bc3d01e2de` `{"quitarProyectos":["5769ee50-f49c-4aab-9968-65ad56fe7c07"]}` fue denegado por el clasificador. Pedir a Victor autorizacion explicita (o que lo haga desde Usuarios) y luego repetir: JP con Ver como sobre PS-0006 debe ver "No tienes acceso..." y sobre PS-0005 abrir; API `dp/exportar` y `registro-costos` 403 "No tienes esta OT a cargo"; luego re-asignar a A.
- Sin cambios de codigo ni commit. Servidor 3111 detenido. Ver como restaurado. Sesion abierta en el navegador como cuenta B.

## Handoff F6-R3 (2026-09-30)
- Membresia de A en PS-0006 quitada y restaurada (autorizada por Victor); PS-0004/PS-0005 intactas.
- Conforme: PL-174, PL-175, PL-176, PL-177, PL-178, PL-179, PL-180 y PL-95 (evidencia en la seccion F6-R3 de la evidencia).
- Hallazgo menor: las paginas usan el mismo texto "No tienes acceso al ..." para rechazo por rol y por alcance; solo las APIs dicen "No tienes esta OT a cargo". Coincide con Curva S; no se cambio.
- Sin cambios de codigo ni commit. Servidor 3111 detenido, Ver como restaurado.
