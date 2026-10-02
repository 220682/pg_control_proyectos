# 2026-10-01 — Dashboard Parcial/Completo por economía, Curva S con selector y costo real de recursos

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Este archivo contiene el Spec (paso 3, aprobado en Gate Spec) y, a partir de «Referencia al Spec aprobado», el Plan y la Punch List del Planner. Promueve el plan futuro «Dashboard Parcial sin datos económicos y restricción económica definitiva» de `planes-futuros.md`.

## Identificación y estado

- Tema: separar de verdad los datos económicos del Dashboard según el rol, dar a la Curva S dos modos (económica y % avance físico) y exponer el costo real desagregado por recurso en el Dashboard Completo.
- Fecha: 2026-10-01.
- Estado: **Implementación completada (2026-10-02)** — tandas A, B, C, D, T2, T3, E y P03 cerradas; Punch List: todos los ítems Conforme salvo **P05** (artefacto «Matriz de permisos», exclusivo de Victor). Código en `local-worker-5` (HEAD `98df43c`), sin merge (espera Gate 2). Pendiente: ronda documental E2 (traslado de M4–M9), Auditoría y Gate 2. Sesión anterior del Orquestador congelada: se retomó el 2026-10-02, se abortó un merge en progreso en `main` de la app sin Gate 2 (ver OP6).

Puertas:

- Gate Spec: `aprobado por Victor (2026-10-02)`
- Gate 1: `aprobado por Victor (2026-10-02)`
- Gate 2: `pendiente`

## Referencia al Spec aprobado

| Spec | Estado |
|---|---|
| El Spec vive en este mismo archivo, sección «Spec / SDD» (inmutable salvo reapertura) | Aprobado (Gate Spec, 2026-10-02) — decisiones D1 a D5 según recomendación |

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

**Coordinación:** el plan `2026-09-30-niveles-paquetes-plan-maestro-rdt` **cerró el 2026-10-02** y sus flujos 14, 16 y 21 quedaron aplicados. Este Spec se implementa desde ese estado; el solape documental se resuelve en la Fase E.

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

## Objetivo, alcance y no alcance

- **Resultado esperado:** ver «Resultado esperado» del Spec (1–5): Dashboard Parcial sin datos económicos y Completo con ellos y con el bloque de costo por recurso; ambos dashboards enlazan la Curva S; Curva S con selector de dos modos; acceso completo a los 5 roles con economía y Parcial + curva física a los 13 roles.
- **Alcance:** Dashboard (flujo 11), Curva S (flujo 21), accesos y chips (flujos 14 y 16) y el artefacto «Matriz de permisos»; documentación de los cuatro flujos.
- **No alcance:** ver «No alcance» del Spec — proyección/EAC sobre la curva, histograma de recursos, TCPI, 3WLA, cambios al motor del PR ni a `evm.ts`, Dashboard del portafolio (sus filas de permisos no cambian) y el plan en curso `2026-09-30-niveles-paquetes-plan-maestro-rdt` (coordinación obligatoria).
- **Validación esperada:** `npm test` (vitest), `npx tsc --noEmit`, `npm run lint` y `npm run build` en el carril; pruebas unitarias de la lógica nueva (% físico y reconciliación del AC); verificación en vivo con Playwright y login real usando el Skill `verificar-permisos-por-rol` para las dos caras (rol con economía y rol sin economía); 403 del modo económico forzado por URL/API; Punch List verificada ítem por ítem contra la app real; coherencia de los flujos 11, 14, 16 y 21 con lo implementado.

## Entorno, repositorios, ramas y worktrees

- Modo: local. Documentación en `pg_control_proyectos` (`main`, directo). Código en `py_control_proyectos_web`.
- **Verificado (2026-10-02):** docs: `main` = `origin/main` (`10ceded`), 0/0 al empezar la sesión. Código: `main` = `origin/main` = `ce5623e`, árbol limpio; worktrees existentes `.worktrees/local-worker-1..4` (ramas `local-worker-N`) usados por el plan `2026-09-30-niveles-paquetes-plan-maestro-rdt`. Comandos de `package.json`: `npm test` (`vitest run`), `npm run lint`, `npm run build` (`next build`; en worktree con `node_modules` enlazado usar `npx next build --webpack`), `npx tsc --noEmit`. Sin carpeta de Skills en el repo de la app.
- **Rama y worktree de este plan:** se definen en el Gate 1 (ii); no se crea rama ni worktree sin autorización. Propuesta: carril nuevo `local-worker-5` desde `main` + `.worktrees/local-worker-5` (puerto 3115), tras el cierre del plan `2026-09-30-niveles-paquetes-plan-maestro-rdt`.
- **Coordinación (precondición):** cumplida — el plan `2026-09-30-niveles-paquetes-plan-maestro-rdt` quedó **Cerrado** el 2026-10-02; su código ya está en `main` de la app y sus flujos 14/16/21 quedaron aplicados. La Fase A arranca desde ese `main`; el solape documental de los flujos 14/16/21 se resuelve en la Fase E (Victor autorizó proceder).
- Sin migraciones nuevas previstas (la serie física se calcula sobre datos existentes: `curva_s_proyecto`, `pr_partidas`, `plan_maestro_asignaciones`, RDT validado). Si durante la implementación aparece una, se detiene y se consulta antes de ejecutarla (protocolo de migraciones, `…-briefs/00-protocolo-migraciones.md`).

## Skills aplicables

Skills de `.claude/skills/` de `pg_control_proyectos` (el repo de la app no tiene carpeta de Skills):

| Skill | Quién | Dónde |
|---|---|---|
| `seguir-flujo-de-planes` | Orquestador | Al lanzar cada fase y antes del mensaje de cierre |
| `verificar-permisos-por-rol` | Worker | Fase A (permisos, chips y registro de accesos) y verificación en vivo de las dos caras (con y sin economía) en Fase D |
| `cerrar-tanda` | Worker | Al final de cada tanda (A, B, C y D) |
| `trasladar-hallazgos` | Documentador | Tanda final (traslado del libro de hallazgos a su destino) |

## Fases y dependencias

| Fase | Qué | Worker | Depende de |
|---|---|---|---|
| A | Permisos y accesos: `puedeVerDashboard` a 13 roles, `puedeVerCurvaS` a 13 roles, nuevo `puedeVerCurvaSEconomica` (5 roles); `registro-accesos.ts` y `matriz-base-flujo14.ts`; sus pruebas; Parcial forzado en servidor para rol sin economía; interruptor Parcial/Completo visible pero deshabilitado con `title` | Worker 1 | Gate 1 + cierre (o coordinación) del plan niveles |
| **T** | **Proyecto de prueba de extremo a extremo** (Gate 1, consulta 1): crear un proyecto con datos desde la creación del servicio hasta la emisión de RDT hasta el ~50 % de avance del servicio — PM, partidas, asignaciones, HH/HM con costo, RDTs validados — para ver toda la estructura funcionando y alimentar la verificación de B, C y D | Worker 1 | A |
| B | Dashboard: Parcial sin dinero (ocultado según PD5), Bloque E visible en ambos modos, enlace a Curva S desde ambos, bloque «Costo real de recursos» con reconciliación = AC (PD1) | Worker 1 | A (verifica con la Fase T) |
| C | Curva S: selector segmentado de dos modos (PD4), serie física % (PV/BAC y EV/BAC), contrato `GET /api/curva-s?modo=` con 403 (PD2) | Worker 1 | A (verifica con la Fase T) |
| D | Integración y verificación en vivo: Playwright con login real, 13 roles, dos caras, móvil; suite/`tsc`/lint/build; proyecto de prueba usado de punta a punta | Worker 1 + Orquestador | B, C, T |
| E | Documentación: flujos 11, 14, 16 y 21, índice de planes, `planes-futuros.md`; artefacto «Matriz de permisos» (lo edita Victor); traslado del libro de hallazgos | Documentador | D |

