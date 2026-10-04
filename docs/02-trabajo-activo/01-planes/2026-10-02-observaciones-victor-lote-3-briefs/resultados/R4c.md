# R4c — Determinismo del reposicionamiento y `sinLinea` (corrección del Auditor)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md`, Ola 0 del «Plan de las tandas que faltan». **Nivel 3** (`n3` = `opencode-go/qwen3.7-plus`), por decisión de Victor del 2026-10-04.
**Rama/worktree:** `local-worker-4`. **Sin push, sin merge a `main`.**
**Fecha:** 2026-10-04.

## El hallazgo que corrige

El Auditor encontró que el `update` de `rdt_actividades` en la `093` emparejaba la actividad con **cada** fila del payload que mencionara su id, y Postgres se quedaba con **una sola, sin forma de elegir cuál**:

```sql
update rdt_actividades a
   set paquete_trabajo_id = nullif(c->>'paqueteNuevo','')::uuid
  from jsonb_array_elements(v_payload) c
 where a.id = (c->>'actividadId')::uuid;
```

El payload se arma **uno por vínculo** y una actividad declarada puede tener varios. Si el plan nuevo mandaba dos partidas de la misma actividad a paquetes distintos, `rdt_actividades.paquete_trabajo_id` quedaba con un paquete arbitrario: **el RDT se mostraba bajo el paquete equivocado y su real quedaba descolocado en el Plan Maestro** — justo lo que la aclaración de Victor del 2026-10-04 vino a evitar.

## Qué se hizo

**Migración `db/094_aprobar_plan_maestro_reposicion_determinista.sql`** (`create or replace`, misma firma de 3 argumentos):

| Update | Regla |
|---|---|
| `rdt_actividad_partidas` | Agrupa por el par `(actividad, partida)`, que es la PK, y **solo escribe si el payload no se contradice sobre ese par** (`having count(distinct …) = 1`) |
| `rdt_actividades` | **Solo escribe si TODAS las entradas de esa actividad coinciden** en `paqueteNuevo`. Con desacuerdo no se cambia nada y la actividad sale en `actividadesAmbiguas` con los paquetes en conflicto |

El bloqueo `for update`, las validaciones, el historial (U7) y `recalcular_pr_planificado` (U8) quedan igual. La función acepta el payload en los dos contratos: array (093) u objeto `{cambios, sinLinea}` (094).

**`sinLinea`** (los vínculos cuya partida ya no tiene línea en el plan nuevo) se calculaba y se descartaba en silencio: ahora viaja en el payload y la función lo devuelve en su `jsonb`, sin cambiar la escritura de esos casos. La ruta lo expone en la respuesta.

**Capa TS** (`reposicionamiento.ts`, `reposicionamiento-servidor.ts`): la función pura retira del payload las actividades ambiguas y reporta el caso; el guard de la SQL queda como defensa en profundidad para cualquier otro llamador.

**Aviso de dependencia** (lo que faltaba y el Auditor señaló): `db/093` y su fila en `db/README.md`averse advierte ahora que **la acción de aprobación falla por completo si la `093` no está aplicada** en ese entorno, y que sin ella no hay fallback.

## Validación (salida real)

- `npx tsc --noEmit` → `TSC_EXIT=0`.
- `npx vitest run` → `Test Files 107 passed (107)` · `Tests 1115 passed (1115)`.
- Pruebas nuevas: la ambigua no se mueve y se reporta; dos vínculos al mismo paquete **sí** se mueven; la prueba que lee el `.sql` de la 094 verifica que no tiene el join ambiguo, sin depender de la base; la ruta sigue devolviendo 200; `sinLinea` vuelve en el 200.
- Durante el trabajo se detectaron y corrigieron dos pruebas que fallaban al principio (`sinLinea` en el `jsonb` y la aserción del caso ambiguo).

## Commit

- `ae476f1` — `R4c: el reposicionamiento es determinista (094), devuelve sinLinea y actividades ambiguas, y avisa de la dependencia de 093`. 9 archivos, +703/−53.

## Lo que NO se hizo, y por qué

**La migración `094` NO se aplicó.** El archivo de credenciales autorizado quedó inalcanzable durante la tanda: `Get-ChildItem` lo lista en `D:\1 Nueva carpeta\todo\DIARIO` con 677 bytes, pero ninguna API lo abre (`FileNotFoundError` en Python, `FileNotFoundException` en .NET, `Test-Path` en `False`), y reintentar seis veces no lo cambia. La misma credencial funcionó a las 08:41 de hoy para aplicar la `093`. Conforme al protocolo —«si no veo las credenciales, me detengo y aviso; no busco otras»—, **no se buscó ninguna otra vía**.

Consecuencia: la base tiene la `093` (no determinista) y el repositorio tiene la `094`. **La acción de aprobación queda con la versión no determinista hasta que se aplique la `094`.**

## Hallazgos

### Mejoras de trabajo
- **R4c-M1** — Una tanda que aplica una migración no puede ejecutarse en un Worker por `opencode run` (permiso de directorio externo) y además depende de un archivo de credenciales que puede quedar inalcanzable sin aviso. **El brief de una tanda con migración debería abrir con «verifica que la credencial se lee, antes de escribir una línea de código»**. Destino: `03-aprendizaje-continuo/`.
- **R4c-M2** — El Worker de nivel 3 se cortó dos veces seguidas en la misma tanda (la primera antes de escribir, la segunda tras validar y antes de commitear). Un corte así no deja ni commit ni resultado: **el brief debería exigir el commit y el archivo de resultado antes que cualquier refinamiento opcional**. Destino: `03-aprendizaje-continuo/`.

### Reglas de negocio
- **R4c-R1** — Una actividad con varios vínculos que el plan nuevo reparte en paquetes distintos **no se reposiciona** y se reporta en `actividadesAmbiguas`. Es una regla nueva que el código ya aplica y que **no está escrita en ningún flujo**: hay que decidir si se documenta como tal o si se cambia el comportamiento. Destino: `06-rdt.md` / `20-plan-maestro.md`. **Pendiente de decisión (Victor).**

### Observaciones sobre la política
- **R4c-O1** — Un archivo puede estar listado por el sistema de archivos y a la vez ser inaccesible a toda API. El protocolo de migraciones asume que la credencial está o no está; falta el caso intermedio. Destino: protocolo de migraciones. Registrada.

### Carpetas/archivos huérfanos
Ninguno.