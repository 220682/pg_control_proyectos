# Resumen de cierre — T7B (bandeja, servicio, RDT, checklist y móvil)

## Tanda, rol y modelo

T7B · Worker de verificación con navegador (Playwright) · Sonnet · esfuerzo medio. Ítems T7-03 a T7-06, más los tres hallazgos menores de T7A (a, b, c). Fecha de la prueba: 2026-10-18.

Capturas: `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/t7/` (27 PNG con prefijo `t7b-`; las de escritorio a 1440 px, las `t7b-06-*` a 390 px).

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| T7-03 | **Conforme** (con 2 observaciones menores, ver hallazgos T7B-H2 y T7B-H5) | Servicio `PS-0005` «PRUEBA T7» creado por el administrador con el supervisor operativo (jeyger) a cargo. Vía 1 (crear): jeyger recibe «Se te asignó el servicio PS-0005 — PRUEBA T7» (`t7b-03-p1`); el administrador no recibe aviso propio. Vía 2 (datos del servicio, jeyger → Logística 1): jeyger recibe «Ya no tienes a cargo…» y su «Se te asignó» queda Atendido (`p2`); Logística 1 recibe «Se te asignó…» (`p3`). Vía 3 (Usuarios): quitar PS-0000 a Logística 1 (con rol supervisor operativo) genera «Ya no tienes a cargo…» y volver a agregarlo «Se te asignó…» (`p9`); asignar PS-0005 a Logística 2 (sin rol supervisor operativo) no genera ningún aviso. RDT registrado por jeyger: el administrador y quien tiene los roles de jefatura reciben «RDT registrado para validar» (`p4`). RDT validado (17-10) y RDT rechazado con motivo (14-10): jeyger recibe «Tu RDT del 17-10-2026 … fue validado.» y «… fue rechazado: PRUEBA T7: faltan las horas de la noche»; los avisos «para validar» del administrador pasan a Atendido (`p5`). Comentario de Logística 1 sobre el RQ `PS-0000-LL-SO-003` (desde el Consolidado RQ): llegan el administrador (`p4`) y el solicitante jeyger (`p5`). | — |
| T7-04 | **Conforme** | Un aviso sin servicio muestra la insignia «Entorno» y uno de servicio muestra su N° OT (`t7b-04-p4`, `p5`). Grupo «Jefatura» presente en el filtro «Todos los grupos» y en las tarjetas (`p6`). Filtro «Tipo de aviso» = Servicio deja solo los 3 avisos de servicio/checklist (`p1`). Filtro «Solo Entorno (sin servicio)» muestra solo avisos sin servicio (`p2`, `p4`) y vacío cuando no hay ninguno. «Enviar mensaje» (Mi entorno) arranca en «Entorno (sin servicio)» (`p3`); el mensaje enviado así llega como Entorno. | — |
| T7-05 | **Conforme** (con la observación T7B-H3) | **Subir cierra el aviso y la campana baja:** el ítem «PRUEBA T7 plano de campo» (por usuario, Logística 1) genera «OT PS-0005: falta subir…»; Logística 1 sube un archivo y el aviso queda Atendido; la campana pasa de 3 a 2 tras recargar (`t7b-05-p4`, `p5`, `p6`). **Aviso por rol cerrado para ambas personas:** el aviso «Servicio PS-0005: falta subir "Requerimientos del servicio"» (cola del rol supervisor operativo) estaba Pendiente para jeyger y Logística 1 (con rol supervisor operativo temporal); al reasignar el documento a un usuario concreto quedó Atendido para las dos personas. **Aviso por usuario solo de una:** el aviso de ese mismo documento reasignado a jeyger llegó solo a jeyger; Logística 1 no lo tiene. **Informativo se cierra al abrirlo:** «Ya no tienes a cargo…» pasa de Pendiente a Atendido al abrirlo (`t7b-05-p1`). **Dos roles, una tarjeta:** Logística 2 (con jefe de proyectos y jefe de oficina técnica temporales) recibe un solo aviso «RDT registrado para validar» con dos filas internas; al abrirlo ambas pasan a Revisado (`t7b-05-p2`, `p3`). | — |
| T7-06 | **Conforme** (con la observación T7B-H4) | A 390 px la bandeja, el aviso de RQ abierto, el flujo «Devolver» con motivo, el aviso de devolución cerrado y el panel «Corregir y reenviar» se ven sin desborde horizontal de la página (scrollWidth = clientWidth = 390 en cada paso) (`t7b-06-p1` a `p6`). Registro de consola de toda la sesión: 0 errores de la app (el único `[ERROR]` es un 404 de una consulta propia a una ruta que no existe, hecha para mirar el catálogo). | — |

