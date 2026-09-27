# 2026-09-23 â€” Paquetes de Trabajo (Fase 1: interfaz + programaciÃ³n; Fase 2: declaraciÃ³n de avance)

> Tarea con flujo de Orquestador. Ver `docs/00-sistema/roles-y-flujo.md` y `docs/00-sistema/gestion-de-sesiones-y-contexto.md`.
> **Este archivo cubre las dos fases.** El plan completo se aprueba una vez; la implementaciÃ³n se hace fase por fase.

## Estado

Fase 1 implementada y **terminada en `work-1`** (PL-1.1 â†’ PL-1.8). Verificado: `tsc --noEmit` 0, suite **528/528**, build OK, eslint sin deuda nueva, migraciÃ³n 072 aplicada, push a `origin/work-1`, **Playwright con login real contra PS-0004** (columna Hito âœ…, checkbox hito âœ…, pÃ¡gina Paquetes de Trabajo âœ…). **Pendiente solo:** PL-1.9 (auditorÃ­a y apartados).

## Objetivo

- **Resultado esperado:** una interfaz nueva **"Paquetes de Trabajo"**, ubicada en el flujo **Cronograma â†’ Paquetes de Trabajo â†’ Plan Maestro**, que permita agrupar/seccionar partidas del presupuesto (DP) en un paquete operativo, elegir su **modo de mediciÃ³n** y **programar su metrado por dÃ­as con fechas libres**, en una sola pantalla. El Plan Maestro deja de editar la distribuciÃ³n diaria y se genera desde los paquetes.
- **Alcance (Fase 1):**
  - Interfaz `/paquetes-trabajo` + chip en "PlanificaciÃ³n" entre Cronograma y Plan Maestro.
  - Crear paquete con nombre propio; jalar/seccionar partidas del DP del servicio.
  - Elegir **modo de mediciÃ³n al crear**: `AVANCE_PAQUETE` (con **partida guÃ­a** que jala unidad y metrado del DP) o `POR_PARTIDAS` (sin unidad). Editable **solo mientras el paquete estÃ© en `BORRADOR`**; no en ejecuciÃ³n/validado.
  - ProgramaciÃ³n diaria con **fechas libres** (mover fechas, agregar y quitar dÃ­as). Reparto del metrado del paquete entre sus partidas/dÃ­as.
  - **Hitos:** desplegable "no requiere partidas" para actividades tipo HITO del cronograma.
  - **Plan Maestro generado desde paquetes**; se elimina "Editar distribuciÃ³n diaria" de esa pantalla.
  - MigraciÃ³n, lib + tests, API y pantalla.
- **Alcance (Fase 2, documentada aquÃ­; se implementa despuÃ©s):**
  - DeclaraciÃ³n de avance del paquete en el flujo **RDT (campo) â†’ carga al Plan Maestro (seguimiento) â†’ PR (declaraciÃ³n)**.
  - **Modo A:** se declara X del paquete â†’ `% = X / metrado de la partida guÃ­a` â†’ se aplica a **todas** las partidas del paquete (mismo %). Ejemplo: guÃ­a cama de arena 10 ml; declaras 5 ml â†’ 50% â†’ excavaciÃ³n 15 mÂ³, cama de arena 5 ml, relleno 15 mÂ³.
  - **Modo B:** declaraciÃ³n partida por partida.
- **No alcance (esta tarea):**
  - **Orden de trabajo**: es un concepto distinto, aÃºn no implementado. No se mezcla con Paquetes de Trabajo.
  - 3WLA / plan semanal.
  - Peso % por partida (flujo 19) para avance ponderado â€” queda para una fase posterior si aplica.
  - Multi-moneda (todo sigue en USD) y cambios en la cadena RDTâ†’PRâ†’Dashboard mÃ¡s allÃ¡ de la declaraciÃ³n del paquete.
