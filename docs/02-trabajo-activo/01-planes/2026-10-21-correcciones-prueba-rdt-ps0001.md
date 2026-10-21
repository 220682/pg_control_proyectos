# Correcciones de la prueba del RDT en PS-0001

## Identificación y estado

- Tema: cerrar los vacíos que dejó la prueba funcional del RDT (19.10.2026, PS-0001 TECNET) y repetir la prueba con un guion actualizado.
- Fecha: 2026-10-21.
- Estado: `En ejecución` — Gate Spec aprobado por Victor (2026-10-21); Gate 1 aprobado el mismo día (equipo, modelos, tandas y entorno como se propone abajo). El Lote 0 (desplegar restricciones) quedó autorizado por Victor el mismo día y **se ejecutó el 2026-10-21**: app `ddb18ee` en `main`, 2146 pruebas y build en verde, pendiente de verificación en producción (día 3 de la prueba v2). `db/095` y `db/114` quedaron fuera.

Puertas:

- Gate Spec: `aprobado por Victor (2026-10-21)`
- Gate 1: `aprobado por Victor (2026-10-21)`
- Gate 2: `pendiente`

Fuentes: informe final `01_pg_planeamiento/vpc_trabajo/servicios/PS-167-2026_.../..._prueba-rdt.md`; [log de ejecución](../06-pruebas/03-prueba-rdt-ps0001-ejecucion.md); [plan de la prueba](../06-pruebas/02-prueba-rdt-ps0001-plan.md). Respuestas de Victor del 2026-10-21 en el Registro de decisiones.

## Spec

### Qué se encontró y qué se decidió

| # | Vacío de la prueba | Decisión de Victor (2026-10-21) | Lote |
|---|---|---|---|
| 1 | Se acepta un RDT con fecha futura; el corte queda en hoy y el SPI sale sin sentido (4,89) | Bloquear la fecha futura | 1 |
| 2 | Curva S semanal: una parte lee la semana completa y la otra solo los días ya ejecutados | Que ambas lean la misma cantidad de días | 1 |
| 3 | Restricciones escritas en la actividad no generan registro (pantalla sin desplegar) | Desplegar y dejar «pendiente de verificación» | 0 |
| 4 | Las HH de la transversal 1.1 entran a las HH reales y al IP | Aplicar la regla ya decidida | 3 |
| 5 | Cargos con horas pero sin tarifa (cuestan 0 sin avisar) | Resolver al importar el presupuesto y exigir tarifa; aviso con el nombre que no existe | 2 |
| 6 | «Met.», «Met. acum.», «Met. rest.» y «Avance del paquete» muestran los de la partida, no los del paquete | Arreglar | 4 |
| 7 | «Met. prog.» y la descripción no se autocompletan | Arreglar | 4 |
| 8 | Equipos: no se pueden elegir partidas derivadas ni se ve el paquete | **Quitar la partida del equipo**: el equipo ya no se asigna a una partida | 4 |
| 9 | El motivo del rechazo es poco visible para el autor | Revisar y mejorar | 4 |

Los menores (columna HM del Status, columna «Paquete» sin directas, mensaje transitorio del Plan Maestro, rótulo «Sin resolver») entran en el Lote 4 sin decisión aparte.

### Lote 0 — Desplegar restricciones (punto 3)

La función ya está implementada (db/113 aplicada, pantalla y API). **Estado verificado el 2026-10-21:** el árbol de trabajo de la app tiene cambios sin commit de otros trabajos mezclados con los de restricciones (Foto de campo, avisos, matriz de accesos, `db/095`, `db/114`) y `origin/main` va un commit adelante de `main` local. Por eso el Worker git:

1. Trae `origin/main`.
2. Separa y commitea solo lo de restricciones (archivos nuevos y los hunks de `catalogo.ts`, `permisos.ts`, `registro-accesos.ts`, `matriz-base-flujo14.ts`, `parte.ts`, `FormularioCrearRdt.tsx`, `rdts/partes/route.ts`, `EditorInforme`/`EditoresBloque` que le correspondan).
3. Corre `npm test` y el build, y empuja a `main` (Vercel).
4. Anota en el plan de Lote 4 de observaciones y en el flujo 22: «Restricciones: desplegado el <fecha>, **pendiente de verificación**».

La verificación es el caso de restricción del guion v2 (día 3).

### Lote 1 — Fechas y cortes (puntos 1 y 2)

- **Fecha futura:** el selector de fecha del RDT tiene máximo = hoy (zona Lima) y el servidor responde 400 `FECHA_FUTURA` si la fecha del parte es posterior a hoy. Aplica a crear, corregir y subir RDT. Con esto el corte del PR, el Dashboard y la Curva S vuelve a ser coherente, y las Inasistencias de cualquier RDT son consultables.
- **Curva S semanal:** el PV, el EV y el AC de la fila de una semana se cortan en la misma fecha. Una semana en curso o con corte a mitad se muestra como «S1 al 21-10» (parcial), no como «posterior a la fecha de corte». La lectura de la tarjeta usa esa misma fecha. Cuando la semana completa ya pasó, la fila es la semana entera.
- Sin regla nueva de negocio: el flujo 21 ya dice que la serie real no pasa de la fecha de corte; se agrega la regla de «misma fecha para PV y real» y la del bloqueo de fecha futura en el flujo 06.

### Lote 2 — Cargos, tarifas e importación (punto 5)

**Hallazgo sobre cómo está hoy** (código leído, solo lectura):

- La regla «el presupuesto no se importa si un recurso suyo no existe en la base de datos» **ya existe** (`detectarRecursosNoResueltos` en `src/lib/dp/equivalencias.ts`): compara los cargos y equipos del presupuesto contra el catálogo de la empresa o contra una equivalencia guardada del servicio. En PS-0001 esa regla no falló: los cargos del presupuesto sí existen en el catálogo.
- El vacío es el **sentido contrario**: el personal está cargado con cargos del catálogo (OPERARIO, OFICIAL, INGENIERO DE SEGURIDAD) que **no son filas de este presupuesto** (el presupuesto trae OPERARIO CIVIL, OFICIAL CIVIL, INGENIERO SSOMA). Nadie comprueba eso, y el cálculo (`tarifas-servidor.ts`) los deja en costo 0.
- Lo que propone Victor («si el presupuesto dice INGENIERO SSOMA y el personal tiene INGENIERO DE SEGURIDAD, se asigna al que existe en el presupuesto») **es la equivalencia por servicio**, y el cálculo ya la usa (`recursos_cargo_equivalencias`, por proyecto). Lo que falta es la regla y la pantalla que la pidan.

**Cambios:**

