# 2026-10-02 — Plan: lote 1 — checklist (catálogo y responsables), área Jefatura y error del cronograma

> Plan del **Planner** sobre el Spec aprobado [`2026-10-02-observaciones-victor.md`](2026-10-02-observaciones-victor.md) (Gate Spec: aprobado por Victor, 2026-10-02). Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Un solo Worker, tandas secuenciales. Briefs por tanda en `2026-10-02-observaciones-victor-briefs/`.

## Identificación y estado

- Tema: Lote 1 de observaciones de Victor — (O1) responsable en checklist, (O2) área PR→JF, (O3) catálogo definitivo del checklist, (O4) error de importación de cronograma (loguear + corregir).
- Fecha: 2026-10-02.
- Estado: **Planificando**.
- Gate 1: `pendiente`.

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
- **Verificado (2026-10-02):** `main` = `origin/main` = `647999a` (árbol limpio). `local-worker-1` está en `647999a` (libre); `local-worker-2..4` quedaron atrás. Comandos: `npm test` (vitest run), `npx tsc --noEmit`, `npm run lint`, `npm run build`.
- **Carril único:** 1 Worker en la rama `local-worker-1` (reusada, ya en `main`; se confirma en el Gate 1). Sin worktree nuevo: el Worker trabaja en el checkout raíz cambiado a esa rama (evita el problema conocido de junction de turbopack con worktrees).
- Merge a `main` **solo tras el Gate 2**.

## Skills aplicables

Skills de `.claude/skills/` de `pg_control_proyectos` (el repo de código no tiene carpeta de Skills, verificado 2026-09-30):

| Skill | Quién | Dónde |
|---|---|---|
| `cerrar-tanda` | Worker | Al final de cada tanda |
| `seguir-flujo-de-planes` | Orquestador | Al lanzar la tanda y antes del mensaje de cierre |
| `trasladar-hallazgos` | Documentador | Tanda final (traslado de hallazgos) |
| `verificar-permisos-por-rol` | — | **No aplica**: ninguna observación cambia permisos por rol |

El Worker lista `.claude/skills/` de ambos repos al empezar y lo anota en su `resultados/<tanda>.md`.

## Fases y dependencias

| Fase | Qué | Depende de |
|---|---|---|
| A | Migraciones (catálogo del checklist y área JF) | — |
| B | Checklist: responsables (O1) y catálogo/UI (O3) | A |
| C | Cronograma: error (O4) | — (independiente) |

## Equipo del plan

| Rol | Modelo | Sesión/tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|
| Orquestador | Sonnet | esta sesión | `main` (docs) | N/A | Activo |
| Planner | Sonnet | este plan | `main` (docs) | N/A | Plan entregado |
| Worker 1 | Sonnet | tandas A, B, C | `local-worker-1` | checkout raíz | Pendiente |
| Documentador | Sonnet | tanda final | `main` (docs) | N/A | Pendiente |
| Worker git | Haiku | a pedido | opera sobre las demás | — | Pendiente |
| Auditor | Sonnet | | `main` (docs) | N/A | Pendiente |

1 solo Worker de código (Victor decide en el Gate 1 si quiere más; las observaciones son chicas y comparten pocos archivos, no conviene paralelizar).

## Archivos / componentes afectados

- Migraciones nuevas (`py_control_proyectos_web/db/`): catálogo del checklist (insert + rename + delete + orden) y áreas PR→JF. Rangos: `087` (catálogo) y `088` (áreas), y actualizar `db/README.md`.
- `src/components/ui/SelectorUsuario.tsx`, `src/lib/usuarios/lista-usuarios.ts` (O1).
- `src/app/(workspace)/proyectos/[id]/checklist/editar/editor-checklist.tsx` (O1, O3).
- `src/lib/checklist/checklist.ts` (O3: completar por check).
- `src/lib/config/registro-accesos.ts` (O3: "Personal NUEVO").
- `src/app/api/cronograma/route.ts`, `src/lib/errores/traducir-error.ts` (O4: logging + mensaje + fix).
- `src/components/ui/FormularioCronograma.tsx` (O4: superficie del error).

## Punch List embebida