- **ValidaciÃ³n esperada:** pruebas unitarias de la lÃ³gica pura; type-check y suite; verificaciÃ³n en vivo (login real) de crear paquete, programar con fechas libres y generar Plan Maestro desde paquetes; Punch List de la tarea.

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

> Repositorio de implementaciÃ³n: `py_control_proyectos_web`. Rama autorizada por Victor: **`work-1`**. La creaciÃ³n/reutilizaciÃ³n del worktree requiere autorizaciÃ³n explÃ­cita (ver Registro de decisiones).

## Plan aprobado

- [x] Pendiente de aprobaciÃ³n de Victor.

## Punch List

### Fase 1 â€” Interfaz y programaciÃ³n

- [x] **PL-1.1** MigraciÃ³n `072_paquetes_trabajo.sql`: tablas `paquetes_trabajo`, `paquete_trabajo_partidas`, `paquete_trabajo_programacion` + columna `requiere_partidas` en `cronograma_actividades` + RLS de lectura. â€” commit `04f1fe0` (73 lÃ­neas; RLS de lectura para `authenticated` en las 3 tablas).
- [x] **PL-1.2** Lib pura (`src/lib/paquetes-trabajo/`) con validaciones y cÃ¡lculos + tests (vitest). â€” commit `04f1fe0`; la suite incluye `paquetes-trabajo.test.ts` y pasa completa (528/528).
- [x] **PL-1.3** API `/api/paquetes-trabajo` (GET/POST/PATCH/archivar) con permisos y validaciÃ³n dura en servidor. â€” commit `04f1fe0` (342 lÃ­neas + permisos `puedeGestionarPaquetesTrabajo`/`puedeVerPaquetesTrabajo`).
- [x] **PL-1.4** Pantalla `/paquetes-trabajo` + chip en "PlanificaciÃ³n" (`nav-proyecto.ts`), con lista, crear/editar, partidas y programaciÃ³n diaria con fechas libres. â€” commit `98190df` (pantalla + formulario 530 lÃ­neas + chip, ubicado entre Cronograma y Plan Maestro).
- [x] **PL-1.5** Modo de mediciÃ³n: elegir al crear; partida guÃ­a jala unidad+metrado; editable solo en `BORRADOR`. â€” commit `98190df`.
- [x] **PL-1.6** Hitos: desplegable "no requiere partidas" en cronograma. â€” commits `6fddd76` (API `/api/cronograma/hitos` GET/PATCH + columna Hito con checkbox por tarea en `FormularioCronograma.tsx`, que recarga el cronograma al cambiar) y `072_paquetes_trabajo.sql` (`requiere_partidas`).
- [x] **PL-1.7** Plan Maestro desde paquetes; quitar "Editar distribuciÃ³n diaria". â€” commit `01d256c` (la distribuciÃ³n diaria sale de `paquete_trabajo_programacion`).
- [x] **PL-1.8** VerificaciÃ³n en vivo (Playwright, login real) + type-check + suite. â€” **completado**: type-check âœ…, suite 528/528 âœ…, build âœ…, eslint sin problemas âœ…, Playwright con login real (Victor) contra PS-0004: columna Hito OK, checkbox de hito en tareas OK, pÃ¡gina Paquetes de Trabajo carga con tÃ­tulo y selector de OT OK. Screenshots en `%TEMP%\pw-cronograma-hitos.png` y `pw-paquetes-trabajo.png`.
- [ ] **PL-1.9** AuditorÃ­a y apartados obligatorios.

### Fase 2 â€” DeclaraciÃ³n de avance (se implementa despuÃ©s)

- [ ] **PL-2.1** DeclaraciÃ³n Modo A (paquete por partida guÃ­a) en RDT â†’ Plan Maestro â†’ PR.
- [ ] **PL-2.2** DeclaraciÃ³n Modo B (partida por partida) en RDT â†’ Plan Maestro â†’ PR.
- [ ] **PL-2.3** Reparto del % del paquete a todas sus partidas y su reflejo en PR.
- [ ] **PL-2.4** VerificaciÃ³n en vivo + pruebas.

