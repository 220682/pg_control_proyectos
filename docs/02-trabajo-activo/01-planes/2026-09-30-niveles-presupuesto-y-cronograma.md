# 2026-09-30 — Niveles del presupuesto y del cronograma (mapa de niveles al importar)

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Este archivo contiene el Spec (paso 3). **Se ejecuta primero**: Victor decidió (2026-09-30) que los niveles se arreglan antes de Paquetes de Trabajo y Plan Maestro (ver `2026-09-30-paquetes-y-plan-maestro-grilla.md`).

## Identificación y estado

- Tema: el sistema debe entender cuántos niveles tiene cada presupuesto (DP) y cada cronograma, y qué es cada nivel.
- Fecha: 2026-09-30.
- Estado: **Planificando** (Spec `Aprobado` en el Gate Spec del 2026-09-30; sigue la delegación al Planner).

## Spec / SDD

### Estado

`Aprobado (Gate Spec, 2026-09-30)`.

### Problema y contexto

Victor explicó (2026-09-30): ningún presupuesto ni cronograma tiene los mismos niveles. El **último nivel** es siempre la partida, que es donde están los datos (metrado, unidad, precio, fechas). Antes de ella puede haber un grupo de partidas, un subpresupuesto, un área (cuando un servicio exige un quinto nivel, el nivel 2 queda sin nombre) y arriba el servicio. Al importar, hoy no todas las filas se exponen.

Ejemplos de Victor:

```text
4 niveles:  1 Servicio · 2 Subpresupuesto · 3 Paquete de partidas · 4 Partida
5 niveles:  1 Servicio · 2 Área (sin nombre fijo) · 3 Subpresupuesto · 4 Paquete de partidas · 5 Partida
```

**Estado verificado en el código (`py_control_proyectos_web`, `main`, 2026-09-30):**

| Pieza | Lo que hace hoy | Dónde |
|---|---|---|
| Niveles del DP | Fijos en dos encabezados. Subpresupuesto = código de **1 segmento** (`/^\d+$/`); paquete de partidas = código de **2 segmentos** (`/^\d+\.\d+$/`). Una partida es la fila con WBS y metrado numérico. Un presupuesto con 5 niveles, o con el área en el nivel 2, queda mal leído: los encabezados que no calzan en esos dos patrones se descartan. | `src/lib/dp/parser-cd.ts` (líneas ~130-148), `parser.ts`, `tipos.ts` |
| Dónde se guardan | `dp_subpresupuestos` (`db/031`) y `dp_paquetes` (`db/034`, "paquete de partidas"). Sin FK: la partida pertenece al subpresupuesto por el primer segmento de su WBS, y al paquete por los dos primeros. `reemplazar_dp` los borra y reinserta. | `db/031`, `db/034`, `db/060` |
| Quién usa la convención | Pantallas DP y PR, filtros de Crear RDT y Consolidado RDTs, enlace del cronograma, API de catálogos de RDT. | `subpresupuestos.ts` y sus consumidores (una búsqueda de "subpresupuesto" da 17 archivos bajo `src/`, incluidas pruebas; el Planner los inventaría) |
| Niveles del cronograma | No se guardan. `tipo` = `HITO` si la duración es 0; `RESUMEN` si otro EDT empieza con `"<edt>."`; si no, `TAREA`. El informe enlaza cada actividad con el DP comparando su EDT contra códigos de partida, subpresupuesto o paquete. | `src/lib/cronograma/parser-excel.ts` (líneas ~104-127), `informe.ts`, `db/036` |
| Nombre "paquete" | El DP ya llama "paquete de partidas" a un nivel y la pantalla de Crear RDT lo muestra así. No es el Paquete de Trabajo. | `db/034`, `FormularioCrearRdt.tsx` |

### Modelo de niveles

**El número de un nivel no es su rol.** El archivo trae N niveles numerados; cada uno recibe un rol. Los roles tienen un orden fijo, de mayor a menor:

```text
Servicio  >  Área  >  Subpresupuesto  >  Paquete de partidas  >  Partida
obligatorio  opcional   opcional            opcional             obligatorio (siempre el último nivel)
```

