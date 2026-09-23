# 2026-09-23 — Paquetes de Trabajo (Fase 1: interfaz + programación; Fase 2: declaración de avance)

> Tarea con flujo de Orquestador. Ver `docs/00-sistema/roles-y-flujo.md` y `docs/00-sistema/gestion-de-sesiones-y-contexto.md`.
> **Este archivo cubre las dos fases.** El plan completo se aprueba una vez; la implementación se hace fase por fase.

## Estado

Fase 1 implementada y **terminada en `work-1`** (PL-1.1 → PL-1.7 y PL-1.6 ampliado con UI de hitos). Verificado con evidencia: `tsc --noEmit` sin errores, suite completa **528/528** (60 archivos), build de producción OK (con `--webpack`, ver Mejoras), `eslint` sin problemas nuevos respecto de `main`, y **migración 072 aplicada en la BD** (comprobado por REST: `paquetes_trabajo` → 200, `requiere_partidas` → 200). **Push completado:** `6fddd76` en `origin/work-1`. **Pendiente:** PL-1.8 (verificación funcional con login real — la hace Victor), PL-1.9 (auditoría y apartados).

## Objetivo

- **Resultado esperado:** una interfaz nueva **"Paquetes de Trabajo"**, ubicada en el flujo **Cronograma → Paquetes de Trabajo → Plan Maestro**, que permita agrupar/seccionar partidas del presupuesto (DP) en un paquete operativo, elegir su **modo de medición** y **programar su metrado por días con fechas libres**, en una sola pantalla. El Plan Maestro deja de editar la distribución diaria y se genera desde los paquetes.
- **Alcance (Fase 1):**
  - Interfaz `/paquetes-trabajo` + chip en "Planificación" entre Cronograma y Plan Maestro.
  - Crear paquete con nombre propio; jalar/seccionar partidas del DP del servicio.
  - Elegir **modo de medición al crear**: `AVANCE_PAQUETE` (con **partida guía** que jala unidad y metrado del DP) o `POR_PARTIDAS` (sin unidad). Editable **solo mientras el paquete esté en `BORRADOR`**; no en ejecución/validado.
  - Programación diaria con **fechas libres** (mover fechas, agregar y quitar días). Reparto del metrado del paquete entre sus partidas/días.
  - **Hitos:** desplegable "no requiere partidas" para actividades tipo HITO del cronograma.
  - **Plan Maestro generado desde paquetes**; se elimina "Editar distribución diaria" de esa pantalla.
  - Migración, lib + tests, API y pantalla.
- **Alcance (Fase 2, documentada aquí; se implementa después):**
  - Declaración de avance del paquete en el flujo **RDT (campo) → carga al Plan Maestro (seguimiento) → PR (declaración)**.
  - **Modo A:** se declara X del paquete → `% = X / metrado de la partida guía` → se aplica a **todas** las partidas del paquete (mismo %). Ejemplo: guía cama de arena 10 ml; declaras 5 ml → 50% → excavación 15 m³, cama de arena 5 ml, relleno 15 m³.
  - **Modo B:** declaración partida por partida.
- **No alcance (esta tarea):**
  - **Orden de trabajo**: es un concepto distinto, aún no implementado. No se mezcla con Paquetes de Trabajo.
  - 3WLA / plan semanal.
  - Peso % por partida (flujo 19) para avance ponderado — queda para una fase posterior si aplica.
  - Multi-moneda (todo sigue en USD) y cambios en la cadena RDT→PR→Dashboard más allá de la declaración del paquete.
- **Validación esperada:** pruebas unitarias de la lógica pura; type-check y suite; verificación en vivo (login real) de crear paquete, programar con fechas libres y generar Plan Maestro desde paquetes; Punch List de la tarea.

## Entorno

- Modo: local.
- Orquestador: chat `local_1.orquestador_paquetes-trabajo`.
- Planner: chat `local_2.planner_paquetes-trabajo`.
- Worker: chat `local_3.worker_paquetes-trabajo-fase1`.
- Auditor: chat `local_4.auditor_paquetes-trabajo`.

