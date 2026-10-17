# Resumen de cierre — Tanda M (Documentador)

## Tanda, rol y modelo

Tanda M del plan [Informes de supervisión y Dashboard](../../2026-10-15-informes-supervision-y-dashboard.md): traslado de los hallazgos a su destino. Rol: Documentador (Worker de documentación), Sonnet 5.5, 2026-10-17, sobre `main` del repositorio de documentación. Código leído solo para comprobar los flujos: rama `local-worker-3` de la app (commit `d5233c9`), sin editar nada ahí. Skills usados: `trasladar-hallazgos` (leído desde su archivo; el Skill tool no se invocó). Otros Skills revisados: ninguno más aplica a documentar.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| M-inventario | Conforme | 57 filas de política, 19 de mejoras, 42 de reglas y 4 de huérfanos del libro, cotejadas con los resúmenes A a S y L; 20 filas nuevas agregadas (M20 a M25, R43 a R47, P58 a P61, H5 a H7) | |
| M-reglas | Conforme, con 2 pendientes | Reglas integradas en los flujos 06, 08, 10, 11, 14, 16, 21 y 22 (ver abajo) | Pendientes de decisión: ver «Pendientes de decisión» |
| M-flujo22 | Conforme | `docs/04-flujos-de-negocio/22-informes-de-supervision.md`, con su línea `Lee si:`; enlazado en el índice de flujos, `docs/README.md` y `docs/02-trabajo-activo/README.md` | |
| M-14 | Conforme | Filas de las tablas 1 y 2 y notas 11 y 12 en el flujo 14 | La Matriz de permisos la actualiza Victor (lista abajo) |
| M-designmd | Conforme | `design.md` §5 «Recuadros del Dashboard: contorno punteado amarillo» + historial 1.10.0 | |
| M-aprendizaje | Conforme | `docs/03-aprendizaje-continuo/2026-10-17-informes-supervision-y-dashboard-aprendizajes-de-trabajo.md` + fila en el índice | |
| M-referencias | Conforme | `python scripts/verificar-referencias.py docs/04-flujos-de-negocio docs/03-aprendizaje-continuo docs/05-diseno-y-referencias docs/README.md docs/02-trabajo-activo/README.md`: 0 huérfanos, 0 enlaces rotos, 27 menciones sin archivo (todas preexistentes, ninguna mía) | |
| M-cierre-filas | Conforme | Todas las filas del libro pasaron de `Registrada` a `Trasladada`, `Descartada` o `Pendiente de decisión` | |

## Rama, commits y archivos tocados

Rama `main`. Commits (verificados con `git branch --contains`): `ddf8399` (flujos, `design.md`, aprendizaje e índices), `e3469e1` (flujo 04, maqueta de subcontratos y capturas de evidencia) y el commit de cierre del libro del plan y de este resumen (el último de la rama, ver `git log`).

Archivos con cambios míos: flujos 04, 06, 08, 10, 11, 14, 16, 21 y 22 (nuevo), `docs/04-flujos-de-negocio/README.md`, `docs/README.md`, `docs/02-trabajo-activo/README.md`, `docs/03-aprendizaje-continuo/README.md` y el archivo de aprendizaje nuevo, `docs/05-diseno-y-referencias/design.md`, `mockups/pr-subcontratos-medicion.html`, la carpeta de capturas `03-evidencia/capturas/2026-10-15-informes-supervision-y-dashboard/` (28 archivos), el plan (solo estados y filas nuevas del libro), `resultados/L.md` y este archivo.

**Archivos de otros planes tocados por mí con cambios puntuales** (06, 14, 16, `design.md`, `02-trabajo-activo/README.md`): copia previa en el scratchpad; al commitear puse en el índice solo mis líneas con una fusión de tres vías (`git merge-file`), y verifiqué con `git diff --cached` que no entró ninguna línea ajena. Los cambios sin commitear de los otros planes siguen intactos en el árbol de trabajo. En el flujo 16 mi viñeta quedó separada de las líneas del otro plan para que la fusión no tuviera conflicto. **Ningún archivo queda con cambios míos sin commitear.**

## Qué se trasladó y dónde

