# Planes futuros

> Renombrado desde `tareas-futuras.md` (antes en `docs/Tareas de implementacion/`) durante la reestructuración documental de 2026-09-27, adaptado al formato de `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md` § Convención de planes futuros (§2.5 del plan de reestructuración). Es el último archivo fijo de `01-planes/`.

Archivo permanente — no es un plan aprobado: no tiene progreso, evidencia ni Worker asignado, y debe pasar por Spec/SDD antes de convertirse en plan real:

```text
planes-futuros.md → Spec/SDD → plan aprobado (Gate 1) → progreso y evidencia
```

## Cómo se usa

- Solo se agrega algo aquí cuando **Victor lo indica explícitamente** como pendiente a futuro — no es donde el agente guarda por su cuenta algo que no alcanzó a hacer.
- Cada ítem anota: origen, descripción, motivo de la postergación, estado y si requiere Spec/SDD antes de retomarse.
- Cuando Victor decide retomarlo, se saca de aquí y se convierte en un plan nuevo en `01-planes/` con la fecha del día en que se retoma. El ítem se conserva acá como "promovido", con enlace al plan nuevo — no se borra sin trazabilidad.

## Pendientes a futuro

### Paquetes de trabajo como filtro operativo (Plan Maestro / flujo 20)

- **Origen:** `docs/Tareas de implementacion/2026-09-20-control-avance-plan-maestro.md` (Pendiente Fase 2 del flujo 20-plan-maestro).
- **Qué es:** paquetes de trabajo, área, disciplina y frente como filtros operativos del Plan Maestro, sin reemplazar las partidas DP.
- **Pospuesto:** 2026-09-20.
- **Estado:** pendiente, sin promover.
- **Requiere Spec/SDD:** sí, antes de convertirse en plan.

### 3WLA como plan operativo separado

- **Origen:** `docs/Tareas de implementacion/2026-09-20-control-avance-plan-maestro.md` (Pendiente Fase 2 del flujo 20-plan-maestro).
- **Qué es:** construir el 3WLA/Plan semanal como interfaz propia (compromisos, restricciones, condiciones de satisfacción, cumplido/no cumplido, causa, PPC/CNC), según lo describe `18-control-avance.md`.
- **Por qué se pospone:** el objetivo actual del flujo 18 es la cadena de datos RDT validado → PR → Dashboard (métricas EVM: EV, AC, SPI, CPI). El 3WLA no alimenta esa cadena — mide PPC (LPS), un indicador aparte que `18-control-avance.md` marca explícitamente que no debe mezclarse con SPI. No es indispensable para que el dato de RDT llegue al Dashboard.
- **Pospuesto:** 2026-09-20.
- **Estado:** pendiente, sin promover.
- **Requiere Spec/SDD:** sí.

### Apartado "Inasistencias" al final del RDT

- **Origen:** pedido directo de Victor, 2026-09-20 (sesión de trabajo del sub-lote de RDT rechazo/historial).
- **Qué es:** un apartado nuevo al final del RDT (Crear RDTs), listado tipo desplegable con: personal (elegido del catálogo `recursos_personal`, igual que el Tareo), motivo de inasistencia, y lo que haga falta — diseño y campos exactos quedan a criterio de quien lo retome (Victor lo dejó abierto explícitamente).
- **Ojo — confirmar antes de construir:** Victor escribió "RDO", pero toda la sesión fue sobre **RDT** (Crear RDTs, PROM-GP-002) — "RDO" en este repo históricamente se refiere a otro formato distinto (reporte con fotos/personal de cantera, `Informacion para pruebas/RDO`). Antes de implementar, confirmar si es el RDT (más probable, por contexto) o si de verdad es el flujo RDO aparte.
- **Pospuesto:** 2026-09-20.
- **Estado:** pendiente, sin promover.
- **Requiere Spec/SDD:** sí — incluye una ambigüedad a resolver con Victor antes de planificar.

### Gestión de permisos y accesos desde la app (matriz editable)

- **Origen:** pedido directo de Victor, 2026-09-28. Relacionado con "Gestión visual de accesos" del flujo 14 (pedido del 2026-09-20).
- **Qué es:** llevar a la app web la misma interfaz del artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT): las dos tablas (interfaces con y sin datos económicos; acciones), una casilla por rol, comentarios y aprobación. Solo para administrador y jefe de proyectos, con su chip y demás accesos en el apartado OT y dentro del sistema de paneles (registro único de accesos). Permite cambiar accesos y permisos con la app en producción, sin desplegar.
- **Sujeción obligatoria:** este plan se somete al artefacto y al flujo 14. Su Spec cita el artefacto como base. Mientras la pantalla no exista, toda interfaz, acción, permiso o acceso nuevo actualiza el artefacto y el flujo 14 (política de coherencia y trazabilidad, `docs/01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md`). Al implementarse, el Spec define si la pantalla reemplaza al artefacto como instrumento de edición y qué documento queda como referencia.
- **Lo que debe definir su Spec:** dónde se guardan los permisos (hoy están fijos en `permisos.ts`), la validación en servidor de cada cambio, el registro de quién cambió qué y cuándo, y cómo convive con el alcance por OT.
- **Depende de:** el plan `2026-09-27-paneles-servicio-persistente` (registro único de accesos) y del Spec de economía (siguiente punto).
- **Pospuesto:** 2026-09-28.
- **Estado:** pendiente, sin promover.
- **Requiere Spec/SDD:** sí.