1. **En Importar DP**, tras la conciliación actual, nueva sección: «Cargos del catálogo de personal sin fila en este presupuesto». Para cada cargo del personal que pueda trabajar en el servicio sin fila de mano de obra en HH (ni MOI) en el presupuesto, el usuario elige a qué fila del presupuesto equivale (OPERARIO → OPERARIO CIVIL; OFICIAL → OFICIAL CIVIL; INGENIERO DE SEGURIDAD → INGENIERO SSOMA). La equivalencia es **del servicio** (otro servicio puede mapear OPERARIO a OPERARIO MECANICO). Sin resolver, el botón de importar queda bloqueado y el aviso nombra cada cargo: «El cargo X no existe en el presupuesto de este servicio».
2. **En Crear/Corregir RDT**: si se elige a una persona cuyo cargo no tiene tarifa en el presupuesto del servicio (ni MOI ni equivalencia), se rechaza con un mensaje que dice qué hacer («pida al jefe de proyectos declarar la equivalencia en Importar DP»). Así ninguna hora entra con costo 0 sin que se vea. La validación en servidor repite la comprobación (el navegador no basta).
3. **Aviso `rdt.recursos_sin_tarifa`**: existe en el código (`avisarRecursosSinTarifa`) y se invoca al validar, pero en la prueba no llegó. **Lectura del Planner (2026-10-21):** el recorrido de código es correcto (`resolverYCongelarTarifas` devuelve `sinResolver` y el PUT de validación avisa a administrador y jefe de proyectos); la función existe desde el 2026-09-21. No se puede explicar solo leyendo código; el Worker del Lote 2 lo diagnostica **consultando la base** (tabla de avisos del 19 al 23.10 y qué devolvió `sinResolver`) antes de tocarlo. Hipótesis: el aviso se creó pero se cerró o quedó en la cola compartida; o el cargo resolvió como MOI en vez de sin resolver (las horas sin costo no serían «sin tarifa» sino «MOI»). Con el punto 2 dejará de dispararse casi siempre, pero queda para equipos y datos antiguos.
4. **Dashboard «Recursos sin tarifa»**: la tarjeta lista los nombres y su enlace va a esa lista (hoy solo cuenta y abre `/recursos/personal`).
5. La fila del presupuesto en unidad **MES** (p. ej. OPERARIO 0,5 MES) no es tarifa por hora: se ignora para HH, como hoy, y el mensaje del punto 1 lo dice.

### Lote 3 — Regla de HH (punto 4)

Decidido el 2026-10-19 y ratificado hoy: **las HH de partidas transversales no entran a las HH reales ni al IP**. Se muestran aparte, informativas. Supuesto del Orquestador, a confirmar en el Gate 1: las HH ganadas tampoco incluyen la parte de la transversal (si no, el IP mezclaría un lado con y otro sin). Aplica en la app (PR, Dashboard, Plan Maestro) y en los flujos 06, 10, 11 y 18.

### Lote 4 — Formulario y pantallas (puntos 6 a 9 y menores)

- **Métricas del paquete:** en el formulario, «Met.», «Met. acum.», «Met. rest.» y «Avance del paquete» salen de la línea del paquete (30 / 101), no de la partida (267). Cada paquete muestra su propio avance, no el mismo para todos.
- **Autocompletar:** al elegir la actividad se trae «Met. prog.» del Plan Maestro por día y la descripción de la partida.
- **Equipos sin partida:** se elimina la columna/selector de partida (WBS) de la fila de equipo. El equipo se declara con nombre, HM, stand-by y estado. **Efecto a registrar:** el costo de equipos sigue sumando al costo real del servicio, pero deja de repartirse por partida; el PR muestra «costo atribuido por partida» solo con personal. Contradice lo escrito en los flujos 06, 10 y 18: Victor lo ordenó el 2026-10-21 y se edita en la tanda de documentación.
- **Motivo del rechazo:** visible en la fila RECHAZADO del Status y en «Revisar RDT» del autor; «Revisar RDT» de un rechazado no suma su propio metrado al acumulado.
- **Menores:** la columna HM del Status cuenta operativas + stand-by (igual que el PR); la columna «Paquete» del Status incluye las directas; el Plan Maestro no ofrece «crear borrador» mientras carga; el rótulo «Sin resolver» de las transversales pasa a «Transversales (prorrata)».

### Lote 5 — Documentación y trazabilidad

Flujos afectados: 06 (RDT: fecha futura, equipos sin partida, métricas, rechazo, restricciones), 09 (importar DP: equivalencias de cargos del personal), 10 (PR: HH, costo por partida, rótulos), 11 (Dashboard: HH, lista sin tarifa), 18 (control de avance: HH), 21 (Curva S: misma fecha), 22 (restricciones: estado del despliegue), 14 (accesos: sin cambio previsto; se revisa). Cada contradicción con lo escrito se confirma con Victor antes de editar, y la **Matriz de permisos** se actualiza si cambia una interfaz, acción o acceso (política del 2026-09-28). El Auditor verifica la trazabilidad antes del Gate 2.

