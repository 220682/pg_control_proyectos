# Resumen de cierre — Tanda I: Dashboard, gráficas

## Tanda, rol y modelo

Tanda I, Ola 1, carril W2. Worker 2, Sonnet, esfuerzo medio. Rama `local-worker-2`.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| I1 | Conforme | `src/lib/dashboard/avance-por-nivel.ts` + prueba (8 casos: agrupación por nivel, bajada, Pendiente sin plan, salida solo fracciones, normalización). `npm test` verde. | |
| I2 | Observado | `GraficoAvanceNivel.tsx` (barras verticales, selector de nivel, clic baja, ruta con volver/subir, «Pendiente» sin plan aprobado) conectado en la página. tsc, lint y build verdes; render estático probado. | Sin captura ni interacción real: sin cuentas de prueba ni migraciones aplicadas. Tanda L. |
| I3 | Conforme | `recursos-contractual-acumulado.ts` + prueba: suma HH/HM igual a la del PR; exceso en rojo = acumulado − contractual. | |
| I4 | Observado | `GraficoRecursos.tsx`: pestañas HH, HM, Subcontratos (deshabilitada con título en Parcial, probado). Subcontratos usa `resolverSubcontratos` de N (cargador). La página pasa el cliente admin al cargador solo si `puedeVerEconomia`. HM lee `cantidad_acumulada` tal como la da el cargador. | El cierre de R no está en la rama: no se probó que el stand-by llegue sumado en `cantidad_acumulada`. Confirmar en L tras incorporar R/`db/102`. |
| I5 | Observado | Leyenda con `aria-pressed` que oculta series; globo con mouse (`pointerenter`), toque (`pointerdown`) y teclado (foco, Esc); cada valor está en etiqueta y en tabla «Ver valores». | Comportamiento táctil y de teclado sin verificar en navegador (L). |
| I6 | Observado | `GET /api/proyectos/[id]/dashboard/recurso-partidas?tipo=mano_obra\|equipo&descripcion=` con guardia de rol y alcance; solo horas; prueba del aggregator. Panel en la gráfica con estados carga, error y vacío. | No ejecutada contra datos reales (sin sesión). El cargo se une al recurso del PR por nombre normalizado. |
| I7 | Observado | Estados vacíos probados en render estático (avance y recursos); carga/error en el panel de I6. | Capturas en escritorio y 390 px no posibles en esta sesión (L). |

## Rama, commits y archivos tocados

Rama `local-worker-2`. Commits: `6a1ed04` (I1, I3 y cargador con `unidad` y `cantidad_contractual`) y `32334bd` (I2, I4-I7: componentes, API, página). Ambos en la rama (`git branch --contains HEAD` → `local-worker-2`) y subidos con push. Archivos: `src/lib/dashboard/{avance-por-nivel,recursos-contractual-acumulado,recurso-partidas}.ts` y sus pruebas; `src/components/dashboard/{GraficoAvanceNivel,GraficoRecursos,grafica-comun}.tsx` y `graficas-parcial.test.ts`; `src/app/api/proyectos/[id]/dashboard/recurso-partidas/route.ts`; `dashboard/page.tsx`; `cargar-dashboard.ts`. Snapshot de `curva-s` restaurado con `git checkout`.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| I-H1 | regla de negocio acordada | P5: la unidad de `cantidad_contractual` de equipos es HM (el DP guarda la `unidad` del recurso y el import fija HM por defecto; `db/004`, `aplicar-equivalencias.ts`). No se verificó con un DP real. | Flujo 11 (Dashboard), para que Victor lo confirme |
| I-H2 | conflicto con un flujo o pregunta | No hay llave entre el cargo del tareo (texto copiado) y `pr_recursos.descripcion`: el detalle por partida (I6) los une por nombre normalizado (sin tildes, mayúsculas ni espacios dobles). Los nombres distintos quedan sin coincidir. Pregunta: ¿se acepta, o se pide una llave en la tanda R? | Victor / flujo 11 |
| I-H3 | regla de negocio acordada | Para que el Parcial no lleve dinero a la gráfica interactiva (cliente), las partidas se normalizan a fracciones del BAC total (`normalizarPartidasAvance`). | Flujo 11 |
| I-H4 | mejora de trabajo | `cat <<'EOF'` con bloques TSX largos falló en Git Bash («unexpected EOF»); la herramienta Write funciona. | `docs/03-aprendizaje-continuo/` |
| I-H5 | observación sobre la política | El brief pide escribir en la raíz de `resultados/` pero el Worker no commitea en el repositorio de documentación; aclarar quién lo commitea. Ya lo cubre el brief (lo hace el Orquestador). | Sin acción |

## Traspaso

- Hecho: I1-I7 en código. Sin dinero en el Parcial (prueba que recorre HTML y datos enviados).
- Falta (tanda L): capturas en escritorio y 390 px de las seis vistas; verificar con cuentas de prueba el clic, el teclado, el toque y la API; confirmar el stand-by en HM al incorporar R.
- Verificación: `npm test` 126 archivos / 1237 pruebas verdes; `npx tsc --noEmit` sin errores; `npm run lint` 9 errores y 22 avisos (iguales a los preexistentes); `npx next build --webpack` exitoso.
- Pendiente de decisión: I-H2.

## Llamadas y contexto

Unas 22 llamadas (la medición exacta la hace el Orquestador).

## Skills revisados

`cerrar-tanda` (secuencia seguida a mano: estados, evidencia, traspaso, commit; el commit de documentación lo hace el Orquestador). Los demás no aplican a esta tanda.

## Fuentes de verdad revisadas

No se editó ningún flujo. Pendientes para el Documentador: flujo 11 (gráficas de avance por nivel y de recursos, pestaña Subcontratos solo en Completo, fracciones sin dinero en el Parcial, unidad HM de equipos) y matriz de permisos/flujo 14 por la ruta nueva `recurso-partidas` (permiso: `puedeVerDashboard` + alcance sobre el servicio, solo horas).

## Correcciones posteriores del Orquestador

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| I-H3 (corregido) | regla de negocio acordada | Commit `461a0f9`: ya no se mandan partidas como fracciones del BAC al cliente. El servidor calcula con `construirVistasAvance` el porcentaje programado y real de cada nodo de cada nivel; el cliente recibe solo código, nombre, porcentajes y `tieneHijos`. Prueba en `graficas-parcial.test.ts` que recorre lo serializado. `npm test` 1238 verdes, `tsc` limpio. | Flujo 11 |
| I-H2 (riesgo aceptado) | observación | Cruce cargo-recurso por nombre normalizado aceptado por el Orquestador; riesgo: nombres distintos no coinciden. | Verificación en vivo |
