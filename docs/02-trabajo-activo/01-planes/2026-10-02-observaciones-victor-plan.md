# 2026-10-02 — Plan: lote 1 — checklist (catálogo y responsables), área Jefatura y error del cronograma

> Plan del **Planner** sobre el Spec aprobado [`2026-10-02-observaciones-victor.md`](2026-10-02-observaciones-victor.md) (Gate Spec: aprobado por Victor, 2026-10-02). Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. **2 Workers** con propiedad de archivos disjunta. Briefs por tanda en `2026-10-02-observaciones-victor-briefs/`.

## Identificación y estado

- Tema: Lote 1 de observaciones de Victor — (O1) responsable en checklist, (O2) área PR→JF, (O3) catálogo definitivo del checklist, (O4) error de importación de cronograma (loguear + corregir).
- Fecha: 2026-10-02.
- Estado: **Implementando** — **Gate 1 aprobado por Victor** (2026-10-02).
- Gate 1: `aprobado por Victor (2026-10-02)` — 2 Workers; datos de prueba OK; pre-autorizaciones OK; tabla de flujos OK.

## Referencia al Spec aprobado

| Spec | Estado |
|---|---|
| [`2026-10-02-observaciones-victor.md`](2026-10-02-observaciones-victor.md) | Aprobado (Gate Spec, 2026-10-02) |

## Objetivo, alcance y no alcance

- **Resultado esperado:** ver «Resultado esperado (Lote 1)» del Spec (O1–O4).
- **Alcance:** O1, O2, O3, O4.
- **No alcance:** generación automática de "Recursos del servicio" desde el DP; fusión de chips; observaciones futuras; "Acta de conformidad" (CIERRE) intacta.
- **Validación esperada:** vitest, `tsc`, lint, build, smoke de API (sin Playwright), navegación manual de Victor.

## Entorno, repositorios, ramas y worktrees

- Modo: local. Documentación en `pg_control_proyectos` (`main`, directo). Código en `py_control_proyectos_web`.
- **Verificado y sincronizado (2026-10-02):** `main` = `origin/main` = `647999a`. `local-worker-1` y `local-worker-2` **ambas en `647999a`**, limpias, con `node_modules` y `.env.local` en sus worktrees. `local-worker-3`/`local-worker-4` quedaron atrás (no se usan; limpiar en plan futuro).
- **2 carriles** (ramas/worktrees existentes, sin crear infraestructura):

| Carril | Rama | Worktree | Observaciones |
|---|---|---|---|
| 1 · Checklist | `local-worker-1` | `.worktrees/local-worker-1` | O1 + O3 |
| 2 · Cronograma y área | `local-worker-2` | `.worktrees/local-worker-2` | O2 + O4 |

- Merge a `main` **solo tras el Gate 2** (lo hace el Orquestador vía Worker git).

## Skills aplicables

Skills de `.claude/skills/` de `pg_control_proyectos` (el repo de código no tiene carpeta de Skills, verificado 2026-09-30):

| Skill | Quién | Dónde |
|---|---|---|
| `cerrar-tanda` | Worker | Al final de cada tanda |
| `seguir-flujo-de-planes` | Orquestador | Al lanzar cada carril y antes del mensaje de cierre |
| `trasladar-hallazgos` | Documentador | Tanda final (traslado de hallazgos) |
| `verificar-permisos-por-rol` | — | **No aplica**: ninguna observación cambia permisos por rol |

## Fases y dependencias

| Fase | Qué | Worker | Depende de |
|---|---|---|---|
| A | Migración catálogo (`087`) + checklist UI/lógica (O1 + O3) | Worker 1 | — |
| B | Migración área (`088`) + cronograma (O2 + O4) | Worker 2 | — |
| C | Integración (db/README + verificación cruzada) | Orquestador/Worker git | A, B (tras Gate 2) |
| D | Documentación (flujos + traslado de hallazgos) | Documentador | A, B |

A y B son independientes (matriz de propiedad disjunta): corren en paralelo.

## Matriz de propiedad de archivos