### Lote 6 — Prueba v2

Se corre con [la guía v2](../06-pruebas/04-prueba-rdt-ps0001-v2-guion.md) y el [calculador de esperados](../../../scripts/esperados_rdt_ps0001.py). Precondición: Victor rechaza o borra los 5 RDT de prueba y decide sobre el supervisor a cargo (Braulio).

### Verificación de la prueba anterior (resaltado pedido por Victor)

**Los parámetros que el plan esperaba, ¿estuvieron correctos?** Recalculados hoy con el calculador, **independiente de la app** y desde el presupuesto y el cronograma:

| Familia | ¿El esperado del plan original se cumplió? |
|---|---|
| Valor ganado, % físico, metrados, programado, Plan Maestro, PPC | **Sí.** EV 1.284,44 / 2.978,37 / 4.827,61 / 6.549,78 / 8.287,52 coinciden con el plan original y con la app (centavos). |
| Costo real (AC) | **No** con el esperado original: D5 esperado 9.167 a 9.528, mostrado 7.754,89. La diferencia se reconcilia **exacta**: personal 3.810,76 esperado contra 2.020,66 mostrado = 1.790,10 de horas con costo 0 por cargos sin tarifa; el resto es materiales (la app usa 5.389,32). |
| HH reales / IP | **No**: 290,72 y 0,76 contra 268 y 0,788 (regla nueva) o 0,809 del plan. Por las HH de la transversal y las horas de cargos sin tarifa. |
| SPI y PV del PR | **No** desde el RDT del día 2: PV al 19.10 contra EV de hasta el 23.10 (SPI 4,89). |

Qué falló en el método de la sesión anterior, y no debe repetirse: **desde la tanda 2 los «esperados» se recalcularon con las reglas que la app mostraba** (tarifas sin resolver, materiales 5.389,32, HH con la transversal) y los cuadros dijeron «OK». Eso comprueba que la app acumula de forma consistente, **no que la regla sea la correcta**. Además se sustituyeron personas (CAPATAZ por un OPERARIO, etc.), de modo que la prueba nunca ejercitó las tarifas previstas. El informe final sí lista las diferencias contra el plan original, pero su veredicto «los cálculos cuadran» es cierto solo para avance, valor ganado y metrados. La guía v2 corrige esto: los esperados se fijan antes de empezar, no se editan durante la prueba y cualquier diferencia es hallazgo.

## Objetivo, alcance y no alcance

- Resultado esperado: los nueve vacíos corregidos o con decisión escrita, y una prueba v2 con esperados independientes que pase.
- Alcance: app `py_control_proyectos_web` (RDT, importación del DP, PR, Dashboard, Curva S, Plan Maestro) y los flujos 06, 09, 10, 11, 18, 21 y 22.
- No alcance: Foto de campo y APK (otro plan), informe diario con fotos, observación 2 de partidas transversales (otro plan), contenido del PDF del RDT.
- Validación esperada: `npm test` y build de la app; prueba v2 sin diferencias; Auditor con trazabilidad al día.

## Entorno, repositorios, ramas y worktrees

Propuesta para el Gate 1: trabajar **directo en `main`** de la app, sin rama ni worktree (así se trabajó hasta ahora y `AGENTS.md` lo fija por defecto). Estado verificado el 2026-10-21 tras el Lote 0: `main` = `origin/main` = `ddb18ee`; solo quedan sin seguimiento `db/095` y `db/114` (de otros trabajos, no se tocan). La migración nueva del Lote 3 será `db/115`, aplicada solo con autorización de Victor.

## Skills aplicables

`seguir-flujo-de-planes` (al activar y al cerrar), `cerrar-tanda` (cada tanda), `trasladar-hallazgos` (tanda final), `verificar-permisos-por-rol` (Lote 4 si cambia algún acceso).

## Fases y dependencias

