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
- **El RDT usa los paquetes y partidas del Plan Maestro aprobado** (o una partida directa); sin Plan Maestro aprobado **y** servicio en Ejecución no se puede crear RDT ([flujo 06](06-rdt.md), U1). Al validarlo, el sistema registra el vinculo actividad RDT - partida DP (con su paquete).
- No se suman unidades fisicas incompatibles entre partidas.
- El 3WLA es una capa operativa separada y no modifica automaticamente la linea base.
- Una nueva version aprobada reemplaza la version vigente como linea base, pero conserva la version anterior.
- **El Plan Maestro es el umbral del servicio (U3, Enmienda E1 2026-10-03).** Aprobado el Plan Maestro, **lo único editable es el propio Plan Maestro** (versión nueva con motivo obligatorio); quedan **congelados** el DP, el PR, los cronogramas y los paquetes. Lo **administrativo** (checklist, notificaciones y datos del servicio) sigue funcionando normal. Antes de aprobarlo, todos esos datos de planeación son editables.
- **El Plan Maestro no puede dejar de contemplar ninguna partida (U5).** Al modificarlo solo se **mueven partidas** y se **crean o desagrupan paquetes**; nunca se elimina una partida del plan. Por eso no puede quedar un RDT sin partida.
- **Las partidas transversales (Victor, 2026-10-19) no llevan línea en el Plan Maestro** ni entran en la regla del 100 %: se marcan en Paquetes ([flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)), cada versión aprobada **guarda cuáles eran las suyas** (`plan_maestro_transversales`) y es la foto de la versión **aprobada** la que rige los cálculos. Es la única excepción a U5: siguen contempladas porque se calculan, no porque se programen. Su PV es su costo directo × PV % del resto del servicio, y su avance, EV, HH y costo real salen del % físico del resto ([flujo 10](10-generacion-pr.md)). **El lienzo las muestra** (Victor, 2026-10-19) como filas «Transversal» de **solo lectura** (costo, programado y real), calculadas con esas mismas reglas: programado de cada día = su metrado × (PV del resto ese día ÷ BAC del resto); real = su metrado × (EV real del resto ÷ BAC del resto), con las HH del APU **mostradas en su fila pero informativas**: el total real del servicio **no las suma** (Victor, 2026-10-21; `db/116`, [flujo 10](10-generacion-pr.md)). No son líneas: no se guardan ni entran a la regla del 100 %, pero **sí suman al «Total del servicio»** (Victor, 2026-10-19): el consolidado vuelve a la estructura inicial del presupuesto y, con todas las partidas, el avance llega al 100 % en metrado y costo, y en las HH programadas; las HH **reales** del servicio no cuentan las de la transversal. **Pendiente de decisión (no es regla):** si las HH contractuales y las HH programadas del Plan Maestro también deben excluir la transversal. Su valor lo calcula el sistema; no se programan día por día.
- **Una partida se puede repetir en el Plan Maestro** (repartida en varios paquetes y/o como directa): se relajó la restricción de WBS único (migración `076`, autorizada por Victor). El PV, el planificado del PR y la Curva S **suman todas las líneas de la partida**.
- **El detalle diario de `plan_maestro_asignaciones` (fecha + metrado planificado) alcanza para alimentar series temporales por agregación en el momento de lectura — no hace falta una tabla de snapshots ni un historial semanal materializado.** El spec original del Dashboard (`docs/superpowers/specs/2026-08-16-dashboard-parcial-design.md` §2, repo `py_control_proyectos_web`) daba por necesario ese snapshot para la Curva S; quedó obsoleto al construirla en Fase 3 (2026-09-22) — ver [21-curva-s.md](21-curva-s.md).
- **Declaración de metrados por paquete (no por partida)**: el usuario declara el metrado total del paquete (celda editable en verde); las partidas dentro del paquete reciben su proporción automáticamente según la partida guía (migración `091`); la unidad del paquete es la de la guía. Las partidas muestran su metrado contractual fijo (no editable).
- **Fechas editables por paquete**: las columnas `fecha_inicio` y `fecha_fin` son opcionales y editables en las filas de paquete; se pintan en rojo si están fuera del rango visible del lienzo (migración `091`).
- **Plegables individuales por grupo de medida**: Físico, Económico y HH se pliegan independientemente (cada uno oculta sus 2 columnas: semanal y acumulado).
- **Selector OT compacto**: el selector de servicio tiene `max-width: 200px` y el select interno `max-width: 110px`.
- **Icono de asistente flotante**: el icono IA flota con `position: fixed` sobre el contenido sin reservar espacio en el layout (sin `padding-right`).

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

