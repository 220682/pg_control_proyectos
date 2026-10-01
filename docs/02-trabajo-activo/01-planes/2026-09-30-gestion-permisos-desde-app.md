# 2026-09-30 — Gestión de permisos y accesos desde la app (matriz editable)

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Este archivo contiene el Spec (paso 3) y, debajo, el plan con su Punch List (paso 6, Planner, 2026-10-01). Nace de «Planes futuros» → «Gestión de permisos y accesos desde la app (matriz editable)» (pedido de Victor, 2026-09-28).
>
> **Secuencia acordada con Victor (2026-09-30):** se llega hasta tener el plan redactado; luego se **espera a que el grupo de «niveles, paquetes, Plan Maestro y RDT» termine y pushee**, se revisa este plan contra lo que ese grupo deje (migraciones, pantallas, permisos nuevos) y recién entonces se pide el Gate 1 y se continúa. **Mientras tanto, nada se pushea a `main`** (solo commits locales); el push llega con la aprobación del Spec y del plan.

## Identificación y estado

- Tema: llevar a la app la interfaz del artefacto «Matriz de permisos» para que administrador y jefe de proyectos cambien quién ve cada pantalla y quién ejecuta cada acción, sin desplegar.
- Fecha: 2026-09-30.
- Estado: **Planificando** (plan y Punch List redactados el 2026-10-01; Spec aprobado el 2026-09-30). Siguiente: esperar a que el grupo de paquetes termine y pushee, repetir la comprobación de «Estado tras el grupo de paquetes» y pedir el Gate 1 (con las autorizaciones y preguntas del plan).
- Orquestador: Claude (sesión de 2026-09-30). Planner: Claude (plan redactado 2026-10-01). Worker y Auditor: por asignar.

## Spec / SDD

### Estado

`Aprobado` (2026-09-30).

### Problema y contexto

Hoy los permisos viven **fijos en el código** (`src/lib/permisos/permisos.ts`, 460 líneas, una función por acción o interfaz, más los roles y sus etiquetas). Cambiar quién puede algo obliga a modificar código, probar y desplegar. La decisión de qué rol hace qué se toma con Victor en el artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT), se copia al flujo 14 y luego alguien la traduce a código; los tres sitios pueden desalinearse (el 2026-09-30 se encontraron dos filas de descargas desactualizadas en el artefacto).

**Estado verificado del código (`py_control_proyectos_web`, `main`, `45c9e0a`, 2026-09-30):**

| Pieza | Lo que hace hoy | Dónde |
|---|---|---|
| Permisos | Funciones `puedeXxx(roles)` con los roles escritos dentro; 13 roles fijos. Un usuario puede tener varios roles (`rolesUsuario: Rol[]`). | `src/lib/permisos/permisos.ts` |
| Dónde se usan | 52 rutas de API y 32 páginas importan esas funciones. | `src/app/api/**/route.ts`, `src/app/**/page.tsx` |
| Registro único de accesos | Cada chip/acceso de los paneles declara su función de permiso; nav y paneles se derivan de él. | `src/lib/config/registro-accesos.ts` (611 líneas) |
| Matriz derivada | Calcula una matriz roles × accesos evaluando cada función con un solo rol; se compara con una transcripción de ~30 filas del flujo 14. | `src/lib/config/matriz-accesos.ts`, `matriz-base-flujo14.ts` |
| Alcance por OT | Aparte del rol: escribir sobre una OT exige tenerla asignada en `proyecto_miembros`. | `src/lib/permisos/alcance-proyecto.ts` |
| Registro de cambios de permisos | No existe. No se encontró tabla de bitácora en `db/`. | `db/` (última migración: 072) |

**Estado verificado del artefacto:** base de datos `matriz/actual` con 15 interfaces y 49 acciones; cada fila guarda los roles marcados, si es económica (solo interfaces), un comentario, y la aprobación global. El artefacto no conoce «Requiere OT a cargo» (eso solo está en el flujo 14).

**Diferencias entre las filas del artefacto y las funciones del código** (el Spec debe resolverlas, no ignorarlas):
- Varias filas del artefacto se cubren con **una** función (por ejemplo adjudicar, crear programa y crear portafolio), y otras dos filas pueden compartir función; 64 filas frente a 53 funciones.
- «Subir documento del proyecto» depende además del rol responsable de cada documento (`catalogo_documentos.rol_responsable_id`); no cabe en una casilla fija.
- «Asignar rol administrador» y «Ver como» son exclusivas del administrador «por diseño de sistema» (flujo 14).
- El código exige un rol conocido para varias descargas («rechaza a quien no tenga un rol conocido»); el artefacto solo marca 13 casillas.

### Resultado esperado

1. Una pantalla en la app (solo administrador y jefe de proyectos), con las dos tablas del artefacto: interfaces (con su marca de «económica») y acciones; una casilla por rol; comentario por fila; y la aprobación.
2. Lo que se guarda en esa pantalla **es lo que la app aplica**, en servidor y en interfaz, en producción, sin desplegar.
3. **Cada cambio queda registrado:** quién, cuándo, qué fila, qué rol, valor anterior y nuevo.
4. La validación ocurre siempre en servidor: un cambio enviado por alguien sin permiso para gestionar permisos se rechaza (403), aunque el navegador lo permita.
5. Una defensa contra el bloqueo propio: el sistema **nunca** deja sin acceso a la propia pantalla de gestión (el administrador siempre puede gestionarla) ni quita las dos filas exclusivas del administrador.
6. La pantalla se asemeja al artefacto en estructura, sin limitarse a él (puede mejorarlo). Manda la app; el artefacto sigue existiendo y se actualiza tras cada guardado (D4).

### Alcance

- Modelo de datos para guardar permisos por fila y rol, y el registro de cambios (migración nueva; el número se toma al planificar, después de lo que el grupo de paquetes deje).
- Lectura de esos permisos desde el servidor, con los valores actuales del flujo 14 como **valores iniciales** (la base de datos se siembra con lo que hoy hace `permisos.ts`, así el día uno nada cambia para nadie).
- Cambio de las funciones de `permisos.ts` para que consulten lo guardado (o un espejo en caché) y no los roles escritos en el código.
- Pantalla de gestión: dos tablas, casillas, comentarios, marca económica, botón «Guardar cambios» (borrador, D3) y registro de cambios visible. Chip en la página «Configuraciones» (D7).
- Alta de la pantalla en el registro único de accesos y como chip en la página «Configuraciones», **y en la propia matriz de permisos** (la política exige actualizar el artefacto y el flujo 14 en la misma tarea).
- Pruebas por los 13 roles, con la habilidad `verificar-permisos-por-rol`.
- Documentación: flujo 14, flujo 16, flujo 02 si aplica, `planes-futuros.md` (promover el ítem y corregir dos entradas desactualizadas), design.md si hay componente nuevo.

### No alcance

- El **alcance por OT** (`proyecto_miembros`) no se vuelve editable aquí: sigue fijo en código y por usuario.
- Crear roles nuevos o renombrar los 13 (los roles siguen fijos).
- Permisos **por usuario** (excepciones individuales); esta pantalla es por rol.
- El **Dashboard Parcial sin datos económicos** y la restricción económica definitiva: son otro Spec (`planes-futuros.md`). Aquí la marca «económica» solo clasifica la fila; no separa datos de un mismo dashboard.
- Permisos de los paquetes de trabajo y cualquier interfaz que el grupo de paquetes cree: esas filas entran cuando ese grupo las deje en `main` (ver D6).
- El asistente del shell (no tiene fila, flujo 14).

### Usuarios / roles afectados

- **Administrador y jefe de proyectos:** usan la pantalla.
- **Los 13 roles:** todo lo que cada uno ve o ejecuta pasa a depender de lo guardado. El día uno, igual que hoy.

### Reglas de negocio y documentos afectados

| Documento | Por qué |
|---|---|
| `14-accesos-y-restricciones.md` | La tabla deja de ser la única fuente de los valores: pasa a ser la **referencia aprobada** y la pantalla el instrumento (D4). Se añade la regla de quién puede cambiar la matriz y el registro de cambios. |
| `16-paneles.md` | La pantalla es un acceso nuevo: un chip en la página «Configuraciones» (rueda del shell) y su alta en el registro único. |
| `01-configuracion.md` | Hoy «pendiente de definir»; esta pantalla es su primer contenido real. Se consulta a Victor antes de editarlo. |
| `07-nucleo-auth.md` y `02-usuarios.md` | Revisar si citan «permisos fijos en código» o la tabla de roles. |
| `planes-futuros.md` | Promover el ítem; corregir «4 roles con economía» (hoy 5 más dos excepciones) y los conflictos CO1 a CO5 (ya resueltos). Se consulta a Victor antes de editar. |
| Artefacto «Matriz de permisos» | Fila nueva: «Gestionar la matriz de permisos» (administrador y jefe de proyectos). |

Regla de negocio nueva que este Spec propone (a confirmar en el Gate Spec): **«Solo administrador y jefe de proyectos cambian permisos; el administrador no puede quedarse sin acceso a la gestión de permisos; la columna del administrador no es editable; «Asignar rol administrador» y «Ver como» son solo del administrador y no se pueden dar a otro rol.»**

### Datos, API, migraciones o dependencias

- **Datos nuevos (propuesta, el Planner la detalla):** una tabla de permisos (clave de fila, tipo interfaz/acción, rol, permitido, marca económica, comentario) y una tabla de bitácora de cambios. Se siembran con los valores vigentes de `permisos.ts`.
- **API:** leer la matriz (cualquier usuario autenticado no necesita esa lectura; el servidor la consulta) y guardarla (solo quien gestiona permisos, con validación de fila, rol y reglas de bloqueo).
- **Migración:** aditiva, sin borrar ni renombrar columnas. **No se corre ninguna migración sin confirmar con Victor** (AGENTS.md).
- **Dependencias:** el plan `2026-09-27-paneles-servicio-persistente` (ya mergeado: el registro único de accesos). Y **el grupo de paquetes en curso**, que toca permisos y migraciones (ver riesgos).

### Diseño / UI aplicable

- **Criterio de fidelidad (Victor, 2026-09-30):** la pantalla se asemeja en **estructura** al artefacto (dos tablas, roles en columnas, comentario por fila), pero eso **no limita mejorar lo actual** (por ejemplo, filtros, búsqueda, agrupación, mejor lectura del registro de cambios). Toda mejora respeta `design.md` y no cambia las reglas ya decididas.
- La pantalla parte del artefacto (dos tablas con scroll horizontal, columnas de roles, columna «Fila» y «Comentario», contorno de cambio, aprobación), según `docs/05-diseno-y-referencias/design.md`; no se crea un estilo nuevo.
- Se ubica como un chip dentro de la página «Configuraciones» (D7), registrado en el registro único, no como una pantalla suelta.
- Estados vacío, carga y error; accesible con teclado; responsive con la regla del repositorio.

### Decisiones de Victor (2026-09-30)

| Id | Decisión | Resuelto |
|---|---|---|
| D1 | Dónde se guardan los permisos | **Base de datos** como fuente, sembrada con los valores de hoy. Cambiar un permiso no toca el código. |
| D2 | Qué no se puede editar | **El rol administrador completo:** su columna en las dos tablas no se edita desde la interfaz (ni se le quita ni se le agrega nada), así nunca pierde su acceso, incluida esta pantalla. Además, «Ver como» y «Asignar rol administrador» quedan fijas: solo el administrador, y ningún otro rol puede recibirlas desde la pantalla (Victor: «nadie puede ver "ver como"»; se aplicó la misma regla a «Asignar rol administrador» por igual motivo, a confirmar al aprobar el Spec). |
| D3 | Cómo se aplican los cambios | **Borrador y botón «Guardar cambios» al final.** Hasta guardar, la app aplica lo último guardado. |
| D4 | Relación con el artefacto | **El artefacto sigue existiendo. Manda la app:** si difieren, vale la app. Tras cada «Guardar cambios», el artefacto y el flujo 14 se actualizan para coincidir. |
| D5 | Marca «económica» | **Editable**, pero solo informativa hasta el Spec de economía. |
| D6 | Filas de lo que crea el grupo de paquetes | **Se agregan al final**, cuando ese grupo pushee (los ocho accesos de paquetes del flujo 14 y las pantallas nuevas). |
| D7 | Ubicación de la pantalla | **Un chip dentro de «Configuraciones»**, que se abre con la rueda pequeña de la parte inferior izquierda del shell (`WorkspaceShell.tsx`, botón «Configuraciones», ruta `/configuraciones`, verificado en el código). Hoy esa página solo muestra el tema oscuro y la sesión. No se crea grupo nuevo en el registro de accesos: el chip se suma a esa página y se registra en el registro único y en el flujo 16. Todos los roles entran a «Configuraciones»; el chip de permisos lo usa solo quien gestiona permisos, y los demás lo ven deshabilitado (regla del flujo 16). |

### Riesgos

