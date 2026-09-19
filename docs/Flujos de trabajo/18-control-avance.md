
# 18 — Control de avance — versión mejorada

## Objetivo

Integrar en una sola cadena de control:

```text
Presupuesto / DP
→ Partidas y WBS
→ Paquetes opcionales
→ Cronograma
→ Plan Maestro aprobado
→ 3WLA / Plan semanal
→ RDT validado
→ PR
→ Dashboard
```

El sistema debe distinguir siempre entre:

- Lo que se aprobó planificar.
- Lo que se prepara y compromete semanalmente.
- Lo que se ejecutó realmente.
- Lo que se consolida.
- Lo que se visualiza.

## Tres universos del control

### Plan Maestro

Es la línea base físico-económica completa del servicio. Define, para cada partida y cada periodo, qué metrado y qué costo se esperaba ejecutar.

Responde:

```text
¿Qué debía hacerse según presupuesto, cronograma y línea base?
```

Contiene:

- Partida.
- Unidad.
- Metrado contractual.
- Precio unitario.
- BAC.
- Actividad de cronograma.
- Fecha de inicio y fin.
- Metrado programado por día o semana.
- Costo programado por día o semana.
- PV semanal y acumulado.
- HH programadas.

El Plan Maestro aprobado no se sobrescribe por la ejecución real. Cualquier cambio aprobado debe generar una nueva revisión.

### 3WLA / Plan semanal

Es la planificación operativa móvil de corto plazo. Se construye a partir del Plan Maestro, pero incorpora restricciones, condiciones de preparación y compromisos reales.

Responde:

```text
¿Qué trabajo está listo y qué se intentará o comprometerá ejecutar?
```

El 3WLA y el Plan semanal no modifican automáticamente el PV de la línea base.

Deben registrar:

- Partida o paquete.
- Actividad.
- Semana.
- Responsable.
- Cantidad comprometida.
- Restricciones.
- Condiciones de satisfacción.
- Estado de preparación.
- Cumplido o no cumplido.
- Causa de incumplimiento.
- Acción siguiente.

### Ejecución real

La ejecución real proviene de RDT validados. Cada registro debe alimentar la fecha, partida, paquete opcional, cantidad, HH, costo y evidencia correspondiente.

Responde:

```text
¿Qué se ejecutó realmente?
```

El RDT no modifica la programación base. Es una capa real que se superpone al Plan Maestro.

## Ejemplo de desviación

Plan Maestro:

```text
30/08 — Montaje de estructura: 5 t.
```

RDT validado:

```text
30/08 — Montaje de estructura: 0 t.
30/08 — Vaciado de concreto: 4 m³.
```

El sistema debe conservar ambos datos:

```text
Montaje de estructura:
Plan: 5 t.
Real: 0 t.

Vaciado de concreto:
Plan: 0 m³.
Real: 4 m³.
```

No se suman toneladas y metros cúbicos. La variación física se muestra por partida y la variación global se calcula mediante valor económico.

## Estructura longitudinal del Plan Maestro

La interfaz se lee de izquierda a derecha:

```text
Columnas fijas
→ Semana 1
→ Semana 2
→ Semana 3
→ ...
```

Las columnas fijas deben incluir:

- WBS.
- Área.
- Disciplina.
- Frente.
- Paquete.
- Código de partida.
- Descripción.
- Unidad.
- Metrado contractual.
- Precio unitario.
- BAC.
- HH contractuales.
- Duración.
- Inicio base.
- Fin base.
- Método de medición.

Cada semana agrupa:

- Sábado a viernes, según configuración del servicio.
- Metrado programado diario.
- Metrado real diario validado.
- Cierre semanal.

El cierre semanal muestra:

- Metrado programado.
- Metrado real.
- Variación.
- Avance económico programado.
- Avance físico programado.
- HH programadas.
- Avance económico real.
- Avance físico real.
- HH reales.
- Incidencias.
- Causa y acción siguiente.

Las semanas deben agregarse horizontalmente según la duración del servicio. No se debe limitar la interfaz a un número fijo de semanas.

## Cálculos

### Metrado acumulado

```text
Metrado acumulado = suma del metrado real validado hasta la fecha de corte
```

### Metrado restante

```text
Metrado restante = metrado contractual - metrado acumulado
```

Si el resultado es negativo, debe generarse una alerta de sobre-ejecución.

### Avance físico por partida

```text
Avance físico = metrado real acumulado / metrado contractual × 100
```

Para hitos o paquetes ponderados se aplica el método de medición configurado.

### Valor planificado

```text
PV de partida y periodo = cantidad programada × precio unitario
```

