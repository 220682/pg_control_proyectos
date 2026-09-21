# PR enriquecido — Fase 1 (Agente A): pipeline RDT → PR

**Estado (2026-09-21):** PLAN APROBADO, PUNCH LIST APROBADA. Migración `052` corrida en Supabase. **Agente A EN EJECUCIÓN**, rama `feat/pr-fase-1-pipeline-rdt`. Trabaja en paralelo con [Fase 2](2026-09-21-pr-fase-2-pipeline-linea-base.md) (Agente B, rama `feat/pr-fase-2-linea-base-evm`).

**Pendiente para siguiente sesión:** ambos agentes en vivo haciendo loop de verificación → PR cuando al 100% del checklist. Victor revisará ambos PRs.

**Ya resuelto, no volver a preguntar:**
- Punch List de esta fase (19 ítems, tabla más abajo) — **aprobada por Victor.**
- `db/052_pr_enriquecido.sql` — **corrida en Supabase por Victor.** El contrato del PR ya existe: `pr_partidas` y `proyecto_pr` tienen todas las columnas del Paso 0.
- Credenciales de verificación en memoria (`cuentas-prueba.md`), reglas de negocio de costo/EVM (`reglas-costo-evm.md`), protocolo de verificación con Playwright (`protocolo-verificacion-agente.md`).

**Único punto que sigue pendiente de coordinar con el Agente B:** el orden de migraciones — la `053` de esta fase va antes que la `060` de la Fase 2 (ver "Qué puede romperse", el caso de `reemplazar_dp()` borrando el PR).

## Ejecución en la nube (decidido 2026-09-21)

- **Cada agente trabaja en su propia rama** (no directo a `main`). Al llegar al 100% de su checklist de implementación, abre un **PR** para que Victor lo revise antes de mergear. Rama sugerida: `feat/pr-fase-1-pipeline-rdt`.
- **Las migraciones se corren solas, sin pausar a confirmar cada una** — excepción puntual autorizada por Victor solo para esta tarea (ver `mejoras-futuras.md`, sección "Acceso directo a Postgres/Supabase"). El agente lee la cadena de conexión directa de Postgres de la variable de entorno **`PR_DB_URL`**, configurada por Victor en el entorno de `claude.ai/code` de este repositorio. **No es un secreto cifrado** — la documentación de Claude Code advierte que cualquiera con acceso a ese entorno puede leerla —, así que el riesgo aceptado es acotado a que hoy solo Victor tiene ese acceso. El agente nunca imprime el valor completo en su salida ni lo commitea.
- Credenciales de verificación (Playwright) en las variables **`PR_TEST_ADMIN_EMAIL`** / **`PR_TEST_ADMIN_PASSWORD`** (cuenta con permisos altos) y **`PR_TEST_USER_EMAIL`** / **`PR_TEST_USER_PASSWORD`** (cuenta sin permisos de administración), mismo entorno.
- Aun así, **cada migración queda documentada en su propio archivo `db/0NN_*.sql`, commiteada, y resumida en el PR** — la autonomía es sobre no pausar a pedir permiso, no sobre dejar de dejar rastro.
- Al terminar, el agente entrega en el PR: el checklist de implementación (A1–A10) marcado, la Punch List de 19 ítems con el resultado de cada uno verificado con Playwright, y el informe de limpieza.

## Contexto — el eslabón roto

`18-control-avance.md` define la cadena `RDT validado → PR → Dashboard`. Hoy esa cadena está cortada en un punto exacto y verificable.

Revisión del código real de `py_control_proyectos_web` (2026-09-21): **todas** las referencias a `pr_partidas.metrado_acumulado`, `pr_recursos.costo_acumulado` y `pr_recursos.cantidad_acumulada` son `.select()` — lecturas. **No existe una sola escritura.** `reemplazar_dp()` las crea en 0 y nada las vuelve a tocar nunca.

Lo que eso significa:

- La matemática EVM **ya está construida**: `src/lib/dashboard/dashboard.ts` calcula EV, BAC, AC, PV al corte, SV, CPI, SPI, % avance físico, HH ganadas, HH reales, IP, EAC, semáforo y resumen ejecutivo.
- El Dashboard de proyecto, el rollup de portafolio y la pantalla PR **ya leen esas columnas**.
- **Todos están leyendo ceros.**

