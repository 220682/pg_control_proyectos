# Brief Tanda R6a — Guardia de U1 en la carga de RDT por archivo

**Plan:** `pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-3-plan.md`, Enmienda E1, reglas **U1** y **U9**.
**Rama y worktree:** `local-worker-4` en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-4` (ya estás ahí: es tu `--dir`).
**Sin push. Sin merge a `main`. Sin migración de base de datos.**

## Qué hay que hacer

La regla U1 dice que un RDT solo se crea cuando el Plan Maestro del servicio está **APROBADO** y el servicio está en **EJECUCIÓN** (las dos condiciones). U9 aclara que el congelamiento de U3 es de los datos de **planeación** y que **cualquier vía de creación de un RDT**, incluida la **carga por archivo**, exige las dos condiciones.

Hoy eso solo está en la creación del RDT estructurado. Falta en la **carga por archivo**:

- `src/app/api/rdts/route.ts` → `POST` (subir foto o PDF del RDT). Hoy no comprueba nada del Plan Maestro.

## Cómo está hecho en el resto del código (léelo y reúsalo, no lo reescribas)

- `src/app/api/rdts/partes/route.ts` → `POST`: es el patrón de referencia. Valida primero el Plan Maestro (guarda existente) y después el estado del servicio.
- `src/lib/proyectos/plan-maestro-aprobado.ts` → helper `planMaestroAprobado(admin, proyectoId)`.
- `src/lib/rdts/catalogo-plan-maestro.ts` → `MENSAJE_RDT_SIN_EJECUCION` y el código `SERVICIO_NO_EN_EJECUCION` (los agregó la tanda R3, commit `74734d7`).
- El estado del servicio se expone en `src/app/api/rdts/catalogos/route.ts` (campo `estado`).

Reusa esos tres, con el mismo tono de mensaje y el mismo orden de guardas. **Ninguna escritura antes de que las dos condiciones se cumplan.**

## Qué NO se toca

- `src/app/api/rdts/partes/route.ts` (ya tiene la guardia).
- La acción `MOVER` de paquetes: queda fuera de esta tanda (hay una pregunta abierta del plan).
- No apliques reglas de negocio que no estén aquí. Si encuentras una ambigüedad, **no la resuelvas**: escríbela en «Observaciones sobre la política».

## Pruebas

- Suite de la ruta de carga: mira cómo prueba `src/app/api/rdts/partes/partes-paquetes.test.ts` el mismo caso y replica el estilo (mismo doble de Supabase, sin red).
- Casos mínimos: (a) sin Plan Maestro aprobado → 400 con el mensaje de plan, sin escribir; (b) con Plan Maestro aprobado y servicio fuera de `EJECUCION` → 400 con `SERVICIO_NO_EN_EJECUCION` nombrando las dos condiciones, sin escribir; (c) con las dos condiciones → sigue funcionando.

## Validación obligatoria antes de commitear

1. `npx tsc --noEmit` → exit 0.
2. `npx vitest run` → suite completa en verde; reporta el conteo real de archivos y tests.
3. `git status --short` → solo los archivos de esta tanda.

Un commit, con mensaje que empiece con `R6a:` y explique la regla (U1/U9), no el archivo.

## Entrega

1. Commit en `local-worker-4`.
2. Resultado en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\02-trabajo-activo\01-planes\2026-10-02-observaciones-victor-lote-3-briefs\resultados\R6a.md`, con: qué se hizo, qué no se tocó, las validaciones con su salida real, el commit, y los **hallazgos en las cuatro categorías** (mejoras de trabajo · reglas de negocio · observaciones sobre la política · huérfanos), uno por línea y con destino propuesto. No muevas hallazgos a sus destinos: los traslada el Documentador.