La **Partida** es siempre el último nivel: es donde están los datos (metrado, unidad, precio, fechas). El **Servicio** es siempre el primero. Área, Subpresupuesto y Paquete de partidas aparecen solo si el archivo los tiene. Combinaciones por defecto que el sistema propone según los niveles encontrados (el usuario puede cambiarlas por fila con el desplegable):

| Niveles encontrados | Nivel 1 | Nivel 2 | Nivel 3 | Nivel 4 | Nivel 5 |
|---|---|---|---|---|---|
| 2 | Servicio | Partida | | | |
| 3 | Servicio | Subpresupuesto | Partida | | |
| 4 | Servicio | Subpresupuesto | Paquete de partidas | Partida | |
| 5 | Servicio | **Área** | Subpresupuesto | Paquete de partidas | Partida |

En el caso de 5 niveles, el nivel extra se inserta en el **nivel 2** (el que "queda sin nombre", en palabras de Victor) y se le propone "Área". **Más de 5 niveles** o combinaciones distintas (por ejemplo 4 niveles con Área y sin Paquete de partidas) se resuelven con el mismo desplegable; el nombre del rol extra queda pendiente (D6).

Esto aplica al **DP** y, con roles propios pendientes (D2), al **cronograma**. Cada uno guarda su propio mapa, porque un presupuesto y un cronograma del mismo servicio pueden tener niveles distintos.

### Resultado esperado

1. Al importar un DP o un cronograma, el sistema **cuenta los niveles** que encontró y muestra el presupuesto (o cronograma) en orden, con lo que aparece en cada nivel.
2. Cada nivel recibe un **rol** elegido en un desplegable: Servicio, Área, Subpresupuesto, Paquete de partidas o Partida. El sistema propone un rol por defecto (por ejemplo, el nivel 1 cuyo nombre coincide con el del servicio es Servicio) y el usuario solo aprueba o corrige.
3. Para no revisar cada fila, el sistema muestra **una fila de muestra por grupo de hermanas**: lo que se elige para esa fila vale para las demás del mismo nivel y del mismo padre. Las filas que no siguen el patrón quedan marcadas "para revisar".
4. El **mapa de niveles** se guarda por servicio (uno para el DP y uno para el cronograma) y reemplaza la convención de "primer segmento del WBS". DP, PR, RDT, Consolidado RDTs y el enlace del cronograma leen de ahí.
5. Funciona con cualquier número de niveles, no solo 4 ni 5.

### Alcance

- Detección de niveles y pantalla de confirmación en la importación del DP (flujo 09) y del cronograma (flujo 15).
- Guardado del mapa de niveles y de las filas de encabezado con su rol, y migración de lo ya importado (los servicios existentes quedan con un mapa por defecto equivalente a la convención actual).
- Adaptar los consumidores de `subpresupuestos.ts` y de `dp_paquetes` al mapa nuevo.
- Reimportar (`reemplazar_dp`, reemplazo del cronograma) reconstruye el mapa y conserva las confirmaciones por código cuando siguen existiendo.
- Documentación: flujos 09, 15, 10 y los que usen subpresupuesto o paquete de partidas.

### No alcance

- Paquetes de Trabajo, Plan Maestro y Gantt (otros planes).
- Cambiar cómo se calculan costos, HH o EVM.
- Resolver automáticamente hallazgos del agente de validación del DP (flujo 09, pendiente aparte).

### Usuarios / roles afectados

- Quién confirma el mapa al importar: quien ya puede importar el DP (administrador y jefe de proyectos, sobre un servicio a su cargo, flujo 09 vigente) y quien ya puede subir el cronograma (administrador, jefe de proyectos y planner, flujo 15 vigente).
- Sin chip ni pantalla nuevos: es un paso dentro de la importación. Si el Auditor encuentra una acción o un acceso nuevo, se actualizan en la misma tarea el artefacto «Matriz de permisos» y el flujo 14.

### Reglas de negocio y documentos afectados

| Flujo | Dice hoy | Cambia a | Estado |
|---|---|---|---|
| 09 Importar DP | Subpresupuesto y paquete de partidas por patrón de código | Niveles detectados y roles confirmados por el usuario | **Pendiente de consulta a Victor** |
| 15 Cronograma | `RESUMEN`/`TAREA`/`HITO` por prefijo y duración; enlace por EDT | Niveles y roles propios del cronograma | **Pendiente de consulta a Victor** |
| 10 PR, 11 Dashboard, 06 RDT | Agrupan por subpresupuesto y por paquete de partidas | Agrupan por el mapa de niveles | Por verificar (el Planner revisa los 21 flujos) |

