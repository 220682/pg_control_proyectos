# Resumen de cierre — Tanda J

## Tanda, rol y modelo

Tanda J (Dashboard: detalles e interacciones), Worker 2, Sonnet, esfuerzo medio.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| J1 | Observado | Código: `TarjetaTocable` + `DetalleTarjeta` (EstadoDashboard.tsx), detalle bajo la fila, se cierra al volver a tocar; PPC en el Bloque E. `tsc`, pruebas y build en verde. | Falta la captura/recorrido visual (P36: sin cuentas de prueba, migraciones 098-101 sin aplicar). Se cierra en la tanda L. |
| J2 | Observado | Botón por detalle (`destino`), filas de la matriz tocables (`FilaPartidaTocable`). Sin recorrido visual. | Igual que J1. |
| J3 | Observado | `FranjaRevision` (avance, IP; CPI solo Completo), fila resaltada con «En revisión», barras atenuadas en avance por nivel y desempeño; Quitar y Escape en el proveedor. Prueba de render de la franja. | Igual que J1. |
| J4 | Observado | Dona: Mano de obra→HH, Equipos→HM (`pedirPestana`); barras de «Desempeño por partida» marcan la partida y llevan a la matriz. | Igual que J1; ver pregunta 1. |
| J5 | Conforme | `src/components/dashboard/detalles-parcial.test.ts`: datos serializados y HTML de cada detalle abierto y de la franja en Parcial sin importes ni SPI/CPI/BAC/PV. | — |
| J6 | Observado | Botones reales (Tab/Enter/Espacio), `aria-expanded`/`aria-controls`, foco visible, filas y barras con teclado, Escape global. | Sin prueba en navegador; tanda L. |
| J7 | Observado | No hay capturas. | P36; tanda L. |

## Rama, commits y archivos tocados

Rama `local-worker-2`, commit `8e60ced` (pusheado; `git branch --contains` = local-worker-2). Archivos: `EstadoDashboard.tsx` (nuevo), `detalles-tarjetas.ts` (nuevo), `detalles-parcial.test.ts` (nuevo), `BloqueE`, `DonaCosto`, `GraficoAvanceNivel`, `GraficoBarrasHorizontales`, `GraficoRecursos`, `MatrizPartidasDashboard`, `dashboard/page.tsx`. Un solo commit para J1-J7 (no dos). Snapshot de curva-s restaurado con `git checkout`.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| J-H1 | mejora de trabajo | El `node_modules` del repo principal estaba a medias (otro `npm ci` en curso); se eliminó solo el enlace del worktree y se corrió `npm ci` en el worktree, por aviso del Orquestador. | Aprendizaje continuo |
| J-H2 | mejora de trabajo | La regla `react-hooks/set-state-in-effect` falla con setState en `useEffect`; se usó el patrón de ajustar estado durante el render. | Aprendizaje continuo |
| J-H3 | conflicto/pregunta | «Clic en Desempeño por partida marca la matriz»: se implementó como clic en cada barra (marca la partida y baja a la matriz). | Pregunta 1 |
| J-H4 | conflicto/pregunta | La tarjeta AC lleva a «Costo real de recursos», no a una pestaña (no hay gráfica de AC). PPC no tiene tarjeta en la fila: su detalle va en el Bloque E. | Pregunta 2 |

## Traspaso

Hecho: J1-J7 en código. Falta: recorrido visual y capturas (tanda L). Verificación: `npm test` 127 archivos / 1243 pruebas verdes; `npx tsc --noEmit` sin salida; `npm run lint` tras la corrección sin errores nuevos (el conteo previo a la corrección fue 10 errores por un error propio ya arreglado; los 9 preexistentes se mantienen); `npx next build --webpack` compila. Las tarjetas ahora son botones envolventes, por lo que su altura no se estira en la rejilla.

## Llamadas y contexto

Aproximadamente 35 llamadas.

## Skills revisados

`cerrar-tanda` aplicado; los demás no aplican (sin permisos nuevos ni hallazgos a trasladar).

## Fuentes de verdad revisadas

No se editó ningún flujo. Pendiente para el Orquestador: flujo 11 (detalles de tarjetas, franja «Revisando partida», R7) y matriz de permisos no cambian de acceso.