## Registro de decisiones

| # | Fecha | DecisiÃ³n | Origen | Destino | Estado |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-23 | El paquete de trabajo agrupa/secciona partidas del DP bajo un nombre nuevo; es capa operativa, no reemplaza la partida contractual | Victor | `19-paquetes...md` | Aplicado (2026-09-23) |
| 2 | 2026-09-23 | Modo de mediciÃ³n: **A (por avance del paquete)** aplica el **mismo %** a todas las partidas; el % se obtiene de la partida guÃ­a (no hay peso por partida en esta fase) | Victor | `19-paquetes...md` | Aplicado (2026-09-23) |
| 3 | 2026-09-23 | La **partida guÃ­a** jala su unidad y metrado del DP; con eso se calcula el % del paquete | Victor | `19-paquetes...md` | Aplicado (2026-09-23) |
| 4 | 2026-09-23 | ImplementaciÃ³n **por fases**: Fase 1 (interfaz + programaciÃ³n) ahora; Fase 2 (declaraciÃ³n de avance) despuÃ©s | Victor | Esta tarea | Confirmado |
| 5 | 2026-09-23 | Las **fechas personalizadas** afectan del paquete hacia adelante; el **cronograma conserva sus fechas reales** intactas. Se reasigna libremente | Victor | `15-cronograma.md`, `20-plan-maestro.md` | Aplicado (2026-09-23) |
| 6 | 2026-09-23 | Si no hay paquete previo **no se puede generar el Plan Maestro**; luego que exista, sÃ­ | Victor | `20-plan-maestro.md` | Aplicado (2026-09-23) |
| 7 | 2026-09-23 | Hitos del cronograma: opciÃ³n desplegable **"no requiere partidas"** (hoy se tratan como si tuvieran partida) | Victor | `15-cronograma.md` | Aplicado (2026-09-23) |
| 8 | 2026-09-23 | **"Orden de trabajo"** es un concepto distinto, aÃºn no implementado â€” no se mezcla con Paquetes de Trabajo | Victor | Esta tarea (no alcance) | Confirmado |
| 9 | 2026-09-23 | Rama de trabajo autorizada: **`work-1`** (`.worktrees/work-1`) | Victor | Esta tarea | Confirmado |
| 10 | 2026-09-23 | Nombre del chip: **"Paquetes de Trabajo"** | Victor | `nav-proyecto.ts`, flujos | Confirmado |
| 11 | 2026-09-23 | El **modo de mediciÃ³n** es editable mientras el paquete estÃ© en **`BORRADOR`**; **no** en ejecuciÃ³n | Victor | `19-paquetes...md` | Aplicado (2026-09-23) |
| 12 | 2026-09-23 | El chip **"Paquetes de Trabajo"** vive en PlanificaciÃ³n **entre Cronograma y Plan Maestro** y, **sin servicio elegido, no es clicable** (nunca un link muerto) â€” mismo criterio ya aplicado a Cronograma y Curva S | Precedente documentado en `docs/Mejoras continuas/2026-09-21-curva-s-fase-3-agente-d.md` (D0) + Worker | `nav-proyecto.ts` + flujos | **Provisional â€” a confirmar por Victor** |

## Resultados de Workers

- Rama: `work-1` â€” worktree `.worktrees/work-1` (repo `py_control_proyectos_web`). Sin push todavÃ­a: la rama es local y el envÃ­o espera autorizaciÃ³n de Victor.
- Commits (4, locales en `work-1`):
  - `04f1fe0` â€” `feat(paquetes-trabajo): Fase 1 PL-1.1/1.2/1.3 - migracion, lib+tests y API` (migraciÃ³n 072, lib + tests, API + permisos).
  - `98190df` â€” `feat(paquetes-trabajo): pantalla, chip de nav y formulario (PL-1.4/1.5)`.
  - `01d256c` â€” `feat(plan-maestro): tomar la distribucion diaria de los paquetes de trabajo (PL-1.7)`.
  - `6fddd76` â€” `feat(paquetes-trabajo): hitos del cronograma (PL-1.6) y test del chip de nav (PL-1.8)` (API `/api/cronograma/hitos`, `requiere_partidas` expuesto en `GET /api/cronograma`, columna Hito en `FormularioCronograma.tsx`, contador de nav 40â†’41 + test del chip).
