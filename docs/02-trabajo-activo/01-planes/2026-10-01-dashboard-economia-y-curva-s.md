# 2026-10-01 — Dashboard Parcial/Completo por economía, Curva S con selector y costo real de recursos

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Este archivo contiene el Spec (paso 3). Promueve el plan futuro «Dashboard Parcial sin datos económicos y restricción económica definitiva» de `planes-futuros.md`.

## Identificación y estado

- Tema: separar de verdad los datos económicos del Dashboard según el rol, dar a la Curva S dos modos (económica y % avance físico) y exponer el costo real desagregado por recurso en el Dashboard Completo.
- Fecha: 2026-10-01.
- Estado: **Spec aprobado (Gate Spec, 2026-10-02)** — pendiente: Plan + Punch List del Planner (Gate 1).

## Spec / SDD

### Estado

`Aprobado` — Gate Spec aprobado por Victor el 2026-10-02, con las decisiones D1 a D5 según sus propuestas (ver Registro de decisiones).

### Problema y contexto

El sistema sigue una metodología híbrida LPS + EVM (`docs/06-material-de-apoyo/conocimiento/01-fundamentos-control-de-proyectos-evm-lps.md`). Ese fundamento distingue desde su §5.3 **dos curvas S que no deben confundirse**: la **Curva S física** (% de avance de obra, sin dinero) y la **Curva S financiera/valorizada** (S/ o USD). La literatura coincide (AACE 55R-09, Lean Construction Institute) y advierte que *comparar % contra dinero mezcla unidades y miente*.

Hoy el sistema tiene tres brechas respecto a ese diseño:

1. **El Dashboard Parcial muestra datos económicos.** El flujo 11 dice que Parcial y Completo comparten BAC, PV, EV, AC, SPI, CPI y EAC en USD; solo difieren en PPC/Pareto y enlace a Curva S. La matriz del flujo 14 (nota ¹) ya fija el estado **objetivo**: Parcial sin datos económicos (13 roles), Completo con ellos (los roles con `puedeVerEconomia`). Hoy esa separación no está implementada.
2. **La Curva S es solo económica.** Pantalla y chip propios (`21-curva-s.md`), una sola serie PV/EV/AC en USD, habilitada solo para los 5 roles con economía. No existe la contraparte no económica (Curva S física en %).
3. **El costo real (AC) no se desagrega.** El Dashboard muestra AC como un total, sin descomponerlo por recurso (qué recurso incide más).

### Resultado esperado

1. **Dashboard Parcial sin datos económicos; Completo con ellos.** El Parcial deja de mostrar BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC y VAC en dinero, y conserva lo físico/operativo (avance físico %, matriz de partidas sin costo, diagnóstico, PPC/Pareto). El Completo conserva todo y agrega el bloque nuevo de costo por recurso.
2. **Ambos dashboards enlazan a la Curva S.** Parcial y Completo tienen su botón/enlace a la pantalla de Curva S (hoy solo lo tiene el Completo, flujo 11).
3. **La Curva S pasa a tener un selector de dos modos:** «Económica (USD)» y «Avance físico (%)». El rol **ve** las dos opciones, pero la que no le corresponde queda **deshabilitada** (patrón "ver no es acceder", flujo 16); el servidor valida igual que la interfaz.
4. **Nuevo bloque «Costo real de recursos» solo en el Completo:** lista los recursos con el costo de cada uno (para ver su incidencia) y el total igual al AC.
5. **Acceso por rol:** los roles con economía (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos, jefe de costos) acceden a todo (Parcial + Completo, ambas curvas); los demás solo a Parcial + Curva S % avance físico.

### Alcance

