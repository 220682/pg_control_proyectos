# DOCS-L3 — Las tres olas de documentación del Lote 3 (Olas 1, 2 y 4)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` («Plan de las tandas que faltan», escrito tras el informe del Auditor). **Origen del trabajo:** los siete puntos de «APLICAR AHORA», las tres decisiones de negocio pendientes de escribir y el libro de hallazgos.
**Repositorio:** `pg_control_proyectos` (documentación), `main`, **sin commit** — los documentos los commitea el Orquestador. **No se tocó el repositorio de código.**
**Nivel:** 0 (`n0`). **Fecha:** 2026-10-04.

## Qué cambié en cada archivo

### `docs/04-flujos-de-negocio/20-plan-maestro.md`

| Apartado | Cambio |
|---|---|
| §3 «Qué ocurre al aprobar» — U6 | Se escribe la **secuencia**: primero se pide el aviso y se muestra qué RDT van a cambiar (cuántos, con qué fechas y metrados), y **solo después se confirma**; la confirmación es la que aplica el reposicionamiento y el recálculo. Sin nombres de endpoint ni rutas inventadas |
| §3 — U4 | Se separa **lo que no cambia** (metrado ejecutado, metrados derivados, horas, estado de validación, y las cifras del PR consolidado) de **lo que sí cambia**: la asociación de paquete del RDT (`rdt_actividades.paquete_trabajo_id` y `rdt_actividad_partidas.paquete_trabajo_id`), que es la clave de reporte `paquete × partida` y **se ve en el propio formulario del RDT y en la pantalla Status**. Se dice por qué: no hay FK ni tabla de unión entre el RDT y la línea del plan |
| §3 — U7 | El historial promete **solo lo que se guarda**: acción `REPOSICIONAMIENTO` y, en el `snapshot`, plan anterior, plan nuevo y versión, diff de claves y quién aprobó. Se dice explícitamente que **no guarda fecha ni metrado como dato consultable** |
| §6 «Umbral» | La lista de datos congelados ahora incluye **`MOVER`** (reordenar paquetes), con su regla (U10) y la decisión de Victor del 2026-10-04, para que coincida con el flujo 19 y con el código |

### `docs/04-flujos-de-negocio/06-rdt.md`

| Apartado | Cambio |
|---|---|
| «Crear RDT con el Plan Maestro» — U9 | Se añade que **las dos condiciones son de creación, no de operación**: registrar, reasignar el paquete, validar y rechazar un RDT ya existente exigen **solo Plan Maestro aprobado** |
| «Reposicionamiento de los RDT al aprobar un Plan Maestro nuevo» | Aviso previo (U6, enlace al flujo 20); «lo que NO cambia» con la lista exacta; «lo que SÍ cambia» (asociación de paquete, visible en el propio formulario y en Status), con la mención de que la frase anterior era más fuerte que el código; U7 limitado a lo que guarda el `snapshot`; y, en los casos sin resolver, que **`sinLinea` hoy vuelve en la respuesta de la aprobación como aviso** (no reasocia ni escribe historial) |

### `docs/02-trabajo-activo/01-planes/…-lote-3-plan.md`

- **U7** reescrita para prometer solo plan, versión, diff de claves y quién aprobó.
- **U9** reescrita: la segunda condición (servicio en Ejecución) es de **creación**; las operaciones sobre un RDT existente exigen solo Plan Maestro aprobado.
- **Aclaración de U4** (§ «Consecuencia implementable»): se añade el «sí cambia la asociación de paquete» y la corrección del lenguaje.
- **Fila R5b** de la tabla de estado de tareas: U10 quedó escrita **solo en el flujo 19** (no en 06, 19 y 20); el §6 del flujo 20 se completó después, en esta Ola 1.
- **Fila duplicada malformada** de la tabla de observaciones (repetía G-O1, sin ID y sin barra inicial): **eliminada**. Era la fila que rompía la tabla del libro.
- **Ola 0** marcada cerrada (`ae476f1`, 1115 tests) y con sus tres puntos de estado real; **la `094` no se aplicó** (Ola 0b pendiente) y la base sigue con la `093`.
- **R4c** añadida a la tabla «Estado real de las tareas».
- **Tabla de olas**: las 1, 2 y 4 marcadas como hechas (en `n0`), con el enlace a este resultado; la 0b y la 3 siguen pendientes.
- **Libro de hallazgos**: 16 filas nuevas, clasificación de las 39, OP7 corregido (ver abajo) y el riesgo de `rdt_actividades` registrado (ver abajo).