### Datos, API, migraciones o dependencias

Propuesta, sujeta al Planner (todo aditivo; nada se borra sin autorización):

- Tabla de niveles por servicio y origen (`DP` o `CRONOGRAMA`): número de nivel, rol.
- Tabla de encabezados con código, nombre, nivel y rol (generaliza `dp_subpresupuestos` y `dp_paquetes`, que se mantienen pobladas hasta migrar todos los consumidores).
- `reemplazar_dp` y la carga de cronograma reconstruyen el mapa.
- Dependencia: `db/031`, `034`, `036`, `060`, `071`. La migración hay que aplicarla a mano en el SQL Editor; se confirma con Victor antes de correr cada una.
- Pruebas con archivos reales de `docs/06-material-de-apoyo/Informacion para pruebas/` (presupuestos de 4 y 5 niveles, cronogramas exportados de MS Project).

### Diseño / UI aplicable

- Paso nuevo entre "archivo leído" e "informe de extracción": encabezado con el número de niveles encontrados; lista del presupuesto en orden con un desplegable de rol por fila de muestra; botón para aprobar.
- Respeta `docs/05-diseno-y-referencias/design.md` y el flujo 16.

### Riesgos y decisiones pendientes

**Decisiones que Victor debe confirmar en el Gate Spec:**

- **D1.** Nombres de los roles: "Área" y "Paquete de partidas" (este último es el que ya muestra la app y el que Victor usó; se propone conservarlo, distinto de "Paquete de trabajo"). Alternativa: "Grupo de partidas".
- **D2.** Roles del cronograma (Victor no los definió): propuesta Servicio, Área, Fase, Actividad resumen y Tarea; las hojas con duración 0 siguen siendo hito.
- **D3.** ¿Se puede corregir el mapa después de importar, y quién? (propuesta: administrador y jefe de proyectos).
- **D4.** ¿Se puede terminar de importar sin confirmar el mapa? (propuesta: sí, queda el mapa por defecto marcado "pendiente de confirmar").
- **D5.** Cuando el WBS no usa puntos (por ejemplo códigos de ancho fijo), la profundidad se toma por la estructura de la hoja. A verificar con archivos reales antes de fijar el detector.
- **D6.** Con más de 5 niveles, ¿cómo se llama el rol extra? Y si el archivo del cronograma no trae una fila de servicio, el nivel Servicio es implícito (el servicio seleccionado): propuesta, a confirmar.
- **D7 (definida por Victor en el plan hermano).** Si ya existe un Plan Maestro aprobado, no se puede volver a cargar un DP ni un cronograma (restricción); el borrador no restringe. Sin Plan Maestro aprobado, la recarga se bloquea, se avisa qué se perdería y solo después de una confirmación explícita se permite. Aplica también a la reimportación de este plan.

**Servicios existentes (Victor, 2026-09-30):** todos son de prueba, así que no se exige compatibilidad hacia atrás con ellos. PS-0006 ya no existe: se eliminó en la limpieza de datos de prueba del plan de paneles, autorizada por Victor (quedan PS-0004 y PS-0005). Todos los servicios existentes son de prueba y se pueden tocar. Victor autorizó crear un servicio de prueba dedicado para la verificación de este plan (con DP, cronograma y RDT propios). Esto no autoriza migraciones destructivas: cada migración se sigue confirmando con Victor.

**Riesgos:** tocar la importación del DP, que hoy funciona y alimenta PR y Dashboard; unos 17 archivos dependen de la convención; los servicios ya importados deben seguir igual tras la migración.

### Criterios de aceptación

