# 2026-09-30 — Plan: niveles del presupuesto y cronograma, paquetes de trabajo, Plan Maestro (lienzo) y RDT desde el Plan Maestro

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Plan del **Planner**, sobre los tres Specs aprobados en el Gate Spec del 2026-09-30. **Un solo plan** para los tres; hasta **4 Workers a la vez** sin pisarse. Briefs por tanda en `2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/`.

## Identificación y estado

- Tema: rediseño de la cadena Cronograma → Paquetes de Trabajo → Plan Maestro → RDT, con niveles de presupuesto y cronograma confirmados al importar.
- Fecha: 2026-09-30.
- Estado: **Planificando** (a la espera del Gate 1 de Victor).
- Gate 1: **pendiente**.

## Referencia al Spec aprobado

| Spec | Estado |
|---|---|
| [`2026-09-30-niveles-presupuesto-y-cronograma.md`](2026-09-30-niveles-presupuesto-y-cronograma.md) | Aprobado (Gate Spec, 2026-09-30) |
| [`2026-09-30-paquetes-y-plan-maestro-grilla.md`](2026-09-30-paquetes-y-plan-maestro-grilla.md) (incluye el Anexo de 4 semanas y las novedades verificadas) | Aprobado (Gate Spec, 2026-09-30) |
| [`2026-09-30-rdt-desde-plan-maestro.md`](2026-09-30-rdt-desde-plan-maestro.md) | Aprobado (Gate Spec, 2026-09-30) |

## Objetivo, alcance y no alcance

- **Resultado esperado:**
  - Al importar un DP o un cronograma, el sistema cuenta los niveles y el usuario confirma el rol de cada uno (Servicio, Área, Subpresupuesto, Paquete de partidas, Partida).
  - En Paquetes de Trabajo se declara actividad → partida → metrado y se agrupan las actividades en paquetes; una partida puede repartirse entre paquetes.
  - El Plan Maestro es un lienzo donde solo se coloca metrado por día (seis columnas por semana, Prog. y Real) y se crea cuando todo está repartido.
  - El RDT lista lo que está en el Plan Maestro y atribuye el real al paquete × partida; el PR sigue sumando por partida.
- **Alcance:** los tres Specs completos (ver sus secciones «Alcance»), más la fase de diseño previa a la interfaz y la verificación en vivo con un servicio de prueba dedicado.
- **No alcance:** Gantt con línea base y real (`planes-futuros.md`), 3WLA, multi-moneda, orden de trabajo, cambios al motor del PR, Dashboard y Curva S (solo pruebas que los lean), borrar columnas o tablas existentes.
- **Validación esperada:** pruebas unitarias de la lógica pura (incluido el anexo de 4 semanas), `tsc`, suite, lint comparado con `main`, build, pruebas cruzadas (F5-A), verificación en vivo con login real (F5-B y F5-C), 13 roles, móvil y regresión.

## Entorno, repositorios, ramas y worktrees

- Modo: local. Documentación en `pg_control_proyectos` (`main`, directo). Código en `py_control_proyectos_web`.
- **Verificado (2026-09-30):** `main` = `origin/main` = `45c9e0a` en la app; existe `.worktrees/local-worker-1` (rama `local-worker-1`, limpia, en `45c9e0a`); `.env.local` ya copiado ahí (autorización permanente de Victor para copiarlo a cada worktree). `node_modules` es un enlace: dev y build con `--webpack`. Comandos de `package.json`: `npm test` (`vitest run`, entorno `node`, `src/**/*.test.ts`, **sin pruebas de componentes**), `npm run lint`, `npm run build`. La última migración es la `072`.
- **Carriles propuestos** (la creación de ramas y worktrees requiere autorización explícita de Victor en este Gate 1):

| Carril | Rama | Worktree | Puerto | Tandas |
|---|---|---|---|---|
| 1 · Niveles | `local-worker-1` (existe) | `.worktrees/local-worker-1` | 3111 | F1-A · F1-B · F1-C |
| 2 · Plan Maestro | `local-worker-2` (nueva, desde `main`) | `.worktrees/local-worker-2` | 3112 | F3-A · F3-B · F3-C · F3-D |
| 3 · Paquetes | `local-worker-3` (nueva, desde `main`) | `.worktrees/local-worker-3` | 3113 | F2-A · F2-B · F2-C |
| 4 · RDT | `local-worker-4` (nueva, desde `main`) | `.worktrees/local-worker-4` | 3114 | F4-A · F4-B · F4-C |

- Las tandas de diseño (F0) y de documentación (F5-D) trabajan en `pg_control_proyectos` y no usan worktree de la app.
- La integración se hace **en la rama del carril 1** (`local-worker-1`, sin crear otra): el Orquestador une primero Paquetes, luego Plan Maestro, luego RDT. El merge a `main` ocurre **solo tras el Gate 2**.
- Con cuatro Workers, la regla de la mejora anterior «un solo worktree activo a la vez» se **reemplaza** por «un worktree por carril»; se mantienen tandas de 4 a 8 ítems, brief ≤ 8 KB y ~80 llamadas por sesión.

## Skills aplicables

Política vigente (flujo pasos 6, 8 y 12; `03-sesiones-contexto-y-handoff.md` «Inicio de cada chat»). Skills de `.claude/skills/` de `pg_control_proyectos`; **el repositorio de la app no tiene carpeta de Skills** (verificado 2026-09-30).

| Skill | Quién | Dónde se usa |
|---|---|---|
| `cerrar-tanda` | todo Worker | Al final de **toda** tanda (las 19). **Adaptación de este plan:** con varios Workers a la vez, sus pasos de estados, evidencia y traspaso se escriben en `resultados/<tanda>.md`, no en el plan, la evidencia ni el progreso compartidos (evita choques entre carriles); los demás pasos van igual. El Orquestador consolida |
| `verificar-permisos-por-rol` | Worker | F3-B (añade `puedeCrearVersionPlanMaestro` a `permisos.ts`), F5-A (edita `permisos.ts`, el registro de accesos y sus pruebas) y F5-C (permisos por rol en vivo con «Ver como») |
| `seguir-flujo-de-planes` | Orquestador | Al lanzar **cada ola** (seis) y **antes de escribir el mensaje de cierre** |
| Comprobación de uso | Auditor | Paso 12: comprueba que se usaron los Skills citados aquí y en los briefs, o que consta por qué no |

Todo Worker, antes de empezar, lista `.claude/skills/` de ambos repositorios y anota «Skills revisados» en su `resultados/<tanda>.md`; el Orquestador lo copia a la sección «Skills revisados» del progreso. Los 19 briefs y el índice de tandas nombran los Skills que corresponden a cada tanda.

## Fases y dependencias

Detalle completo, grafo y olas en `…-briefs/00-indice-de-tandas.md`.

| Fase | Qué es | Tandas | Depende de |
|---|---|---|---|
| F0 | Maquetas y `design.md` (Niveles, Paquetes, lienzo, paneles, selector RDT) | F0-A, F0-B | — |
| F1 | Niveles (lógica, datos e importación, pantallas) | F1-A, F1-B, F1-C | F1-C espera maquetas de F0-A |
| F2 | Paquetes (vínculos y API, pantalla, orden y estados) | F2-A, F2-B, F2-C | F2-B espera maquetas de F0-A |
| F3 | Plan Maestro (lógica, datos y API, lienzo, Prog./Real) | F3-A, F3-B, F3-C, F3-D | F3-C y F3-D esperan maquetas de F0-B |
| F4 | RDT (datos y catálogo, API, pantalla) | F4-A, F4-B, F4-C | F4-C espera la maqueta del selector (F0-B) |
| F5 | Integración, verificación en vivo, documentación | F5-A, F5-B, F5-C, F5-D | todas las anteriores; F5-B espera las migraciones aplicadas |

**Olas (≤ 4 Workers a la vez):** 1) F0-A · F1-A · F2-A · F3-A; 2) F0-B · F1-B · F3-B · F4-A; 3) F1-C · F2-B · F3-C · F4-B; 4) F2-C · F3-D · F4-C; 5) F5-A; 6) F5-B y luego F5-C y F5-D en paralelo. **Las tandas de datos y de lógica no esperan las maquetas**; solo las de interfaz.

**Puntos de control de Victor:** (1) este Gate 1; (2) revisión de las maquetas de F0-A y de F0-B antes de la ola 3; (3) aplicar las migraciones 073–084, una por una, antes de F5-B; (4) Gate 2.

### Matriz de propiedad de archivos (resumen; la completa está en el índice)