### `docs/02-trabajo-activo/02-progreso/…-lote-3.md`

- «Avances terminados»: el reposicionamiento **no toca el metrado ni las cifras del PR; sí toca la asociación de paquete**, y se corrige la frase anterior («no toca los datos del RDT»), que era más fuerte que el código.
- Tabla de tareas: fila **R4c** (cerrada en código, `094` sin aplicar).
- «Deuda que sigue abierta»: se suma que la base usa la `093` (no determinista).
- «Bloqueos y riesgos»: la dependencia de la `093` se deja escrita **con su consecuencia exacta** (la aprobación falla por completo, sin fallback) y **con dónde está el aviso** (`db/093` y `db/README.md`, `ae476f1`).
- «Hallazgos y preguntas de negocio» y «Pendientes»: conteos del libro actualizados (24/13/19), **R4c-R1** entre las reglas pendientes de decisión, y el pendiente de la fila OP7 marcado como resuelto.
- «Estado general» y «Trabajo actual»: el informe del Auditor ya existe; lo que sigue es Ola 0b → Ola 3 → Ola 5 → Gate 2.

### `docs/02-trabajo-activo/03-evidencia/…-lote-3.md`

- Fila de **R4c** en la tabla de tachy (commit, `tsc`, tests) y `resultados/R4c.md` entre las salidas íntegras.
- Apartado nuevo **«2b. Dependencia de la `093` y estado de la `094`»**: dónde está el aviso de dependencia, y que la `094` **está en el repositorio y no en la base** (con el efecto: la base usa la versión no determinista).
- «Verificación en vivo: la que NO hay»: `sinLinea` verificado **por pruebas, no en vivo**.
- «Documentación»: línea de esta tanda con el resultado del verificador.
- «Lo que quedó sucio»: la fila OP7 deja de ser pendiente.

## Salida del verificador

```
python scripts/verificar-referencias.py
Archivos revisados: 46

HUÉRFANOS (0): nadie los menciona

ENLACES ROTOS (0)

MENCIONES SIN ARCHIVO (2): nombres entre comillas invertidas que no existen
   docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md -> convenciones-de-trabajo.md
EXIT=0
```

**0 huérfanos, 0 enlaces rotos, exit 0.** Las dos «menciones sin archivo» son preexistentes y ajenas (no las cuenta para el código de salida). Este archivo queda enlazado desde el plan, el progreso y la evidencia, así que no es huérfano.

## El libro de hallazgos, cómo quedó

**56 filas** (39 del Auditor + 17 nuevas). Tablas bien formadas: **cada fila tiene 7 celdas, como su cabecera** (la fila duplicada era la única que no).

| Categoría | Total | Trasladada | Descartada | Pendiente de decisión | Registrada |
|---|---|---|---|---|---|
| Mejoras (de trabajo) | 24 | 5 | 0 | 0 | 19 |
| Reglas de negocio | 13 | 4 | 3 | 5 | 1 |
| Observaciones sobre la política | 19 | 1 | 1 | 4 | 13 |
| **Total** | **56** | **10** | **4** | **9** | **33** |

### Las 16 filas que entraron

