# 2026-09-30 — Paquetes de Trabajo (declarar y agrupar) y Plan Maestro (lienzo de programación diaria)

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Este archivo contiene el Spec (paso 3). **Reemplaza por completo la versión anterior del mismo día**, que contradecía lo acordado con Victor (partida en un solo paquete, fechas dentro de Paquetes, metrado eliminado del cronograma).
>
> **Orden de ejecución decidido por Victor (2026-09-30):** primero `2026-09-30-niveles-presupuesto-y-cronograma.md`; después este plan. Este Spec puede aprobarse antes, pero no se planifica ni implementa hasta cerrar Niveles, porque los listados de Paquetes usan el mapa de niveles.

## Identificación y estado

- Tema: Cronograma → Paquetes de Trabajo → Plan Maestro.
- Fecha: 2026-09-30.
- Estado: **Planificando** (Spec `Aprobado` en el Gate Spec del 2026-09-30; sigue la delegación al Planner).
- Specs hermanos, se aprueban juntos: `2026-09-30-niveles-presupuesto-y-cronograma.md` y `2026-09-30-rdt-desde-plan-maestro.md`.
- Continúa y reemplaza en lo que contradice: `2026-09-23-paquetes-de-trabajo.md` (Fase 1 implementada; PL-1.9 sin cerrar).

## Spec / SDD

### Estado

`Aprobado (Gate Spec, 2026-09-30)`.

### Problema y contexto

Victor pidió entender cómo funcionan hoy Cronograma, Paquetes de Trabajo y Plan Maestro, porque no reflejan lo que quiere. Lo que quiere, en sus palabras y tras las aclaraciones del 2026-09-30:

1. **Cronograma:** cargar el archivo y ver el cronograma. Es lo que se entrega al cliente como base.
2. **Paquetes de Trabajo:** en un lado el listado del cronograma y en el otro el DP (solo partidas, solo visual). Ahí se **declara** a qué partida pertenece cada actividad y con qué metrado (columna nueva "Metrado"), y luego se **agrupan** en paquetes para mejorar la reportabilidad de campo. Hay partidas que no pertenecen a ningún paquete (por ejemplo "Eliminación de material excedente").
3. **Plan Maestro:** un lienzo con todos los días, las seis columnas por semana (avance físico, avance económico y HH, cada uno semanal y acumulado) y las filas ya armadas desde Paquetes (partidas, metrados, agrupación). El usuario solo coloca metrados por día; **no se puede crear el Plan Maestro hasta repartir todos los metrados**.
4. **PR:** recibe la extracción del DP directamente. Como el vínculo actividad ↔ partida ya se hace en Paquetes, es fácil saber cómo llenar cada partida. Una partida puede estar dividida entre varios paquetes; en el PR sigue siendo una sola.

**Estado verificado en el código (`py_control_proyectos_web`, `main` = `origin/main`, 2026-09-30):**

| Pieza | Lo que hay hoy | Dónde |
|---|---|---|
| Cronograma | Además de cargar y mostrar, tiene el bloque que vincula cada tarea con partidas del DP **con metrado exacto** y exige el 100% por partida antes de guardar (`PATCH /api/cronograma` rechaza vínculos sin metrado > 0). Al subir el archivo, el enlace automático 1:1 por EDT asigna a la tarea el metrado contractual de la partida. | `FormularioCronograma.tsx`, `src/app/api/cronograma/route.ts` (~113-205 y ~378), `src/lib/cronograma/vinculos.ts`, `db/071` |
| Uso del vínculo | `recalcular_pr_fechas_base` toma las fechas base del PR de ese vínculo, sin mirar el metrado. | `db/062_pr_fechas_base_cronograma.sql` |
| Paquetes | Formulario único: marcar partidas, metrado, inicio y fin por partida, botón "Repartir en días", lista vertical fecha → metrado. Tras guardar, la tarjeta muestra solo código, nombre, estado y "N partida(s)": sin contenido, sin orden, sin edición (solo Archivar). Una partida puede estar en varios paquetes (sus aportes se suman). | `FormularioPaquetesTrabajo.tsx`, `src/app/api/paquetes-trabajo/route.ts`, `db/072` |
| Programación diaria | Vive en `paquete_trabajo_programacion`. Al generar el Plan Maestro se **copia** a `plan_maestro_asignaciones`. Dos tablas con el mismo dato. | `db/072`, `db/037`, `src/app/api/plan-maestro/route.ts` (POST) |
| Plan Maestro | "Generar propuesta" copia desde paquetes; vistas Resumen y Semanal de solo lectura; conserva "Editar distribución diaria" (lista vertical), aunque el plan del 23-sep daba por hecho quitarla. | `FormularioPlanMaestro.tsx` (~369) |
| Reglas al generar | Exige que **todas** las partidas estén en algún paquete. Sin paquetes, error. | `src/app/api/plan-maestro/route.ts` (~139-233) |
| Aprobación | `PATCH APROBAR` exige que cada partida sume exactamente su metrado contractual; reemplaza la versión anterior y recalcula el planificado del PR. | `src/app/api/plan-maestro/route.ts` (~367-421) |
| Partida repetida | `plan_maestro_partidas` tiene `unique (plan_maestro_id, wbs)`: una sola línea por partida. `recalcular_pr_planificado` y la Curva S **ya suman por WBS**, así que repetir líneas funciona una vez relajada esa restricción. | `db/037`, `db/061`, `db/070` |
| HH por unidad | `dp_partidas.hh_und_partida` existe. HH programadas = Σ (metrado del día × HH por unidad). | `db/004_dp.sql` |