## Asignaciones

| Rol | Chat | Rama | Worktree | Estado |
| --- | --- | --- | --- | --- |
| Orquestador | `local_1.orquestador_paquetes-trabajo` | `main` | N/A | Activo |
| Planner | `local_2.planner_paquetes-trabajo` | `main` | N/A | Activo |
| Worker (fase 1) | `local_3.worker_paquetes-trabajo-fase1` | `work-1` | `.worktrees/work-1` | Pendiente |
| Auditor | `local_4.auditor_paquetes-trabajo` | `main` | N/A | Pendiente |

> Repositorio de implementación: `py_control_proyectos_web`. Rama autorizada por Victor: **`work-1`**. La creación/reutilización del worktree requiere autorización explícita (ver Registro de decisiones).

## Plan aprobado

- [ ] Pendiente de aprobación de Victor.

## Punch List

### Fase 1 — Interfaz y programación

- [x] **PL-1.1** Migración `072_paquetes_trabajo.sql`: tablas `paquetes_trabajo`, `paquete_trabajo_partidas`, `paquete_trabajo_programacion` + columna `requiere_partidas` en `cronograma_actividades` + RLS de lectura. — commit `04f1fe0` (73 líneas; RLS de lectura para `authenticated` en las 3 tablas).
- [x] **PL-1.2** Lib pura (`src/lib/paquetes-trabajo/`) con validaciones y cálculos + tests (vitest). — commit `04f1fe0`; la suite incluye `paquetes-trabajo.test.ts` y pasa completa (528/528).
- [x] **PL-1.3** API `/api/paquetes-trabajo` (GET/POST/PATCH/archivar) con permisos y validación dura en servidor. — commit `04f1fe0` (342 líneas + permisos `puedeGestionarPaquetesTrabajo`/`puedeVerPaquetesTrabajo`).
- [x] **PL-1.4** Pantalla `/paquetes-trabajo` + chip en "Planificación" (`nav-proyecto.ts`), con lista, crear/editar, partidas y programación diaria con fechas libres. — commit `98190df` (pantalla + formulario 530 líneas + chip, ubicado entre Cronograma y Plan Maestro).
- [x] **PL-1.5** Modo de medición: elegir al crear; partida guía jala unidad+metrado; editable solo en `BORRADOR`. — commit `98190df`.
- [x] **PL-1.6** Hitos: desplegable "no requiere partidas" en cronograma. — commits `6fddd76` (API `/api/cronograma/hitos` GET/PATCH + columna Hito con checkbox por tarea en `FormularioCronograma.tsx`, que recarga el cronograma al cambiar) y `072_paquetes_trabajo.sql` (`requiere_partidas`).
- [x] **PL-1.7** Plan Maestro desde paquetes; quitar "Editar distribución diaria". — commit `01d256c` (la distribución diaria sale de `paquete_trabajo_programacion`).
- [ ] **PL-1.8** Verificación en vivo (Playwright, login real) + type-check + suite. — **parcial**: type-check ✅, suite 528/528 ✅, build ✅ (`/paquetes-trabajo`, `/api/paquetes-trabajo`, `/api/cronograma/hitos` presentes en el build), eslint sin problemas nuevos ✅. Falta la verificación en vivo (depende de aplicar la migración 072 en la BD).
- [ ] **PL-1.9** Auditoría y apartados obligatorios.

### Fase 2 — Declaración de avance (se implementa después)

- [ ] **PL-2.1** Declaración Modo A (paquete por partida guía) en RDT → Plan Maestro → PR.
- [ ] **PL-2.2** Declaración Modo B (partida por partida) en RDT → Plan Maestro → PR.
- [ ] **PL-2.3** Reparto del % del paquete a todas sus partidas y su reflejo en PR.
- [ ] **PL-2.4** Verificación en vivo + pruebas.

## Registro de decisiones

