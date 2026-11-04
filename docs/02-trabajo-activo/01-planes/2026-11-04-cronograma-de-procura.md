# Cronograma de procura (Seguimiento)

## Identificación y estado

Tema: cronograma de procura de los RQ, para todos los servicios. Fecha: 2026-11-04. Estado: `Implementando`.

- Gate Spec: `aprobado por Victor (2026-11-04)`
- Gate 1: `aprobado por Victor (2026-11-04)`
- Gate 2: `pendiente`

## Spec

### Estado

`Aprobado (Gate Spec)` — Victor, 2026-11-04 («ok todo bien, dale»).

### Problema y contexto

Hoy los RQ se siguen solo en el Status de requerimiento (estado del RQ y, desde el 2026-11-04, la barra de avance por materiales atendidos). No hay una vista que diga **qué material debe estar comprado y para cuándo** según lo que programa el Plan Maestro, ni qué compras están por vencer o se compraron tarde. Victor quiere elegir qué RQ entran en ese seguimiento y verlo en un cronograma que se actualice solo.

### Resultado esperado

1. En el **Status de requerimiento**, cada RQ tiene una marca **«Va a procura»: Por decidir / SÍ / NO**. Un RQ nuevo entra como **Por decidir**.
2. Grupo nuevo **«Seguimiento»** en el panel derecho con el chip **«Cronograma procura»**: un cronograma de **todos los servicios** con los RQ marcados SÍ, que se actualiza solo al marcar un RQ o al cambiar su avance.
3. Cada RQ del cronograma muestra **cuándo lo necesita la obra** (sacado del Plan Maestro aprobado) y su estado de compra.
4. **Comprado automático:** cuando el RQ llega al **100 %** de la barra (todos sus materiales Atendidos), aparece como **Comprado**, con la fecha de ese día. También se puede marcar Comprado **a mano**.
5. **Informe de alertas** en la misma pantalla: atrasados, por vencer, próximas compras, sin fecha, comprados a tiempo y comprados tarde.
6. Descarga del cronograma y del informe en **PDF y Excel**.

### Alcance

- **Marca «Va a procura»** en el Status RQ: columna nueva con el valor; la cambian solo administrador y jefe de proyectos (Victor, 2026-11-04). Se marca **el RQ completo** (no por material). Filtro y contador de «Por decidir» para que no quede ninguno sin marcar.
- **Dos fechas distintas (Victor, 2026-11-04):** la **fecha requerida del RQ** es la que escribió el solicitante y solo se muestra como dato; **la fecha en obra** es la que manda en el cronograma. El cronograma lleva su propia fecha de procura, aparte de lo que diga el RQ.
- **Fecha en obra** = el **primer día con metrado programado** de la actividad del RQ en el **Plan Maestro aprobado** de su servicio (si el RQ tiene varias actividades, el día más temprano). Verificado el 2026-11-04 con PS-108-2026: el RQ guarda su actividad (`actividad_id`) y esa misma actividad está en las líneas del Plan Maestro aprobado (`plan_maestro_partidas.actividad_id` → `plan_maestro_asignaciones.fecha`); p. ej. VP-PL-004 (2.4.1) → 05.11.2026. Si el RQ no tiene actividad o su actividad no está programada, queda **«Sin fecha en obra»** hasta que se configure (ver D2); **nunca se toma la fecha requerida del RQ**.
- **Fechas de la procura, hacia atrás desde la fecha en obra (Victor, 2026-11-04):**
  1. **Llega a destino** = fecha en obra − **días de llegada** (por defecto **1**: el material llega un día antes a donde se requiere).
  2. **Cierre de compra** (la compra debe estar finalizada) = fecha en obra − **días de cierre** (por defecto **7**).
  3. **Inicio de procura** = cierre de compra − **tiempo de procura** (cada RQ tiene el suyo: unos 10 días, otros 30).
- **Cada RQ es configurable** (Victor, 2026-11-04: «cada requerimiento es diferente»): tiempo de procura, días de cierre, días de llegada y días de «por vencer», todos en **días hábiles** (lunes a sábado sin feriados). Los valores por defecto (tiempo de procura 7, cierre 7, llegada 1, por vencer 3) se configuran una vez y cada RQ los puede cambiar; lo cambian administrador y jefe de proyectos, y queda en el historial.
- **Cronograma de barras de colores**, una fila por RQ, sobre una escala de días:
  - **Plan:** barra de **procura** (inicio → cierre de compra), tramo de **entrega** (cierre → llegada) y marca de **en obra**.
  - **Real** (debajo, sin mezclarse con el plan): desde que el RQ se aprueba hasta que llega a 100 % (Comprado).
  - **Colores por estado:** gris = aún no empieza; azul = en procura a tiempo; ámbar = por vencer; rojo = atrasado; verde = comprado. Línea vertical de **hoy**.
