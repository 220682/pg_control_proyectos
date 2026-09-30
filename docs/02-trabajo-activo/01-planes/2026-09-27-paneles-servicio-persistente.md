# Paneles: servicio persistente y panel izquierdo completo

## Identificación y estado

- Tema: paneles con servicio persistente y panel izquierdo completo (flujo 16).
- Fecha: 2026-09-27.
- Estado: `Pendiente del Responsable humano` — Spec/SDD aprobado en el Gate Spec (2026-09-27, con un ajuste incorporado). Plan, Punch List y análisis de decisiones abiertas redactados por el Planner (2026-09-27), listos para el Gate 1. **Versión 8 (2026-09-29):** la ejecución se reparte en tandas (un Worker por tanda; briefs, índice y medición en `2026-09-27-paneles-servicio-persistente-briefs/`); R30 y C35 resueltas.
- Entorno: `local` (verificado: sesión de Claude Code en la máquina de Victor, Windows).
- Chat del Orquestador sugerido: `local_1.orquestador_paneles-servicio-persistente` (Victor lo renombra; el agente no tiene herramienta para hacerlo).

---

# Spec/SDD

## Estado

`Aprobado (Gate Spec)` — 2026-09-27, con un ajuste: el resultado esperado 6 pasa de "deseable" a obligatorio.

## Problema y contexto

Victor reporta que al entrar a ciertas interfaces los botones de los paneles no funcionan y debe volver a otra interfaz para encontrarlos. La idea de los paneles está definida en `04-flujos-de-negocio/16-paneles.md`; lo que falta es que se cumpla en toda pantalla.

**Evidencia verificada el 2026-09-27** (servidor local de `py_control_proyectos_web`, cuenta de administrador, Playwright, solo lectura — no se modificó ningún dato ni archivo):

1. **El servicio seleccionado se pierde al cambiar de pantalla.** `WorkspaceShell.tsx` (`resolverProyectoId`, líneas 114–121) solo conserva el servicio en rutas `/proyectos/[id]/...`, y `?proyectoId=` únicamente en `/mi-entorno` y `/plan-maestro`. Sin servicio, el panel derecho dice "Selecciona un servicio para habilitar las herramientas del panel" y sus chips (Cronograma, Paquetes de Trabajo, DP, PR, Dashboard, Curva S) quedan sin enlace; el panel izquierdo deja de mostrar los accesos del servicio.
   - `/cronograma?proyectoId=<id>` y `/paquetes-trabajo?proyectoId=<id>` reciben el servicio y lo preseleccionan en su selector, pero el shell lo ignora → paneles muertos (confirmado en el navegador para Cronograma).
   - `/rdts/*`, `/requerimientos`, `/logistica/consolidado-rq`, `/notificaciones` y `/recursos/*` no llevan servicio en la URL → paneles sin servicio.
   - `/proyectos/<id>/requerimientos` redirige a `/requerimientos?ots=<id>`, y el panel pierde el servicio.
2. **Los chips del panel derecho no pasan el servicio a todas las pantallas.** `hrefItemPanel` (`nav-proyecto.ts`) agrega `?proyectoId=` solo a Cronograma, Paquetes de Trabajo, Plan Maestro, Subir RDTs y Crear RQ. Requerimiento, Consolidado RQ, Crear RDTs, Status de RDTs, Archivo de RDTs y Consolidado RDTs van sin servicio, y las pantallas de RDTs y Consolidado RQ no leen ningún parámetro de servicio.
3. **El panel izquierdo con servicio solo lo ven administrador y jefe de proyectos** (`puedeVerApartadoProyectos`; escrito en flujos 01 y 14). Los demás roles abren un servicio y su panel izquierdo no cambia.
4. **Contenido actual del panel izquierdo con servicio:** "Todos los servicios"; Recursos de empresa (Personal, Cargos, Equipos, Materiales inerte, Causas CNC); grupo "Proyecto" con Notificaciones, DP, PR, Dashboard y Curva S funcionando, y (OT) Orden de trabajo, Presupuesto, Recursos hh/hm/mat, Materiales c/c, Alcance del servicio, Personal NUEVO y Consolidado de servicio sin pantalla.
5. **Pantallas que ya existen pero no están en el panel izquierdo:** Paquetes de trabajo, Cronograma, Plan Maestro, Consolidado RDTs, Requerimientos (RQ), Crear RDT, Generar RQ (vive en Mi entorno). También existen pantallas de servicio que el flujo 16 no lista: Registro de costos, Editar servicio, Editar checklist.
6. No existe separación visual entre chips informativos y de acción.

## Resultado esperado

1. **Servicio persistente.** Una vez elegido un servicio, se conserva en todas las pantallas del workspace mediante el parámetro `?proyectoId=` en la URL (patrón que ya usan Cronograma, Paquetes de Trabajo, Plan Maestro y Mi entorno). Los tres paneles quedan activos en toda pantalla hasta que el usuario cambie de servicio o salga a "Todos los servicios".
2. **Panel izquierdo con servicio, visible para todos los roles.** Cada rol ve todos los chips del servicio; los que su permiso no autoriza se muestran **deshabilitados** (mismo patrón visual de Mi entorno: `opacity-40 cursor-not-allowed` con título explicativo), sin acceso. La validación de permisos en servidor sigue siendo la barrera real (la URL directa no evade permisos).
3. **Recursos de empresa** (catálogos corporativos: Personal, Cargos, Equipos, Causas CNC) no se reemplazan al abrir un servicio: llevan un **botón mostrar/ocultar**, disponible con o sin servicio. **Se elimina "Materiales" de esta sección** — no es un recurso de empresa.
4. **Contenido del panel izquierdo con servicio**, organizado según el flujo 16: Alcance y presupuesto (Alcance, Presupuesto, Paquetes de trabajo) · Planificación (Cronograma, Plan Maestro y lo que corresponda) · Recursos del servicio (Cargos HH, Equipos HM) · Documentación (Planos, PETS) · Reportes (Consolidado RDTs, RQ) · Acciones (Generar RQ, Crear RDT, Crear paquete). Todo chip **cuya pantalla ya existe funciona**; el que no tiene pantalla permanece visible e inerte, como hoy.
5. **Chips informativos y de acción separados visualmente**; las acciones quedan fijadas al servicio actual.
7. **Interfaz nueva = política completa por defecto (agregado por Victor tras el Gate Spec).** Toda interfaz nueva nace con toda la política de interfaces que le corresponde, sin que Victor deba indicar chip por chip "falta en este panel" o "falta en aquel". Se logra con dos piezas:
   - **Un registro único de accesos** (el "registro centralizado de chips" que el flujo 16 ya marca como pendiente). Cada acceso se declara una sola vez con sus metadatos (id, nombre, grupo, tipo informativo/acción, ruta, requiere servicio, permiso requerido, y en qué paneles es visible). De ese registro se derivan **automáticamente**: el panel izquierdo, el panel derecho, Mi entorno, el envío de `?proyectoId=`, el estado habilitado/deshabilitado por permiso y la matriz del flujo 14. Hoy son listas independientes: `NAV_PROYECTO`, `herramientasPorGrupo` (`grupo-proceso.ts`), las rutas fijas del panel izquierdo en `WorkspaceShell.tsx`, 9 excepciones por chip en `hrefItemPanel` y la tabla manual del flujo 14.
   - **Una política escrita de "interfaz nueva"** que un Worker aplica sin recordatorio. Lo que hereda toda pantalla nueva: vive dentro del shell con los tres paneles; conserva el servicio por `?proyectoId=` y lo preselecciona en su selector de OT; se registra una vez en el registro de accesos (no en cada panel); tiene tipo informativo o acción; muestra deshabilitado lo que el rol no puede usar y el servidor valida autenticación, rol y pertenencia al servicio; sale en la matriz del flujo 14; respeta `design.md`, navegación móvil y tablas con scroll horizontal; usa las fuentes únicas de estados y colores; y las notificaciones van a `/notificaciones`. Una prueba automática falla si existe una pantalla del workspace sin entrada en el registro (o sin excepción declarada).
6. **Estandarizado para todos (obligatorio):** al hacer clic en un chip del panel derecho estando dentro de un servicio, la pantalla destino abre con ese servicio ya elegido en su selector de OT. Ya existen chips que lo hacen (Cronograma, Paquetes de Trabajo, Plan Maestro, Subir RDTs, Crear RQ); el mismo comportamiento se extiende a todos los demás chips del panel derecho cuya pantalla existe (Crear RDTs, Status de RDTs, Archivo de RDTs, Consolidado RDTs, Requerimiento, Consolidado RQ, Registro de costos, etc.).
8. **Asistente disponible en toda pantalla, como icono (agregado por Victor, 2026-09-27, tras el Gate Spec).** Hoy el asistente es la barra `ChatPlaceholder` a todo el ancho al pie de la pantalla: solo aparece dentro de un servicio (`proyectoId`), solo en escritorio (`hidden … lg:block`) y además está duplicada en la pantalla del portafolio. Debe estar disponible en **todas** las interfaces y, para ganar espacio, mostrarse como un **icono**; al hacer clic recién se despliega su apariencia (el panel de conversación). Sigue siendo una vista previa sin datos: conectar el asistente a datos reales **no** entra en este plan (flujo 17: "No habilitado, sin diseño técnico").

## Alcance

- Conservar el servicio en la URL en todas las pantallas del workspace y hacer que el shell lo reconozca (`WorkspaceShell.tsx`).
- Completar el panel izquierdo con servicio según el resultado esperado 2–5.
- Añadir botón mostrar/ocultar a Recursos de empresa; quitar Materiales de esa sección.
- Que las pantallas de RDTs, Requerimientos, Consolidado RQ y las que hoy no leen el servicio lo reciban por `?proyectoId=` y lo preseleccionen, y que **todos** los chips del panel derecho con pantalla existente lo envíen (`hrefItemPanel`).
- Crear el registro único de accesos, migrar a él los chips existentes y derivar de él ambos paneles, Mi entorno y la matriz del flujo 14 (resultado esperado 7).
- Escribir la política de "interfaz nueva" en su lugar normativo (regla del sistema → flujo 16; instrucción para el Worker → `01-contexto-repositorio/05-diseno-y-ui.md`) y añadir una prueba automática que la haga cumplir.
- Mover el asistente (`ChatPlaceholder`) al shell como icono disponible en toda pantalla que despliega su panel al hacer clic, quitar la barra fija al pie y el duplicado de la pantalla del portafolio, con adaptación móvil (resultado esperado 8).
- Actualizar los flujos de negocio afectados (ver abajo) y la matriz del flujo 14.

## No alcance

- Construir las pantallas que hoy no existen (Alcance, Presupuesto, Planos, PETS, Personal NUEVO, Consolidado de servicio, 3WLA, Programación diaria, Tareo/Consolidado MOI, Status de servicios, Informe de servicio, Acta de conformidad, capacitaciones). Sus chips siguen inertes.
- Cambiar qué rol puede hacer qué (matriz del flujo 14): solo cambia **cómo se muestra** lo que un rol no puede usar (visible y deshabilitado, no oculto).
- Restricción de datos económicos por rol.
- El catálogo de Materiales.

## Usuarios / roles afectados

Los 13 roles. Cambia lo que ven administrador y jefe de proyectos (se reorganiza) y, sobre todo, los demás roles (hoy no ven nada del servicio en el panel izquierdo).

## Reglas de negocio y documentos afectados

Reglas ya escritas que esta tarea contradice o modifica — se consultan con Victor y se registran en el Registro de decisiones **antes** de editar el flujo (una fuente de verdad no se edita por cuenta del agente):

| Flujo | Regla actual | Cambio acordado (2026-09-27) |
|---|---|---|
| 16 — Paneles | Regla 2: "con servicio se muestran solo accesos autorizados". Regla 3: "un chip oculto por permisos…". | Se muestran todos; los no autorizados, visibles y deshabilitados. |
| 16 — Paneles | Panel izquierdo sin servicio = recursos corporativos; con servicio = chips del servicio. | Recursos de empresa disponibles siempre, con botón mostrar/ocultar. |
| 01 — Configuración | "Apartado Proyectos (panel izquierdo): solo administrador y jefe de proyectos". | Lo ven todos los roles; el acceso sigue el permiso. |
| 14 — Accesos y restricciones | Fila "Ver apartado Proyectos (panel izquierdo)" ✓ solo Admin y JP. | Se revisa la fila; se agrega la regla "ver ≠ acceder" para los chips del servicio. |
| 16 — Paneles | Regla 10: "cada chip nuevo debe registrarse también en el flujo 14"; "Registro centralizado de chips" figura como pendiente. | El registro pasa a ser único y es la fuente de la que se deriva el flujo 14; la política de interfaz nueva queda integrada en el flujo. |
| 14 — Accesos y restricciones | Regla: "cada vez que se agrega un chip/acceso nuevo, esta tabla debe actualizarse" (a mano). | La tabla se deriva del registro; no se mantiene una lista independiente. |
| 03, 05, 06 | Chips a pantalla completa con "Salir a Mi entorno"; chips que abren sin servicio. | Por decidir (ver decisiones pendientes). |

Flujos a leer completos por el Planner: todos (`04-flujos-de-negocio/`).

## Datos, API, migraciones o dependencias

- Sin migraciones ni cambios de base de datos.
- Repositorio de código: `py_control_proyectos_web`. Archivos previsibles: `src/components/ui/WorkspaceShell.tsx`, `src/components/ui/PanelSecciones.tsx`, `src/lib/config/nav-proyecto.ts` (+ `nav-proyecto.test.ts`), `src/lib/permisos/permisos.ts`, y las páginas `rdts/*`, `requerimientos`, `logistica/consolidado-rq`. La lista definitiva la fija el Planner.
- Regla de servidor (flujo 16): toda ruta valida autenticación, rol y pertenencia del recurso al servicio; nunca se confía solo en el `servicio_id` del navegador.

## Diseño / UI aplicable

`05-diseno-y-referencias/design.md`. Reutilizar los patrones existentes: `NAV_PROYECTO`, `GruposAccordion`, `PanelSecciones`, `WorkspaceShell`, y el estilo de chip deshabilitado de `EntornoTrabajoGrupo.tsx`. Mantener navegación móvil y tablas con scroll horizontal.

## Riesgos y decisiones pendientes

**Decisiones pendientes para el Gate Spec:**

1. **(Resuelta 2026-09-27, aprobada la recomendación)** Estado por defecto del botón mostrar/ocultar de Recursos de empresa: visible sin servicio, oculto con servicio.
2. **(Resuelta 2026-09-27, aprobada la recomendación)** PR, Dashboard y Curva S van en la sección "Reportes" del panel izquierdo.
3. Si los chips del panel **derecho** también pasan a "visible y deshabilitado" para lo no autorizado, o se mantienen como hoy.
4. Qué pasa con el chip "Salir a Mi entorno" de las pantallas a pantalla completa, ahora que los paneles permanecen activos en toda pantalla.
5. Destino de "(OT) Orden de trabajo" y "Recursos hh, hm, mat. (s/c)": la app tiene pantallas candidatas (`/proyectos/[id]`, `/proyectos/[id]/editar`, `/recursos/*`) y no se asumió cuál corresponde.
6. Dónde ubicar Registro de costos, Editar servicio y Editar checklist.
7. **(Resuelta 2026-09-27, aprobada la recomendación)** Se migran **todos** los chips existentes al registro único en esta tarea, en una fase propia del plan, antes de completar el panel izquierdo (el panel se reescribe de todos modos y dejar listas paralelas mantiene la deuda que se quiere eliminar).

**Siguen abiertas (3 a 6):** el Planner propone opciones con su análisis en el plan y Victor decide en el Gate 1.

**Riesgos:**
- Cambiar quién "ve" un chip no debe cambiar quién "puede" usarlo: la prueba debe comprobar ambos lados (ver estrategia de prueba).
- Pasar `?proyectoId=` a más pantallas puede chocar con parámetros propios de cada una (`/requerimientos` usa `?ots=`, con selección múltiple de OT).
- Tocar `WorkspaceShell.tsx` afecta a todas las pantallas del workspace.

## Criterios de aceptación

- [ ] En cada pantalla del workspace, abierto un servicio, ambos paneles muestran ese servicio y sus chips están activos; ninguna pantalla muestra "Selecciona un servicio" si hay servicio elegido.
- [ ] Cronograma, Paquetes de Trabajo, RDTs (crear, status, archivo, consolidado), Requerimientos y Consolidado RQ conservan el servicio en ambos paneles.
- [ ] El panel izquierdo con servicio es visible para los 13 roles; los chips que el rol no puede usar aparecen deshabilitados, con título, y no navegan.
- [ ] Una URL directa a una pantalla sin permiso sigue rechazada por el servidor.
- [ ] Recursos de empresa tiene botón mostrar/ocultar con y sin servicio; "Materiales" ya no aparece ahí.
- [ ] El panel izquierdo con servicio incluye todos los chips del resultado esperado 4 cuya pantalla existe, y todos funcionan.
- [ ] Informativos y acciones aparecen separados; las acciones quedan fijadas al servicio actual.
- [ ] Desde el panel derecho, dentro de un servicio, **todo** chip cuya pantalla existe abre esa pantalla con el servicio ya elegido en su selector de OT (sin excepciones).
- [ ] Existe un único registro de accesos; ambos paneles, Mi entorno, el envío de `?proyectoId=` y la matriz del flujo 14 se derivan de él (no quedan listas paralelas).
- [ ] Prueba de humo del estándar: se declara un acceso de prueba **solo en el registro** y aparece en los paneles correspondientes, con servicio persistente, permiso (habilitado/deshabilitado) y fila en la matriz, sin tocar otro archivo.
- [ ] Una prueba automática falla si hay una pantalla del workspace sin entrada en el registro ni excepción declarada.
- [ ] La política de "interfaz nueva" está escrita en el flujo 16 y en `05-diseno-y-ui.md`, y el Punch List de cualquier tarea con pantalla nueva la incluye sin que Victor la pida.
- [ ] El asistente aparece como icono en **toda** pantalla del workspace (con y sin servicio, escritorio y móvil); al hacer clic despliega su panel y al cerrarlo vuelve a ser solo el icono; ya no hay barra fija al pie ni una segunda copia en la pantalla del portafolio.
- [ ] Navegación móvil y tablas con scroll horizontal se conservan.
- [ ] Los flujos 16, 01, 14 (y 03/05/06 si aplica) quedan actualizados y coherentes con lo implementado.

## Estrategia de prueba / evidencia

Ciclo del protocolo de verificación aprobado por Victor: **checklist aprobado antes de implementar** → implementación → autoverificación del Worker con Playwright en la app real con login real → llenar el checklist → loop hasta 100% Completado → recién entonces revisión de Victor. Cada permiso se prueba **por los dos lados** con las dos cuentas de prueba (una con permisos altos y una sin permisos de administración); un permiso comprobado solo con administrador no está comprobado. Las credenciales viven fuera del repositorio y no se copian a ningún archivo. Evidencia en `02-trabajo-activo/03-evidencia/` con enlace al artifact de checklist visual si se crea.

## Aprobación (Gate Spec)

- [x] El Responsable humano aprueba este Spec/SDD (2026-09-27, con el ajuste del resultado esperado 6).

---

# Plan

## Referencia al Spec aprobado

Spec/SDD de este mismo archivo, aprobado en el Gate Spec el 2026-09-27. De las 7 decisiones de "Riesgos y decisiones pendientes", las **1, 2 y 7 quedaron resueltas** (Victor aprobó las recomendaciones). Las **3, 4, 5 y 6 siguen abiertas**: el Planner las incorpora a su plan con opciones y análisis, y Victor decide en el Gate 1.

## Objetivo, alcance y no alcance

Ver Spec/SDD arriba.

## Entorno, repositorios, ramas y worktrees