```text
PV semanal = suma del PV de las partidas programadas en la semana
PV acumulado = suma del PV semanal desde el inicio
BAC = suma del presupuesto de las partidas
PV final = BAC
```

### Valor ganado

```text
EV = avance físico real validado × BAC de la partida
```

El EV no se obtiene simplemente del dinero gastado.

### Costo real

El AC proviene de costos validados de:

- Mano de obra.
- Equipos.
- Subcontratos.
- Materiales con control real.

Los materiales no medidos deben permanecer como estimación provisional y no confundirse con AC real.

### HH restantes

```text
HH restantes = HH contractuales - HH reales acumuladas
```

Si se usa una proyección, debe mostrarse como `HH estimadas para terminar`.

### Rendimiento

```text
Rendimiento real = metrado ejecutado / HH reales
Rendimiento base = metrado contractual / HH contractuales
```

### HH ganadas

```text
HH ganadas = avance físico real × HH contractuales
```

### IP

Definir el significado de IP en la configuración del sistema. Recomendación inicial:

```text
IP = HH ganadas / HH reales
```

Debe mostrarse nombre, fórmula y unidad, no solo la abreviatura IP.

### Indicadores EVM

```text
SV = EV - PV
CV = EV - AC
SPI = EV / PV
CPI = EV / AC
```

### Indicador LPS

```text
PPC = compromisos completados / compromisos planificados × 100
```

PPC y SPI miden cosas diferentes y no deben mezclarse.

## Flujo de datos RDT → Plan Maestro

1. El usuario registra un RDT asociado a una OT vigente.
2. El RDT identifica servicio, fecha, partida y paquete opcional.
3. El usuario registra cantidad, unidad, HH, HM, costo y evidencia.
4. El sistema valida que la partida pertenezca al servicio.
5. El sistema valida unidad y cantidad.
6. El registro queda en estado `Registrado`.
7. Un usuario autorizado lo revisa.
8. El registro pasa a `Validado` o `Rechazado`.
9. Solo un RDT validado alimenta las casillas `Real` del Plan Maestro.
10. El sistema recalcula acumulados, avance físico, EV, HH reales, rendimiento, HH ganadas e IP.
11. El PR recibe los datos consolidados.
12. El Dashboard actualiza sus indicadores.

Estados:

```text
Registrado → Revisado → Validado
                         └→ Rechazado
```

Un RDT corregido debe mantener historial de la corrección.

## Historial y reprogramación

El sistema no debe mover automáticamente una actividad no ejecutada a otra semana.

Debe conservar:

```text
Plan base:
Semana 1 — 5 t de estructura.

Real:
Semana 1 — 0 t.

Reprogramación aprobada:
Semana 2 — 5 t.

Causa:
Falta de pernos.
```

El Plan Maestro original se conserva como línea base. Una reprogramación aprobada genera una nueva revisión:

```text
PM-Rev-01 — línea base original.
PM-Rev-02 — reprogramación aprobada.
```

El PR debe poder comparar contra la línea base original y contra la revisión vigente.

## Relación con PR y Dashboard

El PR es el consolidado técnico. Debe poder consultar:

```text
Servicio
→ Área
→ Disciplina
→ Frente
→ Paquete
→ Partida
→ Actividad
→ Día / semana
```

El Dashboard es una vista derivada y debe mostrar:

- Curva S PV, EV y AC.
- Avance físico.
- SPI y CPI.
- PPC.
- Paquetes atrasados.
- Partidas sin asignar.
- Partidas sin actividad.
- Incidencias abiertas.
- Tendencia.

## Reglas de diseño

1. No sobrescribir el Plan Maestro aprobado con RDT.
2. No convertir un RDT registrado en real oficial sin validación.
3. No usar 3WLA para modificar el PV automáticamente.
4. No mezclar unidades físicas incompatibles.
5. No mezclar avance semanal con acumulado.
6. No usar PR como fuente original del alcance.
7. No convertir un paquete en una partida contractual.
8. No tratar materiales estimados como AC real.
9. Mantener historial de revisiones y correcciones.
10. Permitir rastrear cada EV, AC y avance hasta partida y RDT.

## Resultado esperado

El sistema debe permitir ver, por cada partida:

```text
Qué estaba programado cada día.
Qué se ejecutó realmente cada día.
Qué se esperaba al cierre de la semana.
Qué ocurrió al cierre de la semana.
Qué metrado falta.
Cuántas HH se planificaron y utilizaron.
Cuál fue el rendimiento.
Qué incidencias ocurrieron.
Qué se debe preparar o comprometer después.
```
