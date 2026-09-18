# 18. Control de avance

## Objetivo

Establecer el control del avance del proyecto integrando:
- presupuesto y alcance
- cronograma
- Plan Maestro
- Plan semanal / 3WLA
- RDTs
- PR (Reporte del Proyecto)
- Dashboard con Curva S

La idea es construir una cadena lógica de control donde el avance real se compare contra lo programado sin mezclar conceptos.

## Flujo base

1. Presupuesto + alcance
   - Define la línea base contractual.
   - Nace el WBS / partida de obra.
   - Cada WBS trae unidad, metrado contractual, costo base y descripción del trabajo.

2. Cronograma
   - Define fechas, duración y secuencia de actividades.
   - La actividad del cronograma recibe el WBS que le corresponde.
   - El WBS no vive aislado: se une a la programación del cronograma.

3. Relación WBS ↔ cronograma
   - Conecta cada partida contractual con la actividad del cronograma que la ejecuta.
   - Es la pieza clave para poder repartir metrado en el tiempo.
   - Aquí nace la vinculación: WBS + fecha + actividad + duración.
   - Sin esta relación, no se puede transformar el presupuesto en un plan temporal real.

4. Plan Maestro
   - Toma el WBS, la relación con el cronograma y la duración de cada actividad.
   - Reparte el metrado y el costo por semana.
   - Genera PV semanal y PV acumulado.
   - Es la base del avance programado.
   - Es la respuesta a la pregunta: ¿cuánto trabajo y cuánto costo se debía haber ejecutado en cada semana?

5. Plan semanal / 3WLA
   - Se crea a partir del Plan Maestro y se ajusta a corto plazo.
   - Define qué se compromete a ejecutar esta semana.
   - Se modifica durante la obra, pero no reemplaza al Plan Maestro.
   - Es la programación operativa del trabajo real que va a ejecutarse.
   - Responde a: ¿qué se va a hacer esta semana?

6. RDT
   - Se alimenta de la ejecución del campo.
   - Registra avance físico, HH, HM, observaciones y productividad real.
   - Es la medición real que valida si lo que se ejecutó coincide con lo programado.
   - Responde a: ¿qué se hizo realmente?

7. PR (Reporte del Proyecto)
   - Recibe dos entradas principales:
     - Plan Maestro (programado)
     - RDT (real)
   - Consolida por partida el plan y la ejecución.
   - Compara WBS por WBS y calcula el estado real del proyecto.
   - Es la fuente técnica del control del proyecto.
   - Responde a: ¿qué estaba planificado, qué se ejecutó, cuánto costó y qué tan bien va cada WBS?

8. Dashboard
   - Toma el PR y el historial semanal.
   - Muestra Curva S, acumulados, variación y tendencia del proyecto.
   - Es la vista ejecutiva, no el detalle técnico.
   - Responde a: ¿cómo va el proyecto en conjunto?

### Qué debe quedarse muy claro sobre el Plan Maestro

El Plan Maestro no es un cronograma simple ni una vista de avance. Es la capa intermedia que convierte el presupuesto + cronograma en una línea base temporal semanal.

Su función es construir el PV y el costo planificado por semana para cada WBS, a partir de:
- metrado contractual del presupuesto
- duración y fechas del cronograma
- relación WBS ↔ cronograma

Esto hace que el avance programado exista como dato medible, y así pueda compararse con la ejecución real del RDT.

## Criterio de datos

### Presupuesto y alcance
- Son la base contractual del proyecto.
- No cambian por la ejecución en campo.

### Cronograma
- Define cuándo se ejecuta.
- No tiene la lógica de metrado semanal por sí solo.

### Plan Maestro
- Sí define el metrado/costo programado por semana.
- Es la base del PV.

### Plan semanal / 3WLA
- Define el compromiso operativo real de la semana.
- Puede ajustarse sobre la marcha.

### RDT
- Es la medición real del trabajo ejecutado.
- Alimenta EV, AC real medido y avance físico real.

### PR
- Es el consolidado operando con plan + real.
- Es la fuente principal para análisis por partida y para el dashboard.

### Dashboard
- Resume el proyecto para la toma de decisiones.
- La Curva S vive dentro del dashboard y se alimenta del historial semanal.

## Qué debe quedarse claro

### Avance programado
- Se registra en el Plan Maestro.
- Es el PV.

### Avance real
- Se registra en el RDT.
- Es el EV.

### Costo real
- MO, equipos y subcontratos medidos: costo real.
- Materiales sin control real: estimación provisional.
- AC material estimado no debe confundirse con AC real medido.

## Regla de diseño

Las capas deben mantenerse separadas:
- plan
- real
- estimación
- consolidado
- dashboard

Esto evita mezclar el avance programado con lo ejecutado y evitar que el material no medido se vuelva “real” sin validación.

## En resumen

El sistema se construye así:

Presupuesto + alcance -> cronograma -> WBS↔cronograma -> Plan Maestro -> Plan semanal / 3WLA -> RDT -> PR -> Dashboard

Y la regla final es:

- los materiales, si no tienen control real, quedan como estimación provisional;
- la medición de avance y costo real proviene de la ejecución registrada y validada.
