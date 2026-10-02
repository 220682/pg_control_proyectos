# 14 — Accesos y restricciones

Tabla visual con **columnas = roles** y **filas = accesos**. Pedido por Victor el 2026-09-16; construida el 2026-09-20 como paso previo al Sub-lote 2 (alcance por servicio): "primero definir qué puede hacer cada rol". Rehecha y **aprobada por Victor el 2026-09-28** con el artefacto «Matriz de permisos».

## Fuente y regla de actualización

El instrumento editable es el artefacto **«Matriz de permisos»** (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT). Este archivo conserva la última versión aprobada (aprobación del 2026-09-28, 16:02 UTC, versión 17 de las marcas del artefacto). Es la base de los accesos y está ligado al flujo 16 (Paneles).

**Sincronización del artefacto (2026-09-30):** se comprobó el estado guardado del artefacto (versión 41 de la base de datos) contra estas tablas y solo diferían dos filas de descargas, que se corrigieron (versión 42): «Exportar DP» suma al supervisor de oficina técnica y «Descargar plantilla de cronograma» pasa a los 13 roles. La marca «Aprobada» del artefacto se quitó; queda pendiente que Victor la vuelva a dar. Desde entonces artefacto, flujo 14 y `permisos.ts` coinciden fila por fila.

**Actualización 2026-09-30 (tarea paneles-servicio-persistente, F7-B):** solo se añadieron las filas de descargas decididas (tabla 2, nota 7), la nota del asistente del shell y se retiró la marca «por construir» de Recursos (ya construido); ninguna decisión aprobada cambió.

**Actualización 2026-10-01 (plan niveles-paquetes-plan-maestro-rdt, F5-D):** tabla 2 ajustada a lo implementado (cronograma, Plan Maestro y paquetes con su texto nuevo; filas nuevas «Crear una versión nueva del Plan Maestro» y «Reasignar de paquete un RDT»; notas 8 a 10) y sección de paquetes reescrita. La tabla 1 no cambia. No hay chip ni acceso nuevo en el registro. **Corrección 2026-10-01 (F5-G):** aprobar el borrador que reemplaza una versión aprobada lo hacen los tres roles de «Gestionar Plan Maestro»; solo crear la versión nueva es de administrador y jefe de proyectos (nota 9).

**Regla:** toda interfaz, acción, permiso o acceso nuevo, modificado o eliminado actualiza el artefacto y este flujo en la misma tarea (política de coherencia y trazabilidad, `docs/01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md`). Si un Spec o plan entra en conflicto con esta matriz, la implementación abarca todos los flujos afectados (flujo 16 y los que la citen) y se consulta a Victor antes de editarlos.

## Cómo leer las tablas

- **✓** el rol tiene el acceso. **—** no lo tiene.
- Roles, columna por columna: Admin=administrador, JP=jefe_de_proyectos, JOT=jefe_de_oficina_tecnica, SOT=supervisor_oficina_tecnica, Plnr=planner, SCo=supervisor_costos, JCo=jefe_de_costos, SOp=supervisor_operativo, SLog=supervisor_logistica, SAdm=supervisor_administracion, SSO=supervisor_ssoma, Asist=asistente, RRHH=rrhh.
- Un dato es **económico** si muestra dinero (USD/S/): costos, presupuesto, valor planificado, valor ganado, costo real, índices de costo. Los RQ, los RDT y los recursos de empresa **no** muestran costos (solo descripción, cantidad, HH y metrados).
- **Requiere OT a cargo** (tabla de acciones): "Sí" = la acción escribe sobre una OT concreta y, además del rol, hace falta tener esa OT asignada en `proyecto_miembros` (Sub-lote 2, `docs/02-trabajo-activo/01-planes/2026-09-20-sub-lote-2-alcance-proyecto.md`). "No" = la acción no está ligada a ninguna OT (usuarios, catálogos globales, contenedores). **El alcance por OT es además el requisito de partida para ver cualquier interfaz orientada a un servicio** (confirmado por Victor, 2026-09-28); esa condición no se repite fila por fila en la tabla de interfaces.

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
| Registro de costos por servicio, ver ² | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Cronograma, ver | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Paquetes de trabajo, ver | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RDTs: status, archivo de subidos, consolidado | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RQ: status y consolidado | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Recursos de empresa: Personal, Cargos, Equipos, Causas CNC (consulta) | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Ficha del servicio y grilla del portafolio | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Panel izquierdo del servicio | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Notificaciones y Mi entorno | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

