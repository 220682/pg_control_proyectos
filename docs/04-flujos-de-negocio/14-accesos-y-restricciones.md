# 14 — Accesos y restricciones

Tabla visual con **columnas = roles** y **filas = accesos**, construida recorriendo de una sola pasada las funciones de `py_control_proyectos_web/src/lib/permisos/permisos.ts`, cruzadas con el nav lateral (`src/lib/config/nav-proyecto.ts`) y los chips del entorno (`src/lib/notificaciones/grupo-proceso.ts`).

Pedido por Victor el 2026-09-16. Construida el 2026-09-20 como paso previo al Sub-lote 2 (alcance por servicio), pedido explícito de Victor: "primero definir qué puede hacer cada rol".

**Regla:** cada vez que se agrega un chip/acceso nuevo al sistema, esta tabla debe actualizarse.

## Cómo leer la tabla

- **✓** el rol tiene el acceso. **—** no lo tiene.
- **Admin** siempre tiene bypass total — no se repite el razonamiento fila por fila salvo que sea la única excepción real.
- **Requiere OT a cargo**: columna que anticipa el Sub-lote 2 (`docs/02-trabajo-activo/01-planes/2026-09-20-sub-lote-2-alcance-proyecto.md`). "Sí" = la acción escribe sobre una OT concreta y, cuando el sub-lote esté implementado, además del rol hará falta tener esa OT asignada en `proyecto_miembros`. "No (lectura)" = la lectura no se restringe por diseño, todos los roles habilitados ven todas las OT. "No" = la acción no está ligada a ninguna OT (usuarios, catálogos globales, contenedores).
- Roles, columna por columna: Admin=administrador, JP=jefe_de_proyectos, JOT=jefe_de_oficina_tecnica, SOT=supervisor_oficina_tecnica, Plnr=planner, SCo=supervisor_costos, JCo=jefe_de_costos, SOp=supervisor_operativo, SLog=supervisor_logistica, SAdm=supervisor_administracion, SSO=supervisor_ssoma, Asist=asistente, RRHH=rrhh.

## Matriz base de visibilidad por interfaz (decidida por Victor, 2026-09-28)

**Esta es la base de restricciones y accesos por rol.** Donde una fila de las matrices posteriores (sección "Matriz de accesos") sobre **ver** una interfaz contradiga esta sección, manda esta. Las filas posteriores siguen vigentes para las **acciones** (crear, editar, subir, validar, eliminar) salvo lo que se indica en "Acciones que cambian".

**Reglas decididas:**

1. **Interfaces sin datos económicos: las ven los 13 roles.** Incluye Cronograma, Paquetes de trabajo, RDTs (status, archivo, consolidado), RQ (status y consolidado), Recursos de empresa (Personal, Cargos, Equipos, Causas CNC en modo consulta), ficha del servicio, grilla del portafolio, Notificaciones y Mi entorno.
2. **Interfaces con datos económicos: solo 4 roles** — administrador, jefe de proyectos, jefe de oficina técnica y supervisor de costos.
3. **Administrador y jefe de proyectos tienen acceso a todo.**
4. **El jefe de oficina técnica puede crear RDT** (además de subir).
5. **Los recursos de la empresa (catálogos) los ven todos los roles**; gestionar (alta/baja) Causas CNC sigue siendo de administrador y jefe de proyectos.

Un dato es **económico** si muestra dinero (USD/S/): costos, presupuesto, valor planificado, valor ganado, costo real, índices de costo. Los RQ, los RDT y los recursos de empresa **no** muestran costos (solo descripción, cantidad, HH y metrados).

`✓` puede ver · `—` no puede. Columnas: Admin=administrador, JP=jefe_de_proyectos, JOT=jefe_de_oficina_tecnica, SOT=supervisor_oficina_tecnica, Plnr=planner, SCo=supervisor_costos, JCo=jefe_de_costos, SOp=supervisor_operativo, SLog=supervisor_logistica, SAdm=supervisor_administracion, SSO=supervisor_ssoma, Asist=asistente, RRHH=rrhh.

| Interfaz | ¿Datos económicos? | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Dashboard del servicio (Parcial y Completo) ¹ | Sí | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — |
| Dashboard del portafolio | Sí | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — |
| PR (Reporte del proyecto) | Sí | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — |
| DP (Datos del proyecto), ver | Sí | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — |
| Curva S | Sí | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — |
| Plan Maestro, ver | Sí | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — |
| Registro de costos por servicio | Sí | ✓ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — |
| Cronograma, ver | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Paquetes de trabajo, ver | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RDTs: status, archivo de subidos, consolidado | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RQ: status | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RQ: consolidado (ver) | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Recursos de empresa: Personal, Cargos, Equipos, Causas CNC (consulta) | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ficha del servicio y grilla del portafolio | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Notificaciones y Mi entorno | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

