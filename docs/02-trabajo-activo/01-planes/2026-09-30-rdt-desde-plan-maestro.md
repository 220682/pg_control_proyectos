# 2026-09-30 — RDT desde el Plan Maestro (el RDT lista paquetes y partidas del Plan Maestro)

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Este archivo contiene el Spec (paso 3). **Es el tercero de tres Specs hermanos que se aprueban juntos y que un solo plan reparte entre Workers** (decisión de Victor, 2026-09-30): `2026-09-30-niveles-presupuesto-y-cronograma.md`, `2026-09-30-paquetes-y-plan-maestro-grilla.md` y este.

## Identificación y estado

- Tema: el RDT deja de listar las partidas del DP y lista lo que está en el Plan Maestro.
- Fecha: 2026-09-30.
- Estado: **Planificando** (Spec `Aprobado` en el Gate Spec del 2026-09-30; sigue la delegación al Planner).
- Continúa y absorbe: Fase 2 del plan `2026-09-23-paquetes-de-trabajo.md` (declaración de avance del paquete, PL-2.1 a PL-2.4).

## Spec / SDD

### Estado

`Aprobado (Gate Spec, 2026-09-30)`.

### Problema y contexto

Victor (2026-09-30): **el RDT lista las partidas y paquetes que están en el Plan Maestro, ya no las partidas del DP; si no, la trazabilidad y el objetivo no funcionarían.** Razón de fondo: una partida puede estar repartida entre paquetes, y el real solo se puede atribuir a cada paquete si el RDT declara contra el paquete. El PR sigue recibiendo el avance por partida única.

**Estado verificado en el código (`py_control_proyectos_web`, `main`, 2026-09-30):**

| Pieza | Lo que hace hoy | Dónde |
|---|---|---|
| Catálogo del RDT | Devuelve `dp_partidas` y `dp_subpresupuestos` del servicio; la pantalla agrupa por subpresupuesto con la convención del primer segmento del WBS. | `src/app/api/rdts/catalogos/route.ts`, `FormularioCrearRdt.tsx` (~326-485) |
| Cómo elige partida | Cada actividad elige una partida por WBS; eso rellena descripción, WBS y unidad y fija el tipo **D** (directa). Las actividades **C** y **NC** no tienen partida propia: eligen una partida a la que cargan sus horas (regla 12). Los materiales también llevan WBS. | `FormularioCrearRdt.tsx` |
| Vínculo oficial | `rdt_actividad_partidas (rdt_actividad_id, dp_partida_id)`; se registra al validar el RDT. `rdt_actividades.wbs` queda como referencia visual. | `db/040`, `src/app/api/rdts/partes/[id]/route.ts` |
| Quién lee el real | El Plan Maestro lee los RDT `VALIDADO` por ese vínculo y los agrega por partida; HH reales y costo real van en 0 como marcador. | `src/app/api/plan-maestro/route.ts` (GET), `src/lib/plan-maestro/plan-maestro.ts` |
| Regla escrita | Flujo 20: "el RDT debe usar un WBS existente en el DP del mismo servicio; al validarlo se registra el vínculo actividad RDT – partida DP". | `20-plan-maestro.md` |
| Antecedente | El plan del 23-sep describió (sin implementar) la declaración por paquete: modo A (se declara la unidad de la partida guía, el % se aplica a todas las partidas) y modo B (partida por partida). | `2026-09-23-paquetes-de-trabajo.md`, Fase 2 |

### Resultado esperado

1. **Crear RDT** lista, para elegir en cada actividad, los **paquetes y sus partidas** del Plan Maestro aprobado vigente del servicio, más las **partidas directas** (sin paquete), con la jerarquía según el mapa de niveles.
2. **Declaración del avance:**
   - En un paquete de modo "por partidas", el supervisor declara el metrado de cada partida.
   - En uno de modo "por avance del paquete", declara la unidad de la partida guía y el sistema aplica el mismo % a las demás partidas del paquete (Fase 2 del plan del 23-sep, ya definida por Victor).
3. Las actividades **C y NC** cargan sus horas a un paquete × partida del Plan Maestro (antes, a una partida del DP). Los materiales igual.
4. Al validar, el vínculo guarda la **partida y el paquete** con una clave que sobrevive a una versión nueva del Plan Maestro.
5. El Plan Maestro muestra el **real** (físico, EV y HH, acumulados por semana) por paquete × partida, junto a lo programado (lienzo de los otros Specs).
6. El PR sigue sumando el avance por partida única; no cambia su lógica.

### Alcance