El PR no es una vista más: es la tabla que alimenta a todo el sistema. Esta fase construye el pipeline que trae el dato real del RDT hacia el PR. La Fase 2 trae el dato contractual y planificado desde las otras interfaces.

## Reglas de negocio fijas (Victor)

Decididas y confirmadas. **No volver a preguntarlas — quedan escritas aquí.**

1. **El AC medido sale solo de HH (mano de obra) y HM (equipos)**, con la tarifa congelada al validar el RDT (`db/047_rdt_tarifas.sql`: `rdt_tareo.tarifa_hh`, `rdt_equipos_parte.tarifa_hm`).
2. **Todas las HH declaradas en el RDT suman al costo real: Directas (D), Contributorias (C) y No Contributorias (NC).** No se excluye ninguna categoría.
3. **Las HM de equipos declarados en el RDT suman aunque el equipo no esté en el presupuesto contractual.** El sistema resuelve su costo desde la base de datos.
4. Si un recurso declarado **no tiene costo en ninguna tabla**: avisar al administrador o jefe de proyectos. **Ese aviso no es restrictivo** — no puede impedir declarar ni guardar el RDT.
5. **Materiales, subcontratos y todo lo que no sea HH ni HM no se miden por costo capturado: se miden por % de avance económico (EV).**
6. **El metrado programado del RDT es solo informativo.** No es PV y no entra a ningún cálculo. Sí dispara la obligación de registrar CNC cuando no se completa.
7. **El CNC lo marca el supervisor según su criterio de campo**, en catálogo mantenible y obligatorio cuando hay incumplimiento.
8. **El PV sale del Plan Maestro, y el Plan Maestro es restrictivo: sin Plan Maestro aprobado el servicio no puede pasar a Ejecución.**
9. **El sistema calcula solo COSTO DIRECTO.** Por eso el DP extrae únicamente de la hoja **CD**. Gastos generales, utilidad y todo lo que no sea costo directo **no entran a ningún cálculo**. **BAC = costo directo**, y AC también, para que el CPI compare en la misma base.
10. **Las HH del personal indirecto (MOI) se acumulan como horas en el consolidado de RDTs**, pero **no se valorizan** (`tarifa_hh` NULL por diseño, EVM Fase 1). Horas sí, costo no.
11. **Todo el sistema trabaja en USD.** No hay multi-moneda.
12. **Toda actividad se carga a una partida: las D, las C y las NC.** Ninguna hora queda huérfana. La actividad D trae su WBS; la C y la NC se asignan a una partida elegida por el usuario **de un desplegable con las partidas de las actividades D ya declaradas ese día** — el mismo mecanismo que ya existe para los equipos (HM). Por eso el parte necesita **al menos una actividad D con WBS declarada antes** de poder cargar una C o una NC.

### Terminología — dos cosas distintas que NO se deben confundir

Esto causó confusión al armar el plan y queda aclarado de una vez:

| Término | Qué es | Dónde vive |
|---|---|---|
| Actividad **Contributoria (C)** / **No Contributoria (NC)** | Categoría de la **ACTIVIDAD**: traslado, charla, espera. No genera metrado, pero **sí se carga a una partida** (regla 12). | `rdt_actividades.ta` |
| **Mano de obra indirecta (MOI)** | Categoría de la **PERSONA**: supervisor, ingeniero. No es un tipo de actividad. | `dp_moi` |

Son **ejes independientes**: una persona MOI puede declarar horas en actividades D, C o NC; y una actividad NC la puede ejecutar personal directo.

> **Regla de redacción: nunca llamar "indirectas" a las HH de actividades C/NC.** Se las nombra por su tipo — contributorias y no contributorias. **"Indirecto" queda reservado exclusivamente para MOI.**

Lo que C/NC sí cambian respecto de las D: **no generan metrado ejecutado**. Aportan horas y costo a la partida, no avance físico. Por eso el desglose por tipo de actividad se guarda aparte: es lo que permite leer el % de trabajo productivo de cada partida (análisis clásico de LPS).