¹ Hoy los dos modos del Dashboard muestran datos económicos (flujo 11), por eso están restringidos. Cuando exista el Dashboard **Parcial sin datos económicos** (Spec futuro, ver `planes-futuros.md`), el Parcial pasará a la sección "sin datos económicos" y solo el Completo quedará restringido.

Las pantallas por servicio, además, siguen sujetas al **alcance por OT** (`proyecto_miembros`) cuando aplica; esa restricción no aparece en esta tabla.

### Acciones que cambian con esta decisión

| Acción | Antes | Ahora |
|---|---|---|
| Crear RDT estructurado ("Crear RDTs") | Admin, JP, SOp | Admin, JP, **JOT**, SOp |
| Todas las acciones operativas (crear, editar, subir, validar, gestionar) | Según la matriz de abajo | **Administrador y jefe de proyectos pueden ejecutarlas todas** |

### Conflictos operativos por resolver (no decididos; la regla de arriba se aplica al pie de la letra hasta que Victor los resuelva)

1. **Planner y Plan Maestro.** El Plan Maestro es económico (muestra valor planificado en USD), pero el planner es quien lo gestiona (crear y congelar línea base). Con la regla de 4 roles el planner pierde su herramienta.
2. **Supervisor de oficina técnica y DP.** El DP es económico y el supervisor de oficina técnica es quien lo importa. Con la regla de 4 roles pierde la pantalla donde importa.
3. **Supervisor de logística y Registro de costos.** Es quien lo sube, pero la pantalla es económica. Con la regla de 4 roles no puede subirlo.
4. **Jefe de costos.** No está entre los 4 roles con economía (Victor nombró "sup costos", no "jefe de costos"). Confirmar si es intencional: un jefe de costos sin acceso a costos, con su supervisor sí.
5. **Acciones destructivas y de sistema.** "Administrador y jefe de proyectos tienen acceso a todo": falta confirmar si el jefe de proyectos también puede lo que hoy es exclusivo del administrador (asignar rol administrador, "Ver como", borrado definitivo de RDT, RQ, programas y portafolios, y crear RQ, que hoy el administrador no puede).
6. **El propio flujo 14 tiene la regla de restricción económica marcada como pendiente** (al final del archivo, con otra lista de roles: jefe de proyectos, jefe de costos, supervisor de costos y administrador). Esta sección la reemplaza; al confirmar los conflictos anteriores se retira el texto pendiente.

## Matriz de accesos

> Las filas de **ver** una interfaz de esta matriz quedan reemplazadas por la "Matriz base de visibilidad por interfaz" de arriba. Se conservan como referencia de las **acciones** por rol.

### Proyecto / contenedores

| Acceso | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH | Requiere OT a cargo |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Adjudicar proyecto / crear programa / crear portafolio | ✓ | — | ✓ | — | — | — | — | — | — | — | — | — | — | No (crea la OT) |
| Confirmar transición de estado del proyecto | — | — | ✓ | — | — | — | — | — | — | — | — | — | — | Sí ** |
| Archivar / eliminar proyecto | ✓ | — | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar contenedor (programa / portafolio) | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |
| Modificar checklist del proyecto | ✓ | — | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Ver apartado "Proyectos" (panel izquierdo) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (lectura) |
| Ver Recursos (catálogo de empresa: Personal, Equipos) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Gestionar catálogo de causas CNC (Recursos > Causas CNC) — único catálogo de Recursos con alta/baja, los demás son de solo lectura | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Importar DP (Datos del Proyecto) | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | — | Sí |
| Subir documento del proyecto (catálogo AL_INICIO/CIERRE) | ✓ | — | — | * | * | * | * | * | * | * | * | * | * | Sí |
| Editar perfil extendido (propio) | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | No |
| Asignar rol administrador | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |
| Gestionar usuarios (crear / editar / eliminar) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No |
| Simular otro usuario o rol ("Ver como") | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |

`*` **Subir documento** no es un rol fijo: puede el administrador o **el rol responsable de ese documento específico**, según `catalogo_documentos.rol_responsable_id` (asignable a cualquiera de los 13 roles al dar de alta el tipo de documento). No es una fila de roles fijos como las demás.

`**` **Confirmar transición de estado del proyecto**, desde PR Fase 2 (2026-09-21): el permiso de rol es el mismo de siempre, pero la transición `EN_PLANEACION` → `EJECUCION` específicamente tiene además una precondición de negocio (regla 8, [20-plan-maestro.md](20-plan-maestro.md)) — el proyecto debe tener un Plan Maestro en estado `APROBADO`. No es un acceso nuevo por rol; es un requisito adicional, validado en servidor, sobre el acceso que ya existía.

### RDT (Supervisión operativa) — foco directo del Sub-lote 2

