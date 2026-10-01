# El clasificador de permisos bloquea scripts de migración aunque estén autorizados

**Fecha:** 2026-10-01
**Origen:** Workers F1-B, F2-A, F2-D, F3-E y F4-A del plan niveles-paquetes-plan-maestro-rdt
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`
**Categoría:** `migraciones-sql` y `permisos`

## Hallazgo

El protocolo de migraciones (`00-protocolo-migraciones.md`) y Victor autorizan a los Workers a aplicar sus migraciones, pero el clasificador del sistema denegó en varias tandas los scripts `migrar_*.py` (y, una vez, el `check` de una migración y un `grep` sobre `db/`), aunque la regla estuviera dada en `/permissions`. Insistir no sirvió.

## Qué hacer

1. Antes de lanzar Workers con migraciones, que Victor compruebe que la regla de permiso reconoce el script (o definir otra vía de aplicación, como correr el comando con `!`).
2. Si el Worker es denegado, **no insistir ni rodear la regla**: dejar el script listo (fuera del repositorio, sin credenciales), anotar el comando exacto en el handoff y marcar la migración como pendiente de aplicar.
3. Para búsquedas en `db/` o código con rutas con corchetes, usar la herramienta de búsqueda (Grep) en lugar de `grep` en Bash: no fue denegada.

## Destino propuesto

Candidato a `docs/00-estandar-agentes/` (protocolo de migraciones); queda como aprendizaje hasta que Victor decida cómo aplicar las migraciones pendientes.
