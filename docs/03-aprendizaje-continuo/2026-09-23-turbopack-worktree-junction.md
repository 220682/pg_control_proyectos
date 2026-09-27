# Turbopack no corre en worktrees con `node_modules` en Junction

**Fecha:** 2026-09-23  
**Origen:** Worker Fase 1 de Paquetes de Trabajo (chat `local_3`)  
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-09-23-paquetes-de-trabajo.md`

## Hallazgo

En un worktree de `py_control_proyectos_web`, `node_modules` se crea como una **Junction** de Windows al repo principal (`.worktrees/work-1/node_modules` → `py_control_proyectos_web/node_modules`). Next.js 16 con Turbopack como bundler **no soporta este escenario**: tanto `npm run build` como `npm run dev` abortan con:

```
TurbopackInternalError: Symlink [project]/node_modules is invalid,
it points out of the filesystem root
```

El panic ocurre al resolver dependencias (`find_package` → `resolve` → `directory_tree_to_entrypoints`), **antes de compilar código de la app**, por lo que no depende del diff de la rama.

## Workaround verificado

```bash
# Build
npx next build --webpack

# Dev
npm run dev -- --webpack -p <puerto>
```

El servidor con `--webpack` levantó en 1.4s y sirvió las rutas nuevas (`/paquetes-trabajo`, `/api/cronograma/hitos`, etc.) sin problemas. Se comprobó en ambos comandos.

## Consecuencia práctica

Dentro de worktrees, **usar siempre `--webpack`** para build y dev. El build con Turbopack se hace en el checkout principal, donde `node_modules` es una carpeta real (no un junction).