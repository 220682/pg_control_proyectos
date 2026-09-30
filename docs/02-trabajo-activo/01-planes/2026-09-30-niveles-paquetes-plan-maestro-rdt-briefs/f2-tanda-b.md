# F2-B · Paquetes: pantalla de dos lados, declarar y crear paquete

Lee primero `00-reglas-de-contexto.md`. Carril **3 · Paquetes** · rama `local-worker-3`, puerto 3113.
Fase F2 · **Depende de:** F2-A cerrada **y de la maqueta aprobada por Victor**: `mockups/paquetes-declarar.html` y `mockups/paquetes-agrupar.html` (F0-A). Sin maqueta aprobada, no empieces.
**Punto de commit:** al cerrar la tanda, en `local-worker-3`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F2B-1 | Pantalla de **dos lados**: a un lado el cronograma con su jerarquía y la **columna Metrado**; al otro el DP mostrando **solo partidas, solo consulta** | Lógica en módulo puro con prueba; build |
| F2B-2 | **Declarar**: desplegable de partida en la celda Metrado pre-llenado por el enlace automático por EDT; metrado por vínculo; **hitos atenuados** con su marca; indicador de **restante por partida** | Prueba de la lógica + build |
| F2B-3 | Botón **«Crear paquete»** (dentro de la pantalla, no chip): casillas al inicio de cada ítem salvo Servicio, nombre, nivel, guardar; marcar una fila resumen marca sus hijas. `?accion=crear` (acción del panel, ya registrada) abre la pantalla **ya en modo crear** | Prueba de la lógica + build |
| F2B-4 | El paquete creado se ve con **marca visual** y al seleccionarlo se selecciona **completo**; una **partida repartida entre dos paquetes** se acepta y su suma se vigila (100 %) | Prueba con el caso de dos paquetes |
| F2B-5 | Fuera del formulario: fechas inicio y fin, «Repartir en días» y la lista vertical fecha → metrado; la pantalla ya no exige programación para guardar un paquete | Diff + build |
| F2B-6 | Permisos de interfaz: los 13 roles ven; solo administrador, jefe de proyectos y planner ven las acciones de escribir; `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Salida de comandos + prueba de las funciones de permiso |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Pantalla actual: `src/components/ui/FormularioPaquetesTrabajo.tsx` (529 líneas; `abrirNuevoAlInicio` ya recibido desde `paquetes-trabajo/page.tsx`, que lee `?accion=crear`). Reutiliza `Button`, `Card`, `traducirErrorApi`, `formatearServicioLista`. El selector de OT y los mensajes se conservan.
- API de C2 (`GET`, `PUT …/vinculos`, `POST`, `PATCH`); `NodoEstructura` de C1 por props. **Hasta la integración** usa datos simulados o la jerarquía actual de `RESUMEN`/`TAREA`/`HITO`; no importes `src/lib/niveles/`.
- Toda la lógica (selección en árbol, restante, validaciones, orden) en `src/lib/paquetes-trabajo/` con pruebas: **vitest no prueba componentes** (`environment: node`).
- Interfaz: `design.md` §5 (Tablas, Selects), §8 (scroll horizontal, cabecera fija), §9, §10; sin `max-w-*` en la página; `scope` en `th`; no inventes nombres de componentes que no existan en `src/components/`. Sigue la **maqueta aprobada** y, si discrepa de `design.md`, pregunta.
- Permisos de pantalla: `puedeVerPaquetesTrabajo` y `puedeGestionarPaquetesTrabajo` (`permisos.ts`, sin cambios).
- Sin navegador en esta tanda (F5 verifica en vivo): anota las comprobaciones pendientes.

## Qué NO hacer

- No crees chips, rutas ni accesos nuevos. La acción «Crear paquete» del panel ya existe: no la edites (`registro-accesos.ts` está congelado).
- No edites `api/cronograma/**`, `plan-maestro/**`, `rdts/**`. No apliques migraciones. No cambies permisos. Sin push.
- Ante contradicción con un flujo o con la maqueta: detente y devuelve la pregunta.

## Cierre

`resultados/F2-B.md` (estado de F2B-1 a F2B-6, handoff, comprobaciones de navegador para F5, llamadas). Commit en `local-worker-3`, `git add` explícito.
