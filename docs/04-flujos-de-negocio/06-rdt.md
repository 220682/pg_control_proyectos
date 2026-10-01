# 06 — RDT (Registro diario de trabajo)

Archivo (foto/PDF) ligado a una OT vigente. Fecha Lima `dd-mm-yyyy HH:mm`.

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
| Crear RDT | `/rdts/crear` | RDT estructurado (PROM-GP-002); requiere Plan Maestro aprobado |
| **Status de RDTs** | `/rdts/status` | Tabla de RDTs con su estado; aquí se valida, rechaza y corrige según el rol |
| **Archivo de RDTs subidos** | `/rdts/listado` | Los PDF y fotos que llegaron en papel; **aquí se borra un RDT** (columna de borrado solo para quien puede) |
| Consolidado RDTs | `/rdts/consolidado` | Consolidado por filtros |
| Carpeta | `/rdts` | Carpeta de RDTs |

Nav del apartado Supervisión operativa: Crear RDTs, Subir RDTs, Status de RDTs, Archivo de RDTs subidos y Consolidado RDTs. Chip **Subir RDTs** en Accesos rápidos. Las pantallas reciben el servicio con `?proyectoId=` y lo preselecciona en el filtro N° OT. Chips de descarga: **Descargar RDTs (según filtro)** (ZIP) y **Descargar listado RDTs (según filtro)** (PDF PROM-GP-0006). Encabezado PDF: **Fecha y hora** (sin “(Lima)”). Chip **Salir a Mi entorno** (con servicio elegido conserva `?proyectoId=`, flujo 16 regla 7).

**Borrar RDT:** solo en el Archivo de RDTs subidos (`/rdts/listado`); administrador y jefe de proyectos. Es un borrado definitivo: cubre el archivo y el parte estructurado y dispara el recálculo del PR.

No es el flujo OT: solo se vinculan por N° OT.

**RDT validado alimenta el PR.** Toda actividad registrada (D, C y NC) se carga a un **paquete × partida del Plan Maestro aprobado** (o a una partida directa) — solo las D generan metrado ejecutado; C y NC aportan horas y costo, sin avance (regla 12 de negocio, ver [18-control-avance.md](18-control-avance.md)). El metrado programado del RDT es informativo, no oficial. El CNC (causa de no cumplimiento) se registra contra un catálogo mantenible y es obligatorio para actividades NC.

## Crear RDT con el Plan Maestro (2026-09-30)

- **Sin Plan Maestro aprobado no se puede crear un RDT estructurado:** la pantalla `/rdts/crear` muestra el aviso «Sin Plan Maestro aprobado» y bloquea el guardado; el servidor lo rechaza (400). Los roles no cambian.
- **Qué elige el supervisor.** En lugar de las partidas del DP agrupadas por subpresupuesto, el selector de actividad lista **los paquetes del Plan Maestro aprobado** (plegables, con búsqueda) y las **partidas directas** aparte. Cada actividad guarda su clave `paquete|DIRECTA : partida`; el servidor impone el WBS del plan. Las actividades **C y NC, los equipos y los materiales** se cargan a un paquete × partida eligiendo entre las actividades D declaradas ese día (los materiales llevan las claves de sus partidas; deben existir en el plan); al quitar o cambiar una D se limpian las referencias que dependían de ella.
- **Colores del avance real** en el selector: 0 % blanco, en curso amarillo, 100 % verde con ✓ (solo avance real; flujo 18). «Avance real (%)» de una partida = Met. acum. del servicio sobre la suma de sus metrados en el plan.
- **Modo «por avance del paquete».** Si el paquete se mide por su partida guía ([flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)), el supervisor declara solo la unidad de la guía; el servidor calcula el mismo % para las demás partidas y guarda **una fila derivada de solo lectura por cada partida** (como actividad propia, marcada `es_derivada`, con su metrado derivado). Las derivadas se ven bajo la guía y no se envían desde el navegador; no llevan horas propias ni duplican las horas o el metrado declarados. **Las filas derivadas cuentan como actividad en la columna «Activ.» de Status y en el PPC** (decisión de Victor): suben `actividades_acum` de su partida (el motor del PR no cambia).
- **«Met. acum.»** en Crear RDT es el **acumulado del servicio en total para esa partida** (incluye las derivadas, de todos los paquetes en que esté repartida). El real **por paquete × partida** vive solo en el Plan Maestro (flujo 20); el real **por partida** es el que alimenta al PR (flujo 10).
- **Reasignar el paquete.** Mientras el RDT esté `REGISTRADO` o `REVISADO` (no `VALIDADO`), quien puede validar (administrador, jefe de proyectos y jefe de oficina técnica) puede reasignarlo de paquete; al validar también puede asignar la clave. Recalcula las derivadas. El supervisor que registra corrige reemplazando el parte.
- **Status y Consolidado.** Status suma la columna y el filtro «Paquete» (ocultos si ningún parte tiene paquete). El Consolidado suma el filtro «Paquete de trabajo» (se combina con el de partidas del DP) y la etiqueta del paquete en las filas de partidas. Sin paquetes, el aspecto no cambia.
- Un RDT anterior sin paquete se valida solo si su partida está como directa en el plan aprobado.

Spec: `docs/superpowers/specs/2026-08-20-rdt-design.md`.
