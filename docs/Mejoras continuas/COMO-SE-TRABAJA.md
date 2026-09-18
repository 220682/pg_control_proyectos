# Cómo se trabajan las mejoras continuas

## Ciclo

1. Pedido de Victor (pantallas concretas).
2. Crear `Mejoras continuas/YYYY-MM-DD-<tema>.md` con el pedido y pantallas.
3. Implementar **solo el flujo** (y subflujos) indicado. Ver `Flujos de trabajo/`.
4. Verificar esas pantallas (no un tour de toda la app).
5. Al cerrar: llenar **Resultados** en el mismo MD (qué quedó, qué no, qué cambió).
6. Si llega a `main`/prod: actualizar el MD del flujo tocado en el mismo commit o el siguiente.

## Regla principal — aislamiento

Al modificar un flujo, no se tocan los demás. Si un archivo es compartido (`permisos.ts`, fechas, badges):

- Cambio mínimo a la función que hace falta.
- Tests del flujo tocado y smoke de quienes importan ese archivo.
- Declarar el cambio como “compartido” en el MD del lote y listar flujos afectados.

## Hecho de verdad

Una mejora no está hecha hasta que está en **todas las pantallas de ese flujo**. La API sola no cuenta.

Antes de cerrar: buscar el símbolo en el repo y confirmar que está importado. El test `modulos-huerfanos.test.ts` falla si un módulo no es alcanzable.

## No hacer

- Commitear `fetch` a `127.0.0.1` de debug.
- Afirmar que falta un SQL sin sondear Supabase.
- Meter borrar RQ en el consolidado (solo Status, solo admin).
- Tratar OT como RDT. Solo se vinculan por N° OT; el flujo OT aún no está en UI.

## Conceptos que no se mezclan

- **Geren** = administrador + jefe de oficina técnica + jefe de proyectos.
- **Status RQ** = una fila por cabecera, PDF PROM-GP-008.
- **Consolidado RQ** = una fila por ítem/material, PDF PROM-GP-004. Pertenece al flujo RQ.
- Importar DP y generar PR son flujos independientes.
