# Resumen de cierre — Tanda K

## Tanda, rol y modelo

Tanda K (Dashboard: descarga PDF y Excel con Curva S). Worker 2, Sonnet. La sesión se cortó una vez por límite de uso y se retomó sin rehacer lo hecho.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| K1 | Conforme | Ruta `GET /api/proyectos/[id]/dashboard/descargar?formato=pdf\|xlsx&corte=AAAA-MM-DD`; guardia `validarEscrituraProyecto(puedeVerDashboard)` (rol + alcance), 400 en id/formato/corte inválidos, 404/409/500 explícitos. Modo por rol + `tipo_dashboard` en servidor. `tsc` y build verdes. | |
| K2 | Conforme | `src/lib/pdf/graficos.ts` (nuevo, A4 horizontal, barras y líneas vectoriales) y `src/lib/dashboard/pdf-dashboard.ts`; Curva S en hoja aparte (Completo: económica y física; Parcial: física). `hoja.ts` sin tocar. | |
| K3 | Conforme | `excel-dashboard.ts`: hojas Resumen, Avance por nivel, Recursos HH/HM, Pareto CNC, Diagnóstico, Matriz, Curva S física; en Completo además Costo y desviación, Subcontratos, Curva S económica. | |
| K4 | Conforme | `DescargarDashboard.tsx` en la fila de filtros (`FiltrosDashboard`, id desde `useParams`): menú PDF/Excel, estado «Generando…», error en `role="alert"`. | La apertura visual del botón en pantalla queda en L. |
| K5 | Conforme | `descarga-dashboard.test.ts`: PDF (leído con `pdf-parse`) y Excel (leído con `exceljs`) de Parcial no contienen US$, USD, S/, $, BAC, PV, EV, AC, CPI, SPI, SV, CV ni hoja económica; el Completo sí, para que la prueba detecte dinero. | |
| K6 | Conforme | `maxDuration = 60`. Tiempos con 60 partidas y 120 días de serie (suite): PDF Parcial 61 ms, PDF Completo 48 ms, Excel Parcial 38 ms, Excel Completo 17 ms. No incluyen consultas a la base (no medidas: sin cuentas de prueba). | |
| K7 | Observado | Archivos generados solo en la suite, no abiertos ni capturados. | Sin cuentas de prueba y migraciones 098–101 sin aplicar (P36). Se cierra en la tanda L. |

## Rama, commits y archivos tocados

Rama `local-worker-2`, commits `104887c` (K1–K3) y `a4f0808` (K4–K6), empujados; `git branch --contains` los muestra solo en `local-worker-2`. Archivos: `src/lib/pdf/graficos.ts`, `src/lib/dashboard/{datos-descarga,pdf-dashboard,excel-dashboard}.ts`, `src/app/api/proyectos/[id]/dashboard/descargar/route.ts`, `src/components/dashboard/{DescargarDashboard,FiltrosDashboard}.tsx`, `src/lib/dashboard/descarga-dashboard.test.ts`.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| K-H1 | conflicto con un flujo o pregunta para el Responsable humano | La página del Dashboard muestra dinero a todo rol con economía aunque `tipo_dashboard` sea PARCIAL (usa `puedeVerEconomia`, no el tipo). La descarga sigue el brief: Completo solo si rol con economía Y `tipo_dashboard = COMPLETO`; si no, Parcial. Puede haber diferencia entre lo que se ve y lo que se descarga. | Victor decide cuál criterio vale; alinear página o descarga. |
| K-H2 | regla de negocio acordada | Ruta nueva sin fila en el flujo 14 ni en la matriz de permisos: descarga del Dashboard, 13 roles; el dinero solo con economía + Completo. | Documentador: flujo 14, matriz y flujo 11. |
| K-H3 | observación sobre la política | Curva S en la descarga: sesión, rol y alcance se validan en la ruta y luego se usa el cliente de servicio (`crearClienteAdmin`) para `cargarCurvaS` en ambos modos (misma forma que quedará con R). En modo físico no sale dinero. | Orquestador: alinear con el cierre de R. |
| K-H4 | mejora de trabajo | `pdfkit.dash(0, …)` lanza error; no llamarlo con longitud 0 (usar `dash` solo cuando aplica). | `docs/03-aprendizaje-continuo/`. |
| K-H5 | conflicto con un flujo | El corte `corte=` de la ruta es una fecha AAAA-MM-DD (la del filtro ya resuelta), no el preset. La Curva S del archivo recorta EV/AC al corte elegido; `cargarCurvaS` usa hoy para su rango. | Confirmar en el flujo 11. |

## Traspaso

Hecho: K1–K6 con pruebas. Falta: K7 (abrir PDF/Excel reales y capturas), en la tanda L. Verificación: `npm test` 128 archivos / 1246 pruebas verdes; `npx tsc --noEmit` limpio; `npm run lint` 9 errores y 22 avisos (igual que antes, ninguno nuevo); `npx next build --webpack` verde. El snapshot de curva-s se restauró con `git checkout`. Árbol limpio. No se tocó `db/`, `package.json` ni flujos.

## Llamadas y contexto

Unas 35 llamadas en total, con una interrupción por límite de uso.

## Skills revisados

`cerrar-tanda` (secuencia seguida: estados, evidencia, traspaso, fuentes, commit). Los demás no aplican.

## Fuentes de verdad revisadas

Sin editar. Pendientes para el Documentador: flujo 14 (fila de la ruta), matriz de permisos, flujo 11 (descarga y K-H1/K-H5).
