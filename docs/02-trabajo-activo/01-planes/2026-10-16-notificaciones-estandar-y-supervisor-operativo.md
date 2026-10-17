# Notificaciones: estándar de avisos y apoyo al supervisor operativo

## Identificación y estado

- Tema: ordenar el sistema de notificaciones bajo un estándar único (qué evento avisa, a quién, con qué texto, cuándo se cierra) y cerrar los huecos que hoy dejan al supervisor operativo sin saber qué pasó con su servicio, su RQ o su RDT. Prepara el terreno para capacitar a los supervisores operativos en el uso de la app.
- Fecha de inicio: 2026-10-16.
- Estado: `Spec aprobado` (Gate Spec, Victor, 2026-10-16) — pendientes P1, P2, P3 y P5 por consultar una a una antes de delegar al Planner. No hay Planner, Workers, ramas ni migraciones todavía.

Puertas:

- Gate Spec: `aprobado` (Victor, 2026-10-16)
- Gate 1: `pendiente`
- Gate 2: `pendiente`

## Spec

### Estado

`Propuesto` (2026-10-16). Redactado por el Orquestador con lo pedido por Victor y lo verificado en el código y en la bandeja en vivo.

### Problema y contexto

Victor tiene la app casi lista y quiere que los supervisores operativos aprendan a usarla. Antes quiere que las notificaciones les sirvan: **avisar algo que pasó** (se les adjudicó un servicio, cambió el estado de su RQ, se validó o rechazó su RDT), no funcionar como chat. Hoy el flujo 04 tiene 11 líneas y no describe cuándo se avisa, a quién ni cómo se cierra un aviso.

Victor pidió: documentar el flujo de notificaciones del RQ (creación → aprobación de gerencia → Logística recibe → estados → almacén → atendido), verificarlo en el servicio de pruebas, mejorarlo si se puede, mantener un mismo estándar a medida que se avanza, y centrarse en lo que hace el supervisor operativo (crear RQ, subir o crear RDT, informes) y en darle comodidad y monitoreo.

**Qué se verificó y cómo (Orquestador, 2026-10-16).** Lectura del código de la app (`py_control_proyectos_web`, `main` en `628918a`) y de la bandeja de Victor en producción, en solo lectura. No se escribió nada en la app. **No se verificó** el ciclo del RQ de punta a punta en vivo ni la bandeja de un supervisor operativo: el «Ver como» solo cambia la pantalla y la bandeja sigue siendo la del usuario real (se comprobó: la campana seguía en 18).