| Carril | Dueño de |
|---|---|
| 1 | `src/lib/niveles/**`, `src/lib/proyectos/bloqueo-recarga.ts`, `src/lib/dp/**`, `src/lib/cronograma/**`, API del DP y del cronograma, pantallas de DP, cronograma y agrupación de PR, `db/073–075` |
| 2 | `src/lib/plan-maestro/**`, API y pantalla del Plan Maestro, `WorkspaceShell.tsx` (ocultar paneles), `db/076–078`, y la función nueva `puedeCrearVersionPlanMaestro` en `permisos.ts` (única excepción al congelado) |
| 3 | `src/lib/paquetes-trabajo/**`, API y pantalla de Paquetes (incluye `vinculos/route.ts` nuevo), `db/079–081` |
| 4 | `src/app/api/rdts/**`, `src/lib/rdts/**` (incluye `real-por-clave.ts` nuevo), pantallas y tablas de RDT, `db/082–084` |
| Congelados hasta F5-A | `permisos.ts` (salvo la excepción), `registro-accesos.ts` y sus pruebas, `nav-proyecto.*`, `panel-*`, `matriz-accesos*`, `db/README.md`, `package.json`, `src/lib/pr/**`, `src/lib/dashboard/**`, `src/lib/curva-s/**` |

### Migraciones reservadas (hoy la última es la `072`)

| Carril | Rango | Nota |
|---|---|---|
| 1 | 073–075 | niveles y encabezados; `reemplazar_dp` |
| 2 | 076–078 | relaja `unique (plan_maestro_id, wbs)` (autorización expresa); columnas de línea; `motivo_version` |
| 3 | 079–081 | `paquete_trabajo_vinculos`; `orden` y `nivel` |
| 4 | 082–084 | `paquete_trabajo_id` en RDT; campos de derivadas |
| F5 | 085–086 | reserva |

Ninguna depende de otra (las claves foráneas apuntan a tablas que ya existen). Nadie las aplica desde el código: Victor las pega en el SQL Editor, **una por una y con su confirmación**.

## Asignación de roles

| Rol | Chat | Rama | Worktree | Estado |
|---|---|---|---|---|
| Orquestador | por nombrar (`local_1.orquestador_niveles-paquetes-plan-maestro-rdt`) | `main` | N/A | Activo |
| Planner | este plan | `main` | N/A | Plan entregado |
| Worker · diseño (F0) | por asignar | `main` (docs) | N/A | Pendiente del Gate 1 |
| Worker · carril 1 | por asignar por tanda | `local-worker-1` | `.worktrees/local-worker-1` | Pendiente |
| Worker · carril 2 | por asignar por tanda | `local-worker-2` | `.worktrees/local-worker-2` | Pendiente de autorización |
| Worker · carril 3 | por asignar por tanda | `local-worker-3` | `.worktrees/local-worker-3` | Pendiente de autorización |
| Worker · carril 4 | por asignar por tanda | `local-worker-4` | `.worktrees/local-worker-4` | Pendiente de autorización |
| Worker · documentación (F5-D) | por asignar | `main` (docs) | N/A | Pendiente |
| Auditor | por asignar | `main` | N/A | Pendiente |

Chats con el patrón `<entorno>_<jerarquía>.<rol>_<tarea>` (`03-entorno-git-y-worktrees.md`); un chat por tanda.

### Prompt de cada Worker

Plantilla en `…-briefs/00-indice-de-tandas.md` § «Plantilla del prompt de lanzamiento»: cada Worker lee `00-reglas-de-contexto.md` y **solo su brief**; los contratos, por sección. El Worker **no edita** el plan, el progreso ni la evidencia: cierra con `resultados/<tanda>.md`, que consolida el Orquestador. Sin push ni merge.

### Prompt del Auditor

Alcance: los tres Specs, este plan, la Punch List, los `resultados/*.md`, la evidencia y los flujos modificados. Primer chequeo con `git log` / `git branch --contains` (no de memoria): los commits están en las ramas de los carriles asignados y no en `main`; existieron chats de Worker separados. Segundo: apartados obligatorios trasladados a su destino. Además: que la **matriz de propiedad** se respetó (ningún archivo editado por dos carriles en una misma fase), que cada cambio a flujos corresponde a una fila aprobada de la tabla en bloque y que el texto final coincide con el código, y que el artefacto «Matriz de permisos» está al día. **Skills (paso 12):** comprueba que se usaron los Skills de la sección «Skills aplicables» y de los briefs (`cerrar-tanda` en las 19 tandas, `verificar-permisos-por-rol` en las tres que tocan permisos, `seguir-flujo-de-planes` por el Orquestador en cada ola y antes del cierre), o que consta por qué no. El informe se guarda como **archivo propio** en `docs/02-trabajo-activo/04-auditoria/2026-09-30-niveles-paquetes-plan-maestro-rdt.md` con la clasificación `APLICAR AHORA` / `PROPONER A RESPONSABLE` / `NO PROMOVER` / `PROPONER SKILL` (plantilla `06-informe-auditoria.md`); si falta la clasificación, el Orquestador lo devuelve al Auditor.

## Archivos / componentes afectados

Por carril, en la matriz de arriba y en el índice. Nuevos: `src/lib/niveles/**`, `src/lib/proyectos/bloqueo-recarga.ts`, `src/lib/plan-maestro/lienzo.ts`, `src/app/api/paquetes-trabajo/vinculos/route.ts`, `src/lib/rdts/real-por-clave.ts`, `src/components/plan-maestro/**`, `src/components/paquetes/**`; maquetas en `docs/05-diseno-y-referencias/mockups/`.

## Punch List embebida

Formato de `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia de cada ítem va en el archivo de evidencia homónimo (se crea al iniciar la ejecución). **Gate 1: pendiente.** Generada desde los briefs (mismo texto); 109 ítems en 19 tandas.

### F0-A — Maquetas de Niveles y de Paquetes de Trabajo

Brief: [`f0-tanda-a.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f0-tanda-a.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F0A-1 | F0-A | Maqueta HTML **«Importar DP: confirmación de niveles»**: cuenta de niveles encontrados; lista del presupuesto en orden; una **fila de muestra por grupo de hermanas** con desplegable de rol (Servicio, Área, Subpresupuesto, Paquete de partidas, Partida); roles propuestos por defecto; filas «para revisar»; botón de aprobar; aviso de **recarga bloqueada** (con plan aprobado: bloqueo duro; sin él: lista de lo que se perdería y confirmación). Muestra un presupuesto de 4 niveles y uno de 5 (el nivel 2 propone «Área») | Archivo `mockups/importar-dp-niveles.html` | Sin verificar |
| F0A-2 | F0-A | Maqueta de la confirmación de niveles del **cronograma** con sus roles propios y el mismo patrón | `mockups/cronograma-niveles.html` | Sin verificar |
| F0A-3 | F0-A | Maqueta de **Paquetes, paso «Declarar»**: a un lado el cronograma con jerarquía y **columna Metrado** (desplegable de partida pre-llenado, hitos atenuados con su marca, indicador de restante por partida); al otro el DP **solo partidas, solo consulta**; paneles laterales ocultos. Usa el ejemplo real: 06.03.01 a 06.03.07 (excavación, perfilado, cama de arena, instalación de bancoductos, suministro de afirmado, relleno, eliminación de material excedente) | `mockups/paquetes-declarar.html` | Sin verificar |
| F0A-4 | F0-A | Maqueta de Paquetes, paso **«Agrupar»**: botón «Crear paquete» (no chip); casillas al inicio de cada ítem salvo Servicio; nombre, nivel, guardar; el paquete con **marca visual** (color o borde), selección del paquete completo, **flechas arriba/abajo**, **plegar** (solo nombre); 06.03.01–06.03.06 agrupadas y 06.03.07 directa; una partida repartida entre dos paquetes con sus porciones | `mockups/paquetes-agrupar.html` | Sin verificar |
| F0A-5 | F0-A | Las cuatro maquetas muestran estados vacío, carga y error, versión móvil (390 px) y accesibilidad (`scope` en `th`, foco visible, teclado para mover y plegar) | Capturas o secciones visibles en cada archivo | Sin verificar |
| F0A-6 | F0-A | `design.md`: sección nueva para la **jerarquía en árbol con casillas**, la marca de paquete y el plegado, usando los tokens y componentes existentes (§4, §5, §8); sin inventar nombres de componentes que no existen en el código; versión y §15 actualizados | Diff de `design.md` | Sin verificar |
| F0A-7 | F0-A | `mockups/index.html` y `mockups/README.md` enlazan las cuatro maquetas; `resultados/F0-A.md` lista **preguntas de diseño para Victor** (máx. 6, una decisión por pregunta, sin códigos internos) | Enlaces funcionan | Sin verificar |

### F0-B — Maquetas del lienzo del Plan Maestro, paneles ocultables y selector del RDT