- Separar los datos económicos del Dashboard Parcial y dejarlos en el Completo (flujo 11), alineado a la nota ¹ del flujo 14.
- Agregar a la pantalla de Curva S un selector de dos modos y la serie física en % (flujo 21).
- Definir el «% avance físico» de la curva física como **PV/BAC (planificado)** y **EV/BAC (real)** — la misma regla de "% avance físico" ya documentada en `control_de_proyectos.txt` §2.1 (ponderación interna por dinero, salida en %; nunca promedio simple de metrados).
- Agregar el bloque «Costo real de recursos» en el Dashboard Completo.
- Actualizar accesos: flujo 14 (tabla 1, filas Dashboard y Curva S), flujo 16 (chips y registro de accesos) y el artefacto «Matriz de permisos» en la misma tarea (política de coherencia y trazabilidad).
- Documentación de flujos 11, 14, 16 y 21.

### No alcance

- Proyección/EAC dibujado hacia el futuro sobre la curva (sigue fuera de alcance, flujo 21).
- Histograma de recursos (HH/HM planificado vs real) y TCPI: se anotan como candidatos a `planes-futuros.md`, no se construyen aquí.
- 3WLA / Lookahead / restricciones (planes futuros).
- Cambios al motor del PR ni a `evm.ts`: el Dashboard y la Curva S siguen leyendo, no recalculando.
- El plan en curso `2026-09-30-niveles-paquetes-plan-maestro-rdt` (que reescribe los flujos 14, 16 y 21): este Spec se coordina para no pisar sus cambios; la implementación se secuencia después de que ese plan cierre o coordinando los archivos compartidos.

### Usuarios / roles afectados

- **Los 13 roles**, en la medida en que ahora el rol sin economía puede ver el Dashboard Parcial y la Curva S física (antes no entraba a ninguno de los dos).
- Cambio de acceso concreto: la fila «Curva S» del flujo 14 (tabla 1) y el chip «Curva S» dejan de ser "solo 5 roles"; pasa a "13 roles para la física, 5 para la económica". Ver decisión D1.
- El interruptor Parcial/Completo y su visibilidad por rol: ver D3.

### Reglas de negocio y documentos afectados

Tabla de cambios (se aprueba en el Gate 1 junto con el plan; aquí se anticipan las contradicciones):

| Flujo / artefacto | Dice hoy | Pasaría a decir | Estado |
|---|---|---|---|
| 11 Dashboard | Parcial y Completo muestran los mismos KPIs económicos; solo Completo enlaza Curva S | Parcial sin dinero (solo avance físico %, matriz sin costo, diagnóstico, PPC/Pareto); Completo con todo + bloque «Costo real de recursos»; ambos enlazan Curva S | Propuesto |
| 21 Curva S | Una sola serie PV/EV/AC en USD, solo 5 roles (`puedeVerCurvaS`) | Selector «Económica (USD)» / «Avance físico (%)»; la física (PV/BAC y EV/BAC) la ven los 13 roles; la económica, los 5 | Propuesto |
| 14 Accesos (tabla 1) | «Curva S — Sí (económico) — 5 roles»; «Dashboard — Sí — 5 roles» (nota ¹: Parcial/Completo objetivo) | Curva S física sin datos económicos (13 roles) y Curva S económica (5 roles); Dashboard Parcial sin economía (13 roles) y Completo con economía (5 roles) | Propuesto |
| 16 Paneles | Chip «Curva S» habilitado solo para 5 roles | Chip «Curva S» habilitado para 13 roles; dentro, el selector restringe el modo | Propuesto |
| Matriz de permisos (artefacto) | Fila «Curva S» 5 roles | Igual que flujo 14 | Propuesto |

### Datos, API, migraciones o dependencias

- La serie física **no requiere datos nuevos**: `curva_s_proyecto` ya agrega PV/EV/AC por fecha; el % es PV/BAC y EV/BAC sobre lo ya existente (`pr_partidas`, `plan_maestro_asignaciones`, RDT validado). Sin migración nueva para la curva.
- Endpoint `GET /api/curva-s` gana un parámetro de modo (`económica` | `fisica`) y valida el permiso por modo: `fisica` → cualquier rol autenticado con alcance por OT; `económica` → `puedeVerCurvaS` (5 roles). Detalle del contrato a fijar por el Planner.
- «Costo real de recursos»: desagregar el AC por recurso. El dato probablemente ya vive en el PR (`pr_recursos` / costo acumulado por HH y por HM, `control_de_proyectos.txt` §2.1); el Planner lo verifica en el código y propone la fuente exacta. Materiales y subcontratos **no** entran (regla 5: se miden por % avance económico, no por costo capturado); MOI no valoriza (regla 10). Ver D2 para el alcance exacto.
- Sin migraciones destructivas. Si el Planner propone una, se confirma con Victor antes de correrla (regla de migraciones).

