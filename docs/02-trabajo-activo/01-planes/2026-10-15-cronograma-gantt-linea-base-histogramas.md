# 2026-10-15 — Cronograma dentro del sistema: crear, línea base, seguimiento e histogramas

## Identificación y estado

- Tema: crear y seguir el cronograma dentro del sistema, al estilo MS Project (tabla + barras), con línea base, línea de seguimiento contra el RDT, histogramas de HH y HM, y exportación a PDF y Excel.
- Fecha de inicio: 2026-10-15.
- Estado: `Implementando`, **en pausa por orden de Victor (2026-10-16)** después de la ronda 2 de la maqueta (Gate 1 aprobado el 2026-10-15). Ver «Traspaso a la próxima sesión».

Puertas:

- Gate Spec: `aprobado por Victor (2026-10-15)`
- Gate 1: `aprobado por Victor (2026-10-15)`, con la condición de usar Haiku en las tareas simples (ver «Asignación de modelos»)
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

Verificado con `git` por el Planner el 2026-10-15 (la tabla del Orquestador estaba desactualizada: otro plan, «Informes de supervisión», ya usa las ramas 1 a 3).

- Entorno: `local`. Documentación en `main` de `pg_control_proyectos` (directo, sin rama). Código en `py_control_proyectos_web`, en ramas `local-worker-N`; nunca `main` hasta el merge tras el Gate 2.
- Pool real hoy (`git worktree list`, `git status`, `git rev-list` en la app):

| Rama | Estado verificado | Uso para este plan |
|---|---|---|
| `local-worker-1` | 4 commits propios, sin mergear (tanda B de Informes: migración 098) y carpeta `src/lib/informes/` sin seguimiento | No se toca |
| `local-worker-2` | 4 commits propios, sin mergear (tanda N de Informes: migración 101) y 6 archivos modificados | No se toca (el dato «libre» era viejo) |
| `local-worker-3` | Igual a `main`, pero con 5 archivos modificados y la migración 100 sin seguimiento (tandas O/R de Informes) | No se toca (el dato «libre» era viejo) |
| `local-worker-4` | Limpia, sin commits propios, 14 commits atrás de `main`; la reservaba Informes pero su Plan asigna W1 a W3 | **Libre: Worker CR-1** (se actualiza con `main`) |
| `local-worker-5` | 4 commits propios sin mergear, 41 atrás | No se toca |
| `plan-maestro-tres-paneles` | Sin mergear | No es de este plan |

- **Worker CR-1** (línea principal: motor, editor, Gantt, creación, línea base, seguimiento, exportar, permisos): `local-worker-4`, carpeta `.worktrees/local-worker-4`, con `git merge main` al empezar.
- **Worker CR-2** (APU por partida e histogramas): **no hay otra rama limpia**, así que Victor autorizó el 2026-10-15 (P1) crear la rama y carpeta nuevas `local-worker-6` desde `main` y actualizar `local-worker-4` con `main`.
- Puerto de desarrollo: uno por carpeta, que fija el Orquestador al lanzar (por confirmar el número libre).
- Migraciones: **la 102 ya la usa el plan de Informes** (tanda R). Este plan usa desde la **103**: CR-1 = 103 a 106; CR-2 = 107. El Worker vuelve a mirar `ls db/` y `git log` antes de escribir cada archivo.
- Orden de merge a `main` (paso 16a): primero CR-2 (si existe), luego CR-1; el Worker git incorpora `local-worker-6` en `local-worker-4` antes de la tanda C9. Choques esperables y su dueño: `src/lib/permisos/permisos.ts` (el plan de Informes edita el mismo archivo con W1: la tanda C10 va después de que él mergee o resuelve el choque trivial), `db/README.md` (cada Worker agrega solo su línea) y `src/lib/config/registro-accesos.ts` (este plan no lo toca: el chip Cronograma ya existe).

## Skills aplicables

- `seguir-flujo-de-planes`: Orquestador, al activar y antes de cerrar.
- `cerrar-tanda`: cada Worker, al terminar su tanda.
- `verificar-permisos-por-rol`: tanda C10 y verificación C12.
- `trasladar-hallazgos`: Documentador, tanda C11.
- `dataviz` (del entorno): lo consulta el Worker de la maqueta (C0) y de histogramas (C8) para las reglas de color, leyenda y eje de los gráficos, sin dependencias nuevas.
- Herramientas de navegador (Playwright): tanda C12 y las autoverificaciones de interfaz, con las dos cuentas de prueba de la memoria del Orquestador.

## Fases y dependencias

| Fase | Contenido | Tanda(s) | Depende de |
|---|---|---|---|
| F0 | Maqueta HTML aprobada por Victor | C0 | Gate 1 |
| F1 | Motor de programación (4 vínculos, calendario, ciclos, resumen) y datos (migración 103) | C1 | F0 |
| F2 | API de edición, editor tabla, Gantt, tres puertas de creación | C2, C3, C4 | C1 |
| F3 | Línea base dentro de la aprobación (104, 105) y seguimiento RDT/manual (106) | C5, C6 | C4 (necesita actividades en el editor) |
| F4 | APU por partida (107) e histogramas | C7, C8 | C7 libre; C8 necesita el calendario de C1 |
| F5 | Exportar PDF y Excel | C9 | C6 y C8 |
| F6 | Permisos, validación final | C10 | C2 a C9 |
| Doc | Flujos 09, 14, 15, 16, 18, 20, `design.md`, artefacto «Matriz de permisos» | C11 | C10 |
| Verif | Verificación en vivo en PS-0000 y los 12 criterios | C12 | C11 |

Olas: **ola 0** C0 (CR-1) y Gate de la maqueta; **ola 1** C1 (CR-1) en paralelo con C7 (CR-2); **ola 2** C2, C3, C4 (CR-1) en paralelo con C8 (CR-2, tras incorporar C1); **ola 3** C5, C6 (CR-1); **ola 4** C9, C10 (CR-1); **ola 5** C11 (Documentador) y C12. Camino crítico: C0 → C1 → C2 → C3 → C4 → C5 → C6 → C9 → C10 → C11 → C12. Independencia real de archivos entre carriles: CR-2 toca solo `src/lib/dp/**`, `src/app/api/dp/**` (importación), `db/107*`, `src/lib/cronograma/histograma*.ts` y `src/components/cronograma/Histogramas*`; CR-1 no toca esas rutas salvo C9, que importa los datos del histograma sin editarlos.

## Equipo del plan

Orquestador (punto único con Victor), Planner (este plan, ya terminó), Worker CR-1, Worker CR-2, Documentador (tanda C11), Worker git (merges entre ramas de trabajo, `git merge main` al empezar, incorporar CR-2 en CR-1), Auditor (informe en `04-auditoria/`). Sin Opus. Esfuerzo Medio en todas las fases; ninguna requiere esfuerzo Alto ni nivel 5.

**Cuántos agentes y cuáles (respuesta a Victor, 2026-10-15):** 12 sesiones de Worker de código (una por tanda: C0 a C10 y C12), 1 Documentador (C11), 1 Worker git (varias ejecuciones cortas) y 1 Auditor; como mucho dos sesiones de código a la vez, una por carril. **Haiku** (pedido de Victor para tareas simples): C0 maqueta, C4 tres puertas, C11 documentación, Worker git y las búsquedas y mediciones mecánicas del Orquestador. **Sonnet** el resto, porque tocan lógica, dinero del avance o seguridad. Si una tanda en Haiku no logra cerrar, se suspende y se le pide a Victor aprobar Sonnet para repetirla (cambio de nivel durante la ejecución, regla de `seguir-flujo-de-planes`).