## Alcance de esta fase

Traer al PR todo lo que nace del RDT validado: metrado ejecutado, HH reales con su desglose D/C/NC, HM reales, costo real y CNC. Más el cambio en Crear RDT para que toda actividad lleve partida.

## Fuera de alcance (explícito)

- **Dashboard — no se toca.** Ni el de proyecto, ni el rollup de portafolio, ni el Dashboard 2 "Completo".
- Curva S, serie semanal, Pareto de CNC, cierre semanal auditado.
- 3WLA (pospuesto en `mejoras-futuras.md`).
- Ampliar el RDT para capturar materiales o subcontratos con costo (regla 5).

> **Efecto esperado, no es cambio de alcance:** los dashboards que hoy muestran ceros y "Pendiente" empezarán a mostrar números reales sin ser tocados, porque leen las mismas columnas que esta fase empieza a llenar. Si algo se ve raro ahí, es síntoma del pipeline, no del dashboard.

---

## Paso 0 — COMPARTIDO: definición del PR (se hace UNA sola vez)

**Este paso es idéntico en las dos fases y se ejecuta una sola vez, antes de que los dos agentes empiecen en paralelo.** El PR queda definido como **una sola tabla de partidas** (`pr_partidas`), más la cabecera ya existente (`proyecto_pr`). Ningún agente inventa columnas por su cuenta: las de abajo son el contrato completo.

Migración **`db/052_pr_enriquecido.sql`** — aditiva e idempotente (`add column if not exists`). La corre Victor en Supabase antes de arrancar.

```sql
-- BLOQUE A — Línea base contractual, COSTO DIRECTO (origen DP, hoja CD).  Llena: Agente B
alter table pr_partidas
  add column if not exists hh_contractual numeric,
  add column if not exists bac numeric;

-- BLOQUE A' — Planificado (origen Plan Maestro y Cronograma).             Llena: Agente B
alter table pr_partidas
  add column if not exists metrado_planificado_acum numeric not null default 0,
  add column if not exists fecha_inicio_base date,
  add column if not exists fecha_fin_base date;

-- BLOQUE B — Ejecución real (origen RDT validado).                        Llena: Agente A
-- metrado_acumulado ya existe (007_pr.sql) y ES el metrado ejecutado.
-- Regla 12: toda actividad (D, C y NC) se carga a una partida, así que el
-- desglose por tipo vive aquí, por partida, y no en un balde de proyecto.
-- Solo las D generan metrado; las C y NC aportan horas y costo, no avance.
alter table pr_partidas
  add column if not exists hh_reales_acum numeric not null default 0,
  add column if not exists hh_d_acum numeric not null default 0,
  add column if not exists hh_c_acum numeric not null default 0,
  add column if not exists hh_nc_acum numeric not null default 0,
  add column if not exists hm_reales_acum numeric not null default 0,
  add column if not exists costo_real_acum numeric not null default 0,
  add column if not exists actividades_acum int not null default 0,
  add column if not exists actividades_con_cnc_acum int not null default 0,
  add column if not exists recalculado_en timestamptz;

-- Nivel proyecto.                                                         Llena: Agente A
alter table proyecto_pr
  -- MOI: horas acumuladas, SIN costo a propósito (regla 10, no se valoriza).
  add column if not exists hh_mo_indirecta_acum numeric not null default 0,
  -- Balde SOLO para datos anteriores a la regla 12: RDT ya validados cuyas
  -- actividades C/NC o equipos quedaron sin partida y no se pueden reasignar
  -- retroactivamente. En partes nuevos esto queda en 0 y debe seguir en 0.
  add column if not exists hh_legacy_sin_partida_acum numeric not null default 0,
  add column if not exists hm_legacy_sin_partida_acum numeric not null default 0,
  add column if not exists costo_legacy_sin_partida_acum numeric not null default 0,
  add column if not exists recursos_sin_tarifa jsonb not null default '[]'::jsonb,
  add column if not exists recalculado_en timestamptz;
```

