# R6a — Guardia de U1 en la carga de RDT por archivo

## Qué se hizo
- `src/app/api/rdts/route.ts` → `POST`: se agregó la guardia U1/U9 antes de cualquier escritura (subida a Storage o `insert`), después de la comprobación de OT vigente y de `exigirAlcance`, con el mismo orden de guardas que `src/app/api/rdts/partes/route.ts`:
  1. `planMaestroAprobado(admin, proyectoId)`; si falla la lectura → 500; si no hay versión APROBADO → 400 `{ error: MENSAJE_SIN_PLAN_MAESTRO, codigo: 'SIN_PLAN_MAESTRO' }`.
  2. Estado del servicio en `proyectos.estado`; si no es `EJECUCION` → 400 `{ error: MENSAJE_RDT_SIN_EJECUCION, codigo: 'SERVICIO_NO_EN_EJECUCION' }`.
- Se reusaron `planMaestroAprobado` (`src/lib/proyectos/plan-maestro-aprobado.ts`), `MENSAJE_SIN_PLAN_MAESTRO` y `MENSAJE_RDT_SIN_EJECUCION` (`src/lib/rdts/catalogo-plan-maestro.ts`). No se reescribió lógica.
- Se agregó `src/lib/rdts/rdt-carga-archivo.test.ts` con el mismo estilo de doble de Supabase en memoria que `src/lib/rdts/partes-paquetes.test.ts`: (a) sin plan → 400 con mensaje y sin subir/insertar; (b) plan aprobado + estado fuera de `EJECUCION` → 400 `SERVICIO_NO_EN_EJECUCION` nombrando las dos condiciones, sin subir/insertar; (c) con las dos condiciones → 200, una subida y una fila en `rdts`.

## Qué no se tocó
- `src/app/api/rdts/partes/route.ts` (ya tenía la guardia).
- La acción `MOVER` de paquetes (fuera de la tanda; pregunta abierta del plan).
- Sin migración de base de datos, sin cambios de permisos, sin reglas de negocio nuevas.

## Validaciones (salida real)
1. `npx tsc --noEmit` → exit 0 (`TSC_EXIT=0`).
2. `npx vitest run` → `Test Files 104 passed (104)`, `Tests 1082 passed (1082)` (29.37s). La nueva suite aporta 3 tests.
3. `git status --short` → solo los archivos de la tanda:
   - ` M src/app/api/rdts/route.ts`
   - `?? src/lib/rdts/rdt-carga-archivo.test.ts`

## Commit
- `26288bf` — `R6a: la carga de RDT por archivo exige Plan Maestro aprobado y servicio en Ejecucion (E1/U1, U9)` (rama `local-worker-4`, sin push ni merge).

## Hallazgos

### Mejoras de trabajo
- El brief cita la suite de referencia en `src/app/api/rdts/partes/partes-paquetes.test.ts`, que no existe; vive en `src/lib/rdts/partes-paquetes.test.ts`. Destino propuesto: corregir la ruta en el brief/plan (Documentador).
- Dos helpers comprueban lo mismo con distinta forma: `planMaestroAprobado` (booleano) y `cargarPlanAprobado` (aprobado + líneas). Convendría documentar cuál usar en cada caso o unificar. Destino propuesto: backlog de refactor menor.

### Reglas de negocio
- La carga por archivo solo pasa a exigir las dos condiciones; antes podía subirse en cualquier estado. Los RDT por archivo ya existentes en servicios fuera de `EJECUCION` no se ven afectados (no se migran ni se ocultan). Destino propuesto: nota de datos/plan.
- El RDT por archivo no se vincula a líneas del Plan Maestro (es foto/PDF), así que la única relación con el plan es la guardia de creación. Destino propuesto: sin acción (informativo).

### Observaciones sobre la política
- U9 dice "cualquier vía de creación", pero `MOVER` de paquetes queda explícitamente fuera de esta tanda por pregunta abierta del plan: hoy sigue sin la guardia. Destino propuesto: sección de preguntas abiertas del plan.
- No hay ambigüedad resuelta en esta tanda: se aplicó exactamente U1/U9 (dos condiciones, orden plan → estado) sin extenderlo a otras vías ni estados.

### Huérfanos
- `GET /api/rdts` no aplica la guardia (es lectura), coherente con U1; no se encontró código muerto ni export sin uso introducido por esta tanda. Destino propuesto: sin acción.