- **Estado de compra** de cada RQ del cronograma: **Pendiente** (aún no recepcionado), **En proceso** (recepcionado con avance menor a 100 %), **Comprado** (100 % automático o a mano). Se muestra también la barra de avance.
- **Alertas**, calculadas cada vez que se abre la pantalla con la fecha de hoy (Lima):
  - **Debe iniciar:** hoy ya pasó el inicio de procura y el RQ aún no está aprobado.
  - **Por vencer:** no comprado y el cierre de compra llega en los próximos días (cantidad configurable, por defecto 3; D3).
  - **Atrasado:** no comprado y ya pasó el cierre de compra.
  - **Próximas compras:** el inicio de procura cae en los próximos 15 días.
  - **Sin fecha en obra:** la actividad no está en el Plan Maestro aprobado o el RQ no tiene actividad.
  - **Comprado a tiempo / Comprado tarde:** fecha de compra ≤ o > cierre de compra.
- **Pantalla «Cronograma procura»** (a pantalla completa, como el Status RQ): arriba, tarjetas con el conteo de cada alerta (al hacer clic, filtran); debajo, el **cronograma de barras** con, a la izquierda, N° OT, código, actividad (WBS y nombre), tiempo de procura, inicio, cierre, llegada, en obra, F. requerida del RQ (solo dato), avance y estado; botón **Configurar** por RQ. Filtros por servicio, estado y alerta. Con `?proyectoId=` preselecciona el servicio.
- **Descargas:** «Descargar cronograma (PDF)», «Descargar cronograma (Excel)» e «Informe de alertas (PDF y Excel)», según el filtro activo, con el encabezado de PDF configurable que ya existe (flujos 27 y 14).
- **Historial** de la marca y del comprado manual: quién y cuándo (también si un SÍ pasa a NO).

### No alcance

- El **Excel de fabricaciones del PS-108** (civil, estructuras, madera; `…cronograma-requerimiento-fabricacion-v2.xlsx`): Victor lo usará para **otra interfaz más adelante** (2026-11-04). Va a «Elementos postergados».
- Marcar por material, cotizaciones, proveedores, órdenes de compra o costos de la compra.
- Avisos/notificaciones de alertas (se puede proponer después).
- Cambiar la actividad de un RQ desde esta pantalla.

### Usuarios / roles afectados

- **Marcar SÍ/NO y marcar Comprado a mano:** administrador y jefe de proyectos (Victor, 2026-11-04). El servidor lo valida.
- **Ver la pantalla y descargar:** **los 13 roles** (Victor, 2026-11-04, D1).
- **Configurar un RQ** (tiempo de procura, días de cierre, de llegada y de «por vencer», actividad o fecha en obra) y **los valores por defecto:** administrador y jefe de proyectos.

### Reglas de negocio y documentos afectados

| Documento | Cambio |
|---|---|
| [05 RQ](../../04-flujos-de-negocio/05-rq.md) | Marca «Va a procura» en el Status, quién la cambia, «Comprado» al 100 % y su fecha |
| Flujo nuevo **29 — Cronograma de procura** | Toda la regla de la pantalla, fechas, estados, alertas y descargas; su línea `Lee si:` y su fila en el índice |
| [14 Accesos](../../04-flujos-de-negocio/14-accesos-y-restricciones.md) y artefacto «Matriz de permisos» | Pantalla, chip y acciones nuevas por rol. **El artefacto no abre con esta cuenta** (memoria del 2026-10-19): Victor lo actualiza o lo comparte como editor |
| [16 Paneles](../../04-flujos-de-negocio/16-paneles.md) | Grupo «Seguimiento» y chip «Cronograma procura» |
| [20 Plan Maestro](../../04-flujos-de-negocio/20-plan-maestro.md) | Solo una nota: el cronograma de procura lee la versión aprobada (no cambia ninguna regla del Plan Maestro) |

### Datos, API, migraciones o dependencias

