# Verificar lint contra `main` y por archivo tocado, no contra cero

**Fecha:** 2026-09-23  
**Origen:** Worker Fase 1 de Paquetes de Trabajo (chat `local_3`)  
**Tarea relacionada:** `docs/Tareas de implementacion/2026-09-23-paquetes-de-trabajo.md`

## Hallazgo

`npx eslint src` en `py_control_proyectos_web` da **9 errores / 18 warnings** en la rama `main` (setState dentro de effects, `any` explícito, entidades HTML sin escapar, `prefer-const`). Es deuda preexistente, no introducida por la tarea.

Sin ese baseline, cualquier tarea nueva queda "en rojo" y el autor no sabe si los problemas son suyos o heredados.

## Criterio de verificación (ya aplicado)

1. **Comparar el total contra `main`** antes de reclamar un archivo — si el conteo es idéntico, la deuda es previa.
2. **Lintear solo los archivos tocados por la tarea** (`eslint src/lib/x src/app/api/x ...`). Si salen limpios, el trabajo no introdujo deuda nueva.
3. Reportar en la tarea: "eslint: N errores/M warnings, idéntico conteo al de `main`; archivos tocados: limpios".