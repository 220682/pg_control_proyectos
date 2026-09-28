# 14 — Accesos y restricciones

Tabla visual con **columnas = roles** y **filas = accesos**. Pedido por Victor el 2026-09-16; construida el 2026-09-20 como paso previo al Sub-lote 2 (alcance por servicio): "primero definir qué puede hacer cada rol". Rehecha y **aprobada por Victor el 2026-09-28** con el artefacto «Matriz de permisos».

## Fuente y regla de actualización

El instrumento editable es el artefacto **«Matriz de permisos»** (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT). Este archivo conserva la última versión aprobada (aprobación del 2026-09-28, 16:02 UTC, versión 17 de las marcas del artefacto). Es la base de los accesos y está ligado al flujo 16 (Paneles).

**Regla:** toda interfaz, acción, permiso o acceso nuevo, modificado o eliminado actualiza el artefacto y este flujo en la misma tarea (política de coherencia y trazabilidad, `docs/01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md`). Si un Spec o plan entra en conflicto con esta matriz, la implementación abarca todos los flujos afectados (flujo 16 y los que la citen) y se consulta a Victor antes de editarlos.

## Cómo leer las tablas

- **✓** el rol tiene el acceso. **—** no lo tiene.
- Roles, columna por columna: Admin=administrador, JP=jefe_de_proyectos, JOT=jefe_de_oficina_tecnica, SOT=supervisor_oficina_tecnica, Plnr=planner, SCo=supervisor_costos, JCo=jefe_de_costos, SOp=supervisor_operativo, SLog=supervisor_logistica, SAdm=supervisor_administracion, SSO=supervisor_ssoma, Asist=asistente, RRHH=rrhh.
- Un dato es **económico** si muestra dinero (USD/S/): costos, presupuesto, valor planificado, valor ganado, costo real, índices de costo. Los RQ, los RDT y los recursos de empresa **no** muestran costos (solo descripción, cantidad, HH y metrados).
- **Requiere OT a cargo** (tabla de acciones): "Sí" = la acción escribe sobre una OT concreta y, además del rol, hace falta tener esa OT asignada en `proyecto_miembros` (Sub-lote 2, `docs/02-trabajo-activo/01-planes/2026-09-20-sub-lote-2-alcance-proyecto.md`). "No" = la acción no está ligada a ninguna OT (usuarios, catálogos globales, contenedores). Las pantallas por servicio siguen sujetas al alcance por OT cuando aplica; esa restricción no aparece en la tabla de interfaces.

## Tabla 1 — Interfaces: quién puede verlas

**Reglas decididas por Victor (2026-09-28):**

1. **Interfaces sin datos económicos: las ven los 13 roles.**
2. **Interfaces con datos económicos: solo administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos.** Más dos excepciones acotadas a la herramienta de trabajo del rol: el **planner** ve el Plan Maestro y el **supervisor de oficina técnica** ve el DP. El supervisor de logística no ve el registro de costos; solo lo **sube** (ver tabla 2).
3. **Administrador y jefe de proyectos ven todas las interfaces**, las económicas incluidas.
4. **Los recursos de empresa (catálogos) los ven todos los roles.**
5. **El panel izquierdo del servicio lo ven los 13 roles** (flujo 16); lo que el rol no puede usar se muestra deshabilitado.

| Interfaz | ¿Datos económicos? | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Dashboard del servicio (Parcial y Completo) ¹ | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Dashboard del portafolio | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| PR (Reporte del proyecto) | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| DP (Datos del proyecto), ver | Sí | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | — | — | — | — |
| Curva S | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Plan Maestro, ver | Sí | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | — | — | — | — | — | — |
| Registro de costos por servicio, ver y descargar ² | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Cronograma, ver | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Paquetes de trabajo, ver | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RDTs: status, archivo de subidos, consolidado | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RQ: status y consolidado | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Recursos de empresa: Personal, Cargos, Equipos, Causas CNC (consulta) | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ficha del servicio y grilla del portafolio | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Panel izquierdo del servicio | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Notificaciones y Mi entorno | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

