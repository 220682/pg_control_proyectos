# Paneles: servicio persistente y panel izquierdo completo

## Identificación y estado

- Tema: paneles con servicio persistente y panel izquierdo completo (flujo 16).
- Fecha: 2026-09-27.
- Estado: `Propuesta` — Spec/SDD redactado, pendiente del Gate Spec.
- Entorno: `local` (verificado: sesión de Claude Code en la máquina de Victor, Windows).
- Chat del Orquestador sugerido: `local_1.orquestador_paneles-servicio-persistente` (Victor lo renombra; el agente no tiene herramienta para hacerlo).

---

# Spec/SDD

## Estado

`Propuesto`.

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
6. **Deseable (opcional según Victor):** al hacer clic en un chip del panel derecho estando dentro de un servicio, la pantalla destino abre con ese servicio ya elegido en su selector de OT.

## Alcance

- Conservar el servicio en la URL en todas las pantallas del workspace y hacer que el shell lo reconozca (`WorkspaceShell.tsx`).
- Completar el panel izquierdo con servicio según el resultado esperado 2–5.
- Añadir botón mostrar/ocultar a Recursos de empresa; quitar Materiales de esa sección.
- Que las pantallas de RDTs, Requerimientos, Consolidado RQ y las que hoy no leen el servicio lo reciban por `?proyectoId=` y lo preseleccionen.
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

1. Estado por defecto del botón mostrar/ocultar de Recursos de empresa. Recomendación: visible sin servicio, oculto con servicio.
2. Dónde quedan PR, Dashboard y Curva S (hoy en el panel izquierdo, no listados en el flujo 16). Recomendación: sección "Reportes".
3. Si los chips del panel **derecho** también pasan a "visible y deshabilitado" para lo no autorizado, o se mantienen como hoy.
4. Qué pasa con el chip "Salir a Mi entorno" de las pantallas a pantalla completa, ahora que los paneles permanecen activos en toda pantalla.
5. Destino de "(OT) Orden de trabajo" y "Recursos hh, hm, mat. (s/c)": la app tiene pantallas candidatas (`/proyectos/[id]`, `/proyectos/[id]/editar`, `/recursos/*`) y no se asumió cuál corresponde.
6. Dónde ubicar Registro de costos, Editar servicio y Editar checklist.

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
- [ ] Desde el panel derecho, dentro de un servicio, las pantallas destino abren con el servicio preseleccionado (si Victor confirma el punto opcional).
- [ ] Navegación móvil y tablas con scroll horizontal se conservan.
- [ ] Los flujos 16, 01, 14 (y 03/05/06 si aplica) quedan actualizados y coherentes con lo implementado.

## Estrategia de prueba / evidencia

Ciclo del protocolo de verificación aprobado por Victor: **checklist aprobado antes de implementar** → implementación → autoverificación del Worker con Playwright en la app real con login real → llenar el checklist → loop hasta 100% Completado → recién entonces revisión de Victor. Cada permiso se prueba **por los dos lados** con las dos cuentas de prueba (una con permisos altos y una sin permisos de administración); un permiso comprobado solo con administrador no está comprobado. Las credenciales viven fuera del repositorio y no se copian a ningún archivo. Evidencia en `02-trabajo-activo/03-evidencia/` con enlace al artifact de checklist visual si se crea.

## Aprobación (Gate Spec)

- [ ] El Responsable humano aprueba este Spec/SDD.

---

# Plan

## Referencia al Spec aprobado

Pendiente del Gate Spec.

## Objetivo, alcance y no alcance

Ver Spec/SDD arriba.

## Entorno, repositorios, ramas y worktrees

- Documentación: `pg_control_proyectos`, `main` directo.
- Código: `py_control_proyectos_web`, rama `local-worker-N` (por verificar contra `git branch -a` / `git worktree list` de ese repositorio antes de asignar), nunca `main` hasta el Gate 2. El repositorio de la app es accesible desde esta máquina en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` (verificado 2026-09-27).

## Fases y dependencias

Pendiente — lo redacta el Planner tras el Gate Spec.

## Asignación de roles

| Rol | Chat | Rama | Worktree | Estado |
|---|---|---|---|---|
| Orquestador | `local_1.orquestador_paneles-servicio-persistente` (por renombrar) | `main` | N/A | Activo |
| Planner | pendiente | `main` | N/A | Pendiente del Gate Spec |
| Worker (fase 1) | pendiente | pendiente | pendiente | Pendiente |
| Auditor | pendiente | `main` | N/A | Pendiente |

## Archivos / componentes afectados

Ver Spec/SDD (lista previsible). El Planner fija la definitiva.

## Punch List embebida

Pendiente — la redacta el Planner; Victor la aprueba en el Gate 1 antes de implementar.

## Riesgos y bloqueos

Ver Spec/SDD.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-09-27 | El servicio seleccionado se conserva entre pantallas mediante `?proyectoId=` en la URL. | Victor |
| 2026-09-27 | El panel izquierdo con servicio lo ven todos los roles; los chips sin permiso se muestran deshabilitados (visibles, no accesibles), igual que en Mi entorno. Contradice el flujo 16 (reglas 2 y 3), el flujo 01 (Apartado Proyectos solo admin/JP) y la fila del flujo 14. Los flujos se editan al cierre, no antes. | Victor |
| 2026-09-27 | Los recursos de empresa no se reemplazan por los del servicio al abrir uno: llevan un botón mostrar/ocultar, con o sin servicio. | Victor |
| 2026-09-27 | "Materiales" se elimina de Recursos de empresa (no es un recurso de empresa). | Victor |
| 2026-09-27 | Deseable/opcional: los chips del panel derecho abren la pantalla destino con el servicio ya elegido en el selector de OT. | Victor |
| 2026-09-27 | Un chip cuya pantalla no existe puede seguir inerte; uno cuya pantalla ya existe debe funcionar. | Victor |

## Enlaces a progreso y evidencia homónimos

Se crean al pasar el Gate 1 (`02-progreso/` y `03-evidencia/` con este mismo nombre de archivo).

## Mejoras (de trabajo)

- `03-entorno-git-y-worktrees.md` (§ "Pool real de ramas y worktrees") afirma que este repositorio no tiene acceso directo a `py_control_proyectos_web`. Es inexacto: el repositorio de la app está en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`, accesible desde una sesión local, y se pueden correr `git`, el servidor de desarrollo y Playwright sobre él (verificado 2026-09-27). Corregir al cierre.
- Cuando se hacen varias llamadas de Playwright en paralelo sobre el mismo navegador, las navegaciones se pisan. Encadenar una a una.

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