| Destino | Qué se integró |
|---|---|
| Flujo 22 (nuevo) | Pantallas y chips, tipos, código `{OT}-ID/IS-{n}`, estados, foto fija, avance validado, indicadores al corte, vínculo oficial del metrado, formatos y quién crea cada uno, Costos solo con economía, bloques y claves de `config`, período del semanal y límites, banco de fotos, descarga y alcances, aviso al emitir, pestaña Inasistencias (R3, R5, R6, R9, R16, R17, R30 a R42) |
| Flujo 06 | HH extra, HM stand-by y estado del equipo, PDF en el mismo formato, Consolidado (R13, R14, R21, P46) |
| Flujo 08 | Supervisor operativo a cargo: columna propia, transición, cambiar sin vaciar, adjudicación (R1, R4, R23) |
| Flujo 10 | Regla de costo real: todo suma, cuenta por partes, nivel servicio, avance sin tope, Curva S, seguridad, recálculo al aplicar la 102, sección Subcontratos del Reporte, pie del PR (R15, R18, R20, R22, R27, R28, R43) |
| Flujo 11 | Responsable operativo, IP y HH, gráficas, tarjetas con clic, partida en revisión, Descargar, Costo real de recursos con materiales y subcontratos, Parcial sin dinero en pantalla y archivo (R2, R7, R8, R24 a R26, R29, R44 a R47) |
| Flujo 14 | Filas nuevas de las tablas 1 y 2, notas 3, 11 y 12, actualización 2026-10-17 (R19, R24, R33, R36, R38, R42) |
| Flujo 16 | Chips «Informes de supervisión» y «Foto de campo» en los árboles y conteo vigente (R16, R38) |
| Flujo 21 | AC con materiales y subcontratos, regla 5 corregida, la descarga del Dashboard lleva la Curva S (R2, R20) |
| Flujo 04 | Una línea: el aviso al emitir un informe (R9) |
| `design.md` | Punteado amarillo de los recuadros del Dashboard (R8) |
| Maqueta `pr-subcontratos-medicion.html` | Texto de la nota según la regla de costo real (P23) |

## Reglas R24 en adelante (decididas por el Orquestador; Victor las valida en el Gate 2)

R23 (tanda A, vaciar el supervisor) y R24 a R42 (incluida R40, «aceptada, Victor la valida al revisar el flujo de informes»). Se escribieron en los flujos igual y quedaron marcadas así en el libro. Las reglas nuevas que agregué al cotejar, también del Orquestador o de sus tandas: R43 (recalcular el PR al aplicar la 102), R44 (página y archivo del Dashboard con el mismo modo), R45 (texto de la tarjeta de avance en Parcial), R46 (clics del Dashboard) y R47 (unidad HM, pendiente de Victor).

## Pendientes de decisión (Victor)

1. **R47 / P5 — Unidad de los equipos.** El flujo 11 dice que la cantidad contractual de equipos se toma como HM, «no verificado con un DP real». Victor debe confirmar con un DP.
2. **P21 — BAC del PR contra BAC del Dashboard.** Sin base real no se midió si `Σ pr_partidas.bac` y la suma de recursos difieren; el flujo 10 lo deja anotado. Se mide con `db/pruebas/102_comparacion_ac.sql`.
3. **«Guardar Mis formatos» en la tabla 2 del flujo 14.** La lista del plan decía «quien crea informes (los cuatro)»; el código lo permite también al supervisor de costos y al jefe de costos (para formatos con bloques de Costos). Lo escribí como el código (6 roles, nota en la fila). Victor confirma o pide quitar los dos de costos.
4. **Tres líneas de otros planes que no toqué**: P1 (árbol del marco de maquetas `marco-tres-paneles.js`, desactualizado), H1 a H3 y H5 a H7 (huérfanos, abajo).

No hubo contradicciones fuera de la tabla del Gate 1 que me obligaran a no editar un flujo. La corrección del texto de «regla 5» del flujo 21 (línea 93) y la del flujo 11 salen de R20.

## Observaciones sobre la política (lista para el Auditor; no edité el estándar, `AGENTS.md` ni los Skills)