- **Migración aditiva `db/132`** (no borra ni renombra nada) en `proyecto_requerimientos`: `procura` (`POR_DECIDIR` / `SI` / `NO`, por defecto `POR_DECIDIR`), `procura_decidido_por_id`, `procura_decidido_en`, `procura_comprado_en` (fecha de compra), `procura_comprado_manual` (sí/no), `procura_comprado_por_id`, `procura_dias` (tiempo de procura), `procura_dias_cierre`, `procura_dias_llegada` y `procura_fecha_obra_manual` (solo si D2 lo acepta). Tabla de valores por defecto (tiempo de procura, 7, 1 y días de «por vencer»). Tabla `requerimiento_procura_historial` (RQ, campo, valor anterior, valor nuevo, quién, cuándo). Los 19 RQ que ya existen quedan en «Por decidir». La aplica Victor (se le da la ruta completa del SQL).
- **Comprado automático:** en el mismo paso del servidor que pasa el RQ a Atendido (`cambiar-estado-rq` / estado por material), se guarda `procura_comprado_en` = hoy (Lima) si el RQ va a procura y aún no tiene fecha.
- **API nuevas:** cambiar la marca y el comprado manual (PATCH sobre el RQ, validando rol en el servidor y que el RQ exista); leer el cronograma de varios servicios; exportar PDF y Excel. La fecha de necesidad se calcula al leer, desde el Plan Maestro aprobado (no se guarda una copia).
- Reutiliza: `avanceItemsRq` (barra), el exportador de PDF y Excel ya usado en el Status RQ y en Status de servicios, el encabezado de PDF configurable.

### Diseño / UI aplicable

Mismo estilo que el Status de requerimiento (tabla a pantalla completa, filtros en cabecera, «Personalizar campos», chip «Salir a Mi entorno»), tarjetas de conteo como las del dashboard de Status de servicios, colores de alerta: rojo atrasado, ámbar por vencer, azul próximas, gris sin fecha, verde comprado. Scroll horizontal en la tabla sin perder N° OT y código. Se verifica con captura propia a 1366 px antes de entregar.

### Riesgos y decisiones pendientes

Decisiones respondidas por Victor el 2026-11-04:

| # | Decisión | Respuesta de Victor |
|---|---|---|
| D1 | ¿Quién **ve** la pantalla y descarga? | **Todos** (los 13 roles) |
| D2 | RQ marcado SÍ **sin actividad** (hoy 14 de los 19 del PS-108) | En «Configurar» se elige la **actividad del cronograma** del RQ (de ahí sale la fecha en obra del Plan Maestro); si el material no es de ninguna actividad, se escribe la fecha en obra a mano |
| D3 | Días de **«Por vencer»** antes del cierre de compra | **3 por defecto, configurable** (en los valores por defecto y por RQ) |
| D4 | Comprado = **100 % atendido** | Sí |
| D5 | Un Comprado a mano se puede desmarcar | Sí, los mismos dos roles, con historial |
| D6 | Días **hábiles** o calendario | **Hábiles**: lunes a sábado sin feriados (se reutiliza `src/lib/calendario/feriados.ts`, `esDiaHabil`) |
| D7 | **Tiempo de procura** por defecto de un RQ nuevo | **7 días** hábiles; se cambia por RQ |

- Riesgo: un Plan Maestro aprobado nuevo cambia las fechas de necesidad (es lo correcto: siempre se lee la versión aprobada vigente).
- Riesgo: RQ sin actividad no tienen fecha del Plan Maestro; por eso la tarjeta «Sin fecha».

### Criterios de aceptación

1. Un RQ nuevo aparece como «Por decidir» en el Status y suma en su contador.
2. Solo administrador y jefe de proyectos cambian la marca; otro rol recibe 403 del servidor aunque llame la API directo.
3. Al marcar SÍ, el RQ aparece en el Cronograma procura sin recargar a mano; al pasar a NO, sale.
4. La fecha en obra de VP-PL-004 (PS-108-2026) es 05.11.2026 (primer día de 2.4.1 en el Plan Maestro v6 aprobado); con los valores por defecto, llegada = un día antes, cierre de compra = 7 días antes e inicio = cierre − su tiempo de procura. Al cambiar el tiempo de procura de un RQ, solo su barra se mueve.
4b. La fecha requerida del RQ se ve como dato y no mueve ninguna barra.
5. Al llevar todos los materiales de un RQ a Atendido, el RQ sale «Comprado» con la fecha de ese día, sin tocar nada más.
6. Las tarjetas de alerta cuentan bien con la fecha de hoy y filtran la tabla.
7. El PDF y el Excel del cronograma y del informe salen con el filtro activo.
8. Funciona con varios servicios a la vez.

