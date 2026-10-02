# Construir, evidenciar y editar en Windows: worktrees, sesión sin navegador y UTF-8

**Fecha:** 2026-10-02
**Origen:** Worker 1 (tanda A, A-H2 y A-H3) y Worker 2 (tanda B, hallazgos 1 y 2) del plan observaciones de Victor Lote 2
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-2-plan.md` (libro de hallazgos, filas MB1–MB3)
**Categoría:** `entorno/windows`

Tres hallazgos del mismo día sobre cómo trabajamos en el entorno Windows de los Workers: uno de build en worktrees, uno de evidencia sin navegador y uno de edición de archivos. No son reglas del sistema, sino la manera de hacer el trabajo sin romper el entorno.

## 1 · MB1 — `next build` (Turbopack) falla en worktrees → usar `npx next build --webpack`

**Origen:** Worker 1, tanda A (A-H2), 2026-10-02.

En el worktree `.worktrees/local-worker-1`, `npm run build` (Next.js con Turbopack por defecto) aborta porque `node_modules` es una Junction de Windows apuntando fuera del worktree: `Symlink [project]/node_modules is invalid, it points out of the filesystem root`. El fallo ocurre al resolver dependencias, antes de compilar código de la app, así que no depende del diff de la rama.

**Qué funcionó:** `npx next build --webpack` (y si hace falta servidor, `npm run dev -- --webpack -p <puerto>`). Con eso el build quedó `exit 0` en el carril 1 (A8).

**Repetido:** es el mismo fallo que [`2026-09-23-turbopack-worktree-junction.md`](2026-09-23-turbopack-worktree-junction.md), ya promovido a `01-contexto-repositorio/03-entorno-git-y-worktrees.md`. Al repetirse en un segundo plan queda marcado como candidato a refuerzo en el brief base de Workers (o a Skill), a propuesta del Auditor.

## 2 · MB2 — Evidenciar SSR/API sin navegador con password grant de Supabase

**Origen:** Worker 1 (A-H3) y Worker 2 (tanda B, hallazgo 1), 2026-10-02.

Para probar SSR y endpoints de API sin abrir un navegador (en este plan Playwright no estaba autorizado), el camino que funcionó:

1. Login con **password grant** de Supabase → `access_token` + `refresh_token`.
2. Construir la cookie de sesión `sb-<ref>-auth-token` en el formato que espera `@supabase/ssr`: valor `base64-` **troceado en pedazos de 3180 caracteres** (formato verificado leyendo `@supabase/ssr`, no adivinado).
3. Llamar a las rutas con esa cookie en el header `Cookie` y leer la respuesta (HTML SSR o JSON de API).
4. El script de apoyo se crea **fuera del repositorio** (temporal), para no dejar residuos ni secretos en el repo.

Se usó para la evidencia de A3 (SSR de `/proyectos/[id]` con 9 comprobaciones), A5, A6 y los smokes de la tanda B. Las credenciales nunca se imprimen ni quedan en archivos del repositorio.

**Trampa:** sin la cookie bien formada, el middleware redirige a `/login` (HTML) y la evidencia queda incompleta o engañosa; hay que comprobar que la llamada devuelve el 200 esperado, no la página de login.

## 3 · MB3 — PowerShell 5.1 corrompe UTF-8 en `.mjs` y `node -e` rompe con sus comillas

**Origen:** Worker 2 (tanda B, hallazgo 2), 2026-10-02.

En Windows PowerShell 5.1:

- `Get-Content -Raw` + `Set-Content` sobre un `.mjs` con acentos **corrompe el UTF-8** (las tildes se pierden y el archivo queda con la codificación por defecto de la consola).
- `node -e "…"` con comillas anidadas choca con el parser de comillas de PowerShell, y los `$` se interpolan antes de llegar a Node.

**Qué funcionó:** editar los archivos con la **herramienta de edición de archivos** del agente (lectura previa → edición), y para ejecutar lógica de Node, escribir un **`.mjs` temporal** y correrlo con `node archivo.mjs` en vez de `node -e`. Complementa [`2026-10-01-editar-archivos-sin-heredocs-largos.md`](2026-10-01-editar-archivos-sin-heredocs-largos.md), que cubre el mismo riesgo desde el lado de Bash.

## Destino propuesto

Queda como aprendizaje, pendiente de revisión del Auditor. Si Victor lo aprueba: MB1 → refuerzo de `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (el workaround ya está promovido allí) y candidato a nota en el brief de Workers por repetición; MB2 → `01-contexto-repositorio/04-pruebas-y-evidencia.md` como patrón de evidencia sin navegador; MB3 → junto al aprendizaje de heredocs, como nota en el brief base de Workers.
