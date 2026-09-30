# Resultados F1-A · Niveles: logica pura

Rama `local-worker-1` (app). Codigo en `src/lib/niveles/` (tipos, nivel-wbs, roles, hermanas, arbol, detector-profundidad, index + 2 archivos de prueba). Sin tocar `src/lib/dp/**`, `cronograma/**`, BD ni pantallas. Sin migraciones.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda, seguir-flujo-de-planes, verificar-permisos-por-rol. App: sin carpeta de Skills. Se uso `cerrar-tanda` (adaptado: estados/evidencia/traspaso en este archivo). Los otros no aplican (no hay permisos ni flujo de plan que recorrer).

## Estado de los items
| ID | Estado | Evidencia |
|---|---|---|
| F1A-1 | Conforme | `niveles.test.ts` (F1A-1): niveles de 2 a N por codigo, nivel ya conocido |
| F1A-2 | Conforme | prueba con 2, 3, 4 y 5 niveles; Servicio implicito (nivel 0) o nivel 1 que coincide con el servicio |
| F1A-3 | Conforme | muestra por grupo (mismo nivel y padre) y propagacion solo a hermanas |
| F1A-4 | Conforme | hermana de profundidad distinta marcada «para revisar»; grupo homogeneo no marca; empate marca la mas superficial |
| F1A-5 | Conforme | detector (PUNTOS, ESQUEMA, ANCHO_FIJO, SANGRIA, PLANA). Archivos reales: `PPTO-prueba N°01.xlsx` (2 niveles) y `PS-065-2026 ... BANCODUCTOS` (3 niveles), hoja CD, en `niveles-archivos-reales.test.ts` (se omite si no hay carpeta; `PG_INFO_PRUEBAS` cambia la ruta). Ninguno tiene 5 niveles: el caso de 5 y los de ancho fijo/esquema/sangria usan **fixtures SINTETICOS** rotulados en `niveles.test.ts`. `Cron-prueba N°01.xlsx` no se uso (es cronograma). |
| F1A-6 | Conforme | `construirArbol` + `agruparPorMapa` con 4 y 5 niveles; prueba de equivalencia con `agruparPorSubpresupuesto` en 3 niveles |

## Verificacion
- `npm test` (Bash, VITE_CONFIG_NATIVE_IGNORE_WARNING=true): 72 archivos, 698 pruebas verdes (antes del ajuste; tras el ajuste 23/23 en `src/lib/niveles`).
- `npx tsc --noEmit`: limpio. Habia 1 error en `niveles.test.ts` (linea 55, propiedad `nombre` sobrante); corregido.
- Lint: worktree 27 problemas (9 errores, 18 avisos), **0 en `src/lib/niveles`**; no toque nada fuera de ese modulo. `npm run lint` en el repo principal da 24585 porque recorre los `.worktrees`: no sirve de base; la base comparable es el lint del worktree sobre `45c9e0a` (mismos archivos fuera de niveles).

## Handoff (F1-B puede usar el modulo)
- API: `construirArbol(filas, mapa)`, `proponerMapa/proponerMapaDesdeFilas`, `rolesPorDefecto`, `agruparHermanas`, `propagarRolAHermanas`, `filasParaRevisar`, `agruparPorMapa`, `detectarProfundidad`; todo reexportado en `src/lib/niveles/index.ts`.
- Decision tecnica: `MapaNiveles.nivel` = profundidad del codigo WBS; nivel 0 = Servicio implicito cuando el presupuesto no trae fila de servicio. Una fila sin hijas (o `esPartida`) es PARTIDA aunque este en un nivel alto (p. ej. `1.3` en Bancoductos).
- Retomar: `cd .worktrees/local-worker-1; VITE_CONFIG_NATIVE_IGNORE_WARNING=true npx vitest run src/lib/niveles`.

## Hallazgos
- Bancoductos tiene partidas directas del subpresupuesto conviviendo con paquetes (nivel 2 partida): el arbol las soporta; F1-B/F1-C deben mostrarlas sin marcarlas como error.
- El detector por sangria/esquema/ancho fijo solo esta probado con fixtures; ningun archivo real los usa.

## Mejoras de trabajo
- `npm run lint` en el repo principal cuenta los worktrees (24585): medir la base de lint dentro de un worktree limpio.

## Reglas de negocio
Ninguna nueva. Huerfanos: ninguno.

## Llamadas
Aprox. 12 en esta sesion (mas las de la sesion previa cortada, que dejo el WIP 61cdc02).
