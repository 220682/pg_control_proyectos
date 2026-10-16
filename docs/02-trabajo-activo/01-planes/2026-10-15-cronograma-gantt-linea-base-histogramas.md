# 2026-10-15 — Cronograma dentro del sistema: crear, línea base, seguimiento e histogramas

## Identificación y estado

- Tema: crear y seguir el cronograma dentro del sistema, al estilo MS Project (tabla + barras), con línea base, línea de seguimiento contra el RDT, histogramas de HH y HM, y exportación a PDF y Excel.
- Fecha de inicio: 2026-10-15.
- Estado: `Planificando` (Spec aprobado; el Planner arma el plan por tandas con su Punch List para el Gate 1).

Puertas:

- Gate Spec: `aprobado por Victor (2026-10-15)`
- Gate 1: `pendiente`
- Gate 2: `pendiente`

Origen: pedido directo de Victor, 2026-10-15. Promueve el ítem «Cronograma como línea base y línea real de avance (Gantt)» de [`planes-futuros.md`](planes-futuros.md) (pospuesto el 2026-09-30); ese ítem se marca «promovido» con enlace a este plan al aprobarse el Spec.

## Referencia al Spec aprobado

El Spec está en la sección siguiente y fue aprobado por Victor el 2026-10-15 (Gate Spec), con los cambios que él pidió al aprobarlo: los cuatro tipos de vínculo entran en esta entrega. Sus decisiones constan en el Registro de decisiones y en «Riesgos y decisiones».

## Spec / SDD

### Estado

`Aprobado (Gate Spec)` — Victor, 2026-10-15.

### Problema y contexto

Hoy el cronograma solo se **carga** (Excel o PDF exportado de MS Project) y se **muestra** ([flujo 15](../../04-flujos-de-negocio/15-cronograma.md)). Si el cliente no entrega un cronograma, el servicio no puede avanzar: sin cronograma no hay vínculos en Paquetes ni Plan Maestro. Tampoco existe una vista de barras, ni línea base y seguimiento contra lo ejecutado, ni histogramas de recursos; el Gantt figura como «fase 2, no construida».

Insumos de referencia (carpeta `docs/06-material-de-apoyo/Informacion para pruebas/`):

- `CRON-PROMCOSER-AESA-001.pdf`: impresión de MS Project de 3 páginas y 77 filas. Columnas Id, EDT, Nombre de tarea, Duración, Comienzo, Fin; escala semanal; barras de tarea con avance, barras de resumen en negro, hitos con rombo, flechas de predecesoras, leyenda y pie con fecha y página. El calendario es de lunes a sábado: los «12 días» del 6 al 19/08 saltan los domingos.
- `Cron-prueba N°01.xlsx` y `Cron-servicio-marcobre 01.xlsx`: plantilla Excel de programación (Id, EDT, Descripción, Duración, Comienzo, Fin, Predecesoras, Sucesoras).

Dato verificado en el esquema (`db/004_dp.sql`): el presupuesto guarda las **HH por unidad de cada partida** (`dp_partidas.hh_und_partida`) pero **no guarda las HM por partida**; `dp_recursos` solo tiene los totales por cargo y por equipo del servicio. Sin ese dato no hay histograma de HM.

### Resultado esperado

Una pantalla amplia de **Cronograma**, con el mismo marco de tres paneles que el Plan Maestro, donde el planner:

1. **Crea** el cronograma de tres formas: desde el presupuesto (DP) del servicio, subiendo un archivo, o digitándolo a mano desde cero.
2. Lo **edita** como en MS Project: árbol con sangría, tipos Tarea / Hito / Actividad (resumen), duración, comienzo, fin y predecesoras; las fechas se calculan solas por las predecesoras y cualquier actividad se puede fijar a mano; barras que se arrastran.
3. Al aprobarse el Plan Maestro queda fijada la **línea base** (la foto que se entrega al cliente).
4. Lleva la **línea de seguimiento**: avance real contra la base, que por defecto sigue al RDT validado y que se puede tomar a mano actividad por actividad (interruptor «modo RDT / modo manual»).
5. Ve los **histogramas** de HH y de HM por semana, con acumulado, por cargo y por equipo.
6. **Exporta** PDF y Excel con la apariencia de lo que entrega MS Project, listos para reportar al cliente el avance contra la base.

### Alcance

**A. Crear el cronograma (tres puertas, un solo cronograma por servicio)**

