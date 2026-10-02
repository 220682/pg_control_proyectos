# 20 — Plan Maestro
> Lee si: la tarea toca el Plan Maestro: sus fuentes de verdad, el flujo implementado, sus permisos o qué queda pendiente de fase 2.


## Objetivo

Convertir el presupuesto contractual (DP), el cronograma y los vínculos declarados en Paquetes en una linea base temporal del servicio, para comparar lo programado contra la ejecucion real validada.

El Plan Maestro responde:

```text
¿Cuánto metrado y valor debía ejecutarse en cada periodo?
```

No reemplaza el cronograma, el RDT, el PR ni el Dashboard.

## Fuentes de verdad

| Dato | Fuente |
|---|---|
| Alcance, metrado contractual, unidad y precio unitario | DP / presupuesto aprobado |
| Fechas y duracion de actividades | Cronograma (solo como guía sombreada en el lienzo) |
| Relacion actividad - partida y metrado por vínculo | Vínculos declarados en Paquetes (flujo 19) |
| Distribucion diaria del metrado | El lienzo del Plan Maestro (`plan_maestro_asignaciones`, editada por línea: actividad × partida) |
| Metrado programado y PV | Plan Maestro aprobado |
| Ejecucion real | RDT estructurado validado |
| Consolidado tecnico | PR |
| Indicadores ejecutivos | Dashboard |

Reglas:

- **El Plan Maestro define el PV del servicio desde el inicio y es restrictivo: sin uno en estado `APROBADO`, el servicio no puede pasar de `EN_PLANEACION` a `EJECUCION`.** Validado en servidor (`POST /api/proyectos/[id]/confirmar-transicion`), no solo en la interfaz — una transición intentada por URL directa queda igual de bloqueada. Los servicios que ya estaban en `EJECUCION` antes de esta regla no se tocan; el bloqueo aplica solo a la transición (ver [PR Fase 2](../02-trabajo-activo/01-planes/2026-09-21-pr-fase-2-pipeline-linea-base.md), tarea B4).
- El RDT validado alimenta `Real`; nunca sobrescribe `Programado` ni el PV aprobado.
- **El RDT usa los paquetes y partidas del Plan Maestro aprobado** (o una partida directa); sin Plan Maestro aprobado no se puede crear RDT. Al validarlo, el sistema registra el vinculo actividad RDT - partida DP (con su paquete).
- No se suman unidades fisicas incompatibles entre partidas.
- El 3WLA es una capa operativa separada y no modifica automaticamente la linea base.
- Una nueva version aprobada reemplaza la version vigente como linea base, pero conserva la version anterior.
- **Una partida se puede repetir en el Plan Maestro** (repartida en varios paquetes y/o como directa): se relajó la restricción de WBS único (migración `076`, autorizada por Victor). El PV, el planificado del PR y la Curva S **suman todas las líneas de la partida**.
- **El detalle diario de `plan_maestro_asignaciones` (fecha + metrado planificado) alcanza para alimentar series temporales por agregación en el momento de lectura — no hace falta una tabla de snapshots ni un historial semanal materializado.** El spec original del Dashboard (`docs/superpowers/specs/2026-08-16-dashboard-parcial-design.md` §2, repo `py_control_proyectos_web`) daba por necesario ese snapshot para la Curva S; quedó obsoleto al construirla en Fase 3 (2026-09-22) — ver [21-curva-s.md](21-curva-s.md).

## Flujo implementado

```text
DP importado (niveles confirmados)
  -> Cronograma cargado (niveles confirmados; solo carga y vista)
  -> Paquetes: declarar vínculos actividad × partida con metrado, y agrupar (paquete opcional)
  -> Crear borrador del Plan Maestro (líneas desde los vínculos con metrado)
  -> Lienzo: repartir el metrado por día (guardado parcial en BORRADOR)
  -> Crear Plan Maestro (aprueba la linea base al repartir el 100 %)
  -> Registrar RDT estructurado con paquete × partida del Plan Maestro
  -> Validar RDT (administrador, jefe de proyectos o jefe de oficina técnica)
  -> Visualizar Programado, Real validado y PV por semana
```

### 1. Crear el borrador

El usuario con permiso selecciona una OT vigente y pulsa «Crear borrador del Plan Maestro» (único botón de inicio; ya no hay «Generar propuesta» que copie una distribución). El sistema exige:

- DP importado.
- Al menos un vínculo actividad × partida con metrado, declarado en Paquetes (flujo 19).

**Un paquete no es obligatorio**: las partidas sin paquete entran como **partidas directas**. Se retira la regla anterior «sin paquete no hay Plan Maestro».