### Asignación de modelos y esfuerzos por fase

| Tanda / fase | Worker | Nivel de consumo (`10-niveles`) y agente | Modelo Claude | Esfuerzo | Por qué |
|---|---|---|---|---|---|
| C0 maqueta (F0) | CR-1 | 2 (`n2`) | **Haiku** | Medio | HTML estático con brief cerrado, partiendo de dos maquetas existentes; Victor la revisa antes de C1, así que un error se detecta barato |
| C1 motor y datos (F1) | CR-1 | 3 (`n3`) | Sonnet | Medio | Lógica nueva con muchos casos (cuatro vínculos, desfase negativo, ciclos) y una migración aditiva |
| C2 API y editor tabla | CR-1 | 3 (`n3`) | Sonnet | Medio | Varios archivos, validación de servidor y componente grande |
| C3 Gantt | CR-1 | 3 (`n3`) | Sonnet | Medio | SVG a mano con arrastre y teclado, sin librería |
| C4 tres puertas | CR-1 | 2 (`n2`) | **Haiku** | Medio | Reutiliza parsers y niveles existentes; brief cerrado. Si no cierra, se pide a Victor aprobar Sonnet |
| C5 línea base | CR-1 | 3 (`n3`), aprobado por Victor (P5) | Sonnet | Medio | Reescribe la función de aprobación (todo o nada); la prueba de atomicidad cubre el riesgo |
| C6 seguimiento | CR-1 | 3 (`n3`) | Sonnet | Medio | Regla nueva con cruce contra la Curva S |
| C7 APU por partida | CR-2 | 3 (`n3`) | Sonnet | Medio | Parser y datos de cuadrilla por partida; migración aditiva |
| C8 histogramas | CR-2 | 2 (`n2`) | Sonnet | Medio | Cálculo y gráficos con brief cerrado |
| C9 exportar | CR-1 | 2 (`n2`) | Sonnet | Medio | `pdfkit` y `exceljs` ya existen; patrón en `src/lib/pdf/hoja.ts` |
| C10 permisos y validación | CR-1 | 2 (`n2`) | Sonnet | Medio | Funciones de permiso y pruebas contra el flujo 14 |
| C11 documentación | Documentador | 0 o 1 (`n0`/`n1`) | Haiku | Medio | Traslado de reglas ya acordadas |
| C12 verificación en vivo | CR-1 (o Worker nuevo) | 2 (`n2`) | Sonnet | Medio | Protocolo aprobado con Playwright |
| Worker git | Worker git | 0 o 1 | **Haiku** | Medio | `git merge main`, incorporar `local-worker-6` en `local-worker-4`, crear la carpeta de trabajo: mecánico |
| Auditor | Auditor | 0 o 1 | Sonnet | Medio | Revisión de solo lectura |

Los niveles de partida salen de `10-niveles-de-modelos.md`; el benchmark por nivel (Política 2) no se corre porque las tareas se parecen a las ya medidas (Lote 3). Las tablas de «Registro de cambios de nivel» y «Esfuerzos reales usados» se llenan al ejecutar.

## Archivos / componentes afectados

Rutas verificadas con `ls` en la app el 2026-10-15. «Nuevo» = no existe hoy; el nombre es propuesta del Planner y el Worker puede ajustarlo si lo anota en su resumen.

**Existen y se tocan:**
- `src/app/api/cronograma/route.ts` (615 líneas: GET, PATCH de vínculos, POST de carga; llama `recalcular_pr_fechas_base`), `src/app/api/cronograma/hitos/route.ts`, `src/app/api/cronograma/plantilla/route.ts`.
- `src/app/(workspace)/cronograma/page.tsx` (hoy solo cabecera «Fase 1» y `FormularioCronograma`).
- `src/components/ui/FormularioCronograma.tsx` (carga e informe actuales; pasa a ser la «puerta archivo»).
- `src/lib/cronograma/` (`parser-excel.ts`, `parser-pdf.ts`, `informe.ts`, `niveles.ts`, `vinculos.ts`, `tipos.ts`): se extiende `tipos.ts` y los parsers para devolver predecesoras estructuradas.
- `src/components/ui/PersonalizarCampos.tsx` (se reutiliza, no se edita).
- `src/lib/permisos/permisos.ts` (ya trae `puedeVerCronograma`, `puedeSubirCronograma`, `puedeDescargarPlantillaCronograma`).
- `src/lib/dp/parser-apu.ts` (272 líneas, calcula HH por partida), importación del DP bajo `src/app/api/dp/**` y `src/lib/dp/**` (por confirmar el archivo exacto de la ruta de importación en C7).
- `db/094_aprobar_plan_maestro_reposicion_determinista.sql` (función `aprobar_plan_maestro_con_reposicionamiento(uuid, uuid, jsonb)`; no se edita: se crea una versión nueva con `create or replace` en la 105) y `src/lib/proyectos/plan-maestro-aprobado.ts` (solo lee; la tabla es `proyecto_plan_maestro`).
- `src/lib/curva-s/curva-s.ts` (solo se lee para reusar el método de avance físico; no se edita).
- `src/lib/pdf/hoja.ts` (otro plan prohíbe editarlo: se importa; lo nuevo va en archivos nuevos).
- `db/README.md` (una línea por migración).
- En este repositorio: `docs/05-diseno-y-referencias/mockups/` (maqueta nueva + enlace en `index.html` y `README.md`, que hoy están modificados sin commit por el Orquestador), `design.md`, flujos 09, 14, 15, 16, 18, 20 (Documentador), `planes-futuros.md` (marcar «promovido»).

**No existen y se crean (propuesta):**
- `docs/05-diseno-y-referencias/mockups/cronograma-editor-gantt.html`.
- `db/103_cronograma_programacion.sql` (`cronograma_dependencias`, `servicio_calendario`, columnas `fijada_a_mano` y `origen` en `cronograma_actividades`), `db/104_cronograma_lineas_base.sql`, `db/105_aprobar_plan_maestro_con_linea_base.sql`, `db/106_cronograma_seguimiento.sql`, `db/107_dp_partida_recursos.sql`.
- `src/lib/cronograma/calendario.ts`, `predecesoras.ts`, `programacion.ts`, `ciclos.ts` (o dentro de `programacion.ts`), `edt.ts`, `seguimiento.ts`, `linea-base.ts`, `histograma.ts`, `exportar-pdf.ts`, `exportar-excel.ts` y sus `.test.ts`.
- `src/components/cronograma/` (carpeta nueva): `EditorCronograma.tsx`, `TablaCronograma.tsx`, `GanttCronograma.tsx`, `Histogramas.tsx`, `PanelSeguimiento.tsx`.
- `src/app/api/cronograma/actividades/`, `.../dependencias/`, `.../calendario/`, `.../desde-dp/`, `.../linea-base/`, `.../seguimiento/`, `.../histogramas/`, `.../exportar/` (rutas nuevas bajo `/api/cronograma`).
- **Fuera de límites:** `src/lib/rdts/**` (plan de Informes), `src/lib/pr/evm.ts`, `src/lib/dashboard/**`, `src/lib/informes/**`, `db/098` a `db/102`.