1. **Desde el presupuesto (DP) del servicio.** Con el mapa de niveles ya confirmado, cada nivel pasa a actividad (resumen) y cada partida a una tarea con su enlace a la partida (por WBS) y su duración por escribir. No exige archivo nuevo.
2. **Desde un archivo.** Se conserva la carga actual (Excel de la plantilla y PDF de MS Project, con informe de extracción y confirmación de niveles). Cambia que el resultado se abre en el editor; las predecesoras de texto se convierten en dependencias estructuradas (con su tipo y desfase) cuando se pueden leer y las que no se informan. Las fechas del archivo se **respetan** (quedan fijadas) y la pantalla avisa si difieren de lo que calcularían las predecesoras.
3. **A mano desde cero.** Tabla vacía; el EDT se numera solo según la sangría; los niveles se asignan por profundidad y se pueden ajustar.

**B. Editor tipo MS Project**

4. Árbol con sangría de 14 px, plegable. Tipos: Tarea, Hito (duración 0, rombo) y Actividad (resumen: comienzo = el menor de sus hijas, fin = el mayor, calculados, en negro con corchetes).
5. Columnas: Id, EDT, Nombre, Duración, Comienzo, Fin, Predecesoras, Sucesoras (calculada), % avance y variación de fin contra la base (días). Columnas opcionales con «Personalizar campos» (el mismo componente de siempre).
6. **Predecesoras con cálculo automático, con los cuatro tipos de vínculo de MS Project** (decisión de Victor, 2026-10-15): fin-a-comienzo (`FC`, el que se asume si no se escribe tipo), comienzo-a-comienzo (`CC`), fin-a-fin (`FF`) y comienzo-a-fin (`CF`), cada uno con desfase en días, positivo o negativo (`5`, `5FC+2`, `5CC`, `5FF-1`, `5CF`). Se usan las siglas de MS Project en español. Al cambiar una duración o una predecesora, las siguientes se mueven. Una actividad «fijada a mano» no se mueve sola y se marca. Sin ciclos: el servidor los rechaza.
7. **Calendario del servicio:** lunes a sábado por defecto, con una lista simple de días no laborables que edita el planner.
8. **Gantt en la mitad derecha:** escala de días, semanas (sábado a viernes, igual que el Plan Maestro) o meses; barras de tarea, barras de resumen, hitos, flechas de dependencia, línea punteada de «hoy» con su fecha, leyenda siempre visible. Barras que se **mueven y se estiran con el arrastre**, siempre con la alternativa de escribir el valor en la tabla y de usar el teclado.
9. Guardado parcial en borrador, igual que el lienzo del Plan Maestro; servicios grandes con virtualización de filas desde 60 filas.

**C. Línea base**

10. Al aprobarse el Plan Maestro se guarda la línea base: copia congelada de comienzo, fin y duración de cada actividad, ligada a la versión del Plan Maestro. Cada versión nueva aprobada crea una línea base nueva y las anteriores se conservan; la pantalla muestra por defecto la vigente y permite elegir otra.
11. El guardado de la línea base va **dentro de la misma transacción** de la aprobación del Plan Maestro (todo o nada), junto con el reposicionamiento de los RDT y el recálculo del PR.
12. Antes de aprobar el Plan Maestro no hay línea base ni seguimiento (tampoco RDT); el cronograma solo se edita.

**D. Línea de seguimiento**

13. Cada actividad con partidas vinculadas lleva un seguimiento: comienzo de seguimiento, fin de seguimiento y % de avance, con un interruptor **modo RDT / modo manual**.
14. **Modo RDT (por defecto):** los tres valores salen de los RDT validados y son de solo lectura. El comienzo es el primer día con metrado validado; el % se pondera por el valor programado de sus partidas (mismo método interno que la Curva S física, [flujo 21](../../04-flujos-de-negocio/21-curva-s.md), salida en %); el fin es el último día con avance si llegó a 100 %, y mientras no llegue, la fecha de fin base o «hoy» si ya la pasó sin terminar.
15. **Modo manual:** el planner o el jefe de proyectos edita los tres valores. Mientras esté en manual, los RDT nuevos **no** lo cambian. La fila muestra la etiqueta «Manual». Volver a «modo RDT» descarta lo editado, previa confirmación, y queda en un historial (quién, cuándo, qué valores).
16. Una actividad sin partidas (hito o administrativa) no tiene fuente de RDT: solo admite modo manual, y el interruptor de RDT sale deshabilitado con el motivo.
17. La fila «Proyecto» (resumen total) en modo RDT muestra el mismo % de avance físico que la Curva S del mismo corte.
18. El seguimiento **sí** se edita con el Plan Maestro aprobado: es ejecución, no planeación.

