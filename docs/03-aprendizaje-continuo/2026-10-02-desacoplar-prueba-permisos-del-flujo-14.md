# Desacoplar la prueba de permisos del flujo 14 cuando el doc y el código avanzan en ventanas distintas

**Fecha:** 2026-10-02
**Origen:** Worker 1, tanda A (hallazgo A-H1) del plan dashboard-economia-y-curva-s
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s.md` (mejora M1)
**Categoría:** `tests/doc`

## Origen

Plan `2026-10-01-dashboard-economia-y-curva-s`, tanda A (código) y Fase E (documentación), en ventanas distintas.

## Observación

`permisos.test.ts` compara la tabla 1 del flujo 14 **leyendo el markdown por ruta absoluta**, fila por fila y rol por rol. Como la Fase A mueve los permisos antes que el documento (la Fase E edita los flujos después), la comparación fila-por-fila de las filas «Dashboard» y «Curva S» quedaba roja entre A y E. Para no dejar el carril con `npm test` en rojo (las 00-reglas exigen tests verdes), en A se retiraron esas dos filas del mapa y se añadieron pruebas explícitas de los dos modos; la Fase E reescribe el flujo y un Worker de código posterior restaura las filas en el mapa.

## Evidencia

- `permisos.test.ts` (mapa `FUNCIONES`, 7→5 filas; `expect(comparadas).toBe(5 * 13)`), commit `d40cd74` en `local-worker-5`.
- Riesgo R2 del plan y ítem P03 de la Punch List.
- Fase E edita la tabla 1 del flujo 14 (filas Parcial/Completo y física/económica).

## Clasificación

Mejora de trabajo (método de prueba). No es una regla de negocio.

## Etiqueta de categoría

`tests/doc`

## Destino propuesto

Queda como aprendizaje. Candidato a nota en `docs/01-contexto-repositorio/04-pruebas-y-evidencia.md` y/o en el brief base de Workers: cuando una prueba lee un documento por ruta absoluta, la ventana doc/código debe acordarse en el brief (quién espera a quién), o la prueba debe separar la lista de filas comparadas del archivo.

## Cambio propuesto

En el brief de Workers, declarar la dependencia «prueba que lee doc ↔ edición del doc» y la secuencia (código en A, doc en E, restauración posterior), para que el carril no quede rojo entre ventanas.

## Estado

`Borrador` — pendiente de revisión del Auditor.

## Referencia a la aprobación

Pendiente (Gate 2 de Victor).
