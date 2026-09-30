# Resultados F3-A · Plan Maestro: lógica pura del lienzo

Carril 2 · rama `local-worker-2` · worktree `.worktrees/local-worker-2`. Commit de código: ver `git log -1` de la rama (mensaje «F3-A: logica pura del lienzo…»). Sin push ni merge.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada), verificar-permisos-por-rol (no aplica: sin permisos), seguir-flujo-de-planes (del Orquestador). Repositorio de la app: sin carpeta de Skills.

## Estado de ítems
| ID | Estado | Evidencia |
|---|---|---|
| F3A-1 | Conforme | Tipos `LineaPlanMaestro`, `Asignacion`, `RealPorClave` y `claveReporte` (formato C2: `paquete\|DIRECTA:dpPartidaId`) en `src/lib/plan-maestro/lienzo.ts`; prueba de la clave |
| F3A-2 | Conforme | `calcularTotalesPlanMaestro`: por línea, partida, paquete y servicio; económico, HH y físico, semanal y acumulado por separado |
| F3A-3 | Conforme | Anexo de 4 semanas como fixture: P1 26/58/82/100, P2 25/50/75/100, directa 0/0/50/100, total 22,56/48,78/76,22/100; económico 1850/2150/2250/1950 = 8200; HH 47/52/39/34 = 172 |
| F3A-4 | Conforme | `validarCienPorCiento` (línea, partida, negativos, tolerancia 0,000001) con lista de faltantes |
| F3A-5 | Conforme | `repartirUniformeEntreFechas`, `repartirTotalSemana`, `repartirEnFechas` (último día absorbe redondeo), `aplicarBloque`, `ampliarRangoDias` |
| F3A-6 | Conforme | `calcularTotalesReal` (por clave, paquete, servicio: metrado, EV, HH, semanal/acumulado), `semanasConReal` extiende semanas |
| F3A-7 | Conforme | Semanas vía `generarSemanasPlanMaestro` (sin duplicar). `npx vitest run`: 71 archivos, 696 pruebas verdes (21 nuevas). `npx tsc --noEmit`: exit 0. `npx eslint src/lib/plan-maestro`: 0 problemas; `npm run lint` total 27 (9 errores, 18 avisos), todos en archivos no tocados (la rama es `main` 45c9e0a + solo 2 archivos nuevos limpios), por lo tanto igual al de main |

## Handoff
- Módulo listo para F3-B/F3-C: importar de `@/lib/plan-maestro/lienzo`. Semanas: `semanasConReal(rango, asignaciones, reales)`; totales: `calcularTotalesPlanMaestro(lineas, asignaciones, semanas)` y `calcularTotalesReal(lineas, reales, semanas)`. Valores físicos como fracción 0..1 (multiplicar por 100 en pantalla).
- Decisiones técnicas: BAC de línea/grupo = Σ metradoLinea × precio. Físico de línea = metrado ÷ metradoLinea; de partida (`porPartida`) = metrado ÷ contractual sumando líneas; paquete/servicio = económico ÷ BAC. Físico real = EV ÷ BAC de la clave o grupo. Asignaciones/real fuera de `semanas` no se cuentan (real lo avisa en `fechasFueraDeSemanas`; claves sin línea en `clavesSinLinea`). `repartirTotalSemana` usa los 7 días de la semana salvo que se pase `dias`. Decimales por defecto 4.
- Retomar: `cd .worktrees/local-worker-2; npx vitest run src/lib/plan-maestro`.

## Mejoras de trabajo
- Nunca usar `git stash -u` para comparar (lo ejecuté por error y lo restauré de inmediato con `stash pop`; sin pérdida).
- En PowerShell `npx vitest` emite el aviso de Vite por stderr y marca exit 1 aunque pase; usar Bash con `VITE_CONFIG_NATIVE_IGNORE_WARNING=true`.

## Reglas de negocio detectadas
Ninguna nueva. Nota para el Orquestador: el brief dice puerto 3112 en la cabecera y 3102 en el prompt; no se usó servidor.

## Huérfanos
Ninguno.

Llamadas usadas: ~19.