**E. Histogramas de HH y de HM**

19. Pestaña «Histogramas» dentro de la pantalla. Por semana (sábado a viernes): barras de HH y de HM, línea de acumulado y pico, con filtro por cargo y por equipo (barras apiladas). Respeta las reglas de gráficos de `design.md` §13.
20. **Fuente:** con Plan Maestro aprobado, el metrado programado por día del Plan Maestro multiplicado por la tasa de la partida («histograma programado»). Sin Plan Maestro, el metrado vinculado de cada partida repartido parejo sobre los días laborables de su actividad («histograma estimado»). La pantalla rotula cuál de los dos está viendo.
21. **HH por cargo y HM por equipo, por partida:** la importación del DP guarda por partida el consumo de cada cargo (HH) y de cada equipo (HM) tomado del APU. Va en una tanda propia. Los servicios con DP ya aprobado quedan sin HM hasta que se recargue el DP (aceptado por Victor, 2026-10-15).
22. Cuando exista HH real validada (tareo del RDT) se superpone como línea «Real»; la superposición de HM real depende del plan «Informes de supervisión» (HM operativas del RDT) y se enciende cuando ese dato exista.

**F. Exportar**

23. **PDF** apaisado, a la manera de MS Project: título del proyecto, columnas Id / EDT / Nombre / Duración / Comienzo / Fin, escala de tiempo, barras base y de seguimiento con su % de avance, barras de resumen, hitos, flechas, línea «hoy», leyenda al pie, «Fecha: dd/mm/aa» y numeración de página. Opciones: solo base, o base más seguimiento; rango de fechas; escala.
24. **Excel** con tres hojas: «Cronograma» (misma estructura de columnas de la plantilla de carga, más las columnas de base y seguimiento, de modo que se pueda volver a cargar), «Gantt» (celdas coloreadas por semana) y «Histogramas».
25. Los dos se generan en servidor con `pdfkit` y `exceljs`, que ya son dependencias de la app.

### No alcance

- Ruta crítica, holguras y nivelación de recursos de MS Project.
- Asignar recursos a tareas, costos y datos económicos dentro del cronograma.
- Leer o escribir `.mpp` nativo ni XML de MS Project.
- Pronóstico en cascada: cuando una actividad se atrasa en el seguimiento, las siguientes **no** se mueven solas. La variación se ve por actividad.
- Restricciones de fecha de MS Project («no comenzar antes de…»), tareas inactivas, tareas divididas, calendarios por recurso.
- Plan semanal / 3WLA (sigue en `planes-futuros.md`).
- Co-edición simultánea en tiempo real; en móvil, solo lectura.
- Cambiar el Plan Maestro, el RDT, el PR o el Dashboard (excepto la transacción de aprobación del Plan Maestro, que suma el guardado de la línea base).

### Usuarios / roles afectados

Propuesta (se concreta en la tabla del flujo 14 y en el artefacto «Matriz de permisos» en la misma tarea):

| Acción | Roles propuestos |
|---|---|
| Ver cronograma, línea base, seguimiento e histogramas (no llevan datos económicos) | Los 13 roles, sin alcance por OT al leer (igual que hoy) |
| Crear y editar la planeación (desde DP, archivo o a mano), con Plan Maestro sin aprobar | Administrador, jefe de proyectos, planner (los mismos que hoy suben el cronograma) |
| Editar el seguimiento y cambiar el modo RDT / manual | Administrador, jefe de proyectos, planner |
| Exportar PDF y Excel | Los 13 roles |

### Reglas de negocio y documentos afectados

Contradicciones con lo escrito, que se consultan a Victor antes de editar el flujo (tabla definitiva en el Gate 1):

