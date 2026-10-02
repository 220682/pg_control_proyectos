# Progreso — Observaciones de Victor (Lote 1: checklist, área Jefatura y error de cronograma)

> **Deuda documental saldada el 2026-10-02** por el Documentador del Lote 2 (Tanda D, ítem D3): este archivo no existió en su momento (observación OP1 del plan del Lote 2). El estado que sigue se reconstruyó del plan, de su informe de auditoría y de la historia de git, sin inventar datos.

## Referencia al plan

- Plan: [`docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-plan.md`](../01-planes/2026-10-02-observaciones-victor-plan.md).
- Spec: [`docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor.md`](../01-planes/2026-10-02-observaciones-victor.md) (observaciones O1–O4; registro vivo donde sigue abriendo lotes).
- Auditoría: [`docs/02-trabajo-activo/04-auditoria/2026-10-02-observaciones-victor.md`](../04-auditoria/2026-10-02-observaciones-victor.md).
- Evidencia: [`docs/02-trabajo-activo/03-evidencia/2026-10-02-observaciones-victor.md`](../03-evidencia/2026-10-02-observaciones-victor.md) (también creada en esta deuda).
- Briefs: **no existieron** para este plan (la carpeta `2026-10-02-observaciones-victor-briefs/` nunca se creó; registrado en OP1 del Lote 2).

## Estado general y fase actual

- **Estado: Cerrada.** Gate Spec, Gate 1 y Gate 2 aprobados por Victor (todos el 2026-10-02).
- Fases del plan y cómo terminaron:
  - **A — Migración `087` + checklist (O1 responsable/desplegables, O3 catálogo definitivo):** hecha por el Worker 1 en `local-worker-1`; ítems A1–A7 verificados (ver evidencia).
  - **B — Migración `088` + cronograma y área (O2 área JF, O4 loguear/corregir el error):** hecha por el Worker 2 en `local-worker-2`; ítems B1–B5 verificados salvo la confirmación de la importación de punta a punta (ver nota abajo).
  - **C — Integración (`db/README.md` con 087/088, unión de carriles, merge a `main`):** hecha (commit `ce5623e`).
  - **D — Documentación (flujos 12, 02 y 14, libro de hallazgos):** RB1 y RB2 trasladadas (`5f1ed31`, `cd3465b`) y la nota 4 del flujo 14 reescrita tras el informe de auditoría (`9573dd2`). **El D3 (este archivo y su evidencia) quedó sin hacer** — se cierra aquí, en el Lote 2.

## Tabla de roles / Workers y estado

| Rol | Estado al cierre |
|---|---|
| Orquestador | Activo hasta el cierre (Gate 2 y mensaje de cierre, commit `2700ad8`). |
| Planner | Plan entregado (Gate 1 aprobado). |
| Worker 1 (`local-worker-1`) | Tanda A terminada: O1 + O3 (migración `087`, selector de responsables, catálogo de 13 ítems, completado por check). |
| Worker 2 (`local-worker-2`) | Tanda B terminada: O2 + O4 (migración `088`, logging y detección de formato del cronograma). |
| Documentador | **Deuda D3 pendiente hasta hoy** (2026-10-02, tanda D del Lote 2). |
| Auditor | Informe entregado con recomendación inicial «Requiere corrección»; los dos puntos se resolvieron antes del Gate 2 (flujo 14 y evidencia de SQL). |

## Skills revisados

Skills de `.claude/skills/` listados en el plan: `seguir-flujo-de-planes` (Orquestador), `cerrar-tanda` (Workers), `trasladar-hallazgos` (Documentador, tanda final) y `verificar-permisos-por-rol` (**no aplica**: ninguna observación cambia permisos por rol). Este archivo se levanta en la Tanda D del Lote 2 junto con el resto de la documentación; no se ejecuta ningún Skill nuevo aquí.

## Avances terminados

- **O1 — responsables en el checklist:** `SelectorUsuario` ya no filtra por rol del documento; `lista-usuarios.ts` ordena por `PRIORIDAD_ROL_PRINCIPAL` y luego nombre (auditoría: ✓).
- **O2 — área JF:** `areas` `PR`/«Proyecto» → `JF`/«Jefatura» con la migración `088`, conservando `perfiles.area_id`; `area-usuario.ts` mapea el rol administrador y jefe de proyectos a `JF` (auditoría: ✓).
- **O3 — catálogo definitivo:** migración `087` (inserta `cronograma`, `paquete_trabajo`, `plan_maestro`; renombra `recursos_sin_costo`, `personal_requerido` y `pets`; elimina `materiales_con_costo`; fija `orden` 1–13; columna `completado`); los 13 ítems con casilla y responsable, completar por check manual para todos (auditoría: ✓).
- **O4 — cronograma:** detección de formato por MIME con fallback por extensión, `console.error` con contexto (formato, archivo, error) y devolución del mensaje en `respuestaErrorInesperado` (auditoría: ✓ **con matiz** — ver Pendientes).
- Fuentes de verdad del Lote 1 actualizadas en `main` de docs: flujos `12-checklist.md` y `02-usuarios.md` (`5f1ed31`), cierre de las filas RB1/RB2 (`cd3465b`), nota 4 del flujo `14-accesos-y-restricciones.md` (`9573dd2`).
- Deuda de archivo de prueba del Lote 1 (`docs/06-material-de-apoyo/Informacion para pruebas/PPTO-prueba N°01.xlsx`) resuelta: commiteada por decisión de Victor en el Gate 1 del Lote 2 (`94997ab`).