¹ Hoy los dos modos del Dashboard muestran datos económicos (flujo 11), por eso están restringidos. Cuando exista el Dashboard **Parcial sin datos económicos** (Spec futuro, ver `planes-futuros.md`), el Parcial pasará a las interfaces sin economía y solo el Completo quedará restringido.

² «Registro de costos» es un archivo (`.xlsx`, `.xls`, `.pdf` o `.csv`) que Logística sube por servicio; no es el RQ. Hoy solo lo descarga el jefe de proyectos; descargarlo para los cinco roles con economía está **por decidir**.

## Tabla 2 — Acciones: quién puede ejecutarlas

Las acciones son crear, editar, subir, validar o borrar. La visibilidad de las interfaces está en la tabla 1.

| Acción | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH | Requiere OT a cargo |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|
| **Proyecto y sistema** | | | | | | | | | | | | | | |
| Adjudicar proyecto / crear programa / crear portafolio | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | No (crea la OT) |
| Confirmar transición de estado del proyecto ³ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Archivar / eliminar proyecto | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar contenedor (programa / portafolio) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No |
| Editar servicio | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Editar checklist del proyecto | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Importar DP (Datos del Proyecto) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Gestionar catálogo de causas CNC (alta y baja) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Gestionar usuarios (crear / editar / eliminar) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No |
| Editar perfil extendido (propio) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No |
| Asignar rol administrador | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |
| Simular otro usuario o rol («Ver como») | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |
| Subir documento del proyecto (catálogo AL_INICIO/CIERRE) ⁴ | ✓ | — | — | * | * | * | * | * | * | * | * | * | * | Sí |
| **RDT** | | | | | | | | | | | | | | |
| Subir RDT (PDF o foto) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Crear RDT estructurado (PROM-GP-002) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Validar / rechazar RDT | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Corregir RDT rechazado | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Rechazar un RDT ya validado (destraba para corregir, dispara recálculo del PR) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar RDT (borrado definitivo; cubre archivo y parte estructurado, dispara recálculo del PR) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| **Planificación** | | | | | | | | | | | | | | |
| Subir / reemplazar cronograma | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Gestionar Plan Maestro (crear / congelar línea base) | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Gestionar paquetes de trabajo | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| **Requerimientos (RQ) y costos** | | | | | | | | | | | | | | |
| Crear requerimiento (RQ) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Sí |
| Comentar requerimiento | ✓ | ✓ | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Actualizar estado de RQ (dar de alta, ATENDIDO) | ✓ | — | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Derivar RQ a logística (aprobación) | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar requerimiento (borrado definitivo) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Descargar consolidado RQ (PROM-GP-004) ⁵ | ✓ | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | No (descarga) |
| Subir registro de costos por servicio (solo subir; no ve ni descarga el contenido) | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |

³ Desde PR Fase 2 (2026-09-21), la transición `EN_PLANEACION` → `EJECUCION` tiene además una precondición de negocio (regla 8, [20-plan-maestro.md](20-plan-maestro.md)): el proyecto debe tener un Plan Maestro en estado `APROBADO`. No es un acceso nuevo por rol; es un requisito adicional, validado en servidor, sobre el acceso que ya existía.

⁴ **Subir documento** no es un rol fijo: puede el administrador o **el rol responsable de ese documento específico**, según `catalogo_documentos.rol_responsable_id` (asignable a cualquiera de los 13 roles al dar de alta el tipo de documento). El `*` indica «si es el responsable de ese documento».

⁵ Todos los roles ven el consolidado RQ (tabla 1); la descarga se dejó como estaba: administrador, jefe de proyectos, jefe de oficina técnica y logística. Ampliarla está **por decidir**.

### Qué se decidió al aprobar la matriz (2026-09-28)

Respecto de la matriz que regía antes, Victor fijó en el artefacto:

- **Administrador y jefe de proyectos:** acceso a todas las interfaces, y a todas las acciones excepto las dos exclusivas del administrador (asignar rol administrador y «Ver como»). El jefe de proyectos pasa a poder, entre otras, adjudicar y crear programas y portafolios, archivar proyectos, eliminar contenedores, editar servicio, editar checklist, importar DP, editar su perfil y ejecutar los borrados definitivos de RDT y RQ.
- **Jefe de oficina técnica:** conserva adjudicar, confirmar transición, subir RDT, derivar RQ y descargar el consolidado RQ; **gana** crear RDT y validar o rechazar RDT; **deja de** archivar o eliminar proyectos, editar servicio, editar checklist y editar su perfil.
- **Supervisor de oficina técnica:** ve el DP pero **ya no lo importa** (importar DP queda para administrador y jefe de proyectos).
- **Administrador:** ahora puede crear RQ y actualizar el estado de RQ, además de lo que ya hacía.
- **Supervisor de logística:** solo sube el registro de costos; no lo ve ni lo descarga.
- **Planner:** ve y gestiona el Plan Maestro.
- **Jefe de costos:** ve las interfaces con economía, igual que el supervisor de costos.

### Puntos por decidir

1. Descarga del registro de costos (nota 2) y del consolidado RQ (nota 5).
2. **Diferencias con el código actual.** La implementación debe alinear `permisos.ts` a esta matriz; el informe «antes/después por rol» lo produce la fase F0 del plan `docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente.md`.
3. Otros flujos que asignan al jefe de oficina técnica el ciclo de vida del proyecto o reservan los borrados al administrador (por ejemplo 02, 05, 06, 08, 12 y 13) contradicen esta matriz en los puntos de arriba. Se ajustan al cierre del plan, con consulta a Victor por cada contradicción (política de coherencia y trazabilidad).

### Otros grupos del nav (Costos, Oficina Técnica, Administración, SSOMA)

Sin accesos propios más allá de «Notificaciones» (común a todos los grupos, ver abajo). Los ítems `status-servicios`, `tareo-moi`, `consolidado-moi`, `pets` están registrados en el nav pero **sin `ruta` implementada todavía** — no tienen función de permiso propia que registrar aquí hasta que existan. Tampoco están implementados 3WLA ni Status / Programación de capacitaciones (ver `docs/02-trabajo-activo/01-planes/planes-futuros.md`).

### Notificaciones (común a todos los grupos)

| Acceso | Todos los roles autenticados | Requiere OT a cargo |
|---|:-:|---|
| Ver notificaciones propias (por usuario o por rol) | ✓ | No (lectura, filtrada por destinatario) |
| Enviar mensaje a un usuario concreto | ✓ | Sí (la notificación queda ligada a la OT del contexto) |
| Marcar como visto / revisar / atender | ✓ (según sea destinatario) | Sí (ruta resuelve `proyecto_id` de la notificación) |

## Deuda saldada

Estaba pendiente desde el pedido original (2026-09-16): **Cronograma** (flujo 15) y **Crear RDTs** (flujo 06) no estaban registrados en esta tabla. Ambos quedan registrados arriba.

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
Interfaz para que administrador y gerente de proyectos gestionen accesos y restricciones por usuario desde una pantalla (en vez de que vivan fijos en código). Pedido de Victor, 2026-09-20 — registrado también en `docs/02-trabajo-activo/01-planes/planes-futuros.md`. Se retoma cuando esta matriz esté estable y probada en producción. Detallado como plan futuro el 2026-09-28: la pantalla replica el artefacto «Matriz de permisos» y se somete a él (ver `docs/02-trabajo-activo/01-planes/planes-futuros.md`).

### Restricción de datos económicos por rol
La restricción está **decidida y escrita** en la tabla 1 (2026-09-28). Queda pendiente, como Spec aparte (ver `planes-futuros.md`), el Dashboard Parcial sin datos económicos y la restricción económica definitiva.
