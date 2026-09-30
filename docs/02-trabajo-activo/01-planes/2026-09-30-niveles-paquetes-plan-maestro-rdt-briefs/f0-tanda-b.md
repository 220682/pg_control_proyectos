# F0-B · Maquetas del lienzo del Plan Maestro, paneles ocultables y selector del RDT

Lee primero `00-reglas-de-contexto.md`. **Carril de diseño** (docs), el mismo Worker o uno nuevo después de F0-A. Escribes solo en `docs/05-diseno-y-referencias/**`.
Fase F0 · **Depende de:** F0-A cerrada (mismo estilo y `design.md`) · **Bloquea:** F3-C, F3-D y F4-C (interfaz). Datos y lógica **no** esperan.
**Commit:** en `main` de `pg_control_proyectos`, `git add` explícito.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F0B-1 | Maqueta HTML del **lienzo**: a la izquierda de una línea divisoria, columnas **fijas** (WBS, descripción, Und., metrado, costo unitario, **HH por unidad**); a la derecha, una **columna por día** con scroll horizontal, agrupadas por semana (sábado a viernes); encabezado con el **total del servicio**. Columnas de Tiempo (duración, inicio, fin) **no** van | `mockups/plan-maestro-lienzo.html` |
| F0B-2 | Por semana, **seis columnas**: avance físico, avance económico y HH programadas, cada uno **semanal y acumulado**, con rótulos que no se confundan (nombre, unidad), e **interruptor** para ocultar las acumuladas; semanas **plegables y expandibles** (plegada = una columna con sus totales) | Mismo archivo |
| F0B-3 | Filas: **paquetes plegables con subtotal**, partidas repetidas por paquete con su porción, partidas directas sin paquete, jerarquía por niveles; indicador por fila de **cuánto falta repartir**, indicador global y botón «Crear Plan Maestro» deshabilitado hasta el 100 % | Mismo archivo |
| F0B-4 | **Subfilas «Prog.» (editable) y «Real» (solo lectura)** con interruptor para ocultar lo real; real por paquete × partida; marca de «real fuera del rango programado» con semanas extendidas; estados `BORRADOR` y `APROBADO` (solo lectura) | Mismo archivo |
| F0B-5 | Maqueta del control de **ocultar y mostrar los paneles laterales** (escritorio), con el icono flotante del asistente sin tapar columnas, y la vista móvil (los paneles ya son un cajón) | `mockups/paneles-ocultables.html` o sección del lienzo |
| F0B-6 | Maqueta del **selector de actividad del RDT**: paquetes plegables con sus partidas, partidas directas aparte, **modo «por avance del paquete»** (se escribe la unidad de la guía; las demás partidas aparecen calculadas, en solo lectura), horas C/NC y materiales con el mismo selector, mensaje «sin Plan Maestro aprobado» | `mockups/crear-rdt-selector-paquetes.html` |
| F0B-7 | **Los números de la maqueta del lienzo coinciden con el anexo de 4 semanas** del Spec (totales 22,56 / 48,78 / 76,22 / 100 %, $ 8 200, 172 HH). Estados vacío, carga, error, móvil y accesibilidad. `design.md` (§3, §5, §8) actualizado, `mockups/index.html` y `README.md` enlazados, y `resultados/F0-B.md` con **preguntas de diseño para Victor** (máx. 6) | Comparación número a número + diff |

## Qué mirar (solo lo necesario)

- El **anexo de 4 semanas** del Spec `…/2026-09-30-paquetes-y-plan-maestro-grilla.md` (Grep «Anexo»): úsalo entero como datos.
- Flujo 18 §«Estructura longitudinal del Plan Maestro» y su regla 5 («no mezclar avance semanal con acumulado»: aquí van en columnas **separadas y rotuladas**). El flujo 18 lista además Área, Disciplina, Frente, BAC, HH contractuales y método de medición como columnas fijas: **no las incluyas en la maqueta** salvo las que el Spec nombra; anótalo como pregunta para Victor.
- `design.md` §3 «Asistente flotante» y §8 (scroll, columnas fijas `sticky`). La imagen de referencia de Victor: línea naranja, fijo a la izquierda, días a la derecha.
- Las maquetas de F0-A (estilo).

## Qué NO hacer

- No tocar código ni flujos. No agregar columnas que los Specs no nombran. No inventar componentes reales.
- No usar datos reales. No publicar credenciales.

## Cierre

`resultados/F0-B.md` (estado de F0B-1 a F0B-7, handoff, preguntas de diseño). Commit en `main`. Mensaje final: cerrados, pendientes, llamadas.
