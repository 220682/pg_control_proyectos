# R6b — Congelar MOVER de paquetes con Plan Maestro aprobado (U10)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md`, Enmienda E1, regla **U10**.
**Rama/worktree:** `local-worker-4`. Sin push, sin merge a `main`. Sin migración.
**Modelo:** nivel 1 (`deepseek-v4.1-flash`), lanzado con `opencode run --model`.
**Fecha:** 2026-10-04.

## Qué se hizo

La lectura que venía de la tanda R2-R3 (hallazgo **R2-R3-R1**) era que `MOVER` —reordenar paquetes— es solo orden de presentación y, por eso, seguía permitido con Plan Maestro aprobado. **Victor lo derogó el 2026-10-04**: con Plan Maestro aprobado también se congela el reordenamiento. Queda escrito como **U10** en el plan.

- `src/app/api/paquetes-trabajo/route.ts`: se quitó la excepción que dejaba pasar `MOVER`. Ahora la comprobación del Plan Maestro aprobado se aplica a **las tres acciones** (`EDITAR`, `MOVER`, `ARCHIVAR`) y las tres se rechazan con 400 y `MENSAJE_PAQUETES_CONGELADOS`. Se actualizaron los dos comentarios del código, que decían lo contrario.
- `src/app/api/paquetes-trabajo/paquetes-api.test.ts`: el caso que afirmaba que `MOVER` seguía valiendo ahora exige 400 con el mensaje y que no se escriba.

**No se tocó:** `POST` (crear) ni `PUT` de vínculos, que ya estaban congelados desde la tanda R2.

## Validación (salida real)

- `npx tsc --noEmit` → `TSC_EXIT=0`.
- `npx vitest run` → `Test Files 104 passed (104)`, `Tests 1082 passed (1082)`.

## Commit

- `9d033e3` — `R6b: congela MOVER de paquetes con Plan Maestro aprobado (E1/U3)`. 2 archivos, +17/−12.

## Verificación del diff (Orquestador)

El diff se revisó línea por línea antes de darla por cerrada: la excepción `if (body.accion !== 'MOVER')` desapareció, la guarda quedó **antes** de la comprobación de paquete archivado y **antes** de `moverPaquete`, y el comentario nuevo nombra la regla y su fecha. No hay cambio de permisos ni de mensaje.

## Hallazgos

Ninguno de las cuatro categorías. La tanda no produjo mejoras de trabajo, ni reglas de negocio nuevas, ni observaciones sobre la política, ni huérfanos.