**Bloque C (derivados EVM) no se almacena.** Son funciones puras de las columnas de arriba y se calculan al leer — los construye el Agente B en `src/lib/pr/evm.ts`. Almacenarlos duplicaría la verdad. Además el **PV depende de la fecha de corte** (avanza cada día aunque no haya RDT nuevo), así que materializarlo obligaría a un recálculo diario.

Regla de oro del PR, para los dos agentes:

| Qué | Cómo |
|---|---|
| Cambia cuando ocurre un hecho (se importa un DP, se valida un RDT) | **Se materializa**: el pipeline lo escribe en la columna |
| Depende de la fecha de corte o es derivación pura (PV, EV, CPI, SPI, PPC…) | **Se calcula al leer** |

> La regla 12 **no necesita migración**: `rdt_actividades.wbs` y la tabla puente `rdt_actividad_partidas` (`db/040`) ya existen. Lo que cambia es que dejan de ser exclusivas de las actividades D. Es cambio de formulario y de validación, no de esquema.

---

## Tareas — Agente A

### A1. Toda actividad lleva partida (regla 12)

Es la primera tarea porque el motor de acumulación depende de ella.

**En Crear RDT (`FormularioCrearRdt.tsx`):**

- Al elegir `TA = C` o `TA = NC`, aparece un **desplegable de partida** — mismo patrón que el que ya usan los equipos: lista las partidas de las **actividades D ya declaradas en ese parte**, no el DP completo.
- Si todavía no hay ninguna actividad D con WBS, el desplegable sale vacío con el motivo visible ("primero declará una actividad directa con su partida"). **Declarar primero la actividad D con WBS es requisito** (regla 12).
- Las C y NC **no** piden unidad ni metrado: no generan avance físico. Solo horas y costo.

**En la validación (`erroresDelParte()` en `src/lib/rdts/parte.ts`):**

- Bloquea guardar si una actividad C o NC no tiene partida asignada. Es del mismo tipo que la validación ya existente para actividades D sin WBS.
- Igual para los equipos: un equipo sin partida no debería poder guardarse.

**Datos que ya están cargados (legacy):** los RDT validados antes de esta regla tienen C/NC sin partida y no se pueden reasignar solos. Van al balde `*_legacy_sin_partida_acum` del proyecto, que queda **visible y rotulado como dato legacy**, no escondido. Se pueden arreglar uno por uno con el link "Corregir" cuando Victor quiera. **No se inventa una asignación automática.**

### A2. Motor de acumulación `recalcular_pr_desde_rdt()`

Migración **`db/053_pr_motor_rdt.sql`**. Función Postgres, misma escuela que `reemplazar_dp()` y `guardar_rdt_parte()`: una sola llamada atómica.

- Firma: `recalcular_pr_desde_rdt(p_proyecto_id uuid) returns void`.
- **Recálculo completo, no incremental.** Borra a 0 y recalcula desde todos los `rdt_partes` con `estado_validacion = 'VALIDADO'` de ese proyecto. Así una corrección, un rechazo o un borrado nunca dejan residuo.
- Solo entra `VALIDADO` (flujo 18: "solo un RDT validado alimenta las casillas Real").

Atribución de cada dato a su destino:

| Origen | Va a | Regla |
|---|---|---|
| Actividad **D** | `pr_partidas` de su partida: metrado, `hh_d_acum`, costo | El vínculo oficial es `rdt_actividad_partidas` (`040`), no el texto de `rdt_actividades.wbs` |
| Actividad **C** | `pr_partidas` de la partida elegida: `hh_c_acum` y costo. **Sin metrado** | Regla 12 |
| Actividad **NC** | `pr_partidas` de la partida elegida: `hh_nc_acum` y costo. **Sin metrado** | Regla 12 |
| Equipo con partida | `pr_partidas.hm_reales_acum` y costo | Regla 3 |
| Horas de personal **MOI** | `proyecto_pr.hh_mo_indirecta_acum` — **solo horas** | Regla 10: se acumulan, no se valorizan |
| Legacy sin partida (datos viejos) | `proyecto_pr.*_legacy_sin_partida_acum` | Solo para lo cargado antes de la regla 12 |

Cálculos:

- `metrado_acumulado` = suma de `metrado_ejecutado` de las actividades **D** de esa partida. Las C y NC no aportan metrado. **`metrado_programado` no se usa** (regla 6).
- `hh_reales_acum` = `hh_d_acum + hh_c_acum + hh_nc_acum`.
- `costo_real_acum` = `Σ(horas × tarifa_hh)` de las tres categorías + `Σ(horas × tarifa_hm)` de los equipos de esa partida. **Costo directo, en USD** (reglas 9 y 11).
- `actividades_acum` / `actividades_con_cnc_acum`: insumos del PPC que calcula el Agente B.

**Criterio de aceptación:** correr la función dos veces seguidas da el mismo resultado (idempotencia), y con cero RDT validados deja todo en 0 sin fallar.

⚠️ **Punto de choque con el Agente B — reimportar un DP borra el PR.** `reemplazar_dp()` hace `delete from proyecto_pr` y lo reconstruye con los acumulados en 0. Hoy no molesta porque no hay dato real que perder; **en cuanto este motor funcione, reimportar un DP borraría toda la ejecución real acumulada.**

Por eso `recalcular_pr_desde_rdt()` es de **recálculo completo**: el Agente B la llama al final de `reemplazar_dp()` y el lado real se reconstruye solo desde los RDT validados. Dos obligaciones para esta fase:

- La función tiene que poder llamarse **desde dentro de otra función**, sin efectos raros y sin depender de nada de la capa de aplicación.
- **La `053` se corre antes que la `060` del Agente B.** Coordinarlo con él, no asumirlo.

### A3. Mantener vivo `pr_recursos` (no romper lo existente)

⚠️ **Riesgo real detectado.** Hoy el Dashboard calcula BAC y AC desde **`pr_recursos`**, no desde `pr_partidas`. Si el motor llena solo `pr_partidas`, el costo real queda en dos sitios con dos verdades distintas.

El motor de A2 **también** escribe `pr_recursos.costo_acumulado` y `cantidad_acumulada`, agregados por `tipo`.

**Criterio de aceptación (test obligatorio):**
`Σ pr_partidas.costo_real_acum + proyecto_pr.costo_legacy_sin_partida_acum` **=** `Σ pr_recursos.costo_acumulado`

Si no cuadran, el pipeline está mal. No se cierra la fase con esa igualdad rota.

### A4. Enganche a los cambios de estado del RDT

Llamar `recalcular_pr_desde_rdt(proyecto_id)` después de **todo** cambio que altere qué está validado:

- `src/app/api/rdts/partes/[id]/route.ts` — VALIDAR y RECHAZAR.
- `src/app/api/rdts/partes/route.ts` — guardar y corregir un parte.
- Borrado de RDT (solo admin).

**Criterio de aceptación:** validar mueve el PR; rechazar lo devuelve al valor anterior; corregir y revalidar deja el valor correcto.

### A5. Resolución de tarifa y aviso de recurso sin costo

Reglas 3 y 4. Si un cargo o equipo declarado no tiene tarifa congelada:

1. Resolverla desde `dp_recursos` del proyecto, y si no está, desde el catálogo de empresa (`recursos_cargos` / `recursos_equipos`), respetando las equivalencias de la Fase 0.
2. Si aun así no hay costo: registrarlo en `proyecto_pr.recursos_sin_tarifa` y **notificar a administrador y jefe de proyectos** por el flujo 04 ya existente.
3. **Nunca bloquear.** Ni la carga del RDT, ni su validación, ni el recálculo.

**No avisar por MOI** (regla 10): su `tarifa_hh` en NULL es correcto por diseño, no es un dato faltante.

### A6. Catálogo CNC mantenible + obligatoriedad

Migración **`db/054_catalogo_cnc.sql`**.

- Tabla `catalogo_cnc` (descripción, activo, orden). **Semilla: las 12 causas actuales** de `CAUSAS_CNC` en `src/lib/rdts/parte.ts`, sin inventar ninguna nueva.
- `rdt_actividades.cnc` pasa a referenciar el catálogo, conservando el texto ya cargado.
- Pantalla de mantenimiento en el apartado **Recursos**, mismo criterio que Personal y Equipos: solo **administrador y jefe de proyectos**.
- **Disparador confirmado por Victor:** cuando el metrado ejecutado no completa el metrado programado, el CNC es obligatorio. El metrado programado sigue siendo informativo para todo lo demás (regla 6).

