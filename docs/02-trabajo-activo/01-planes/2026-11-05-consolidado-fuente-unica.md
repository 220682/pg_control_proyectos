# Consolidado como fuente única

Fecha: 2026-11-05. Estado: `Implementando` (código y documentos publicados; falta corregir las HH guardadas de los servicios).

Lote de trabajo tradicional por orden directa de Victor: «Arréglalo a tu criterio… Lista. Continúa. Y Termínalo». No siguió el flujo con Orquestador ni tuvo Gates.

## Objetivo, alcance y no alcance

- **Resultado esperado:** Victor solo sube presupuesto y cronograma y solo revisa el DP. Todas las pantallas dan la misma cifra porque leen del Consolidado de servicio; ninguna calcula ni convierte.
- **Alcance:** eliminar el PR (pantalla, nombre, casilla de subcontratos, permisos), reunir lectura y métricas en `src/lib/consolidado/`, convertir MES a HH en el DP, Revisión del DP, cargos del RDT desde el presupuesto, avisos automáticos, candado de pruebas, flujos y arquitectura.
- **No alcance:** renombrar las tablas internas (`pr_*`, `proyecto_pr`): exige SQL a mano y no cambia nada visible. Eliminar paquetes o transversales de servicios existentes: siguen funcionando.

## Repositorios

| Repositorio | Commit | Estado |
|---|---|---|
| `py_control_proyectos_web` | `a002c49` | en `main`, desplegado (Vercel: success) |
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
- [ ] **Corregir las HH guardadas de los 4 servicios** y el nombre del ítem del checklist. La escritura en la base la bloqueó el control de permisos de la sesión; la simulación da exacto (ver Evidencia). Ver Pendientes.
- [ ] Actualizar la Matriz de permisos (artefacto no accesible desde esta cuenta).

## Evidencia

- Pruebas: 2,675 pasan, 1 omitida; tipos y build limpios.
- Simulación de HH por partida (partidas = DP): PS-108 5,054.12; PS-140 1,616.65; PS-167 1,570.50; PS-131 9,005.54; ninguna partida faltante ni metrado distinto.
- HH reales, tres fuentes iguales: PS-108 1,010; PS-131 1,030; PS-140 0; PS-167 850.
- Revisión local con datos reales, sin contraseñas y solo lectura: Consolidado, DP, Dashboard, redirección de `/pr`, catálogo de cargos y matriz de RDT (MOD 1,010 de 5,054.12).
- No se revisó en producción con sesión iniciada.

## Pendientes

1. Correr la corrección de HH y checklist (`D:\VICTOR\RESPALDOS\consolidado-2026-11-05\aplicar-hh-dp.ts`, argumento `aplicar`, desde la carpeta de la app). Hasta entonces el Consolidado y el DP muestran «no cuadra» en PS-108, PS-131, PS-140 y PS-167, y las HH de partidas siguen sin los MES. Respaldo en la misma carpeta.
2. Victor actualiza la Matriz de permisos (chip Consolidado de servicio, sin chip PR, sin medir subcontratos).
3. PS-131: el costo de partidas y de recursos difiere US$ 567.07; queda señalado en la Revisión del DP. Lo decide Victor.

## Mejoras (de trabajo)

- Un candado automático que falla si alguien salta la frontera protege mejor que una regla escrita.
- Medir la misma cifra en todas sus fuentes antes de arreglar evitó adivinar la causa.

## Reglas de negocio acordadas en esta tarea

Integradas en los flujos 6, 9, 10, 11, 14, 20: DP → Consolidado ← RDT; ninguna interfaz calcula; 1 MES = 208 HH solo en el DP; equipos MES = 208 HM y día = 8 HM; RDT sin creación de cargos; la matriz de RDT muestra solo validados; subcontrato sin casilla manual; sin paquetes nuevos.

## Observaciones sobre la política

- Ninguna.

## Carpetas/archivos huérfanos

- `py_control_proyectos_web`: `db/095_cerrar_lectura_directa.sql`, `db/114_personal_datos_contacto.sql`, `scripts/cargar-rq-ps108-fase2.mjs`, `scripts/revision/zz-*` sin versionar y ajenos a este lote. Sin borrar.
- Tabla `pr_subcontrato_medicion`: sin filas; el recálculo aún la consulta. Sin borrar.
