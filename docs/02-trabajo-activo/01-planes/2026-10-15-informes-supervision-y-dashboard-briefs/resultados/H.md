# Resumen de cierre — Tanda H

## Tanda, rol y modelo

Tanda H (Dashboard: responsable, % avance, IP y HH). Worker 2, Sonnet, esfuerzo medio. Rama `local-worker-2`.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| H1 | Observado | Etiqueta morada con `obtenerSupervisorACargo` + nombre de `perfiles`; sin asignar dice «Sin supervisor a cargo» (prueba de render). `tsc` y build en verde. | Sin captura de pantalla: iniciar sesión requiere las cuentas de prueba, cuyo archivo de memoria el entorno no me dejó leer. Captura de escritorio y 390 px en Completo y Parcial queda para el Orquestador o Victor. |
| H2 | Observado | `TarjetaAvanceFisico`: número de 32 px, barra con ejecutado, marca en PV/BAC y restante; sin Plan Maestro no hay marca (pruebas de `armarTarjetaAvance`). En Completo (ocupa 2 de 8 columnas de la misma fila) y en Parcial. | Misma causa: falta captura. |
| H3 | Observado | `TarjetaIp` y `TarjetaHhContractuales`: en Completo dentro del panel de la dona; en Parcial como tarjetas propias en la fila. SPI y CPI no tienen cuadros extra. | Misma causa: falta captura (verificar que la fila no crece). |
| H4 | Conforme | Matriz con HH contract., HH acum. e IP por partida, también en Parcial; prueba compara el IP renderizado con `calcularIndicadoresPartida`. | — |
| H5 | Observado | `CONTORNO_REF` (punteado amarillo, offset 2) en tarjetas, paneles de dona/desviación, diagnóstico, Bloque E, costo real, resumen y matriz. Prueba de render. | El «detalle» que abren las tarjetas y la partida en revisión son de la tanda J: no se hicieron aquí. |
| H6 | Conforme | `dashboard-parcial.test.ts`: IP y HH = sumas de `evm.ts`; matriz y tarjetas Parcial sin `US$`, CPI, AC, PV, EV ni BAC; la única ruta `api/**/dashboard/**` (`tipo-dashboard`) no devuelve montos. | La fila de tarjetas no crece: por diseño (grid de 8 columnas, avance de 2); confirmar con captura. |

## Rama, commits y archivos tocados

Rama `local-worker-2`: `dbe1a5e` (H1-H3), `b196a7a` (H4-H6), ambos pusheados; `git branch --contains` muestra solo `local-worker-2`. Archivos: `dashboard/page.tsx`, `src/components/dashboard/{TarjetasProductividad.tsx,contorno.ts,TarjetaKpi,MatrizPartidasDashboard,PanelDiagnostico,BloqueE,CostoRealRecursos,ResumenEjecutivo}`, `src/lib/dashboard/tarjetas-productividad{,.test}.ts`, `src/components/dashboard/dashboard-parcial.test.ts`. Árbol limpio.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| H-H1 | observación sobre la política | `CabeceraPagina` no admite hijos; la etiqueta del supervisor se puso bajo el encabezado en la página, no «en la línea del servicio» como en la maqueta. | Decisión de Victor / tanda de UI compartida |
| H-H2 | conflicto con un flujo | P21: `evm.ts` usa Σ `pr_partidas.bac` y `calcularBac` usa `costo_contractual` de recursos; no se tocó. | Plan, P21 |
| H-H3 | mejora de trabajo | Correr `npm test` modifica `src/app/api/curva-s/__snapshots__/curva-s-route.test.ts.snap` (restaurado con checkout). | Aprendizaje continuo |
| H-H4 | mejora de trabajo | La tarjeta de avance decía «EV / BAC» en Parcial; se cambió a «Avance físico ejecutado (RDT validados)» para no nombrar BAC en Parcial. | Flujo 11 si la redacción debe fijarse |

## Traspaso

Hecho: H1-H6 en código y pruebas. Falta: capturas (escritorio y 390 px, Completo y Parcial) y revisar a ojo que la fila de tarjetas no crece. Verificación: `npm test` 122 archivos, 1217 pruebas en verde; `npx tsc --noEmit` limpio; `npm run lint` 9 errores y 22 avisos (los preexistentes, sin nuevos); `npx next build --webpack` en verde.

## Llamadas y contexto

Unas 30 llamadas.

## Skills revisados

`cerrar-tanda` (secuencia seguida; el commit de documentación lo hace el Orquestador). `verificar-permisos-por-rol` no aplica: no cambia permisos.

## Fuentes de verdad revisadas

Ninguna editada. Pendiente de Victor: el flujo 11 ya describe esto; solo confirmar la ubicación de la etiqueta (H-H1).