¹ **Confirmado por Victor (2026-09-28): el Dashboard Parcial no tiene datos económicos y lo ven los 13 roles; el Dashboard Completo sí tiene datos económicos y lo ven los roles que corresponde** (los 5 de esta tabla, más las dos excepciones). Hoy el código todavía muestra economía en los dos modos (flujo 11); hasta que el Spec futuro de economía separe realmente los datos de cada modo (`planes-futuros.md`), esta fila es el estado **objetivo**, no el actual — el informe "antes/después por rol" de la fase F0 del plan debe señalar esta brecha. Quién alterna entre Parcial y Completo (Victor, C35, 2026-09-29): lo alternan los roles que ven datos económicos (`puedeVerEconomia`: administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos); los demás lo verían fijo en Parcial, que es del plan futuro (`planes-futuros.md`).

² «Registro de costos» es un archivo (`.xlsx`, `.xls`, `.pdf` o `.csv`) que Logística sube por servicio; no es el RQ. Descargarlo es una acción (tabla 2): la decisión de Victor del 2026-09-28 es que lo descarguen el administrador y el jefe de proyectos.

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
| Importar DP (Datos del Proyecto) ⁸ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Gestionar usuarios (crear / editar / eliminar) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No |
| Editar perfil extendido (propio) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No |
| Asignar rol administrador | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |
| Simular otro usuario o rol («Ver como») | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |
| Subir documento del proyecto (catálogo AL_INICIO/CIERRE) ⁴ | ✓ | ✓ | — | * | * | * | * | * | * | * | * | * | * | Sí |
| **Recursos (Personal, Cargos, Equipos, Causas CNC)** ⁶ | | | | | | | | | | | | | | |
| Crear personal | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Editar personal existente | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Eliminar o desactivar personal | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Crear cargo | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Editar cargo existente | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Eliminar o desactivar cargo | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Crear equipo | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Editar equipo existente | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Eliminar o desactivar equipo | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Crear causa CNC | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Activar / desactivar causa CNC | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| Editar la descripción de una causa CNC | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (catálogo global) |
| **RDT** | | | | | | | | | | | | | | |
| Subir RDT (PDF o foto) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Crear RDT estructurado (PROM-GP-002) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Reasignar de paquete un RDT aún no validado ¹⁰ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Validar / rechazar RDT | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Corregir RDT rechazado | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Rechazar un RDT ya validado (destraba para corregir, dispara recálculo del PR) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar RDT (borrado definitivo; cubre archivo y parte estructurado, dispara recálculo del PR) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| **Planificación** | | | | | | | | | | | | | | |
| Subir / reemplazar cronograma ⁸ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Gestionar Plan Maestro (programar en el lienzo, crear = aprobar la primera versión y aprobar el borrador que reemplaza una versión aprobada) ⁸ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Crear una versión nueva del Plan Maestro (con una aprobada vigente; motivo obligatorio; solo crear el borrador, aprobarlo es «Gestionar Plan Maestro») ⁹ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Gestionar paquetes de trabajo (crear, editar, mover partidas, archivar, declarar vínculos con metrado y hitos; la disciplina es obligatoria) | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| **Requerimientos (RQ) y costos** | | | | | | | | | | | | | | |
| Crear requerimiento (RQ) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Sí |
| Comentar requerimiento | ✓ | ✓ | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Actualizar estado de RQ (dar de alta, ATENDIDO) | ✓ | — | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Derivar RQ a logística (aprobación) | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar requerimiento (borrado definitivo) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Descargar consolidado RQ (PROM-GP-004) ⁵ | ✓ | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | No (descarga) |
| Subir registro de costos por servicio (solo subir; no ve ni descarga el contenido) | — | — | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Descargar registro de costos por servicio | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No (descarga) |
| **Descargas** ⁷ | | | | | | | | | | | | | | |
| Exportar DP (Excel o PDF) | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | — | — | — | — | No (descarga) |
| Descargar RDTs según filtro (ZIP) y listado de RDTs (PDF PROM-GP-0006) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |
| Descargar el PDF de un RDT estructurado | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |
| Descargar el archivo de un RDT subido (PDF o foto) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |
| Descargar listado RQ según filtro (PDF PROM-GP-008) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |
| Descargar el PDF individual de un RQ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |
| Descargar el formato vacío PROM-GP-008 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |
| Descargar la plantilla de cronograma (.xlsx generada desde el DP) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |

³ Desde PR Fase 2 (2026-09-21), la transición `EN_PLANEACION` → `EJECUCION` tiene además una precondición de negocio (regla 8, [20-plan-maestro.md](20-plan-maestro.md)): el proyecto debe tener un Plan Maestro en estado `APROBADO`. No es un acceso nuevo por rol; es un requisito adicional, validado en servidor, sobre el acceso que ya existía.

⁴ **Subir documento** no es un rol fijo: puede el administrador, el jefe de proyectos, **el usuario asignado como responsable de ese documento en el proyecto** (`proyecto_documentos.responsable_usuario_id`) o el rol responsable del documento. Desde el 2026-10-02 el editor del checklist asigna siempre un responsable concreto por proyecto; el `rol_responsable_id` del catálogo dejó de ser obligatorio y es informativo. El `*` indica «si es el responsable de ese documento».

⁵ Todos los roles ven el consolidado RQ (tabla 1); la descarga se dejó como estaba: administrador, jefe de proyectos, jefe de oficina técnica y logística. Ampliarla está **por decidir**.

⁶ **Aprobado por Victor en el artefacto (2026-09-28), tras su propio recorrido de las interfaces del sistema.** Estado real, verificado en el código (no supuesto) antes de la propuesta: **Personal** solo permitía crear (sin editar ni eliminar); **Cargos** y **Equipos** eran de solo lectura (nadie podía crear, editar ni eliminar); **Causas CNC** permitía crear y activar/desactivar (sin editar el texto, sin borrado real). Las filas que entonces se marcaron «por construir» (editar/eliminar Personal; crear/editar/eliminar Cargos y Equipos; editar el texto de una causa CNC) **ya están construidas** (fase F5D del plan de paneles, 2026-09-30): las 9 acciones existen, por eso se retiró la marca, sin cambiar quién puede ejecutarlas.

⁷ **Descargas decididas por Victor (2026-09-30).** Las tres propuestas del artefacto (RDTs y listado de RDTs, listado RQ, exportar DP) quedan confirmadas. Las cinco descargas que el código ya tenía y la matriz no listaba (plantilla de cronograma, PDF de un RDT estructurado, archivo de un RDT subido, PDF individual de un RQ, formato vacío PROM-GP-008) quedan escritas como **los 13 roles; un usuario sin rol conocido queda rechazado**. Exportar DP sigue a «ver DP» (tabla 1). El registro de costos y el consolidado RQ se decidieron el 2026-09-28 (filas de arriba y nota 5). Sin adjuntos de RQ ni documentos del checklist: hoy solo se suben (no hay ruta de descarga por API; la subida es la acción ya listada). *Brecha con el código, ya cumplida (F6-R1, commit `0690c81`, 2026-09-30):* la plantilla de cronograma (`/api/cronograma/plantilla`) y `/api/requerimientos/formato-vacio` ahora responden a los 13 roles y rechazan (403) a quien no tiene rol conocido.

