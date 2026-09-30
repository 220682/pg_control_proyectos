# F1-A · Niveles: lógica pura (detección, roles, muestra, hermanas)

Lee primero `00-reglas-de-contexto.md`. Carril **1 · Niveles** · rama `local-worker-1` (worktree `.worktrees/local-worker-1`, puerto 3111).
Fase F1 · **Depende de:** nada · **No depende de la maqueta** (es lógica sin pantalla). Contrato: `00-contratos-tecnicos.md` § C1.
**Punto de commit:** al cerrar la tanda, en `local-worker-1`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F1A-1 | Tipos `RolNivel`, `RolNivelCronograma`, `MapaNiveles`, `NodoEstructura` (C1) y una función que calcula el **nivel de cada fila** a partir de su código WBS con puntos, soportando de 2 a N niveles | Prueba unitaria |
| F1A-2 | **Roles propuestos por defecto** según el número de niveles (tabla del Spec: 2 → Servicio/Partida; 3 → Servicio/Subpresupuesto/Partida; 4 → Servicio/Subpresupuesto/Paquete de partidas/Partida; 5 → Servicio/**Área**/Subpresupuesto/Paquete de partidas/Partida); el nivel 1 cuyo nombre coincide con el del servicio se propone como Servicio | Prueba con 2, 3, 4 y 5 niveles |
| F1A-3 | **Fila de muestra por grupo de hermanas** y **propagación** del rol elegido a las hermanas (mismo nivel y mismo padre) | Prueba |
| F1A-4 | Filas que **no siguen el patrón** de su grupo (profundidad distinta) quedan marcadas «para revisar» | Prueba |
| F1A-5 | Detector de profundidad para WBS **sin puntos o de ancho fijo** (por estructura de la hoja); verificado con los archivos reales de `docs/06-material-de-apoyo/Informacion para pruebas/` y, si ninguno tiene 5 niveles, con un **fixture sintético** rotulado como tal | Prueba + nota de qué archivos se usaron |
| F1A-6 | `construirArbol(filas, mapa): NodoEstructura[]` y agrupador por mapa, con pruebas sobre un presupuesto de 4 niveles y uno de 5; los servicios de 3 niveles típicos producen la **misma agrupación** que hoy (`agruparPorSubpresupuesto`) | Prueba de equivalencia |

## Contrato técnico verificado (2026-09-30, solo lectura sobre `45c9e0a`)

- Hoy: `src/lib/dp/parser-cd.ts` (~97-148) lee subpresupuestos con `/^\d+$/` y paquetes de partidas con `/^\d+\.\d+$/` vía `leerEncabezadosCD(hoja, patron)`; una partida es la fila con WBS y metrado numérico. `src/lib/dp/subpresupuestos.ts` deriva el subpresupuesto con `wbs.split('.')[0]`. Tipos en `src/lib/dp/tipos.ts` (~41-75).
- El módulo nuevo vive en `src/lib/niveles/` (+ `*.test.ts`). **No edites** `src/lib/dp/**` ni `src/lib/cronograma/**` en esta tanda (eso es F1-B); solo crea código nuevo e importa sus tipos de lectura si hace falta.
- Orden fijo de roles: Servicio > Área > Subpresupuesto > Paquete de partidas > Partida. Partida = siempre el último nivel.
- Archivos de prueba reales: `PPTO-prueba N°01.xlsx`, `PS-065-2026 - BANCODUCTOS - APU CORREGIDO.xlsx`, `Cron-prueba N°01.xlsx` (Excel, se leen con la librería que ya usa el parser; verifica cuál en `parser.ts`). No copies esos archivos al repositorio de la app.
- Vitest solo corre `src/**/*.test.ts` en entorno `node`: no hay pruebas de componentes.

## Qué NO hacer

- No cambies nada de la importación actual, de la base de datos ni de las pantallas (F1-B y F1-C). Sin migraciones.
- No definas roles o nombres distintos a C1; si el Spec y los archivos reales chocan, detente y pregunta.
- No cambies permisos. No toques archivos congelados. Sin push ni merge.
- Ante contradicción con un flujo escrito, acción destructiva o duda de negocio: detente y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

`resultados/F1-A.md` según `00-reglas-de-contexto.md` (estado de tus seis ítems, handoff, llamadas). Commit en `local-worker-1`, `git add` explícito, sin push.
