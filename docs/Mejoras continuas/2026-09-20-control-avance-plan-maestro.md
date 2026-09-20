# Lote 2026-09-20 — Flujo 18 (control de avance): cerrar Plan Maestro (20) y volver a pendientes de 18

## Contexto

`18-control-avance.md` agrupa la metodología completa de control de proyectos (la cadena Presupuesto → WBS → Paquetes → Cronograma → Plan Maestro → 3WLA → RDT → PR → Dashboard). No es un flujo más al mismo nivel que los demás: los demás son piezas de esa cadena.

Orden de trabajo acordado con Victor: se está cerrando **20-plan-maestro** (la pieza en construcción ahora). Al terminarlo, se regresa a los pendientes generales de **18-control-avance**.

Estos pendientes vivían dentro de `docs/Flujos de trabajo/20-plan-maestro.md` (sección "Pendiente (Fase 2)") — se movieron aquí porque un archivo de `Flujos de trabajo/` es la especificación estable del tema, no el lugar para trackear pendientes. Los pendientes viven en `Mejoras continuas/`, según `docs/README.md`.

## Pendiente — Plan Maestro (flujo 20), Fase 2

- Vista detallada diaria por semana: `Prog.` y `Real` por día, con HH y observación cuando existan.
- Acumulados por partida: metrado real, metrado restante, avance físico, PV y EV.
- HH reales, rendimiento, HH ganadas e IP, cuando el modelo de datos permita atribuirlas de forma trazable a la partida.
- AC, CV, CPI, SPI y Curva S, sin usar valorización planificada como costo real.
- Cierre semanal auditado: incidencias, causa de variación, acción siguiente y estados abierta/en revisión/cerrada/reabierta.
- Interfaz de revisión y rechazo de RDT con motivo visible e historial de corrección.
- Integración de indicadores consolidados hacia PR y Dashboard.
- Verificación de pertenencia de usuario por servicio/proyecto, además de rol.
- Vista móvil semanal compacta.

Notas de lo pospuesto a `mejoras-futuras.md` (2026-09-20):
- "Paquetes de trabajo, área, disciplina y frente como filtros operativos".
- "3WLA como plan operativo separado" — el objetivo actual del flujo 18 es la cadena RDT → PR → Dashboard (EVM); 3WLA queda fuera de ese alcance por ahora (ver mejoras-futuras.md para el detalle).

## Pendiente — flujo 18 (control de avance), general

A definir por Victor cuando se retome, una vez cerrado el flujo 20.

## Avance — sub-lote 1: RDT rechazo + historial (2026-09-20)

Implementado en `py_control_proyectos_web` (código local, sin commit/push todavía):

