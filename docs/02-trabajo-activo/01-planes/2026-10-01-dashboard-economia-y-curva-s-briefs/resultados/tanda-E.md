# Resumen de cierre — Tanda E (Documentador)

## Tanda, rol y modelo

- Plan `2026-10-01-dashboard-economia-y-curva-s` · Tanda **E** (Documentador) · repositorio documental `pg_control_proyectos`, rama `main`, trabajo directo.
- Modelo **DeepSeek V4.1 Flash** (`opencode-go/deepseek-v4.1-flash`).
- Insumos: brief de la tanda E, libro de hallazgos del plan, tabla (iii) del Gate 1, resúmenes de cierre de las tandas A, B, C y D, flujos 11/14/16/21 y código del worktree `local-worker-5` (solo lectura, sin editar).

## Inventario (paso 1)

Filas `Registrada` del libro cotejadas con los resúmenes de cierre:

| Grupo | Filas | Cotejo |
|---|---|---|
| Mejoras de trabajo | M1 (A/A-H1), M2 (D), M3 (D) | Presentes en `tanda-A.md` y `tanda-D.md` |
| Reglas de negocio | RB1 (Spec), RB2 (Spec), RB3 (Spec), RB4 (Spec), RB5 (B/B-H1), RB6 (C/C-H2), RB7 (D) | Presentes en Spec / `tanda-B.md` / `tanda-C.md` / `tanda-D.md` |
| Observaciones | OP1 (A/A-H2), OP2 (B/B-H3), OP3 (C/C-H1), OP4 (C-H3→D), OP5 (D), OP6 (Orquestador) | Presentes en los resúmenes / decisión del Orquestador |
| Huérfanos | Ninguna | Confirmado en A, B, C y D |

**Hallazgo del inventario:** la regla **B-H2** (el enlace desde el Dashboard Parcial lleva `?modo=fisica`; el servidor lee el parámetro) figuraba en `tanda-B.md` pero **no había sido volcada al libro**. Se agregó como **RB8** en el libro y se integró en el flujo 11 (aviso al Orquestador). No hubo filas en el libro sin respaldo en las tandas.

## Reglas de negocio trasladadas (paso 2)

Todas dentro de la estructura de su flujo dueño, aplicando la tabla (iii) del Gate 1:

- **Flujo 21 `21-curva-s.md`** — RB1, RB6, RB7: dos modos con selector (económica USD / avance físico %), % planificado PV/BAC y % real EV/BAC; rol con acceso a la pantalla = 13; el modo económico exige `puedeVerCurvaSEconomica` y responde 403; endpoint con `modo=` y derivación determinista; el modo físico lee `Σ pr_partidas.bac` en servidor y **no** lo devuelve; un eje por modo con unidad rotulada; lectura del punto por modo (pp en físico); reglas 9 y 10 (BAC=0 vs sin RDT).
- **Flujo 11 `11-dashboard.md`** — RB2, RB4, RB5, RB8: tabla «Los dos Dashboards» (Parcial sin dinero, Completo con bloques económicos), interruptor visible/deshabilitado fijo en Parcial, chip a 13 roles, lista cerrada PD5, sección nueva «Costo real de recursos» (filas MO/HM, Total = AC, «Sin resolver», legacy no sumable), orden forzado a WBS en Parcial, enlace a Curva S con `?modo=fisica`.
- **Flujo 14 `14-accesos-y-restricciones.md`** — RB3: tabla 1 con dos filas por Dashboard y dos por Curva S; nota ¹ reescrita (Completo = exactamente los 5 con economía, sin «estado objetivo / plan futuro»); bloque de actualización 2026-10-02; «Restricción de datos económicos por rol» pasa a **Implementado (2026-10-02)**.
- **Flujo 16 `16-paneles.md`** — sin cambio de texto (fila 9): solo se añadió el bullet de «Estado de implementación» con chips Dashboard y Curva S habilitados para los 13 roles y la restricción económica dentro de la pantalla.

