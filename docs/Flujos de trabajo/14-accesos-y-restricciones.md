# 14 — Accesos y restricciones

**No implementado en UI.** Tabla visual con **columnas = roles** y **filas = accesos** (qué chip/formato puede usar cada rol), para tener de forma visual lo que hoy vive disperso en `puedeVer*`/`puedeSubir*`/`puedeCrear*` de `py_control_proyectos_web/src/lib/permisos/permisos.ts` y en el mapeo de `herramientasPorGrupo` (`grupo-proceso.ts`) / `NAV_PROYECTO` (`nav-proyecto.ts`).

Pedido por Victor el 2026-09-16.

**Regla:** cada vez que se agrega un chip/acceso nuevo al sistema, esta tabla debe actualizarse. Deuda acumulada desde que se pidió (chips agregados sin entrar aquí todavía): **Cronograma** (flujo 15) y **Crear RDTs** (flujo 06).

Cuando se construya: recorrer TODAS las funciones de permisos de una sola pasada, no rol por rol.

Accesos requeridos para paquetes de trabajo
Los paquetes deben sumarse a la matriz de permisos del flujo 14 con los siguientes accesos mínimos:

- Ver paquetes del servicio.
- Crear paquete.
- Editar paquete.
- Asignar o quitar partidas.
- Revisar avance del paquete.
- Registrar avance o datos de control del paquete.
- Archivar o cerrar paquete.
- Ver detalle de paquete y trazabilidad a partida.

Estas acciones se habilitan según el servicio, el rol y la configuración de control del presupuesto, sin duplicar permisos ya existentes para partidas, RDT ni dashboard.
