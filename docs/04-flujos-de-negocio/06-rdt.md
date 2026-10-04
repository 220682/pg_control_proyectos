# 06 — RDT (Registro diario de trabajo)
> Lee si: la tarea toca el RDT, sus pantallas, o crear un RDT desde el Plan Maestro. No lo confundas con la OT (flujo 13).


Archivo (foto/PDF) ligado a una OT vigente. Fecha Lima `dd-mm-yyyy HH:mm`.

**Catálogo de disciplinas (O10, Victor 2026-10-02):** ampliado de 5 a 8 disciplinas (migración `090`): Civil, Mecánica, Eléctrica, Instrumentación, Tuberías, **Preliminares**, **Cierre**, **Subcontratos**.

**Quién puede qué** (fuente única: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md); no se repiten aquí):

* **Ver** Status de RDTs, Archivo de RDTs subidos y Consolidado RDTs: los 13 roles (no llevan datos económicos). Sin alcance por OT al leer (R30): el servicio de la URL solo preselecciona el filtro N° OT.
* **Subir RDT** (PDF o foto) y **crear RDT estructurado** (PROM-GP-002): administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo. SSOMA no sube (v1).
* **Validar o rechazar RDT:** administrador, jefe de proyectos y jefe de oficina técnica. **Rechazar un RDT ya validado** (destraba para corregir y dispara el recálculo del PR): solo administrador y jefe de proyectos. Corregir un RDT rechazado: administrador, jefe de proyectos y supervisor operativo.
* **Descargas:** RDTs según filtro (ZIP), listado de RDTs (PDF PROM-GP-0006), PDF de un RDT estructurado y archivo de un RDT subido: los 13 roles; un usuario sin rol conocido queda rechazado.
* **Borrar RDT:** administrador y jefe de proyectos (regla transversal «Borrado administrador» del [índice](README.md)); ver más abajo.

Notificación al subir: solo Administración.

## Pantallas

| Pantalla | Ruta | Contenido |
|---|---|---|
| Subir RDT | Mi entorno `?accion=subir-rdt` | Formulario de subida (solo si el rol puede subir) |
| Crear RDT | `/rdts/crear` | RDT estructurado (PROM-GP-002); requiere Plan Maestro aprobado **y** servicio en Ejecución |
| **Status de RDTs** | `/rdts/status` | Tabla de RDTs con su estado; aquí se valida, rechaza y corrige según el rol |
| **Archivo de RDTs subidos** | `/rdts/listado` | Los PDF y fotos que llegaron en papel; **aquí se borra un RDT** (columna de borrado solo para quien puede) |
| Consolidado RDTs | `/rdts/consolidado` | Consolidado por filtros |
| Carpeta | `/rdts` | Carpeta de RDTs |

Nav del apartado Supervisión operativa: Crear RDTs, Subir RDTs, Status de RDTs, Archivo de RDTs subidos y Consolidado RDTs. Chip **Subir RDTs** en Accesos rápidos. Las pantallas reciben el servicio con `?proyectoId=` y lo preselecciona en el filtro N° OT. Chips de descarga: **Descargar RDTs (según filtro)** (ZIP) y **Descargar listado RDTs (según filtro)** (PDF PROM-GP-0006). Encabezado PDF: **Fecha y hora** (sin “(Lima)”). Chip **Salir a Mi entorno** (con servicio elegido conserva `?proyectoId=`, flujo 16 regla 7).

**Borrar RDT:** solo en el Archivo de RDTs subidos (`/rdts/listado`); administrador y jefe de proyectos. Es un borrado definitivo: cubre el archivo y el parte estructurado y dispara el recálculo del PR.

No es el flujo OT: solo se vinculan por N° OT.

**RDT validado alimenta el PR.** Toda actividad registrada (D, C y NC) se carga a un **paquete × partida del Plan Maestro aprobado** (o a una partida directa) — solo las D generan metrado ejecutado; C y NC aportan horas y costo, sin avance (regla 12 de negocio, ver [18-control-avance.md](18-control-avance.md)). El metrado programado del RDT es informativo, no oficial. El CNC (causa de no cumplimiento) se registra contra un catálogo mantenible y es obligatorio para actividades NC.

