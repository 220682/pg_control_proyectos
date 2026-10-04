# Evidencia — Observaciones de Victor, Lote 3 (Enmienda E1)

> Evidencia real de las nueve tandas del 2026-10-04. Lo que no aparece aquí es porque no se verificó.

## 1. Benchmark de modelos (previa a la asignación)

Tarea con resultado conocido: el diseño del reposicionamiento de los RDT, con el formato exacto que se le pidió y sin posibilidad de escribir archivos. Se lanzaron con `opencode run --agent build --model <modelo> --dir <worktree>`.

| Nivel | Modelo | USD | Tokens | Min | Resultado |
|---|---|---|---|---|---|
| 1 | `opencode-go/deepseek-v4.1-flash` | **0,0369** | 1 467 458 | 2,8 | 8/8 |
| 2 | `opencode-go/deepseek-v4-pro` (variante `high`) | 0,0858 | 809 909 | 2,2 | 7/8 |
| 3 | `opencode-go/qwen3.7-plus` | 0,0477 | 325 972 | 2,3 | 7/8 |

Los tres coincidieron: los tres coincidieron en el punto que decide el diseño —la aprobación actual son llamadas HTTP sueltas y no es una transacción, por eso hace falta una función SQL— y en el resto de los puntos (archivo, orden, tabla de historial, alcance de validados). El de nivel 1 además nombró el CHECK del historial, la forma del `snapshot` en `jsonb` y el riesgo de tocar `metrado_ejecutado`.

Medición de esos costos: tabla `session` de `%USERPROFILE%\.local\share\opencode\opencode.db`, filtrando `title like 'bench-%'`.

## 2. Tandas de código

| Tanda | Commit | `tsc` | Tests |
|---|---|---|---|
| R1 | `ceb269e` | — | — |
| R2 | `d916716` | — | — |
| R3 | `74734d7` | exit 0 | 1079 |
| R6a (carga por archivo) | `26288bf` | `TSC_EXIT=0` | `Test Files 104 passed (104)` · `Tests 1082 passed (1082)` |
| R6b (congelar `MOVER`) | `9d033e3` | `TSC_EXIT=0` | `Test Files 104 passed (104)` · `Tests 1082 passed (1082)` |
| R4a (reposicionamiento) | `11804b6`, `56c66e0`, `d7d96fd` | exit 0 | `Test Files 106 passed (106)` · `Tests 1094 passed (1094)` |
| R4c (reposicionamiento determinista, `094`) | `ae476f1` | `TSC_EXIT=0` | `Test Files 107 passed (107)` · `Tests 1115 passed (1115)` |

Las salidas están íntegras en `briefs/resultados/R6a.md`, `R6b.md`, `R4a.md`, `R4c.md` y `R5.md`.

## 2b. Dependencia de la `093` y estado de la `094`

- **La acción de aprobación depende por completo de la `093`:** si no está aplicada en ese entorno (una base restaurada, otro ambiente), **la aprobación falla y no hay fallback**. El 2026-10-04 ese aviso quedó escrito en el repositorio de código (`ae476f1`): en la cabecera de `db/093` y en su fila de `db/README.md`.
- **`094` (R4c) está en el repositorio y NO está aplicada en la base.** La base usa la `093`, que es la versión **no determinista** del reposicionamiento: su `UPDATE` sobre `rdt_actividades` se alimentaba del payload fila por fila y PostgreSQL elegía una arbitrariamente cuando una actividad tenía varios vínculos repartidos en paquetes distintos. La `094` lo corrige y además devuelve `sinLinea` y `actividadesAmbiguas`. **Aplicarla es la Ola 0b** y depende de que el archivo de credenciales se pueda leer otra vez (se encontró listado pero inaccesible a toda API durante la tanda R4c).

## 3. Migración `093` (R4b), aplicada por el Orquestador con el protocolo

- **Hora:** 2026-10-04 08:41:32. **Vía:** conexión directa, con el valor de `PR_DB_URL` leído dentro del proceso, sin imprimirlo.
- **Candado:** creado antes de aplicar, borrado al terminar. Script temporal `migrar_R4b.py`, fuera del repositorio, borrado.
- **Conexión:** `select 1` → OK.
- **Conteos antes y después, idénticos en las ocho tablas:**