## Cambios que contradicen lo escrito (para el Gate 1)

Tabla única: solo lo que contradice. Se consulta a Victor antes de editar cada flujo (el Documentador edita en C11, con la respuesta ya registrada).

| # | Documento | Dice hoy | Pasaría a decir |
|---|---|---|---|
| 1 | Flujo 15, párrafo «El cronograma solo carga y muestra» | El cronograma solo carga y muestra | Se crea (DP, archivo o a mano), se edita hasta aprobar el Plan Maestro y lleva seguimiento |
| 2 | Flujo 15, «Predecesoras/sucesoras son informativas» | Informativas | En modo automático determinan las fechas (FC, CC, FF, CF con desfase); en la carga de archivo se respetan las fechas del archivo |
| 3 | Flujo 15, «Pendiente (fase 2)» | Interfaz Gantt no construida | Gantt construido; se retira de pendientes |
| 4 | Flujo 15 («queda congelado») y flujo 20 §6 / línea 38 («lo único editable es el propio Plan Maestro») | Con Plan Maestro aprobado nada del cronograma se edita | Lo único editable de **planeación** es el Plan Maestro; el **seguimiento** es ejecución y sí se edita |
| 5 | Flujo 20 §3 | Aprobación todo o nada: Plan Maestro, reposicionamiento, recálculo del PR | Suma, en la misma transacción, el guardado de la línea base |
| 6 | AGENTS.md y flujos 18 y 20 | No se declara avance real sin fuente validada | El avance manual del seguimiento no alimenta PR, Dashboard ni Curva S; se rotula «Manual» (D1) |
| 7 | Flujo 20, diagrama de línea 52 | «Cronograma cargado (… solo carga y vista)» | «Cronograma creado o cargado (editable hasta aprobar)» |
| 8 | Flujo 15, «Hitos»: el hito es una `TAREA` con `requiere_partidas = false`, declarado en Paquetes | El hito se marca en Paquetes y no en el cronograma | **Respondida por Victor (2026-10-15):** el tipo Hito del editor (duración 0, rombo) es la fuente; Paquetes solo lo muestra atenuado, de solo lectura, con «◆ Hito», y ya no se marca desde Paquetes. Cómo tratar los hitos ya marcados lo confirma el Worker de C2 (CG-26) |
| 9 | Flujo 15, «Un cronograma por servicio; volver a subirlo lo reemplaza completo» y flujo 14 nota 8 | El aviso de pérdida habla de vínculos, paquetes y borrador del Plan Maestro | **Respondida por Victor (2026-10-15):** el aviso incluye también lo editado en el cronograma y su seguimiento; crear desde el DP sobre un cronograma con actividades también reemplaza, con aviso de lo que se pierde, y queda bloqueado con el Plan Maestro aprobado |
| 10 | Flujo 15, «Relación con Paquetes» (agregada por el Orquestador al revisar; el Planner no leyó el flujo completo) | «El cronograma conserva siempre las fechas del archivo original cargado» | El cronograma conserva las fechas de la planeación (las del archivo si se cargó, o las calculadas si se creó o editó) y, aprobado el Plan Maestro, su línea base; el seguimiento tiene fechas propias; ni Paquetes ni el seguimiento modifican la planeación |

**Se actualizan sin contradicción:** flujo 09 (HH por cargo y HM por equipo por partida), flujo 14 (filas nuevas de crear/editar cronograma, editar seguimiento, histogramas y exportar; nota 8) y el artefacto «Matriz de permisos», flujo 16 (el chip Cronograma gana acciones internas; sin chip nuevo), flujo 18 (cadena e histogramas), flujo 19 (no cambia: sus vínculos siguen en Paquetes; solo se revisa la referencia a fechas), flujo 21 (se cita el método de avance físico compartido), `design.md` (Gantt e histogramas), `planes-futuros.md`.

## Pedido consolidado para el Gate 1

1. **Datos de prueba:** servicio PS-0000 del Portafolio Practica con DP aprobado y APU cargado (los servicios con DP congelado no traen HM por partida hasta recargar el DP: se necesita uno con DP recargado, o permiso para recargarlo ahí); los tres archivos de `docs/06-material-de-apoyo/Informacion para pruebas/`; un servicio con Plan Maestro aprobado y RDT validados para el seguimiento (por confirmar si PS-0000 los tiene) y otro sin Plan Maestro.
2. **Preautorizaciones:** inicio de sesión con las dos cuentas de prueba (las maneja el Orquestador; nunca se leen ni se muestran) y las herramientas de navegador (Playwright) para las verificaciones de C12 y las autoverificaciones.
3. **Ramas y carpetas:** `local-worker-4` (actualizar con `main`) y `local-worker-6` creada desde `main` con su carpeta (autorizado por Victor, 2026-10-15). No se tocan 1, 2, 3 ni 5. El Worker git incorpora `local-worker-6` en `local-worker-4` antes de C9.
4. **Migraciones:** 103 a 106 (CR-1) y 107 (CR-2). Las prepara el Worker, las aplica Victor (o el Orquestador con su autorización y el verificador) una por una, nada se aplica en este paso. Orden: 103 antes de C1, 104 y 105 antes de la verificación de C5, 106 antes de C6, 107 antes de C8.
5. **Modelos y esfuerzos:** tabla de arriba; todo en esfuerzo Medio y sin nivel 5; C5 en nivel 3 (P5 resuelta); Haiku en las tareas simples por pedido de Victor.
6. **Maqueta:** el Gate de la maqueta (Victor aprueba C0) es una puerta intermedia obligatoria antes de C1.

## Punch List embebida

> Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia de cada ítem va en el archivo de evidencia homónimo. «CA» = criterio de aceptación del Spec. Un ítem dice qué se verifica y cómo.

### Estado de aprobación

Gate 1: aprobado por Victor el 2026-10-15 (lista de ítems, tabla de contradicciones, ramas, modelos y orden de migraciones).

### Ítems funcionales

