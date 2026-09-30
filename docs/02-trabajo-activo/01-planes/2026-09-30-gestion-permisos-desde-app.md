# 2026-09-30 — Gestión de permisos y accesos desde la app (matriz editable)

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Este archivo contiene el Spec (paso 3); el Planner agregará el plan debajo. Nace de «Planes futuros» → «Gestión de permisos y accesos desde la app (matriz editable)» (pedido de Victor, 2026-09-28).
>
> **Secuencia acordada con Victor (2026-09-30):** se llega hasta tener el plan redactado; luego se **espera a que el grupo de «niveles, paquetes, Plan Maestro y RDT» termine y pushee**, se revisa este plan contra lo que ese grupo deje (migraciones, pantallas, permisos nuevos) y recién entonces se pide el Gate 1 y se continúa. **Mientras tanto, nada se pushea a `main`** (solo commits locales); el push llega con la aprobación del Spec y del plan.

## Identificación y estado

- Tema: llevar a la app la interfaz del artefacto «Matriz de permisos» para que administrador y jefe de proyectos cambien quién ve cada pantalla y quién ejecuta cada acción, sin desplegar.
- Fecha: 2026-09-30.
- Estado: **Propuesta** (Spec redactado, decisiones D1 a D7 resueltas por Victor el 2026-09-30; pendiente de Gate Spec).
- Orquestador: Claude (sesión de 2026-09-30). Planner, Worker y Auditor: por asignar.

## Spec / SDD

### Estado

`Propuesto`.

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
6. La pantalla replica el artefacto y se somete a él: al entrar en producción, el Spec fija si la pantalla **reemplaza** al artefacto como instrumento de edición y qué documento queda como referencia (ver decisión D4).

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

- La pantalla replica el artefacto (dos tablas con scroll horizontal, columnas de roles, columna «Fila» y «Comentario», contorno de cambio, aprobación), según `docs/05-diseno-y-referencias/design.md`; no se crea un estilo nuevo.
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

- [ ] Victor aprueba este Spec.

## Entorno, repositorios, ramas y worktrees

- Entorno: **local** (verificado: la app es accesible en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`).
- Documentación: `pg_control_proyectos`, `main`, directo.
- Código: `py_control_proyectos_web`, rama `local-worker-1` (existe en el mismo commit que `main`, `45c9e0a`, ya mergeada). **Se reutiliza solo con autorización de Victor**; nada se crea ni se mueve sin ella.
- **Espera a propósito:** no se asigna Worker hasta que el grupo de paquetes pushee; la rama puede cambiar de base en ese momento.
- Skills del repositorio de documentación que aplican: `verificar-permisos-por-rol` (toda tanda que toque permisos), `cerrar-tanda` (al final de cada tanda), `seguir-flujo-de-planes` (Orquestador). El repositorio de código no tiene Skills.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-09-30 | Objetivo confirmado: que administrador y jefe de proyectos cambien desde la app quién ve y ejecuta qué, sin desplegar; no cambian el alcance por OT, la validación en servidor ni las reglas de las tablas del flujo 14. | Victor |
| 2026-09-30 | Se llega hasta tener el plan; luego se espera a que el grupo de paquetes termine y pushee, se revisa este plan y se continúa. | Victor |
| 2026-09-30 | Decisiones D1 a D7 del Spec resueltas (ver tabla «Decisiones de Victor»). Artefacto verificado: versión 42, 49 acciones y 15 interfaces, cero diferencias con el flujo 14; marca «Aprobada» quitada, pendiente de Victor. | Victor / Orquestador |
| 2026-09-30 | Orquestador y Planner comitean cada vez que terminan algo, sin excederse; el push a `main` se habilita con la aprobación del Spec y del plan. | Victor |

## Mejoras (de trabajo)

Ninguna.

## Reglas de negocio acordadas en esta tarea

Ninguna todavía (la regla propuesta arriba espera el Gate Spec).

## Carpetas/archivos huérfanos

Ninguno.
