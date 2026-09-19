# 20 — Plan Maestro

## Objetivo

Convertir el presupuesto contractual (DP) y el cronograma vinculado en una linea base temporal del servicio, para comparar lo programado contra la ejecucion real validada.

El Plan Maestro responde:

```text
¿Cuánto metrado y valor debía ejecutarse en cada periodo?
```

No reemplaza el cronograma, el RDT, el PR ni el Dashboard.

## Fuentes de verdad

| Dato | Fuente |
|---|---|
| Alcance, metrado contractual, unidad y precio unitario | DP / presupuesto aprobado |
| Fechas y duracion de actividades | Cronograma |
| Relacion actividad - partida | Vinculos Cronograma - DP |
| Metrado programado y PV | Plan Maestro aprobado |
| Ejecucion real | RDT estructurado validado |
| Consolidado tecnico | PR |
| Indicadores ejecutivos | Dashboard |

Reglas:

- El RDT validado alimenta `Real`; nunca sobrescribe `Programado` ni el PV aprobado.
- El RDT debe usar un WBS existente en el DP del mismo servicio. Al validarlo, el sistema registra el vinculo actividad RDT - partida DP.
- No se suman unidades fisicas incompatibles entre partidas.
- El 3WLA es una capa operativa separada y no modifica automaticamente la linea base.
- Una nueva propuesta aprobada reemplaza la version vigente como linea base, pero conserva la version anterior.

## Flujo implementado (Fase 1)

```text
DP importado
  -> Cronograma con tareas fechadas
  -> Vinculos tarea de cronograma - partida DP
  -> Generar propuesta de Plan Maestro
  -> Ajustar distribucion diaria (borrador)
  -> Aprobar linea base
  -> Registrar RDT estructurado con WBS DP
  -> Validar RDT (administrador o jefe de proyectos)
  -> Visualizar Programado, Real validado y PV por semana
```

### 1. Generar propuesta

El usuario con permiso selecciona una OT vigente y genera una propuesta. El sistema exige:

- DP importado.
- Una o mas actividades tipo `TAREA` con fecha de inicio y fin por cada partida DP.
- Vinculos guardados entre esas actividades y sus partidas DP.

El sistema crea un borrador versionado y reparte el metrado contractual de cada partida en los dias cubiertos por sus actividades vinculadas. El ultimo dia absorbe el redondeo para que la suma coincida exactamente con el metrado contractual.

### 2. Ajustar y aprobar

Mientras el plan esta en `BORRADOR`, administrador, jefe de proyectos y planner pueden modificar la distribucion diaria y guardar los ajustes.

Antes de aprobar:

- Ningun metrado planificado puede ser negativo.
- No puede haber fecha duplicada para la misma partida.
- La suma diaria de cada partida debe ser exactamente igual a su metrado contractual.

Al aprobar, el estado pasa a `APROBADO`. Si se aprueba una nueva version para el mismo servicio, la aprobada anterior pasa a `REEMPLAZADO`.

### 3. RDT a ejecucion real

El RDT estructurado conserva el WBS de la partida DP. Quien puede validar es solamente:

- Administrador.
- Jefe de proyectos.

Durante la validacion, el sistema verifica que toda actividad directa del RDT tenga un WBS existente en el DP de la misma OT. Si es valido, registra el vinculo actividad RDT - partida DP y cambia el RDT a `VALIDADO`.

Estados de RDT:

```text
REGISTRADO -> REVISADO -> VALIDADO
                       -> RECHAZADO
```

Solo `VALIDADO` es ejecucion real oficial. Un RDT validado no puede reemplazarse mediante una nueva carga para la misma fecha y turno.

### 4. Vista semanal

La pantalla ofrece:

- Resumen por partida: WBS, descripcion, unidad, metrado contractual, metrado planificado y PV.
- Distribucion semanal longitudinal: columnas fijas de WBS, partida, unidad y metrado contractual; semanas dinamicas de sabado a viernes, calculadas desde el rango de fechas real del Plan Maestro.
- Por partida y semana: `Prog.` (metrado de la linea base), `Real` (RDT validado) y `PV` (programado por precio unitario).

Si el servicio dura seis semanas, se generan seis grupos semanales; no existe un numero fijo de semanas en la interfaz.

## Permisos

| Accion | Roles |
|---|---|
| Ver Plan Maestro | Todos excepto asistente |
| Generar, ajustar y aprobar Plan Maestro | Administrador, jefe de proyectos, planner |
| Crear RDT estructurado | Supervisor operativo, administrador, jefe de proyectos |
| Validar o rechazar RDT | Administrador, jefe de proyectos |

## Pendiente (Fase 2)

- Vista detallada diaria por semana: `Prog.` y `Real` por dia, con HH y observacion cuando existan.
- Acumulados por partida: metrado real, metrado restante, avance fisico, PV y EV.
- HH reales, rendimiento, HH ganadas e IP, cuando el modelo de datos permita atribuirlas de forma trazable a la partida.
- AC, CV, CPI, SPI y Curva S, sin usar valorizacion planificada como costo real.
- Cierre semanal auditado: incidencias, causa de variacion, accion siguiente y estados abierta/en revision/cerrada/reabierta.
- Interfaz de revision y rechazo de RDT con motivo visible e historial de correccion.
- Paquetes de trabajo, area, disciplina y frente como filtros operativos, sin reemplazar partidas DP.
- 3WLA como plan operativo separado.
- Integracion de indicadores consolidados hacia PR y Dashboard.
- Verificacion de pertenencia de usuario por servicio/proyecto, ademas de rol.
- Vista movil semanal compacta.

## Referencias

- [06-rdt.md](06-rdt.md)
- [09-importar-dp.md](09-importar-dp.md)
- [10-generacion-pr.md](10-generacion-pr.md)
- [11-dashboard.md](11-dashboard.md)
- [15-cronograma.md](15-cronograma.md)
- [18-control-avance.md](18-control-avance.md)
- [19-paquetes de trabajo y jerarquia de control.md](19-paquetes%20de%20trabajo%20y%20jerarquia%20de%20control.md)