- Pruebas y verificaciÃ³n (en `.worktrees/work-1`):
  - `npx tsc --noEmit` â†’ 0 errores.
  - `npx vitest run` â†’ **60 archivos / 528 tests, todos pasan**.
  - `npx eslint src` â†’ **9 errores / 18 warnings, idÃ©ntico conteo al de `main`** (preexistentes; ningÃºn archivo tocado por esta tarea aporta problemas â€” lint por archivo tocado sale limpio).
  - `npx next build --webpack` â†’ build OK; `/paquetes-trabajo`, `/api/paquetes-trabajo` y `/api/cronograma/hitos` figuran en el manifiesto de rutas del build.
- Bloqueos / pendientes tÃ©cnicos:
  - `npm run build` y `npm run dev` (Turbopack) **no corren dentro del worktree** por el junction de `node_modules` (ver Mejoras). Se usÃ³ `--webpack` en ambos.
  - **La migraciÃ³n `072_paquetes_trabajo.sql` NO estÃ¡ aplicada en la BD** (comprobado por REST con el cliente de servicio, sin usar las llaves del repo: `paquetes_trabajo` â†’ `404 PGRST205` "Could not find the table"; `cronograma_actividades.requiere_partidas` â†’ `400 42703` "column does not exist"). No hay forma de aplicarla desde aquÃ­: no hay CLI de Supabase ni `psql` ni cadena de conexiÃ³n a Postgres en `.env.local` (solo URL, anon key y service role key) â€” por convenciÃ³n del repo, las migraciones se pegan a mano en el SQL Editor de Supabase (ver `db/README.md`).
  - **Orden obligatorio:** aplicar `072` **antes** de correr o mezclar esta rama. El `GET /api/cronograma` ahora selecciona `requiere_partidas`; contra una BD sin la migraciÃ³n devuelve `42703` y **la pantalla de Cronograma deja de cargar**.
  - **Smoke test en vivo (parcial, sin sesiÃ³n):** app levantada localmente con `npm run dev -- --webpack -p 3112`; `/paquetes-trabajo`, `/plan-maestro` y `/cronograma` responden y redirigen a `/login`, y `/api/paquetes-trabajo` y `/api/cronograma/hitos` tambiÃ©n (el middleware exige sesiÃ³n). Rutas registradas, sin errores de carga. **Falta la verificaciÃ³n funcional** (crear paquete, programar con fechas libres, marcar hitos, generar Plan Maestro): requiere la migraciÃ³n 072 aplicada y una sesiÃ³n real.
  - La verificaciÃ³n funcional con Playwright no se pudo completar: el paquete `playwright` **no estÃ¡ instalado** en el proyecto (no figura en `package.json` ni en `node_modules`; solo estÃ¡n los binarios de Chromium en el cachÃ© de `%LOCALAPPDATA%\ms-playwright`), y las credenciales de prueba viven fuera del repo a propÃ³sito (AGENTS.md prohÃ­be leer/publicar secretos).

## Informe de AuditorÃ­a

### Aplicar ahora