Formato `05-punch-list.md`. Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. Evidencia en el archivo homónimo.

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| A1 | A | Migración `087`: catálogo — insertar `cronograma`, `paquete_trabajo`, `plan_maestro`; renombrar `recursos_sin_costo`→"Recursos del servicio", `personal_requerido`→"Listado de personal nuevo", `pets`→"Listado de pets"; eliminar AL_INICIO no listados (incl. `materiales_con_costo`); fijar `orden` 1–13. Idempotente. | SQL + lectura crítica | Sin verificar |
| A2 | A | Migración `088`: `areas` `PR`/`Proyecto` → `JF`/`Jefatura`, conservando `perfiles.area_id`. Idempotente. | SQL + lectura crítica | Sin verificar |
| A3 | A | `db/README.md` lista las migraciones `087` y `088` en orden. | Diff | Sin verificar |
| B1 | B | `lista-usuarios.ts`: ordenar por rol (prioridad `PRIORIDAD_ROL_PRINCIPAL`) y luego nombre; expone el orden en `etiquetaSelector`. | Prueba unitaria + `tsc` | Sin verificar |
| B2 | B | `SelectorUsuario.tsx`: quitar `filtrarPorRolClave` (o dejar de usarlo); listar todos los usuarios ordenados por rol. | `tsc` + build | Sin verificar |
| B3 | B | `editor-checklist.tsx`: no filtrar por rol; todo ítem de catálogo y personalizado muestra desplegable de responsable con todos los usuarios. | `tsc` + build | Sin verificar |
| B4 | B | `checklist.ts`: `documentoCompleto` completa por check manual (archivo presente) para todos, incluidos DP/PR; revisar consumidores de `checklistCompleto`/`documentosPendientes` (pantalla del proyecto, indicador de avance). | Prueba unitaria + grep de consumidores | Sin verificar |
| B5 | B | `registro-accesos.ts`: "Personal NUEVO" → "Listado de personal nuevo". | Diff | Sin verificar |
| C1 | C | `api/cronograma/route.ts`: loguear el error de lectura/parseo en servidor con contexto (mensaje, nombre de archivo, formato) — patrón `console.error` existente. | Lectura crítica + build | Sin verificar |
| C2 | C | Restaurar el mensaje de error específico al usuario (`traducirErrorApi` / `respuestaErrorInesperado` / `FormularioCronograma`). | Smoke de API con fallo forzado | Sin verificar |
| C3 | C | Reproducir con los archivos de prueba y **corregir** el error de lectura/parseo (Excel plantilla y PDF de MS Project). | Smoke de API con importación exitosa | Sin verificar |
| D1 | D | Documentación: flujos `12-checklist.md`, `02-usuarios.md` (y `15-cronograma.md` si aplica) según la tabla del Gate 1; índices de `04-flujos-de-negocio/` y `01-planes/`. | Diff + casilla "aplicado" | Sin verificar |
| D2 | D | Trasladar hallazgos del libro (mejoras/reglas/huérfanos) a su destino; `scripts/verificar-referencias.py` sin rotos. | Salida del verificador | Sin verificar |

## Riesgos y bloqueos

| # | Riesgo | Mitigación |
|---|---|---|
| R1 | Causa raíz del error de cronograma (C3) no identificada aún | C1 loguea el detalle; C2 restaura el mensaje; C3 reproduce con los archivos de prueba antes de corregir |
| R2 | Pasar DP/PR a check manual rompe el indicador "checklist completo" | B4 revisa todos los consumidores de `checklistCompleto`/`documentosPendientes` |
| R3 | Eliminar `materiales_con_costo` deja `proyecto_documentos` huérfanos | La migración `087` preserva o limpia las filas existentes (ver consulta Gate 1, G1-3) |

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-02 | Gate Spec aprobado | Victor |
| 2026-10-02 | Todos los ítems del checklist: casilla + responsable; completar por check | Victor |
| 2026-10-02 | Área PR → JF "Jefatura" | Victor |
| 2026-10-02 | O4: loguear el error y corregirlo (no solo el mensaje) | Victor |

## Enlaces a progreso y evidencia homónimos

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-10-02-observaciones-victor.md`
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-02-observaciones-victor.md`
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-10-02-observaciones-victor.md`

## Libro de hallazgos

Los cuatro apartados siguientes son el libro oficial. Formato de fila: `| ID | Fecha | Quién | Qué | Destino | Estado | Enlace |`. Estados: `Registrada` → `Trasladada` · `Descartada` · `Pendiente de decisión`.

### Mejoras (de trabajo)

Ninguna.

### Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién | Qué | Destino | Estado |
|---|---|---|---|---|---|
| RB1 | 2026-10-02 | Victor | Catálogo definitivo del checklist (13 ítems, orden, responsables, completar por check) | `04-flujos-de-negocio/12-checklist.md` | `Registrada` |
| RB2 | 2026-10-02 | Victor | Área `JF` = "Jefatura" (reemplaza `PR`/"Proyecto") | `04-flujos-de-negocio/02-usuarios.md` | `Registrada` |

### Observaciones sobre la política

Ninguna.

### Carpetas/archivos huérfanos

Ninguna.

## Gate 1 — consultas al Responsable humano

### G1-1 · Datos de prueba

¿Confirmas usar los archivos de prueba `docs/06-material-de-apoyo/Informacion para pruebas/CRON-PROMCOSER-AESA-001.pdf` y `Cron-prueba N°01.xlsx` para reproducir el error del cronograma (C3)? ¿Hay algún otro archivo con el que hayas visto fallar?

### G1-2 · Pre-autorizaciones

El smoke de API requiere una sesión (login) contra el dev local. Autorizas: (a) correr `npm run dev` local; (b) usar credenciales de prueba para el login del smoke (sin mostrar credenciales); (c) leer `.env.local` para los scripts. Nada de esto lee ni muestra secretos.

### G1-3 · Cambios a flujos de negocio (tabla)

| Flujo | Qué dice hoy | Qué pasaría a decir |
|---|---|---|
| `12-checklist.md` | Catálogo actual (12 ítems con "Materiales con costo"); DP/PR auto-completados; responsable por rol | Catálogo de 13 ítems en orden; todos con casilla y responsable; completar por check manual |
| `02-usuarios.md` | Áreas con código `PR` = "Proyecto" | Área `JF` = "Jefatura" (se elimina `PR`) |

Aprobación de esta tabla cubre a todos los Workers (la aplica el Documentador en D1).

### G1-4 · Número de Workers y rama

Propongo **1 Worker** en la rama reusada `local-worker-1`. ¿OK, o prefieres otra rama/más Workers?

## Informe de Auditoría

Enlace al archivo homónimo en `04-auditoria/` (se crea al auditar).

## Mensaje de cierre

Formato `09-cierre.md` (se escribe tras el Gate 2).

## Elementos postergados propuestos para planes futuros

- Generación automática de "Recursos del servicio" desde los datos del DP.
- Revisión del estado de las ramas `local-worker-2..4` (atrás de `main`): limpiarlas cuando Victor lo pida.