| ID | Tanda | Qué se verifica y cómo | CA | Estado |
|---|---|---|---|---|
| CG-01 | C0 | Maqueta HTML de tres paneles con tabla y Gantt (barra base, barra de seguimiento con %, resumen, hito, flechas, línea «hoy», leyenda); abre sin errores de consola | 10 | Conforme (Orquestador: revisó en pantalla la versión de la ronda 2 a 1440 y 1873 px, 0 errores de consola; Comienzo y Fin visibles) |
| CG-02 | C0 | Maqueta de los cuatro estados (vacío, cargando, error, datos) y de las tres puertas de creación | 10 | Conforme (verificado por el Worker por DOM y capturas; el Orquestador no repitió este ítem) |
| CG-03 | C0 | Maqueta de la pestaña Histogramas (barras HH/HM, acumulado, pico, filtros, rótulo de fuente programado/estimado) | 7 | Conforme (Orquestador: revisó el caso de Victor, Operario + Retroexcavadora a 1873 px con paneles ocultos: leyenda, ejes con unidad, semanas y pico a la vista) |
| CG-04 | C0 | Maqueta del interruptor modo RDT / manual, etiqueta «Manual», historial y selector de línea base | 5 | Conforme (verificado por el Worker por DOM y capturas; el Orquestador no repitió este ítem) |
| CG-05 | C0 | Maqueta de las opciones de exportar y de la vista móvil de solo lectura; enlazada en `mockups/index.html` y `README.md` | 8, 10 | Observado (maqueta y vista móvil hechas y verificadas por el Worker; las entradas en `mockups/index.html` y `README.md` existen en el disco pero esos dos archivos tienen cambios sin commit de otros planes, así que no se subieron) |
| CG-06 | C0 | **Victor aprueba la maqueta** (puerta intermedia; sin esto no empieza C1) | — | Sin verificar (entregada la ronda 2 el 2026-10-16; falta que Victor la abra y responda las dudas de «Preguntas pendientes de la maqueta») |
| CG-10 | C1 | Migración 103 escrita, aditiva, con reversa documentada y RLS; no se aplica | 1 | Sin verificar |
| CG-11 | C1 | `calendario.ts`: sumar y restar días laborables de lunes a sábado saltando los no laborables; prueba `vitest` con los 12 días del 6 al 19/08 del PDF de referencia | 1 | Sin verificar |
| CG-12 | C1 | `predecesoras.ts`: lee `5`, `5FC+2`, `5CC`, `5FF-1`, `5CF` y rechaza lo ilegible con motivo; `vitest` | 1, 3 | Sin verificar |
| CG-13 | C1 | `programacion.ts`: los cuatro vínculos con desfase positivo y negativo calculan la fecha correcta; actividad fijada a mano no se mueve; `vitest` por cada tipo | 1 | Sin verificar |
| CG-14 | C1 | Un ciclo se rechaza con el motivo (cadena de actividades); `vitest` | 1 | Sin verificar |
| CG-15 | C1 | Resumen: comienzo = el menor de sus hijas, fin = el mayor, duración calculada; hito de duración 0; `vitest` | 1 | Sin verificar |
| CG-16 | C1 | EDT se numera solo según la sangría (sube, baja, inserta); `vitest` | 1 | Sin verificar |
| CG-20 | C2 | API de actividades: guarda, mueve y borra con validación en servidor (permiso, alcance al servicio, ciclo, tipo, calendario) y rechaza la planeación con Plan Maestro aprobado | 1, 9 | Sin verificar |
| CG-21 | C2 | Editor tabla con árbol de 14 px plegable y columnas Id, EDT, Nombre, Duración, Comienzo, Fin, Predecesoras, Sucesoras, % avance y variación; verificado con Playwright | 1, 10 | Sin verificar |
| CG-22 | C2 | Cambiar una duración o predecesora mueve las siguientes en la tabla y en servidor; crear 15 actividades en 3 niveles desde cero | 1 | Sin verificar |
| CG-23 | C2 | Borrador con guardado parcial; recargar la página conserva lo guardado | 10 | Sin verificar |
| CG-24 | C2 | «Personalizar campos» (componente existente) y virtualización de filas desde 60 filas | 10 | Sin verificar |
| CG-25 | C2 | Editor de calendario: lista de días no laborables que edita el planner y recalcula | 1 | Sin verificar |
| CG-26 | C2 | Hito: el tipo Hito del editor es la fuente; Paquetes lo muestra atenuado, solo lectura, con «◆ Hito»; el Worker anota cómo trata los hitos ya marcados | 1, 5 | Sin verificar |
| CG-30 | C3 | Gantt SVG: escalas día, semana (sábado a viernes) y mes | 10 | Sin verificar |
| CG-31 | C3 | Barras de tarea, resumen (negro con corchetes) e hitos (rombo) con tokens de `design.md`, no solo color | 8, 10 | Sin verificar |
| CG-32 | C3 | Flechas de dependencia de los cuatro tipos en el Gantt | 1, 8 | Sin verificar |
| CG-33 | C3 | Línea «hoy» punteada con su fecha y leyenda siempre visible | 8, 10 | Sin verificar |
| CG-34 | C3 | Arrastrar mueve o estira una barra, actualiza la tabla y marca la actividad «fijada a mano» | 1, 10 | Sin verificar |
| CG-35 | C3 | Todo lo del arrastre se hace con teclado y escribiendo en la tabla | 10 | Sin verificar |
| CG-36 | C3 | Tres paneles ocultables y desplazamiento vertical sincronizado; móvil en solo lectura | 10 | Sin verificar |
| CG-40 | C4 | Puerta «Desde el DP»: una tarea por partida, actividades por nivel, enlace por WBS hecho en PS-0000 | 2 | Sin verificar |
| CG-41 | C4 | Puerta «Desde archivo»: los tres archivos de prueba abren en el editor y sus fechas quedan fijadas | 3 | Sin verificar |
| CG-42 | C4 | Predecesoras legibles del archivo quedan estructuradas; las ilegibles se informan; aviso si las fechas difieren del cálculo | 3 | Sin verificar |
| CG-43 | C4 | Puerta «A mano»: tabla vacía y numeración de EDT según sangría | 1 | Sin verificar |
| CG-44 | C4 | Un cronograma por servicio: avisar lo que se perdería al reemplazar (incluye lo editado), también al crear desde el DP, y bloquear con Plan Maestro aprobado | 2, 3 | Sin verificar |
| CG-50 | C5 | Migraciones 104 (tablas de línea base) y 105 (función de aprobación nueva) escritas, aditivas, con reversa; no se aplican | 4 | Sin verificar |
| CG-51 | C5 | Al aprobar el Plan Maestro se crea la v1 con comienzo, fin y duración congelados, en la misma transacción | 4 | Sin verificar |
| CG-52 | C5 | Prueba de atomicidad: si falla la línea base (o el reposicionamiento), no queda aprobado nada | 4 | Sin verificar |
| CG-53 | C5 | Una versión nueva aprobada crea la v2 y la v1 sigue consultable; selector de línea base y variación de fin en la tabla | 4 | Sin verificar |
| CG-54 | C5 | Antes de aprobar no hay línea base ni seguimiento (tampoco RDT) | 4 | Sin verificar |
| CG-55 | C5 | Primera acción: confirmar con `plan-maestro-aprobado.ts` y la función 094 cómo se crea y aprueba una versión nueva; resultado a su resumen | 4 | Sin verificar |
| CG-60 | C6 | Migración 106: seguimiento (modo, comienzo, fin, %) e historial de cambios; no se aplica | 5 | Sin verificar |
| CG-61 | C6 | Modo RDT: comienzo, fin y % salen de los RDT validados (solo lectura) con la regla del Spec; `vitest` con el método de la Curva S | 5 | Sin verificar |
| CG-62 | C6 | Interruptor modo RDT / manual: en manual los RDT nuevos no cambian los valores y la fila dice «Manual»; volver a RDT pide confirmación, recalcula y deja historial (quién, cuándo, qué valores) | 5 | Sin verificar |
| CG-63 | C6 | Hito o actividad sin partidas: solo manual, interruptor RDT deshabilitado con el motivo | 5 | Sin verificar |
| CG-64 | C6 | La fila «Proyecto» en modo RDT muestra el mismo % físico que la Curva S del mismo corte (prueba cruzada) | 5, 6 | Sin verificar |
| CG-65 | C6 | PR, Dashboard y Curva S iguales antes y después de editar avance manual | 6 | Sin verificar |
| CG-66 | C6 | El seguimiento se edita con el Plan Maestro aprobado y el servidor lo valida (rol, servicio) | 5, 9 | Sin verificar |
| CG-70 | C7 | Migración 107 `dp_partida_recursos` (cargo HH por unidad, equipo HM por unidad); no se aplica | 7 | Observado (escrita y revisada por el Orquestador; no se ejecutó en ningún motor SQL: la aplica y verifica Victor; commit ea55445 en `local-worker-6`) |
| CG-71 | C7 | `parser-apu.ts` devuelve por partida el consumo de cada cargo y equipo; la suma de HH por partida = `hh_und_partida` (`vitest` con APU de prueba) | 7 | Conforme (Orquestador: `vitest src/lib/dp` 17 archivos y 125 pruebas en verde, `tsc` sin errores; el Worker cruzó 3 presupuestos reales con diferencia 0; commit fad38d4) |
| CG-72 | C7 | La importación del DP guarda esos datos; sin cambios en el resto de la importación (regresión) | 7 | Observado (código y pruebas en verde, commit 5de578e; falta la prueba contra la base real, que exige aplicar la 107 y la hace C12 o Victor) |
| CG-73 | C7 | Evaluar volver a leer el APU guardado de un DP aprobado, sin cambiarlo, solo para completar HM; decisión escrita en el resumen (o «no hay archivo guardado») | 7 | Conforme (decisión escrita en `resultados/C7.md`: es viable releer el archivo guardado; no se implementa, queda como postergado) |
| CG-74 | C7 | Servicios sin HM por partida muestran «sin dato» y no cero | 7 | Conforme (contrato de lectura listo, devuelve nulo = «sin dato»; la pantalla que lo pinta es de C8) |
| CG-80 | C8 | Histograma programado: metrado programado por día del Plan Maestro × tasa de la partida; `vitest` | 7 | Sin verificar |
| CG-81 | C8 | Histograma estimado sin Plan Maestro: metrado vinculado repartido parejo sobre días laborables; rótulo de la fuente | 7 | Sin verificar |
| CG-82 | C8 | Con el Plan Maestro al 100 %, Σ HH semanales programadas = HH contractual y Σ HM = HM contractual | 7 | Sin verificar |
| CG-83 | C8 | Pestaña Histogramas en SVG: barras por semana (sábado a viernes), acumulado, pico, filtro por cargo y equipo con barras apiladas, reglas de `design.md` §13 | 7, 10 | Sin verificar |
| CG-84 | C8 | Línea «Real» de HH cuando exista tareo validado; HM real apagado y rotulado hasta que exista el dato | 7 | Sin verificar |
| CG-90 | C9 | PDF apaisado con título, columnas, escala, barras base y seguimiento con %, resumen, hitos, flechas, línea «hoy», leyenda, «Fecha: dd/mm/aa» y paginación | 8 | Sin verificar |
| CG-91 | C9 | Opciones del PDF: solo base o base más seguimiento, rango de fechas y escala | 8 | Sin verificar |
| CG-92 | C9 | Excel de tres hojas: «Cronograma», «Gantt» (celdas por semana) e «Histogramas» | 8 | Sin verificar |
| CG-93 | C9 | La hoja «Cronograma» exportada se vuelve a cargar sin errores | 8 | Sin verificar |
| CG-94 | C9 | PDF comparado a mano con `CRON-PROMCOSER-AESA-001.pdf` (una captura) | 8 | Sin verificar |
| CG-100 | C10 | Funciones de permiso nuevas (crear/editar planeación, editar seguimiento, exportar) y pruebas que comparan contra el flujo 14 | 9 | Sin verificar |
| CG-101 | C10 | `verificar-permisos-por-rol`: los 13 roles ven y pueden exactamente lo de la tabla, con llamadas sin efecto | 9 | Sin verificar |
| CG-102 | C10 | El servidor valida cada escritura (permiso, servicio, tipos, límites) y no confía en el navegador | 9 | Sin verificar |
| CG-103 | C10 | `tsc`, `eslint`, `vitest` y `npm run build` en verde en la rama | 11 | Sin verificar |
| CG-110 | C11 | Flujos 09, 14, 15, 16, 18 y 20 y `design.md` actualizados con lo ya aprobado en el Gate 1 | 12 | Sin verificar |
| CG-111 | C11 | Artefacto «Matriz de permisos» actualizado a la vez que el flujo 14 | 12 | Sin verificar |
| CG-112 | C11 | `python scripts/verificar-referencias.py` sin errores; `planes-futuros.md` marca el ítem como promovido | 12 | Sin verificar |
| CG-113 | C11 | `trasladar-hallazgos`: reglas R1 a R7 y los hallazgos nuevos trasladados, sin dejar nada suelto | 12 | Sin verificar |
| CG-120 | C12 | Criterios 1 a 3 en vivo en PS-0000 (crear, programar, tres puertas) con una captura por ítem | 1–3 | Sin verificar |
| CG-121 | C12 | Criterios 4 a 6 en vivo (línea base, seguimiento, manual no cambia PR/Dashboard/Curva S) | 4–6 | Sin verificar |
| CG-122 | C12 | Criterios 7 a 8 en vivo (histogramas, PDF, Excel) | 7, 8 | Sin verificar |
| CG-123 | C12 | Criterio 10 en vivo (tres paneles, cuatro estados, teclado, móvil solo lectura) | 10 | Sin verificar |