## Crear RDT con el Plan Maestro (2026-09-30)

- **Para crear un RDT hacen falta dos condiciones (U1, Enmienda E1 2026-10-03): el Plan Maestro aprobado y el servicio en Ejecución.** La pantalla `/rdts/crear` avisa si falta alguna y bloquea el guardado; el servidor lo rechaza (400) con un mensaje que nombra las dos condiciones, antes de escribir. Los roles no cambian.
- **Las dos condiciones valen para toda vía de creación de un RDT (U9, 2026-10-04), no solo para la pantalla `Crear RDT`:** el RDT estructurado, la **carga por archivo** (foto o PDF) y las que se creen después. La congelación del Plan Maestro es de los datos de **planeación**; el registro de ejecución sigue funcionando, pero ninguna vía de creación se salta las dos condiciones.
- **Las dos condiciones son de creación, no de operación (U9, precisado el 2026-10-04).** Las exige **crear** un RDT, por cualquier vía. Una vez que el RDT **existe**, las acciones sobre él —reasignarle el paquete, corregirlo, validarlo o rechazarlo— siguen exigiendo **solo Plan Maestro aprobado**: el servicio no tiene que estar en Ejecución para hacerlo.
- **Qué elige el supervisor.** En lugar de las partidas del DP agrupadas por subpresupuesto, el selector de actividad lista **los paquetes del Plan Maestro aprobado** (plegables, con búsqueda) y las **partidas directas** aparte. **Declaración por paquete:** el supervisor selecciona el paquete completo (WBS muestra "PQ-001" o abreviación); las demás partidas del paquete se calculan automáticamente con el mismo % (compatible con `es_derivada` de migración 083). Solo cuando hay partidas no asignadas a paquetes (partidas directas), se declaran individualmente. Cada actividad guarda su clave `paquete|DIRECTA : partida`; el servidor impone el WBS del plan. Las actividades **C y NC, los equipos y los materiales** tienen **libertad de WBS**: pueden elegir cualquier partida del Plan Maestro sin depender de una actividad D previa declarada ese día (cambio de la observación O13 de Victor, 2026-10-02). Los materiales llevan las claves de sus partidas; deben existir en el plan.
- **Colores del avance real** en el selector: 0 % blanco, en curso amarillo, 100 % verde con ✓ (solo avance real; flujo 18). «Avance real (%)» de una partida = Met. acum. del servicio sobre la suma de sus metrados en el plan.
- **Modo «por avance del paquete».** Si el paquete se mide por su partida guía ([flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)), el supervisor declara solo la unidad de la guía; el servidor calcula el mismo % para las demás partidas y guarda **una fila derivada de solo lectura por cada partida** (como actividad propia, marcada `es_derivada`, con su metrado derivado). Las derivadas se ven bajo la guía y no se envían desde el navegador; no llevan horas propias ni duplican las horas o el metrado declarados. **Las filas derivadas cuentan como actividad en la columna «Activ.» de Status y en el PPC** (decisión de Victor): suben `actividades_acum` de su partida (el motor del PR no cambia).
- **«Met. acum.»** en Crear RDT es el **acumulado del servicio en total para esa partida** (incluye las derivadas, de todos los paquetes en que esté repartida). El real **por paquete × partida** vive solo en el Plan Maestro (flujo 20); el real **por partida** es el que alimenta al PR (flujo 10).
- **Reasignar el paquete.** Mientras el RDT esté `REGISTRADO` o `REVISADO` (no `VALIDADO`), quien puede validar (administrador, jefe de proyectos y jefe de oficina técnica) puede reasignarlo de paquete; al validar también puede asignar la clave. Recalcula las derivadas. El supervisor que registra corrige reemplazando el parte.
- **Status y Consolidado.** Status suma la columna y el filtro «Paquete» (ocultos si ningún parte tiene paquete). El Consolidado suma el filtro «Paquete de trabajo» (se combina con el de partidas del DP) y la etiqueta del paquete en las filas de partidas. Sin paquetes, el aspecto no cambia.
- Un RDT anterior sin paquete se valida solo si su partida está como directa en el plan aprobado.