Un solo Worker de código: las tres fases tocan `permisos.ts` / `registro-accesos.ts` (además de pisar el terreno del plan niveles), así que un paralelismo aquí solo generaría conflicto. Si Victor autoriza un segundo carril en el Gate 1, B y C podrían correr en paralelo (archivos disjuntos salvo `permisos.ts`, ya tocado en A). El merge a `main` del código ocurre **solo tras el Gate 2** (Worker git).

## Equipo del plan

| Rol | Modelo | Sesión/tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|
| Orquestador | Sonnet | esta sesión | `main` (docs) | N/A | Activo |
| Planner | Sonnet | este plan | `main` (docs) | N/A | Plan entregado |
| Worker 1 | Sonnet | tandas A–D | por confirmar (Gate 1, ii) | por confirmar | Pendiente |
| Documentador | Sonnet | tanda E | `main` (docs) | N/A | Pendiente |
| Worker git | Haiku | a pedido | opera sobre las demás | — | Pendiente |
| Auditor | Sonnet | tras E | `main` (docs) | N/A | Pendiente |

Sin Opus (política de modelos, `docs/01-contexto-repositorio/09-medicion-y-modelos.md`); el Orquestador mide sus sesiones y se releva según `docs/00-estandar-agentes/08-medicion-y-relevo.md`.

### Brief de cada Worker

Los briefs viven en `2026-10-01-dashboard-economia-y-curva-s-briefs/` (plantilla `13-brief-de-tanda.md`, ≤ 8 KB), uno por tanda (A–D), con su `resultados/<tanda>.md`; la carpeta se crea al lanzar la Fase A. La tanda E (Documentador) trabaja con este archivo como referencia.

### Prompt del Auditor

> Audita este plan contra su Spec (sección «Spec / SDD», criterios 1–8). Revisa: (a) que el Dashboard de un rol sin economía no muestre **ningún** dato monetario — lista de la PD5: KPIs BAC–VAC, resumen ejecutivo, chip semáforo, dona de composición de costo, gráfico de desempeño por partida, columnas PV/EV/AC/SPI/CPI de la matriz, cabecera «Costo directo (US$)» y orden «mayor desviación de costo» — y que conserve filtros, % avance físico, matriz sin costo, diagnóstico, PPC/Pareto y enlace a Curva S; (b) que el bloque «Costo real de recursos» sume exactamente el AC sin doble contar `costo_legacy_sin_partida_acum` y muestre la fila «Sin resolver» solo cuando la diferencia sea distinta de cero; (c) que el servidor rechace con 403 el modo económico a un rol sin economía y que la respuesta en modo físico no exponga USD; (d) que los flujos 11, 14, 16 y 21 y la matriz derivada del registro coincidan con la tabla del Gate 1 y con lo implementado (el artefacto «Matriz de permisos» lo revisa Victor); (e) que la verificación en vivo cubra las dos caras con `verificar-permisos-por-rol` y que la Punch List tenga evidencia ítem por ítem; (f) trazabilidad del libro de hallazgos. Formato: `06-informe-auditoria.md` en `02-trabajo-activo/04-auditoria/`.

## Archivos / componentes afectados

**Código (`py_control_proyectos_web`):**

- `src/lib/permisos/permisos.ts` (+ `permisos.test.ts`): `puedeVerDashboard` → 13 roles, `puedeVerCurvaS` → 13 roles, nuevo `puedeVerCurvaSEconomica` (los 5 de `puedeVerEconomia`); `puedeVerEconomia` y `puedeVerDashboardPortafolio` intactos.
- `src/lib/config/registro-accesos.ts` (+ `registro-accesos.test.ts`) y `src/lib/config/matriz-base-flujo14.ts` (+ `matriz-accesos.test.ts`): filas «Dashboard» y «Curva S».
- `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`: gate de 13 roles, Parcial forzado en servidor, ocultado por modo (PD5), enlace a Curva S, y query de `pr_recursos` que hoy selecciona `tipo, costo_contractual, costo_acumulado, cantidad_acumulada` **sin `descripcion`** (añadirlo).
- `src/components/dashboard/`: `ToggleTipoDashboard.tsx` (opción deshabilitada con `title` para rol sin economía), `BloqueE.tsx` (visible en ambos modos), `MatrizPartidasDashboard.tsx` (columnas de costo solo en Completo), componente nuevo del bloque «Costo real de recursos»; `ResumenEjecutivo`, chip semáforo, `DonaCosto` y gráfico de desempeño por partida ocultos en Parcial.
- `src/components/curva-s/PantallaCurvaS.tsx` (selector segmentado, tarjetas y tabla por modo) y `GraficoCurvaS.tsx` (serie en %); `src/app/(workspace)/proyectos/[id]/curva-s/page.tsx`.
- `src/lib/curva-s/curva-s.ts` (+ `curva-s.test.ts`): serie y lectura en %; `src/app/api/curva-s/route.ts` (+ prueba): parámetro `modo=`.
- `src/app/api/proyectos/[id]/tipo-dashboard/route.ts`: **sin cambio** de permiso (sigue exigiendo `puedeVerEconomia`).
- Pruebas afectadas: `permisos.test.ts` (mapea filas del flujo 14 leyendo su markdown por ruta absoluta), `registro-accesos.test.ts`, `matriz-accesos.test.ts`, `integracion-permisos.test.ts`, `panel-izquierdo.test.ts`, `panel-derecho.test.ts`.
- Sin migraciones; solo lectura de `db/008`, `db/053`, `db/055` y `db/070`.

**Documentación (`pg_control_proyectos`):**

- `docs/04-flujos-de-negocio/11-dashboard.md`, `14-accesos-y-restricciones.md`, `16-paneles.md`, `21-curva-s.md` y sus índices.
- `docs/02-trabajo-activo/01-planes/README.md` (fila del plan) y `docs/02-trabajo-activo/01-planes/planes-futuros.md` (la entrada que este Spec promueve).
- Artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT): lo edita solo Victor, en la misma tarea (política de coherencia y trazabilidad).

## Decisiones de diseño del Planner (delegadas por el Spec)

| # | Decisión | Por qué |
|---|---|---|
| PD1 | **Bloque «Costo real de recursos»:** filas = `pr_recursos` (tipos MO y HM con `descripcion`; añadir `descripcion` a la query del Dashboard); fila «Sin resolver / diferencia» = `AC − Σ filas`, visible solo si ≠ 0, con título que explica las filas sin resolver (deuda de `db/055`); **el balde `costo_legacy_sin_partida_acum` es nota informativa, nunca fila sumable** (ya está dentro de las filas de recursos: sumarlo duplicaría); **Total = AC** leído del PR. | Cumple el criterio 7: total = AC sin doble suma. Por construcción `Σ pr_recursos ≤ AC`; lo que falta queda explicado en la diferencia, no se fuerza a cero. |
| PD2 | **Contrato `GET /api/curva-s`:** parámetro `modo=economica|fisica`; sin `modo`, el servidor deriva: `economica` si `puedeVerEconomia`, si no `fisica`; `modo=economica` exige `puedeVerCurvaSEconomica` (403 en caso contrario, criterio 6); `modo=fisica` **no devuelve montos USD** (solo series y lectura en % y brecha en pp, sin `bac`). | Un solo contrato, determinista, sin confiar en la query del navegador; el modo físico no puede filtrar dinero por la puerta de atrás (criterio 5). |
| PD3 | **Permisos:** `puedeVerDashboard` y `puedeVerCurvaS` pasan a los 13 roles (chip y pantalla abiertos a todos); nuevo `puedeVerCurvaSEconomica` = `puedeVerEconomia`; el servidor **fuerza Parcial** si el rol no tiene economía aunque `tipo_dashboard='COMPLETO'` en BD (la BD se respeta solo para roles con economía); `puedeVerDashboardPortafolio` y el resto de la matriz de economía no cambian. | Spec resultado 5; «ver no es acceder»: los 13 entran, los 5 ven dinero. |
| PD4 | **Selector segmentado** al patrón de `ToggleTipoDashboard` (`role="group"`, `aria-label`, opción no permitida con `disabled` + `title`, nunca oculta); no se reutiliza `SelectorDashboard.tsx` (componente legacy aparentemente sin uso real). | Consistencia con el interruptor Parcial/Completo (criterio 2) y con el patrón de chips del flujo 16. |
| PD5 | **En Parcial se ocultan** (además de los 10 KPI): cabecera «Costo directo (US$)», resumen ejecutivo (imprime SPI/CPI), chip semáforo (deriva de CPI), dona «Composición del costo», gráfico «Desempeño por partida», columnas PV/EV/AC/SPI/CPI de la matriz de partidas y la opción de orden «mayor desviación de costo». **Se conservan:** filtros, % avance físico, matriz de partidas sin costo, panel de diagnóstico, PPC/Pareto y enlace a Curva S. | «Ningún dato monetario» (criterio 1) incluye los números que esos componentes imprimen o de los que derivan. |
| PD6 | **Bloque E (PPC + Pareto) y enlace a Curva S visibles en ambos dashboards**; el enlace abre `?modo=fisica` solo cuando el rol no tiene economía. | El Spec da al Parcial PPC/Pareto (resultado 1) y el enlace en ambos (resultado 2); hoy solo el Completo los tiene. |