⁸ **Recarga bloqueada (plan niveles-paquetes-plan-maestro-rdt, 2026-09-30).** Con un Plan Maestro `APROBADO` el servicio no admite recargar el DP ni reemplazar el cronograma; sin Plan Maestro aprobado se avisa de lo que se perdería y se pide confirmación. No cambia quién puede la acción: es una precondición de negocio validada en servidor, como la nota 3 ([09](09-importar-dp.md), [15](15-cronograma.md), [20](20-plan-maestro.md)). «Gestionar Plan Maestro» ya no incluye «congelar línea base» como acción aparte: el planner programa y crea (aprueba) la primera versión; «Gestionar paquetes» incluye declarar vínculos con metrado y hitos (el cronograma ya no los edita).

⁹ **Decidido por Victor (Gate 1, 2026-09-30; aprobar el borrador, 2026-10-01).** Con un Plan Maestro aprobado, **crear** una versión nueva (el borrador, con motivo obligatorio) lo hacen solo el administrador y el jefe de proyectos; el planner conserva programar y crear la primera versión. **Aprobar** ese borrador, que reemplaza a la versión aprobada, lo hacen los tres roles de «Gestionar Plan Maestro» (administrador, jefe de proyectos y planner), igual que la primera aprobación. Implementado: crear el borrador usa `puedeCrearVersionPlanMaestro` (`POST`) y aprobar usa `puedeGestionarPlanMaestro` (`PATCH`), de modo que el código coincide con el flujo.

¹⁰ **Decidido por Victor (2026-09-30).** Reasignar un RDT de paquete mientras no esté `VALIDADO` lo hace quien valida (mismos roles que «Validar / rechazar RDT»); el supervisor que crea el RDT no reasigna, corrige reemplazando el parte ([06](06-rdt.md)). Vive en la ruta de validar del RDT (`puedeValidarRdt`); no es un permiso nuevo en el código. «Crear paquete» (acción rápida del panel) sigue la fila «Gestionar paquetes de trabajo»: administrador, jefe de proyectos y planner.

### Qué se decidió al aprobar la matriz (2026-09-28)

Respecto de la matriz que regía antes, Victor fijó en el artefacto:

- **Administrador y jefe de proyectos:** acceso a todas las interfaces. En acciones, no hay una regla general de "todo menos N" — cada acción se decidió una por una en el artefacto. El jefe de proyectos pasa a poder, entre otras, adjudicar y crear programas y portafolios, archivar proyectos, eliminar contenedores, editar servicio, editar checklist, importar DP, subir documento del proyecto, editar su perfil y ejecutar los borrados definitivos de RDT y RQ. **No** puede: asignar rol administrador ni "Ver como" (exclusivas de administrador, por diseño de sistema), ni actualizar estado de RQ ni subir el registro de costos (tareas operativas de logística; decidido por Victor el 2026-09-29).
- **Jefe de oficina técnica:** conserva adjudicar, confirmar transición, subir RDT, derivar RQ y descargar el consolidado RQ; **gana** crear RDT y validar o rechazar RDT; **deja de** archivar o eliminar proyectos, editar servicio, editar checklist y editar su perfil.
- **Supervisor de oficina técnica:** ve el DP pero **ya no lo importa** (importar DP queda para administrador y jefe de proyectos).
- **Administrador:** ahora puede crear RQ y actualizar el estado de RQ, además de lo que ya hacía.
- **Supervisor de logística:** solo sube el registro de costos; no lo ve ni lo descarga.
- **Planner:** ve y gestiona el Plan Maestro.
- **Jefe de costos:** ve las interfaces con economía, igual que el supervisor de costos.
- **Recursos (Personal, Cargos, Equipos, Causas CNC):** administrador y jefe de proyectos pueden crear, editar y eliminar (o desactivar) en los cuatro por igual, y editar el texto de una causa CNC. Construir lo que falta (editar/eliminar Personal; crear/editar/eliminar Cargos y Equipos; editar texto de Causas CNC) es trabajo nuevo para el Worker, no solo una guardia de permisos.

### Puntos por decidir

