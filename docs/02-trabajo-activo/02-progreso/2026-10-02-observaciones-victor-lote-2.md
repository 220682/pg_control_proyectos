# Progreso — Observaciones de Victor (Lote 2: acciones del checklist O5, cronograma O6 y acta de conformidad O7)

> **Archivo en actualización** (escrito por primera vez el 2026-10-02 en la Tanda D del Lote 2, ítems D1/D2/D3; queda «en actualización» hasta el cierre del plan). Refleja el estado real al momento de escribirlo.

## Referencia al plan

- Plan: [`docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-2-plan.md`](../01-planes/2026-10-02-observaciones-victor-lote-2-plan.md).
- Spec: [`docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor.md`](../01-planes/2026-10-02-observaciones-victor.md) (O5, O6, O7; Gate Spec aprobado 2026-10-02).
- Briefs y resultados de tanda: [`docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-2-briefs/`](../01-planes/2026-10-02-observaciones-victor-lote-2-briefs/) (`resultados/A.md`, `resultados/B.md`).

## Estado general y fase actual

- **Estado: En ejecución.** Gate Spec y Gate 1 aprobados por Victor (2026-10-02); **Gate 2 pendiente**.
- Fases:
  - **A — Checklist (O5 + O7): CERRADA CONFORME.** A1–A8 todos `Conforme`; migración `089` aplicada y verificada; código en `local-worker-1` (`c219069`, `af60e85`, pusheado a `origin/local-worker-1`).
  - **B — Cronograma (O6): EN CURSO con bloqueo gestionado.** `resultados/B.md` la registra **DETENIDA**: los dos servicios vigentes (PS-0004 y PS-0006) tienen Plan Maestro aprobado y la recarga devuelve 409 **antes** del parser. El Orquestador resolvió el bloqueo con la mitigación **R7 aprobada en el Gate 1**: Worker 2 crea un **servicio de prueba nuevo** (marcado `PRUEBA-…`, sin PM, sin cronograma) por el flujo normal de la app; si no es posible sin navegador, devuelve las opciones 1–3 a Victor (nada destructivo). **Los estados de B1–B7 siguen siendo los de `resultados/B.md`** hasta que la tanda se reanude y actualice ese archivo.
  - **C — Integración (`db/README.md` con `089`, merge a `main`): pendiente** (merge solo tras Gate 2). `db/README.md` aún no tiene la fila `089`.
  - **D — Documentación: EN CURSO (esta tanda).** D1 (índice de planes), D2 (flujos 12, 08, 15, 14 + índices de flujos), D3 (deuda documental del Lote 1: progreso y evidencia homónimos) hechos. **D4 (traslado del libro de hallazgos) queda fuera de esta tanda, pendiente.**
- Auditoría y mensaje de cierre: pendientes (`04-auditoria/2026-10-02-observaciones-victor-lote-2.md`).

## Tabla de roles / Workers y estado

| Rol | Estado |
|---|---|
| Orquestador | Activo. Consolidó el cierre de tanda A y aprobó la mitigación R7 para B. |
| Planner | Plan entregado (Gate 1 aprobado con respuestas (i)–(v)). |
| Worker 1 (tanda A, `local-worker-1`) | Terminada: A1–A8 `Conforme`; 2 commits; push a `origin/local-worker-1`. |
| Worker 2 (tanda B, `local-worker-2`) | En curso: script `scripts/smoke-cronograma.mjs` commiteado (`c502122`, pusheado); smokes bloqueados por 409 hasta crear el servicio de prueba (R7). |
| Documentador | **En curso (esta tanda):** D1, D2 y D3 ejecutados; D4 pendiente. |
| Worker git | Pendiente (merge a `main` tras Gate 2). |
| Auditor | Pendiente (informe al terminar la Fase D). |

## Skills revisados

Del plan: `seguir-flujo-de-planes` (Orquestador, al lanzar carriles y antes del cierre), `cerrar-tanda` (Workers, aplicado en A y parcialmente en B), `trasladar-hallazgos` (Documentador, tanda final — **D4, pendiente**) y `verificar-permisos-por-rol` (**no aplica**: ninguna observación cambia permisos). En esta tanda (D1–D3) no se ejecuta ningún Skill nuevo; el de traslado se usará en D4.

## Avances terminados

- **Tanda A completa (O5 + O7):** migración `089` (columnas `grupo_accion`, `ruta_accion`, `etiqueta_accion`; 9 `PANTALLA`, 4 rutas, 7 etiquetas «Crear / Ver»); regla de render en `acciones-checklist.ts` + 17 tests; `page.tsx` con select ampliado, ocultamiento de fase `CIERRE` y SSR verificado (9 comprobaciones); gate de cierre (`confirmar-transicion`) sin fase `CIERRE` con prueba en ambos sentidos; editor sin ítems de cierre; rechazo 400 de subida a ítems del Grupo B; A7 sin filas que eliminar. Verificación: **100 archivos / 1043 tests OK · `tsc` exit 0 · lint 27 = baseline · `next build --webpack` exit 0**.
- **Bloqueo de B gestionado:** 409 de PS-0006/PS-0004 diagnosticado con salida real (`soloAnalizar=true`, cero escrituras); mitigación R7 (servicio de prueba nuevo `PRUEBA-…`) aprobada y autorizada; además autorizado el arreglo del 500 crudo de `POST /api/cronograma` (falta `esIdProyectoValido`) dentro de B3/B4.
- **Deuda del Lote 1:** `PPTO-prueba N°01.xlsx` commiteada (`94997ab`, decisión de Victor en Gate 1 (i)).
- **Fase D (parcial, esta tanda):** fila del Lote 2 en [`01-planes/README.md`](../01-planes/README.md); flujos `12-checklist.md` (columna «Grupo / acción», Grupos de acción O5, RB1–RB3), `08-programa-portafolio-proyecto.md` (CIERRE no cuenta), `15-cronograma.md` (RB4), `14-accesos-y-restricciones.md` (fila 74 + nota 4 + actualización Gate 1; **el artefacto «Matriz de permisos» lo edita solo Victor**), índice de `04-flujos-de-negocio/README.md`; deuda D3 saldada (progreso y evidencia del Lote 1).

