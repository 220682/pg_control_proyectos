# Reservar llamadas para la importación real de DP y cronograma en briefs con datos de prueba

**Fecha:** 2026-10-02
**Origen:** Worker 1, tanda T2 (mejora M4) del plan dashboard-economia-y-curva-s
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s.md` (mejora M4)
**Categoría:** `briefs/presupuesto`

## Origen

Plan `2026-10-01-dashboard-economia-y-curva-s`, tanda T2 (creación del proyecto de prueba de extremo a extremo `PRUEBA-DASH` / PS-0009).

## Observación

Importar el DP y el cronograma **reales por UI** no es una sola acción: exige 2 pasos (analizar niveles → «Aprobar niveles») y cada POST del parser tarda 30–40 s. La sola carga consume ~10 llamadas y >90 s de parser. En briefs con datos de prueba conviene reservar explícitamente ~10 llamadas para esa carga, o separar la creación de datos de la verificación para no apretar el presupuesto de los ítems funcionales.

## Evidencia

- `tanda-T2.md` § Estados: F12 quedó parcial por falta de presupuesto; § Mejoras: «Importar el DP/cronograma reales por UI exige 2 pasos … cada POST del parser tarda 30–40 s: conviene reservar ~10 llamadas solo para esa carga».
- T2 cerró con ~71 llamadas contra un objetivo de ~60 (OP7 del libro).
- DP `PPTO-prueba-01.xlsx` (BAC US$ 4.482,54) y `Cron-prueba-01.xlsx` (14 actividades) en PS-0009.

## Clasificación

Mejora de trabajo (método / presupuesto de tandas). No es una regla de negocio.

## Etiqueta de categoría

`briefs/presupuesto`

## Destino propuesto

Queda como aprendizaje; candidato a nota en el brief base de Workers (plantilla `13-brief-de-tanda.md`) y al ajuste de presupuesto de tandas de creación de datos.

## Cambio propuesto

En el brief de una tanda con carga de DP/cronograma real: reservar ~10 llamadas para esa carga, declarar los 2 pasos (analizar niveles → «Aprobar niveles») y considerar una tanda propia de creación de datos separada de la de verificación.

## Estado

`Borrador` — pendiente de revisión del Auditor.

## Referencia a la aprobación

Pendiente (Gate 2 de Victor).