El usuario con permiso selecciona una OT vigente y pulsa «Crear borrador del Plan Maestro» (único botón de inicio; **no se ofrece mientras la pantalla carga el servicio**, Victor 2026-10-21; ya no hay «Generar propuesta» que copie una distribución). El sistema exige:

- DP importado.
- Al menos un vínculo actividad × partida con metrado, declarado en Paquetes (flujo 19).

**Un paquete no es obligatorio**: las partidas sin paquete entran como **partidas directas**. Se retira la regla anterior «sin paquete no hay Plan Maestro».

El borrador nace sin repartir: una línea por vínculo con metrado (actividad × partida), dentro de su paquete o como directa; **no lee fechas de paquetes ni copia distribución** (los paquetes no tienen fechas). Las fechas de la actividad solo se sombrean como guía en el lienzo y **no limitan el reparto** (se puede escribir fuera de ellas). Si ya hay un Plan Maestro aprobado, ver «Versión nueva».

### 2. El lienzo

El lienzo se llena en `BORRADOR` y se **guarda parcial**: se puede dejar a medias y retomar. Se lee de izquierda a derecha:

- **Selector OT compacto:** 200px máximo, no ocupa todo el ancho del panel central. Etiqueta "N° OT" + select con el número.
- **Columnas fijas por defecto (Victor, 2026-10-15):** WBS, descripción, Und., **Met.** (metrado contractual de la línea), **Met. acum.** (metrado acumulado: el real validado hasta hoy), **Met. rest.** (metrado restante = contractual − acumulado) y costo unitario, con una línea divisoria gruesa tras la última columna fija visible. **El orden de los tres metrados es siempre contractual, acumulado, restante**, en toda interfaz. **HH por unidad** y **Falta repartir** ya no se ven por defecto (quedan en «Personalizar campos»). En móvil solo WBS y descripción quedan fijas.
- **Columnas opcionales** con el botón «Personalizar campos» (el mismo componente y `campos-visibles` que usan otras pantallas; no hay otro selector; el desplegable se abre hacia donde haya espacio y no se corta con la barra lateral): **HH/unid.** y **Falta repartir** (apagadas por defecto desde 2026-10-15), **Costo total ($)** (BAC de la línea), **HH totales**, **Disciplina** (apagadas por defecto), **Fecha inicio** y **Fecha fin** (nuevas, apagadas por defecto; son las fechas del cronograma por defecto, editables, se ponen en rojo si están fuera del rango visible del lienzo). Tiempo no va.
- **Declaración de metrados por paquete:** el metrado se declara en la fila de la **partida guía** del paquete (resaltada con color; la guía es obligatoria en todo paquete, [flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)), no en las demás partidas. Las partidas del paquete muestran el metrado calculado (distribuido proporcionalmente al contractual) en solo lectura. Las partidas directas (sin paquete) mantienen input editable.
- **Plegables individuales de columnas de medida:** botones separados para **Físico**, **Económico** y **HH** que ocultan/muestran las columnas de ese grupo (semanal + acumulado). Similar al plegado de semanas.
- **Semanas** de sábado a viernes, dinámicas según el rango real; cada semana trae sus columnas diarias de metrado y **seis columnas de cierre** (físico, económico y HH, cada uno semanal y acumulado, rotulados «nombre (unidad)» para no mezclarlos; «Acumuladas: sí/no» deja solo las tres semanales). Las semanas se pliegan (plegada = solo sus totales); «+ 7 días antes/después» amplía el rango.
- **Solo se ve el avance de partidas (Victor, 2026-10-15).** Las filas de **nivel** y de **paquete** **no muestran datos de avance** (físico, económico, HH; programado ni real): se eliminan, no se pintan de otro color, y tampoco hay fila «Real» bajo el paquete ni bajo el nivel. Se **queda el «Total del servicio»**. La **fila del paquete** muestra solo, como **informativo**, lo de su partida guía: **Und., Met., Met. acum., Met. rest.** y el **avance real (%)** junto al nombre (0 % normal, en curso amarillo, 100 % verde con ✓). La fila de **nivel** no muestra ninguno. Una partida de paquete refleja el % del paquete. **La partida guía conserva su propia fila** (en ella se declara el metrado del paquete). Esto reemplaza la lectura anterior en que las filas de grupo traían subtotales de avance.
- **Estructura — jerarquía completa del presupuesto (Victor, 2026-10-14; reemplaza «grupos por paquete y partidas directas»):** se ven todos los niveles del presupuesto tal cual (1 → 1.1 → …), cada uno con su subtotal y plegado propio. **Cada paquete es una fila dentro del nivel donde están sus partidas**, con su subtotal, su declaración de metrado (fila resaltada) y sus fechas; **si un paquete tiene partidas en dos niveles, aparece en cada uno con su parte**. Las **partidas directas van sueltas dentro de su nivel**. Una partida repetida aparece en cada paquete con su porción. Dentro de un nivel el orden es el del presupuesto (WBS). La regla rige en todas las interfaces (flujo 09).
- **Programación diaria de un paquete (Victor, 2026-10-19):** los cuadros de días se editan **solo en la fila del paquete** y programan el **metrado de su partida guía, en la unidad de la guía** (p. ej. ml de perfilado). Las partidas del paquete —la guía incluida— muestran sus días en **solo lectura**: cada una recibe el metrado de la guía de ese día por su proporción (metrado de la línea ÷ metrado de la guía, el mismo % que usa el RDT). **Cómo se guarda:** las asignaciones siguen siendo **por línea** (`plan_maestro_asignaciones`, una por línea y día, calculadas sin redondear): el PV, el PR y la Curva S siguen sumando por partida y cada partida cuadra con su metrado (regla del 100 %). Las partidas directas conservan sus cuadros editables. Un Plan Maestro armado antes de esta regla con días por partida que no siguen la proporción de la guía se marca como «sin cerrar» hasta que se vuelvan a escribir los días del paquete. Si un paquete tiene porciones en dos niveles, los cuadros están en la porción donde está la guía.
- **Subfilas:** «Prog.» (lo programado, editable en BORRADOR; en un paquete, solo en la fila del paquete) y «Real» (RDT validado, solo lectura, con interruptor «Real: sí/no»). Lo real nunca sobrescribe lo programado.
- **Editar por bloques:** partida directa **o paquete**, semana o rango de días y total → reparto uniforme (el último día absorbe el redondeo); reemplaza solo esos días. En un paquete el total es el de su partida guía (en su unidad) y se deriva a todas sus partidas.
- **Total del servicio:** filas «Prog.» y «Real» (físico 22,56 / 48,78 / 76,22 / 100 % en el anexo de prueba, sumando económico y HH por separado; no se suman unidades físicas).
- **Color del avance real:** solo en «Físico acum. (%)» de las filas «Real»: 0 % sin color (blanco), en curso amarillo, 100 % verde con ✓; nunca en lo programado (flujo 18).
- **Falta repartir:** por línea (completa, falta, excede), por grupo («n partidas por ajustar») y global. En el global, un **paquete con guía cuenta como uno** («partidas o paquetes sin cerrar») y dice cuánto falta o excede de la guía; las directas se cuentan una a una.
- **Real de versión anterior:** si hay real validado de una clave que ya no tiene línea en esta versión, se muestra al final con insignia amarilla; sus metrado y HH se ven, su físico y económico salen «—» y **no suman** al total.
- **Icono del agente con reserva de espacio:** el centro tiene padding-right de 56px para que el icono flotante (48px) no tape columnas. Convención del sistema.
- Con servicios grandes la lista de filas se virtualiza (ventana vertical, desde 60 filas); columnas fijas y encabezados no se tocan. Los paneles laterales se pueden ocultar para dar ancho (flujo 16).

