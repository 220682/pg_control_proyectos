# F1-B · Niveles: datos, importación del DP y del cronograma, bloqueo de recarga

Lee primero `00-reglas-de-contexto.md`. Carril **1 · Niveles** · rama `local-worker-1`, puerto 3111.
Fase F1 · **Depende de:** F1-A cerrada. No depende de la maqueta (sin pantalla). Contratos: `00-contratos-tecnicos.md` § C1.
**Migraciones reservadas: `db/073`–`075`** (se escriben, **no se aplican**).
**Punto de commit:** al cerrar la tanda, en `local-worker-1`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F1B-1 | Migraciones 073–075: tablas de **niveles por servicio y origen** (DP o cronograma) y de **encabezados con código, nombre, nivel y rol**; `reemplazar_dp` los reconstruye (`create or replace` con la **firma de 13 parámetros** de `db/071`); lo ya importado queda con un mapa por defecto «pendiente de confirmar» equivalente a la convención actual. Idempotentes, sin borrar `dp_subpresupuestos` ni `dp_paquetes` | Archivos SQL + lectura crítica (sin aplicar) |
| F1B-2 | El parser del DP lee **encabezados de cualquier nivel** (no solo los patrones de 1 y 2 segmentos) y entrega filas para F1-A; las pruebas actuales de `parser*.test.ts` siguen verdes y los servicios de 3 niveles típicos producen lo mismo que hoy | `npm test` |
| F1B-3 | API de importar DP: devuelve **niveles detectados y propuesta**; guarda el mapa confirmado; si el usuario no confirma, guarda el mapa por defecto marcado pendiente | Prueba de API con datos simulados |
| F1B-4 | Cronograma: el parser y el informe guardan **niveles y roles propios**; el enlace con el DP por EDT sigue funcionando; `PATCH /api/cronograma` **acepta vínculos tarea ↔ partida sin metrado** y deja de exigir metrado > 0 y el 100 % por partida (esa regla pasa a Paquetes y al Plan Maestro) | Prueba + `npm test` |
| F1B-5 | `src/lib/proyectos/bloqueo-recarga.ts` (`evaluarRecarga`, contrato C1) y su uso en la importación del DP y en la subida del cronograma: con Plan Maestro `APROBADO` → **409 sin opción de confirmar**; sin él → exige `confirmarPerdida: true` tras el aviso con la lista (vínculos, paquetes, borrador del Plan Maestro). **El borrador no bloquea** | Pruebas de los tres casos |
| F1B-6 | Guardias intactas: rol sin permiso → 403; servicio inexistente → 400/404; `npx tsc --noEmit`, suite y lint comparado con `main` | Salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Importación del DP: `src/app/api/proyectos/[id]/dp/route.ts`; `src/lib/dp/parser.ts` (`parsearWorkbookDP` devuelve `{ partidas, recursos, resumen, moi, subpresupuestos, paquetes }`, ~116), `src/lib/dp/guardar.ts` (~36-37 pasa `p_subpresupuestos` y `p_paquetes` al RPC `reemplazar_dp`). Quien importa: administrador y jefe de proyectos sobre un servicio a su cargo (flujo 09).
- Cronograma: `src/app/api/cronograma/route.ts` — `PATCH` (`manejarPatch`, ~129-229) valida hoy `metrado > 0` y usa `sumarMetradoPorPartida` / `partidasConMetradoIncompleto` de `src/lib/cronograma/vinculos.ts`; `POST` (`manejarPost`, ~238) sube el archivo y crea el **enlace automático 1:1 por EDT con el metrado contractual** (~378): **se conserva**. `recalcular_pr_fechas_base` (RPC, `db/062`) se llama tras escribir vínculos: **se conserva** (el PR toma sus fechas base de ese vínculo, sin mirar el metrado).
- Tipos de actividad hoy: `HITO` si duración 0; `RESUMEN` si otro EDT empieza con `"<edt>."` (`parser-excel.ts` ~104-127).
- `recalcular_pr_fechas_base`, `recalcular_pr_planificado` y el motor del PR no se modifican.
- Quién sube el cronograma: administrador, jefe de proyectos y planner (flujo 15/14). Sin cambio.
- Bloqueo (Victor, 2026-09-30): con Plan Maestro aprobado no se carga nada; el borrador no restringe; sin aprobado, bloqueo + aviso + confirmación.

## Qué NO hacer

- No apliques migraciones. No edites el plan ni `db/README.md`. No toques `src/lib/plan-maestro/**`, `paquetes-trabajo/**`, `rdts/**` (otros carriles).
- No borres tablas ni columnas; cualquier cambio de datos existentes va al handoff como «requiere autorización expresa».
- No cambies permisos. No migres los consumidores de pantallas (F1-C). Sin push.
- Ante contradicción con un flujo escrito, acción destructiva o duda de negocio: detente y devuelve la pregunta.

## Cierre

`resultados/F1-B.md` (estado de F1B-1 a F1B-6, handoff con las migraciones escritas y su orden, llamadas). Commit en `local-worker-1`, `git add` explícito.