| Acceso | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH | Requiere OT a cargo |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Subir RDT (PDF / foto — "Subir RDTs") | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Crear RDT estructurado ("Crear RDTs", PROM-GP-002) | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Validar / Rechazar RDT | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Corregir RDT rechazado | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Eliminar RDT (borrado definitivo) — cubre tanto "Subir RDTs" (archivo) como "Crear RDTs" (parte estructurado, desde el plan PR Fase 1: dispara recálculo del PR) | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Rechazar un RDT ya VALIDADO (desde el plan PR Fase 1: destraba para corregir, dispara recálculo del PR) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Ver RDTs (listado / status / consolidado) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | ✓ | — | ✓ | ✓ | No (lectura) |

### Planificación

| Acceso | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH | Requiere OT a cargo |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Subir / reemplazar cronograma | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Ver cronograma | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | No (lectura; todos menos asistente) |
| Gestionar Plan Maestro (crear / congelar línea base) | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Ver Plan Maestro | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | No (lectura; todos menos asistente) |
| 3WLA | — no implementado (pospuesto, ver `docs/02-trabajo-activo/01-planes/planes-futuros.md`) — | | | | | | | | | | | | | — |
| Ver PR (Reporte del proyecto) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | No (lectura; todos menos asistente) |
| Ver Curva S (serie temporal PV/EV/AC) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | — | ✓ | No (lectura; todos menos asistente) |
| Status / Programación de capacitaciones | — no implementado — | | | | | | | | | | | | | — |

### Logística / Requerimientos (RQ)

| Acceso | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH | Requiere OT a cargo |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| Crear requerimiento (RQ) | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Sí (todos menos administrador) |
| Comentar requerimiento | ✓ | ✓ | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Actualizar estado de RQ (dar de alta, ATENDIDO) | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Derivar RQ a logística (aprobación) | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar requerimiento (borrado definitivo) | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Ver consolidado RQ / descargar PROM-GP-004 | ✓ | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | No (lectura) |
| Subir registro de costos por servicio | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Descargar registro de costos por servicio | — | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (descarga) |

### Otros grupos del nav (Costos, Oficina Técnica, Administración, SSOMA)

Sin accesos propios más allá de "Notificaciones" (común a todos los grupos, ver abajo). Los ítems `status-servicios`, `tareo-moi`, `consolidado-moi`, `pets` están registrados en el nav pero **sin `ruta` implementada todavía** — no tienen función de permiso propia que registrar aquí hasta que existan.

### Notificaciones (común a todos los grupos)

| Acceso | Todos los roles autenticados | Requiere OT a cargo |
|---|:-:|---|
| Ver notificaciones propias (por usuario o por rol) | ✓ | No (lectura, filtrada por destinatario) |
| Enviar mensaje a un usuario concreto | ✓ | Sí (la notificación queda ligada a la OT del contexto) |
| Marcar como visto / revisar / atender | ✓ (según sea destinatario) | Sí (ruta resuelve `proyecto_id` de la notificación) |

## Deuda saldada con esta versión

Estaba pendiente desde el pedido original (2026-09-16): **Cronograma** (flujo 15) y **Crear RDTs** (flujo 06) no estaban registrados en esta tabla. Ambos quedan arriba, en sus secciones correspondientes.

## Accesos requeridos para paquetes de trabajo (pendiente, no implementado)

Los paquetes deben sumarse a esta matriz con los siguientes accesos mínimos, cuando se implemente la interfaz (hoy solo existe el modelo de datos, `dp_paquetes`):

- Ver paquetes del servicio.
- Crear paquete.
- Editar paquete.
- Asignar o quitar partidas.
- Revisar avance del paquete.
- Registrar avance o datos de control del paquete.
- Archivar o cerrar paquete.
- Ver detalle de paquete y trazabilidad a partida.

Estas acciones se habilitan según el servicio, el rol y la configuración de control del presupuesto, sin duplicar permisos ya existentes para partidas, RDT ni dashboard.

## Pendiente a futuro

### Gestión visual de accesos
Interfaz para que administrador y gerente de proyectos gestionen accesos y restricciones por usuario desde una pantalla (en vez de que vivan fijos en código). Pedido de Victor, 2026-09-20 — registrado también en `docs/02-trabajo-activo/01-planes/planes-futuros.md`. Se retoma cuando esta matriz esté estable y probada en producción.

### Restricción de datos económicos por rol
Hoy todos los datos económicos (costos, presupuesto, registro de costos) son visibles por todos los roles que tienen acceso a cada sección. A futuro (pendiente, 2026-09-20): solo gerencia (jefe_de_proyectos, jefe_de_costos, supervisor_costos) y administrador deberían ver datos económicos. Supervisión operativa, logística y otros roles verán la estructura de los datos (partidas, cronograma, RDT) pero no los valores de costo. **Por ahora se deja sin implementar** — la estructura de permisos económicos queda para cuando se revise la confidencialidad de datos con Victor.