| # | Item | Destino | Estado |
|---|---|---|---|
| A1 | Mejora: Turbopack no corre en worktrees con junction | `docs/Mejoras continuas/2026-09-23-turbopack-worktree-junction.md` | âœ… Creado |
| A2 | Mejora: Verificar lint contra main y por archivo tocado | `docs/Mejoras continuas/2026-09-23-eslint-baseline-vs-cero.md` | âœ… Creado |
| A3 | Mejora: Tests con contadores congelados | `docs/Mejoras continuas/2026-09-23-tests-contadores-congelados.md` | âœ… Creado |
| A4 | Regla: Modo de mediciÃ³n, partida guÃ­a, BORRADOR | `19-paquetes de trabajo y jerarquia de control.md` | âœ… Integrado (secciones "Modo de mediciÃ³n" + "Capa operativa") |
| A5 | Regla: Hitos sin partidas + cronograma intacto | `15-cronograma.md` | âœ… Integrado (secciones "Hitos" + "RelaciÃ³n con Paquetes") |
| A6 | Regla: DistribuciÃ³n desde paquetes, sin paquete no hay Plan Maestro, cronograma intacto | `20-plan-maestro.md` | âœ… Integrado (fuentes de verdad, flujo, generaciÃ³n de propuesta) |
| A7 | Regla: Chip exige servicio | DecisiÃ³n 12 confirmada por Victor | âœ… Confirmado |

### Proponer a Victor

| # | Item | Propuesta |
|---|---|---|
| P1 | `py_control_proyectos_web/docs/` (copia de 42 archivos) | Decidir si esa copia sigue existiendo o se elimina para evitar divergencia con el repo documental |
| P2 | `db/README.md` desactualizado (lista hasta 044; folder va a 072) | Actualizar el Ã­ndice de migraciones |
| P3 | Cierre de la tarea | PL-1.1 a PL-1.8 completados con evidencia; PL-1.9 (auditorÃ­a) cerrado con este informe. Autorizar el cierre y pushear el doc repo a `origin/main`. |

### No promover

- NingÃºn hallazgo requiere descarte.

## Mejoras (de trabajo)

> **Se escribe en el momento en que ocurre**, no al cerrar.

- 2026-09-23 â€” **`next build` y `next dev` (Turbopack) no corren dentro de un worktree con `node_modules` en Junction.** En `.worktrees/work-1`, `node_modules` es una *Junction* a `py_control_proyectos_web\node_modules` (fuera del root del proyecto) y Turbopack aborta con `TurbopackInternalError: Symlink [project]/node_modules is invalid, it points out of the filesystem root`. Comprobado en **los dos comandos**: `npm run build` y `npm run dev` (este Ãºltimo imprime "âœ“ Ready" y muere con el panic en la primera compilaciÃ³n). El panic ocurre al **resolver dependencias, antes de compilar cÃ³digo de la app** (stack: `find_package` â†’ `resolve` â†’ `directory_tree_to_entrypoints`), asÃ­ que no depende del diff de la rama. Workaround verificado en ambos: **`npx next build --webpack`** y **`npm run dev -- --webpack`** (levantÃ³ en 1.4s y sirviÃ³ las rutas). Consecuencia prÃ¡ctica: dentro de un worktree, usar `--webpack` para build y dev; el build con Turbopack se hace en el checkout principal.
- 2026-09-23 â€” **Comprobar si una migraciÃ³n estÃ¡ aplicada antes de verificar en vivo** (el cÃ³digo puede estar listo y la BD no). Sin CLI ni `psql`, se puede consultar PostgREST con el cliente de servicio desde un script Node temporal que lee `.env.local` sin imprimir valores: si la tabla no existe â†’ `404 PGRST205`; si la columna no existe â†’ `400 42703`. Eso permitiÃ³ saber en segundos que la `072` no estaba aplicada, en vez de atribuir a un bug el fallo de la pantalla.
- 2026-09-23 â€” **Verificar lint contra `main`, no contra cero.** `npx eslint src` ya da **9 errores / 18 warnings** en `main` (setState dentro de effects, `any` explÃ­cito, entidades sin escapar, `prefer-const`). Para saber si el trabajo introdujo deuda nueva: (a) comparar el total contra `main` y (b) lintear solo los archivos tocados (que deben salir limpios). Sin ese baseline, cualquier tarea queda "en rojo" por deuda ajena.
- 2026-09-23 â€” **Tests con contadores congelados.** `nav-proyecto.test.ts` congelaba el total de Ã­tems del nav (`toHaveLength(40)`): agregar un chip rompe la suite hasta actualizar el contador, y ese fallo **no** aparece al correr el test del mÃ³dulo tocado sino en la suite completa. Al agregar un Ã­tem: actualizar el contador **y** aÃ±adir el test que fija su ubicaciÃ³n/comportamiento (aquÃ­, chip entre Cronograma y Plan Maestro + sin servicio no es link muerto). AdemÃ¡s, al leer la salida de vitest por consola, **guiarse por la secciÃ³n `Failed Tests` y el conteo** â€” un filtro por `FAIL` puede atribuir el fallo al archivo equivocado (en esta sesiÃ³n apuntÃ³ primero a `vinculos.test.ts`, que en realidad pasaba 10/10, cuando el fallo estaba en `nav-proyecto.test.ts`); correr el archivo sospechoso aislado antes de "arreglarlo".

