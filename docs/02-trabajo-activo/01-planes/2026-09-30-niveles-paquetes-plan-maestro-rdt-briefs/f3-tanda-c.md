# F3-C · Plan Maestro: lienzo (columnas, semanas, seis columnas) y ocultar paneles

Lee primero `00-reglas-de-contexto.md`. Carril **2 · Plan Maestro** · rama `local-worker-2`, puerto 3112.
Fase F3 · **Depende de:** F3-B cerrada **y de la maqueta aprobada por Victor**: `mockups/plan-maestro-lienzo.html` y `mockups/paneles-ocultables.html` (F0-B). Sin maqueta aprobada, no empieces.
**Punto de commit:** al cerrar la tanda, en `local-worker-2`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F3C-1 | **Ocultar y mostrar los paneles laterales** desde el shell (escritorio), recordado por usuario; en móvil los paneles siguen como cajón; el icono del asistente no tapa columnas | Lógica en módulo puro con prueba; build |
| F3C-2 | **Lienzo**: columnas fijas a la izquierda (WBS, descripción, Und., metrado, costo unitario, **HH por unidad**), una **columna por día** deslizante, entrada de metrado por día, fila de **total del servicio** | Prueba de la lógica + build |
| F3C-3 | **Semanas plegables** (plegada = una columna con sus totales), editar por bloques, **escribir el total de la semana y repartirlo**, ampliar el rango de días antes o después con las fechas de la actividad **sombreadas como guía** (no limitan) | Prueba de la lógica |
| F3C-4 | **Seis columnas por semana** (físico, económico, HH; semanal y acumulado) con **interruptor** para ocultar las acumuladas, rotuladas con nombre y unidad | Prueba de los totales con el caso del anexo |
| F3C-5 | Indicador por fila de **cuánto falta repartir** y global; el botón de crear (aprobar) el Plan Maestro solo se habilita con el 100 %; el `BORRADOR` se guarda parcial | Prueba de la lógica |
| F3C-6 | **Se retiran** «Generar propuesta» (copia) y «Editar distribución diaria»; `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Diff + salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Pantalla actual: `src/components/ui/FormularioPlanMaestro.tsx` (~409 líneas; vistas «Resumen» y «Distribución semanal» de solo lectura y el `<details>` «Editar distribución diaria» en ~375). Página: `src/app/(workspace)/plan-maestro/page.tsx`.
- Shell: `src/components/ui/WorkspaceShell.tsx` — asides de escritorio `hidden … lg:flex` (izquierdo `w-60`, ~390; derecho `w-64`, ~424) y cajón móvil (~308). El flujo 16 describe el asistente como icono flotante de 48 px abajo a la derecha dentro del `main`. **Eres el único carril que edita el shell**; sus pruebas nuevas van en archivos nuevos, sin tocar las existentes de `src/lib/config/`.
- Lógica de totales y validaciones: `src/lib/plan-maestro/lienzo.ts` (F3-A). El componente solo pinta.
- API de C3: `GET` → `{ plan, lineas, asignaciones, semanas, reales }`; `PATCH` guardar y aprobar. Mientras el carril 4 no entregue el real, `reales` viene vacío.
- Interfaz: `design.md` §3 (layout y asistente), §5, §8 (columnas `sticky` y scroll), §9, §10; tablas largas con scroll horizontal sin perder contexto; no inventes componentes. **No hay chip, ruta ni acceso nuevo**.
- Sin navegador en esta tanda: lo que lo exija queda `Observado — pendiente de F5`.

## Qué NO hacer

- No edites `permisos.ts`, `registro-accesos.ts`, `nav-proyecto.*`, `panel-*` ni sus pruebas (congelados). No edites `paquetes-trabajo/**` ni `rdts/**`.
- No agregues las columnas de Tiempo ni Área/Disciplina/Frente (no están aprobadas; ver pregunta del Gate 1). No apliques migraciones. Sin push.
- Ante contradicción con un flujo o la maqueta: detente y devuelve la pregunta.

## Cierre

`resultados/F3-C.md` (estado de F3C-1 a F3C-6, handoff, comprobaciones para F5, llamadas). Commit en `local-worker-2`, `git add` explícito.