### Datos y cálculos

Cubierto por CG-11 a CG-16, CG-61, CG-64, CG-71, CG-80 a CG-82 (cifras cruzadas contra `hh_und_partida × metrado` y contra la Curva S).

### Permisos

CG-100 a CG-102, CG-66 y CG-20.

### UI / responsive / accesibilidad

CG-01 a CG-05, CG-21, CG-30 a CG-36, CG-83 y CG-123.

### Estados vacío / carga / error

CG-02 y CG-123 (en maqueta y en vivo).

### Validación en servidor / API

CG-20, CG-44, CG-52, CG-66 y CG-102.

### Regresión

CG-65 (PR, Dashboard, Curva S sin cambios), CG-72 (importación del DP), CG-44 (carga actual), CG-103 (suite completa) y la prueba de que la carga actual del cronograma (`cronograma-get.test.ts`, parsers) sigue en verde.

**Cobertura de criterios de aceptación:** 1 → CG-11 a 16, 20 a 26, 34, 43, 120; 2 → CG-40, 44, 120; 3 → CG-41, 42, 44, 120; 4 → CG-50 a 55, 121; 5 → CG-60 a 63, 66, 121; 6 → CG-64, 65, 121; 7 → CG-70 a 84, 122; 8 → CG-90 a 94, 122; 9 → CG-100 a 102; 10 → CG-01 a 05, 21, 30 a 36, 123; 11 → CG-103; 12 → CG-110 a 113.

## Riesgos y bloqueos

Además de «Riesgos y decisiones» del Spec:

| # | Riesgo | Mitigación |
|---|---|---|
| RB1 | **Aprobación del Plan Maestro (todo o nada).** La línea base entra en una función SQL nueva (105) que reemplaza la 094; un error dejaría el servicio sin poder aprobar | Una sola tanda y un solo Worker; `create or replace` con reversa documentada; prueba de atomicidad (CG-52); la aplica Victor tras revisión y con el verificador; el Plan Maestro v1 de un servicio de prueba se aprueba antes de tocar uno real |
| RB2 | **Choque con el plan de Informes**: mismo `permisos.ts`, mismo `db/README.md`, misma numeración (la 102 es de ellos) y ramas 1 a 3 ocupadas | Este plan usa 103 en adelante, deja `permisos.ts` para C10 (al final) y trabaja en `local-worker-4`; el Orquestador resuelve el choque trivial al integrar |
| RB3 | **Tamaño y arrastre accesible** (Gantt a mano sin librería, 12 tandas) | Maqueta aprobada antes de código, tandas pequeñas, ocultar el arrastre si no hay tiempo y dejar la tabla como vía principal |
| RB4 | Dos cifras de avance (cronograma vs Curva S) | Misma función compartida y prueba cruzada CG-64 |
| RB5 | Servicios con DP congelado sin HM por partida | CG-73 evalúa releer el APU guardado; si no hay archivo, el histograma de HM dice «sin dato» |
| RB6 | Bloqueo de ramas (resuelto el 2026-10-15: Victor autorizó `local-worker-6`) | Queda como riesgo solo si la creación de la carpeta falla; en ese caso un solo Worker haría todo, más lento |
| RB7 | La nota «versión nueva del Plan Maestro» del Spec: aún no verificada en código | CG-55 es la primera acción de C5; si el flujo exige un paso más, vuelve a Victor |

## Prompt del Auditor

> Eres el Auditor del plan «Cronograma dentro del sistema: crear, línea base, seguimiento e histogramas». Solo lees; no editas código ni flujos. Entrada: el plan `2026-10-15-cronograma-gantt-linea-base-histogramas.md`, su Punch List, los resúmenes en `…-briefs/resultados/`, la evidencia y las ramas `local-worker-4` (y `local-worker-6` si existió). Verifica, con comandos y lecturas reales y sin fiarte del resumen de los Workers: (1) que cada uno de los 12 criterios de aceptación tiene su ítem en estado Conforme con evidencia que se pueda abrir; (2) trazabilidad: los flujos 09, 14, 15, 16, 18 y 20, `design.md` y el artefacto «Matriz de permisos» dicen lo mismo entre sí y con lo implementado; la tabla de contradicciones del plan se aplicó fila por fila con la respuesta de Victor; (3) que ninguna migración fue aplicada sin autorización y que la numeración 103 a 107 no pisa 098 a 102; (4) que la función de aprobación del Plan Maestro es todo o nada (revisa CG-52) y que el avance manual no llega a PR, Dashboard ni Curva S (CG-65); (5) que no hay dependencias nuevas de interfaz en `package.json`, que `src/lib/rdts/**` y `src/lib/pdf/hoja.ts` no cambiaron, y que no se leyeron ni copiaron credenciales; (6) que el libro de hallazgos está lleno y trasladado (reglas al flujo, mejoras a `03-aprendizaje-continuo`, huérfanos reportados sin borrar) y que `scripts/verificar-referencias.py` no da errores; (7) `tsc`, `eslint`, `vitest` y `npm run build` en verde. Clasifica las observaciones sobre la política para que Victor decida en el Gate 2. Escribe el informe en `docs/02-trabajo-activo/04-auditoria/2026-10-15-cronograma-gantt-linea-base-histogramas.md` con veredicto Conforme / Observado y la lista de pendientes.

## Preguntas para Victor (Gate 1) — todas respondidas el 2026-10-15

Respuestas: **P1** sí («1 ok»); **P2** sí, la maqueta es puerta obligatoria (aprobada por defecto con el Gate 1); **P3** sí, el editor es la fuente del hito; **P4** reemplaza con aviso de lo que se pierde; **P5** nivel 3 (aprobado por defecto con el Gate 1). Se conserva el texto original de las preguntas:

- **P1.** ¿Autorizas crear la rama y carpeta `local-worker-6` para el segundo Worker (APU e histogramas)? Hoy las ramas 1, 2, 3 y 5 tienen trabajo sin mergear y solo `local-worker-4` está limpia. Recomendación: sí; si no, un solo Worker hace todo y tarda más.
- **P2.** ¿La tanda de la maqueta (C0) se aprueba como puerta intermedia? Recomendación: sí.
- **P3.** Hoy el hito es una tarea marcada en Paquetes. Con el editor, ¿el tipo «Hito» del cronograma pasa a ser la fuente y la marca de Paquetes se conserva solo como lectura? Ejemplo: un hito «Entrega de planos» creado en el editor, ¿aparece ya atenuado en Paquetes? Recomendación: sí.
- **P4.** Al crear el cronograma desde el DP por segunda vez, ¿reemplaza todo lo editado (con aviso) o se bloquea si ya hay actividades? Recomendación: reemplaza con aviso, igual que la carga de archivo.
- **P5.** ¿C5 (reescribe la aprobación del Plan Maestro) se hace en nivel 3 con la prueba de atomicidad, o subes a nivel 4? Recomendación: nivel 3.

## Preguntas pendientes de la maqueta (las responde Victor al aprobarla, CG-06)

Las dejó el Worker de la ronda 2; ninguna bloquea lo ya decidido (paleta, variación en días laborables y Comienzo/Fin visibles). Con la recomendación del Orquestador:

1. **Gantt angosto con los tres paneles abiertos a 1440 px** (unos 372 px de ancho). El divisor arrastrable y ocultar un panel lo resuelven. Recomendación: aceptar.
2. **Nombre cortado con «…» en los niveles profundos.** `design.md` pide no truncar sin aprobación. Recomendación: aprobar el corte con el texto completo al pasar el cursor.
3. **HH y HM lado a lado o de uno en uno** (más altura para las barras). Recomendación: lado a lado en pantallas anchas y uno bajo el otro en las angostas.
4. **Tono nuevo `#0e1424` para las filas de resumen** (`design.md` §4.1 no admite colores nuevos sin aprobación). Recomendación: usar un token existente si hay uno cercano; si no, aprobar este.
5. **Duración y Var. fin muestran solo el número, con «d lab.» en el encabezado.** Recomendación: aceptar.

## Traspaso a la próxima sesión (pausa pedida por Victor, 2026-10-16)