### Resultado esperado

**Cronograma:** solo carga y vista (el Gantt con línea base y real es un plan futuro, ya registrado en `planes-futuros.md`). El enlace automático por EDT se conserva y pre-llena la columna Metrado.

**Paquetes de Trabajo**, en la misma pantalla y con los paneles laterales ocultables:

- **Declarar.** A un lado, el listado del cronograma con su jerarquía de niveles y la columna **Metrado**. Al otro, el DP mostrando solo las partidas, solo para consulta. Por actividad se declara partida y metrado; una actividad puede tener varias partidas y una partida varias actividades.
- **Agrupar.**
  - Botón **"Crear paquete"** (no es un chip del panel). Al pulsarlo aparece una casilla al inicio de cada ítem, menos el de Servicio.
  - El usuario marca los ítems, escribe el nombre del paquete, le asigna su nivel (todo ítem tiene un nivel) y guarda.
  - El paquete creado se distingue con un color u otra marca visual. Al seleccionarlo se selecciona el paquete completo. Se puede **mover hacia arriba o abajo** (flechas) para cambiar el orden y **plegar** para ver solo su nombre.
- Las partidas o actividades que no se agrupan quedan como filas directas.
- Una partida puede quedar **dividida entre paquetes** porque sus actividades van a paquetes distintos; la suma de sus metrados declarados debe dar el 100% del contractual.

**Plan Maestro:** el lienzo de la imagen de Victor, editable mientras está en `BORRADOR` y solo visual una vez aprobado:

- A la izquierda, columnas fijas: WBS, descripción, Und., metrado, costo unitario y **HH por unidad de partida** (`dp_partidas.hh_und_partida`, de donde salen las HH programadas).
- A la derecha, una columna por día, agrupadas por semana (sábado a viernes), y **seis columnas por semana** (decidido por Victor): avance físico, avance económico y HH programadas, cada uno **semanal y acumulado**, con la definición de P8. El avance económico programado acumulado es el **PV** del servicio.
- El Plan Maestro muestra también la **ejecución real** (RDT validado), junto a lo programado: lo programado alimenta el PV y el planificado del PR; lo real alimenta el avance y el EV del PR. Son dos fuentes que no se mezclan: lo real nunca sobrescribe lo programado (flujo 20). Ver P14 a P16.
- Fila de total del servicio arriba; filas de paquete plegables con subtotal; partidas repetidas por paquete con su porción; partidas directas.
- El usuario solo escribe metrado por día. Cada fila muestra cuánto le falta repartir.
- Semanas que se pueden **colapsar y expandir**: se edita una semana, se colapsa y se sigue con otra.
- Paneles laterales ocultables.
- Solo se puede crear (aprobar) el Plan Maestro cuando todos los metrados están repartidos.

### Alcance

1. **Paquetes:** pantalla de dos lados (cronograma con Metrado y DP solo visual); declaración actividad → partida → metrado; "Crear paquete" con casillas, nombre y nivel; marca visual; selección de paquete completo; mover arriba o abajo; plegar; paquete sin fechas; partida repartida entre paquetes; edición de paquetes en `BORRADOR`.
2. **Cronograma:** se retira de su pantalla el bloque de vínculos con metrado y la lista de partidas incompletas, que pasan a Paquetes. `PATCH /api/cronograma` deja de exigir el 100% ahí; la regla del 100% se exige al abrir el Plan Maestro.
3. **Plan Maestro:**
   - Lienzo con sus columnas fijas, días, semanas plegables y seis columnas por semana (con interruptor para ocultar las acumuladas), más la visualización de lo real junto a lo programado.
   - Filas desde Paquetes: una línea por actividad × partida, con su paquete.
   - Fin de "Generar propuesta" (copia) y de "Editar distribución diaria".
   - Versión nueva en `BORRADOR` desde la aprobada vigente o, si no hay, desde Paquetes.
   - Validaciones de aprobación intactas (cada partida suma su contractual).
4. **Ocultar paneles laterales:** control del shell, reutilizable, usado en Paquetes y Plan Maestro.
5. **Documentación:** flujos 15, 19, 20 y 16 (14 solo si cambian acciones o accesos), tras consultar cada contradicción a Victor.

### No alcance

- Niveles de importación (plan previo), Gantt con línea base y real (plan futuro), 3WLA, el cambio del RDT para listar paquetes y partidas del Plan Maestro y declarar avance por paquete (Spec posterior propuesto, P14; Fase 2 del plan del 23-sep), multi-moneda, orden de trabajo (concepto distinto).
- Borrar columnas o tablas existentes: todo cambio de esquema es aditivo o relaja una restricción; `paquete_trabajo_programacion` y lo que quede sin uso se conservan hasta que Victor autorice su retiro.

### Usuarios / roles afectados

- Paquetes: sin cambio de permisos (`puedeGestionarPaquetesTrabajo`; ver para los 13 roles según el plan `paneles-servicio-persistente`). No muestra dinero.
- Plan Maestro: ver = `puedeVerPlanMaestro`; editar y aprobar = `puedeGestionarPlanMaestro` (administrador, jefe de proyectos, planner). El lienzo muestra costos, así que lo ven los roles con economía más el planner (flujo 14).
- No se crea chip, pantalla ni acción nueva ("Crear paquete" es un botón interno). Si el Auditor encuentra que alguna acción cambia de nombre o alcance, se actualizan en la misma tarea el artefacto «Matriz de permisos» y el flujo 14.