## Reposicionamiento de los RDT al aprobar un Plan Maestro nuevo (U4/U7, Enmienda E1 2026-10-03)

- **Al aprobar un Plan Maestro nuevo, los RDT se reposicionan**: se vuelven a **asociar a las líneas del plan vigente**, por la clave de reporte `paquete × partida`, para que el Plan Maestro muestre ese RDT en las fechas y metrados de la nueva línea base. Alcanza a **todos** los RDT del servicio, **incluidos los validados**.
- **Antes de confirmar esa aprobación se pide y se muestra un aviso de qué RDT van a cambiar** (U6, [flujo 20](20-plan-maestro.md) §3). La confirmación es lo que aplica el reposicionamiento.
- **Lo que el reposicionamiento NO cambia (aclaración de Victor, 2026-10-04):** no reescribe el metrado ejecutado, ni los metrados derivados, ni las horas, ni el estado de validación, ni los archivos, y **no cambia las cifras del PR consolidado**: en el PR los RDT siguen declarados como estaban. El PR agrupa el real por partida, no por paquete, así que no se mueve.
- **Lo que SÍ cambia es la asociación de paquete del RDT** (`rdt_actividades.paquete_trabajo_id` y `rdt_actividad_partidas.paquete_trabajo_id`), que es la clave de reporte `paquete × partida`: entre el RDT y la línea del plan no hay FK y no hay tabla de unión. Por eso un RDT ya registrado puede **verse con otro paquete en su propio formulario y en la pantalla Status**, y no solo en el Plan Maestro (corrección del Auditor, 2026-10-04: lo escrito antes decía «no cambia los datos del RDT», y eso era más fuerte que lo que el código garantiza).
- **El reposicionamiento deja rastro en el historial de cada RDT:** una fila con la acción `REPOSICIONAMIENTO`, cuyo `snapshot` guarda **el plan anterior, el plan nuevo y su versión, el diff de claves** (de qué clave pasó a cuál) **y quién aprobó el Plan Maestro**. **No guarda fecha ni metrado como dato consultable**: qué se movió se lee en el diff de claves. Sin historial sería un cambio invisible sobre datos ya validados.
- **Casos sin resolver, pendientes de decisión:** un RDT que apunta a una partida que ya no está en el plan queda sin línea y no se reasocia por WBS; y una partida presente en dos líneas con paquetes distintos se considera ambigua y no se reposiciona. Ninguno de los dos casos rompe datos: no se tocan. Se resuelven con una regla nueva, no por interpretación. **Lo que sí ocurre hoy con el primero:** la aprobación lo devuelve en su respuesta como **aviso** (los vínculos que quedan sin línea), para que no desaparezcan en silencio; no escribe fila de historial ni reasocia.
- No es una edición que haga el usuario sobre el RDT: es un efecto de la aprobación, dentro del mismo paso, en el orden **Plan Maestro → reposicionamiento de RDT → recálculo del PR**, todo o nada (flujo 20, U8).

## Disciplinas (observación O10 de Victor, 2026-10-02)

- **Catálogo ampliado de 8 disciplinas:** Civil, Mecánica, Eléctrica, Instrumentación, Tuberías, **Preliminares, Cierre, Subcontratos** (agregadas en migración 090).
- **Plegable en disciplinas:** el selector de actividades del RDT agrupa los paquetes por disciplina (plegable), facilitando la navegación cuando hay muchos paquetes.
- La partida directa lleva su propia disciplina, obligatoria. La partida dentro de un paquete hereda la del paquete.

Spec: `docs/superpowers/specs/2026-08-20-rdt-design.md`.
