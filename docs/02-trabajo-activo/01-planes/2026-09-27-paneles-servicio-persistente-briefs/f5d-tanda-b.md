# F5D-B · Gestión de Recursos: Cargos y Equipos (crear, editar, desactivar) y editar texto de Causa CNC

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5D · **Depende de:** F5D-A cerrada (`puedeGestionarRecursos` existe).
**Punto de commit:** Al cerrar la fase F5D (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-163 | Crear Cargo (construir): formulario nuevo en `TablaRecursos.tsx` (tipo cargos), `POST /api/recursos`; mismo patrón de permiso | Capturas + respuesta API |
| PL-164 | Editar Cargo existente (construir): control por fila, `PATCH` nuevo; mismo patrón de permiso | Capturas + respuesta API |
| PL-165 | Eliminar o desactivar Cargo (construir): `activo = false`; mismo patrón de permiso; un cargo desactivado deja de ofrecerse al crear Personal (la API de Personal ya exige `activo = true`) | Capturas + verificación en crear Personal |
| PL-166 | Crear Equipo (construir): formulario nuevo en `TablaRecursos.tsx` (tipo equipos), `POST /api/recursos`; mismo patrón de permiso | Capturas + respuesta API |
| PL-167 | Editar Equipo existente (construir): control por fila, `PATCH` nuevo; mismo patrón de permiso | Capturas + respuesta API |
| PL-168 | Eliminar o desactivar Equipo (construir): `activo = false`; mismo patrón de permiso | Capturas + respuesta API |
| PL-169 | Editar el texto de una Causa CNC (construir): control de editar en `TablaCatalogoCnc.tsx` (la API `PATCH …/catalogo-cnc/[id]` ya acepta `descripcion`); mismo patrón de permiso; el texto editado se refleja en el desplegable de Crear RDT | Capturas + verificación en Crear RDT |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- `TablaRecursos.tsx` (`src/components/ui/`, cliente) es **solo lectura** hoy y sirve a `recursos/cargos/page.tsx` y `recursos/equipos/page.tsx` (filtros, orden y «Personalizar campos» de `src/lib/recursos/{filtros,tipos,mapeo}.ts`, que deben conservarse: PL-170). Añade formulario de alta y acciones por fila (editar, desactivar), visibles solo con `puedeGestionarRecursos`.
- `src/app/api/recursos/route.ts` hoy solo `GET` con `?tipo=cargos|equipos` (`TABLA_POR_TIPO`: `recursos_cargos`, `recursos_equipos`; columnas `descripcion` única, `unidad`, `categoria`, `activo`, `origen`): suma `POST`; crea `src/app/api/recursos/[id]/route.ts` con `PATCH` (`tipo` en cuerpo o ruta, a decisión del Worker; documéntalo). «Eliminar» = `activo = false`, nunca borrado. Escritura con `crearClienteAdmin()` tras la guardia (las tablas solo tienen `select` por RLS; sin migraciones).
- **Riesgo a revisar antes de editar la descripción de un Cargo:** `recursos_personal.cargo` guarda el texto del cargo y existen `recursos_cargo_equivalencias`/`recursos_equipo_equivalencias` (`db/046`), tarifas de RDT y datos históricos. Con `Grep` en `src/` y `db/` confirma qué referencia la descripción por texto; si renombrar puede romper referencias, limita la edición a `unidad`/`categoria` (o bloquea el cambio) y **devuelve la duda al Orquestador**. Un cargo desactivado deja de ofrecerse al crear Personal (`personal/route.ts` ~22 filtra `activo = true`; por verificar).
- Causas CNC: `TablaCatalogoCnc.tsx` suma el control de editar el texto; `PATCH …/catalogo-cnc/[id]` ya acepta `descripcion` (~20-24, rechaza vacío); el texto editado se refleja en el desplegable de Crear RDT.
- Mismo patrón de permiso que F5D-A (administrador y JP; otro rol sin control y API 403). **Datos reales:** misma regla que F5D-A: sin escribir hasta que el Orquestador confirme la autorización de Victor; camino feliz `Observado` con esa causa.

## Qué NO hacer

- No renombres cargos con referencias vivas. No cambies Materiales. No borres filas.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
