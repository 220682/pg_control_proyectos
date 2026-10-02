# 09 — Importar DP
> Lee si: la tarea toca la importación del DP, sus tres fases de validación, la confirmación de niveles o los tres informes que genera.


Independiente de la generación PR. Excel DP → `proyecto_dp`. Spec `2026-08-16-dp-import`.

**Quién importa:** administrador y jefe de proyectos, sobre un servicio a su cargo (fila «Importar DP» de la tabla 2 del [flujo 14](14-accesos-y-restricciones.md)). Ver y exportar el DP sigue a la tabla 1 y a la nota 7.

## Arquitectura de validación: 3 fases (Victor, 2026-09-17)

Al importar un DP, el análisis corre en 3 fases secuenciales. Ninguna fase se salta: la 2 solo corre si la 1 no encontró nada, la 3 solo corre si la 2 extrajo datos con éxito.

### Fase 1 — Errores de forma (bloqueante)

Antes de tocar el contenido del presupuesto, escanea el archivo completo buscando problemas de forma/estructura del archivo mismo — no del contenido numérico. Si encuentra al menos uno, sigue analizando TODO el archivo buscando más (no corta en el primero) y devuelve un único **informe de forma** que los lista todos juntos, con la fila/hoja exacta de cada uno. No se extrae ningún dato mientras haya errores de forma sin resolver.

Ejemplos de errores de forma vistos hasta ahora en el presupuesto PS-065 Bancoductos (ya detectados hoy uno a la vez en `parser.ts` / `parser-cd.ts` / `parser-apu.ts` / `parser-gg.ts`, pendiente juntarlos en un solo informe). **Esta lista NO es cerrada** — es lo encontrado en un solo presupuesto real; cada presupuesto nuevo puede traer tipos de error de forma distintos, y se van agregando aquí a medida que aparezcan, sin que eso limite el catálogo a lo ya visto:
- Falta la hoja CD o APU (incluye el caso real: la hoja existe pero con otro nombre — hoy se reporta como "falta", no como "nombre distinto").
- Código de partida (WBS) duplicado en CD, o duplicado dentro de la propia hoja APU (caso real PS-065 Bancoductos: un bloque completo copiado y pegado con el código de otro — 6.1/7.1/8.1 repetidos, infló el costo total ~30%).
- CD no tiene ninguna partida con WBS + metrado numérico.
- Layout de columnas irreconocible en APU o en GG.
- APU no tiene ningún bloque de partida reconocible.
- Partida presente en CD sin bloque en APU, o presente en APU sin fila en CD.

### Fase 2 — Extracción de datos (bloqueante) — método de 4 pasos

Solo corre si la fase 1 no encontró errores de forma. El flujo para extraer HH de mano de obra ya está definido (implementado en `parser-apu.ts`, ver [[reference-apu-parser-mismatch]] y [[reference-hh-presupuesto-ps065]] en la memoria de Claude):

1. Por cada insumo de mano de obra, comparar `Cantidad × PU` vs `Cuadrilla × Cantidad × PU` contra el `Parcial` real que el Excel ya trae. El que coincide dice si ese presupuesto ya trae la cuadrilla incorporada en Cantidad o no (fila por fila; las filas con Cuadrilla=1 no distinguen, hay que mirar las que tienen Cuadrilla≠1).
2. HH por unidad de metrado = suma de Cantidad de esa partida (o Cuadrilla × Cantidad, según lo que diga el paso 1).
3. HH por partida = HH por unidad × metrado real de esa partida (cruzado por WBS contra CD/PS, nunca por posición ni copiado de otra fila).
4. HH contractual = suma de HH por partida de todo el presupuesto.

Si siguiendo estos 4 pasos el sistema no logra extraer datos de alguna partida (ej. una fila que rompe la lógica de extracción pese a haber pasado la fase 1 limpia), emite un **informe de fondo** y no continúa a la fase 3. Igual que en la fase 1, los motivos de informe de fondo vistos hasta ahora no son una lista cerrada — el único visto en PS-065 es la anotación de texto "AJUSTE HH: ..." que no trae fila "Mano de obra:" real (ver [[reference-hh-presupuesto-ps065]]); van apareciendo más con cada presupuesto nuevo.

### Fase 3 — Observación de importación de DP (no bloqueante)

Solo corre si la fase 2 extrajo los datos con éxito. Compara lo extraído contra lo esperado (ej. una partida indica una actividad pero no tiene HH). Si encuentra algo raro o distinto, **no bloquea**: completa la importación igual y deja la observación guardada de forma durable, visible mientras dure el proyecto — mismo criterio ya aplicado para "partidas sin mano de obra" (`028_dp_resumen_no_restrictivo.sql`, columna `observaciones` en `proyecto_dp`). Tampoco es una lista cerrada: cada tipo nuevo de discrepancia detectada se suma al catálogo de observaciones, no reemplaza a las anteriores.

## Paso de confirmación de niveles (plan niveles-paquetes-plan-maestro-rdt, 2026-09-30)

Las tres fases se conservan. Entre el análisis y el guardado se suma un paso de **confirmación de niveles**: el archivo se analiza primero sin guardar (`soloAnalizar`) y la pantalla de Importar DP pasa a dos pasos.