### A7. Registrar los chips y accesos nuevos en el flujo 14

La pantalla de catálogo CNC es un acceso nuevo. `16-paneles.md` regla 10: todo chip nuevo se registra en `14-accesos-y-restricciones.md`.

### A8. Verificación técnica

- `tsc --noEmit` limpio, `eslint` limpio, suite completa en verde, `next build` sin errores.
- Tests nuevos: idempotencia del motor, atribución D vs C vs NC vs MOI, reconciliación de A3, equipo sin tarifa, CNC obligatorio, C/NC sin partida bloqueada.
- Migraciones `052`, `053`, `054` aplicadas en Supabase por Victor. **El SQL completo se pega en el mensaje, nunca se remite a un archivo que Victor no ve** (lección de la ronda 4 del sub-lote 1).

---

## Qué puede romperse

### Cambios de comportamiento esperados — no son fallas

1. **El semáforo del Dashboard pasa de PENDIENTE a color real.** Hoy `calcularCpi` devuelve `'Pendiente'` cuando AC = 0, y `calcularSemaforo` devuelve `PENDIENTE` si CPI o IP están pendientes: o sea, **hoy todos los servicios están en PENDIENTE**. Al llenarse el AC, el semáforo toma color de verdad. Y como el umbral es `peor < 0.85 → ROJO`, y el CPI ahora incluye horas C y NC (que cuestan pero no generan EV), **es esperable que varios servicios salgan ROJO el primer día**. Es aritmética, no un bug.
2. El resumen ejecutivo del Dashboard cambia de texto, y el rollup de portafolio empieza a agregar números reales. Ninguno de los dos se toca en código.
3. **Crear RDT se vuelve más estricto:** una C o NC sin partida, y un metrado incompleto sin CNC, dejan de poder guardarse. Quien antes guardaba sin eso ahora queda bloqueado. Es intencional, pero es un cambio de rutina para el supervisor en campo.

### Riesgos reales de rotura

1. ⚠️ **El PDF PROM-GP-002.** `src/lib/rdts/exportador-parte-pdf.ts:159` imprime la causa como texto plano (`a.cnc ?? ''`). Si el catálogo CNC convierte esa columna en un id, **el PDF pasaría a imprimir un UUID en la columna CNC**. La migración `054` tiene que dejar el PDF mostrando la descripción. Verificar descargando un PDF de un parte viejo y uno nuevo.
2. ⚠️ **Validar RDT queda acoplado al recálculo del PR.** Si el motor falla, no puede tumbar la validación del RDT. **Decidir explícitamente y dejarlo escrito:** o va en la misma transacción —y entonces tiene que ser sólido—, o va aparte y un fallo deja el PR desfasado hasta el siguiente recálculo, lo cual es tolerable justamente porque es recálculo completo. No dejarlo al azar.
3. **Datos legacy conviviendo con los nuevos.** En un mismo servicio van a mezclarse partes viejos (C/NC sin partida, en el balde legacy) con partes nuevos (todo atribuido). Los totales del servicio son correctos, pero el desglose por partida queda incompleto para el período viejo. Por eso el balde va rotulado y visible, no escondido.
4. **La suite de tests.** Hay 409 tests pasando hoy. Los cambios de validación de `erroresDelParte()` van a tocar varios. Que pasen todos es requisito de cierre, no un detalle.

## Protocolo de verificación y cierre (obligatorio)

Este es el ciclo de trabajo del agente. **No se salta ningún paso.**