| Documento | Dice hoy | Pasaría a decir |
|---|---|---|
| Flujo 15 | «El cronograma solo carga y muestra» | El cronograma se crea, se edita (hasta aprobar el Plan Maestro) y lleva seguimiento |
| Flujo 15 | «Predecesoras/sucesoras son informativas» | En modo automático las predecesoras determinan las fechas; en la carga de archivo siguen respetando las fechas del archivo |
| Flujo 15 | «Interfaz Gantt: fase 2, no construida» | Gantt construido; se retira de pendientes |
| Flujo 20 §6 y flujo 15 | «Con Plan Maestro aprobado lo único editable es el propio Plan Maestro» | Lo único editable de **planeación** es el Plan Maestro; el **seguimiento** del cronograma es ejecución y sí se edita |
| Flujo 20 §3 | La aprobación es todo o nada: Plan Maestro → reposicionamiento → recálculo del PR | Suma, en la misma transacción, el guardado de la línea base |
| AGENTS.md y flujos 18 y 20 | No se declara avance real sin fuente validada | El avance manual del seguimiento **no** alimenta PR, Dashboard ni Curva S: se rotula «Manual» y solo se ve en el cronograma (decisión D1) |

Además se actualizan, sin contradicción: flujo 09 (la importación guarda HH por cargo y HM por equipo, por partida), flujo 14 y artefacto «Matriz de permisos» (filas nuevas), flujo 16 (el chip Cronograma pasa a tener acciones internas; no hay chip nuevo, los histogramas son una pestaña), flujo 18 (la cadena y los histogramas) y `docs/05-diseno-y-referencias/design.md` (sección del Gantt y de los histogramas).

### Datos, API, migraciones o dependencias

Propuesta; el Planner la fija. Numeración desde la `102` (la `095` queda sin aplicar y la `098` a la `101` están reservadas por el plan «Informes de supervisión»); se confirma con `git` y con la carpeta `db/` al planificar. Las migraciones las prepara el Worker y las aplica Victor, con revisión previa.

- `cronograma_dependencias`: actividad, predecesora, tipo (`FC`, `CC`, `FF`, `CF`), desfase en días (puede ser negativo).
- `servicio_calendario`: días laborables de la semana y lista de días no laborables.
- `cronograma_actividades`: columnas nuevas para «fijada a mano» y origen (archivo, DP, manual). Se conservan `predecesoras` y `sucesoras` como texto de origen.
- `cronograma_lineas_base` y `cronograma_linea_base_actividades`: la foto por versión del Plan Maestro.
- `cronograma_seguimiento` (modo, comienzo, fin, % por actividad) y su historial de cambios.
- `dp_partida_recursos`: por partida, el cargo (HH por unidad) y el equipo (HM por unidad). La suma de HH de una partida debe igualar `hh_und_partida`.
- Nueva versión de la función de aprobación del Plan Maestro (hoy `094`) que incluye la línea base.
- API (se extiende `/api/cronograma`): estado final de las actividades, desde DP, seguimiento, línea base, histogramas y exportar. Validación en servidor: permisos por rol, alcance por servicio, ciclos, tipos, calendario y bloqueo con Plan Maestro aprobado.
- **Sin dependencias nuevas de interfaz:** el Gantt y los histogramas son SVG o rejilla CSS hechos a mano, como la Curva S (`design.md` §1 y §13). Una biblioteca de Gantt requiere aprobación expresa de Victor.

### Diseño / UI aplicable

- Pantalla `/cronograma` (ya existe: selector de OT, carga e informe). Se amplía con tres paneles ocultables como el Plan Maestro ([flujo 20](../../04-flujos-de-negocio/20-plan-maestro.md), `design.md` §3 y «Lienzo del Plan Maestro»), pestañas «Cronograma | Histogramas» y la carga de archivo como una de las tres puertas de creación.
- Se reutiliza: tabla nativa con primera columna fija, árbol con sangría de 14 px, «Personalizar campos», estados vacío / cargando / error / datos, abreviaturas «Met.», «Acum.», «Prog.».
- Primera tanda: **maqueta HTML** en `docs/05-diseno-y-referencias/mockups/` (partiendo de `plan-maestro-tres-paneles.html` y `cronograma-niveles.html`), que Victor aprueba antes de escribir código.
- Colores con los tokens del sistema, no el morado de MS Project; nunca solo color (texto o icono además). Línea «hoy» punteada con su fecha. Todo lo que se hace con el arrastre se puede hacer con teclado y escribiendo en la tabla.

### Riesgos y decisiones

Decisiones confirmadas por Victor al aprobar el Spec (2026-10-15). No se vuelven a consultar:

- **D1.** El avance del modo manual **no** alimenta PR, Dashboard ni Curva S; se rotula «Manual» y vale solo para el cronograma. Así no se rompe la regla de no declarar avance sin fuente validada.
- **D2.** Con el Plan Maestro aprobado, el seguimiento se puede editar aunque la planeación esté congelada (es ejecución). Entra por defecto con la aprobación del Spec.
- **D3.** Entran **los cuatro tipos de vínculo** de MS Project en esta entrega (cambio respecto de la propuesta, que traía solo fin-a-comienzo).
- **D4.** Calendario de lunes a sábado con lista de días no laborables que edita el planner.
- **D5.** Sin cascada de pronóstico en el seguimiento (ver «No alcance»). Entra por defecto con la aprobación del Spec; queda en los postergados.

Riesgos técnicos:

- **Tamaño.** Es el plan más grande desde el de Paquetes y Plan Maestro; por eso va por tandas y con una maqueta aprobada primero.
- **Transacción de aprobación.** Tocar la función de aprobación (todo o nada) es lo más delicado; la línea base debe revertirse junto con todo si algo falla.
- **Dos cifras de avance.** El % del proyecto en el cronograma debe coincidir con la Curva S física; se verifica con una prueba.
- **Coexistencia.** El plan «Informes de supervisión» cambia el RDT (HM operativas y stand-by) y reserva migraciones; la revisión completa de la app sigue abierta. Este plan no toca `src/lib/rdts/**` ni la numeración reservada.
- **DP ya aprobado.** Sin HM por partida en los servicios con DP congelado hasta recargarlo. El Planner evalúa si conviene volver a leer el APU guardado, sin cambiar el DP, solo para completar ese dato.
- **Versión nueva del Plan Maestro.** El flujo 20 dice que es la vía para cambiar el cronograma, pero también que su edición está bloqueada con una aprobada. Se verifica en `src/lib/proyectos/plan-maestro-aprobado.ts` y se resuelve en el Plan.

### Criterios de aceptación

1. **Desde cero:** crear 15 actividades en 3 niveles con sangría; el EDT se numera solo; cambiar la duración de una mueve a sus sucesoras en calendario de lunes a sábado y saltando los días no laborables; el resumen recalcula su comienzo, fin y duración; los cuatro tipos de vínculo (`FC`, `CC`, `FF`, `CF`) con desfase positivo y negativo calculan la fecha correcta, y un ciclo se rechaza con su motivo.
2. **Desde el DP:** el servicio de prueba genera una tarea por partida con sus niveles; el enlace a la partida queda hecho.
3. **Desde archivo:** los tres archivos de prueba cargan y abren en el editor; las fechas del archivo se respetan; las predecesoras legibles quedan estructuradas.
4. **Línea base:** al aprobar el Plan Maestro se crea la v1 con las fechas congeladas; una versión nueva aprobada crea la v2 y la v1 sigue consultable; si algo falla, no queda aprobado nada.
5. **Seguimiento:** en modo RDT el % y las fechas coinciden con lo validado; en modo manual los RDT nuevos no los cambian; al volver a RDT se recalculan y queda historial; un hito solo admite manual.
6. El avance manual no cambia PR, Dashboard ni Curva S (se comprueba antes y después de editarlo).
7. **Histogramas:** con el Plan Maestro al 100 %, la suma de HH semanales programadas iguala la HH contractual del servicio, y lo mismo las HM; la fuente se rotula; la semana va de sábado a viernes.
8. **PDF:** apaisado, con columnas, escala, barras base y de seguimiento, resumen, hitos, flechas, leyenda, fecha y paginación, comparado a mano con el PDF de MS Project de referencia. **Excel:** tres hojas, y la hoja «Cronograma» se vuelve a cargar sin errores.
9. **Permisos:** cada rol ve y puede exactamente lo que dice la tabla del flujo 14, verificado con el Skill `verificar-permisos-por-rol`, y el servidor valida cada escritura.
10. **Interfaz:** tres paneles ocultables, los cuatro estados, teclado y móvil en solo lectura.
11. `tsc`, `eslint`, `vitest` y `npm run build` en verde.
12. Los flujos 09, 14, 15, 16, 18 y 20, `design.md` y el artefacto «Matriz de permisos» quedan coherentes entre sí; `scripts/verificar-referencias.py` sin errores.

### Estrategia de prueba / evidencia