## Trabajo actual

Tanda B (O6): reanudación sobre el servicio de prueba nuevo de R7 (o devolución de la pregunta con las opciones 1–3 de `resultados/B.md`). Tanda D: D4 (traslado del libro de hallazgos + verificador de referencias) pendiente.

## Pendientes

1. **B:** reanudar la tanda con el servicio de prueba nuevo; cerrar B1–B7 (diagnóstico, corrección, logs, `traducir-error`, smokes de éxito y fallo, comandos).
2. **A-H1:** expresión no nulo-safe en `page.tsx` — **Pendiente de decisión de Victor en el Gate 2** (nulo-safe ahora u otro plan).
3. **C1:** `db/README.md` con la fila `089` + merge a `main` tras Gate 2.
4. **D4:** trasladar el libro de hallazgos (MB1–MB3, RB1–RB4, OP1–OP4, huérfanos) y ejecutar `python scripts/verificar-referencias.py` sin referencias rotas.
5. Informe de Auditoría, mensaje de cierre y Gate 2; verificación final de Victor en la app desplegada (riesgo R6).
6. `resultados/B.md` sigue registrando «DETENIDA» con la pregunta de PS-0006: al reanudar, actualizar su tabla de estados (el archivo aún no refleja la decisión R7 del Orquestador).

## Commits, ramas y worktrees usados

- **Código (`py_control_proyectos_web`):** `local-worker-1` (base `ce5623e`): `c219069`, `af60e85` (+ push a `origin/local-worker-1`). `local-worker-2` (fast-forward a `main`, autorizado en Gate 1 (iv)): `c502122` (+ push). **`main` sigue en `ce5623e`** (merge de A y B solo tras Gate 2). Worktrees `.worktrees/local-worker-1` y `.worktrees/local-worker-2`.
- **Migración `089`:** aplicada por **Worker 2/Worker 1 con credenciales autorizadas** (Q3; script temporal fuera del repo, protocolo de migraciones) y verificada con conteos antes/después.
- **Documentación (`pg_control_proyectos`, `main`):** `99f9280` (briefs), `1899d39` (Gate Spec), `10ceded` (tanda A conforme, tanda B detenida, hallazgos consolidados, decisión R7); esta tanda D se commitea aparte.

## Medición

Sin filas de medición todavía (la mide el Orquestador al cerrar, plantilla `10-medicion-y-eficiencia.md`).

## Operaciones de git

- `push origin local-worker-1` y `push origin local-worker-2` → hechos por los Workers.
- `merge local-worker-1 + local-worker-2 → main` → **pendiente, solo tras Gate 2**.

## Hallazgos y preguntas de negocio

- Libro de hallazgos del plan (§ Hallazgos): MB1–MB3 `Registrada`; RB1–RB4 `Registrada` (**RB1–RB4 ya escritas en los flujos dueño en esta tanda, D2 — pendiente de marcar `Trasladada` al hacer D4**); OP1–OP4 `Registrada` (clasificación del Auditor pendiente); huérfanos: ninguno detectado (revisión de esta tanda: aparecen 2 archivos no míos sin confirmar en el repo — ver Dudas abajo).
- Preguntas vivas: A-H1 (Gate 2) y, si R7 no puede ejecutarse sin navegador, las opciones 1–3 de `resultados/B.md`.

## Bloqueos, riesgos y decisiones requeridas

- **R7 en ejecución:** mientras no exista el servicio de prueba nuevo, B1–B6 no avanzan (409 previo al parser).
- R2 (gate de cierre): cubierto con prueba en ambos sentidos (A4). R6 (local ≠ Vercel): verificación final de Victor en producción al cierre. R5: `089` aplicada, no hubo denegación.

## Próximo paso verificable

Reanudar la tanda B con el servicio de prueba nuevo (R7) y, en paralelo, la tanda D4 (traslado de hallazgos + verificador), cerrando después con Auditoría y Gate 2.

## Última actualización y responsable

2026-10-02, Documentador (Tanda D, ítems D1/D2/D3). **Archivo en actualización** hasta el cierre del plan.

## Handoffs

### Handoff del 2026-10-02 (Documentador → Orquestador)

- D1, D2 y D3 ejecutados en esta tanda; D4 queda pendiente (no ejecutar hasta que el Orquestador lo indique).
- El libro de hallazgos sigue `Registrada` en todas las filas: RB1–RB4 ya tienen su texto en los flujos dueño (commits de esta tanda), se marcan `Trasladada` con enlace y commit en D4.
- **Dudas para Victor/Orquestador:** (1) `docs/02-trabajo-activo/01-planes/README.md` decía que el Lote 1 estaba «Implementando» pese a estar cerrado — se dejó como estaba al editar solo la fila del Lote 2; (2) el índice de `04-flujos-de-negocio/README.md` llamaba «Plan en curso» al Lote 1 cerrado — corregido al añadir la fila del Lote 2; (3) la Punch List del Lote 1 quedó con estados «Sin verificar» pese al cierre (la evidencia reconstruida está en la homónima del Lote 1); (4) hay cambios ajenos sin confirmar en el repo: `scripts/README.md` modificado y sin commit, más `scripts/arranque.py` y `docs/02-trabajo-activo/01-planes/2026-10-02-contexto-de-arranque-de-agentes.md` sin trackear — **no se tocaron ni se commitearon**.