Contradicciones **no** previstas en la tabla (iii): ninguna nueva; las de nota ¹ y el «sin interruptor / plan futuro» ya estaban listadas como contradicciones resueltas por (iii) filas 7 y 2.

## Mejoras de trabajo trasladadas (paso 3)

Un archivo por mejora en `docs/03-aprendizaje-continuo/` (plantilla `08-aprendizaje.md`), fecha 2026-10-02, con fila nueva en el índice de esa carpeta:

- [`2026-10-02-desacoplar-prueba-permisos-del-flujo-14.md`](../../../../03-aprendizaje-continuo/2026-10-02-desacoplar-prueba-permisos-del-flujo-14.md) (M1, etiqueta `tests/doc`).
- [`2026-10-02-agrupar-capturas-por-pantalla-en-tandas-con-navegador.md`](../../../../03-aprendizaje-continuo/2026-10-02-agrupar-capturas-por-pantalla-en-tandas-con-navegador.md) (M2, etiqueta `playwright/evidencia`).
- [`2026-10-02-viewport-movil-con-cdp-emulation.md`](../../../../03-aprendizaje-continuo/2026-10-02-viewport-movil-con-cdp-emulation.md) (M3, etiqueta `playwright/viewport`).

## Observaciones sobre la política — para el Auditor (paso 4)

No se editó el estándar, `AGENTS.md` ni Skills. Lista para que el Auditor clasifique (Victor decide en Gate 2):

| ID | Documento afectado | Propuesta / observación |
|---|---|---|
| OP1 | `00-estandar-agentes` / reglas de tests | Entre ventanas doc↔código puede convivir un `npm test` rojo; el plan lo resolvió ajustando el mapa de la prueba. Definir cómo se maneja la ventana. |
| OP2 | Prompt de auditoría del plan | Decía «los 10 KPI» donde la lista cerrada PD5 oculta 6; el brief mandó. Corregir la referencia de PD5. |
| OP3 | PD4 / `design.md` §254 | PD4 decía `disabled` + `title`; U01/`design.md` piden `aria-disabled` accesible por teclado; se implementó `aria-disabled`. Proponer PD4 como `aria-disabled`. |
| OP4 | E01 (Curva S) | Interpretación «EV=0 → no dibujar serie real + nota; tabla con —» confirmada en D; el Auditor verifica la clasificación. |
| OP5 | Presupuesto de tandas | ~80 llamadas subestimado para Fase T + 22 ítems de Fase D con navegador; se usaron ~108 y F12 quedó para T2. Ajustar la estimación. |
| OP6 | Política de Gate 2 | Al retomar la sesión se halló un merge `local-worker-5` → `main` de la app **sin Gate 2**; se abortó y `main` volvió a `35ac5dd`. Reforzar el control de que el merge solo ocurre tras Gate 2. |

## Archivos huérfanos (paso 5)

**Ninguno** reportado por las tandas A, B, C y D, ni detectado por el Documentador. No se borró nada.

Nota operativa (no huérfano de contenido): en el repo documental aparecieron archivos no trackeados de la **tanda T2 en curso** (`docs/02-trabajo-activo/03-evidencia/capturas/dashboard-economia-y-curva-s/T2-F13-*.png`, `….briefs/resultados/tanda-T2.md`) y un `login-snap.md` en la raíz. **No se tocaron ni se agregaron**; se reportan al Orquestador.

## Derivados e índices (paso 6)

- `docs/02-trabajo-activo/01-planes/README.md`: la fila del plan pasa de «En preparación» a **«En ejecución»** (tandas A–D cerradas, Fase E en curso, T2 y P03 pendientes).
- `docs/02-trabajo-activo/01-planes/planes-futuros.md`: se **retira** la entrada «Dashboard Parcial sin datos económicos y restricción económica definitiva» (promovida por este plan).
- Flujo 14, línea ~196: «Restricción de datos económicos por rol» → **Implementado (2026-10-02)**.
- Artefacto «Matriz de permisos»: **no se tocó** (exclusivo de Victor, P05).

