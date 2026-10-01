# Entorno, Git y worktrees

## Dónde se trabaja

Desde el 2026-10-01 todo el trabajo corre **en terminal**, con Claude Code o con Cursor: un Orquestador y sus subagentes (ver `09-medicion-y-modelos.md`). Ya no se coordina con chats con nombre ni con aplicaciones de escritorio o web. Para trabajar sin la laptop, Victor entra a ella por un medio de control remoto externo mientras queda encendida; el avance real vive siempre en git y en el archivo de progreso, no en una sesión.

## Regla de los dos repos (según el plan y las convenciones aprobadas)

| Tipo de trabajo | Repositorio | Rama | Worktree |
|---|---|---|---|
| Documentación de proceso (Spec, plan, progreso, evidencia, hallazgos, informe de auditoría, fuentes de verdad, mensaje de cierre) | `pg_control_proyectos` | `main`, directo, sin rama ni merge | No se usa |
| Código de la app | `py_control_proyectos_web` | `<entorno>-worker-N` (ej. `local-worker-1`); nunca `main` hasta el merge tras el Gate 2 | `.worktrees/` de ese repo, subcarpeta con el mismo nombre de la rama |

- `entorno` es `local` o `nube`; se verifica con la herramienta disponible, no se asume. Hoy se trabaja en `local`.
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

**Verificado el 2026-09-27 (Orquestador) y 2026-09-30.** El repositorio de la app está en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` y es accesible desde una sesión local: se pueden correr `git`, el servidor de desarrollo y Playwright sobre él. Estado real: ramas `main` y `local-worker-1`; worktrees: el checkout principal y `.worktrees/local-worker-1` (los demás restos de `.worktrees/` se conservan como `hist_nucleo` y `hist_local-worker`, sin abrir). La nomenclatura `work-1`/`work-2` de `convenciones-de-trabajo.md` está obsoleta y su tabla no se debe usar como vigente. La existencia de una carpeta se comprueba con `ls`, no con la salida de `git worktree list` (esta no muestra carpetas sueltas). Antes de asignar un Worker de código a una rama, correr `git branch -a` y `git worktree list` en `py_control_proyectos_web` y actualizar esta sección.

## Worktrees y bundler (verificado 2026-09-23)

En un worktree de `py_control_proyectos_web` donde `node_modules` se crea como Junction de Windows al repo principal, Next.js 16 con Turbopack **no soporta este escenario**: tanto `npm run build` como `npm run dev` abortan con un error de resolución de símlinks (`Symlink [project]/node_modules is invalid, it points out of the filesystem root`) al resolver dependencias, antes de compilar cualquier código de la app — no depende del diff de la rama.

**Workaround verificado:** dentro de worktrees, usar siempre `--webpack` para build y dev (`npx next build --webpack`, `npm run dev -- --webpack -p <puerto>`). El build con Turbopack se hace en el checkout principal, donde `node_modules` es una carpeta real, no un junction.

## `.env.local` en worktrees

Copiar el `.env.local` del checkout principal al worktree de un Worker, entre carpetas locales del mismo proyecto, no requiere consulta (decisión de Victor, 2026-09-27). Se hace con `cp` sin leer ni mostrar valores, se verifica con `cmp` y se comprueba que git lo ignora (`git status` del worktree en 0). Alcance: solo `.env.local` del mismo proyecto; cualquier otro archivo de entorno o de secretos se sigue consultando. Antes de proponer borrar un `.env.local` se compara por `cmp`/hash y por nombres de variable, sin mostrar valores: un archivo con el mismo nombre puede ser la única fuente de otras credenciales.

## Commits durante la implementación

- No un commit por cada ítem de la Punch List.
- Commitear aproximadamente **cada 35% de avance acumulado** de la Punch List de la tarea.
- El commit se hace **solo al terminar completo** el ítem de checklist en curso — nunca a medias de un ítem, aunque eso implique pasar el 35% antes de commitear.
- `git add` explícito de los archivos tocados — nunca `git add -A` o `git add .` sin revisar qué se está agregando.
- Aplica tanto en `pg_control_proyectos` (documentación) como en `py_control_proyectos_web` (código), salvo que Victor indique otra cosa para una tarea puntual.

## Sesiones y subagentes

Las sesiones no se nombran ni se renombran: el Orquestador lanza subagentes y los identifica por su rol y tanda (por ejemplo «Worker F2-A»), y esa descripción queda en el registro de sesión que lee el script de medición. Un subagente corresponde a una tanda; no se reutiliza para otra. Al terminar su tanda se cierra y su resumen de cierre queda en el archivo de resultados del plan. La regla universal de sesiones (contexto, handoff, relevo del Orquestador) está en `../00-estandar-agentes/03-sesiones-contexto-y-handoff.md` y `../00-estandar-agentes/08-medicion-y-relevo.md`.