- Catálogo del RDT desde el Plan Maestro aprobado; selector por paquete y partida; declaración modo A y modo B; carga de horas C/NC y materiales.
- Vínculo con el paquete (columna aditiva), validación en servidor de que el paquete y la partida pertenecen al Plan Maestro vigente del servicio.
- Conexión de HH reales por semana y paquete × partida para el lienzo (hoy en 0 como marcador); el Planner verifica de dónde salen en el consolidado de RDTs.
- Cambios en el consolidado de RDTs para poder ver el paquete.
- Documentación: flujos 06, 18 y 20.

### No alcance

- Niveles de importación, Paquetes y lienzo del Plan Maestro (Specs hermanos).
- HH ganadas (flujo 18); el PR no cambia su fórmula; 3WLA; Gantt.
- Cambiar quién crea o valida RDT (sin cambios de roles).

### Usuarios / roles afectados

- Crear RDT: los roles que hoy crean (supervisor operativo, administrador, jefe de proyectos, jefe de oficina técnica). Validar o rechazar: administrador, jefe de proyectos y jefe de oficina técnica; rechazar un RDT ya validado: administrador y jefe de proyectos (flujos 06 y 14 vigentes al 2026-09-30). Sin cambios de roles.
- Sin chip, pantalla ni acción nueva. Si el Auditor encuentra un cambio de acceso, se actualizan en la misma tarea el artefacto «Matriz de permisos» y el flujo 14.

### Reglas de negocio y documentos afectados

| Flujo | Dice hoy | Cambia a | Estado |
|---|---|---|---|
| 06 RDT | Elige partidas del DP agrupadas por subpresupuesto | Elige paquetes y partidas del Plan Maestro | **Pendiente de consulta** |
| 18 Control de avance | Avance por partida; método de medición configurado para paquetes | El real se declara contra paquete × partida; el PR suma por partida | **Pendiente de consulta** |
| 20 Plan Maestro | El RDT usa un WBS existente en el DP; vínculo RDT – partida DP | El RDT usa paquetes y partidas del Plan Maestro; vínculo con paquete | **Pendiente de consulta** |
| 10 PR, 21 Curva S | Suman el real por partida | Sin cambio esperado; el Planner verifica | Por verificar |

### Datos, API, migraciones o dependencias

Propuesta, sujeta al Planner (aplicar a mano en el SQL Editor; cada migración se confirma con Victor):

- `rdt_actividad_partidas`: columna nueva `paquete_trabajo_id` (nulo = partida directa); se conserva `dp_partida_id` para que el PR y la Curva S sigan funcionando.
- `GET /api/rdts/catalogos`: devuelve las líneas del Plan Maestro aprobado con su paquete (y el mapa de niveles para agrupar) en vez de `dp_partidas`/`dp_subpresupuestos`.
- API de partes y de validación: verificar en servidor que el paquete y la partida estén en el Plan Maestro aprobado vigente.
- Dependencias: Spec de Paquetes y Plan Maestro (modelo de líneas y claves estables) y Spec de Niveles (jerarquía del selector).
- **Servicios existentes:** todos son de prueba (Victor); sin compatibilidad hacia atrás. PS-0006 ya no existe: se eliminó en la limpieza de datos de prueba del plan de paneles, autorizada por Victor (quedan PS-0004 y PS-0005). Todos los servicios existentes son de prueba y se pueden tocar. Victor autorizó crear un servicio de prueba dedicado para la verificación de este plan (con DP, cronograma y RDT propios).

### Diseño / UI aplicable

- Pantallas: Crear RDT (`/rdts/crear`) y Status de RDTs (`/rdts/status`, donde se valida). El selector de actividad del RDT agrupa por paquete (plegable) y muestra las partidas directas aparte; respeta el formato actual de desplegable con texto cortado (pedido de Victor del 13-sep) y `design.md`.
- Un paquete "por avance del paquete" muestra la unidad de la guía y calcula el % que se aplica al resto, en solo lectura.

### Riesgos y decisiones pendientes

**Decisiones que Victor debe confirmar en el Gate Spec:**

- **R1.** Sin Plan Maestro aprobado, no se puede crear RDT (coherente con el flujo 20, que ya impide pasar a ejecución sin él). El mensaje lo indica. Propuesta: sí.
- **R2.** Las actividades **C y NC** eligen el paquete × partida al que cargan sus horas. Con una partida repartida entre paquetes, el supervisor debe elegir a cuál. Propuesta: sí, mismo selector.
- **R3.** Los materiales usan el mismo selector. Propuesta: sí.
- **R4.** Cuando el Plan Maestro tiene una versión nueva en la que un paquete cambió o desapareció, los RDT ya validados conservan el paquete con el que se validaron (nombre copiado). En el lienzo, el real de un paquete que ya no existe aparece en una fila "real de versión anterior". Propuesta: sí.
- **R5.** ¿Un RDT ya registrado pero no validado se puede reasignar a otro paquete? Propuesta: sí, mientras esté en `REGISTRADO` o `REVISADO`; no cuando esté `VALIDADO`.
- **R6.** Modo "por avance del paquete": ¿el supervisor puede corregir a mano el metrado calculado de una partida, o es solo lectura? Propuesta: solo lectura (el modo dice "mismo %"); si necesita otra cosa, el paquete debe ser de modo "por partidas".