Lote 0 primero y sin depender de nada. Lotes 1, 2, 3 y 4 son independientes entre sí (el 2 toca importación y el formulario; el 4 toca el formulario: ordenar 2 antes de 4 para no pisarse). Lote 5 al final de cada lote. Lote 6 al final, con los RDT de prueba limpios.

## Equipo del plan

Propuesta para el Gate 1 (modelos según `09-orquestacion-y-modelos.md`; sin Opus), en tandas de 4 a 8 ítems con brief de hasta 8 KB:

| Tanda | Contenido | Quién | Modelo |
|---|---|---|---|
| T1 | Lote 1 (fecha futura y Curva S) | Worker 1 | Sonnet |
| T2 | Lote 3 (regla de HH, `db/115`, PR, Dashboard, Plan Maestro) | Worker 1 | Sonnet |
| T3 | Lote 2 (cargos, tarifas, Importar DP, diagnóstico del aviso) | Worker 2 | Sonnet |
| T4 | Lote 4 (formulario, equipos sin partida, rechazo, menores) | Worker 2, tras T3 | Sonnet |
| T5 | Lote 5 (flujos 06, 09, 10, 11, 18, 21, 22 y Matriz) | Documentador | Haiku |
| T6 | Auditoría de trazabilidad | Auditor | Sonnet |

T1 y T3 pueden ir en paralelo (no comparten archivos); T2 va después de T1 porque ambos tocan el PR y el Dashboard. Los commits y el push los hace el Orquestador, uno por tanda, con `npm test` y build en verde.

## Archivos / componentes afectados

Mapa del Planner (lectura, 2026-10-21; los Workers confirman líneas exactas):

| Lote | Archivos de la app |
|---|---|
| 1 | `src/app/api/rdts/partes/route.ts` (crear: ya valida `fechaLima`), `src/app/api/rdts/partes/[id]/route.ts` (corregir), ruta de RDT subidos, `FormularioCrearRdt.tsx` (`type="date"`, línea ~1122), `src/app/api/curva-s/route.ts`, `src/lib/curva-s/curva-s.ts`, `cargar-curva-s.ts`, `textos.ts` |
| 2 | `src/lib/dp/equivalencias.ts`, `tarifas.ts`, `tarifas-servidor.ts`, pantalla Importar DP, `rdts/partes/route.ts` (rechazo al crear), `src/lib/pr/acumulacion-rdt.ts`, `dashboard/page.tsx` (tarjeta sin tarifa), `recursos_cargo_equivalencias` |
| 3 | `db/115` (redefine `recalcular_pr_desde_rdt`, vigente en `db/112`), `pr/page.tsx`, `dashboard/page.tsx`, `src/lib/dashboard/cargar-dashboard.ts`, `datos-descarga.ts`, `src/lib/informes/cargar-fuentes.ts` |
| 4 | `FormularioCrearRdt.tsx` (columna WBS del equipo, línea ~1831; métricas y autocompletado de actividad, líneas ~1234-1295), `rdts/partes/[id]/route.ts` (**quitar el bloqueo de validación «equipo sin WBS válido del DP»**, líneas ~340-355), Status de RDT, Revisar RDT, Plan Maestro (estado de carga y rótulo «Sin resolver») |

**Hallazgo nuevo del Planner:** al validar, el servidor hoy responde 400 «No se puede validar: N equipo(s) no tiene(n) un WBS válido del DP». Al quitar la partida del equipo ese bloqueo debe desaparecer en el mismo cambio, o ningún RDT con equipo podría validarse.

## Riesgos y bloqueos