- **Cuenta de niveles.** El sistema detecta cuántos niveles tiene la estructura del presupuesto (de 2 a 5; la detección admite códigos con puntos, esquema, ancho fijo, sangría o lista plana). El nivel 1 es el Servicio (implícito si el presupuesto no trae esa fila). Un servicio con profundidad fuera de 2 a 5 muestra error y no deja aprobar.
- **Rol por nivel.** Cada nivel lleva un rol elegido en un desplegable (orden fijo; Servicio y Partida son obligatorios y Partida va en el último nivel). El rol se guarda **por nivel**, no por grupo de hermanas: cambiar uno cambia todo el nivel, y la pantalla lo dice.
- **Fila de muestra por grupo.** Cada grupo de hermanas (mismo nivel y mismo padre) muestra una fila de muestra con «Ver N hermanas»; confirmar el rol confirma el grupo completo. Las columnas Und. y Met. van separadas.
- **Filas «para revisar».** Una hermana cuya profundidad de subárbol difiere de la de su grupo se marca «para revisar». **Mientras haya filas para revisar sin confirmar, «Aprobar niveles» queda bloqueado.** Una partida directa del subpresupuesto que convive con paquetes no se marca como error.
- **Mapa guardado.** Al aprobar se guarda el mapa (`servicio_niveles`) y los encabezados de cada nivel (`servicio_encabezados`, origen DP) con `confirmado = true`; sin confirmar se guarda el propuesto con `confirmado = false`. Subpresupuestos y paquetes de partidas (`dp_subpresupuestos`, `dp_paquetes`) se siguen poblando con el patrón de código de 1 y 2 segmentos para lo que aún los consume; un DP de 3 niveles produce el mismo agrupamiento de siempre. DP y PR agrupan según el mapa; sin mapa, como antes.

### Recarga bloqueada

Volver a importar un DP sobre un servicio con datos derivados se evalúa antes de guardar:

- **Con Plan Maestro `APROBADO`: recarga bloqueada** (409, sin opción de continuar). Para cambiar el DP hace falta antes una versión nueva del Plan Maestro (flujo 20).
- **Sin Plan Maestro aprobado:** si hay algo que perder (vínculos del cronograma, paquetes, borrador del Plan Maestro) se muestra el **aviso de lo que se perdería** y una casilla de confirmación (`confirmarPerdida`); sin confirmar no se reemplaza. Si no hay nada que perder, la carga es libre. Un borrador no bloquea.
- La conciliación de partidas (flujo existente) es un aviso distinto; al reenviar con resoluciones se reenvía también la confirmación.

### Resolución automática — a futuro, no ahora

Más adelante se planea sumarle al agente capacidad de **resolver** algunos de estos hallazgos por su cuenta (ej. renombrar/ubicar una hoja con nombre distinto, elegir la fila correcta ante un WBS duplicado). Por ahora el agente solo **detecta y reporta** las 3 fases — no corrige nada automáticamente. Esa capacidad queda pendiente hasta que Victor la pida.

## Los 3 informes resultantes

| # | Informe | Fase | ¿Bloquea la importación? |
|---|---------|------|---------------------------|
| 1 | Informe de forma | 1 | Sí |
| 2 | Informe de fondo | 2 | Sí |
| 3 | Observación de importación de DP | 3 | No |

## Estado de implementación (2026-09-17)

**Fase 1 (informe de forma) implementada.** `parsearWorkbookDP` (`src/lib/dp/parser.ts`) ya no corta en el primer error: revisa hoja CD, hoja APU, hoja GG y el cruce de partidas entre CD/APU cada uno por su lado, junta TODOS los mensajes en `ErrorParseoDP.erroresDeForma` (array) y solo entonces lanza el informe único. `leerCD` (`parser-cd.ts`) junta TODOS los WBS duplicados de CD, y `leerAPU` (`parser-apu.ts`) hace lo mismo para WBS duplicado **dentro de APU** — este último es el chequeo que agarra el caso real que originó todo este pedido (6.1/7.1/8.1 repetidos en PS-065 Bancoductos), verificado corriendo `leerAPU` contra ese archivo real: detecta los 3 duplicados con su fila exacta. La API (`route.ts`) devuelve `errores: string[]` y la pantalla de importar DP (`importar-dp.tsx`) los lista todos.

**Fase 3 (observaciones) — se agregó un chequeo nuevo.** `calcularResumen` (`agregacion.ts`) compara, por cada bloque de APU, el "Costo Unitario" que la propia hoja declara contra la suma de los insumos que el parser reconoció; si no cuadra (fuera de tolerancia de redondeo) queda como observación no bloqueante, mismo mecanismo que "partida sin mano de obra". **Importante:** este chequeo, corrido contra los 51 bloques reales de PS-065, dio 0 falsos positivos pero tampoco detectó el caso de 6.1/7.1/8.1 — cada copia duplicada es internamente consistente consigo misma, así que ese caso lo agarra el chequeo de WBS duplicado en APU (arriba), no este. Quedan como dos chequeos complementarios, no uno reemplazando al otro.

**Sin implementar:** informe de fondo (fase 2) sin un caso concreto pedido todavía; generalizar observaciones más allá de estas dos (sin mano de obra, Costo Unitario) queda para cuando aparezca un caso nuevo.
