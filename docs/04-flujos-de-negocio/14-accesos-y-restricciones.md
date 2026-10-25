# 14 — Accesos y restricciones
> Lee si: **cualquier** interfaz, permiso, acción o acceso nuevo, modificado o eliminado, en cualquier parte del sistema. Este flujo es la base de los accesos y manda sobre los demás.


Tabla visual con **columnas = roles** y **filas = accesos**. Pedido por Victor el 2026-09-16; construida el 2026-09-20 como paso previo al Sub-lote 2 (alcance por servicio): "primero definir qué puede hacer cada rol". Rehecha y **aprobada por Victor el 2026-09-28** con el artefacto «Matriz de permisos».

## Fuente y regla de actualización

El instrumento editable es el artefacto **«Matriz de permisos»** (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT). Este archivo conserva la última versión aprobada (aprobación del 2026-09-28, 16:02 UTC, versión 17 de las marcas del artefacto). Es la base de los accesos y está ligado al flujo 16 (Paneles).

**Sincronización del artefacto (2026-09-30):** se comprobó el estado guardado del artefacto (versión 41 de la base de datos) contra estas tablas y solo diferían dos filas de descargas, que se corrigieron (versión 42): «Exportar DP» suma al supervisor de oficina técnica y «Descargar plantilla de cronograma» pasa a los 13 roles. La marca «Aprobada» del artefacto se quitó; queda pendiente que Victor la vuelva a dar. Desde entonces artefacto, flujo 14 y `permisos.ts` coinciden fila por fila.

**Actualización 2026-09-30 (tarea paneles-servicio-persistente, F7-B):** solo se añadieron las filas de descargas decididas (tabla 2, nota 7), la nota del asistente del shell y se retiró la marca «por construir» de Recursos (ya construido); ninguna decisión aprobada cambió.

**Actualización 2026-10-01 (plan niveles-paquetes-plan-maestro-rdt, F5-D):** tabla 2 ajustada a lo implementado (cronograma, Plan Maestro y paquetes con su texto nuevo; filas nuevas «Crear una versión nueva del Plan Maestro» y «Reasignar de paquete un RDT»; notas 8 a 10) y sección de paquetes reescrita. La tabla 1 no cambia. No hay chip ni acceso nuevo en el registro. **Corrección 2026-10-01 (F5-G):** aprobar el borrador que reemplaza una versión aprobada lo hacen los tres roles de «Gestionar Plan Maestro»; solo crear la versión nueva es de administrador y jefe de proyectos (nota 9).

**Actualización 2026-10-02 (plan observaciones-victor, Lote 2, Gate 1):** la acción «Subir documento del proyecto» se acota a los ítems del **Grupo A** del checklist y a los personalizados (fila de la tabla 2 y nota 4); el servidor rechaza con 400 subir a un ítem del Grupo B y el «Acta de conformidad» (fase CIERRE) queda fuera del alcance. La fila informativa 6 de ese Gate (chip inerte con título «Sin pantalla todavía», flujo 16) no cambia. **El artefacto «Matriz de permisos» lo actualiza solo Victor** (lo edita él; aquí solo queda registrado el cambio).

**Actualización 2026-10-02 (plan dashboard-economia-y-curva-s, Fase E):** la tabla 1 separa el Dashboard y la Curva S en dos filas cada uno: el **Dashboard Parcial** y la **Curva S — avance físico (%)** quedan **sin datos económicos** para los 13 roles; el **Dashboard Completo** y la **Curva S — económica (USD)** los ven **exactamente los cinco roles con economía** (las excepciones de planner y supervisor de OT son para Plan Maestro y DP, no para el Completo). El interruptor Parcial/Completo queda visible pero **deshabilitado con título** para quien no tiene economía (fijo en Parcial) y el servidor **fuerza Parcial** y **rechaza con 403** el modo económico sin permiso. Nota ¹ reescrita; deja de aplicar la antigua lectura de «estado objetivo / plan futuro». **El artefacto «Matriz de permisos» lo actualiza solo Victor** (P05, pendiente).

**Actualización 2026-10-03 (plan observaciones-victor, Lote 3, Enmienda E1):** se **retira** la acción del 2026-10-02 (F2-A) «Editar actividad del cronograma con Plan Maestro aprobado» y su permiso. Con Plan Maestro aprobado lo único editable es el Plan Maestro (U3), así que editar actividades individuales del cronograma deja de existir y reemplazar el cronograma sigue bloqueado. La tabla 2 pierde esa fila y su nota.

**Actualización 2026-10-17 (plan Informes de supervisión y Dashboard, tanda M):** las tablas 1 y 2 suman las filas de informes de supervisión (ver, crear, emitir, versión nueva, Costos, fotos de campo, «Mis formatos», pestaña Inasistencias, descargas), del Reporte del proyecto (subcontratos con dos formas de medir), de los campos nuevos del RDT y de la descarga del Dashboard (notas 11 y 12); la nota 3 suma el supervisor a cargo. **El artefacto «Matriz de permisos» no se pudo abrir desde la cuenta de Claude Code** (lectura «artifact not found», verificado el 2026-10-15): lo actualiza Victor con la lista del resumen de la tanda M.