| # | Hallazgo | Evidencia |
|---|---|---|
| H1 | **El «0000».** Un mensaje enviado desde fuera de un servicio se guarda en el primer servicio de la lista, que es `PS-0000` («SERVICIO PRUEBA MARCOBRE 2026-10-07-19-33»). La base exige un servicio en cada aviso, así que «sin servicio / Entorno» no existe. | `EntornoTrabajoGrupo.tsx` (si no hay servicio, preselecciona `lista[0]`); `api/proyectos/vigentes` ordena por número; `db/001_esquema.sql` (`proyecto_id uuid not null`); lista de OT en vivo |
| H2 | **El grupo «Jefatura» no aparece.** El área JF se llama «Jefatura» en Usuarios y en el RQ, pero el filtro de notificaciones usa una lista fija de 8 grupos con «Proyecto». El «grupo» de un aviso es el del rol destinatario, no un grupo de personas. | `grupo-proceso.ts` (`GRUPOS_PROCESO`, `MAPA_ROL_GRUPO`); `area-usuario.ts` (JF → «Jefatura»); flujo 02; filtro en vivo |
| H3 | **Asignar un servicio a un supervisor no lo avisa.** Ninguna de las tres vías crea un aviso: al crear la OT con supervisor operativo, al cambiar el responsable en los datos del servicio y al asignar OT desde Usuarios. Lo único que recibe son los avisos de documentos del checklist, si es responsable de alguno. | `api/proyectos/route.ts`; `api/proyectos/[id]/datos/route.ts`; `api/admin/usuarios/[id]/route.ts` |
| H4 | **Recepcionado.** Abrir el aviso solo lo pasa a «Revisado». «Recepcionado» es un botón aparte, en el aviso y en el consolidado. | `api/notificaciones/[id]/revisar`; `AccionesRqEnNotificacion.tsx`; `TablaConsolidadoRq.tsx`; `acciones-estado.ts` |
| H5 | **RDT validado o rechazado: no avisa al autor.** El supervisor operativo no se entera, y es quien corrige un RDT rechazado. El único aviso en la validación es el de recursos sin tarifa, a administrador y jefe de proyectos. | `api/rdts/partes/[id]/route.ts`; `acumulacion-rdt.ts`; flujo 06 («Notificación al subir: solo Administración») |
| H6 | **Huecos del RQ.** El comentario de Logística avisa a jefes y administrador, no al solicitante. El cambio de estado por la vía genérica (sin `accion`) no cierra avisos ni avisa al solicitante. No existe estado de rechazo. | `comentarios/route.ts`; `requerimientos/[rqId]/estado/route.ts`; `tipos.ts` |
| H7 | **Ruido en la bandeja.** Los avisos «falta subir…» no se cierran al subir el documento (solo se cierran a mano o los del RQ). Algunos textos llevan el N° de OT y otros no. Bandeja de Victor: 18 pendientes, casi todos de pruebas viejas. | `checklist/route.ts` («Servicio: falta subir…» sin N° OT) frente a `proyectos/route.ts` («Servicio PS-0001: falta subir…»); búsqueda de escrituras de `ATENDIDO` en la API |
| H8 | **Avisos por rol: una sola fila compartida.** Con dos personas en el rol, el estado que cambia una cambia para ambas. | `notificaciones.ts` (`destinatario_rol_id`); `api-helpers.ts` |
| H9 | **El flujo 04 contradice al código.** Dice «Al aprobar un RQ se notifica solo a `supervisor_logistica`», pero el código también avisa al solicitante si no es quien aprobó. | flujo 04; `transicion-notificar.ts` |
| H10 | **Documentación mínima.** El flujo 04 no describe estados, cierre, catálogo de eventos, por usuario o por rol, ni «Entorno». El flujo 05 no describe los avisos del ciclo del RQ. | flujos 04 y 05 |

Lo que **sí** funciona hoy (verificado en el código): el ciclo de estados del RQ (Solicitado → Aprobado → Recepcionado → En almacén → Atendido); el aviso a los aprobadores al crear un RQ (o directo a Logística si lo crea un jefe de proyectos o de oficina técnica); el aviso a Logística y al solicitante al aprobar; el aviso al solicitante en cada paso siguiente, cerrando los avisos anteriores del RQ; los avisos de documentos del checklist al crear el servicio y al asignar responsable; el aviso a Administración al subir un RDT.

### Resultado esperado

1. **Flujo 04 reescrito** con el estándar de aviso: qué es un aviso, el catálogo de eventos (evento, quién lo dispara, a quién llega, texto, grupo y cuándo se cierra), estados, regla por usuario o por rol, «Entorno» y grupos.
2. **Ciclo del RQ documentado** en el flujo 05 y **verificado en vivo** con cuentas de prueba, con el aviso de cada paso.
3. **El supervisor operativo recibe** aviso de: servicio asignado, cada paso de su RQ, comentario sobre su RQ, RDT validado o rechazado (con el motivo) y documento del checklist asignado.
4. **Bandeja ordenada:** etiqueta «Entorno» cuando no hay servicio, grupo «Jefatura», filtro por tipo de aviso, avisos que se cierran solos cuando se cumple lo que pedían y campana que cuenta lo pendiente de verdad.
5. **Un solo estándar:** todo aviso nuevo (incluido el «informe emitido» del plan de Informes) pasa por el mismo catálogo y el mismo punto de código.

### Alcance

Orden propuesto de trabajo (lo detalla el Planner):

1. **Verificar en vivo y documentar cómo funciona hoy** el ciclo del RQ y la bandeja del supervisor operativo, con usuarios de prueba por rol en `PS-0000`.
2. **Definir el estándar** (catálogo de eventos) y decidir con Victor las pendientes de abajo.
3. **Implementar** el estándar y los cierres: servicio asignado, RDT validado o rechazado, comentario al solicitante, unificar los caminos de estado del RQ, Recepcionado al abrir, «Entorno», grupo «Jefatura», cierre automático de «falta subir…» y filtro por tipo.
4. **Documentar el resultado** (flujos 04, 05, 06, 12, 14 y los que cite) y verificar de nuevo en vivo.
5. Auditoría y cierre.