Brief: [`f0-tanda-b.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f0-tanda-b.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F0B-1 | F0-B | Maqueta HTML del **lienzo**: a la izquierda de una línea divisoria, columnas **fijas** (WBS, descripción, Und., metrado, costo unitario, **HH por unidad**); a la derecha, una **columna por día** con scroll horizontal, agrupadas por semana (sábado a viernes); encabezado con el **total del servicio**. Columnas de Tiempo (duración, inicio, fin) **no** van | `mockups/plan-maestro-lienzo.html` | Sin verificar |
| F0B-2 | F0-B | Por semana, **seis columnas**: avance físico, avance económico y HH programadas, cada uno **semanal y acumulado**, con rótulos que no se confundan (nombre, unidad), e **interruptor** para ocultar las acumuladas; semanas **plegables y expandibles** (plegada = una columna con sus totales) | Mismo archivo | Sin verificar |
| F0B-3 | F0-B | Filas: **paquetes plegables con subtotal**, partidas repetidas por paquete con su porción, partidas directas sin paquete, jerarquía por niveles; indicador por fila de **cuánto falta repartir**, indicador global y botón «Crear Plan Maestro» deshabilitado hasta el 100 % | Mismo archivo | Sin verificar |
| F0B-4 | F0-B | **Subfilas «Prog.» (editable) y «Real» (solo lectura)** con interruptor para ocultar lo real; real por paquete × partida; marca de «real fuera del rango programado» con semanas extendidas; estados `BORRADOR` y `APROBADO` (solo lectura) | Mismo archivo | Sin verificar |
| F0B-5 | F0-B | Maqueta del control de **ocultar y mostrar los paneles laterales** (escritorio), con el icono flotante del asistente sin tapar columnas, y la vista móvil (los paneles ya son un cajón) | `mockups/paneles-ocultables.html` o sección del lienzo | Sin verificar |
| F0B-6 | F0-B | Maqueta del **selector de actividad del RDT**: paquetes plegables con sus partidas, partidas directas aparte, **modo «por avance del paquete»** (se escribe la unidad de la guía; las demás partidas aparecen calculadas, en solo lectura), horas C/NC y materiales con el mismo selector, mensaje «sin Plan Maestro aprobado» | `mockups/crear-rdt-selector-paquetes.html` | Sin verificar |
| F0B-7 | F0-B | **Los números de la maqueta del lienzo coinciden con el anexo de 4 semanas** del Spec (totales 22,56 / 48,78 / 76,22 / 100 %, $ 8 200, 172 HH). Estados vacío, carga, error, móvil y accesibilidad. `design.md` (§3, §5, §8) actualizado, `mockups/index.html` y `README.md` enlazados, y `resultados/F0-B.md` con **preguntas de diseño para Victor** (máx. 6) | Comparación número a número + diff | Sin verificar |

### F1-A — Niveles: lógica pura (detección, roles, muestra, hermanas)

Brief: [`f1-tanda-a.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f1-tanda-a.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F1A-1 | F1-A | Tipos `RolNivel`, `RolNivelCronograma`, `MapaNiveles`, `NodoEstructura` (C1) y una función que calcula el **nivel de cada fila** a partir de su código WBS con puntos, soportando de 2 a N niveles | Prueba unitaria | Sin verificar |
| F1A-2 | F1-A | **Roles propuestos por defecto** según el número de niveles (tabla del Spec: 2 → Servicio/Partida; 3 → Servicio/Subpresupuesto/Partida; 4 → Servicio/Subpresupuesto/Paquete de partidas/Partida; 5 → Servicio/**Área**/Subpresupuesto/Paquete de partidas/Partida); el nivel 1 cuyo nombre coincide con el del servicio se propone como Servicio | Prueba con 2, 3, 4 y 5 niveles | Sin verificar |
| F1A-3 | F1-A | **Fila de muestra por grupo de hermanas** y **propagación** del rol elegido a las hermanas (mismo nivel y mismo padre) | Prueba | Sin verificar |
| F1A-4 | F1-A | Filas que **no siguen el patrón** de su grupo (profundidad distinta) quedan marcadas «para revisar» | Prueba | Sin verificar |
| F1A-5 | F1-A | Detector de profundidad para WBS **sin puntos o de ancho fijo** (por estructura de la hoja); verificado con los archivos reales de `docs/06-material-de-apoyo/Informacion para pruebas/` y, si ninguno tiene 5 niveles, con un **fixture sintético** rotulado como tal | Prueba + nota de qué archivos se usaron | Sin verificar |
| F1A-6 | F1-A | `construirArbol(filas, mapa): NodoEstructura[]` y agrupador por mapa, con pruebas sobre un presupuesto de 4 niveles y uno de 5; los servicios de 3 niveles típicos producen la **misma agrupación** que hoy (`agruparPorSubpresupuesto`) | Prueba de equivalencia | Sin verificar |

### F1-B — Niveles: datos, importación del DP y del cronograma, bloqueo de recarga

Brief: [`f1-tanda-b.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f1-tanda-b.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F1B-1 | F1-B | Migraciones 073–075: tablas de **niveles por servicio y origen** (DP o cronograma) y de **encabezados con código, nombre, nivel y rol**; `reemplazar_dp` los reconstruye (`create or replace` con la **firma de 13 parámetros** de `db/071`); lo ya importado queda con un mapa por defecto «pendiente de confirmar» equivalente a la convención actual. Idempotentes, sin borrar `dp_subpresupuestos` ni `dp_paquetes` | Archivos SQL + lectura crítica (sin aplicar) | Sin verificar |
| F1B-2 | F1-B | El parser del DP lee **encabezados de cualquier nivel** (no solo los patrones de 1 y 2 segmentos) y entrega filas para F1-A; las pruebas actuales de `parser*.test.ts` siguen verdes y los servicios de 3 niveles típicos producen lo mismo que hoy | `npm test` | Sin verificar |
| F1B-3 | F1-B | API de importar DP: devuelve **niveles detectados y propuesta**; guarda el mapa confirmado; si el usuario no confirma, guarda el mapa por defecto marcado pendiente | Prueba de API con datos simulados | Sin verificar |
| F1B-4 | F1-B | Cronograma: el parser y el informe guardan **niveles y roles propios**; el enlace con el DP por EDT sigue funcionando; `PATCH /api/cronograma` **acepta vínculos tarea ↔ partida sin metrado** y deja de exigir metrado > 0 y el 100 % por partida (esa regla pasa a Paquetes y al Plan Maestro) | Prueba + `npm test` | Sin verificar |
| F1B-5 | F1-B | `src/lib/proyectos/bloqueo-recarga.ts` (`evaluarRecarga`, contrato C1) y su uso en la importación del DP y en la subida del cronograma: con Plan Maestro `APROBADO` → **409 sin opción de confirmar**; sin él → exige `confirmarPerdida: true` tras el aviso con la lista (vínculos, paquetes, borrador del Plan Maestro). **El borrador no bloquea** | Pruebas de los tres casos | Sin verificar |
| F1B-6 | F1-B | Guardias intactas: rol sin permiso → 403; servicio inexistente → 400/404; `npx tsc --noEmit`, suite y lint comparado con `main` | Salida de comandos | Sin verificar |

### F1-C — Niveles: pantallas de confirmación, aviso de recarga y consumidores propios

Brief: [`f1-tanda-c.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f1-tanda-c.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F1C-1 | F1-C | Importar DP muestra el **paso de confirmación de niveles** según la maqueta: cuenta de niveles, lista en orden, fila de muestra por grupo con desplegable de rol, propuesta por defecto, filas «para revisar», aprobar | Lógica en módulo puro con prueba; `tsc` y build | Sin verificar |
| F1C-2 | F1-C | El cronograma tiene el mismo paso con sus roles. **Se retira de su pantalla** el bloque de vínculos con metrado, la lista «partidas incompletas» y la columna Hito (pasan a Paquetes, F2); la carga y la vista quedan | Prueba de la lógica + build | Sin verificar |
| F1C-3 | F1-C | **Aviso de recarga** en DP y cronograma: con Plan Maestro aprobado, bloqueo con mensaje; sin él, lista de lo que se perdería y confirmación explícita (`confirmarPerdida`) | Prueba de la lógica de mensajes | Sin verificar |
| F1C-4 | F1-C | Las pantallas **DP y PR agrupan según el mapa** (archivos propios: `proyectos/[id]/dp/**` y `proyectos/[id]/pr/page.tsx`), con el mismo aspecto para servicios de 3 niveles típicos | Prueba de equivalencia + build | Sin verificar |
| F1C-5 | F1-C | Estados **vacío, carga y error**, móvil (390 px) y accesibilidad del paso de niveles; `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Salida de comandos | Sin verificar |

### F2-A — Paquetes: vínculos, API y lógica (sin pantalla)

Brief: [`f2-tanda-a.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f2-tanda-a.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F2A-1 | F2-A | Migraciones 079–081: tabla `paquete_trabajo_vinculos` (PK, claves foráneas al vínculo `cronograma_actividad_partidas` con borrado en cascada, `unique (cronograma_actividad_id, dp_partida_id)`), más `orden` y `nivel` en `paquetes_trabajo`. **Se conservan sin uso** `paquete_trabajo_partidas` y `paquete_trabajo_programacion`. Idempotentes, con RLS de lectura como las de `db/072` | Archivos SQL + lectura crítica (sin aplicar) | Sin verificar |
| F2A-2 | F2-A | Lógica pura en `src/lib/paquetes-trabajo/`: suma del metrado declarado por partida contra el contractual (100 %) y **restante por partida**; hitos no cuentan; selección de jerarquía (**marcar una fila resumen marca sus hijas**, desmarcables); orden y movimiento; plegado. Copia de `sumarMetradoPorPartida` y `partidasConMetradoIncompleto` (hoy en `src/lib/cronograma/vinculos.ts`, que es del carril 1) | Pruebas unitarias | Sin verificar |
| F2A-3 | F2-A | `PUT /api/paquetes-trabajo/vinculos` (archivo nuevo): fija vínculos con metrado y la marca de hito (`requiere_partidas`); valida en servidor (partida del servicio, actividad con fechas, metrado > 0, hito sin metrado); llama `recalcular_pr_fechas_base`; permiso `puedeGestionarPaquetesTrabajo` | Prueba de API con datos simulados | Sin verificar |
| F2A-4 | F2-A | `POST` y `PATCH` de `/api/paquetes-trabajo` con la forma de C2: crear (nombre, nivel, modo, guía, vínculos), editar en `BORRADOR`, **mover** (orden), archivar; un vínculo en **un solo** paquete; una partida puede estar en varios; la guía debe estar entre las partidas del paquete; **sin fechas** | Pruebas | Sin verificar |
| F2A-5 | F2-A | `GET /api/paquetes-trabajo` devuelve paquetes con vínculos, actividades como `NodoEstructura[]` (hoy, con la jerarquía de `RESUMEN`/`TAREA`/`HITO`), partidas del DP para consulta y `restantePorPartida` | Prueba | Sin verificar |
| F2A-6 | F2-A | Guardias: rol sin permiso → 403; servicio inexistente o ajeno → 400/404 según alcance; ver para los 13 roles; `npx tsc --noEmit`, suite y lint comparado con `main` | Salida de comandos | Sin verificar |

### F2-B — Paquetes: pantalla de dos lados, declarar y crear paquete

Brief: [`f2-tanda-b.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f2-tanda-b.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F2B-1 | F2-B | Pantalla de **dos lados**: a un lado el cronograma con su jerarquía y la **columna Metrado**; al otro el DP mostrando **solo partidas, solo consulta** | Lógica en módulo puro con prueba; build | Sin verificar |
| F2B-2 | F2-B | **Declarar**: desplegable de partida en la celda Metrado pre-llenado por el enlace automático por EDT; metrado por vínculo; **hitos atenuados** con su marca; indicador de **restante por partida** | Prueba de la lógica + build | Sin verificar |
| F2B-3 | F2-B | Botón **«Crear paquete»** (dentro de la pantalla, no chip): casillas al inicio de cada ítem salvo Servicio, nombre, nivel, guardar; marcar una fila resumen marca sus hijas. `?accion=crear` (acción del panel, ya registrada) abre la pantalla **ya en modo crear** | Prueba de la lógica + build | Sin verificar |
| F2B-4 | F2-B | El paquete creado se ve con **marca visual** y al seleccionarlo se selecciona **completo**; una **partida repartida entre dos paquetes** se acepta y su suma se vigila (100 %) | Prueba con el caso de dos paquetes | Sin verificar |
| F2B-5 | F2-B | Fuera del formulario: fechas inicio y fin, «Repartir en días» y la lista vertical fecha → metrado; la pantalla ya no exige programación para guardar un paquete | Diff + build | Sin verificar |
| F2B-6 | F2-B | Permisos de interfaz: los 13 roles ven; solo administrador, jefe de proyectos y planner ven las acciones de escribir; `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Salida de comandos + prueba de las funciones de permiso | Sin verificar |

### F2-C — Paquetes: orden, plegado, edición y estados

Brief: [`f2-tanda-c.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f2-tanda-c.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F2C-1 | F2-C | **Mover arriba/abajo** un paquete con flechas (y con teclado); el orden se guarda (`PATCH … MOVER`) y se conserva al recargar | Prueba de la lógica de orden + prueba de API | Sin verificar |
| F2C-2 | F2-C | **Plegar y expandir** un paquete (plegado = solo su nombre); «plegar todo / expandir todo» | Prueba de la lógica de plegado | Sin verificar |
| F2C-3 | F2-C | **Editar** un paquete en `BORRADOR` (nombre, nivel, vínculos, modo, guía) y **archivarlo**; detalle con trazabilidad del paquete a la partida; un paquete validado o archivado no se edita | Prueba | Sin verificar |
| F2C-4 | F2-C | Estados **vacío, carga y error**, móvil (390 px) y accesibilidad (teclado para mover y plegar, foco visible, `scope`) | Comprobación por estructura + lista para F5 | Sin verificar |
| F2C-5 | F2-C | Prueba cruzada del caso de Victor: una partida de 10 unidades repartida 5 + 5 entre dos paquetes suma el 100 %; con 5 + 4 avisa el faltante; `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Salida de comandos | Sin verificar |

### F3-A — Plan Maestro: lógica pura del lienzo (totales, semanas, 100 %, real)

Brief: [`f3-tanda-a.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f3-tanda-a.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F3A-1 | F3-A | Tipos `LineaPlanMaestro`, `Asignacion`, `RealPorClave` y `claveReporte` (C3/C4) en `src/lib/plan-maestro/lienzo.ts` (+ `lienzo.test.ts`) | Prueba | Sin verificar |
| F3A-2 | F3-A | Totales por **línea, paquete y servicio**, cada medida **semanal y acumulada**: avance **económico** (metrado × precio), **HH** (metrado × HH por unidad) y avance **físico** (partida: metrado ÷ contractual; paquete y total: ponderado por costo = económico del grupo ÷ BAC del grupo) | Prueba | Sin verificar |
| F3A-3 | F3-A | **Caso de 4 semanas del Spec** como prueba: dos paquetes y una directa, totales exactos — Paquete 1: 26/58/82/100 %, Paquete 2: 25/50/75/100 %, directa: 0/0/50/100 %, total: 22,56 / 48,78 / 76,22 / 100 %; económico total $ 8 200 y por semana $ 1 850 / 2 150 / 2 250 / 1 950; HH totales 172 (47/52/39/34) | Prueba con los números del anexo | Sin verificar |
| F3A-4 | F3-A | **Validación del 100 %**: por línea (Σ días = `metradoLinea`) y por partida (Σ líneas = contractual), con la lista de líneas y partidas que faltan; tolerancia `0,000001` como en el código actual | Prueba | Sin verificar |
| F3A-5 | F3-A | Edición por bloques: **repartir uniforme** entre dos fechas, **escribir el total de una semana y repartirlo** entre sus días, redondeo que lo absorbe el último día; ampliar el rango de días antes o después | Prueba | Sin verificar |
| F3A-6 | F3-A | **Real**: agrega `RealPorClave` a semana y acumulado (metrado, EV = metrado × precio, HH); extiende las semanas si hay real fuera del rango programado | Prueba | Sin verificar |
| F3A-7 | F3-A | Semanas de **sábado a viernes** con `generarSemanasPlanMaestro` (existente) sin duplicar su lógica; `npx tsc --noEmit`, suite y lint comparado con `main` | Salida de comandos | Sin verificar |

### F3-B — Plan Maestro: datos y API (líneas, borrador, aprobar)

Brief: [`f3-tanda-b.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f3-tanda-b.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F3B-1 | F3-B | Migraciones 076–078: relajar `unique (plan_maestro_id, wbs)`; agregar `metrado_linea`, `actividad_id`, `clave_reporte`, `paquete_trabajo_id`, `paquete_codigo`, `paquete_nombre`, `paquete_orden`, `hh_und_partida` a `plan_maestro_partidas`, y `motivo_version text` a `proyecto_plan_maestro`. **Cambio de restricción: el handoff lo marca «requiere autorización expresa de Victor»**; nada se borra | Archivos SQL + lectura crítica (sin aplicar) | Sin verificar |
| F3B-2 | F3-B | `POST /api/plan-maestro`: crea `BORRADOR` **sin exigir paquetes** ni leer `paquete_trabajo_programacion`; líneas desde vínculos (en paquete o directos) con metrado > 0; si hay versión aprobada, parte de sus asignaciones y **exige `motivo`** (se guarda en `motivo_version`); sin copia de programación | Prueba con datos simulados | Sin verificar |
| F3B-3 | F3-B | `GET /api/plan-maestro` → `{ plan, lineas, asignaciones, semanas, reales }` (C3); `reales` viene de un **adaptador** que lee `realPorClaveReporte` (C4, carril 4) y mientras no exista devuelve `[]` | Prueba | Sin verificar |
| F3B-4 | F3-B | `PATCH` guardar y aprobar: valida Σ días = `metradoLinea` por línea **y** Σ líneas = contractual por partida; reemplaza la versión aprobada anterior y llama `recalcular_pr_planificado` (RPC existente); mensajes que dicen qué líneas o partidas faltan | Prueba | Sin verificar |
| F3B-5 | F3-B | **Partida repetida sin romper nada**: prueba unitaria de que el PV, el planificado del PR y la Curva S **suman** las líneas repetidas de un mismo WBS (lectura de `pr/page.tsx`, `dashboard/page.tsx`, `api/curva-s/route.ts` y del SQL de `db/061` y `db/070`; si algo no suma, se reporta, no se edita) | Prueba + nota | Sin verificar |
| F3B-6 | F3-B | Guardias: ver = `puedeVerPlanMaestro` **y alcance por OT**; gestionar = `puedeGestionarPlanMaestro` (administrador, jefe de proyectos, planner); **crear una versión nueva cuando ya hay una aprobada = `puedeCrearVersionPlanMaestro` (administrador y jefe de proyectos; función nueva en `permisos.ts` con su prueba para los 13 roles; es una restricción más estricta que la de gestionar y se registra en el handoff para la tabla del flujo 14)**; 403 por rol, 400/404 por servicio; `npx tsc --noEmit`, suite y lint comparado con `main` | Salida de comandos | Sin verificar |

### F3-C — Plan Maestro: lienzo (columnas, semanas, seis columnas) y ocultar paneles

Brief: [`f3-tanda-c.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f3-tanda-c.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F3C-1 | F3-C | **Ocultar y mostrar los paneles laterales** desde el shell (escritorio), recordado por usuario; en móvil los paneles siguen como cajón; el icono del asistente no tapa columnas | Lógica en módulo puro con prueba; build | Sin verificar |
| F3C-2 | F3-C | **Lienzo**: columnas fijas a la izquierda (WBS, descripción, Und., metrado, costo unitario, **HH por unidad**), una **columna por día** deslizante, entrada de metrado por día, fila de **total del servicio** | Prueba de la lógica + build | Sin verificar |
| F3C-3 | F3-C | **Semanas plegables** (plegada = una columna con sus totales), editar por bloques, **escribir el total de la semana y repartirlo**, ampliar el rango de días antes o después con las fechas de la actividad **sombreadas como guía** (no limitan) | Prueba de la lógica | Sin verificar |
| F3C-4 | F3-C | **Seis columnas por semana** (físico, económico, HH; semanal y acumulado) con **interruptor** para ocultar las acumuladas, rotuladas con nombre y unidad | Prueba de los totales con el caso del anexo | Sin verificar |
| F3C-5 | F3-C | Indicador por fila de **cuánto falta repartir** y global; el botón de crear (aprobar) el Plan Maestro solo se habilita con el 100 %; el `BORRADOR` se guarda parcial | Prueba de la lógica | Sin verificar |
| F3C-6 | F3-C | **Se retiran** «Generar propuesta» (copia) y «Editar distribución diaria»; `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Diff + salida de comandos | Sin verificar |

### F3-D — Plan Maestro: paquetes, Prog./Real, estados y rendimiento

Brief: [`f3-tanda-d.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f3-tanda-d.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F3D-1 | F3-D | Filas de **paquete plegables con subtotal**; la **partida repetida** aparece en cada paquete con su porción; partidas **directas** sin paquete; jerarquía por niveles con `NodoEstructura[]` (simulado hasta la integración) | Prueba de la lógica de agrupación + build | Sin verificar |
| F3D-2 | F3-D | **Subfilas «Prog.» y «Real»** con interruptor para ocultar lo real; el real se muestra por **clave de reporte** (paquete × partida); marca «real de versión anterior» si el paquete ya no existe en esta versión | Prueba con `RealPorClave` simulado | Sin verificar |
| F3D-3 | F3-D | Estados: `APROBADO` = solo lectura; `BORRADOR` guardado parcial y retomable; **nueva versión** con motivo (administrador y jefe de proyectos) que parte de la aprobada | Prueba de la lógica de estados | Sin verificar |
| F3D-4 | F3-D | Estados **vacío, carga y error**, móvil (390 px), teclado y accesibilidad del lienzo; el icono del asistente no tapa columnas | Comprobación por estructura + lista para F5 | Sin verificar |
| F3D-5 | F3-D | **Rendimiento** con un servicio grande (≥ 150 partidas × ≥ 120 días simulados): medición del render; si hace falta, virtualización de filas o columnas sin perder columnas fijas; `npx tsc --noEmit`, suite, lint comparado con `main` y build | Medición + salida de comandos | Sin verificar |

### F4-A — RDT: datos, catálogo desde el Plan Maestro y real por clave

Brief: [`f4-tanda-a.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f4-tanda-a.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F4A-1 | F4-A | Migraciones 082–084: `paquete_trabajo_id uuid null → paquetes_trabajo(id)` en `rdt_actividades` y en `rdt_actividad_partidas` (nulo = partida directa); campos para las filas **derivadas** del modo por avance del paquete (`declaracion_id`, `es_derivada`; nombres **por confirmar con Victor** en el Gate 1). Se conservan `dp_partida_id`, `wbs` y la PK. Idempotentes | Archivos SQL + lectura crítica (sin aplicar) | Sin verificar |
| F4A-2 | F4-A | Lógica pura: **reparto del % del paquete** a sus partidas (reutiliza `repartirAvanceDelPaquete` de `src/lib/paquetes-trabajo/`, que es del carril 3: **lo importas, no lo editas**) y validaciones de la declaración por paquete | Pruebas | Sin verificar |
| F4A-3 | F4-A | `GET /api/rdts/catalogos` devuelve `estadoPlanMaestro` y `lineasPlanMaestro` por **clave de reporte** (C5) desde el Plan Maestro aprobado, en vez de `dp_partidas`/`dp_subpresupuestos`; sin plan aprobado → estado claro | Prueba con datos simulados | Sin verificar |
| F4A-4 | F4-A | `src/lib/rdts/real-por-clave.ts`: `realPorClaveReporte(admin, proyectoId)` (C4): metrado de actividades `D` de partes `VALIDADO`, horas de `rdt_tareo_horas` sin MOI y fecha `fecha_lima`, agregados por clave y día | Prueba con datos simulados | Sin verificar |
| F4A-5 | F4-A | **Clave estable entre versiones** del Plan Maestro: prueba de que un RDT validado contra el paquete P y la partida X se sigue atribuyendo a `P:X` aunque haya una versión nueva (con otro id de línea) | Prueba | Sin verificar |

### F4-B — RDT: API de partes (crear, validar, modo por avance del paquete)

Brief: [`f4-tanda-b.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f4-tanda-b.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F4B-1 | F4-B | **Crear parte** (`POST /api/rdts/partes`): exige Plan Maestro aprobado (mensaje claro sin él) y valida en servidor que el `(paquete, partida)` de cada actividad D, y de cada C/NC y material, pertenece al Plan Maestro aprobado vigente del servicio | Pruebas de los casos válido, sin plan y fuera del plan | Sin verificar |
| F4B-2 | F4-B | **Validar** (`PATCH` de `partes/[id]`): escribe el vínculo con **partida y paquete**; las actividades C/NC y los materiales cargan a una clave (paquete × partida o directa) elegida por el supervisor | Prueba | Sin verificar |
| F4B-3 | F4-B | **Modo «por avance del paquete»**: se declara la unidad de la guía; el servidor calcula y guarda las filas derivadas de las demás partidas (mismo %), **de solo lectura**; en modo «por partidas» se declara cada una | Prueba del reparto y de que el cliente no puede falsearlas | Sin verificar |
| F4B-4 | F4-B | **Reasignar paquete** de un RDT mientras esté `REGISTRADO` o `REVISADO`, no cuando esté `VALIDADO`; el PR **suma por partida** aunque la partida esté en dos paquetes (prueba de lectura sobre el motor existente; no se edita) | Prueba | Sin verificar |
| F4B-5 | F4-B | Permisos intactos (crear: administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo; validar o rechazar: administrador, jefe de proyectos, jefe de oficina técnica; rechazar uno validado: administrador y jefe de proyectos); 403 por rol, 400/404 por servicio; `npx tsc --noEmit`, suite y lint comparado con `main` | Pruebas de las funciones de permiso para los 13 roles + salida de comandos | Sin verificar |

### F4-C — RDT: pantalla de Crear RDT, consolidado y status

Brief: [`f4-tanda-c.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f4-tanda-c.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F4C-1 | F4-C | El selector de actividad de **Crear RDT** lista los **paquetes (plegables) y sus partidas** del Plan Maestro, más las **partidas directas** aparte; elegir una rellena descripción, WBS y unidad y fija el tipo D, como hoy | Lógica en módulo puro con prueba; build | Sin verificar |
| F4C-2 | F4-C | **Modo «por avance del paquete»** en la pantalla: se escribe la unidad de la guía y las demás partidas aparecen calculadas, en solo lectura | Prueba de la lógica + build | Sin verificar |
| F4C-3 | F4-C | Actividades **C/NC** y **materiales** usan el mismo selector para elegir el paquete × partida al que cargan | Prueba | Sin verificar |
| F4C-4 | F4-C | **Status** y **Consolidado RDTs** muestran el paquete y permiten filtrarlo, sin perder los filtros actuales ni el aspecto con servicios sin paquetes | Prueba de la lógica de filtros + build | Sin verificar |
| F4C-5 | F4-C | Estados **vacío, carga y error**, móvil (390 px), accesibilidad y el mensaje **«sin Plan Maestro aprobado»** (no se puede crear RDT); `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Salida de comandos | Sin verificar |

### F5-A — Integración: unir los cuatro carriles y pruebas cruzadas

Brief: [`f5-tanda-a.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f5-tanda-a.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F5A-1 | F5-A | La rama integrada compila sin conflictos sin resolver; los conflictos que aparecieron (se esperan ninguno por la matriz de propiedad) están resueltos con el criterio del dueño del archivo y anotados. `db/README.md` lista las migraciones 073 a 084 con su orden de aplicación | `git status`, diff de `db/README.md` | Sin verificar |
| F5A-2 | F5-A | `npm test`, `npx tsc --noEmit`, `npm run lint` (comparado con el total medido en `main` `45c9e0a`, que mides tú primero) y `npx next build --webpack` en verde; sin deuda de lint nueva en los archivos tocados | Salida de comandos | Sin verificar |
| F5A-3 | F5-A | **Prueba cruzada del anexo de 4 semanas** de punta a punta en un archivo nuevo de pruebas: paquetes con una partida repartida → líneas del Plan Maestro → totales semanales y acumulados → planificado del PR (suma por partida) → PV de la Curva S; los números del anexo salen exactos | Prueba verde | Sin verificar |
| F5A-4 | F5-A | **Prueba cruzada del RDT**: el real se atribuye al paquete × partida; el PR suma por partida aunque esté en dos paquetes; la clave sigue igual tras una versión nueva del Plan Maestro | Prueba verde | Sin verificar |
| F5A-5 | F5-A | Los datos simulados se reemplazan por los reales: las pantallas de Paquetes, lienzo y selector del RDT consumen `NodoEstructura[]` de `src/lib/niveles/`; `reales` del lienzo sale de `realPorClaveReporte`; sin adaptadores vacíos | Diff + pruebas | Sin verificar |
| F5A-6 | F5-A | Permisos y accesos: las pruebas existentes de `registro-accesos`, `matriz-accesos`, `panel-*` y `nav-proyecto` siguen verdes **sin chip nuevo**; `puedeCrearVersionPlanMaestro` (administrador y jefe de proyectos) probada con los 13 roles; la acción «Crear paquete» del panel abre Paquetes en modo crear | Pruebas verdes | Sin verificar |

### F5-B — Servicio de prueba dedicado y verificación en vivo (niveles, paquetes, Plan Maestro)

Brief: [`f5-tanda-b.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f5-tanda-b.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F5B-1 | F5-B | Se crea el **servicio de prueba dedicado** (nombre marcado `PRUEBA-…`, con el portafolio que indique el Orquestador) — autorizado por Victor — y se le importa un **DP de 5 niveles** (real si existe; si no, el sintético de F1-A, rotulado) | Captura de la ficha y URL | Sin verificar |
| F5B-2 | F5-B | Importación con **confirmación de niveles**: cuenta los niveles, propone roles (nivel 2 = Área), fila de muestra que se propaga, filas «para revisar»; luego se importa el **cronograma** con su propio mapa | Capturas + snapshot de texto | Sin verificar |
| F5B-3 | F5-B | **Paquetes**: declarar actividad → partida → metrado (pre-llenado por EDT), marcar un hito, crear dos paquetes con **una partida repartida entre ambos** (suma 100 %), marca visual, seleccionar completo, mover y plegar; «Crear paquete» desde el panel abre en modo crear | Capturas + comprobación del restante en 0 | Sin verificar |
| F5B-4 | F5-B | **Plan Maestro**: lienzo con columnas fijas y días, semanas plegables, seis columnas; repartir todos los metrados; el botón de crear solo se habilita al 100 %; aprobar; los totales coinciden con el cálculo de la lógica; el PV aparece en la **Curva S** | Capturas + números comparados | Sin verificar |
| F5B-5 | F5-B | **Recarga**: con Plan Maestro aprobado, cargar de nuevo el DP o el cronograma queda bloqueado; con solo un borrador, se permite tras el aviso y la confirmación | Capturas + resultado de la API | Sin verificar |

### F5-C — Verificación en vivo: RDT, permisos por rol, móvil y regresión

Brief: [`f5-tanda-c.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f5-tanda-c.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F5C-1 | F5-C | **RDT desde el Plan Maestro**: Crear RDT lista los paquetes y partidas del Plan Maestro (no el DP); se crea un RDT que declara en una partida repartida y en un paquete «por avance del paquete»; se valida; el **real aparece en el lienzo** por paquete × partida (físico, EV y HH) y el **PR** muestra la partida una sola vez con la suma | Capturas + números del PR | Sin verificar |
| F5C-2 | F5-C | **Permisos por rol** con «Ver como» (`POST /api/ver-como`): los 13 roles ven y pueden exactamente lo que dicen las tablas 1 y 2 del flujo 14 en Cronograma, Paquetes, Plan Maestro y Crear RDT, incluida la **versión nueva** del Plan Maestro (administrador y jefe de proyectos); APIs sin efecto para las acciones (403 por rol = rechazado) | Tabla rol × pantalla + resultados de API. Usa el Skill `verificar-permisos-por-rol` | Sin verificar |
| F5C-3 | F5-C | **Móvil (390 px) y estados**: paso de niveles, Paquetes, lienzo y Crear RDT en vacío, carga y error; lienzo con scroll horizontal y columnas fijas; icono del asistente sin tapar columnas | Capturas | Sin verificar |
| F5C-4 | F5-C | **Regresión** en un servicio existente (PS-0004 o PS-0005): DP, PR, Dashboard y Curva S se ven igual que antes del plan; los filtros del Consolidado y Status de RDTs siguen funcionando | Comparación con la línea base medida al inicio de la tanda | Sin verificar |
| F5C-5 | F5-C | **Limpieza de datos de prueba** solo con autorización expresa de Victor (el Orquestador la confirma en el prompt): se eliminan el servicio de prueba y los registros marcados por id exacto, con SELECT previo y verificación posterior; evidencia de lo eliminado | Lista de ids + verificación | Sin verificar |

### F5-D — Documentación: flujos, matriz de permisos y trazabilidad

Brief: [`f5-tanda-d.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/f5-tanda-d.md)

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| F5D-1 | F5-D | Flujos **09 y 15** según la tabla aprobada: paso de confirmación de niveles, mapa por servicio y origen, recarga bloqueada, vínculo con metrado que se declara en Paquetes, cronograma solo carga y vista | Diff + casilla «aplicado» en la tabla | Sin verificar |
| F5D-2 | F5-D | Flujos **19 y 20**: paquete sin fechas, partida repartida entre paquetes, lienzo del Plan Maestro, seis columnas, versión nueva con motivo, sin paquete permitido | Diff + casilla | Sin verificar |
| F5D-3 | F5-D | Flujos **06, 18, 10 y 21**: el RDT lista lo del Plan Maestro, real por paquete × partida, columnas fijas del lienzo (sin Tiempo), el PR suma por partida, sin cambio de fórmulas | Diff + casilla | Sin verificar |
| F5D-4 | F5-D | Flujos **14 y 16** y el artefacto **«Matriz de permisos»** (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT): filas de la tabla 2 (cronograma, paquetes, Plan Maestro, versión nueva), sección «Accesos requeridos para paquetes (pendiente)» reescrita, ocultar paneles, acción «Crear paquete» | Diff + artefacto actualizado | Sin verificar |
| F5D-5 | F5-D | Índices: `04-flujos-de-negocio/README.md`, `02-trabajo-activo/01-planes/README.md` (estado del plan), `06-material-de-apoyo` si aplica; `planes-futuros.md` sin cambios salvo lo que Victor pida | Diff | Sin verificar |
| F5D-6 | F5-D | **Trazabilidad**: para cada flujo de la tabla, el texto final coincide con lo implementado (comprobado contra el código de la rama integrada); las **mejoras de trabajo** del plan (`resultados/*.md`) trasladadas a `03-aprendizaje-continuo/`; las reglas de negocio integradas **en el flujo**, nunca en un archivo aparte | Lista por flujo con el resultado | Sin verificar |


## Riesgos y bloqueos

| # | Riesgo | Mitigación |
|---|---|---|
| 1 | Doce migraciones sobre tablas en uso (PR, Curva S, RDT) | Son aditivas y sin dependencias entre sí; se aplican una por una con confirmación de Victor; F5-A y F5-B las verifican antes de cualquier prueba en vivo |
| 2 | Relajar `unique (plan_maestro_id, wbs)` cambia una restricción | Requiere autorización expresa de Victor (Gate 1); prueba de que PR, Dashboard y Curva S suman las líneas repetidas (F3B-5, F5A-3) |
| 3 | Cuatro carriles editando a la vez | Matriz de propiedad, contratos definidos de antemano, archivos congelados hasta F5-A, rangos de migraciones reservados y cierre por `resultados/<tanda>.md` (nadie edita el mismo archivo compartido) |
| 4 | La maqueta no se aprueba a tiempo | Los carriles de datos y lógica no esperan; solo F1-C, F2-B, F3-C, F3-D y F4-C |
| 5 | Las HH reales por semana no existen conectadas hoy (el Plan Maestro las deja en 0) | F4-A las construye desde `rdt_tareo_horas`; las horas de equipos no entran (no hay tabla puente) |
| 6 | Sin pruebas de componentes en el repositorio | Toda la lógica de pantalla en módulos puros con prueba; la verificación visual se concentra en F5-B y F5-C |
| 7 | Rendimiento del lienzo (muchas filas × muchos días) | F3D-5 mide con ≥ 150 partidas × ≥ 120 días y virtualiza si hace falta |
| 8 | `072` pudo no estar aplicada en algún entorno | Se comprueba antes de F5-B (consulta con el cliente de servicio, sin imprimir valores) |
| 9 | Dos navegadores en paralelo se pisan | Solo F5-B y F5-C usan navegador, uno a la vez |
| 10 | Contradicciones Spec ↔ flujos nuevas | Registradas abajo como preguntas del Gate 1; ningún flujo se edita sin su fila aprobada |
| 11 | Cerrar sin haber subido todo (ocurrió con el plan anterior) | Este plan no cierra sin merge y push de **ambos** repositorios y sin informe del Auditor con clasificación (ver «Cierre») |

## Tabla en bloque de cambios a flujos (Gate 1)

Una sola aprobación de Victor cubre a todos los Workers de F5-D (mismo método que el plan de paneles). Política: un cambio que choca con lo escrito se implementa en **todos** los flujos afectados. Cada fila se marca «aplicado» en F5-D solo tras comprobarla contra el código.

| Flujo | Dice hoy | Pasaría a decir | Aplicado |
|---|---|---|---|
| **06 RDT** | El supervisor elige partidas del DP agrupadas por subpresupuesto; «toda actividad registrada (D, C y NC) se carga a una partida» | Elige **paquetes y partidas del Plan Maestro aprobado** (o partida directa); sin Plan Maestro aprobado no se puede crear RDT; C/NC y materiales cargan a un paquete × partida; modo «por avance del paquete» (se declara la unidad de la guía, las demás se calculan en solo lectura); un RDT se reasigna de paquete mientras no esté `VALIDADO`. Roles sin cambio | ☐ |
| **09 Importar DP** | Tres fases (forma, fondo, observación); subpresupuesto y paquete de partidas por patrón de código de 1 y 2 segmentos | Se suma el **paso de confirmación de niveles** (cuenta de niveles, roles por desplegable, fila de muestra por grupo, filas «para revisar»); las tres fases se conservan; **recarga bloqueada** con Plan Maestro aprobado y, sin él, aviso de lo que se perdería y confirmación | ☐ |
| **10 PR** | `metrado_planificado_acum` = suma de asignaciones del Plan Maestro aprobado por partida; fechas base desde el vínculo cronograma ↔ partida | Sin cambio de fórmulas. Se aclara que la suma es **por partida** aunque esté repartida en varios paquetes, y que el vínculo con metrado se declara en Paquetes | ☐ |
| **14 Accesos** (tabla 2) | «Subir / reemplazar cronograma»; «Gestionar Plan Maestro (crear / congelar línea base)»; «Gestionar paquetes de trabajo» (administrador, jefe de proyectos, planner) | Mismo conjunto de roles. Se ajusta el texto: paquetes incluye declarar vínculos con metrado y hitos; Plan Maestro = programar y crear (aprobar); **fila nueva: «Crear una versión nueva del Plan Maestro» solo administrador y jefe de proyectos**; nota de recarga bloqueada. Sección «Accesos requeridos para paquetes (pendiente)» reescrita a lo implementado | ☐ |
| **14 Accesos** (tabla 1) | Plan Maestro ver: roles con economía + planner; Cronograma y Paquetes: 13 roles | Sin cambio | ☐ |
| **15 Cronograma** | Vínculo con metrado exacto y 100 % por partida editados en su pantalla; columna Hito; «Relación con Paquetes» (fechas de paquetes); Gantt como «fase 2, no construida» | El cronograma **solo carga y muestra**, con su mapa de niveles; el vínculo simple tarea ↔ partida y el enlace automático por EDT se conservan; el metrado y los hitos se declaran en Paquetes; recarga bloqueada; Gantt remitido a `planes-futuros.md` | ☐ |
| **16 Paneles** | «Paquetes de trabajo» como chip informativo; «Crear paquete» como acceso rápido; panel izquierdo con Recursos de empresa mostrar/ocultar | Se suma **ocultar y mostrar los paneles laterales** (escritorio, recordado por usuario); «Crear paquete» abre Paquetes en modo crear; el asistente flotante no tapa columnas del lienzo. Sin chip nuevo | ☐ |
| **18 Control de avance** | Columnas fijas del Plan Maestro: WBS, Área, Disciplina, Frente, Paquete, código, descripción, unidad, metrado, precio, BAC, HH contractuales, duración, inicio base, fin base, método; «paquete opcional» en el RDT | Columnas fijas del lienzo: **WBS, descripción, Und., metrado, costo unitario y HH por unidad** (las demás y las de Tiempo: ver pregunta 3 del Gate 1); seis columnas por semana (físico, económico y HH, semanal y acumulado, rotuladas para no mezclarlas); subfilas Prog./Real; el real se declara contra paquete × partida | ☐ |
| **19 Paquetes** | Datos del paquete con Área, Disciplina, Frente, unidad, meta, responsable, fechas opcionales y tipos estándar/flexible; avance ponderado por pesos; «no se duplican partidas activas, salvo distribución parcial autorizada» | Paquete = **nombre, nivel, modo de medición, partida guía y orden**; agrupa vínculos actividad × partida; **sin fechas**; una partida repartida entre paquetes es la regla general y suma 100 %; el avance se declara por partida o por la guía (los pesos quedan superados). Ver pregunta 4 del Gate 1 | ☐ |
| **20 Plan Maestro** | Distribución diaria desde los paquetes (`paquete_trabajo_programacion`); «Generar propuesta» copia; sin paquete no hay Plan Maestro; «el RDT debe usar un WBS existente en el DP» | **Lienzo** que se llena en `BORRADOR` (guardado parcial), se crea (aprueba) al repartir el 100 %; sin paquete permitido (partidas directas); versión nueva con motivo; el RDT usa paquetes y partidas del Plan Maestro; real por clave; recarga bloqueada con plan aprobado | ☐ |
| **21 Curva S** | PV desde `plan_maestro_asignaciones × plan_maestro_partidas.precio_unitario`; EV por `rdt_actividad_partidas × dp_partidas.precio_unitario` | Sin cambio de fórmulas; se aclara que las líneas repetidas por partida se suman y que el vínculo del RDT lleva el paquete sin afectar el EV | ☐ |
| **Artefacto «Matriz de permisos»** | Sin la fila de versión nueva ni la redacción de paquetes | Actualizado con el flujo 14 (misma tarea) | ☐ |

## Preguntas para el Gate 1 (una decisión por pregunta; lenguaje simple)

1. **Ramas y worktrees.** ¿Autorizas usar `local-worker-1` (ya existe) y crear `local-worker-2`, `local-worker-3` y `local-worker-4` desde `main`, cada una con su carpeta en `.worktrees/`? Sin esto no hay cuatro Workers en paralelo.
2. **Revisión de maquetas.** ¿Confirmas que revisarás las maquetas (Niveles, Paquetes, lienzo, paneles ocultables y selector del RDT) antes de que se construya la interfaz? Mientras tanto avanzan solo los carriles de datos y lógica.
3. **Columnas fijas del lienzo.** El flujo 18 hoy lista más columnas (Área, Disciplina, Frente, BAC, HH contractuales y método de medición). Recomiendo solo las del Spec (WBS, descripción, Und., metrado, costo unitario, HH por unidad), con BAC y HH contractuales en la fila de total. ¿Conforme?
4. **Datos del paquete (flujo 19).** Recomiendo que el paquete tenga solo nombre, nivel, modo de medición, partida guía y orden, y retirar Área/Disciplina/Frente (el Área la da el mapa de niveles), unidad y meta, responsable, tipos estándar/flexible y los pesos por partida. ¿Conforme, o quieres conservar alguno?
5. **Real del paquete.** Contradicción que aparece al unir los Specs: la línea del Plan Maestro es actividad × partida, pero el RDT declara contra paquete × partida. Recomiendo que lo **programado** se edite por línea (actividad × partida) y lo **real** se vea por paquete × partida. ¿Conforme?
6. **Modo «por avance del paquete» en el RDT.** Recomiendo que el servidor guarde una fila derivada de solo lectura por cada partida del paquete (mismo %), agrupadas por una declaración. La alternativa es una sola fila de declaración. ¿Cuál prefieres?
7. **Permiso nuevo.** Crear una **versión nueva** del Plan Maestro, cuando ya hay una aprobada, solo administrador y jefe de proyectos (hoy «gestionar» incluye al planner). ¿Confirmas esa restricción para que entre en la matriz y el flujo 14?
8. **Migraciones.** Son 12 (073–084). ¿Las aplicarás tú una por una en el SQL Editor, y autorizas expresamente relajar la restricción de WBS único del Plan Maestro (076–078)?
9. **Tabla de cambios a flujos.** ¿Apruebas en bloque la tabla de arriba (con lo que respondas a las preguntas 3 a 7) para que el Worker de documentación la aplique sin volver a preguntar?

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-09-30 | Tres Specs aprobados juntos; un solo plan los reparte; hasta 4 Workers en paralelo si el plan lo indica | Victor |
| 2026-09-30 | Fase de diseño previa: las maquetas de Paquetes y del lienzo se diseñan y se aprueban antes de construir la interfaz | Victor |
| 2026-09-30 | Servicios existentes de prueba; se autoriza crear un servicio de prueba dedicado; PS-0006 ya no existe | Victor |
| 2026-09-30 | Política nueva: el informe del Auditor es un archivo propio en `02-trabajo-activo/04-auditoria/`, no va dentro del plan | Victor |
| 2026-09-30 | Política de Skills incorporada al plan a pedido del coordinador: `cerrar-tanda` en toda tanda (adaptado al cierre por `resultados/<tanda>.md`), `verificar-permisos-por-rol` en F3-B, F5-A y F5-C, `seguir-flujo-de-planes` por el Orquestador en cada ola y antes del cierre; el Auditor comprueba su uso | Coordinador / Planner |
| 2026-09-30 | Preguntas del Gate 1 sobre carpetas de trabajo, maquetas, columnas fijas del lienzo y datos del paquete: Victor pidió dejar por defecto las opciones propuestas por el Orquestador (autorizar las tres carpetas de trabajo nuevas; revisar las maquetas antes de construir la interfaz; columnas fijas del Spec; paquete con nombre, nivel, modo de medición, partida guía y orden) | Victor |
| 2026-09-30 | Columnas adicionales del lienzo (área, disciplina, frente, costo total, HH totales, método de medición y otras): se ofrecen con el botón «Personalizar campos», el mismo que ya usan Status de Requerimiento y otras pantallas (`src/components/ui/PersonalizarCampos.tsx` y `src/lib/ui/campos-visibles`); no se crea otro selector de columnas | Victor |
| 2026-09-30 | **Gate 1, respuestas de Victor a las seis preguntas restantes:** (1) sí: lo programado se edita por línea (actividad × partida) y lo real se ve por paquete × partida, para mejorar la reportabilidad; (2) sí: en el RDT, modo «por avance del paquete», una fila derivada de solo lectura por partida; (3) sí: crear una versión nueva del Plan Maestro, cuando ya hay una aprobada, solo administrador y jefe de proyectos; (4) **las migraciones las aplican los Workers** (Victor ya dejó las credenciales; si no pueden, avisan), y se autoriza relajar la restricción de WBS único: **una partida se puede repetir en el Plan Maestro**; (5) sí: se aprueba en bloque la tabla de cambios a flujos; (6) sí: cada Worker entrega su resumen de cierre al Orquestador antes de declarar terminada su tanda, en un archivo propio por tanda; el Orquestador lo consolida en el progreso y, al terminar la última fase, se traslada a su destino (mejora de política, ya en el estándar) | Victor |
| 2026-09-30 | Credenciales de base de datos: están en la carpeta `C:\Users\BRANDY\Downloads\DIARIO` (nombres de variable `PR_DB_URL` y `SUPABASE_ACCESS_TOKEN`; el `.env.local` de la app solo tiene la URL y las dos llaves de acceso REST, que no permiten crear tablas). Regla: ningún valor se copia a archivos del repositorio, briefs, logs ni capturas; se leen en el momento por el script de migración. Antecedente: `PR_DB_URL` fue inalcanzable desde un sandbox sin salida IPv6 y la vía alterna fue la Management API de Supabase | Orquestador, por indicación de Victor |
| 2026-09-30 | Decisiones de método del Planner (a confirmar en el Gate 1): integración en la rama del carril 1; cierre de tanda por `resultados/<tanda>.md`; navegador solo en F5; `permisos.ts` congelado salvo una función | Planner |

## Enlaces a progreso, evidencia y auditoría homónimos

Se crean **solo cuando inicie la ejecución** (el Orquestador, desde las plantillas `03-progreso.md` —con su sección «Skills revisados»— y `04-evidencia.md`):

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`
- Resultados por tanda: `2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/resultados/<tanda>.md`

## Mejoras (de trabajo)

Ninguna todavía. Se llena en el momento en que ocurre cada hallazgo.

## Reglas de negocio acordadas en esta tarea

Las de los tres Specs (ver sus apartados) se trasladan a su flujo al cerrar, por la tabla en bloque de arriba. Nuevas de este plan: ninguna todavía.

## Carpetas/archivos huérfanos

- `FormularioPlanMaestro.tsx` todavía contiene «Editar distribución diaria» (el plan del 23-sep daba por eliminada esa edición): se retira en F3C-6.
- `paquete_trabajo_partidas` y `paquete_trabajo_programacion` quedan sin uso y **se conservan**; `dp_subpresupuestos` y `dp_paquetes` se conservan hasta migrar todos los consumidores. Se reportan a Victor al cerrar; nada se borra sin su autorización.

## Informe de Auditoría

Se guarda como archivo propio (política nueva del 2026-09-30): `docs/02-trabajo-activo/04-auditoria/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`. Este plan solo enlaza a él; el informe no se escribe aquí. Pendiente.

## Mensaje de cierre

Pendiente. **No se declara cerrado el plan** hasta cumplir, en este orden (política vigente, pasos 13 y 16–18 del flujo y memoria `cierre-de-plan-completo`): informe del Auditor **con clasificación** emitido; Gate 2 con la **autorización del push de la app** pedida a Victor; merge de la rama integrada a `main` de la app; mejoras de política y Skills agnósticos aprobados aplicados en el mismo cierre; `git rev-list --left-right --count origin/main...main` en **ambos** repositorios sin commits pendientes; y recién entonces el mensaje de cierre, sin códigos internos.

## Elementos postergados propuestos para planes futuros

- Nota en el ítem del 3WLA de `planes-futuros.md`: que reutilice el lienzo del Plan Maestro (solo si Victor lo pide).
- Retirar `paquete_trabajo_partidas`, `paquete_trabajo_programacion`, `dp_subpresupuestos` y `dp_paquetes` una vez que nada los use (requiere autorización expresa).
- Nombre del rol extra cuando un archivo trae más de 5 niveles (pendiente del Spec de Niveles).