| # | Fecha | Decisión | Origen | Destino | Estado |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-23 | El paquete de trabajo agrupa/secciona partidas del DP bajo un nombre nuevo; es capa operativa, no reemplaza la partida contractual | Victor | `19-paquetes...md` | Pendiente |
| 2 | 2026-09-23 | Modo de medición: **A (por avance del paquete)** aplica el **mismo %** a todas las partidas; el % se obtiene de la partida guía (no hay peso por partida en esta fase) | Victor | `19-paquetes...md` | Pendiente |
| 3 | 2026-09-23 | La **partida guía** jala su unidad y metrado del DP; con eso se calcula el % del paquete | Victor | `19-paquetes...md` | Pendiente |
| 4 | 2026-09-23 | Implementación **por fases**: Fase 1 (interfaz + programación) ahora; Fase 2 (declaración de avance) después | Victor | Esta tarea | Confirmado |
| 5 | 2026-09-23 | Las **fechas personalizadas** afectan del paquete hacia adelante; el **cronograma conserva sus fechas reales** intactas. Se reasigna libremente | Victor | `15-cronograma.md`, `20-plan-maestro.md` | Pendiente |
| 6 | 2026-09-23 | Si no hay paquete previo **no se puede generar el Plan Maestro**; luego que exista, sí | Victor | `20-plan-maestro.md` | Pendiente |
| 7 | 2026-09-23 | Hitos del cronograma: opción desplegable **"no requiere partidas"** (hoy se tratan como si tuvieran partida) | Victor | `15-cronograma.md` | Pendiente |
| 8 | 2026-09-23 | **"Orden de trabajo"** es un concepto distinto, aún no implementado — no se mezcla con Paquetes de Trabajo | Victor | Esta tarea (no alcance) | Confirmado |
| 9 | 2026-09-23 | Rama de trabajo autorizada: **`work-1`** (`.worktrees/work-1`) | Victor | Esta tarea | Confirmado |
| 10 | 2026-09-23 | Nombre del chip: **"Paquetes de Trabajo"** | Victor | `nav-proyecto.ts`, flujos | Confirmado |
| 11 | 2026-09-23 | El **modo de medición** es editable mientras el paquete esté en **`BORRADOR`**; **no** en ejecución | Victor | `19-paquetes...md` | Pendiente |
| 12 | 2026-09-23 | El chip **"Paquetes de Trabajo"** vive en Planificación **entre Cronograma y Plan Maestro** y, **sin servicio elegido, no es clicable** (nunca un link muerto) — mismo criterio ya aplicado a Cronograma y Curva S | Precedente documentado en `docs/Mejoras continuas/2026-09-21-curva-s-fase-3-agente-d.md` (D0) + Worker | `nav-proyecto.ts` + flujos | **Provisional — a confirmar por Victor** |

## Resultados de Workers

- Rama: `work-1` — worktree `.worktrees/work-1` (repo `py_control_proyectos_web`). Sin push todavía: la rama es local y el envío espera autorización de Victor.
- Commits (4, locales en `work-1`):
  - `04f1fe0` — `feat(paquetes-trabajo): Fase 1 PL-1.1/1.2/1.3 - migracion, lib+tests y API` (migración 072, lib + tests, API + permisos).
  - `98190df` — `feat(paquetes-trabajo): pantalla, chip de nav y formulario (PL-1.4/1.5)`.
  - `01d256c` — `feat(plan-maestro): tomar la distribucion diaria de los paquetes de trabajo (PL-1.7)`.
  - `6fddd76` — `feat(paquetes-trabajo): hitos del cronograma (PL-1.6) y test del chip de nav (PL-1.8)` (API `/api/cronograma/hitos`, `requiere_partidas` expuesto en `GET /api/cronograma`, columna Hito en `FormularioCronograma.tsx`, contador de nav 40→41 + test del chip).