### No alcance

- La guía o capacitación de uso para los supervisores operativos: es el plan que sigue a este.
- El chat agéntico (flujo 17) y el botón de chat flotante.
- Correo o avisos externos (push, WhatsApp): la app no los tiene hoy; si Victor los quiere es un plan aparte («por confirmar»).
- La emisión de informes de supervisión: es del plan de Informes; aquí solo se fija el estándar al que su aviso se alinea.
- Cambiar quién puede qué (matriz de permisos). Si algo lo exige, se consulta a Victor y se actualiza el artefacto «Matriz de permisos» y el flujo 14 en la misma tarea.
- Borrar o archivar avisos existentes (los 18 de la bandeja de Victor, por ejemplo) sin orden suya.

### Usuarios / roles afectados

Supervisor operativo (principal). Supervisor de logística (recibe y recepciona RQ). Jefe de proyectos, jefe de oficina técnica y administrador (aprueban RQ, adjudican y asignan servicios, validan RDT). Supervisor de administración (recibe los RDT subidos). Los 13 roles ven la bandeja.

### Reglas de negocio y documentos afectados

Tabla para el Gate 1 (su aprobación cubre a todos los Workers; una regla que contradiga algo escrito y no esté aquí se consulta antes de editar):

| Tema | Dice hoy | Pasaría a decir | Documento afectado |
|---|---|---|---|
| Quién recibe el aviso al aprobar un RQ | Flujo 04: «solo `supervisor_logistica`» (el código ya avisa también al solicitante) | Se avisa a Logística y al solicitante (si no es quien aprobó) | 04, 05 |
| Recepcionado | Flujo 05 no lo precisa; el código lo marca con un botón | Cuando Logística abre el aviso de un RQ aprobado, pasa solo a Recepcionado, queda registrado quién lo recepcionó y se avisa al solicitante. En almacén y Atendido siguen con botón. El consolidado conserva el botón. | 05, 04, 14 |
| Grupo de notificación | Se llama «Proyecto» | Se llama «Jefatura» (jefe de proyectos y administrador), igual que el área JF | 04, 02 |
| Aviso sin servicio | No existe: cae en el primer servicio | Se muestra «Entorno». Con servicio, se muestra su N° OT | 04, 16 |
| Servicio asignado | No avisa | Avisa a la persona asignada (y a quien se retira) en las tres vías | 04, 02, 08 |
| RDT validado o rechazado | No avisa al autor (flujo 06: «Notificación al subir: solo Administración») | Se mantiene el aviso al subir y se avisa al autor al validar o rechazar, con el motivo | 06, 04 |
| Comentario sobre un RQ | Avisa a Logística o a jefes y administrador | También avisa al solicitante | 05, 04 |
| Avisos «falta subir…» | Quedan pendientes hasta cerrarlos a mano | Se cierran solos al subir o completar el documento | 12, 04 |
| Estado de un RQ | Dos caminos: con acción (avisa) y genérico (no avisa) | Un solo camino que siempre cierra y avisa | 05, 04 |

### Datos, API, migraciones o dependencias

- **Migración (≥ 108, no destructiva):** `notificaciones.proyecto_id` admite vacío para «Entorno»; columna `evento` (clave del catálogo) con índice, para cerrar por evento y filtrar por tipo. El Planner decide el relleno de los avisos existentes y el cambio de `grupo_nav` «Proyecto» → «Jefatura» (dato o lectura). La numeración se reconfirma al planificar: hoy la más alta es la 107, en `local-worker-6`.
- **Revisar antes de migrar:** la seguridad por filas de la tabla (`db/003_rls.sql`) y las consultas que unen avisos con servicios.
- **Las migraciones las aplica Victor a mano** (como en los planes anteriores), con el verificador antes si está activo.
- **Archivos de la app que se tocan (por confirmar en el plan):** `src/lib/notificaciones/*`; `src/app/api/notificaciones/*`; `src/app/(workspace)/notificaciones/ListaNotificaciones.tsx`; `src/components/ui/EntornoTrabajoGrupo.tsx`, `AccionesRqEnNotificacion.tsx`, `DetalleRqNotificacion.tsx`; `src/lib/requerimientos/*`; `api/proyectos/[id]/requerimientos/*`, `api/proyectos/route.ts`, `api/proyectos/[id]/datos/route.ts`, `api/admin/usuarios/[id]/route.ts`, `api/rdts/partes/[id]/route.ts`, `api/proyectos/[id]/checklist/route.ts` y `documentos/[documentoId]/route.ts`.
- **Sin choque hoy** con los planes en vuelo: ninguna rama de Worker (1 a 6) modifica estos archivos. El código de este plan iría en una rama nueva, que se pide autorizar en el Gate 1.