**Riesgos:** el RDT de campo es la pantalla más usada y hoy funciona; la migración agrega columnas sin tocar las existentes; HH reales por semana no existen conectadas.

### Criterios de aceptación

1. En un servicio con Plan Maestro aprobado, Crear RDT lista los paquetes y partidas del Plan Maestro, agrupados, más las partidas directas; no lista el DP.
2. Una partida repartida entre dos paquetes aparece en ambos; el supervisor elige en cuál declara.
3. En un paquete "por avance del paquete", declarar la unidad de la guía calcula el % y lo aplica a las demás partidas.
4. Las actividades C/NC y los materiales cargan a un paquete × partida.
5. Al validar, el vínculo guarda partida y paquete; el PR muestra la partida una sola vez con la suma del avance.
6. El lienzo del Plan Maestro muestra el real por paquete × partida (físico, EV y HH, acumulados).
7. Crear una versión nueva del Plan Maestro no deja RDT validados sin paquete.
8. Sin Plan Maestro aprobado, el RDT no se puede crear y el mensaje lo explica.
9. Flujos 06, 18 y 20 coherentes con lo implementado; el Auditor verifica la trazabilidad antes del Gate 2.

### Estrategia de prueba / evidencia

- Lógica pura con vitest: reparto del % del paquete a sus partidas, suma por partida, atribución con partida repartida, clave estable entre versiones.
- `tsc --noEmit`, suite completa, lint comparado contra `main`.
- Verificación en vivo con Playwright y login real sobre el servicio de prueba dedicado de este plan (servicio nuevo creado para este plan): crear RDT listando el Plan Maestro, validar, ver el real en el lienzo y en el PR; una captura por ítem.

### Aprobación (Gate Spec)

- [x] Victor aprueba este Spec, incluidas R1 a R6 y la consulta de cada contradicción de la tabla de flujos.

## Entorno, repositorios, ramas y worktrees

Ver la sección "Ejecución conjunta" de `2026-09-30-paquetes-y-plan-maestro-grilla.md` (hasta 4 Workers, rama y worktree por Worker con autorización de Victor, archivos de choque y rangos de migraciones). Este Spec corresponde al Worker D del reparto orientativo y depende de los datos de los otros tres.

## Asignación de roles

| Rol | Chat | Rama | Worktree | Estado |
|---|---|---|---|---|
| Orquestador | por nombrar | `main` | N/A | Activo |
| Planner | tras el Gate Spec (un solo plan para los tres Specs) | `main` | N/A | Pendiente |
| Worker | tras el Gate 1 | por confirmar | por confirmar | Pendiente |
| Auditor | por asignar | `main` | N/A | Pendiente |

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-09-30 | **Gate Spec: Victor aprobó los tres Specs ("todo aprobado")**, con las recomendaciones del Orquestador para todas las decisiones pendientes. Queda abierto, sin bloquear: el nombre del rol extra cuando un archivo trae más de 5 niveles (D6). El texto exacto de cada flujo contradicho se le muestra antes de editarlo. | Victor |
| 2026-09-30 | El RDT lista los paquetes y partidas del Plan Maestro, no las del DP; sin eso no funciona la trazabilidad. | Victor |
| 2026-09-30 | El RDT va en su propio Spec; los tres Specs se aprueban juntos y un solo plan los reparte. | Victor |
| 2026-09-30 | Los servicios existentes son de prueba: sin compatibilidad hacia atrás, PS-0006 ya no existe (eliminado en la limpieza del plan de paneles). Se autoriza crear un servicio de prueba dedicado para este plan. | Victor |

## Enlaces a progreso y evidencia homónimos

- Progreso y evidencia: se crean al iniciar la implementación (`02-progreso/` y `03-evidencia/`, mismo nombre de archivo).

## Mejoras (de trabajo)

Ninguna todavía.

## Reglas de negocio acordadas en esta tarea

Se trasladan a su flujo al cerrar, previa consulta de cada contradicción a Victor.

- 2026-09-30 — El RDT lista los paquetes y partidas del Plan Maestro; el real se atribuye al paquete × partida; el PR suma por partida → `06-rdt.md`, `18-control-avance.md`, `20-plan-maestro.md` (pendiente).

## Carpetas/archivos huérfanos

Ninguno detectado hasta ahora.

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

Ninguno todavía.