1. Un presupuesto de 4 niveles y uno de 5 se importan sin perder filas de encabezado y cada nivel muestra su rol (en el de 5, el nivel 2 propone "Área").
2. La pantalla muestra el número de niveles y una fila de muestra por grupo, con rol sugerido; aprobar aplica el rol a las hermanas.
3. Las filas fuera de patrón quedan marcadas para revisar.
4. DP, PR, Crear RDT y Consolidado RDTs agrupan según el mapa y los servicios ya importados se ven igual que antes.
5. El cronograma guarda su mapa propio; el enlace con el DP sigue funcionando.
6. Reimportar conserva las confirmaciones de los códigos que siguen existiendo.
7. Flujos 09, 15 y los afectados coherentes con lo implementado.

### Estrategia de prueba / evidencia

- Lógica pura con vitest: detección de niveles, propuesta por defecto, propagación a hermanas, filas fuera de patrón.
- `tsc --noEmit`, suite completa y lint comparado contra `main`.
- Verificación en vivo con Playwright y login real sobre un servicio con 4 niveles y otro con 5; una captura por ítem.
- Comprobar que los servicios existentes no cambian (DP, PR, filtros de RDT).

### Aprobación (Gate Spec)

- [x] Victor aprueba este Spec, incluidas D1 a D7 y la consulta de cada contradicción de la tabla de flujos.

## Entorno, repositorios, ramas y worktrees

- Modo: local. Documentación en `pg_control_proyectos` (`main`, directo); código en `py_control_proyectos_web`.
- `git worktree list` (2026-09-30): existe `.worktrees/local-worker-1` (rama `local-worker-1`). Verificado el 2026-09-30: está limpio y su rama ya está mergeada en `main` (plan de paneles cerrado), así que puede reutilizarse con autorización de Victor; no se crea ni borra rama o worktree sin autorización.
- Plan grande: tandas de 4 a 8 ítems, brief ≤ 8 KB, ~80 llamadas por Worker (`planes-grandes-en-tandas`).

## Asignación de roles

| Rol | Chat | Rama | Worktree | Estado |
|---|---|---|---|---|
| Orquestador | por nombrar | `main` | N/A | Activo |
| Planner | tras el Gate Spec | `main` | N/A | Pendiente |
| Worker | tras el Gate 1 | por confirmar | por confirmar | Pendiente |
| Auditor | por asignar | `main` | N/A | Pendiente |

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-09-30 | **Gate Spec: Victor aprobó los tres Specs ("todo aprobado")**, con las recomendaciones del Orquestador para todas las decisiones pendientes. Queda abierto, sin bloquear: el nombre del rol extra cuando un archivo trae más de 5 niveles (D6). El texto exacto de cada flujo contradicho se le muestra antes de editarlo. | Victor |
| 2026-09-30 | El último nivel de un presupuesto o cronograma es la partida (donde están metrado, fecha, etc.); los niveles anteriores varían por servicio. | Victor |
| 2026-09-30 | Al importar, el sistema indica cuántos niveles encontró, lista el contenido de cada uno y el usuario asigna el rol por desplegable. | Victor |
| 2026-09-30 | Para no iterar todo el presupuesto, se muestra una partida por paquete de partidas; sus hermanas siguen la misma secuencia. Los nombres reconocidos (p. ej. el del servicio) llegan como opción por defecto y solo falta la aprobación del usuario. | Victor |
| 2026-09-30 | Los niveles se arreglan **antes** que Paquetes de Trabajo y Plan Maestro. | Victor |
| 2026-09-30 | Si ya existe un Plan Maestro aprobado no se puede volver a cargar nada anterior a él (restricción). El borrador no restringe. Sin Plan Maestro aprobado, recargar se bloquea, se avisa qué se perdería y solo después se permite. | Victor |

## Enlaces a progreso y evidencia homónimos

- Progreso y evidencia: se crean al iniciar la implementación (`02-progreso/` y `03-evidencia/`, mismo nombre de archivo).

## Mejoras (de trabajo)

Ninguna todavía.

## Reglas de negocio acordadas en esta tarea

Se trasladan a su flujo al cerrar, previa consulta de cada contradicción a Victor.

- 2026-09-30 — El último nivel es la partida; los niveles previos (Servicio, Área, Subpresupuesto, Paquete de partidas) varían por servicio y se confirman al importar → `09-importar-dp.md` y `15-cronograma.md` (pendiente).

## Carpetas/archivos huérfanos

Ninguno detectado hasta ahora.

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

Ninguno todavía.