El **real se identifica por clave** `paquete|DIRECTA : partida` y no por el id de la línea, así sobrevive a las versiones nuevas del Plan Maestro.

**Maqueta del rediseño:** `docs/05-diseno-y-referencias/mockups/plan-maestro-rediseño.html` (F0-A, Observaciones Victor Lote 3, 2026-10-02).

### 3. Crear (aprobar) el Plan Maestro

«Crear Plan Maestro» queda inhabilitado hasta que el reparto cumple (la pantalla dice qué falta):

- Ningun metrado planificado puede ser negativo.
- No puede haber fecha duplicada para la misma línea.
- La suma diaria de cada **línea** debe ser exactamente igual a su metrado de línea.
- La suma de las líneas de cada **partida** debe ser exactamente igual a su metrado contractual (el 100 %; las partidas del DP sin línea se señalan). **Las partidas transversales quedan exentas** (no llevan línea) y el borrador no debe traer líneas de ellas: si las trae, se genera de nuevo.
- Las transversales marcadas deben tener la composición de mano de obra y equipo guardada al importar el DP (flujo 09).
- **Toda partida directa debe tener su disciplina** (ver más abajo).

Al crear, el sistema guarda y aprueba; el estado pasa a `APROBADO` (solo lectura para todo rol). Si ya había una aprobada, esta pasa a `REEMPLAZADO`. La aprobación se ejecuta en un solo paso, en este orden, y es **todo o nada** (U8): **Plan Maestro → reposicionamiento de los RDT → recálculo del PR**. Los tres ocurren **en una sola transacción**: si algo falla —también si el reposicionamiento o el recálculo fallan— no queda aprobado nada, ni el Plan Maestro en `APROBADO`, ni los RDT reposicionados, ni el PR recalculado.

**Qué ocurre al aprobar:**

- **Aviso de impacto antes de confirmar (U6).** Aprobar no es un solo paso: primero **se pide el aviso** y se muestra **qué RDT van a cambiar** (cuántos, y con qué fechas y metrados); **solo después se confirma**. Es la confirmación la que aplica el reposicionamiento y el recálculo, así que sin el aviso a la vista no hay nada que confirmar.
- **Reposicionamiento de los RDT (U4).** Cada RDT se vuelve a asociar a las líneas del plan vigente, por la clave de reporte `paquete × partida`, para que el Plan Maestro lo muestre en las fechas y metrados de la nueva línea base. Alcanza a **todos** los RDT del servicio, **incluidos los validados** (Enmienda E1, 2026-10-03).
  - **Lo que NO cambia:** ni el metrado ejecutado, ni los metrados derivados, ni las horas, ni el estado de validación. Y **las cifras del PR consolidado tampoco cambian**: el PR sigue declarando los RDT igual (aclaración de Victor, 2026-10-04).
  - **Lo que SÍ cambia es la asociación de paquete del RDT** (`rdt_actividades.paquete_trabajo_id` y `rdt_actividad_partidas.paquete_trabajo_id`), que es justamente la clave de reporte `paquete × partida`. Por eso un RDT ya registrado puede **verse con otro paquete en su propio formulario y en la pantalla Status**, además de cambiar de sitio en el Plan Maestro. No es una tabla de unión: entre el RDT y la línea del plan no hay FK, y la asociación de paquete **es** el vínculo (corrección del Auditor, 2026-10-04).