El borrador nace sin repartir: una línea por vínculo con metrado (actividad × partida), dentro de su paquete o como directa; **no lee fechas de paquetes ni copia distribución** (los paquetes no tienen fechas). Las fechas de la actividad solo se sombrean como guía en el lienzo y **no limitan el reparto** (se puede escribir fuera de ellas). Si ya hay un Plan Maestro aprobado, ver «Versión nueva».

### 2. El lienzo

El lienzo se llena en `BORRADOR` y se **guarda parcial**: se puede dejar a medias y retomar. Se lee de izquierda a derecha:

- **Columnas fijas:** WBS, descripción, Und., Met. (metrado de la línea), costo unitario y HH por unidad, más «Falta repartir» y una línea divisoria. En móvil solo WBS y descripción quedan fijas.
- **Columnas opcionales** con el botón «Personalizar campos» (el mismo componente y `campos-visibles` que usan otras pantallas; no hay otro selector): hoy **Costo total ($)** (BAC de la línea), **HH totales** y **Disciplina** (apagadas por defecto). Tiempo no va.
- **Semanas** de sábado a viernes, dinámicas según el rango real; cada semana trae sus columnas diarias de metrado y **seis columnas de cierre** (físico, económico y HH, cada uno semanal y acumulado, rotulados «nombre (unidad)» para no mezclarlos; «Acumuladas: sí/no» deja solo las tres semanales). Las semanas se pliegan (plegada = solo sus totales); «+ 7 días antes/después» amplía el rango.
- **Estructura:** filas de nivel (con subtotal y plegado propio), grupos por paquete y partidas directas, con subtotales; una partida repetida aparece en cada paquete con su porción.
- **Subfilas:** «Prog.» (lo programado, editable en BORRADOR) y «Real» (RDT validado, solo lectura, con interruptor «Real: sí/no»). Lo real nunca sobrescribe lo programado.
- **Editar por bloques:** partida, semana o rango de días y total → reparto uniforme (el último día absorbe el redondeo); reemplaza solo esos días de esa partida.
- **Total del servicio:** filas «Prog.» y «Real» (físico 22,56 / 48,78 / 76,22 / 100 % en el anexo de prueba, sumando económico y HH por separado; no se suman unidades físicas).
- **Color del avance real:** solo en «Físico acum. (%)» de las filas «Real»: 0 % sin color (blanco), en curso amarillo, 100 % verde con ✓; nunca en lo programado (flujo 18).
- **Falta repartir:** por línea (completa, falta, excede), por grupo («n partidas por ajustar») y global.
- **Real de versión anterior:** si hay real validado de una clave que ya no tiene línea en esta versión, se muestra al final con insignia amarilla; sus metrado y HH se ven, su físico y económico salen «—» y **no suman** al total.
- Con servicios grandes la lista de filas se virtualiza (ventana vertical, desde 60 filas); columnas fijas y encabezados no se tocan. Los paneles laterales se pueden ocultar para dar ancho (flujo 16).

El **real se identifica por clave** `paquete|DIRECTA : partida` y no por el id de la línea, así sobrevive a las versiones nuevas del Plan Maestro.

### 3. Crear (aprobar) el Plan Maestro

«Crear Plan Maestro» queda inhabilitado hasta que el reparto cumple (la pantalla dice qué falta):

- Ningun metrado planificado puede ser negativo.
- No puede haber fecha duplicada para la misma línea.
- La suma diaria de cada **línea** debe ser exactamente igual a su metrado de línea.
- La suma de las líneas de cada **partida** debe ser exactamente igual a su metrado contractual (el 100 %; las partidas del DP sin línea se señalan).
- **Toda partida directa debe tener su disciplina** (ver más abajo).