- Pruebas unitarias del motor de programación (`vitest`): calendario, desfase, ciclos, resumen, fecha fijada.
- Pruebas de interfaz con Playwright en el servicio de prueba PS-0000 del Portafolio Practica, con las dos cuentas de prueba (que viven solo en la memoria del Orquestador, nunca en el repositorio). Protocolo ya aprobado: checklist antes de empezar, autoverificación del Worker y repetir hasta 100 % Completado; después revisa Victor.
- Verificación de permisos por rol con suplantación y llamadas sin efecto.
- Cifras cruzadas: histogramas contra `hh_und_partida × metrado`; % del proyecto contra la Curva S física.
- Evidencia en `03-evidencia/` y en la Punch List interactiva.

### Aprobación (Gate Spec)

- [x] Victor aprueba este Spec (incluidas D1 a D5), 2026-10-15. Autoriza subirlo a `main`.

## Objetivo, alcance y no alcance

Ver «Spec / SDD». No se duplica.

## Entorno, repositorios, ramas y worktrees

Propuesta del Orquestador, verificada con `git` el 2026-10-15; se vuelve a verificar al planificar y se autoriza en el Gate 1.

- Entorno: `local`. Documentación en `main` de `pg_control_proyectos` (directo, sin rama). Código en `py_control_proyectos_web`, en ramas `local-worker-N`, nunca `main` hasta el merge tras el Gate 2.
- Pool real:

| Rama | Estado | Situación |
|---|---|---|
| `local-worker-2` | Limpia, mergeada a `main`, 46 commits atrás | Libre; se actualiza con `main` |
| `local-worker-3` | Limpia, mergeada a `main`, 72 commits atrás | Libre; se actualiza con `main` |
| `local-worker-4` | Limpia, mergeada a `main`, 14 commits atrás | Libre; se deja para el plan de Informes |
| `local-worker-1` | 3 commits sin mergear (Dashboard, tanda A) | En uso, no se toca |
| `local-worker-5` | 4 commits sin mergear (Dashboard y Curva S) | En uso, no se toca |
| `plan-maestro-tres-paneles` | 14 commits sin mergear | No es de este plan |

- Propuesta: `local-worker-2` para el cronograma (motor, editor, línea base, seguimiento, exportar) y `local-worker-3` para el APU por partida y los histogramas. Rangos de migración separados desde la `102`. Crear, actualizar con `main` o reasignar ramas y carpetas requiere la autorización del Gate 1.

## Skills aplicables

Del repositorio (`.claude/skills/`): `seguir-flujo-de-planes` (Orquestador, al activar y antes de cerrar), `cerrar-tanda` (al terminar cada tanda), `verificar-permisos-por-rol` (tanda de permisos), `trasladar-hallazgos` (Documentador). Se completa al planificar.

## Fases y dependencias

Forma probable, a detallar por el Planner: F0 maqueta aprobada por Victor → F1 motor de programación y datos → F2 editor con las tres puertas de creación → F3 línea base y seguimiento → F4 APU por partida e histogramas (independiente de F2, candidata a otro Worker) → F5 exportar PDF y Excel → F6 permisos, flujos y matriz → Documentador → Auditoría.

## Equipo del plan

Lo propone el Planner en el paso 6 (por defecto: Orquestador, Planner, de 1 a 3 Workers de código, Documentador y Worker git; sin Opus).

## Archivos / componentes afectados

Lo completa el Planner.

## Punch List embebida

Lo completa el Planner.

## Riesgos y bloqueos

