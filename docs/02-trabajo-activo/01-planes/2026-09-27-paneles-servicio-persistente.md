# Paneles: servicio persistente y panel izquierdo completo

## Identificación y estado

- Tema: paneles con servicio persistente y panel izquierdo completo (flujo 16).
- Fecha: 2026-09-27.
- Estado: `Pendiente del Responsable humano` — Spec/SDD aprobado en el Gate Spec (2026-09-27, con un ajuste incorporado). Plan, Punch List y análisis de decisiones abiertas redactados por el Planner (2026-09-27), listos para el Gate 1.
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

## Alcance

- Conservar el servicio en la URL en todas las pantallas del workspace y hacer que el shell lo reconozca (`WorkspaceShell.tsx`).
- Completar el panel izquierdo con servicio según el resultado esperado 2–5.
- Añadir botón mostrar/ocultar a Recursos de empresa; quitar Materiales de esa sección.
- Que las pantallas de RDTs, Requerimientos, Consolidado RQ y las que hoy no leen el servicio lo reciban por `?proyectoId=` y lo preseleccionen, y que **todos** los chips del panel derecho con pantalla existente lo envíen (`hrefItemPanel`).
- Crear el registro único de accesos, migrar a él los chips existentes y derivar de él ambos paneles, Mi entorno y la matriz del flujo 14 (resultado esperado 7).
- Escribir la política de "interfaz nueva" en su lugar normativo (regla del sistema → flujo 16; instrucción para el Worker → `01-contexto-repositorio/05-diseno-y-ui.md`) y añadir una prueba automática que la haga cumplir.
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
- **Verificado por el Planner el 2026-09-27** (solo lectura, `git` en el repositorio de la app): `git branch -a` muestra únicamente `main` y `remotes/origin/main`; `git worktree list` muestra solo el checkout principal (`main`, commit `1942b01`); árbol limpio; no existe la carpeta `.worktrees/`. **La rama `local-worker-1` y su worktree `.worktrees/local-worker-1` no existen todavía**: crearlos requiere autorización explícita de Victor (la pide el Orquestador al aprobarse el Gate 1). En un worktree con `node_modules` como Junction, `npm run dev` y `npm run build` deben ir con `--webpack` (ver `01-contexto-repositorio/03-entorno-git-y-worktrees.md`). El worktree necesita las variables de entorno locales (`.env.local`, no versionado): el Worker no lee ni muestra sus valores; si hace falta copiarlo entre carpetas locales lo consulta con Victor.
- Documentación: todo lo que el Worker escriba en `pg_control_proyectos` va a `main` directo (commit + push, `git add` explícito), nunca a `vpc/`.

## Resumen para el Gate 1

Lo que Victor decide al aprobar este plan (detalle en las secciones indicadas):

1. **Plan y Punch List** (secciones "Fases y dependencias" y "Punch List embebida"): 8 fases, un solo Worker, 87 ítems verificables con Playwright y las dos cuentas de prueba.
2. **Decisiones abiertas 3, 4, 5 y 6 del Spec**: opciones y recomendación en "Decisiones abiertas 3 a 6 — opciones y recomendación". Resumen de recomendaciones: (3) chips del panel derecho también visibles y deshabilitados; (4) conservar "Salir a Mi entorno" pero que preserve el servicio; (5) "(OT) Orden de trabajo" y "Recursos hh, hm, mat (s/c)" quedan inertes; (6) Registro de costos en Reportes y un grupo "Servicio" con Ficha del servicio, Editar servicio y Editar checklist.
3. **Tres conflictos con reglas ya escritas que el Spec no cubría** (E1 a E3, en "Decisiones adicionales que necesitan respuesta de Victor"): acciones "fijadas" vs. selector editable; pantallas sin guardia de rol (PR, Dashboard, DP, Status RQ) frente a los flujos 14 y 16; destino de "Status de RDTs" en Mi entorno.
4. **Contradicciones con flujos ya escritos** (sección "Contradicciones con reglas de negocio ya escritas"): 20 puntos, ninguno se edita antes del cierre y cada uno se consulta a Victor antes de tocar el flujo.
5. **Supuestos menores A1 a A9** (sección "Supuestos menores del Planner"): aprobar el plan los aprueba salvo que Victor los objete.
6. **Autorización de infraestructura**: crear la rama `local-worker-1` y su worktree en `py_control_proyectos_web` (la pide el Orquestador; el Planner no crea nada).
7. **Texto de la política de "interfaz nueva"** (sección "Política de interfaz nueva — texto propuesto"): es lo que el Worker copiará al flujo 16 y a `05-diseno-y-ui.md`; conviene que Victor lo lea aquí antes de que se escriba en las fuentes de verdad.

Dimensión estimada: tarea grande. Unos 35 a 45 archivos del repositorio de la app (3 a 5 nuevos), sin migraciones ni cambios de base de datos, y 8 a 10 documentos de `pg_control_proyectos` al cierre.

## Fases y dependencias

Un solo Worker, en orden. Los archivos compartidos (`WorkspaceShell.tsx`, `nav-proyecto.ts`, `grupo-proceso.ts`, `permisos.ts`, `PanelSecciones.tsx`, `CabeceraPagina.tsx`) impiden paralelizar de forma segura (ver "Asignación de roles").

| Fase | Contenido | Depende de | Punto de commit/push a `local-worker-1` |
|---|---|---|---|
| **F0 — Preparación y línea base** | Con la rama y el worktree autorizados: `npm test`, `npm run lint` y `npm run build` sobre `main` para fijar el baseline (lint se compara contra `main`, no contra cero; el baseline de 2026-09-23 fue 9 errores/18 advertencias y hay que volver a medirlo). Capturas Playwright de la línea base: los dos paneles y Mi entorno con cada cuenta, con y sin servicio, en escritorio y móvil, y una tabla "chip → destino → habilitado" del comportamiento actual (base de la regresión). Elegir los servicios de prueba SV1/SV2/SVX (ver Punch List). | Gate 1 aprobado + rama/worktree autorizados | Ninguno (solo evidencia) |
| **F1 — Registro único de accesos y migración de todos los chips** | Crear el registro con los metadatos del flujo 16 (id, nombre, grupo, tipo, ruta o acción, requiere servicio, permiso, visibilidad por panel). Migrar **todos** los accesos existentes: 41 ítems de `NAV_PROYECTO`, los 10 chips de `herramientasPorGrupo` (Mi entorno), `CHIPS_ACCESO_RAPIDO` y las rutas fijas del panel izquierdo (Personal, Cargos, Equipos, Causas CNC). `NAV_PROYECTO`, `herramientasPorGrupo` y `hrefItemPanel` pasan a ser derivaciones del registro. **Sin cambio visible** salvo las diferencias declaradas (ver PL-52). Prueba de equivalencia: lo que derivan Mi entorno y el panel derecho es idéntico a la línea base de F0. Actualizar los contadores congelados de `nav-proyecto.test.ts`. | F0 | Al cerrar la fase |
| **F2 — Servicio persistente** | Reconocer `?proyectoId=` en toda ruta del workspace además de `/proyectos/[id]/…` (`resolverProyectoId` de `WorkspaceShell.tsx`); mostrar el servicio actual en el panel izquierdo y validarlo contra los servicios visibles del usuario; que el registro envíe el servicio a todo acceso; que las pantallas lo reciban y lo preseleccionen (selector de OT o filtro N° OT según la pantalla); que los redirects del servidor y las salidas de formularios lo conserven (14 páginas con `redirect('/mi-entorno')`, 2 `router.push`, `CabeceraPagina`, redirect de `/proyectos/[id]/requerimientos`); sincronizar el selector interno de cada pantalla con la URL (A1). | F1 | Al cerrar la fase |
| **F3 — Panel izquierdo completo** | Panel izquierdo con servicio para los 13 roles; grupos y chips según Spec 4 y decisiones 5 y 6; chips no autorizados deshabilitados con título; chips sin pantalla inertes; informativos separados de acciones; Recursos de empresa con botón mostrar/ocultar (visible sin servicio, oculto con servicio) y sin "Materiales"; `puedeVerApartadoProyectos` deja de gobernar el panel y `puedeVerRecursos` se desacopla conservando sus roles; `accion=crear` en Paquetes de Trabajo. Adaptación móvil (mismo contenido en el cajón). | F1, F2 | Al cerrar la fase |
| **F4 — Panel derecho estandarizado** | Todos los chips del panel derecho y de "Accesos rápidos" con pantalla existente abren con el servicio elegido (resultado esperado 6, sin excepciones); estado habilitado/deshabilitado por permiso según la decisión 3; marca visual del tipo informativo/acción coherente con la de F3. | F1, F2 (y F3 para reutilizar el chip) | Al cerrar la fase |
| **F5 — Pruebas automáticas y prueba de humo** | Prueba de cobertura (falla si hay una pantalla del workspace sin entrada en el registro ni excepción declarada), prueba de integridad del registro, prueba de humo "una entrada nueva solo en el registro aparece en todo", prueba de fuente contra redirects que pierden el servicio, función de matriz roles × accesos derivada del registro. | F1 a F4 | Al cerrar la fase |
| **F6 — Verificación integral y loop** | Autoverificación con Playwright de toda la Punch List con las dos cuentas (permisos por ambos lados) y el barrido de los 13 roles con "Ver como" desde la cuenta con permisos altos; corregir y repetir hasta 100% Conforme; lint contra `main`, `npm test`, `npm run build`. Evidencia en `02-trabajo-activo/03-evidencia/`. | F1 a F5 | Al cerrar la fase y antes de reportar |
| **F7 — Consolidación documental y cierre del Worker** | Con la consulta previa a Victor de cada contradicción (excepción D6, en el chat del Worker): actualizar flujos 16, 01, 14 y los que apliquen (03, 05, 06, 11, 15, 21), escribir la política de "interfaz nueva" en el flujo 16 y en `05-diseno-y-ui.md`, documentar el chip deshabilitado y el registro en `design.md`, regenerar la matriz del flujo 14 desde el registro, trasladar mejoras de trabajo, reglas de negocio y huérfanos de los apartados obligatorios a sus destinos. | F6 | Commit + push a `main` de `pg_control_proyectos` (`git add` explícito) |