- Documentación: `pg_control_proyectos`, `main` directo.
- Código: `py_control_proyectos_web`, rama `local-worker-1`, nunca `main` hasta el Gate 2. El repositorio de la app es accesible desde esta máquina en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` (verificado 2026-09-27).
- **Modo de ejecución (Victor, 2026-09-27): todo es local.** Worker y Auditor corren como **subagentes de la sesión del Orquestador**, no como chats separados en la app. Los nombres de chat son etiquetas lógicas (`local_3.worker_paneles-servicio-persistente-fase1`, `local_4.auditor_paneles-servicio-persistente`). Un subagente no puede conversar con Victor: la excepción D6 se aplica de otra forma (ver "Prompt de cada Worker").
- **Estado verificado del repositorio de la app (versión 2 del plan, 2026-09-27, `git` y `ls` sobre `py_control_proyectos_web`, solo lectura).**
  - Rama: `local-worker-1` **ya existe**. La creó el Orquestador desde `main` (commit `1942b01`) con autorización de Victor.
  - Worktree: **`.worktrees/local-worker-1` creado el 2026-09-27** por el Orquestador, por autorización de Victor ("sigue la política, limpia ramas y renómbralas, lo mismo con los worktree"). Verificado: `git worktree list` lista el checkout principal (`main`) y `.worktrees/local-worker-1` (rama `local-worker-1`, commit `1942b01`, árbol limpio). `node_modules` del worktree es un Junction de Windows hacia el del repositorio principal (403 elementos visibles; git lo ignora). **`.env.local` copiado** el 2026-09-27 desde el checkout principal, con autorización permanente de Victor (sin leer valores; verificado idéntico; git lo ignora).
  - **Corrección a la versión anterior de este plan**, que decía que `.worktrees/` no existía: **sí existía**. Lo que había afirmado era una inferencia sin comprobar con `ls`. Tenía restos de sesiones anteriores, que el Orquestador limpió así (2026-09-27, tras inventariarlos en solo lectura): las carpetas `local-worker-1` y `work-1`, que solo contenían un enlace simbólico `node_modules`, se retiraron (se borró únicamente el enlace, sin `-r`; el `node_modules` real del repositorio principal quedó intacto: 400 paquetes antes y después); `nucleo` pasó a `hist_nucleo` y el archivo `local-worker` (806 bytes, script JavaScript que no se abrió) pasó a `hist_local-worker`. Nada con contenido se borró.
  - **Sin pendientes de entorno.** El Worker no lee ni muestra los valores de `.env.local`. Puede usar `npm run dev -- --webpack -p <puerto>` en el worktree.
  - Con `node_modules` como Junction o enlace simbólico, `npm run dev` y `npm run build` deben ir con `--webpack` (ver `01-contexto-repositorio/03-entorno-git-y-worktrees.md`). El `.env.local` del worktree ya está copiado por autorización permanente de Victor: el Worker no lo lee ni muestra sus valores y no vuelve a preguntar por copiarlo. Cualquier **otro** archivo de entorno o de secretos sí se consulta antes de tocarlo.
- Documentación: todo lo que el Worker escriba en `pg_control_proyectos` va a `main` directo (commit + push, `git add` explícito), nunca a `vpc/`.

## Resumen para el Gate 1

### Cambios de la versión 8 (2026-09-29; respecto de la versión 7, commit 6547e56)

1. **Ejecución por tandas, un Worker por tanda (sustituye a «un solo Worker, en orden»).** Un Worker con los 181 ítems no cabe en una sesión. Medición en otro plan de Victor (`hermes_agent`): un Worker de fase entera llegó a 156–191 llamadas, 625–682k tokens de contexto y 84–97M de caché; repartido en tandas, el total bajó a ~28M con contexto máximo de 186k. Aquí: **38 tandas** (F0 3, F1 2, F2 5, F2B 2, F3 3, F4 1, F4B 3, F5 1, F5B 3, F5C 4, F5D 2, F6 5, F7 4; ver «Tandas de ejecución y trazabilidad ítem → tanda»), un Worker subagente nuevo por tanda, un solo worktree (`local-worker-1`) y tandas en serie (los archivos compartidos impiden paralelizar). Cada tanda tiene un brief de ≤ 8 KB (el mayor mide 5,5 KB) en `2026-09-27-paneles-servicio-persistente-briefs/`: solo sus ítems (texto y evidencia del plan), el contrato técnico verificado en el código (archivos y funciones reales, con rutas), qué no hacer, dependencias y punto de commit. El Worker **no lee el plan completo** (Grep por ID). Reglas comunes: `00-reglas-de-contexto.md`. Metas por tanda: ≤ 80 llamadas (cierre a las ~60 con handoff), ≤ 200k de contexto, ≤ 12M de caché; línea base, script de medición y tabla de resultados: `medicion.md`. Hoja de ruta del Orquestador: `00-indice-de-tandas.md`.
2. **R30 resuelta (Victor, 2026-09-29): no se agrega alcance por OT al leer en Cronograma, Paquetes de Trabajo, RDTs ni RQ**; solo en las seis pantallas con economía (PL-174 a PL-179). **PL-181 se cierra** (`No aplica`, con la cita de la decisión) y la duda (c) desaparece.
3. **C35 resuelta (Victor, 2026-09-29):** el interruptor Parcial/Completo del Dashboard lo activan los roles con datos económicos de la matriz (`puedeVerEconomia`); que los demás roles lo vean fijo en Parcial es del plan futuro (`planes-futuros.md`). Cambian PL-90 (el interruptor sigue a `puedeVerEconomia`, con `ToggleTipoDashboard` y `PATCH …/tipo-dashboard`), la fila de `puedeAdjudicarProyecto` en «Funciones de permisos.ts que cambian» y el flujo 11 (F7-C). La duda (b) desaparece.
4. **Duda (a) anulada (Victor, 2026-09-29):** actualizar estado de RQ y subir registro de costos siguen siendo solo de logística (más administrador en el estado de RQ, ya en la tabla 2). **Siguen esperando a Victor:** las tres descargas propuestas (A12) y las cinco no listadas (A13) en el artefacto; el flujo 14 no se toca hasta entonces (PL-155, PL-156).
5. **Autonomía del Orquestador (Victor, 2026-09-29).** Lanza las tandas una tras otra y decide por su cuenta lo que pueda decidir; solo consulta a Victor por contradicciones con flujos escritos, cambios de permisos, acciones destructivas o de infraestructura no autorizadas y dudas de negocio. La lista de lo que sí decide y lo que debe escalar está en `00-indice-de-tandas.md`.
6. **Hallazgos del Planner al verificar el código para los briefs (solo lectura, 2026-09-29; `local-worker-1` = `main` `1942b01`, árbol limpio):**
   - **Ítems que piden escribir datos reales.** PL-158 a PL-162, PL-172 y los de PL-163 a PL-169 exigen «crea, edita o desactiva sin error» en Recursos de empresa, pero el método del plan (y PL-79) es solo lectura. **Pregunta para Victor (no bloquea las demás tandas):** ¿autoriza registros de prueba marcados (por ejemplo con prefijo `ZZ-PRUEBA-`) en Recursos de empresa, o se verifica solo con pruebas unitarias y llamadas sin efecto? Mientras tanto los briefs de F5D y F6-C dejan el camino feliz `Observado`.
   - **Las tablas `recursos_cargos` y `recursos_equipos` solo tienen política RLS de lectura** (`db/025_recursos_rdt.sql`); las altas de Personal ya escriben con `crearClienteAdmin()` (`src/lib/supabase/admin.ts`) tras la guardia de rol. F5D usa el mismo patrón: **sin migración**.
   - **Editar la descripción de un Cargo** puede romper referencias por texto (`recursos_personal.cargo`, equivalencias de `db/046`, tarifas y datos históricos de RDT): el brief de F5D-B pide comprobarlo antes y devolver la duda si hay riesgo.
   - **Alcance por OT en el dashboard del portafolio:** `tieneAlcanceSobreProyecto` es por servicio y un portafolio agrupa varios; el plan dice «mismo patrón» (PL-176). El brief de F5B-B propone mostrar solo las OT con alcance (administrador todas) y pide devolver la duda si no queda evidente.
   - **`local-worker-1` no tiene upstream remoto** (verificado con `git branch -vv`): el plan hablaba de «commit + push a tu rama»; los briefs commitean y no hacen push; el primer push (crea una rama remota) lo decide Victor.
   - **El `AGENTS.md` de la app (687 bytes) solo contiene el bloque de Next.js**; no existen las secciones «Code Shape Rules», «TypeScript style» ni «Testing»; el Worker lee ese archivo y `CLAUDE.md` (626 bytes) enteros.
7. **Totales:** 13 fases (sin cambio); **181 ítems** de Punch List (180 abiertos + PL-181 cerrado); 38 tandas; cobertura verificada por script el 2026-09-29: los 180 ítems abiertos asignados exactamente una vez (tabla de trazabilidad ítem → tanda); 36 contradicciones (C35 resuelta) y 7 vacíos; supuestos A1 a A13. Se conserva intacto el resto del plan (Spec, matriz, contradicciones, política de interfaz nueva).

### Cambios de la versión 7 (2026-09-28; respecto de la versión 6, commit c58323e). Superada por la versión 8 en R30, C35 y las dudas (a) a (c)

1. **Alcance por OT para leer: vacío real, ya resuelto por Victor.** El Registro de decisiones (2026-09-28, "Correcciones a la v5") ya dice: "el alcance por OT (`proyecto_miembros`) es el requisito de partida para ver cualquier interfaz orientada a un servicio, en todas las pantallas de servicio, no en ninguna". El plan decía lo contrario en dos lugares (la nota "Pertenencia al servicio" y C21, que lo dejaba como pregunta abierta). Verificado en el código, pantalla por pantalla: **Curva S ya exige** `tieneAlcanceSobreProyecto` (página) y `validarEscrituraProyecto` (API) para leer; **PR, Dashboard del servicio, Dashboard del portafolio, DP, Plan Maestro y Registro de costos no exigen nada** (ni la página ni su API). F5B pasa a incluir la guardia de alcance en las seis. Ítems nuevos PL-174 a PL-181. C21 queda **resuelta**, citando la decisión.
2. **Riesgo nuevo, no decidido por el Planner:** la frase de Victor ("todas las pantallas de servicio, no en ninguna") es más amplia que las seis pantallas con economía. Hoy Cronograma y Paquetes de Trabajo (sin economía, fase F2B) solo exigen alcance en sus **acciones de escritura**, no al **leer**; Status/Archivo/Consolidado de RDTs y Status/Consolidado de RQ ni siquiera tienen un `id` de servicio único en la URL (son listados de todos los servicios con filtro de columna). Si la regla de Victor cubre también esas pantallas, falta decidir cómo se aplica a un listado que no tiene un solo servicio activo. **No lo decido**: queda como riesgo R30 y duda nueva para Victor.
3. **Limpieza de "Dudas para Victor" (línea ~191) y del punto 1 de "Puntos que el Planner deja anotados".** Las dos ya quedaron resueltas por el Registro de decisiones antes de la v6 y yo no las había limpiado: el jefe de proyectos **ya tiene** "Subir documento del proyecto" (omisión corregida, artefacto v.19), y la frase "todas las acciones excepto dos" se retiró del flujo 14 (no hay regla general de "todo menos N"). Se reescriben para dejar solo lo genuinamente abierto: (a) si el jefe de proyectos también debe actualizar estado de RQ y subir registro de costos (hoy exclusivos de logística); (b) C35, quién alterna el Dashboard Parcial/Completo (recomendación sin confirmar: administrador y jefe de proyectos). Busqué otras referencias sueltas a "excepto dos" y "sin Subir documento": no encontré más.
4. **Totales:** 13 fases (sin cambio) y **181 ítems** de Punch List (8 nuevos: PL-174 a PL-181).

### Cambios de la versión 6

Victor aprobó en el artefacto la **gestión completa de Recursos** (Personal, Cargos, Equipos, Causas CNC), escrita en el flujo 14 (tabla 2, grupo "Recursos", nota ⁶, commit 68fc0e6). No es solo una guardia de permisos: hay que **construir pantallas que hoy no existen**.

1. **Qué ya existe (solo falta confirmar el rol, sin UI nueva):** crear Personal, crear Causa CNC, activar o desactivar Causa CNC — las tres ya funcionan en el código; el flujo 14 las decide para administrador y jefe de proyectos.
2. **Qué hay que construir (UI + API + guardia de servidor):** editar Personal existente; eliminar o desactivar Personal; crear, editar y eliminar o desactivar Cargo; crear, editar y eliminar o desactivar Equipo; editar el texto de una Causa CNC. Son **9 acciones marcadas "(por construir)"** en el flujo 14 (verificado contando las filas de esa tabla).
3. **Fase nueva F5D**, después de F5C: construye lo que falta, con una función única `puedeGestionarRecursos` (administrador y jefe de proyectos) que reemplaza el uso de `puedeVerRecursos` en el POST de Personal y con la que `puedeGestionarCatalogoCnc` pasa a delegar (mismo patrón ya usado para separar alias en F5C).
4. **Ítems nuevos PL-157 a PL-173** (17): 3 de regresión de lo que ya existe, 9 de construcción (una por acción "por construir"), y 5 de regresión de lectura y verificación por los dos lados con las dos cuentas.
5. **No cambia** qué recurso es "de empresa" (siguen siendo catálogos globales, visibles en consulta para los 13 roles desde la versión 4) ni que "Materiales" no es un recurso de empresa (ya excluido).
6. **Totales:** 13 fases (se añade F5D) y **173 ítems** de Punch List.

### Cambios de la versión 5

Victor **aprobó la matriz de permisos** (artefacto «Matriz de permisos», marcas versión 17, 2026-09-28 16:02 UTC) y el flujo 14 quedó reescrito con ella (commit 8027037). El flujo 14 es la **única fuente de permisos**: este plan lo enlaza y no copia sus tablas. Rige además la política de coherencia y trazabilidad (`AGENTS.md` y `docs/01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md`, § Políticas de coherencia y trazabilidad).

1. **CO1 a CO5 están resueltos.** Se quitan las condiciones sobre F5B y F5C y el gate por conflictos: el Worker puede ejecutar todas las fases. La sección de conflictos se reemplaza por una nota corta de cómo se resolvieron. PL-99 (gate de roles) se reescribe como referencia a la versión aprobada de la matriz.
2. **Interfaces (tabla 1): sin cambio de fondo respecto de la v4**, pero el conjunto de economía suma al **jefe de costos**: `puedeVerEconomia` = administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos; con dos excepciones acotadas: el planner ve el Plan Maestro y el supervisor de oficina técnica ve el DP. Lo demás lo ven los 13 roles.
3. **Acciones (tabla 2): cambian varias respecto de la v4 y del código.** F5C se reescribe con la lista completa de funciones de `permisos.ts` que cambian, incluidas cuatro funciones que hoy comparten alias y hay que separar (`puedeEditarServicio`, `puedeImportarDp`, `puedeCorregirRdt`, `puedeRechazarRdtValidado`) y la descarga del consolidado RQ, que se desacopla de "ver". Ítems de Punch List por acción que cambia de permiso (PL-128 a PL-145), probados por ambos lados.
4. **Más contradicciones con flujos.** Darle al jefe de proyectos los borrados definitivos y quitarle al jefe de oficina técnica el ciclo de vida del proyecto choca con los flujos 05, 06, 08, 11, 20 y el índice de `04-flujos-de-negocio`. Se amplía la lista (ahora 36) y se añade una **tabla de trazabilidad por flujo** con destino, para que el Auditor verifique que no queda ninguno sin actualizar.
5. **Descargas (addendum del 2026-09-28).** Son **acciones**, no interfaces: la tabla 1 dice "Registro de costos, ver" y la descarga pasa a la tabla 2. **Decididas:** descargar el registro de costos, administrador y jefe de proyectos (hoy solo el jefe de proyectos); descargar el consolidado RQ, como estaba. **Propuestas sin aprobar** (sección «Descargas» del artefacto, no están en el flujo 14): RDTs (ZIP) y listado de RDTs (PDF PROM-GP-0006) para los 13 roles; listado RQ (PDF PROM-GP-008) para los 13 roles; exportar DP para los seis roles que ven el DP. En el plan las decididas son requisito y las tres propuestas son **supuestos marcados** (A12) que no bloquean nada. Se añaden ítems de guardias de servidor de todas las descargas (PL-126, PL-127, PL-152 a PL-156). El estado del artefacto quedó «En revisión».
6. **F0 compara contra las dos tablas completas** (interfaces y acciones) y el Worker entrega la lista de funciones de `permisos.ts` que cambian, con las páginas, APIs y guardias de servidor que las usan (PL-146 y PL-147).
7. **Artefacto como base de accesos.** Toda interfaz, acción, permiso o acceso nuevo o cambiado en esta tarea (por ejemplo las entradas del registro único) actualiza el artefacto y el flujo 14 en la misma tarea: PL-149 en F7 y una comprobación del Auditor.
8. **Totales:** 12 fases y **156 ítems** de Punch List (29 nuevos: PL-128 a PL-156; PL-126 y PL-127 se reescriben para las descargas); 36 contradicciones; 7 vacíos; supuestos A1 a A13.
9. **Dudas para Victor** (no bloquean; limpiado en la v7 — lo que sigue ya NO son dudas: el jefe de proyectos ya tiene "Subir documento del proyecto" desde el 2026-09-28, y ya no existe la regla "todas las acciones excepto dos"): (a) si el jefe de proyectos también debe actualizar estado de RQ y subir registro de costos, hoy exclusivos de logística; (b) C35, quién alterna el Dashboard Parcial/Completo (recomendación sin confirmar: administrador y jefe de proyectos); (c) R30, si el alcance por OT para leer cubre también las pantallas sin economía (Cronograma, Paquetes de Trabajo, RDTs, RQ) y, si sí, cómo se aplica a un listado sin un único servicio activo. Ver "Puntos que el Planner deja anotados para Victor". **(Actualización 2026-09-29: (a) anulada, (b) C35 y (c) R30 resueltas; de esta lista no queda ninguna duda abierta.)**
10. **Descargas y exportaciones que el código tiene y el artefacto no lista** (se reportan a Victor, el plan no decide sobre ellas; A13): `GET /api/cronograma/plantilla` (plantilla `.xlsx` generada desde el DP, hoy con la guardia de subir cronograma); `GET /api/rdts/partes/[id]/pdf` (PDF de un RDT estructurado) y `GET /api/rdts/[id]/archivo` (archivo de un RDT subido), ambos con la guardia de ver RDTs; el PDF individual de un RQ (`…/requerimientos/exportar` con `tipo=detalle`, botón `BotonDescargarPdf` en el panel de ver RQ, la notificación de RQ y el formulario de RQ, hoy sin guardia de rol); el formato vacío PROM-GP-008 (`GET /api/requerimientos/formato-vacio` y su pantalla, solo sesión); y, por verificar por el Worker, la descarga de adjuntos de RQ y de documentos del checklist.

### Cambios de la versión 4 (2026-09-28; respecto de la versión 3, commit d1e67ac). Superada en lo que se indica en la versión 5

Victor decidió una **matriz base de permisos por interfaz**, ya escrita en el flujo 14 (sección "Matriz base de visibilidad por interfaz", commit 1c019d6). Esa sección es la **única fuente** de los roles por interfaz: este plan no copia la tabla, la enlaza.

1. **E2 queda sustituida por la matriz base.** Los conjuntos de roles propuestos en la versión 2 ("todos menos el rol Asistente", "los 13 roles" para Status RQ) desaparecen. Ahora: las interfaces **sin datos económicos** las ven los 13 roles; las **con datos económicos** (Dashboard del servicio y del portafolio, PR, DP ver, Curva S, Plan Maestro ver, Registro de costos) solo administrador, jefe de proyectos, jefe de oficina técnica y supervisor de costos. Administrador y jefe de proyectos tienen acceso a todo; el jefe de oficina técnica también crea RDT. Recursos de empresa: visibles y **accesibles** para los 13 roles (gestionar Causas CNC sigue solo con administrador y jefe de proyectos).
2. **Fases reordenadas (total: 12).** La antigua **F1B se llama ahora F5B** y se ejecuta después de F5, **condicionada** a los conflictos operativos CO1 a CO5 del flujo 14. Fases nuevas: **F2B** (abre a los 13 roles las interfaces sin economía; no depende de ningún conflicto) y **F5C** (acciones de administrador y jefe de proyectos, y JOT que crea RDT; condicionada a CO5, salvo la regla del JOT). **F0, F1, F2, F2B, F3, F4, F4B y F5 no dependen de la resolución de los conflictos**: F1 usa primero las funciones de permiso vigentes y F2B y F5B cambian el `permiso` de los accesos después.
3. **Cinco conflictos operativos con recomendación** (sección "Conflictos operativos CO1 a CO5 — opciones y recomendación"): planner y Plan Maestro, supervisor de oficina técnica y DP, supervisor de logística y Registro de costos, jefe de costos, y acciones destructivas o de sistema del jefe de proyectos.
4. **Dashboard del portafolio** (`app/programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx`, fuera del shell y sin guardia de rol hoy) entra en las guardias de F5B, junto con las APIs que sirven las pantallas con economía.
5. **Verificación contra la matriz.** El barrido de 13 roles se reemplaza por una verificación contra la matriz del flujo 14 leída del propio archivo (PL-96); la tabla de referencia de permisos del plan ya no lista roles por interfaz: solo las funciones y el estado de las guardias en el código.
6. **Ítems:** PL-88 a PL-101 reescritos; PL-27, PL-36, PL-38, PL-42 a PL-46, PL-48, PL-49, PL-56, PL-71 y PL-83 ajustados; **nuevos PL-119 a PL-127** (9). **Total: 127 ítems y 12 fases.** Riesgos R4, R5, R6, R16 y R18 reescritos; nuevos R24 a R26. Supuestos: A4 ampliado y A12 nuevo. Contradicciones: 28 (C11, C12, C14 y C21 actualizadas; nuevas C23 a C28). Vacíos: 5 (V5 nuevo).
7. **`vpc/` ya no existe** (verificado por el Orquestador el 2026-09-28): se actualiza "Carpetas/archivos huérfanos".
8. **Sin cambios:** el asistente (chat) como icono, el `.env.local` y el resto de las versiones 2 y 3. El **flujo 14 ya lo editó Victor**: el Worker no reescribe la matriz base.

### Cambios de la versión 3 (2026-09-27; respecto de la versión 2, commit 6a2444b)

1. **Requisito nuevo de Victor (Spec, resultado esperado 8): el asistente como icono en toda pantalla.** El asistente (`ChatPlaceholder`, "Pregúntale algo al asistente…") debe estar disponible en **todas** las pantallas del workspace, con y sin servicio, en escritorio y móvil, mostrado como un **icono**; al hacer clic se despliega su panel de conversación. Hoy es una barra a todo el ancho al pie de `<main>` en `WorkspaceShell.tsx`, solo con servicio y solo en escritorio (`hidden lg:block`), y está duplicada en la pantalla del portafolio. Sigue siendo vista previa sin datos (flujo 17: no habilitado). Se añade la fase **F4B** y 17 ítems nuevos (**PL-102 a PL-118**). Ver "Asistente como icono en toda pantalla" en la Punch List y las filas F4B, A10, A11, R20 a R23, C22 y V1 a V4.
2. **Aclaración de "asistente".** En la sección E2 y en los mensajes sobre guardias de rol, "asistente" es el **rol de usuario "Asistente"** (uno de los 13 roles), no el chat de ayuda. La **confirmación de los conjuntos de roles de E2 sigue pendiente de Victor** (F5B no empieza sin ella). En este documento, cuando se habla del chat se dice "el asistente (chat)" o "el asistente del shell".
3. **`.env.local` ya copiado al worktree** (autorización permanente de Victor). Los prompts del Worker ya no piden consultar antes de copiarlo; sigue sin leer ni mostrar sus valores, y cualquier otro archivo de entorno o de secretos sí se consulta. El worktree existe y no hay pendientes de entorno.
4. **Totales (versión 3):** 10 fases (F0, F1, F1B, F2, F3, F4, F4B, F5, F6, F7; la F1B pasó a llamarse F5B en la versión 4) y 118 ítems de Punch List; 22 contradicciones (se añade C22) y 4 vacíos (V1 a V4); supuestos A1 a A11 (A10 y A11 son nuevos).
5. **Regla del asistente: dónde integrarla al cierre (propuesta).** En el **flujo 16** (subsección nueva "Asistente: elemento del shell fuera de los tres paneles"), con una referencia breve en el flujo 01 (shell) y una aclaración en el flujo 17; y en `design.md` §3 (posición, z-index y patrón). Detalle en "Vacíos con reglas de negocio ya escritas".

### Cambios de la versión 2 (respecto de la versión 110dc7b)


1. **E2 se implementa ahora (decisión de Victor).** Nueva fase **F5B** (en las versiones 2 y 3 se llamaba F1B; ver versión 4) y 14 ítems nuevos (PL-88 a PL-101): guardias de rol en servidor para PR, Dashboard, DP (ver) y Status de Requerimiento, con funciones nuevas en `permisos.ts` que el registro usa como `permiso`. Los conjuntos propuestos entonces quedaron **sustituidos en la versión 4** por la matriz base del flujo 14 (ver "Permisos base…").
2. **A4 cambia (decisión de Victor).** Recursos de empresa es visible para los 13 roles; lo que el rol no puede usar se muestra deshabilitado con título. `puedeVerRecursos` deja de gobernar la visibilidad y queda como permiso de acceso (administrador y jefe de proyectos). Cambian F3, PL-27, PL-49, PL-71, la tabla de referencia de permisos y las contradicciones C11 y C12.
3. **Entorno corregido y resuelto.** `.worktrees/` **sí existía** (se corrigió la afirmación anterior) y tenía restos que impedían `git worktree add`. Victor autorizó la limpieza y el Orquestador la hizo el 2026-09-27: rama y worktree `local-worker-1` existen. Cambian "Entorno", R9, R15 y "Carpetas/archivos huérfanos".
4. **Modo local con subagentes.** Worker y Auditor son subagentes del Orquestador; la excepción D6 cambia (el Worker se detiene, registra la pregunta y la devuelve al Orquestador, que la relaya a Victor y reanuda al Worker). Cambian la nomenclatura de chats, los prompts, el Registro de decisiones y "Mejoras".
5. **Aprobación con cambios.** El Orquestador conserva las recomendaciones del Planner para 3, 4, 5, 6, E1 y E3 y los supuestos A1 a A3 y A5 a A9. El plan vuelve a `Pendiente del Responsable humano` porque E2 y A4 son ítems nuevos. Se registran las decisiones de Victor en el Registro de decisiones.
6. **Riesgos nuevos:** R16 (cerrar rutas hoy abiertas puede dejar sin acceso a un rol), R17 (enlaces internos a pantallas ahora protegidas), R18 (APIs que sirven las mismas pantallas) y R19 (Curva S exige alcance por OT aunque el flujo 14 dice que la lectura no lo exige). Contradicciones: 21 (se añade C21).
7. **Totales (versión 2):** 9 fases (F0, F1, F5B, F2 a F7), 101 ítems de Punch List.

### Qué decide Victor ahora

1. **Nada bloquea al Worker.** La matriz de permisos está aprobada y CO1 a CO5 resueltos. Lo que sigue abierto son las tres descargas propuestas en el artefacto (A12, supuestos), las descargas extra que el código tiene y el artefacto no lista (A13, se reportan) y las consultas por contradicción durante F7.
2. **Plan y Punch List** (secciones "Fases y dependencias" y "Punch List embebida"): 13 fases repartidas en 38 tandas (un Worker subagente por tanda, en serie), 181 ítems de Punch List (180 abiertos; PL-181 cerrado) verificables con Playwright y las dos cuentas de prueba.
3. **Decisiones 3, 4, 5 y 6 del Spec, E1 y E3**: recomendaciones conservadas (secciones "Decisiones abiertas 3 a 6" y "Decisiones adicionales"). Resumen: (3) chips del panel derecho visibles y deshabilitados; (4) conservar "Salir a Mi entorno" preservando el servicio; (5) "(OT) Orden de trabajo" inerte y "Recursos hh, hm, mat (s/c)" reemplazado por Cargos (HH) y Equipos (HM); (6) Registro de costos en Reportes y grupo "Servicio" (Ficha, Editar servicio, Editar checklist); (E1) preseleccionado y editable con la URL como fuente única; (E3) unificar "Status de RDTs" en `/rdts/status`.
4. **Contradicciones con flujos ya escritos** (36, más 7 vacíos, con tabla de trazabilidad por flujo): ninguna se edita antes del cierre y cada una se consulta a Victor antes de tocar el flujo.
5. **Supuestos menores A1 a A3 y A5 a A9**: aprobados por el Orquestador con la aprobación con cambios. A4 se reemplazó por la decisión de Victor. **A10 y A11 (asistente como icono), A12 (tres descargas propuestas) y A13 (descargas sin listar) son supuestos**: se aprueban con el plan salvo objeción de Victor; no son decisiones.
6. **Infraestructura:** ~~autorizar retirar o renombrar los restos de `.worktrees/`~~ **hecho el 2026-09-27** (rama y worktree `local-worker-1` creados, restos limpiados). El `.env.local` también se copió (autorización permanente de Victor).
7. **Texto de la política de "interfaz nueva"** (sección "Política de interfaz nueva — texto propuesto"): es lo que el Worker copiará al flujo 16 y a `05-diseno-y-ui.md`.
8. **Una pregunta que solo Victor puede responder (no bloquea las demás tandas):** si autoriza registros de prueba marcados en Recursos de empresa para verificar F5D (ver «Cambios de la versión 8», punto 6); mientras no responda, esos ítems quedan `Observado` en su camino feliz.
9. **Autonomía del Orquestador (2026-09-29):** lanza las tandas sin consultar y solo escala lo que no le corresponde decidir (ver `00-indice-de-tandas.md`).

Dimensión estimada: tarea grande. Unos 65 a 75 archivos del repositorio de la app (3 a 5 nuevos), sin migraciones ni cambios de base de datos, y 8 a 10 documentos de `pg_control_proyectos` al cierre.

## Fases y dependencias

Las fases se ejecutan **en el orden de la tabla, repartidas en 38 tandas, un Worker (subagente) por tanda, en serie y en un solo worktree** (`local-worker-1`). Los archivos compartidos (`WorkspaceShell.tsx`, `nav-proyecto.ts`, `grupo-proceso.ts`, `permisos.ts`, `PanelSecciones.tsx`, `CabeceraPagina.tsx`) impiden paralelizar de forma segura (ver "Asignación de roles"). Reparto: F0 (3 tandas), F1 (2), F2 (5), F2B (2), F3 (3), F4 (1), F4B (3), F5 (1), F5B (3), F5C (4), F5D (2), F6 (5), F7 (4); ver «Tandas de ejecución y trazabilidad ítem → tanda». Línea base y medición: `2026-09-27-paneles-servicio-persistente-briefs/medicion.md`.

| Fase | Contenido | Depende de | Punto de commit/push a `local-worker-1` |
|---|---|---|---|
| **F0 — Preparación y línea base** | Con la rama y el worktree autorizados: `npm test`, `npm run lint` y `npm run build` sobre `main` para fijar el baseline (lint se compara contra `main`, no contra cero; el baseline de 2026-09-23 fue 9 errores/18 advertencias y hay que volver a medirlo). Capturas Playwright de la línea base: los dos paneles y Mi entorno con cada cuenta, con y sin servicio, en escritorio y móvil, y una tabla "chip → destino → habilitado" del comportamiento actual (base de la regresión) y del asistente actual (la barra del pie con y sin servicio, en escritorio y móvil, y su copia en la pantalla del portafolio). Elegir los servicios de prueba SV1/SV2/SVX (ver Punch List). **Línea base por rol (matriz base del flujo 14):** con "Ver como" desde la cuenta A, para cada uno de los 13 roles y cada interfaz de la matriz base (incluido el dashboard del portafolio y las APIs que las sirven) anotar si abre o es rechazado hoy (tabla rol × interfaz "antes", que es la base del informe PL-97). **Lo mismo para las acciones:** para cada fila de la tabla 2 del flujo 14 y cada rol, quién puede hoy ejecutarla en el código (UI y guardia de servidor). Además, el Worker entrega la **lista de funciones de `permisos.ts` que cambian** (ver "Funciones de permisos.ts que cambian"), con las páginas, APIs y guardias de servidor que las usan (PL-146, PL-147), y el **inventario de descargas y exportaciones** del código contra la sección «Descargas» del artefacto (PL-127, PL-155). | Gate 1 aprobado (el worktree y el `.env.local` ya existen) | Ninguno (solo evidencia) |
| **F1 — Registro único de accesos y migración de todos los chips** | Crear el registro con los metadatos del flujo 16 (id, nombre, grupo, tipo, ruta o acción, requiere servicio, permiso, visibilidad por panel). Migrar **todos** los accesos existentes: 41 ítems de `NAV_PROYECTO`, los 10 chips de `herramientasPorGrupo` (Mi entorno), `CHIPS_ACCESO_RAPIDO` y las rutas fijas del panel izquierdo (Personal, Cargos, Equipos, Causas CNC). `NAV_PROYECTO`, `herramientasPorGrupo` y `hrefItemPanel` pasan a ser derivaciones del registro. **Sin cambio visible** salvo las diferencias declaradas (ver PL-52). Prueba de equivalencia: lo que derivan Mi entorno y el panel derecho es idéntico a la línea base de F0. Actualizar los contadores congelados de `nav-proyecto.test.ts`. En F1 el `permiso` de cada acceso es la función de `permisos.ts` **vigente** (no cambia quién puede); F2B y F5B cambian los permisos después, en una sola pieza. | F0 | Al cerrar la fase |
| **F2 — Servicio persistente** | Reconocer `?proyectoId=` en toda ruta del workspace además de `/proyectos/[id]/…` (`resolverProyectoId` de `WorkspaceShell.tsx`); mostrar el servicio actual en el panel izquierdo y validarlo contra los servicios visibles del usuario; que el registro envíe el servicio a todo acceso; que las pantallas lo reciban y lo preseleccionen (selector de OT o filtro N° OT según la pantalla); que los redirects del servidor y las salidas de formularios lo conserven (14 páginas con `redirect('/mi-entorno')`, 2 `router.push`, `CabeceraPagina`, redirect de `/proyectos/[id]/requerimientos`); sincronizar el selector interno de cada pantalla con la URL (A1). | F1 | Al cerrar la fase |
| **F2B — Interfaces sin economía abiertas a los 13 roles (matriz base)** | Según la tabla 1 del flujo 14 (única fuente; no se copia aquí). En `permisos.ts`, las funciones de **ver** de las interfaces sin datos económicos (`puedeVerCronograma`, `puedeVerPaquetesTrabajo`, `puedeVerRdts`, `puedeVerConsolidadoRq`, `puedeVerRecursos`) pasan a permitir a los 13 roles y se crea `puedeVerStatusRequerimiento` (13 roles). `puedeVerRecursos` deja de ser alias de `puedeVerApartadoProyectos`. Se abren las páginas y APIs que hoy usan esas funciones como guardia (`/cronograma`, `/paquetes-trabajo`, `/rdts/*`, `/logistica/consolidado-rq`, `/recursos/*`, `GET /api/cronograma`, `/api/paquetes-trabajo`, `/api/rdts/consolidado`, `/api/logistica/requerimientos`, `/api/recursos/*`, `GET /api/proyectos/[id]/requerimientos` y su exportación). **Descargas:** las APIs de exportar y descargar de esas interfaces (`rdts/exportar`, `rdts/partes/[id]/pdf`, `rdts/[id]/archivo`, `…/requerimientos/exportar`) cumplen la misma regla que "ver" (supuesto A12, PL-152 y PL-154). **Solo consulta:** las acciones dentro de esas pantallas siguen con sus funciones (gestionar Causas CNC, solo administrador y jefe de proyectos; comentar, actualizar estado y borrar RQ como hoy). Las descargas siguen a "ver" (A12). El Worker revisa que estas pantallas no muestran dinero (PL-121). **No depende de nada pendiente**: solo amplía el acceso. | F0, F1, F2 | Al cerrar la fase |
| **F3 — Panel izquierdo completo** | Panel izquierdo con servicio para los 13 roles; grupos y chips según Spec 4 y decisiones 5 y 6; chips no autorizados deshabilitados con título; chips sin pantalla inertes; informativos separados de acciones; Recursos de empresa con botón mostrar/ocultar (visible sin servicio, oculto con servicio) y sin "Materiales", **visible para los 13 roles** (A4 nuevo) **y accesible** (F2B abre la consulta): los chips de Personal, Cargos, Equipos y Causas CNC están activos para los 13 roles y solo gestionar Causas CNC queda para administrador y jefe de proyectos; `puedeVerApartadoProyectos` deja de gobernar el panel; `accion=crear` en Paquetes de Trabajo. Adaptación móvil (mismo contenido en el cajón). | F1, F2, F2B | Al cerrar la fase |
| **F4 — Panel derecho estandarizado** | Todos los chips del panel derecho y de "Accesos rápidos" con pantalla existente abren con el servicio elegido (resultado esperado 6, sin excepciones); estado habilitado/deshabilitado por permiso según la decisión 3; marca visual del tipo informativo/acción coherente con la de F3. | F1, F2 (y F3 para reutilizar el chip) | Al cerrar la fase |
| **F4B — Asistente como icono en toda pantalla (Spec 8)** | Quitar `<ChatPlaceholder />` del pie de `<main>` en `WorkspaceShell.tsx` (hoy solo con servicio y solo en escritorio) y de `app/(workspace)/programas/[id]/portafolios/[portafolioId]/page.tsx` (copia duplicada). El shell renderiza **un único** asistente en toda pantalla dentro de `(workspace)`, con y sin servicio, escritorio y móvil: un icono que al hacer clic despliega el panel de conversación y al cerrarlo vuelve a ser solo el icono. Se reutiliza `ChatPlaceholder` (pasa de barra a icono más panel; no se crea un componente paralelo). Propuesta de posición, que el Worker puede cambiar si lo justifica con Playwright: escritorio, esquina inferior derecha del área central, dentro de `<main>` y no fija a la ventana, para no invadir el panel derecho; móvil, en la cabecera móvil o flotante respetando `env(safe-area-inset-bottom)`, sin tapar el botón de herramientas ni los cajones. Capa (`z-index`) por debajo de los modales y cajones (`z-50`) y por encima de las cabeceras fijas de las tablas (`z-20` a `z-30`). Accesibilidad: nombre accesible, `aria-expanded`, foco por teclado, cierre con Escape (mismo patrón de `CajonMovil`). El estado abierto o cerrado vive en el shell, que no se remonta al cambiar de pantalla. **Sigue siendo vista previa: sin datos, sin llamadas a APIs** (flujo 17: no habilitado). `design.md` no define ningún patrón de botón flotante ni de panel desplegable: se reutilizan los tokens y el patrón de diálogo de `CajonMovil`, y la aprobación del Gate 1 cubre este cambio de layout (`design.md` §3 prohíbe wrappers nuevos sin aprobación). | F3, F4 (mismo archivo, `WorkspaceShell.tsx`) | Al cerrar la fase |
| **F5 — Pruebas automáticas y prueba de humo** | Prueba de cobertura (falla si hay una pantalla del workspace sin entrada en el registro ni excepción declarada), prueba de integridad del registro, prueba de humo "una entrada nueva solo en el registro aparece en todo", prueba de fuente contra redirects que pierden el servicio, función de matriz roles × accesos derivada del registro. | F1 a F4 | Al cerrar la fase |
| **F5B — Interfaces con economía (tabla 1 del flujo 14)** | Sin condiciones: la matriz está aprobada. Funciones en `permisos.ts` (nombres propuestos): `puedeVerEconomia` (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos), **único punto de cambio**, y las específicas: `puedeVerDashboard`, `puedeVerDashboardPortafolio`, `puedeVerPr`, `puedeVerCurvaS` (= economía), `puedeVerDp` (economía más supervisor de oficina técnica), `puedeVerPlanMaestro` (economía más planner) y `puedeVerRegistroCostos` (economía; logística entra a la pantalla solo para **subir**, sin ver ni descargar el contenido). Guardia en servidor en `/proyectos/[id]/pr`, `dashboard`, `dp`, `curva-s`, `registro-costos`, en `/plan-maestro` y en el **dashboard del portafolio**; **además del rol, exige alcance por OT para leer** (`proyecto_miembros`, con el mismo bypass de administrador que ya usa Curva S) en PR, Dashboard del servicio, Dashboard del portafolio, DP, Plan Maestro y Registro de costos — hoy ninguna de las seis lo exige, ni en la página ni en su API; Curva S ya lo tenía y no cambia. Se reutiliza el helper existente (`validarEscrituraProyecto` / `exigirAlcance` de `src/lib/auth/guard-proyecto.ts`), pese a su nombre: ya es el que usa Curva S para leer (`app/programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx`: fuera del shell y hoy sin guardia de rol). Las mismas funciones protegen las APIs (`…/dp/exportar` con la regla de "ver DP", PL-153; `GET /api/curva-s`, `GET /api/plan-maestro`, `…/registro-costos`); `…/partidas` **no** (lo usa Crear RQ). Los enlaces internos se muestran u ocultan según permiso (ficha del servicio, enlace al dashboard desde la grilla del portafolio). El registro pasa a usar estas funciones como `permiso`. Pruebas unitarias por los 13 roles contra la tabla 1. | F0, F1, F2B, F5 | Al cerrar la fase |
| **F5C — Acciones (tabla 2 del flujo 14)** | Sin condiciones. Se alinean las funciones de acción de `permisos.ts` con la tabla 2 (lista completa en "Funciones de permisos.ts que cambian"): adjudicar y crear programa y portafolio; confirmar transición; archivar y eliminar proyecto; eliminar contenedor; editar servicio; editar checklist; importar DP; editar perfil; crear, validar, rechazar y eliminar RDT; crear RQ, actualizar estado y eliminar RQ; descarga del consolidado RQ; subir y descargar registro de costos (esta última, administrador y jefe de proyectos, PL-126) y las guardias de servidor de todas las descargas y exportaciones (PL-126, PL-127, PL-152 a PL-156). **Cuatro funciones que hoy comparten alias se separan** para que un cambio no arrastre a otro rol: `puedeEditarServicio` (hoy usa `puedeAdjudicarProyecto`), `puedeImportarDp` (hoy usa `puedeSubirDocumento` con el supervisor de oficina técnica como responsable), `puedeCorregirRdt` (hoy usa `puedeCrearRdtEstructurado`, y el JOT ganaría corregir sin querer) y `puedeRechazarRdtValidado` (hoy usa `puedeValidarRdt`). También se desacopla `puedeDescargarConsolidadoRq` de `puedeVerConsolidadoRq`. Se cambian con las funciones las **páginas, APIs y guardias de servidor** que las usan. Las exclusivas del administrador (asignar rol administrador y «Ver como») no cambian. Las acciones que requieren OT a cargo siguen sujetas a `proyecto_miembros`. Ninguna prueba ejecuta escrituras ni borrados reales. | F0, F1 (y F5B para el modo "solo subir" del registro de costos) | Al cerrar la fase |
| **F5D — Gestión completa de Recursos (construir lo que falta)** | Función `puedeGestionarRecursos` en `permisos.ts` (administrador y jefe de proyectos; único punto de cambio), que reemplaza `puedeVerRecursos` en el POST de Personal y de la que `puedeGestionarCatalogoCnc` pasa a delegar (mismo patrón de F5C: separar alias que hoy comparten función). **Confirmar (sin UI nueva):** crear Personal, crear Causa CNC, activar o desactivar Causa CNC quedan con la función nueva. **Construir:** editar y eliminar/desactivar Personal (`TablaPersonal.tsx` + `PATCH /api/recursos/personal/[id]` nuevo); crear, editar y eliminar/desactivar Cargo y Equipo (`TablaRecursos.tsx`, hoy "solo lectura" — se le agregan formulario de alta y acciones por fila; `POST` y `PATCH` en `src/app/api/recursos/route.ts` y un `route.ts` nuevo por id); editar el texto de una Causa CNC (`TablaCatalogoCnc.tsx` — la API `PATCH …/catalogo-cnc/[id]` ya acepta `descripcion`, solo falta el control en pantalla). "Eliminar" se implementa como desactivar (`activo = false`), nunca borrado físico (AGENTS.md, y ya es el patrón de Causas CNC, Cargos y Equipos). No cambia qué recurso es "de empresa" ni la exclusión de Materiales. | F0, F1, F2B | Al cerrar la fase |
| **F6 — Verificación integral y loop** | Autoverificación con Playwright de toda la Punch List con las dos cuentas (permisos por ambos lados) y la verificación de los 13 roles con "Ver como" desde la cuenta con permisos altos **contra la matriz base del flujo 14 leída del propio archivo** (paneles, Mi entorno, pantallas y APIs; el plan no duplica la tabla). Corregir y repetir hasta 100% Conforme; informe "qué cambió por rol respecto de la línea base de F0", que compara contra la **tabla 1 y la tabla 2 completas** del flujo 14; lint contra `main`, `npm test`, `npm run build`. Evidencia en `02-trabajo-activo/03-evidencia/`. | F1 a F5 (incluye F2B, F4B, F5B y F5C) | Al cerrar la fase y antes de reportar |
| **F7 — Consolidación documental y cierre del Worker** | Con la consulta previa a Victor de cada contradicción (por la vía de subagente: el Worker se detiene, devuelve la pregunta al Orquestador y este la relaya): actualizar flujos 16, 01, 14 y los que apliquen (03, 05, 06, 11, 15, 17, 21), escribir la regla del asistente como icono en toda pantalla en el flujo 16 (con referencia cruzada en el 01 y aclaración en el 17), **verificar que el flujo 14 aprobado (tablas 1 y 2) coincide con lo implementado y no reescribirlo salvo lo que Victor decida (descargas); actualizar el artefacto «Matriz de permisos» y el flujo 14 con toda entrada nueva o cambiada del registro único; y aplicar la lista de trazabilidad por flujo (sección "Contradicciones"), con consulta a Victor por cada contradicción y anotando dónde quedó aplicado cada cambio**, escribir la política de "interfaz nueva" en el flujo 16 y en `05-diseno-y-ui.md`, documentar el chip deshabilitado y el registro en `design.md`, comparar la matriz derivada del registro con la matriz base del flujo 14, trasladar mejoras de trabajo, reglas de negocio y huérfanos de los apartados obligatorios a sus destinos. | F6 | Commit + push a `main` de `pg_control_proyectos` (`git add` explícito) |

Regla de commits (`03-entorno-git-y-worktrees.md`), adaptada a las tandas: cada tanda termina con un commit en `local-worker-1` (`git add` explícito, sin logs ni capturas pesadas), solo al terminar completo el ítem en curso; el «~35% de la Punch List» de la regla original se cumple de sobra con ~38 commits. **Sin push:** `local-worker-1` no tiene upstream (verificado) y el primer push lo decide Victor. Las tandas F7 (documentación) commitean en `main` de `pg_control_proyectos` con `git add` explícito y solo con la autorización vigente de Victor que confirme el Orquestador. Como el Worker es un subagente, cada cierre de tanda es también el punto natural para devolver una pregunta al Orquestador.

### Diseño propuesto del registro de accesos

Los nombres son propuestas; el Worker puede ajustarlos si los justifica, pero los metadatos son los del flujo 16 más los marcados como "extensión".

```ts
interface AccesoRegistrado {
  id: string;                       // slug único; sustituye las claves paralelas de hoy
  etiqueta: string;
  grupo: string;                    // grupo del panel derecho / de la sección del panel izquierdo
  tipo: 'informativo' | 'accion';
  ruta?: (servicioId?: string) => string;  // sin pantalla => sin ruta => chip inerte
  requiereServicio: 'si' | 'opcional' | 'no'; // extensión: 'opcional' = abre sin servicio y lo preselecciona si lo hay (Plan Maestro, Status RQ, Consolidado RQ, Status RDTs…)
  permiso?: (roles: Rol[]) => boolean;        // sin permiso => cualquier usuario autenticado (solo para accesos sin restricción de rol, como Notificaciones o la ficha); usa las funciones de permisos.ts, incluidas las nuevas de F5B
  tituloDeshabilitado?: string;
  visible: { izquierdo: boolean; centro: boolean; derecho: boolean; accesoRapido?: boolean };
  icono; colorClase; orden;
}
```

De él se derivan con funciones puras (parametrizadas por el registro, para poder probarlas con un registro de prueba): el panel derecho, el panel izquierdo, `herramientasPorGrupo` (Mi entorno), el href con `?proyectoId=`, el estado habilitado o deshabilitado por rol y la matriz roles × accesos del flujo 14. `puedeGestionarRecursos` no es un metadato nuevo del registro: Personal, Cargos, Equipos y Causas CNC siguen siendo un solo acceso cada uno (visible para los 13, `permiso` = `puedeVerRecursos`); las acciones de F5D viven dentro de esas pantallas, igual que "Crear paquete" dentro de Paquetes de Trabajo (A7). El registro también declara las **pantallas sin chip** (excepciones con motivo: `/login`, `/admin/usuarios`, `/configuraciones`, `/mi-perfil`, `/programas/**`, etc.).

### Cómo se preselecciona el servicio en cada pantalla (dimensionado real)

No todas las pantallas tienen un "selector de OT". El Worker aplica el patrón que la pantalla ya usa:

| Pantalla | Mecanismo actual | Preselección con `?proyectoId=` |
|---|---|---|
| Cronograma, Paquetes de Trabajo, Plan Maestro | prop `proyectoIdInicial` desde `searchParams` | Ya existe; solo falta que el shell lo reconozca y que el selector actualice la URL |
| Crear RDTs (`FormularioCrearRdt`) | estado `parte.proyectoId`, selector de OT | Leer el parámetro y usarlo como valor inicial |
| Consolidado RDTs (`TablaConsolidadoRdts`) | estado `proyectoId` vacío, selector "Elige el N° OT…" | Nueva prop de valor inicial; carga automática |
| Subir RDTs, Crear RQ | `proyectoIdInicial` en Mi entorno | Ya existe |
| Status de RDTs, Archivo de RDTs, Consolidado RQ | **sin selector**; filtro de texto por columna "N° OT" | Filtro `numeroOt` inicial = N° OT del servicio (el servidor lo resuelve desde el id) |
| Status de Requerimiento (`/requerimientos`) | multiselección `?ots=` y filtro `numeroOt` | `proyectoId` equivale a `ots=<id>` cuando no viene `ots`; `ots` sigue siendo la selección de la tabla y `proyectoId` el contexto de los paneles |
| `/proyectos/[id]/dp`, `pr`, `dashboard`, `curva-s`, `registro-costos` | el servicio va en la ruta | Sin cambio; solo se reconoce como contexto |

Detalle a vigilar: el filtro N° OT es de "contiene", y `PS-0001` también coincidiría con `PS-00010`. Se documenta como riesgo; si aparece en la práctica, se usa coincidencia exacta al preseleccionar.

## Tandas de ejecución y trazabilidad ítem → tanda

**Carpeta de briefs:** `docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente-briefs/` (`00-reglas-de-contexto.md`, `00-indice-de-tandas.md`, `medicion.md` y un brief por tanda, `f<fase>-tanda-<letra>.md`, de 2,7 a 5,5 KB, todos ≤ 8 KB). Criterio de reparto: cohesión de archivos compartidos y de fase, sin partir un ítem en dos tandas y respetando el orden y las dependencias de fase. Los ítems con dos fases (PL-88, PL-93, PL-95, PL-99, PL-152, PL-155) se asignan a la tanda donde se cierran (PL-88 → `F5B-A`, con `F2B-A` implementando su mitad; PL-93, PL-95 y PL-99 → `F5B-C`; PL-152 → `F2B-B`; PL-155 → `F7-B`, con la lista de `F0-A`); PL-35 y PL-36 («F1 a F7») → `F6-E`. Además de los ítems hay **entregables sin fila de Punch List**: LB-01 (línea base técnica, `F0-A`), LB-02 a LB-05 (línea base en el navegador, `F0-B`), el registro base (`F1-A`) y el helper de servicio (`F2-A`); su evidencia va a `03-evidencia/`.

**Comprobación de cobertura (script sobre este archivo, 2026-09-29):** el plan tiene 181 filas PL-xxx únicas; 1 cerrada por decisión (PL-181, `No aplica`) y **180 abiertas, asignadas exactamente una vez** (sin duplicados, sin faltantes, sin ítems asignados que no existan).

| Tanda | Fase | Ítems de Punch List | N.º |
|---|---|---|---|
| `F0-A` | F0 | PL-127, PL-146 | 2 |
| `F0-B` | F0 | Entregables LB-02 a LB-05 (sin fila PL) | 0 |
| `F0-C` | F0 | PL-147 | 1 |
| `F1-A` | F1 | PL-51 | 1 |
| `F1-B` | F1 | PL-50, PL-52 | 2 |
| `F2-A` | F2 | PL-01, PL-15, PL-16, PL-37, PL-47, PL-66, PL-72 | 7 |
| `F2-B` | F2 | PL-02 a PL-04, PL-11, PL-12, PL-14 | 6 |
| `F2-C` | F2 | PL-05 a PL-10, PL-13 | 7 |
| `F2-D` | F2 | PL-19 a PL-21, PL-70 | 4 |
| `F2-E` | F2 | PL-17, PL-18, PL-67, PL-69 | 4 |
| `F2B-A` | F2B | PL-92, PL-94, PL-119, PL-120 | 4 |
| `F2B-B` | F2B | PL-121, PL-152, PL-154 | 3 |
| `F3-A` | F3 | PL-22 a PL-26 | 5 |
| `F3-B` | F3 | PL-27 a PL-29, PL-49, PL-59, PL-60, PL-62 | 7 |
| `F3-C` | F3 | PL-38 a PL-40, PL-48, PL-61, PL-63, PL-64, PL-71 | 8 |
| `F4-A` | F4 | PL-30 a PL-34, PL-41, PL-42 | 7 |
| `F4B-A` | F4B | PL-102 a PL-107 | 6 |
| `F4B-B` | F4B | PL-108 a PL-111 | 4 |
| `F4B-C` | F4B | PL-112 a PL-116 | 5 |
| `F5-A` | F5 | PL-53, PL-55 a PL-57 | 4 |
| `F5B-A` | F5B | PL-88 a PL-90, PL-125, PL-174, PL-175 | 6 |
| `F5B-B` | F5B | PL-91, PL-122, PL-123, PL-153, PL-176 a PL-178 | 7 |
| `F5B-C` | F5B | PL-93, PL-95, PL-98, PL-99, PL-101, PL-124, PL-179 | 7 |
| `F5C-A` | F5C | PL-128 a PL-133, PL-135 | 7 |
| `F5C-B` | F5C | PL-134, PL-136 a PL-138 | 4 |
| `F5C-C` | F5C | PL-126, PL-139 a PL-143 | 6 |
| `F5C-D` | F5C | PL-144, PL-145, PL-148, PL-151 | 4 |
| `F5D-A` | F5D | PL-157 a PL-162 | 6 |
| `F5D-B` | F5D | PL-163 a PL-169 | 7 |
| `F6-A` | F6 | PL-43, PL-96, PL-97 | 3 |
| `F6-B` | F6 | PL-44 a PL-46, PL-54, PL-73, PL-180 | 6 |
| `F6-C` | F6 | PL-65, PL-117, PL-170 a PL-172 | 5 |
| `F6-D` | F6 | PL-68, PL-77, PL-78, PL-80 | 4 |
| `F6-E` | F6 | PL-35, PL-36, PL-74 a PL-76, PL-79, PL-87 | 7 |
| `F7-A` | F7 | PL-58, PL-84, PL-118 | 3 |
| `F7-B` | F7 | PL-83, PL-100, PL-149, PL-155, PL-156, PL-173 | 6 |
| `F7-C` | F7 | PL-82 | 1 |
| `F7-D` | F7 | PL-81, PL-85, PL-86, PL-150 | 4 |
| — | F0 | PL-181 cerrado por decisión de Victor (R30, 2026-09-29), estado `No aplica` | 0 |
| **Total** | 13 fases | **180 ítems abiertos asignados exactamente una vez + 1 cerrado = 181** | **180** |

**Tandas de corrección reservadas:** `F6-R#`, solo si tras `F6-E` quedan ítems `Observado` corregibles (no cuentan en las 38). El mapa ítem → tanda ordenado por ID está en `00-indice-de-tandas.md`.

## Asignación de roles

| Rol | Chat | Rama | Worktree | Estado |
|---|---|---|---|---|
| Orquestador | `local_1.orquestador_paneles-servicio-persistente` (por renombrar) | `main` | N/A | Activo |
| Planner | `local_2.planner_paneles-servicio-persistente` | `main` | N/A | Versión 8 del plan entregada para el Gate 1 (2026-09-29) |
| Worker **de tanda** (un subagente nuevo por cada una de las 38 tandas de F0 a F7, incluidas F2B, F4B, F5B, F5C y F5D; en serie), **subagente** del Orquestador | `local_3.worker_paneles-servicio-persistente-<ID de tanda>` (etiqueta lógica, p. ej. `…-f2-tanda-c`) | `local-worker-1` (**creada** por el Orquestador desde `main`, commit `1942b01`; sin upstream remoto) | `.worktrees/local-worker-1` en `py_control_proyectos_web` (**creado** el 2026-09-27; `.env.local` copiado; único worktree activo) | Listo para arrancar en cuanto Victor apruebe el Gate 1: sin fases condicionadas |
| Auditor, **subagente** del Orquestador | `local_4.auditor_paneles-servicio-persistente` (etiqueta lógica) | `main` | N/A | Pendiente |

**Un Worker por tanda, en serie y sobre una sola rama, y por qué.** Todo lo importante pasa por los mismos archivos: `WorkspaceShell.tsx` (los dos paneles y el asistente), el registro de accesos y sus derivaciones (`nav-proyecto.ts`, `grupo-proceso.ts`), `permisos.ts`, `PanelSecciones.tsx` y `CabeceraPagina.tsx`; partir el trabajo entre Workers en paralelo obligaría a coordinar ramas sobre el mismo registro (criterio del estándar: independencia real de archivos). Lo que sí se parte es la **sesión**: un solo Worker con 181 ítems no cabe en una sesión (medición de referencia: 156–191 llamadas y 625–682k tokens de contexto en un Worker de fase entera; con tandas, hasta ~28M en total y contexto máximo de 186k). Por eso cada tanda (1 a 8 ítems, con su brief de ≤ 8 KB) la ejecuta un Worker nuevo que lee solo su brief y las reglas de contexto, cierra con commit, evidencia y handoff, y devuelve el control; el siguiente Worker retoma del estado de la rama y del handoff, no del plan. Se ejecutan de una en una para que el árbol de trabajo siempre esté limpio y commiteado al lanzar la siguiente.

**Orquestador.** Lanza las tandas una tras otra según `00-indice-de-tandas.md` y decide por su cuenta lo que pueda decidir; solo consulta a Victor por lo que no le corresponda (contradicciones con flujos escritos, cambios de permisos, acciones destructivas o de infraestructura no autorizadas, dudas de negocio). Mide cada tanda (`medicion.md`) y ajusta el brief siguiente si se pasó de la meta. No aprueba en nombre de Victor ni hace merge, push, PR ni crea ramas o worktrees sin autorización explícita.

**Auditor.** Uno solo, al terminar F7.

**Ejecución como subagentes (Victor, 2026-09-27).** Worker y Auditor corren dentro de la sesión del Orquestador. Un subagente no puede conversar con Victor ni recibir mensajes suyos: toda consulta pasa por el Orquestador. El chequeo del Auditor de "existió un chat de Worker separado" se cumple con un subagente distinto del Orquestador y del Planner, identificado por su etiqueta lógica y por los commits en `local-worker-1`.

### Prompt del Planner

```text
Rol: Planner. Chat: local_2.planner_paneles-servicio-persistente.
Objetivo: a partir del Spec/SDD aprobado en docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente.md, redactar en ese mismo archivo (secciones "Plan") las fases, la Punch List verificable, la asignación de Workers y los prompts de Worker y Auditor, para el Gate 1 de Victor.
Leer: AGENTS.md; docs/00-estandar-agentes/04-flujo-sdd-y-planes.md (pasos 5–7), 02-roles-y-delegacion.md § Planner, 06-plantillas/02-plan.md y 05-punch-list.md; TODOS los flujos de docs/04-flujos-de-negocio/; docs/03-aprendizaje-continuo/README.md (solo el índice); docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md; el Spec completo, incluido el Registro de decisiones.
Código (solo lectura, para dimensionar): D:\VICTOR\CLAUDE CODE\py_control_proyectos_web — WorkspaceShell.tsx, PanelSecciones.tsx, nav-proyecto.ts(+test), grupo-proceso.ts, permisos.ts y las páginas rdts/*, requerimientos, logistica/consolidado-rq, cronograma, paquetes-trabajo, plan-maestro.
Criterios de salida: (1) fases con dependencias; la migración al registro único es fase propia y va antes de completar el panel izquierdo; (2) Punch List con checklist verificable por Playwright con las dos cuentas de prueba (permisos por ambos lados), para que Victor lo apruebe ANTES de implementar; (3) división en Workers solo si hay independencia real de archivos (WorkspaceShell y nav son archivos compartidos: probablemente un solo Worker); (4) opciones con análisis y recomendación para las decisiones abiertas 3, 4, 5 y 6 del Spec; (5) contradicciones con reglas de negocio ya escritas anticipadas y listadas (flujos 16, 01, 14, 03, 05, 06); (6) prompts cerrados y breves para Worker y Auditor; (7) archivos afectados.
Restricciones: no implementas ni apruebas el plan; no creas ramas ni worktrees; commit y push del plan solo a main de pg_control_proyectos, con git add explícito de los archivos que toques; no tocar la carpeta vpc/ (es de otra sesión); las credenciales de las cuentas de prueba no se copian a ningún archivo del repositorio; no editar flujos de negocio (eso ocurre al cierre, con consulta previa a Victor).
```

### Prompt de cada Worker

```text
Rol: Worker de tanda, subagente local del Orquestador. Etiqueta lógica: local_3.worker_paneles-servicio-persistente-<ID de tanda> (por ejemplo f2-tanda-c).
Recibes UNA tanda, la cierras y terminas; no continúas con la siguiente (el Orquestador lanza otro Worker). Repositorio de código: D:\VICTOR\CLAUDE CODE\py_control_proyectos_web, rama local-worker-1, worktree .worktrees/local-worker-1 (ya existen; el .env.local ya está copiado por autorización permanente de Victor: no lo leas ni muestres sus valores ni preguntes por copiarlo; cualquier OTRO archivo de entorno o de secretos se consulta antes). Nunca trabajes en el checkout principal. Nunca main, nunca merge ni push, nunca borrar ramas, worktrees ni carpetas. Las tandas F7 trabajan la documentación en pg_control_proyectos, rama main, con git add explícito y solo con la autorización de commit que el Orquestador te confirme.
Lee, en este orden y nada más de inicio: (1) D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\02-trabajo-activo\01-planes\2026-09-27-paneles-servicio-persistente-briefs\00-reglas-de-contexto.md; (2) el brief de tu tanda en esa misma carpeta (f<fase>-tanda-<letra>.md). NO leas el plan completo (221 KB): si necesitas un dato, Grep por su ID (PL-123, C35, R28, A12…) y lee solo esas líneas.
Objetivo: dejar los ítems de tu brief en Conforme (o Observado con su causa), verificados por ti con Playwright, pruebas y llamadas sin efecto, con las dos cuentas de prueba por los dos lados de cada permiso (las credenciales viven fuera del repositorio, en la memoria del agente: no las copies ni las imprimas), aplicando el contrato técnico del brief.
Cierre (detalle en 00-reglas-de-contexto.md): solo tus filas de la Punch List (Grep del ID + Edit), evidencia al final del archivo de evidencia, handoff de máx. 15 líneas al final del progreso, commit en local-worker-1 con git add explícito, y mensaje final con ítems cerrados, pendientes, preguntas devueltas y número de llamadas. Meta ~80 llamadas; a las ~60 cierra y escribe el handoff.
Registra en el momento, en los apartados del plan, cada mejora de trabajo, regla de negocio acordada y carpeta/archivo huérfano.
Ante una contradicción con un flujo escrito, un cambio de permisos que las tablas 1 y 2 del flujo 14 no decidan, una acción destructiva o irreversible, infraestructura no autorizada o una duda de negocio: eres un subagente y no hablas con Victor; DETENTE en ese punto, deja hecho el commit de lo terminado, registra la pregunta en «Reglas de negocio acordadas en esta tarea» (opciones y tu recomendación) y DEVUÉLVELA al Orquestador en tu reporte final. Si un ítem no depende de la pregunta, avanza con él antes.
Restricciones: las de 00-reglas-de-contexto.md y las de tu brief. No cambia quién puede hacer qué salvo lo decidido por Victor y escrito en el flujo 14 (tablas 1 y 2); verificación de solo lectura sobre datos reales; sin migraciones ni cambios en db/; no modificar src/lib/pr, dashboard, curva-s, plan-maestro ni dp; no conectar el asistente (chat) a datos (flujo 17); «asistente» en los permisos es el ROL.
```

### Prompt del Auditor

```text
Rol: Auditor, ejecutado como subagente local del Orquestador. Etiqueta lógica: local_4.auditor_paneles-servicio-persistente. Rama: main de pg_control_proyectos (solo documentación). No implementas, no haces merge, no apruebas por Victor, no borras nada. Como subagente no hablas con Victor: cualquier duda va a tu reporte para el Orquestador.
Primer chequeo (antes de todo lo demás): con git log y git branch --contains en py_control_proyectos_web confirma, no de memoria, que la implementación está en local-worker-1 y no en main ni en ninguna rama del Orquestador o del Planner, y que la hizo un subagente Worker distinto del Orquestador (por sus commits y el progreso). Si no se cumple, la tarea no pasa auditoría: reporta y detente.
Segundo chequeo: que las mejoras de trabajo, reglas de negocio y huérfanos estén en los apartados obligatorios del plan y trasladados a su destino (mejoras a 03-aprendizaje-continuo, reglas directo a los flujos, huérfanos reportados a Victor).
Luego revisa: Spec, plan, Punch List (los 180 ítems abiertos con evidencia; PL-181 cerrado por decisión de Victor), la carpeta de briefs (índice de tandas con cada tanda cerrada y su commit en local-worker-1, y la tabla de resultados de medicion.md), progreso, evidencia y el diff de local-worker-1 contra main. Comprueba de forma independiente, sobre una muestra que incluya siempre las verificaciones de permisos por ambos lados, que la Punch List se cumple con Playwright y las dos cuentas de prueba (las credenciales viven fuera del repositorio; no las copies a ningún archivo). Verifica: el asistente (chat) aparece como un único icono en toda pantalla del workspace, sin barra fija ni duplicado en el portafolio, sin tapar contenido y sin conectarse a datos; registro único sin listas paralelas; prueba de cobertura y prueba de humo realmente rojas cuando deben serlo; matriz del flujo 14 derivada del registro y diferencias con la tabla anterior informadas; el diff no toca db/ ni src/lib/pr, dashboard, curva-s, plan-maestro y dp, y en las páginas de PR, Dashboard (servicio y portafolio), DP, Curva S, Plan Maestro y Registro de costos solo cambia la guardia; los permisos coinciden con la matriz base del flujo 14 leída del archivo (comprobación por los dos lados con las dos cuentas y con "Ver como" para los 13 roles, en pantallas y APIs) y el informe "qué cambió por rol" coincide con la línea base de F0; los permisos implementados coinciden con las tablas 1 y 2 del flujo 14 (todas las filas y los 13 roles), la lista de funciones de permisos.ts que cambian está completa con sus páginas, APIs y guardias, y no queda ningún alias que arrastre a otro rol; Recursos (Personal, Cargos, Equipos, Causas CNC) tiene crear, editar y eliminar/desactivar para administrador y jefe de proyectos, probado por los dos lados, y "eliminar" nunca borra físico; el artefacto «Matriz de permisos» y el flujo 14 quedaron actualizados con toda entrada nueva o cambiada del registro; la tabla de trazabilidad por flujo del plan no deja ningún flujo o documento afectado sin actualizar ni referencia a la versión anterior (política de coherencia y trazabilidad); ningún dato real fue modificado; los flujos 16, 01, 14 (y 03, 05, 06, 11, 15, 21 si aplica) y 05-diseno-y-ui.md quedaron coherentes con lo implementado y con las respuestas de Victor; la política de interfaz nueva coincide con el texto aprobado en el Gate 1; lint contra main; ninguna credencial en el repositorio.
Lee todos los flujos de 04-flujos-de-negocio/.
Entrega el Informe de Auditoría en el propio plan con el formato de 06-plantillas/06-informe-auditoria.md: APLICAR AHORA / PROPONER A RESPONSABLE / NO PROMOVER / PROPONER SKILL, pendientes técnicos y documentales, y recomendación de estado (listo, bloqueado o requiere corrección).
```

## Archivos / componentes afectados

Rutas relativas a `py_control_proyectos_web/`, salvo la sección de documentación. Definitiva salvo que el Worker justifique otra cosa en el progreso.

**Nuevos (propuestos, ver "Diseño propuesto del registro")**

| Archivo | Para qué |
|---|---|
| `src/lib/config/registro-accesos.ts` (+ `.test.ts`) | Registro único, derivaciones puras (panel izquierdo, panel derecho, Mi entorno, href con servicio, habilitado por rol, matriz) y lista de pantallas sin chip |
| `src/lib/config/servicio-contexto.ts` (+ `.test.ts`) | Helper para añadir/leer `?proyectoId=`, usado por shell, redirects, `CabeceraPagina` y salidas de formularios |
| Prueba de cobertura de pantallas (`src/lib/config/cobertura-pantallas.test.ts`) | Recorre `src/app/**/page.tsx` con el sistema de archivos de Node (el entorno de vitest es `node`) y falla si una pantalla no está en el registro ni en las excepciones |
| Componente de chip compartido (informativo, acción, deshabilitado, inerte) y sección del panel izquierdo (por ejemplo en `src/components/ui/`) | Una sola pieza visual para ambos paneles; `design.md` §5 exige justificar componentes nuevos y documentarlos: la aprobación del Gate 1 cubre esta creación y el detalle se documenta al cierre |

**Modificados**

| Archivo | Qué cambia |
|---|---|
| `src/components/ui/WorkspaceShell.tsx` | `resolverProyectoId`, `ContenidoNav` (panel izquierdo completo), `ContenidoHerramientas`, servicio actual visible, enlaces del pie con servicio y (F4B) el asistente como único icono en toda pantalla, sin la barra del pie |
| `src/components/ui/ChatPlaceholder.tsx` | **F4B:** pasa de barra a icono más panel desplegable (accesible, con Escape y foco); sigue siendo vista previa sin datos; el texto de ejemplo se neutraliza (A10) |
| `src/app/(workspace)/programas/[id]/portafolios/[portafolioId]/page.tsx` | **F4B:** se quita la segunda copia de `<ChatPlaceholder />` |
| `src/components/ui/PanelSecciones.tsx` | `AccesosRapidos` y `GruposAccordion`: servicio en todos los enlaces, deshabilitado por permiso, marca de tipo |
| `src/lib/config/nav-proyecto.ts` + `nav-proyecto.test.ts` | Pasa a derivar del registro; se reescriben las pruebas que fijan contadores (41 ítems) y las que exigen "Cronograma necesita servicio elegido" |
| `src/lib/notificaciones/grupo-proceso.ts` + `grupo-proceso.test.ts` | `herramientasPorGrupo` deriva del registro y los chips de Mi entorno envían el servicio |
| `src/components/ui/EntornoTrabajoGrupo.tsx` | Consume la derivación; conserva el estilo de chip deshabilitado (`opacity-40 cursor-not-allowed`) |
| `src/app/(workspace)/layout.tsx` | Deja de pasar `puedeVerApartadoProyectos` como puerta del panel; puede pasar la lista de servicios vigentes para validar y nombrar el servicio actual |
| `src/components/ui/TablaRecursos.tsx` | **F5D:** deja de ser "solo lectura" (Cargos y Equipos); formulario de alta y acciones de editar y desactivar por fila, con el mismo permiso |
| `src/components/ui/TablaPersonal.tsx` | **F5D:** suma editar y desactivar a la creación que ya tiene |
| `src/components/ui/TablaCatalogoCnc.tsx` | **F5D:** suma el control de editar el texto (la API ya lo acepta) |
| `src/app/api/recursos/route.ts` | **F5D:** hoy solo `GET` para cargos y equipos; suma `POST` y, en un archivo nuevo por id, `PATCH` |
| `src/app/api/recursos/[id]/route.ts` (nuevo) | **F5D:** `PATCH` de un cargo o equipo (editar o desactivar), con `tipo` en el cuerpo o en la ruta, según decida el Worker |
| `src/app/api/recursos/personal/[id]/route.ts` (nuevo) | **F5D:** `PATCH` de un trabajador (editar o desactivar) |
| `src/lib/permisos/permisos.ts` + `permisos.test.ts` | **Permisos:** `puedeVerEconomia` y las funciones de ver nuevas o ajustadas (F2B, F5B), cuatro funciones nuevas que separan alias (`puedeEditarServicio`, `puedeImportarDp`, `puedeCorregirRdt`, `puedeRechazarRdtValidado`) y los cambios de roles de las funciones de acción, todo según la tabla tal cual está en el flujo 14. `puedeVerRecursos` deja de ser alias de `puedeVerApartadoProyectos`. Lista completa en "Funciones de permisos.ts que cambian" |
| `src/app/(workspace)/proyectos/[id]/pr/page.tsx`, `dashboard/page.tsx`, `dp/page.tsx` y `src/app/(workspace)/requerimientos/page.tsx` | **E2:** guardia de rol en servidor antes de leer datos. Solo se añade la guardia; los cálculos y consultas existentes no se tocan |
| `src/app/api/proyectos/[id]/requerimientos/route.ts` (GET), `requerimientos/exportar/route.ts`, `dp/exportar/route.ts` | **E2:** las mismas funciones de permiso protegen las APIs que sirven esas pantallas. `partidas/route.ts` **no** se restringe (lo usa Crear RQ) |
| `src/app/(workspace)/proyectos/[id]/page.tsx` (ficha del servicio) | El enlace "Ver Dashboard" (y los de PR y DP del checklist de documentos) se muestra u oculta según permiso, como ya hace el de Plan Maestro |
| `src/app/(workspace)/rdts/{crear,status,listado,consolidado}/page.tsx` + `FormularioCrearRdt.tsx`, `TablaStatusRdts.tsx`, `TablaListadoRdts.tsx`, `TablaConsolidadoRdts.tsx` | Reciben y preseleccionan el servicio |
| `src/app/(workspace)/requerimientos/page.tsx`, `logistica/consolidado-rq/page.tsx` + `ListadoRequerimientos.tsx`, `TablaConsolidadoRq.tsx` | Idem (con la regla `proyectoId` ↔ `ots`) |
| `src/app/(workspace)/cronograma/page.tsx`, `paquetes-trabajo/page.tsx`, `plan-maestro/page.tsx`, `mi-entorno/page.tsx` + `FormularioPaquetesTrabajo.tsx`, `FormularioCronograma.tsx`, `FormularioPlanMaestro.tsx` | El selector actualiza la URL (A1); `accion=crear` en Paquetes (A7) |
| Las 14 páginas con `redirect('/mi-entorno')` (`cronograma`, `logistica/consolidado-rq`, `mi-perfil`, `paquetes-trabajo`, `plan-maestro`, `rdts` ×5, `recursos` ×4) | El redirect conserva `?proyectoId=` con el helper |
| `src/app/(workspace)/proyectos/[id]/requerimientos/page.tsx`, `proyectos/[id]/mi-entorno/page.tsx`, `proyectos/[id]/entorno/[grupo]/page.tsx` | Redirects que hoy pasan el servicio por otro parámetro o lo pierden |
| `src/components/ui/CabeceraPagina.tsx` | Chip "Salir a Mi entorno" según la decisión 4 |
| `src/components/ui/FormularioCrearRdt.tsx` (`router.push('/rdts/status')`), `FormularioRequerimiento.tsx` (`router.push('/requerimientos')`) | La salida tras guardar conserva el servicio |

**Solo lectura / no se tocan**: `db/**`, `src/lib/pr`, `src/lib/dashboard`, `src/lib/curva-s`, `src/lib/plan-maestro`, `src/lib/dp`, `src/middleware.ts`. `src/app/api/**` solo en las APIs que usan las funciones de permisos que cambian (tabla siguiente).

### Funciones de permisos.ts que cambian (línea base del código → flujo 14)

Esta tabla describe **el cambio de código**; los roles finales son los del flujo 14 (tablas 1 y 2) y no se repiten aquí. El Worker la completa y verifica en F0 (PL-146) y la mantiene al día.

| Función | Hoy (código) | Cambio | Usos que hay que revisar (páginas, APIs y guardias) |
|---|---|---|---|
| `puedeVerEconomia` (nueva) y las específicas `puedeVerDashboard`, `puedeVerDashboardPortafolio`, `puedeVerPr`, `puedeVerCurvaS` | Dashboard y PR sin función; Curva S excluye al rol Asistente | Economía: los cinco roles de la regla 2 | Páginas `dashboard`, `pr`, `curva-s`, dashboard del portafolio; `GET /api/curva-s`; enlaces de la ficha y de la grilla; interruptor Parcial/Completo (`ToggleTipoDashboard`, `PATCH …/tipo-dashboard`: sigue a `puedeVerEconomia`, C35 resuelta) |
| `puedeVerDp` | Sin función | Economía más supervisor de oficina técnica | Página `dp`; `dp/exportar` |
| `puedeVerPlanMaestro` | Excluye al rol Asistente | Economía más planner | `plan-maestro`; `GET /api/plan-maestro`; enlace de la ficha |
| `puedeVerRegistroCostos` (nueva) | La página abre si puede subir o descargar | Economía; logística entra solo para subir | `registro-costos` (página y API) |
| `puedeSubirRegistroCostosServicio` | Logística | Sin cambio de roles; la pantalla pasa a modo "solo subir" para logística | `registro-costos` |
| `puedeDescargarRegistroCostosServicio` | Jefe de proyectos | Suma administrador (decidido 2026-09-28; es una acción de la tabla 2) | API `registro-costos` GET y control de descarga de la pantalla |
| Descargas y exportaciones (`…/dp/exportar`, `…/requerimientos/exportar`, `rdts/exportar`, `rdts/partes/[id]/pdf`, `rdts/[id]/archivo`, `requerimientos/formato-vacio`, `cronograma/plantilla`) | `dp/exportar` y `requerimientos/exportar` sin guardia de rol; las de RDT usan `puedeVerRdts`; `cronograma/plantilla` usa `puedeSubirCronograma` | Misma regla que "ver" para las propuestas del artefacto (supuesto A12); lo no listado en el artefacto se reporta (A13) | PL-152 a PL-156 |
| `puedeVerCronograma`, `puedeVerPaquetesTrabajo`, `puedeVerRdts`, `puedeVerConsolidadoRq`, `puedeVerRecursos`, `puedeVerStatusRequerimiento` (nueva) | Restringidas (excluyen roles) o sin función (Status RQ) | Los 13 roles | Ver fila F2B de "Fases" |
| `puedeDescargarConsolidadoRq` | Alias de `puedeVerConsolidadoRq` | Se desacopla: conserva su conjunto actual (nota 5 del flujo 14) | `logistica/requerimientos/exportar-004`, chip |
| `puedeAdjudicarProyecto`, `puedeCrearPrograma`, `puedeCrearPortafolio` | Jefe de oficina técnica | Suma administrador y jefe de proyectos | `programas/**`, `proyectos/nuevo`, `api/proyectos`, `siguiente-ot`, `api/programas`, `api/portafolios` |
| `puedeConfirmarTransicionEstado` | Jefe de oficina técnica | Suma administrador y jefe de proyectos | Ficha del servicio; `confirmar-transicion` |
| `puedeArchivarProyecto`, `puedeEliminarProyecto` | Administrador y jefe de oficina técnica | Cambia el jefe de oficina técnica por el jefe de proyectos | Ficha, portafolio, archivados; `api/proyectos/[id]` |
| `puedeEliminarContenedor` | Administrador | Suma jefe de proyectos | `programas/**`; APIs de programas y portafolios |
| `puedeEditarServicio` (nueva) | Usa `puedeAdjudicarProyecto` | Función propia | `proyectos/[id]/editar`; `api/proyectos/[id]/datos`; enlace de la ficha |
| `puedeModificarChecklist` | Administrador y jefe de oficina técnica | Cambia el jefe de oficina técnica por el jefe de proyectos | `checklist/editar`; `api/proyectos/[id]/checklist`; ficha |
| `puedeImportarDp` (nueva) | `puedeSubirDocumento` con el supervisor de oficina técnica como responsable | Función propia: ya no importa el supervisor de oficina técnica | Página `dp`; `POST api/proyectos/[id]/dp` |
| `puedeEditarPerfilExtendido` | Administrador, jefe de oficina técnica y jefe de proyectos | El jefe de oficina técnica deja de tenerla | Perfil (página y API) |
| `puedeCrearRdtEstructurado` | Administrador, jefe de proyectos y supervisor operativo | Suma jefe de oficina técnica | `rdts/crear`; `api/rdts/partes` POST; `catalogos`; `plantillas`; chips |
| `puedeCorregirRdt` (nueva) | Usa `puedeCrearRdtEstructurado` | Función propia (el jefe de oficina técnica no corrige) | `api/rdts/partes/[id]` PUT; `rdts/status` |
| `puedeValidarRdt` | Administrador y jefe de proyectos | Suma jefe de oficina técnica | `rdts/status`; `api/rdts/partes/[id]` PATCH |
| `puedeRechazarRdtValidado` (nueva) | Usa `puedeValidarRdt` | Función propia (el jefe de oficina técnica no rechaza uno ya validado) | PATCH RECHAZAR sobre un RDT VALIDADO |
| `puedeEliminarRdt` | Administrador | Suma jefe de proyectos | `rdts/listado`; `api/rdts/[id]`; `api/rdts/partes/[id]` DELETE |
| `puedeCrearRequerimiento` | Todos menos administrador | Los 13 roles | `mi-entorno`, `proyectos/[id]/requerimientos/nuevo`, POST de RQ |
| `puedeActualizarEstadoRequerimiento` | Logística | Suma administrador | Consolidado RQ, Status RQ, notificaciones, Mi entorno; API `…/estado` |
| `puedeEliminarRequerimiento` | Administrador | Suma jefe de proyectos | `requerimientos`; `…/requerimientos/[rqId]` DELETE |
| **Sin cambio (se verifican)** | `puedeSubirRdt`, `puedeSubirCronograma`, `puedeGestionarPlanMaestro`, `puedeGestionarPaquetesTrabajo`, `puedeGestionarCatalogoCnc`, `puedeGestionarUsuarios`, `puedeAsignarRolAdministrador`, `puedeSimularRol`, `puedeSubirDocumento`, `puedeComentarRequerimiento`, `puedeDerivarRequerimientoLogistica` | Igual que la tabla 2 | Regresión (PL-145) |

**Documentación en `pg_control_proyectos` (F7, tras consultar a Victor)**: `04-flujos-de-negocio/16-paneles.md`, `01-configuracion.md`, `14-accesos-y-restricciones.md` y, según lo que corresponda, `03-entorno.md`, `05-rq.md`, `06-rdt.md`, `11-dashboard.md`, `15-cronograma.md`, `21-curva-s.md`; `01-contexto-repositorio/05-diseno-y-ui.md`; `05-diseno-y-referencias/design.md` (chip deshabilitado, registro, política); `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (corrección ya anotada en "Mejoras"); mejoras nuevas en `03-aprendizaje-continuo/`; `02-progreso/` y `03-evidencia/` de este plan; `docs/README.md` y `01-planes/README.md`.

## Punch List embebida

Formato de `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia de cada ítem va en `02-trabajo-activo/03-evidencia/2026-09-27-paneles-servicio-persistente.md`.

### Estado de aprobación

Gate 1: **pendiente** (versión 5 del plan: alineada con la matriz de permisos aprobada por Victor el 2026-09-28 y con el flujo 14 reescrito; ítems nuevos PL-128 a PL-181 y reescritos los de permisos. Ya no hay ítems condicionados). **Versión 8 (2026-09-29):** PL-181 cerrado (`No aplica`) y PL-90 ajustado por C35; la lista se ejecuta por tandas (ver «Tandas de ejecución y trazabilidad ítem → tanda»); 180 ítems abiertos. Victor aprueba esta lista **antes** de implementar (protocolo de verificación). Una vez aprobada, el Worker la verifica él mismo con Playwright y no entrega con ítems abiertos.

### Método, cuentas y datos de prueba (aplica a todos los ítems)

- **Cuenta A**: perfil con permisos altos. **Cuenta B**: perfil sin permisos de administración (el Worker anota en la evidencia el rol de B, tal como lo muestra el pie del panel izquierdo, y calcula los resultados esperados con la matriz base del flujo 14; si B tiene varios roles, el resultado es la unión). Las credenciales viven fuera del repositorio y nunca se copian a archivos ni al chat.
- **SV1**: un servicio vigente con DP, cronograma y Plan Maestro (el que el Worker elija entre los existentes; se nombra por N° OT en la evidencia). **SV2**: otro servicio vigente. **SVX**: un servicio sobre el que la cuenta B no tiene alcance (`proyecto_miembros`); si no existe ninguno, el Worker lo declara como limitación en la evidencia.
- **Solo lectura**: ninguna verificación guarda, borra ni sube datos reales. Las acciones (Generar RQ, Crear RDT, Subir RDT, Crear paquete) se prueban hasta abrir su formulario con el servicio preseleccionado; la salida tras guardar se prueba con la prueba unitaria del helper y la revisión de código.
- **Tamaños**: escritorio (1440 px de ancho) y móvil (390 px de ancho).
- **Playwright**: leer con `textContent()` y no con `innerText()` (hay etiquetas con `uppercase`); esperar la condición real (URL, atributo) y no un tiempo fijo; encadenar las navegaciones una a una sobre el mismo navegador (en paralelo se pisan).
- **Verificación de roles**: la cuenta A puede simular cada uno de los 13 roles con "Ver como" (el servidor trata la sesión con los roles simulados). La verificación se hace **contra las tablas 1 y 2 del flujo 14 leídas del propio archivo** (una fila = una interfaz o una acción y sus APIs): el plan no duplica las tablas. No sustituye a la cuenta B: complementa.
- **Acciones sin escribir**: los permisos de acciones se prueban con (1) el estado del botón o chip en pantalla, (2) pruebas unitarias de cada función de `permisos.ts` para los 13 roles y (3) llamadas a la API sin efecto: id inexistente o cuerpo inválido, donde **403 por rol = rechazado** y 404 o 400 = pasó la guardia de rol (nunca se envía un cuerpo válido a un servicio real). Ojo: "Ver como" cambia los roles pero el alcance por OT (`proyecto_miembros`) sigue siendo el del usuario real, así que un 403 por falta de OT puede parecerse a un 403 por rol; se distinguen por el mensaje de la respuesta y por las pruebas unitarias.

**Fuente única de los roles por interfaz:** sección "Matriz base de visibilidad por interfaz" (y "Acciones que cambian con esta decisión") de `docs/04-flujos-de-negocio/14-accesos-y-restricciones.md`. No se copia en este plan; el Worker la lee del archivo. La tabla siguiente **no lista roles por interfaz**: registra el estado del código el 2026-09-27 (línea base) y la fase que lo cambia. Abreviaturas de rol como en el flujo 14.

| Interfaz | Función y guardia en el código hoy | Fase que la cambia |
|---|---|---|
| Cronograma | `puedeVerCronograma` (excluye al rol Asistente); guardia en la página y en `GET /api/cronograma` | F2B |
| Paquetes de Trabajo | `puedeVerPaquetesTrabajo` (excluye al rol Asistente); página y API | F2B |
| RDTs: status, archivo, consolidado | `puedeVerRdts` (7 de los 13 roles); páginas y `GET /api/rdts/consolidado` | F2B |
| RQ: status | Sin guardia de rol (solo sesión); página y `GET /api/proyectos/[id]/requerimientos` | F2B (`puedeVerStatusRequerimiento`, nueva) |
| RQ: consolidado (ver) | `puedeVerConsolidadoRq` (4 roles); página y `GET /api/logistica/requerimientos`; `puedeDescargarConsolidadoRq` es su alias | F2B (la descarga se desacopla y no cambia, F5C) |
| Recursos de empresa: Personal, Cargos, Equipos | `puedeVerRecursos`, alias de `puedeVerApartadoProyectos` (administrador y jefe de proyectos); páginas y `GET /api/recursos*` | F2B |
| Recursos: Causas CNC (consulta) | `puedeGestionarCatalogoCnc` en página y API, sin separar consulta de gestión | F2B (separa consulta de gestión) |
| Ficha del servicio, grilla del portafolio, Notificaciones, Mi entorno | Sin guardia de rol | Sin cambio |
| Dashboard del servicio | Sin guardia de rol; el interruptor Parcial/Completo usa `puedeAdjudicarProyecto` | F5B |
| Dashboard del portafolio | Sin guardia de rol; fuera del shell (`app/programas/…`) | F5B |
| PR | Sin guardia de rol | F5B |
| DP (ver) | Sin guardia de rol para ver; importar: `puedeSubirDocumento` con el supervisor de oficina técnica como responsable | F5B (ver); F5C (importar, función propia) |
| Curva S | `puedeVerCurvaS` (excluye al rol Asistente) más alcance sobre la OT (`tieneAlcanceSobreProyecto`) | F5B |
| Plan Maestro (ver y gestionar) | `puedeVerPlanMaestro` (excluye al rol Asistente) y `puedeGestionarPlanMaestro` (administrador, jefe de proyectos, planner) | F5B (ver); gestionar sin cambio |
| Registro de costos | Subir: `puedeSubirRegistroCostosServicio` (logística); descargar: `puedeDescargarRegistroCostosServicio` (jefe de proyectos); la página abre si puede alguna | F5B (ver); F5C (modo "solo subir" y descarga: suma administrador) |
| Crear RDTs | `puedeCrearRdtEstructurado` | F5C |
| Editar servicio, Editar checklist | `puedeAdjudicarProyecto` para editar servicio y `puedeModificarChecklist` | F5C (`puedeEditarServicio` propia) |

### Ítems funcionales

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-01 | F2 | Cuenta A abre SV1 desde "Todos los servicios": el panel izquierdo muestra el servicio actual (N° OT y nombre) y el panel derecho tiene sus chips activos | Captura de ambos paneles y URL | Conforme |
| PL-02 | F2 | Cronograma con SV1: `?proyectoId=` en la URL, ambos paneles con SV1 y selector de OT = SV1 | Captura + URL | Conforme |
| PL-03 | F2 | Paquetes de Trabajo con SV1: ídem PL-02 | Captura + URL | Conforme |
| PL-04 | F2 | Plan Maestro con SV1: ídem PL-02 | Captura + URL | Conforme |
| PL-05 | F2 | Crear RDTs con SV1: selector de OT = SV1 y ambos paneles con SV1 | Captura + URL | Conforme |
| PL-06 | F2 | Status de RDTs con SV1: ambos paneles con SV1 y filtro N° OT = SV1 (no aparecen filas de otros servicios) | Captura + URL | Conforme |
| PL-07 | F2 | Archivo de RDTs subidos con SV1: ídem PL-06 | Captura + URL | Observado |
| PL-08 | F2 | Consolidado RDTs con SV1: selector de servicio = SV1 y consolidado cargado sin clic adicional | Captura + URL | Conforme |
| PL-09 | F2 | Status de Requerimiento con SV1: ambos paneles con SV1 y filtro de OT = SV1; si se cambia la multiselección `ots` de la tabla, el contexto de los paneles sigue siendo SV1 | Captura + URL | Conforme |
| PL-10 | F2 | Consolidado RQ con SV1: ambos paneles con SV1 y filtro N° OT = SV1 | Captura + URL | Conforme |
| PL-11 | F2 | Notificaciones, Mi entorno (`?accion=crear-rq` y `?accion=subir-rdt`) y Recursos de empresa (Personal, Cargos, Equipos): los paneles conservan SV1 | Captura + URL de cada una | Conforme |
| PL-12 | F2 | DP, PR, Dashboard, Curva S y Registro de costos (rutas `/proyectos/<id>/…`): ambos paneles con SV1 (regresión de lo que ya funcionaba) | Captura + URL de cada una | Observado |
| PL-13 | F2 | `/proyectos/<SV1>/requerimientos` redirige a Status de Requerimiento y los paneles conservan SV1 | URL final + captura | Conforme |
| PL-14 | F2 | Cambiar de servicio (SV1 a SV2) con el selector de una pantalla: la URL y ambos paneles pasan a SV2 | URL antes y después + captura | Conforme |
| PL-15 | F2 | Volver a "Todos los servicios" y elegir SV2: los paneles muestran SV2 sin restos de SV1 | Captura | Conforme |
| PL-16 | F2 | "Todos los servicios" limpia el servicio: paneles sin servicio, los chips que requieren servicio quedan inertes y los que funcionan sin servicio (Plan Maestro, Status de Requerimiento, Consolidado RQ, Status de RDTs) navegan como en la línea base | Captura + comparación con la línea base de F0 | Conforme |
| PL-17 | F2 | Recargar (F5) y usar Atrás/Adelante conservan el servicio; pegar la URL en una pestaña nueva lo restaura | Secuencia de URL y capturas | Conforme |
| PL-18 | F2 | Ninguna pantalla de PL-02 a PL-13 muestra "Selecciona un servicio…" con servicio elegido (no hay parpadeo del mensaje durante la carga) | Tabla ruta → resultado + captura de la carga | Conforme |
| PL-19 | F2 | Redirección del servidor por falta de permiso: la cuenta B abre por URL una pantalla que no puede usar con `?proyectoId=SV1` y aterriza en Mi entorno conservando SV1 | URL final + captura | Conforme |
| PL-20 | F2 | Las salidas tras guardar (Crear RDTs a Status de RDTs, Crear RQ a Status de Requerimiento) y `CabeceraPagina` conservan el servicio | Prueba unitaria del helper + revisión de código (sin guardar datos reales) | Conforme |
| PL-21 | F2 | El chip "Salir a Mi entorno" se comporta según la decisión 4 aprobada (con servicio, va a `/mi-entorno?proyectoId=…`) | Captura antes y después de hacer clic | Conforme |
| PL-22 | F3 | Con servicio, el panel izquierdo muestra los grupos acordados (decisiones 5 y 6): Alcance y presupuesto, Planificación, Recursos del servicio, Documentación, Reportes, y el grupo Servicio si se aprueba; las acciones van separadas de los informativos | Captura | Conforme |
| PL-23 | F3 | Cada chip del panel izquierdo cuya pantalla existe abre esa pantalla con SV1 (DP, Paquetes de Trabajo, Cronograma, Plan Maestro, Consolidado RDTs, Requerimiento, PR, Dashboard, Curva S, Registro de costos y, si se aprueba, Ficha del servicio, Editar servicio y Editar checklist) | Tabla chip → URL → servicio visible | Conforme |
| PL-24 | F3 | Los chips sin pantalla (Alcance, Presupuesto, Cargos HH, Equipos HM, Planos, PETS y los que fije la decisión 5) se ven, no tienen enlace, el clic no cambia la URL y no hay error en consola | Captura + registro de consola | Conforme |
| PL-25 | F3 | Acciones: Generar RQ abre Crear RQ con SV1; Crear RDT abre Crear RDTs con SV1; Crear paquete abre Paquetes de Trabajo con SV1 y el formulario de paquete nuevo abierto; Subir RDT abre su formulario con SV1. Ninguna guarda al abrir | Captura de cada formulario | Conforme |
| PL-26 | F3 | Las acciones quedan fijadas al servicio actual (según E1): el formulario abre con SV1 y, si se cambia el servicio dentro de la acción, la URL y los paneles lo siguen (no puede haber dos servicios distintos a la vez) | Captura antes y después | Conforme |
| PL-27 | F3 | Recursos de empresa: botón mostrar/ocultar; sin servicio aparece visible por defecto y con servicio, oculto por defecto; el botón funciona en ambos casos; abrir Personal, Cargos o Equipos no cierra el servicio; el apartado es visible y accesible para los 13 roles (A4 ampliado por la matriz base) | Capturas en los dos estados y con las dos cuentas | Conforme |
| PL-28 | F3 | "Materiales" ya no aparece en Recursos de empresa | Captura | Conforme |
| PL-29 | F3 | El pie del panel izquierdo (Usuarios, Notificaciones, Configuraciones, Cerrar sesión, "Ver como", Mi entorno) sigue funcionando, no queda tapado por el nuevo contenido y sus enlaces llevan el servicio | Captura y clic en cada uno | Conforme |
| PL-30 | F4 | Dentro de SV1, cada chip del panel derecho cuya pantalla usa selector de OT (Crear RDTs, Subir RDTs, Crear RQ, Consolidado RDTs, Cronograma, Paquetes de Trabajo, Plan Maestro) abre con SV1 ya elegido en el selector | Tabla chip → valor del selector | Conforme |
| PL-31 | F4 | Dentro de SV1, cada chip cuya pantalla filtra por N° OT (Status de RDTs, Archivo de RDTs, Requerimiento, Consolidado RQ) abre con el filtro = SV1 | Tabla chip → filtro | Conforme |
| PL-32 | F4 | Dentro de SV1, cada chip con ruta de servicio (DP, PR, Dashboard, Curva S, Registro de costos) abre con SV1 | Tabla chip → URL | Conforme |
| PL-33 | F4 | Recorrido completo de los 7 grupos del panel derecho y de "Accesos rápidos": ningún chip cuya pantalla existe queda sin el servicio (una fila por chip, sin excepciones) | Tabla completa de chips | Conforme |
| PL-34 | F4 | El valor preseleccionado se puede cambiar y la pantalla responde (selector o filtro) | Captura antes y después | Conforme |

### Datos y cálculos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-35 | F1 a F7 | No hay migraciones ni cambios en `db/` ni en tablas: el diff de `local-worker-1` contra `main` no toca `db/` | `git diff --stat` | Conforme |
| PL-36 | F1 a F7 | El diff no toca `src/lib/pr`, `dashboard`, `curva-s`, `plan-maestro` ni `dp` (los cálculos EVM no cambian); en las páginas de PR, Dashboard (servicio y portafolio), DP, Curva S, Plan Maestro y Registro de costos solo cambia la guardia (F5B) | `git diff --stat` + revisión del diff de esas páginas | Conforme |
| PL-37 | F2 | El N° OT y el nombre que muestra el panel izquierdo corresponden al `id` de la URL (SV1 y SV2) | Captura + comparación con la ficha del servicio | Conforme |

### Permisos (por los dos lados)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-38 | F3 | Cuenta A con SV1: cada chip del panel izquierdo está habilitado o deshabilitado según la matriz base del flujo 14 y sus acciones (administrador y jefe de proyectos con acceso a todo, según lo que resuelva CO5); las diferencias con el código vigente se listan, no se corrigen en silencio | Tabla chip → estado esperado → estado real | Conforme |
| PL-39 | F3 | Cuenta B con SV1: el panel izquierdo **es visible** (antes no lo era); los chips que su rol no puede usar están deshabilitados con `opacity-40`, `cursor-not-allowed` y título explicativo; los que puede usar están activos | Tabla + captura | Conforme |
| PL-40 | F3 | Cuenta B: hacer clic en un chip deshabilitado no navega (URL sin cambios) y no hay error en consola | Captura + consola | Conforme |
| PL-41 | F4 | Cuenta B: en el panel derecho los chips que su rol no puede usar aparecen deshabilitados con título (según la decisión 3 aprobada; si se decide mantener el comportamiento actual, el ítem se reescribe en el Gate 1) | Tabla + captura | Conforme |
| PL-42 | F4 | Cuentas A y B: Mi entorno conserva los mismos chips que en la línea base (A3); su estado habilitado o deshabilitado sigue la matriz base (cambia respecto de la línea base solo donde la matriz lo decide) y ahora envían el servicio | Comparación con la línea base de F0 | Conforme |
| PL-43 | F6 | Verificación de los 13 roles con "Ver como" desde la cuenta A: para cada rol, el estado de cada chip del panel izquierdo, del derecho y de Mi entorno coincide con la matriz base del flujo 14 (leída del archivo, no copiada) | Tabla 13 roles × chips generada contra la matriz | Conforme |
| PL-44 | F6 | **Ver no es acceder.** Cuenta B, por URL directa (con `?proyectoId=`), a cada pantalla cuyo chip esté deshabilitado para su rol según la matriz base (con la cuenta B, típicamente las interfaces con economía, Editar servicio y Editar checklist): el servidor responde con la guardia de la pantalla (redirección o mensaje) y no muestra datos | URL, resultado y captura de cada una | Conforme |
| PL-45 | F6 | Cuenta B, por URL directa, a las interfaces con economía (PR, Dashboard, DP, Curva S, Plan Maestro, Registro de costos y dashboard del portafolio): rechazo según la matriz base; detalle en PL-89 a PL-91 y PL-122 a PL-124 | Remite a esos ítems | Conforme |
| PL-46 | F6 | Cuenta B, desde el navegador con la sesión iniciada, llama a `GET /api/cronograma`, `/api/rdts/consolidado` y `/api/curva-s` con `proyectoId` de SV1, de SVX y con un id inexistente: las dos primeras responden según la matriz base (los 13 roles) y `/api/curva-s` rechaza a un rol fuera de la matriz; con id inexistente, respuesta 4xx clara y nunca 500 ni datos de un servicio sin alcance | Respuestas registradas | Conforme |
| PL-47 | F2 | `?proyectoId=` inexistente, de un servicio archivado o sin acceso: el shell no falla, trata la sesión como sin servicio (o muestra un aviso claro) y no revela nombre ni datos del servicio | Captura + consola | Conforme |
| PL-48 | F3 | "Ver no es modificar": dentro de las pantallas, los botones de acción (Consolidado RQ, Status de RDTs, Paquetes de Trabajo, Recursos) siguen la matriz de acciones del flujo 14 (con los cambios de F5C); poder ver una interfaz no habilita ninguna acción | Comparación con la línea base y con el flujo 14 | Conforme |
| PL-49 | F3 | Recursos de empresa visible y accesible para los 13 roles: con la cuenta A y con la cuenta B los chips de Personal, Cargos, Equipos y Causas CNC (consulta) están activos y sus pantallas abren; el alta y la baja de Causas CNC solo aparecen para administrador y jefe de proyectos y las llamadas de escritura con otro rol responden 403 | Captura de cada cuenta + respuesta de la API | Conforme |

### Registro único y estándar de interfaz nueva

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-50 | F1 | Existe un único registro de accesos; `NAV_PROYECTO`, `herramientasPorGrupo`, `CHIPS_ACCESO_RAPIDO`, `hrefItemPanel` y las rutas fijas del panel izquierdo derivan de él: no queda ninguna lista paralela de chips | Búsqueda de código (`rg`) + diff | Conforme |
| PL-51 | F1 | Cada acceso tiene todos los metadatos (id, nombre, grupo, tipo, ruta o acción, requiere servicio, permiso, visibilidad por panel) y la prueba de integridad lo comprueba (ids únicos, sin rutas sin permiso declarado por omisión silenciosa) | `npm test` | Conforme |
| PL-52 | F1 | Migración completa: los 41 ítems de `NAV_PROYECTO`, los 10 chips de Mi entorno, los 7 de Accesos rápidos y los 4 de Recursos de empresa que se conservan (Personal, Cargos, Equipos y Causas CNC; "Materiales" se elimina y no se migra) están en el registro; tabla clave anterior → id nuevo sin pérdidas; las únicas diferencias visibles son las declaradas (por ejemplo la unión de `rdt` y `subir-rdt`, y E3 según la respuesta de Victor) | Tabla de mapeo + prueba de equivalencia | Conforme |
| PL-53 | F5 | Prueba de humo automática: una función pura recibe un registro con **una** entrada de prueba nueva y esa entrada aparece en panel izquierdo, panel derecho, Mi entorno, con `?proyectoId=`, con estado por permiso y como fila de la matriz | `npm test` | Conforme |
| PL-54 | F6 | Prueba de humo en vivo: añadir una entrada de prueba **solo en el registro** (sin commitearla) y comprobar con Playwright, con las dos cuentas, que aparece en los paneles correspondientes, conserva el servicio, se habilita o deshabilita por permiso y sale en la matriz, sin tocar ningún otro archivo; se revierte y el diff final no la contiene | Captura + `git status` con un solo archivo modificado, luego limpio | Conforme |
| PL-55 | F5 | Prueba de cobertura: falla si existe una pantalla del workspace sin entrada en el registro ni excepción declarada. Se demuestra en rojo (página temporal, sin commitearla) y en verde | Salida de `npm test` en rojo y en verde | Conforme |
| PL-56 | F5 | Función de matriz derivada del registro: produce roles × accesos; se **compara** con la matriz base del flujo 14 y las diferencias quedan listadas en la evidencia (la matriz base es la fuente: el registro se ajusta a ella, no al revés) | Lista de diferencias | Conforme |
| PL-57 | F5 | Prueba de fuente: ningún `redirect('/mi-entorno')` ni enlace literal a una pantalla de servicio en el workspace pierde el servicio (o está en una lista de excepciones con motivo) | `npm test` | Conforme |
| PL-58 | F7 | Política de "interfaz nueva" escrita en el flujo 16 y en `05-diseno-y-ui.md` con el texto aprobado en el Gate 1, con su plantilla de ítems de Punch List | Diff de `pg_control_proyectos` | Conforme |

### Permisos: interfaces (tabla 1 del flujo 14; fases F2B y F5B)

**Fuente única:** las tablas 1 y 2 de `docs/04-flujos-de-negocio/14-accesos-y-restricciones.md`. No se copian aquí: el Worker las lee del archivo y compara. En estos ítems, "rol Asistente" es el rol de usuario, no el chat. Nada está condicionado.

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-88 | F2B y F5B | `permisos.ts`: las funciones de ver de las interfaces sin economía permiten a los 13 roles (F2B); `puedeVerEconomia` cubre los cinco roles de la regla 2 como único punto de cambio y las específicas delegan en ella, con las excepciones del planner (Plan Maestro) y el supervisor de oficina técnica (DP) (F5B); `puedeVerRecursos` ya no es alias de `puedeVerApartadoProyectos`. Las pruebas unitarias recorren los 13 roles y comparan con la tabla 1 leída del flujo 14 | `npm test` + salida de la comparación | Conforme |
| PL-89 | F5B | PR: los roles de la tabla 1 abren `/proyectos/<SV1>/pr` con datos; con "Ver como" un rol fuera (por ejemplo supervisor operativo) ve "No tienes acceso…" sin datos y sin error 500 | Capturas de los tres casos | Conforme |
| PL-90 | F5B | Dashboard del servicio (Parcial y Completo): ídem PL-89 en `/proyectos/<SV1>/dashboard`; el interruptor Parcial/Completo (`ToggleTipoDashboard` y `PATCH /api/proyectos/[id]/tipo-dashboard`) sigue a `puedeVerEconomia`: lo activan los roles con datos económicos de la matriz y se comprueba por los dos lados (C35 resuelta por Victor el 2026-09-29; que los demás roles vean un Parcial sin economía es del plan futuro de `planes-futuros.md`) | Capturas | Conforme |
| PL-91 | F5B | DP (ver): ídem PL-89 en `/proyectos/<SV1>/dp`, con el supervisor de oficina técnica dentro y el planner fuera; el botón de importar sigue la fila "Importar DP" de la tabla 2 (PL-134) | Capturas | Conforme |
| PL-92 | F2B | Status de Requerimiento: los 13 roles (con "Ver como") abren `/requerimientos` y cada rol que crea RQ ve su lista; sin sesión lleva a `/login`; un usuario sin ningún rol conocido es rechazado (prueba unitaria) | Tabla 13 roles + captura | Conforme |
| PL-93 | F2B y F5B | APIs, desde el navegador con la sesión iniciada: las de interfaces sin economía (`GET /api/proyectos/<SV1>/requerimientos` y su exportación, `/api/logistica/requerimientos`, `/api/recursos*`, `/api/paquetes-trabajo`) responden a los 13 roles; las de economía (`…/dp/exportar`, `GET /api/curva-s`, `GET /api/plan-maestro`, `…/registro-costos`) responden 403 a un rol fuera de la tabla 1 | Respuestas registradas | Conforme |
| PL-94 | F2B | `GET /api/proyectos/<SV1>/partidas` no se restringió: con "Ver como" rol Asistente, Crear RQ carga las partidas y abre su formulario (sin guardar) | Captura | Conforme |
| PL-95 | F2B y F5B | Los chips de interfaces sin economía están activos para los 13 roles (F2B); los de economía usan las funciones nuevas como `permiso` del registro: para un rol fuera de la tabla 1 aparecen deshabilitados con título en los tres paneles y en Accesos rápidos, y para uno dentro, activos | Tabla chip × rol + captura | Observado |
| PL-96 | F6 | Verificación de los 13 roles contra las tablas 1 y 2 del flujo 14 leídas del archivo (una fila = una interfaz o acción y sus APIs): el resultado del servidor y el estado del chip o botón coinciden columna por columna; el plan no duplica las tablas | Tabla generada contra el flujo 14 | Conforme |
| PL-97 | F6 | Informe "qué cambió por rol respecto de la línea base de F0" contra la **tabla 1 y la tabla 2 completas**: rol × interfaz y rol × acción, antes y después. Cambian solo las celdas que el flujo 14 decide; cualquier otro cambio es un hallazgo. Victor revisa esta tabla | Tabla en la evidencia | Conforme |
| PL-98 | F5B | Enlaces internos: la ficha del servicio, su checklist de documentos (que enlaza a PR y DP) y la grilla del portafolio (enlace al dashboard) no muestran a un rol fuera de la tabla 1 un enlace que lleve a una pantalla rechazada | Captura con "Ver como" | Conforme |
| PL-99 | F5B y F5C | La referencia de F5B y F5C es la versión aprobada del flujo 14 (commit 8027037, artefacto versión 17); el Worker anota en el progreso el commit del flujo 14 contra el que verifica y, si cambia durante la tarea, lo comunica al Orquestador antes de seguir | Nota en el progreso | Conforme |
| PL-100 | F7 | El flujo 14 aprobado (tablas 1 y 2) coincide con lo implementado; solo se toca si Victor decide algo nuevo (las tres descargas propuestas, A12), con consulta previa y sin dejar dos versiones conviviendo | Diff de `pg_control_proyectos` (vacío o con la decisión) | Conforme |
| PL-101 | F5B | La guardia se evalúa antes de leer datos del servicio: para un rol fuera de la tabla 1 no se ejecutan consultas de datos de PR, DP, Dashboard, Curva S, Plan Maestro ni Registro de costos y la respuesta no revela nombre ni datos del servicio | Revisión de código + captura | Observado |
| PL-119 | F2B | Cronograma, Paquetes de Trabajo, RDTs (status, archivo de subidos, consolidado) y consolidado RQ (ver) abren para los 13 roles, incluido el rol Asistente; las acciones dentro de cada pantalla siguen la tabla 2 | Tabla rol × pantalla con "Ver como" + capturas | Conforme |
| PL-120 | F2B | Recursos de empresa (Personal, Cargos, Equipos, Causas CNC en consulta) abren para los 13 roles, en páginas y APIs de lectura; gestionar Causas CNC (alta y baja) sigue solo con las filas de la tabla 2, en pantalla y en API | Capturas + respuestas de la API | Conforme |
| PL-121 | F2B | Las interfaces declaradas sin datos económicos no muestran dinero (USD ni S/: costos, precios, tarifas, valores): revisión de Consolidado RDTs, Paquetes de Trabajo, Status y archivo de RDTs, RQ, Recursos de empresa, ficha del servicio y grilla del portafolio. Si aparece alguno, es un hallazgo que se devuelve a Victor antes de seguir | Revisión de código + capturas | Conforme |
| PL-122 | F5B | Dashboard del portafolio (`app/programas/…/dashboard`, fuera del shell): los roles de la tabla 1 lo ven; los demás reciben "No tienes acceso…" con enlace de vuelta a la grilla del portafolio, sin datos y sin error 500 | Capturas por rol + respuesta | Conforme |
| PL-123 | F5B | Plan Maestro (ver) y Curva S: Plan Maestro para los roles de economía más el planner; Curva S solo economía (el rol Asistente ya no entra por la excepción del código vigente); gestionar Plan Maestro no cambia | Capturas por rol + API | Conforme |
| PL-124 | F5B | Registro de costos, ver: según la tabla 1 (la descarga es una acción, PL-126); logística entra a la pantalla en modo "solo subir" (sin descarga, sin fecha ni contenido del archivo); la pantalla no rechaza a quien deba subir | Capturas por rol | Conforme |
| PL-125 | F5B | Las excepciones acotadas se aplican tal como quedaron aprobadas, en un solo lugar (`puedeVerEconomia` y las específicas): planner solo en Plan Maestro; supervisor de oficina técnica solo en DP (y sin importar); jefe de costos con economía; se comprueban por los dos lados con "Ver como" | Tabla por rol | Conforme |

### Permisos: acciones (tabla 2 del flujo 14; fase F5C)

Para cada acción que **cambia de permiso** respecto del código: se prueban por los dos lados los 13 roles con "Ver como" desde la cuenta A (estado del botón o chip, prueba unitaria de la función y llamada sin efecto a la API) y, con las dos cuentas, el caso que cada una pueda representar. "Cambia" indica solo el delta frente a la línea base; los roles exactos de cada fila son los del flujo 14.

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-128 | F5C | Adjudicar proyecto, crear programa y crear portafolio: **suma administrador y jefe de proyectos** (el jefe de oficina técnica conserva); el resto de roles, sin acceso | Tabla 13 roles (UI, prueba unitaria, API sin efecto) | Conforme |
| PL-129 | F5C | Confirmar transición de estado: **suma administrador y jefe de proyectos**; se mantiene la precondición del Plan Maestro aprobado (validada en servidor, no se ejecuta la transición) | Tabla 13 roles + revisión del guardia | Conforme |
| PL-130 | F5C | Archivar y eliminar proyecto: **el jefe de proyectos entra y el jefe de oficina técnica sale**; administrador conserva | Tabla 13 roles; DELETE con id inexistente (403 o 404) | Conforme |
| PL-131 | F5C | Eliminar contenedor (programa y portafolio): **suma jefe de proyectos** | Tabla 13 roles; DELETE con id inexistente | Conforme |
| PL-132 | F5C | Editar servicio: función propia; **entra el jefe de proyectos y sale el jefe de oficina técnica**; el enlace de la ficha y `api/proyectos/[id]/datos` usan la misma función | Tabla 13 roles; PATCH con cuerpo inválido | Conforme |
| PL-133 | F5C | Editar checklist: **entra el jefe de proyectos y sale el jefe de oficina técnica** (pantalla, enlace de la ficha y API) | Tabla 13 roles; API sin efecto | Conforme |
| PL-134 | F5C | Importar DP: función propia; **entra el jefe de proyectos y sale el supervisor de oficina técnica** (que sigue viendo el DP); el botón de importar y `POST …/dp` usan la misma función | Tabla 13 roles; POST con cuerpo inválido | Conforme |
| PL-135 | F5C | Editar perfil extendido propio: **sale el jefe de oficina técnica** | Tabla 13 roles (UI y API sin efecto) | Conforme |
| PL-136 | F5C | Crear RDT estructurado: **suma jefe de oficina técnica**; abre `rdts/crear` y el chip está activo (sin guardar) | Tabla 13 roles + captura | Conforme |
| PL-137 | F5C | Validar o rechazar RDT: **suma jefe de oficina técnica**; rechazar un RDT ya validado sigue solo con la fila propia de la tabla 2 y corregir RDT sigue sin el jefe de oficina técnica (funciones separadas) | Tabla 13 roles por las tres acciones; PATCH y PUT sin efecto | Observado |
| PL-138 | F5C | Eliminar RDT (archivo y parte estructurado): **suma jefe de proyectos**; se comprueba sin borrar (id inexistente) y con revisión del recálculo de PR que dispara | Tabla 13 roles; DELETE con id inexistente | Conforme |
| PL-139 | F5C | Crear RQ: **suma administrador** (los 13 roles); el formulario abre con servicio preseleccionado sin guardar | Tabla 13 roles + captura | Conforme |
| PL-140 | F5C | Actualizar estado de RQ (dar de alta, atendido): **suma administrador**; los botones del consolidado y del Status siguen a la misma función | Tabla 13 roles; PATCH con id inexistente | Conforme |
| PL-141 | F5C | Eliminar requerimiento: **suma jefe de proyectos** | Tabla 13 roles; DELETE con id inexistente | Conforme |
| PL-142 | F5C | Descargar consolidado RQ (PROM-GP-004): se desacopla de "ver" y conserva su conjunto actual (nota 5 del flujo 14); los 13 roles ven el consolidado pero solo esos descargan | Tabla 13 roles (botón y ruta de exportación) | Conforme |
| PL-143 | F5C | Registro de costos, modo "solo subir": logística sube y no ve ni descarga el contenido; se comprueba sin subir (control presente o ausente, y API con archivo ausente) | Capturas por rol + respuesta | Conforme |
| PL-144 | F5C | Exclusivas del administrador (asignar rol administrador y «Ver como»): sin cambio; el jefe de proyectos no las tiene (no ve el selector de "Ver como" y la API responde 403 a la asignación) | Tabla 13 roles | Conforme |
| PL-145 | F5C | Regresión de las acciones que no cambian (subir RDT, corregir RDT, subir y gestionar cronograma, gestionar Plan Maestro, gestionar paquetes, catálogo CNC, gestionar usuarios, comentar RQ, derivar RQ, subir documento del proyecto): los 13 roles coinciden con la tabla 2 | Tabla 13 roles × acciones | Conforme |
| PL-146 | F0 | Entregable de F0: lista de funciones de `permisos.ts` que cambian (la tabla "Funciones de permisos.ts que cambian" confirmada o corregida contra el código), con las páginas, APIs y guardias de servidor que las usan, sin omitir alias | Tabla en la evidencia | Conforme |
| PL-147 | F0 | Línea base "antes" por rol de la **tabla 1 y la tabla 2 completas** (no solo de las interfaces con economía): quién puede hoy cada interfaz y cada acción, en UI y servidor | Tablas rol × interfaz y rol × acción | Conforme |
| PL-148 | F5C | Sin efectos colaterales de los alias separados: `puedeEditarServicio`, `puedeImportarDp`, `puedeCorregirRdt`, `puedeRechazarRdtValidado` y `puedeDescargarConsolidadoRq` no cambian a ningún rol que la tabla 2 no cambie (por ejemplo, el jefe de oficina técnica no gana corregir RDT al ganar crear) | Pruebas unitarias por función | Conforme |
| PL-149 | F7 | Política de trazabilidad: toda interfaz, acción, permiso o acceso nuevo o cambiado en esta tarea (por ejemplo las entradas del registro único, el modo "solo subir", el asistente, Ficha del servicio, Editar servicio, Editar checklist) figura en el artefacto «Matriz de permisos» y en el flujo 14 en la misma tarea; el Auditor lo comprueba | Diff del flujo 14 + captura del artefacto actualizado | Observado |
| PL-150 | F7 | Trazabilidad por flujo: cada fila de la tabla "Trazabilidad por flujo" del plan tiene su consulta a Victor, el flujo actualizado y el enlace a la sección donde quedó aplicado; ningún flujo o documento afectado queda sin actualizar ni con referencia a la versión anterior | Tabla completada en el progreso | Conforme |
| PL-151 | F5C | Alcance por OT: las acciones que la tabla 2 marca "Requiere OT a cargo: Sí" siguen sujetas a `proyecto_miembros` para el jefe de proyectos y el jefe de oficina técnica (solo el administrador salta la restricción); la verificación distingue el rechazo por rol del rechazo por falta de OT | Tabla con mensaje de respuesta por caso | Conforme |

### Permisos: descargas y exportaciones (tabla 2 y sección «Descargas» del artefacto; F5C, con F2B y F5B)

Las descargas son acciones. Decididas: registro de costos (administrador y jefe de proyectos) y consolidado RQ (como estaba). Las tres propuestas del artefacto (RDTs y listado de RDTs, listado RQ, exportar DP) son **supuestos** (A12) hasta que Victor las apruebe. Todas se prueban sin descargar datos reales de más: con "Ver como", llamada a la API desde el navegador y lectura del código de estado.

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-126 | F5C | Descargar registro de costos por servicio: **suma administrador** (el jefe de proyectos conserva); los roles que ven la pantalla pero no descargan (jefe de oficina técnica, supervisor de costos, jefe de costos) no tienen el control y `GET …/registro-costos` les responde 403; logística tampoco descarga | Tabla 13 roles (control y API) | Conforme |
| PL-127 | F0 | Inventario de descargas y exportaciones del código (rutas de `src/app/api/` con `Content-Disposition`, `BotonDescargarPdf` y descargas por almacenamiento) contra la sección «Descargas» del artefacto y el flujo 14: lo que no figura en el artefacto se **lista y se reporta a Victor**, y su guardia actual no se cambia sin decisión | Inventario en la evidencia | Conforme |
| PL-152 | F2B y F5C | Guardias de servidor de las descargas de interfaces sin economía (`rdts/exportar` ZIP y PDF PROM-GP-0006, `rdts/partes/[id]/pdf`, `rdts/[id]/archivo`, `…/requerimientos/exportar` listado PROM-GP-008): cumplen la misma regla que "ver" su interfaz (los 13 roles, supuesto A12) y un usuario sin ningún rol conocido es rechazado; hoy `requerimientos/exportar` no tiene guardia de rol | Respuestas por rol (13 roles) | Conforme |
| PL-153 | F5B | Exportar DP (`…/dp/exportar`): solo los roles que ven el DP (economía más supervisor de oficina técnica, supuesto A12); cualquier otro rol recibe 403; hoy no tiene guardia de rol | Respuestas por rol (13 roles) | Conforme |
| PL-154 | F2B | Descargar RDTs (ZIP), listado de RDTs (PDF PROM-GP-0006) y listado RQ (PDF PROM-GP-008): habilitadas para los 13 roles (supuesto A12); el botón y la API coinciden; no se cambian los conjuntos de los demás controles de esas pantallas | Tabla 13 roles + capturas | Conforme |
| PL-155 | F0 y F7 | Descargas encontradas por el Planner y no listadas en el artefacto (plantilla de cronograma, PDF de RDT estructurado, archivo de RDT subido, PDF individual de RQ, formato vacío PROM-GP-008; por verificar: adjuntos de RQ y documentos del checklist): el Worker confirma la lista, la entrega a Victor y, si Victor las decide, actualiza el artefacto y el flujo 14 en la misma tarea | Lista en la evidencia + respuesta de Victor | Conforme |
| PL-156 | F7 | La sección «Descargas» del artefacto y la tabla 2 del flujo 14 quedan alineadas con lo decidido y con lo que el Worker implementó (registro de costos y consolidado RQ; las propuestas aprobadas o rechazadas), y el estado del artefacto deja de estar «En revisión» solo por decisión de Victor | Diff del flujo 14 + captura del artefacto | Observado |

### Alcance por OT al leer (F5B, cierra C21)

Decidido por Victor (2026-09-28): el alcance por OT es el requisito de partida para ver cualquier interfaz orientada a un servicio. Se prueba con un rol de la regla de economía (por ejemplo supervisor de costos) que SÍ tiene el permiso pero NO tiene esa OT asignada en `proyecto_miembros`: debe rechazar igual que hoy rechaza Curva S. El administrador salta el alcance (bypass ya resuelto por el helper existente).

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-174 | F5B | PR (`/proyectos/[id]/pr`): un rol con permiso de economía pero sin esa OT asignada ve "No tienes acceso…" sin datos, igual que Curva S; con la OT asignada, abre normalmente | Capturas de los dos casos + SVX | Observado |
| PL-175 | F5B | Dashboard del servicio: mismo patrón que PL-174 en `/proyectos/[id]/dashboard` | Capturas + SVX | Observado |
| PL-176 | F5B | Dashboard del portafolio (`app/programas/…/dashboard`, fuera del shell): mismo patrón; el mensaje enlaza de vuelta a la grilla del portafolio | Capturas + SVX | Observado |
| PL-177 | F5B | DP (ver): mismo patrón en `/proyectos/[id]/dp` y en `…/dp/exportar` | Capturas + respuesta de la API | Observado |
| PL-178 | F5B | Plan Maestro (ver): mismo patrón en `/plan-maestro?proyectoId=` y en `GET /api/plan-maestro`; el planner (excepción de la tabla 1) también queda sujeto al alcance | Capturas + respuesta de la API | Observado |
| PL-179 | F5B | Registro de costos: mismo patrón en `/proyectos/[id]/registro-costos` y en su API; logística (modo "solo subir") también queda sujeta al alcance para esa OT | Capturas + respuesta de la API | Observado |
| PL-180 | F6 | El administrador salta el alcance en las seis pantallas (bypass ya resuelto por el helper existente); se comprueba que sigue entrando a SVX sin ser miembro | Captura | Observado |
| PL-181 | F0 | ~~Reporte a Victor (no se implementa sin su respuesta): si el alcance por OT para leer cubre también Cronograma, Paquetes de Trabajo, RDTs y RQ (R30), y, de ser así, cómo se define el "servicio activo" en los listados que hoy muestran todos los servicios a la vez~~ **Cerrado por decisión de Victor (2026-09-29, R30 resuelta): no se agrega alcance por OT al leer en esas pantallas; no hay nada que reportar ni implementar** | Registro de decisiones (2026-09-29) | No aplica |

### Recursos: gestión completa (Personal, Cargos, Equipos, Causas CNC; fase F5D)

**Fuente:** flujo 14, tabla 2, grupo "Recursos" (nota ⁶). Administrador y jefe de proyectos crean, editan y eliminan/desactivan en los cuatro por igual; "eliminar" siempre es desactivar (`activo = false`), nunca borrado físico. No cambia qué recurso es "de empresa" ni la exclusión de Materiales.

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-157 | F5D | Existe `puedeGestionarRecursos` (administrador y jefe de proyectos) y `puedeGestionarCatalogoCnc` delega en ella; el POST de Personal deja de usar `puedeVerRecursos`. Pruebas unitarias por los 13 roles | `npm test` | Conforme |
| PL-158 | F5D | Crear Personal (ya existente): con la cuenta A y con "Ver como" administrador y jefe de proyectos, el formulario crea sin error; con la cuenta B o cualquier otro rol, sin control visible y `POST /api/recursos/personal` responde 403 | Capturas + respuesta API | Conforme |
| PL-159 | F5D | Crear Causa CNC (ya existente): mismo patrón que PL-158 sobre `POST /api/recursos/catalogo-cnc` | Capturas + respuesta API | Conforme |
| PL-160 | F5D | Activar o desactivar Causa CNC (ya existente): mismo patrón sobre `PATCH /api/recursos/catalogo-cnc/[id]` con `activo` | Capturas + respuesta API | Conforme |
| PL-161 | F5D | Editar Personal existente (construir): botón o control de editar en `TablaPersonal.tsx`, `PATCH /api/recursos/personal/[id]` nuevo; administrador y jefe de proyectos editan sin error, cualquier otro rol no ve el control y la API responde 403 | Capturas + respuesta API | Conforme |
| PL-162 | F5D | Eliminar o desactivar Personal (construir): control que pone `activo = false` (nunca borra la fila); mismo patrón de permiso que PL-161; el trabajador desactivado deja de aparecer en el desplegable de Crear RDT | Capturas + verificación en Crear RDT | Conforme |
| PL-163 | F5D | Crear Cargo (construir): formulario nuevo en `TablaRecursos.tsx` (tipo cargos), `POST /api/recursos`; mismo patrón de permiso | Capturas + respuesta API | Conforme |
| PL-164 | F5D | Editar Cargo existente (construir): control por fila, `PATCH` nuevo; mismo patrón de permiso | Capturas + respuesta API | Conforme |
| PL-165 | F5D | Eliminar o desactivar Cargo (construir): `activo = false`; mismo patrón de permiso; un cargo desactivado deja de ofrecerse al crear Personal (la API de Personal ya exige `activo = true`) | Capturas + verificación en crear Personal | Conforme |
| PL-166 | F5D | Crear Equipo (construir): formulario nuevo en `TablaRecursos.tsx` (tipo equipos), `POST /api/recursos`; mismo patrón de permiso | Capturas + respuesta API | Conforme |
| PL-167 | F5D | Editar Equipo existente (construir): control por fila, `PATCH` nuevo; mismo patrón de permiso | Capturas + respuesta API | Conforme |
| PL-168 | F5D | Eliminar o desactivar Equipo (construir): `activo = false`; mismo patrón de permiso | Capturas + respuesta API | Conforme |
| PL-169 | F5D | Editar el texto de una Causa CNC (construir): control de editar en `TablaCatalogoCnc.tsx` (la API `PATCH …/catalogo-cnc/[id]` ya acepta `descripcion`); mismo patrón de permiso; el texto editado se refleja en el desplegable de Crear RDT | Capturas + verificación en Crear RDT | Conforme |
| PL-170 | F6 | Regresión de lectura: Cargos y Equipos conservan filtro, orden y "Personalizar campos" que ya tenían, para los 13 roles, después de agregar los controles de alta, edición y baja | Comparación con la línea base de F0 | Conforme |
| PL-171 | F6 | Regresión: Personal conserva su flujo de creación (validación de DNI único, cargo tomado del catálogo activo) después de agregar edición y baja | Comparación con la línea base de F0 | Conforme |
| PL-172 | F6 | Por los dos lados con las dos cuentas: la cuenta A (o "Ver como" administrador y jefe de proyectos) crea, edita y desactiva en los cuatro recursos sin error; la cuenta B (o cualquier otro rol) no ve ningún control de mutación y sus llamadas directas (`POST`, `PATCH`, `PATCH` de desactivar) responden 403, sin cambiar ningún dato | Tabla 13 roles × las 12 acciones de Recursos | Conforme |
| PL-173 | F7 | El flujo 14 ya no necesita las marcas "(por construir)" del grupo Recursos porque las 9 acciones existen; se verifica sin volver a escribir la matriz aprobada (solo se retira la marca si Victor lo pide, con consulta previa) | Nota en el progreso | Conforme |

### Asistente (chat) como icono en toda pantalla (Spec 8, F4B)

Aquí "asistente" es el chat de ayuda del shell (`ChatPlaceholder`), no el rol de usuario "Asistente".

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-102 | F4B | Con servicio, en escritorio: el icono del asistente es visible en **todas** las pantallas del workspace, incluidas las que hoy no muestran la barra (recorrido de cada ruta de PL-02 a PL-13, Mi entorno, Notificaciones, Recursos, Configuraciones y Mi perfil) | Tabla ruta → icono visible + capturas | Conforme |
| PL-103 | F4B | Sin servicio, en escritorio: icono visible en Todos los servicios, Programas, Portafolio, Mi entorno, Recursos, Notificaciones, Usuarios, Configuraciones y Mi perfil | Tabla ruta → icono visible | Conforme |
| PL-104 | F4B | En móvil (390 px), con y sin servicio: icono visible en las mismas pantallas (hoy la barra no se mostraba en móvil) | Capturas móvil | Conforme |
| PL-105 | F4B | El clic en el icono despliega el panel (mensaje de vista previa, campo y botón Enviar); un segundo clic en el icono o el botón de cerrar lo repliega a solo icono, y el foco vuelve al icono | Captura abierto y cerrado + foco | Conforme |
| PL-106 | F4B | Ya no hay barra fija al pie: en escritorio con servicio desaparece la banda "Pregúntale algo al asistente…" y el área de contenido recupera esa altura respecto de la línea base de F0 | Captura antes y después + medida del contenedor | Conforme |
| PL-107 | F4B | No hay duplicado: en la pantalla del portafolio y en cualquier otra hay **una sola** instancia del asistente (conteo de elementos con su nombre accesible = 1) | Conteo por pantalla | Conforme |
| PL-108 | F4B | Escritorio: posición y capas verificadas con Playwright: el icono no tapa chips de ningún panel, el pie del panel izquierdo, controles del contenido ni el final de las tablas largas (Consolidado RDTs, Status de RDTs, PR, Plan Maestro) y formularios largos (comprobación con la caja del elemento y `elementFromPoint`) | Cajas medidas + capturas | Conforme |
| PL-109 | F4B | Móvil: el icono no tapa la cabecera (botón de menú y botón de herramientas), no se solapa con los cajones ni con la zona segura inferior; con un cajón o un modal abierto (capa `z-50`) el asistente queda por debajo o se oculta, sin quedar encima | Capturas con cajón y modal abiertos | Conforme |
| PL-110 | F4B | Panel desplegado: cabe en pantalla (alto máximo con scroll interno), en escritorio no cubre los paneles laterales y en móvil deja visible cómo cerrarlo y no impide usar la navegación | Capturas escritorio y móvil | Conforme |
| PL-111 | F4B | Accesibilidad: el botón tiene nombre accesible ("Asistente"), `aria-expanded` y `aria-controls`; el panel tiene rol y etiqueta; se llega con Tab, Enter o Espacio abren, Escape cierra y devuelve el foco al icono; el objetivo táctil mide al menos 40 px | Snapshot de accesibilidad + prueba con teclado | Conforme |
| PL-112 | F4B | Estado al cambiar de pantalla: con el panel abierto, navegar a otra pantalla del shell lo conserva abierto (el estado vive en el shell) y al recargar vuelve a icono; el comportamiento queda escrito en la evidencia y en el flujo (si el Worker decide otro, lo documenta) | Secuencia de capturas | Conforme |
| PL-113 | F4B | Sigue siendo vista previa: abrir el panel o pulsar Enviar no genera ninguna llamada de red a `/api` y el formulario no envía; el texto "todavía no está conectado a ningún dato" sigue visible | Registro de red de Playwright | Conforme |
| PL-114 | F4B | Reutilización y diseño: se modifica `ChatPlaceholder` en vez de crear un componente paralelo; se usan tokens y clases existentes y el patrón de diálogo y Escape de `CajonMovil`; sin dependencias nuevas y sin `max-w-*` nuevo en contenedores de página | Revisión del diff | Conforme |
| PL-115 | F4B | Disponible para los 13 roles (sin permiso propio): cuenta A, cuenta B y una muestra de roles con "Ver como" ven el icono; el asistente no forma parte del registro de accesos ni de la matriz del flujo 14 (queda escrito) | Capturas + nota | Conforme |
| PL-116 | F4B | Pantallas fuera del shell: login y activar cuenta no muestran el asistente (sin sesión); la pantalla `programas/[id]/portafolios/[portafolioId]/dashboard` (fuera de `(workspace)`) queda como excepción declarada y se reporta a Victor | Captura + nota (V4, R21) | Conforme |
| PL-117 | F6 | Regresión con el asistente ya como icono: pantallas con tablas y formularios largos no ganan scroll horizontal de página ni pierden filas visibles respecto de la línea base; portafolio y Mi entorno se ven como antes salvo la barra | Comparación con F0 | Observado |
| PL-118 | F7 | La regla "asistente como icono en toda pantalla" queda escrita en el flujo 16 (subsección propia), con referencias en los flujos 01 y 17 y la posición y capas en `design.md` §3, tras consultar a Victor | Diff de `pg_control_proyectos` | Conforme |

### UI / responsive / accesibilidad

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-59 | F3 | Móvil (390 px): el cajón izquierdo y el derecho muestran el mismo contenido que en escritorio, se cierran al navegar y la página no tiene scroll horizontal | Capturas móvil | Conforme |
| PL-60 | F3 | Escritorio: el panel izquierdo con todos los grupos hace scroll interno y no oculta el pie; con Recursos de empresa oculto queda compacto | Captura | Conforme |
| PL-61 | F3 | Chip deshabilitado accesible: `aria-disabled="true"`, título, no enfocable como enlace y no depende solo del color (texto legible) | Snapshot de accesibilidad | Conforme |
| PL-62 | F3 | Botón mostrar/ocultar con `aria-expanded`, operable con teclado; las secciones usan `<nav>` y encabezados | Snapshot de accesibilidad + prueba con teclado | Conforme |
| PL-63 | F3 | La marca informativo/acción es visible y no depende solo del color, en ambos paneles | Captura | Conforme |
| PL-64 | F3 | Diseño: se usan los tokens y el estilo de `EntornoTrabajoGrupo.tsx`, sin `max-w-*` nuevo en contenedores de página y sin dependencias visuales nuevas | Revisión de diff | Conforme |
| PL-65 | F6 | Las tablas largas conservan scroll horizontal y columnas fijas (Consolidado RDTs, Status de RDTs, Consolidado RQ, PR) | Captura de cada una | Observado |

### Estados vacío / carga / error

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-66 | F2 | Usuario o momento sin servicio elegido: los paneles muestran el estado sin servicio, sin errores y con Recursos de empresa visible | Captura | Conforme |
| PL-67 | F2 | Durante la carga inicial con `?proyectoId=` en la URL no se ve el mensaje "Selecciona un servicio" ni un salto de layout | Grabación o capturas seguidas | Conforme |
| PL-68 | F6 | Recorrido completo (PL-02 a PL-13 con ambas cuentas): sin errores nuevos en la consola del navegador respecto de la línea base | Registro de consola | Conforme |
| PL-69 | F2 | Servicio sin datos (sin DP, sin cronograma o sin Plan Maestro): los paneles y sus chips se comportan igual y las pantallas muestran su estado vacío habitual | Captura | Conforme |

### Validación en servidor / API

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-70 | F2 | El parámetro `?proyectoId=` nunca se usa en servidor sin validar pertenencia: las pantallas y APIs que lo reciben validan autenticación, rol y acceso al servicio como antes | Revisión de código + PL-46 | Conforme |
| PL-71 | F3 | Cambiar quién "ve" un chip no cambió quién "puede" usarlo, salvo lo decidido en el flujo 14: el diff de `permisos.ts` coincide con la matriz base y con "Acciones que cambian con esta decisión"; ninguna otra función cambia de roles; `permisos.test.ts` verde | Diff + `npm test` | Conforme |
| PL-72 | F2 | Los redirects del servidor conservan el servicio sin abrir un redireccionamiento abierto: el helper solo acepta identificadores con formato de id y rutas internas | Prueba unitaria del helper | Conforme |
| PL-73 | F6 | Con sesión cerrada, cualquier ruta del workspace con `?proyectoId=` lleva a `/login` (el middleware sigue igual) | Captura | Conforme |

### Regresión

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-74 | F6 | `npm test` completo verde; contadores actualizados con pruebas específicas de ubicación y comportamiento de los ítems nuevos (no solo el número) | Resumen del runner (no un filtro de texto) | Conforme |
| PL-75 | F6 | Lint sin deuda nueva: mismo total que `main` y archivos tocados limpios | Conteo contra `main` | Conforme |
| PL-76 | F6 | `npm run build` correcto (en worktree con `--webpack`) | Salida del build | Conforme |
| PL-77 | F6 | Sin servicio, todas las pantallas se comportan como en la línea base de F0 (mismos destinos y estados) | Comparación con F0 | Conforme |
| PL-78 | F6 | Flujos que usan chips siguen intactos (sin guardar datos): Crear RQ abre desde Mi entorno, filtros de Status de Requerimiento, selector y carga del Consolidado RDTs, Plan Maestro y Cronograma abren con y sin servicio | Capturas | Observado |
| PL-79 | F6 | Ningún dato real fue creado, modificado ni borrado durante la verificación | Nota en la evidencia + revisión de las acciones ejecutadas | Conforme |
| PL-80 | F6 | Navegación móvil y escritorio: el pie, "Ver como" y los cajones se comportan como en la línea base | Capturas | Conforme |

### Documentación y cierre

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-81 | F7 | Cada contradicción de la lista se consultó a Victor antes de editar el flujo afectado y su respuesta quedó en el progreso | Progreso con pregunta y respuesta | Conforme |
| PL-82 | F7 | Flujos 16, 01 y 14 (y 03, 05, 06, 11, 15, 21 si aplica) actualizados y coherentes con lo implementado, sin reglas pegadas al final | Diff de `pg_control_proyectos` | Conforme |
| PL-83 | F7 | La matriz derivada del registro coincide con la matriz base del flujo 14 (salvo lo que Victor haya aprobado); el Worker no reescribe la matriz base y deja anotado cómo repetir la comparación | Diff + comando o prueba usada | Conforme |
| PL-84 | F7 | `design.md` documenta el chip deshabilitado, el registro y la política (con la confirmación de Victor que exige su regla de evolución) | Diff | Conforme |
| PL-85 | F7 | Apartados "Mejoras (de trabajo)", "Reglas de negocio acordadas" y "Carpetas/archivos huérfanos" trasladados a sus destinos; huérfanos reportados a Victor sin borrar nada | Diff + mensaje | Conforme |
| PL-86 | F7 | Ninguna credencial de las cuentas de prueba aparece en ningún archivo de ninguno de los dos repositorios | Búsqueda en el diff | Observado |
| PL-87 | F6 | Evidencia completa en `03-evidencia/` con enlace al artifact de checklist visual si se crea, y limitaciones declaradas (SVX si no existe, rol de la cuenta B) | Archivo de evidencia | Conforme |

## Riesgos y bloqueos

Los del Spec (cambiar quién "ve" no debe cambiar quién "puede"; `?proyectoId=` frente a `?ots=`; tocar el shell afecta a todas las pantallas) y los que el Planner encontró al dimensionar en el código:

| # | Riesgo o bloqueo | Cómo se controla |
|---|---|---|
| R1 | **El servicio se pierde por dentro de las pantallas, no solo en los paneles.** 14 páginas hacen `redirect('/mi-entorno')` al faltar permiso, dos formularios hacen `router.push` tras guardar y `CabeceraPagina` lleva a `/mi-entorno` sin servicio. Arreglar solo los chips dejaría el mismo síntoma que Victor reportó. | Helper de servicio en F2, PL-19, PL-20, PL-21 y prueba de fuente PL-57 |
| R2 | **No todas las pantallas tienen "selector de OT"**: Status de RDTs, Archivo de RDTs y Consolidado RQ solo tienen un filtro de texto por columna; Status de Requerimiento usa `?ots=`. "Preseleccionar el servicio" significa cosas distintas por pantalla. | Tabla "Cómo se preselecciona el servicio en cada pantalla"; PL-30 a PL-34 |
| R3 | **El filtro N° OT es de "contiene"** (`PS-0001` coincide con `PS-00010`). | Coincidencia exacta al preseleccionar si aparece el caso |
| R4 | **Pantallas sin guardia de rol** (PR, Dashboard del servicio y del portafolio, DP para ver, Status de Requerimiento). Se resuelve en F2B y F5B según la matriz base. | F2B, F5B; PL-88 a PL-101 y PL-119 a PL-127 |
| R5 | **El código difiere de las tablas 1 y 2 del flujo 14 en muchas celdas** (por ejemplo `puedeAdjudicarProyecto` solo incluye al jefe de oficina técnica, Crear RQ excluye al administrador, PR y Dashboard no tienen guardia). El flujo 14 manda; `permisos.ts` y el registro se ajustan a él. | F0 entrega el antes/después completo (PL-146, PL-147); F2B, F5B y F5C alinean; PL-96 verifica |
| R6 | **`puedeVerRecursos` es un alias de `puedeVerApartadoProyectos`.** Con la matriz base, Recursos de empresa y el apartado del panel son de los 13 roles. | Desacople y apertura en F2B; PL-49 y PL-71 |
| R7 | **El chip habilitado no garantiza que la pantalla abra** para un rol con permiso pero sin alcance sobre la OT: ya no es solo Curva S — con F5B pasa también en PR, Dashboard, DP, Plan Maestro y Registro de costos, por decisión de Victor. | Las pantallas muestran su mensaje sin datos (mismo patrón de Curva S); se documenta en el flujo 16 |
| R8 | **Datos reales y Supabase real.** La verificación con las cuentas de prueba corre sobre datos de trabajo. | Solo lectura (PL-79); las acciones se prueban hasta abrir el formulario |
| R9 | **Worktree, variables de entorno y Turbopack.** La rama `local-worker-1` y su worktree existen desde el 2026-09-27 (el resto que lo bloqueaba se limpió con autorización de Victor). El worktree ya tiene `.env.local` (copiado con autorización permanente de Victor) y exige `--webpack` con `node_modules` como Junction. | El Worker no lee ni muestra los valores; cualquier otro archivo de entorno o de secretos se consulta antes de copiarlo |
| R10 | **Next.js 16 con cambios de API** (aviso de `AGENTS.md` del repositorio de la app): `searchParams` asíncronos y `useSearchParams` con `Suspense` en el shell. | El Worker lee la guía de `node_modules/next/dist/docs/` antes de tocar el shell |
| R11 | **Bucle entre selector y URL** si cada pantalla actualiza la URL desde su estado y el shell vuelve a pasar el valor. | Una sola fuente de verdad (la URL) y `router.replace` sin recarga; se prueba en PL-14 |
| R12 | **Contadores congelados en pruebas** (`nav-proyecto.test.ts` fija 41 ítems y varias pruebas asumen que Cronograma exige servicio). | Se reescriben con pruebas de ubicación y comportamiento (aprendizaje del 2026-09-23) |
| R13 | **Pantalla fuera del shell**: `src/app/programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx` cuelga de la raíz de `app`, no de `(workspace)`, por lo que no tiene paneles ni tendrá el icono del asistente (R21). | La prueba de cobertura la incluye como excepción declarada o se reporta a Victor; no se mueve sin autorización |
| R14 | **El componente nuevo choca con la regla de `design.md` §5** (no crear componentes sin justificar). | Se propone que el Gate 1 lo apruebe y `design.md` se actualiza al cierre (PL-84) |
| R15 | ~~**Bloqueo**: sin worktree el Worker no puede empezar.~~ **Resuelto el 2026-09-27**: el worktree `.worktrees/local-worker-1` existe (rama `local-worker-1`, `1942b01`). El `.env.local` también quedó copiado (2026-09-27). | Ninguno: el Worker puede arrancar cuando Victor apruebe el plan y confirme los roles de E2 |
| R16 | **Cambiar quién ve qué y quién hace qué afecta a muchos roles a la vez.** Interfaces: ganan acceso los roles que hoy no ven RDTs, consolidado RQ, Recursos, Cronograma o Paquetes; pierden acceso los roles fuera de economía en PR, Dashboard y DP (hoy abiertos a todos los autenticados) y en Plan Maestro y Curva S. Acciones: el jefe de proyectos gana varias (incluidos los borrados definitivos), el jefe de oficina técnica pierde archivar, editar servicio, editar checklist y editar perfil, el supervisor de oficina técnica pierde importar DP, y logística deja de ver el registro de costos. | PL-97 (antes/después completo) que Victor revisa; PL-128 a PL-145 por acción y por rol |
| R17 | **Enlaces internos a pantallas ahora protegidas**: la ficha del servicio muestra "Ver Dashboard" sin mirar permisos y su checklist enlaza a PR y DP; puede haber más. | Búsqueda de código en F5B y PL-98 |
| R18 | **APIs que sirven las mismas pantallas**: proteger solo la página dejaría abiertas `GET /api/proyectos/[id]/requerimientos` (que ahora se abre a los 13), `dp/exportar`, `GET /api/curva-s`, `GET /api/plan-maestro` y `registro-costos`. Proteger de más rompería Crear RQ (`…/partidas` lo usa cualquier rol que crea RQ) y las notificaciones que enlazan a un RQ. | Las mismas funciones en páginas y APIs; `partidas` sin restringir a propósito (PL-93 y PL-94) |
| R19 | **Curva S ya exigía alcance por OT** (`tieneAlcanceSobreProyecto`) antes de esta tarea; F5B suma la misma guardia a PR, Dashboard (servicio y portafolio), DP, Plan Maestro y Registro de costos, por decisión de Victor (cierra C21). | PL-174 a PL-179 |
| R20 | **El icono del asistente puede solaparse** con contenido, con los chips de los paneles, con el final de tablas largas, con el botón de herramientas (`PanelRight`) y el de menú de la cabecera móvil, con los cajones y con los modales (`PanelVerRq`, `ModalPartidasServicio`, `ModalHistorialRdt`, `ResolverRecursosImportacion`, todos `fixed … z-50`). Un elemento fijo a la ventana invade además el panel derecho (`w-64`). | Posición propuesta dentro de `<main>` (escritorio) y en la cabecera o con margen de zona segura (móvil); capa por debajo de `z-50`; PL-108 a PL-110 con medidas reales en Playwright |
| R21 | **No toda pantalla cuelga del shell.** `programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx` está fuera de `(workspace)` (R13) y las pantallas de `(inicio)` (login, activar) tampoco lo usan: un asistente montado en `WorkspaceShell` no aparecerá ahí. | Login y activar quedan fuera por diseño (sin sesión); el dashboard de portafolio se declara excepción y se reporta a Victor (PL-116, V4); no se mueve sin autorización |
| R22 | **Se puede tomar el asistente por funcional.** Al verse en todas las pantallas, un usuario puede esperar respuestas reales; y su texto de ejemplo habla de portafolios ("¿Cuántos proyectos tiene este portafolio?"), fuera de lugar en otras pantallas. | El aviso "todavía no está conectado a ningún dato" permanece visible (PL-113) y se neutraliza el ejemplo (A10) |
| R23 | **El estado del panel puede perderse al navegar** si el asistente se monta dentro de un componente que se remonta (el shell envuelve su contenido en `Suspense` y usa `useSearchParams`). | El estado vive en el shell y se comprueba con navegación real (PL-112); si se pierde, se documenta o se corrige |
| R24 | ~~F5B y F5C dependen de decisiones abiertas (CO1 a CO5).~~ **Resuelto por Victor el 2026-09-28** con la aprobación de la matriz: ya no hay condiciones. | Nota "Conflictos operativos CO1 a CO5: resueltos" |
| R25 | **Abrir interfaces a los 13 roles puede exponer dinero** si alguna pantalla "sin economía" muestra costos, precios o tarifas (por ejemplo Recursos de empresa o Paquetes de Trabajo, que manejan `precio_unitario` internamente). | PL-121: revisión de cada pantalla antes de cerrar F2B; un hallazgo se devuelve a Victor |
| R26 | **El dashboard del portafolio está fuera del shell y sin guardia**: al proteger, la respuesta no puede apoyarse en los paneles ni en los patrones del shell. | Mensaje "No tienes acceso…" con enlace de vuelta a la grilla, sin datos (PL-122); no se mueve la página sin autorización |
| R27 | **Alias que arrastran permisos a otro rol.** Editar servicio usa la función de adjudicar; importar DP usa la de subir documento; corregir RDT usa la de crear; rechazar un RDT ya validado usa la de validar; descargar el consolidado RQ usa la de ver. Cambiar una sin separar daría o quitaría acceso por accidente (por ejemplo, el jefe de oficina técnica ganaría corregir RDT). | F5C separa las funciones; PL-148 lo comprueba por función |
| R28 | **"Ver como" y el alcance por OT.** "Ver como" cambia los roles pero el alcance por OT sigue siendo el del usuario real: un 403 por falta de OT puede confundirse con un 403 por rol, y las acciones que requieren OT a cargo pueden aparecer rechazadas para el rol simulado. | Método de "Acciones sin escribir": pruebas unitarias por función y distinción por mensaje (PL-151) |
| R29 | **Borrados definitivos para el jefe de proyectos y ciclo de vida del proyecto sin el jefe de oficina técnica.** Los flujos 05, 06, 08 y el índice de `04-flujos-de-negocio` dicen que solo el administrador borra y que el jefe de oficina técnica adjudica, confirma y (según permiso) borra. Un borrado es irreversible y dispara recálculos del PR. | Los borrados no se ejecutan en la verificación (PL-138, PL-141, PL-130, PL-131); las contradicciones C29 a C34 se consultan a Victor y se actualizan todos los flujos afectados; el Auditor verifica la tabla de trazabilidad |
| R30 | ~~**Alcance por OT en pantallas sin economía (Cronograma, Paquetes de Trabajo, RDTs, RQ): sin decidir.**~~ **Resuelto por Victor el 2026-09-29:** limitar esas pantallas a las OT asignadas restringiría demasiado; se dejan como están y el alcance por OT al leer queda solo en las seis pantallas con economía (PL-174 a PL-179). | PL-181 cerrado (`No aplica`); nada que implementar |
| R31 | **Ejecución por tandas: el estado entre tandas vive solo en la rama, el handoff y el plan.** Una tanda que no cierra deja el árbol sucio, filas de la Punch List sin actualizar o un contrato distinto del que asume el brief siguiente; los briefs citan líneas de `1942b01` que se desplazan. | Cierre obligatorio (`00-reglas-de-contexto.md`), `git status` limpio antes de lanzar la siguiente, el Worker verifica nombres reales con Read/Grep antes de usar lo creado por tandas previas, y el Orquestador anota estado y commit en `00-indice-de-tandas.md` |
| R32 | **Ítems que exigen escribir datos reales.** PL-158 a PL-169 y PL-172 piden «crea, edita o desactiva sin error» en Recursos de empresa, pero el método del plan y PL-79 son solo lectura. | Pregunta a Victor (Resumen, versión 8, punto 6); mientras tanto el camino feliz queda `Observado` y se prueba la guardia con cuerpo inválido o id inexistente |
| R33 | **Editar o desactivar un Cargo o Equipo puede romper referencias por texto** (`recursos_personal.cargo`, equivalencias de `db/046`, tarifas e historia de RDT); las tablas `recursos_cargos` y `recursos_equipos` solo tienen RLS de lectura, así que la escritura pasa por `crearClienteAdmin()` tras la guardia de rol. | F5D-B revisa las referencias antes de permitir editar la descripción y devuelve la duda si hay riesgo; «eliminar» = `activo = false`; sin migraciones |
| R34 | **Alcance por OT en el dashboard del portafolio**: `tieneAlcanceSobreProyecto` es por servicio y un portafolio agrupa varios (PL-176). | Recomendación del Planner: mostrar solo las OT con alcance (administrador todas); F5B-B devuelve la duda al Orquestador si no queda evidente |

## Decisiones abiertas 3 a 6 — opciones y recomendación

### Decisión 3 — ¿Los chips del panel derecho también pasan a "visibles y deshabilitados"?

Hoy el panel derecho **no mira permisos**: muestra todos los chips activos a todos los roles y, al hacer clic, la pantalla redirige a Mi entorno sin explicar nada. El panel izquierdo (decisión ya tomada) y Mi entorno sí usan "visible y deshabilitado".

| Opción | Efecto | A favor | En contra |
|---|---|---|---|
| **A. Dejar como hoy** (visible y clicable para todos) | El rol sin permiso hace clic y rebota a Mi entorno | Cero cambio | Tres criterios distintos para el mismo chip según el panel; clic que "no hace nada"; el cambio de fondo del flujo 16 queda a medias |
| **B. Visible y deshabilitado** (recomendada) | Mismo patrón que Mi entorno y el panel izquierdo: `opacity-40`, `cursor-not-allowed`, título con el motivo | Coherencia total; con el registro es casi gratis (el permiso ya es un metadato del acceso); evita el clic muerto; cumple el ajuste del Spec de que todo chip funcione o se vea claramente inerte | Cambia lo que ve cada rol hoy en el panel derecho (no lo que puede hacer) |
| **C. Oculto** | El chip desaparece si no hay permiso | Panel más corto | Es la regla que Victor ya descartó para el panel izquierdo; el usuario no sabe que existe |

Recomendación: **B**. Nota: los chips cuya pantalla no tiene guardia hoy (PR, Dashboard, DP, Status de Requerimiento) quedan habilitados para todos, coherente con el código (ver E2). Documentar en el flujo 16 (panel derecho) y en el 03.

### Decisión 4 — ¿Qué pasa con "Salir a Mi entorno"?

`CabeceraPagina` (la usan unas 20 pantallas y componentes de listado y de servicio) lo muestra por defecto y lleva a `/mi-entorno` **sin** servicio, es decir, rompe justo lo que esta tarea quiere cuidar. Con los paneles siempre activos la palabra "salir" ya no describe un cambio de modo; además el pie del panel izquierdo tiene el acceso a Mi entorno siempre visible.

| Opción | Efecto | A favor | En contra |
|---|---|---|---|
| **A. Mantener tal cual** | Sigue perdiendo el servicio | Ningún cambio | Contradice el objetivo de la tarea |
| **B. Mantener y que conserve el servicio** (recomendada) | Va a `/mi-entorno?proyectoId=…` si hay servicio y a `/mi-entorno` si no; mismo texto | Un solo archivo (`CabeceraPagina.tsx`); no cambia el texto que Victor y el equipo conocen; en móvil ahorra abrir el cajón; reversible | Chip parcialmente redundante con el pie del panel izquierdo |
| **C. Eliminarlo en todas las pantallas** | `mostrarVolver` por defecto en falso | Interfaz más limpia; sin redundancia | Cambia los flujos 01, 05 y 06 (que lo nombran) y quita un atajo; conviene decidirlo cuando Victor vea los paneles ya completos |

Recomendación: **B**, y dejar C como limpieza posterior si Victor la quiere. Efecto documental: flujo 16 regla 7, flujos 01, 05 y 06.

### Decisión 5 — Destino de "(OT) Orden de trabajo" y de "Recursos hh, hm, mat. (s/c)"

Hechos verificados: el flujo 13 dice que la OT "no está implementada en UI" y que la captura estructurada de la OT no se escribió; `/proyectos/[id]` es la **ficha del servicio** (N° OT, cliente, OC/OS, estado, checklist, documentos), no una OT estructurada. `/recursos/*` es el **catálogo de empresa** (`recursos_cargos`, personal, equipos), no por servicio. Los recursos por servicio (mano de obra, equipos, materiales y MOI) hoy se ven dentro de la pantalla DP, **con costos**, lo que no cuadra con "s/c" (sin costo) y con la restricción de datos económicos pendiente.

| Chip | Opciones |
|---|---|
| **(OT) Orden de trabajo** | a) inerte (recomendada): respeta el flujo 13 y la regla "si no existe pantalla, permanece inerte"; b) apuntar a la ficha del servicio: confunde la ficha con la captura estructurada de la OT; c) apuntar a Editar servicio: es una acción, no una consulta |
| **Recursos hh, hm, mat. (s/c)** | a) inerte y reemplazado por los dos chips del flujo 16, **Cargos (HH)** y **Equipos (HM)**, que dicen lo mismo con más precisión, dejando "Materiales (c/c)" inerte como está (recomendada); b) apuntar a `/recursos/*`: mezcla lo corporativo con lo del servicio, que el flujo 16 prohíbe; c) apuntar a DP con ancla: muestra costos (contradice "s/c") |

Recomendación: **(OT) inerte** y **Recursos hh, hm, mat. (s/c) retirado a favor de Cargos (HH) y Equipos (HM)**. Los demás chips inertes del grupo actual (Presupuesto, Alcance del servicio, Personal NUEVO, Consolidado de servicio, Materiales c/c) se conservan visibles e inertes en su sección hasta que exista su pantalla (A6). Con el registro, activar uno cuando llegue su pantalla es cambiar una entrada.

### Decisión 6 — Dónde ubicar Registro de costos, Editar servicio y Editar checklist

Las tres pantallas existen. Registro de costos ya tiene chip en el panel derecho (Logística) pero no en el izquierdo; Editar servicio y Editar checklist **no tienen chip**: solo se llega desde la ficha del servicio, es decir, hay que "volver a otra interfaz" para encontrarlas, que es el síntoma que Victor reportó. Permisos: Registro de costos, Logística (subir) y Jefe de Proyectos (descargar); Editar servicio, jefe de oficina técnica; Editar checklist, administrador y jefe de oficina técnica.

| Opción | Efecto | A favor | En contra |
|---|---|---|---|
| **A. Agregar un grupo "Servicio" al panel izquierdo** (recomendada): informativo **Ficha del servicio**; acciones **Editar servicio** y **Editar checklist**; **Registro de costos** en Reportes | Las tres pantallas y la ficha se alcanzan desde cualquier pantalla; se ven deshabilitadas para quien no puede usarlas | Resuelve el síntoma; consistente con "ver ≠ acceder"; cada una es una entrada del registro | Añade un grupo que el flujo 16 no lista; dos chips más deshabilitados para casi todos los roles |
| **B. Solo declararlas como excepciones de cobertura (sin chip)** | Se siguen alcanzando desde la ficha | Panel más corto | Mantiene el problema original para esas tres pantallas; el flujo 16 "todo chip cuya pantalla existe funciona" se cumple solo por omisión |
| **C. Registro de costos en "Alcance y presupuesto"; el resto como B** | | | Mezcla un archivo de costos de Logística con alcance |

Recomendación: **A**. Registro de costos se clasifica como **informativo** (abrirlo no modifica datos; subir o descargar ocurre dentro de la pantalla, igual que Paquetes de Trabajo). Los roles que pueden verlo salen de la matriz base del flujo 14 (regla 2); subir y descargar siguen CO3 y CO5. Hasta que F5B lo cambie, el chip refleja el código vigente.

## Decisiones adicionales que necesitan respuesta de Victor

Conflictos que el Spec no cubre y que el Planner detectó al leer los flujos y el código. **E2 quedó sustituida por la matriz de permisos aprobada del flujo 14 (ver la sección siguiente). E1 y E3 conservan la recomendación del Planner, aprobada por el Orquestador con la aprobación con cambios de Victor (2026-09-27).**

| # | Conflicto | Opciones | Recomendación |
|---|---|---|---|
| **E1** | El flujo 16 dice: "El usuario no debe poder cambiar de servicio durante una acción iniciada desde este panel", y el Spec 5: "las acciones quedan fijadas al servicio actual". El Spec 6 pide que el selector de OT abra con el servicio elegido, y esos selectores hoy son editables. | a) Bloquear el selector cuando la acción viene del panel (requiere un modo "solo lectura" en cada formulario: Crear RDTs, Crear RQ, Subir RDT, Paquetes). b) Preseleccionado y editable, pero cambiar el selector actualiza la URL y los paneles (nunca dos servicios a la vez). | **b.** Cumple la intención (no hay divergencia entre el servicio de la acción y el del contexto) sin tocar cada formulario; a) queda como mejora posterior. Al cierre se ajusta la frase del flujo 16. |
| **E2** | Los flujos 14 y 16 dicen que "toda ruta valida autenticación, rol y pertenencia"; el código tenía pantallas sin guardia de rol. | a) reflejar el código; b) implementar las guardias. | **SUSTITUIDA (2026-09-28):** Victor implementa las guardias y aprobó la matriz de permisos (flujo 14, tablas 1 y 2). Ver "Permisos: la matriz aprobada del flujo 14 y su implementación". |
| **E3** | En Mi entorno, el chip "Status de RDTs" (`listado-rdts`) va a `/rdts/listado`, que en el panel derecho es "Archivo de RDTs subidos"; el "Status de RDTs" del panel derecho (`status-rdts`) va a `/rdts/status`. El flujo 06 todavía dice que `/rdts/listado` es Status de RDTs. | a) Unificar en el registro: "Status de RDTs" = `/rdts/status` en todos los paneles y "Archivo de RDTs subidos" = `/rdts/listado`. b) Conservar la diferencia. | **a**, con la corrección del flujo 06 al cierre; es el único cambio de destino visible de la migración. Si Victor prefiere b, el Worker lo replica tal cual y lo deja anotado. |

## Permisos: la matriz aprobada del flujo 14 y su implementación (sustituye a E2 y a CO1 a CO5)

**Fuente única y aprobación.** Victor aprobó la matriz de permisos el 2026-09-28 (artefacto «Matriz de permisos», https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT, marcas versión 17) y el flujo 14 la contiene completa: la **tabla 1** (interfaces, con y sin datos económicos) y la **tabla 2** (acciones por rol, con "Requiere OT a cargo"). Este plan las enlaza y no las copia. Un dato es económico si muestra dinero; los RQ, los RDT y los recursos de empresa no. **El "Registro de costos" es un archivo que Logística sube por servicio y no es el RQ.** Rige la política de coherencia y trazabilidad: el artefacto es la base de los accesos y este plan abarca todos los flujos afectados (ver "Trazabilidad por flujo").

**Cómo se traduce en código (nombres propuestos; lista completa en "Funciones de permisos.ts que cambian").**
- **Interfaces sin economía (F2B):** los 13 roles. Incluye Recursos de empresa (consulta), Cronograma, Paquetes, RDTs, RQ (status y consolidado), ficha, grilla del portafolio, panel izquierdo, Notificaciones y Mi entorno.
- **Interfaces con economía (F5B):** `puedeVerEconomia` = administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos, con dos excepciones acotadas a la herramienta del rol: el planner ve el Plan Maestro y el supervisor de oficina técnica ve el DP. Las específicas delegan en ella.
- **Acciones (F5C):** las funciones de acción de `permisos.ts` se alinean con la tabla 2, separando los alias que hoy arrastrarían a otro rol.

**Qué se protege.** Páginas y APIs con la misma función, más el **dashboard del portafolio**, que hoy no tiene guardia y vive fuera del shell.

**Pertenencia al servicio y alcance por OT.** El `id` de la URL corresponde a un servicio existente y visible para el usuario con su sesión; si no, mensaje o `notFound`, sin datos. **Resuelto (Victor, 2026-09-28, Registro de decisiones):** el alcance por OT (`proyecto_miembros`) es el requisito de partida para ver cualquier interfaz orientada a un servicio, en todas las pantallas de servicio, no en ninguna — cierra C21. F5B añade esa guardia a las seis pantallas con economía (PR, Dashboard del servicio, Dashboard del portafolio, DP, Plan Maestro, Registro de costos); Curva S ya la tenía. Las acciones de la tabla 2 con "Requiere OT a cargo: Sí" siguen sujetas a `proyecto_miembros` (PL-151). **Resuelto (R30, Victor, 2026-09-29):** la regla NO cubre las pantallas sin economía (Cronograma, Paquetes de Trabajo, RDTs, RQ): siguen exigiendo alcance solo al escribir, como hoy; ahí este plan solo da acceso y restringe a quien corresponde según la matriz.

**Comportamiento al rechazar.** En `/proyectos/[id]/…`: el patrón de Curva S (mensaje "No tienes acceso…" dentro del shell, sin leer datos). En pantallas con redirección: a Mi entorno conservando `?proyectoId=`. En el dashboard del portafolio: mensaje con enlace de vuelta a la grilla. Las APIs responden 403.

**Pantalla en modo "solo subir".** El supervisor de logística sube el registro de costos pero no lo ve ni lo descarga (tabla 1 y tabla 2): la pantalla abre para logística solo con el control de subir, sin descarga, fecha ni contenido del archivo. Es el equivalente en pantalla de la excepción de rol.

**Impacto por rol (resumen, no sustituye a PL-97).**
- **Ganan interfaces:** el rol Asistente (Cronograma y Paquetes); los roles que hoy no ven RDTs, consolidado RQ o Recursos de empresa; jefe de costos y administrador en economía donde no entraban.
- **Pierden interfaces:** los roles fuera de economía en PR, Dashboard y DP (hoy abiertos a todo autenticado) y en Plan Maestro y Curva S (salvo el planner en Plan Maestro y el supervisor de oficina técnica en DP); logística pierde la vista del registro de costos y conserva solo subir.
- **Acciones:** el jefe de proyectos gana adjudicar y crear programa y portafolio, confirmar transición, archivar y eliminar proyecto, eliminar contenedor, editar servicio, editar checklist, importar DP, editar su perfil y los borrados definitivos de RDT y RQ, pero no asignar rol administrador ni «Ver como» (exclusivas del administrador). El jefe de oficina técnica gana crear y validar o rechazar RDT, conserva adjudicar, confirmar transición, subir RDT, derivar RQ y descargar el consolidado RQ, y pierde archivar y eliminar proyecto, editar servicio, editar checklist y editar su perfil. El supervisor de oficina técnica ve el DP pero ya no lo importa. El administrador gana adjudicar (hoy solo el jefe de oficina técnica), editar servicio, crear RQ y actualizar estado de RQ.

### Conflictos operativos CO1 a CO5: resueltos

Eran los cinco conflictos que el flujo 14 dejó abiertos el 2026-09-28. **Victor los resolvió al aprobar la matriz**; ya no condicionan ninguna fase.

| # | Conflicto | Cómo se resolvió | Dónde se aplica |
|---|---|---|---|
| CO1 | Planner y Plan Maestro | El planner **ve y gestiona** el Plan Maestro (excepción acotada) | `puedeVerPlanMaestro`, F5B |
| CO2 | Supervisor de oficina técnica y DP | **Ve** el DP y **ya no lo importa** (importar: administrador y jefe de proyectos) | `puedeVerDp` (F5B), `puedeImportarDp` (F5C) |
| CO3 | Supervisor de logística y Registro de costos | **Solo lo sube**; no lo ve ni lo descarga | Modo "solo subir" (F5B, F5C) |
| CO4 | Jefe de costos | **Entra** a las interfaces con economía, igual que el supervisor de costos | `puedeVerEconomia` (F5B) |
| CO5 | Acciones destructivas y de sistema | Administrador y jefe de proyectos: todas las acciones **salvo asignar rol administrador y «Ver como»**, exclusivas del administrador; el jefe de proyectos sí ejecuta los borrados definitivos de RDT y RQ | F5C; contradicciones C29 a C34 |

Difieren de las recomendaciones del Planner de la versión 4 en CO2 (el supervisor de oficina técnica ve pero no importa), CO3 (logística no ve el contenido) y CO5 (el jefe de proyectos sí tiene los borrados definitivos y el resto de acciones del ciclo de vida).

### Puntos que el Planner deja anotados para Victor (no bloquean)

1. **(Resuelto, ya no es duda)** ~~La tabla 2 deja al jefe de proyectos sin "Subir documento del proyecto"...~~ El jefe de proyectos ya tiene "Subir documento del proyecto" (omisión corregida, artefacto v.19, flujo 14 fila 4) y no hay regla general de "todo menos N". **Anulado (Victor, 2026-09-29):** actualizar estado de RQ y subir registro de costos siguen siendo exclusivos de logística.
2. **(Resuelto, ya no es duda, C35, 2026-09-29)** El interruptor Parcial/Completo del Dashboard lo activan los roles con datos económicos de la matriz (`puedeVerEconomia`); el Parcial sin economía para los demás roles es del plan futuro. "Editar perfil" para el jefe de oficina técnica figura en la tabla 2 como pérdida.
3. Descargas: registro de costos y consolidado RQ, decididas; las tres propuestas del artefacto (RDTs y listado de RDTs, listado RQ, exportar DP) siguen sin aprobar (A12) y las que el código tiene y el artefacto no lista se reportan (A13).
4. **(Resuelto, ya no es duda)** Alcance por OT para leer, en las seis pantallas con economía: cierra C21 (F5B, PL-174 a PL-179).
5. **(Resuelto, ya no es duda, R30, 2026-09-29)** El alcance por OT al leer no se aplica a Cronograma, Paquetes de Trabajo, RDTs ni RQ.

## Supuestos menores del Planner

Aprobados por el Orquestador con la aprobación con cambios de Victor (2026-09-27), salvo **A4, que Victor reemplazó por una decisión propia**. **A10 y A11 son nuevos (versión 3) y se aprueban con el plan salvo objeción de Victor. A12 (versión 4, corregido en la 5) y A13 (versión 5) son **supuestos**, no decisiones, y se tratan igual.**

| # | Supuesto | Motivo |
|---|---|---|
| A1 | Cuando el usuario cambia el selector de OT dentro de una pantalla, la URL (`?proyectoId=`) se actualiza con `router.replace` y los paneles siguen el cambio. | Una sola fuente de verdad; cumple "hasta que el usuario cambie de servicio" |
| A2 | El servicio persiste también en los enlaces del pie del panel izquierdo (Usuarios, Notificaciones, Configuraciones, Mi entorno) y en Recursos de empresa. Solo "Todos los servicios" y el logo lo limpian; las pantallas de contenedores (`/programas/**`) no llevan servicio. | Spec 1: "en todas las pantallas del workspace" |
| A3 | Mi entorno conserva el mismo conjunto de chips que hoy (no se le agregan PR, Dashboard, etc.); solo cambia que ahora envía el servicio y sale del registro. | Sin ampliar alcance |
| A4 | **Ampliado por la matriz base (2026-09-28):** Recursos de empresa es visible y **accesible** para los 13 roles (Personal, Cargos, Equipos y Causas CNC en consulta), igual que todo el panel izquierdo; solo gestionar Causas CNC queda para administrador y jefe de proyectos. `puedeVerRecursos` deja de ser alias de `puedeVerApartadoProyectos` y abre a todos. | Decisión de Victor |
| A5 | El chip "Notificaciones" no se repite en el panel izquierdo (la campana del pie ya lo cubre; regla 8 del flujo 16). Sigue en cada grupo del panel derecho. | Regla 8: no duplicar |
| A6 | Los chips actuales sin pantalla que ninguna decisión ubica (Presupuesto, Alcance del servicio, Personal NUEVO, Consolidado de servicio, Materiales c/c) se conservan como inertes en su sección. | "El que no tiene pantalla permanece visible e inerte" |
| A7 | "Crear paquete" abre `/paquetes-trabajo?proyectoId=…&accion=crear`, con un cambio mínimo en `FormularioPaquetesTrabajo.tsx` para abrir directo el formulario de paquete nuevo. | El Spec lo lista en Acciones y la pantalla ya tiene el formulario ("Nuevo paquete") |
| A8 | "Subir RDT" también se incluye en Acciones del panel izquierdo (el flujo 16 lo cita como chip de acción). | Es una acción existente con pantalla |
| A9 | La matriz del flujo 14 se "deriva" del registro solo para **compararla** con la matriz base (PL-56, PL-83); el Worker no reescribe la matriz base, que es decisión de Victor. El mecanismo de comparación lo fija el Worker (sin inventar comandos: el que use debe quedar verificado y documentado). | La matriz base ya está decidida y escrita |
| A10 | El texto de ejemplo del asistente ("¿Cuántos proyectos tiene este portafolio?") se neutraliza porque ahora aparece en todas las pantallas; el aviso de que no está conectado a ningún dato se conserva. | Ya no es exclusivo del portafolio |
| A11 | Comportamiento por defecto del asistente: disponible para los 13 roles sin permiso propio; fuera del registro de accesos (no es un chip); en escritorio es un panel no modal anclado al icono y en móvil una hoja superpuesta con diálogo; el estado abierto o cerrado se conserva al navegar entre pantallas del shell y se pierde al recargar; no aparece en login ni activar. | Spec 8 pide icono en toda pantalla; el resto no está definido y esta es la opción más simple |
| A12 | **SUPUESTO, no decisión:** las tres descargas **propuestas** en la sección «Descargas» del artefacto y aún no aprobadas (no están en el flujo 14): descargar RDTs (ZIP) y listado de RDTs (PDF PROM-GP-0006) = los 13 roles; descargar listado RQ (PDF PROM-GP-008) = los 13 roles; exportar DP = los seis roles que ven el DP. Las decididas (registro de costos: administrador y jefe de proyectos; consolidado RQ: como estaba) son requisito, no supuesto. | Las descargas son acciones y las guardias de servidor deben cumplir la misma regla que "ver"; no bloquea nada |
| A13 | **SUPUESTO:** las descargas y exportaciones que el código tiene y el artefacto no lista (plantilla de cronograma, PDF de RDT estructurado, archivo de RDT subido, PDF individual de RQ, formato vacío PROM-GP-008) **mantienen su guardia actual** y se reportan a Victor; el plan no decide sobre ellas | Regla de la política de coherencia: lo que no está en el artefacto se reporta, no se decide solo |

## Contradicciones con reglas de negocio ya escritas

Anticipadas tras leer los 21 flujos y `README.md`, y revisadas contra el flujo 14 reescrito (tablas 1 y 2). **Quién decide: Victor, siempre**: ninguna se edita antes del cierre; antes de tocar un flujo, el Worker devuelve la contradicción al Orquestador, que la relaya a Victor (el Worker es un subagente y no habla con él), y se anota dónde quedó aplicada. Por la política de coherencia y trazabilidad, la implementación abarca **todos** los flujos afectados: la tabla "Trazabilidad por flujo" (después de los vacíos) es la lista completa con su destino, y el Auditor verifica que no quede ninguno sin actualizar.

| # | Flujo y regla escrita | Choque con esta tarea o con el código | Acción propuesta al cierre |
|---|---|---|---|
| C1 | **16**, regla 2: "Con servicio se muestran solo accesos autorizados" | Decisión de Victor: se muestran todos, los no autorizados deshabilitados | Reescribir la regla |
| C2 | **16**, regla 3: "Un chip oculto por permisos no debe ser accesible solo escribiendo la URL" y criterio de aceptación "Se respetan permisos en la interfaz y en el servidor" | El chip ya no está oculto sino deshabilitado; la barrera del servidor no cambia | Reformular: "un chip deshabilitado no es accesible por URL" |
| C3 | **16**, "Panel izquierdo — sin servicio: recursos corporativos; con servicio: accesos del servicio" y su bloque final (2026-09-16): "con un servicio seleccionado, **cambia**" | Recursos de empresa se conserva con botón mostrar/ocultar, con o sin servicio | Reescribir ambos apartados |
| C4 | **16**, sin servicio: "Cargos de personal, Maquinaria, Herramientas" | La app tiene Personal, Cargos, Equipos y Causas CNC; "Materiales" se elimina | Corregir la lista |
| C5 | **16**, regla 7: "Las pantallas a pantalla completa deben ofrecer Salir a Mi entorno" | Decisión 4; hoy el chip pierde el servicio | Reescribir según la respuesta |
| C6 | **16**, Organización del panel izquierdo (árbol) | Se agregan el grupo Servicio (decisión 6), PR, Dashboard y Curva S en Reportes (decisión 2 del Spec), Plan Maestro y "Recursos del servicio" sin los chips de la decisión 5 | Actualizar el árbol |
| C7 | **16**, "Estado de implementación" (Pendiente: panel izquierdo completo, registro centralizado) y el bloque final "NO EXISTE TODAVÍA" | Quedan implementados; el flujo tiene dos versiones superpuestas de la misma especificación y la última línea está cortada ("tablas con scrol") | Consolidar en una sola versión y corregir el texto cortado |
| C8 | **16**, "Con servicio… El usuario no debe poder cambiar de servicio durante una acción" | E1 | Reescribir según la respuesta |
| C9 | **16**, regla 10 y "Tabla de accesos" ("no mantener listas independientes"); **14**, regla "cada vez que se agrega un chip… actualizar esta tabla" | El registro único pasa a ser la fuente; la tabla se deriva | Sustituir por la política de interfaz nueva |
| C10 | **16**, metadatos "Requiere servicio: sí/no" | Se necesita un tercer valor "opcional" (Plan Maestro, Status de Requerimiento, Consolidado RQ, Status de RDTs abren sin servicio y lo preseleccionan con él) | Extender el metadato |
| C11 | **01**: "Apartado Proyectos (panel izquierdo): solo administrador y jefe de proyectos" y "Pantallas de listado a pantalla completa… chip Salir a Mi entorno" | Lo ven todos los roles (matriz base y decisión de Victor); Recursos de empresa también se ve y se abre para todos; decisión 4. El flujo 01 se declara "pendiente de definir" y guarda una regla de paneles que pertenece al 16 | Reescribir y, con Victor, mover la regla del panel al 16 dejando un enlace |
| C12 | **14**, filas antiguas de la matriz de accesos (apartado Proyectos, Ver Recursos, ver Cronograma, Plan Maestro, PR, Curva S, RDTs, consolidado RQ) | **Cerrada:** Victor reescribió el flujo 14 con las tablas 1 y 2 (commit 8027037); las filas antiguas ya no conviven | Verificar en F7 (PL-100) |
| C13 | **14**, "Admin siempre tiene bypass total" | **Cerrada:** la tabla 2 lista acción por acción los roles, incluido el administrador y las dos exclusivas; el código se alinea en F5C | Verificar en F7 |
| C14 | **14**, filas de "ver" antiguas; **16**, regla 4 "Toda ruta debe validar autenticación, rol y pertenencia" | **Cerrada** en el 14; el código se alinea en F2B y F5B y la regla 4 del 16 pasa a cumplirse | Verificar en F7 |
| C15 | **14**, "Accesos requeridos para paquetes de trabajo (pendiente, no implementado)" | Paquetes de Trabajo Fase 1 ya está implementado (`puedeVerPaquetesTrabajo`, `puedeGestionarPaquetesTrabajo`) | Actualizar con la matriz derivada |
| C16 | **03**: chips comunes de Mi entorno y "Panel derecho: Subir RDTs clicable sin servicio" | Los chips de Mi entorno ahora envían `?proyectoId=` (Cronograma y Plan Maestro hoy no lo hacen); Mi entorno sale del registro. El 03 no lista Cronograma ni Plan Maestro entre los chips que sí muestra | Actualizar 03 |
| C17 | **05**: Status `/requerimientos` con "Chip Salir a Mi entorno" y filtros por `?ots=`; "Crear RQ: Mi entorno `?accion=crear-rq`" | Decisión 4; nuevo `?proyectoId=` que equivale a `ots=<id>`; Generar RQ ahora también sale del panel izquierdo (sigue abriendo Mi entorno) | Actualizar 05 |
| C18 | **06**: "`/rdts/listado` (**Status de RDTs**)", nav "Subir RDTs, Status de RDTs y Consolidado RDTs", chip "Salir a Mi entorno" | El código tiene `/rdts/status` (Status) y `/rdts/listado` (Archivo de RDTs subidos), más `/rdts/crear`; decisión 4; E3 | Actualizar 06 |
| C19 | **11** y **21**: el chip Dashboard/Curva S "aparece en los tres paneles… desde una única definición", grupo Planificación | Dashboard no está en Mi entorno hoy (A3); en el panel izquierdo van en Reportes (decisión 2 del Spec), en el derecho siguen en Planificación | Añadir la nota de ubicación por panel |
| C20 | **15**: Cronograma "necesita servicio elegido" (decisión previa registrada en el test de `nav-proyecto`) y "Chip Cronograma, único en el apartado Planificación del entorno" | Sigue necesitando servicio (`requiereServicio: 'si'`); al abrir se preselecciona; en Mi entorno pasa a enviar el servicio | Confirmar que no hay conflicto y actualizar la nota |
| C21 | **14**, matriz base: "las pantallas por servicio siguen sujetas al alcance por OT cuando aplica"; matriz de accesos: Curva S "No (lectura)" | **RESUELTA (Victor, 2026-09-28, Registro de decisiones):** el alcance por OT es el requisito de partida para ver cualquier interfaz orientada a un servicio, en todas las pantallas de servicio, no en ninguna. F5B lo implementa en las seis pantallas con economía (PL-174 a PL-179); R30 **resuelta (Victor, 2026-09-29)**: no se agrega alcance por OT al leer en las pantallas sin economía | Verificar en F7 que la nota de la tabla 1 quede coherente con lo implementado |
| C22 | **16**, "Tres paneles" (título y estructura); **design.md** §3 ("estructura fija": nav izquierda, centro, herramientas; "no crear otro layout global… sin aprobación") | El asistente es un cuarto elemento del shell, fuera de los tres paneles: hoy una barra al pie del centro, y con Spec 8 un icono más panel desplegable en toda pantalla | Añadir en el flujo 16 la subsección del asistente y en `design.md` §3 su posición y capas (con la confirmación que exige su regla de evolución) |
| C23 | **03**: "Geren (interno): administrador, jefe de oficina técnica, jefe de proyectos"; chips por grupo ("jefe_de_oficina_tecnica: Status de RDTs, Consolidado RDTs, Subir RDT"; "supervisor_oficina_tecnica: Status de RDTs si `puedeVerRdts`"; "Consolidado RQ solo quien `puedeVerConsolidadoRq`"; SSOMA "sin Subir RDT") | Los 13 roles ven Status y Consolidado de RDTs y el consolidado RQ; el jefe de oficina técnica gana crear y validar o rechazar RDT; el administrador gana crear RQ; el chip deshabilitado deja de aplicar a esas interfaces | Reescribir la tabla de chips por rol de 03 con las tablas 1 y 2 |
| C24 | **06**: "Quien ve carpeta/listado/consolidado: Geren + Administración + Supervisión operativa"; "Quien sube: Supervisión operativa y Geren" | Los 13 roles ven esas interfaces; el jefe de oficina técnica también crea RDT estructurado | Reescribir |
| C25 | **15** ("Quién ve: todos menos asistente"), **20** ("Ver Plan Maestro: todos excepto asistente"; "Crear RDT estructurado: SOp, admin, JP") y **21** (endpoint: "rol (todos menos asistente…)") | Cronograma lo ven los 13 roles; Plan Maestro, los roles de economía más el planner; Curva S, los roles de economía (incluido el jefe de costos); Crear RDT suma al jefe de oficina técnica | Actualizar cada flujo |
| C26 | **05**: consolidado RQ y Status sin restricción explícita de roles; **03**: "Consolidado RQ (solo quien `puedeVerConsolidadoRq`)" | El consolidado RQ (ver) pasa a los 13 roles; la descarga PROM-GP-004 no está definida (A12, V5) | Aclarar en 05 y 03 |
| C27 | **14**, texto pendiente de "Restricción de datos económicos por rol" | **Cerrada:** el flujo 14 reescrito ya lo tiene decidido (tabla 1) | Verificar en F7 |
| C28 | **16** ("Tabla de accesos": "el flujo 14 debe derivarse de los mismos identificadores usados por los paneles y permisos") | El flujo 14 y el artefacto son la base y el registro único se ajusta a ellos; la matriz derivada solo se compara (A9). La regla 10 del 16 ya cita el artefacto, pero esa sección sigue diciendo lo contrario | Reescribir la sección "Tabla de accesos" del 16 |
| C29 | **05**: "Borrar RQ: solo Status, solo `administrador`"; "Crear RQ: ..." sin el administrador (flujo 14 antiguo) | Eliminar requerimiento: administrador **y jefe de proyectos**; el administrador también crea RQ y actualiza su estado | Reescribir la regla de borrado y las de creación y estado en 05 |
| C30 | **06**: "Borrar RDT: solo admin (listado/consolidado)"; quién valida no figura | Eliminar RDT: administrador **y jefe de proyectos**; validar o rechazar RDT suma al jefe de oficina técnica; crear RDT estructurado también lo hace el jefe de oficina técnica | Reescribir en 06 |
| C31 | **08**: "Ciclo de vida de contenedores. **Jefe de oficina técnica adjudica**" | Adjudicar y crear programa y portafolio: administrador, jefe de proyectos **y** jefe de oficina técnica | Reescribir en 08 |
| C32 | **08**: "**Borrado admin:** solo administrador (o jefe OT en proyecto según permiso)" | Archivar y eliminar proyecto, y eliminar contenedor: administrador **y jefe de proyectos**; el jefe de oficina técnica **pierde** archivar y eliminar proyecto | Reescribir en 08 |
| C33 | **08**: "Quien confirma la transición sigue siendo el jefe de oficina técnica" | Confirmar transición: administrador, jefe de proyectos **y** jefe de oficina técnica | Reescribir en 08 |
| C34 | **Índice de `04-flujos-de-negocio/README.md`**: "Borrado administrador... regla transversal (solo admin destruye RQ / RDT / proyecto / programa / portafolio). Está citada en 05, 06 y 08" | El jefe de proyectos también borra RDT, RQ, proyecto y contenedores | Reescribir la regla transversal y sus tres citas (05, 06, 08) |
| C35 | **11**: el interruptor Parcial/Completo "se edita con el mismo permiso que ya edita el proyecto (`puedeAdjudicarProyecto`)" | **RESUELTA (Victor, 2026-09-29):** lo activan los roles que pueden ver datos económicos según la matriz aprobada (`puedeVerEconomia`); los demás lo verían fijo en Parcial, parte que pertenece al plan futuro de `planes-futuros.md`. `puedeAdjudicarProyecto` ya no rige el interruptor | Reescribir en 11 (F7-C); código en F5B-A (`ToggleTipoDashboard` y `tipo-dashboard`) |
| C36 | **20**: "Validar RDT (administrador o jefe de proyectos)"; "Quien puede validar es solamente: administrador, jefe de proyectos"; tabla "Validar o rechazar RDT" | Suma al jefe de oficina técnica; rechazar un RDT ya validado sigue solo con administrador y jefe de proyectos | Reescribir en 20 |

Revisados sin contradicción de reglas de rol (ver la tabla de trazabilidad): 02 (gestionar usuarios: administrador y jefe de proyectos, y solo el administrador asigna el rol administrador, igual que la tabla 2; el flujo 14 lo citaba como posible choque y no lo es), 04, 07, 10, 13, 17, 18 y 19. Los flujos 09 y 12 no dicen quién importa el DP ni quién edita el checklist (vacío V6).

### Vacíos con reglas de negocio ya escritas (nada escrito que contradecir, pero sin dueño)

El asistente (chat) del shell no está documentado en ningún flujo. Se propone dónde integrarlo al cierre, tras consultar a Victor.

| # | Vacío | Propuesta |
|---|---|---|
| V1 | Ningún flujo describe el asistente (`ChatPlaceholder`): ni el 16 (paneles), ni el 03 (Mi entorno), ni el 01 (shell, pendiente de definir). | **Integrar la regla en el flujo 16**, en una subsección nueva "Asistente: elemento del shell fuera de los tres paneles", dentro de su estructura y no pegada al final: icono en toda pantalla del workspace, con y sin servicio, escritorio y móvil; clic despliega el panel y otro clic lo repliega; no es un chip ni forma parte del registro de accesos ni de la matriz del flujo 14; disponible para todos los roles; vista previa sin datos; comportamiento del estado al navegar. Motivo: el 16 es el dueño de la navegación y del shell; el 01 es el contenido original de "interfaz/workspace" marcado como pendiente de definir (basta una referencia breve al shell que apunte al 16); el 03 trata de Mi entorno y no cambia. |
| V2 | El flujo 17 (chat agéntico) es **otra cosa**: un agente que conversa tras leer un archivo subido (presupuesto, cronograma), no habilitado y sin diseño técnico. No define si algún día el asistente del shell será ese agente. | No resolverlo. Añadir en el flujo 17 una aclaración de una línea: "el asistente que hoy se ve en el shell es solo una vista previa sin datos (flujo 16); este flujo describe un agente distinto y sigue sin habilitar". |
| V3 | `design.md` no define ningún patrón de botón flotante ni de panel desplegable (§3 fija tres elementos y §12 prohíbe layouts paralelos sin aprobación). El único precedente es `CajonMovil` (diálogo, Escape, `z-50`) y los modales `z-50`. | La aprobación del Gate 1 cubre el cambio; al cierre `design.md` §3 documenta posición, capas y patrón, con la confirmación que exige su regla de evolución. |
| V4 | La regla "toda pantalla" no dice qué pasa con las pantallas fuera del shell (login, activar, dashboard de portafolio bajo `app/programas/…`). | Definir en el flujo 16 que aplica a las pantallas del workspace; login y activar quedan fuera por no tener sesión, y el dashboard de portafolio se reporta a Victor como excepción (R21). |
| V5 | La tabla 1 y la tabla 2 solo recogen las descargas decididas (registro de costos, consolidado RQ); las demás están en el artefacto como propuesta sin aprobar o no figuran (RDT, listado RQ, exportar DP y las de A13). | A12 y A13 (supuestos). Se escribe la decisión en el flujo 14 cuando Victor la tome (PL-156) |
| V6 | Los flujos **09** (Importar DP) y **12** (Checklist editable) no dicen quién importa el DP ni quién edita el checklist. | Añadir una línea con el enlace a la tabla 2 (importar DP y editar checklist: administrador y jefe de proyectos) |
| V7 | El flujo **16** no describe que un rol pueda entrar a una pantalla sin ver su contenido (logística sube el registro de costos sin verlo) ni las dos excepciones acotadas de la tabla 1 (planner en Plan Maestro, supervisor de oficina técnica en DP). | Escribirlo en 16, dentro de la regla de chips deshabilitados y de "Ver no es acceder" |

### Trazabilidad por flujo (política de coherencia y trazabilidad)

Lista completa de documentos afectados o revisados, con su destino. Es la lista contra la que el Auditor verifica, antes del Gate 2, que no queda ningún flujo o documento sin actualizar ni ninguna referencia a la versión anterior. La columna "Estado" la completa el Worker en el progreso: consulta a Victor hecha, sección actualizada y enlace.

| Documento | Contradicciones o vacíos | Destino (sección) | Estado |
|---|---|---|---|
| `01-configuracion.md` | C11 | "Apartado Proyectos" y "Pantallas de listado…Salir a Mi entorno"; mover la regla de paneles al 16 | Pendiente |
| `02-usuarios.md` | Ninguna (consistente con la tabla 2) | Añadir enlace a la tabla 2 si Victor lo pide | Revisado |
| `03-entorno.md` | C16, C23, C26 | Tabla de chips por rol; "Panel derecho" | Pendiente |
| `04-notificaciones.md` | Ninguna | — | Revisado |
| `05-rq.md` | C17, C26, C29 | Subflujos Status y Consolidado; "Borrar RQ"; creación y estado | Pendiente |
| `06-rdt.md` | C18, C24, C30 | Quién sube, ve y valida; "Borrar RDT"; pantallas | Pendiente |
| `07-nucleo-auth.md` | Ninguna | — | Revisado |
| `08-programa-portafolio-proyecto.md` | C31, C32, C33 | Ciclo de vida, borrado y transición | Pendiente |
| `09-importar-dp.md` | V6 | Línea con quién importa | Pendiente |
| `10-generacion-pr.md` | Ninguna | — | Revisado |
| `11-dashboard.md` | C19, C35 | Ubicación del chip por panel; permiso del interruptor | Pendiente |
| `12-checklist.md` | V6 | Línea con quién edita | Pendiente |
| `13-orden-de-trabajo.md` | Ninguna | — | Revisado |
| `14-accesos-y-restricciones.md` | C21; descargas propuestas sin aprobar (A12) y no listadas (A13) | Ya reescrito por Victor (commits 8027037 y e9ad3c8); se verifica y solo se toca por decisión nueva o por entradas nuevas del registro | Verificar |
| `15-cronograma.md` | C20, C25 | "Quién ve" | Pendiente |
| `16-paneles.md` | C1 a C10, C22, C28, V1, V7 | Reglas de navegación, panel izquierdo, tabla de accesos, subsección del asistente | Pendiente |
| `17-chat-agentico.md` | V2 | Aclaración de una línea | Pendiente |
| `18-control-avance.md` | Ninguna | — | Revisado |
| `19-paquetes-de-trabajo-y-jerarquia-de-control.md` | Ninguna | Los accesos de paquetes viven en el flujo 14 | Revisado |
| `20-plan-maestro.md` | C25, C36 | Permisos, flujo de validación | Pendiente |
| `21-curva-s.md` | C19, C25 | Endpoint y chip | Pendiente |
| `04-flujos-de-negocio/README.md` | C34 | Regla transversal "Borrado administrador" | Pendiente |
| Artefacto «Matriz de permisos» | PL-149 | Toda entrada nueva o cambiada del registro, del asistente, del modo "solo subir" y de las interfaces y acciones nuevas, y la sección «Descargas» (registro de costos y consolidado RQ decididos; tres propuestas pendientes) | Pendiente |
| `01-contexto-repositorio/05-diseno-y-ui.md` y `05-diseno-y-referencias/design.md` | V3 | Política de interfaz nueva, chip deshabilitado, asistente | Pendiente |
| `01-contexto-repositorio/03-entorno-git-y-worktrees.md` | Mejoras del plan | Corrección del pool de ramas y del acceso al repositorio de la app | Pendiente |
| `planes-futuros.md` | Ninguna | "Gestión de permisos desde la app" ya está sometido al artefacto | Revisado |
| Planes cerrados que citan la matriz antigua (por ejemplo `2026-09-20-sub-lote-2-alcance-proyecto.md`) | Ninguna | Son históricos: un plan cerrado no se edita | Sin acción |
| `2026-09-23-paquetes-de-trabajo.md` (abierto) | Ninguna | No cita roles | Revisado |
| `AGENTS.md`, `README.md`, `docs/README.md` | Ninguna | La política ya está en `AGENTS.md` | Revisado |

## Política de interfaz nueva — texto propuesto

Este es el texto que el Worker escribirá, tras la aprobación del Gate 1, como regla del sistema en `16-paneles.md` (integrada en su estructura) y como instrucción para el Worker en `01-contexto-repositorio/05-diseno-y-ui.md`. Lo que sigue es la versión para leer y aprobar aquí.

**Toda pantalla nueva del workspace nace con esta política, sin que Victor tenga que pedirla chip por chip:**

1. **Vive dentro del shell** (`WorkspaceShell`, los tres paneles); no crea layout paralelo.
2. **Se declara una sola vez** en el registro único de accesos, con id, nombre, grupo, tipo (informativo o acción), ruta o acción, si requiere servicio (sí, opcional o no), permiso requerido y en qué paneles es visible. De ese registro salen automáticamente el panel izquierdo, el derecho, Mi entorno, el envío de `?proyectoId=`, el estado habilitado o deshabilitado y la matriz del flujo 14. Si la pantalla no debe tener chip, se declara como excepción con motivo. **Una prueba automática falla si hay una pantalla del workspace sin entrada ni excepción.**
3. **Conserva el servicio.** Recibe `?proyectoId=` (o vive bajo `/proyectos/[id]`), no lo pierde al navegar ni al redirigir (usa el helper de servicio) y lo preselecciona en su selector de OT o en su filtro N° OT. Cambiar el servicio dentro de la pantalla actualiza la URL.
4. **Tiene tipo.** Un chip informativo consulta, visualiza o descarga y no muta datos; un chip de acción ejecuta una operación sobre el servicio actual y lo indica.
5. **Permisos.** Define su función de permiso en `permisos.ts`, con ver, crear, editar, eliminar o archivar, subir, registrar avance y descargar evaluados por separado. La interfaz muestra **deshabilitado, con título explicativo**, lo que el rol no puede usar; el servidor valida autenticación, rol y pertenencia del recurso al servicio, nunca solo el `servicio_id` del navegador. Ver no implica poder.
6. **Sale en la matriz del flujo 14**, derivada del registro; la tabla no se edita a mano.
7. **Diseño.** Respeta `design.md`: componentes existentes, tablas con scroll horizontal y encabezado fijo, sin `max-w-*` en el contenedor de página, navegación móvil, `scope` en los `<th>`.
8. **Estados y colores** de las fuentes únicas existentes (por ejemplo `claseBadgeEstado`); estados de carga, vacío y error contemplados.
9. **Las notificaciones** van a `/notificaciones`, no se duplican en otros paneles.
10. **Su Punch List incluye estos puntos por defecto**, con la prueba de cada permiso por los dos lados (cuenta con permisos altos y cuenta sin permisos de administración) y la prueba de humo del registro.

**Plantilla de ítems para la Punch List de cualquier tarea con pantalla nueva** (el Planner la copia sin que Victor la pida):

| Ítem | Evidencia mínima |
|---|---|
| Existe la entrada del acceso en el registro (o la excepción con motivo) y la prueba de cobertura pasa | `npm test` |
| El chip aparece en los paneles declarados, informativo o acción según corresponda | Captura |
| Abierta desde un servicio, la pantalla conserva `?proyectoId=` en ambos paneles y preselecciona el servicio | Captura + URL |
| Cuenta con permisos altos y cuenta sin permisos de administración: chip habilitado o deshabilitado según el permiso, con título | Tabla + captura |
| URL directa sin permiso: el servidor la rechaza igual que antes | URL + resultado |
| Fila en la matriz derivada del flujo 14 | Diff de la matriz |
| Móvil, scroll horizontal de tablas y estados vacío, carga y error | Capturas |

Ubicación normativa propuesta: la regla del sistema, en el flujo 16 (regla del sistema, integrada en su estructura); la instrucción para el Worker y la plantilla de ítems, en `05-diseno-y-ui.md`. Que el Planner incluya la plantilla en toda Punch List con pantalla nueva es una instrucción para el rol Planner: si Victor quiere que viva también en el estándar agnóstico (`00-estandar-agentes/`), es una propuesta que el Auditor puede elevar en su informe; el Planner no la modifica.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-09-27 | El servicio seleccionado se conserva entre pantallas mediante `?proyectoId=` en la URL. | Victor |
| 2026-09-27 | El panel izquierdo con servicio lo ven todos los roles; los chips sin permiso se muestran deshabilitados (visibles, no accesibles), igual que en Mi entorno. Contradice el flujo 16 (reglas 2 y 3), el flujo 01 (Apartado Proyectos solo admin/JP) y la fila del flujo 14. Los flujos se editan al cierre, no antes. | Victor |
| 2026-09-27 | Los recursos de empresa no se reemplazan por los del servicio al abrir uno: llevan un botón mostrar/ocultar, con o sin servicio. | Victor |
| 2026-09-27 | "Materiales" se elimina de Recursos de empresa (no es un recurso de empresa). | Victor |
| 2026-09-27 | Deseable/opcional: los chips del panel derecho abren la pantalla destino con el servicio ya elegido en el selector de OT. **(Reemplazada por la fila siguiente.)** | Victor |
| 2026-09-27 | Gate Spec aprobado. Ajuste: el clic en el panel derecho **ya no es opcional**; como ya existen chips que redirigen exactamente al servicio, se estandariza para todos los chips con pantalla existente. | Victor |
| 2026-09-27 | Un chip cuya pantalla no existe puede seguir inerte; uno cuya pantalla ya existe debe funcionar. | Victor |
| 2026-09-27 | "Aprobado todo": se autoriza el commit y push de este plan a `main`; se aprueban las recomendaciones de las decisiones 1 (Recursos de empresa: visible sin servicio, oculto con servicio), 2 (PR, Dashboard y Curva S en "Reportes") y 7 (migrar todos los chips al registro único, en fase propia previa). Las decisiones 3–6 no tenían recomendación y quedan abiertas para el Gate 1. | Victor |
| 2026-09-27 | Toda interfaz nueva debe crearse con toda la política de interfaces que corresponda, aplicada de forma estandarizada y sin que Victor tenga que indicar "falta el chip en este panel o en aquel". Se agrega al Spec como resultado esperado 7 (registro único + política escrita + prueba automática). | Victor |
| 2026-09-27 | **E2 se implementa ahora** ("unifiquemos todo"): el código debe cumplir lo que dicen los flujos 14 y 16 (toda ruta valida autenticación, rol y pertenencia al servicio). Se añaden la fase F1B y los ítems PL-88 a PL-101: guardias de rol en servidor para PR, Dashboard, DP (ver) y Status de Requerimiento, con funciones nuevas en `permisos.ts` que el registro usa como `permiso`, pruebas por los dos lados y barrido de los 13 roles. | Victor |
| 2026-09-27 | Conjuntos de roles de E2: Ver PR y Ver Curva S = todos menos asistente (regla vigente del flujo 14). **PROPUESTO, Victor confirma:** Dashboard y DP (ver) = el mismo conjunto que PR; Status de Requerimiento = los 13 roles. F1B no empieza sin la confirmación. | Planner propone; Victor confirma (pendiente) |
| 2026-09-27 | **A4 cambia:** Recursos de empresa es visible para los 13 roles, igual que todo el panel izquierdo; lo que el rol no puede usar se muestra deshabilitado con título (ver no es acceder). `puedeVerRecursos` deja de gobernar la visibilidad y queda como permiso de acceso. | Victor |
| 2026-09-27 | La rama `local-worker-1` fue creada por el Orquestador desde `main` (commit `1942b01`) con autorización de Victor. El worktree `.worktrees/local-worker-1` no se pudo crear: la ruta está ocupada por un resto de una sesión anterior. Victor debe autorizar retirar o renombrar ese resto (el Orquestador se lo consulta). Corrección del Planner: `.worktrees/` sí existe. | Orquestador (con autorización de Victor para la rama) |
| 2026-09-28 | **Matriz base de visibilidad por interfaz (Victor).** Escrita en el flujo 14 (sección "Matriz base de visibilidad por interfaz"), que pasa a ser la base de restricciones y accesos por rol. Reglas: (1) las interfaces **sin** datos económicos las ven los 13 roles; (2) las **con** datos económicos (Dashboard del servicio y del portafolio, PR, DP ver, Curva S, Plan Maestro ver, Registro de costos) solo 4 roles: administrador, jefe de proyectos, jefe de oficina técnica y supervisor de costos; (3) administrador y jefe de proyectos tienen acceso a todo; (4) el jefe de oficina técnica puede crear RDT; (5) los recursos de empresa los ven todos. **Reemplaza** el criterio de E2 ("todos menos asistente") y el supuesto A4 (Recursos solo admin/JP), y **anula** "que el asistente vea todo" para las pantallas con economía. Los flujos 01, 16 y 03 se ajustan al cierre. Conflictos abiertos (planner/Plan Maestro, SOT/DP, SLog/Registro de costos, jefe de costos, acciones destructivas del JP) listados en el flujo 14; hasta que Victor los resuelva la regla se aplica al pie de la letra. | Victor |
| 2026-09-28 | **Correcciones a la v5 (Victor, respuesta a las 3 dudas).** (1) El jefe de proyectos **sí** puede subir documento del proyecto (catálogo AL_INICIO/CIERRE); no había casilla en el artefacto para esa acción — omisión del Orquestador, no decisión de Victor, corregida (artefacto v.19, flujo 14 fila 4). La frase "acceso a todo excepto dos" del flujo 14 se retira: no hay una regla general de "todo menos N", cada acción se decidió una por una; quedan por confirmar si el jefe de proyectos también debe tener actualizar estado de RQ y subir registro de costos (hoy exclusivos de logística). (2) **Confirmado:** el Dashboard Parcial no tiene datos económicos y lo ven los 13 roles; el Completo sí y lo ven los roles que corresponde. Hoy el código muestra economía en ambos modos (flujo 11); esta es la regla objetivo hasta que el Spec futuro de economía separe los datos reales — la fase F0 debe señalar esa brecha en el informe antes/después. Quién alterna Parcial/Completo queda propuesto (administrador y jefe de proyectos) sin confirmar. (3) **Confirmado, cierra C21:** el alcance por OT (`proyecto_miembros`) es el requisito de partida para ver cualquier interfaz orientada a un servicio, en todas las pantallas de servicio, no en ninguna. | Victor |
| 2026-09-28 | **Matriz de permisos APROBADA por Victor en el artefacto** (marcas versión 17, aprobada el 2026-09-28 16:02 UTC). **Reemplaza** los conjuntos de roles de E2, la recomendación del Planner para CO1 a CO5 y los supuestos A4 y A12 donde difieran. Queda escrita completa en el flujo 14 (tabla 1: interfaces; tabla 2: acciones), que es la única fuente de permisos del plan. **CO1 a CO5 quedan RESUELTOS**: planner ve y gestiona Plan Maestro; supervisor de oficina técnica ve el DP pero **ya no lo importa**; supervisor de logística solo sube el registro de costos; jefe de costos entra a las interfaces con economía; administrador y jefe de proyectos tienen acceso a todas las interfaces y a todas las acciones salvo asignar rol administrador y «Ver como» (exclusivas del administrador). Cambios de acciones respecto de la propuesta: jefe de proyectos gana adjudicar y crear programas y portafolios, archivar proyectos, eliminar contenedores, editar servicio, editar checklist, importar DP, editar su perfil y los borrados definitivos de RDT y RQ; el jefe de oficina técnica gana crear RDT y validar o rechazar RDT y **pierde** archivar proyectos, editar servicio, editar checklist y editar su perfil; el administrador gana crear RQ y actualizar estado de RQ. Ya no hay conflictos abiertos de permisos: **F5B y F5C dejan de estar condicionadas** (solo queda por decidir la descarga del registro de costos y del consolidado RQ, notas 2 y 5 del flujo 14). Los flujos que contradicen esta matriz (02, 05, 06, 08, 12, 13 y los que el Planner identifique) se ajustan al cierre con consulta a Victor, por la política de coherencia y trazabilidad. | Victor |
| 2026-09-28 | **Artefacto «Matriz de permisos» y políticas de coherencia y trazabilidad (Victor).** Se publicó el artefacto https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT (interfaces con y sin economía; acciones; casillas por rol, comentarios y aprobación) como instrumento editable de la matriz. Victor ordenó: (1) el artefacto es la base del flujo 14, ligado al flujo 16, y ambos flujos lo **citan**; (2) toda interfaz, acción, permiso o acceso nuevo actualiza el artefacto; (3) si un Spec o plan entra en conflicto con estos flujos, la implementación abarca **todos** los afectados, con trazabilidad y sin dejar nada suelto; (4) guardarlo como política de este repositorio. **Aplicado por el Orquestador por orden expresa de Victor:** política en `01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md` § Políticas de coherencia y trazabilidad, puntero en `AGENTS.md`, cita del artefacto en el flujo 14 (sección base y "Gestión visual de accesos") y en el flujo 16 (regla 10), y el plan futuro «Gestión de permisos y accesos desde la app» en `planes-futuros.md`. **Para el Auditor:** este cambio toca `AGENTS.md` y `01-contexto-repositorio/`, que el estándar reserva al camino Auditor propone, Gate 2 aprueba, Orquestador aplica; se aplicó antes por instrucción directa de Victor y debe revisarse en la auditoría y en el Gate 2. El Auditor también verifica la política nueva: que ningún flujo afectado por este plan quede sin actualizar. | Victor (ordena) / Orquestador (aplica) |
| 2026-09-28 | **Aclaración sobre "Registro de costos".** Es un archivo (`.xlsx`, `.xls`, `.pdf` o `.csv`) que Logística sube por servicio y el jefe de proyectos descarga (`PanelRegistroCostos`); no es el RQ. Los RQ no tienen costos (descripción y cantidad). | Orquestador |
| 2026-09-28 | **Plan futuro registrado** en `planes-futuros.md`: "Dashboard Parcial sin datos económicos y restricción económica definitiva" (Spec aparte, a pedido de Victor). Fuera del alcance de este plan. | Victor |
| 2026-09-27 | **Limpieza de ramas y worktrees.** Victor: "sobre las ramas, worktree, sigue la política, limpia ramas y renómbralas, lo mismo con los worktree". Ejecutado por el Orquestador tras inventario en solo lectura: (a) `py_control_proyectos_web`: worktree `.worktrees/local-worker-1` creado sobre la rama `local-worker-1` (que ya cumple `<entorno>-worker-N`, sin renombrar); restos de `.worktrees/` limpiados según "Entorno" (dos carpetas vacías retiradas, `nucleo` y `local-worker` renombrados con prefijo `hist_`); no había ramas locales ni remotas viejas. (b) `pg_control_proyectos`: se borraron del remoto las dos ramas `claude/opus-token-consumption-9mkqsf` (`421c6bc`) y `claude/reestructuracion-documental-pg-control-jvj5mf` (`d571f21`), ambas **con 0 commits sin mergear** (todo su contenido ya está en `main`); los SHAs quedan anotados para poder recrearlas. Los `git stash` del repositorio de la app (`feat/rdt: wip-local-rq` y `frontend-redesign`) **no se tocaron**: son trabajo sin mergear, no ramas. | Victor (autoriza) / Orquestador (ejecuta) |
| 2026-09-27 | **Aclaración de un malentendido.** En la consulta de los conjuntos de roles de E2, "asistente" era el **rol de usuario "Asistente"** (uno de los 13 roles, como supervisor o planner), no el chat de ayuda. Victor pidió aclaración; la **confirmación de esos conjuntos de roles sigue pendiente** (F1B no empieza sin ella). | Orquestador |
| 2026-09-27 | **Asistente (chat de ayuda) en toda pantalla, como icono.** Victor: "el asistente debería aparecer en todas las interfaces, pero para ganar espacio podemos crearle un icono; al hacerle clic recién mostrar su apariencia". Se agrega al Spec como resultado esperado 8. Solo cambia dónde y cómo se muestra la vista previa; conectarlo a datos reales queda fuera (flujo 17). | Victor |
| 2026-09-27 | **`.env.local` al worktree: autorizado, y ya no se vuelve a preguntar** en esta ni en otras tareas. Ejecutado por el Orquestador: copia del `.env.local` del checkout principal a `.worktrees/local-worker-1/.env.local` sin leer ni mostrar valores; verificado idéntico con `cmp`; git lo ignora (0 cambios en el worktree). Registrado como mejora de trabajo. | Victor (autoriza) / Orquestador (ejecuta) |
| 2026-09-27 | **`hist_nucleo/.env.local` se conserva.** Victor preguntó si eliminarlo afecta al Worker y pidió no borrarlo si es la única fuente de credenciales. Verificado sin mostrar valores: el Worker usa el `.env.local` del checkout principal (otro archivo); el de `hist_nucleo` **difiere** de ese (220 y 211 bytes; 2026-08-16 y 2026-08-19; mismas tres variables), así que no se puede demostrar que sea una copia redundante. No se borra. | Orquestador |
| 2026-09-27 | **Modo de ejecución local.** Worker y Auditor corren como subagentes de la sesión del Orquestador. Un subagente no puede conversar con Victor: la excepción D6 se aplica así: el Worker se detiene, registra la pregunta en el plan, la devuelve al Orquestador en su reporte final; el Orquestador la relaya a Victor, registra la respuesta y reanuda al Worker con `SendMessage`. Etiquetas lógicas: Worker `local_3.worker_paneles-servicio-persistente-fase1`, Auditor `local_4.auditor_paneles-servicio-persistente`. | Victor / Orquestador |
| 2026-09-27 | **Aprobación con cambios del Gate 1**: Victor respondió con los cambios anteriores y dijo "dejemos al agente continuar" y "se crean las ramas y worktree según la política". El Orquestador lo trata como aprobación con cambios y conserva las recomendaciones del Planner para las decisiones 3, 4, 5, 6, E1 y E3 y los supuestos A1 a A3 y A5 a A9. Como E2 y A4 traen ítems nuevos, el plan vuelve a `Pendiente del Responsable humano`. | Victor / Orquestador |
| 2026-09-28 | **Hallazgo de Victor: falta gestión de Recursos en la matriz — recorrió las interfaces y buscó las acciones.** "Vi una acción que no aparece en tu artefacto y es crear cargos, es decir personal, en los 4 recursos; en solo dos de ellos se puede AGREGAR, debería ser en los 4 y no solo agregar sino eliminar o editar un recurso existente; además no vi quién solo puede realizar estas acciones en Recursos." Verificado en el código, no supuesto: **Personal** solo permite crear; **Cargos** y **Equipos** son de **solo lectura** (nadie puede escribir); **Causas CNC** permite crear y activar/desactivar (no edita el texto, no borra). No había ninguna de estas acciones en el artefacto — omisión del Orquestador. Se agregaron 12 filas nuevas al artefacto (grupo «Recursos»), con administrador y jefe de proyectos como propuesta, y las que no existen en el código marcadas «por construir»: editar/eliminar Personal, crear/editar/eliminar Cargos, crear/editar/eliminar Equipos, editar el texto de una Causa CNC. **Aprobado por Victor en el artefacto** (versión 35, 2026-09-28 23:47:41 UTC, sin ediciones posteriores — verificado dos veces por el Orquestador antes de fijarlo). Escrito ahora en el flujo 14 como decidido (tabla 2, grupo "Recursos", nota ⁶): administrador y jefe de proyectos pueden crear, editar y eliminar (o desactivar) en los cuatro recursos por igual, y editar el texto de una causa CNC. Las acciones marcadas "(por construir)" en el flujo 14 son trabajo nuevo para el Worker (editar/eliminar Personal; crear/editar/eliminar Cargos y Equipos; editar texto de Causas CNC), no solo una guardia de permisos — el Planner debe sumarlas a la Punch List y a las fases del plan. | Victor (hallazgo y aprobación) / Orquestador (verifica y aplica) |
| 2026-09-29 | **Duda (a) anulada.** Actualizar estado de RQ y subir registro de costos siguen siendo exclusivos de logística; el jefe de proyectos no los gana. No cambia la matriz ni el flujo 14. | Victor |
| 2026-09-29 | **A13 llevado al artefacto.** Se agregaron 5 filas a la sección «Descargas» del artefacto «Matriz de permisos» (versión 5 de la página): plantilla de cronograma, PDF de un RDT estructurado, archivo de un RDT subido, PDF individual de un RQ y formato vacío PROM-GP-008, cada una con la regla actual del código como propuesta. Victor las confirma o ajusta en el artefacto y vuelve a aprobar; hasta entonces el flujo 14 no se toca (PL-155, PL-156). | Orquestador (Victor lo pidió) |
| 2026-09-29 | **R30 resuelta: no se toca.** Victor: limitar Cronograma, Paquetes de Trabajo, RDTs y RQ a las OT asignadas al usuario restringiría demasiado; se dejan como están. En esas pantallas este plan solo da acceso y restringe a quien corresponde según la matriz; no se agrega alcance por OT al leer (PL-181 se cierra con esta respuesta). La regla de alcance por OT al leer queda solo en las seis pantallas con economía (PL-174 a PL-179). | Victor |
| 2026-09-29 | **C35 resuelta: interruptor Parcial/Completo del Dashboard.** Los roles que pueden ver datos económicos según la matriz aprobada pueden activarlo; los roles sin acceso a datos económicos lo ven fijo en Parcial y no pueden cambiarlo. Como hoy el Parcial también muestra dinero y esos roles no ven el Dashboard, la parte «Parcial sin economía para los demás roles» pertenece al plan futuro ya registrado en `planes-futuros.md`; en este plan el interruptor sigue a los roles con economía de la matriz. Flujo 11 se edita al cierre. | Victor |
| 2026-09-29 | **Artefacto: descargas separadas.** La sección «Descargas» del artefacto se divide en «Descargas con datos económicos» (registro de costos, exportar DP) y «Descargas sin datos económicos» (las otras ocho), sin cambiar casillas ni ids. | Victor (pide) / Orquestador (ejecuta) |
| 2026-09-29 | Victor: el Orquestador lanza las tandas una tras otra y decide por su cuenta lo que pueda decidir; solo consulta a Victor por lo que no le corresponda decidir (contradicciones con flujos escritos, cambios de permisos, acciones destructivas o de infraestructura no autorizadas, dudas de negocio). | Victor |
| 2026-09-29 | **Plan v8: ejecución por tandas.** El Planner reparte la ejecución en 38 tandas (un Worker por tanda, en serie, un solo worktree), con briefs de ≤ 8 KB, reglas de contexto, línea base y medición, en `2026-09-27-paneles-servicio-persistente-briefs/`; PL-181 se cierra por R30 y PL-90 se ajusta por C35 (decisiones de Victor de la misma fecha, ya registradas arriba). Cobertura de los 180 ítems abiertos verificada por script. **Pendiente del Gate 1 de Victor.** Pregunta abierta para Victor: registros de prueba marcados en Recursos (R32). | Planner propone; Victor aprueba en el Gate 1 (pendiente) |
| 2026-09-30 | **A12 confirmado por Victor.** Descargar RDTs (ZIP y PDF PROM-GP-0006), el PDF de un RDT, el archivo de RDT subido y el listado RQ (PDF) quedan abiertos a los 13 roles; un usuario sin rol conocido queda rechazado. Se agrega la guardia de rol a `requerimientos/exportar` (F2B-B). |
| 2026-09-30 | **Precios (Victor):** ningún rol sin permiso de economía debe recibir precios, ni en la interfaz ni en las respuestas de la API. Se retiró `precio_unitario` del select de Paquetes de Trabajo (F2B-B); PR, Dashboard, DP, Curva S, Plan Maestro y Registro de costos quedan restringidos a economía (F5B). |
| 2026-09-30 | **Registros de prueba en Recursos (Victor):** autorizados registros de prueba marcados `PRUEBA-PL`, sin borrar filas (baja = `activo=false`), dejados todos desactivados (F5D-A/B, F6-C: 12 registros). |
| 2026-09-30 | **Edición de Cargos y Equipos (Victor):** no se renombra un cargo o equipo ya en uso; se crean los que faltan y solo se editan unidad, categoría y activo. |
| 2026-09-30 | **Confirmadas por Victor (ya no provisionales):** el dashboard del portafolio muestra solo las OT con alcance del usuario (el administrador todas); perfil extendido solo administrador y jefe de proyectos (tabla 2); `GET /api/cronograma` y `/api/rdts/consolidado` sin alcance por OT en lectura (R30). |
| 2026-09-30 | **Reescritura de flujos aprobada por Victor** (16, 01, 17, 03, 05, 06, 08, 09, 11, 12, 15, 20, 21, README, `05-diseno-y-ui.md`, `design.md`) según las resoluciones C1 a C36 y V1 a V7; **descargas de A13** (plantilla de cronograma, PDF de RDT estructurado, archivo de RDT subido, PDF individual RQ, formato vacío PROM-GP-008): los 13 roles, usuario sin rol conocido rechazado; **actualizar el artefacto** «Matriz de permisos» autorizado (publicado v7 por F7-B; el estado «En revisión» solo lo cambia Victor). |
| 2026-09-30 | **Incidente F7-B:** un script del Worker vació este archivo; se restauró desde HEAD (66e1026) y se reaplicaron los estados de la Punch List desde los handoffs. Notas sin commitear que no eran estados pudieron perderse: las decisiones de esta fecha se repusieron arriba. |

## Enlaces a progreso y evidencia homónimos

Se crean al pasar el Gate 1 (`02-progreso/` y `03-evidencia/` con este mismo nombre de archivo).

## Mejoras (de trabajo)

**Trasladadas en F7-D (2026-09-30)** a `docs/03-aprendizaje-continuo/2026-09-30-plan-paneles-servicio-persistente-tandas.md` (lecciones y medición) y a `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (pool de ramas y worktrees). Se conserva el detalle original abajo como registro.

- `03-entorno-git-y-worktrees.md` (§ "Pool real de ramas y worktrees") afirma que este repositorio no tiene acceso directo a `py_control_proyectos_web`. Es inexacto: el repositorio de la app está en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`, accesible desde una sesión local, y se pueden correr `git`, el servidor de desarrollo y Playwright sobre él (verificado 2026-09-27). Corregir al cierre.
- Cuando se hacen varias llamadas de Playwright en paralelo sobre el mismo navegador, las navegaciones se pisan. Encadenar una a una.
- Lección del Planner (2026-09-27): para saber solo el **rol** de una cuenta de prueba, no se abre ni se filtra con `sed`/`grep` el archivo de credenciales de la memoria (`cuentas-prueba.md`): la salida de la herramienta imprimió valores que no debían mostrarse. Los valores no se copiaron a ningún archivo ni a este plan, pero la exposición ocurrió en la salida de una herramienta. Práctica: el rol de la cuenta se pregunta a Victor o lo lee el Worker de la propia interfaz (pie del panel izquierdo). Conviene además que el archivo de la memoria separe el rol de las credenciales.
- `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (§ "Pool real de ramas y worktrees") además dice "por verificar"; el Planner lo verificó el 2026-09-27 solo con `git` (solo `main`, un único worktree) y concluyó, sin comprobarlo con `ls`, que no había carpeta `.worktrees/`; **sí la había**, con restos de sesiones anteriores (ver "Entorno"). Estado real tras la limpieza del Orquestador (2026-09-27): ramas `main` y `local-worker-1`; worktrees: checkout principal y `.worktrees/local-worker-1`; `.worktrees/hist_nucleo` y `.worktrees/hist_local-worker` conservados. Actualizar la sección al cierre con este resultado y retirar la tabla obsoleta de `work-1`/`work-2`.
- Lección del Planner (2026-09-27, versión 2): afirmé que la carpeta `.worktrees/` no existía sin haberlo comprobado; solo había corrido `git worktree list`, que no muestra carpetas sueltas. El Orquestador comprobó con `ls` que sí existe y tiene restos. Práctica: la existencia de una carpeta se comprueba con `ls`, no se infiere de la salida de `git` (refuerza `2026-09-23-verificar-antes-de-afirmar.md`).
- **Modo local con subagentes y la excepción D6.** El estándar (`04-flujo-sdd-y-planes.md`, "Excepción de consulta directa del Worker (D6)", y `02-roles-y-delegacion.md`) supone que el Worker tiene un chat propio donde consulta a Victor. Con Worker y Auditor como subagentes del Orquestador eso no es posible. Ajuste usado en esta tarea: el Worker se detiene, registra la pregunta y la devuelve al Orquestador, que la relaya y reanuda al Worker con `SendMessage`. Al cierre, proponer (vía Auditor) que el estándar describa este modo. Los nombres de chat del modo local son etiquetas lógicas.
- **Autorización permanente para el `.env.local` de los worktrees (Victor, 2026-09-27: "no volver a la pregunta en demás tareas").** Copiar el `.env.local` del checkout principal al worktree de un Worker, entre carpetas locales del mismo proyecto, **no requiere consulta** en esta ni en tareas futuras. Cómo: `cp` sin leer ni mostrar valores, verificar con `cmp`, comprobar que git lo ignora (`git status` del worktree en 0). Alcance: solo `.env.local` del mismo proyecto; cualquier otro archivo de entorno o de secretos se sigue consultando. Reemplaza la regla anterior "se consulta antes de copiar". Al cierre, trasladar a `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (§ Worktrees) y al índice de `03-aprendizaje-continuo/`.
- **Política: un cambio que choca con flujos se implementa en todos los afectados (Victor, 2026-09-28).** Cuando un Spec o plan entra en conflicto con lo escrito en un flujo, en el artefacto de permisos o en otro plan, la implementación cubre todos los afectados, con enlace a cada uno, y nada queda suelto. Ya aplicada en `01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md` y `AGENTS.md`. Al cierre, dejar constancia en `03-aprendizaje-continuo/` de cómo se aplicó en esta tarea (lista de contradicciones C1 a C28 con su destino).
- **El archivo con credenciales que se copia y el que se conserva no son el mismo.** Al limpiar restos de worktrees hay que comparar (por `cmp`/hash y por nombres de variable, sin mostrar valores) antes de proponer borrar un `.env.local`: un archivo con el mismo nombre puede ser una versión distinta y ser la única fuente de otras credenciales.
- **Un Worker de fase entera no cabe en una sesión (2026-09-29).** Con 181 ítems y 13 fases, el plan v7 asumía un solo Worker. La medición de otro plan de Victor (`hermes_agent`: 156–191 llamadas, 625–682k de contexto, 84–97M de caché por Worker de fase; ~28M y contexto máximo de 186k al repartir en tandas) llevó a la v8: tandas de 1 a 8 ítems con brief de ≤ 8 KB, una sesión por tanda, metas de llamadas, contexto y caché y un script de medición. Al cierre, trasladar a `03-aprendizaje-continuo/` con los resultados reales de `medicion.md`.

## Reglas de negocio acordadas en esta tarea

Ver "Registro de decisiones". Se trasladan a `04-flujos-de-negocio/` (16, 01, 14 y los que apliquen) al cierre, integradas en su estructura, tras la consulta con Victor de cada contradicción. **Verificado en F7-D (2026-09-30):** ya están aplicadas en los flujos por F7-A a F7-C2 (tabla «Trazabilidad por flujo» del progreso); no se creó ningún archivo aparte.

## Carpetas/archivos huérfanos

- ~~`vpc/` en la raíz de `pg_control_proyectos`~~: **ya no existe** (verificado por el Orquestador el 2026-09-28). No queda acción.
- `.worktrees/` en `py_control_proyectos_web` (verificado por el Orquestador el 2026-09-27): restos de sesiones anteriores, no creados por esta tarea. **Tratados por autorización de Victor** (ver Registro de decisiones): las carpetas vacías `local-worker-1` y `work-1` (solo un enlace a `node_modules`) se retiraron; `nucleo` y el archivo `local-worker` se renombraron a `hist_nucleo` y `hist_local-worker`. **Siguen ahí, sin abrir:** `hist_nucleo/.env.local` (fechado 2026-09-19, contiene valores de entorno; Victor decide si se conserva o se elimina) y `hist_local-worker` (script JavaScript de 806 bytes).
- Dos `git stash` antiguos en `py_control_proyectos_web` (`stash@{0}` en `feat/rdt` "wip-local-rq" y `stash@{1}` en `frontend-redesign`): trabajo sin mergear de sesiones anteriores. Reportados; no se tocan.

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

Ninguno por ahora.
