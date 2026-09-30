# F3-D · Plan Maestro: paquetes, Prog./Real, estados y rendimiento

Lee primero `00-reglas-de-contexto.md`. Carril **2 · Plan Maestro** · rama `local-worker-2`, puerto 3112.
Fase F3 · **Depende de:** F3-C cerrada. Misma maqueta aprobada (`mockups/plan-maestro-lienzo.html`).
**Punto de commit:** al cerrar la tanda, en `local-worker-2`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F3D-1 | Filas de **paquete plegables con subtotal**; la **partida repetida** aparece en cada paquete con su porción; partidas **directas** sin paquete; jerarquía por niveles con `NodoEstructura[]` (simulado hasta la integración) | Prueba de la lógica de agrupación + build |
| F3D-2 | **Subfilas «Prog.» y «Real»** con interruptor para ocultar lo real; el real se muestra por **clave de reporte** (paquete × partida); marca «real de versión anterior» si el paquete ya no existe en esta versión | Prueba con `RealPorClave` simulado |
| F3D-3 | Estados: `APROBADO` = solo lectura; `BORRADOR` guardado parcial y retomable; **nueva versión** con motivo (administrador y jefe de proyectos) que parte de la aprobada | Prueba de la lógica de estados |
| F3D-4 | Estados **vacío, carga y error**, móvil (390 px), teclado y accesibilidad del lienzo; el icono del asistente no tapa columnas | Comprobación por estructura + lista para F5 |
| F3D-5 | **Rendimiento** con un servicio grande (≥ 150 partidas × ≥ 120 días simulados): medición del render; si hace falta, virtualización de filas o columnas sin perder columnas fijas; `npx tsc --noEmit`, suite, lint comparado con `main` y build | Medición + salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Contratos C3 y C4: línea = actividad × partida; el real llega por **clave de reporte** y se muestra en la fila del grupo, no por línea. El Real nunca sobrescribe lo programado (flujo 20).
- Estados del plan y reemplazo de versión: `proyecto_plan_maestro` (`BORRADOR`, `APROBADO`, `REEMPLAZADO`); al aprobar una nueva, la anterior pasa a `REEMPLAZADO` y el PR recalcula el planificado (ya implementado; no lo tocas).
- Quién crea una versión nueva: administrador y jefe de proyectos, con motivo (propuesta aprobada en el Spec; el motivo se guarda en `proyecto_plan_maestro.motivo_version`, columna escrita en F3-B, rango 076–078; `POST /api/plan-maestro` ya lo exige).
- Interfaz: `design.md` §8 (scroll, `sticky`) y la maqueta aprobada; sin navegador en esta tanda.

## Qué NO hacer

- No edites archivos de otros carriles ni congelados. No agregues columnas no aprobadas. No apliques migraciones. Sin push.
- Ante contradicción con un flujo, con la maqueta o duda de negocio: detente y devuelve la pregunta.

## Cierre

`resultados/F3-D.md` (estado de F3D-1 a F3D-5, handoff, comprobaciones para F5, llamadas). Commit en `local-worker-2`, `git add` explícito.