**Actualización 2026-10-17 (Alcance y Presupuesto del servicio, pedido de Victor):** los chips «Alcance» y «Presupuesto» del panel izquierdo dejan de ser inertes y abren una pantalla propia con el archivo del ítem del mismo nombre del checklist. **Ver y descargar:** Alcance, los 13 roles; Presupuesto, los roles que ven el DP (tabla 1: trae precios). **Cargar, reemplazar y eliminar el archivo: solo el administrador** (tabla 2, nota 13). La subida desde la fila del checklist (fila «Subir documento del proyecto», nota 4) **sigue como estaba**: conviven (decisión de Victor, 2026-10-17). Filas nuevas en las tablas 1 y 2 y nota 13. **El artefacto «Matriz de permisos» no se pudo abrir desde la cuenta de Claude Code** (ver nota de arriba): lo actualiza Victor.

**Actualización 2026-10-18 (plan Notificaciones estándar y supervisor operativo, tanda T8):** la tabla 2 suma «Devolver un RQ» y «Corregir y reenviar un RQ Devuelto» (nota 15) y reemplaza «Editar perfil extendido (propio)» por tres acciones del perfil propio para los 13 roles: «Editar mi celular», «Cambiar mi correo» y «Cambiar mi contraseña» (nota 14). **Corrige lo decidido el 2026-09-28**, cuando solo el administrador y el jefe de proyectos editaban su perfil y el jefe de oficina técnica dejaba de editarlo; la nueva decisión es de Victor (2026-10-17). La sección «Notificaciones» precisa cuándo hace falta tener el servicio a cargo (no para «Entorno»). Ninguna otra decisión aprobada cambia. **El artefacto «Matriz de permisos» no se pudo abrir desde la cuenta de Claude Code** (verificado el 2026-10-18: «artifact not found»): lo actualiza Victor con la lista de filas del resumen de la tanda T8B del plan.

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
| Dashboard del servicio — Parcial ¹ | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Dashboard del servicio — Completo ¹ | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Dashboard del portafolio | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| PR (Reporte del proyecto) | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Reporte del proyecto: sección Subcontratos (elegir la forma de medir y ver el monto) ¹² | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| DP (Datos del proyecto), ver | Sí | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | — | — | — | — |
| Curva S — avance físico (%) | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Curva S — económica (USD) | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Plan Maestro, ver | Sí | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | — | — | — | — | — | — |
| Registro de costos por servicio, ver ² | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Cronograma, ver | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Paquetes de trabajo, ver | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RDTs: status, archivo de subidos, consolidado | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RDT: campos HH extra, HM stand-by y estado del equipo (ver) ¹¹ | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Informes de supervisión: ver emitidos (dentro de servicios asignados) ¹¹ | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Informe de formato Costos: ver ¹¹ | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Informes: pestaña Inasistencias (dentro de servicios asignados) ¹¹ | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Banco de fotos del día (ver y usar) ¹¹ | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Restricciones-Notas del servicio (Supervisión operativa; antes «Restricciones»): ver ¹⁷ | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Fuente-Gmail (minutas y correos del cliente, dentro de servicios a su alcance; el portafolio solo por rol) ¹⁹ | Sí | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| Fuente-WhatsApp (grupo del servicio; pantalla vacía hasta conectarla, dentro de servicios a su alcance) ²² | Sí | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| Fuente-Drive (Drive de Oficina Técnica filtrado al servicio; pantalla vacía hasta conectarla, dentro de servicios a su alcance) ²² | Sí | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| Gestión de emails (documentos del servicio con su estado y semáforo, dentro de servicios a su alcance) ²⁰ | Sí | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| Gestión documentaria (árbol de archivos de cada documento, dentro de servicios a su alcance) ²¹ | Sí | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — |
| RQ: status y consolidado | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Recursos de empresa: Personal, Cargos, Equipos, Causas CNC (consulta) | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Recursos del servicio, ver (Cargos HH, Equipos HM, Materiales c/c, Subcontratos; sin costos) ⁷ | Sí | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Alcance del servicio: ver y descargar el archivo ¹³ | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Presupuesto del servicio: ver y descargar el archivo ¹³ | Sí | ✓ | ✓ | ✓ | ✓ | — | ✓ | ✓ | — | — | — | — | — | — |
| Ficha del servicio y grilla del portafolio | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Panel izquierdo del servicio | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Notificaciones y Mi entorno | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

¹ **Confirmado por Victor (2026-09-28) y aplicado el 2026-10-02** (plan `2026-10-01-dashboard-economia-y-curva-s`): el Dashboard Parcial no tiene datos económicos y lo ven los 13 roles; el Dashboard Completo sí tiene datos económicos y lo ven **exactamente los cinco roles con economía** de esta tabla (las excepciones de planner y supervisor de oficina técnica son para Plan Maestro y DP, no para el Completo). Quién alterna entre Parcial y Completo (Victor, C35, 2026-09-29): lo alternan los roles que ven datos económicos (`puedeVerEconomia`: administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos); los demás ven el interruptor **deshabilitado con título** y quedan **fijos en Parcial** (D3). El servidor fuerza Parcial para el rol sin economía aunque `tipo_dashboard` esté en `COMPLETO`. La separación del Dashboard Parcial y de la Curva S física ya **no** es un estado objetivo ni depende de `planes-futuros.md`: está implementada.

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
| Editar servicio (incluye asignar el supervisor operativo a cargo) ¹² | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Editar checklist del proyecto | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Importar DP (Datos del Proyecto) ⁸ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Declarar equivalencias de cargos del servicio (pantalla «Equivalencias de cargos del servicio» en la página del DP) ¹⁸ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Gestionar usuarios (crear / editar / eliminar) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No |
| Editar mi celular (propio; solo el celular, nunca nombre, cargo, área ni roles) ¹⁴ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No |
| Cambiar mi correo (propio; pide la contraseña actual y rige al confirmarlo por enlace) ¹⁴ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No |
| Cambiar mi contraseña (propia; pide la actual) ¹⁴ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No |
| Asignar rol administrador | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |
| Simular otro usuario o rol («Ver como») | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | No |
| Subir documento del proyecto (catálogo AL_INICIO, Grupo A y personalizados) ⁴ | ✓ | ✓ | — | * | * | * | * | * | * | * | * | * | * | Sí |
| Cargar, reemplazar o eliminar el archivo de Alcance o de Presupuesto del servicio (pantalla propia) ¹³ | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | Sí |
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
| Registrar HH extra, HM stand-by y estado del equipo en el RDT (igual que Crear RDT estructurado) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Reasignar de paquete un RDT aún no validado ¹⁰ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Validar / rechazar RDT | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Corregir RDT rechazado | ✓ | ✓ | — | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Rechazar un RDT ya validado (destraba para corregir, dispara recálculo del PR) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar RDT del Archivo de RDTs subidos (borrado definitivo, dispara recálculo del PR) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Eliminar parte de RDT estructurado desde Status de RDTs (borrado definitivo; si estaba VALIDADO, recálculo del PR; deja foto en el historial) | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | Sí |
| **Planificación** | | | | | | | | | | | | | | |
| Subir / reemplazar cronograma ⁸ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Gestionar Plan Maestro (programar en el lienzo, crear = aprobar la primera versión y aprobar el borrador que reemplaza una versión aprobada) ⁸ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Crear una versión nueva del Plan Maestro (con una aprobada vigente; motivo obligatorio; solo crear el borrador, aprobarlo es «Gestionar Plan Maestro») ⁹ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Gestionar paquetes de trabajo (crear, editar, mover partidas, archivar, declarar vínculos con metrado y hitos; la disciplina es obligatoria) | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| Declarar partidas transversales (paso «Transversales» de Paquetes; con Plan Maestro aprobado solo administrador y jefe de proyectos) ¹⁶ | ✓ | ✓ | — | — | ✓ | — | — | — | — | — | — | — | — | Sí |
| **Informes de supervisión y Dashboard** ¹¹ | | | | | | | | | | | | | | |
| Crear, editar su borrador y emitir un informe (formatos que no son Costos) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Crear, emitir y ver un informe de formato Costos (el supervisor de costos y el jefe de costos solo crean, editan, emiten y versionan Costos) | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — | Sí |
| Emitir una versión nueva de un informe ajeno (del propio, quien lo creó) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| Guardar «Mis formatos» (arreglos de bloques propios; los de Costos solo con economía) | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | ✓ | — | — | — | — | — | No |
| Tomar y subir foto de campo «para partidas» | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Elegir la forma de medir y escribir el monto de un subcontrato en el Reporte del proyecto ¹² | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — | Sí |
| **Restricciones** ¹⁷ | | | | | | | | | | | | | | |
| Crear una restricción (pantalla Restricciones) | — | — | — | — | — | — | — | ✓ | — | — | ✓ | — | — | Sí |
| Crear una restricción desde el RDT (quien llena «restricciones» en una actividad; mismos roles que Crear RDT estructurado) | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — | Sí |
| Recepcionar y atender una restricción (y recibir su aviso) | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Subir una foto «para restricciones» | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | ✓ | — | — | Sí |
| **Fuente-Gmail** ¹⁹ | | | | | | | | | | | | | | |
| Ver el correo completo y descargar adjuntos y minutas | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | Sí |
| Crear, renombrar, cerrar o eliminar temas; escribir o quitar notas; ubicar o ignorar un correo; subir o eliminar minutas | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí (en el portafolio solo el rol) |
| Conectar o desconectar correos, pausarlos, cambiar las horas de lectura, pausar la lectura y «Sincronizar ahora» (`/admin/estado-servicio`) | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | No |
| **Gestión documentaria** ²¹ | | | | | | | | | | | | | | |
| Ver el árbol de archivos, abrirlos y descargarlos | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | Sí |
| Corregir el estado de una versión, ponerle etiqueta o comentario, subir o borrar un archivo a mano y copiar los adjuntos pendientes | ✓ | — | — | — | — | — | — | — | — | — | — | — | — | Sí |
| **Gestión de emails** ²⁰ | | | | | | | | | | | | | | |
| Ver los documentos, su historial de correos y exportar a Excel | ✓ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | Sí |
| Crear, editar o borrar un documento, corregir su estado o su área, asignar o sacar correos | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | — | Sí |
| **Requerimientos (RQ) y costos** | | | | | | | | | | | | | | |
| Crear requerimiento (RQ) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Sí |
| Comentar requerimiento | ✓ | ✓ | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Actualizar estado de RQ (recepcionar el RQ; En almacén y Atendido por material) | ✓ | — | — | — | — | — | — | — | ✓ | — | — | — | — | Sí |
| Derivar RQ a logística (aprobación) | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Devolver un RQ Solicitado con motivo (mismo reparto que Derivar RQ a logística) ¹⁵ | ✓ | ✓ | ✓ | — | — | — | — | — | — | — | — | — | — | Sí |
| Corregir y reenviar un RQ Devuelto (el solicitante del RQ y el administrador) ¹⁵ | ✓ | * | * | * | * | * | * | * | * | * | * | * | * | Sí |
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
| Descargar un informe emitido (el de Costos solo los 5 con economía) ¹¹ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |
| Descargar las inasistencias en PDF ¹¹ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |
| Descargar el Dashboard en PDF o Excel (el contenido sigue su modo: Parcial sin dinero; Completo solo los 5 con economía) ¹¹ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | No (descarga) |

³ Desde PR Fase 2 (2026-09-21), la transición `EN_PLANEACION` → `EJECUCION` tiene además una precondición de negocio (regla 8, [20-plan-maestro.md](20-plan-maestro.md)): el proyecto debe tener un Plan Maestro en estado `APROBADO`. Desde el 2026-10-15 exige también **un supervisor operativo a cargo** asignado (columna propia del servicio, [flujo 08](08-programa-portafolio-proyecto.md)). No es un acceso nuevo por rol; son requisitos adicionales, validados en servidor, sobre el acceso que ya existía.

⁴ **Subir documento** no es un rol fijo: puede el administrador, el jefe de proyectos, **el usuario asignado como responsable de ese documento en el proyecto** (`proyecto_documentos.responsable_usuario_id`) o el rol responsable del documento. Desde el 2026-10-02 el editor del checklist asigna siempre un responsable concreto por proyecto; el `rol_responsable_id` del catálogo dejó de ser obligatorio y es informativo. El `*` indica «si es el responsable de ese documento». **Alcance de la acción (Lote 2, Gate 1 2026-10-02):** la subida cubre **solo los ítems del Grupo A del checklist** (Alcance, Presupuesto, Listado de personal nuevo y Listado de pets) **y los personalizados**; el servidor **rechaza con 400** subir un archivo a un ítem del Grupo B (pantalla propia), y el «Acta de conformidad» (fase CIERRE) sale del alcance porque no figura en la lista (ver [flujo 12](12-checklist.md), sección «Grupos de acción»).

⁵ Todos los roles ven el consolidado RQ (tabla 1); la descarga se dejó como estaba: administrador, jefe de proyectos, jefe de oficina técnica y logística. Ampliarla está **por decidir**.

⁷ **Decidido por Victor el 2026-10-15.** Pantallas solo informativas con los recursos del servicio según el DP, **sin precios ni costos**; las ve cualquier rol y el servidor nunca envía datos económicos al navegador (flujo 16). **Pendiente de Victor: reflejar la fila en el artefacto «Matriz de permisos»**, que es la base de este flujo y lo edita él.

⁶ **Aprobado por Victor en el artefacto (2026-09-28), tras su propio recorrido de las interfaces del sistema.** Estado real, verificado en el código (no supuesto) antes de la propuesta: **Personal** solo permitía crear (sin editar ni eliminar); **Cargos** y **Equipos** eran de solo lectura (nadie podía crear, editar ni eliminar); **Causas CNC** permitía crear y activar/desactivar (sin editar el texto, sin borrado real). Las filas que entonces se marcaron «por construir» (editar/eliminar Personal; crear/editar/eliminar Cargos y Equipos; editar el texto de una causa CNC) **ya están construidas** (fase F5D del plan de paneles, 2026-09-30): las 9 acciones existen, por eso se retiró la marca, sin cambiar quién puede ejecutarlas.

⁷ **Descargas decididas por Victor (2026-09-30).** Las tres propuestas del artefacto (RDTs y listado de RDTs, listado RQ, exportar DP) quedan confirmadas. Las cinco descargas que el código ya tenía y la matriz no listaba (plantilla de cronograma, PDF de un RDT estructurado, archivo de un RDT subido, PDF individual de un RQ, formato vacío PROM-GP-008) quedan escritas como **los 13 roles; un usuario sin rol conocido queda rechazado**. Exportar DP sigue a «ver DP» (tabla 1). El registro de costos y el consolidado RQ se decidieron el 2026-09-28 (filas de arriba y nota 5). Sin adjuntos de RQ ni documentos del checklist: hoy solo se suben (no hay ruta de descarga por API; la subida es la acción ya listada). *Brecha con el código, ya cumplida (F6-R1, commit `0690c81`, 2026-09-30):* la plantilla de cronograma (`/api/cronograma/plantilla`) y `/api/requerimientos/formato-vacio` ahora responden a los 13 roles y rechazan (403) a quien no tiene rol conocido.

⁸ **Recarga bloqueada (plan niveles-paquetes-plan-maestro-rdt, 2026-09-30).** Con un Plan Maestro `APROBADO` el servicio no admite recargar el DP ni reemplazar el cronograma; sin Plan Maestro aprobado se avisa de lo que se perdería y se pide confirmación. No cambia quién puede la acción: es una precondición de negocio validada en servidor, como la nota 3 ([09](09-importar-dp.md), [15](15-cronograma.md), [20](20-plan-maestro.md)). «Gestionar Plan Maestro» ya no incluye «congelar línea base» como acción aparte: el planner programa y crea (aprueba) la primera versión; «Gestionar paquetes» incluye declarar vínculos con metrado y hitos (el cronograma ya no los edita).

⁹ **Decidido por Victor (Gate 1, 2026-09-30; aprobar el borrador, 2026-10-01).** Con un Plan Maestro aprobado, **crear** una versión nueva (el borrador, con motivo obligatorio) lo hacen solo el administrador y el jefe de proyectos; el planner conserva programar y crear la primera versión. **Aprobar** ese borrador, que reemplaza a la versión aprobada, lo hacen los tres roles de «Gestionar Plan Maestro» (administrador, jefe de proyectos y planner), igual que la primera aprobación. Implementado: crear el borrador usa `puedeCrearVersionPlanMaestro` (`POST`) y aprobar usa `puedeGestionarPlanMaestro` (`PATCH`), de modo que el código coincide con el flujo.

¹⁰ **Decidido por Victor (2026-09-30).** Reasignar un RDT de paquete mientras no esté `VALIDADO` lo hace quien valida (mismos roles que «Validar / rechazar RDT»); el supervisor que crea el RDT no reasigna, corrige reemplazando el parte ([06](06-rdt.md)). Vive en la ruta de validar del RDT (`puedeValidarRdt`); no es un permiso nuevo en el código. «Crear paquete» (acción rápida del panel) sigue la fila «Gestionar paquetes de trabajo»: administrador, jefe de proyectos y planner.

¹¹ **Decididos por Victor el 2026-10-15 (plan Informes de supervisión y Dashboard; [flujo 22](22-informes-de-supervision.md)).** Los informes emitidos, el banco de fotos del día y las inasistencias los ven y usan los 13 roles dentro de los servicios que tienen asignados (`proyecto_miembros`; el administrador ve todos); el borrador de un informe lo ve solo su autor. Los informes sin dinero los crean, editan y emiten el administrador, el jefe de proyectos, el jefe de oficina técnica y el supervisor operativo (los mismos de «Crear RDT estructurado»); el formato **Costos** solo lo crean, emiten y ven los 5 roles con datos económicos (regla 2 de la tabla 1), y el servidor responde 403 al resto también por URL directa. Sin aprobación previa de la jefatura. La foto de campo (subir una foto) la toman solo los mismos 4 roles; el banco del día lo ven y usan los 13 (decidido por Victor el 2026-10-17, que cierra la contradicción que había entre esta nota, la fila y el código). Descargar un informe sigue a verlo; el Dashboard se descarga como se ve: el archivo Parcial no lleva dinero y el Completo solo sale para los 5 roles con economía y `tipo_dashboard` COMPLETO. Rutas nuevas: `api/proyectos/[id]/informes` (con su detalle, emitir, nueva versión, descargar y formatos propios), `api/proyectos/[id]/fotos-campo`, `api/inasistencias` (y `/pdf`), `api/proyectos/[id]/dashboard/descargar` y `api/proyectos/[id]/dashboard/recurso-partidas` (esta última, `puedeVerDashboard` más alcance, solo horas). **Pendiente de Victor: reflejar estas filas en el artefacto «Matriz de permisos»** (la lista exacta está en el resumen de cierre de la tanda M del plan).

¹² **Decidido por Victor el 2026-10-15.** Cada subcontrato tiene dos formas de medir (por avance físico, o ingreso manual del monto acumulado); se elige y se escribe en el Reporte del proyecto, solo por los 5 roles con datos económicos con el servicio asignado ([flujo 10](10-generacion-pr.md)). **Editar servicio** no lleva fila nueva por esto: asignar el **supervisor operativo a cargo** (campo propio, uno por servicio) es parte de la fila existente; con el servicio en ejecución se puede cambiar pero no vaciar ([flujo 08](08-programa-portafolio-proyecto.md)). El registro de accesos suma `foto-campo` (acción, requiere servicio, `puedeTomarFotoCampo`) y el chip `informe-servicio` pasa a «Informes de supervisión» con `puedeVerInformes` ([flujo 16](16-paneles.md)).

¹³ **Decidido por Victor el 2026-10-17** (pedido: «el chip de presupuesto también está muerto, hay que habilitarlo; solo yo puedo interactuar en ellos y los demás visualizar y descargar»). Las pantallas son `/proyectos/{id}/alcance` y `/proyectos/{id}/presupuesto`; muestran el archivo de la fila del mismo nombre del checklist (un archivo por servicio, cargar otro lo reemplaza). **Cargar, reemplazar y eliminar: solo el administrador**, con la OT a su alcance; el servidor lo comprueba en cada ruta. **Ver y descargar:** Alcance lo ven y descargan los 13 roles con el servicio a su alcance; el Presupuesto, **porque trae precios**, lo ven y descargan los roles que ven el DP (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de oficina técnica, supervisor de costos y jefe de costos) — **interpretación de «los demás» pendiente de confirmar con Victor**: si quiere que los 13 roles descarguen el Presupuesto, se cambia `puedeVerPresupuestoServicio` y esta fila. La subida desde el checklist (nota 4) **convive** con la pantalla: el rol responsable puede seguir subiendo desde la fila del checklist, pero eliminar el archivo solo se hace en la pantalla, por el administrador. Eliminar quita el archivo y deja la fila sin archivo; la marca de completado no se toca.

¹⁴ **Decidido por Victor el 2026-10-17 (plan Notificaciones, ampliaciones; preguntas Q7 y Q8 aprobadas en el Gate 1).** Cada usuario, de los 13 roles, cambia desde el Perfil de Mi entorno su propio celular, su propio correo y su propia contraseña; la persona ve «Editar mi perfil» con tres bloques. El servidor usa siempre el id de la sesión (nunca uno enviado en el cuerpo) y solo acepta esos tres datos: **nombre, cargo, área y roles siguen siendo del administrador** (fila «Gestionar usuarios»). **Celular:** de 6 a 20 caracteres con dígitos, espacios, `+`, guiones y paréntesis; vacío lo borra. **Contraseña:** se pide la actual, la nueva (mínimo 8 caracteres, distinta de la actual) y su confirmación; no se escribe ninguna contraseña en respuestas ni registros. **Correo:** se pide la contraseña actual; el correo nuevo debe ser válido, distinto del actual y no usado por otro usuario; **solo rige cuando se confirma desde el buzón nuevo** y hasta entonces el perfil muestra «pendiente de confirmar» y sigue valiendo el anterior. Reemplaza la fila «Editar perfil extendido (propio)» (que era solo del administrador y el jefe de proyectos): administrador y jefe de proyectos no pierden nada, y el jefe de oficina técnica ya no «deja de editar su perfil». Rutas: `api/perfil` (celular), `api/perfil/contrasena` y `api/perfil/correo`; el permiso vive en un archivo propio (`lib/auth/perfil-propio.ts`, `puedeEditarPerfilPropio`) y `puedeEditarPerfilExtendido` ya no se usa en el perfil. Detalle en [flujo 03](03-entorno.md) y [flujo 07](07-nucleo-auth.md). **Pendiente de Victor: reflejar las tres filas en el artefacto «Matriz de permisos»** (reemplazan «Editar perfil extendido (propio)»).

¹⁵ **Decidido por Victor (plan Notificaciones, Gate 1, 2026-10-17).** **Devolver** un RQ lo hace quien ya puede aprobar (administrador, jefe de proyectos y jefe de oficina técnica), solo desde Solicitado y con un motivo obligatorio (hasta 500 caracteres); el servidor responde 403 al resto de los roles. **Corregir y reenviar** un RQ Devuelto lo hacen el solicitante del RQ y el administrador (el `*` indica «si es el solicitante»; el resto responde 403): corregir cambia fecha, prioridad, área y los ítems que ya existen (no se agregan ni se quitan) y reenviar lo devuelve a Solicitado y avisa de nuevo a quienes aprueban. Un RQ Devuelto no se aprueba ni avanza sin reenviarse. Ambas acciones exigen tener el servicio a cargo. Ciclo completo en el [flujo 05](05-rq.md); avisos en el [flujo 04](04-notificaciones.md). **Pendiente de Victor: reflejar las dos filas en el artefacto «Matriz de permisos».**

¹⁶ **Decidido por Victor (2026-10-19, tarea directa; [flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md), «Partidas transversales»).** Marcar una partida como transversal lo hacen quienes ya gestionan paquetes (administrador, jefe de proyectos y planner, con el servicio a su cargo). **Con el Plan Maestro aprobado**, el cambio solo lo prepara el administrador o el jefe de proyectos (los que pueden crear una versión nueva) y rige al aprobar esa versión ([flujo 20](20-plan-maestro.md)). Ruta nueva: `api/partidas-transversales` (el servidor valida rol, alcance y que el DP tenga la composición de mano de obra y equipo); usa `puedeGestionarPaquetesTrabajo` y, con plan aprobado, `puedeCrearVersionPlanMaestro`. No agrega chips ni cambia el [flujo 16](16-paneles.md): vive dentro de la pantalla de Paquetes. **Pendiente de Victor: reflejar la fila en el artefacto «Matriz de permisos»** (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT); esta cuenta no puede abrirlo.

¹⁷ **Decidido por Victor (2026-10-19, observación 1 del levantamiento; [flujo 22](22-informes-de-supervision.md), «Restricciones»).** La pantalla Restricciones (`/proyectos/{id}/restricciones`) la ven los **13 roles**, dentro de los servicios a su alcance. **Crean** una restricción el supervisor operativo y el supervisor SSOMA; **excepción:** quien llena el texto «restricciones» de una actividad al crear un RDT (administrador, jefe de proyectos, jefe de oficina técnica o supervisor operativo) crea una restricción a su nombre. **Recepcionan y atienden** el administrador, el jefe de proyectos y el jefe de oficina técnica (cualquiera de los tres, aunque no la haya recepcionado), y los tres reciben el aviso de las nuevas. Las fotos «para restricciones» las suben los cuatro roles de campo más el supervisor SSOMA, que solo puede subir ese uso. Todas las acciones exigen el servicio a cargo (el administrador pasa). Impacto en la Matriz de permisos: ver el artefacto (pendiente de actualizar por Victor).

¹⁸ **Decidido por Victor (2026-10-21, plan Correcciones de la prueba del RDT en PS-0001; [flujo 09](09-importar-dp.md), «Cargos del personal sin fila en el presupuesto»).** Declarar a qué fila del presupuesto equivale un cargo del personal, **también con el servicio en ejecución** (cuando Importar DP ya no abre y el RDT sí se crea), lo hacen solo el administrador y el jefe de proyectos (mismo permiso que Importar DP: `puedeImportarDp`), con el servicio a su cargo y en planeación o en ejecución (no cerrado). Ruta nueva: `PUT /api/proyectos/[id]/dp/equivalencias-cargos` (el servidor valida sesión, rol, alcance, estado y la asignación). La pantalla es una sección de la página del DP (`/proyectos/[id]/dp`): no agrega chip ni cambia el [flujo 16](16-paneles.md). **Pendiente de Victor: sumar a la Matriz de permisos «Equivalencias de cargos del servicio» (administrador y jefe de proyectos)** (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT); esta cuenta no puede abrirlo.

¹⁹ **Propuesta de roles por confirmar con Victor (2026-10-24, plan [Estado del servicio](../02-trabajo-activo/01-planes/2026-10-24-estado-del-servicio.md); [flujo 23](23-estado-del-servicio.md)).** El pedido y el alcance son de Victor; los **roles** los propuso el Orquestador porque los correos del cliente pueden traer precios y contratos. **Ven** Fuente-Gmail (pantalla, correo completo, adjuntos y minutas) el administrador, el jefe de proyectos, el jefe de oficina técnica y el supervisor de oficina técnica, dentro de los servicios a su alcance. **Gestionan** (temas, notas, ubicar correos, minutas, correos conectados y horas) solo el administrador y el jefe de proyectos. El chip «Fuente-Gmail» (grupo Jefatura) es el único acceso nuevo de servicio; `/admin/estado-servicio` y el estado del portafolio son pantallas de contenedor o globales sin chip (excepciones declaradas); `/admin/estado-servicio` se abre con un icono «Correos del cliente» en la parte baja del panel izquierdo (junto a Usuarios), solo para administrador y jefe de proyectos. Impacto en la Matriz de permisos: ver el artefacto (pendiente de actualizar por Victor, que debe compartirlo como editor).

²⁰ **Provisorio, igual que la nota ¹⁹ (2026-10-25, plan [Gestión documentaria](../02-trabajo-activo/01-planes/2026-10-25-gestion-documentaria.md); [flujo 24](24-gestion-documentaria.md)).** El chip «Gestión de emails» (id `gestion-emails`, grupo Planificación, `/proyectos/{id}/gestion-emails`) lo ven y lo gestionan los mismos roles que la Fuente-Gmail, hasta que Victor aplique al final la regla «todos ven, solo el administrador crea, edita y elimina». Impacto en la Matriz de permisos: ver el artefacto (pendiente de actualizar por Victor, que debe compartirlo como editor).

²¹ **Provisorio, igual que la nota ²⁰ para ver (2026-10-25, plan [Archivos documentarios](../02-trabajo-activo/01-planes/2026-10-25-repositorio-de-archivos-documentarios.md); [flujo 25](25-archivos-documentarios.md)).** El chip «Gestión documentaria» (id `gestion-documentaria`, grupo Planificación, `/proyectos/{id}/gestion-documentaria`) lo ven —y desde él abren y descargan archivos— los mismos cuatro roles que la Gestión de emails. **Gestiona solo el administrador** (estado a mano, etiqueta, comentario, subir, borrar lo subido y copiar adjuntos). Victor aplicará al final la regla «todos ven, solo el administrador edita». Impacto en la Matriz de permisos: ver el artefacto (pendiente de actualizar por Victor, que debe compartirlo como editor).

²² **Renombrado de apartados y fuentes nuevas (Victor, 2026-10-25; plan de la reestructuración Fuentes / Gestión documentaria).** Nombres vigentes: «Fuente-Gmail» (antes «Gestión de interesados», id `fuente-gmail`, flujo 23), «Fuente-WhatsApp» (id `fuente-whatsapp`) y «Fuente-Drive» (id `fuente-drive`), «Gestión de emails» (antes «Gestión documentaria», id `gestion-emails`, flujo 24), «Gestión documentaria» (antes «Archivos documentarios», id `gestion-documentaria`, flujo 25) y «Restricciones-Notas» (antes «Restricciones», mismo id `restricciones`). Los enlaces viejos `/estado-servicio` y `/archivos-documentarios` redirigen a las pantallas nuevas. **Provisorio:** Fuente-WhatsApp y Fuente-Drive nacen con los mismos cuatro roles que Fuente-Gmail (ven) y sin acciones propias todavía; sus permisos de gestión se definen cuando se construyan. Impacto en la Matriz de permisos: ver el artefacto (pendiente de actualizar por Victor, que debe compartirlo como editor).

### Qué se decidió al aprobar la matriz (2026-09-28)

Respecto de la matriz que regía antes, Victor fijó en el artefacto:

- **Administrador y jefe de proyectos:** acceso a todas las interfaces. En acciones, no hay una regla general de "todo menos N" — cada acción se decidió una por una en el artefacto. El jefe de proyectos pasa a poder, entre otras, adjudicar y crear programas y portafolios, archivar proyectos, eliminar contenedores, editar servicio, editar checklist, importar DP, subir documento del proyecto, editar su perfil (hoy el celular, el correo y la contraseña propios son de los 13 roles; nota ¹⁴) y ejecutar los borrados definitivos de RDT y RQ. **No** puede: asignar rol administrador ni "Ver como" (exclusivas de administrador, por diseño de sistema), ni actualizar estado de RQ ni subir el registro de costos (tareas operativas de logística; decidido por Victor el 2026-09-29).
- **Jefe de oficina técnica:** conserva adjudicar, confirmar transición, subir RDT, derivar RQ y descargar el consolidado RQ; **gana** crear RDT y validar o rechazar RDT; **deja de** archivar o eliminar proyectos, editar servicio y editar checklist (la restricción de «editar su perfil» ya no rige: desde el 2026-10-17 el celular, el correo y la contraseña propios son de los 13 roles, nota ¹⁴).
- **Supervisor de oficina técnica:** ve el DP pero **ya no lo importa** (importar DP queda para administrador y jefe de proyectos).
- **Administrador:** ahora puede crear RQ y actualizar el estado de RQ, además de lo que ya hacía.
- **Supervisor de logística:** solo sube el registro de costos; no lo ve ni lo descarga.
- **Planner:** ve y gestiona el Plan Maestro.
- **Jefe de costos:** ve las interfaces con economía, igual que el supervisor de costos.
- **Elegir servicio** (2026-10-15, flujo 16): la abre cualquier rol que tenga permitido el chip de origen; no da acceso nuevo, porque solo lista los servicios vigentes y la pantalla de destino valida rol y alcance. No necesita fila propia en la matriz de permisos.
- **Recursos (Personal, Cargos, Equipos, Causas CNC):** administrador y jefe de proyectos pueden crear, editar y eliminar (o desactivar) en los cuatro por igual, y editar el texto de una causa CNC. Construir lo que falta (editar/eliminar Personal; crear/editar/eliminar Cargos y Equipos; editar texto de Causas CNC) es trabajo nuevo para el Worker, no solo una guardia de permisos. **Eliminar y desactivar son dos acciones distintas** (Victor, 2026-10-15: «existe inactivo, pero no eliminar»): desactivar oculta el registro y se puede revertir; eliminar lo borra de verdad **aunque ya se haya usado** (Victor, 2026-10-15). Los RDT conservan el nombre, DNI, cargo o descripción que copiaron y solo pierden el enlace al catálogo; los trabajadores conservan el texto de su cargo; las equivalencias de DP que apuntaban al cargo o equipo se borran, así que el próximo DP de ese servicio vuelve a preguntar por ese texto. Pide confirmación en la misma fila antes de borrar.
- **Rebase del catálogo de Cargos y Equipos desde presupuestos reales (Victor, 2026-10-15):** el catálogo se vació por completo y se recargó desde 4 servicios (PS-140 CCI, PS-167 Tecnet, PROPUE_1 Jahuay, Villa Fase 2), migración `097`. Reglas de extracción: los cargos salen del bloque «Mano de obra» del APU **más las secciones 1 (Área Técnica) y 2 (Empleado/Administración) de Gastos Generales** — amplía la regla original de `025`, que solo usaba el APU — y siempre quedan en HH; los equipos salen del bloque «Equipo:» del APU con su unidad tal cual, excluido el `%MO` (herramienta manual); los bloques «Sub Partidas:» y «Subcontratos:» del APU no son insumos; descripción normalizada sin tildes, MAYÚSCULAS, espacios colapsados, punto final quitado; las categorías de equipo son `vehiculo` / `maquinaria` / `equipo_menor` / `herramienta_electrica` / `herramienta` (las herramientas viven dentro de Equipos, no hay tabla aparte). Materiales y subcontratos no se catalogan como recursos de empresa. Base de datos en Excel y trazabilidad: `docs/06-material-de-apoyo/Informacion para pruebas/base-datos-recursos-4-servicios.xlsx`.

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
| Enviar mensaje a un usuario o a un rol | ✓ | Solo si el mensaje es de un servicio: tener ese servicio a cargo (el administrador pasa). No para «Entorno» (mensaje sin servicio) ni para un aviso a uno mismo |
| Marcar como visto / revisar / atender | ✓ (según sea destinatario) | Sí si el aviso tiene servicio (la ruta resuelve el `proyecto_id` de la notificación); los avisos de «Entorno» no lo exigen |

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
La restricción está **decidida y escrita** en la tabla 1 (2026-09-28) y **aplicada** el 2026-10-02 (plan `2026-10-01-dashboard-economia-y-curva-s`): el Dashboard Parcial (sin dinero, 13 roles), el Dashboard Completo (con dinero, 5 roles) y los dos modos de la Curva S ya respetan la separación económica; el servidor fuerza Parcial y rechaza con 403 el modo económico sin permiso. La entrada «Dashboard Parcial sin datos económicos y restricción económica definitiva» se **retira** de `planes-futuros.md` por quedar promovida a ese plan.