## Los tres hallazgos de T7A

| ID | Resultado | Evidencia |
|---|---|---|
| (a) «Confirmar devolución» con motivo vacío | **Conforme**: el botón está habilitado, al pulsarlo aparece «Escribe el motivo» y no se envía ninguna petición PATCH. | `t7b-03-p6` |
| (b) Cantidad vieja tras reenviar | **Observado, confirmado**: el solicitante corrige grava de 4 a 6 y reenvía; el panel «Lo solicitado» de su tarjeta abierta sigue mostrando «4 m3» hasta recargar. El aviso del administrador ya muestra «6 m3». | `t7b-03-p7`, `p8`; comparar con `t7b-06-p2` |
| (c) Grupo «pendiente de aprobación» del administrador | **Observado (sin decisión de negocio)**: el aviso se guarda una fila por rol: administrador y jefe de proyectos → «Jefatura»; jefe de oficina técnica → «Oficina Técnica». La bandeja junta las filas en una sola tarjeta y muestra el grupo de la fila que toma como representante, que varía: el mismo tipo de aviso aparece como «Oficina Técnica» en unas tarjetas y «Jefatura» en otras (administrador: RDT del 14-10 «Oficina Técnica», RDT del 17-10 «Jefatura»; con el filtro de grupo «Jefatura» el mismo RQ aparece como «Jefatura»). Para Logística 2 (jefe de proyectos + jefe de oficina técnica) pasa igual. Los demás roles ven su propio grupo: supervisor operativo → «Supervisión operativa»; supervisor de logística → «Logística»; mensajes y avisos «de persona» llevan el grupo de quien envía (indicado). Las cuentas de jefe de proyectos y de oficina técnica reales no se usaron (las de prueba no existen). | `t7b-03-p4`, `t7b-04-p5`, `t7b-04-p6`, `t7b-05-p2` |

## Hallazgos nuevos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| T7B-H1 | pregunta de negocio / datos | El único documento marcado al crear el servicio («Requerimientos del servicio») es de tipo pantalla (no admite subir archivo). Su aviso «falta subir» va a la cola de TODO el rol supervisor operativo, o sea también a Victor Vazquez (supervisor operativo real). Quedó con un aviso pendiente de «Servicio PS-0005: falta subir…» (ya cerrado después por reasignación del documento: ver T7-05; el aviso ya cerrado no le molesta, pero llegó a su cola). | Orquestador: avisar a Victor Vazquez o limpiar en T7-07 |
| T7B-H2 | observación menor (UI) | El formulario «Adjudicar servicio» muestra «N° OT PS-0001» (correlativo automático), pero el servidor creó `PS-0005` (calcula el siguiente con todos los servicios). No es un fallo del servidor; el rótulo del formulario no coincide. | Orquestador decide si se corrige la vista previa del N° OT |
| T7B-H3 | observación menor (UI) | La campana no baja en la misma pantalla al subir un archivo del checklist: mostró 3 justo después de subir y 2 solo tras recargar. El aviso sí quedó Atendido. | Orquestador decide |
| T7B-H4 | observación menor (UI móvil) | En el panel «Corregir y reenviar» a 390 px, la tabla de ítems tiene scroll horizontal interno: unidad y cantidad quedan fuera de la vista hasta desplazar. La página no desborda. | Orquestador decide (la regla de interfaz permite scroll horizontal en tablas) |
| T7B-H5 | observación menor (copia/comportamiento) | «Editar checklist» exige «asigne un responsable» para cada documento tildado, aunque el ya existente se creó con responsable por rol; para guardar hubo que asignarle un usuario (con lo cual se cerró su aviso por rol y se creó uno por usuario con el texto «OT PS-0005: falta subir "Requerimientos del servicio"», aunque ese documento no se sube, se completa en pantalla). | Orquestador / Victor |
| T7B-H6 | observación menor (UI) | Al cambiar rápido dos filtros de la bandeja (tipo de aviso y luego «Solo Entorno»), la lista mostró un momento los resultados del filtro anterior (posible respuesta atrasada que pisa a la nueva). Se reprodujo una vez, con cambios en menos de un segundo; con una pausa funcionó bien. | Orquestador decide si se investiga |
| T7B-H7 | informe de proceso | Servicio «PRUEBA T7» consumió el número real `PS-0005` en el portafolio «Servicios Marcobre» (los servicios reales son PS-0001 a PS-0004): mientras exista, el próximo servicio real saldrá como PS-0006. El servicio se puede «Eliminar proyecto» desde su página (lo decide Victor en T7-07). | Orquestador con Victor (T7-07) |