Al crear, el sistema guarda y aprueba; el estado pasa a `APROBADO` (solo lectura para todo rol). Si ya había una aprobada, esta pasa a `REEMPLAZADO` y en el mismo paso se recalcula `pr_partidas.metrado_planificado_acum` (bloque A' del PR) desde las asignaciones del plan recién aprobado — **sumado por partida** aunque esté repartida en varios paquetes, sin rastro del plan reemplazado.

### 4. Versión nueva

Con un Plan Maestro `APROBADO`, el botón «Crear versión nueva» pide un **motivo obligatorio** (máximo 500 caracteres) y crea un borrador que **parte de las asignaciones y de las disciplinas de la aprobada** (misma actividad y WBS). **Solo administrador y jefe de proyectos** pueden crear una versión nueva (fila propia en la tabla 2 del [flujo 14](14-accesos-y-restricciones.md)). **Aprobar** ese borrador, que reemplaza a la versión aprobada, lo pueden hacer los tres roles que gestionan el Plan Maestro (administrador, jefe de proyectos y planner), igual que la primera aprobación. El motivo se muestra en la versión aprobada. La versión nueva es la vía para cambiar el DP o el cronograma, cuya recarga está bloqueada mientras haya una aprobada.

### 5. Disciplina

- Catálogo fijo de 5 (Civil, Mecánica, Eléctrica, Instrumentación, Tuberías).
- **La partida directa lleva su propia disciplina**, obligatoria: se elige en el lienzo («Disciplina *») y es requisito para crear el Plan Maestro; el servidor la exige al aprobar y rechaza una inexistente o inactiva.
- **La partida dentro de un paquete hereda la del paquete** (se muestra «Hereda: X», no se edita aquí; se define en Paquetes, flujo 19).
- Las líneas anteriores a este plan quedan **sin disciplina** («Sin disciplina»); una línea de paquete cuyo paquete es anterior no bloquea la aprobación.

### 6. Recarga bloqueada

Con un Plan Maestro `APROBADO` **no se puede recargar el DP ni el cronograma** (flujos 09 y 15). Sin plan aprobado, la recarga avisa lo que se perdería (vínculos, paquetes, borrador) y pide confirmación.

### 7. RDT a ejecucion real

El RDT estructurado elige paquetes y partidas del Plan Maestro aprobado (o una partida directa) y conserva el WBS de la partida DP (flujo 06). Quien puede validar o rechazar es solamente:

- Administrador.
- Jefe de proyectos.
- Jefe de oficina técnica.

Rechazar un RDT que ya está `VALIDADO` (para destrabarlo) es más restrictivo: solo administrador y jefe de proyectos.

Durante la validacion, el sistema exige Plan Maestro aprobado y que cada actividad (D, C y NC) tenga una clave existente en él. Si es valido, registra el vinculo actividad RDT - partida DP (con el paquete) y cambia el RDT a `VALIDADO`. Un RDT anterior sin paquete se valida solo si su partida está como directa en el plan aprobado.

Estados de RDT:

```text
REGISTRADO -> REVISADO -> VALIDADO
                       -> RECHAZADO
```

Solo `VALIDADO` es ejecucion real oficial. Un RDT validado no puede reemplazarse mediante una nueva carga para la misma fecha y turno.

**Real en el lienzo:** el real por paquete × partida vive **solo en el Plan Maestro**; el real por partida (suma de todos sus paquetes) alimenta al PR. Cuenta solo el metrado de actividades D y las horas del tareo no MOI de partes `VALIDADO`.

### 8. Vista semanal

Por partida y semana: `Prog.` (metrado de la linea base), `Real` (RDT validado) y el PV (programado por precio unitario). Si el servicio dura seis semanas, se generan seis grupos semanales; no existe un numero fijo de semanas en la interfaz. Estados de pantalla: sin servicio, cargando, error con «Reintentar», sin plan, sin partidas y listo.

## Permisos

Fuente única: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md). Resumen:

| Accion | Roles |
|---|---|
| Ver Plan Maestro (lleva datos económicos) | Administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos, jefe de costos y planner |
| Crear borrador, repartir en el lienzo y crear (aprobar) el Plan Maestro | Administrador, jefe de proyectos, planner |
| **Crear una versión nueva** (el borrador, cuando ya hay una aprobada) | **Administrador, jefe de proyectos** |
| Aprobar el borrador de una versión nueva (reemplaza a la aprobada) | Administrador, jefe de proyectos, planner |
| Crear RDT estructurado | Supervisor operativo, administrador, jefe de proyectos, jefe de oficina técnica |
| Validar o rechazar RDT | Administrador, jefe de proyectos, jefe de oficina técnica |
| Rechazar un RDT ya validado | Administrador, jefe de proyectos |

## Pendiente (Fase 2)

Ver `docs/02-trabajo-activo/01-planes/2026-09-20-control-avance-plan-maestro.md` — los pendientes se trackean ahí, no en este archivo.

## Referencias

- [06-rdt.md](06-rdt.md)
- [09-importar-dp.md](09-importar-dp.md)
- [10-generacion-pr.md](10-generacion-pr.md)
- [11-dashboard.md](11-dashboard.md)
- [15-cronograma.md](15-cronograma.md)
- [18-control-avance.md](18-control-avance.md)
- [21-curva-s.md](21-curva-s.md)
- [19-paquetes-de-trabajo-y-jerarquia-de-control.md](19-paquetes-de-trabajo-y-jerarquia-de-control.md)