1. **Descargas.** Resuelto el 2026-09-30: todas las descargas están decididas y escritas en la tabla 2 (nota 7). Sin puntos abiertos, salvo la brecha del código que la nota 7 indica.
2. **Diferencias con el código actual.** La implementación debe alinear `permisos.ts` a esta matriz; el informe «antes/después por rol» lo produce la fase F0 del plan `docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente.md`.
3. **Otros flujos.** Cerrado el 2026-09-30: los flujos 05, 06, 08, 12 y el resto de los alcanzados se reescribieron con la aprobación de Victor según esta matriz; los flujos 02 y 13 no citan el ciclo de vida del proyecto ni reservan los borrados al administrador, y no requirieron cambios.
4. **Estado de RQ y registro de costos para el jefe de proyectos.** Cerrado (Victor, 2026-09-29): siguen siendo solo de logística (más el administrador en el estado de RQ, ya en la tabla 2).
5. **Quién alterna el Dashboard entre Parcial y Completo.** Cerrado (Victor, C35, 2026-09-29): ver nota ¹.

6. **Aprobar el borrador que reemplaza un Plan Maestro aprobado.** Resuelto por Victor (2026-10-01): lo aprueban los tres roles de «Gestionar Plan Maestro» (administrador, jefe de proyectos y planner); solo crear la versión nueva queda para administrador y jefe de proyectos (nota 9). Sin brecha con el código.

### Asistente del shell (excepción, sin fila en las tablas)

El asistente (icono flotante y panel desplegable del shell, flujo 16) **no es una interfaz ni una acción con permiso**: no figura en el registro de accesos ni en las tablas 1 y 2, y está disponible para los 13 roles, sin datos ni API (flujo 17: agente no habilitado). No confundir con el **rol** de usuario «asistente» (columna Asist). Se anota aquí y en el artefacto solo por trazabilidad.

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

## Accesos de paquetes de trabajo (implementados)

Los paquetes ya tienen interfaz (`/paquetes-trabajo`, flujo 19) y quedan en la matriz así, sin duplicar permisos de partidas, RDT ni dashboard:

- **Ver paquetes del servicio y su detalle:** los 13 roles (tabla 1, «Paquetes de trabajo, ver»).
- **Crear, editar, mover partidas entre paquetes, archivar, declarar vínculos con metrado y hitos, elegir disciplina:** una sola función de permiso, «Gestionar paquetes de trabajo» (tabla 2): administrador, jefe de proyectos y planner, con OT a cargo.
- **Crear paquete como acceso rápido del panel:** abre `/paquetes-trabajo?proyectoId=…&accion=crear` (flujo 16); no es un chip ni un permiso aparte.
- **Reasignar el RDT de un paquete a otro:** se rige por validar RDT (tabla 2, nota 10), no por gestionar paquetes.
- **Registrar el avance real:** ya no se declara en el paquete; se declara en el RDT contra paquete × partida (flujos 06 y 18) y el paquete solo lo muestra.
- **Disciplina:** dato obligatorio (catálogo fijo `GET /api/disciplinas`, lectura para cualquier usuario autenticado); no es un permiso ni un acceso.

## Pendiente a futuro

### Gestión visual de accesos
Interfaz para que administrador y gerente de proyectos gestionen accesos y restricciones por usuario desde una pantalla (en vez de que vivan fijos en código). Pedido de Victor, 2026-09-20 — registrado también en `docs/02-trabajo-activo/01-planes/planes-futuros.md`. Se retoma cuando esta matriz esté estable y probada en producción. Detallado como plan futuro el 2026-09-28: la pantalla replica el artefacto «Matriz de permisos» y se somete a él (ver `docs/02-trabajo-activo/01-planes/planes-futuros.md`).

### Restricción de datos económicos por rol
La restricción está **decidida y escrita** en la tabla 1 (2026-09-28). Queda pendiente, como Spec aparte (ver `planes-futuros.md`), el Dashboard Parcial sin datos económicos y la restricción económica definitiva.