| Tabla | Antes | Después |
|---|---|---|
| `proyecto_plan_maestro` | 8 | 8 |
| `rdt_partes` | 73 | 73 |
| `rdt_actividades` | 104 | 104 |
| `rdt_actividad_partidas` | 51 | 51 |
| `rdt_partes_historial` | 41 | 41 |
| `plan_maestro_partidas` | 267 | 267 |
| `dp_partidas` | 66 | 66 |
| `paquetes_trabajo` | 2 | 2 |

- **CHECK de `rdt_partes_historial.accion`:** antes `ARRAY['CORRECCION','VALIDAR','RECHAZAR','BORRADO']`; después `ARRAY['CORRECCION','VALIDAR','RECHAZAR','BORRADO','REPOSICIONAMIENTO']`.
- **Función creada:** `aprobar_plan_maestro_con_reposicionamiento(p_plan_id uuid, p_aprobado_por_id uuid, p_reposicionamiento jsonb)`. Coincide con la firma que llama la ruta.
- **`recalcular_pr_planificado(p_proyecto_id uuid)`** existe en la base (desde `db/061`), así que U8 cabe dentro de la misma transacción.
- **Commit** de la base de datos: `COMMIT ok`. Sin cambios de datos.

## 4. Verificación en vivo: la que NO hay

- **R4 (reposicionamiento): sin verificación en vivo.** No existe un servicio de prueba con Plan Maestro en BORRADOR (OP9). Lo verificado es `tsc`, la suite completa, la prueba de la función pura y la migración aplicada.
- **`sinLinea` (R4c):** verificado por pruebas, no en vivo. La función pura lo clasifica, la función SQL lo devuelve en su `jsonb` y la ruta lo expone en la respuesta de la aprobación (prueba: «`sinLinea` vuelve en el 200»). En la app no se ha visto.
- **R6a y R6b:** verificados por pruebas con doble de Supabase, **no** por una llamada real a la API.
- **R1, R2, R3:** verificados por pruebas; R3 tuvo además tres llamadas en vivo en la tanda R2-R3 (servicios PS-0004, PS-0007 y PS-0008).

## 5. Documentación

- `python scripts/verificar-referencias.py` → `Archivos revisados: 46` · `HUÉRFANOS (0)` · `ENLACES ROTOS (0)` · `EXIT=0`. Las dos menciones sin archivo son preexistentes y ajenas a este plan.
- Flujos tocados: `06-rdt.md`, `14-accesos-y-restricciones.md`, `15-cronograma.md`, `19-paquetes-de-trabajo-y-jerarquia-de-control.md`, `20-plan-maestro.md` y el `README.md` de `04-flujos-de-negocio/`.
- **2026-10-04, Olas 1, 2 y 4** ( [`resultados/DOCS-L3.md`](../01-planes/2026-10-02-observaciones-victor-lote-3-briefs/resultados/DOCS-L3.md) ): se corrigió el lenguaje de U4 en los cuatro archivos, se aplicó la clasificación del Auditor a las 39 filas del libro y se pasaron las 16 filas que faltaban. Verificador: 0 huérfanos, 0 enlaces rotos, exit 0.

## 6. Política de niveles de modelos

- `python scripts/niveles-modelos.py` → 21 modelos medidos, 30,0936 USD en total, con la banda de corte impresa.
- Hechos comprobados el 2026-10-04 (opencode 1.18.34): la herramienta de subagentes no acepta modelo; `opencode.json` en la raíz del proyecto pisa al global; `.opencode/config.json` **no** lo pisa; `opencode run --model` pisa todo en la invocación; la configuración se resuelve al arrancar el proceso. Detalle y comandos en `docs/00-estandar-agentes/10-niveles-de-modelos.md`.

## 7. Lo que quedó sucio y no se tocó

- En `pg_control_proyectos`: 30 archivos `.playwright-mcp/` (logs y volcados de página de sesiones del 2026-10-03 y 2026-10-04) sin trackear. No son de este plan y no se borraron.
- Fila `OP7` del libro de hallazgos: **resuelto el 2026-10-04** — estaba incompleta (una celda menos) y su estado («Resuelta») no era cierto; se completó y quedó en «Registrada» con el motivo.
