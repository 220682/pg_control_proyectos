# F2-C · Paquetes: orden, plegado, edición y estados

Lee primero `00-reglas-de-contexto.md`. Contratos que lees: `contrato-c2-paquetes.md` y `contrato-c6-interfaz.md`. Carril **3 · Paquetes** · rama `local-worker-3`, puerto 3113.
Fase F2 · **Depende de:** F2-B cerrada. Misma maqueta aprobada (`mockups/paquetes-agrupar.html`).
**Punto de commit:** al cerrar la tanda, en `local-worker-3`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F2C-1 | **Mover arriba/abajo** un paquete con flechas (y con teclado); el orden se guarda (`PATCH … MOVER`) y se conserva al recargar | Prueba de la lógica de orden + prueba de API |
| F2C-2 | **Plegar y expandir** un paquete (plegado = solo su nombre); «plegar todo / expandir todo» | Prueba de la lógica de plegado |
| F2C-3 | **Editar** un paquete en `BORRADOR` (nombre, nivel, vínculos, modo, guía) y **archivarlo**; detalle con trazabilidad del paquete a la partida; un paquete validado o archivado no se edita | Prueba |
| F2C-4 | Estados **vacío, carga y error**, móvil (390 px) y accesibilidad (teclado para mover y plegar, foco visible, `scope`) | Comprobación por estructura + lista para F5 |
| F2C-5 | Prueba cruzada del caso de Victor: una partida de 10 unidades repartida 5 + 5 entre dos paquetes suma el 100 %; con 5 + 4 avisa el faltante; `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Contrato C2 (`PATCH` con `accion: 'EDITAR' | 'MOVER' | 'ARCHIVAR'`), estados de paquete de `db/072`: `BORRADOR`, `VALIDADO`, `ARCHIVADO` (un paquete con avance no se elimina físicamente, flujo 19).
- La lógica de orden y plegado va en `src/lib/paquetes-trabajo/` con pruebas; el componente solo la pinta. Reutiliza los componentes y botones existentes; no inventes nombres.
- «Validar paquete» y el avance ponderado por pesos del flujo 19 **no** se construyen aquí: el avance se declara en el RDT (plan del RDT) y el flujo 19 se reescribe en F5-D.
- Permisos: sin cambios (ver: 13 roles; gestionar: administrador, jefe de proyectos, planner).
- Sin navegador: lo que lo exija queda `Observado — pendiente de F5`.

## Qué NO hacer

- No toques archivos de otros carriles, ni `registro-accesos.ts`/`permisos.ts`. No apliques migraciones. No agregues fechas ni programación al paquete. Sin push.
- Ante contradicción con un flujo o la maqueta: detente y devuelve la pregunta.

## Cierre

**Skills:** al empezar, lista `.claude/skills/` de `pg_control_proyectos` (hoy: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`) y del repositorio de la app (hoy sin carpeta de Skills) y anota «Skills revisados» en tu `resultados/F2-C.md`. **Usa `cerrar-tanda` al terminar** (adaptación de este plan: sus pasos de estados, evidencia y traspaso van en tu `resultados/F2-C.md`, no en el plan ni en el progreso compartidos).

`resultados/F2-C.md` (estado de F2C-1 a F2C-5, handoff, comprobaciones para F5, llamadas). Commit en `local-worker-3`, `git add` explícito.