## Punch List embebida

Formato `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia de cada ítem va en el archivo de evidencia homónimo.

### Estado de aprobación

Gate 1: **aprobado** por Victor el 2026-10-02 — plan, Punch List (40 ítems), tabla de 12 cambios a flujos, pre-autorizaciones en bloque y preguntas Q1–Q6, todo en una sola aprobación (respuestas más abajo).

### Ítems funcionales

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F01 | A | El chip «Dashboard» queda habilitado para los 13 roles (`puedeVerDashboard` + `registro-accesos`), con alcance por OT; sin permiso queda deshabilitado con título y sin enlace | Tests + captura del chip por rol | Conforme (A: tests; D: barrido 13 roles R03 + R05 sin chips rotos) |
| F02 | A | El chip «Curva S» queda habilitado para los 13 roles; `puedeVerCurvaSEconomica` devuelve true solo a los 5 con economía | Tests + captura del chip por rol | Conforme (A: tests; D: barrido 13 roles R03/R05) |
| F03 | A/B | Con BD en `COMPLETO`, un rol sin economía abre **Parcial** (el servidor lo fuerza); con rol con economía se respeta la BD | Prueba con BD en COMPLETO y rol sin economía | Conforme (D: PS-0008 COMPLETO + `supervisor_operativo` → Parcial sin USD) |
| F04 | B | Parcial no muestra ningún dato monetario (lista cerrada de la PD5), incluso con BD en COMPLETO | Captura + inspección ítem por ítem | Conforme (D: barrido DOM, 8 roles sin economía → sin `US$` ni «Costo directo») |
| F05 | B | Parcial conserva filtros, % avance físico, matriz de partidas sin costo, diagnóstico, PPC/Pareto (Bloque E) y enlace a Curva S | Captura | Conforme (D: captura `F03-F04-F05-U05-*`) |
| F06 | B | El interruptor Parcial/Completo se ve en ambos casos; deshabilitado con `title` (D3) para rol sin economía; con economía alterna sin recargar (`router.refresh()`) | Captura + prueba de alternancia | Conforme (D: `disabled`+`title` sin economía; admin alterna sin recargar) |
| F07 | B | Ambos dashboards enlazan a Curva S; desde Parcial con rol sin economía la URL lleva `?modo=fisica`; desde Completo abre el modo económico | Captura + URL | Conforme (D: DOM `hrefCurvaS` = `/curva-s?modo=fisica` en Parcial) |
| F08 | B | Bloque «Costo real de recursos» solo en Completo: filas por recurso, fila «Sin resolver» cuando corresponde, nota del legacy y Total = AC | Captura + suma manual | Conforme (B: tests D02; D: captura `U03-F08-F13-*`) |
| F09 | C | El selector de dos modos se ve siempre; «Económica (USD)» deshabilitada con `title` para rol sin economía; los dos activos para rol con economía | Captura por rol | Conforme (D: `aria-disabled="true"`+`title` sin economía; ambos activos con admin — matiz (a) confirmado) |
| F10 | C | La curva física dibuja % planificado (PV/BAC) y % real (EV/BAC) con unidad rotulada, sin USD en eje, tooltips, tarjetas ni tabla | Captura | Conforme (D: PS-0004 EV real 12.3 %, eje «Avance físico (%)», sin USD) |
| F11 | C | Sin Plan Maestro aprobado: % planificado «Pendiente» (D5); % real dibujado con los RDT validados existentes | Captura en servicio sin PM | Conforme con nota (D: PS-0007 banner «Pendiente»; % real con RDT visto en PS-0004; no existe proyecto sin-PM-con-RDT en los datos) |
| F12 | T | Proyecto de prueba creado de extremo a extremo: creación del servicio → PM → partidas y asignaciones → HH/HM con costo → RDTs validados hasta ~50 % de avance del servicio (datos marcados y desactivables) | Proyecto de prueba existente con su trayectoria | Conforme (T2+T3: PS-0009 `PRUEBA-DASH` con DP, cronograma, paquete `PT-001`, PM v2 APROBADO con 22 asignaciones, 2 RDTs VALIDADOS, 50 % de avance; lista de borrado en `resultados/tanda-T2.md` y `tanda-T3.md`) |
| F13 | T | Con ese proyecto se ve toda la estructura funcionando: Dashboard (Parcial y Completo), Curva S (los dos modos), bloque «Costo real de recursos» y accesos por rol | Capturas de cada pantalla con el proyecto de prueba | Conforme (T3: capturas `T3-F13-*` — Completo con AC 297,76 = Total del bloque; Parcial sin USD; Curva S económica y física con datos reales) |

### Datos y cálculos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| D01 | B | La query del Dashboard añade `descripcion` a `pr_recursos` (hoy falta) y el bloque la usa | Diff + salida de la consulta | Conforme (B: commit `94a5f79`) |
| D02 | B | Función de reconciliación con tests: `Σ filas + (AC − Σ) = AC`; con legacy; sin legacy; filas sin resolver ≠ 0; diferencia = 0 (no se muestra la fila) | `npm test` | Conforme (B: `costo-recursos.test.ts` 6 pruebas) |
| D03 | C | Serie física en lógica pura con tests: PV/BAC y EV/BAC, BAC = 0 → sin serie, recorte al corte conservado, agrupación semanal intacta | `npm test` | Conforme (C: `curva-s.test.ts` 18/18) |
| D04 | B/C | Dashboard y Curva S siguen leyendo, no recalculando: sin cambios en `evm.ts`, `dashboard.ts` ni funciones SQL | Diff | Conforme (B/C: diff verificado) |
| D05 | B | El Total del bloque es el mismo AC que imprime el KPI AC (misma fuente del PR) | Captura comparando Total y KPI | Conforme (B: misma fuente; D: captura `U03-F08-F13-*`) |

### Permisos

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| P01 | A | `permisos.ts`: `puedeVerDashboard` y `puedeVerCurvaS` a los 13 roles; nuevo `puedeVerCurvaSEconomica` = 5; sin rol conocido → false; `puedeVerEconomia` intacto | `npm test` (`permisos.test.ts`) | Conforme (A: commit `d40cd74`) |
| P02 | A | `registro-accesos.ts` y `matriz-base-flujo14.ts` coherentes: matriz derivada vs base con 0 diferencias | `matriz-accesos.test.ts` | Conforme (A: 0 diferencias) |
| P03 | A/E | Las pruebas que leen la tabla 1 del flujo 14 por ruta absoluta (`permisos.test.ts`, mapeo de filas × 13 roles) se actualizan en la misma ventana que el flujo 14 (Fase E); si no, `npm test` local queda rojo | `npm test` con el flujo 14 ya editado | Conforme (tanda P03: mapa 5→9 filas × 13 = 117 celdas; 93 tests del archivo, suite 1063 verde, tsc 0; commit `98df43c`) |
| P04 | A | Alcance por OT intacto en Dashboard y Curva S (pantalla y API), con bypass del administrador como hoy | Prueba con OT ajena y con admin | Conforme (A: tests OT ajena/propia/admin; D: guard sin cambios; prueba en vivo OT ajena se intenta en T2) |
| P05 | E | Artefacto «Matriz de permisos» actualizado con las filas nuevas, por Victor | Confirmación de Victor | Pendiente (Victor, Fase E) |

### UI / responsive / accesibilidad

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| U01 | C | Selector con `role="group"` y `aria-label`; opción no permitida accesible por teclado con `title` (no oculta, `aria-disabled`) | Inspección del DOM | Conforme (C: inspección; D: confirmado en vivo) |
| U02 | A/B | Interruptor Parcial/Completo y opciones de modo: deshabilitados **visibles** con `title` que explica el permiso | Captura por rol | Conforme (D: DOM, opciones visibles `disabled`+`title`) |
| U03 | B | Bloque de recursos con tabla con scroll horizontal, encabezado fijo y `scope` en los `th`; sin `max-w-*` en el contenedor de página; paleta de `design.md` | Captura escritorio y móvil | Conforme (D: DOM + capturas escritorio y móvil) |
| U04 | C | Un solo eje Y por modo con unidad rotulada; nunca % y USD en el mismo eje | Captura de ambos modos | Conforme (D: «US$ acumulado (CD)» vs «Avance físico (%)») |
| U05 | B | El ocultado en Parcial no deja huecos de layout ni secciones vacías | Captura móvil y escritorio | Conforme (D: 0 secciones vacías, escritorio y 390 px) |

### Estados vacío / carga / error

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| E01 | C | Sin PM aprobado: «Pendiente» en % planificado, sin curva PV inventada; sin RDT validados: serie real vacía con su nota | Captura en servicio sin PM y sin RDT | Conforme (D: PS-0007 sin PM «Pendiente»; PS-0008 sin RDT nota serie vacía — matiz (b) confirmado; aclaración RB7: con BAC=0 el mensaje es otro) |
| E02 | B | Bloque de recursos sin filas: estado vacío; diferencia = 0: no aparece la fila «Sin resolver» | Captura | Conforme (B: tests D02; estado vacío no visto en vivo — los datos de prueba tienen recursos) |
| E03 | B/C | Carga atenuada sin salto de layout; error de API con mensaje claro (patrón existente) | Captura o forzado de error | Conforme (D: 500 forzado → mensaje del cuerpo + carga atenuada `opacity-50`) |
| E04 | C | `modo=economica` sin permiso vía URL/API → 403 con mensaje; la interfaz nunca ofrece el modo | Llamada directa | Conforme (D: 403 «No tienes acceso a la Curva S económica»; botón `aria-disabled`) |

### Validación en servidor / API

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| V01 | C | `GET /api/curva-s?modo=economica` con rol sin economía → 403 aunque se fuerce (criterio 6); sin `modo` la respuesta es determinista por permiso | Llamada directa con las dos cuentas | Conforme (D: 403 forzado; sin `modo` → `fisica` sin dinero; admin → 200) |
| V02 | C | La respuesta de `modo=fisica` no incluye montos USD ni `bac` (cuerpo de respuesta revisado) | Cuerpo JSON de la respuesta | Conforme (C: cuerpo revisado; D: claves sin `ac` confirmado en vivo) |
| V03 | A | La página del Dashboard valida rol y alcance en servidor; el PATCH de `tipo-dashboard` sigue exigiendo `puedeVerEconomia` (sin cambio) | Prueba de rol sin economía forzando la ruta + revisión del PATCH | Conforme (D: F03 forzado de Parcial en servidor; T2: «Ver como» `supervisor_operativo` → `PATCH /tipo-dashboard` 403 «No autorizado») |
| V04 | A | Sin sesión o sin alcance: rechazo igual que antes (los guards no se debilitan) | Prueba sin sesión y con OT ajena | Conforme (D: sin sesión → 307 `/login`; T2: sesión real de López con OT ajena → 403 «No tienes esta OT a cargo» en API y «No tienes acceso» en Dashboard/Curva S — captura `T2-V04-*`) |

### Regresión

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| R01 | D | `npm test`, `npx tsc --noEmit`, `npm run lint` (comparado con `main`) y `npm run build` verdes en el carril | Salida de los comandos | Conforme (D: 1063 tests, tsc 0, lint 27=baseline, build 0) |
| R02 | D | Los 5 roles con economía ven idéntico al de hoy en Completo (mismos KPIs, mismo PR, misma curva económica) más el bloque nuevo | Antes/después con capturas | Conforme (D: barrido DOM de los 5 roles) |
| R03 | D | Los 13 roles entran a Parcial y a Curva S sin perder alcance por OT; el Dashboard del portafolio y el resto de interfaces de economía sin cambios | `verificar-permisos-por-rol` completo | Conforme (D: barrido 13 roles — 8 Parcial, 5 Completo; portafolio admin OK) |
| R04 | D | Las pruebas del plan coordinado `2026-09-30-niveles-paquetes-plan-maestro-rdt` siguen verdes tras integrar (en especial `integracion-permisos.test.ts`) | Suite completa | Conforme (D: `integracion-permisos` 5 OK; suite completa verde) |
| R05 | D | Verificación en vivo con login real (móvil y escritorio): sin chips rotos, sin enlaces muertos, paneles coherentes (flujo 16) | Capturas | Conforme (D: 1440 y 390 px vía CDP; capturas `R05-*`) |
| R06 | E | `python scripts/verificar-referencias.py` sin referencias rotas; índice de `01-planes/README.md` actualizado | Salida del verificador | Conforme (E: 45 archivos, 0 huérfanos, 0 rotos; índice actualizado — las 2 menciones sin archivo son preexistentes y ajenas) |

## Riesgos y bloqueos

| # | Riesgo | Mitigación |
|---|---|---|
| R1 | **Cerrado el riesgo base:** el plan `2026-09-30-niveles-paquetes-plan-maestro-rdt` quedó Cerrado (2026-10-02) y su código está en `main`. Resta la coordinación documental de los flujos 14/16/21 en la Fase E | El plan niveles ya no edita esos flujos; la Fase E parte de su versión final y R04 verifica la coherencia |
| R2 | `permisos.test.ts` lee el flujo 14 por ruta absoluta y compara fila por fila (7 filas × 13 roles, con `skipIf(existsSync)`): cambiar el doc sin cambiar el test rompe `npm test` en la máquina de Victor | La Fase A actualiza el mapa de filas y la Fase E edita el flujo 14 en la misma ventana; P03 se verifica con ambos ya cambiados |
| R3 | `pr_recursos` puede traer filas con `descripcion` NULL o horas huérfanas (deuda de `db/055`): `Σ filas < AC` | Fila «Sin resolver» = `AC − Σ` con explicación; nunca se fuerza a cero ni se inventa data |
| R4 | La respuesta de `modo=fisica` filtra USD por un componente reutilizado | Contrato PD2 (`bac` fuera de la respuesta) + V02 |
| R5 | Fuga de dinero en Parcial por un componente no previsto (resumen, semáforo, dona, orden por desviación) | Lista cerrada PD5 + verificación rol por rol con `verificar-permisos-por-rol` en la Fase D |
| R6 | El clasificador bloquea login de prueba, comandos o herramientas de navegador | Todo pedido autorizado de una vez en el Gate 1 (ii); si se deniega, no se rodea: se detiene y se vuelve a Victor |
| R7 | Cambiar `puedeVerDashboard` / `puedeVerCurvaS` afecta consumidores no previstos (hoy: ambas páginas, el enlace del ficha de proyecto, el registro de accesos y la API de curva) | P04 + grep de consumidores al empezar la Fase A; cualquier uso nuevo que asuma economía se consulta |
| R8 | Sin datos de prueba adecuados (servicio con PM aprobado y RDTs, servicio sin PM, recursos con costo) la verificación en vivo queda incompleta | El Gate 1 (i) fija los servicios antes de lanzar la Fase A |

## Consultas para el Gate 1

Tres bloques, según la política del flujo. Las respuestas se añadirán en «Gate 1 — respuestas de Victor» al aprobar.

### (i) Datos de prueba

- Servicio con Plan Maestro aprobado y RDTs validados, para la Curva S (los dos modos) y el Dashboard: ¿cuál? (PS-0004 y PS-0006 tienen PM aprobado según el lote 2; confirmar si sirven).
- Servicio **sin** Plan Maestro aprobado, para D5 («Pendiente» en % planificado).
- Servicio con `pr_recursos` poblado (MO y HM con `descripcion` y `costo_acumulado`) y AC > 0, para el bloque de recursos; si no existe, ¿cuál se crea?
- Cuentas para las dos caras de la verificación: una con rol de los 5 con economía y una solo con rol sin economía (suplantación «Ver como»).
- Dispositivo/navegador para la verificación responsive.

### (ii) Pre-autorizaciones — se piden autorizadas en bloque

- `npm run dev` local con `.env.local` (copia al worktree si falta) y puertos indicados.
- `npm test`, `npx tsc --noEmit`, `npm run lint` y `npm run build` en el carril.
- Credenciales de prueba para el login de Playwright, sin mostrar ni copiar ningún secreto.
- Suplantación de rol «Ver como» y llamadas de prueba sin efecto (Skill `verificar-permisos-por-rol`).
- Consultas de **solo lectura** a la base (verificar `pr_recursos`, AC y `tipo_dashboard`).
- Datos de prueba mínimos, marcados/desactivables: se crean y quedan marcados; **los borra Victor**, el agente no borra nada.
- Playwright en navegador con login real.
- Creación de la rama y el worktree del carril (propuesta: `local-worker-5` + `.worktrees/local-worker-5`, puerto 3115) o reutilización de uno libre.
- No hay migraciones previstas; si aparece alguna, se detiene y se consulta (protocolo de migraciones).

### (iii) Tabla de cambios a flujos — aprobación en bloque

| # | Documento | Qué dice hoy | Qué pasaría a decir | Quién lo edita |
|---|---|---|---|---|
| 1 | `11-dashboard.md` (tabla «Los dos Dashboards», líneas 13–22) | KPI, gráficos, matriz, diagnóstico y resumen en ambos modos; **Bloque E** y **Enlace a la Curva S** solo en Completo (`—` en Parcial) | Parcial: filtros, KPI de avance físico, matriz sin costo, diagnóstico, **Bloque E (PPC + Pareto)** y **enlace a Curva S**; Completo: todo lo anterior + KPIs de dinero, gráficos de dinero, resumen ejecutivo y bloque «Costo real de recursos» | Documentador |
| 2 | `11-dashboard.md` (líneas 24–31, interruptor) | «el interruptor lo activan los roles con datos económicos… **que los demás roles vean el Parcial fijo, sin interruptor, pertenece al plan futuro**» | «el interruptor se ve en ambos modos; los roles sin economía lo ven **deshabilitado con título**, fijo en Parcial (D3)» — se deroga «sin interruptor / pertenece al plan futuro» | Documentador |
| 3 | `11-dashboard.md` (líneas 68–84, indicadores) | BAC…% avance físico en ambos; PPC y Pareto «solo en el Completo»; resumen ejecutivo en ambos | Dinero (BAC–VAC, SPI, CPI, EAC), gráficos de dinero, resumen ejecutivo y semáforo **solo en Completo**; % avance físico, **PPC y Pareto en ambos**; regla nueva del bloque «Costo real de recursos» (filas MO/HM, fila «Sin resolver», nota del legacy no sumable, Total = AC) | Documentador |
| 4 | `11-dashboard.md` (líneas 51–53, chip) | «Lo ven habilitado los roles con datos económicos (`puedeVerDashboard`); los demás lo ven deshabilitado con título» | «lo ven habilitados los **13 roles** (Parcial); el Completo requiere datos económicos» | Documentador |
| 5 | `14-accesos-y-restricciones.md` (tabla 1, fila «Dashboard del servicio (Parcial y Completo)», línea 36) | Una sola fila, datos económicos `Sí`, 5 roles | Dos filas: «Dashboard — Parcial» (13 roles, datos económicos `—`) y «Dashboard — Completo» (5 roles, datos económicos `Sí`) | Documentador |
| 6 | `14-accesos-y-restricciones.md` (fila «Curva S», línea 40) | Una fila, datos económicos `Sí`, 5 roles | Dos filas: «Curva S — avance físico (%)» (13 roles, datos económicos `—`) y «Curva S — económica (USD)» (5 roles, datos económicos `Sí`) | Documentador |
| 7 | `14-accesos-y-restricciones.md` (nota ¹, línea 52) | Completo: «los 5 de esta tabla, **más las dos excepciones**»; «los demás lo verán fijo en Parcial, que es del plan futuro»; «esta fila es el estado **objetivo**, no el actual» | Completo: **exactamente los 5 roles con economía** (las excepciones planner/SOT son para Plan Maestro y DP, no para el Completo — resultado 5 del Spec); Parcial: 13 roles con interruptor visible deshabilitado; la nota deja de hablar de «plan futuro» y de «estado objetivo» | Documentador |
| 8 | `14-accesos-y-restricciones.md` (línea 196) | «Queda pendiente… el Dashboard Parcial sin datos económicos y la restricción económica definitiva» (apunta a `planes-futuros.md`) | «Implementado» con la fecha de cierre de este plan; la entrada se retira de `planes-futuros.md` en la Fase E | Documentador |
| 9 | `16-paneles.md` | No fija roles por chip (deriva del registro; regla 2: «ver no es acceder») | **Sin cambio de texto**: el chip Curva S (y Dashboard) quedan habilitados para los 13 porque `registro-accesos.ts` usa `puedeVerCurvaS` / `puedeVerDashboard`; la matriz derivada se regenera sola. Solo se actualiza «Estado de implementación» si cambia algo observable | Documentador |
| 10 | `21-curva-s.md` (regla 1, líneas 61–66) | «Lo ven habilitado los roles con datos económicos; los demás lo ven deshabilitado» | «lo ven habilitado los **13 roles**; dentro de la pantalla, el selector muestra «Económica (USD)» **deshabilitada con título** a los que no tienen economía» | Documentador |
| 11 | `21-curva-s.md` (regla 2 «Todo en USD», líneas 67; endpoint, 95–104; gráfico, 106–115; lectura, 117–122) | Serie única PV/EV/AC en USD; endpoint validado con `puedeVerCurvaS` (5 roles); eje único de dinero; lectura con SV/CV/SPI/CPI en USD | **Selector de dos modos** (Económica USD / Avance físico %); endpoint con `modo=` y 403 para el modo económico sin permiso; eje por modo con unidad rotulada; en modo físico la lectura es % planificado, % real y brecha en **pp** (sin SV/CV en USD); sin PM → «Pendiente» (D5) | Documentador |
| 12 | Artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT) | Filas Dashboard y Curva S en 5 roles | Igual que las filas 5, 6 y 7 de esta tabla | **Victor** (solo él lo edita) |

#### Contradicciones no anticipadas en la tabla del Spec

- Nota ¹ del flujo 14 (fila 7): «más las dos excepciones» para el Completo choca con el resultado 5 del Spec (solo los 5 roles con economía). No figuraba en la tabla de cambios del Spec.
- Flujo 11 (fila 2): «el Parcial fijo, **sin interruptor**, pertenece al plan futuro» choca con D3 (interruptor visible pero deshabilitado). No figuraba en la tabla del Spec.
- Chip «Dashboard» 5 → 13 (filas 4 y 9): la tabla del Spec solo listaba el chip Curva S; el chip Dashboard también cambia.
- «Resumen ejecutivo ✓ en Parcial» y chip semáforo hoy en ambos modos: no estaban itemizados; derivan de SPI/CPI → se ocultan en Parcial (PD5, filas 1 y 3) — **confirmar con Victor**.
- Bloque E con `—` en Parcial (hoy) vs «Parcial conserva PPC/Pareto» (Spec): se resuelve visible en ambos (PD6, fila 1) — **confirmar con Victor**.
- Acople prueba↔doc: `permisos.test.ts` lee el flujo 14 por ruta absoluta (riesgo R2). No cambia ninguna regla, pero condiciona la secuencia doc/código.

#### Preguntas sueltas

| # | Consulta | Por qué importa |
|---|---|---|
| Q1 | ¿Servicios de prueba para (i): con PM aprobado y RDTs, sin PM, con recursos y AC? | Sin ellos la verificación en vivo queda incompleta |
| Q2 | ¿Se confirma PD5 (ocultar resumen ejecutivo y semáforo en Parcial)? | No lo dice literalmente el Spec y toca dos componentes visibles |
| Q3 | ¿Se confirma PD6 (Bloque E visible en ambos dashboards)? | Deriva del Spec pero cambia la tabla del flujo 11 |
| Q4 | ¿Arrancar tras el cierre del plan niveles o coordinar sus archivos? | Condiciona el lanzamiento de la Fase A |
| Q5 | ¿Rama/worktree nuevos (`local-worker-5`) o reutilizar uno libre? | El Gate 1 (ii) debe autorizar la infraestructura |
| Q6 | ¿Quién y cuándo actualiza el artefacto «Matriz de permisos» en la misma tarea? | Política de coherencia: solo Victor puede editarlo |

### Gate 1 — respuestas de Victor (2026-10-02)

Aprobación única: plan, Punch List (40 ítems), tabla de 12 cambios a flujos (iii) y pre-autorizaciones en bloque (ii) — **aprobados**.

| # | Consulta | Respuesta de Victor |
|---|---|---|
| 1 | (i) Servicios de prueba | **No depende de servicios existentes: se crea un paso nuevo en el plan** — el agente implementador crea un proyecto con datos desde la creación del servicio hasta la emisión de RDT hasta el ~50 % de avance del servicio, para ver toda la estructura funcionando (ver Fase T y F12–F13). |
| 2 | Q2 — PD5 (ocultar resumen ejecutivo y semáforo en Parcial) | **Sí**, confirmada. |
| 3 | Q3 — PD6 (Bloque E en ambos dashboards) | **Sí**, se deja. |
| 4 | Q4 — secuencia con el plan niveles | **Esperar el cierre** del plan `2026-09-30-niveles-paquetes-plan-maestro-rdt` («ya debería cerrar»). |
| 5 | Q5 — rama/worktree | **OK**: carril nuevo `local-worker-5` + `.worktrees/local-worker-5` (puerto 3115), tras el cierre del plan niveles. |
| 6 | Q6 — Matriz de permisos | **Actualizar la matriz: debe existir una matriz actualizada en el flujo** (Fase E: tabla 1 del flujo 14 con las filas nuevas) y el artefacto «Matriz de permisos» actualizado por Victor en la misma tarea. |

Nota de sesión: esta sesión del Orquestador llega hasta el cierre del plan; la ejecución (Workers) corre en sesiones/agente aparte (Victor, 2026-10-02).

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
| 2026-10-02 | Plan y Punch List entregados (40 ítems, fases A–E); Estado `Planificando`, Gate 1 pendiente. | Planner |
| 2026-10-02 | **PD1:** bloque «Costo real de recursos» = filas `pr_recursos` (MO+HM) + fila «Sin resolver» = `AC − Σ`; legacy como nota no sumable; Total = AC. | Planner (delegado por el Spec) |
| 2026-10-02 | **PD2:** contrato `GET /api/curva-s?modo=`; `fisica` sin USD en la respuesta; `economica` con 403 sin permiso; sin `modo` se deriva por permiso. | Planner (delegado por el Spec) |
| 2026-10-02 | **PD3:** `puedeVerDashboard` y `puedeVerCurvaS` a los 13 roles; nuevo `puedeVerCurvaSEconomica` (5); el servidor fuerza Parcial si el rol no tiene economía. | Planner (delegado por el Spec) |
| 2026-10-02 | **PD4:** selector segmentado al patrón de `ToggleTipoDashboard`; no se usa `SelectorDashboard` legacy. | Planner (delegado por el Spec) |
| 2026-10-02 | **PD5:** lista cerrada de ocultados en Parcial (cabecera USD, resumen ejecutivo, semáforo, dona, desempeño por partida, columnas de costo, orden por desviación). | Planner (delegado por el Spec) |
| 2026-10-02 | **PD6:** Bloque E (PPC + Pareto) y enlace a Curva S visibles en ambos dashboards; el enlace lleva `?modo=fisica` sin economía. | Planner (delegado por el Spec) |
| 2026-10-02 | **Gate 1 aprobado:** plan, Punch List (40 ítems), tabla de 12 cambios a flujos y pre-autorizaciones en bloque; consultas 1–6 resueltas (Fase T nueva: proyecto de prueba de extremo a extremo hasta 50 % de avance; PD5 y PD6 confirmadas; espera de cierre del plan niveles; `local-worker-5`; matriz actualizada en el flujo + artefacto por Victor). | Victor |
| 2026-10-02 | **Modelo de los Workers:** todos los Workers del plan corren con **DeepSeek V4.1 Flash** (`opencode-go/deepseek-v4.1-flash`, corregido el 2026-10-02: el config tenía `opencode/deepseek-v4.1-flash`, proveedor inexistente), fijado en la config de opencode (`~/.config/opencode/opencode.jsonc`, agentes `general` y `explore`). La tabla «Modelos por rol» de `09-medicion-y-modelos.md` se actualiza al cierre (Fase E / paso 16b). | Victor |
| 2026-10-02 | **Tandas A, B y C cerradas** (commits `d40cd74`, `94a5f79`, `5e773c7` en `local-worker-5`). Sesión del Orquestador congelada tras lanzar C; la ejecución continuó en sesión nueva. | Orquestador |
| 2026-10-02 | **OP6:** al retomar, se encontró y abortó un merge en progreso `local-worker-5` → `main` de la app sin Gate 2 (política violada); `main` restaurado a `35ac5dd`, 0/0 con origin. | Orquestador |
| 2026-10-02 | **Tanda D cerrada** (~108 llamadas): 21 ítems Conforme (F03–F11, U02–U05, E01/E03/E04, V01, R01–R05); F12/F13 Observado (proyecto `PRUEBA-DASH` no creado por presupuesto); V03/V04 parciales. Sin cambios de código. Matices (a) y (b) de C confirmados. | Worker 1 · D |
| 2026-10-02 | Se lanzan en paralelo la **tanda T2** (F12: proyecto de prueba de extremo a extremo + F13 + pendiente V03/V04 en vivo) y el **Documentador (Fase E)**; tras E, Worker de código corto para P03 (restaurar filas del flujo 14 en `permisos.test.ts`). | Orquestador |
| 2026-10-02 | **Tanda T2 cerrada** (~71 llamadas): creado el servicio de prueba **PS-0009** `PRUEBA-DASH Servicio T2` (id `da33f1fa-0d2c-4cf6-adf3-2d723390b44d`) con DP (BAC US$ 4.482,54; 9 partidas HH/HM con costo) y cronograma (14 actividades). **V03 y V04 cerrados Conforme** (PATCH 403 con «Ver como»; López con OT ajena → 403). F12/F13 parciales: faltaba Paquetes → PM → RDTs. Sin código tocado. | Worker 1 · T2 |
| 2026-10-02 | **Tanda E cerrada** (Documentador, ~55 llamadas): flujos 11, 14, 16 y 21 editados según la tabla (iii) del Gate 1 (commit `d262395`); M1–M3 trasladadas a `03-aprendizaje-continuo/` (`2ec79de`); índices y `planes-futuros.md` actualizados (`0e757f3`); resumen + RB8 (`ffeeb74`); `verificar-referencias.py` 0 huérfanos / 0 rotos (R06 Conforme). B-H2 se agregó como **RB8** (no estaba volcada al libro). OP1–OP6 quedan para el Auditor. | Documentador · E |
| 2026-10-02 | **Tanda T3 cerrada** (~68 llamadas): **F12 y F13 Completados**. PS-0009 con paquete `PT-001` (9 partidas), Plan Maestro v2 APROBADO (22 asignaciones), 2 RDTs VALIDADOS → **50 % de avance** (BAC/PV 4.482,54; EV 2.241,27; AC 297,76). Bloque «Costo real de recursos»: Σ MO+HM = Total = AC = 297,76 (reconciliación exacta, sin «Sin resolver»). Curva S económica y física dibujadas con datos reales. **Bug fuera de alcance detectado (OP8):** APROBAR con asignaciones inline no las persiste. Sin código tocado. | Worker 1 · T3 |
| 2026-10-02 | **Tanda P03 cerrada** (~26 llamadas): `permisos.test.ts` vuelve a comparar las 4 filas nuevas del flujo 14 (mapa 5→9 filas × 13 = 117 celdas); 93 tests del archivo, suite 1063 verde, tsc 0. Commit **`98df43c`** en `local-worker-5`. | Worker 1 · P03 |

## Enlaces a progreso y evidencia homónimos

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-10-01-dashboard-economia-y-curva-s.md` (se crea al iniciar la implementación).
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-01-dashboard-economia-y-curva-s.md` (se crea al iniciar la implementación).
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-10-01-dashboard-economia-y-curva-s.md` (la escribe el Auditor tras la Fase E, fuera de este archivo).