| Fila | Documento afectado | Propuesta |
|---|---|---|
| P11 | `docs/00-estandar-agentes/09` y `10` | Los niveles y modelos están escritos para opencode (deepseek, qwen, agentes n0 a n5); en Claude Code el Orquestador usó una equivalencia por tipo de tarea. Definirla en el estándar. |
| P12 | `AGENTS.md`, flujo 14 | El artefacto «Matriz de permisos» no se puede abrir desde la cuenta de Claude Code. Que las tablas del flujo 14 sean la fuente editable por los agentes y el artefacto se vuelva a publicar desde ellas, o que Victor lo comparta con esa cuenta. |
| P17, P44 | Estándar de planes | Dos planes tocaron los mismos archivos (RDT, flujos 06/14/16/18, `design.md`) y la coordinación fue manual. Fijar una regla de congelación de archivos entre planes en curso. |
| P25 | `01-contexto-repositorio/04-pruebas-y-evidencia.md` | `npm run lint` tiene 9 errores y 22 avisos preexistentes; el criterio quedó en «no agregar errores nuevos». Decidir si se corrigen. |
| P26, P43 | `scripts/verificar.ps1` y su documento (07) | El verificador devolvió ESCALAR a avances rápidos de ramas de trabajo ya pre-autorizados y BLOQUEAR a subir documentación autorizada por Victor. No lee la pre-autorización del texto del plan y trata el «Gate 2 pendiente» como condición de todo push; separar push de documentación de push de código. |
| P30 | Briefs y Skills | Un Worker no leyó `cerrar-tanda` ni `verificar-permisos-por-rol` aunque el brief lo pedía, y dejó un permiso mal. Exigir en el brief la tabla observada o una lectura verificable del Skill. |
| P36 | Estándar (pruebas) | Los Workers no pueden leer las cuentas de prueba (viven solo en la memoria del Orquestador) y todos los ítems con captura quedaron `Observado` hasta la verificación en vivo. Definir cómo se les entrega una cuenta de prueba. |
| P42 | Clasificador de permisos | Bloqueó como «destructivo» un `git merge --no-ff` entre ramas de trabajo que el Gate 1 pre-autorizaba. Las pre-autorizaciones del Gate 1 no llegan al clasificador. |
| P48, P58, P59 | Skill `verificar-permisos-por-rol` | La tabla de los 13 roles queda `Observado` hasta la verificación en vivo; `ver-como` conserva el id del administrador y no permite observar «borrador ajeno = 404»; una sonda POST crea datos (no existe sonda sin efecto). Añadirlo al Skill. |
| P52 | Estándar de pruebas | Valorar una prueba de que cada ruta del registro de accesos tenga página (un commit intermedio apuntaba a una ruta sin página). |
| P60 | Flujo 16 / plan de otro | El recuento «28 chips: 22 con pantalla y 6 inertes» de un plan en curso sumaba mal los inertes (7 de 28 antes, 7 de 30 ahora); corregido en una viñeta nueva, la línea original sigue en el árbol de trabajo de ese plan. |
| P61 | `AGENTS.md`, `01-contexto-repositorio/02` y `06-mapa-documental.md` | Dicen «21 flujos»; son 22. |
| P29, P34, P57 | — | Informativas: sin cambio de política. |

## Mejoras de trabajo

Un archivo nuevo en `docs/03-aprendizaje-continuo/`: `2026-10-17-informes-supervision-y-dashboard-aprendizajes-de-trabajo.md` (M1 a M7, M10 a M12, M14 a M25), con su fila en el índice. **Candidatas a Skill (repetidas):** editar archivos en Windows desde Bash sin heredocs (7 tandas) y el snapshot de la Curva S que `npm test` reescribe (5 tandas; mejor corregirlo de raíz con `.gitattributes`).

## Archivos huérfanos (para Victor; no borré nada)

- **H1.** `.playwright-mcp/` de este repositorio: muchos `console-*.log`, capturas y descargas de prueba (PDF, Word y Excel de los informes y del Dashboard) sin seguimiento.
- **H2.** En la app: `db/095_cerrar_lectura_directa.sql` y archivos del DP (`leer-libro.ts`, `parser-apu-s10.test.ts`) sin seguimiento, de otra tarea.
- **H3 y H7.** `node_modules` del repositorio principal de la app a medias (50 entradas, sin `vitest`) y el enlace `.worktrees/_node_modules_bloqueado_w4` que apunta a él.
- **H5.** Datos de prueba en PS-0000 (fotos «PRUEBA foto de campo 1..6», informes ID-1, IS-1, ID-2 emitido e inmutable, ID-3, ID-5 y **ID-4 de origen desconocido**); decidir si se desactivan o se conservan.
- **H6.** `tipo_dashboard` de PS-0000 se alternó y quedó en COMPLETO (se asumió que era el original): Victor confirma.
- Fuera del plan, sin tocar: archivos sin seguimiento de otros planes en `docs/` (`2026-10-07-plan-maestro-tres-paneles.md`, `2026-10-14-revision-completa-app.md`, `06-pruebas/`, `2026-10-15-verificar-en-la-base-y-presupuestos-reales.md` y varios archivos de «Informacion para pruebas»).

## Filas para la Matriz de permisos (Victor la actualiza; el artefacto no abre desde Claude Code)

Orden de columnas: Admin, JP, JOT, SOT, Plnr, SCo, JCo, SOp, SLog, SAdm, SSO, Asist, RRHH. Las mismas filas, ya escritas, están en las tablas 1 y 2 del flujo 14.

**Tabla 1 — Interfaces**

| Interfaz | Económico | Roles con ✓ |
|---|---|---|
| Informes de supervisión: ver emitidos (dentro de servicios asignados) | No | los 13 |
| Informe de formato Costos: ver | Sí | Admin, JP, JOT, SCo, JCo |
| Informes: pestaña Inasistencias (dentro de servicios asignados) | No | los 13 |
| Banco de fotos del día | No | Admin, JP, JOT, SOp |
| Reporte del proyecto: sección Subcontratos | Sí | Admin, JP, JOT, SCo, JCo |
| RDT: campos HH extra, HM stand-by y estado del equipo (ver) | No | los 13 |

**Tabla 2 — Acciones**

| Acción | Requiere OT | Roles con ✓ |
|---|---|---|
| Crear, editar su borrador y emitir un informe (formatos que no son Costos) | Sí | Admin, JP, JOT, SOp |
| Crear, emitir y ver un informe de formato Costos | Sí | Admin, JP, JOT, SCo, JCo |
| Emitir una versión nueva de un informe ajeno | Sí | Admin, JP |
| Guardar «Mis formatos» | No | Admin, JP, JOT, SOp (y SCo, JCo para formatos con bloques de Costos; ver pendiente 3) |
| Tomar y subir foto de campo | Sí | Admin, JP, JOT, SOp |
| Descargar un informe emitido (el de Costos solo los 5 con economía) | No | los 13 (Costos: Admin, JP, JOT, SCo, JCo) |
| Descargar las inasistencias en PDF | No | los 13 |
| Descargar el Dashboard (Parcial sin dinero; Completo solo los 5 con economía) | No | los 13 (Completo: Admin, JP, JOT, SCo, JCo) |
| Elegir la forma de medir y escribir el monto de un subcontrato en el Reporte del proyecto | Sí | Admin, JP, JOT, SCo, JCo |
| Registrar HH extra, HM stand-by y estado del equipo en el RDT | Sí | Admin, JP, JOT, SOp |
| Editar servicio (asignar el supervisor operativo a cargo) | Sí | sin fila nueva: solo la nota en la fila existente (Admin, JP) |

Accesos del registro: `informe-servicio` (etiqueta «Informes de supervisión», 13 roles) y `foto-campo` (Admin, JP, JOT, SOp; los otros nueve lo ven deshabilitado con título). La ruta `GET /api/proyectos/[id]/dashboard/recurso-partidas` va con `puedeVerDashboard` más alcance y no lleva fila propia.

## Traspaso

Hecho: todo lo anterior. Falta: la validación de Victor de las reglas R23 a R47 y de los tres pendientes; la actualización de la Matriz; la auditoría. Comandos de verificación: `python scripts/verificar-referencias.py <carpetas>` (0 huérfanos, 0 rotos); `git log --oneline -3` y `git branch --contains` para los commits.

## Llamadas y contexto

Unas 95 llamadas a herramientas. Las cifras exactas las mide el Orquestador.

## Skills revisados

`trasladar-hallazgos` (usado). Ningún otro aplica a una tanda de documentación.

## Fuentes de verdad revisadas

Actualizadas: flujos 04, 06, 08, 10, 11, 14, 16, 21 y 22; `design.md`; índices. Pendientes: la Matriz de permisos (Victor), y los flujos 18 y 19, que otros planes en curso tienen modificados sin commitear y que la tabla del Gate 1 no nombra.