### Diseño / UI aplicable

Se reutiliza la bandeja y sus insignias; no se crea una segunda interfaz. «Entorno» se muestra con el mismo estilo de la insignia de OT. El filtro «Tipo de aviso» se suma a los existentes. Se sigue `docs/05-diseno-y-referencias/design.md`; si se agrega algo visual nuevo se hace una maqueta antes de implementar.

### Riesgos y decisiones pendientes

**Decididas por Victor (2026-10-16):**

- Recepcionado al abrir el aviso, por Logística.
- El grupo se llama «Jefatura».
- No hay personas reales con rol de Logística, jefe de proyectos u oficina técnica: se pueden crear usuarios de prueba. Victor indica los correos.

**Pendientes (se consultan una por una):**

- **P1.** ¿Debe existir «rechazar o devolver» un RQ? Recomendación: no abrirlo en este plan; quien aprueba comenta y el solicitante corrige.
- **P2.** Reglas por rol o por usuario. Recomendación: un aviso **por rol** es una cola de trabajo (el primero que lo atiende lo cierra para todos, como en Logística); un aviso **por usuario** es informativo y es solo de esa persona (servicio asignado, RDT rechazado, estado de su RQ).
- **P3.** Los 18 avisos viejos de la bandeja de Victor: no se tocan. Si quiere limpiarlos es una orden directa suya.
- **P4.** Correos de los usuarios de prueba (Logística, jefe de proyectos, jefe de oficina técnica, supervisor operativo y supervisor de administración). Las contraseñas viven solo en la memoria del Orquestador, nunca en el repositorio ni en el chat.
- **P5.** Orden de integración con el plan de Informes (su Gate 2 sigue pendiente): su aviso de «informe emitido» debe pasar por este catálogo. Propuesta: este plan parte de `main`; si Informes se integra antes, se adapta aquí; si después, se adapta en Informes.

**Riesgos:**

- La app de pruebas es la de producción: toda prueba con escritura va solo en `PS-0000` y con los usuarios de prueba, con registros marcados y desactivables.
- Hacer opcional `proyecto_id` toca listados y filtros que asumen un servicio en cada aviso.
- El estado compartido de los avisos por rol puede sorprender si se pasa a avisos por usuario sin avisar.

### Criterios de aceptación

1. El flujo 04 trae modelo del aviso, catálogo de eventos, estados, por usuario o por rol, «Entorno» y grupos. Todo evento del código está en el catálogo y viceversa.
2. En vivo, en `PS-0000`: el supervisor operativo crea un RQ, el jefe lo aprueba, Logística lo abre y queda Recepcionado, luego En almacén y Atendido. En cada paso el aviso llega a quien dice el catálogo y a nadie más, y el aviso anterior se cierra.
3. El supervisor operativo recibe aviso al asignarlo a un servicio (las tres vías), cuando su RDT se valida o se rechaza (con el motivo) y cuando comentan su RQ.
4. Un mensaje fuera de un servicio muestra «Entorno»; dentro de uno, su N° OT. No queda nada en `PS-0000` por defecto.
5. El filtro de grupos dice «Jefatura» y ya no «Proyecto».
6. Subir un documento del checklist cierra su aviso y la campana baja.
7. Cada verificación se hace por los dos lados (quien ejecuta y quien no debería recibir) con cuentas distintas.
8. Pruebas unitarias del catálogo y de cada disparador; las existentes siguen pasando (el comando exacto se confirma en el `package.json` de la app; no se inventa).
9. El aviso de «informe emitido» usa el catálogo, o consta por qué no.

### Estrategia de prueba / evidencia

Protocolo de verificación del proyecto: checklist aprobado antes de implementar, autoverificación del agente con Playwright en la app real con login real, loop hasta 100 % en Completado y solo entonces la revisión de Victor. Cuentas: las dos de prueba ya existentes (administrador y supervisor operativo) más los usuarios de prueba por rol de P4. Para la bandeja no sirve «Ver como»: hay que iniciar sesión con la cuenta de cada rol. Evidencia en `03-evidencia/` y enlace al artefacto de checklist visual.

