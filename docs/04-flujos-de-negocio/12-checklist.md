# 12 — Checklist editable
> Lee si: la tarea toca el checklist editable, su catálogo definitivo o los grupos de acción.


Ítems de catálogo y ad-hoc por proyecto. Spec `2026-08-18-checklist-editable`.

**Quién edita:** administrador y jefe de proyectos, sobre un servicio a su cargo (fila «Editar checklist del proyecto» de la tabla 2 del [flujo 14](14-accesos-y-restricciones.md)). Subir un documento del catálogo lo puede además el rol responsable de ese documento (nota 4 de esa tabla); la subida **solo aplica a los ítems del Grupo A y a los personalizados** — el servidor rechaza con 400 subir a un ítem del Grupo B (ver «Grupos de acción», más abajo, y la nota 4 del flujo 14).

## Catálogo definitivo (AL_INICIO)

Trece ítems, en este orden exacto. **Todos llevan casilla de check y todos llevan responsable**, y **completar se marca por check manual**. La columna «Grupo / acción» declara qué muestra cada fila (reglas RB1, RB2 y RB3, decisión de Victor 2026-10-02, observación O5/O7).

| # | Ítem | Completar | Responsable | Grupo / acción |
|---|---|---|---|---|
| 1 | Orden de trabajo (OT) | Check | Sí | B · Pantalla propia — Crear / Ver, botón muerto «Sin pantalla todavía» |
| 2 | Alcance | Check | Sí | A · Archivo — Seleccionar archivo |
| 3 | Presupuesto | Check | Sí | A · Archivo — Seleccionar archivo |
| 4 | Cronograma | Check | Sí | B · Pantalla propia — Crear / Ver → `/cronograma?proyectoId=` |
| 5 | Recursos del servicio | Check | Sí | B · Pantalla propia — Crear / Ver, botón muerto «Sin pantalla todavía» |
| 6 | DP (Datos del proyecto) | Check | Sí | B · Pantalla propia — Crear DP / Ver DP |
| 7 | Paquetes de trabajo | Check | Sí | B · Pantalla propia — Crear / Ver → `/paquetes-trabajo?proyectoId=` |
| 8 | Plan maestro | Check | Sí | B · Pantalla propia — Crear / Ver → `/plan-maestro?proyectoId=` |
| 9 | PR (Reporte del proyecto) | Check | Sí | B · Pantalla propia — Crear PR / Ver PR |
| 10 | 3WLA | Check | Sí | B · Pantalla propia — Crear / Ver, botón muerto «Sin pantalla todavía» |
| 11 | Requerimientos del servicio | Check | Sí | B · Pantalla propia — Crear / Ver → `/requerimientos?proyectoId=` |
| 12 | Listado de personal nuevo | Check | Sí | A · Archivo — Seleccionar archivo |
| 13 | Listado de pets | Check | Sí | A · Archivo — Seleccionar archivo |

- **Completar = marca por check (manual)** para todos los ítems, incluidos DP y PR: ya no se auto-completa por archivo subido ni por la existencia del DP.
- **Todos los ítems llevan casilla y responsable**, sin excepción por «generado por el sistema» (la fuente de datos — manual o módulo — es informativa, no cambia que hoy se completan marcando la casilla).
- **La «Acta de conformidad» no figura en la lista del checklist del proyecto:** los documentos de fase CIERRE se ocultan de la lista y del editor y **no cuentan para el checklist completo** (deroga la decisión D5 del Lote 1; observación O7). Es ocultado, no borrado: las filas existentes se conservan en la base y su bootstrap no se modifica (sin migración destructiva).

## Grupos de acción (O5)

Cada ítem del catálogo pertenece a uno de dos grupos, y la fila muestra la acción de su grupo (decisión de Victor, 2026-10-02; la fuente de verdad de la asignación son las columnas `grupo_accion`, `ruta_accion` y `etiqueta_accion` de `catalogo_documentos`):

- **Grupo A (Archivo) — 4 ítems:** 2 Alcance, 3 Presupuesto, 12 Listado de personal nuevo y 13 Listado de pets. La fila muestra «Seleccionar archivo» y el documento **se sube como hasta ahora**, más los ítems personalizados del proyecto (ad-hoc, sin catálogo). **Sin subida en el Grupo B:** el servidor rechaza con 400 la subida de archivo a un ítem de ese grupo («Este documento se completa en la pantalla de su módulo, no subiendo un archivo»).
- **Grupo B (Pantalla propia) — 9 ítems:** 1 OT, 4 Cronograma, 5 Recursos del servicio, 6 DP, 7 Paquetes de trabajo, 8 Plan maestro, 9 PR, 10 3WLA y 11 Requerimientos. La fila **no ofrece subir archivo, solo el enlace** «Crear / Ver» a la pantalla de su módulo, con `?proyectoId=` en las cuatro rutas que existen (`/cronograma`, `/paquetes-trabajo`, `/plan-maestro`, `/requerimientos`); DP y PR conservan sus etiquetas actuales (Crear/Ver DP, Cargar/Ver PR). Cada enlace se muestra solo a quien la pantalla destino no va a rechazar (permiso de esa pantalla, [flujo 14](14-accesos-y-restricciones.md)).
- **Ítems sin pantalla todavía (RB2):** OT, Recursos del servicio y 3WLA se quedan en el Grupo B pero **hoy su botón está muerto**: se ve con el título «Sin pantalla todavía» y no navega (mismo patrón que los chips inertes del [flujo 16](16-paneles.md)). Victor construirá esas tres pantallas después, en un plan aparte.
