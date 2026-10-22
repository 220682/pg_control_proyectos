# 09 — Importar DP
> Lee si: la tarea toca la importación del DP, sus tres fases de validación, la confirmación de niveles o los tres informes que genera.


Independiente de la generación PR. Excel DP → `proyecto_dp`. Spec `2026-08-16-dp-import`.

**Quién importa:** administrador y jefe de proyectos, sobre un servicio a su cargo (fila «Importar DP» de la tabla 2 del [flujo 14](14-accesos-y-restricciones.md)). Ver y exportar el DP sigue a la tabla 1 y a la nota 7.

**Botón "Cargar" + barra de progreso (O1, Victor 2026-10-02):** la pantalla muestra un botón "Cargar DP" (antes "Importar / reimportar DP") y una barra de progreso (`<progress>`) durante el análisis y la importación, para que el usuario vea que el sistema está procesando el archivo.

**Qué archivos acepta (Victor, 2026-10-15).**
- **Formato:** Excel `.xlsx` y `.xls` (Excel 97-2003, como bajan los presupuestos de ventas). El formato se reconoce por el contenido del archivo, no por la extensión. El `.xls` se abre con el lector SheetJS, que pasa a la app los valores ya calculados y el formato de número de cada celda.
- **Uno o varios archivos:** el presupuesto puede venir en un solo libro o repartido (partidas, APU y GG en archivos separados, como PROPUE_1 Jahuay). Se eligen juntos y las hojas se buscan en todos a la vez.
- **Hoja de partidas sin importar su nombre:** si ninguna hoja se llama «CD», la app reconoce la hoja de partidas por su encabezado (ITEM, a la derecha DESCRIPCIÓN y dos columnas más allá METRADO o CANTIDAD). Así se reconoce la hoja «PS», aunque lleve un espacio al final, y se salta la carátula «PRESUPUESTO». La hoja APU se busca primero por su nombre y, si no, por su forma. Si dos hojas pueden ser la misma, es un error de forma: el sistema no elige por su cuenta.
- **APU en dos formas:** la *clásica*, con la etiqueta de subtotal al cierre («Mano de obra:», «Equipo:»…), y la de *S10*, con el título de la categoría arriba («Mano de Obra», «Materiales», «Equipos», «Subcontratos»), el subtotal sin etiqueta y el encabezado «Descripción Recurso». Las dos usan el mismo método de 4 pasos de la fase 2.
- **Código de partida escrito como número:** se lee como se ve en Excel. Si la celda tiene formato con decimales fijos («0.00»), 1.10 no se confunde con 1.1.

## Arquitectura de validación: 3 fases (Victor, 2026-09-17)

Al importar un DP, el análisis corre en 3 fases secuenciales. Ninguna fase se salta: la 2 solo corre si la 1 no encontró nada, la 3 solo corre si la 2 extrajo datos con éxito.

### Fase 1 — Errores de forma (bloqueante)

Antes de tocar el contenido del presupuesto, escanea el archivo completo buscando problemas de forma/estructura del archivo mismo — no del contenido numérico. Si encuentra al menos uno, sigue analizando TODO el archivo buscando más (no corta en el primero) y devuelve un único **informe de forma** que los lista todos juntos, con la fila/hoja exacta de cada uno. No se extrae ningún dato mientras haya errores de forma sin resolver.

Ejemplos de errores de forma vistos hasta ahora en el presupuesto PS-065 Bancoductos (ya detectados hoy uno a la vez en `parser.ts` / `parser-cd.ts` / `parser-apu.ts` / `parser-gg.ts`, pendiente juntarlos en un solo informe). **Esta lista NO es cerrada** — es lo encontrado en un solo presupuesto real; cada presupuesto nuevo puede traer tipos de error de forma distintos, y se van agregando aquí a medida que aparezcan, sin que eso limite el catálogo a lo ya visto:
- No se encuentra la hoja de partidas o la APU, ni por su nombre ni por su forma. Una hoja con otro nombre ya no es error si su encabezado calza (ver «Qué archivos acepta»).
- Más de una hoja puede ser la de partidas, la APU o la GG (por ejemplo, el mismo APU en dos archivos).
- APU de S10 con insumos sin título de categoría (caso real PROPUE_1 Jahuay, partida 02.02: el PETROLEO D-2 quedó después del subtotal de Mano de Obra, sin el título «Materiales»).
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
- **Mapa guardado.** Al aprobar se guarda el mapa (`servicio_niveles`) y los encabezados de cada nivel (`servicio_encabezados`, origen DP) con `confirmado = true`; sin confirmar se guarda el propuesto con `confirmado = false`. Subpresupuestos y paquetes de partidas (`dp_subpresupuestos`, `dp_paquetes`) se siguen poblando con el patrón de código de 1 y 2 segmentos para lo que aún los consume; un DP de 3 niveles produce el mismo agrupamiento de siempre.
- **Jerarquía completa en toda interfaz (Victor, 2026-10-14).** Toda pantalla que lista partidas muestra **todos los niveles del presupuesto tal cual** (1 → 1.1 → partidas), sin perder el orden jerárquico: una fila por cada nivel (código y nombre, con sangría por profundidad) antes de sus partidas, en el orden del WBS. Rige en DP, PR, Dashboard (matriz de partidas con orden «Por WBS»; los órdenes de ranking, como «Mayor desviación primero», siguen siendo listas planas), Plan Maestro (flujo 20), selector de Crear RDT (flujo 06) y la consulta de partidas del Requerimiento. Los niveles salen del mapa guardado (`servicio_encabezados`, sin el Servicio); sin mapa, se usan los subpresupuestos como primer nivel. **Ningún agrupador se pone por encima de la jerarquía** (Victor, 2026-10-15): ni la disciplina en Crear RDT ni otro criterio; los paquetes y las partidas directas van dentro de su nivel. **La lista de actividades del Cronograma también lleva la sangría de su EDT** (cada nivel se ve un escalón más adentro).

### Recarga bloqueada

Volver a importar un DP sobre un servicio con datos derivados se evalúa antes de guardar:

- **Con Plan Maestro `APROBADO`: recarga bloqueada** (409, sin opción de continuar). Para cambiar el DP hace falta antes una versión nueva del Plan Maestro (flujo 20).
- **Sin Plan Maestro aprobado:** si hay algo que perder (vínculos del cronograma, paquetes, borrador del Plan Maestro) se muestra el **aviso de lo que se perdería** y una casilla de confirmación (`confirmarPerdida`); sin confirmar no se reemplaza. Si no hay nada que perder, la carga es libre. Un borrador no bloquea.
- La conciliación de partidas (flujo existente) es un aviso distinto; al reenviar con resoluciones se reenvía también la confirmación.

### Resolución automática — a futuro, no ahora

Más adelante se planea sumarle al agente capacidad de **resolver** algunos de estos hallazgos por su cuenta (ej. elegir la fila correcta ante un WBS duplicado; ubicar la hoja con otro nombre ya se hace, ver «Qué archivos acepta»). Por ahora el agente solo **detecta y reporta** las 3 fases — no corrige nada automáticamente. Esa capacidad queda pendiente hasta que Victor la pida.

## Mano de obra directa en la vista del DP: HH reales (Victor, 2026-10-17)

Un presupuesto trae sus cargos de mano de obra en HH o en MES (conductor, topógrafo, capataz de movilización). Sumar los meses como si fueran horas falsea el total.

- **Conversión única: 1 MES = 208 HH** (8 h × 26 días, el mismo factor de la MOI de Gastos Generales). El cálculo vive en un solo lugar (`src/lib/dp/conversion-hh.ts`) y lo usan la pantalla del DP, las descargas de Excel y PDF y la pantalla «Cargos (HH)» ([flujo 16](16-paneles.md)). Una unidad que no sea HH ni MES no tiene HH calculables: se muestra «—», nunca un número inventado.
- **Tabla C1 (pantalla del DP, Excel y PDF):** Cargo · Unid. · **Cantidad** (en su unidad, tal como la trae el DP) · **HH Contractual** (las HH reales: las HH tal cual y los MES × 208) · Costo Contractual. El TOTAL de «HH Contractual» suma HH reales. El costo no cambia: sigue siendo lo que trae el DP. Debajo de la tabla, una nota dice la conversión (N MES = X HH). Es la misma lectura que la MOI (Cantidad · Meses · HH · Costo).
- **Misma cifra en la tarjeta del servicio (Victor, 2026-10-22):** la tarjeta del servicio en el panel del portafolio muestra «HH contractual» con el **mismo total que la tabla C1** (HH tal cual + MES × 208), no el de las partidas; así el DP y la tarjeta dan el mismo dato aunque el presupuesto traiga cargos en MES. Se calcula con la misma función de conversión. Sin cargos de mano de obra en HH o MES, la tarjeta cae a las HH de las partidas. El Dashboard y el PR siguen midiendo las HH por partida (base del IP).
- **Reconciliación de HH:** las partidas no cuentan los cargos en MES (solo los de unidad HH suman a las HH de la partida, `parser-apu.ts`). Por eso la reconciliación compara las HH de las partidas contra las HH de mano de obra **que el DP trae en HH**, y los cargos en MES se muestran aparte («Aparte, cargos en MES: N MES = X HH, no están en las partidas»). Antes se sumaban los meses como horas y la reconciliación marcaba una diferencia falsa (PS-0003: 9,20 MES daban 0,54 %; ahora 0,00 %).
- **Un mismo cargo en MES y en HH:** sigue siendo dos líneas distintas (costo mensual y horas de labor); no se fusionan ni se restan.
- **Pendiente de Victor:** los Equipos (C2) con unidad MES (camioneta, minivan) siguen bajo «HM Contractual» sin conversión; no está definido cuántas horas-máquina vale un mes.

## Cargos del personal sin fila en el presupuesto y equivalencias del servicio (Victor, 2026-10-21)

**Regla:** todo cargo del personal con horas debe tener tarifa en el presupuesto del servicio: una **fila de mano de obra en HH**, un cargo **MOI** o una **equivalencia declarada del servicio** (`recursos_cargo_equivalencias`, por servicio; la equivalencia puede apuntar a una fila MOI, p. ej. INGENIERO DE SEGURIDAD → INGENIERO SSOMA, y entonces cuenta como MOI). Una fila en unidad **MES** no es tarifa por hora. Sin tarifa, las horas costarían 0 sin avisar (hallazgo de la prueba del RDT en PS-0001: el personal estaba cargado como OPERARIO, OFICIAL e INGENIERO DE SEGURIDAD y el presupuesto traía OPERARIO CIVIL, OFICIAL CIVIL e INGENIERO SSOMA). Es el sentido contrario de la conciliación de recursos del presupuesto contra el catálogo de la empresa, que ya existía.

- **Al importar el DP**, tras la conciliación de cargos y equipos, aparece la sección **«Cargos del catálogo de personal sin fila en este presupuesto»**: lista los cargos del personal activo que existen en el catálogo `recursos_cargos` y no tienen fila HH, MOI ni equivalencia en este presupuesto. Por cada uno el usuario elige **a qué fila del presupuesto equivale** (la equivalencia es **del servicio**: otro servicio puede mapear OPERARIO a OPERARIO MECANICO) o marca **«No se usa en este servicio»** (no guarda nada). **Una fila del presupuesto no puede equivaler a dos cargos.** Sin resolver todos, **no se importa** y el aviso dice «El cargo X no existe en el presupuesto de este servicio» (respuesta 409 con la lista de cargos y las filas disponibles). Si el presupuesto no trae mano de obra ni MOI, no se exige nada. Marcar «No se usa» solo desbloquea la importación: la protección real es el rechazo al crear el RDT ([flujo 06](06-rdt.md)).
- **Pantalla «Equivalencias de cargos del servicio»** (página del DP, `/proyectos/[id]/dp`; guarda con `PUT /api/proyectos/[id]/dp/equivalencias-cargos`): permite declarar esas equivalencias **también con el servicio en ejecución** (cuando Importar DP ya no abre y el RDT sí se crea). **Solo administrador y jefe de proyectos** (mismo permiso que Importar DP, con alcance sobre el servicio; [flujo 14](14-accesos-y-restricciones.md)); se ofrece con el servicio en planeación o en ejecución, no cerrado, y con presupuesto importado. El servidor valida el permiso, el alcance, el estado, que la fila exista en el presupuesto y que no esté ya tomada por otro cargo. **No recalcula nada:** los RDT ya validados conservan la tarifa que se congeló al validarlos.
- **Dónde se ve el efecto:** crear o corregir un RDT con un cargo sin tarifa se rechaza ([flujo 06](06-rdt.md), 400 `CARGO_SIN_TARIFA`); el Dashboard lista los recursos sin tarifa con su nombre y enlaza a esta página ([flujo 11](11-dashboard.md)).

## Composición de mano de obra y equipo por partida (Victor, 2026-10-19; `db/112`)

Al importar el DP, además de las partidas se guarda **cuánto de cada partida es mano de obra y cuánto es equipo** (costo de MO, costo de equipo y HM de equipo, en la tabla `dp_partida_costos`, por servicio y WBS). Sirve para calcular el costo real de las **partidas transversales** ([flujo 10](10-generacion-pr.md), «Partidas transversales»): de una transversal se carga al costo real su mano de obra y su equipo × el % físico del resto del servicio.

- **Solo las HM de equipos en unidad HM** cuentan como horas de equipo (igual que en el resto del sistema).
- **Un DP importado antes de esta versión no trae esa composición:** hay que **reimportarlo** antes de marcar o aprobar partidas transversales; la app lo avisa y no deja marcar sin ella. Después de reimportar, se recalcula el PR.

| # | Informe | Fase | ¿Bloquea la importación? |
|---|---------|------|---------------------------|
| 1 | Informe de forma | 1 | Sí |
| 2 | Informe de fondo | 2 | Sí |
| 3 | Observación de importación de DP | 3 | No |

## Estado de implementación (2026-09-17)

**Fase 1 (informe de forma) implementada.** `parsearWorkbookDP` (`src/lib/dp/parser.ts`) ya no corta en el primer error: revisa hoja CD, hoja APU, hoja GG y el cruce de partidas entre CD/APU cada uno por su lado, junta TODOS los mensajes en `ErrorParseoDP.erroresDeForma` (array) y solo entonces lanza el informe único. `leerCD` (`parser-cd.ts`) junta TODOS los WBS duplicados de CD, y `leerAPU` (`parser-apu.ts`) hace lo mismo para WBS duplicado **dentro de APU** — este último es el chequeo que agarra el caso real que originó todo este pedido (6.1/7.1/8.1 repetidos en PS-065 Bancoductos), verificado corriendo `leerAPU` contra ese archivo real: detecta los 3 duplicados con su fila exacta. La API (`route.ts`) devuelve `errores: string[]` y la pantalla de importar DP (`importar-dp.tsx`) los lista todos.

**Fase 3 (observaciones) — se agregó un chequeo nuevo.** `calcularResumen` (`agregacion.ts`) compara, por cada bloque de APU, el "Costo Unitario" que la propia hoja declara contra la suma de los insumos que el parser reconoció; si no cuadra (fuera de tolerancia de redondeo) queda como observación no bloqueante, mismo mecanismo que "partida sin mano de obra". **Importante:** este chequeo, corrido contra los 51 bloques reales de PS-065, dio 0 falsos positivos pero tampoco detectó el caso de 6.1/7.1/8.1 — cada copia duplicada es internamente consistente consigo misma, así que ese caso lo agarra el chequeo de WBS duplicado en APU (arriba), no este. Quedan como dos chequeos complementarios, no uno reemplazando al otro.

**Sin implementar:** informe de fondo (fase 2) sin un caso concreto pedido todavía; generalizar observaciones más allá de estas dos (sin mano de obra, Costo Unitario) queda para cuando aparezca un caso nuevo.
