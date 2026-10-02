# Flujos de negocio

## Qué vive acá

Las reglas funcionales y operativas permanentes del sistema, una vez por tema dueño (migradas desde `docs/Flujos de trabajo/`): pantallas, roles, subflujos y archivos de cada tema. Al desplegar una mejora, se actualiza el MD del flujo que corresponda.

**Interfaz:** al crear una pantalla nueva o modificar una existente en `py_control_proyectos_web`, la convención obligatoria de diseño/UI es [`../05-diseno-y-referencias/design.md`](../05-diseno-y-referencias/design.md) — layout, tokens, componentes, columnas, accesibilidad. Leerlo antes de tocar cualquier interfaz.

## Índice de los 21 flujos, con su disparador

Cada flujo abre con una línea `Lee si:` que dice en qué situación hace falta. **El disparador es la puerta de entrada**: si ninguna línea de la tarea coincide con él, ese flujo no se abre. Por eso la tabla de abajo basta para decidir, y no hace falta leer los flujos para saber cuáles_skip.

| # | Flujo | Cuándo abrirlo | Archivo |
|---|--------|----------------|---------|
| 01 | Configuración (pendiente de definir) | shell, login, móvil o el apartado Proyectos del panel izquierdo | [01-configuracion.md](01-configuracion.md) |
| 02 | Usuarios | crear, editar o borrar usuarios, roles, cargo o área | [02-usuarios.md](02-usuarios.md) |
| 03 | Entorno por rol | «Mi entorno», sus chips o herramientas por rol | [03-entorno.md](03-entorno.md) |
| 04 | Notificaciones | bandeja, chips de aviso, y a quién se notifica o no | [04-notificaciones.md](04-notificaciones.md) |
| 05 | Requerimiento de servicios (RQ) | crear, aprobar o rechazar un RQ; subflujos y estados | [05-rq.md](05-rq.md) |
| 06 | RDT | el RDT, sus pantallas, o crearlo desde el Plan Maestro | [06-rdt.md](06-rdt.md) |
| 07 | Núcleo / auth | login, sesión con cookie, `NEXT_PUBLIC_SITE_URL` | [07-nucleo-auth.md](07-nucleo-auth.md) |
| 08 | Programa / portafolio / proyecto | adjudicar, crear, archivar o eliminar contenedores | [08-programa-portafolio-proyecto.md](08-programa-portafolio-proyecto.md) |
| 09 | Importar DP | importación, sus tres fases, confirmación de niveles, informes | [09-importar-dp.md](09-importar-dp.md) |
| 10 | Generación PR | el PR, sus tres bloques, cuándo se recalcula, relación con Dashboard | [10-generacion-pr.md](10-generacion-pr.md) |
| 11 | Dashboard | los dos dashboards, filtros, indicadores, diagnóstico | [11-dashboard.md](11-dashboard.md) |
| 12 | Checklist editable | catálogo definitivo o grupos de acción | [12-checklist.md](12-checklist.md) |
| 13 | Orden de trabajo (OT) | la OT o su número. Hoy no hay UI | [13-orden-de-trabajo.md](13-orden-de-trabajo.md) |
| 14 | Accesos y restricciones | **cualquier** interfaz, permiso, acción o acceso nuevo o modificado | [14-accesos-y-restricciones.md](14-accesos-y-restricciones.md) |
| 15 | Cronograma | cronograma, sus hitos, o su relación con Paquetes | [15-cronograma.md](15-cronograma.md) |
| 16 | Paneles | navegación, tres paneles, panel izquierdo, chips, asistente del shell | [16-paneles.md](16-paneles.md) |
| 17 | Chat agéntico | agente conversacional. Hoy deshabilitado | [17-chat-agentico.md](17-chat-agentico.md) |
| 18 | Control de avance | tres universos, estructura longitudinal, cálculos, RDT → Plan Maestro | [18-control-avance.md](18-control-avance.md) |
| 19 | Paquetes de trabajo y jerarquía de control | agrupar en paquetes, jerarquía de control o modo de medición | [19-paquetes-de-trabajo-y-jerarquia-de-control.md](19-paquetes-de-trabajo-y-jerarquia-de-control.md) |
| 20 | Plan Maestro | fuentes de verdad, flujo implementado, permisos, fase 2 | [20-plan-maestro.md](20-plan-maestro.md) |
| 21 | Curva S | reglas fijas, granularidad, endpoint, pantalla propia | [21-curva-s.md](21-curva-s.md) |

**Borrado administrador** no es un flujo: es una regla transversal: el borrado definitivo de RQ, RDT, proyecto (archivar y eliminar), programa y portafolio lo ejecutan solo el administrador y el jefe de proyectos (tabla 2 del [flujo 14](14-accesos-y-restricciones.md)); ningún otro rol, el jefe de oficina técnica incluido. Está citada en [05](05-rq.md), [06](06-rdt.md) y [08](08-programa-portafolio-proyecto.md).

**Plan en curso que reescribe flujos (2026-09-30):** [`niveles-paquetes-plan-maestro-rdt`](../02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md) actualiza los flujos 06, 09, 10, 14, 15, 16, 18, 19, 20 y 21 según su tabla en bloque aprobada por Victor; mientras no se cierre, el estado de cada fila está en esa tabla.

**Plan de observaciones de Victor, Lote 1 (cerrado con Gate 2 el 2026-10-02):** [`observaciones-victor`](../02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-plan.md) reescribió los flujos 02 (área `JF` = "Jefatura") y 12 (catálogo definitivo del checklist y completar por check).

**Plan de observaciones de Victor, Lote 2 (cerrado, 2026-10-02):** [`observaciones-victor-lote-2`](../02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-2-plan.md) actualiza los flujos 08 (el checklist completo para cerrar no cuenta los documentos de fase CIERRE), 12 (grupos de acción por fila, subida solo en el Grupo A y «Acta de conformidad» fuera de la lista), 14 (acción «Subir documento» acotada al Grupo A y a los personalizados) y 15 (mensaje específico y log en servidor al fallar la importación del cronograma).

## Qué no vive acá

Bitácoras de sesión, estado de planes o procedimientos de agentes — eso vive en `../00-estandar-agentes/` y `../02-trabajo-activo/`.

## Regla de lectura y actualización

**Lectura por rol (D10):** **ningún rol lee los 21 flujos por costumbre.** Los cuatro leen el índice de este archivo —la tabla de disparadores de arriba— y abren solo los flujos cuyo `Lee si:` coincide con su tarea. El Worker va más acotado: solo los que el plan declara afectados por su parte. La lista completa se lee únicamente si el plan toca más de la mitad de los flujos, o si el Auditor necesita comparar dos flujos enteros porque detectó un conflicto entre reglas. Regla completa en [`../00-estandar-agentes/04-flujo-sdd-y-planes.md`](../00-estandar-agentes/04-flujo-sdd-y-planes.md).

**Al agregar o cambiar un flujo:** su línea `Lee si:` es parte del flujo y se escribe con él. Si el disparador no describe algo que el flujo realmente contiene, está mal: el disparador no promete alcance que el flujo no tenga.

Una regla se escribe una sola vez, en su flujo dueño; otros documentos enlazan, no copian. Se actualiza solo cuando una decisión de negocio fue validada y aprobada por el Responsable humano (ver `../00-estandar-agentes/05-aprendizaje-continuo.md`).

**Checklists de verificación:** cada mejora o fase implementada tiene su checklist en la Punch List interactiva (ver `../02-trabajo-activo/01-planes/README.md`), así la implementación se haya seccionado en varias fases o sub-lotes.