### Diseño / UI aplicable

- Selector segmentado en la pantalla de Curva S («Económica (USD)» | «Avance físico (%)»), un solo eje Y por modo y unidad rotulada (nunca % y $ en el mismo eje). La opción no permitida se muestra deshabilitada con título explicativo.
- Bloque «Costo real de recursos» en el Completo: tabla/lista recurso → costo, con total = AC, reutilizando componentes existentes y la paleta de `design.md`.
- Respeta `docs/05-diseno-y-referencias/design.md` y el flujo 16 (patrón "ver no es acceder", tablas con scroll, estados de carga/vacío/error).

### Riesgos y decisiones pendientes

**Decisiones que Victor debe confirmar en el Gate Spec:**

- **D1. Chip y acceso «Curva S».** Propuesta: el chip «Curva S» se habilita para los 13 roles (pueden entrar a ver la curva física); dentro de la pantalla, el selector restringe la económica a los 5 roles. Esto cambia la fila «Curva S» del flujo 14. Alternativa: mantener el chip deshabilitado para los 8 roles y que solo entren vía el botón del Dashboard Parcial (dos vías distintas). Recomiendo habilitar para los 13 (más simple y coherente con "ver no es acceder").
- **D2. Alcance de «Costo real de recursos».** Propuesta: **Personal (HH) + Equipos (HM)**, que son los dos componentes del AC real según las reglas 5 y 10; el balde "sin partida vinculada" (`costo_legacy_sin_partida_acum`) se muestra como fila/nota aparte si existe; materiales y subcontratos quedan fuera (no tienen costo real capturado). Confirmar si además quiere una vista por partida o solo por recurso.
- **D3. Interruptor Parcial/Completo.** Propuesta: los roles sin economía ven el Dashboard fijo en Parcial, con el interruptor visible pero deshabilitado (con título). Es el estado objetivo ya escrito en la nota ¹ del flujo 14.
- **D4. Enlace a Curva S desde Parcial.** Confirmar que el Dashboard Parcial gana el botón/enlace a Curva S (hoy solo lo tiene el Completo), y que abre la Curva S en el modo % para quien no tiene economía.
- **D5. Sin Plan Maestro aprobado.** La serie "% planificado" (PV/BAC) muestra «Pendiente» sin Plan Maestro aprobado (mismo patrón que hoy, flujo 21 regla 3); el "% real" (EV/BAC) se sigue dibujando con los RDT validados que existan.

**Coordinación:** el plan `2026-09-30-niveles-paquetes-plan-maestro-rdt` sigue reescribiendo los flujos 14, 16 y 21. Se implementa este Spec recién cuando ese plan cierre (o se coordinan los archivos compartidos), para no pisar cambios.

### Criterios de aceptación

1. Con un rol sin economía, el Dashboard abre en Parcial y **no muestra** ningún dato monetario (BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC, VAC); con un rol con economía, el Completo los muestra todos y el bloque «Costo real de recursos» suma igual al AC.
2. El interruptor Parcial/Completo se ve en ambos casos; en el rol sin economía está deshabilitado (fijo en Parcial).
3. Ambos dashboards enlazan a la Curva S.
4. La Curva S muestra el selector; un rol sin economía ve «Económica (USD)» deshabilitado y «Avance físico (%)» activo; un rol con economía ve los dos activos.
5. La curva física dibuja % planificado (PV/BAC) y % real (EV/BAC) sin exponer dinero; la económica dibuja PV/EV/AC en USD.
6. El servidor rechaza con 403 el modo económico para un rol sin economía aunque lo fuerce por URL/API.
7. «Costo real de recursos» (Completo) lista cada recurso con su costo, el total iguala AC y no suma dos veces el balde legacy.
8. Flujos 11, 14, 16 y 21 y la matriz de permisos quedan coherentes con lo implementado.