- **Los 5 RDT de prueba no se pueden borrar desde la pantalla** (hallazgo del 2026-10-21): el flujo 06 dice que administrador y jefe de proyectos borran RDT, pero en Status no aparece la opción para un RDT validado (el borrado documentado está en el archivo de subidos). Hasta resolverlo la precondición P1 de la prueba v2 queda abierta; alternativa sin borrar: rechazarlos (administrador o jefe de proyectos pueden rechazar un VALIDADO y sale del PR). Decisión pendiente de Victor; si se quiere la opción de borrar, entra al Lote 4.
- Los cambios sin commit de otros trabajos en la app pueden contaminar el commit de restricciones (Lote 0).
- Quitar la partida del equipo cambia el PR: hay que revisar `recalcular_pr_desde_rdt` y los datos de RDT ya validados (la columna no se borra, solo se deja de pedir).
- Una equivalencia mal elegida (OPERARIO a OPERARIO CIVIL en un servicio mecánico) da una tarifa equivocada sin avisar: se declara por servicio y la elige una persona con rol de jefatura.
- Bloquear la fecha futura impide cargar un RDT por adelantado; Victor lo aceptó.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-21 | Bloquear la fecha futura del RDT | Victor |
| 2026-10-21 | Curva S semanal: PV y real con la misma cantidad de días | Victor |
| 2026-10-21 | Desplegar restricciones y dejarlas «pendiente de verificación» | Victor |
| 2026-10-21 | Aplicar la regla de HH de la transversal (fuera de HH reales e IP) | Victor |
| 2026-10-21 | Cargos sin tarifa: resolver al importar el presupuesto, exigir la tarifa y avisar el nombre que no existe | Victor |
| 2026-10-21 | Arreglar métricas del paquete, autocompletar «Met. prog.», y revisar el motivo del rechazo | Victor |
| 2026-10-21 | Los equipos no llevan partida: quitar la opción | Victor |
| 2026-10-21 | Gate Spec aprobado. Las HH ganadas tampoco cuentan la parte de la transversal (queda con la misma regla que las HH reales) | Victor |
| 2026-10-21 | Gate 1 aprobado tal como se propuso; Victor pidió ejecutar hasta terminar sin más preguntas (decide el Orquestador lo operativo) | Victor |
| 2026-10-21 | Autorizado separar y empujar a `main` solo lo de restricciones (Lote 0) | Victor |
| 2026-10-21 | Limpieza de los 5 RDT de prueba: queda **pendiente**. Victor intentó borrarlos y la pantalla no ofrece la opción (solo el administrador puede borrar RDT ya validados) | Victor |

## Enlaces a progreso y evidencia homónimos

Se crean al activar el Gate 1: `02-progreso/` y `03-evidencia/2026-10-21-correcciones-prueba-rdt-ps0001/`.

## Libro de hallazgos

### Mejoras (de trabajo)

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| M1 | 2026-10-21 | Orquestador | Los esperados de una prueba se fijan antes y se calculan desde el presupuesto, no desde lo que muestra la app; no se recalculan durante la prueba | `03-aprendizaje-continuo/` | Registrada | — |

### Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| R1 | 2026-10-21 | Victor | No se registra un RDT con fecha posterior a hoy | Flujo 06 | Pendiente de decisión (se escribe al implementar) | — |
| R2 | 2026-10-21 | Victor | Todo cargo con horas debe tener tarifa en el presupuesto del servicio (fila, MOI o equivalencia del servicio); si no, no se importa ni se registra | Flujos 09 y 06 | Pendiente de decisión | — |
| R3 | 2026-10-21 | Victor | El equipo no se asigna a una partida; su costo suma al servicio | Flujos 06, 10 y 18 | Pendiente de decisión (contradice lo escrito) | — |
| R4 | 2026-10-21 | Victor | PV y valor ganado de la Curva S se leen a la misma fecha | Flujo 21 | Pendiente de decisión | — |

### Observaciones sobre la política

Ninguna.

### Carpetas/archivos huérfanos

Ninguno detectado.

## Informe de Auditoría

Pendiente: se creará en `04-auditoria/` homónimo.

## Elementos postergados propuestos para planes futuros

- Prueba del informe diario con fotos, materiales manuales, trabajador no listado y contenido del PDF.
- Permisos por API de cada rol sobre el RDT.