- **Rastro en el historial del RDT (U7).** Cada RDT afectado deja una fila de historial con la acción `REPOSICIONAMIENTO`. Su campo `snapshot` guarda **el plan anterior, el plan nuevo y su versión, el diff de claves** (de qué clave `paquete × partida` pasó a cuál) **y quién aprobó el Plan Maestro**. **No guarda fecha ni metrado como dato consultable**: qué se movió se lee en el diff de claves (flujo 06).
- **Recálculo del PR (bloque A' del PR).** `pr_partidas.metrado_planificado_acum` se recalcula desde las asignaciones del plan recién aprobado — **sumado por partida** aunque esté repartida en varios paquetes, sin arrastrar el reparto del plan reemplazado.

El Plan Maestro **no puede dejar de contemplar ninguna partida** (U5): al modificarlo solo se **mueven partidas** y se **crean o desagrupan paquetes**; nunca se elimina una partida del plan. Por eso ningún RDT queda sin partida.

### 4. Versión nueva

Con un Plan Maestro `APROBADO`, el botón «Crear versión nueva» pide un **motivo obligatorio** (máximo 500 caracteres) y crea un borrador que **parte de las asignaciones y de las disciplinas de la aprobada** (misma actividad y WBS). **Solo administrador y jefe de proyectos** pueden crear una versión nueva (fila propia en la tabla 2 del [flujo 14](14-accesos-y-restricciones.md)). **Aprobar** ese borrador, que reemplaza a la versión aprobada, lo pueden hacer los tres roles que gestionan el Plan Maestro (administrador, jefe de proyectos y planner), igual que la primera aprobación. El motivo se muestra en la versión aprobada. Al aprobarla rigen las mismas consecuencias de arriba: aviso de impacto (U6), reposicionamiento de los RDT (U4), rastro en el historial (U7) y recálculo del PR (U8). La versión nueva es la vía para cambiar el DP, el cronograma o los paquetes, cuya edición está bloqueada mientras haya una aprobada (U3), y también para **marcar o desmarcar partidas transversales** (Victor, 2026-10-19): se prepara el cambio en Paquetes, se crea el borrador nuevo (parte de la vigente), se aprueba, y desde ahí rigen las transversales nuevas; las métricas de los RDT se acomodan al nuevo plan.

### 5. Disciplina

- Catálogo fijo de 5 (Civil, Mecánica, Eléctrica, Instrumentación, Tuberías).
- **La partida directa lleva su propia disciplina**, obligatoria: se elige en el lienzo («Disciplina *») y es requisito para crear el Plan Maestro; el servidor la exige al aprobar y rechaza una inexistente o inactiva.
- **La partida dentro de un paquete hereda la del paquete** (se muestra «Hereda: X», no se edita aquí; se define en Paquetes, flujo 19).
- Las líneas anteriores a este plan quedan **sin disciplina** («Sin disciplina»); una línea de paquete cuyo paquete es anterior no bloquea la aprobación.

### 6. Umbral: planeación congelada con el Plan Maestro aprobado (U3)

Con un Plan Maestro `APROBADO` **lo único editable es el propio Plan Maestro** (crear una versión nueva con motivo obligatorio). Quedan **congelados** los datos de planeación:

- El **DP** y el **cronograma**: no se recargan ni se reemplazan (flujos 09 y 15).
- El **PR**: no se edita a mano; se recalcula desde sus fuentes (flujo 10) y dentro de la aprobación (U8).
- Los **paquetes de trabajo**: no se crean, editan ni archivan, **ni se reordenan** (`MOVER`), ni se declaran vínculos con metrado o hitos (flujo 19; el congelamiento de `MOVER` es U10, decided el 2026-10-04).

Lo **administrativo** (checklist, notificaciones y datos del servicio) sigue funcionando normal. Sin Plan Maestro aprobado, la recarga avisa lo que se perdería (vínculos, paquetes, borrador) y pide confirmación.

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