Regla de commits (`03-entorno-git-y-worktrees.md`): cada ~35% de la Punch List en Conforme, solo al terminar completo el ítem en curso, con `git add` explícito. Puntos naturales: al terminar F1, F2, F3, F4 más F5, y F6.

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
  permiso?: (roles: Rol[]) => boolean;        // sin permiso => cualquier usuario autenticado; usa las funciones existentes de permisos.ts
  tituloDeshabilitado?: string;
  visible: { izquierdo: boolean; centro: boolean; derecho: boolean; accesoRapido?: boolean };
  icono; colorClase; orden;
}
```

De él se derivan con funciones puras (parametrizadas por el registro, para poder probarlas con un registro de prueba): el panel derecho, el panel izquierdo, `herramientasPorGrupo` (Mi entorno), el href con `?proyectoId=`, el estado habilitado o deshabilitado por rol y la matriz roles × accesos del flujo 14. El registro también declara las **pantallas sin chip** (excepciones con motivo: `/login`, `/admin/usuarios`, `/configuraciones`, `/mi-perfil`, `/programas/**`, etc.).

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

## Asignación de roles

| Rol | Chat | Rama | Worktree | Estado |
|---|---|---|---|---|
| Orquestador | `local_1.orquestador_paneles-servicio-persistente` (por renombrar) | `main` | N/A | Activo |
| Planner | `local_2.planner_paneles-servicio-persistente` | `main` | N/A | Plan entregado para el Gate 1 |
| Worker (único, fases F0 a F7) | `local_3.worker_paneles-servicio-persistente` | `local-worker-1` (por crear, autorización de Victor) | `.worktrees/local-worker-1` en `py_control_proyectos_web` (por crear) | Pendiente del Gate 1 |
| Auditor | `local_4.auditor_paneles-servicio-persistente` | `main` | N/A | Pendiente |

**Un solo Worker, y por qué.** Todo lo importante pasa por los mismos archivos: `WorkspaceShell.tsx` (los dos paneles), el registro de accesos y sus derivaciones (`nav-proyecto.ts`, `grupo-proceso.ts`), `permisos.ts`, `PanelSecciones.tsx` y `CabeceraPagina.tsx`. Las pantallas que reciben el servicio (RDTs, Requerimientos, Consolidado RQ) dependen del contrato del registro y del helper de servicio de F1 y F2. La única parte casi independiente son esas pantallas (unos 10 archivos), pero solo lo es después de fijar el contrato, y partirla obliga a coordinar dos ramas sobre el mismo registro; por el criterio del estándar (independencia real de archivos) no se divide. Si Victor prefiere velocidad sobre simplicidad, el corte posible es: Worker de F1+F3+F4 (shell, registro y paneles) y Worker de F2 (pantallas), con F2 empezando después de que F1 esté pusheada, cada uno en su rama.

**Auditor.** Uno solo, al terminar F7.

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
Rol: Worker (único). Chat: local_3.worker_paneles-servicio-persistente.
Repositorio de código: D:\VICTOR\CLAUDE CODE\py_control_proyectos_web. Rama: local-worker-1, worktree .worktrees/local-worker-1 (autorizados por Victor; verifica con git branch -a / git worktree list antes de empezar). Nunca main, nunca merge, nunca borrar ramas ni worktrees. Documentación: pg_control_proyectos, main directo, git add explícito, sin tocar vpc/.
Subalcance: las fases F0 a F7 de docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente.md, en ese orden: línea base, registro único de accesos, servicio persistente por ?proyectoId=, panel izquierdo completo, panel derecho estandarizado, pruebas automáticas y de humo, verificación con Playwright hasta 100% Conforme, y consolidación documental.
Leer antes de escribir código: AGENTS.md y CLAUDE.md de ambos repositorios; la guía de Next.js en py_control_proyectos_web/node_modules/next/dist/docs/ (esta versión, Next 16, tiene cambios de API respecto de lo que conoces: searchParams asíncronos, useSearchParams y Suspense, redirects); el plan completo (Spec, decisiones aprobadas en el Registro de decisiones, Punch List aprobada); los flujos 16, 14, 01, 03, 04, 05, 06, 11, 15, 19, 20 y 21; 05-diseno-y-referencias/design.md (secciones 3, 5, 9, 10 y 12); 01-contexto-repositorio/03-entorno-git-y-worktrees.md, 04-pruebas-y-evidencia.md y 05-diseno-y-ui.md; el índice de 03-aprendizaje-continuo/README.md, abriendo solo la mejora que aplique a la acción inmediata (contadores congelados de tests, falsos negativos de Playwright, lint contra main).
Criterios de salida: 100% de la Punch List en Conforme, verificado por ti con Playwright en la app real, con login real, con las dos cuentas de prueba por los dos lados de cada permiso (las credenciales viven fuera del repositorio: no las copies a ningún archivo ni al chat); npm test verde con contadores actualizados; lint sin deuda nueva respecto de main; build correcto; evidencia en 02-trabajo-activo/03-evidencia/2026-09-27-paneles-servicio-persistente.md; progreso en 02-trabajo-activo/02-progreso/ con el mismo nombre. Commit + push a tu rama cada ~35% de la Punch List, solo al terminar completo el ítem en curso.
Registra en el momento, en los apartados del plan, cada mejora de trabajo, regla de negocio acordada y carpeta/archivo huérfano. Ante un conflicto de regla de negocio no anticipado (la lista de contradicciones del plan ya anticipa varias), consulta a Victor directamente en tu chat, valida su respuesta, regístrala en el progreso y recién continúa.
Restricciones: no cambia quién puede hacer qué (matriz del flujo 14): solo cómo se muestra; sin migraciones ni cambios en db/; no modificar src/lib/pr, dashboard, curva-s, plan-maestro ni dp; la verificación es de solo lectura sobre los datos reales (no guardar, borrar ni subir nada; las acciones se prueban hasta abrir el formulario); no editar ningún flujo de 04-flujos-de-negocio sin haber consultado antes a Victor cada contradicción; no crear infraestructura ni cambiar el alcance del plan.
```

### Prompt del Auditor

```text
Rol: Auditor. Chat: local_4.auditor_paneles-servicio-persistente. Rama: main de pg_control_proyectos (solo documentación). No implementas, no haces merge, no apruebas por Victor.
Primer chequeo (antes de todo lo demás): con git log y git branch --contains en py_control_proyectos_web confirma, no de memoria, que la implementación está en local-worker-1 y no en main ni en ninguna rama del Orquestador o del Planner, y que existió un chat de Worker separado. Si no se cumple, la tarea no pasa auditoría: reporta y detente.
Segundo chequeo: que las mejoras de trabajo, reglas de negocio y huérfanos estén en los apartados obligatorios del plan y trasladados a su destino (mejoras a 03-aprendizaje-continuo, reglas directo a los flujos, huérfanos reportados a Victor).
Luego revisa: Spec, plan, Punch List (los 87 ítems con evidencia), progreso, evidencia y el diff de local-worker-1 contra main. Comprueba de forma independiente, sobre una muestra que incluya siempre las verificaciones de permisos por ambos lados, que la Punch List se cumple con Playwright y las dos cuentas de prueba (las credenciales viven fuera del repositorio; no las copies a ningún archivo). Verifica: registro único sin listas paralelas; prueba de cobertura y prueba de humo realmente rojas cuando deben serlo; matriz del flujo 14 derivada del registro y diferencias con la tabla anterior informadas; el diff no toca db/, pr, dashboard, curva-s, plan-maestro ni dp; ningún dato real fue modificado; los flujos 16, 01, 14 (y 03, 05, 06, 11, 15, 21 si aplica) y 05-diseno-y-ui.md quedaron coherentes con lo implementado y con las respuestas de Victor; la política de interfaz nueva coincide con el texto aprobado en el Gate 1; lint contra main; ninguna credencial en el repositorio.
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
| `src/components/ui/WorkspaceShell.tsx` | `resolverProyectoId`, `ContenidoNav` (panel izquierdo completo), `ContenidoHerramientas`, servicio actual visible, enlaces del pie con servicio |
| `src/components/ui/PanelSecciones.tsx` | `AccesosRapidos` y `GruposAccordion`: servicio en todos los enlaces, deshabilitado por permiso, marca de tipo |
| `src/lib/config/nav-proyecto.ts` + `nav-proyecto.test.ts` | Pasa a derivar del registro; se reescriben las pruebas que fijan contadores (41 ítems) y las que exigen "Cronograma necesita servicio elegido" |
| `src/lib/notificaciones/grupo-proceso.ts` + `grupo-proceso.test.ts` | `herramientasPorGrupo` deriva del registro y los chips de Mi entorno envían el servicio |
| `src/components/ui/EntornoTrabajoGrupo.tsx` | Consume la derivación; conserva el estilo de chip deshabilitado (`opacity-40 cursor-not-allowed`) |
| `src/app/(workspace)/layout.tsx` | Deja de pasar `puedeVerApartadoProyectos` como puerta del panel; puede pasar la lista de servicios vigentes para validar y nombrar el servicio actual |
| `src/lib/permisos/permisos.ts` + `permisos.test.ts` | `puedeVerRecursos` se desacopla de `puedeVerApartadoProyectos` (hoy es su alias) y conserva sus roles actuales (administrador y jefe de proyectos); sin cambio en quién puede qué |
| `src/app/(workspace)/rdts/{crear,status,listado,consolidado}/page.tsx` + `FormularioCrearRdt.tsx`, `TablaStatusRdts.tsx`, `TablaListadoRdts.tsx`, `TablaConsolidadoRdts.tsx` | Reciben y preseleccionan el servicio |
| `src/app/(workspace)/requerimientos/page.tsx`, `logistica/consolidado-rq/page.tsx` + `ListadoRequerimientos.tsx`, `TablaConsolidadoRq.tsx` | Idem (con la regla `proyectoId` ↔ `ots`) |
| `src/app/(workspace)/cronograma/page.tsx`, `paquetes-trabajo/page.tsx`, `plan-maestro/page.tsx`, `mi-entorno/page.tsx` + `FormularioPaquetesTrabajo.tsx`, `FormularioCronograma.tsx`, `FormularioPlanMaestro.tsx` | El selector actualiza la URL (A1); `accion=crear` en Paquetes (A7) |
| Las 14 páginas con `redirect('/mi-entorno')` (`cronograma`, `logistica/consolidado-rq`, `mi-perfil`, `paquetes-trabajo`, `plan-maestro`, `rdts` ×5, `recursos` ×4) | El redirect conserva `?proyectoId=` con el helper |
| `src/app/(workspace)/proyectos/[id]/requerimientos/page.tsx`, `proyectos/[id]/mi-entorno/page.tsx`, `proyectos/[id]/entorno/[grupo]/page.tsx` | Redirects que hoy pasan el servicio por otro parámetro o lo pierden |
| `src/components/ui/CabeceraPagina.tsx` | Chip "Salir a Mi entorno" según la decisión 4 |
| `src/components/ui/FormularioCrearRdt.tsx` (`router.push('/rdts/status')`), `FormularioRequerimiento.tsx` (`router.push('/requerimientos')`) | La salida tras guardar conserva el servicio |

**Solo lectura / no se tocan**: `db/**`, `src/app/api/**` (salvo que el Worker demuestre que hace falta y lo consulte), `src/lib/pr`, `src/lib/dashboard`, `src/lib/curva-s`, `src/lib/plan-maestro`, `src/lib/dp`, `src/middleware.ts`.

**Documentación en `pg_control_proyectos` (F7, tras consultar a Victor)**: `04-flujos-de-negocio/16-paneles.md`, `01-configuracion.md`, `14-accesos-y-restricciones.md` y, según lo que corresponda, `03-entorno.md`, `05-rq.md`, `06-rdt.md`, `11-dashboard.md`, `15-cronograma.md`, `21-curva-s.md`; `01-contexto-repositorio/05-diseno-y-ui.md`; `05-diseno-y-referencias/design.md` (chip deshabilitado, registro, política); `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (corrección ya anotada en "Mejoras"); mejoras nuevas en `03-aprendizaje-continuo/`; `02-progreso/` y `03-evidencia/` de este plan; `docs/README.md` y `01-planes/README.md`.

## Punch List embebida

Formato de `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia de cada ítem va en `02-trabajo-activo/03-evidencia/2026-09-27-paneles-servicio-persistente.md`.

### Estado de aprobación

Gate 1: **pendiente**. Victor aprueba esta lista **antes** de implementar (protocolo de verificación). Una vez aprobada, el Worker la verifica él mismo con Playwright y no entrega con ítems abiertos.

### Método, cuentas y datos de prueba (aplica a todos los ítems)

- **Cuenta A**: perfil con permisos altos. **Cuenta B**: perfil sin permisos de administración (el Worker anota en la evidencia el rol de B, tal como lo muestra el pie del panel izquierdo, y calcula los resultados esperados con la tabla de referencia de abajo; si B tiene varios roles, el resultado es la unión). Las credenciales viven fuera del repositorio y nunca se copian a archivos ni al chat.
- **SV1**: un servicio vigente con DP, cronograma y Plan Maestro (el que el Worker elija entre los existentes; se nombra por N° OT en la evidencia). **SV2**: otro servicio vigente. **SVX**: un servicio sobre el que la cuenta B no tiene alcance (`proyecto_miembros`); si no existe ninguno, el Worker lo declara como limitación en la evidencia.
- **Solo lectura**: ninguna verificación guarda, borra ni sube datos reales. Las acciones (Generar RQ, Crear RDT, Subir RDT, Crear paquete) se prueban hasta abrir su formulario con el servicio preseleccionado; la salida tras guardar se prueba con la prueba unitaria del helper y la revisión de código.
- **Tamaños**: escritorio (1440 px de ancho) y móvil (390 px de ancho).
- **Playwright**: leer con `textContent()` y no con `innerText()` (hay etiquetas con `uppercase`); esperar la condición real (URL, atributo) y no un tiempo fijo; encadenar las navegaciones una a una sobre el mismo navegador (en paralelo se pisan).
- **Barrido de roles**: la cuenta A puede simular cada uno de los 13 roles con "Ver como" (el servidor trata la sesión con los roles simulados), lo que permite comprobar todos los roles con una sola cuenta. No sustituye a la cuenta B: complementa.

**Tabla de referencia de permisos** (leída de `src/lib/permisos/permisos.ts` y de la guardia de cada pantalla el 2026-09-27; el Worker la contrasta con el código vigente al empezar y anota cualquier diferencia). Abreviaturas de rol como en el flujo 14.

| Acceso | Función de permiso | Roles habilitados | Guardia en la pantalla hoy |
|---|---|---|---|
| Cronograma | `puedeVerCronograma` | todos menos Asist | Sí (redirige a Mi entorno) |
| Paquetes de Trabajo | `puedeVerPaquetesTrabajo` | todos menos Asist | Sí (redirige a Mi entorno) |
| Plan Maestro | `puedeVerPlanMaestro` | todos menos Asist | Sí (redirige a Mi entorno) |
| Curva S | `puedeVerCurvaS` + alcance sobre la OT | todos menos Asist; además Admin o miembro de la OT | Sí (mensaje "No tienes acceso…") |
| PR | ninguna | todos los autenticados | **No** |
| Dashboard | ninguna (el interruptor Parcial/Completo usa `puedeAdjudicarProyecto`) | todos los autenticados | **No** |
| DP (ver) | ninguna (importar: `puedeSubirDocumento` de SOT: Admin y SOT) | todos los autenticados | **No** para ver |
| Crear RDTs | `puedeCrearRdtEstructurado` | Admin, JP, SOp | Sí |
| Subir RDTs | `puedeSubirRdt` | Admin, JP, JOT, SOp | El formulario de Mi entorno solo se muestra si puede |
| Status de RDTs / Archivo de RDTs / Consolidado RDTs | `puedeVerRdts` | Admin, JP, JOT, SOp, SAdm, Asist, RRHH | Sí |
| Crear RQ / Generar RQ | `puedeCrearRequerimiento` | todos menos Admin | El formulario de Mi entorno solo se muestra si puede |
| Status de Requerimiento | ninguna | todos los autenticados | **No** |
| Consolidado RQ | `puedeVerConsolidadoRq` | Admin, JP, JOT, SLog | Sí |
| Registro de costos | `puedeSubirRegistroCostosServicio` o `puedeDescargarRegistroCostosServicio` | SLog, JP (Admin **no**) | Sí (redirige a la ficha) |
| Editar servicio | `puedeAdjudicarProyecto` | JOT (Admin **no**) | Sí (redirige a la ficha) |
| Editar checklist | `puedeModificarChecklist` | Admin, JOT | Sí (redirige a la ficha) |
| Ficha del servicio, Notificaciones | ninguna | todos los autenticados | No |
| Recursos de empresa (Personal, Cargos, Equipos) | `puedeVerRecursos` | Admin, JP | Sí |
| Recursos de empresa: Causas CNC | `puedeGestionarCatalogoCnc` | Admin, JP | Sí |

### Ítems funcionales

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-01 | F2 | Cuenta A abre SV1 desde "Todos los servicios": el panel izquierdo muestra el servicio actual (N° OT y nombre) y el panel derecho tiene sus chips activos | Captura de ambos paneles y URL | Sin verificar |
| PL-02 | F2 | Cronograma con SV1: `?proyectoId=` en la URL, ambos paneles con SV1 y selector de OT = SV1 | Captura + URL | Sin verificar |
| PL-03 | F2 | Paquetes de Trabajo con SV1: ídem PL-02 | Captura + URL | Sin verificar |
| PL-04 | F2 | Plan Maestro con SV1: ídem PL-02 | Captura + URL | Sin verificar |
| PL-05 | F2 | Crear RDTs con SV1: selector de OT = SV1 y ambos paneles con SV1 | Captura + URL | Sin verificar |
| PL-06 | F2 | Status de RDTs con SV1: ambos paneles con SV1 y filtro N° OT = SV1 (no aparecen filas de otros servicios) | Captura + URL | Sin verificar |
| PL-07 | F2 | Archivo de RDTs subidos con SV1: ídem PL-06 | Captura + URL | Sin verificar |
| PL-08 | F2 | Consolidado RDTs con SV1: selector de servicio = SV1 y consolidado cargado sin clic adicional | Captura + URL | Sin verificar |
| PL-09 | F2 | Status de Requerimiento con SV1: ambos paneles con SV1 y filtro de OT = SV1; si se cambia la multiselección `ots` de la tabla, el contexto de los paneles sigue siendo SV1 | Captura + URL | Sin verificar |
| PL-10 | F2 | Consolidado RQ con SV1: ambos paneles con SV1 y filtro N° OT = SV1 | Captura + URL | Sin verificar |
| PL-11 | F2 | Notificaciones, Mi entorno (`?accion=crear-rq` y `?accion=subir-rdt`) y Recursos de empresa (Personal, Cargos, Equipos): los paneles conservan SV1 | Captura + URL de cada una | Sin verificar |
| PL-12 | F2 | DP, PR, Dashboard, Curva S y Registro de costos (rutas `/proyectos/<id>/…`): ambos paneles con SV1 (regresión de lo que ya funcionaba) | Captura + URL de cada una | Sin verificar |
| PL-13 | F2 | `/proyectos/<SV1>/requerimientos` redirige a Status de Requerimiento y los paneles conservan SV1 | URL final + captura | Sin verificar |
| PL-14 | F2 | Cambiar de servicio (SV1 a SV2) con el selector de una pantalla: la URL y ambos paneles pasan a SV2 | URL antes y después + captura | Sin verificar |
| PL-15 | F2 | Volver a "Todos los servicios" y elegir SV2: los paneles muestran SV2 sin restos de SV1 | Captura | Sin verificar |
| PL-16 | F2 | "Todos los servicios" limpia el servicio: paneles sin servicio, los chips que requieren servicio quedan inertes y los que funcionan sin servicio (Plan Maestro, Status de Requerimiento, Consolidado RQ, Status de RDTs) navegan como en la línea base | Captura + comparación con la línea base de F0 | Sin verificar |
| PL-17 | F2 | Recargar (F5) y usar Atrás/Adelante conservan el servicio; pegar la URL en una pestaña nueva lo restaura | Secuencia de URL y capturas | Sin verificar |
| PL-18 | F2 | Ninguna pantalla de PL-02 a PL-13 muestra "Selecciona un servicio…" con servicio elegido (no hay parpadeo del mensaje durante la carga) | Tabla ruta → resultado + captura de la carga | Sin verificar |
| PL-19 | F2 | Redirección del servidor por falta de permiso: la cuenta B abre por URL una pantalla que no puede usar con `?proyectoId=SV1` y aterriza en Mi entorno conservando SV1 | URL final + captura | Sin verificar |
| PL-20 | F2 | Las salidas tras guardar (Crear RDTs a Status de RDTs, Crear RQ a Status de Requerimiento) y `CabeceraPagina` conservan el servicio | Prueba unitaria del helper + revisión de código (sin guardar datos reales) | Sin verificar |
| PL-21 | F2 | El chip "Salir a Mi entorno" se comporta según la decisión 4 aprobada (con servicio, va a `/mi-entorno?proyectoId=…`) | Captura antes y después de hacer clic | Sin verificar |
| PL-22 | F3 | Con servicio, el panel izquierdo muestra los grupos acordados (decisiones 5 y 6): Alcance y presupuesto, Planificación, Recursos del servicio, Documentación, Reportes, y el grupo Servicio si se aprueba; las acciones van separadas de los informativos | Captura | Sin verificar |
| PL-23 | F3 | Cada chip del panel izquierdo cuya pantalla existe abre esa pantalla con SV1 (DP, Paquetes de Trabajo, Cronograma, Plan Maestro, Consolidado RDTs, Requerimiento, PR, Dashboard, Curva S, Registro de costos y, si se aprueba, Ficha del servicio, Editar servicio y Editar checklist) | Tabla chip → URL → servicio visible | Sin verificar |
| PL-24 | F3 | Los chips sin pantalla (Alcance, Presupuesto, Cargos HH, Equipos HM, Planos, PETS y los que fije la decisión 5) se ven, no tienen enlace, el clic no cambia la URL y no hay error en consola | Captura + registro de consola | Sin verificar |
| PL-25 | F3 | Acciones: Generar RQ abre Crear RQ con SV1; Crear RDT abre Crear RDTs con SV1; Crear paquete abre Paquetes de Trabajo con SV1 y el formulario de paquete nuevo abierto; Subir RDT abre su formulario con SV1. Ninguna guarda al abrir | Captura de cada formulario | Sin verificar |
| PL-26 | F3 | Las acciones quedan fijadas al servicio actual (según E1): el formulario abre con SV1 y, si se cambia el servicio dentro de la acción, la URL y los paneles lo siguen (no puede haber dos servicios distintos a la vez) | Captura antes y después | Sin verificar |
| PL-27 | F3 | Recursos de empresa: botón mostrar/ocultar; sin servicio aparece visible por defecto y con servicio, oculto por defecto; el botón funciona en ambos casos; abrir Personal, Cargos o Equipos no cierra el servicio | Capturas en los dos estados | Sin verificar |
| PL-28 | F3 | "Materiales" ya no aparece en Recursos de empresa | Captura | Sin verificar |
| PL-29 | F3 | El pie del panel izquierdo (Usuarios, Notificaciones, Configuraciones, Cerrar sesión, "Ver como", Mi entorno) sigue funcionando, no queda tapado por el nuevo contenido y sus enlaces llevan el servicio | Captura y clic en cada uno | Sin verificar |
| PL-30 | F4 | Dentro de SV1, cada chip del panel derecho cuya pantalla usa selector de OT (Crear RDTs, Subir RDTs, Crear RQ, Consolidado RDTs, Cronograma, Paquetes de Trabajo, Plan Maestro) abre con SV1 ya elegido en el selector | Tabla chip → valor del selector | Sin verificar |
| PL-31 | F4 | Dentro de SV1, cada chip cuya pantalla filtra por N° OT (Status de RDTs, Archivo de RDTs, Requerimiento, Consolidado RQ) abre con el filtro = SV1 | Tabla chip → filtro | Sin verificar |
| PL-32 | F4 | Dentro de SV1, cada chip con ruta de servicio (DP, PR, Dashboard, Curva S, Registro de costos) abre con SV1 | Tabla chip → URL | Sin verificar |
| PL-33 | F4 | Recorrido completo de los 7 grupos del panel derecho y de "Accesos rápidos": ningún chip cuya pantalla existe queda sin el servicio (una fila por chip, sin excepciones) | Tabla completa de chips | Sin verificar |
| PL-34 | F4 | El valor preseleccionado se puede cambiar y la pantalla responde (selector o filtro) | Captura antes y después | Sin verificar |

### Datos y cálculos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-35 | F1 a F7 | No hay migraciones ni cambios en `db/` ni en tablas: el diff de `local-worker-1` contra `main` no toca `db/` | `git diff --stat` | Sin verificar |
| PL-36 | F1 a F7 | El diff no toca `src/lib/pr`, `dashboard`, `curva-s`, `plan-maestro` ni `dp` (los cálculos EVM no cambian) | `git diff --stat` | Sin verificar |
| PL-37 | F2 | El N° OT y el nombre que muestra el panel izquierdo corresponden al `id` de la URL (SV1 y SV2) | Captura + comparación con la ficha del servicio | Sin verificar |

### Permisos (por los dos lados)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-38 | F3 | Cuenta A con SV1: cada chip del panel izquierdo está habilitado o deshabilitado según la tabla de referencia (incluye Registro de costos y Editar servicio deshabilitados para un rol Admin puro, igual que el código actual) | Tabla chip → estado esperado → estado real | Sin verificar |
| PL-39 | F3 | Cuenta B con SV1: el panel izquierdo **es visible** (antes no lo era); los chips que su rol no puede usar están deshabilitados con `opacity-40`, `cursor-not-allowed` y título explicativo; los que puede usar están activos | Tabla + captura | Sin verificar |
| PL-40 | F3 | Cuenta B: hacer clic en un chip deshabilitado no navega (URL sin cambios) y no hay error en consola | Captura + consola | Sin verificar |
| PL-41 | F4 | Cuenta B: en el panel derecho los chips que su rol no puede usar aparecen deshabilitados con título (según la decisión 3 aprobada; si se decide mantener el comportamiento actual, el ítem se reescribe en el Gate 1) | Tabla + captura | Sin verificar |
| PL-42 | F4 | Cuentas A y B: Mi entorno conserva exactamente los mismos chips y estados habilitado/deshabilitado que en la línea base, ahora enviando el servicio | Comparación con la línea base de F0 | Sin verificar |
| PL-43 | F6 | Barrido de los 13 roles con "Ver como" desde la cuenta A: para cada rol, el estado de cada chip del panel izquierdo, del derecho y de Mi entorno coincide con las funciones de `permisos.ts` | Tabla 13 roles × chips | Sin verificar |
| PL-44 | F6 | **Ver no es acceder.** Cuenta B, por URL directa (con `?proyectoId=`), a cada pantalla con guardia cuyo chip está deshabilitado para su rol (Cronograma/Paquetes/Plan Maestro si aplica, RDTs, Consolidado RQ, Recursos, Registro de costos, Editar servicio, Editar checklist, Curva S): el servidor responde igual que hoy (redirección o mensaje) y no muestra datos | URL, resultado y captura de cada una | Sin verificar |
| PL-45 | F6 | Cuenta B, por URL directa, a las pantallas sin guardia de rol (PR, Dashboard, DP, Status de Requerimiento): se comporta como en la línea base (consecuencia de E2); el resultado queda escrito en la evidencia | Captura + nota de E2 | Sin verificar |
| PL-46 | F6 | Cuenta B, desde el navegador con la sesión iniciada, llama a `GET /api/cronograma`, `/api/rdts/consolidado` y `/api/curva-s` con `proyectoId` de SV1, de SVX y con un id inexistente: la respuesta es la misma que en la línea base (401, 403 o 4xx claro) y nunca 500 ni datos de un servicio sin alcance | Respuestas registradas | Sin verificar |
| PL-47 | F2 | `?proyectoId=` inexistente, de un servicio archivado o sin acceso: el shell no falla, trata la sesión como sin servicio (o muestra un aviso claro) y no revela nombre ni datos del servicio | Captura + consola | Sin verificar |
| PL-48 | F3 | "Ver no es modificar": dentro de las pantallas, los botones de acción (Consolidado RQ, Status de RDTs, Paquetes de Trabajo) siguen habilitados solo para los mismos roles que en la línea base | Comparación con la línea base | Sin verificar |
| PL-49 | F3 | Con la cuenta A, los chips de "Recursos de empresa" (Personal, Cargos, Equipos, Causas CNC) y con la cuenta B (que no los ve hoy) se comportan según A4 | Captura de cada cuenta | Sin verificar |

### Registro único y estándar de interfaz nueva

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-50 | F1 | Existe un único registro de accesos; `NAV_PROYECTO`, `herramientasPorGrupo`, `CHIPS_ACCESO_RAPIDO`, `hrefItemPanel` y las rutas fijas del panel izquierdo derivan de él: no queda ninguna lista paralela de chips | Búsqueda de código (`rg`) + diff | Sin verificar |
| PL-51 | F1 | Cada acceso tiene todos los metadatos (id, nombre, grupo, tipo, ruta o acción, requiere servicio, permiso, visibilidad por panel) y la prueba de integridad lo comprueba (ids únicos, sin rutas sin permiso declarado por omisión silenciosa) | `npm test` | Sin verificar |
| PL-52 | F1 | Migración completa: los 41 ítems de `NAV_PROYECTO`, los 10 chips de Mi entorno, los 7 de Accesos rápidos y los 4 de Recursos de empresa que se conservan (Personal, Cargos, Equipos y Causas CNC; "Materiales" se elimina y no se migra) están en el registro; tabla clave anterior → id nuevo sin pérdidas; las únicas diferencias visibles son las declaradas (por ejemplo la unión de `rdt` y `subir-rdt`, y E3 según la respuesta de Victor) | Tabla de mapeo + prueba de equivalencia | Sin verificar |
| PL-53 | F5 | Prueba de humo automática: una función pura recibe un registro con **una** entrada de prueba nueva y esa entrada aparece en panel izquierdo, panel derecho, Mi entorno, con `?proyectoId=`, con estado por permiso y como fila de la matriz | `npm test` | Sin verificar |
| PL-54 | F6 | Prueba de humo en vivo: añadir una entrada de prueba **solo en el registro** (sin commitearla) y comprobar con Playwright, con las dos cuentas, que aparece en los paneles correspondientes, conserva el servicio, se habilita o deshabilita por permiso y sale en la matriz, sin tocar ningún otro archivo; se revierte y el diff final no la contiene | Captura + `git status` con un solo archivo modificado, luego limpio | Sin verificar |
| PL-55 | F5 | Prueba de cobertura: falla si existe una pantalla del workspace sin entrada en el registro ni excepción declarada. Se demuestra en rojo (página temporal, sin commitearla) y en verde | Salida de `npm test` en rojo y en verde | Sin verificar |
| PL-56 | F5 | Función de matriz derivada del registro: produce roles × accesos; sus diferencias con la tabla actual del flujo 14 quedan listadas en la evidencia (no se corrigen en silencio) | Lista de diferencias | Sin verificar |
| PL-57 | F5 | Prueba de fuente: ningún `redirect('/mi-entorno')` ni enlace literal a una pantalla de servicio en el workspace pierde el servicio (o está en una lista de excepciones con motivo) | `npm test` | Sin verificar |
| PL-58 | F7 | Política de "interfaz nueva" escrita en el flujo 16 y en `05-diseno-y-ui.md` con el texto aprobado en el Gate 1, con su plantilla de ítems de Punch List | Diff de `pg_control_proyectos` | Sin verificar |

### UI / responsive / accesibilidad

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-59 | F3 | Móvil (390 px): el cajón izquierdo y el derecho muestran el mismo contenido que en escritorio, se cierran al navegar y la página no tiene scroll horizontal | Capturas móvil | Sin verificar |
| PL-60 | F3 | Escritorio: el panel izquierdo con todos los grupos hace scroll interno y no oculta el pie; con Recursos de empresa oculto queda compacto | Captura | Sin verificar |
| PL-61 | F3 | Chip deshabilitado accesible: `aria-disabled="true"`, título, no enfocable como enlace y no depende solo del color (texto legible) | Snapshot de accesibilidad | Sin verificar |
| PL-62 | F3 | Botón mostrar/ocultar con `aria-expanded`, operable con teclado; las secciones usan `<nav>` y encabezados | Snapshot de accesibilidad + prueba con teclado | Sin verificar |
| PL-63 | F3 | La marca informativo/acción es visible y no depende solo del color, en ambos paneles | Captura | Sin verificar |
| PL-64 | F3 | Diseño: se usan los tokens y el estilo de `EntornoTrabajoGrupo.tsx`, sin `max-w-*` nuevo en contenedores de página y sin dependencias visuales nuevas | Revisión de diff | Sin verificar |
| PL-65 | F6 | Las tablas largas conservan scroll horizontal y columnas fijas (Consolidado RDTs, Status de RDTs, Consolidado RQ, PR) | Captura de cada una | Sin verificar |

### Estados vacío / carga / error

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-66 | F2 | Usuario o momento sin servicio elegido: los paneles muestran el estado sin servicio, sin errores y con Recursos de empresa visible | Captura | Sin verificar |
| PL-67 | F2 | Durante la carga inicial con `?proyectoId=` en la URL no se ve el mensaje "Selecciona un servicio" ni un salto de layout | Grabación o capturas seguidas | Sin verificar |
| PL-68 | F6 | Recorrido completo (PL-02 a PL-13 con ambas cuentas): sin errores nuevos en la consola del navegador respecto de la línea base | Registro de consola | Sin verificar |
| PL-69 | F2 | Servicio sin datos (sin DP, sin cronograma o sin Plan Maestro): los paneles y sus chips se comportan igual y las pantallas muestran su estado vacío habitual | Captura | Sin verificar |

### Validación en servidor / API

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-70 | F2 | El parámetro `?proyectoId=` nunca se usa en servidor sin validar pertenencia: las pantallas y APIs que lo reciben validan autenticación, rol y acceso al servicio como antes | Revisión de código + PL-46 | Sin verificar |
| PL-71 | F3 | Cambiar quién "ve" un chip no cambió quién "puede" usarlo: `git diff` de `permisos.ts` solo desacopla `puedeVerRecursos` y `puedeVerApartadoProyectos`, sin alterar los roles de ninguna otra función; `permisos.test.ts` verde | Diff + `npm test` | Sin verificar |
| PL-72 | F2 | Los redirects del servidor conservan el servicio sin abrir un redireccionamiento abierto: el helper solo acepta identificadores con formato de id y rutas internas | Prueba unitaria del helper | Sin verificar |
| PL-73 | F6 | Con sesión cerrada, cualquier ruta del workspace con `?proyectoId=` lleva a `/login` (el middleware sigue igual) | Captura | Sin verificar |

### Regresión

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-74 | F6 | `npm test` completo verde; contadores actualizados con pruebas específicas de ubicación y comportamiento de los ítems nuevos (no solo el número) | Resumen del runner (no un filtro de texto) | Sin verificar |
| PL-75 | F6 | Lint sin deuda nueva: mismo total que `main` y archivos tocados limpios | Conteo contra `main` | Sin verificar |
| PL-76 | F6 | `npm run build` correcto (en worktree con `--webpack`) | Salida del build | Sin verificar |
| PL-77 | F6 | Sin servicio, todas las pantallas se comportan como en la línea base de F0 (mismos destinos y estados) | Comparación con F0 | Sin verificar |
| PL-78 | F6 | Flujos que usan chips siguen intactos (sin guardar datos): Crear RQ abre desde Mi entorno, filtros de Status de Requerimiento, selector y carga del Consolidado RDTs, Plan Maestro y Cronograma abren con y sin servicio | Capturas | Sin verificar |
| PL-79 | F6 | Ningún dato real fue creado, modificado ni borrado durante la verificación | Nota en la evidencia + revisión de las acciones ejecutadas | Sin verificar |
| PL-80 | F6 | Navegación móvil y escritorio: el pie, "Ver como" y los cajones se comportan como en la línea base | Capturas | Sin verificar |

### Documentación y cierre

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-81 | F7 | Cada contradicción de la lista se consultó a Victor antes de editar el flujo afectado y su respuesta quedó en el progreso | Progreso con pregunta y respuesta | Sin verificar |
| PL-82 | F7 | Flujos 16, 01 y 14 (y 03, 05, 06, 11, 15, 21 si aplica) actualizados y coherentes con lo implementado, sin reglas pegadas al final | Diff de `pg_control_proyectos` | Sin verificar |
| PL-83 | F7 | Matriz del flujo 14 regenerada desde el registro, con nota de cómo regenerarla y sin edición manual | Diff + comando o prueba usada | Sin verificar |
| PL-84 | F7 | `design.md` documenta el chip deshabilitado, el registro y la política (con la confirmación de Victor que exige su regla de evolución) | Diff | Sin verificar |
| PL-85 | F7 | Apartados "Mejoras (de trabajo)", "Reglas de negocio acordadas" y "Carpetas/archivos huérfanos" trasladados a sus destinos; huérfanos reportados a Victor sin borrar nada | Diff + mensaje | Sin verificar |
| PL-86 | F7 | Ninguna credencial de las cuentas de prueba aparece en ningún archivo de ninguno de los dos repositorios | Búsqueda en el diff | Sin verificar |
| PL-87 | F6 | Evidencia completa en `03-evidencia/` con enlace al artifact de checklist visual si se crea, y limitaciones declaradas (SVX si no existe, rol de la cuenta B) | Archivo de evidencia | Sin verificar |

## Riesgos y bloqueos

Los del Spec (cambiar quién "ve" no debe cambiar quién "puede"; `?proyectoId=` frente a `?ots=`; tocar el shell afecta a todas las pantallas) y los que el Planner encontró al dimensionar en el código:

| # | Riesgo o bloqueo | Cómo se controla |
|---|---|---|
| R1 | **El servicio se pierde por dentro de las pantallas, no solo en los paneles.** 14 páginas hacen `redirect('/mi-entorno')` al faltar permiso, dos formularios hacen `router.push` tras guardar y `CabeceraPagina` lleva a `/mi-entorno` sin servicio. Arreglar solo los chips dejaría el mismo síntoma que Victor reportó. | Helper de servicio en F2, PL-19, PL-20, PL-21 y prueba de fuente PL-57 |
| R2 | **No todas las pantallas tienen "selector de OT"**: Status de RDTs, Archivo de RDTs y Consolidado RQ solo tienen un filtro de texto por columna; Status de Requerimiento usa `?ots=`. "Preseleccionar el servicio" significa cosas distintas por pantalla. | Tabla "Cómo se preselecciona el servicio en cada pantalla"; PL-30 a PL-34 |
| R3 | **El filtro N° OT es de "contiene"** (`PS-0001` coincide con `PS-00010`). | Coincidencia exacta al preseleccionar si aparece el caso |
| R4 | **Pantallas sin guardia de rol** (PR, Dashboard, DP para ver, Status de Requerimiento): un chip "deshabilitado" no tendría respaldo en el servidor y los flujos 14 y 16 dicen lo contrario de lo que el código hace. | E2; PL-45; el registro refleja el código vigente y la diferencia se informa |
| R5 | **La matriz derivada del código difiere de la tabla escrita del flujo 14** (por ejemplo, el flujo 14 marca a Admin en "Adjudicar proyecto" y `puedeAdjudicarProyecto` solo incluye al jefe de oficina técnica; no incluye la fila de Dashboard ni la de DP). Al derivar se hará visible. | PL-56 y contradicción C13: se informa, no se corrige en silencio |
| R6 | **`puedeVerRecursos` es un alias de `puedeVerApartadoProyectos`.** Abrir el panel a todos los roles arrastraría el catálogo de empresa si no se desacopla. | Desacople en F3, PL-49 y PL-71 |
| R7 | **El chip habilitado no garantiza que la pantalla abra** para un rol con permiso pero sin alcance sobre la OT (por ejemplo, Curva S exige además alcance por `proyecto_miembros`). | Fuera de alcance por el Spec (solo cambia lo que se muestra por rol); las pantallas siguen mostrando su mensaje; se documenta en el flujo 16 |
| R8 | **Datos reales y Supabase real.** La verificación con las cuentas de prueba corre sobre datos de trabajo. | Solo lectura (PL-79); las acciones se prueban hasta abrir el formulario |
| R9 | **Worktree, variables de entorno y Turbopack.** El worktree no existe, necesita `.env.local` y, con `node_modules` como Junction, exige `--webpack`. | Ver "Entorno"; el Worker lo consulta antes de copiar cualquier archivo de entorno |
| R10 | **Next.js 16 con cambios de API** (aviso de `AGENTS.md` del repositorio de la app): `searchParams` asíncronos y `useSearchParams` con `Suspense` en el shell. | El Worker lee la guía de `node_modules/next/dist/docs/` antes de tocar el shell |
| R11 | **Bucle entre selector y URL** si cada pantalla actualiza la URL desde su estado y el shell vuelve a pasar el valor. | Una sola fuente de verdad (la URL) y `router.replace` sin recarga; se prueba en PL-14 |
| R12 | **Contadores congelados en pruebas** (`nav-proyecto.test.ts` fija 41 ítems y varias pruebas asumen que Cronograma exige servicio). | Se reescriben con pruebas de ubicación y comportamiento (aprendizaje del 2026-09-23) |
| R13 | **Pantalla fuera del shell**: `src/app/programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx` cuelga de la raíz de `app`, no de `(workspace)`, por lo que no tiene paneles. | La prueba de cobertura la incluye como excepción declarada o se reporta a Victor; no se mueve sin autorización |
| R14 | **El componente nuevo choca con la regla de `design.md` §5** (no crear componentes sin justificar). | Se propone que el Gate 1 lo apruebe y `design.md` se actualiza al cierre (PL-84) |
| R15 | **Bloqueo**: la rama `local-worker-1` y su worktree no existen. | El Orquestador pide la autorización de Victor al aprobarse el Gate 1 |

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

Recomendación: **A**. Registro de costos se clasifica como **informativo** (abrirlo no modifica datos; subir o descargar ocurre dentro de la pantalla, igual que Paquetes de Trabajo). Para un rol Admin puro aparecerá deshabilitado, porque `permisos.ts` hoy no lo incluye (ver R5).

## Decisiones adicionales que necesitan respuesta de Victor

Conflictos que el Spec no cubre y que el Planner detectó al leer los flujos y el código. Cada uno trae recomendación; Victor decide en el Gate 1 (o el Worker lo consulta en su chat si prefiere verlo con la pantalla delante).

| # | Conflicto | Opciones | Recomendación |
|---|---|---|---|
| **E1** | El flujo 16 dice: "El usuario no debe poder cambiar de servicio durante una acción iniciada desde este panel", y el Spec 5: "las acciones quedan fijadas al servicio actual". El Spec 6 pide que el selector de OT abra con el servicio elegido, y esos selectores hoy son editables. | a) Bloquear el selector cuando la acción viene del panel (requiere un modo "solo lectura" en cada formulario: Crear RDTs, Crear RQ, Subir RDT, Paquetes). b) Preseleccionado y editable, pero cambiar el selector actualiza la URL y los paneles (nunca dos servicios a la vez). | **b.** Cumple la intención (no hay divergencia entre el servicio de la acción y el del contexto) sin tocar cada formulario; a) queda como mejora posterior. Al cierre se ajusta la frase del flujo 16. |
| **E2** | Los flujos 14 y 16 dicen que "toda ruta valida autenticación, rol y pertenencia" y que Ver PR y Ver Curva S son "todos menos asistente". En el código, **PR, Dashboard, DP (ver) y Status de Requerimiento no tienen guardia de rol** (solo el middleware de sesión); Curva S sí. Dashboard y DP no figuran en la matriz del flujo 14. | a) El registro refleja el código vigente (habilitadas para todos) y la discrepancia se informa; alinear el código queda como plan aparte. b) Añadir en esta tarea `puedeVerPr` y guardias para que el código cumpla el flujo 14. | **a.** El Spec excluye cambiar qué rol puede qué. La discrepancia se anota en el Informe de Auditoría como "PROPONER A RESPONSABLE" y en `planes-futuros.md` si Victor lo decide. Sin embargo, si Victor prefiere corregirlo ya, es un ítem pequeño y aislado que se suma como PL nuevo. |
| **E3** | En Mi entorno, el chip "Status de RDTs" (`listado-rdts`) va a `/rdts/listado`, que en el panel derecho es "Archivo de RDTs subidos"; el "Status de RDTs" del panel derecho (`status-rdts`) va a `/rdts/status`. El flujo 06 todavía dice que `/rdts/listado` es Status de RDTs. | a) Unificar en el registro: "Status de RDTs" = `/rdts/status` en todos los paneles y "Archivo de RDTs subidos" = `/rdts/listado`. b) Conservar la diferencia. | **a**, con la corrección del flujo 06 al cierre; es el único cambio de destino visible de la migración. Si Victor prefiere b, el Worker lo replica tal cual y lo deja anotado. |

## Supuestos menores del Planner

Aprobar el plan los aprueba salvo que Victor los objete en el Gate 1.

| # | Supuesto | Motivo |
|---|---|---|
| A1 | Cuando el usuario cambia el selector de OT dentro de una pantalla, la URL (`?proyectoId=`) se actualiza con `router.replace` y los paneles siguen el cambio. | Una sola fuente de verdad; cumple "hasta que el usuario cambie de servicio" |
| A2 | El servicio persiste también en los enlaces del pie del panel izquierdo (Usuarios, Notificaciones, Configuraciones, Mi entorno) y en Recursos de empresa. Solo "Todos los servicios" y el logo lo limpian; las pantallas de contenedores (`/programas/**`) no llevan servicio. | Spec 1: "en todas las pantallas del workspace" |
| A3 | Mi entorno conserva el mismo conjunto de chips que hoy (no se le agregan PR, Dashboard, etc.); solo cambia que ahora envía el servicio y sale del registro. | Sin ampliar alcance |
| A4 | Recursos de empresa sigue visible solo para administrador y jefe de proyectos (la matriz del flujo 14 no cambia); para los demás roles el apartado no se muestra. `puedeVerRecursos` se desacopla de `puedeVerApartadoProyectos` conservando esos roles. | El Spec excluye cambiar quién puede qué |
| A5 | El chip "Notificaciones" no se repite en el panel izquierdo (la campana del pie ya lo cubre; regla 8 del flujo 16). Sigue en cada grupo del panel derecho. | Regla 8: no duplicar |
| A6 | Los chips actuales sin pantalla que ninguna decisión ubica (Presupuesto, Alcance del servicio, Personal NUEVO, Consolidado de servicio, Materiales c/c) se conservan como inertes en su sección. | "El que no tiene pantalla permanece visible e inerte" |
| A7 | "Crear paquete" abre `/paquetes-trabajo?proyectoId=…&accion=crear`, con un cambio mínimo en `FormularioPaquetesTrabajo.tsx` para abrir directo el formulario de paquete nuevo. | El Spec lo lista en Acciones y la pantalla ya tiene el formulario ("Nuevo paquete") |
| A8 | "Subir RDT" también se incluye en Acciones del panel izquierdo (el flujo 16 lo cita como chip de acción). | Es una acción existente con pantalla |
| A9 | La matriz del flujo 14 se "deriva" con una función del registro cuya salida el Worker pega en el flujo 14 al cierre, marcada como generada; el mecanismo exacto lo fija el Worker (sin inventar comandos: el que use debe quedar verificado y documentado). | El repositorio de la app no puede escribir en el de documentación |

## Contradicciones con reglas de negocio ya escritas

Anticipadas tras leer los 21 flujos y `README.md`. Ninguna se edita antes del cierre; el Worker consulta cada una a Victor (excepción D6) antes de tocar el flujo, y el Orquestador puede adelantar las que Victor resuelva en el Gate 1.

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
| C11 | **01**: "Apartado Proyectos (panel izquierdo): solo administrador y jefe de proyectos" y "Pantallas de listado a pantalla completa… chip Salir a Mi entorno" | Lo ven todos los roles; decisión 4. El flujo 01 se declara "pendiente de definir" y guarda una regla de paneles que pertenece al 16 | Reescribir y, con Victor, mover la regla del panel al 16 dejando un enlace |
| C12 | **14**, fila "Ver apartado Proyectos (panel izquierdo): solo Admin y JP" y "Ver Recursos" | La primera cambia (todos los roles ven el panel; ver ≠ acceder); la segunda se mantiene (A4) | Revisar ambas filas y añadir la regla "ver ≠ acceder" |
| C13 | **14**, "Admin siempre tiene bypass total" y sus filas (Adjudicar, Confirmar transición, Registro de costos) | `permisos.ts` no da bypass a Admin en esas funciones (por ejemplo `puedeAdjudicarProyecto` solo incluye al jefe de oficina técnica). La matriz derivada del código mostrará una columna Admin distinta | Consulta a Victor: qué manda, el código o la tabla (PL-56) |
| C14 | **14**, "Ver PR" y "Ver Curva S: todos menos asistente"; **16**, regla 4 "Toda ruta debe validar autenticación, rol y pertenencia" | PR, Dashboard, DP (ver) y Status de Requerimiento no tienen guardia de rol; Dashboard y DP no están en la matriz | E2 |
| C15 | **14**, "Accesos requeridos para paquetes de trabajo (pendiente, no implementado)" | Paquetes de Trabajo Fase 1 ya está implementado (`puedeVerPaquetesTrabajo`, `puedeGestionarPaquetesTrabajo`) | Actualizar con la matriz derivada |
| C16 | **03**: chips comunes de Mi entorno y "Panel derecho: Subir RDTs clicable sin servicio" | Los chips de Mi entorno ahora envían `?proyectoId=` (Cronograma y Plan Maestro hoy no lo hacen); Mi entorno sale del registro. El 03 no lista Cronograma ni Plan Maestro entre los chips que sí muestra | Actualizar 03 |
| C17 | **05**: Status `/requerimientos` con "Chip Salir a Mi entorno" y filtros por `?ots=`; "Crear RQ: Mi entorno `?accion=crear-rq`" | Decisión 4; nuevo `?proyectoId=` que equivale a `ots=<id>`; Generar RQ ahora también sale del panel izquierdo (sigue abriendo Mi entorno) | Actualizar 05 |
| C18 | **06**: "`/rdts/listado` (**Status de RDTs**)", nav "Subir RDTs, Status de RDTs y Consolidado RDTs", chip "Salir a Mi entorno" | El código tiene `/rdts/status` (Status) y `/rdts/listado` (Archivo de RDTs subidos), más `/rdts/crear`; decisión 4; E3 | Actualizar 06 |
| C19 | **11** y **21**: el chip Dashboard/Curva S "aparece en los tres paneles… desde una única definición", grupo Planificación | Dashboard no está en Mi entorno hoy (A3); en el panel izquierdo van en Reportes (decisión 2 del Spec), en el derecho siguen en Planificación | Añadir la nota de ubicación por panel |
| C20 | **15**: Cronograma "necesita servicio elegido" (decisión previa registrada en el test de `nav-proyecto`) y "Chip Cronograma, único en el apartado Planificación del entorno" | Sigue necesitando servicio (`requiereServicio: 'si'`); al abrir se preselecciona; en Mi entorno pasa a enviar el servicio | Confirmar que no hay conflicto y actualizar la nota |

Revisados sin contradicción: 02 (Usuarios: el chip del pie no cambia), 04 (Notificaciones: se cumple que van a `/notificaciones`; A5), 07, 08, 09, 10, 12, 13 (refuerza que "(OT) Orden de trabajo" quede inerte), 17, 18, 19 (Paquetes de Trabajo como chip informativo con "Crear paquete" como acceso rápido: consistente con A7) y 20 (Plan Maestro se abre con selector de OT: consistente con la preselección). Además, `03-entorno-git-y-worktrees.md` contiene una afirmación inexacta ya anotada en "Mejoras" (acceso al repositorio de la app).

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

## Enlaces a progreso y evidencia homónimos

Se crean al pasar el Gate 1 (`02-progreso/` y `03-evidencia/` con este mismo nombre de archivo).

## Mejoras (de trabajo)

- `03-entorno-git-y-worktrees.md` (§ "Pool real de ramas y worktrees") afirma que este repositorio no tiene acceso directo a `py_control_proyectos_web`. Es inexacto: el repositorio de la app está en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`, accesible desde una sesión local, y se pueden correr `git`, el servidor de desarrollo y Playwright sobre él (verificado 2026-09-27). Corregir al cierre.
- Cuando se hacen varias llamadas de Playwright en paralelo sobre el mismo navegador, las navegaciones se pisan. Encadenar una a una.
- Lección del Planner (2026-09-27): para saber solo el **rol** de una cuenta de prueba, no se abre ni se filtra con `sed`/`grep` el archivo de credenciales de la memoria (`cuentas-prueba.md`): la salida de la herramienta imprimió valores que no debían mostrarse. Los valores no se copiaron a ningún archivo ni a este plan, pero la exposición ocurrió en la salida de una herramienta. Práctica: el rol de la cuenta se pregunta a Victor o lo lee el Worker de la propia interfaz (pie del panel izquierdo). Conviene además que el archivo de la memoria separe el rol de las credenciales.
- `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (§ "Pool real de ramas y worktrees") además dice "por verificar"; el Planner lo verificó el 2026-09-27: el repositorio de la app solo tiene `main`, sin worktrees ni carpeta `.worktrees/`. Actualizar la sección al cierre con ese resultado.

## Reglas de negocio acordadas en esta tarea

Ver "Registro de decisiones". Se trasladan a `04-flujos-de-negocio/` (16, 01, 14 y los que apliquen) al cierre, integradas en su estructura, tras la consulta con Victor de cada contradicción.

## Carpetas/archivos huérfanos

- `vpc/` en la raíz de `pg_control_proyectos`: carpeta sin seguimiento con una copia agnóstica del estándar (AGENTS.md, README y `docs/` reducido), modificada durante esta sesión por otra sesión. No la creó esta tarea. **Reportada a Victor; no se toca.**

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

Ninguno por ahora.