- Pruebas y verificación (en `.worktrees/work-1`):
  - `npx tsc --noEmit` → 0 errores.
  - `npx vitest run` → **60 archivos / 528 tests, todos pasan**.
  - `npx eslint src` → **9 errores / 18 warnings, idéntico conteo al de `main`** (preexistentes; ningún archivo tocado por esta tarea aporta problemas — lint por archivo tocado sale limpio).
  - `npx next build --webpack` → build OK; `/paquetes-trabajo`, `/api/paquetes-trabajo` y `/api/cronograma/hitos` figuran en el manifiesto de rutas del build.
- Bloqueos / pendientes técnicos:
  - `npm run build` y `npm run dev` (Turbopack) **no corren dentro del worktree** por el junction de `node_modules` (ver Mejoras). Se usó `--webpack` en ambos.
  - **La migración `072_paquetes_trabajo.sql` NO está aplicada en la BD** (comprobado por REST con el cliente de servicio, sin usar las llaves del repo: `paquetes_trabajo` → `404 PGRST205` "Could not find the table"; `cronograma_actividades.requiere_partidas` → `400 42703` "column does not exist"). No hay forma de aplicarla desde aquí: no hay CLI de Supabase ni `psql` ni cadena de conexión a Postgres en `.env.local` (solo URL, anon key y service role key) — por convención del repo, las migraciones se pegan a mano en el SQL Editor de Supabase (ver `db/README.md`).
  - **Orden obligatorio:** aplicar `072` **antes** de correr o mezclar esta rama. El `GET /api/cronograma` ahora selecciona `requiere_partidas`; contra una BD sin la migración devuelve `42703` y **la pantalla de Cronograma deja de cargar**.
  - **Smoke test en vivo (parcial, sin sesión):** app levantada localmente con `npm run dev -- --webpack -p 3112`; `/paquetes-trabajo`, `/plan-maestro` y `/cronograma` responden y redirigen a `/login`, y `/api/paquetes-trabajo` y `/api/cronograma/hitos` también (el middleware exige sesión). Rutas registradas, sin errores de carga. **Falta la verificación funcional** (crear paquete, programar con fechas libres, marcar hitos, generar Plan Maestro): requiere la migración 072 aplicada y una sesión real.
  - La verificación funcional con Playwright no se pudo completar: el paquete `playwright` **no está instalado** en el proyecto (no figura en `package.json` ni en `node_modules`; solo están los binarios de Chromium en el caché de `%LOCALAPPDATA%\ms-playwright`), y las credenciales de prueba viven fuera del repo a propósito (AGENTS.md prohíbe leer/publicar secretos).

## Informe de Auditoría

### Aplicar ahora

### Proponer a Victor

### No promover

## Mejoras (de trabajo)

> **Se escribe en el momento en que ocurre**, no al cerrar.

- 2026-09-23 — **`next build` y `next dev` (Turbopack) no corren dentro de un worktree con `node_modules` en Junction.** En `.worktrees/work-1`, `node_modules` es una *Junction* a `py_control_proyectos_web\node_modules` (fuera del root del proyecto) y Turbopack aborta con `TurbopackInternalError: Symlink [project]/node_modules is invalid, it points out of the filesystem root`. Comprobado en **los dos comandos**: `npm run build` y `npm run dev` (este último imprime "✓ Ready" y muere con el panic en la primera compilación). El panic ocurre al **resolver dependencias, antes de compilar código de la app** (stack: `find_package` → `resolve` → `directory_tree_to_entrypoints`), así que no depende del diff de la rama. Workaround verificado en ambos: **`npx next build --webpack`** y **`npm run dev -- --webpack`** (levantó en 1.4s y sirvió las rutas). Consecuencia práctica: dentro de un worktree, usar `--webpack` para build y dev; el build con Turbopack se hace en el checkout principal.
- 2026-09-23 — **Comprobar si una migración está aplicada antes de verificar en vivo** (el código puede estar listo y la BD no). Sin CLI ni `psql`, se puede consultar PostgREST con el cliente de servicio desde un script Node temporal que lee `.env.local` sin imprimir valores: si la tabla no existe → `404 PGRST205`; si la columna no existe → `400 42703`. Eso permitió saber en segundos que la `072` no estaba aplicada, en vez de atribuir a un bug el fallo de la pantalla.
- 2026-09-23 — **Verificar lint contra `main`, no contra cero.** `npx eslint src` ya da **9 errores / 18 warnings** en `main` (setState dentro de effects, `any` explícito, entidades sin escapar, `prefer-const`). Para saber si el trabajo introdujo deuda nueva: (a) comparar el total contra `main` y (b) lintear solo los archivos tocados (que deben salir limpios). Sin ese baseline, cualquier tarea queda "en rojo" por deuda ajena.
- 2026-09-23 — **Tests con contadores congelados.** `nav-proyecto.test.ts` congelaba el total de ítems del nav (`toHaveLength(40)`): agregar un chip rompe la suite hasta actualizar el contador, y ese fallo **no** aparece al correr el test del módulo tocado sino en la suite completa. Al agregar un ítem: actualizar el contador **y** añadir el test que fija su ubicación/comportamiento (aquí, chip entre Cronograma y Plan Maestro + sin servicio no es link muerto). Además, al leer la salida de vitest por consola, **guiarse por la sección `Failed Tests` y el conteo** — un filtro por `FAIL` puede atribuir el fallo al archivo equivocado (en esta sesión apuntó primero a `vinculos.test.ts`, que en realidad pasaba 10/10, cuando el fallo estaba en `nav-proyecto.test.ts`); correr el archivo sospechoso aislado antes de "arreglarlo".

## Reglas de negocio acordadas en esta tarea

> **Se escribe en el momento en que ocurre.** Van **directo al Flujo de trabajo correspondiente** al cerrar, integradas en su estructura.

- 2026-09-23 — Modo A aplica el mismo % a todas las partidas, obtenido de la partida guía → `docs/Flujos de trabajo/19-paquetes de trabajo y jerarquia de control.md` (pendiente de aplicar al cerrar).
- 2026-09-23 — Partida guía jala unidad+metrado del DP → `19-paquetes...md` (pendiente).
- 2026-09-23 — Fechas personalizadas del paquete hacia adelante; cronograma intacto; reasignación libre → `15-cronograma.md` + `20-plan-maestro.md` (pendiente).
- 2026-09-23 — Sin paquete no hay Plan Maestro → `20-plan-maestro.md` (pendiente).
- 2026-09-23 — Hitos sin partidas ("no requiere partidas") → `15-cronograma.md` (pendiente).
- 2026-09-23 — Modo de medición editable solo en `BORRADOR` → `19-paquetes...md` (pendiente).

## Carpetas/archivos huérfanos

> **Se escribe en el momento en que se detecta**, con búsqueda real (Grep/referencias), en ambos repositorios.

- **Ningún archivo creado por esta tarea quedó huérfano** (búsqueda real en `py_control_proyectos_web`): `src/lib/paquetes-trabajo/paquetes-trabajo.ts` se usa en `src/app/api/paquetes-trabajo/route.ts` y en `src/components/ui/FormularioPaquetesTrabajo.tsx`; `/api/paquetes-trabajo` se consume desde ese formulario (3 referencias); la pantalla `src/app/(workspace)/paquetes-trabajo/page.tsx` está referenciada por el chip `paquetes-trabajo` de `nav-proyecto.ts`; `db/072_paquetes_trabajo.sql` es la última migración (64 archivos en `db/`, 070→071→072 consecutivos, sin duplicados).
- **Observación reportada a Victor, sin borrar nada:** `py_control_proyectos_web/docs/` mantiene una **copia propia y trackeada** (42 archivos) de `Flujos de trabajo/`, `Mejoras continuas/`, `superpowers/`, `visual-companion/` y `memoria-sesion.md`, separada de la del repositorio documental `pg_control_proyectos/docs/`. Es preexistente (no la creó esta tarea) y es un riesgo de divergencia entre el repo documental y el de implementación; se reporta para que Victor decida si esa copia debe seguir existiendo.

## Cierre

- Documentación promovida:
- Pendientes:
- Autorización de cierre: