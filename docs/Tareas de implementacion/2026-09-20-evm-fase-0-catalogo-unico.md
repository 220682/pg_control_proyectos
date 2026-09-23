# EVM Fase 0 — Catálogo único de cargos/equipos (2026-09-20/21)

**Corrección (2026-09-21):** esta versión reemplaza una anterior con datos incorrectos (tabla `cargo_equipo_tarifa` inventada, sin verificar contra el código real). Contenido corregido contra el commit real `0dcdbd1`.

## Contexto

Prerrequisito para los indicadores EVM del Plan Maestro (AC/CV/CPI/SPI): antes de valorizar HH/HM reales hace falta que exista **una sola base de datos de cargos y equipos**, no un catálogo desincronizado del presupuesto de cada servicio.

El catálogo maestro ya existía (`recursos_cargos` / `recursos_equipos`, `db/025_recursos_rdt.sql`) — es de EMPRESA, no por proyecto, y **no tiene columna de tarifa** (solo `descripcion`, `unidad`, `categoria`). Lo que faltaba era el mecanismo de conciliación: qué pasa cuando un presupuesto importado trae un cargo/equipo con un nombre que no coincide exactamente con el catálogo.

## Implementación (commit `0dcdbd1`)

### Migración `db/046_recursos_equivalencias.sql`
✅ **Aplicada en Supabase**

- Dos tablas nuevas (cargos y equipos por separado, no polimórfica): `recursos_cargo_equivalencias` y `recursos_equipo_equivalencias`
- Cada una: `proyecto_id`, `descripcion_presupuesto`, `cargo_id`/`equipo_id` (FK al catálogo maestro), `creado_por_id`, `creado_en`
- `unique (proyecto_id, descripcion_presupuesto)` — la equivalencia es válida solo dentro de ese proyecto (ej. "AYUDANTE" del presupuesto = "AYUDANTE TOPOGRAFO" del catálogo, pero solo para ese servicio)
- RLS: lectura abierta a autenticados; escritura solo desde código con service role (mismo criterio que `025_recursos_rdt.sql`)

### Lógica de detección — `src/lib/dp/equivalencias.ts`
- Detecta cargos/equipos del presupuesto que no calzan contra el catálogo
- Normaliza mayúsculas, punto final, espacios y guiones (Excel autocorrige "-" a en-dash) para evitar falsos positivos
- Excluye herramientas con unidad `%MO` (no son equipo asignable, son un porcentaje sobre mano de obra)

### Resolución — `src/lib/dp/aplicar-equivalencias.ts` + `ResolverRecursosImportacion.tsx`
- Al importar un DP, si hay recursos sin conciliar, la API responde `409` con `pendienteConciliacion`
- Modal `ResolverRecursosImportacion`: por cada cargo/equipo no resuelto, el admin/jefe de proyectos elige:
  - **Crear nuevo** en el catálogo maestro, o
  - **Es equivalente** (solo en este proyecto) a uno que ya existe con otro nombre
- Nunca queda un recurso sin resolver ni duplicado silenciosamente

### Hallazgos aparte (mismo commit, probando con "Ver como")
- Mi entorno ocultaba completo los chips de acción sin permiso (Crear/Subir RDTs no existían en Logística/SSOMA) — ahora aparecen deshabilitados con tooltip, mismo criterio en los 8 grupos.
- Chip de Plan Maestro no existía en Mi entorno; en el panel derecho no era clicable sin proyecto elegido pese a tener su propio selector.

## Verificación

✅ Compilación: tsc/eslint limpios, 437 tests, build limpio.

## Resultados

**CERRADO 100%** (según checklist "EVM Plan Maestro — Fase 0" en Punch List, 11/11 Conforme).

Catálogo único listo para Fase 1 (congelar tarifa al validar RDT).

## Mejoras a flujos

(vacío)

---

## Mejoras (de trabajo)

Ninguna identificada en esta tarea.

## Reglas de negocio acordadas en esta tarea

Ninguna nueva — esta tarea cargó datos de catálogo (cargos/equipos), no introdujo una regla de negocio nueva.
