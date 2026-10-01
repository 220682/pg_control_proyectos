# Arquitectura funcional y modelo de datos

> Movido desde `AGENTS.md` el 2026-10-01 sin cambios de contenido, para que `AGENTS.md` quede por debajo de 200 líneas. Las reglas operativas siguen en `AGENTS.md`; este documento describe cómo está organizado el sistema.

## Arquitectura funcional

La organización funcional que aparece con mayor consistencia es la siguiente:

- Autenticación.
- Usuarios y permisos.
- Servicios y proyectos.
- Presupuesto / DP.
- Cronograma.
- Paquetes de trabajo.
- Plan Maestro.
- Plan semanal / 3WLA.
- RDT.
- PR.
- Dashboard.
- RQ.
- Notificaciones.

### Flujo principal documentado

1. Presupuesto + alcance.
2. Cronograma.
3. Relación WBS ↔ cronograma.
4. Plan Maestro.
5. Plan semanal / 3WLA.
6. RDT.
7. PR.
8. Dashboard.

La regla central documentada es que el sistema no debe mezclar:
- lo planificado,
- lo ejecutado,
- lo estimado,
- lo consolidado,
- y la vista ejecutiva.

## Modelo de datos y fuentes de verdad

### Presupuesto / DP
Fuente del alcance, partidas, metrados y costos base.
- Es la base contractual del proyecto.
- No debe confundirse con ejecución real.

### Cronograma
Fuente de fechas, duración y secuencia.
- Define cuándo se ejecuta cada actividad.
- No es, por sí solo, la fuente del costo programado semanal.

### Plan Maestro
Fuente del valor planificado temporal.
- Reparte metrado y costo por semana.
- Es el origen del PV.
- No reemplaza el plan semanal operativo.

### RDT validado
Fuente del avance real y de los costos reales medidos.
- Alimenta la ejecución real y validación del campo.
- Los materiales sin control real no deben convertirse en costo real sin validación.

### PR
Consolidado técnico del proyecto.
- No es la fuente original del alcance ni del cronograma.
- Sí es la capa de consolidación entre plan y real para análisis técnico.

### Dashboard
Vista derivada.
- Consume el PR y el historial.
- No es fuente de datos; es una representación ejecutiva del estado del proyecto.

### Paquetes de trabajo
Agrupación operativa opcional.
- No reemplazan la partida contractual ni la estructura base del presupuesto.
