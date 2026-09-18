# 14 — Accesos y restricciones

**No implementado en UI.** Tabla visual con **columnas = roles** y **filas = accesos** (qué chip/formato puede usar cada rol), para tener de forma visual lo que hoy vive disperso en `puedeVer*`/`puedeSubir*`/`puedeCrear*` de `py_control_proyectos_web/src/lib/permisos/permisos.ts` y en el mapeo de `herramientasPorGrupo` (`grupo-proceso.ts`) / `NAV_PROYECTO` (`nav-proyecto.ts`).

Pedido por Victor el 2026-09-16.

**Regla:** cada vez que se agrega un chip/acceso nuevo al sistema, esta tabla debe actualizarse. Deuda acumulada desde que se pidió (chips agregados sin entrar aquí todavía): **Cronograma** (flujo 15) y **Crear RDTs** (flujo 06).

Cuando se construya: recorrer TODAS las funciones de permisos de una sola pasada, no rol por rol.