### Dashboard Parcial sin datos económicos y restricción económica definitiva

- **Origen:** pedido directo de Victor, 2026-09-28 (durante el plan `2026-09-27-paneles-servicio-persistente`). La tabla base de visibilidad por rol ya está en el flujo 14.
- **Qué es:** (1) el Dashboard **Parcial sin datos económicos** y el **Completo con ellos** (hoy los dos muestran BAC, PV, EV, AC, CPI y EAC en USD; solo difieren en PPC/Pareto CNC y el enlace a Curva S, flujo 11); (2) cuando exista el Parcial sin economía, moverlo a la sección "sin datos económicos" de la matriz del flujo 14; (3) resolver los conflictos operativos que la regla de "4 roles con economía" deja abiertos (planner y Plan Maestro; supervisor de oficina técnica y DP; supervisor de logística y Registro de costos; jefe de costos; acciones destructivas del jefe de proyectos), listados al final de la sección nueva del flujo 14.
- **Por qué se pospone:** es una configuración distinta de los paneles; Victor pidió que sea otro Spec.
- **Pospuesto:** 2026-09-28.
- **Estado:** pendiente, sin promover.
- **Requiere Spec/SDD:** sí.

### Cronograma como línea base y línea real de avance (Gantt)

- **Origen:** pedido directo de Victor, 2026-09-30 (durante el Spec `2026-09-30-paquetes-y-plan-maestro-grilla`). Ya figuraba como "fase 2, no construida" en el flujo 15.
- **Qué es:** el cronograma que se entrega al cliente como base debe devolverse con dos líneas: la **línea base** (las fechas del archivo cargado, fijas) y la **línea real de avance físico** (editable: puede quedar antes, después, más corta o más larga que la base). Su función es seguir el avance físico del servicio.
- **Dato que lo sostiene:** el vínculo actividad ↔ partida con metrado (`cronograma_actividad_partidas.metrado`, `db/071`), que el Spec del 30-sep mueve a la pantalla de Paquetes de Trabajo. Por eso ese dato no se descarta: el avance de una actividad saldría del avance de sus partidas. El flujo 15 lista además como pendientes el candado de checklist "Cronograma" y restringir el reemplazo mientras el servicio siga "En Planeación".
- **Por qué se pospone:** Victor lo declaró "otro tema, aún no implementado"; primero se resuelve Paquetes de Trabajo y Plan Maestro.
- **Pospuesto:** 2026-09-30.
- **Estado:** pendiente, sin promover.
- **Requiere Spec/SDD:** sí.

### Acceso directo a Postgres/Supabase para correr SQL

- **Origen:** decisión pendiente registrada el 2026-09-17 (antes en `docs/memoria-sesion.md`, ya retirado).
- **Qué es:** hoy Claude solo tiene las llaves REST de Supabase (leer/escribir filas de tablas existentes), no la cadena de conexión directa de Postgres — por eso Victor sigue pegando y corriendo el SQL él mismo en el SQL Editor de Supabase. Si se agrega la cadena de conexión directa (Project Settings → Database → Connection string), Claude podría correr migraciones (`CREATE TABLE`, etc.) directamente. **La regla general sigue siendo: aun con esa llave, se confirma con Victor antes de correr cada migración — es un cambio difícil de deshacer.**
- **Pospuesto:** 2026-09-20.
- **Estado:** pendiente, sin promover.
- **Requiere Spec/SDD:** sí, dado que implica manejo de credenciales e infraestructura.

**Excepción puntual (2026-09-21):** para el plan de PR enriquecido en dos fases ([Fase 1](2026-09-21-pr-fase-1-pipeline-rdt.md), [Fase 2](2026-09-21-pr-fase-2-pipeline-linea-base.md)), Victor autorizó explícitamente dar la cadena de conexión directa a los dos agentes que trabajan en la nube, para que corran sus propias migraciones (`053`+ y `060`+) sin pausar a pedir confirmación una por una. **Es una excepción acotada a esos dos agentes y a esa tarea, no un cambio de la regla general** — cualquier otra sesión (incluida esta) sigue sin esa cadena de conexión y sigue confirmando cada migración con Victor.

Herramientas de Claude Code no tienen forma de inyectar esa credencial en el sandbox de un agente en la nube (el tool de lanzar agentes no acepta variables de entorno ni secretos) — Victor tiene que configurarla él mismo del lado de la plataforma, en la sección de entornos/secretos del sandbox para ese repositorio. Nunca se pega en un chat.

> **Nota de la reestructuración (2026-09-27):** los dos enlaces de "Fase 1"/"Fase 2" de arriba apuntan todavía a `docs/Tareas de implementacion/` porque esas tareas se migran recién en la Fase 7 de `2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md`. Cuando esa fase las mueva a `01-planes/`, estos enlaces se corrigen en el mismo commit (pasan a ser archivos hermanos, sin prefijo de carpeta).