### Estrategia de prueba / evidencia

Pruebas unitarias del cálculo de fecha de necesidad, estado de compra y alertas; pruebas de API (marca, permisos 403, comprado automático); verificación en pantalla con captura a 1366 px; prueba con los RQ reales del PS-108 en solo lectura; prueba de escritura solo sobre el servicio de prueba. Commit y push a `main`; Victor revisa en la app publicada.

### Aprobación (Gate Spec)

- [x] Victor aprueba este Spec (y responde D1 a D5 o acepta las propuestas por defecto).

## Referencia al Spec aprobado

Pendiente del Gate Spec.

## Objetivo, alcance y no alcance

- Resultado esperado, alcance y no alcance: los del Spec.
- Validación esperada: pruebas unitarias y de API en verde, `tsc` sin errores, captura propia a 1366 px de cada pantalla, commit y push a `main` por tanda; Victor revisa en la app publicada.

## Entorno, repositorios, ramas y worktrees

Trabajo directo en `main` de `py_control_proyectos_web` (app) y `pg_control_proyectos` (docs), como se viene haciendo; sin worktrees. Ejecución en esta sesión, sin subagentes (lote de trabajo normal, no flujo de Orquestador). Escritura de datos de prueba solo en el servicio de prueba; los RQ reales del PS-108 solo se leen.

## Skills aplicables

`verificar-permisos-por-rol` en la tanda 3 (pantalla y acciones nuevas por rol). `cerrar-tanda` al terminar cada tanda.

## Fases y dependencias

| Tanda | Qué | Depende de |
|---|---|---|
| T1 — Datos y cálculo | Migración aditiva `db/132` (columnas de procura en `proyecto_requerimientos`, historial y valores por defecto); módulo de cálculo puro: fecha en obra desde el Plan Maestro aprobado, fechas hacia atrás en días hábiles, estado de compra, color y alertas; pruebas unitarias | — (Victor aplica `db/132`) |
| T2 — Servidor | API: marcar SÍ/NO, configurar un RQ, comprado a mano y valores por defecto (solo administrador y jefe de proyectos, 403 a los demás, con historial); leer el cronograma de varios servicios (los 13 roles); comprado automático al pasar el RQ a Atendido; pruebas de API | T1 |
| T3 — Pantallas | Status RQ: columna «Va a procura» con contador de «Por decidir»; grupo **Seguimiento** y chip **Cronograma procura**; pantalla con tarjetas de alerta, cronograma de barras (plan y real, línea de hoy) y panel **Configurar**; captura a 1366 px | T2 |
| T4 — Descargas | PDF y Excel del cronograma y del informe de alertas, según el filtro, con el encabezado de PDF configurable | T3 |
| T5 — Documentación | Flujo nuevo 29 y su fila en el índice; flujos 05, 14, 16 y nota en 20; aviso a Victor para la Matriz de permisos | T1–T4 |

## Punch List embebida