## Libro de hallazgos

Formato de fila: `| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |`. Estados: `Registrada` → `Trasladada` (con enlace y commit) · `Descartada` (con motivo) · `Pendiente de decisión` (con quién decide). Los Workers no editan este archivo: dejan sus hallazgos en su resumen de cierre y el Orquestador los pasa aquí. Al final, el Documentador traslada cada fila a su destino y el Auditor verifica el traslado.

## Mejoras (de trabajo)

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| M1 | 2026-10-02 | Worker 1 (A) | A-H1: `permisos.test.ts` compara la tabla 1 del flujo 14 por ruta absoluta; mover permisos antes que el doc rompe la prueba. Se desacopló (mapa 7→5 filas + pruebas explícitas de los dos modos); Fase E re-añade las filas. | `03-aprendizaje-continuo/` | Trasladada | [`2026-10-02-desacoplar-prueba-permisos-del-flujo-14.md`](../../03-aprendizaje-continuo/2026-10-02-desacoplar-prueba-permisos-del-flujo-14.md) — `2ec79de` |
| M2 | 2026-10-02 | Worker 1 (D) | Con 22+ ítems con navegador, «una captura por ítem» no cabe en ~80 llamadas: conviene agrupar capturas por pantalla desde el brief. | `03-aprendizaje-continuo/` | Trasladada | [`2026-10-02-agrupar-capturas-por-pantalla-en-tandas-con-navegador.md`](../../03-aprendizaje-continuo/2026-10-02-agrupar-capturas-por-pantalla-en-tandas-con-navegador.md) — `2ec79de` |
| M3 | 2026-10-02 | Worker 1 (D) | `browser_resize` no aplicaba el viewport (seguía 1440); para móvil 390 px hubo que usar CDP `Emulation.setDeviceMetricsOverride`. | `03-aprendizaje-continuo/` | Trasladada | [`2026-10-02-viewport-movil-con-cdp-emulation.md`](../../03-aprendizaje-continuo/2026-10-02-viewport-movil-con-cdp-emulation.md) — `2ec79de` |
| M4 | 2026-10-02 | Worker 1 (T2) | Importar DP/cronograma reales por UI exige 2 pasos (analizar niveles → «Aprobar niveles») y cada POST del parser tarda 30–40 s: conviene reservar ~10 llamadas solo para esa carga en los briefs con datos de prueba. | `03-aprendizaje-continuo/` | Trasladada | [`2026-10-02-reservar-llamadas-importacion-datos-reales.md`](../../03-aprendizaje-continuo/2026-10-02-reservar-llamadas-importacion-datos-reales.md) — `f3af620` |
| M5 | 2026-10-02 | Worker 1 (T2) | `playwright_browser_file_upload` no era fiable: se usó `page.setInputFiles` con el fixture copiado a Temp con nombre ASCII (el original trae `N°`). | `03-aprendizaje-continuo/` | Trasladada | [`2026-10-02-tecnicas-de-verificacion-en-vivo-con-playwright.md`](../../03-aprendizaje-continuo/2026-10-02-tecnicas-de-verificacion-en-vivo-con-playwright.md) — `f3af620` |
| M6 | 2026-10-02 | Worker 1 (T2) | Para la verificación en vivo fue más barato forzar «Ver como» por `POST /api/ver-como` + `page.reload` que por el combobox de la interfaz. | `03-aprendizaje-continuo/` | Trasladada | [`2026-10-02-tecnicas-de-verificacion-en-vivo-con-playwright.md`](../../03-aprendizaje-continuo/2026-10-02-tecnicas-de-verificacion-en-vivo-con-playwright.md) — `f3af620` |
| M7 | 2026-10-02 | Worker 1 (T3) | Para un caller de la API de Plan Maestro: `APROBAR` **no** reemplaza a `GUARDAR_ASIGNACIONES`; hay que guardar el reparto antes de aprobar o la versión queda sin PV. | — | Pendiente de decisión | Conocimiento del sistema/API (no método): no se creó archivo ni se trasladó; decide Victor en Gate 2 |
| M8 | 2026-10-02 | Worker 1 (T3) | Los `window.*` guardados vía `browser_evaluate` se pierden entre llamadas tras ciertos renders: conviene re-`fetch`ar catálogos/plan dentro de cada evaluate de escritura. | `03-aprendizaje-continuo/` | Trasladada | [`2026-10-02-tecnicas-de-verificacion-en-vivo-con-playwright.md`](../../03-aprendizaje-continuo/2026-10-02-tecnicas-de-verificacion-en-vivo-con-playwright.md) — `f3af620` |
| M9 | 2026-10-02 | Worker 1 (T3) | Payload mínimo de RDT con varias actividades: `metradoProgramado`/`metradoEjecutado` por orden y personas con `horas:[{ordenActividad,horas}]`; el `wbs` y el paquete los fija el servidor desde el Plan. | — | Pendiente de decisión | Conocimiento del sistema/API (no método): no se creó archivo ni se trasladó; decide Victor en Gate 2 |

## Reglas de negocio acordadas en esta tarea

Se trasladan a su flujo al cerrar, previa consulta de cada contradicción a Victor (el destino de cada una ya está fijado por la tabla del Gate 1 (iii)).

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| RB1 | 2026-10-01 | Victor (Spec) | La Curva S tiene dos modos: económica (USD, los 5 roles con economía) y física (% avance físico: PV/BAC y EV/BAC, los 13 roles) | `04-flujos-de-negocio/21-curva-s.md` | Trasladada | [21-curva-s.md](../../04-flujos-de-negocio/21-curva-s.md) (§ Objetivo, regla 2) — `d262395` |
| RB2 | 2026-10-02 | Victor (Spec, resultado 1) | Dashboard Parcial sin ningún dato monetario para los 13 roles; Completo con todo más el bloque «Costo real de recursos»; ambos enlazan la Curva S | `04-flujos-de-negocio/11-dashboard.md` | Trasladada | [11-dashboard.md](../../04-flujos-de-negocio/11-dashboard.md) (§ Los dos Dashboards, Indicadores, Costo real de recursos) — `d262395` |
| RB3 | 2026-10-02 | Victor (Spec, resultado 5 + D1) | Accesos: Parcial y curva física para los 13 roles; Completo y curva económica para los 5 con economía; el servidor fuerza Parcial y rechaza con 403 el modo económico sin permiso | `04-flujos-de-negocio/14-accesos-y-restricciones.md` (+ artefacto «Matriz de permisos», Victor) | Trasladada (flujo); artefacto pendiente de Victor (P05) | [14-accesos-y-restricciones.md](../../04-flujos-de-negocio/14-accesos-y-restricciones.md) (tabla 1, nota ¹) — `d262395` |
| RB4 | 2026-10-02 | Victor (Spec, D2) | «Costo real de recursos» = Personal (HH) + Equipos (HM); balde `costo_legacy_sin_partida_acum` como nota aparte no sumable; materiales y subcontratos fuera; Total = AC; vista solo por recurso | `04-flujos-de-negocio/11-dashboard.md` | Trasladada | [11-dashboard.md](../../04-flujos-de-negocio/11-dashboard.md) (§ Costo real de recursos) — `d262395` |
| RB5 | 2026-10-02 | Worker 1 (B) | B-H1: en Parcial, el orden «mayor desviación de costo» se fuerza a `WBS` en el servidor aunque la URL traiga otro orden (es dinero derivado); la matriz igual llega en orden contractual | `04-flujos-de-negocio/11-dashboard.md` | Trasladada | [11-dashboard.md](../../04-flujos-de-negocio/11-dashboard.md) (§ Filtros) — `d262395` |
| RB6 | 2026-10-02 | Worker 1 (C) | C-H2: el modo físico necesita el BAC = `Σ pr_partidas.bac` (flujo 21 §8), leído en servidor y **no** devuelto en la respuesta de `modo=fisica` | `04-flujos-de-negocio/21-curva-s.md` | Trasladada | [21-curva-s.md](../../04-flujos-de-negocio/21-curva-s.md) (§ Fuentes de verdad, regla 9) — `d262395` |
| RB7 | 2026-10-02 | Worker 1 (D) | Aclaración de E01: la nota «serie real vacía» solo aparece cuando hay BAC (>0) y todas las EV del rango son 0; con `BAC=0` el mensaje es «Este servicio no tiene BAC…» y no se dibuja gráfico (D03) | `04-flujos-de-negocio/21-curva-s.md` | Trasladada | [21-curva-s.md](../../04-flujos-de-negocio/21-curva-s.md) (regla 10) — `d262395` |
| RB8 | 2026-10-02 | Worker 1 (B) | B-H2: el enlace a la Curva S desde el Dashboard Parcial lleva `?modo=fisica`; la lectura real del parámetro la hace el servidor | `04-flujos-de-negocio/11-dashboard.md` | Trasladada — fila agregada por el Documentador (B-H2 no se había volcado al libro) | [11-dashboard.md](../../04-flujos-de-negocio/11-dashboard.md) (§ La Curva S no vive en ningún Dashboard) — `d262395` |

## Observaciones sobre la política

| ID | Fecha | Quién (rol, tanda) | Qué | Estado |
|---|---|---|---|---|
| OP1 | 2026-10-02 | Worker 1 (A) | A-H2: R2/P03 anticipan un carril con `npm test` rojo entre A y E mientras las `00-reglas` exigen tests verdes; la tensión se resolvió ajustando el mapa de la prueba en A sin tocar el flujo | Pendiente de decisión — Auditor clasifica; Victor decide en Gate 2 |
| OP2 | 2026-10-02 | Worker 1 (B) | B-H3: el prompt de auditoría del plan dice que PD5 oculta «los 10 KPI» pero la lista cerrada oculta 6 KPI; el brief manda y se implementó la lista del brief | Pendiente de decisión — Auditor clasifica; Victor decide en Gate 2 |
| OP3 | 2026-10-02 | Worker 1 (C) | C-H1: PD4 dice «opción no permitida con `disabled` + `title`» pero U01 y `design.md` §254 piden `aria-disabled` accesible por teclado; se implementó `aria-disabled` (confirmado en vivo en D). Proponer PD4 como `aria-disabled` | Pendiente de decisión — Auditor clasifica; Victor decide en Gate 2 |
| OP4 | 2026-10-02 | Worker 1 (C→D) | C-H3: la interpretación de E01 (todas las EV=0 → no dibujar la serie real + nota; tabla con «—») quedó confirmada en la tanda D | Pendiente de decisión — Auditor clasifica; Victor decide en Gate 2 |
| OP5 | 2026-10-02 | Worker 1 (D) | El presupuesto de ~80 llamadas está subestimado para una tanda con Fase T + 22 ítems de Fase D con navegador y capturas (se usaron ~108); F12 quedó sin ejecutar y requiere la tanda T2 | Pendiente de decisión — Auditor clasifica; Victor decide en Gate 2 |
| OP6 | 2026-10-02 | Orquestador | Al retomar la sesión congelada se encontró en el repo de la app un **merge en progreso `local-worker-5` → `main` sin Gate 2** (17 archivos staged, sin conflictos), contrario a la política (el merge es solo tras Gate 2). Se abortó con `git merge --abort`; `main` restaurado a `35ac5dd` (0/0 con origin). Se desconoce qué sesión lo inició | Pendiente de decisión — Auditor clasifica; Victor decide en Gate 2 |
| OP7 | 2026-10-02 | Worker 1 (T2) | El alcance completo de F12 (adjudicar → DP/cronograma → partidas HH/HM → PM con asignaciones → aprobar → RDTs a ~50 % → validar) no cabe en ~60 llamadas: solo la carga de DP + cronograma con confirmación de niveles consume ~10 llamadas y >90 s de parser. Las tandas de creación de datos de extremo a extremo necesitan presupuesto propio mayor o dividirse | Pendiente de decisión — Auditor clasifica; Victor decide en Gate 2 |
| OP8 | 2026-10-02 | Worker 1 (T3) | **Bug detectado fuera del alcance del plan (no se tocó código):** `PATCH /api/plan-maestro` con `accion:'APROBAR'` acepta `asignaciones` inline, las usa solo para validar y aprueba, pero **no las persiste** (`src/app/api/plan-maestro/route.ts` §APROBAR solo inserta en la rama `GUARDAR_ASIGNACIONES`). Resultado: plan `APROBADO` con 0 asignaciones y PV US$ 0,00. En PS-0009 se destrabó sin código (versión nueva → `GUARDAR_ASIGNACIONES` → `APROBAR`). Latente para cualquier caller que asuma que APROBAR persiste | Pendiente de decisión — Victor decide en Gate 2: plan de arreglo aparte o `planes-futuros.md` |
| OP9 | 2026-10-02 | Worker 1 (T3) | Matiz a OP7: el bloqueo de T2 («PM sin paquetes») sí era destrabable en una sola tanda (~14 llamadas: vínculo faltante + 1 paquete + PM + repartir + aprobar). Medición real de la creación de datos de extremo a extremo: D ~108 (con 22 ítems), T2 ~71 (parcial), T3 ~68 (completó F12/F13) | Pendiente de decisión — Auditor clasifica junto con OP7 |