Ver «Riesgos y decisiones» del Spec.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-15 | Objetivo: cronograma creado en el sistema al estilo MS Project; tres formas de crearlo (presupuesto, archivo o a mano); interfaz amplia como la del Plan Maestro; PDF y Excel exportados similares a MS Project; línea base y línea de seguimiento para reportar al cliente; histogramas de HH y HM que nacen de lo programado en la semana, ligados a las partidas | Victor |
| 2026-10-15 | La línea base queda fijada al aprobar el Plan Maestro | Victor |
| 2026-10-15 | Seguimiento: parte de lo declarado en el RDT y es editable; interruptor «modo RDT / modo manual» para poder volver a seguir al RDT después de editar | Victor |
| 2026-10-15 | Las fechas se calculan solas por las predecesoras, con opción de fijar a mano | Victor |
| 2026-10-15 | Las HM por partida se leen del APU al importar el DP, en una tanda propia | Victor |
| 2026-10-15 | D1: el avance del modo manual no alimenta PR, Dashboard ni Curva S (queda solo en el cronograma, rotulado «Manual») | Victor |
| 2026-10-15 | D3: entran los cuatro tipos de vínculo de MS Project (fin-a-comienzo, comienzo-a-comienzo, fin-a-fin y comienzo-a-fin), cambio respecto de la propuesta | Victor |
| 2026-10-15 | D4: calendario de lunes a sábado con lista de días no laborables | Victor |
| 2026-10-15 | **Gate Spec aprobado** y autorización para subir el Spec a `main` | Victor |
| 2026-10-15 | D2 y D5 (seguimiento editable con el Plan Maestro aprobado; sin cascada de pronóstico) quedan aprobados por defecto con el Spec | Orquestador (propuso) / Victor (aprobó el Spec) |
| 2026-10-15 | Gantt e histogramas hechos a mano en SVG o rejilla CSS, sin dependencia nueva (regla de `design.md` §1 y §13) | Orquestador |
| 2026-10-15 | Calendario por defecto de lunes a sábado (deducido del PDF de MS Project de referencia); al cargar un archivo se respetan sus fechas | Orquestador |
| 2026-10-15 | El % de una actividad de resumen y del proyecto sigue el criterio de la Curva S física, para no tener dos cifras de avance | Orquestador |

## Enlaces a progreso y evidencia homónimos

Se crean al pasar a implementación (D9, Gate 1 del 2026-09-27): `02-progreso/2026-10-15-cronograma-gantt-linea-base-histogramas.md` y `03-evidencia/2026-10-15-cronograma-gantt-linea-base-histogramas.md`.

## Libro de hallazgos

Formato de cada fila: ID / Fecha / Quién (rol, tanda) / Qué / Destino propuesto / Estado / Enlace al destino.

## Mejoras (de trabajo)

Ninguna.

## Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| R1 | 2026-10-15 | Orquestador (Spec) | La línea base del cronograma queda fijada al aprobar el Plan Maestro; cada versión aprobada crea una nueva y conserva las anteriores | Flujos 15 y 20 | Registrada | |
| R2 | 2026-10-15 | Orquestador (Spec) | El seguimiento por actividad es RDT por defecto y editable a mano; un interruptor devuelve a modo RDT | Flujo 15 | Registrada | |
| R3 | 2026-10-15 | Orquestador (Spec) | Las fechas del cronograma se calculan por predecesoras (cuatro tipos de vínculo, con desfase) y una actividad se puede fijar a mano | Flujo 15 | Registrada | |
| R5 | 2026-10-15 | Victor (D1) | El avance manual del seguimiento no alimenta PR, Dashboard ni Curva S; se rotula «Manual» | Flujos 15, 18 y 20 | Registrada | |
| R4 | 2026-10-15 | Orquestador (Spec) | La importación del DP guarda por partida las HH por cargo y las HM por equipo (APU) | Flujo 09 | Registrada | |

## Observaciones sobre la política

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| O1 | 2026-10-15 | Orquestador | `AGENTS.md` prohíbe al Orquestador hacer commit o push sin autorización, el paso 3 del flujo manda commit y push del Spec a `main`, y `02-roles-y-delegacion.md` solo lo libera dentro de lo aprobado en el Gate 1. No hay regla para el Spec previo al Gate Spec | Lista del Auditor | Registrada | |
| O2 | 2026-10-15 | Orquestador | El índice de `01-planes/README.md` no lista los planes `2026-10-07-plan-maestro-tres-paneles`, `2026-10-14-revision-completa-app` ni `2026-10-15-informes-supervision-y-dashboard` | Lista del Auditor | Registrada | |

## Carpetas/archivos huérfanos

Ninguno detectado hasta ahora. `.playwright-mcp/` tiene muchos archivos sin seguimiento de git (registros de consola y un PDF); se reporta a Victor, sin borrar nada.

## Informe de Auditoría

Pendiente. Vivirá en `02-trabajo-activo/04-auditoria/2026-10-15-cronograma-gantt-linea-base-histogramas.md`.

## Mensaje de cierre

Pendiente.

### Tabla de esfuerzos reales usados

| Fase | Modelo asignado | Esfuerzo default | Esfuerzo usado | Cambio autorizado |
|---|---|---|---|---|
| | | Medio | | |

## Elementos postergados propuestos para planes futuros

- Pronóstico en cascada del seguimiento (las actividades siguientes se mueven al atrasarse una).
- Ruta crítica.