### Reglas de negocio y documentos afectados

Toda contradicción con lo escrito se consulta a Victor antes de editar el flujo.

| Flujo | Dice hoy | Cambia a | Estado |
|---|---|---|---|
| 15 Cronograma | Vínculo con metrado exacto y 100% por partida editados en el cronograma; "Relación con Paquetes" (fechas de paquete) | El cronograma solo carga y muestra; el vínculo con metrado se declara en Paquetes; el 100% se exige al abrir el Plan Maestro | **Pendiente de consulta** |
| 19 Paquetes | "Fechas planificadas opcionales"; "no se duplican partidas activas, salvo distribución parcial autorizada" | Sin fechas en el paquete; la partida repartida entre paquetes es regla general; el paquete agrupa actividades × partida con su metrado y se ordena | **Pendiente de consulta** |
| 20 Plan Maestro | Distribución diaria desde paquetes; sin paquete no hay Plan Maestro; "Generar propuesta" copia | Lienzo que se llena en `BORRADOR`; partidas sin paquete permitidas; sin copia | **Pendiente de consulta** |
| 16 Paneles | El panel izquierdo ya existe (Recursos de empresa con mostrar/ocultar y accesos del servicio, plan `paneles-servicio-persistente` cerrado); no hay control para ocultar los paneles laterales | Suma ocultar los paneles laterales (izquierdo y derecho) | **Pendiente de consulta** |
| 06 RDT | El supervisor elige partidas del DP agrupadas por subpresupuesto | Elige paquetes y partidas del Plan Maestro (Spec posterior, P14) | **Pendiente de consulta** |
| 18 Control de avance | Avance por partida; "para hitos o paquetes ponderados se aplica el método de medición configurado" | El real se declara contra paquete × partida y el PR suma por partida | **Pendiente de consulta** |
| 20 Plan Maestro (regla del RDT) | "El RDT debe usar un WBS existente en el DP del mismo servicio; al validar se registra el vínculo RDT – partida DP" | El RDT usa paquetes y partidas del Plan Maestro | **Pendiente de consulta** |
| 14 Accesos | Acciones de Plan Maestro y Paquetes | Sin cambio esperado; el Auditor lo verifica | Por verificar |
| Decisiones 5 y 6 del plan 2026-09-23 | Fechas personalizadas del paquete; sin paquete no hay Plan Maestro | Reemplazadas por este Spec | **Pendiente de consulta** |

### Datos, API, migraciones o dependencias

Propuesta, sujeta al Planner (aplicar a mano en el SQL Editor según `db/README.md`; se comprueba antes si `072` está aplicada):

- **Membresía del paquete:** hoy `paquete_trabajo_partidas` es `(paquete, partida, metrado)` con `unique (paquete, partida)`. Pasa a referirse al vínculo actividad × partida (con su metrado), para que una misma partida pueda estar en varios paquetes con porciones distintas. El Planner verifica la llave de `cronograma_actividad_partidas` (`db/039`).
- `paquetes_trabajo`: `orden` y `nivel` (rol o nivel del árbol donde se muestra).
- `plan_maestro_partidas`: relajar `unique (plan_maestro_id, wbs)` (hoy una línea por partida) y agregar referencia al vínculo, más copia del paquete (id, código, nombre, orden) y de `hh_und_partida`, para que una versión aprobada no cambie si luego se renombra o archiva un paquete.
- API: `GET /api/plan-maestro` devuelve líneas con paquete e HH por unidad; `POST` crea `BORRADOR` sin exigir paquetes; `PATCH` mantiene guardar y aprobar con la validación del 100% y la recalculación del PR. Paquetes: creación, edición y orden por vínculo. Cronograma: el `PATCH` de vínculos sin la regla del 100%.
- Dependencias: el plan de Niveles (listados con jerarquía). El plan `paneles-servicio-persistente` ya está **cerrado y mergeado** (`45c9e0a` en la app, verificado 2026-09-30), así que "ocultar paneles" parte de un `WorkspaceShell.tsx` y un registro único de accesos estables. El `main` de la app está 27 commits por delante de `origin/main` (sin push); eso lo decide Victor.

### Diseño / UI aplicable

- **Paquetes:** dos lados (cronograma con Metrado | DP solo partidas); "Crear paquete" con casillas; color o marca para paquetes; flechas arriba y abajo; plegar. Cronograma y DP con su jerarquía según el mapa de niveles.
- **Lienzo:** referencia principal, la imagen de Victor.
  - Fijo a la izquierda de la línea naranja, desliza a la derecha.
  - Seis columnas por semana (físico, económico y HH; semanal y acumulado).
  - Encabezado de total del servicio.
  - Semanas plegables.
- Sujeto a `docs/05-diseno-y-referencias/design.md`; el Planner lo lee antes de fijar componentes. Tablas largas con scroll horizontal y columnas fijas (regla de interfaz de `AGENTS.md`).

### Riesgos y decisiones pendientes

**Propuestas del Orquestador que Victor debe confirmar en el Gate Spec** (las no mencionadas por Victor siguen marcadas como pendientes):

- **P1.** Cómo se elige la partida de una actividad: desplegable en la celda Metrado, pre-llenado por el enlace automático por EDT. El DP del otro lado es solo de consulta.
- **P2.** "Asignarle su nivel" al paquete: ¿es el nivel del árbol donde el paquete aparece (por ejemplo al nivel de "Paquete de partidas")? Propuesta: sí, elegido entre los niveles del mapa.
- **P3.** Marcar una fila resumen (un nivel) marca todas sus hijas; se pueden desmarcar.
- **P4.** La regla del 100% por partida se exige **para abrir el Plan Maestro**; en Paquetes se puede guardar parcial. Una partida sin actividad bloquea y se avisa cuál.
- **P5.** "Crear el Plan Maestro" es el actual "Aprobar línea base"; el `BORRADOR` se puede guardar parcial y retomar otro día; tras cerrar, una versión nueva la hacen administrador y jefe de proyectos con motivo.
- **P6 (confirmada por Victor).** Fechas libres (no limitadas a las del cronograma): el rango de la actividad se sombrea como guía y el rango de días se puede ampliar antes o después.
- **P7 (colapsar y expandir confirmado por Victor; repartir el total de la semana, pendiente).** Semanas: colapsar y expandir, más la opción de escribir el total de una semana y repartirlo entre sus días.
- **P8.** Las tres medidas del Plan Maestro se calculan por separado y no se mezclan: **avance físico** = metrado programado acumulado ÷ metrado contractual, por partida (flujo 10 y 18); **avance económico** = metrado × precio unitario; **HH programadas** = Σ (metrado programado × HH por unidad de la partida). Para las filas de paquete y el total del servicio, donde se juntan partidas con unidades distintas (m³, kg, ml) y el metrado no se puede sumar, **Victor decidió (2026-09-30) la opción A**: el % físico se pondera por costo, igual que el sistema ya define EV ÷ BAC (`calcularAvanceFisico` en `dashboard.ts`), aplicado al programado. El resultado es un porcentaje; el costo solo sirve de peso. El avance físico se muestra de **dos maneras: avance semanal y avance acumulado** (ver el anexo con el ejemplo de 4 semanas). Pendiente: si el avance económico y las HH también se muestran semanal y acumulado (propuesta: sí, los tres). Se retira la idea de ponderar por HH (salió de interpretar la imagen, no del sistema). **HH ganadas** (HH de lo ejecutado contra HH reales, flujo 18) no pertenece al Plan Maestro.
- **P9.** Eliminar las columnas de Tiempo (Duración, Inicio, Fin) del lienzo; Victor lo planteó ("quizás debamos eliminar tiempo"). Las fechas del cronograma se ven en Paquetes.
- **P10 (confirmada por Victor).** Paquete en modo "por avance del paquete": se edita la unidad del paquete, que es la de su partida guía; las demás partidas se calculan con el mismo % y quedan en solo lectura. Con partidas repartidas, la base es la porción de la guía dentro de ese paquete.
- **P11 (definida por Victor).** Volver a cargar algo que está **antes** del Plan Maestro (DP, cronograma):
  - **Si ya existe un Plan Maestro `APROBADO`, no se puede cargar nada**: es una restricción, sin confirmación que la levante.
  - **El `BORRADOR` no restringe** (definido por Victor): no cuenta como Plan Maestro existente.
  - Sin Plan Maestro aprobado, recargar se bloquea primero: el sistema avisa exactamente qué se perdería (vínculos, paquetes, lo avanzado en el borrador) y solo después de ese aviso y de una confirmación explícita permite cargar.
- **P12.** Ocultar paneles es un control global del shell, recordado por usuario.
- **P13 (confirmada por Victor).** `paquete_trabajo_programacion`: conservar sin uso; el Worker comprueba si tiene filas en la BD real antes de decidir.
- **P14 (definida por Victor). El RDT lista lo que está en el Plan Maestro** (paquetes y sus partidas, y las partidas directas), **ya no las partidas del DP**. Sin eso la trazabilidad y el objetivo no funcionarían. Consecuencias:
  - **Se resuelve la partida repartida entre paquetes:** el RDT declara contra la fila del paquete, así que el real se atribuye a cada paquete sin estimar nada. El PR sigue sumando por partida.
  - Hoy el catálogo del RDT sale de `dp_partidas` y `dp_subpresupuestos` (`/api/rdts/catalogos`) y el vínculo del RDT guarda solo `dp_partida_id` (`rdt_actividad_partidas`, `db/040`). Ambos cambian.
  - **Clave estable:** el vínculo del RDT debe apuntar a algo que sobreviva a una versión nueva del Plan Maestro (paquete + partida, no el id de la línea de una versión), para que los RDT validados no queden huérfanos al re-baselinear.
  - **Sin respaldo para servicios antiguos** (Victor, 2026-09-30): todos los servicios existentes son de prueba; el RDT lista siempre el Plan Maestro. PS-0006 ya no existe: se eliminó en la limpieza de datos de prueba del plan de paneles, autorizada por Victor (quedan PS-0004 y PS-0005). Todos los servicios existentes son de prueba y se pueden tocar.
  - La unidad de declaración del RDT es el paquete × partida (las actividades son del cronograma); en modo "por avance del paquete" se declara la unidad del paquete y se reparte el % a sus partidas (P10, Fase 2 del plan del 23-sep).
  - **Alcance (Victor confirmó):** el cambio del RDT es grande (flujos 06, 18 y 20) y va en su propio Spec, `2026-09-30-rdt-desde-plan-maestro.md`. Los tres Specs se aprueban juntos y un solo plan los reparte entre Workers; este Spec solo deja las claves estables y el dato listo.
- **P15 (aceptada por Victor).** Cada partida con dos subfilas, "Prog." (editable en borrador) y "Real" (solo lectura, desde RDT validado), con las mismas columnas por semana; el Real se oculta con un interruptor. Las semanas del lienzo se extienden si hay real fuera del rango programado (ejecución atrasada).
- **P16. Medidas de lo real (Victor: avance físico, avance económico y HH, acumuladas por semana).** % físico real, **EV** (metrado real × precio unitario, valor ganado; no el costo gastado) y **HH reales**. Las HH reales por semana hoy no están conectadas: el Plan Maestro las deja en 0 como marcador y el PR las guarda acumuladas por partida (la pieza existe en el consolidado de RDTs; el Planner la verifica). Hay que construir ese dato. **HH ganadas** (flujo 18) sigue fuera del Plan Maestro. **Decidido por Victor:** lo real se muestra igual que lo programado, semanal y acumulado (6 columnas por semana), con interruptor para ocultar las acumuladas.
- **P17. Hitos del cronograma (actividades que "no requieren partidas").** Existen desde el 23-sep (`cronograma_actividades.requiere_partidas`, columna Hito en la pantalla del cronograma, `/api/cronograma/hitos`). Al mover la declaración a Paquetes, hay que decidir dónde se marcan y qué pasa con ellos. Propuesta: la marca de hito se mueve a Paquetes junto a la columna Metrado (quien declara metrado decide qué actividades no llevan partida); los hitos se ven atenuados en el listado, sin metrado, no entran a paquetes ni al Plan Maestro y no cuentan para la regla del 100%.

**Riesgos:**

- `WorkspaceShell.tsx`, el registro único de accesos y `permisos.ts` siguen siendo archivos de choque entre los Workers de este plan.
- Dependencia de Niveles: si se atrasa, este plan espera.
- La `072` pudo no estar aplicada en algún entorno.
- Los servicios con Plan Maestro aprobado no se tocan; la nueva versión parte de sus asignaciones.
- Tamaño del lienzo (filas × días): el Planner evalúa virtualización.
- Relajar `unique (plan_maestro_id, wbs)` es un cambio de restricción; requiere autorización expresa y revisión de datos existentes.

### Criterios de aceptación

1. Cronograma: carga y muestra; sin edición de metrado ni del 100% en su pantalla; el PR conserva sus fechas base.
2. Paquetes: se ven el cronograma (con columna Metrado) y las partidas del DP; se declara actividad → partida → metrado; se crean paquetes con casillas, nombre y nivel; el paquete se distingue, se selecciona completo, se mueve arriba o abajo y se pliega.
3. Una partida puede estar en dos o más paquetes con metrados que suman su contractual; el PR la muestra una sola vez con la suma.
4. Plan Maestro: el lienzo muestra columnas fijas (incluida "HH por unidad de partida") y días deslizantes, semanas plegables, seis columnas por semana con su definición propia (físico, económico y HH; semanal y acumulado), lo real junto a lo programado y total del servicio; solo se escribe metrado por día; los totales se recalculan.
   - Recargar el DP o el cronograma con datos posteriores se bloquea, avisa qué se perdería y pide confirmación (P11).
5. No se puede crear el Plan Maestro mientras alguna línea no reparta su metrado; el mensaje indica cuáles.
6. Un servicio sin paquetes programa sus partidas directas.
7. Al aprobar, la versión anterior pasa a `REEMPLAZADO` y el PR recalcula el planificado; aprobado = solo lectura.
8. Se pueden ocultar y mostrar los paneles laterales.
9. Flujos 15, 19, 20 (y 16) coherentes con lo implementado; el Auditor verifica la trazabilidad antes del Gate 2.

### Estrategia de prueba / evidencia

- Lógica pura con vitest: suma por partida entre paquetes, 100%, totales semanales, HH, % físico (según P8), reparto proporcional (P10), agrupación por semana, orden de paquetes.
- `tsc --noEmit`, suite completa, lint comparado contra `main` (baseline al 2026-09-23: 9 errores / 18 warnings; se vuelve a medir).
- Verificación en vivo con Playwright y login real (cuentas en memoria, nunca en el repositorio), una captura por ítem, snapshot de texto como comprobación principal.
- Punch List con resultado por ítem en `03-evidencia/`; progreso en `02-progreso/`.

### Aprobación (Gate Spec)

- [x] Victor aprueba este Spec, incluidas P1 a P17 y la consulta de cada contradicción de la tabla de flujos.

## Anexo — Ejemplo de 4 semanas (caso de prueba de los totales)

Datos inventados, para fijar las fórmulas. Dos paquetes y una partida directa. Todo llega a 100% acumulado en la semana 4.

| Fila | Modo | Und. | Metrado | Precio unitario | BAC | HH por unidad |
|---|---|---|---|---|---|---|
| Paquete 1 "Banco ducto" | por partidas | | | | $5 000 | |
| · Excavación | | m³ | 100 | $10 | $1 000 | 0.5 |
| · Cama de arena | | ml | 50 | $20 | $1 000 | 0.4 |
| · Acero | | kg | 1 000 | $3 | $3 000 | 0.05 |
| Paquete 2 "Relleno" | por avance del paquete, guía = Relleno | | | | $2 200 | |
| · Relleno (guía) | | m³ | 80 | $15 | $1 200 | 0.3 |
| · Suministro afirmado | | m³ | 40 | $25 | $1 000 | 0.2 |
| Directa "Eliminación de material" | sin paquete | m³ | 200 | $5 | $1 000 | 0.1 |
| **Total del servicio** | | | | | **$8 200** | |

Metrado programado por semana (Paquete 1 y la directa se escriben por partida; en el Paquete 2 solo se escribe el de la guía y el afirmado se calcula con el mismo %):

| Partida | S1 | S2 | S3 | S4 | Suma |
|---|---|---|---|---|---|
| Excavación | 50 | 50 | 0 | 0 | 100 |
| Cama de arena | 10 | 10 | 15 | 15 | 50 |
| Acero | 200 | 300 | 300 | 200 | 1 000 |
| Relleno (guía, escrito) | 20 | 20 | 20 | 20 | 80 |
| Afirmado (calculado, 25% c/semana) | 10 | 10 | 10 | 10 | 40 |
| Eliminación | 0 | 0 | 100 | 100 | 200 |

Totales por fila y semana. Físico de una partida = metrado ÷ contractual. Físico de un paquete o del total = avance económico ÷ BAC de ese grupo (opción A).

| Fila | Medida | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|
| Paquete 1 | Avance económico semanal | $1 300 | $1 600 | $1 200 | $900 |
| | % físico semanal | 26% | 32% | 24% | 18% |
| | % físico acumulado | 26% | 58% | 82% | 100% |
| | HH programadas | 39 | 44 | 21 | 16 |
| Paquete 2 | Avance económico semanal | $550 | $550 | $550 | $550 |
| | % físico semanal | 25% | 25% | 25% | 25% |
| | % físico acumulado | 25% | 50% | 75% | 100% |
| | HH programadas | 8 | 8 | 8 | 8 |
| Directa | Avance económico semanal | $0 | $0 | $500 | $500 |
| | % físico semanal | 0% | 0% | 50% | 50% |
| | % físico acumulado | 0% | 0% | 50% | 100% |
| | HH programadas | 0 | 0 | 10 | 10 |
| **Total** | Avance económico semanal | $1 850 | $2 150 | $2 250 | $1 950 |
| | % físico semanal | 22.56% | 26.22% | 27.44% | 23.78% |
| | % físico acumulado | 22.56% | 48.78% | 76.22% | **100%** |
| | HH programadas | 47 | 52 | 39 | 34 |

Comprobaciones: los semanales de cada fila suman 100%, el económico suma el BAC ($8 200) y las HH suman 172.

## Novedades verificadas tras cerrar el plan de paneles (2026-09-30)

Verificadas en el código y los flujos vigentes, no de memoria. **No cambian ninguna decisión aprobada en el Gate Spec**; ajustan detalles de ejecución.

| # | Hallazgo | Efecto en estos Specs |
|---|---|---|
| 1 | `.worktrees/local-worker-1` se avanzó a `main` (`45c9e0a`, sin push, limpio). Su `node_modules` es un enlace al del repositorio principal: Turbopack no corre ahí, se usa `--webpack` (`03-entorno-git-y-worktrees.md`). La última migración sigue siendo la `072`: el plan de paneles no agregó ninguna. | Los rangos de migración se reservan desde la `073`. |
| 2 | Existe un **registro único de accesos** (`src/lib/config/registro-accesos.ts`, 611 líneas) con pruebas (`registro-accesos.test.ts`, `registro-humo.test.ts`, `matriz-accesos.test.ts`, `panel-izquierdo.test.ts`, `nav-proyecto.test.ts`). Todo chip o acción pasa por ahí. | Estos Specs no crean chips. Si un Worker toca el registro, actualiza sus pruebas; `registro-accesos.ts` y `permisos.ts` son archivos de choque. |
| 3 | Ya hay una acción registrada **"Crear paquete"** (A7, `/paquetes-trabajo?accion=crear`) que abre Paquetes con el formulario de paquete nuevo abierto (`abrirNuevoAlInicio`). Victor pidió "Crear paquete (no chip)" dentro de la pantalla. | Se conservan las dos cosas: el botón dentro de Paquetes y la acción del panel, que abre la pantalla ya en "modo crear" (casillas activas). **Confirmado por Victor (2026-09-30).** |
| 4 | El flujo 14 ya lista "Subir / reemplazar cronograma", "Gestionar Plan Maestro (crear / congelar línea base)" y "Gestionar paquetes de trabajo", los tres con los mismos roles (administrador, jefe de proyectos, planner). Además conserva una sección "Accesos requeridos para paquetes (pendiente)" con acciones más finas (crear, editar, archivar, registrar avance…). | Mover la declaración actividad → partida → metrado del cronograma a Paquetes **no cambia roles**: se ajusta el texto de esas filas y de la sección pendiente (recomendación: una sola acción "Gestionar paquetes"). El artefacto «Matriz de permisos» se actualiza en la misma tarea. |
| 5 | Ver Plan Maestro exige rol con economía o planner **y alcance por OT al leer** (F5B). Cronograma, Paquetes y las pantallas de RDT se ven con los 13 roles y sin alcance por OT al leer (R30). | Sin cambio: el lienzo hereda esa guarda. |
| 6 | El flujo 16 ya describe el panel izquierdo. "Recursos de empresa" tiene su propio mostrar/ocultar; en móvil los paneles son un cajón. | "Ocultar paneles laterales" es nuevo, solo para escritorio, y no reemplaza ese botón. |
| 7 | Mejora `2026-09-30-plan-paneles-servicio-persistente-tandas.md`: la consulta a Victor sobre flujos se hizo **en bloque** (tabla de contradicciones con lo que dice hoy y lo que pasaría a decir) y una sola aprobación cubrió a todos los Workers. Un Worker de fase entera no cabe en una sesión. Faltó un servicio de prueba con datos. | El Planner arma esa tabla en bloque para el Gate 1. Las tandas siguen en 4 a 8 ítems. **Este plan necesita un servicio de prueba dedicado con DP, cronograma y RDT**, distinto del que Victor quiere conservar. |
| 8 | Prácticas de verificación: agrupar el trabajo por cuenta o usar "Ver como" (`POST /api/ver-como`), no tomar snapshot del login relleno, comprobar redirecciones con la URL final, no usar scripts de reemplazo masivo sobre el plan, declarar al inicio las herramientas de navegador que se usarán. | Se copian a los briefs de las tandas. |

**Servicio de prueba:** PS-0006 ya no existe: se eliminó en la limpieza de datos de prueba del plan de paneles, autorizada por Victor (quedan PS-0004 y PS-0005). Todos los servicios existentes son de prueba y se pueden tocar. Victor autorizó crear un servicio de prueba dedicado para la verificación de este plan (con DP, cronograma y RDT propios).

## Entorno, repositorios, ramas y worktrees

- Modo: local. Documentación en `pg_control_proyectos` (`main`, directo); código en `py_control_proyectos_web`.
- `git worktree list` (2026-09-30): existe `.worktrees/local-worker-1` (rama `local-worker-1`, commit `0690c81`). Verificado el 2026-09-30: está limpio y su rama ya está mergeada en `main` (plan de paneles cerrado), así que puede reutilizarse con autorización de Victor; no se crea ni borra rama o worktree sin autorización.
- Plan grande: tandas de 4 a 8 ítems, brief ≤ 8 KB, ~80 llamadas por Worker (`planes-grandes-en-tandas`). Un solo worktree activo a la vez.
- **Ejecución conjunta (Victor, 2026-09-30):** los tres Specs (Niveles, Paquetes y Plan Maestro, RDT desde el Plan Maestro) se aprueban juntos y **un solo plan** los reparte. Victor quiere **hasta 4 Workers en paralelo** si el plan lo indica. Condiciones que el Planner debe respetar:
  - Solo se divide donde haya independencia real de archivos, migraciones y componentes base (`02-roles-y-delegacion.md`). Orden de datos: Niveles → Paquetes → Plan Maestro → RDT; la UI y la lógica pura sí se pueden construir en paralelo con datos simulados.
  - Cada Worker necesita su rama y su worktree. **Crear ramas y worktrees requiere autorización explícita de Victor**; hoy existe solo `.worktrees/local-worker-1`. La mejora `planes-grandes-en-tandas` decía "un solo worktree activo a la vez" (por los costos de contexto de esa vez); con 4 Workers esa regla se revisa, manteniendo tandas de 4 a 8 ítems, brief ≤ 8 KB y ~80 llamadas por sesión.
  - **Archivos de choque** que el Planner asigna a un solo Worker por fase: `permisos.ts`, `nav-proyecto.ts`, `WorkspaceShell.tsx`, el contador del test de nav, y la numeración de migraciones (reservar rangos por Worker: hoy la última es `072`).
  - Reparto posible (orientativo): Worker A Niveles (importación DP y cronograma, mapa, migración); Worker B lienzo del Plan Maestro (lógica pura de totales y componente) con ocultar paneles; Worker C Paquetes (pantalla, declarar y agrupar); Worker D RDT desde el Plan Maestro. Los Workers C y D dependen de datos de A y B.

## Asignación de roles