| Archivo | Worker 1 (checklist) | Worker 2 (cronograma+área) |
|---|---|---|
| `db/087_catalogo_checklist.sql` (nuevo) | Dueño | — |
| `db/088_area_jefatura.sql` (nuevo) | — | Dueño |
| `src/components/ui/SelectorUsuario.tsx` | Dueño | — |
| `src/lib/usuarios/lista-usuarios.ts` | Dueño | — |
| `src/app/(workspace)/proyectos/[id]/checklist/editar/editor-checklist.tsx` | Dueño | — |
| `src/lib/checklist/checklist.ts` (+ test) | Dueño | — |
| `src/lib/config/registro-accesos.ts` | Dueño | — |
| `src/app/api/cronograma/route.ts` | — | Dueño |
| `src/lib/errores/traducir-error.ts` | — | Dueño |
| `src/components/ui/FormularioCronograma.tsx` | — | Dueño |
| `db/README.md` | — (integración) | — (integración) |

**Sin archivos compartidos entre carriles.** `db/README.md` (líneas `087` y `088`) lo actualiza la integración (C), no los Workers, para evitar choque.

## Equipo del plan

| Rol | Modelo | Sesión/tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|
| Orquestador | Sonnet | esta sesión | `main` (docs) | N/A | Activo |
| Planner | Sonnet | este plan | `main` (docs) | N/A | Plan entregado |
| Worker 1 | Sonnet | tanda A | `local-worker-1` | `.worktrees/local-worker-1` | Pendiente |
| Worker 2 | Sonnet | tanda B | `local-worker-2` | `.worktrees/local-worker-2` | Pendiente |
| Documentador | Sonnet | tanda final | `main` (docs) | N/A | Pendiente |
| Worker git | Haiku | a pedido | opera sobre las demás | — | Pendiente |
| Auditor | Sonnet | | `main` (docs) | N/A | Pendiente |

## Archivos / componentes afectados

Ver «Matriz de propiedad». Nuevos: `db/087_catalogo_checklist.sql`, `db/088_area_jefatura.sql`.

## Punch List embebida

Formato `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. Evidencia en el archivo homónimo.

### Worker 1 — Checklist (O1 + O3)

| ID | Ítem | Evidencia mínima | Estado |
|---|---|---|---|
| A1 | Migración `087`: insertar `cronograma`, `paquete_trabajo`, `plan_maestro`; renombrar `recursos_sin_costo`→"Recursos del servicio", `personal_requerido`→"Listado de personal nuevo", `pets`→"Listado de pets"; eliminar AL_INICIO no listados (incl. `materiales_con_costo`); fijar `orden` 1–13. Idempotente. | SQL + lectura crítica | Sin verificar |
| A2 | `lista-usuarios.ts`: ordenar por rol (`PRIORIDAD_ROL_PRINCIPAL`) y luego nombre; reflejar en `etiquetaSelector`. | Prueba unitaria + `tsc` | Sin verificar |
| A3 | `SelectorUsuario.tsx`: quitar filtro por rol; listar todos los usuarios ordenados por rol. | `tsc` + build | Sin verificar |
| A4 | `editor-checklist.tsx`: todo ítem (catálogo y personalizado) muestra desplegable de responsable con todos los usuarios; sin filtro por rol. | `tsc` + build | Sin verificar |
| A5 | `checklist.ts`: `documentoCompleto` completa por check manual para todos (incl. DP/PR); revisar consumidores de `checklistCompleto`/`documentosPendientes`. | Prueba unitaria + grep de consumidores | Sin verificar |
| A6 | `registro-accesos.ts`: "Personal NUEVO" → "Listado de personal nuevo". | Diff | Sin verificar |
| A7 | `npm test`, `npx tsc --noEmit`, `npm run lint`, build verdes en el carril. | Salida de comandos | Sin verificar |

### Worker 2 — Cronograma y área (O2 + O4)

| ID | Ítem | Evidencia mínima | Estado |
|---|---|---|---|
| B1 | Migración `088`: `areas` `PR`/`Proyecto` → `JF`/`Jefatura`, conservando `perfiles.area_id`. Idempotente. | SQL + lectura crítica | Sin verificar |
| B2 | `api/cronograma/route.ts`: loguear el error de lectura/parseo en servidor con contexto (mensaje, archivo, formato). | Lectura crítica + build | Sin verificar |
| B3 | Restaurar el mensaje específico (`traducirErrorApi` / `respuestaErrorInesperado` / `FormularioCronograma`). | Smoke con fallo forzado | Sin verificar |
| B4 | Reproducir y **corregir** el error de lectura/parseo (Excel plantilla y PDF de MS Project). | Smoke con importación exitosa | Sin verificar |
| B5 | `npm test`, `npx tsc --noEmit`, `npm run lint`, build verdes en el carril. | Salida de comandos | Sin verificar |

### Integración y documentación

| ID | Ítem | Evidencia mínima | Estado |
|---|---|---|---|
| C1 | `db/README.md` lista `087` y `088`; ramas integradas sin conflictos. | Diff + git status | Sin verificar |
| D1 | Flujos `12-checklist.md` y `02-usuarios.md` según la tabla del Gate 1; índices actualizados. | Diff + casilla "aplicado" | Sin verificar |
| D2 | Trasladar hallazgos (RB1, RB2) a su destino; `verificar-referencias.py` sin rotos. | Salida del verificador | Sin verificar |

## Riesgos y bloqueos

| # | Riesgo | Mitigación |
|---|---|---|
| R1 | Causa raíz del error de cronograma (B4) no identificada aún | B2 loguea el detalle; B3 restaura el mensaje; B4 reproduce con los archivos de prueba antes de corregir |
| R2 | Pasar DP/PR a check manual rompe el indicador "checklist completo" | A5 revisa todos los consumidores de `checklistCompleto`/`documentosPendientes` |
| R3 | Eliminar `materiales_con_costo` deja `proyecto_documentos` huérfanos | La migración `087` preserva o limpia las filas existentes |

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-02 | Gate Spec aprobado | Victor |
| 2026-10-02 | Todos los ítems del checklist: casilla + responsable; completar por check | Victor |
| 2026-10-02 | Área PR → JF "Jefatura" | Victor |
| 2026-10-02 | O4: loguear el error y corregirlo (no solo el mensaje) | Victor |
| 2026-10-02 | Gate 1 aprobado: 2 Workers, datos de prueba y pre-autorizaciones OK, tabla de flujos OK | Victor |

## Enlaces a progreso y evidencia homónimos

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-10-02-observaciones-victor.md`
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-02-observaciones-victor.md`
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-10-02-observaciones-victor.md`

## Libro de hallazgos

Formato de fila: `| ID | Fecha | Quién | Qué | Destino | Estado | Enlace |`. Estados: `Registrada` → `Trasladada` · `Descartada` · `Pendiente de decisión`.

### Mejoras (de trabajo)

Ninguna.

### Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién | Qué | Destino | Estado |
|---|---|---|---|---|---|
| RB1 | 2026-10-02 | Victor | Catálogo definitivo del checklist (13 ítems, orden, responsables, completar por check) | `04-flujos-de-negocio/12-checklist.md` | `Trasladada` (commit `5f1ed31`) |
| RB2 | 2026-10-02 | Victor | Área `JF` = "Jefatura" (reemplaza `PR`/"Proyecto") | `04-flujos-de-negocio/02-usuarios.md` | `Trasladada` (commit `5f1ed31`) |

### Observaciones sobre la política

Ninguna.

### Carpetas/archivos huérfanos

Ninguna.

## Gate 1 — respuestas de Victor (2026-10-02)

- Datos de prueba: OK (usar `CRON-PROMCOSER-AESA-001.pdf` y `Cron-prueba N°01.xlsx`).
- Pre-autorizaciones: OK (`npm run dev` local + credenciales de prueba para el smoke, sin mostrar secretos).
- Tabla de flujos: OK (aplicada por el Documentador en D1).
- 2 Workers (no 1), ramas `local-worker-1` y `local-worker-2`, worktrees sincronizados a `main`.

## Informe de Auditoría

Enlace al archivo homónimo en `04-auditoria/` (se crea al auditar).

## Mensaje de cierre

Formato `09-cierre.md` (se escribe tras el Gate 2).

## Elementos postergados propuestos para planes futuros

- Generación automática de "Recursos del servicio" desde los datos del DP.
- Limpieza de ramas/worktrees `local-worker-3` y `local-worker-4` (atrás de `main`).
