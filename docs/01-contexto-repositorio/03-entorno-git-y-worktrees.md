# Entorno, Git y worktrees

## Regla de los dos repos (según el plan y las convenciones aprobadas)

| Tipo de trabajo | Repositorio | Rama | Worktree |
|---|---|---|---|
| Documentación de proceso (Spec, plan, progreso, evidencia, hallazgos, informe de auditoría, fuentes de verdad, mensaje de cierre) | `pg_control_proyectos` | `main`, directo, sin rama ni merge | No se usa |
| Código de la app | `py_control_proyectos_web` | `<entorno>-worker-N` (ej. `local-worker-1`, `nube-worker-1`); nunca `main` hasta el merge tras el Gate 2 | `.worktrees/` de ese repo, subcarpeta con el mismo nombre de la rama |

- `entorno` es `local` o `nube`; se verifica con la herramienta disponible (`list_environments`), no se asume.
- La nomenclatura `work-1`/`work-2` está **obsoleta**. Solo se conserva como dato histórico en las tareas que la usaron.
- No se crea, borra, renombra o reasigna rama ni worktree sin autorización de Victor.
- Los roles de coordinación (Orquestador, Planner, Auditor) trabajan en `main` de `pg_control_proyectos`.

## Hallazgo verificado — el harness de sesiones en la nube no siempre respeta "main directo"

> Registrado por el Worker de la reestructuración documental (2026-09-27), verificado con `git branch --show-current` y `git log` de `origin/main` — no asumido. Pendiente de evaluación por el Auditor y el Orquestador; no se resuelve por cuenta propia del Worker.

La regla de arriba ("documentación de proceso → `main` directo, sin rama") es la aprobada en el plan y en `convenciones-de-trabajo.md`. En la práctica, al menos una sesión de Worker en la nube corrió en un contenedor cuyo harness:

- exige commitear y pushear en una rama designada por sesión (ej. `claude/<slug>`), no en `main`;
- prohíbe explícitamente pushear a una rama distinta sin permiso.

Al intentar `git push -u origin main` esa sesión fue rechazada (`non-fast-forward`): `origin/main` tenía historia propia, de otra sesión concurrente, no relacionada con la tarea en curso. La sesión pusheó entonces a su rama designada.

**Esto no invalida la regla aprobada** — es un dato de entorno que la regla no contemplaba. Queda para el Orquestador decidir, con Victor, cómo se reconcilia el trabajo hecho en una rama designada por el harness con la regla de "`main` directo": abrir un PR puntual, o que el Orquestador haga el merge una vez cerrado el plan. Ningún agente decide esto por su cuenta.

## Pool real de ramas y worktrees del repositorio de código

**Por verificar.** Este repositorio (`pg_control_proyectos`) no tiene acceso directo a `py_control_proyectos_web`: no se puede ejecutar `git branch -a` ni `git worktree list` sobre ese repositorio desde acá. La tabla de pool `work-1`/`work-2` de `convenciones-de-trabajo.md` (creada 2026-09-23) está marcada como obsoleta en la nomenclatura (ver arriba) y no fue verificada de nuevo en esta tarea. Antes de asignar un Worker de código a una rama concreta, quien tenga acceso a `py_control_proyectos_web` debe correr `git branch -a` / `git worktree list` ahí y actualizar esta sección con el resultado real — no se copia la tabla vieja como si fuera vigente.

## Worktrees y bundler (verificado 2026-09-23)

En un worktree de `py_control_proyectos_web` donde `node_modules` se crea como Junction de Windows al repo principal, Next.js 16 con Turbopack **no soporta este escenario**: tanto `npm run build` como `npm run dev` abortan con un error de resolución de símlinks (`Symlink [project]/node_modules is invalid, it points out of the filesystem root`) al resolver dependencias, antes de compilar cualquier código de la app — no depende del diff de la rama.

**Workaround verificado:** dentro de worktrees, usar siempre `--webpack` para build y dev (`npx next build --webpack`, `npm run dev -- --webpack -p <puerto>`). El build con Turbopack se hace en el checkout principal, donde `node_modules` es una carpeta real, no un junction.

## Commits durante la implementación

- No un commit por cada ítem de la Punch List.
- Commitear aproximadamente **cada 35% de avance acumulado** de la Punch List de la tarea.
- El commit se hace **solo al terminar completo** el ítem de checklist en curso — nunca a medias de un ítem, aunque eso implique pasar el 35% antes de commitear.
- `git add` explícito de los archivos tocados — nunca `git add -A` o `git add .` sin revisar qué se está agregando.
- Aplica tanto en `pg_control_proyectos` (documentación) como en `py_control_proyectos_web` (código), salvo que Victor indique otra cosa para una tarea puntual.

## Chats

- Un chat corresponde a una tarea o etapa clara; no se reutiliza un chat de una tarea cerrada para una tarea nueva.
- Al cerrar una tarea, se antepone el prefijo `hist_` al nombre del chat.
- Los chats no se borran, se renombran. Eliminar un chat requiere la misma autorización explícita que eliminar una rama o un worktree.
- La nomenclatura completa de chats (distinción local/nube, jerarquía de roles) está en `../00-estandar-agentes/03-sesiones-contexto-y-handoff.md`.
