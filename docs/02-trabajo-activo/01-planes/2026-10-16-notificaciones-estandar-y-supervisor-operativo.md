# Notificaciones: estándar de avisos y apoyo al supervisor operativo

## Identificación y estado

- Tema: ordenar el sistema de notificaciones bajo un estándar único (qué evento avisa, a quién, con qué texto, cuándo se cierra) y cerrar los huecos que hoy dejan al supervisor operativo sin saber qué pasó con su servicio, su RQ o su RDT. Prepara el terreno para capacitar a los supervisores operativos en el uso de la app.
- Fecha de inicio: 2026-10-16.
- Estado: `En implementación` desde el 2026-10-17 (Gate 1 aprobado por Victor). Lo que sigue en esta línea es el historial de la planificación: `Planificando`, **listo para el Gate 1**. El Planner entregó el plan, la Punch List, el equipo y las tandas el 2026-10-17; el Orquestador lo revisó el mismo día, lo contrastó con el estado real de la app (`main` en `69ebf94`, con Informes ya integrado; ver «Referencia al Spec aprobado») y pasó los hallazgos del Planner al libro. El Spec sigue aprobado (Gate Spec, Victor, 2026-10-16) con P1, P2, P3 y P5 decididas; P4 (correos de las cuentas de prueba) sigue pendiente y bloquea la verificación en vivo, no la implementación. No hay Workers, ramas ni migraciones todavía.
- Fecha de entrega del plan: 2026-10-17.

Puertas:

- Gate Spec: `aprobado` (Victor, 2026-10-16)
- Gate 1: `aprobado` (Victor, 2026-10-17)
- Gate 2: `pendiente`

## Spec

### Estado

`Aprobado` (Gate Spec, Victor, 2026-10-16). Redactado por el Orquestador con lo pedido por Victor y lo verificado en el código y en la bandeja en vivo.

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
2. **Ciclo del RQ documentado** en el flujo 05 y **verificado en vivo** con cuentas de prueba, con el aviso de cada paso, incluida la nueva opción de **devolver** un RQ con motivo (decisión P1).
3. **El supervisor operativo recibe** aviso de: servicio asignado, cada paso de su RQ, RQ devuelto (con el motivo), comentario sobre su RQ, RDT validado o rechazado (con el motivo) y documento del checklist asignado.
4. **Bandeja ordenada:** etiqueta «Entorno» cuando no hay servicio, grupo «Jefatura», filtro por tipo de aviso, avisos que se cierran solos cuando se cumple lo que pedían y campana que cuenta lo pendiente de verdad.
5. **Un solo estándar:** todo aviso nuevo (incluido el «informe emitido» del plan de Informes) pasa por el mismo catálogo y el mismo punto de código.

### Alcance

Orden propuesto de trabajo (lo detalla el Planner):

1. **Verificar en vivo y documentar cómo funciona hoy** el ciclo del RQ y la bandeja del supervisor operativo, con usuarios de prueba por rol en `PS-0000`.
2. **Definir el estándar** (catálogo de eventos) y decidir con Victor las pendientes de abajo.
3. **Implementar** el estándar y los cierres: servicio asignado, RDT validado o rechazado, comentario al solicitante, unificar los caminos de estado del RQ, Recepcionado al abrir, devolver un RQ con motivo (estado nuevo), «Entorno», grupo «Jefatura», cierre automático de «falta subir…» y filtro por tipo. Antes de implementar, el Planner define con Victor el detalle de «devolver» (ver fila en la tabla de reglas) y hace una maqueta si la pantalla cambia.
4. **Documentar el resultado** (flujos 04, 05, 06, 12, 14 y los que cite) y verificar de nuevo en vivo.
5. Auditoría y cierre.

### No alcance

- La guía o capacitación de uso para los supervisores operativos: es el plan que sigue a este.
- El chat agéntico (flujo 17) y el botón de chat flotante.
- Correo o avisos externos (push, WhatsApp): la app no los tiene hoy; si Victor los quiere es un plan aparte («por confirmar»).
- La emisión de informes de supervisión: es del plan de Informes; aquí solo se fija el estándar al que su aviso se alinea.
- Cambiar quién puede qué (matriz de permisos), salvo lo que exija «devolver» un RQ (lo puede hacer quien ya puede aprobarlo). Si algo más lo exige, se consulta a Victor y se actualiza el artefacto «Matriz de permisos» y el flujo 14 en la misma tarea.
- Borrar o archivar avisos existentes sin orden de Victor. Única excepción: los 18 avisos viejos de su bandeja, por orden directa del 2026-10-16 (se respaldan y se cierran como atendidos, sin borrar nada; ver registro de decisiones).

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
| Devolver un RQ | No existe: el jefe solo puede comentar (o aprobar) | Propuesta del Orquestador, a cerrar con Victor en el Gate 1: quien puede aprobar un RQ en estado Solicitado puede **devolverlo** con un motivo obligatorio; pasa al estado «Devuelto» y se avisa al solicitante con el motivo; el solicitante lo corrige y lo **reenvía** (vuelve a Solicitado y se avisa de nuevo a los aprobadores). Un RQ Devuelto no avanza a Aprobado sin reenviarse. | 05, 04, 14, matriz de permisos |

### Datos, API, migraciones o dependencias

- **Migración (≥ 108, no destructiva):** `notificaciones.proyecto_id` admite vacío para «Entorno»; columna `evento` (clave del catálogo) con índice, para cerrar por evento y filtrar por tipo. El Planner confirma si el estado de un RQ está limitado por una restricción en la base (para agregar «Devuelto») y dónde se guarda el motivo de la devolución. El Planner decide el relleno de los avisos existentes y el cambio de `grupo_nav` «Proyecto» → «Jefatura» (dato o lectura). La numeración se reconfirma al planificar: hoy la más alta es la 107, en `local-worker-6`.
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

**Decididas por Victor al aprobar el Spec (2026-10-16):**

- **P1.** **Sí se crea «devolver» un RQ**, en este plan (contra la recomendación del Orquestador de dejarlo fuera; decisión de Victor). El detalle (quién, motivo, reenvío) está en la fila «Devolver un RQ» de la tabla de reglas y se cierra con Victor en el Gate 1.
- **P2.** Un aviso **por rol** es una cola de trabajo compartida (el primero que lo atiende lo cierra para todos, como en Logística); un aviso **por usuario** es informativo y es solo de esa persona (servicio asignado, RDT rechazado, estado de su RQ, RQ devuelto).
- **P3.** **Limpiar los 18 avisos viejos** de la bandeja de Victor: orden directa. Se respaldan (id, texto, tipo, destinatario, estado) antes de tocarlos, se cierran como atendidos (sin borrar filas) y se hace al reabrir el navegador de pruebas, al inicio de la etapa 1. Solo los de la bandeja de Victor; ningún otro aviso.
- **P5.** Este plan **parte de `main`**; si Informes se integra antes, se adapta aquí; si después, se adapta su aviso de «informe emitido» al catálogo nuevo. Ninguno espera al otro.

**Pendiente (lo único que falta de Victor):**

- **P4.** Correos de los usuarios de prueba (Logística, jefe de proyectos, jefe de oficina técnica, supervisor operativo y supervisor de administración). Las contraseñas viven solo en la memoria del Orquestador, nunca en el repositorio ni en el chat.

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
10. En vivo, en `PS-0000`: el jefe devuelve un RQ con motivo, el solicitante recibe el aviso con el motivo, lo corrige y lo reenvía, y los aprobadores reciben el aviso otra vez. Un RQ Devuelto no se puede aprobar sin reenviarse, y quien no puede aprobar no ve la opción de devolver.
11. Los 18 avisos viejos de la bandeja de Victor quedan respaldados y cerrados, sin borrar filas.

### Estrategia de prueba / evidencia

Protocolo de verificación del proyecto: checklist aprobado antes de implementar, autoverificación del agente con Playwright en la app real con login real, loop hasta 100 % en Completado y solo entonces la revisión de Victor. Cuentas: las dos de prueba ya existentes (administrador y supervisor operativo) más los usuarios de prueba por rol de P4. Para la bandeja no sirve «Ver como»: hay que iniciar sesión con la cuenta de cada rol. Evidencia en `03-evidencia/` y enlace al artefacto de checklist visual.

### Aprobación (Gate Spec)

- [x] El Responsable humano aprueba este Spec (Victor, 2026-10-16).

## Referencia al Spec aprobado

El Spec es la sección «Spec» de este mismo archivo (Gate Spec aprobado por Victor el 2026-10-16). Este plan lo convierte en trabajo: tandas, Punch List, equipo y modelos. No lo reescribe.

**Tres correcciones al Spec que Victor confirma en el Gate 1** (el Planner verificó en el código y en los flujos; el Spec queda como se aprobó y estas correcciones rigen sobre él):

1. **«Sin choque hoy» era falso al planificar, y el Orquestador lo actualizó el 2026-10-17 contra el estado real.** Las ramas de Informes (`local-worker-1`, `2` y `3`) modificaban archivos que este plan también toca: `api/proyectos/route.ts`, `api/proyectos/[id]/datos/route.ts`, `api/proyectos/[id]/confirmar-transicion/route.ts`, `api/rdts/partes/[id]/route.ts`, `src/lib/permisos/permisos.ts` y `db/README.md`. **Informes ya entró a `main`** (verificado con `git branch --merged main`: `local-worker-1` a `4` están dentro; `main` está en `69ebf94`, no en `628918a`), con las migraciones 098 a 102 y `src/lib/informes/notificar-emision.ts`. Por la decisión P5, este plan parte de ese `main` y se adapta a lo que Informes ya dejó; no hay que esperar a nadie. Siguen sin integrarse `local-worker-5` (permisos; toca `permisos.ts`) y `local-worker-6` (Cronograma; migración 107 y `db/README.md`): ahí queda el único choque posible. Las pruebas de los archivos de avisos y de RQ no han cambiado en `main` desde `628918a` (comprobado con `git diff`). Cómo se evita pisarse está en «Riesgos y bloqueos».
2. **Tres filas de la tabla «dice hoy / pasaría a decir» estaban mal citadas** (grupo «Proyecto», aviso sin servicio y servicio asignado): lo que «dice hoy» no está escrito en un flujo, es comportamiento del código. Ver «Tabla verificada de flujos».
3. **Pruebas:** los comandos confirmados en el `package.json` de la app son `npm test` (corre `vitest run`), `npm run lint` y `npm run build`. Con eso se cumple el criterio 8.

**Ampliación de alcance pedida por Victor (2026-10-17): cambiar la propia contraseña desde Mi entorno.** Hoy el administrador crea el usuario con una contraseña que el correo de invitación no trae (`api/admin/usuarios/route.ts`), y el usuario no puede cambiarla nunca. Lo único editable en el perfil de Mi entorno (`PerfilEntorno.tsx`, `api/perfil`) es el celular, y solo para el administrador y el jefe de proyectos (`puedeEditarPerfilExtendido`; flujo 14, fila «Editar perfil extendido (propio)»): los otros 11 roles no editan nada de su perfil. No existe «olvidé mi contraseña» ni cambio de contraseña en la app (verificado por búsqueda en `src/`). Se agrega al plan la tanda **T9** (8 ítems tras la segunda ampliación, abajo) y los ítems de verificación en vivo **T7-08** y **T7-09**; sin migración, con un archivo de permiso propio (no se toca `permisos.ts`, que `local-worker-5` también modifica). Criterios de aceptación que se suman al Spec: **12.** cualquier usuario con sesión, de los 13 roles, cambia su contraseña desde Mi entorno indicando la actual y la nueva, y después entra con la nueva y no con la anterior; **13.** el servidor valida (sesión, contraseña actual, largo mínimo de 8, nueva distinta de la actual, confirmación) y no escribe ninguna contraseña en respuestas ni registros. No es un cambio de «quién puede qué» de la matriz existente: es una acción nueva para los 13 roles, y se agrega a la tabla 2 del flujo 14 y al artefacto «Matriz de permisos» en la misma tarea (política de coherencia).

**Segunda ampliación (Victor, 2026-10-17): celular y correo propios para todos.** Cada usuario, de los 13 roles, puede **ingresar o cambiar su número de celular y su correo electrónico** desde el Perfil de Mi entorno, además de la contraseña. Hoy la edición del perfil (solo el celular) la tienen únicamente el administrador y el jefe de proyectos. **Esto contradice lo escrito** y se lista para el Gate 1 (pregunta Q8): flujo 14, fila 94 «Editar perfil extendido (propio)» (solo administrador y jefe de proyectos) y flujo 14, línea 184, donde el jefe de oficina técnica «deja de… editar su perfil» (decisión anterior de Victor). El correo es el identificador de ingreso y vive en el sistema de autenticación (no en la tabla de perfiles): cambiarlo exige la contraseña actual y la confirmación del nuevo correo por enlace (detalle en el riesgo 19). Nombre, cargo, área y roles siguen siendo del administrador. Criterios que se suman: **14.** los 13 roles ven «Editar mi perfil» y pueden ingresar o cambiar su celular; **15.** los 13 roles pueden cambiar su correo con la contraseña actual, y el correo nuevo solo rige cuando lo confirman desde ese buzón; hasta entonces sigue valiendo el anterior.

## Objetivo, alcance y no alcance

**Objetivo.** Que cada aviso de la app salga de un solo catálogo y de un solo punto de código, y que el supervisor operativo se entere de lo que le pasa a su servicio, su RQ y su RDT (servicio asignado, RQ avanzado o devuelto con el motivo, comentario sobre su RQ, RDT validado o rechazado con el motivo, documento por subir), con una bandeja ordenada («Entorno», N° OT, «Jefatura», filtro por tipo, avisos que se cierran solos). Prepara la capacitación que viene después.

**Alcance.** Los 11 criterios de aceptación del Spec más los 4 de las ampliaciones (12 a 15), en 9 tandas: T1 preparación y cómo funciona hoy, T2 catálogo y base, T3 bandeja, T4 ciclo del RQ, T5 devolver y reenviar, T6 supervisor operativo y cierres, T9 mi perfil propio: contraseña, celular y correo (ampliaciones), T7 verificación en vivo, T8 documentación y cierre.

**No alcance** (además de lo del Spec):

- Reparar la seguridad por filas de la base (migración 095): no se toca. Por confirmar si está aplicada en producción.
- Crear una opción de «desactivar usuario»: hoy solo existe eliminar. Se reporta, no se construye.
- Actualizar de golpe los avisos viejos con grupo «Proyecto» en la base: «Jefatura» se resuelve al leer (ver decisiones).
- Unificar las dos pantallas que muestran avisos (la página de notificaciones y la bandeja de Mi entorno): ambas se mantienen y reciben el mismo cambio.
- Cambiar quién puede qué, salvo «devolver» y «corregir y reenviar» (ver «Tabla verificada de flujos»).

## Entorno, repositorios, ramas y worktrees

- **Repositorio documental** (`pg_control_proyectos`): se trabaja directo en `main` (AGENTS.md). Aquí viven este plan, los flujos y los informes.
- **App real** (`py_control_proyectos_web`): **`main` está en `69ebf94`** (verificado el 2026-10-17; el Planner había leído `628918a`, que es de antes de integrar Informes y Alcance y Presupuesto). Ramas existentes: `main`, `local-worker-1` a `6` y `plan-maestro-tres-paneles`; worktrees `.worktrees/local-worker-1` a `6`. `local-worker-1` a `4` ya están dentro de `main` (Informes). `local-worker-5` (4 commits propios, permisos) y `local-worker-6` (Cronograma, 3 commits, migración 107) no se han integrado. `local-worker-4` está en `628918a`, atrás de `main`, y no se reutiliza sin confirmar con Victor.
- **Rama y worktree propuestos (Victor los autoriza en el Gate 1):** `local-worker-7` y `.worktrees/local-worker-7`, creados desde `main` (`69ebf94`, o el que tenga `main` el día de crearlos; el Worker git lo comprueba antes). No existen hoy: se verificó con `git branch` y la lista de worktrees. El Worker git los crea y copia el `.env.local` principal al worktree (autorización permanente, ver `docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md`).
- **Comandos verificados** (`package.json`): `npm test` (= `vitest run`), `npm run lint` (= `eslint`), `npm run build` (= `next build`). En worktrees se usa `npx next build --webpack` y `npm run dev -- --webpack -p <puerto>` (doc 03). `tsc --noEmit` no es un script del proyecto: por confirmar antes de usarlo. Las pruebas de Vitest corren en entorno de servidor sobre `src/**/*.test.ts`: no hay pruebas de componentes, así que lo visual se verifica en vivo (T7).
- **Base de datos:** la misma de producción. Toda prueba con escritura va solo en `PS-0000` con registros marcados «PRUEBA». Las migraciones las aplica Victor a mano.
- **Numeración de migraciones:** `main` llega a la **102** (Informes, ya integrado); la rama de Cronograma (`local-worker-6`) tiene la 107 y no está integrada; no hay 103 a 106 en ninguna rama (verificado el 2026-10-17). Este plan usa la **108** (notificaciones) y la **109** (estado Devuelto del RQ). Se reconfirma antes de escribir y antes de aplicar.
- **Dónde corre la verificación en vivo (T7):** servidor local del worktree contra la misma base. Por confirmar con el Orquestador; no es una pregunta para Victor.

## Skills aplicables

- `seguir-flujo-de-planes`: al activar el flujo y antes de declarar cerrado el plan.
- `cerrar-tanda`: al cerrar cada tanda.
- `trasladar-hallazgos`: en la tanda final del Documentador.
- `verificar-permisos-por-rol`: solo si la tanda toca permisos por rol. Su mecanismo de suplantación no alcanza a la bandeja; para avisos se usa el inicio de sesión real de cada cuenta.

## Fases y dependencias

Nueve tandas (T9 se numeró al final para no renumerar las demás, pero se ejecuta antes de T7). Una tanda es un bloque de 6 a 8 ítems de la Punch List para un solo Worker en una sola sesión. Los ítems se identifican como `T<tanda>-<número>` (por ejemplo, `T4-02` es el segundo ítem de la tanda 4).

| Tanda | Qué hace | Depende de | Quién |
|---|---|---|---|
| (antes) | Gate 1: Victor aprueba plan, Punch List, modelos, rama y pre-autorizaciones, y responde la consulta única. El Worker git crea la rama y el worktree. | Spec aprobado | Victor, Worker git |
| T1 | Preparación y «cómo funciona hoy»: cuentas de prueba, respaldo y cierre de los 18 avisos, informes del ciclo del RQ y de la bandeja del supervisor operativo, datos de prueba y maqueta | Gate 1; P4 (correos) para T1-01; navegador libre | Worker de verificación |
| T2 | Catálogo y base: migración 108, catálogo, módulo central de avisos, regla por usuario o por rol, API con servicio opcional | Gate 1 y rama | Worker 7 |
| T3 | Bandeja: «Entorno», N° OT, «Jefatura», filtro por tipo, avisos de RQ por evento | T2 y maqueta T1-07 | Worker 7 |
| T4 | Ciclo del RQ: un solo camino de estado, Recepcionado al abrir, comentario al solicitante, avisos por catálogo | T2 | Worker 7 |
| T5 | Devolver y reenviar: migración 109, estado Devuelto, botón, edición y reenvío | T4 y maqueta T1-07 | Worker 7 |
| T6 | Supervisor operativo y cierres: servicio asignado (3 vías), RDT validado, rechazado y registrado, «falta subir» con cierre automático | T2; va después de T5 por los archivos compartidos con Informes | Worker 7 |
| T9 | Mi perfil propio desde Mi entorno (ampliaciones pedidas por Victor): cambiar contraseña, ingresar o cambiar celular y cambiar correo; rutas del servidor, permiso propio para los 13 roles, formulario en el perfil, mensajes y regresión | Rama `local-worker-7`; no depende de T2 a T6 (archivos distintos), pero va después de T6 para no abrir un frente nuevo en medio | Worker 7 |
| T7 | Verificación en vivo con cuentas por rol, por los dos lados (incluye contraseña, T7-08, y celular y correo, T7-09, este último con un clic de Victor en el enlace de confirmación) | T2 a T6 y T9; migraciones 108 y 109 aplicadas por Victor; servidor del worktree en marcha; cuentas listas; navegador libre | Worker de verificación |
| T8 | Documentación: flujos 04, 05, 06, 12, 14 (y 02, 08, 16), artefacto «Matriz de permisos», traslado de hallazgos, índices | T7; flujos ajenos con cambios sin commitear ya commiteados | Documentador |
| (después) | Auditor, Gate 2 y cierre (16a merge a `main` con permiso de Victor, 16b push, 16c mensaje) | T8 | Auditor, Orquestador |

**Orden:** T1 → T2 → T3 → T4 → T5 → T6 → T9 → T7 → T8 → Auditor. **T1 y T2 pueden correr a la vez:** T1 solo mira la app tal como está hoy y escribe evidencia; T2 solo escribe código en el worktree; no comparten archivos. La parte visual de T3 y T5 espera la maqueta aprobada (T1-07). T6 va al final del código a propósito: toca archivos que Informes también tocó. Informes ya entró a `main` (2026-10-17), así que `local-worker-7` nace con esos cambios; antes de T6 el Worker git solo hace `git merge main` si `main` avanzó (por ejemplo, si entran Permisos o Cronograma).

**Por qué un solo Worker de código y no tres.** T2 a T6 comparten el módulo central de avisos y las dos pantallas de avisos; partirlas en carriles obligaría a coordinar los mismos archivos. Informes ya toca cuatro de los archivos de API de T6. Paralelizar solo ahorraría reloj, no costo, y subiría el riesgo de pisarse. Si Victor quiere ganar tiempo, la única división sana es T6 en una segunda rama (`local-worker-8`), pero no se recomienda.

**Qué tandas usan navegador:** T1 y T7 (verificación en vivo). El navegador lo usa otro agente a ratos: T1 y T7 se programan cuando Victor confirme que está libre. T2 a T6 no necesitan navegador.

## Equipo del plan

Trabajamos en Claude Code con subagentes; **no se usa Opus**. Esfuerzo medio en todo. El nivel 1 a 5 del archivo `10-niveles-de-modelos.md` es una **equivalencia propuesta** por tipo de tarea (ese archivo mide modelos de opencode, no los de Claude Code).

| Rol | Modelo | Esfuerzo | Sesión o tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|---|
| Orquestador | El que Victor fije con `/model` (sin Opus) | El que Victor fije | todo el plan | `main` | N/A | activo |
| Planner | Sonnet | Medio | este plan | `main` | N/A | entregado (2026-10-17) |
| Worker 7 (código) | Sonnet | Medio | T2, T3, T4, T5, T6, T9 | `local-worker-7` (nueva, por autorizar en el Gate 1) | `.worktrees/local-worker-7` | pendiente |
| Worker de verificación | Sonnet | Medio | T1 y T7 (navegador; no escribe código) | N/A | N/A | pendiente |
| Documentador | Sonnet (flujos) y Haiku (índices, traslados y referencias) | Medio | T8 | `main` (repositorio documental) | N/A | pendiente |
| Worker git | Haiku | Medio | a pedido: crear rama y worktree, copiar `.env.local`, `git merge main` antes de T6 y antes del cierre, commits y merges que pida el Orquestador | opera sobre `local-worker-7` | `.worktrees/local-worker-7` | pendiente |
| Auditor | Sonnet | Medio | tras T8 | `main` | N/A | pendiente |

**Un solo Worker de código basta** (ver «Fases y dependencias»). El merge a `main` es el paso 16a y solo con permiso explícito de Victor.

### Asignación de modelos y esfuerzos por fase (Gate 1)

| Tanda | Contenido | Ítems | Worker | Modelo | Esfuerzo | Nivel equiv. | Justificación | Aprobación Victor |
|---|---|---|---|---|---|---|---|---|
| T1 | Preparación y cómo funciona hoy | 7 | Verificación | Sonnet | Medio | 3 | Navegador, cuentas por rol, respaldo y cierre de avisos, tres informes; sin código | aprobado (Victor, 2026-10-17) |
| T2 | Catálogo y base | 7 | Worker 7 | Sonnet | Medio | 4 | Migración 108 con columnas nuevas, módulo central por el que pasan todos los avisos y regla por usuario o por rol; es la base de todo lo demás | aprobado (Victor, 2026-10-17) |
| T3 | Bandeja | 7 | Worker 7 | Sonnet | Medio | 3 | Dos pantallas de avisos, filtro y renombre de grupo, con pruebas existentes que cambian | aprobado (Victor, 2026-10-17) |
| T4 | Ciclo del RQ | 7 | Worker 7 | Sonnet | Medio | 3 | Un camino de estado, Recepcionado al abrir con cuidado de concurrencia, varios archivos | aprobado (Victor, 2026-10-17) |
| T5 | Devolver y reenviar | 8 | Worker 7 | Sonnet | Medio | 4 | Regla de negocio nueva, migración 109, edición de RQ que no existe y estado nuevo en 9 archivos | aprobado (Victor, 2026-10-17) |
| T6 | Supervisor operativo y cierres | 8 | Worker 7 | Sonnet | Medio | 3 | Once rutas de API con cambios pequeños cada una; choque posible con Informes | aprobado (Victor, 2026-10-17) |
| T9 | Mi perfil propio: contraseña, celular y correo (ampliaciones) | 8 | Worker 7 | Sonnet | Medio | 3 | Dos rutas nuevas que tocan autenticación (contraseña y correo, con la actual verificada en el servidor), la ruta del perfil que pasa a los 13 roles y un formulario con componentes que ya existen; sin migración | aprobado (Victor, 2026-10-17) |
| T7 | Verificación en vivo | 9 | Verificación | Sonnet | Medio | 3 | Navegador, permisos por rol, móvil, limpieza de datos, contraseña, celular y correo | aprobado (Victor, 2026-10-17) |
| T8 | Documentación y traslado de hallazgos | 8 | Documentador | Sonnet / Haiku | Medio | 3 y 1 | Reescritura del flujo 04 y ediciones de otros cinco flujos (Sonnet); índices, referencias y traslados (Haiku) | aprobado (Victor, 2026-10-17) |

**Esfuerzo alto: no se solicita en ninguna tanda.** Candidatos eventuales, solo si algo falla dos veces y se pide en el momento: `T2-04` (regla por usuario o por rol) y `T4-02` (Recepcionado al abrir, por la concurrencia). **Nivel 5: no se usa.** Total: **9 tandas, 69 ítems** (59 originales + 8 de T9 + T7-08 y T7-09). Si T9 falla dos veces en la verificación de la contraseña actual, se pide esfuerzo alto en ese momento.

### Brief de cada Worker

El brief de cada tanda vive en la carpeta `2026-10-16-notificaciones-estandar-y-supervisor-operativo-briefs/` (con `resultados/` para el resumen de cierre de cada tanda), con la plantilla `13-brief-de-tanda.md`: 8 KB como máximo, lista exacta de archivos y líneas a leer y lo que no, y tope de unas 80 llamadas por Worker. **Los briefs aún no están escritos** (el Planner no escribe fuera de este archivo): los escribe el Orquestador justo antes de lanzar cada tanda, a partir de la sección «Archivos / componentes afectados» y de la Punch List de abajo.

### Prompt del Auditor

Alcance: el código de la rama `local-worker-7`, este plan, la Punch List, la evidencia y los documentos editados por el Documentador.

1. **Primer chequeo:** con `git log` y `git branch --contains`, comprobar que el código de las tandas T2 a T6 y T9 está en `local-worker-7` y no en `main` (el merge es posterior, en 16a).
2. **Segundo chequeo:** que el libro de hallazgos del plan esté trasladado (mejoras de trabajo a `03-aprendizaje-continuo/`, reglas de negocio a su flujo, huérfanos reportados a Victor).
3. **Revisar:** el Spec, el plan, la Punch List (cada ítem con su evidencia), la evidencia, los flujos 04, 05, 06, 12, 14, 02, 08 y 16 y el artefacto «Matriz de permisos». Verificar la trazabilidad (política de coherencia): toda interfaz, acción o permiso nuevo está en el flujo 14 y en el artefacto; el catálogo de eventos del flujo 04 coincide con el del código.
4. **Informe:** en `docs/02-trabajo-activo/04-auditoria/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md`, con las categorías APLICAR AHORA / PROPONER A RESPONSABLE / NO PROMOVER / PROPONER SKILL, los pendientes y una recomendación: Listo para Gate 2 / Bloqueado / Requiere corrección.
5. El Auditor no implementa ni aprueba.

## Archivos / componentes afectados

Rutas relativas a `py_control_proyectos_web/` salvo que se indique. Los nombres de archivos nuevos son **propuestas**; el Worker los confirma al crearlos.

| Tanda | Archivos nuevos | Archivos que se modifican |
|---|---|---|
| T1 | `docs/05-diseno-y-referencias/mockups/notificaciones-bandeja.html` (repositorio documental; no se toca `mockups/index.html` ni `mockups/README.md`, que tienen cambios de otras sesiones); `docs/02-trabajo-activo/03-evidencia/<plan>/respaldo-avisos-victor.json` | Ninguno de la app |
| T2 | `db/108_notificaciones_evento_entorno.sql`; `src/lib/notificaciones/catalogo.ts` y `avisar.ts` (con pruebas) | `db/README.md` (solo su línea); `src/lib/notificaciones/notificaciones.ts`; `src/lib/notificaciones/crear-para-usuario.ts`; `src/lib/notificaciones/api-helpers.ts`; `src/app/api/notificaciones/route.ts`; `src/app/api/notificaciones/count/route.ts` |
| T3 | Ninguno obligatorio | `src/lib/notificaciones/grupo-proceso.ts` y su prueba; `src/app/(workspace)/notificaciones/ListaNotificaciones.tsx`; `src/components/ui/EntornoTrabajoGrupo.tsx`; `src/app/(workspace)/mi-entorno/page.tsx`; `src/lib/config/equivalencia-f1b.test.ts`; `src/app/api/notificaciones/route.ts` |
| T4 | Ninguno obligatorio | `src/app/api/proyectos/[id]/requerimientos/[rqId]/estado/route.ts`; `.../[rqId]/comentarios/route.ts`; `src/app/api/proyectos/[id]/requerimientos/route.ts`; `src/lib/requerimientos/transicion-notificar.ts`; `src/lib/requerimientos/derivar-logistica.ts`; `src/lib/requerimientos/aprobacion.ts`; `src/lib/requerimientos/acciones-estado.ts` (y su prueba); `src/app/api/notificaciones/[id]/revisar/route.ts` y `.../atender/route.ts`; `src/components/ui/AccionesRqEnNotificacion.tsx`; `src/components/ui/DetalleRqNotificacion.tsx`; `TablaConsolidadoRq.tsx` |
| T5 | `db/109_rq_devuelto.sql`; `src/lib/requerimientos/permisos-devolver.ts`; página `src/app/(workspace)/proyectos/[id]/requerimientos/[rqId]/editar/page.tsx` | `src/lib/requerimientos/tipos.ts`; `estado-ui.ts`; `filtros-registro.ts`; `acciones-estado.ts`; `contactos-pdf.ts`; `.../[rqId]/route.ts` (edición); `.../[rqId]/estado/route.ts`; `FormularioRequerimiento.tsx`; `PanelVerRq.tsx`; `ListadoRequerimientos.tsx`; `db/README.md` |
| T6 | Ninguno obligatorio | `src/app/api/proyectos/route.ts`; `src/app/api/proyectos/[id]/datos/route.ts`; `src/app/api/admin/usuarios/[id]/route.ts`; `src/app/api/rdts/partes/[id]/route.ts`; `src/app/api/rdts/partes/route.ts`; `src/app/api/proyectos/[id]/checklist/route.ts`; `.../documentos/[documentoId]/route.ts`; `.../dp/route.ts`; `.../confirmar-transicion/route.ts`; `src/app/api/rdts/route.ts`; `src/lib/pr/acumulacion-rdt.ts` |
| T9 | `src/app/api/perfil/contrasena/route.ts` y `src/app/api/perfil/correo/route.ts` (rutas nuevas, con sus pruebas); `src/lib/auth/perfil-propio.ts` (validaciones de contraseña, celular y correo, y permiso para los 13 roles, con prueba; archivo propio, no se toca `permisos.ts`) | `src/app/api/perfil/route.ts` (el `PATCH` del celular deja de depender de `puedeEditarPerfilExtendido` y solo acepta el celular); `src/components/ui/PerfilEntorno.tsx` (chip «Editar mi perfil» para todos y formularios, con `InputContrasena` y `Input` existentes). Sin migración |
| T7 | Evidencia en `03-evidencia/<plan>/` | Ninguno |
| T8 | Entrada nueva en `03-aprendizaje-continuo/` (traslado de mejoras) | Flujos 04, 05, 06, 12, 14, 02, 08, 16 (03 por revisar), índices y referencias; artefacto «Matriz de permisos» |

**Contratos de API que cambian** (se documentan en el flujo 04 y en el 14): `POST /api/notificaciones` pasa a aceptar `proyectoId` vacío («Entorno»); `GET /api/notificaciones` y `count` suman el parámetro `categoria` y la regla por usuario o por rol; `estado/route.ts` pierde la vía genérica sin `accion` y suma las acciones devolver y reenviar; ruta nueva de edición del RQ devuelto.

## Punch List embebida

Formato de `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia de cada ítem va en el resumen de cierre de su tanda (`resultados/<tanda>.md`) y en `03-evidencia/`.

### Estado de aprobación

Gate 1: aprobado (Victor, 2026-10-17; ver «Registro de decisiones»).

**69 ítems en 9 tandas** (las ampliaciones de perfil propio suman T9-01 a T9-08, T7-08 y T7-09). Cada verificación de aviso se hace por los dos lados (quien ejecuta y quien no debería recibir), con cuentas distintas.

### Ítems funcionales

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T1-04 | T1 | Informe «cómo funciona hoy» del ciclo del RQ en `PS-0000` (crear, aprobar, Logística recibe, estados): a quién llega cada aviso y cuál se cierra | Informe con una fila por paso, hecho con cuentas distintas | Sin verificar |
| T1-05 | T1 | Informe «cómo funciona hoy» de la bandeja del supervisor operativo: qué recibe y qué no; prueba con dos personas del mismo rol (hallazgo H8) | Informe y captura de la bandeja de cada persona antes y después de que una abra el aviso | Sin verificar |
| T2-02 | T2 | Catálogo de eventos en un solo archivo: clave, categoría, quién lo dispara, a quién llega, texto, grupo y cuándo se cierra | Archivo del catálogo y prueba unitaria que valida cada entrada | Sin verificar |
| T2-03 | T2 | Módulo central de avisos: crear y cerrar por evento o referencia; los 4 creadores actuales siguen funcionando como envoltorios y prueba de cobertura (todo evento del código está en el catálogo y viceversa) | Pruebas unitarias; la prueba de cobertura falla si se agrega un aviso fuera del catálogo | Sin verificar |
| T2-06 | T2 | `informe.emitido` queda reservado en el catálogo y el aviso del plan de Informes (`crearNotificacionParaUsuario`) sigue funcionando | Prueba unitaria y nota en el catálogo | Sin verificar |
| T3-01 | T3 | Se muestra «Entorno» cuando el aviso no tiene servicio y el N° OT cuando lo tiene, en las dos pantallas de avisos | Captura de ambas pantallas con un aviso de cada tipo | Sin verificar |
| T3-02 | T3 | «Enviar mensaje» usa «Entorno» por defecto: ya no se guarda nada nuevo en `PS-0000` | Consulta que muestra el mensaje nuevo sin servicio y captura | Sin verificar |
| T3-04 | T3 | Filtro «Tipo de aviso» (Requerimientos, RDT, Servicio, Checklist, Mensajes, Otros) | Prueba del parámetro `categoria` y captura filtrando | Sin verificar |
| T3-05 | T3 | Los avisos de RQ se reconocen por su evento y no por su texto: el aviso «Nuevo requerimiento» (RQ directo a Logística) ahora tiene sus acciones | Prueba unitaria y captura con la cuenta de Logística | Sin verificar |
| T4-01 | T4 | Un solo camino para cambiar el estado de un RQ: siempre cierra el aviso anterior y avisa al solicitante | Prueba unitaria y comprobación de que ninguna pantalla usa la vía sin `accion` | Sin verificar |
| T4-02 | T4 | Recepcionado al abrir (en el servidor): solo Logística, solo avisos de RQ aprobado, una sola vez aunque dos personas abran a la vez; registra quién recepcionó, cierra los avisos de Logística y avisa al solicitante | Pruebas unitarias con doble de base: dos aperturas seguidas dan una sola recepción; un rol no Logística no la produce | Sin verificar |
| T4-04 | T4 | El comentario sobre un RQ avisa también al solicitante (además de a quien ya avisaba) | Prueba unitaria por los dos lados | Sin verificar |
| T4-05 | T4 | Los avisos del RQ salen del catálogo con referencia al RQ y se cierran por esa referencia, no por el comienzo del texto | Prueba: cerrar el aviso del RQ con código `-1` no cierra el de `-1x` | Sin verificar |
| T5-04 | T5 | Botón «Devolver» con motivo, visible solo para quien puede aprobar (aviso, Status y consolidado) | Captura con una cuenta que aprueba y otra que no | Sin verificar |
| T5-05 | T5 | El solicitante (o el administrador) edita un RQ Devuelto: ítems, cantidades, fecha y prioridad; los adjuntos ya subidos se conservan | Prueba de la ruta de edición y captura | Sin verificar |
| T5-06 | T5 | Reenviar: Devuelto pasa a Solicitado, avisa otra vez a los aprobadores y cierra el aviso de devolución; un Devuelto no se puede aprobar sin reenviar | Pruebas (el servidor rechaza aprobar un Devuelto) y captura de los avisos | Sin verificar |
| T6-01 | T6 | Servicio asignado, vía 1: al crear el servicio con supervisor operativo se le avisa (el creador no se avisa a sí mismo) | Prueba unitaria por los dos lados | Sin verificar |
| T6-02 | T6 | Servicio asignado, vía 2: al cambiar el responsable en los datos del servicio se avisa solo si la persona es nueva en el servicio | Prueba unitaria: mismo responsable no avisa | Sin verificar |
| T6-03 | T6 | Servicio asignado y retirado, vía 3 (Usuarios): se avisa solo a los nuevos al asignar y a quien se retira al quitar | Prueba unitaria | Sin verificar |
| T6-04 | T6 | RDT validado: se avisa al autor del RDT | Prueba unitaria por los dos lados | Sin verificar |
| T6-05 | T6 | RDT rechazado: se avisa al autor con el motivo; el aviso se cierra al validarse | Prueba unitaria | Sin verificar |
| T6-06 | T6 | RDT registrado (estructurado): se avisa a quienes lo validan, según la respuesta a la pregunta Q4; si Victor dice que no, el ítem pasa a «No aplica» | Prueba unitaria o nota de «No aplica» | Sin verificar |
| T6-07 | T6 | Avisos «falta subir…» con N° OT y cierre automático al subir, completar o quitar el documento; reasignar cierra el aviso del anterior; sin avisos de documentos de cierre ocultos (según Q5) | Pruebas unitarias en checklist y documentos | Sin verificar |
| T7-01 | T7 | Ciclo completo del RQ en vivo en `PS-0000`: crear, aprobar, Logística abre y queda Recepcionado, En almacén, Atendido; en cada paso el aviso llega a quien dice el catálogo y a nadie más, y el anterior se cierra (criterios 2 y 7) | Resumen de cierre con una captura por paso, por los dos lados | Sin verificar |
| T7-02 | T7 | Devolver y reenviar en vivo (criterio 10): motivo visible para el solicitante, reenvío avisa a los aprobadores, un Devuelto no se aprueba, quien no aprueba no ve el botón | Capturas por los dos lados | Sin verificar |
| T7-03 | T7 | Servicio asignado (3 vías), RDT validado, RDT rechazado con motivo y comentario sobre su RQ llegan al supervisor operativo (criterio 3) | Capturas de la bandeja del supervisor operativo | Sin verificar |
| T7-04 | T7 | «Entorno» fuera de un servicio y N° OT dentro de uno; grupo «Jefatura»; filtro «Tipo de aviso» (criterios 4 y 5) | Capturas | Sin verificar |
| T7-05 | T7 | Subir un documento del checklist cierra su aviso y la campana baja (criterio 6); con dos personas del mismo rol, el aviso por rol se cierra para ambas y el aviso por usuario es solo de una (regla P2) | Capturas de la campana antes y después, de las dos personas | Sin verificar |
| T9-01 | T9 | Cambiar mi contraseña desde Mi entorno: el usuario escribe la actual, la nueva y su confirmación, y queda cambiada; entra con la nueva y no con la anterior | Prueba de la ruta y del flujo completo; la comprobación en vivo está en T7-08 | Sin verificar |
| T9-07 | T9 | Celular propio para los 13 roles: quien no tiene número lo ingresa y quien lo tiene lo cambia o lo borra; solo texto de 6 a 20 caracteres con dígitos, espacios, `+`, guiones y paréntesis (formato propuesto, a confirmar en Q8); el servidor guarda solo el celular de la sesión y rechaza nombre, cargo, área o roles en el cuerpo | Pruebas de la ruta con un rol que antes no podía y con administrador; captura | Sin verificar |
| T9-08 | T9 | Cambiar mi correo: pide la contraseña actual y un correo nuevo válido, distinto del actual y no usado por otro usuario; envía la confirmación al correo nuevo; el correo cambia solo al confirmar y hasta entonces el perfil muestra «pendiente de confirmar» y sigue valiendo el anterior | Pruebas de la ruta (formato inválido 400, repetido 409, contraseña incorrecta 400 o 403, sin sesión 401) y captura del estado pendiente | Sin verificar |
| T7-08 | T7 | Cambio de contraseña en vivo con una cuenta de prueba (criterios 12 y 13): clave actual incorrecta rechazada, nueva corta rechazada, cambio correcto, cierre de sesión y entrada con la nueva; se anota la nueva clave solo en la memoria local de cuentas de prueba | Capturas del formulario, de cada mensaje y del ingreso con la nueva; nunca se muestra la clave | Sin verificar |
| T7-09 | T7 | Celular y correo en vivo (criterios 14 y 15): un rol que antes no editaba el perfil ingresa su celular; cambia su correo a otro alias de Victor, **Victor abre el enlace de confirmación** en su buzón, y la cuenta entra con el correo nuevo; el correo anterior ya no entra | Capturas del perfil antes y después, del estado pendiente y del ingreso con el correo nuevo; sin mostrar claves | Sin verificar |

### Datos y cálculos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T1-02 | T1 | Respaldo de los 18 avisos de la bandeja de Victor antes de tocarlos (id, texto, tipo, destinatario, estado) | `respaldo-avisos-victor.json` con 18 filas | Sin verificar |
| T1-03 | T1 | Los 18 avisos quedan cerrados como atendidos, sin borrar filas y sin aprobar ningún RQ (criterio 11) | Conteo antes y después; las filas siguen existiendo; ningún RQ cambió de estado | Sin verificar |
| T1-06 | T1 | Datos de prueba listos: `PS-0000` en Ejecución con Plan Maestro aprobado (o el plan B que defina el Orquestador), un RDT de prueba y registros marcados «PRUEBA» | Lista de datos de prueba en la evidencia | Sin verificar |
| T2-01 | T2 | Migración 108 (aditiva e idempotente): `proyecto_id` admite vacío, columnas `evento` y `referencia_id`, índices y relleno de `evento` en los avisos existentes por su texto; sin cambiar «Proyecto» en los datos. Revisada y aplicada por Victor | Archivo de la migración, revisión del verificador si está activo y confirmación de Victor con una consulta de comprobación | Sin verificar |
| T4-03 | T4 | `recepcionado_por` no se pisa al marcar Atendido (hoy lo pisa en la vía con acción; el flujo 05 dice que queda quien recepcionó) | Prueba unitaria | Sin verificar |
| T5-01 | T5 | Migración 109: el estado Devuelto es válido en la base y se guardan motivo, quién devolvió y cuándo. Revisada y aplicada por Victor | Archivo de la migración, revisión y confirmación de Victor | Sin verificar |
| T5-02 | T5 | Devuelto se reconoce en tipos, etiqueta, color, filtros y PDF; un Devuelto no se lee como Solicitado | Pruebas de `normalizarEstadoRequerimiento` y de los filtros | Sin verificar |
| T7-07 | T7 | Limpieza de los datos de prueba según la respuesta a la pregunta Q6, sin tocar datos reales | Lista de lo archivado o eliminado, con confirmación | Sin verificar |

### Permisos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T1-01 | T1 | Cuentas de prueba por rol, todas miembros de `PS-0000` (si no, la app responde «No tienes esta OT a cargo»): dos de Logística, jefe de proyectos, jefe de oficina técnica, un segundo supervisor operativo y supervisor de administración, además de las dos existentes. Nombre «PRUEBA <rol>». Requiere P4 | Lista de cuentas por rol sin claves y un inicio de sesión exitoso por cuenta | Sin verificar |
| T2-04 | T2 | Regla por usuario o por rol en lista, campana y autorización: un aviso por usuario lo ve solo esa persona aunque tenga rol; un aviso por rol es una cola compartida (P2) | Pruebas unitarias con dos usuarios del mismo rol | Sin verificar |
| T4-06 | T4 | Quién recibe y quién no recibe cada aviso del RQ está en el catálogo y se cumple; aprobar desde el aviso, el Status y el consolidado sigue igual | Pruebas unitarias por rol | Sin verificar |
| T8-05 | T8 | Artefacto «Matriz de permisos» actualizado con «Devolver RQ», «Corregir y reenviar RQ devuelto», «Cambiar mi contraseña», «Cambiar mi correo» y «Editar mi celular» (13 roles; la fila «Editar perfil extendido (propio)» se reemplaza o precisa; se lee el artefacto antes de publicar) | Enlace al artefacto y captura de las filas nuevas | Sin verificar |
| T9-03 | T9 | Permiso de perfil propio («cambiar mi contraseña», «editar mi celular» y «cambiar mi correo»): lo tienen los 13 roles; sin sesión no; `puedeEditarPerfilExtendido` deja de usarse en el perfil (administrador y jefe de proyectos no pierden nada); la función vive en un archivo propio y las rutas usan el id de la sesión, nunca uno enviado en el cuerpo | Prueba unitaria con los 13 roles, un rol desconocido y sin sesión | Sin verificar |

### UI / responsive / accesibilidad

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T1-07 | T1 | Maqueta de la bandeja (Entorno, N° OT, Jefatura, filtro por tipo, botón Devolver con motivo, RQ Devuelto) aprobada por Victor antes de la parte visual de T3 y T5 | `notificaciones-bandeja.html` y aprobación de Victor registrada | Sin verificar |
| T3-03 | T3 | El grupo «Jefatura» reemplaza a «Proyecto» en el filtro; los avisos viejos con «Proyecto» se leen como «Jefatura»; pruebas actualizadas | Prueba de `grupo-proceso` y captura del filtro | Sin verificar |
| T7-06 | T7 | La bandeja y el flujo de devolver se ven bien en móvil (390 px) y no hay errores en la consola | Capturas a 390 px y registro de la consola | Sin verificar |
| T9-04 | T9 | En el Perfil de Mi entorno, el chip «Editar mi perfil» pasa a verse para los 13 roles (hoy solo lo ven administrador y jefe de proyectos) y abre tres bloques: celular, correo (con la contraseña actual) y contraseña (actual, nueva y confirmación, con el ojo `InputContrasena`); el texto «Solo puedes editar tu celular» se corrige; reutiliza los componentes del perfil; se ve bien a 390 px. No requiere maqueta por reutilizar lo existente; Victor lo revisa en T7 | Captura a 1440 px y a 390 px con un rol que no edita el perfil y con otro que sí | Sin verificar |

### Estados vacío / carga / error

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T3-06 | T3 | Estados vacío, carga y error de la bandeja con el filtro nuevo, y ancho de 390 px | Capturas | Sin verificar |
| T5-07 | T5 | Estados vacío y error de devolver y corregir (motivo vacío, el RQ ya no está Solicitado, error de red) | Capturas y pruebas | Sin verificar |
| T9-05 | T9 | Mensajes del perfil propio en español claro: contraseña actual incorrecta, nueva muy corta, nueva igual a la actual, confirmación distinta, celular con formato inválido, correo inválido o ya usado, correo pendiente de confirmar, error de red y éxito; el botón se desactiva mientras guarda y el formulario se limpia al terminar | Capturas de cada mensaje y pruebas | Sin verificar |

### Validación en servidor / API

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T2-05 | T2 | La API de avisos acepta un aviso sin servicio («Entorno») y, si hay servicio, exige que el usuario lo tenga a cargo (según Q2); los avisos propios y «Entorno» no exigen servicio | Pruebas de la API por rol | Sin verificar |
| T5-03 | T5 | Acción devolver validada en el servidor: solo quien puede aprobar, solo desde Solicitado, motivo obligatorio de hasta unos 500 caracteres | Pruebas de la API: sin permiso 403, sin motivo 400, estado distinto 409 | Sin verificar |
| T9-02 | T9 | Ruta del servidor `PATCH` de contraseña propia: exige sesión, verifica la contraseña actual en el servidor (sin tocar la sesión del navegador), exige nueva de al menos 8 caracteres, distinta de la actual y con confirmación, y no escribe ninguna contraseña en respuestas ni registros | Pruebas de la API: sin sesión 401, actual incorrecta 400 o 403, nueva corta 400, igual a la actual 400, correcta 200; revisión de que no se registra ninguna clave | Sin verificar |

### Regresión

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T2-07 | T2 | Regresión de T2: `npm test`, `npm run lint` y `npx next build --webpack` en verde | Salida de los tres comandos | Sin verificar |
| T3-07 | T3 | Regresión de T3: las mismas tres comprobaciones | Salida | Sin verificar |
| T4-07 | T4 | Regresión de T4: las tres comprobaciones y aprobar desde aviso, Status y consolidado igual que antes; En almacén y Atendido siguen con botón | Salida y pruebas | Sin verificar |
| T5-08 | T5 | Regresión de T5: las tres comprobaciones y los RQ existentes se ven igual | Salida | Sin verificar |
| T6-08 | T6 | Regresión de T6: las tres comprobaciones y los avisos que ya existían (crear servicio, checklist, RDT subido, recursos sin tarifa) siguen llegando a quien llegaban | Salida y pruebas | Sin verificar |
| T9-06 | T9 | Regresión de T9: las tres comprobaciones, el ingreso con correo y contraseña sigue funcionando, la lista de usuarios del administrador sigue mostrando el correo de cada uno y el celular sigue igual para administrador y jefe de proyectos | Salida y pruebas | Sin verificar |

### Documentación y trazabilidad (sección agregada por este plan; la plantilla no la trae)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T8-01 | T8 | Flujo 04 reescrito: qué es un aviso, catálogo de eventos (quién lo dispara, a quién llega, texto, grupo y cuándo se cierra), estados, por usuario o por rol, «Entorno», grupos, y `informe.emitido` reservado (criterios 1 y 9) | Diff del flujo y revisión del Auditor | Sin verificar |
| T8-02 | T8 | Flujo 05: ciclo del RQ con Recepcionado al abrir, Devuelto, corregir y reenviar, comentarios y «Lee si» actualizado | Diff del flujo | Sin verificar |
| T8-03 | T8 | Flujos 06 (avisos del RDT) y 12 (cierre automático de «falta subir») | Diff de ambos | Sin verificar |
| T8-04 | T8 | Flujo 14 (filas nuevas de la tabla 2: Devolver, Corregir y reenviar, Cambiar mi contraseña, Cambiar mi correo y Editar mi celular; corrección de la fila 94 y de las líneas 183 y 184 según Q8; precisión sobre «Entorno») y flujos 02, 08 y 16; el flujo 03 (perfil de Mi entorno con su nuevo chip, y por si nombra el grupo «Proyecto») y el 07 (cambio de contraseña propia) | Diff y revisión | Sin verificar |
| T8-06 | T8 | Libro de hallazgos trasladado con el skill `trasladar-hallazgos` | Enlaces de destino en el libro | Sin verificar |
| T8-07 | T8 | Índices actualizados y `scripts/verificar-referencias.py` sin errores | Salida del script | Sin verificar |
| T8-08 | T8 | Coherencia de los flujos con el código: cada fila del catálogo del flujo 04 coincide con lo que hace la rama | Tabla de comparación en la evidencia | Sin verificar |

## Riesgos y bloqueos

1. **La app de pruebas es la de producción.** Toda escritura va solo en `PS-0000` con registros «PRUEBA». Mitigación: T1-06 y T7-07; el verificador antes de acciones irreversibles si está activo.
2. **Choque con Informes** (corrige el Spec; **ya integrado en `main` el 2026-10-17**, el riesgo baja a adaptarse a lo que dejó y a los cambios que aún traigan Permisos y Cronograma). Informes cambió `api/proyectos/route.ts`, `api/proyectos/[id]/datos/route.ts` (supervisor a cargo con columna propia), `confirmar-transicion/route.ts`, `api/rdts/partes/[id]/route.ts`, `permisos.ts`, `registro-accesos.ts` y `db/README.md`, y tiene `notificar-emision.ts`, que usa `crearNotificacionParaUsuario`. Mitigación: en esos archivos, cambios mínimos de una línea; la lógica va en archivos nuevos; T6 al final; `git merge main` antes de T6 si Informes ya entró; las funciones `crearNotificacion`, `crearNotificacionParaRol`, `crearNotificacionParaRoles` y `crearNotificacionParaUsuario` se mantienen como envoltorios compatibles; `informe.emitido` queda reservado; quien se integre segundo adapta (P5); la función de permiso de devolver va en un archivo propio y reutiliza `puedeDerivarRequerimientoLogistica`, para no editar `permisos.ts`.
3. **Numeración de migraciones.** Las ramas de Informes (098 a 102) y Cronograma (107) pueden chocar con 108 y 109. Se reconfirma antes de escribir y antes de aplicar.
4. **`proyecto_id` opcional.** Listados, enlaces y la comprobación de alcance asumen un servicio en cada aviso; la función de alcance recibe un texto obligatorio. Mitigación: T2-05 y pruebas; los avisos propios y «Entorno» no exigen servicio.
5. **Estado compartido por rol.** Una persona de Logística que recepciona o cierra un aviso lo cierra para todas, y la campana baja a las compañeras. Es lo decidido en P2, pero sorprende: se verifica con dos cuentas (T1-05, T7-05).
6. **Recepcionado al abrir y concurrencia.** Si dos personas abren a la vez, debe registrarse una sola recepción: el cambio se hace en el servidor con una actualización condicional «solo si sigue Aprobado». La pantalla debe esperar la respuesta antes de refrescar.
7. **Filtros anidados de la base.** La lista y la campana hoy usan un filtro «por usuario o por rol» que mezcla ambos. La recomendación es hacer dos consultas (por usuario; por rol y sin usuario) y unirlas en el código, porque un filtro anidado no se puede validar con los dobles de prueba. Lo real de la base no se pudo ejecutar en el diseño (por confirmar en T7).
8. **«Ver como» no cambia la bandeja** (M1): las pruebas de avisos exigen iniciar sesión con cada cuenta.
9. **Crear usuarios de prueba envía un correo de invitación** al correo indicado (la app usa la invitación de Supabase y luego fija la contraseña). Riesgo: mandar correos a terceros. Mitigación: solo buzones de Victor (P4 y pregunta de pre-autorización); el límite de envíos de invitación queda por confirmar. No existe «desactivar usuario»: solo eliminar, y eliminar deja los avisos del usuario sin dueño.
10. **Navegador ocupado.** Otro agente lo usa a ratos. T1 y T7 se programan cuando Victor confirme que está libre.
11. **`PS-0000` podría no estar en Ejecución con Plan Maestro aprobado**, y el RDT lo exige (flujo 06). Se comprueba en T1-06; si no, el Orquestador define un plan B.
12. **Flujos con cambios sin commitear de otras sesiones** (06, 09, 12, 14, 16, 18, 19, 20 y otros). Ningún agente los toca hasta T8, y T8 solo tras confirmar que ya se commitearon; el commit de T8 incluye únicamente sus líneas.
13. **Aviso «atender» que aprueba.** `atender` sobre un aviso de aprobación de RQ, con un rol que aprueba, **aprueba el RQ**. Nunca se usa para limpiar los 18 avisos (T1-03).
14. **Seguridad por filas (095) y cliente de sesión.** `db/095_cerrar_lectura_directa.sql` quita lecturas abiertas, pero probablemente no está aplicada: por confirmar. Fuera de alcance; la migración 108 no cambia políticas.
15. **Acciones irreversibles** (aplicar migraciones, cerrar avisos, crear o eliminar usuarios) pasan por el verificador si está activo.
16. **Estado Devuelto leído como Solicitado.** Hoy `normalizarEstadoRequerimiento` devuelve «Solicitado» para cualquier estado que no conoce: un Devuelto sería aprobable. Mitigación: T5-02.
17. **Cambiar la contraseña (T9) y la autenticación de Supabase.** Supabase puede exigir reautenticación para `updateUser`, y verificar la contraseña actual con el cliente de la sesión puede alterar las cookies. Mitigación: verificar la actual con un cliente sin sesión persistente y, si `updateUser` pide reautenticar, cambiar la clave en el servidor con la misma llamada de administrador que ya usa la creación de usuarios (`updateUserById`), siempre con el id de la sesión y nunca con uno del cuerpo. El Worker confirma el mecanismo con una prueba antes de cerrar T9-02; si ninguno sirve, se detiene y se consulta. Prueba repetida de la contraseña actual: queda el límite de intentos de Supabase (por confirmar).
18. **Cuentas de prueba y claves.** Probar el cambio de contraseña (T7-08) deja una clave nueva en una cuenta de prueba: se anota solo en la memoria local de cuentas, nunca en el repositorio, el chat ni capturas.
19. **Cambiar el correo (T9-08).** El correo es el identificador de ingreso y solo vive en el sistema de autenticación (la tabla de perfiles no lo guarda; el listado de usuarios lo lee de ahí). Un error al escribirlo dejaría a la persona sin poder entrar. Mitigación: pedir la contraseña actual, confirmar el correo nuevo por enlace (`updateUser` de Supabase) y mantener el anterior hasta confirmar. Por confirmar con una prueba del Worker: si la confirmación llega a ambos buzones (opción «secure email change» de Supabase), a qué dirección redirige el enlace (hoy `NEXT_PUBLIC_SITE_URL` y la plantilla de correo) y si la sesión sigue abierta después. Si el proyecto de Supabase no envía bien esos correos, T9-08 se detiene y se consulta a Victor. Con los alias `+` del plan, el enlace llega al mismo buzón de Victor, que es quien lo abre en T7-09.

## Hallazgos adicionales del Planner

Encontrados al planificar. **El Orquestador los pasó al libro el 2026-10-17:** los que son defectos de código quedan cubiertos por ítems de la Punch List (se indica el ítem); el 6 es la mejora de trabajo M2; el 3, el 4 y el 5 son reportes a Victor (van a «Elementos postergados»); los que dependen de una pregunta (7 a 13) están como reglas pendientes de decisión R4 a R7. Destino propuesto entre paréntesis.

1. **Aviso «Nuevo requerimiento» directo sin acciones.** Cuando un jefe crea un RQ, nace Aprobado y avisa a Logística con un texto que no coincide con el que reconocen las pantallas, así que Logística no ve el botón de recepcionar en ese aviso (corrige T3-05; flujo 05).
2. **No existe edición de RQ.** Solo se puede crear y eliminar; «corregir y reenviar» exige construirla (T5-05; flujo 05).
3. **`atender` aprueba el RQ** si el aviso es de aprobación y el rol aprueba; no hay acción masiva para limpiar avisos (reporte a Victor; sin cambio de código).
4. **Avisos huérfanos al eliminar un usuario:** se ponen en vacío el destinatario y el remitente; quedan sin dueño o visibles por rol (reporte a Victor).
5. **Seguridad por filas 095 y cliente de sesión:** por confirmar si está aplicada (reporte a Victor).
6. **Crear un usuario envía un correo de invitación** (mejora de trabajo: advertirlo en el protocolo de cuentas de prueba, `03-aprendizaje-continuo/`).
7. **El cierre de avisos de RQ por comienzo del texto** (`Requerimiento <código>%`) puede cerrar el RQ equivocado si un código es prefijo de otro; hoy lo mitiga que el código lleva secuencia de 3 dígitos (T4-05 lo reemplaza por referencia).
8. **Avisos «falta subir X para poder cerrar»** de documentos de cierre que el flujo 12 oculta: nadie los puede atender (pregunta Q5).
9. **`recepcionado_por` se pisa al Atender** en la vía con acción; el flujo 05 dice que queda quien recepcionó (T4-03; flujo 05).
10. **El RDT estructurado no avisa a nadie al registrarse**, y solo el RDT subido como archivo avisa a Administración (pregunta Q4; flujo 06).
11. **Enviar mensaje no valida el alcance** aunque el flujo 14 (línea 187) dice que sí lo exige; además la pantalla «Entorno» preselecciona el primer servicio y el primer rol del usuario (pregunta Q2).
12. **La vía de estado sin `accion` no la usa ninguna pantalla** (los 3 llamadores envían `accion`), por lo que se puede quitar sin efecto visible; por confirmar con una búsqueda en T4.
13. **El título «Entorno · Proyecto» de Mi entorno cambia a «Entorno · Jefatura»** con el renombre (pregunta Q3).
14. **(Orquestador, 2026-10-17, al agregar la contraseña propia.)** «Editar mi perfil» solo lo ven el administrador y el jefe de proyectos (`puedeEditarPerfilExtendido`, flujo 14 línea 94); los otros 11 roles solo ven «Mi perfil» y no pueden cambiar nada, ni siquiera el celular. No hay «olvidé mi contraseña» ni cambio de contraseña en `src/`. La contraseña la fija el administrador al crear el usuario y el correo de invitación no la trae (`api/admin/usuarios/route.ts`). Se cubre con T9; los otros dos puntos quedan en «Elementos postergados».

## Tabla verificada de flujos

Verificación de la columna «Dice hoy» del Spec contra los flujos y el código (2026-10-17). Veredicto: ✓ confirmado · CORREGIDA = lo que dice «hoy» es otra cosa.

| # | Tema | Lo que realmente dice hoy (fuente) | Veredicto | Documentos a actualizar |
|---|---|---|---|---|
| 1 | Quién recibe el aviso al aprobar un RQ | Flujo 04, línea 9: «Al aprobar un RQ se notifica solo a `supervisor_logistica`. No se crea un aviso "atendida" al aprobador.» Flujo 05, línea 14: «Aprobación / Notificación / Status / Geren deriva a Logística» | ✓ | 04, 05 |
| 2 | Recepcionado | Flujo 05 sí lo menciona (línea 5 estados; 27 «Personal Logístico solo después de Recepcionado (quien recepcionó)»; 31 columna Acción del consolidado; 20 «Actualizar estado: administrador y logística»; flujo 14, línea 115) pero **no dice cómo se llega desde el aviso** | CORREGIDA | 05, 04, 14 |
| 3 | Grupo «Proyecto» | **Ningún flujo lo nombra:** está solo en el código (`grupo-proceso.ts`). El flujo 02, línea 7, ya dice que el área PR («Proyecto») pasó a JF («Jefatura»). El flujo 03 no se leyó: el Documentador lo revisa | CORREGIDA | 04, 02 (03 por revisar) |
| 4 | Aviso sin servicio | **No está en ningún flujo.** El flujo 14 dice, línea 187, «Enviar mensaje… Sí (la notificación queda ligada a la OT del contexto)»; línea 188, «Marcar como visto / revisar / atender… Sí (la ruta resuelve el `proyecto_id` de la notificación)»; línea 186, «Ver notificaciones propias (por usuario o por rol)… No». El flujo 16 (líneas 204 y 224) dice que las notificaciones van a `/notificaciones`, sin contradecir | CORREGIDA (contradicción nueva A) | 04, 16, 14 |
| 5 | Servicio asignado | «No avisa» **no está escrito** en el flujo 02 ni en el 08 (el 08 trata solo adjudicar, archivar y transición): es comportamiento del código | CORREGIDA | 04, 02, 08 |
| 6 | RDT validado o rechazado | Flujo 06, línea 17: «Notificación al subir: solo Administración.» Matiz: aplica al RDT subido como archivo; el RDT estructurado no avisa a nadie | ✓ | 06, 04 |
| 7 | Comentario sobre un RQ | Solo en el código: el flujo 05 no dice a quién avisan los comentarios | Solo código | 05, 04 |
| 8 | «Falta subir…» | Solo en el código; flujo 12, línea 29: «Completar = marca por check (manual)» | Solo código | 12, 04 |
| 9 | Estado de un RQ (dos caminos) | Solo en el código; flujo 05, línea 20, solo describe permisos | Solo código | 05, 04 |
| 10 | Devolver un RQ | «No existe» sigue vigente: flujo 14, línea 116, solo trae «Derivar RQ a logística»; el flujo 05 (línea 2) y el README (línea 19) prometen «aprueba o rechaza» sin describir el rechazo. **Corrección:** el jefe de oficina técnica **no puede ni comentar** (flujo 14, línea 114; `permisos.ts`, línea 480): solo aprobar | ✓ con corrección | 05 (estado «Devuelto», «Corregir y reenviar», «Lee si: devolver»), 14 (tabla 2) y artefacto |
| 11 | Perfil propio (ampliaciones de Victor, 2026-10-17) | Flujo 14, línea 94: «Editar perfil extendido (propio)» solo administrador y jefe de proyectos; línea 183, el jefe de proyectos «puede… editar su perfil»; línea 184, el jefe de oficina técnica «deja de… editar su perfil». Cambiar contraseña y correo propios no están en ningún flujo; el flujo 02 solo dice «crear (contraseña + invite)» y el 07 solo describe el ingreso | **Contradicción nueva** (Q8) | 14 (fila 94 y líneas 183 y 184), 03, 02, 07 y artefacto |

**Filas nuevas del flujo 14 (tabla 2)** que propone este plan, a aprobar en el Gate 1: «Devolver RQ» con el mismo reparto que «Derivar RQ a logística» (administrador, jefe de proyectos y jefe de oficina técnica) y «Corregir y reenviar RQ devuelto» (el solicitante del RQ y el administrador). Se actualizan en la misma tarea el flujo 14 y el artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT).

**Contradicciones y puntos nuevos a consultar con Victor antes de editar un flujo:**

- **A.** Flujo 14 (187 y 188) exige tener el servicio a cargo para enviar o atender un aviso, pero «Entorno» no tiene servicio y los avisos propios (servicio asignado, RDT rechazado) tampoco; además el código hoy no valida el alcance al enviar. Pregunta Q2.
- **B.** La regla P2 (por usuario o por rol) y la visibilidad no están escritas en ningún flujo: se documentan en el 04.
- **C.** Aviso a los validadores al registrar un RDT estructurado: hoy no existe. Pregunta Q4.
- **D.** `recepcionado_por` se pisa al marcar Atendido, contra el flujo 05 (línea 27). Se corrige el código; el flujo ya dice lo correcto.
- **E.** Avisos de documentos de cierre que el flujo 12 (línea 31) oculta. Pregunta Q5.
- **F.** El renombre «Jefatura» cambia también el título «Entorno · Proyecto». Pregunta Q3.

## Consulta única para el Gate 1

Para que Victor responda de una vez. Cada pregunta trae un ejemplo y la recomendación del Planner.

**i. Datos de prueba.** Se usa `PS-0000` (debe estar en Ejecución con Plan Maestro aprobado; T1-06 lo comprueba). Todo lo que se cree se marca «PRUEBA» y se puede archivar. Se necesitan cuentas de prueba: unas 6 nuevas (dos de Logística, jefe de proyectos, jefe de oficina técnica, un segundo supervisor operativo y supervisor de administración) además de las dos existentes. **P4: Victor indica los correos** (buzones suyos). Cada cuenta recibe un correo de invitación al crearse.

**ii. Pre-autorizaciones** (para no volver a preguntar durante el plan):

- Iniciar sesión con las cuentas de prueba y usar las herramientas de navegador en T1 y T7, sin leer ni mostrar claves.
- Crear y eliminar usuarios de prueba (advertencia: crear envía un correo de invitación; solo a buzones de Victor).
- Cerrar los 18 avisos viejos con respaldo previo y sin borrar filas.
- Crear un servicio de prueba nuevo para probar la vía 1 de «servicio asignado» (consume el siguiente N° OT) y archivarlo al terminar.
- Copiar el `.env.local` principal al worktree nuevo (ya autorizado, se menciona por completitud).

**iii. Rama y worktree.** Autorizar `local-worker-7` y `.worktrees/local-worker-7`, creados desde `main` (hoy `69ebf94`, con Informes ya integrado).

**iv. Migraciones.** La 108 (después de T2) y la 109 (después de T5) las aplica Victor a mano. Son aditivas y no borran nada.

**v. Preguntas:**

- **Q1. Cómo funciona «devolver» un RQ.** Ejemplo: Pedro pide 10 bolsas de cemento; el jefe de proyectos cree que son 5, lo devuelve escribiendo el motivo; Pedro recibe el aviso con el motivo, corrige la cantidad y lo reenvía; los jefes reciben el aviso otra vez. Recomendación: quien devuelve es quien ya puede aprobar (administrador, jefe de proyectos y jefe de oficina técnica); el motivo es obligatorio (hasta unos 500 caracteres) y se guarda en el RQ; solo se puede devolver mientras esté Solicitado; el solicitante (o el administrador) corrige ítems, cantidades, fecha y prioridad, sin cambiar los adjuntos, y reenvía; un RQ Devuelto no se puede aprobar hasta reenviarse. ¿Se aprueba así?
- **Q2. Contradicción en el flujo 14.** El flujo exige tener el servicio a cargo para enviar o atender un aviso, pero «Entorno» y los avisos propios no tienen servicio. Recomendación: hacer cumplir lo escrito cuando el aviso es de un servicio (solo para quien lo tiene a cargo), sin exigirlo en «Entorno» ni en los avisos propios, y corregir el flujo 14 con esa precisión. ¿Se aprueba?
- **Q3. Renombre de «Proyecto» a «Jefatura».** También cambiaría el título «Entorno · Proyecto» de Mi entorno por «Entorno · Jefatura». Recomendación: sí, es lo coherente con el área JF. ¿Se aprueba?
- **Q4. RDT registrado en pantalla (estructurado).** Hoy no avisa a nadie; solo el RDT subido como archivo avisa a Administración. Ejemplo: el supervisor registra su RDT del día y nadie de quien lo valida se entera. Recomendación: avisar a quienes pueden validarlo. ¿Sí o no?
- **Q5. Avisos de documentos de cierre.** Hoy se generan avisos «falta subir X para poder cerrar» de documentos de cierre que el flujo 12 oculta, así que nadie puede atenderlos. Recomendación: dejar de generarlos. ¿Sí o no?
- **Q6. Qué hacer con las cuentas y el servicio de prueba al terminar.** Recomendación: conservar las cuentas (sirven para la capacitación que sigue; hoy solo se pueden eliminar, no desactivar), eliminar los datos marcados «PRUEBA» y archivar el servicio de prueba nuevo. ¿Se aprueba o se eliminan también las cuentas?
- **Q7. Cambiar mi contraseña (ampliación).** Ejemplo: Pedro recibe la invitación, entra con la clave que le dio el administrador y quiere una propia; en Mi entorno, Perfil, pulsa «Cambiar contraseña» y escribe la actual, la nueva y la repite. Recomendación: pedir la contraseña actual (así nadie que encuentre la sesión abierta puede dejar a Pedro fuera de su cuenta), mínimo 8 caracteres como al activar la cuenta, y que lo vean los 13 roles. No se obliga a cambiarla en el primer ingreso (queda como mejora futura). ¿Se aprueba?
- **Q8. Celular y correo propios para todos (contradice lo escrito).** Hoy el flujo 14 dice que solo el administrador y el jefe de proyectos editan su perfil, y que el jefe de oficina técnica «deja de editar su perfil» (decisión anterior tuya). Tú pediste que todos puedan; este plan lo hace así y corrige el flujo 14 y el artefacto «Matriz de permisos» en la misma tarea. Ejemplo: Pedro, supervisor operativo, no tiene celular registrado; entra a su perfil, escribe su número y queda guardado; si cambia de correo, escribe el nuevo con su contraseña y confirma desde el buzón nuevo. Recomendación: sí para los 13 roles, incluido el jefe de oficina técnica; el correo nuevo solo rige al confirmarlo por enlace; el celular admite dígitos, espacios, `+`, guiones y paréntesis (6 a 20 caracteres). ¿Se aprueba, incluido el jefe de oficina técnica?

**Operativo, no es pregunta para Victor:** dónde corre T7 (servidor local del worktree contra la misma base; el Orquestador lo confirma).

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-16 | Objetivo: ordenar las notificaciones y servir al supervisor operativo antes de capacitarlo; documentar y verificar el ciclo del RQ, mejorar lo que se pueda y mantener un solo estándar | Victor |
| 2026-10-16 | Recepcionado pasa solo cuando Logística abre el aviso | Victor |
| 2026-10-16 | El grupo «Proyecto» de las notificaciones pasa a llamarse «Jefatura» | Victor |
| 2026-10-16 | No hay personas reales con esos roles: se pueden crear usuarios de prueba; Victor da los correos | Victor |
| 2026-10-16 | Gate Spec aprobado. Las claves de las cuentas de prueba por rol se guardan solo en la memoria local del Orquestador (tabla creada, cuentas aún sin crear) | Victor |
| 2026-10-16 | El navegador de Playwright usado en las verificaciones se cerró para que otro agente use Chrome; se reabre solo cuando haga falta | Victor / Orquestador |
| 2026-10-16 | P1: sí se crea «devolver» un RQ en este plan (la recomendación del Orquestador era no abrirlo) | Victor |
| 2026-10-16 | P2: aviso por rol = cola compartida; aviso por usuario = informativo y solo de esa persona | Victor |
| 2026-10-16 | P3: limpiar los 18 avisos viejos de su bandeja (orden directa): respaldar y cerrar como atendidos, sin borrar filas | Victor |
| 2026-10-16 | P5: este plan parte de `main`; Informes o este plan se adaptan según cuál se integre primero | Victor |
| 2026-10-16 | Se verificó en solo lectura (código y bandeja en vivo); no se escribió en la app | Orquestador |
| 2026-10-17 | **Propuesta del Planner, a aprobar en el Gate 1:** un solo Worker de código (`local-worker-7`) para T2 a T6, más un Worker de verificación para T1 y T7; las tandas comparten el módulo central y las pantallas de avisos | Planner (propuesta) |
| 2026-10-17 | **Propuesta:** rama `local-worker-7` y worktree `.worktrees/local-worker-7` desde `main`; no se reutiliza `local-worker-4` sin confirmar. **Ajuste del Orquestador:** `main` ya no está en `628918a` sino en `69ebf94` (Informes integrado) | Planner (propuesta) / Orquestador |
| 2026-10-17 | Revisión del Orquestador: Punch List de 59 ítems verificada ítem por ítem (T1: 7, T2: 7, T3: 7, T4: 7, T5: 8, T6: 8, T7: 7, T8: 8), estado de ramas y migraciones contrastado con `git`, hallazgos del Planner pasados al libro, estados desactualizados corregidos. Operativo: T7 corre en servidor local del worktree contra la misma base | Orquestador |
| 2026-10-17 | **Ampliación de alcance:** el usuario invitado puede cambiar su propia contraseña desde Mi entorno (hoy solo el administrador y el jefe de proyectos editan el celular; nadie cambia contraseña). Se suma la tanda T9 y el ítem T7-08. Pregunta Q7 para el Gate 1 | Victor |
| 2026-10-17 | **Segunda ampliación:** todos los usuarios pueden ingresar o cambiar su celular y su correo electrónico desde Mi entorno. T9 pasa a 8 ítems y se suma T7-09: el plan queda en 9 tandas y 69 ítems. Contradice el flujo 14 (fila 94 y línea 184); pregunta Q8 para el Gate 1 | Victor |
| 2026-10-17 | **Gate 1 aprobado.** Victor respondió «si ok, procede con la implementación, te quedarás trabajando solo»: el Orquestador lo lee como aprobación del plan, la Punch List (69 ítems en 9 tandas), la asignación de modelos (Sonnet, esfuerzo medio, sin Opus), las pre-autorizaciones (rama y worktree `local-worker-7`, usuarios de prueba con alias de su buzón, cierre de los 18 avisos con respaldo, servicio de prueba, migraciones 108 y 109 que aplica Victor a mano) y las recomendaciones de Q1 a Q8, que quedan como sus decisiones (R4 a R7, R9 y R10 pasan a `Registrada`). Cualquier duda de alcance se le devuelve; las migraciones y el enlace de confirmación de T7-09 requieren una acción suya | Victor |
| 2026-10-17 | Respuesta a P4: los correos de las cuentas de prueba serán alias `+` del buzón `victor.sup22@gmail.com` (`+logistica1`, `+logistica2`, `+jefeproy`, `+ofitec`, `+supop2`, `+admin2`); se prueba con la primera cuenta antes de crear las demás y, si la app o Supabase rechazan el `+`, se usan los otros buzones de Victor. Confirmado con el Gate 1 | Victor (aprobó) |
| 2026-10-17 | **Propuesta:** migraciones 108 (notificaciones, tras T2) y 109 (RQ Devuelto, tras T5), aplicadas por Victor; se reconfirma la numeración por el choque posible con Informes y Cronograma | Planner (propuesta) |
| 2026-10-17 | **Propuesta:** columna extra `referencia_id` en `notificaciones` (id del RQ, RDT o documento) para cerrar avisos por referencia y no por el comienzo del texto; los avisos viejos se siguen cerrando por texto | Planner (propuesta) |
| 2026-10-17 | **Propuesta:** «Jefatura» se resuelve al leer, sin actualizar filas: los avisos viejos con «Proyecto» se leen como «Jefatura» y los nuevos se escriben con «Jefatura». El grupo de un aviso por usuario es el del rol de la persona (un supervisor operativo ve «Supervisión operativa») | Planner (propuesta) |
| 2026-10-17 | **Propuesta:** Recepcionado al abrir se hace en el servidor (`revisar`), solo para Logística y solo sobre avisos de RQ aprobado, con actualización condicional «solo si sigue Aprobado», para que sea una sola vez aunque abran dos personas | Planner (propuesta) |
| 2026-10-17 | **Propuesta:** «corregir y reenviar» exige una edición de RQ nueva, permitida solo en estado Devuelto al solicitante o al administrador; motivo de devolución de hasta unos 500 caracteres; la función de permiso va en un archivo propio y reutiliza `puedeDerivarRequerimientoLogistica` | Planner (propuesta) |
| 2026-10-17 | **Propuesta:** la limpieza de los 18 avisos (P3) se hace por id con respuesta fija y respaldo previo; nunca con `atender` sobre un aviso de aprobación de RQ aún Solicitado (aprobaría el RQ): esos se dejan y se reportan, o se cierran con un SQL que prepara el Worker y aplica Victor | Planner (propuesta) |
| 2026-10-17 | **Propuesta:** T6 va al final del código para tocar lo más tarde posible los archivos que comparte con Informes; `git merge main` antes de T6 si Informes ya entró | Planner (propuesta) |

## Enlaces a progreso y evidencia homónimos

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md` (se crea al iniciar T1).
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/` (incluye `respaldo-avisos-victor.json`).
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md` (la escribe el Auditor).
- Briefs de las tandas: `docs/02-trabajo-activo/01-planes/2026-10-16-notificaciones-estandar-y-supervisor-operativo-briefs/` (plantilla `13-brief-de-tanda.md`, 8 KB como máximo, unas 80 llamadas por Worker), con `resultados/<tanda>.md` para el resumen de cierre de cada una (plantilla `12-resumen-de-cierre-de-tanda.md`). Aún sin crear.

## Libro de hallazgos

Un hallazgo se anota en el momento en que ocurre. Los Workers dejan los suyos en su resumen de cierre y el Orquestador los pasa aquí; al final, el Documentador traslada cada fila a su destino. Estados: `Registrada` → `Trasladada` · `Descartada` · `Pendiente de decisión`.

### Mejoras (de trabajo)

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| M1 | 2026-10-16 | Orquestador, diagnóstico | El «Ver como» solo cambia la pantalla: la bandeja y la campana siguen siendo las del usuario real. Para verificar avisos de otro rol hay que iniciar sesión con su cuenta. | `03-aprendizaje-continuo/` | Registrada | — |
| M2 | 2026-10-17 | Planner (hallazgo 6) | Crear un usuario de prueba envía un correo de invitación al correo indicado: usar solo buzones de Victor y advertirlo en el protocolo de cuentas de prueba. | `03-aprendizaje-continuo/` | Registrada | — |
| M3 | 2026-10-17 | Orquestador, revisión | El «Sin choque hoy» del Spec se redactó por impresión y falló; el Planner lo corrigió con `git diff` entre ramas, y al revisar se encontró que la base (`main`) ya había avanzado. Antes de afirmar que hay o no choque con otros planes, y antes de fijar la base de una rama, comprobar con `git branch --merged main`, `git diff --name-only main...<rama>` y el commit actual de `main`, el mismo día. | `03-aprendizaje-continuo/` | Registrada | — |

### Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| R1 | 2026-10-16 | Victor, Spec | Logística abre el aviso de un RQ aprobado y el RQ pasa solo a Recepcionado; se registra quién lo recepcionó y se avisa al solicitante | Flujo 05 (y 04, 14) | Registrada | — |
| R2 | 2026-10-16 | Victor, Spec | El grupo de notificación «Proyecto» se llama «Jefatura» (el título «Entorno · Proyecto» también: pregunta Q3) | Flujo 04 (y 02) | Registrada | — |
| R3 | 2026-10-16 | Victor, Spec (P2) | Un aviso por rol es una cola compartida (el primero que lo atiende lo cierra para todos); un aviso por usuario es informativo y solo de esa persona | Flujo 04 | Registrada | — |
| R4 | 2026-10-17 | Orquestador, Gate 1 (Q1) | Devolver un RQ: lo hace quien ya puede aprobar, con motivo obligatorio (hasta unos 500 caracteres); solo desde Solicitado; el solicitante o el administrador lo corrige y reenvía; un Devuelto no se aprueba sin reenviarse. Alcance decidido por Victor (P1); el detalle lo confirma en el Gate 1 | Flujos 05, 04 y 14 | Registrada | — |
| R5 | 2026-10-17 | Planner (A), Gate 1 (Q2) | El flujo 14 exige tener el servicio a cargo para enviar o atender un aviso, pero «Entorno» y los avisos propios no tienen servicio. Propuesta: exigirlo solo cuando el aviso es de un servicio | Flujos 14 y 04 | Registrada | — |
| R6 | 2026-10-17 | Planner (C), Gate 1 (Q4) | Un RDT registrado en pantalla avisa a quienes pueden validarlo (hoy solo avisa el RDT subido como archivo, a Administración) | Flujos 06 y 04 | Registrada | — |
| R7 | 2026-10-17 | Planner (E), Gate 1 (Q5) | Dejar de generar avisos «falta subir…» de documentos de cierre que el flujo 12 oculta | Flujos 12 y 04 | Registrada | — |
| R8 | 2026-10-17 | Victor, ampliación | Todo usuario invitado, de cualquiera de los 13 roles, puede cambiar su propia contraseña desde Mi entorno (hoy no puede: solo el administrador crea o fija la clave) | Flujos 14 (tabla 2), 03, 02 y 07, y artefacto «Matriz de permisos» | Registrada | — |
| R10 | 2026-10-17 | Victor, segunda ampliación | Todo usuario de los 13 roles puede ingresar o cambiar su propio celular y su propio correo desde Mi entorno (hoy solo administrador y jefe de proyectos editan el celular; el jefe de oficina técnica «deja de editar su perfil» según el flujo 14). Nombre, cargo, área y roles siguen siendo del administrador | Flujo 14 (fila 94 y línea 184), flujos 03, 02 y 07, y artefacto «Matriz de permisos» | Registrada | — |
| R9 | 2026-10-17 | Orquestador, Gate 1 (Q7) | Para cambiar la contraseña se pide la actual, además de la nueva y su confirmación (mínimo 8 caracteres, distinta de la actual) | Flujos 07 y 03 | Registrada | — |

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

1. ~~El Orquestador revisa este plan y pasa al libro los hallazgos del Planner~~ (hecho el 2026-10-17). Los briefs de las tandas los escribe el Orquestador cuando toque lanzar cada una.
2. **Victor revisa el plan y responde la «Consulta única para el Gate 1»** (autorizaciones, rama, migraciones y preguntas Q1 a Q8) y la pendiente P4 (correos de las cuentas de prueba). Con sus respuestas, el Orquestador marca la aprobación en la Punch List y en la tabla de modelos, y registra las decisiones.
3. Con el Gate 1 aprobado: el Worker git crea `local-worker-7` y su worktree; arranca T1 (cuando el navegador esté libre) y T2 en paralelo.

## Informe de Auditoría

Pendiente. Se escribe en `docs/02-trabajo-activo/04-auditoria/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md` (formato de `06-informe-auditoria.md`); no se escribe dentro del plan.

## Mensaje de cierre

Pendiente (formato de `09-cierre.md`).

### Tabla de esfuerzos reales usados

| Fase | Modelo asignado | Esfuerzo default | Esfuerzo usado | Cambio autorizado |
|---|---|---|---|---|
| T1 | Sonnet | Medio | pendiente | — |
| T2 | Sonnet | Medio | pendiente | — |
| T3 | Sonnet | Medio | pendiente | — |
| T4 | Sonnet | Medio | pendiente | — |
| T5 | Sonnet | Medio | pendiente | — |
| T6 | Sonnet | Medio | pendiente | — |
| T9 | Sonnet | Medio | pendiente | — |
| T7 | Sonnet | Medio | pendiente | — |
| T8 | Sonnet / Haiku | Medio | pendiente | — |

## Elementos postergados propuestos para planes futuros

- Guía y capacitación de uso para los supervisores operativos (el plan que sigue a este).
- Opción de «desactivar usuario» (hoy solo se puede eliminar, y eliminar deja avisos sin dueño).
- Revisar la seguridad por filas de la base (migración 095) y si la app depende del cliente de sesión.
- Actualizar en la base los avisos viejos con grupo «Proyecto», si algún día estorba la lectura con traducción.
- Unificar las dos pantallas que muestran avisos en un solo componente.
- Avisos por correo, notificaciones push o WhatsApp (la app no los tiene; por confirmar si Victor los quiere).
- Acción masiva y segura para limpiar avisos: hoy «atender» sobre un aviso de aprobación de RQ, con un rol que aprueba, **aprueba el RQ**; por eso la limpieza de los 18 avisos se hace por id (reporte a Victor).
- Avisos sin dueño al eliminar un usuario: se vacían el destinatario y el remitente (reporte a Victor; lo resuelve «desactivar usuario»).
- «Olvidé mi contraseña» (recuperación por correo): la app no lo tiene; si alguien pierde la clave hoy debe pedírsela al administrador.
- Obligar a cambiar la contraseña en el primer ingreso.
