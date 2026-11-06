# Consolidado como fuente única

Fecha: 2026-11-05. Estado: `Implementando` (código, documentos y datos de los 4 servicios corregidos; falta la revisión de Victor y las decisiones de Pendientes).

Lote de trabajo tradicional por orden directa de Victor: «Arréglalo a tu criterio… Lista. Continúa. Y Termínalo». No siguió el flujo con Orquestador ni tuvo Gates.

## Objetivo, alcance y no alcance

- **Resultado esperado:** Victor solo sube presupuesto y cronograma y solo revisa el DP. Todas las pantallas dan la misma cifra porque leen del Consolidado de servicio; ninguna calcula ni convierte.
- **Alcance:** eliminar el PR (pantalla, nombre, casilla de subcontratos, permisos), reunir lectura y métricas en `src/lib/consolidado/`, convertir MES a HH en el DP, Revisión del DP, cargos del RDT desde el presupuesto, avisos automáticos, candado de pruebas, flujos y arquitectura.
- **No alcance:** renombrar las tablas internas (`pr_*`, `proyecto_pr`): exige SQL a mano y no cambia nada visible. Eliminar paquetes o transversales de servicios existentes: siguen funcionando.

## Repositorios

| Repositorio | Commit | Estado |
|---|---|---|
| `py_control_proyectos_web` | `a002c49` y `16d46e7` | en `main`, desplegados |
| `pg_control_proyectos` | este commit | en `main` |

## Avance

- [x] `lib/consolidado`: `leerConsolidado`, recursos agrupados, cuadre.
- [x] Dashboard, portafolio, informes, curva, descargas y Valorización leen del Consolidado.
- [x] PR eliminado; `/proyectos/:id/pr` redirige al Consolidado.
- [x] Lector del presupuesto suma los cargos en MES a las HH de la partida.
- [x] Revisión del DP y aviso `dp.sin_cuadrar` al importar.
- [x] Crear RDT con cargos del presupuesto (19 directos y 6 indirectos en PS-108, verificado).
- [x] Matriz «Consolidado RDTs» solo con RDT validados.
- [x] Candado `frontera.test.ts`.
- [x] Flujos 6, 9, 10, 11, 12, 14, 16, 20, arquitectura, AGENTS y README.
- [x] Segunda orden de Victor: recursos = presupuesto con líneas de ajuste, cargo en los dos lados es directo, equipos en HM con tarifa convertida, verificación automática con detalle por día, gastos generales y utilidad por defecto en Valorización.
- [x] Datos guardados de los 4 servicios y nombre del ítem del checklist: corregidos. Victor corrió `aplicar-cuadre.ts` el 2026-11-05, porque el control de permisos de la sesión bloqueó esa escritura.
- [ ] Actualizar la Matriz de permisos (artefacto no accesible desde esta cuenta).

## Evidencia

- Pruebas: 2,696 pasan, 1 omitida; tipos y build limpios.
- Causa de PS-131 (leída del Excel): presupuesto 263,778.08 y APU 264,345.14, diferencia 567.07. En la partida 02.02 el precio es 10.20 y su APU 9.2243 (+487.87); en la 03.01.01 el precio es 2.72 y su APU 10.2036 (−1,058.55); la 4.02 da +0.31 y el redondeo del resto +3.31.
- Después de corregir los datos, en local con datos reales y solo lectura: las 9 comprobaciones están correctas en PS-108, PS-131, PS-140 y PS-167, y Valorización da 416,760.93; 320,003.41; 73,597.84 y 50,921.27 sin IGV.
- Simulación con el lector nuevo: recursos = presupuesto en los 4 servicios (322,877.39; 61,331.54; 39,930.56; 263,778.08) y costo directo + gastos generales + utilidad = monto del presupuesto (416,760.93; 73,597.84; 50,921.27; 320,003.41).
- Verificación vista en local con datos reales de PS-108 y PS-131: las 5 comparaciones por día cuadran; las de presupuesto fallan hasta correr la corrección, como se esperaba.
- Simulación de HH por partida (partidas = DP): PS-108 5,054.12; PS-140 1,616.65; PS-167 1,570.50; PS-131 9,005.54; ninguna partida faltante ni metrado distinto.
- HH reales, tres fuentes iguales: PS-108 1,010; PS-131 1,030; PS-140 0; PS-167 850.
- Revisión local con datos reales, sin contraseñas y solo lectura: Consolidado, DP, Dashboard, redirección de `/pr`, catálogo de cargos y matriz de RDT (MOD 1,010 de 5,054.12).
- No se revisó en producción con sesión iniciada.

## Pendientes

2. Victor actualiza la Matriz de permisos (chip Consolidado de servicio, sin chip PR, sin medir subcontratos).
3. PS-131: revisar si los precios de 02.02 y 03.01.01 del Excel son correctos; el APU de 03.01.01 da 10.20, que es el precio escrito en 02.02. No cambia el cuadre.
4. PS-108: 6 h de RETROEXCAVADORA en RDT validados no tienen fila en el presupuesto y siguen sin tarifa.
5. PS-131: el WBS `4.02` del Excel debería ser `04.02`; por eso Valorización abre un «Título 4» aparte.

## Mejoras (de trabajo)

- Un candado automático que falla si alguien salta la frontera protege mejor que una regla escrita.
- Medir la misma cifra en todas sus fuentes antes de arreglar evitó adivinar la causa.
- Antes de declarar un dato en un reporte, leerlo de la fuente: el reporte anterior dio 1,248 h del conductor en cada lado, y en gastos generales eran 208 h.

## Reglas de negocio acordadas en esta tarea

Integradas en los flujos 6, 9, 10, 11, 14, 18, 20, 28: líneas de ajuste de cuadre; tarifa ponderada; cargo en los dos lados es directo; tarifa de equipos convertida a HM; verificación automática; gastos generales y utilidad por defecto en Valorización; DP → Consolidado ← RDT; ninguna interfaz calcula; 1 MES = 208 HH solo en el DP; equipos MES = 208 HM y día = 8 HM; RDT sin creación de cargos; la matriz de RDT muestra solo validados; subcontrato sin casilla manual; sin paquetes nuevos.

## Observaciones sobre la política

- Ninguna.

## Carpetas/archivos huérfanos

- `py_control_proyectos_web`: `db/095_cerrar_lectura_directa.sql`, `db/114_personal_datos_contacto.sql`, `scripts/cargar-rq-ps108-fase2.mjs`, `scripts/revision/zz-*` sin versionar y ajenos a este lote. Sin borrar.
- Tabla `pr_subcontrato_medicion`: sin filas; el recálculo aún la consulta. Sin borrar.