- Ya existía a nivel de API/DB: `PATCH /api/rdts/partes/[id]` con acción RECHAZAR + motivo, columnas `estado_validacion`/`motivo_rechazo` en `rdt_partes` (migración 040).
- Nuevo: `db/041_rdt_partes_historial.sql` — tabla `rdt_partes_historial` + reemplazo de `guardar_rdt_parte()` para que guarde una foto completa del parte (cabecera + actividades + tareo + equipos) antes de cada corrección. **Falta aplicarla en Supabase** (y confirmar que la 040 ya esté aplicada).
- Nuevo: `GET /api/rdts/partes/[id]/historial` — devuelve el historial de un RDT por (proyecto, fecha, turno).
- UI en `TablaStatusRdts.tsx` (pantalla `/rdts/status`): botón Rechazar junto a Validar, etiqueta "Rechazado" con el motivo en tooltip, y botón de Historial (ícono reloj) que abre `ModalHistorialRdt.tsx`.
- Verificado: `tsc --noEmit` sin errores, `eslint` limpio, 78 tests unitarios pasan, `next build` completo sin errores.
- **Cargado como checklist en la Punch List de Mejoras** ("RDT: rechazo visible con motivo + historial de corrección") — pendiente que Victor aplique la migración 041, haga commit/push, y verifique cada ítem ahí.
- Ajustes hechos durante la verificación en vivo de Victor (mismo día):
  1. El badge "Rechazado" era texto de 10px al lado de los mismos botones — invisible en la práctica. Se cambió a un badge con fondo rojo y el motivo escrito directamente (no solo en tooltip).
  2. El historial solo capturaba una corrección completa del parte (Crear RDTs), no un simple Validar/Rechazar sobre el mismo RDT — se agregó una foto al historial también en `PATCH /api/rdts/partes/[id]` antes de cada cambio de estado.
  3. Validar un RDT que había sido rechazado, sin corregir nada, no dejaba ninguna explicación. Nuevo: `db/042_rdt_partes_historial_accion.sql` agrega `accion`/`motivo_accion` a `rdt_partes_historial` — validar así ahora pide un motivo obligatorio ("¿por qué se valida sin corregir?"), y el historial muestra la acción (Corrigió/Validó/Rechazó) y su motivo. **Falta aplicar esta migración también en Supabase.**
  4. Victor rechazó un RDT y no encontró cómo corregirlo — no existía ningún camino visible (había que ir a Crear RDTs y retipear todo desde cero, sin saber que reemplazaba al anterior). Nuevo: link **"Corregir"** en Status de RDTs (para cualquier RDT no Validado) que abre Crear RDTs con `?editarId=`, precargado con los datos reales del RDT (actividades, personas, horas, equipos — reutiliza la misma lógica de "plantillas" ya existente, `aplicarDatosPlantilla`). Al guardar, sigue el mismo flujo de reemplazo que ya existía (confirmación + queda en el historial).

## Avance — sub-lote 1, ronda 3: hallazgos de Victor probando Crear RDTs (2026-09-20)

Victor probó el formulario completo y encontró 3 cosas:

1. **Corregir el parte completo no pedía motivo** (a diferencia de Validar/Rechazar). Nuevo `db/043_rdt_correccion_motivo.sql`: `guardar_rdt_parte()` recibe `p_motivo_correccion` (default null, no rompe llamadas viejas); el formulario ahora pide "¿qué se observó y cómo se corrigió?" al confirmar el reemplazo, y queda en `rdt_partes_historial.motivo_accion`. **Falta aplicar esta migración en Supabase.**
2. **Bug real de alineación**: en la tabla de Tareo de Crear RDTs, la fila "Total HH" usaba `colSpan={5}` en vez de `6` (el encabezado tiene 6 columnas fijas: #, Persona, DNI, Apellidos, Cargo, Especialidad) — los totales por actividad quedaban corridos una columna. Corregido en `FormularioCrearRdt.tsx`.
3. **Validación cruzada nueva**: la suma de HH por persona (fila) y por actividad (columna) debe coincidir siempre — si no coincide, hay horas huérfanas de una actividad borrada. Nueva función `totalPorColumnas()` en `lib/rdts/parte.ts`, usada como aviso visual en la tabla y como validación que bloquea guardar (`erroresDelParte`).

**Aclarado por Victor:** no era un campo específico — era la idea general de no dejar cargar un RDT si falta algo indispensable para que sirva después. Se identificó el hueco real: una actividad Directa (TA=D) sin partida del DP asignada se podía guardar igual, y solo se descubría que estaba incompleta al intentar Validarla (días después). Nuevo: `erroresDelParte()` en `lib/rdts/parte.ts` ahora bloquea el guardado si hay actividades Directas sin `wbs`. No requiere migración (es validación en el formulario/API, no cambia el esquema). 3 tests nuevos.

## Avance — sub-lote 1, ronda 4 (2026-09-20)

- **Bug de despliegue, corregido en el chat:** Claude le pasó a Victor una SQL de la 043 sin el contenido pegado ("arriba tienes el contenido exacto" — pero "arriba" no existía en el chat). Causó el error real `Could not find the function public.guardar_rdt_parte(...)` al intentar crear un RDT. Se le volvió a pasar completa. **Lección: siempre pegar el SQL completo en el mensaje, nunca remitir a una lectura de archivo que el usuario no ve.**
- **Errores técnicos en la UI:** ese mismo error salía crudo (en inglés, con nombres de función Postgres) en el formulario. `POST /api/rdts/partes` ahora registra el error real en el log del servidor y le muestra al usuario un mensaje genérico en español ("problema técnico, avisa al equipo"). Mismo patrón (`error.message` crudo al cliente) existe en otras rutas de la app, no tocado — queda fuera de este lote.
- **Campos obligatorios nuevos:** Victor encontró que se podía cargar un RDT sin Especialidad, Ubicación/Área ni Semana N° (y "Jornada laboral (H)", que es solo referencia visual, ni se guarda). Los tres primeros ahora bloquean el guardado en `erroresDelParte()`; Jornada se valida aparte en el formulario (no vive en el modelo `Parte`). 2 tests nuevos. No requiere migración.
- **Dato ya cargado sin estos campos:** el RDT que Victor guardó antes de este arreglo quedó en la base sin Especialidad/Ubicación/Semana. Se puede corregir con el link "Corregir" (ronda 2) cuando quiera.

## Avance — sub-lote 1, ronda 5 (2026-09-20)

Victor pidió: la comparación de horas de cada persona contra la jornada del día (ya existía, visual, no bloqueante) debe **avisar, no bloquear**, tanto al cargar el RDT como en su revisión posterior — hoy la jornada no se guardaba, así que era imposible mostrarla después.

- Nuevo `db/044_rdt_jornada_horas.sql`: columna `jornada_horas` en `rdt_partes` + parámetro `p_jornada_horas` en `guardar_rdt_parte()`. **Falta aplicar en Supabase.**
- La jornada ahora se guarda al crear el RDT, y se restaura al abrir "Corregir" (mismo resaltado ámbar por persona que ya existía).
- Nuevo en Status de RDTs: si algún trabajador sumó distinto que la jornada del día, la columna HH muestra un ícono de alerta (ámbar) con tooltip — informativo, no bloquea Validar/Rechazar. RDT de antes de esta regla (sin jornada guardada) no muestran nada, no hay con qué comparar.

## Avance — sub-lote 1, ronda 6 (2026-09-20)

Victor probó y el ámbar de la tabla no era suficiente — se puede pasar por alto. Pidió algo explícito, tipo "el trabajador XXXX registra 2 horas menos de la jornada normal, ¿cargamos el RDT?", antes de guardar.

- Nuevo: al guardar (primer intento, no en el reintento de reemplazo), si alguna persona sumó distinto que la jornada, aparece un `confirm()` que lista cada persona con la diferencia exacta ("2h menos", "1h más") y pregunta si continuar. Sigue siendo informativo — cancelar el confirm no guarda, pero no hay forma de "arreglarlo" para que pase: es aceptar y cargar, o cancelar y corregir a mano. No requiere migración.

## Avance — sub-lote 1, ronda 7 (2026-09-20)

Victor corrigió un RDT rechazado y, al volver a Status de RDTs, el link seguía diciendo "Corregir" pero el estado volvió a REGISTRADO — parecía indistinguible de un RDT nunca tocado (aunque el badge "Para revisión" de la ronda anterior sí estaba bien). Pidió: el link debe decir **"Revisar"** por defecto, **"Corregir"** solo si está Rechazado, y **"Revisar" en otro color (ámbar)** si ya tuvo un rechazo antes (aunque ahora esté REGISTRADO) — para diferenciar "nunca tocado" de "ya se corrigió una vez, revisar de nuevo".

- Nuevo `fueRechazadoAntes` en `GET /api/rdts/partes`: consulta `rdt_partes_historial` por `accion = 'RECHAZAR'` para esa (OT, fecha, turno), sin importar si ya se corrigió. No requiere migración (usa la columna `accion` de la 042, ya aplicada).
- Link en Status de RDTs: "Corregir" (rojo) si Rechazado; "Revisar" (ámbar) si tuvo un rechazo antes; "Revisar" (gris/neutro) si nunca se tocó.

## Avance — sub-lote 1, ronda 8 (2026-09-20)

- El badge "Para revisión" (ronda 6) rompía la altura de fila en Status de RDTs. Victor pidió sacarlo: la columna Validación vuelve a ser siempre una sola fila (los dos botones); el motivo del rechazo pasó a tooltip sobre la columna Estado en vez de un badge aparte.
- En Crear RDTs: los botones "+ Actividad", "+ Persona" y "+ Equipo" estaban todos arriba, lejos de sus apartados (2.0, 3.0, Equipos) — solo "+ Material" ya estaba pegado a su sección. Se movió cada botón junto al título de su propio apartado, mismo patrón que Materiales. Ninguno de los dos cambios requiere migración.

## Avance — sub-lote 1, ronda 9, cierre (2026-09-20)

Victor repitió el punto por tercera vez, más claro: **revisar (Validar/Rechazar) no es lo mismo que corregir datos**. El revisor no debería aterrizar en un formulario editable solo por "revisar" — eso ya lo hace con los botones Validar/Rechazar que están al lado. Corregir solo tiene sentido *después* de un Rechazo, nunca antes.

- Simplificado de una vez: el link de editar (antes "Revisar"/"Corregir" con 3 combinaciones de color) ahora **solo aparece cuando el RDT está Rechazado**, y siempre dice **"Corregir"** (rojo). En cualquier otro estado no hay ningún link de editar — solo quedan Validar/Rechazar.
- Se quitó `fueRechazadoAntes` (el flag detrás de la variante ámbar) de la API, el tipo y los tests — quedó sin uso al simplificar.
- No requiere migración.

## Avance — sub-lote 1, ronda 10 (2026-09-20)

Victor corrigió: no había que borrar "Revisar" — debía quedarse, pero **sin función de corregir**, solo para ver el RDT. La ronda 9 se pasó de simple.

- Restaurado "Revisar" (gris, ícono ojo) en Status de RDTs, visible en todas las filas junto a Historial. Abre `/rdts/crear?verId=<id>` en **modo solo lectura**: mismo formulario, pero envuelto en un `<fieldset disabled>` — todos los campos, selects y botones (incluido "Cargar RDT al sistema") quedan deshabilitados, nada se puede editar ni guardar.
- "Corregir" (rojo) sigue existiendo solo para RDT Rechazado, con `?editarId=` (editable, como antes).
- No requiere migración.

## Avance — sub-lote 1, ronda 11 (2026-09-20)

Victor: después de Crear, Corregir o Revisar no había forma clara de volver a Status de RDTs (donde se valida/rechaza y se verifica que la corrección quedó bien).

- Crear RDTs y Corregir: al guardar con éxito, redirige automáticamente a `/rdts/status` (antes solo mostraba un aviso y se quedaba en la misma pantalla).
- Revisar (solo lectura): botón fijo "← Volver a Status de RDTs" debajo del título.
- No requiere migración.

## Avance — sub-lote 1, ronda 12 (2026-09-20)

Victor: unificar las columnas "Descargar" (con Revisar/Corregir) y "Validación" (Validar/Rechazar) en una sola.

- Columna "Descargar" queda solo con descarga de PDF e Historial.
- Columna "Validación" (ahora visible si `puedeValidar` **o** `puedeCorregir`, antes solo `puedeValidar`) agrupa todo: Validado / Validar+Rechazar / Revisar / Corregir, todo en íconos sin texto (antes tenían label) para no crecer la fila.
- No requiere migración.

## Avance — sub-lote 1, ronda 13 (2026-09-20)

Victor: la altura de la tabla (70vh) quedó bien, pero faltaba que el ancho llene el panel central (quedaba espacio muerto a la derecha), el encabezado ocupa más de lo necesario arriba, y la columna Servicio no debe truncarse.

- `/rdts/status/page.tsx`: quitado `max-w-6xl` — la página ya no capa su ancho, llena el panel central.
- `CabeceraPagina.tsx` (compartido en toda la app): espaciado reducido (`mb-3`→`mb-2`, `mb-2`→`mb-1.5`).
- Columna Servicio: se quitó el truncado que se había agregado en la ronda 13 anterior (fue un error, Victor la quería completa) — solo "Cargado por" sigue truncado.
- **Documentada la convención** en `pg_control_proyectos/docs/visual-companion/README.md` (nueva sección "Convención — pantallas de listado en el panel central") para que no haya que repetir este pedido en cada pantalla nueva: sin `max-w-*`, tablas largas con `max-h-[70vh] overflow-y-auto` + header sticky, columnas de texto largo sin truncar salvo secundarias, header compacto.
- No requiere migración.

Nota: "Verificación de pertenencia de usuario por servicio/proyecto" se separó de este sub-lote — la exploración del código mostró que es un cambio estructural mucho más grande (tabla de membresía nueva + tocar casi todas las rutas de escritura), no algo para sumar de paso a esto. Queda como sub-lote 2 propio, a iniciar cuando este quede Conforme.

## Avance — sub-lote 1, ronda 14 (2026-09-20)

Victor pidió consolidar las convenciones de interfaz en un `design.md` propio (reemplazando la sección de convención del `README.md` de `visual-companion/`), y marcó en una captura del Status de RDTs dos problemas de ancho de columna más espacio muerto debajo de la tabla.

**Documentación (`pg_control_proyectos`):**
- Creado `docs/visual-companion/design.md` — sistema de diseño completo (protocolo de agente, tokens, layout, algoritmo de columnas, accesibilidad, checklist de pre-vuelo). Ajustado contra el código real de `py_control_proyectos_web` para no quedar en conflicto: separa el patrón `<BadgeEstado>` (estado de proyecto/servicio) del patrón icono+color de validación (RDT), documenta los colores `rose/emerald/amber` como semánticos de validación (no tokenizados), y agrega una tabla de precedentes ya resueltos (Servicio sin truncar, Cargado por truncado a 130px) para no volver a preguntar.
- `docs/visual-companion/README.md`: se quitó la sección de convención (la reemplaza `design.md`); queda solo como índice de mockups + pointer a `design.md`.
- `docs/Flujos de trabajo/README.md` y `docs/README.md`: agregado pointer a `design.md` como lectura obligatoria antes de crear/modificar cualquier interfaz.
- Deuda técnica reconocida y documentada (no ejecutada): ninguna tabla existente tiene `scope="col"` en sus `<th>` (regla de accesibilidad nueva de `design.md`). Aplica a tablas nuevas/modificadas desde ahora; el retrofit de las 12 tablas existentes queda pendiente, a pedido explícito de Victor.

**Código (`py_control_proyectos_web`) — Status de RDTs:**
- `SelectFiltro.tsx`: agregado prop opcional `ancho` (por defecto el mismo `w-24 max-w-[8rem]` de siempre, sin romper las otras 4 pantallas que lo usan sin pasarlo).
- `TablaStatusRdts.tsx`: columnas de contenido corto (N° OT, Turno, Especialidad) ahora usan un filtro más angosto (`w-20`/`w-16`) — antes el filtro de 96px de ancho, mayor que el contenido real, dejaba una franja vacía dentro de esas columnas (lo que Victor marcó con los óvalos verdes). Altura de la tabla `max-h-[70vh]` → `max-h-[80vh]` para reducir el espacio muerto debajo de la tabla que Victor marcó con la flecha.
- Verificado: tsc limpio, eslint limpio, 409 tests, build limpio. No se verificó visualmente en navegador (Playwright MCP sigue sin conectar) — pendiente que Victor confirme en vivo si el ancho de 80vh y los anchos de filtro quedaron bien, o si hace falta ajustar más.
- No requiere migración.

### Corrección — mismo día: `80vh` seguía sin resolverlo de raíz

Victor probó en vivo: con `80vh` la caja de la tabla quedaba más alta que la ventana real del navegador, así que el borde inferior (con la barra de scroll horizontal) volvía a quedar fuera de la vista — el mismo problema que se había corregido antes, solo que ahora con un número distinto. Cualquier `max-h-[Nvh]` fijo es frágil: depende del alto de la ventana y del alto del encabezado, y tarde o temprano se desalinea.

Fix de raíz, sin adivinar porcentaje: la caja de la tabla ahora usa `flex-1 min-h-0` en vez de `max-h-[Nvh]`, dentro de una columna flex que ocupa el alto real disponible del panel central (`status/page.tsx` con `flex h-full flex-col`, `TablaStatusRdts.tsx` con `flex h-full flex-col`). Así la tabla siempre ocupa exactamente lo que sobra debajo del encabezado y los filtros, sin importar el tamaño de ventana — el borde inferior con el scroll horizontal nunca puede quedar fuera de la vista.

- `status/page.tsx`: `min-w-0 p-1` → `flex h-full min-w-0 flex-col p-1`.
- `TablaStatusRdts.tsx`: contenedor raíz `space-y-3` → `flex h-full flex-col gap-3`; caja de la tabla `max-h-[80vh] overflow-y-auto` → `flex-1 min-h-0 overflow-y-auto`.
- Verificado: tsc limpio, eslint limpio, 409 tests, build limpio. Sigue sin verificación visual en navegador — este es el enfoque técnicamente correcto (alto real disponible, no una fracción de la ventana adivinada), pero falta que Victor lo confirme en vivo.
- No requiere migración.

### Corrección — mismo día: espacio entre encabezado y tabla

Victor marcó en captura el espacio entre `CabeceraPagina` + fila de filtros/controles y el inicio de la tabla: pidió una medida fija y más chica ("una medida definida"), no el `gap-3` suelto que quedaba.

- `TablaStatusRdts.tsx`: contenedor raíz `flex h-full flex-col gap-3` → `gap-2`.
- `design.md` sección 4.3: agregada la fila "Entre bloques de una pantalla de listado" = `gap-2`, para que quede como medida fija documentada y no se repita el pedido en otra pantalla. Versión 1.2.1 → 1.2.2 (ver también el fix de `flex-1 min-h-0` de más arriba, que quedó como 1.2.1).
- Verificado: tsc limpio, eslint limpio, 409 tests, build limpio. Sin verificación visual (Playwright sin conectar) — pendiente confirmación de Victor en vivo, junto con el fix de `flex-1 min-h-0` de este mismo día.
- No requiere migración.

### Corrección — mismo día: fila de filtros se ocultaba al bajar + espacio seguía sin notarse

Victor pidió usar el MCP de Playwright para revisar (sigue sin conectar — mismo `CONNECT_TIMEOUT` de antes, no se pudo reintentar desde la sesión, necesita reinicio de Claude Code). Reportó dos problemas en vivo:

1. **Al bajar el scroll de la tabla, la fila de filtros ("Todos ▾" de cada columna) desaparecía.** Causa real: solo la primera fila del encabezado (`<tr>` de etiquetas) tenía `sticky top-0`; la segunda fila (filtros) no tenía sticky, así que se iba con el resto de filas al hacer scroll. Fix: las dos filas ahora son sticky, apiladas (`top-0 h-6` la primera, `top-6` la segunda).
2. **La reducción de espacio de la ronda anterior no se notaba.** Causa real: `CabeceraPagina` ya trae su propio `mb-2`, y el `gap-2` que le puse al contenedor flex se sumaba encima (8px + 8px = 16px), casi igual que antes. Fix: quitado el `gap` del contenedor; cada bloque (fila de controles, mensaje de error) pone su propio `mb-2` — una sola medida, no se suman.

- `TablaStatusRdts.tsx`: contenedor raíz `flex h-full flex-col gap-2` → `flex h-full flex-col` (sin gap); fila de controles y mensaje de error con `mb-2` propio; encabezado de tabla con las dos filas sticky apiladas.
- `design.md` actualizado a **1.2.3** con ambas correcciones documentadas (secciones 4.3 y 8), para que no se repita ninguno de los dos errores en otra pantalla.
- Verificado: tsc limpio, eslint limpio, 409 tests, build limpio. Sigue sin verificación visual — Playwright no conectó, pendiente que Victor confirme en vivo.
- No requiere migración.

### Corrección — mismo día: el fix del sticky de dos filas empeoró el problema

Victor pidió usar Playwright para revisar (sigue sin conectar, mismo `CONNECT_TIMEOUT`). Mandó captura: con el fix anterior (sticky + `h-6`/`top-6` en el `<tr>` completo) las filas del encabezado quedaban superpuestas con filas de datos al hacer scroll — texto de una fila tapando a otra, peor que el bug original (donde solo desaparecía la fila de filtros).

Causa: `position: sticky` combinado con un alto forzado en dos `<tr>` apiladas es frágil, los navegadores no lo manejan bien. Fix real: mover el `sticky` de la fila a cada celda (`<th>`) — el mismo patrón que ya usa `TablaConsolidadoRdts.tsx` para sus columnas pegadas al desplazar (ahí es horizontal con `left`, acá es vertical con `top`).

- `TablaStatusRdts.tsx`: quitado `sticky`/`h-6`/`bg-bg-elevated` de los dos `<tr>` del `<thead>`; agregado a cada `<th>` de la fila 1 (`sticky top-0 z-20 h-6 bg-bg-elevated`) y de la fila 2 (`sticky top-6 z-20 bg-bg-elevated`), incluidas las celdas vacías (Descargar, Validación).
- `design.md` actualizado a **1.2.4**: regla general agregada — el sticky de un encabezado de varias filas va siempre en la celda, nunca en la fila.
- Verificado: tsc limpio, eslint limpio, 409 tests, build limpio. Sigue sin verificación visual (Playwright no conectó) — pendiente que Victor confirme en vivo, con especial atención a si esta vez sí queda estable al hacer scroll.
- No requiere migración.

## Avance — sub-lote 1, ronda 15: cierre de sesión (2026-09-20)

**Commits realizados:**

- **pg_control_proyectos**: commit 4efc478
  - Creado `docs/visual-companion/design.md` (v1.2.4) como sistema de diseño oficial, reemplazando convenciones dispersas en README.
  - Actualizado `docs/README.md`, `docs/Flujos de trabajo/README.md`, `docs/visual-companion/README.md` — todos apuntan a `design.md` como referencia normativa para interfaces.
  - Actualizado este archivo (`2026-09-20-control-avance-plan-maestro.md`) con todas las rondas 1-14 y el resumen de implementación.

- **py_control_proyectos_web**: commit 6f1e7a1
  - Sumadas todas las migraciones 041-044 (rdt_partes_historial, accion, motivo_correccion, jornada_horas).
  - Sumados todos los cambios de componentes y API para rechazo, historial, modal, y correcciones de layout.
  - Sumadas todas las correcciones de rondas 14-15 (TablaStatusRdts con sticky en <th>, flex-1 min-h-0, spacing sin gap sumado, SelectFiltro con ancho variable).
  - Build: tsc limpio, eslint limpio, 409 tests pasando, build completo sin errores.

**Estado del sub-lote 1:**
- ✅ Código: 100% implementado y testeado en local.
- ✅ Documentación: design.md v1.2.4 lista como sistema oficial.
- ⏳ Verificación en vivo de Victor: pendiente. Ítems críticos a confirmar:
  - Ancho de página llena el panel central (sin `max-w-*`).
  - Espaciado entre encabezado y tabla es fijo (`mb-2` en cada bloque, sin `gap` sumado).
  - Filtros en fila 2 permanecen visible al desplazar (sticky en `<th>`, no en `<tr>`).
  - Tabla llena alto disponible (`flex-1 min-h-0`, borde con barra de scroll siempre visible).
  - SelectFiltro más angosto funciona sin quebrar columnas (N°OT, Turno, Especialidad).

**Status:**
- Sub-lote 1 completo en código/docs.
- Migraciones SQL: falta aplicar 041-044 en Supabase (Victor debe hacerlo o indicar si ya se aplicaron).
- Siguiente paso: Victor verifica en navegador con ventana en varios tamaños, confirma Punch List, y toca Go/No-Go para pasar a Sub-lote 2 (pertenencia usuario por servicio/proyecto).

## Mejoras a flujos

(vacío por ahora)