## Carpetas/archivos huérfanos

Ninguno detectado (tandas A, B, C y D). **Confirmado por el Documentador (tanda E, 2026-10-02):** sin huérfanos; no se borró nada. Si durante la auditoría aparece alguno, se reporta aquí sin borrar nada.

## Informe de Auditoría

Pendiente: el Auditor lo escribe tras la Fase E, en `docs/02-trabajo-activo/04-auditoria/` (formato `06-informe-auditoria.md`), fuera de este archivo. El prompt está en «Prompt del Auditor».

## Mensaje de cierre

Pendiente (formato `09-cierre.md`): merge a `main` tras el Gate 2, flujos 11, 14, 16 y 21 y artefacto «Matriz de permisos» actualizados, libro de hallazgos trasladado, verificación del Auditor y Gate 2 de Victor.

## Elementos postergados propuestos para planes futuros

- **Bug OP8:** `PATCH /api/plan-maestro` con `accion:'APROBAR'` y `asignaciones` inline valida pero no persiste las asignaciones (plan APROBADO con PV 0). Detectado en T3 sobre PS-0009; requiere plan de arreglo aparte (decide Victor en Gate 2).
- **TCPI** como KPI del Dashboard Completo (el fundamento lo lista; hoy no está).
- **EAC como línea proyectada** sobre la Curva S (hoy marcado "fuera de alcance" en el flujo 21).
- **Histograma de recursos (HH/HM)** planificado vs real.