### Estrategia de prueba / evidencia

- Lógica pura con vitest: cálculo de % físico (PV/BAC, EV/BAC), desagregación de AC por recurso y suma = AC (incluido el balde legacy).
- `tsc --noEmit`, suite completa y lint comparado contra `main`.
- Verificación en vivo con Playwright y login real, usando el Skill `verificar-permisos-por-rol` para las dos caras (rol con economía y rol sin economía), sobre un servicio de prueba.
- Probar que forzar la URL/API del modo económico con un rol sin economía devuelve 403.

### Aprobación (Gate Spec)

- [x] Victor aprueba este Spec, incluidas las decisiones D1 a D5. — 2026-10-02 («dale»); D1 según recomendación, D2–D5 según sus propuestas.

## Entorno, repositorios, ramas y worktrees

- Modo: local. Documentación en `pg_control_proyectos` (`main`, directo); código en `py_control_proyectos_web`.
- Rama y worktree del Worker se definen tras el Gate 1 (no se crea rama ni worktree sin autorización). Se secuencia tras el plan `2026-09-30-niveles-paquetes-plan-maestro-rdt` (ver coordinación).

## Asignación de roles

| Rol | Rama | Worktree | Estado |
|---|---|---|---|
| Orquestador | `main` | N/A | Activo |
| Planner | `main` | N/A | Pendiente (tras Gate Spec) |
| Worker | por confirmar | por confirmar | Pendiente (tras Gate 1) |
| Auditor | `main` | N/A | Pendiente |

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-01 | La Curva S física (no económica) se dibuja como dos series en %: planificado (PV/BAC) y real (EV/BAC); el dinero solo pondera internamente. | Victor |
| 2026-10-02 | **Gate Spec aprobado** (Spec completo con D1–D5). | Victor |
| 2026-10-02 | **D1:** el chip «Curva S» se habilita para los 13 roles; dentro de la pantalla, el selector restringe la curva económica a los 5 roles con economía. | Victor |
| 2026-10-02 | **D2:** «Costo real de recursos» = Personal (HH) + Equipos (HM); el balde `costo_legacy_sin_partida_acum` como fila/nota aparte; materiales y subcontratos fuera; vista solo por recurso (no por partida). | Victor |
| 2026-10-02 | **D3:** los roles sin economía ven el Dashboard fijo en Parcial, con el interruptor visible pero deshabilitado. | Victor |
| 2026-10-02 | **D4:** el Dashboard Parcial gana enlace a Curva S y lo abre en modo «Avance físico (%)» para quien no tiene economía. | Victor |
| 2026-10-02 | **D5:** sin Plan Maestro aprobado, la serie % planificado (PV/BAC) muestra «Pendiente»; el % real (EV/BAC) se dibuja con los RDT validados existentes. | Victor |

## Enlaces a progreso y evidencia homónimos

- Progreso y evidencia: se crean al iniciar la implementación (`02-progreso/` y `03-evidencia/`, mismo nombre de archivo).

## Mejoras (de trabajo)

Ninguna todavía.

## Reglas de negocio acordadas en esta tarea

Se trasladan a su flujo al cerrar, previa consulta de cada contradicción a Victor.

- 2026-10-01 — La Curva S tiene dos modos: económica (USD, roles con economía) y física (% avance físico, todos los roles). → `21-curva-s.md` (pendiente de Gate 1).

## Observaciones sobre la política

Ninguna todavía.

## Carpetas/archivos huérfanos

Ninguno detectado hasta ahora.

## Informe de Auditoría

Pendiente.

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

- **TCPI** como KPI del Dashboard Completo (el fundamento lo lista; hoy no está).
- **EAC como línea proyectada** sobre la Curva S (hoy marcado "fuera de alcance" en el flujo 21).
- **Histograma de recursos (HH/HM)** planificado vs real.
