# Resultado — Tanda C: Informes, datos de los bloques del sistema

## Tanda, rol y modelo

Worker 1, Sonnet 5.5, esfuerzo medio. Tanda C, Ola 2, carril W1. Sesión cortada una vez por el límite de uso de la cuenta y reanudada.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| C1 | Conforme | `armar-datos-diario.test.ts`: RDT VALIDADO (acumulado, %, sin etiqueta) y REGISTRADO («reportado, pendiente de validación», no suma al acumulado); indicadores sin dinero. | No probado en base (098-102 sin aplicar). |
| C2 | Conforme | Misma prueba: parte nuevo (extra 2, stand-by 2, estado Operativo) y viejo (extra 0, stand-by 0, estado «—»). | No probado en base. |
| C3 | Conforme | Avance por nivel, PPC y causas, avance de partida, Plan Maestro 7 días, Curva S (envuelve el resultado de `cargarCurvaS` modo fisica). | Observado menor: ver H1 y H2. |
| C4 | Conforme | `armar-datos-semanal.test.ts`: anterior + periodo = acumulado a la fecha, y el periodo = suma de los diarios; columnas por día (<=10 días) o por semana. | No probado en base. |
| C5 | Conforme | `armar-datos-costos.test.ts`: AC del formato = AC de `calcularIndicadoresProyecto` (620+300 con materiales/subcontratos), filas de costo por partida suman el AC con la fila «Materiales y subcontratos (sin partida)»; rechaza roles sin economía. | No probado en base. |
| C6 | Conforme | `congelar` hace copia profunda; la prueba cambia el RDT y la tarifa después y la foto no cambia. | — |
| C7 | Conforme | `sin-dinero.test.ts`: TECNICO, EJECUTIVO, FOTOGRAFICO, PERSONALIZADO y semanal sin campos de dinero; control negativo con COSTOS. | — |

Comandos: `npm test` 132 archivos, 1311 pruebas en verde; `npx tsc --noEmit` sin errores; `npm run lint` 9 errores y 22 avisos (iguales a los preexistentes, ninguno en `src/lib/informes`); `npx next build --webpack` en verde.

## Rama, commits y archivos tocados

Rama `local-worker-1`: e089e38 (C1-C3) y a8e85d2 (C4-C7), subidos; `git branch -a --contains` muestra `local-worker-1` y `origin/local-worker-1`. Creados en `src/lib/informes/`: `datos-rdt.ts`, `bloques-avance.ts`, `armar-datos-diario.ts`, `armar-datos-semanal.ts`, `armar-datos-costos.ts`, `congelar.ts`, `cargar-fuentes.ts`, `fixtures-informes.ts` y sus pruebas (`armar-datos-diario`, `armar-datos-semanal`, `armar-datos-costos`, `cargar-fuentes`, `sin-dinero`). Sin cambios en `tipos.ts`, `db/**`, `evm.ts`, `rdts/**`.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| C-H1 | conflicto con un flujo o pregunta para el Responsable humano | El PR suma metrado por el vínculo oficial `rdt_actividad_partidas` (db/053), no por el texto `rdt_actividades.wbs`. Los informes usan el texto `wbs` (misma fuente que el parte). Si una actividad vincula otra partida distinta de su texto, el acumulado del informe no coincidiría con el del PR. | Pregunta a Victor: elegir el vínculo oficial en el cargador (cambio solo en `cargar-fuentes.ts`). |
| C-H2 | conflicto con un flujo o pregunta para el Responsable humano | Los indicadores «al corte» de un diario de una fecha pasada usan el PR actual (EV acumulado de hoy), no el de esa fecha; avance/programado del periodo semanal sí salen de la serie de la Curva S por fecha. | Decidir si el diario usa también la serie por fecha. |
| C-H3 | observación sobre la política | El brief manda quitar el enlace `node_modules` con `cmd /c rmdir`; desde bash de Git en Windows ese comando no actuó (abrió un cmd interactivo) y el `npm ci` siguiente corrió a través del enlace. Pasó EPERM a medias sobre `node_modules` del repositorio principal. Se resolvió con `cmd.exe /c "rmdir node_modules"` desde PowerShell. | Corregir la instrucción en el brief/estándar: usar PowerShell y comprobar `LinkType` vacío antes de `npm ci`. |
| C-H4 | archivo o carpeta huérfano | `node_modules` del repo principal `py_control_proyectos_web` quedó con 50 entradas y sin `.bin` tras ese `npm ci` fallido. Ya estaba «a medias» según el Orquestador, pero conviene reinstalar. | Reportado a Victor; correr `npm ci` en el repo principal. |
| C-H5 | mejora de trabajo | La prueba `modulos-huerfanos` exige que todo módulo nuevo de `src/lib` sea alcanzable; un cargador sin consumidor aún necesita al menos una prueba que lo importe. | `docs/03-aprendizaje-continuo/`. |

Regla de negocio acordada: ninguna. Sin conflicto de reglas: HH MOI sin valorizar, legacy en fila aparte (`FILA_LEGACY`) y «Materiales y subcontratos (sin partida)» como el brief.

## Traspaso

- Hecho: C1 a C7 en código y pruebas, subido.
- Falta: la ruta/interfaz de la Ola 3 consume `armarDatosDiario`, `armarDatosSemanal`, `armarDatosCostos`, `congelar`; el cargador `cargar-fuentes.ts` no está probado contra base. Composición del cargador completo (PR, Curva S, informes emitidos) queda para la ruta.
- Pendiente: aplicar 098-102 (Victor) y probar `cargarPartesRdt`; responder C-H1 y C-H2; reinstalar `node_modules` del repo principal.

## Llamadas y contexto

Unas 55 llamadas a herramientas entre las dos partes de la sesión.

## Skills revisados

`cerrar-tanda` (consultado por nombre; el commit de documentación lo hace el Orquestador). Demás: ninguno aplica (tanda de funciones puras).

## Fuentes de verdad revisadas

No se editó ningún flujo. Flujos 06, 10 y 11 no se releyeron por completo; las columnas se verificaron en `db/026`, `040`, `047`, `053`, `100`, `102`. Pendiente anotar en el flujo 18/21, si procede, el origen de los bloques de informe.
