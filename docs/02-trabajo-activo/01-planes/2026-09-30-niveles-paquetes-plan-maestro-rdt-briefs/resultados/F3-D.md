# Resultados F3-D · Plan Maestro: paquetes, Prog./Real, estados y rendimiento

Carril 2 · rama `local-worker-2` · commit sobre `82cc863` (hash en el mensaje final del Worker). Sin push ni merge. Sin migraciones (no se aplicó ninguna). Sin navegador.

## Skills revisados

`pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `seguir-flujo-de-planes`, `verificar-permisos-por-rol`. Repositorio de la app: sin carpeta de Skills. Se aplicó `cerrar-tanda` (estados, evidencia y traspaso en este archivo). `verificar-permisos-por-rol` no aplica: no cambia quién puede qué (se reutilizan `puedeGestionarPlanMaestro` y `puedeCrearVersionPlanMaestro`; ningún chip ni acceso nuevo).

## Qué ya existía de F3-C y no se rehízo

Grupos por paquete y directas con subtotal y plegado, filas «Prog.» y «Real» con interruptor «Real: sí/no», real por clave de reporte (solo la primera línea de cada clave dentro del grupo lo lleva), estado `APROBADO` de solo lectura, botón «Crear versión nueva» con motivo y el color del real. F3-D amplió esas piezas.

## Estado de los ítems

| ID | Estado | Evidencia |
|---|---|---|
| F3D-1 | Conforme (lógica y build); vista **Observado — pendiente de F5** | `construirFilas(lineas, plegados, { nodos, reales })` en `src/lib/plan-maestro/lienzo-vista.ts`: con `NodoEstructura[]` agrega filas de **nivel** (con subtotal y plegado propio, sangría por profundidad) dentro de cada grupo; sin nodos se ve igual que antes. Tipo copiado del contrato C1 en `niveles-tipos.ts` (no se importa `src/lib/niveles/`). Subtotales de grupos y niveles en `calcularVistaTotales(..., nodos)`. La **partida repetida** aparece en cada paquete con su porción (claves de reporte distintas). Pruebas en `lienzo-d.test.ts` (F3D-1: 5 casos: repetida, subtotales 1 600 / 400 / 1 000 y servicio 3 000, niveles con subtotal, nivel plegado, partida sin nodo). |
| F3D-2 | Conforme (lógica y build); vista **Observado — pendiente de F5** | Filas «Prog.» y «Real» y interruptor ya estaban; se verificó con `RealPorClave` simulado que el real va por clave (p1 = 50 %, p2 = 25 % de la misma partida) y no altera lo programado. **Nuevo:** las claves con real y sin línea en esta versión se pintan al final como **«Real de versión anterior»** (insignia amarilla): muestran metrado por día y HH; físico y económico salen «—» (sin línea no hay precio ni BAC) y **no suman** al total del servicio. `filasDeRealAnterior`, `totalesRealAnterior`. 4 casos de prueba. |
| F3D-3 | Conforme (lógica) | `src/lib/plan-maestro/estados.ts` + pruebas: `APROBADO` = solo lectura para todo rol; `BORRADOR` editable y guardable solo con permiso de gestionar, guardado parcial (el 100 % solo se exige al crear); versión nueva solo con una aprobada y solo `puedeCrearVersion`, con motivo obligatorio recortado (máx. 500). El servidor ya exige motivo y parte de las asignaciones de la aprobada (`POST /api/plan-maestro`, sin cambios). La pantalla usa `vistaEstadoPlan` y `validarMotivoVersion`; muestra el motivo de una versión aprobada. |
| F3D-4 | Conforme por estructura; **Observado — pendiente de F5** (vista) | Seis estados con `estadoPantalla` (sin servicio — mensaje nuevo —, cargando `role=status aria-busy`, error `role=alert` con «Reintentar», sin plan, sin partidas, listo; probado). Región del lienzo con `tabIndex=0`, `aria-label` y `aria-describedby` a un resumen para lectores de pantalla; semanas y grupos con `aria-expanded`; controles envuelven (`flex-wrap`) para 390 px; en móvil solo WBS y descripción quedan fijas. El icono del asistente no tapa columnas porque el shell reserva `pb-[4.5rem]` bajo el contenido (hallazgo 4 de F3-C, sin cambios). |
| F3D-5 | Conforme (medición) | Servicio simulado de 150 partidas × 120 días (18 000 asignaciones, 50 partidas con real): totales + filas en milisegundos (prueba con tope de 3 s). **Render de servidor** (`scripts/medicion/lienzo-render.medicion.ts`): completo = **73 746 celdas, 14,9 MB de HTML, ~0,9–1,2 s**; con **ventana de filas** = **10 605 celdas (−86 %), 2,2 MB, ~0,3–0,5 s**. Ventana vertical: `ventanaDeFilas` (alturas fijas por fila, espaciadores arriba y abajo, margen de 400 px, solo desde 60 filas); el `scrollTop` se cuantiza a 120 px y se mide con `ResizeObserver`; las **columnas fijas y los encabezados `sticky` no se tocan**. No se virtualizaron columnas (las semanas plegables ya reducen columnas; riesgo con `sticky left` y el recorrido de teclado). `npx tsc --noEmit` limpio; `vitest run`: 76 archivos, **770 pruebas verdes**; `eslint src`: **27 problemas, igual que `main`** (9 errores, 18 avisos); `npx next build --webpack` correcto. |

## Archivos tocados (todos del carril 2)

`src/lib/plan-maestro/lienzo-vista.ts` (+ prueba), `estados.ts`, `niveles-tipos.ts`, `lienzo-d.test.ts` (nuevos), `src/components/plan-maestro/LienzoPlanMaestro.tsx`, `src/components/ui/FormularioPlanMaestro.tsx` (prop opcional `nodos`), `scripts/medicion/lienzo-render.medicion.ts` (nuevo, medición manual, no entra en `npm test`).

## Handoff

- Falta (F5-A, integración): pasar `nodos` reales del carril 1 a `FormularioPlanMaestro` (prop `nodos`, `NodoEstructura[]`) desde `page.tsx`/API y cambiar `niveles-tipos.ts` por el tipo del carril 1; sustituir `leerRealPorClave` (`real-adaptador.ts`) por `realPorClaveReporte` del carril 4 (mientras tanto `reales = []` y todas las filas «Real» marcan 0 %).
- Medición del render: `scripts/medicion/lienzo-render.medicion.ts` necesita el alias `@/`, que `vitest.config.ts` no define: copiar una configuración temporal a la raíz del worktree con `resolve.alias: { '@': '<worktree>/src' }` e `include: ['scripts/**/*.medicion.ts']`, ejecutar `npx vitest run --config <archivo> --disable-console-intercept` y borrarla.
- Comandos: `cd D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-2` · `npx vitest run src/lib/plan-maestro` · `npx tsc --noEmit` · `npm run dev -- --webpack -p 3112`.

## Comprobaciones para F5 (navegador)

1. Servicio con paquetes y partidas directas: plegar paquete y nivel; la partida repetida sale en cada paquete con su porción; el subtotal del paquete coincide con la suma de sus filas.
2. Con real simulado o real: filas «Real» bajo cada clave; un paquete eliminado deja la fila amarilla «Real de versión anterior» (físico y económico «—», HH visibles).
3. `APROBADO`: todas las casillas deshabilitadas, sin guardar ni crear; con administrador o jefe de proyectos aparece «Crear versión nueva» y exige motivo; otro rol con permiso de gestionar no lo ve.
4. `BORRADOR` guardado parcial y retomado tras recargar.
5. Estados vacío, cargando, error (cortar red) y sin servicio; 390 px (controles envueltos, solo WBS y descripción fijas); teclado: Tab llega a la región del lienzo, flechas la desplazan, Enter plega.
6. Servicio grande (≥ 150 partidas × ≥ 120 días): desplazar vertical rápido sin saltos de altura ni filas en blanco; columnas fijas intactas; filas de 28 px (partida, paquete y nivel) y 24 px (real): comprobar que ningún texto las desborda.
7. Los 28 px / 24 px y el margen de 400 px se eligieron sin verlos; si hay saltos, ajustar `ALTO_FILA` en `lienzo-vista.ts` a la altura real.

## Hallazgos y preguntas para el Orquestador

1. `vitest.config.ts` no define el alias `@/`: ninguna prueba puede importar componentes. La medición del render quedó como script manual (ver Handoff). Si se quiere en `npm test`, F5-A decide agregar el alias (archivo congelado/ajeno).
2. Al crear un Plan Maestro con paquetes, la fila de nivel de la maqueta («Por avance del paquete») sigue sin implementarse (no está en C3), igual que en F3-C.
3. Las filas de «Real de versión anterior» solo existen si `realPorClaveReporte` devuelve claves sin línea; hoy sin carril 4 nunca aparecen.

## Mejoras de trabajo

- Un archivo de medición dentro de `src/` que ninguna entrada carga lo rompe `modulos-huerfanos.test.ts`: poner los scripts de medición en `scripts/`.
- Con `python` en la shell, un script largo con tildes y comillas falla con heredoc (ya anotado en F3-C): escribir el script con la herramienta Write y ejecutarlo.

## Reglas de negocio detectadas

- Ninguna nueva. Se aplicó lo escrito: `APROBADO` solo lectura, el real nunca sobrescribe lo programado, versión nueva con motivo solo para administrador y jefe de proyectos, borrador parcial.

## Huérfanos

- Los de F3-C (`generarPropuestaDiaria` y sus pruebas) siguen sin uso. Ninguno nuevo.

## Llamadas

Aprox. 40 llamadas de herramienta.