### Aprobación (Gate Spec)

- [x] El Responsable humano aprueba este Spec (Victor, 2026-10-16).

## Skills aplicables

- `seguir-flujo-de-planes`: al activar el flujo y antes de declarar cerrado el plan.
- `cerrar-tanda`: al cerrar cada tanda.
- `trasladar-hallazgos`: en la tanda final del Documentador.
- `verificar-permisos-por-rol`: solo si la tanda toca permisos por rol. Su mecanismo de suplantación no alcanza a la bandeja; para avisos se usa el inicio de sesión real de cada cuenta.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-16 | Objetivo: ordenar las notificaciones y servir al supervisor operativo antes de capacitarlo; documentar y verificar el ciclo del RQ, mejorar lo que se pueda y mantener un solo estándar | Victor |
| 2026-10-16 | Recepcionado pasa solo cuando Logística abre el aviso | Victor |
| 2026-10-16 | El grupo «Proyecto» de las notificaciones pasa a llamarse «Jefatura» | Victor |
| 2026-10-16 | No hay personas reales con esos roles: se pueden crear usuarios de prueba; Victor da los correos | Victor |
| 2026-10-16 | Gate Spec aprobado. Las claves de las cuentas de prueba por rol se guardan solo en la memoria local del Orquestador (tabla creada, cuentas aún sin crear) | Victor |
| 2026-10-16 | El navegador de Playwright usado en las verificaciones se cerró para que otro agente use Chrome; se reabre solo cuando haga falta | Victor / Orquestador |
| 2026-10-16 | Se verificó en solo lectura (código y bandeja en vivo); no se escribió en la app | Orquestador |

## Libro de hallazgos

Un hallazgo se anota en el momento en que ocurre. Los Workers dejan los suyos en su resumen de cierre y el Orquestador los pasa aquí; al final, el Documentador traslada cada fila a su destino. Estados: `Registrada` → `Trasladada` · `Descartada` · `Pendiente de decisión`.

### Mejoras (de trabajo)

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| M1 | 2026-10-16 | Orquestador, diagnóstico | El «Ver como» solo cambia la pantalla: la bandeja y la campana siguen siendo las del usuario real. Para verificar avisos de otro rol hay que iniciar sesión con su cuenta. | `03-aprendizaje-continuo/` | Registrada | — |

### Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| R1 | 2026-10-16 | Victor, Spec | Logística abre el aviso de un RQ aprobado y el RQ pasa solo a Recepcionado; se registra quién lo recepcionó y se avisa al solicitante | Flujo 05 (y 04, 14) | Registrada | — |
| R2 | 2026-10-16 | Victor, Spec | El grupo de notificación «Proyecto» se llama «Jefatura» | Flujo 04 (y 02) | Registrada | — |

### Observaciones sobre la política

Ninguna.

### Carpetas/archivos huérfanos

Se reportan a Victor; no se borra nada. Todos son código de la app, por confirmar si tienen uso.

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| O1 | 2026-10-16 | Orquestador, diagnóstico | `src/app/api/notificaciones/[id]/marcar-visto/route.ts`: alias de «revisar» «por compatibilidad con UI anterior»; ninguna pantalla de la app lo llama | Reporte a Victor | Registrada | — |
| O2 | 2026-10-16 | Orquestador, diagnóstico | `src/app/api/notificaciones/route.ts`: consulta de respaldo `COLUMNAS_LEGACY` para una base sin la columna de remitente (migración 018) | Reporte a Victor | Registrada | — |
| O3 | 2026-10-16 | Orquestador, diagnóstico | `src/app/api/areas/route.ts`: tres consultas de comprobación sobre `proyectos`, `proyecto_documentos` y `notificaciones` cuyo resultado no se usa | Reporte a Victor | Registrada | — |

## Siguiente paso

Victor revisa este Spec y las pendientes P1 a P5. Con el Gate Spec aprobado, el Orquestador delega al Planner (paso 5), que entrega el plan con la Punch List, el equipo, los modelos y esfuerzos por fase, la tabla de cambios a flujos y la consulta única de datos de prueba y pre-autorizaciones (paso 7).