1. **Antes de implementar — Victor aprueba el checklist.** El resultado esperado se define **antes** de escribir código. Sin checklist aprobado, la implementación no arranca.
2. **Implementación** de A1 a A8.
3. **Autoverificación del agente con el MCP de Playwright.** Cada ítem se comprueba **en la app real, con login real** — no razonando sobre el código. Precedente: el bug de los `<th>` sticky del sub-lote 1 sobrevivió a dos arreglos "razonados por código" y solo apareció inspeccionando el navegador en vivo.
4. **El agente llena el checklist** con el resultado de cada ítem.
5. **Loop hasta cerrar.** Mientras quede un ítem que no esté en **Completado**, el agente corrige y vuelve a verificar. No se entrega con ítems abiertos ni con "pendiente de que Victor confirme".
6. **Fin del trabajo del agente:** cuando el 100% está en Completado.
7. **Recién entonces Victor hace la revisión final.**

### Credenciales de verificación

Las dos cuentas están en la **memoria local del proyecto**, archivo `cuentas-prueba.md` (`C:\Users\BRANDY\.claude\projects\d--VICTOR-CLAUDE-CODE-pg-control-proyectos\memory\`). **Fuera del repositorio a propósito:** los dos repos están en GitHub y AGENTS.md prohíbe publicar credenciales, así que aquí se referencia la ubicación y nunca el valor.

Son dos porque casi toda verificación tiene dos lados: una cuenta con permisos altos (validar y rechazar RDT, mantener el catálogo CNC, recibir el aviso de recurso sin tarifa) y una sin permisos de administración (cargar el RDT, comprobar el bloqueo de CNC obligatorio y el de C/NC sin partida). Un permiso que solo se comprueba con la cuenta de admin no está comprobado.

---

## Informe de limpieza (entregable obligatorio al cerrar)

Al terminar, **antes de dar la fase por cerrada**, el agente entrega un informe de qué quedó viejo. Va escrito en este mismo archivo, en una sección `## Archivos y código que quedaron viejos`.

Qué se reporta:

| Tipo | Ejemplos |
|---|---|
| Archivos | Módulos, componentes o scripts que ya no usa nadie |
| Código dentro de un archivo | Funciones, constantes, tipos o props que quedaron sin referencias |
| Tests | Casos que prueban algo que ya no existe o que quedó reemplazado |
| Columnas de base de datos | Columnas que dejaron de leerse o escribirse |
| Documentación | Párrafos de flujos o de `Mejoras continuas` que quedaron contradichos |

Por cada ítem, cuatro datos: **qué es**, **por qué quedó viejo**, **qué lo reemplaza** y **quién más lo referencia hoy**.

Reglas:

- **El agente no borra nada.** Reporta y Victor decide (AGENTS.md: no eliminar archivos sin aprobación explícita).
- **Ninguna columna de base de datos se borra ni se renombra** sin un plan de migración aparte, aunque quede sin uso (AGENTS.md).
- Cada "esto quedó sin uso" se sostiene con una **búsqueda real de referencias en el código**, no de memoria. Sin esa comprobación, el ítem no se reporta.

Candidato ya identificado para esta fase, para que sirva de ejemplo del formato esperado:

- **`CAUSAS_CNC`** (`src/lib/rdts/parte.ts:32`) — array fijo con las 12 causas. Queda reemplazado por la tabla `catalogo_cnc` de la migración `054`. Lo referencian hoy `FormularioCrearRdt.tsx` y el bloque `describe('CAUSAS_CNC')` de `src/lib/rdts/parte.test.ts`, que espera exactamente 12 elementos. Confirmar si queda del todo sin uso o si sigue haciendo falta como semilla.

## Checklist de implementación — Agente A

- [ ] A0 · Migración `052_pr_enriquecido.sql` aplicada (compartida, una sola vez)
- [ ] A1 · Toda actividad lleva partida: desplegable para C/NC, validación y tratamiento del legacy
- [ ] A2 · `recalcular_pr_desde_rdt()` en `053`, recálculo completo e idempotente
- [ ] A3 · `pr_recursos` mantenido y reconciliación cuadrando
- [ ] A4 · Enganche en validar / rechazar / corregir / borrar
- [ ] A5 · Resolución de tarifa + aviso no restrictivo a admin y JP
- [ ] A6 · Catálogo CNC en `054` + pantalla + obligatoriedad
- [ ] A7 · Chips nuevos registrados en el flujo 14
- [ ] A8 · tsc, eslint, tests y build limpios; migraciones aplicadas
- [ ] A9 · Autoverificación Playwright completa, checklist 100% Completado
- [ ] A10 · Informe de limpieza entregado: qué quedó viejo, con referencias comprobadas

## Punch List — checklist a aprobar ANTES de implementar

Se carga en la Punch List de Mejoras como checklist nuevo: **"PR Fase 1 — pipeline RDT → PR"**. **Victor lo aprueba antes de que arranque la implementación.** El agente lo llena con Playwright al terminar y hace loop hasta cerrarlo completo.

| # | Ítem | Resultado esperado |
|---|---|---|
| 1 | Crear RDT, elegir TA = C o NC | Aparece el desplegable de partida con las partidas de las actividades D del día |
| 2 | Intentar cargar una C o NC sin haber declarado antes una actividad D | El desplegable sale vacío y explica que primero hace falta una actividad directa |
| 3 | Guardar un parte con una C o NC sin partida asignada | No deja guardar |
| 4 | PR sin RDT validados | Muestra 0 en ejecutado, no rompe |
| 5 | Validar un RDT | El metrado ejecutado de esa partida se mueve en el PR |
| 6 | Pantalla PR | El % de avance deja de estar clavado en 0 |
| 7 | HH reales de la partida | Coinciden con la suma de las columnas del tareo de esa partida, sumando D, C y NC |
| 8 | Desglose por tipo | `hh_d`, `hh_c` y `hh_nc` de la partida suman exactamente las HH reales de esa partida |
| 9 | Actividades C y NC | Aportan horas y costo a su partida, pero **no** mueven el metrado ejecutado |
| 10 | Costo real de la partida | Coincide con HH × tarifa + HM × tarifa, en USD |
| 11 | Horas de personal MOI | Se acumulan como horas, sin costo asociado |
| 12 | Equipo declarado fuera del presupuesto | Suma su HM al costo real de su partida |
| 13 | Recurso sin costo en ninguna tabla | Genera aviso a admin/JP y **no** impide guardar ni validar |
| 14 | Rechazar un RDT ya validado | El PR vuelve al valor anterior |
| 15 | Corregir y revalidar | Queda el valor correcto, sin duplicar |
| 16 | Catálogo CNC | Se mantiene desde Recursos, solo admin y jefe de proyectos |
| 17 | RDT con metrado incompleto sin causa | No deja guardar |
| 18 | RDT viejos, cargados antes de la regla | Sus C/NC quedan en el balde legacy, rotulado como tal, sin romper ningún cálculo |
| 19 | Reconciliación de costo | Partidas + legacy cuadra con el total de `pr_recursos` |

## Coordinación con el Agente B

| | Agente A (esta fase) | Agente B (Fase 2) |
|---|---|---|
| **Migraciones** | `053`–`059` | `060`–`069` |
| **Escribe en el PR** | Bloque B (real) + nivel proyecto | Bloque A y A' (contractual y planificado) |
| **Archivos propios** | `src/lib/pr/acumulacion-rdt.ts`, `src/lib/rdts/**`, `src/app/api/rdts/**`, `FormularioCrearRdt.tsx`, catálogo CNC | `src/lib/pr/evm.ts`, `src/lib/dp/**`, Plan Maestro, cronograma, `proyectos/[id]/pr/page.tsx` |
| **No toca** | La pantalla PR (la rehace B), `src/lib/pr/evm.ts` | El motor de RDT, el catálogo CNC, el formulario de RDT |

**Prohibido para los dos:** `src/app/proyectos/[id]/dashboard/page.tsx`, `src/lib/dashboard/dashboard.ts` y el rollup de portafolio.

Migración `052` es compartida: la corre Victor una sola vez antes de arrancar. Es idempotente.

## Mejoras a flujos

- `06-rdt.md`: que el RDT validado alimenta el PR; que **toda actividad, incluidas C y NC, se carga a una partida** (regla 12); que el metrado programado es informativo; y que el CNC pasa a catálogo mantenible y obligatorio.
- `18-control-avance.md`: dejar escritas las reglas 1 a 12, en especial la 9 (solo costo directo), la 10 (MOI horas sin costo), la 12 (toda actividad lleva partida) y la aclaración de terminología C/NC vs MOI.