| # | Ítem | Tanda | Estado |
|---|---|---|---|
| 1 | `db/132` aditiva + ruta completa del SQL a Victor | T1 | Hecho (app `4847835`); aplicada por Victor el 2026-11-04 |
| 2 | Cálculo de fecha en obra (primer día con metrado de la actividad en el PM aprobado; varias actividades = el más temprano; manual si no hay actividad) | T1 | Hecho (app `4847835`, 18 pruebas) |
| 3 | Fechas hacia atrás en días hábiles: llegada, cierre, inicio | T1 | Hecho (app `4847835`, 18 pruebas) |
| 4 | Estado de compra, color de la barra y las 7 alertas | T1 | Hecho (app `4847835`, 18 pruebas) |
| 5 | API marcar / configurar / comprado a mano / valores por defecto con 403 e historial | T2 | Hecho (app `e6a3446`; 293 pruebas, tipos y lint en verde) |
| 6 | API lectura del cronograma multi-servicio | T2 | Hecho (app `e6a3446`; consultas comprobadas en solo lectura con PS-108: VP-PL-004 → en obra 05.11) |
| 7 | Comprado automático al llegar a 100 % | T2 | Hecho (app `e6a3446`; no pisa un comprado a mano) |
| 8 | Columna «Va a procura» y contador en el Status RQ | T3 | Hecho (app `f0bdb42`; filtrable, también en el PDF del listado; en producción: 19 «Por decidir») |
| 9 | Grupo Seguimiento + chip Cronograma procura | T3 | Hecho (app `f0bdb42`; después de Logística, con Notificaciones como los demás grupos; visto en producción) |
| 10 | Pantalla: tarjetas, barras plan/real, hoy, filtros, Configurar | T3 | Hecho (app `f0bdb42`; captura a 1366 px con datos de ejemplo en una página temporal ya borrada, porque aún no hay RQ en SÍ; el cronograma de barras va arriba y el detalle abajo para que las barras se vean con los dos paneles abiertos) |
| 11 | Verificación por rol (13 ven; 2 editan) | T3 | Hecho en producción con las dos cuentas de prueba: administrador ve y edita; la cuenta sin administración ve el cronograma y la marca, sin selector ni «Valores por defecto», y el servidor responde 403 a marcar y a cambiar valores. Pendiente: guardar un cambio real (lo hace Victor al marcar el primer RQ) |
| 12 | PDF y Excel del cronograma | T4 | Pendiente |
| 13 | PDF y Excel del informe de alertas | T4 | Pendiente |
| 14 | Flujos 29, 05, 14, 16, 20 e índice | T5 | Pendiente |
| 15 | Matriz de permisos (Victor la actualiza o comparte como editor) | T5 | Pendiente de Victor |

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-11-04 | La tarea es en la app (no un Excel): marca SÍ/NO en Status RQ y pantalla «Seguimiento › Cronograma procura» | Victor |
| 2026-11-04 | Descargas en PDF y Excel; informe de alertas (por vencer, próximas, no comprados a tiempo) | Victor |
| 2026-11-04 | RQ al 100 % = Comprado automático; también a mano | Victor |
| 2026-11-04 | Marcan administrador y jefe de proyectos | Victor |
| 2026-11-04 | Fechas cruzadas con el Plan Maestro; para todos los servicios | Victor |
| 2026-11-04 | Respuestas D1–D7: ven todos; RQ sin actividad se configura; por vencer 3 configurable; comprado = 100 %; desmarcable; días hábiles; tiempo de procura por defecto 7 | Victor |
| 2026-11-04 | Fecha requerida del RQ ≠ fecha en obra; el cronograma usa la fecha en obra. Llega 1 día antes, compra cerrada 7 días antes, tiempo de procura propio de cada RQ (10, 30 días…); todo configurable por RQ; cronograma de barras de colores | Victor |
| 2026-11-04 | Barra de avance por materiales atendidos en el Status RQ, hecha antes del Spec (app `800af77`, docs `b9f6658`) | Victor |
| 2026-11-04 | Grupo Seguimiento después de Logística, con su chip Notificaciones como los demás grupos; en Configurar también se puede cambiar la marca (No o Por decidir = sale del cronograma) | Orquestador (operativo) |

## Libro de hallazgos

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|

## Mejoras (de trabajo)

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| M1 | 2026-11-04 | Orquestador | Antes de ejecutar un prompt preparado, confirmar con Victor si el resultado va en la app o en un archivo: el prompt pedía un Excel y Victor quería la función en la app | `03-aprendizaje-continuo/` | Registrada | |

## Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| R1 | 2026-11-04 | Orquestador | Barra de avance del Status RQ = materiales Atendidos ÷ materiales del RQ; reemplaza «el Status no muestra avance parcial» | Flujo 05 | Trasladada | `b9f6658` |

## Observaciones sobre la política

Ninguna.

## Preguntas abiertas a Victor

| ID | Fecha | Qué | Estado |
|---|---|---|---|
| P1 | 2026-11-04 | Otra sesión está agregando el estado «Comprado» por material (Logística cierra la compra y anota la fecha de llegada a almacén; `db/133`, sin publicar). D4 dice «Comprado = 100 % atendido». ¿El cronograma debe tomar como comprado el RQ cuando todos sus materiales están Comprados (cierre de compra real) y usar su fecha de llegada como llegada real? | Consultada |

## Carpetas/archivos huérfanos

Ninguna.

## Elementos postergados propuestos para planes futuros

- Interfaz para el Excel de fabricaciones del PS-108 (civil, estructuras, madera, módulos; `pg_planeamiento/…/03_cronograma/PS-108-2026_fase-2_cronograma-requerimiento-fabricacion-v2.xlsx`) — Victor, 2026-11-04.