| ID | Categoría | Qué | Estado |
|---|---|---|---|
| R1-M1 | Mejora | Para confirmar que una columna o botón **desapareció** de una tabla que se arma en el cliente hace falta API + SSR + Playwright | Registrada |
| R1-M2 | Mejora | `planMaestroAprobado` es subcadena de `hayPlanMaestroAprobado`: grep con falsos positivos | Registrada |
| R2-R3-M1 | Mejora | El criterio «Plan Maestro aprobado» ya vivía en tres módulos; conviene un helper único | Registrada |
| R4a-M4 | Mejora | Cada aprobación relee todos los RDT del servicio (lotes de 200) solo para calcular el diff | Registrada |
| R5-M1 | Mejora | Buscar una regla derogada por palabra suelta (`impacto`) da falsos positivos: buscar por símbolo o ruta | Registrada |
| R4c-M1 | Mejora | Una tanda con migración no puede correr en un Worker con `opencode run`, y la credencial puede quedar inalcanzable sin aviso | Registrada |
| R4c-M2 | Mejora | Un corte a mitad de tanda no deja commit ni resultado: exigirlos antes de refinamientos | Registrada |
| R5-R2 | Regla | G-R2 y V-R1 quedan superadas por U2/U3 y deben pasar a «Descartada» | Trasladada (aplicada hoy) |
| R5-R3 | Regla | U9 no estaba en el mapeo de R5: la carga por archivo no estaba en el flujo 06 | Trasladada |
| R6a-R1 | Regla | Los RDT por archivo ya existentes en servicios fuera de `EJECUCION` no se migran ni se ocultan | Registrada (el flujo 06 aún no lo dice) |
| R4c-R1 | Regla | Actividad con varios vínculos repartidos en paquetes distintos: no se reposiciona y se reporta | **Pendiente de decisión (Victor)** |
| R4a-O1 | Observación | El protocolo de migraciones y el brief de R4a se contradicen sobre quién aplica la migración | Registrada |
| R4a-O2 | Observación | U8 exige «todo o nada» y la aprobación no era transaccional: falta un ítem de revisión | Registrada |
| R4a-O3 | Observación | `UPDATE` alimentado por un payload fila por fila no es determinista con varios vínculos (riesgo de `rdt_actividades`) | Registrada (el código ya lo corrige con la `094`) |
| R5-O1 | Observación | La política no dice si un registro histórico de cambio se conserva o se reescribe al derogarse | Registrada |
| R5-O2 | Observación | `impacto` es término prohibido en la verificación y a la vez el nombre del concepto vigente U6 | Registrada |
| R4c-O1 | Observación | Un archivo puede estar listado y ser inaccesible a toda API: falta ese caso en el protocolo | Registrada |

### Cambios de estado en las 39 filas existentes

- **Descartada (4):** G-R1, G-R2 y V-R1 (E1-D3 y U2/U3: la acción y el endpoint ya no existen) y OP8 (resuelta por la Enmienda E1, el disparador único es U4). Cada una con su motivo en la fila.
- **Trasladada (10):** V-M2, V-M5, E-M3, R4a-M1, R4a-M2, R4b-O1, F-R1, F-R2, R5-R2 y R5-R3. Cuando el destino existe en este repositorio, la fila **enlaza a él**; cuando el destino es el código (`db/093`, `reposicionamiento*.ts`), se dice en prosa, porque ese repositorio no se edita desde aquí. Dos de ellas (R4a-M1, R4a-M2) están trasladadas **a otro sitio** del que se propuso: el Auditor lo anota y así queda escrito.
- **Pendiente de decisión (9):** las cuatro de R4a y R4c-R1 las decide **Victor**; G-O1, OP1, OP2 y OP3 son del **Gate 2**.
- **Registrada (33):** las que no tienen destino escrito todavía (19 mejoras, R6a-R1 y 13 observaciones), cada una con el motivo por el que sigue ahí, cuando el Auditor dio uno.

### Las dos filas que hoy quedaron obsoletas

- **OP7** decía **«Resuelta (2026-10-03)»**. El Auditor verificó que solo la mitad lo estaba (el config del repo ya no define modelos), pero las tablas del estándar y el pendiente 5 del progreso siguen nombrando `qwen3.8-plus`. Ahora está en **«Registrada (la fila decía Resuelta y no del todo)»**, con el motivo. También se le completó la celda que le faltaba.
- **La que nombraba las filas sin trasladar:** el brief pedía actualizar «la que nombra las 11 filas sin trasladar». **En el plan no existe ninguna fila con ese número**: lo comprobé con búsqueda de `\b11\b` sobre el libro entero y sobre el progreso (las únicas coincidencias son la nota 11 del flujo 14, el paso 11 del estándar, «11 corridas» del benchmark V-M2 y «11 commits del carril» del cierre). Lo que el brief perseguiría es la **fila que nombra los conteos** —la de la Ola 4, «pasar las 12 filas que faltaron y aplicar la clasificación del Auditor a las 39»—, y la frase del **progreso** «El libro de hallazgos del plan tiene 17 mejoras, 9 reglas y 13 observaciones». **Las dos quedaron actualizadas** con los números reales (56 filas: 24/13/19) y con lo que se hizo. Si el brief se refería a otra fila, no la encontré: queda dicho en vez de inventar el blanco.