## Referencias (paso 7, R06)

`python scripts/verificar-referencias.py` (invocación por defecto = núcleo de la política):

```text
Archivos revisados: 45
HUÉRFANOS (0)
ENLACES ROTOS (0)
MENCIONES SIN ARCHIVO (2)
```

Las 2 menciones sin archivo son preexistentes (`01-contexto-repositorio/03-entorno-git-y-worktrees.md` → `convenciones-de-trabajo.md`) y ajenas a esta tanda. Verificación adicional de las carpetas tocadas (`01-planes`, `03-aprendizaje-continuo`, `04-flujos-de-negocio`): **ningún enlace roto ni huérfano nuevo** aportado por mis ediciones; subsisten enlaces históricos de planes viejos (rutas `../Flujos%20de%20trabajo/…`, `CLAUDE.md` de briefs) fuera del alcance autorizado. El `tanda-T2.md` de la tanda en curso aparece referenciando un `login-snap.md` no trackeado: es de T2, no mío.

## Cierre de filas (paso 8)

- **Trasladadas:** M1–M3 (commit `2ec79de`), RB1–RB8 (commit `d262395`); RB3 con el matiz «artefacto pendiente de Victor (P05)».
- **Pendiente de decisión:** OP1–OP6 (los clasifica el Auditor; decide Victor en Gate 2).
- **Descartadas:** ninguna.
- Ninguna fila queda en `Registrada`.

## Pendientes devueltos

- **P03 (código, no lo toco):** con el flujo 14 ya editado (commit `d262395`), falta que un **Worker de código** restaure las filas «Dashboard … Parcial/Completo» y «Curva S … física/económica» al mapa `FUNCIONES` de `src/lib/permisos/permisos.test.ts`, ajuste `expect(comparadas)` y vuelva a alinear con la nueva tabla 1. Sin eso, la comparación fila-por-fila contra el archivo queda parcial (hoy siguen excluidas esas filas).
- **P05:** el artefacto «Matriz de permisos» lo actualiza **Victor** (misma tarea).
- **F12/F13:** en curso en la tanda **T2** (proyecto `PRUEBA-DASH`, evidencia T2 ya apareciendo).
- **R06:** el verificador por defecto da 0 rotos / 0 huérfanos; el Auditor lo confirma contra la Punch List.

## Commits en `main` (`pg_control_proyectos`)

| Commit | Contenido |
|---|---|
| `d262395` | Flujos 11, 14, 16 y 21 (reglas RB1–RB8) |
| `2ec79de` | Mejoras M1–M3 + índice de `03-aprendizaje-continuo/` |
| `0e757f3` | Índice de planes, retiro en `planes-futuros.md` y libro de hallazgos marcado |
| (este) | Resumen de cierre `tanda-E.md` + fila RB8 del inventario |

Rama comprobada antes de commitear con `git branch --contains`/`git status`; `git add` siempre explícito por archivo (nunca `-A`). Push `origin main` al cierre.

## Llamadas y contexto

~55 llamadas aproximadas. Las cifras exactas las mide el Orquestador con el script.

## Skills revisados

- `pg_control_proyectos/.claude/skills/`: `trasladar-hallazgos` (usado), `cerrar-tanda`, `seguir-flujo-de-planes`, `verificar-permisos-por-rol` (no aplica a esta tanda). Repo de la app: **no tiene** `.claude/skills` (solo lectura).

## Fuentes de verdad revisadas

- Editadas: `04-flujos-de-negocio/11-dashboard.md`, `14-accesos-y-restricciones.md`, `16-paneles.md`, `21-curva-s.md`; `03-aprendizaje-continuo/README.md`; `02-trabajo-activo/01-planes/README.md` y `planes-futuros.md`; libro de hallazgos del plan.
- Solo lectura: código del worktree `local-worker-5` (`permisos.ts`, `permisos.test.ts`, `matriz-base-flujo14.ts`, `route.ts` de `api/curva-s`) para comprobar coherencia con los flujos.