| Rol | Chat | Rama | Worktree | Estado |
|---|---|---|---|---|
| Orquestador | por nombrar | `main` | N/A | Activo |
| Planner | tras el Gate Spec y el cierre de Niveles | `main` | N/A | Pendiente |
| Worker | tras el Gate 1 | por confirmar | por confirmar | Pendiente |
| Auditor | por asignar | `main` | N/A | Pendiente |

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-09-30 | **Gate Spec: Victor aprobó los tres Specs ("todo aprobado")**, con las recomendaciones del Orquestador para todas las decisiones pendientes. Queda abierto, sin bloquear: el nombre del rol extra cuando un archivo trae más de 5 niveles (D6). El texto exacto de cada flujo contradicho se le muestra antes de editarlo. | Victor |
| 2026-09-30 | El cronograma solo carga y muestra; es la base que se entrega al cliente. El seguimiento con línea base y real es otro plan (registrado en `planes-futuros.md`). | Victor |
| 2026-09-30 | Actividad → partida → metrado se declara en Paquetes de Trabajo, con una columna "Metrado" junto al cronograma; sale del cronograma. | Victor |
| 2026-09-30 | Paquetes: cronograma en un lado y DP (solo partidas, solo visual) en el otro. | Victor |
| 2026-09-30 | "Crear paquete" es un botón (no un chip): casillas en todos los ítems menos Servicio, nombre, nivel, guardar; el paquete se ve distinto, se selecciona completo, se mueve arriba o abajo y se pliega. | Victor |
| 2026-09-30 | Una partida puede dividirse entre paquetes; los metrados suman el 100% desde Paquetes. El PR muestra una sola partida con la suma. | Victor |
| 2026-09-30 | Hay partidas que no pertenecen a ningún paquete; un servicio puede no usar paquetes. | Victor |
| 2026-09-30 | Las tres medidas (físico, económico, HH) van con avance semanal y avance acumulado: seis columnas por semana. El Plan Maestro muestra el PV (lo programado) y la ejecución real; cada uno alimenta sus propias tablas. Se parece al plan semanal (3WLA) pero este completa la programación de todo el servicio. | Victor |
| 2026-09-30 | Los servicios existentes son de prueba: sin compatibilidad hacia atrás, PS-0006 ya no existe (eliminado en la limpieza del plan de paneles). Se autoriza crear un servicio de prueba dedicado para este plan. | Victor |
| 2026-09-30 | Los tres Specs se aprueban juntos y un solo plan los reparte; hasta 4 Workers en paralelo si el plan lo indica. El RDT va en su propio Spec. | Victor |
| 2026-09-30 | **El RDT lista los paquetes y partidas que están en el Plan Maestro, ya no las partidas del DP**; si no, la trazabilidad y el objetivo no funcionarían. | Victor |
| 2026-09-30 | En el lienzo, cada partida lleva una subfila "Prog." y una "Real" (P15). Lo real mide avance físico, avance económico (EV) y HH, acumuladas por semana (P16). | Victor |
| 2026-09-30 | Plan Maestro: lienzo de días con columnas por semana y filas desde Paquetes; solo se colocan metrados; se crea cuando todos estén repartidos; paneles laterales ocultables. | Victor |
| 2026-09-30 | Edición por bloques de semana con colapsar y expandir; el rango de fechas se puede ampliar. | Victor |
| 2026-09-30 | El avance se define por la partida. El Plan Maestro mide tres cosas por separado: avance físico (partida), avance económico (partida × costo) y HH programadas (Σ metrado × HH por unidad). No se mezclan; HH ganadas es otro concepto (flujo 18) y no entra. | Victor |
| 2026-09-30 | % físico en las filas de paquete y en el total del servicio: ponderado por costo (opción A, como el Dashboard). El avance físico se muestra como avance semanal y avance acumulado. | Victor |
| 2026-09-30 | Si ya existe un Plan Maestro aprobado no se puede volver a cargar nada anterior a él: es una restricción. El borrador no restringe. Sin Plan Maestro aprobado, recargar se bloquea, se avisa lo que se perdería y solo después se permite. | Victor |
| 2026-09-30 | El PR recibe la extracción del DP directamente. | Victor |
| 2026-09-30 | Primero Niveles, después este plan. Este Spec reemplaza la versión anterior. | Victor |

## Enlaces a progreso y evidencia homónimos

- Progreso y evidencia: se crean al iniciar la implementación (`02-progreso/` y `03-evidencia/`, mismo nombre de archivo).

## Mejoras (de trabajo)

Ninguna todavía.

## Reglas de negocio acordadas en esta tarea

Se trasladan a su flujo al cerrar, previa consulta de cada contradicción a Victor.

- 2026-09-30 — Actividad → partida → metrado se declara en Paquetes, no en el cronograma → `15-cronograma.md` y `19-paquetes...md` (pendiente).
- 2026-09-30 — Una partida puede estar en varios paquetes; sus metrados suman el 100%; el PR la ve una sola vez → `19-paquetes...md` y `20-plan-maestro.md` (pendiente).
- 2026-09-30 — El paquete no lleva fechas; agrupa y ordena → `19-paquetes...md` (pendiente).
- 2026-09-30 — El Plan Maestro es un lienzo donde se coloca el metrado por día; se crea cuando todos los metrados están repartidos; un servicio puede no usar paquetes → `20-plan-maestro.md` (pendiente).
- 2026-09-30 — El Plan Maestro mide tres cosas separadas: avance físico (por partida), avance económico (metrado × precio unitario) y HH programadas = Σ (metrado programado × `hh_und_partida`), con la columna "HH por unidad de partida" visible → `20-plan-maestro.md` (pendiente; definición del % físico en paquetes y total según P8).
- 2026-09-30 — El RDT lista los paquetes y partidas del Plan Maestro, no las del DP; el real se atribuye al paquete × partida y el PR suma por partida → `06-rdt.md`, `18-control-avance.md` y `20-plan-maestro.md` (pendiente; Spec posterior).
- 2026-09-30 — Recargar el DP o el cronograma con datos posteriores se bloquea; se avisa qué se perdería y se exige confirmación → `09-importar-dp.md` y `15-cronograma.md` (pendiente).

## Carpetas/archivos huérfanos

- **Discrepancia verificada, reportada a Victor:** el plan `2026-09-23-paquetes-de-trabajo.md` marca PL-1.7 ("quitar Editar distribución diaria") como hecho, pero `FormularioPlanMaestro.tsx` todavía contiene ese editor (línea ~369) en `main`. No se borra nada; lo resuelve F2 de esta tarea.
- Sin otros huérfanos detectados hasta ahora.

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

- Gantt con línea base y línea real de avance: ya registrado en `planes-futuros.md` (2026-09-30).