## Hallazgos de mi propia revisión, en las cuatro categorías

### Mejoras (de trabajo)

1. **Un brief puede pedir corregir una fila que no existe, y el agente tiene que decirlo en vez dedal la más parecida.** El punto 4 de la Ola 4 («la que nombra las 11 filas sin trasladar») no corresponde a ninguna fila del libro: lo verifiqué con herramientas, no de memoria. Elegí la fila que sí nombra conteos y lo dejé escrito en el resultado. La versión de esta ola que funciona: **cada punto del brief debería llevar el identificador del hallazgo (o el texto literal) que hay que corregir.**
2. **Los identificadores de hallazgo chocan cuando el Auditor numera un hallazgo nuevo con uno que ya existe.** El Auditor llamó «R4a-M1 (rendimiento)» a un hallazgo cuyo ID ya lo tenía el de la clave de reporte. Elegí `R4a-M4` y lo dejé dicho dentro de la propia fila, para que nadie lo busque bajo el nombre del informe.
3. **Un hallazgo se puede volver obsoleto sin que nadie lo note porque el texto dice algo razonable.** `OP7` decía «Resuelta» y el resto del entorno la contradecía; el pendiente 6 del progreso también. La fila queda con el estado real y con el motivo.

### Reglas de negocio

1. **R6a-R1 sigue sin escribir y es de las que alguien esperaría encontrar** (los RDT por archivo de servicios fuera de `EJECUCION` no se migran ni se ocultan). Está en el libro con su destino, pero el flujo 06 todavía no lo dice. **Es una traducción pendiente, no una decisión pendiente.**
2. **La «regla de negocio» de R6a-M1 (el RDT por archivo no se vincula a líneas del Plan Maestro, su única relación con el plan es la guardia de creación) no entró al libro**: el Worker la dejó como informativa y el Auditor tampoco la listó entre las doce. La anoto aquí porque **afecta a U9**: si algún día el reposicionamiento busca vínculos en RDT por archivo, no los encontrará y no es un defecto.

### Observaciones sobre la política

1. **El riesgo de `rdt_actividades` se registró en «Observaciones sobre la política», como pidió el brief, y es discutible que sea de política**: es un defecto técnico de una sentencia SQL, no un fallo del proceso. Lo dejé en esa tabla porque el brief lo pide, y redacté la fila para que contenga la **lección de proceso** (un brief que escribe SQL debe exigir comprobar el determinismo de todo `UPDATE` alimentado por un payload por fila, y el checklist de revisión debe incluirlo) y no solo el defecto. Si prefieres que vaya a una categoría nueva, es una línea.
2. **El orden Documentador → Auditor no evita este tipo de retraso**: el Auditor encontró que doce hallazgos de cinco resúmenes de cierre nunca llegaron al libro, y eso solo se vio porque la clasificación se hizo *después*. La regla del plan («pasar fila por fila lo que cada Worker deja en su resumen») ya existe y no se cumplió; el problema no es la regla, que nadie la fiscaliza.

### Carpetas/archivos huérfanos

**Ninguno.** No se creó ningún archivo salvo este resultado (enlazado desde el plan, el progreso y la evidencia). No se borró nada. El repositorio de código no se tocó.

## Lo que queda para las otras olas

- **Ola 0b:** aplicar la `094` (la base usa la `093`, no determinista).
- **Ola 3:** U6 en código (nivel 3, corre en paralelo). La regla ya está escrita en el flujo 20 como vigente y describe la secuencia correcta.
- **Ola 5:** verificación en vivo (desbloquea OP9).
- **Ola 6:** Gate 2. Siguen abiertas, sin cambio: las **cinco** reglas de negocio pendientes de decisión (R4a-R1 a R4a-R4 y R4c-R1), OP1, OP3, OP4, el artefacto «Matriz de permisos» (que no refleja el retiro de la acción del cronograma ni el congelamiento de `MOVER`) y F5 parcial.