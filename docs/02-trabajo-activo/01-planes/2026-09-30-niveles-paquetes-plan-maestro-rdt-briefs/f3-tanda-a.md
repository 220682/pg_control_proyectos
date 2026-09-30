# F3-A · Plan Maestro: lógica pura del lienzo (totales, semanas, 100 %, real)

Lee primero `00-reglas-de-contexto.md`. Carril **2 · Plan Maestro** · rama `local-worker-2` (worktree `.worktrees/local-worker-2`, puerto 3112).
Fase F3 · **Depende de:** nada · No depende de la maqueta (sin pantalla). Contratos: `00-contratos-tecnicos.md` § C3 (y § C4 para `RealPorClave`).
**Punto de commit:** al cerrar la tanda, en `local-worker-2`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F3A-1 | Tipos `LineaPlanMaestro`, `Asignacion`, `RealPorClave` y `claveReporte` (C3/C4) en `src/lib/plan-maestro/lienzo.ts` (+ `lienzo.test.ts`) | Prueba |
| F3A-2 | Totales por **línea, paquete y servicio**, cada medida **semanal y acumulada**: avance **económico** (metrado × precio), **HH** (metrado × HH por unidad) y avance **físico** (partida: metrado ÷ contractual; paquete y total: ponderado por costo = económico del grupo ÷ BAC del grupo) | Prueba |
| F3A-3 | **Caso de 4 semanas del Spec** como prueba: dos paquetes y una directa, totales exactos — Paquete 1: 26/58/82/100 %, Paquete 2: 25/50/75/100 %, directa: 0/0/50/100 %, total: 22,56 / 48,78 / 76,22 / 100 %; económico total $ 8 200 y por semana $ 1 850 / 2 150 / 2 250 / 1 950; HH totales 172 (47/52/39/34) | Prueba con los números del anexo |
| F3A-4 | **Validación del 100 %**: por línea (Σ días = `metradoLinea`) y por partida (Σ líneas = contractual), con la lista de líneas y partidas que faltan; tolerancia `0,000001` como en el código actual | Prueba |
| F3A-5 | Edición por bloques: **repartir uniforme** entre dos fechas, **escribir el total de una semana y repartirlo** entre sus días, redondeo que lo absorbe el último día; ampliar el rango de días antes o después | Prueba |
| F3A-6 | **Real**: agrega `RealPorClave` a semana y acumulado (metrado, EV = metrado × precio, HH); extiende las semanas si hay real fuera del rango programado | Prueba |
| F3A-7 | Semanas de **sábado a viernes** con `generarSemanasPlanMaestro` (existente) sin duplicar su lógica; `npx tsc --noEmit`, suite y lint comparado con `main` | Salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- `src/lib/plan-maestro/plan-maestro.ts` ya exporta: `generarPropuestaDiaria`, `validarAsignacionesPartida`, `calcularResumenPartidaPlanMaestro`, `SemanaPlanMaestro`, `generarSemanasPlanMaestro(min, max)`, `RealDiarioPartida`, `AgregadoRealPartida`, `agregarRealDiarioPorPartida`. **Se conserva** todo lo que ya usen otras pantallas; el módulo nuevo es `lienzo.ts`.
- Fórmulas de PR/Dashboard (flujo 10 y 18): % físico por partida = metrado acumulado ÷ contractual; EV = metrado acumulado × precio; HH ganadas **no** entran al Plan Maestro. **No mezcles** semanal con acumulado: columnas y funciones separadas y nombradas.
- Semana = sábado a viernes; el número de semanas sale del rango de fechas, sin tope fijo.
- El anexo completo de 4 semanas está en `docs/02-trabajo-activo/01-planes/2026-09-30-paquetes-y-plan-maestro-grilla.md` (Grep «Anexo»): úsalo como fixture. Los números de arriba deben salirte exactos.
- **No modifiques** `src/lib/pr`, `src/lib/dashboard`, `src/lib/curva-s`: solo los lees para reutilizar fórmulas (`calcularAvanceFisico` = EV ÷ BAC, `dashboard.ts`).

## Qué NO hacer

- No edites API, pantallas ni migraciones (F3-B y F3-C). No edites `src/lib/paquetes-trabajo/**` ni `src/lib/niveles/**`. No toques archivos congelados. Sin push.
- Ante contradicción con un flujo escrito, cambio de contrato o duda de negocio: detente y devuelve la pregunta.

## Cierre

`resultados/F3-A.md` (estado de F3A-1 a F3A-7, handoff, llamadas). Commit en `local-worker-2`, `git add` explícito.