- **Bloqueo propio:** una mala edición podría dejar a nadie con acceso a la pantalla. Mitigación: reglas de D2 en servidor, y restauración a la siembra.
- **Pérdida de protección por un error de datos:** si la tabla falla o queda vacía, el sistema podría permitir o negar de más. Mitigación: ante error, **se niega** (falla cerrada), salvo para administrador.
- **Rendimiento:** 52 rutas y 32 páginas consultarían la matriz en cada llamada. Mitigación: lectura única por solicitud y caché corta; el Planner la dimensiona.
- **Desalineación con el grupo de paquetes:** migraciones numeradas en paralelo, funciones de permisos nuevas y filas nuevas de la matriz. Por eso el plan espera a que ese grupo termine.
- **Filas sin función propia** (las 64 frente a 53): el Planner define la correspondencia fila ↔ función antes de codificar.
- **Rol «sin rol conocido»:** varias descargas lo rechazan hoy; la tabla debe conservar esa regla.

### Criterios de aceptación

1. Con la siembra, la app responde **igual que hoy** para los 13 roles en las dos tablas del flujo 14 (sin diferencias).
2. Un cambio guardado en la pantalla cambia lo que ve y puede hacer ese rol, sin desplegar, verificado con una cuenta del rol.
3. Un rol que no es administrador ni jefe de proyectos no puede guardar cambios (403 en servidor).
4. Nadie puede quitarle al administrador el acceso a la gestión, ni editar las dos filas exclusivas.
5. Cada cambio aparece en el registro con autor, fecha, fila, rol, antes y después.
6. Si la lectura de permisos falla, el sistema niega (falla cerrada).
7. Artefacto, flujo 14, flujo 16 y `planes-futuros.md` quedan coherentes entre sí; lo que contradiga lo escrito se consultó a Victor.

### Estrategia de prueba / evidencia

- Pruebas unitarias de las funciones de permisos contra la siembra (hoy ya hay 589 líneas de pruebas por los 13 roles como base).
- Prueba de cada regla de bloqueo y de falla cerrada.
- Verificación en interfaz con las cuentas de prueba (Playwright), usando `verificar-permisos-por-rol` (suplantación de rol y llamadas sin efecto).
- Comparación matriz guardada ↔ flujo 14 ↔ artefacto.
- Sin migraciones ni escrituras en datos reales sin confirmación.

### Aprobación (Gate Spec)

- [x] Victor aprueba este Spec (2026-09-30), con el criterio de fidelidad añadido.

## Entorno, repositorios, ramas y worktrees