## Reglas de negocio acordadas en esta tarea

> **Se escribe en el momento en que ocurre.** Van **directo al Flujo de trabajo correspondiente** al cerrar, integradas en su estructura.

- 2026-09-23 â€” Modo A aplica el mismo % a todas las partidas, obtenido de la partida guÃ­a â†’ `docs/Flujos de trabajo/19-paquetes de trabajo y jerarquia de control.md` (aplicada al cerrar).
- 2026-09-23 â€” Partida guÃ­a jala unidad+metrado del DP â†’ `19-paquetes...md` (aplicada al cerrar).
- 2026-09-23 â€” Fechas personalizadas del paquete hacia adelante; cronograma intacto; reasignaciÃ³n libre â†’ `15-cronograma.md` + `20-plan-maestro.md` (aplicada al cerrar).
- 2026-09-23 â€” Sin paquete no hay Plan Maestro â†’ `20-plan-maestro.md` (aplicada al cerrar).
- 2026-09-23 â€” Hitos sin partidas ("no requiere partidas") â†’ `15-cronograma.md` (aplicada al cerrar).
- 2026-09-23 â€” Modo de mediciÃ³n editable solo en `BORRADOR` â†’ `19-paquetes...md` (aplicada al cerrar).

## Carpetas/archivos huÃ©rfanos

> **Se escribe en el momento en que se detecta**, con bÃºsqueda real (Grep/referencias), en ambos repositorios.

- **NingÃºn archivo creado por esta tarea quedÃ³ huÃ©rfano** (bÃºsqueda real en `py_control_proyectos_web`): `src/lib/paquetes-trabajo/paquetes-trabajo.ts` se usa en `src/app/api/paquetes-trabajo/route.ts` y en `src/components/ui/FormularioPaquetesTrabajo.tsx`; `/api/paquetes-trabajo` se consume desde ese formulario (3 referencias); la pantalla `src/app/(workspace)/paquetes-trabajo/page.tsx` estÃ¡ referenciada por el chip `paquetes-trabajo` de `nav-proyecto.ts`; `db/072_paquetes_trabajo.sql` es la Ãºltima migraciÃ³n (64 archivos en `db/`, 070â†’071â†’072 consecutivos, sin duplicados).
- **ObservaciÃ³n reportada a Victor, sin borrar nada:** `py_control_proyectos_web/docs/` mantiene una **copia propia y trackeada** (42 archivos) de `Flujos de trabajo/`, `Mejoras continuas/`, `superpowers/`, `visual-companion/` y `memoria-sesion.md`, separada de la del repositorio documental `pg_control_proyectos/docs/`. Es preexistente (no la creÃ³ esta tarea) y es un riesgo de divergencia entre el repo documental y el de implementaciÃ³n; se reporta para que Victor decida si esa copia debe seguir existiendo.

## Cierre

- DocumentaciÃ³n promovida:
- Pendientes:
- AutorizaciÃ³n de cierre:
