# Resultados F1-C · Niveles: pantallas de confirmación, aviso de recarga y consumidores propios

Rama `local-worker-1` (app), commit `ba81f64`. Sin navegador, sin migraciones, sin push.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda, seguir-flujo-de-planes, verificar-permisos-por-rol. App: sin carpeta de Skills. Se usó `cerrar-tanda` (adaptado). Los otros no aplican (sin permisos por rol; el recorrido del flujo es del Orquestador).

## Estado de los ítems
| ID | Estado | Evidencia |
|---|---|---|
| F1C-1 | Conforme (lógica) / Observado (en vivo) | Módulo puro `src/lib/niveles/pantalla-niveles.ts` (grupos de hermanas con fila de muestra, Servicio implícito, resumen, validación, mapa a enviar) + `src/components/niveles/ConfirmarNiveles.tsx` (solo pinta). Importar DP en dos pasos: `soloAnalizar` → paso «Confirmar niveles» → «Aprobar niveles» envía `mapaNiveles`. **Und. y Met. en columnas separadas**; Nivel y Met. a la derecha, Und. a la izquierda. Pruebas en `pantalla-niveles.test.ts`. `tsc` y build verdes. |
| F1C-2 | Conforme (lógica) / Observado (en vivo) | Mismo paso en `FormularioCronograma.tsx` con roles del cronograma y columna Duración; la API `POST /api/cronograma` ahora acepta `soloAnalizar` y devuelve `propuesta` con `filas` y `nombreServicio`. Retirados de la pantalla: bloque de vínculos con metrado, lista «partidas incompletas», columna Hito y `SelectorPartidasDp` (la carga y la vista de actividades quedan). Las rutas `PATCH /api/cronograma` y `/hitos` no se tocaron (las usará Paquetes, F2/F3). |
| F1C-3 | Conforme (lógica) | `src/lib/proyectos/aviso-recarga.ts`: con Plan Maestro aprobado, bloqueo sin opción; si no, lista de lo que se perdería y casilla de confirmación (`confirmarPerdida`). `AvisoRecarga.tsx` lo pinta en DP y cronograma. Pruebas de los tres casos y de que otros 409 (conciliación) no son aviso. |
| F1C-4 | Conforme (equivalencia) / Observado (en vivo) | `src/lib/niveles/agrupar-pantallas.ts` (`agruparSegunNiveles`): misma forma que `agruparPorSubpresupuesto`; sin mapa o sin encabezados usa lo de siempre. Prueba: con 3 niveles típicos el resultado es `toEqual` al agrupador actual; con 5 niveles agrupa por el subpresupuesto del nivel 3. `dp/page.tsx` y `pr/page.tsx` leen `servicio_niveles` y `servicio_encabezados` (origen DP). Se quitó `max-w-6xl` del contenedor de DP (regla de diseño). |
| F1C-5 | Conforme (comandos) / Observado (móvil y accesibilidad en vivo) | `npx tsc --noEmit`: limpio. Suite: 76 archivos, 736 pruebas verdes. `npx eslint .`: 27 problemas (9 errores, 18 avisos) = igual que `main`/F1-B; 0 en archivos nuevos. `npx next build --webpack`: correcto. Estados vacío, carga («Leyendo…», `role=status`, `aria-busy`), error (`role=alert`) y vacío del cronograma implementados; `th scope="col"`, `caption` solo lector, foco nativo, icono + texto en «Para revisar»; tabla con scroll y cabecera fija; desplegable con ancho mínimo menor en móvil. |

## Handoff (máx. 15 líneas)
1. Pendiente F5 (navegador, 390 px y escritorio con 3 paneles): ver lista abajo.
2. **Decisión técnica a confirmar:** el mapa guarda un rol **por nivel**, no por grupo. La maqueta muestra un desplegable por grupo; en la app cambiar uno cambia todo el nivel (se dice en pantalla). Si Victor quiere roles distintos por grupo de hermanas, haría falta cambiar el modelo (`servicio_niveles` por nivel).
3. «Para revisar» sale del detector de F1-A (profundidad de subárbol distinta a la de las hermanas), no de «sin metrado ni unidad» como dice el texto de ejemplo de la maqueta. «Confirmar rol» confirma el grupo completo y desbloquea «Aprobar niveles».
4. Flujo de recarga: el aviso aparece tras el primer análisis (`soloAnalizar` ya evalúa la recarga); al confirmar se reenvía `confirmarPerdida` también en el guardado final y en el reintento de conciliación. La lista de pérdidas usa solo lo que la API devuelve (vínculos, paquetes, borrador); no cuenta partidas del DP actual como en la maqueta.
5. Servicios con profundidad fuera de 2 a 5 niveles: el paso muestra error y no deja aprobar (antes la base aplicaba su mapa por defecto).
6. Componentes nuevos en `src/components/niveles/` (no estaba en la matriz; carpeta nueva del carril 1). Migraciones 073-075: según el prompt ya aplicadas; no verifiqué en la base.
7. Aviso para el Orquestador: Victor dijo (mensajes durante la tanda) que las barras deslizantes de las maquetas «siguen de color blanco» (color no va); es de la maqueta (F0-V), no de esta tanda. En la app, `globals.css` ya tiene barras con tema oscuro y las tablas nuevas lo heredan. Victor también pidió no cortar Workers en marcha y asignar esa corrección al primero que se desocupe.

## Comprobaciones de navegador pendientes para F5
- Importar DP con DP de 3, 4 y 5 niveles: paso 2 con cuenta de niveles, fila de muestra por grupo, «Ver N hermanas», cambio de rol (valida orden y hoja), «Aprobar niveles» bloqueado con filas para revisar y luego activo; tras aprobar, importación y vista DP/PR igual que antes en 3 niveles.
- Recarga con Plan Maestro aprobado (bloqueo, sin continuar) y sin él (lista + casilla + «Reemplazar y continuar»).
- Cronograma: mismo paso con Duración; sin bloque de vínculos ni columna Hito; con y sin fila de servicio.
- Archivo inválido (error), servicio sin cronograma (vacío), carga lenta (estado de carga), 390 px (scroll horizontal, botones que envuelven), teclado y lector de pantalla.
- Servicio con DP anterior sin mapa: DP/PR agrupan como siempre.
- Consulta de `servicio_niveles`/`servicio_encabezados` con el cliente de usuario (RLS de lectura para autenticados según db/073-074).

## Mejoras de trabajo
- `heredoc 'EOF'` largo en Bash volvió a fallar por el analizador; usar Write a un archivo temporal y leerlo desde Python.
- Un `grep` tras `cd` a rutas con corchetes puede ser denegado por reglas de permiso ajenas; usar la herramienta Grep.

## Reglas de negocio acordadas en esta tarea
Ninguna nueva. Decisión de Victor aplicada: «Und.» y «Met.» en columnas separadas en Importar DP (el flujo 09 y `design.md` deben reflejarlo en F5-D). Pendiente de confirmar: rol por nivel vs por grupo (handoff 2).

## Carpetas/archivos huérfanos
`SelectorPartidasDp`, el bloque de vínculos y `/api/cronograma/hitos` ya no tienen uso en la pantalla del cronograma (la ruta PATCH y hitos se conservan para Paquetes). `sumarMetradoPorPartida` y `partidasConMetradoIncompleto` siguen sin uso (heredado de F1-B). Nada se borró.

## Llamadas
Aprox. 45.
