# Índice de tandas — Cronograma dentro del sistema

> Plan: [`2026-10-15-cronograma-gantt-linea-base-histogramas.md`](../2026-10-15-cronograma-gantt-linea-base-histogramas.md). Un Worker = una tanda = una sesión (tope ~80 llamadas; a las 60 cierra). Estados al empezar: `pendiente`.

| Tanda | Título | Ítems | Worker | Rama | Migración | Nivel | Ola | Depende de | Estado |
|---|---|---|---|---|---|---|---|---|---|
| [C0](C0-maqueta-html-del-cronograma.md) | Maqueta HTML del cronograma | 6 (CG-01…CG-06) | CR-1 | local-worker-4 | — | 2 (n2), Haiku | Ola 0 | Gate 1 | entregada; espera la aprobación de Victor (CG-06) |
| [C1](C1-motor-de-programacion-y-datos.md) | Motor de programación y datos (migración 103) | 7 (CG-10…CG-16) | CR-1 | local-worker-4 | 103 | 3 (n3) | Ola 1 | C0 aprobada | pendiente |
| [C2](C2-api-de-edicion-y-editor-de-tabla.md) | API de edición y editor de tabla | 7 (CG-20…CG-26) | CR-1 | local-worker-4 | — | 3 (n3) | Ola 2 | C1 | pendiente |
| [C3](C3-gantt-a-mano-en-svg.md) | Gantt a mano en SVG | 7 (CG-30…CG-36) | CR-1 | local-worker-4 | — | 3 (n3) | Ola 2 | C2 | pendiente |
| [C4](C4-las-tres-puertas-de-creacion.md) | Las tres puertas de creación | 5 (CG-40…CG-44) | CR-1 | local-worker-4 | — | 2 (n2), Haiku | Ola 2 | C3 | pendiente |
| [C5](C5-linea-base-dentro-de-la-aprobacion-del-p.md) | Línea base dentro de la aprobación del Plan Maestro (104 y 105) | 6 (CG-50…CG-55) | CR-1 | local-worker-4 | 104, 105 | 3 (n3), aprobado por Victor | Ola 3 | C4 | pendiente |
| [C6](C6-seguimiento-modo-rdt-manual.md) | Seguimiento modo RDT / manual (106) | 7 (CG-60…CG-66) | CR-1 | local-worker-4 | 106 | 3 (n3) | Ola 3 | C5 | pendiente |
| [C7](C7-apu-por-partida.md) | APU por partida (107) | 5 (CG-70…CG-74) | CR-2 | local-worker-6 | 107 | 3 (n3) | Ola 1 | Gate 1 | cerrada (3 Conforme, 2 Observado; commits ea55445, fad38d4, 5de578e en `local-worker-6`; la 107 espera a Victor) |
| [C8](C8-histogramas-de-hh-y-hm.md) | Histogramas de HH y HM | 5 (CG-80…CG-84) | CR-2 | local-worker-6 | — | 2 (n2) | Ola 2 | C1, C7 | pendiente |
| [C9](C9-exportar-pdf-y-excel.md) | Exportar PDF y Excel | 5 (CG-90…CG-94) | CR-1 | local-worker-4 | — | 2 (n2) | Ola 4 | C6, C8 | pendiente |
| [C10](C10-permisos-y-validacion-final.md) | Permisos y validación final | 4 (CG-100…CG-103) | CR-1 | local-worker-4 | — | 2 (n2) | Ola 4 | C9 | pendiente |
| [C11](C11-documentacion-y-traslado-de-hallazgos.md) | Documentación y traslado de hallazgos | 4 (CG-110…CG-113) | Documentador | main del repo documental | — | 0 o 1 (n0/n1) | Ola 5 | C10 | pendiente |
| [C12](C12-verificacion-en-vivo-en-ps-0000.md) | Verificación en vivo en PS-0000 | 4 (CG-120…CG-123) | CR-1 o Worker nuevo | local-worker-4 con todo incorporado | — | 2 (n2) | Ola 5 | C11 | pendiente |

## Carriles

- **CR-1** (`local-worker-4`): C0 → C1 → C2 → C3 → C4 → C5 → C6 → C9 → C10 → C12. Migraciones 103 a 106.
- **CR-2** (`local-worker-6`, autorizada por Victor el 2026-10-15): C7 → C8. Migración 107.
- **Documentador:** C11 después de C10 y de las respuestas de Victor a la tabla de contradicciones.
- **Worker git (Haiku):** `git merge main` al empezar cada rama; incorpora `local-worker-6` en `local-worker-4` antes de C9. No toca `main`.

## Puertas intermedias

- Victor aprueba la maqueta (CG-06) antes de C1.
- Victor revisa y aplica las migraciones una por una (103 antes de C2; 104 y 105 antes de verificar C5; 106 antes de C6; 107 antes de C8).
- Cada brief lleva el resumen de cierre en `resultados/<tanda>.md`.
