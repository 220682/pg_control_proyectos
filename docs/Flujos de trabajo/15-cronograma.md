# 15 — Cronograma

**Fase 1 implementada (en main, 2026-09-16/17).** Importa Excel (plantilla WBS de programación, rotulada EDT si así viene del origen/Nombre de tarea/Duración/Comienzo/Fin/Predecesoras/Sucesoras) o PDF exportado de MS Project, y genera un **informe de extracción** (cuántas actividades se leyeron, cuántas quedaron completas, cuántas se enlazaron al DP). No lee `.mpp` nativo.

Un cronograma por servicio (`proyecto_cronograma`, `proyecto_id` como llave — volver a subir reemplaza el anterior completo). Actividades en `cronograma_actividades`, tipo TAREA/HITO/RESUMEN.

**Terminología:** EDT y WBS son la misma estructura de descomposición. Para evitar ambigüedad, este flujo llama **WBS de programación** al código de la actividad del cronograma, aunque MS Project o el PDF lo rotule como `EDT`; llama **WBS presupuestal** al código contractual de la partida en DP. Pueden coincidir literalmente, pero no se reescriben para forzarlo.

**Enlace de trazabilidad: SOLO contra DP.** El cronograma relaciona cada tarea con la partida `dp_partidas` que ejecuta (WBS presupuestal), **nunca contra PR**. Si WBS de programación y WBS presupuestal coinciden, el enlace se propone automáticamente; si difieren, se registra un vínculo explícito sin cambiar ninguno de los dos códigos.

Predecesoras/sucesoras son informativas: su ausencia no marca la fila como incompleta.

**Quién sube/reemplaza:** Geren (jefe_de_proyectos, administrador) y Planner. **Quién ve:** todos menos asistente.

Pantalla: `/cronograma` (selector de OT + carga + informe). Chip **Cronograma**, único en el apartado "Planificación" del entorno del usuario — aparece en todos los grupos salvo deshabilitado para asistente. También en el panel de accesos por servicio (`nav-proyecto.ts`, grupo Planificación).

**Duración del servicio:** las tarjetas de Portafolio y el Dashboard de servicio ahora prefieren la duración calculada del Cronograma (fecha de inicio más temprana → fecha de fin más tardía) sobre la fórmula del presupuesto (que hoy siempre da sin dato, ver flujo 11).

## Pendiente (fase 2, no construida)

- Interfaz Gantt: barra base (fija) + barra de avance real (editable, puede quedar antes/después/más corta/más larga).
- Candado de checklist "Cronograma" antes de pasar de "En Planeación" a "Ejecución".
- Restringir el reemplazo a Geren solo mientras el servicio siga "En Planeación" (hoy cualquiera con permiso de subir puede reemplazar en cualquier momento).
- Flujo 17 (Chat agéntico) usaría el informe de extracción como base.

Código: `src/lib/cronograma/` (parsers + informe), `src/app/api/cronograma/route.ts`, `db/036_cronograma.sql`.