## Trabajo actual

Ninguno: el plan está cerrado. El trabajo vivo del registro de observaciones continúa en el Lote 2 ([plan](../01-planes/2026-10-02-observaciones-victor-lote-2-plan.md)).

## Pendientes

1. **El smoke real de O4 nunca se hizo.** La corrección de la importación de cronograma (éxito de punta a punta con `CRON-PROMCOSER-AESA-001.pdf` y `Cron-prueba N°01.xlsx`, más fallo con mensaje específico) quedó sin evidencia: solo hubo pruebas unitarias, lectura de código y la detección de formato. El informe de auditoría lo dejó como «APLICAR AHORA» y aun así el plan cerró. **Lo reabre O6 en el Lote 2, y su evidencia vive en la homónima del Lote 2:** [`docs/02-trabajo-activo/03-evidencia/2026-10-02-observaciones-victor-lote-2.md`](../03-evidencia/2026-10-02-observaciones-victor-lote-2.md).
2. **Prop muerto `filtrarPorRolClave`** en `SelectorUsuario.tsx` (quedó sin uso tras O1): clasificado NO PROMOVER por el Auditor; limpieza opcional en un plan futuro.

## Commits, ramas y worktrees usados

- **Código (`py_control_proyectos_web`):** rama `local-worker-1` desde `647999a` con `1e8cf52` (Worker 1, O1+O3) y `9ad0640` (Worker 2, O2+O4), merge de `local-worker-2` en `3951668` e integración en **`ce5623e`**. Merge a `main` y push tras el Gate 2: `main` = `origin/main` = `ce5623e`, árbol limpio (verificado en el cierre). Worktrees `.worktrees/local-worker-1` y `.worktrees/local-worker-2`.
- **Documentación (`pg_control_proyectos`, `main`):** `b482660` (Spec), `2402205`/`1be4953` (plan y Gate 1), `5f1ed31` (RB1 → flujo 12, RB2 → flujo 02), `cd3465b` (filas RB cerradas como `Trasladada`), `a006081` (informe de auditoría), `9573dd2` (flujo 14, nota 4), `2700ad8` (cierre: Gate 2, merge y mensaje de cierre).
- **Migraciones:** `087` (catálogo del checklist) y `088` (área Jefatura) **aplicadas por Victor en Supabase el 2026-10-02 y verificadas** en el Gate 2.

## Medición

Sin filas de medición registradas para este plan en su cierre; si se retoma este archivo, la llena el Orquestador con la plantilla `10-medicion-y-eficiencia.md`.

## Operaciones de git

- `merge local-worker-1 (ce5623e) → main` de la app, tras Gate 2 → hecho y verificado (`0 0` contra `origin/main`).
- `push origin main` (app y docs) → hecho en el cierre (`2700ad8` en docs).

## Hallazgos y preguntas de negocio

- Gate 1 (2026-10-02): datos de prueba OK (los dos archivos de cronograma), pre-autorizaciones OK (`npm run dev` local y credenciales de prueba para el smoke), tabla de flujos OK y **2 Workers** con `local-worker-1`/`local-worker-2`.
- RB1 (catálogo definitivo del checklist) y RB2 (área `JF` = «Jefatura») trasladadas a los flujos dueño y cerradas en el libro de hallazgos (`Trasladada`, commits `5f1ed31`/`cd3465b`).

## Bloqueos, riesgos y decisiones requeridas

- Ninguno abierto al cierre. Riesgo R2 (que el cambio de «completado» rompiera el indicador «checklist completo») cubierto con la revisión de consumidores de `checklistCompleto`/`documentosPendientes` (auditoría: grep verificado, sin huérfanos).
- La contradicción del flujo 14 detectada por el Auditor (nota 4 desactualizada) se resolvió con `9573dd2` antes del Gate 2.

## Próximo paso verificable

Ninguno propio: el plan está cerrado. El siguiente paso del registro es el Lote 2 (O5, O6, O7), que incluye el smoke de importación pendiente de aquí.

## Última actualización y responsable

2026-10-02, Documentador (Tanda D del Lote 2, ítem D3 — deuda documental del Lote 1).

## Handoffs

### Handoff del 2026-10-02 (Documentador → Orquestador)

- Este archivo y su evidencia homónima cerraron la deuda OP1 del Lote 2; el plan del Lote 1 ya puede leerse completo (plan + progreso + evidencia + auditoría).
- Lo único que sigue vivo del Lote 1 es el **smoke de O4**, que corre como O6 en el Lote 2 con su evidencia en la homónima del Lote 2.
- No se tocó el plan del Lote 1 ni ningún otro documento propio de esa tarea.
