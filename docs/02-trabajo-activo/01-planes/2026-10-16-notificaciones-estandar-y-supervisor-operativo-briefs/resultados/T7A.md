# Resumen de cierre — T7A (ciclo del RQ)

## Tanda, rol y modelo

T7A · Worker de verificación con navegador (Playwright) · Sonnet · esfuerzo medio. Ítems T7-01 y T7-02. Fecha de la prueba: 2026-10-18.

Capturas: `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/t7/` (27 PNG a 1440 px, prefijos `t7-01-…` y `t7-02-…`).

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| T7-01 | **Conforme** | RQ `PS-0000-LL-SO-002` «PRUEBA T7 cemento» (PS-0000). 1) Supervisor operativo (jeyger22) lo crea: no recibe aviso propio (`p1-supop-bandeja-sin-aviso`). 2) Administrador recibe un solo aviso «pendiente de aprobación» (grupo mostrado: Oficina Técnica), lo abre (Revisado), pulsa Aprobado: el aviso pasa a Atendido y el RQ a «Enviado a Logística» (`p2-*`). 3) Logística 1 y Logística 2 reciben el aviso «aprobado» de la cola por rol (Pendiente) (`p3-log1/log2-recibe-aprobado-pendiente`). Logística 1 lo abre: RQ pasa solo a **Recepcionado** y el aviso queda Atendido (`p3-log1-abre-aviso-recepcionado`). 4) Logística 1 pulsa «En almacen»; Logística 2 ve el mismo aviso ya cerrado (Atendido) (`p4-log2-aviso-cerrado`); el solicitante tiene «aprobado» y «recepcionado» ya cerrados y «está en almacén» pendiente (`p4-supop-avisos-solicitante`). 5) Logística 1 pulsa «Atendido»: RQ Atendido; el solicitante tiene «está en almacén» cerrado y «ha sido atendido por PRUEBA Logística 1» pendiente (`p5-*`). Cada aviso llegó a quien dice el catálogo y el anterior se cerró. | — |
| T7-02 | **Conforme** | RQ `PS-0000-LL-SO-003` «PRUEBA T7 devolución» (2 ítems). Administrador abre su aviso y pulsa Devolver: aparece textarea de motivo y «Confirmar devolución»; confirma con motivo (`t7-02-p1-*`). El aviso «pendiente de aprobación» del administrador queda Atendido. Con el RQ en Devuelto: el botón «Aprobado» queda deshabilitado con el texto «Un RQ Devuelto no se puede aprobar…» y el servidor responde **409** («El requerimiento está devuelto…») a `derivar-logistica` (`p2-admin-aprobado-deshabilitado-409`). El solicitante recibe el aviso «Requerimiento … devuelto por Victor Perez Contreras: <motivo>» y, al abrirlo, ve el cuadro «Motivo de la devolución» y «Corregir y reenviar» (`p3-*`, `p4-supop-corregir-panel`): puede cambiar datos (cantidad, observaciones, fecha, prioridad, área) pero no agregar ni quitar ítems. Corrige grava 2→4 con observación y pulsa Reenviar: aviso de devolución Atendido, RQ Solicitado, mensaje «Se avisó otra vez a quienes aprueban» (`p4-supop-reenviado`). El administrador recibe un aviso nuevo «pendiente de aprobación» (Pendiente) con Aprobado y Devolver habilitados (`p5-admin-*`). Logística 1 y el supervisor operativo (no aprueban) ven el panel «Ver» del RQ sin Devolver ni Aprobar, con la cantidad corregida (4) y los 2 ítems (`p6-*`); el servidor responde **403** («No autorizado») al intentar `devolver` con el supervisor operativo. | — |

## Rama, commits y archivos tocados

Rama `local-worker-7` (verificada con `git branch --show-current`), último commit `85626fd`. Sin commits ni cambios al código. Solo se crearon las capturas y este resumen. Servidor `npm run dev -- --webpack -p 3107` levantado y cerrado al terminar (puerto 3107 sin escucha).

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| T7A-H1 | observación menor (UI) | Tras reenviar, el aviso del solicitante abierto sigue mostrando «Lo solicitado» con la cantidad vieja (grava 2 m3) hasta recargar; el panel «Ver» de otros roles y el aviso del administrador ya muestran 4. Es datos viejos en una tarjeta ya cargada, no un fallo de datos. | Orquestador decide si se corrige (refrescar los ítems tras reenviar) |
| T7A-H2 | pregunta de negocio / posible corrección | Los avisos por rol que van a administrador, jefe de proyectos y jefe de oficina técnica («pendiente de aprobación», RQ) se rotulan con el grupo «Oficina Técnica» para el administrador. El catálogo declara grupo `segun_rol`; no es un error del catálogo, pero confirmar si es el grupo deseado para esa cola compartida. | Orquestador / Victor |
| T7A-H3 | observación menor (UI) | «Confirmar devolución» está habilitado con el motivo vacío (el texto dice «obligatorio»); no se probó pulsarlo vacío, así que no se sabe si valida al pulsar. | Pasarlo a T7B/T7C o revisar en código |
| T7A-H4 | observación menor | Para pulsar «Atendido» en el aviso de Logística hay que abrir el aviso; una primera tentativa con selector ambiguo no hizo nada (error del Worker, no de la app). | ninguno |

## Traspaso

- Quedan sin limpiar en `PS-0000` (los decide el Orquestador con Victor, T7-07): RQ `PS-0000-LL-SO-002` (Atendido), RQ `PS-0000-LL-SO-003` (Solicitado, con su aviso pendiente para el administrador; ya reenviado) y sus avisos.
- Cuentas usadas: administrador, supervisor operativo (jeyger22), Logística 1 y 2. No se usaron las de jefe de proyectos ni oficina técnica (no creadas).
- `read_console_messages` por errores: solo 2, ambas las llamadas de rechazo intencionales (409 y 403). Sin errores de la app.
- Snapshots nuevos de `.playwright-mcp/` (todos sin claves; el de ingreso se tomó antes de escribir nada): `page-2026-10-18T20-04-27-099Z.yml`, `…20-04-52-863Z`, `…20-05-13-555Z`, `…20-05-38-832Z`, `…20-05-53-130Z`, `…20-06-20-473Z`, `…20-06-57-191Z`, `…20-07-16-367Z`, `…20-07-51-781Z`, `…20-08-08-728Z`, `…20-09-18-115Z`, `…20-10-59-904Z` (todos `.yml`). También hay logs `console-2026-10-18T20-0*.log`.

## Llamadas y contexto

Unas 50 llamadas (muchas agrupando varios pasos en un `run_code`).

## Skills revisados

Ninguno aplica (verificación con Playwright siguiendo el brief; `verificar-permisos-por-rol` no se usó porque se entró con las cuentas reales de cada rol).

## Fuentes de verdad revisadas

Catálogo `src/lib/notificaciones/catalogo.ts` del worktree (manda sobre el flujo 04, que aún tiene texto viejo). No se editó ninguna fuente.