- **Dónde quedó el plan:** Gate Spec y Gate 1 aprobados. Ninguna tanda en ejecución. Hechas: C7 (APU por partida, cerrada: 3 Conforme y 2 Observado) y C0 (maqueta, ronda 2 entregada y revisada por el Orquestador; CG-06 pendiente de Victor). El resto (C1 a C6, C8 a C12) sigue sin empezar.
- **Código (repositorio de la app `py_control_proyectos_web`, nada subido a `origin`):** `local-worker-6` tiene 3 commits propios (`ea55445`, `fad38d4`, `5de578e`; migración 107 sin aplicar), árbol limpio. `local-worker-4` está limpia, al día con `main` (`628918a`) y sin commits propios, con `node_modules` reinstalado. El código solo se sube tras el Gate 2.
- **Siguiente paso, en orden:** (1) Victor abre `docs/05-diseno-y-referencias/mockups/cronograma-editor-gantt.html`, responde las cinco preguntas de arriba y aprueba la maqueta. (2) El Orquestador lanza C1 (Sonnet, `local-worker-4`, puerto de desarrollo sugerido 3014) con el brief `C1-motor-de-programacion-y-datos.md`; Victor aplica la migración 103 antes de C2. (3) C8 espera a C1 y requiere aplicar la 107 antes de verificarse (puerto sugerido 3016 en `local-worker-6`).
- **Reglas de trabajo vigentes:** Haiku solo para tareas simples (git, documentación, entorno, y C4 con aviso a Victor si no cierra); cualquier subida a Sonnet la aprueba Victor y se anota en la tabla de esfuerzos; el prompt de cada Worker lista archivos y rangos de líneas a leer y lo que no (ver M3); revisar las entregas de interfaz con filtros y al ancho de Victor (~1873 px).
- **Pendientes de Victor:** aprobar la maqueta; aplicar las migraciones 103 a 107 cuando se las pida (una por una); decidir qué hacer con `.playwright-mcp/` (unas 300 entradas sin seguimiento) y con la carpeta `.worktrees/_node_modules_bloqueado_w4/`; revisar el aviso de la migración 095 (el README la lista, el archivo no existe en `main`).
- **No verificado:** el estado de los datos de prueba de PS-0000 (RDT validados y presupuesto con APU); la conexión al MCP de base de datos falló durante la sesión.
- **Reglas de negocio R1 a R10:** siguen «Registrada» en el libro de hallazgos; las traslada el Documentador en C11 (después de C10), con el artefacto «Matriz de permisos» y el flujo 14 en la misma tarea. No se editaron flujos todavía porque describirían funciones sin construir.
- **Límite de uso:** la sesión llegó una vez al límite de uso (se reinicia a las 3 a. m. hora de Lima) y cortó la ronda 2 de la maqueta; el trabajo se reanudó sin pérdidas porque el archivo no se había tocado.

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
| 2026-10-15 | **Gate 1 aprobado** (opción 1: plan, Punch List, tabla de contradicciones, ramas, modelos y orden de migraciones), con la condición de usar Haiku para las tareas simples | Victor |
| 2026-10-15 | P1: autoriza crear la rama y carpeta `local-worker-6` desde `main` y actualizar `local-worker-4` con `main` | Victor |
| 2026-10-15 | Hitos: el tipo Hito del editor es la fuente; Paquetes solo lo muestra atenuado y de solo lectura | Victor |
| 2026-10-15 | Crear desde el DP sobre un cronograma con actividades reemplaza con aviso de lo que se pierde (igual que la carga de archivo) | Victor |
| 2026-10-15 | P2 (la maqueta es puerta obligatoria antes de C1) y P5 (C5 en nivel 3 con prueba de atomicidad) quedan aprobadas por defecto con el Gate 1 | Orquestador (propuso) / Victor (aprobó el Gate 1) |
| 2026-10-15 | Haiku en C0, C4, C11, Worker git y mecánicos del Orquestador; Sonnet en el resto; si una tanda en Haiku no cierra, se suspende y se pide a Victor aprobar Sonnet | Orquestador (propuso) / Victor (pidió Haiku para tareas simples) |
| 2026-10-15 | Se agrega el ítem CG-26 (hito del editor visible en Paquetes) a la tanda C2 | Orquestador |
| 2026-10-16 | Pausa: Victor ordena terminar la ronda 2 de la maqueta, detener la implementación, entregar informe de avance y de consumo, hacer commit y cerrar sesión | Victor |
| 2026-10-15 | Maqueta, duda 1: se aprueba la paleta de series de los gráficos (azul, naranja, verde, ámbar, magenta); se anota en `design.md` §4.1 como paleta para series de gráficos | Victor |
| 2026-10-15 | Maqueta, duda 2: la variación del fin se mide en días laborables (lunes a sábado, sin los no laborables), igual que la duración | Victor («2 ok», aceptó la recomendación) |
| 2026-10-15 | Maqueta, duda 3: Comienzo y Fin quedan siempre visibles en la tabla; el resto con desplazamiento horizontal | Victor («3 ok», aceptó la recomendación) |
| 2026-10-15 | Ronda 2 de la maqueta con **Sonnet** (cambio de Haiku a Sonnet aprobado por Victor para esta tanda: «utiliza Sonnet, pero haz bien tu trabajo, delega bien, dile qué leer»); el prompt del Worker nombra los archivos y las líneas exactas que debe leer y lo que no | Victor |
| 2026-10-15 | La maqueta no se aprueba todavía: Victor pide mejorar el acabado (falta leyenda y explicación de lo que se ve, ejes sin título ni unidad); se hace una ronda 2 de la tanda C0 (ver el brief) | Victor |
| 2026-10-15 | C7: la tabla nueva `dp_partida_recursos` queda con RLS activada y sin política de lectura directa; solo se lee desde el servidor con permisos validados en código (coherente con la dirección de la 095 y la 096 y con «validar siempre en servidor») | Orquestador |
| 2026-10-15 | C7: el relleno retroactivo de HM por partida desde el archivo guardado (servicios con DP ya aprobado que no pueden recargar) NO se implementa ahora; escribiría datos en servicios reales y exige autorización de Victor. Mientras tanto esos servicios muestran «sin dato» (decisión de Victor, CG-74) | Orquestador |

## Enlaces a progreso y evidencia homónimos

Se crean al pasar a implementación (D9, Gate 1 del 2026-09-27): `02-progreso/2026-10-15-cronograma-gantt-linea-base-histogramas.md` y `03-evidencia/2026-10-15-cronograma-gantt-linea-base-histogramas.md`.

## Libro de hallazgos

Formato de cada fila: ID / Fecha / Quién (rol, tanda) / Qué / Destino propuesto / Estado / Enlace al destino.

## Mejoras (de trabajo)

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| M2 | 2026-10-15 | Worker CR-1 · C0 | El Playwright del entorno bloquea `file://` y solo guarda capturas dentro del repositorio (o de `.playwright-mcp/`). Solución: servir la carpeta con `python -I -m http.server <puerto> --bind 127.0.0.1`, y al terminar detener el servidor (en Git Bash no hay `pkill`: usar PowerShell con `Stop-Process`) | `docs/03-aprendizaje-continuo/` | Trasladada | [`2026-10-16-cronograma-entorno-windows-y-delegacion-a-workers.md`](../../03-aprendizaje-continuo/2026-10-16-cronograma-entorno-windows-y-delegacion-a-workers.md) |
| M1 | 2026-10-15 | Orquestador (Worker git) | En Windows, `npm ci` falla con EPERM al borrar `node_modules/lightningcss-win32-x64-msvc/lightningcss.win32-x64-msvc.node` cuando algún proceso mantiene abierto ese archivo (no se identificó cuál; el proceso que sospechó el Worker ya no existía). Se comprobó con `File.Open` exclusivo que seguía bloqueado. Solución que funcionó: renombrar la carpeta `node_modules` (el renombre sí se permite) a una carpeta aparte fuera del árbol de git, correr `npm ci` y reportar la carpeta sobrante sin borrarla | `docs/03-aprendizaje-continuo/` | Trasladada | [`2026-10-16-cronograma-entorno-windows-y-delegacion-a-workers.md`](../../03-aprendizaje-continuo/2026-10-16-cronograma-entorno-windows-y-delegacion-a-workers.md) |
| M3 | 2026-10-16 | Orquestador (pedido de Victor) | Delegar con lecturas exactas: el prompt de lanzamiento de un Worker lista los archivos con rangos de líneas y dice qué no leer; Haiku solo para tareas simples de brief cerrado, Sonnet cuando hay criterio visual o lógica; al revisar una interfaz, probar el caso con filtros y el ancho real de pantalla de Victor. Nació cuando el Worker Haiku de la maqueta leyó `design.md` completo (308k de contexto) y entregó un acabado básico | `docs/03-aprendizaje-continuo/` y plantilla de brief | Trasladada | [`2026-10-16-cronograma-entorno-windows-y-delegacion-a-workers.md`](../../03-aprendizaje-continuo/2026-10-16-cronograma-entorno-windows-y-delegacion-a-workers.md) |

## Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| R1 | 2026-10-15 | Orquestador (Spec) | La línea base del cronograma queda fijada al aprobar el Plan Maestro; cada versión aprobada crea una nueva y conserva las anteriores | Flujos 15 y 20 | Registrada | |
| R2 | 2026-10-15 | Orquestador (Spec) | El seguimiento por actividad es RDT por defecto y editable a mano; un interruptor devuelve a modo RDT | Flujo 15 | Registrada | |
| R3 | 2026-10-15 | Orquestador (Spec) | Las fechas del cronograma se calculan por predecesoras (cuatro tipos de vínculo, con desfase) y una actividad se puede fijar a mano | Flujo 15 | Registrada | |
| R4 | 2026-10-15 | Orquestador (Spec) | La importación del DP guarda por partida las HH por cargo y las HM por equipo (APU) | Flujo 09 | Registrada | |
| R5 | 2026-10-15 | Victor (D1) | El avance manual del seguimiento no alimenta PR, Dashboard ni Curva S; se rotula «Manual» | Flujos 15, 18 y 20 | Registrada | |
| R6 | 2026-10-15 | Victor (Gate 1) | El tipo Hito del editor del cronograma es la fuente del hito; la pantalla de Paquetes lo muestra atenuado, de solo lectura, con «◆ Hito», y ya no se marca desde Paquetes | Flujos 15 y 19 | Registrada | |
| R9 | 2026-10-15 | Victor (maqueta) | La «variación del fin» contra la línea base se mide en días laborables (lunes a sábado, sin los no laborables) | Flujos 15 y 18 | Registrada | |
| R10 | 2026-10-15 | Victor (maqueta) | Los gráficos de series (histogramas) usan la paleta validada de cinco colores (azul, naranja, verde, ámbar, magenta) como excepción a «no colores nuevos» | `design.md` §4.1 | Registrada | |
| R8 | 2026-10-15 | Orquestador (tanda C7) | Solo los equipos con unidad `HM` cuentan como horas-máquina por partida; los de unidad `HE` (aparece solo en un renglón de herramienta de la semilla 097, no en los 3 presupuestos de prueba), `%MO`, `DIA`, `MES` y `UND` no. Decidido por defecto por el Orquestador al no haber dato real que lo contradiga; se reabre si aparece un presupuesto con `HE` como hora-equipo | Flujo 09 | Registrada | |
| R7 | 2026-10-15 | Victor (Gate 1) | Crear el cronograma desde el DP sobre uno que ya tiene actividades lo reemplaza con aviso de lo que se pierde (incluye lo editado y su seguimiento); queda bloqueado con el Plan Maestro aprobado | Flujos 14 (nota 8) y 15 | Registrada | |

## Observaciones sobre la política

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| O1 | 2026-10-15 | Orquestador | `AGENTS.md` prohíbe al Orquestador hacer commit o push sin autorización, el paso 3 del flujo manda commit y push del Spec a `main`, y `02-roles-y-delegacion.md` solo lo libera dentro de lo aprobado en el Gate 1. No hay regla para el Spec previo al Gate Spec | Lista del Auditor | Registrada | |
| O3 | 2026-10-15 | Worker CR-1 · C0 | El Skill `cerrar-tanda` incluye un commit verificado, y los briefs de esta tanda prohíben el commit (lo hace el Orquestador). El estándar no dice qué hace `cerrar-tanda` cuando la tanda no commitea | Lista del Auditor | Registrada | |
| O2 | 2026-10-15 | Orquestador | El índice de `01-planes/README.md` no lista los planes `2026-10-07-plan-maestro-tres-paneles`, `2026-10-14-revision-completa-app` ni `2026-10-15-informes-supervision-y-dashboard` | Lista del Auditor | Registrada | |

## Carpetas/archivos huérfanos

- `.playwright-mcp/` (en `pg_control_proyectos`) tiene muchos archivos sin seguimiento de git (registros de consola y un PDF); se reporta a Victor, sin borrar nada.
- Inconsistencia en la app (reportada por el Worker de C7): `db/README.md` lista la migración 095, pero el archivo `db/095_cerrar_lectura_directa.sql` no existe en `main`. Se reporta a Victor; no se toca.
- `py_control_proyectos_web/.worktrees/_node_modules_bloqueado_w4/` (ignorada por git): el `node_modules` incompleto de `local-worker-4` que quedó bloqueado por Windows (ver M1). Se puede borrar cuando el archivo se libere (por ejemplo tras reiniciar); no se borra sin aprobación de Victor.

## Informe de Auditoría

Pendiente. Vivirá en `02-trabajo-activo/04-auditoria/2026-10-15-cronograma-gantt-linea-base-histogramas.md`.

## Mensaje de cierre

Pendiente.

### Tabla de esfuerzos reales usados

| Fase | Modelo asignado | Esfuerzo default | Esfuerzo usado | Cambio autorizado |
|---|---|---|---|---|
| Worker git (ramas) | Haiku | Medio | Medio | No |
| C0 maqueta | Haiku | Medio | Medio | No |
| C0 maqueta, ronda 2 | Sonnet | Medio | Medio | Sí: de Haiku a Sonnet, aprobado por Victor el 2026-10-15 |
| C7 APU por partida | Sonnet | Medio | Medio | No |

### Consumo medido por evento (`scripts/medir.py`, 2026-10-15)

Medido con `python -I scripts/medir.py --resumen --desde 2026-10-15`, que lee los registros de sesión de Claude Code. «Cache leída» es lo que más pesa; «contexto máx.» es el tamaño de la sesión y no se suma. El total de cierre se recalcula con el mismo script sobre las sesiones de este plan.

| Tanda | Modelo | Llamadas | Cache creada | Cache leída | Contexto máx. |
|---|---|---|---|---|---|
| Planner (plan por tandas) | Sonnet | 13 | 220k | 0,99M | 136k |
| Worker git · ramas del plan | Haiku | 15 | 62k | 0,76M | 62k |
| Worker git · subir el plan | Haiku | 4 | 51k | 0,14M | 51k |
| C0 maqueta (ronda 1) | Haiku | 33 | 368k | 6,44M | **308k** |
| C0 maqueta (ronda 2, con el corte por límite y la reanudación) | Sonnet | 77 | 576k | 17,00M | **317k** |
| C7 APU por partida | Sonnet | 49 | 201k | 6,71M | 201k |
| Orquestador (esta sesión, antes y después de la compactación) | Sonnet | 143 | 964k | 27,20M | 313k |
| **Total identificado de este plan al 2026-10-16** | | **334** | **≈ 2,44M** | **≈ 59,2M** | — |

Lectura: la sesión de C0 (Haiku) llegó a 308k de contexto porque leyó `design.md` completo y varias maquetas; para las tandas de Haiku siguientes, el brief debe nombrar las secciones exactas y prohibir leer el archivo entero.

## Elementos postergados propuestos para planes futuros

- Relleno retroactivo de HH por cargo y HM por equipo por partida desde el archivo del presupuesto guardado, para los servicios con DP ya aprobado que no pueden recargarlo (CG-73; escribe datos en servicios reales y exige autorización de Victor).
- Pronóstico en cascada del seguimiento (las actividades siguientes se mueven al atrasarse una).
- Ruta crítica.