## Rama, commits y archivos tocados

Rama `local-worker-7` (verificada con `git branch --show-current`), último commit `85626fd`. Sin commits ni cambios al código ni al `.env.local`. Solo se crearon las capturas, este resumen y el archivo de prueba `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\.playwright-mcp\PRUEBA-T7-plano.txt` (el que se subió al checklist de PS-0005). Servidor `npm run dev -- --webpack -p 3107` levantado y cerrado al terminar (puerto 3107 sin escucha).

## Datos de prueba que quedan (para T7-07)

- Servicio `PS-0005` «PRUEBA T7» (en planeación, N° OC/OS `PRUEBA-T7`, responsable jeyger, checklist con «Requerimientos del servicio» reasignado a jeyger y «PRUEBA T7 plano de campo» con el archivo `PRUEBA-T7-plano.txt`). Logística 2 y Logística 1 ya no están asignadas a PS-0005; jeyger sí.
- En PS-0000: RDT del 17-10 (Validado) y del 14-10 (Rechazado) de jeyger, con 8 h de una persona real del personal; RQ `PS-0000-LL-SO-003` en Solicitado (2 ítems, cantidad de grava 6), RQ `-002` Atendido, y sus avisos; mensaje «PRUEBA T7 mensaje de Entorno (sin servicio)» a la bandeja del administrador (Entorno); comentarios y avisos de prueba.
- El RDT validado del 17-10 es de la actividad 1.1.4 (sin metrado ejecutado) del Plan Maestro de PS-0000: puede alterar mínimamente el acumulado de ese servicio de prueba.
- **Cambios temporales en cuentas, ya revertidos:** Logística 1 recibió y perdió el rol supervisor operativo; Logística 2 recibió y perdió los roles jefe de proyectos y jefe de oficina técnica. Se verificó en Usuarios que ambas quedaron solo con «Supervisor de Logística» y con la única OT PS-0000. Logística 1 perdió y recuperó su asignación a PS-0000 (generó los avisos «Ya no tienes…» y «Se te asignó…» de la vía 3).

## Cuentas usadas

Administrador, supervisor operativo (jeyger), Logística 1 y 2 (las dos con roles temporales). No existen las cuentas de jefe de proyectos ni oficina técnica. Antes de cada paso se cambió de cuenta cerrando sesión; las claves se escribieron solo en el formulario de ingreso.

## Snapshots y archivos de `.playwright-mcp/` nuevos

Sin claves (el ingreso se hizo con `fill` sin tomar snapshot con la clave escrita). Snapshots nuevos: `page-2026-10-18T20-15-21-923Z.yml` (pantalla de ingreso, antes de escribir), `…20-16-34-053Z.yml`, `…20-19-48-080Z.yml`, `…20-21-17-370Z.yml`, `…20-22-59-453Z.yml`, `…20-26-33-647Z.yml`, `…20-27-28-294Z.yml`. También hay `page-2026-10-18T20-*.png` (capturas de apoyo sin valor de evidencia) y logs `console-2026-10-18T20-1*.log` a `…20-26-29-655Z.log`, además del archivo de prueba `PRUEBA-T7-plano.txt`. No se borró nada.

## Llamadas y contexto

Unas 125 llamadas (muy por encima de la meta de 80, porque el brief pedía crear servicio, RDT, roles temporales y ocho recorridos con cuentas distintas; casi todas agrupaban varios pasos en un `run_code`).

## Skills revisados

Ninguno aplica (verificación con Playwright siguiendo el brief; `verificar-permisos-por-rol` no se usó porque se entró con las cuentas reales de cada rol).

## Fuentes de verdad revisadas

Catálogo `src/lib/notificaciones/catalogo.ts` del worktree (manda sobre el flujo 04, que aún tiene texto viejo), `avisos-servicio.ts`, `avisos-duplicados.ts` y `grupo-proceso.ts`. No se editó ninguna fuente.