- Entorno: **local** (verificado: la app es accesible en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`).
- Documentación: `pg_control_proyectos`, `main`, directo.
- Código: `py_control_proyectos_web`, rama `local-worker-1` (existe en el mismo commit que `main`, `45c9e0a`, ya mergeada). **Se reutiliza solo con autorización de Victor**; nada se crea ni se mueve sin ella.
- **Espera a propósito:** no se asigna Worker hasta que el grupo de paquetes pushee; la rama puede cambiar de base en ese momento.
- Skills del repositorio de documentación que aplican: `verificar-permisos-por-rol` (toda tanda que toque permisos), `cerrar-tanda` (al final de cada tanda), `seguir-flujo-de-planes` (Orquestador). El repositorio de código no tiene Skills.

---

# PLAN (paso 6, Planner, 2026-10-01)

> Redactado por el Planner sobre el Spec aprobado de arriba. Estado: **listo para Gate 1, pero el Gate 1 espera** a que el grupo de «niveles, paquetes, Plan Maestro y RDT» termine y pushee (secuencia acordada con Victor). Al lanzarse, se repite la comprobación de la sección «Estado tras el grupo de paquetes».

## Puertas

- Gate Spec: `aprobado por Victor (2026-09-30)`
- Gate 1: `pendiente`
- Gate 2: `pendiente`

## Referencia al Spec aprobado

Spec de este mismo archivo (arriba), decisiones D1 a D7, criterios de aceptación 1 a 7 y los riesgos. Este plan no cambia ninguna decisión; donde el Spec deja un hueco (qué hacer con las filas que no tienen permiso detrás, cómo se sincroniza el artefacto, qué pasa con la regla de economía) el plan propone una salida y la deja como **pregunta abierta** para Victor (sección «Preguntas abiertas»).

## Objetivo, alcance y no alcance

- **Resultado esperado:** los del Spec. En una frase: que administrador y jefe de proyectos cambien desde la app, en un chip de «Configuraciones», quién ve cada pantalla y quién ejecuta cada acción; lo guardado es lo que la app aplica en servidor y en interfaz, sin desplegar; cada cambio queda en un registro; y nadie puede bloquearse.
- **Alcance:** el del Spec, más lo que el plan concreta: 67 filas (15 interfaces y 52 acciones), una migración aditiva (`087`), reconexión de las funciones de `permisos.ts` y del registro único, API de gestión, pantalla con borrador y registro de cambios, mecanismo realista de sincronización con el artefacto y el flujo 14, y la documentación.
- **No alcance:** el del Spec (alcance por OT, roles nuevos, permisos por usuario, Dashboard Parcial sin economía, asistente del shell). Además, **este plan no corrige** las brechas de código ya registradas en otros planes (aprobar un borrador del Plan Maestro; ver «Estado tras el grupo de paquetes»): la siembra las refleja tal como están hoy.
- **Validación esperada:** los siete criterios del Spec, cada uno con su ítem de verificación en la Punch List; pruebas automáticas (equivalencia con la siembra de los 13 roles en las 67 filas, falla cerrada, bloqueos) y verificación en navegador con `verificar-permisos-por-rol`.

## Entorno, repositorios, ramas y worktrees

Ver la sección «Entorno, repositorios, ramas y worktrees» de arriba (local; documentación directo en `main`; código en rama de Worker). Lo que el plan agrega:

- **Código:** `py_control_proyectos_web`. Ramas propuestas: `local-worker-1` (carril de permisos) y `local-worker-2` (carril de datos, API y pantalla). **Solo con autorización de Victor** (ver «Autorizaciones y datos de prueba para el Gate 1»); antes de empezar se reubican en `origin/main` una vez que el grupo de paquetes haya pusheado, comprobándolo con `git branch --contains` y no de memoria.
- **Documentación:** `pg_control_proyectos`, `main`. Briefs en `docs/02-trabajo-activo/01-planes/2026-09-30-gestion-permisos-desde-app-briefs/` (índice de tandas, reglas de contexto, protocolo de migraciones adaptado del plan de paquetes, un brief por tanda, carpeta `resultados/`).
- **Base de datos:** la única base compartida del proyecto (la misma que usa el grupo de paquetes). No hay entorno de pruebas aparte: por eso la migración es solo aditiva y la verificación en vivo se limita a cambios reversibles (ver Gate 1).

## Skills aplicables

| Skill (`.claude/skills/` de `pg_control_proyectos`) | Dónde se usa |
|---|---|
| `seguir-flujo-de-planes` | Orquestador: al activar el flujo, antes del Gate 1, y antes de escribir el mensaje de cierre. |
| `verificar-permisos-por-rol` | Tandas T4, T5, T6 y T9 (toda tanda que toque permisos por rol): suplantación de rol y llamadas sin efecto, contra las tablas 1 y 2 del flujo 14. |
| `cerrar-tanda` | Al final de **cada** tanda (T0 a T10): estados de la lista, evidencia, resumen de cierre, revisión de fuentes de verdad y commit verificado. |
| `trasladar-hallazgos` | Solo en la tanda final de documentación (T10): traslada el libro de hallazgos a su destino sin editar por su cuenta las fuentes centrales. |

El repositorio de la app no tiene carpeta de Skills (comprobado en el plan de paquetes). Ningún Skill nuevo se propone por ahora; el Auditor puede proponer alguno (por ejemplo «sincronizar la matriz de permisos con el flujo 14 y el artefacto»).

## Fases y dependencias

Una sola migración nueva y un cambio profundo en `permisos.ts`; por eso el orden importa. **T0 a T10 son tandas de 4 a 8 ítems, brief de 8 KB como máximo y unas 80 llamadas por Worker.**

| Tanda | Qué hace | Carril | Depende de |
|---|---|---|---|
| T0 | Maqueta de la pantalla (tres paneles, estados, registro de cambios) | Documentador | nada (no bloquea; Victor la revisa mientras corren T1 a T6) |
| T1 | Catálogo de 67 filas, siembra en código y reglas de bloqueo | W1 | nada |
| T2 | Migración 087: tablas, función atómica, RLS y siembra; aplicación y verificación | W2 | T1 (de ahí sale la siembra) |
| T3 | Almacén de la matriz, cargador de servidor con caché, falla cerrada, proveedor de cliente, acceso en el registro | W1 | T1 y T2 aplicada |
| T4 | Funciones de permisos 1 a 1 reconectadas | W1 | T3 |
| T5 | Funciones compartidas divididas por fila, rutas y páginas, registro de accesos, prueba de inventario | W1 | T4 |
| T6 | API de gestión (leer, guardar, bitácora, reflejada, exportar) | W2 | T2 y el contrato de T3 |
| T7 | Pantalla: ruta, chip, tablas y celdas | W2 | T6 (T0 como guía) |
| T8 | Pantalla: borrador, guardar, registro de cambios, sincronización, pruebas de componente | W2 | T7 |
| T9 | Verificación en vivo con navegador y regresión | W1 (uno a la vez con navegador) | T5 y T8 |
| T10 | Documentación y traslado de hallazgos (Documentador) | Documentador | T9 (y las respuestas de Victor a las preguntas) |

Después: Auditor (informe en `04-auditoria/`) y Gate 2. El merge y el push de la app solo tras el Gate 2.

**Orden de migraciones:** una sola, `087_permisos_matriz.sql`, que es la siguiente libre (la última es `086`; comprobado que `origin/main` y las cuatro ramas `local-worker-*` no traen `087` ni posteriores). Antes de aplicar, el Orquestador vuelve a comparar `db/` de `origin/main` y de las ramas por si otro grupo tomó el número; si lo tomó, se renumera esta (aditiva, sin dependencias de orden con las anteriores salvo que `permisos_filas_roles` apunta a `roles(clave)`, que ya existe desde `002`).

**Olas sugeridas** (máx. 2 Workers a la vez por el límite de uso de la cuenta, que ya cortó tandas del grupo anterior): ola 1 = T0 y T1; ola 2 = T2; ola 3 = T3 (W1) y arranque de T6 (W2) contra el contrato; ola 4 = T4 y T6; ola 5 = T5 y T7; ola 6 = T8; ola 7 = T9; ola 8 = T10 y Auditor.

## Equipo del plan

| Rol | Modelo | Sesión o tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|
| Orquestador | Sonnet | sesión actual | `main` | N/A | activo |
| Planner | Sonnet | este plan | `main` | N/A | terminó (plan redactado) |
| Worker 1 (carril de permisos) | Sonnet | T1, T3, T4, T5, T9 | `local-worker-1` (a autorizar) | por autorizar | sin asignar |
| Worker 2 (carril de datos, API y pantalla) | Sonnet | T2, T6, T7, T8 | `local-worker-2` (a autorizar) | por autorizar | sin asignar |
| Documentador | Sonnet | T0 y T10 | `main` | N/A | sin asignar |
| Worker git | Haiku | a pedido (merge, push, reubicar ramas) | opera sobre las demás | | sin asignar |
| Auditor | Sonnet | tras T10 | `main` | N/A | sin asignar |

**Por qué dos Workers y no tres:** hay independencia real de archivos entre el carril de permisos (`permisos.ts`, almacén, registro de accesos, call sites) y el de datos/API/pantalla (`db/`, `src/app/api/permisos/**`, `configuraciones/permisos/**`, `src/components/permisos/**`). Un tercero tropezaría con ambos. **Alternativa:** un solo Worker en secuencia (más lento, sin riesgo de choque). Decide Victor en el Gate 1; se recomienda dos.

**Contrato entre carriles (para no pisarse):** W1 es dueño de `src/lib/permisos/**`, `registro-accesos.ts`, `usuario-actual.ts`, `layout.tsx` del workspace y `WorkspaceShell.tsx`; W2 es dueño del resto de lo nuevo. W2 consume de W1 únicamente `puedeGestionarPermisos(roles)`, `reglas-matriz.ts`, `catalogo-filas.ts`, `siembra-permisos.ts` y `invalidarMatriz()` (todos entregados en T1 y T3). Si W2 necesita cambiar algo de W1, lo pide por el Orquestador.

### Brief de cada Worker

Un brief por tanda en `…-briefs/` (plantilla `13-brief-de-tanda.md`, ≤ 8 KB), con: archivos que puede tocar, ítems con su criterio, Skills a usar (de la tabla de arriba), comandos de verificación de la app (`npm test`, `npx tsc --noEmit`, `npm run lint`; verificados en `package.json`: `test` = `vitest run`, `lint` = `eslint`), y el formato del resumen de cierre. El Orquestador los escribe al lanzar cada ola.

### Prompt del Auditor

Alcance: las 64 filas de la Punch List, el código de las ramas de los Workers y los documentos de T10. Primer chequeo (obligatorio): con `git log` y `git branch --contains`, confirmar que los commits están en la rama del Worker asignado. Revisar: (1) los siete criterios del Spec con su evidencia; (2) trazabilidad: artefacto, flujo 14, flujo 16, flujo 01, `planes-futuros.md`, `08-arquitectura-funcional-y-datos.md`, `AGENTS.md` y la política de coherencia coinciden entre sí y con la tabla «dice hoy / pasaría a decir» aprobada; (3) que cada hallazgo del libro se trasladó a su destino; (4) que se usaron los Skills citados; (5) que ninguna ruta o página usa una función de permiso fuera del catálogo (prueba de inventario T5-6); (6) que la verificación en vivo dejó los datos como estaban (valores revertidos; bitácora de prueba identificada). Formato: `06-informe-auditoria.md` con APLICAR AHORA / PROPONER A RESPONSABLE / NO PROMOVER / PROPONER SKILL. Clasifica además las observaciones sobre la política de este plan.

## Estado tras el grupo de paquetes

Verificado con herramientas el 2026-10-01 (solo lectura). Fuentes: `git` de ambos repositorios, `permisos.ts`, `registro-accesos.ts`, `db/`, flujos 14 y 16, progreso del grupo de paquetes y el estado guardado del artefacto (`matriz/actual`, 15 interfaces y 49 acciones).

### Lo ya verificado

| Dato | Resultado |
|---|---|
| App, `main` | `main` = `origin/main` = `0250dab` (F5-A, integración de los cuatro carriles). Árbol limpio. Es lo que el Spec llamó «`origin/main` ya trae la integración F5-A». |
| Migraciones | Última: `086_plan_maestro_partidas_disciplina.sql` (`db/README.md` documenta 073 a 086). **Siguiente libre: `087`.** Ni `origin/main` ni `local-worker-1` a `-4` traen `087` o mayor. (El Spec decía «hasta 072»: quedó desactualizado.) |
| Permisos en código | `permisos.ts`: 470 líneas, 13 roles. 113 archivos importan `permisos/permisos` (53 rutas de API, páginas y 6 componentes de cliente; el Spec decía 52 y 32). Las funciones nuevas del grupo: `puedeCrearVersionPlanMaestro` (ya existía en el Spec) y nada más; **no hay funciones de permisos nuevas para paquetes** (`puedeGestionarPaquetesTrabajo` delega en `puedeGestionarPlanMaestro`; `puedeVerPaquetesTrabajo` = rol conocido). |
| Registro de accesos | Sin chips ni accesos nuevos del grupo (lo afirma `integracion-permisos.test.ts`). «Crear paquete» ya estaba. `/configuraciones` está declarada como **excepción** de cobertura de pantallas (`cobertura-pantallas.ts`): «se abre desde el menú de usuario, no desde los paneles». |
| Flujo 14 tras F5-D2 (commits locales `c27a50d` y `e8361f0`, aún sin push) | Tabla 1: **15 interfaces** (sin cambio). Tabla 2: **51 acciones** (hoy dos más que el artefacto): «Reasignar de paquete un RDT aún no validado» (nota 10) y «Crear una versión nueva del Plan Maestro» (nota 9); notas 8 a 10 nuevas. «Gestionar paquetes» ya incluye vínculos con metrado e hitos. |
| Artefacto «Matriz de permisos», estado guardado | 15 interfaces y **49 acciones**: **faltan esas 2 filas** de F5-D2 (no se había actualizado cuando se escribió este plan; es pendiente del Orquestador, regla de la política de coherencia). Con la fila nueva de este plan serían 52. |
| D6 («las ocho filas de paquetes») | Ya no existen como ocho: F5-D2 las redujo a la fila de interfaz «Paquetes de trabajo, ver», la acción «Gestionar paquetes de trabajo» y las dos acciones de arriba. **D6 queda cumplido con esas filas, incluidas en la siembra desde el día uno**; no hay «filas al final» que esperar. |
| Brechas de código ya registradas | (a) `PATCH /api/plan-maestro` usa `puedeGestionarPlanMaestro`, así que el planner podría aprobar un borrador que creó un administrador o jefe de proyectos (flujo 14, punto 6 de «Puntos por decidir»). (b) `GET proyectos/[id]/registro-costos` combina «ver» y «descargar». (c) `puedeVerApartadoProyectos` se calcula en `layout.tsx` y se pasa a `WorkspaceShell`, que declara el campo y **no lo lee** (ver «Carpetas/archivos huérfanos»). Esta tarea no las corrige; la siembra las refleja como están. |

### Lo que falta revisar al lanzar el plan

1. **El grupo de paquetes no ha terminado:** no existen `resultados/F5-B.md` ni `F5-C.md` (verificación en vivo, comprobación por rol); faltan el Auditor, el Gate 2, el merge y el push. Tres commits de documentación (`c27a50d`, `9a95e68`, `e8361f0`) están solo locales.
2. **Repetir la comparación** justo antes del Gate 1: `git diff 0250dab origin/main -- src/lib/permisos src/lib/config db` en la app, y `git diff` de `14-accesos-y-restricciones.md` y `16-paneles.md`. Si F5-B o F5-C agregaron una función de permiso, una fila o una migración, T1 las incorpora al catálogo y la siembra antes de seguir.
3. **Reconfirmar el número 087** (ver «Fases y dependencias»).
4. **Actualizar el artefacto** con las dos filas de F5-D2 (Orquestador); no hace falta esperar a este plan, pero T1 parte de que el flujo 14 es la referencia, no el artefacto.
5. **No verificado por el Planner:** dónde se hospeda la app y si corre en una o varias instancias (afecta solo el plazo en que otra instancia nota un cambio; ver «Caché y rendimiento»); el comportamiento de módulos de servidor y de cliente en Next 16 (se comprueba en T3-4 y T9-5); las cuentas de prueba (no se leyeron; ver Gate 1).

## Modelo de datos

**Decisión D1 (base de datos como fuente) y D3 (borrador hasta «Guardar cambios»).** El borrador **no se guarda en la base**: vive en el navegador de quien edita; la app solo aplica lo último guardado. Un guardado es **una sola operación atómica** que escribe los valores y la bitácora (si falla, no queda nada a medias). Si Victor prefiere un borrador que sobreviva al cierre de la pestaña, es la pregunta 5.

### Tablas (migración `087_permisos_matriz.sql`, aditiva e idempotente)

| Tabla | Para qué | Columnas principales |
|---|---|---|
| `permisos_filas` | Una fila por interfaz o acción (67). Metadatos y lo editable por fila. | `clave` (texto, clave primaria; **se reutilizan las claves del artefacto**, p. ej. `crono`, `adjudicar`; nuevas: `reasignarrdt`, `versionpm`, `gestpermisos`), `tipo` (`interfaz`/`accion`), `seccion`, `etiqueta`, `orden`, `economica` (editable, solo interfaces, D5), `comentario` (máx. 500), `fija` (no editable), `requiere_ot` (informativa, no editable), `actualizado_en`, `actualizado_por`. |
| `permisos_filas_roles` | Casilla fila × rol (67 × 13 = 871). | `fila_clave` → `permisos_filas`, `rol` → `roles(clave)` (ya existe y es única), `permitido`; clave primaria `(fila_clave, rol)`. |
| `permisos_matriz_estado` | Una sola fila: versión y sincronización. | `version` (sube con cada guardado), `actualizado_en/por`, `reflejada_version`, `reflejada_en/por` (hasta qué versión se reflejó en el artefacto y el flujo 14). |
| `permisos_bitacora` | **Registro de cambios; solo se agrega, nunca se edita ni se borra** (disparador y permisos lo impiden). | `id`, `guardado_id` (agrupa lo guardado de una vez), `version`, `fecha`, `usuario_id`, `usuario_nombre` (copia del nombre al momento), `fila_clave`, `fila_etiqueta`, `campo` (`permitido`/`economica`/`comentario`), `rol` (nulo si no aplica), `valor_anterior`, `valor_nuevo`, `motivo` (opcional, lo escribe quien guarda). |

- **Función `guardar_matriz_permisos(p_version_base, p_cambios jsonb, p_usuario_id, p_usuario_nombre, p_motivo)`:** bloquea la fila de estado, compara la versión base (si no coincide, error de versión desactualizada, que la API traduce a 409), aplica solo cambios que de verdad difieren, **vuelve a validar en SQL** las reglas de bloqueo (segunda línea de defensa: columna del administrador, filas fijas, marca económica solo en interfaces), escribe la bitácora y sube la versión. Devuelve la versión nueva y cuántos cambios aplicó.
- **RLS activada en las cuatro tablas, sin políticas para usuarios**; solo la clave de servicio (la API, después de validar permiso) lee y escribe. La función no se puede ejecutar con los roles `anon` ni `authenticated`. Los permisos de lectura que la app reparte (ver «Caché») salen de la API de servidor, no de consultas del navegador.
- **Siembra:** 67 filas, 871 casillas, comentarios y marcas «económica» del estado actual del artefacto, más las tres filas nuevas. Se genera **desde `siembra-permisos.ts`** (T1), que a su vez se produce **evaluando las funciones actuales de `permisos.ts` antes de tocarlas** («como hoy»), y una prueba compara la siembra con el flujo 14 y con `MATRIZ_BASE_FLUJO14`. `on conflict do nothing`: volver a ejecutar el archivo no pisa lo que se editó. Una prueba compara el SQL con el TypeScript (conteos y valores) para que no se desalineen.
- **Reversión:** el archivo termina con un comentario que dice cómo deshacerlo (borrar las cuatro tablas y la función); no se ejecuta sin autorización de Victor. Nada de lo existente se borra ni se renombra.
- **Qué NO se guarda en la base:** la columna del administrador y las filas fijas **no se leen de la base**; vienen de una constante en código (así, aunque la tabla quedara vacía o alterada, el administrador conserva el acceso y las dos filas exclusivas siguen exclusivas). Tampoco se guarda el alcance por OT.

### Cómo se evalúa un permiso (regla única, `puedeEnFila(clave, roles)`)

1. Si el usuario **no tiene ningún rol conocido** (lista vacía o roles ajenos a los 13): **niega**. Conserva la regla actual de las descargas que «rechazan a quien no tiene un rol conocido».
2. Si la fila es **fija o libre** (ver más abajo): resuelve por la constante en código.
3. Si el usuario es **administrador**: usa la columna fija del administrador (constante: todo ✓ salvo «Subir registro de costos por servicio», que hoy el administrador no tiene y, por D2, no se le agrega).
4. Para los demás roles: ✓ si **alguno** de sus roles tiene la casilla marcada en lo guardado (igual que hoy: un usuario con varios roles suma). **Si lo guardado no está disponible, niega** (falla cerrada, Spec).

## Correspondencia fila ↔ función de permisos

Hoy hay **67 filas** (15 + 52) frente a unas 53 funciones. El plan fija: **una fila = una clave = una función que la lee**. Donde una función cubre varias filas, se divide (T5); donde dos funciones leen la misma fila, ambas se conservan como alias (T4). Los nombres de las funciones y sus firmas **no cambian** para las rutas y páginas que ya existen, salvo las que se dividen. Las claves son las del artefacto; la columna «Verificar» marca lo que el Worker de T1 debe comprobar en el código antes de fijarlo.

### Interfaces (tabla 1)

| Clave | Fila (flujo 14) | Función(es) hoy | Tratamiento |
|---|---|---|---|
| `dash_srv` | Dashboard del servicio | `puedeVerDashboard` | 1 a 1. Marca económica. |
| `dash_port` | Dashboard del portafolio | `puedeVerDashboardPortafolio` | 1 a 1. Marca económica. |
| `pr` | PR | `puedeVerPr` | 1 a 1. Económica. |
| `dp` | DP, ver | `puedeVerDp` | 1 a 1. Económica. Exportar DP tiene fila propia (`descdp`). |
| `curva` | Curva S | `puedeVerCurvaS` | 1 a 1. Económica. |
| `pm` | Plan Maestro, ver | `puedeVerPlanMaestro` | 1 a 1. Económica. |
| `regcostos` | Registro de costos, ver | `puedeVerRegistroCostos` | 1 a 1. Económica. La ruta de registro de costos hoy exige «ver» **y** «descargar» a la vez: T5-4 conserva ese comportamiento. |
| `crono` | Cronograma, ver | `puedeVerCronograma` | 1 a 1. |
| `paq` | Paquetes de trabajo, ver | `puedeVerPaquetesTrabajo` | 1 a 1. |
| `rdts` | RDTs: status, archivo de subidos, consolidado | `puedeVerRdts` | La función hoy también protege las **descargas** de RDT: se separan en T5-2 (filas `descrdts`, `descpdfrdt`, `descarchrdt`) para que cambiar una no cambie la otra. |
| `rqver` | RQ: status y consolidado | `puedeVerStatusRequerimiento` y `puedeVerConsolidadoRq` | Dos funciones, una fila (las dos leen `rqver`). |
| `recursos` | Recursos de empresa (consulta) | `puedeVerRecursos` | 1 a 1. |
| `ficha` | Ficha del servicio y grilla del portafolio | ninguna (`PERMISO_LIBRE`) | **Fila libre con candado** (pregunta 1). |
| `panelizq` | Panel izquierdo del servicio | ninguna | **Fila libre con candado** (pregunta 1). |
| `notif` | Notificaciones y Mi entorno | ninguna | **Fila libre con candado** (pregunta 1). |

### Acciones (tabla 2)

| Clave | Fila | Función(es) hoy | Tratamiento |
|---|---|---|---|
| `adjudicar` | Adjudicar proyecto / crear programa / crear portafolio | `puedeAdjudicarProyecto`; `puedeCrearPrograma` y `puedeCrearPortafolio` delegan en ella | 1 fila, 3 funciones (alias). |
| `transicion` | Confirmar transición de estado | `puedeConfirmarTransicionEstado` | 1 a 1. La precondición del Plan Maestro aprobado sigue en servidor. |
| `archivar` | Archivar / eliminar proyecto | `puedeArchivarProyecto` y `puedeEliminarProyecto` | 1 fila, 2 funciones. |
| `elimcont` | Eliminar contenedor | `puedeEliminarContenedor` | 1 a 1. |
| `editserv` | Editar servicio | `puedeEditarServicio` | 1 a 1. |
| `editcheck` | Editar checklist del proyecto | `puedeModificarChecklist` | 1 a 1. |
| `impdp` | Importar DP | `puedeImportarDp` | 1 a 1. |
| `usuarios` | Gestionar usuarios | `puedeGestionarUsuarios` | 1 a 1. |
| `perfil` | Editar perfil extendido (propio) | `puedeEditarPerfilExtendido` | 1 a 1. |
| `roladmin` | Asignar rol administrador | `puedeAsignarRolAdministrador` | **Fija:** solo administrador, no editable (D2). |
| `vercomo` | Simular otro usuario o rol («Ver como») | `puedeSimularRol` (en `src/lib/auth/ver-como.ts`, usa los roles reales) | **Fija:** solo administrador, no editable (D2). No pasa por la matriz. |
| `subirdoc` | Subir documento del proyecto | `puedeSubirDocumento` y `puedeSubirDocumentoAsignado` | **Caso especial.** La casilla decide solo «administrador y jefe de proyectos» (editable el jefe de proyectos). Se suma siempre, en código, **el rol responsable de ese documento** (`catalogo_documentos.rol_responsable_id`) y el usuario asignado. La fila muestra un texto fijo: «Además puede el rol responsable de cada documento (se define en el catálogo de documentos, no aquí)». |
| `crearpersonal`, `editarpersonal`, `eliminarpersonal` | Personal: crear, editar, eliminar o desactivar | hoy una sola: `puedeGestionarRecursos` (rutas `recursos/personal` y `recursos/personal/[id]`) | **Se divide en 3 funciones** (T5-1). |
| `crearcargo`, `editarcargo`, `eliminarcargo`, `crearequipo`, `editarequipo`, `eliminarequipo` | Cargos y equipos | `puedeGestionarRecursos` (rutas `recursos` y `recursos/[id]`) | **Se divide en 6 funciones** (T5-1); verificar por tipo de recurso en la ruta. |
| `cnc`, `cncestado`, `editarcnc` | Causas CNC: crear, activar/desactivar, editar texto | `puedeGestionarCatalogoCnc` (delegaba en `puedeGestionarRecursos`) | **Se divide en 3 funciones** (T5-1). |
| `subirrdt` | Subir RDT | `puedeSubirRdt` | 1 a 1. |
| `crearrdt` | Crear RDT estructurado | `puedeCrearRdtEstructurado` | 1 a 1. |
| `reasignarrdt` | Reasignar de paquete un RDT no validado | hoy `puedeValidarRdt` (la ruta `PATCH rdts/partes/[id]` lo exige antes de cualquier acción) | **Fila nueva** (F5-D2). Función nueva `puedeReasignarPaqueteRdt`; la ruta pasa a pedir la fila de la acción concreta. **Verificar** (T4-2) que cambiar la fila tenga efecto real y no quede tapada por la exigencia general de validar. |
| `validar` | Validar / rechazar RDT | `puedeValidarRdt` | 1 a 1. |
| `corregir` | Corregir RDT rechazado | `puedeCorregirRdt` | 1 a 1. |
| `rechval` | Rechazar un RDT ya validado | `puedeRechazarRdtValidado` | 1 a 1. |
| `elimrdt` | Eliminar RDT | `puedeEliminarRdt` | 1 a 1. |
| `subircrono` | Subir / reemplazar cronograma | `puedeSubirCronograma` | 1 a 1. |
| `gestpm` | Gestionar Plan Maestro | `puedeGestionarPlanMaestro` | 1 a 1. Es la que usa hoy el `PATCH` (brecha registrada). |
| `versionpm` | Crear una versión nueva del Plan Maestro | `puedeCrearVersionPlanMaestro` | **Fila nueva** (F5-D2); función ya existe. |
| `gestpaq` | Gestionar paquetes de trabajo | `puedeGestionarPaquetesTrabajo` (hoy delega en `puedeGestionarPlanMaestro`) | Pasa a **su propia fila** (T4-3). Sembrada igual. |
| `crearrq` | Crear requerimiento | `puedeCrearRequerimiento` | 1 a 1. |
| `comentarrq` | Comentar requerimiento | `puedeComentarRequerimiento` | 1 a 1. |
| `estadorq` | Actualizar estado de RQ | `puedeActualizarEstadoRequerimiento` | 1 a 1. |
| `derivarrq` | Derivar RQ a logística | `puedeDerivarRequerimientoLogistica` | 1 a 1. |
| `elimrq` | Eliminar requerimiento | `puedeEliminarRequerimiento` | 1 a 1. |
| `descrq` | Descargar consolidado RQ (PROM-GP-004) | `puedeDescargarConsolidadoRq` | 1 a 1. |
| `subircostos` | Subir registro de costos por servicio | `puedeSubirRegistroCostosServicio` | 1 a 1. **El administrador no la tiene hoy**; queda como está y no se le puede agregar (columna fija). |
| `descregcostos` | Descargar registro de costos por servicio | `puedeDescargarRegistroCostosServicio` | 1 a 1 (la ruta además pide «ver»; ver `regcostos`). |
| `descdp` | Exportar DP (Excel o PDF) | hoy `puedeVerDp` (ruta `proyectos/[id]/dp/exportar`) | Fila propia, función nueva. Sembrada igual a `dp`. |
| `descrdts` | Descargar RDTs (ZIP) y listado (PDF) | hoy `puedeVerRdts` (ruta `rdts/exportar`) | Fila propia (T5-2). |
| `descpdfrdt` | PDF de un RDT estructurado | hoy `puedeVerRdts` (ruta `rdts/partes/[id]/pdf`) | Fila propia (T5-2). |
| `descarchrdt` | Archivo de un RDT subido | hoy `puedeVerRdts` (ruta `rdts/[id]/archivo`) | Fila propia (T5-2). |
| `descrqlist` | Listado RQ según filtro (PDF PROM-GP-008) | hoy `puedeVerStatusRequerimiento` (ruta `proyectos/[id]/requerimientos/exportar`) | Fila propia (T5-3). |
| `descpdfrq` | PDF individual de un RQ | hoy probablemente `puedeVerStatusRequerimiento` | **Verificar** la ruta en T1-1. Fila propia (T5-3). |
| `descformato` | Formato vacío PROM-GP-008 | `puedeDescargarFormatoRequerimientoVacio` | 1 a 1. Rechaza a quien no tiene rol conocido (regla 1). |
| `descplantcrono` | Plantilla de cronograma | `puedeDescargarPlantillaCronograma` | 1 a 1. Ídem. |
| `gestpermisos` | **Gestionar la matriz de permisos (nueva)** | `puedeGestionarPermisos` (nueva) | **Fija:** administrador y jefe de proyectos; ninguna casilla editable (pregunta 2). Es la fila que protege la propia pantalla. |

**Filas fijas (6):** `roladmin`, `vercomo`, `gestpermisos` (no editables ni por los gestores) y las libres `ficha`, `panelizq`, `notif` (se muestran con candado; pregunta 1). **Quedan 61 filas editables × 12 roles (todos menos el administrador) = 732 casillas editables.** Además son editables la marca «económica» (solo en las 15 interfaces; hoy 7 la tienen: dashboard del servicio, dashboard del portafolio, PR, DP, Curva S, Plan Maestro y registro de costos; solo informativa, D5) y el comentario de cada fila editable.

**Funciones que NO tienen fila y se quedan en código** (lista cerrada, verificada por la prueba de inventario T5-6): `puedeVerEconomia` (pregunta 3), `puedeVerApartadoProyectos` (sin uso real, ver «Carpetas/archivos huérfanos»), `etiquetaRol`, `etiquetaRolPrincipal` y `tieneRolConocido` (utilidades), y `tieneAlcanceSobreProyecto` (alcance por OT, no cambia).

**Consecuencia para las pruebas existentes:** `permisos.test.ts` (591 líneas) y las de registro, matriz derivada y equivalencia siguen verdes **sin cambiar sus expectativas**, porque en pruebas el almacén se inicia con la siembra (un archivo de preparación de `vitest`, T3-6). Eso es justamente el criterio 1 del Spec: «con la siembra, igual que hoy».

## API y servidor

Todas las rutas siguen el patrón actual: `obtenerUsuarioActual()` → comprobación del permiso con la función → recién entonces lectura o escritura con el cliente de servicio (`crearClienteAdmin`, solo en servidor). Nada se confía al navegador.

| Ruta | Método | Quién | Qué hace |
|---|---|---|---|
| `/api/permisos/matriz` | `GET` | `puedeGestionarPermisos` | Devuelve filas, casillas, versión, estado de sincronización y la siembra (para «Restablecer»). Sin caché del navegador (`no-store`). |
| `/api/permisos/matriz` | `PUT` | `puedeGestionarPermisos` | Recibe `{ versionBase, cambios: [{ fila, rol?, permitido? , economica?, comentario? }], motivo? }`. Valida con `reglas-matriz.ts` y vuelve a validar en SQL; llama a la función atómica; invalida la caché propia; devuelve la versión nueva. |
| `/api/permisos/bitacora` | `GET` | `puedeGestionarPermisos` | Registro de cambios paginado por cursor (50 por página) con filtros por fila, rol, usuario y fechas. |
| `/api/permisos/reflejada` | `POST` | `puedeGestionarPermisos` | Marca hasta qué versión quedó reflejada en el artefacto y el flujo 14 (quién y cuándo). |
| `/api/permisos/exportar` | `GET` | `puedeGestionarPermisos` | `?formato=json` (mismo formato que el estado guardado del artefacto: `interfaces` y `acciones` con `eco`, `nota`, `roles`), `?formato=md` (tablas 1 y 2 en el formato del flujo 14) y la lista de diferencias respecto de la última versión reflejada. |

**Códigos de respuesta:** `401` sin sesión; **`403` si el usuario no gestiona permisos** (también bajo «Ver como»: se evalúan los roles efectivos, así la suplantación sirve para probar el 403); `400` con la lista de errores por fila (columna del administrador, fila fija, marca económica en una acción, rol o fila inexistente, comentario demasiado largo, cambio vacío mal formado); `409` si la versión base no es la vigente (otro gestor guardó antes; la respuesta trae la versión actual para recargar sin perder el borrador); `500` con mensaje genérico sin detalles internos. La **bitácora anota al usuario real**, no al rol simulado.

**Falla cerrada:** si la lectura de la matriz falla o devuelve algo inválido, `puedeEnFila` niega todo salvo la columna fija del administrador; el cargador registra el error (sin datos sensibles) y reintenta en la siguiente solicitud. La pantalla de gestión, si no puede leer, muestra un error y **nunca una tabla vacía que parezca «todo denegado»**.

### Caché y rendimiento

- **Qué se carga:** la matriz completa son 67 filas y 871 casillas, unos pocos KB. Una sola consulta con lectura de las tres tablas.
- **Dónde:** un almacén en memoria del proceso de servidor (`almacen-matriz.ts`, **sin** `server-only`, porque `permisos.ts` también lo importan componentes de cliente) y un cargador solo de servidor (`cargar-matriz.ts`, con `server-only`) que lo refresca cuando pasaron más de **10 segundos**. `obtenerUsuarioActual()` espera ese refresco antes de devolver al usuario: como **toda ruta y página ya la llama antes de decidir permisos**, las funciones `puedeXxx(roles)` siguen siendo **síncronas y con la misma firma**, y no hay que reescribir los 113 archivos que las usan. React `cache()` evita repetir la consulta dentro de una misma solicitud.
- **Al guardar:** la instancia que guarda invalida su almacén de inmediato. Si la app corriera en varias instancias, las demás notan el cambio en **10 segundos como máximo** (la pantalla lo dice). No hay un canal en tiempo real: no hace falta.
- **Cliente:** `layout.tsx` entrega la matriz a `WorkspaceShell` (componente de cliente que calcula los paneles con los roles), y este la establece **antes de evaluar** `construirPanelIzquierdo/Derecho`. Es un mapa `fila → roles` sin secretos (los chips ya se ven deshabilitados). Riesgo conocido de Next: los módulos de servidor y los de cliente renderizado en servidor son instancias separadas; por eso el almacén se establece explícitamente al renderizar el componente y se prueba en T3-4 y en navegador en T9-5 (sin diferencias de hidratación).
- **Alcance por OT:** no cambia; sigue siendo una segunda capa por usuario (`tieneAlcanceSobreProyecto`).

## Interfaz

**Dónde:** un chip dentro de la página «Configuraciones» (D7), que se abre con la rueda del shell (`WorkspaceShell.tsx`, botón «Configuraciones», ruta `/configuraciones`, verificado). Hoy esa página solo muestra el tema oscuro y la sesión. Se convierte en una página con una **fila de chips**: «Preferencias» (lo de hoy) y «Permisos y accesos» (nuevo, ruta `/configuraciones/permisos`). Todos los roles entran a Configuraciones; el chip de permisos lo usan solo quienes gestionan permisos y los demás lo ven **deshabilitado con el motivo** (regla del flujo 16: nunca se oculta). Quien escriba la URL sin permiso recibe el rechazo del servidor (el chip deshabilitado no es una barrera).

**Registro único:** el acceso `gestionar-permisos` se declara en `registro-accesos.ts` (tipo acción, `requiereServicio: 'no'`, permiso `puedeGestionarPermisos`, **visible en ninguno de los tres paneles**, porque vive dentro de Configuraciones y no en los paneles del servicio). Como el registro exige un grupo, se usa el existente más cercano fuera de la navegación del servicio, «Mi entorno» (**no se crea grupo nuevo**, D7). `/configuraciones` sigue siendo excepción de cobertura; `/configuraciones/permisos` queda cubierta por el registro. Ratificar esto en el Gate 1 (está en la tabla de cambios a flujos).

**Estructura (semejante al artefacto, mejorada donde conviene, sin estilos nuevos; `design.md` §5 y §8):**

1. Cabecera de página y fila de chips de Configuraciones.
2. **Banda de estado:** versión vigente, quién guardó por última vez y cuándo; aviso de sincronización con los documentos («al día» o «hay cambios de las versiones n a m sin reflejar en el flujo 14 y el artefacto»); aviso «los cambios se aplican en toda la app en un máximo de 10 segundos».
3. **Barra de acciones:** contador «N cambios sin guardar», botón primario **«Guardar cambios»** (deshabilitado sin cambios), «Descartar» y «Restablecer a valores iniciales» (carga la siembra en el borrador; no guarda).
4. **Pestañas:** «Interfaces», «Acciones» y «Registro de cambios».
5. **Tabla de interfaces** (como el artefacto): columna fija «Fila», marca «Económica» editable, **13 columnas de rol** (abreviaturas del flujo 14 con el nombre completo en `title`) con una casilla por rol, comentario por fila (máx. 500).
6. **Tabla de acciones** agrupada por sección (Proyecto y sistema, Recursos, RDT, Planificación, RQ y costos, Descargas), con la columna informativa «Requiere OT a cargo» (que el artefacto no tenía) y la nota de «Subir documento».
7. **Celdas bloqueadas** (columna del administrador y filas fijas o libres): casilla marcada o vacía con **candado** y `title` que explica el motivo; no se pueden editar.
8. **Contorno de cambio** en la celda modificada (como el artefacto) y fila resaltada.
9. **Mejoras sobre el artefacto:** búsqueda por texto, filtro por sección, «solo filas con cambios», resalte de la columna del rol al pasar el cursor o el foco, confirmación antes de guardar con la lista «antes → después» y motivo opcional, y un registro de cambios legible (ver abajo).
10. **Registro de cambios** (pestaña): tabla paginada agrupada por guardado: autor, fecha, fila, rol, valor anterior, valor nuevo, motivo; filtros por fila, rol y usuario.

**Estados:** *carga* (esqueleto de tabla); *vacío* (registro de cambios sin entradas: «Todavía no se ha cambiado nada desde la siembra»); *error de lectura* (mensaje con «Reintentar»; no se pinta la tabla); *error al guardar* (400 con las filas observadas marcadas; 403 con aviso de que perdió el permiso; 409 con «Otra persona guardó antes: recargar» conservando el borrador; 500 genérico conservando el borrador); *sin permiso* (si llegan por URL: mensaje y vuelta a Configuraciones).

**Accesibilidad y diseño:** tablas con `<th scope>`, encabezado y primera columna fijos, scroll horizontal con el contexto visible (regla del repositorio), casillas con `aria-label` que nombran rol y fila («Jefe de Proyectos puede Adjudicar proyecto»), orden de tabulación coherente, color nunca como única señal (el contorno de cambio lleva también texto «modificado» para lectores de pantalla), aviso al salir con cambios sin guardar. Se reutilizan las clases de tabla compartidas (`tablaWrapClase`, `tablaClase` de `Table.tsx`) y los tokens de `globals.css`; antes de codificar, el Worker de T7 responde el **análisis de pre-vuelo de §11** de `design.md`. La **maqueta T0** va primero y es la guía visual; si aparece un componente nuevo reutilizable se documenta en `design.md` en T10.

## Cómo se sincronizan el artefacto y el flujo 14 después de cada guardado

La decisión D4 dice: manda la app; tras cada «Guardar cambios», el artefacto y el flujo 14 se actualizan para coincidir. **La app no puede escribir en el artefacto ni en los documentos** (están fuera de ella y no se le dan credenciales para eso). Lo realista, y lo que este plan construye:

1. **Cada guardado sube una versión** y la app recuerda hasta cuál **se reflejó** (`reflejada_version`). Mientras haya diferencia, la banda de estado lo dice en la pantalla (es lo que evita que el desalineamiento pase inadvertido, como las dos filas de descargas que se encontraron el 2026-09-30).
2. **El botón «Exportar»** entrega, de la versión vigente: (a) el JSON en el formato del estado guardado del artefacto (`interfaces`/`acciones` con `eco`, `nota` y `roles`), listo para escribirse en el artefacto; (b) las tablas 1 y 2 en Markdown con el formato del flujo 14; (c) la lista de diferencias frente a la última versión reflejada.
3. **Quién actualiza y cuándo:** en la **siguiente sesión del Orquestador o cuando Victor lo pida**, con el archivo exportado (Victor lo entrega, o autoriza al Orquestador a leerlo con la cuenta de prueba), el Orquestador escribe los valores en el artefacto (con la herramienta de datos del artefacto) y el Documentador actualiza las tablas del flujo 14; luego un gestor pulsa **«Marcar como reflejada»**. No se declara «sincronizado» sin esa marca.
4. **Mientras no se sincroniza, manda la app** (D4). El flujo 14 conserva el rótulo «referencia aprobada» y la fecha de la última versión reflejada.
5. **Alcance de este plan:** al cierre (T10) el artefacto y el flujo 14 coinciden con la versión final guardada de la app. **Después del cierre** la sincronización pasa a ser un hábito de trabajo; la política de coherencia de `AGENTS.md` no define quién la hace (observación O-1, a decidir en el Gate 2). Se pregunta a Victor en la pregunta 4 si este camino le sirve.
6. **Lo que NO hace la prueba automática:** la prueba `MATRIZ_BASE_FLUJO14` compara la **siembra** con el flujo 14; no compara lo editado en producción (eso es justo lo que la banda y la exportación vigilan).

## Archivos / componentes afectados

**App (`py_control_proyectos_web`), nuevos:** `db/087_permisos_matriz.sql`; `src/lib/permisos/` → `catalogo-filas.ts`, `siembra-permisos.ts`, `reglas-matriz.ts`, `almacen-matriz.ts`, `cargar-matriz.ts` (solo servidor) y sus pruebas; `src/app/api/permisos/{matriz,bitacora,reflejada,exportar}/route.ts`; `src/app/(workspace)/configuraciones/permisos/page.tsx`; `src/components/permisos/*` (tablas, barra de guardar, registro de cambios, banda de estado); archivo de preparación de `vitest` que inicia el almacén con la siembra.
**App, modificados:** `src/lib/permisos/permisos.ts` (funciones leen filas; se dividen las compartidas; `puedeGestionarPermisos`, `puedeReasignarPaqueteRdt` y las de descarga nuevas); `src/lib/config/registro-accesos.ts` (permisos por fila y el acceso `gestionar-permisos`); `src/lib/auth/usuario-actual.ts` (espera el refresco del almacén); `src/app/(workspace)/layout.tsx` y `src/components/ui/WorkspaceShell.tsx` (entrega y establece la matriz en el cliente); `src/app/(workspace)/configuraciones/page.tsx` (fila de chips); rutas y páginas que usan las funciones divididas (recursos, descargas de RDT y RQ, DP, registro de costos, `rdts/partes/[id]`); `db/README.md`. Las 53 rutas de API y las páginas que ya usan una función 1 a 1 **no cambian**.
**Documentación (`pg_control_proyectos`):** flujos 14, 16 y 01; `planes-futuros.md`; `08-arquitectura-funcional-y-datos.md`; `AGENTS.md` y `01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md` (política, solo con consulta); `01-contexto-repositorio/05-diseno-y-ui.md`; `design.md` y `mockups/` (maqueta T0); progreso, evidencia y auditoría homónimos; el artefacto «Matriz de permisos». Los flujos 02 y 07 se revisaron: **no mencionan permisos fijos en código ni la tabla de roles** (solo «solo administrador asigna el rol administrador», que sigue igual), no requieren cambios. Los flujos 11 y 21 citan `puedeVerEconomia` y la lista de cinco roles: **no cambian** (la regla de economía se queda en código, pregunta 3).

## Punch List embebida

Formato de `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia de cada ítem va en `03-evidencia/2026-09-30-gestion-permisos-desde-app.md`. «Evidencia mínima» incluye el **criterio de aceptación** del ítem. Los identificadores `Tn-m` indican tanda y número. 64 ítems en 11 tandas.

### Estado de aprobación

Gate 1: **pendiente** (espera al grupo de paquetes; ver «Estado tras el grupo de paquetes»).

### Datos y cálculos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T1-1 | T1 | Inventario verificado fila ↔ función(es) ↔ rutas y páginas que la usan (67 filas) | `resultados/T1.md` con la tabla; cada fila tiene función, o está marcada fija o libre; las divergencias con la tabla de este plan quedan listadas | Sin verificar |
| T1-2 | T1 | `catalogo-filas.ts`: 15 interfaces y 52 acciones con clave, tipo, sección, etiqueta, orden, marca económica por defecto, «requiere OT», fija y nota | Prueba: 67 claves únicas, 15 + 52, etiquetas iguales a las del flujo 14, claves del artefacto reutilizadas | Sin verificar |
| T1-3 | T1 | `siembra-permisos.ts`: valores de las 67 × 13 casillas obtenidos evaluando las funciones **actuales** (constante fija, no recalculada) | Prueba: igual a `MATRIZ_BASE_FLUJO14` y a las tablas 1 y 2 del flujo 14 transcritas en la prueba; cualquier diferencia se reporta al Orquestador, no se corrige en silencio | Sin verificar |
| T2-1 | T2 | `db/087_permisos_matriz.sql`: cuatro tablas, función atómica, RLS, restricciones y disparador de solo-agregar en la bitácora | Revisión: solo `create ... if not exists` y `create or replace function`; nada borra ni renombra; comentario de reversión al final | Sin verificar |
| T2-2 | T2 | Siembra SQL generada desde `siembra-permisos.ts` (67 filas, 871 casillas, comentarios y marcas) con `on conflict do nothing` | Prueba automática compara SQL ↔ TypeScript (conteos y valores); volver a ejecutar no duplica ni pisa | Sin verificar |
| T2-3 | T2 | `db/README.md` con la entrada de la 087; script `migrar_T2.py` con modos `check` (por defecto, solo lectura) y `apply` | README actualizado; el script cumple el protocolo (candado, transacción, sin imprimir credenciales) | Sin verificar |
| T2-4 | T2 | Aplicar la 087 con autorización (candado, transacción) | Conteos antes/después de las tablas existentes **sin cambio**; después: 67 filas, 871 casillas, 1 fila de estado, 0 de bitácora | Sin verificar |
| T2-5 | T2 | Probar la función en una transacción **que se revierte**: versión desactualizada, columna del administrador, fila fija | Los tres casos se rechazan; tras revertir no queda bitácora ni cambio de versión (conteos) | Sin verificar |
| T6-5 | T6 | `reflejada` y `exportar` (JSON del formato del artefacto, Markdown del flujo 14, diferencias) | Con la siembra, el JSON exportado coincide con el estado guardado del artefacto salvo las 3 filas nuevas; el Markdown coincide con las tablas del flujo 14 (prueba) | Sin verificar |

### Permisos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T1-4 | T1 | `reglas-matriz.ts`: validación pura de cambios (columna del administrador, filas fijas, marca económica solo en interfaces, rol y fila existentes, comentario ≤ 500) | Pruebas exhaustivas, incluidas las tres reglas del Spec (criterio 4); la usan servidor y pantalla | Sin verificar |
| T3-1 | T3 | `almacen-matriz.ts` (sin `server-only`): `establecerMatriz`, `puedeEnFila` con la regla única de 4 pasos | Pruebas: rol desconocido niega; administrador por constante; fila libre y fija por constante; sin matriz niega | Sin verificar |
| T3-5 | T3 | `puedeGestionarPermisos` (fila fija: administrador y jefe de proyectos) y acceso `gestionar-permisos` en el registro único (grupo existente, sin visibilidad en paneles) | Prueba de registro (`validarRegistro`) y de humo en verde; 13 roles: solo administrador y jefe de proyectos | Sin verificar |
| T3-6 | T3 | Pruebas de falla cerrada y de administrador, y archivo de preparación de `vitest` con la siembra | Sin matriz, con matriz nula y con error de lectura: se niega todo salvo la columna fija del administrador | Sin verificar |
| T4-1 | T4 | Funciones de «Proyecto y sistema» leen su fila (adjudicar con sus alias, transición, archivar y eliminar, contenedor, servicio, checklist, importar DP, usuarios, perfil, asignar rol administrador, subir documento) | `permisos.test.ts` verde sin cambiar sus expectativas; `puedeSubirDocumento` suma el rol responsable en código | Sin verificar |
| T4-2 | T4 | Funciones de RDT (subir, crear, validar, corregir, rechazar validado, eliminar) y `puedeReasignarPaqueteRdt` | Verde; la ruta `PATCH rdts/partes/[id]` pide la fila de la acción concreta y **cambiar la fila de reasignar tiene efecto real** (prueba) | Sin verificar |
| T4-3 | T4 | Funciones de planificación (subir cronograma, gestionar Plan Maestro, versión nueva, gestionar paquetes con fila propia) | Verde; `puedeGestionarPaquetesTrabajo` ya no delega en el Plan Maestro y la siembra da lo mismo | Sin verificar |
| T4-4 | T4 | Funciones de RQ y costos (crear, comentar, estado, derivar, eliminar, descargar consolidado, subir y descargar registro de costos) | Verde; el administrador sigue **sin** «subir registro de costos» | Sin verificar |
| T4-5 | T4 | Funciones de las 12 interfaces con función (dashboards, PR, DP, Curva S, Plan Maestro, registro de costos, cronograma, paquetes, RDTs, RQ, recursos) | Verde; `puedeVerEconomia` sigue en código con su lista de cinco roles (pregunta 3) | Sin verificar |
| T5-1 | T5 | Recursos divididos por operación: 9 funciones de personal, cargos y equipos y 3 de causas CNC, con sus rutas y páginas | Cada ruta pide su función; con la siembra, igual que hoy; prueba por operación y por rol | Sin verificar |
| T5-2 | T5 | Descargas de RDT separadas de «ver» (`descrdts`, `descpdfrdt`, `descarchrdt`) | Cambiar una fila no cambia las demás (prueba); con la siembra, igual que hoy; rol desconocido rechazado | Sin verificar |
| T5-3 | T5 | Descargas de RQ y DP separadas (`descrqlist`, `descpdfrq`, `descdp`) y formato vacío y plantilla de cronograma | Igual que arriba | Sin verificar |
| T5-4 | T5 | Registro de costos: la ruta conserva exactamente lo que exige hoy («ver» y «descargar» juntos para descargar) | Prueba con los 13 roles contra el comportamiento previo | Sin verificar |
| T9-1 | T9 | Equivalencia el día uno en navegador: 13 roles × tablas 1 y 2 con `verificar-permisos-por-rol` | Tabla esperado ↔ observado sin diferencias (criterio 1 del Spec) | Sin verificar |
| T9-3 | T9 | 403 y bloqueos: los 12 roles que no gestionan reciben 403; jefe de proyectos y administrador pasan; columna del administrador y filas fijas se rechazan con 400 y no son editables en pantalla | Criterios 3 y 4 del Spec con evidencia por rol | Sin verificar |

### Funcionales

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T3-3 | T3 | `obtenerUsuarioActual()` espera el refresco del almacén antes de devolver; prueba de que toda ruta que decide permisos pasa por ella | Prueba de inventario (nombra rutas y páginas que no pasan, si las hay) | Sin verificar |
| T3-4 | T3 | `layout.tsx` entrega la matriz y `WorkspaceShell` la establece antes de evaluar los paneles | Prueba unitaria; la hidratación sin diferencias se confirma en T9-5 | Sin verificar |
| T5-5 | T5 | Registro de accesos: cada `permiso` lee su fila; `derivarMatrizAccesos` con la siembra da **cero diferencias** contra `MATRIZ_BASE_FLUJO14`; chips deshabilitados con título | Pruebas de registro, matriz y paneles verdes | Sin verificar |
| T5-6 | T5 | Prueba de inventario: toda función `puede*` exportada tiene fila o está en la lista cerrada de excepciones; ningún permiso por rol escrito a mano fuera de `permisos.ts` | Prueba que falla si aparece una función sin fila (protege contra el desalineamiento futuro) | Sin verificar |
| T8-1 | T8 | Borrador local: diferencia contra lo guardado, contorno de celda cambiada, contador y «Descartar» | Prueba de componente; marcar y desmarcar la misma casilla deja 0 cambios | Sin verificar |
| T8-2 | T8 | «Guardar cambios» con confirmación (lista antes → después, motivo opcional); éxito, 400, 403, 409 y 500 con mensaje claro; el borrador se conserva en 409 y 500 | Pruebas de componente con las cinco respuestas | Sin verificar |
| T8-3 | T8 | Aviso al salir con cambios sin guardar (cierre de pestaña y navegación interna) | Prueba de componente; comprobado a mano en T9-5 | Sin verificar |
| T8-4 | T8 | «Restablecer a valores iniciales»: carga la siembra en el borrador, sin guardar | Tras restablecer, el contador muestra solo lo que difiere de lo guardado | Sin verificar |
| T8-6 | T8 | Banda de sincronización, «Exportar» (JSON y Markdown) y «Marcar como reflejada» | Prueba: guardar sube la versión y activa el aviso; marcar lo apaga y registra quién y cuándo | Sin verificar |
| T9-2 | T9 | Ciclo de cambio real: con la cuenta de administrador, cambiar una casilla de bajo riesgo, guardar, ver el efecto con «Ver como» sin desplegar, revertir y comprobar el registro | Criterios 2 y 5 del Spec; el valor queda como antes; la bitácora trae los dos guardados con motivo «PRUEBA» | Sin verificar |

### UI / responsive / accesibilidad

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T0-1 | T0 | Maqueta `configuraciones-permisos.html` con los tres paneles reales (chips de Configuraciones, tabla de interfaces, tabla de acciones, barra de guardar) | Archivo en `docs/05-diseno-y-referencias/mockups/`, registrado en el índice, regla de «tres paneles» cumplida | Sin verificar |
| T0-2 | T0 | Maqueta de estados: carga, error de lectura, sin permiso, 409 y banda de sincronización | Mismos requisitos | Sin verificar |
| T0-3 | T0 | Maqueta del registro de cambios y de la confirmación antes de guardar | Mismos requisitos | Sin verificar |
| T0-4 | T0 | Análisis de pre-vuelo de tabla (`design.md` §11) y propuesta de componentes reutilizados y cambios a `design.md` | Texto en `resultados/T0.md`; no edita `design.md` | Sin verificar |
| T7-1 | T7 | Ruta `/configuraciones/permisos` y fila de chips en Configuraciones; chip deshabilitado con motivo; URL directa rechazada por el servidor | Pantallas cubiertas por la prueba de cobertura; deshabilitado con `aria-disabled` y `title` | Sin verificar |
| T7-3 | T7 | Tabla de interfaces: columna «Fila» fija, «Económica» editable, 13 roles con casilla, comentario por fila | Scroll horizontal con contexto, encabezado fijo, `th scope`, sin `max-w-*` en el contenedor | Sin verificar |
| T7-4 | T7 | Tabla de acciones agrupada por sección, con «Requiere OT a cargo» y la nota de «Subir documento» | Mismos criterios; 52 filas visibles | Sin verificar |
| T7-5 | T7 | Celdas bloqueadas (columna del administrador, filas fijas y libres) con candado y título; casillas con `aria-label` | Navegación con teclado; las celdas bloqueadas no cambian | Sin verificar |
| T7-6 | T7 | Búsqueda, filtro por sección, «solo filas con cambios» y resalte de la columna del rol | Funcionan con y sin borrador; responsive sin romper el shell | Sin verificar |
| T8-7 | T8 | Pruebas de componente y revisión contra `design.md` (tokens, sin colores nuevos, teclado) | Lista de comprobación de §11 respondida; sin colores fuera de tokens | Sin verificar |
| T9-5 | T9 | Capturas en escritorio y móvil, teclado, consola sin errores, sin diferencias de hidratación | Capturas en `03-evidencia/capturas/gestion-permisos-desde-app/` | Sin verificar |

### Estados vacío / carga / error

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T7-2 | T7 | Carga de datos con esqueleto, error de lectura con «Reintentar» (nunca una tabla vacía), sin permiso | Prueba de componente de los tres estados | Sin verificar |
| T8-5 | T8 | Registro de cambios visible: tabla paginada agrupada por guardado, con filtros, y sus tres estados (vacío, carga, error) | Prueba de componente; con la bitácora real (T9-2) se ven autor, fecha, fila, rol, antes y después (criterio 5) | Sin verificar |

### Validación en servidor / API

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T3-2 | T3 | `cargar-matriz.ts` (solo servidor): lectura con el cliente de servicio, caché de 10 s, `cache()` por solicitud, invalidación al guardar; error → se niega | Pruebas con doble de la base: caché, invalidación y error (criterio 6) | Sin verificar |
| T6-1 | T6 | `GET /api/permisos/matriz` | 401, 403 y 200 por rol (mocks); `no-store` | Sin verificar |
| T6-2 | T6 | `PUT /api/permisos/matriz`: valida, llama a la función atómica, invalida la caché, devuelve la versión | Prueba: guardado atómico (si falla la bitácora no queda el valor) y versión sube una vez | Sin verificar |
| T6-3 | T6 | Códigos 400 (errores por fila), 403, 409 (trae la versión actual) y 500 genérico | Una prueba por código; ningún mensaje interno al cliente | Sin verificar |
| T6-4 | T6 | `GET /api/permisos/bitacora` paginado con filtros | Prueba de paginación y filtros; solo gestores | Sin verificar |
| T6-6 | T6 | Los 13 roles contra cada ruta nueva con `verificar-permisos-por-rol` (mocks) | Solo administrador y jefe de proyectos pasan; con la lectura rota se niega | Sin verificar |
| T6-7 | T6 | Llamadas sin efecto a la base real: `PUT` con `cambios: []` y con un cambio inválido | Respuesta esperada; versión y conteo de la bitácora **sin cambio** | Sin verificar |
| T9-4 | T9 | Falla cerrada comprobada en local con el cargador inyectado (sin romper la base real) | Con la lectura rota, ninguna fila se concede salvo la columna del administrador; la pantalla muestra error | Sin verificar |

### Regresión

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T4-6 | T4 | Pruebas de permisos, registro, matriz derivada y equivalencia en verde sin cambiar expectativas; prueba nueva 13 roles × 67 filas = siembra | `npm test`, `npx tsc --noEmit` y `npm run lint` iguales o mejores que `main` | Sin verificar |
| T9-6 | T9 | Regresión general y recorrido por los casos sensibles: planner (Plan Maestro), supervisor de oficina técnica (DP), logística (registro de costos), jefe de costos | Mismas tres comprobaciones; recorrido sin cambios respecto de antes | Sin verificar |

### Documentación y trazabilidad (T10, Documentador)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| T10-1 | T10 | Flujo 14 según la tabla «dice hoy / pasaría a decir» (solo lo aprobado en el Gate 1) | Diff revisable; cada fila de la tabla tiene su edición | Sin verificar |
| T10-2 | T10 | Flujo 16 y flujo 01 según la tabla | Ídem | Sin verificar |
| T10-3 | T10 | `planes-futuros.md` (promover el ítem, corregir «4 roles» y los conflictos ya resueltos) y `08-arquitectura-funcional-y-datos.md` (tablas nuevas) | Ídem | Sin verificar |
| T10-4 | T10 | `AGENTS.md`, `02-arquitectura-y-fuentes-de-verdad.md` y `05-diseno-y-ui.md`: solo lo que la tabla marque y con consulta previa | Ídem; sin edición de política sin respuesta de Victor | Sin verificar |
| T10-5 | T10 | Artefacto «Matriz de permisos» con el estado final de la app (filas nuevas y las dos de F5-D2); **sin** marcar «Aprobada» | Lectura posterior del artefacto: 15 interfaces y 52 acciones; coincide con el flujo 14 y la exportación | Sin verificar |
| T10-6 | T10 | `design.md` y mockups si hay componente nuevo | Ídem | Sin verificar |
| T10-7 | T10 | `trasladar-hallazgos`: cada fila del libro a su destino; evidencia y progreso completos | Libro sin filas en `Registrada`; enlaces y commits anotados | Sin verificar |

## Cambios a flujos y documentos: «qué dice hoy / qué pasaría a decir / documento afectado»

Tabla única para el Gate 1 (paso 7, punto iii): su aprobación cubre a todos los Workers y al Documentador. **La columna «Consulta» marca lo que contradice o reemplaza algo ya escrito**: esas filas se muestran a Victor una por una al aprobar la tabla, antes de editar (política de coherencia). Las filas marcadas «No» son altas o precisiones que no contradicen nada. Las ediciones las hace el Documentador en T10, no antes; si una respuesta cambia, se corrige la fila.

| # | Documento y lugar | Dice hoy | Pasaría a decir | Consulta |
|---|---|---|---|---|
| 1 | `14-accesos-y-restricciones.md` § «Fuente y regla de actualización» | «El instrumento editable es el artefacto «Matriz de permisos»… Este archivo conserva la última versión aprobada.» | El instrumento editable es la **pantalla «Permisos y accesos» de la app** (D4: manda la app). Este archivo y el artefacto son la **referencia sincronizada**, con la fecha y la versión de la última sincronización; la sincronización se hace con la exportación de la app (sección «Cómo se sincronizan…»). | **Sí** |
| 2 | 14, mismo apartado, párrafo «Sincronización del artefacto» | «Desde entonces artefacto, flujo 14 y `permisos.ts` coinciden fila por fila.» | Artefacto, flujo 14 y la **siembra** coinciden fila por fila; los valores vigentes viven en la base y pueden diferir hasta la siguiente sincronización. | **Sí** |
| 3 | 14, § «Puntos por decidir», punto 2 | «La implementación debe alinear `permisos.ts` a esta matriz; el informe «antes/después por rol» lo produce la fase F0…» | La implementación alinea la **siembra** a esta matriz y las funciones de `permisos.ts` leen lo guardado en la base; el informe antes/después lo cubre T9-1 de este plan. | **Sí** |
| 4 | 14, tabla 2, sección «Proyecto y sistema» | (no existe la fila) | Fila nueva «Gestionar la matriz de permisos (pantalla «Permisos y accesos»)»: administrador ✓, jefe de proyectos ✓, resto —; requiere OT: No. Nota: fila fija, no editable desde la pantalla. | No |
| 5 | 14, nota 4 («Subir documento») | «…el administrador o el rol responsable de ese documento específico…» | Igual, más: el rol responsable se define en el catálogo de documentos y **no se edita en la matriz**; la casilla de la fila decide solo administrador y jefe de proyectos. | No |
| 6 | 14, sección nueva «Gestión de la matriz desde la app» | (no existe) | Reglas: quién gestiona (administrador y jefe de proyectos); la columna del administrador no se edita; «Asignar rol administrador», «Ver como» y esta fila son fijas y solo del administrador (la tercera, de administrador y jefe de proyectos); filas sin permiso detrás (ficha, panel izquierdo, notificaciones) con candado (pregunta 1); cambios por borrador y «Guardar cambios»; bitácora de solo-agregar con autor, fecha, fila, rol, antes y después; falla cerrada; aplicación en 10 s como máximo. | **Sí** (cada punto aprobado en el Gate Spec o en las preguntas) |
| 7 | 14, § «Pendiente a futuro → Gestión visual de accesos» | «…gestionen accesos y restricciones **por usuario**… Se retoma cuando esta matriz esté estable.» | «Implementado (fecha)»: la pantalla gestiona **por rol** (por usuario queda fuera, Spec «no alcance») y reemplaza esta nota. | **Sí** |
| 8 | 14, intro «Cómo leer las tablas» | Las columnas son los 13 roles fijos. | Sin cambio de roles; se agrega que las **casillas** pueden cambiar desde la app y la fecha de la última sincronización encabeza las tablas. | No |
| 9 | `16-paneles.md` § «Política de interfaz nueva», punto 5 | «Define su función de permiso en `permisos.ts`…» | «Declara su fila en la matriz de permisos (clave en el catálogo y siembra) y su función de `permisos.ts` **lee esa fila**». | **Sí** |
| 10 | 16, punto 6 de la política | «Sale en la matriz del flujo 14, derivada del registro; la tabla no se edita a mano.» | «Sale en la matriz: su fila se agrega al catálogo y a la siembra; los valores se editan **solo desde la pantalla de la app**, y el flujo 14 se sincroniza desde la exportación». | **Sí** |
| 11 | 16, § «Tabla de accesos» (párrafo de la fuente) | «El flujo 14 y el artefacto son la base de quién puede qué: el registro se ajusta a ellos…» | La **matriz guardada en la app** es la fuente viva; el flujo 14 y el artefacto son su referencia sincronizada; el registro lee la matriz. | **Sí** |
| 12 | 16, acceso nuevo | (no existe) | Acceso `gestionar-permisos`: acción, `requiereServicio` no, permiso `puedeGestionarPermisos`, ruta `/configuraciones/permisos`, **sin visibilidad en los tres paneles** (vive como chip de la página «Configuraciones»), grupo «Mi entorno»; `/configuraciones` sigue como excepción de cobertura. | No (D7) |
| 13 | `01-configuracion.md` | «Pendiente de definir/implementar… contenido original (interfaz/workspace)» | «Configuración» tiene su primer contenido real: la página `/configuraciones` con dos chips, «Preferencias» y «Permisos y accesos»; el contenido original de interfaz/workspace se conserva debajo. | **Sí** (el Spec lo exige) |
| 14 | `planes-futuros.md`, ítem «Gestión de permisos y accesos desde la app» | «Estado: pendiente, sin promover.» | «Promovido: plan `2026-09-30-gestion-permisos-desde-app` (fecha)» y, al cierre, «Implementado». | **Sí** |
| 15 | `planes-futuros.md`, ítem «Dashboard Parcial sin datos económicos…» | «…resolver los conflictos operativos que la regla de «4 roles con economía» deja abiertos (planner y Plan Maestro; …)» | «Cinco roles con economía más dos excepciones acotadas; los conflictos operativos ya están resueltos en las tablas 1 y 2 del flujo 14.» (No se encontró el rótulo «CO1 a CO5»; los conflictos se describen en esa línea.) | **Sí** |
| 16 | `08-arquitectura-funcional-y-datos.md` | Modelo de datos sin tablas de permisos. | Se agregan las cuatro tablas, la función atómica y que la matriz guardada es la fuente de los permisos. | No |
| 17 | `AGENTS.md` § «Políticas de coherencia y trazabilidad» (y su texto completo en `01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md`) | «El artefacto «Matriz de permisos»… es la base del flujo 14… Toda interfaz, acción, permiso o acceso nuevo… actualiza el artefacto y el flujo 14 en la misma tarea.» | Una vez que exista la pantalla: la **base es la matriz guardada en la app**; el artefacto y el flujo 14 se sincronizan con su exportación, y la regla «en la misma tarea» pasa a «al cerrar la tarea y tras cada guardado importante». **Es una edición de política: la hace Victor o se propone al Auditor** (observación O-1). | **Sí** |
| 18 | `01-contexto-repositorio/05-diseno-y-ui.md` (plantilla de ítems de interfaz nueva, fila «Fila en la matriz derivada del flujo 14») | «Diff de la matriz» | Se agrega «fila en el catálogo y la siembra de permisos». | No |
| 19 | `design.md` y mockups | (sin pantalla de permisos) | Maqueta nueva y, solo si aparece un componente reutilizable nuevo, su fila en §5. | No |
| 20 | Artefacto «Matriz de permisos» | 15 interfaces y 49 acciones; sin las dos filas de F5-D2 ni la de gestionar permisos | 15 interfaces y 52 acciones, con el estado final guardado de la app. No se marca «Aprobada» (lo decide Victor). | No (política vigente) |
| — | Flujos 02, 07, 11 y 21 | Verificados: no requieren cambio (ver «Archivos afectados»). | — | — |

## Autorizaciones y datos de prueba para el Gate 1

Lista consolidada (paso 7 del flujo). Se piden **todas en una sola consulta**; lo no pedido aquí se registra como `Observado` desde el brief.

**Autorizaciones**

1. **Aprobar** este plan, la Punch List (64 ítems en 11 tandas) y la tabla «dice hoy / pasaría a decir» (que cubre a todos los Workers y al Documentador, con las filas «Sí» respondidas).
2. **Carpetas de trabajo del código** (`py_control_proyectos_web`): usar `local-worker-1` y `local-worker-2` **reubicándolas en `origin/main`** después de que el grupo de paquetes haya pusheado (comprobado con `git branch --contains`); o crear `local-worker-5` y `-6` con sus carpetas. Recomendación: reutilizar las dos primeras, porque ya están integradas en `main`. Nada se mueve sin esta autorización. Y decidir **uno o dos Workers de código** (se recomiendan dos).
3. **Migración `087`:** aditiva, sin borrar ni renombrar nada; la aplica el Worker de T2 con el protocolo del plan de paquetes (candado, transacción, `migrar_T2.py` con `check`/`apply`, sin leer ni mostrar credenciales) contra la base compartida. Comprobación posterior con la función en una transacción que se revierte.
4. **Pre-autorización de operaciones que el clasificador suele bloquear:** inicio de sesión con las cuentas de prueba, herramientas de navegador (Playwright), «Ver como» y los scripts `migrar_*.py` (las reglas Allow ya están en `/permissions`; las reglas Deny de la carpeta de credenciales y de `entorno_variable` siguen vigentes). **Nunca cubre leer ni mostrar credenciales.**
5. **Escrituras de prueba sobre la matriz real** (T9-2): un cambio reversible en **una** casilla de bajo riesgo (propuesta: la plantilla de cronograma para un solo rol, no administrador), guardado con motivo «PRUEBA», verificado con «Ver como» y revertido al terminar. **La bitácora no se borra** (es de solo-agregar): quedan dos registros de prueba identificables. También: llamadas sin efecto (`PUT` con lista vacía o inválida) y probar la función SQL en una transacción que se revierte.
6. **Push:** las ramas de los Workers pueden subirse a su propia rama cada ~35 %, nunca a `main`; el merge y el push de la app solo tras el Gate 2, con autorización de Victor. Los commits de documentación (plan, progreso, resultados) van a `main` como en el plan anterior; **hasta el Gate 1 todo queda en commits locales**.
7. **Artefacto:** permiso para que el Orquestador escriba en la base de datos del artefacto «Matriz de permisos» al sincronizar (T10-5); la marca «Aprobada» no se toca.
8. **Ritmo:** máximo dos Workers a la vez y el navegador de uno en uno, por el límite de uso de la cuenta.

**Datos de prueba que se piden** (i): ningún servicio ni registro de datos reales; **las cuentas de prueba** que ya existen (las dos de la memoria del Orquestador; el Planner no las leyó) y el uso de «Ver como» para ver cada uno de los 13 roles. No se necesita quitar ni reponer membresías (esta tarea no toca el alcance por OT).

## Preguntas abiertas para Victor

Se hacen **de a una**, en lenguaje simple, con ejemplo y recomendación. Si Victor acepta la recomendación, se sigue sin más vueltas.

1. **Tres filas del artefacto no tienen ningún permiso detrás hoy.** «Ficha del servicio y grilla del portafolio», «Panel izquierdo del servicio» y «Notificaciones y Mi entorno» las ven los 13 roles porque el sistema no pregunta por rol. *Ejemplo:* si en la pantalla se desmarcara «Notificaciones» para RRHH, **hoy no pasaría nada**, y si lo conectáramos, RRHH quedaría sin notificaciones o sin menú. ¿Se muestran **con candado** (siempre los 13, no se pueden cambiar), o se conectan para poder quitarlas? **Recomendación: con candado**; es lo que evita que alguien se quede sin navegación y no inventa una regla nueva. *Si dice «conectar»:* se agregan funciones nuevas y pruebas en T4 y T5, y un riesgo de dejar a un rol sin navegación.
2. **La fila nueva «Gestionar la matriz de permisos» (administrador y jefe de proyectos): ¿se puede editar?** *Ejemplo:* ¿puede el administrador quitarle a los jefes de proyectos el acceso a esta pantalla? **Recomendación: fila fija** (no editable), porque el Spec aprobó la regla «solo administrador y jefe de proyectos cambian permisos». *Si dice «editable»:* solo la casilla del jefe de proyectos quedaría libre; la del administrador sigue fija.
3. **Quién ve los datos con dinero dentro de las pantallas (la «regla de economía»).** *Ejemplo:* si se le da el Dashboard del servicio a un planner desde la pantalla, él vería el dashboard, pero el interruptor Parcial/Completo y las columnas con dinero siguen la regla de los cinco roles que está en código. **Recomendación: dejar esa regla en código** hasta el plan de economía (el Spec ya dijo que la marca «económica» solo clasifica), y avisarlo con un texto en la pantalla. *Si dice «que también se edite»:* hace falta una fila técnica más y revisar el dashboard y la Curva S (otro plan).
4. **Cómo se mantienen al día el artefacto y el flujo 14 después de guardar.** La app **no puede escribir** en ellos. Lo propuesto: cada guardado sube una versión; la pantalla avisa «hay cambios sin reflejar»; el botón «Exportar» entrega el archivo; el Orquestador (con el archivo que Victor le pase, o leyéndolo con la cuenta de prueba) actualiza el artefacto y el flujo 14 en su siguiente sesión o cuando Victor lo pida, y un gestor marca «reflejada». *Ejemplo:* si Victor da hoy «Descargar plantilla de cronograma» a RRHH, esa tarde la matriz de la app manda y el flujo 14 queda atrasado hasta que se sincronice, con el aviso visible. **Recomendación: aceptar este camino**, porque es el único que no pone credenciales de documentos dentro de la app. *Alternativa:* un trabajo programado que lea la exportación y abra una tarea (más construcción, fuera de este plan).
5. **El borrador, ¿se pierde si se cierra la pestaña?** D3 pidió borrador y «Guardar cambios». *Ejemplo:* Victor marca 8 casillas, cierra el navegador sin guardar: **se pierden** (con aviso antes de salir). **Recomendación: así** (borrador solo en la pantalla), porque es lo más simple y evita un estado a medias en la base. *Alternativa:* guardar el borrador en la base (otra tabla, otro estado «sin aplicar» y más reglas de quién ve el borrador de quién).

## Riesgos y bloqueos

Incluye los del Spec (bloqueo propio, pérdida de protección por un error de datos, rendimiento, desalineación con el grupo de paquetes, filas sin función, rol sin rol conocido) con su mitigación en este plan: columna del administrador y filas fijas por constante en código (no se leen de la base); falla cerrada; almacén con caché de 10 s; revisión del grupo de paquetes antes del Gate 1; tabla fila ↔ función; regla 1 de `puedeEnFila`. Riesgos adicionales:

| Riesgo | Mitigación |
|---|---|
| Reconectar ~53 funciones y ~30 rutas cambia el comportamiento sin querer | Siembra generada desde las funciones actuales; prueba 13 roles × 67 filas contra el flujo 14; las pruebas existentes pasan sin cambiar expectativas (T4-6); verificación en navegador (T9-1). |
| Una función usada antes de que el almacén cargue deniega por error | `obtenerUsuarioActual()` espera el refresco; prueba de inventario (T3-3); falla cerrada (nunca concede de más). |
| En Next, el módulo del servidor y el del cliente renderizado en servidor son instancias distintas | El almacén se establece al renderizar `WorkspaceShell`; prueba en T3-4 y comprobación de hidratación en T9-5. |
| Otra instancia tarda en notar un cambio | Tope de 10 s y aviso en la pantalla; no se pudo verificar cuántas instancias hay (ver «Estado tras el grupo»). |
| Dos gestores guardan a la vez | Versión base y respuesta 409; el borrador se conserva. |
| La verificación en vivo escribe en la base compartida | Un solo cambio reversible, motivo «PRUEBA», verificación previa y posterior por conteos; la bitácora de prueba queda identificada (autorizado en el Gate 1). |
| La siembra se desalinea de lo aprobado | Prueba de siembra contra el flujo 14 y contra el SQL; un cambio de permisos en otro plan antes del Gate 1 se incorpora en T1 (revisión de «Estado tras el grupo»). |
| Otro grupo toma el número `087` | Reconfirmación antes de aplicar; renumerar es trivial (aditiva y sin dependencias de orden). |
| Límite de uso de la cuenta corta una tanda a medias | Tandas de ≤ 80 llamadas, 4 a 8 ítems, `resultados/<tanda>.md` al final, máximo dos Workers, y el Orquestador las reanuda con `SendMessage` sin rehacer (mejora del plan de paquetes). |
| El administrador pierde el acceso por una alteración directa de la base | Su columna y las filas fijas no se leen de la base. |
| Quien guarda bajo «Ver como» queda mal registrado | La bitácora anota al usuario real. |
| Datos personales en la bitácora (nombres) | Solo nombre y fecha de quien cambia; visible solo para quienes gestionan permisos. |


## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-09-30 | Objetivo confirmado: que administrador y jefe de proyectos cambien desde la app quién ve y ejecuta qué, sin desplegar; no cambian el alcance por OT, la validación en servidor ni las reglas de las tablas del flujo 14. | Victor |
| 2026-09-30 | Se llega hasta tener el plan; luego se espera a que el grupo de paquetes termine y pushee, se revisa este plan y se continúa. | Victor |
| 2026-09-30 | Decisiones D1 a D7 del Spec resueltas (ver tabla «Decisiones de Victor»). Artefacto verificado: versión 42, 49 acciones y 15 interfaces, cero diferencias con el flujo 14; marca «Aprobada» quitada, pendiente de Victor. | Victor / Orquestador |
| 2026-09-30 | **Gate Spec aprobado.** Criterio añadido: la interfaz se asemeja en estructura al artefacto sin limitar mejoras. | Victor |
| 2026-09-30 | Orquestador y Planner comitean cada vez que terminan algo, sin excederse; el push a `main` se habilita con la aprobación del Spec y del plan. | Victor |
| 2026-10-01 | Plan y Punch List redactados (64 ítems, 11 tandas). **Propuestas de diseño del Planner, a ratificar en el Gate 1:** claves de fila = las del artefacto (más `reasignarrdt`, `versionpm`, `gestpermisos`); una fila = una clave = una función; borrador solo en el navegador y guardado atómico con versión (409 si cambió); columna del administrador y filas fijas por constante en código; filas sin permiso detrás con candado (pregunta 1); fila de gestión fija (pregunta 2); `puedeVerEconomia` en código (pregunta 3); caché de 10 s con `obtenerUsuarioActual()` esperando el refresco para conservar las firmas síncronas; acceso `gestionar-permisos` en el registro sin visibilidad en paneles y en el grupo «Mi entorno»; sincronización por exportación y marca «reflejada» (pregunta 4); un solo `087`; dos Workers. | Planner |
| 2026-10-01 | Estado del grupo de paquetes verificado (ver sección homónima): `main` de la app `0250dab`, última migración `086`, flujo 14 con 51 acciones y artefacto con 49. | Planner |

## Enlaces a progreso y evidencia homónimos

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-09-30-gestion-permisos-desde-app.md` (se crea al lanzar la primera tanda).
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-09-30-gestion-permisos-desde-app.md` y `capturas/gestion-permisos-desde-app/` (se crean cuando haya algo que registrar).
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-09-30-gestion-permisos-desde-app.md` (la crea el Auditor).
- Briefs y resultados: `docs/02-trabajo-activo/01-planes/2026-09-30-gestion-permisos-desde-app-briefs/`.

## Libro de hallazgos

Los cuatro apartados siguientes son el libro oficial de hallazgos del plan (formato de la plantilla). Un hallazgo se anota cuando ocurre; los Workers dejan los suyos en su resumen de cierre y el Orquestador los pasa aquí. Al final, el Documentador (T10, Skill `trasladar-hallazgos`) traslada cada fila a su destino.

Formato de cada fila: ID / Fecha / Quién (rol, tanda) / Qué / Destino propuesto / Estado / Enlace al destino.

## Mejoras (de trabajo)

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| M-1 | 2026-10-01 | Planner (este plan) | Un intento anterior del Planner se cortó por el límite de uso y **no dejó nada** porque el plan se escribía al final. Método: leer lo necesario una sola vez, redactar el plan **por secciones en archivos de la carpeta temporal de la sesión** y volcarlo al archivo del plan en bloques, haciendo el commit al terminar. | Archivo nuevo en `docs/03-aprendizaje-continuo/` | Registrada | — |
| M-2 | 2026-10-01 | Planner (este plan) | Los números del Spec (última migración `072`, 52 rutas y 32 páginas) estaban desactualizados al planificar: el grupo de paquetes avanzó hasta `086`. Antes de planificar, **re-verificar con herramientas** todo número o estado del Spec que dependa de otro grupo en curso. | Archivo nuevo en `docs/03-aprendizaje-continuo/` | Registrada | — |

## Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| R-1 | 2026-09-30 | Victor (Gate Spec) | «Solo administrador y jefe de proyectos cambian permisos; la columna del administrador no es editable; «Asignar rol administrador» y «Ver como» son solo del administrador y no se dan a otro rol; el administrador no puede quedarse sin acceso a la gestión.» | Flujo 14, sección «Gestión de la matriz desde la app» (tabla de cambios, fila 6) | Registrada (aprobada) | — |
| R-2 | 2026-10-01 | Planner | Los cambios se guardan por **borrador y «Guardar cambios»**, de forma atómica y con versión; cada guardado deja en la bitácora (solo-agregar) autor, fecha, fila, rol, valor anterior y nuevo; la app aplica lo último guardado y, si no puede leerlo, **niega** (salvo la columna del administrador). Se deriva de D3, criterios 5 y 6 del Spec. | Flujo 14, misma sección | Registrada (derivada de lo aprobado) | — |
| R-3 | 2026-10-01 | Planner | Filas sin permiso detrás hoy (ficha, panel izquierdo, notificaciones): con candado, siempre los 13 roles. | Flujo 14 | Pendiente de decisión (Victor, pregunta 1) | — |
| R-4 | 2026-10-01 | Planner | La fila «Gestionar la matriz de permisos» es fija (administrador y jefe de proyectos). | Flujo 14 | Pendiente de decisión (Victor, pregunta 2) | — |
| R-5 | 2026-10-01 | Planner | La regla de economía (`puedeVerEconomia`) sigue en código hasta el plan de economía; la marca «económica» solo clasifica la fila (D5). | Flujo 14 y flujo 11 (sin cambio de texto, solo nota) | Pendiente de decisión (Victor, pregunta 3) | — |
| R-6 | 2026-10-01 | Planner | La app es la fuente viva; el artefacto y el flujo 14 son su referencia sincronizada mediante exportación y marca «reflejada». | Flujo 14, flujo 16, política | Pendiente de decisión (Victor, pregunta 4) | — |

## Observaciones sobre la política

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| O-1 | 2026-10-01 | Planner | La política de coherencia («toda interfaz, acción o permiso nuevo actualiza el artefacto y el flujo 14 en la misma tarea») supone que una persona edita las tres cosas. Cuando los permisos se cambian desde la app **ya no hay tarea ni autor que actualice los documentos**. La política no dice quién sincroniza, cuándo ni cómo se comprueba. Este plan propone la exportación y la marca «reflejada», pero la regla debería escribirse en la política. | Lista para el Auditor; Victor decide en el Gate 2 | Pendiente de decisión (Victor, Gate 2) | — |
| O-2 | 2026-10-01 | Planner | El paso 6 del estándar dice que el Planner hace commit y push a `main`; la secuencia acordada con Victor para este plan pide **solo commit local hasta el Gate 1**. El estándar no prevé un plan cuyo Gate 1 espera a otro grupo. | Lista para el Auditor | Registrada | — |

## Carpetas/archivos huérfanos

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| H-1 | 2026-10-01 | Planner | `puedeVerApartadoProyectos` (`py_control_proyectos_web/src/lib/permisos/permisos.ts`): `layout.tsx` la calcula y se la pasa a `WorkspaceShell`, que declara el campo en su tipo y **no lo lee** (verificado con búsqueda). Posible código sin uso; además su texto («solo administrador y jefe de proyectos») contradice el flujo 01 («lo ven todos los roles»). **No se borra**; se reporta a Victor. | Reporte a Victor al cerrar | Registrada | — |

## Informe de Auditoría

Enlace al archivo homónimo en `02-trabajo-activo/04-auditoria/` (`2026-09-30-gestion-permisos-desde-app.md`); lo crea el Auditor. El informe no se escribe dentro del plan.

## Mensaje de cierre

Pendiente (formato de `09-cierre.md`), a escribir por el Orquestador tras las acciones 16a a 16c.

## Elementos postergados propuestos para planes futuros

- Permisos por usuario (excepciones individuales) y alcance por OT editable (ya fuera del alcance en el Spec).
- Borrador compartido en el servidor, aprobación en dos pasos o comparación entre versiones (si Victor lo pide; ver pregunta 5).
- Tarea programada que compare la matriz de la app con el flujo 14 y avise (ver pregunta 4).
- Conectar las tres filas sin permiso detrás, si Victor responde «conectar» (pregunta 1).
- Regla de economía editable desde la pantalla, junto con el Dashboard Parcial sin economía (pregunta 3; otro plan).
- Corrección del `PATCH` que deja aprobar un borrador del Plan Maestro al planner (brecha ya registrada en el flujo 14).
