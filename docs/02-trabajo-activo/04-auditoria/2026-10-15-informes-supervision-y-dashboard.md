# Informe de Auditoría — Informes de supervisión y Dashboard

Plan: [2026-10-15-informes-supervision-y-dashboard.md](../01-planes/2026-10-15-informes-supervision-y-dashboard.md). Auditor: subagente en Sonnet 5.5, 2026-10-17. Solo lectura: no se editó código, flujos ni el plan; no se hizo commit ni se aplicó nada. Distingo siempre **[V]** = verificado por el Auditor (comando o lectura de código) de **[R]** = lo dice el resumen de la tanda o el plan, sin que yo lo reprodujera, y **[NV]** = no verificable por el Auditor (con quién puede cerrarlo).

## Alcance auditado

Tandas A a S, L y M (19 tandas, 124 ítems) y el prompt del Auditor del plan (chequeos 1 a 10), más los chequeos (a) a (l) del encargo. Repositorio de docs `pg_control_proyectos` (`main`, HEAD 8715689) y app `py_control_proyectos_web` (worktrees `local-worker-1` aa843f5, `-2` 7067a79, `-3` d5233c9).

## Material revisado

- Plan: Identificación y estado, Prompt del Auditor, tabla «dice hoy / pasaría a decir», Registro de decisiones y los cuatro apartados del libro (25 mejoras, 47 reglas, 61 observaciones, 7 huérfanos). Resúmenes `resultados/L.md` y `M.md` completos; los demás solo por cita (G.md).
- Código en `local-worker-3`: `db/098`–`102` (y `db/pruebas/102_comparacion_ac.sql`), `src/app/api/proyectos/[id]/{informes/**,fotos-campo/**,pr/subcontratos,dashboard/descargar}`, `src/app/api/inasistencias`, `src/lib/informes/**`, `src/lib/permisos/permisos.ts`, `src/lib/config/registro-accesos.ts`, `src/lib/dashboard/datos-descarga.ts`, `src/lib/pr/subcontratos.ts`, `src/lib/auth/guard-proyecto.ts`.
- Flujos 04, 06, 08, 10, 11, 14, 16, 21, 22 y `design.md` leídos desde `git show HEAD:` (el árbol de trabajo de 06, 14, 16 y `design.md` tiene cambios sin commitear de otros planes; verifiqué el texto en HEAD, no en el árbol).
- No leí el Spec completo, ni credenciales, ni `.env*`. MCP `postgresql` caído: **no hay verificación contra base de datos real**.

## Verificación de rama

- **(a) Primer chequeo [V].** `git branch --contains` de 13 commits representativos (e65dcae A, 1fa141d B, 2879b46 N, 3233b93 O, a8f7089 R, 1d7c338 S, a8e85d2 C, e7ac566 G, 37a5ea8 F, fec676c Q, aa843f5, 7067a79, d5233c9): todos en `local-worker-1/2/3` según corresponde y en ningún otro; ninguno en `main`. `git log main -- db/098_informes_supervision.sql src/lib/informes` = vacío. `git log main..local-worker-3` = 53 commits, todos de este plan. `local-worker-3..local-worker-1` = 0 y `local-worker-3..local-worker-2` = 0 (W3 contiene a W1 y W2); `local-worker-3..main` = 0 (W3 contiene a `main` 628918a, avance rápido posible). `git -C local-worker-3 status` limpio. Última rama publicada: `origin/local-worker-3` contiene d5233c9.
- **Aviso [V]:** `db/096` ya está en `main` (otro plan) y `db/095_cerrar_lectura_directa.sql` sigue sin seguimiento en `main` (otra tarea). Ningún commit de este plan toca `db/095*` (`git log -- db/095_cerrar_lectura_directa.sql` = vacío; el archivo no existe en el worktree).
- Docs: `ddf8399` y los commits de cierre están en `main` y en `origin/main` [V].

## Cumplimiento de SDD, plan, Punch List y evidencia

**Chequeos del plan 1–10**

| # | Chequeo | Resultado |
|---|---|---|
| 1 | Migraciones 098–102 aditivas, RLS sin política, trigger de inmutabilidad, no tocan 095 | **Cumple [V] por lectura.** 098: `create table if not exists` ×4, `enable row level security` ×4 sin `create policy`, trigger `trg_informes_inmutable` (db/098:114-136; solo permite EMITIDO→REEMPLAZADO cambiando estado y `actualizado_en`). 099: `add column if not exists` + relleno idempotente (`where supervisor_operativo_id is null`). 100: `add column if not exists`. 101: tabla nueva con RLS sin política. 102: dos columnas con `if not exists`. Detalle de 100 y 102 más abajo. No aplicadas por mí [NV]. |
| 1b | HH/HM de los RDT idénticos; delta de AC solo por materiales y subcontratos; cuatro lugares coinciden; una función compartida | **Parcial.** Por lectura [V]: la 102 redefine `recalcular_pr_desde_rdt` y `curva_s_proyecto` con el cuerpo de la 100 íntegro; `diff` de ambos cuerpos = solo las líneas de 102 (variables `v_ev_acum`, `v_materiales`, `v_subcontratos`, `v_bac`, `v_avance`; ampliar el reset a `material` y `subcontrato`; bloque de materiales/subcontratos; columnas `costo_materiales_acum`/`costo_subcontratos_acum`; en la Curva S, el CTE `serie0` + `cross join lateral ac_materiales_subcontratos_al_corte`). Una sola función compartida (`ac_materiales_subcontratos_al_corte`) para el PR y la Curva S [V]. Solo W3 redefine las dos funciones (100 y 102): no hay dos Workers distintos sobre la misma función [V, por `git log`]. Los cuatro valores del AC = 97.215,06 en PS-0000 tras «Recalcular PR» **[R, L.md §10]**; las pruebas `ac-equivalencia.test.ts` verifican por texto y fórmula, no contra base. **No hay medición de HH/HM del PR «antes y después» de la 100 contra datos reales [NV]** (Victor/Orquestador con `db/pruebas/102_comparacion_ac.sql` o consulta de solo lectura). |
| 1c | Subcontrato manual cambia el AC en (monto − valor físico) y no el EV/PV/BAC | **Cumple por pruebas [V]**: `ac-equivalencia.test.ts:137` («R5 (d)») y `subcontratos.test.ts:49` («N7»), ambas verdes. Con datos reales **Observado** (PS-0000 no tiene subcontratos; `PUT` da 400) [R, L.md §10]. |
| 1d | Pestaña Inasistencias con alcance por servicio para los 13 roles; filas de las tablas 1 y 2 del flujo 14 | **Cumple [V]**: `inasistencias-consulta.ts:45-81` (401 sin sesión, 403 sin rol, 403 sin alcance con `tieneAlcanceSobreProyecto`, filtro `proyectosACargo` para no administrador); pruebas `inasistencias-roles.test.ts` y `inasistencias-aislamiento.test.ts` verdes; filas en flujo 14 líneas 62 y 147 (HEAD). |
| 2 | Cada ruta nueva valida sesión, rol y alcance en servidor; `COSTOS` 403 sin economía | **Cumple con una discrepancia (H-2)**. Ver el chequeo (d). |
| 3 | Límites del período por llamada directa | **Cumple [V]**: `validarPeriodoServidor` (`src/lib/informes/ruta.ts:116`) lo llaman crear (`informes/route.ts`), editar (`[informeId]/route.ts`) y emitir (`emitir/route.ts`). Probado por pruebas de ruta [R: `informes-rutas.test.ts`, verdes]. |
| 4 | Ningún formato distinto de Costos ni el Dashboard Parcial lleva dinero | **Cumple en código [V]**, ver (e). |
| 5 | Restricción C por llamada directa | **Cumple [V]**: `bloquesSinDineroSiNoEsCostos` rechaza con 403 en crear/editar/formatos propios (`reglas-informe.ts`, `informes/route.ts:120-122`, `[informeId]/route.ts:64-66`, `formatos-usuario/route.ts:49-50`). |
| 6 | Dashboard: IP, HH y recursos coinciden con el PR; AC con materiales y subcontratos según R20 | **Cumple por pruebas [V]** (`recursos-contractual-acumulado.test.ts`, `costo-recursos.test.ts`, `descarga-dashboard.test.ts`, verdes); en vivo en PS-0000 AC = 97.215,06 en PR, Dashboard, Curva S y Costos **[R, L.md §10]**. BAC del PR vs. BAC del Dashboard (P21): **sin medir [NV]**. |
| 7 | Punch List completa con evidencia | **Parcial (H-4)**: 124 de 124 ítems cerrados «en sus ramas», pero varios `Observado` quedaron sin disposición individual. |
| 8 | Tabla «dice hoy / pasaría a decir» aplicada; flujo 22 creado y enlazado; `design.md` con el punteado | **Cumple [V]** (muestreo en (b) y grep en (c)). |
| 9 | Se usaron los Skills citados | **Parcial**: ver P30 y la desviación de la tanda Q (aplicó la idea del Skill sin abrir su archivo; anotada en el Registro, 2026-10-16). `trasladar-hallazgos` en M se leyó por archivo, no con la herramienta Skill [R, M.md]. |
| 10 | Lista de filas nuevas para la Matriz de permisos entregada a Victor | **Entregada [V]** en `resultados/M.md` §«Filas para la Matriz» y en las tablas 1 y 2 del flujo 14. El artefacto sigue sin actualizarse (P12) **[NV]**: lo hace Victor. |

**Pruebas [V]** en `local-worker-3` (d5233c9), (g):
- `npm test`: **160 archivos pasan, 1 omitido; 1623 pruebas pasan, 1 omitida (1624)**, ~29 s, salida 0. Antes: 1620 (L-bis). Subió 3.
- `npx tsc --noEmit`: sin salida, código 0 (limpio).
- `npm test` volvió a reescribir `src/app/api/curva-s/__snapshots__/curva-s-route.test.ts.snap` (fin de línea): lo restauré con `git checkout` y el árbol quedó limpio (0 cambios). Es la reincidencia nº 5 (M6, M10): ver clasificación.
- No ejecuté `npm run build` ni lint (fuera de lo permitido); las cifras de lint (9 errores, 22 avisos preexistentes) son **[R]**.

## Verificación de la revisión de fuentes de verdad por fase

- **(b) Segundo chequeo.** `grep` de «Registrada» en el plan: una sola coincidencia, en el texto del propio prompt del Auditor (línea 622) **[V]**: ninguna fila del libro está en `Registrada`. Estados presentes: Trasladada, Descartada, Pendiente de decisión. Total del libro: 25 mejoras, 47 reglas, 61 observaciones, 7 huérfanos.
- **Muestreo de 19 destinos «Trasladada» [V], en HEAD** (`git show HEAD:… | grep`): R4/R23 supervisor a cargo (flujo 08: columna y «no vaciar»), R13 HH extra ×1,25 (06), R14 stand-by (06), R21 PROM-GP-002 (06), R20/R22 «sin tope» (10), R43 «Recalcular PR» (10), P37 seguridad `service_role`/revoca (10), R44 `tipo_dashboard` (11), R8 punteado amarillo (11 y `design.md`), R6 «3 meses» (22), R9 `MENSAJE` (22) y aviso en el flujo 04, R30 vínculo oficial `rdt_actividad_partidas` (22), P7 `geolocation`/GPS (22), R40 alcances resumen/fotos y 1000 px (22), R20 en el flujo 21 (3 menciones), R38 chips «Foto de campo» (16), P23 maqueta `pr-subcontratos-medicion.html` (HEAD ya no dice «no como costo real»: 0 coincidencias de esa frase). Todos presentes. El commit citado `ddf8399` está en `origin/main`.
- **(c) Regla R20 en 10, 11, 21 y 22 [V]**: `grep` de «materiales y subcontratos no suman|no suman al costo real|regla 5|…» en `docs/04`, `docs/01` y `docs/05` solo devuelve frases que **citan la regla antigua para decir que fue reemplazada** (10:48, 11:162, 21:46 y 21:92) y un texto de maqueta no relacionado. Sin restos vigentes. Sin conflicto con `docs/01-contexto-repositorio/02` (línea 36 coincide con R20). La memoria `reglas-costo-evm.md` ya tiene tachada la regla vieja. (Solo en 21:92 el título conserva la numeración «5.» de esa lista; no es la «regla 5» antigua.)
- **Tabla «dice hoy / pasaría a decir»** aplicada en 11, 21, 16, 08, 14, 06, 10 y 22 [V por muestreo]. Pendiente conocido: P61 («21 flujos» en `AGENTS.md`, `01-contexto-repositorio/02` y `06-mapa-documental.md`) **[V]**: `grep` confirma «21 flujos» en `AGENTS.md:32` y `06-mapa-documental.md:5`; el estándar de `01-contexto/02` línea 15 no dice la cifra pero se repite en otros sitios.
- `python scripts/verificar-referencias.py docs/04-flujos-de-negocio docs/03-aprendizaje-continuo docs/README.md docs/02-trabajo-activo/README.md` **[V]**: solo menciones preexistentes sin archivo (27 según M.md; no las recontee).

## Hallazgos con evidencia

Severidades: Alta (puede dañar datos, dinero o accesos), Media, Baja.

**H-1 (Alta, [V] parcial + [NV]). La ruta de cálculo de HH extra ×1,25 y HM stand-by nunca corrió con datos reales.** L-bis anota que ninguno de los 32 partes de PS-0000 trae `horasExtra` ni `horasStandby` > 0 (L.md §10, «D RDT…: Observado»). La 100 reescribe `guardar_rdt_parte` y las dos funciones de costo (db/100:34, 177, 456); sus pruebas son de texto/fórmula. El subcontrato manual también está sin datos reales. L5 se dio `Conforme` con la evidencia de «columnas en la vista previa», que no ejerce la escritura ni el recálculo. Cierra: Victor (crear un parte «PRUEBA» con extra y stand-by en PS-0000 y validarlo, comparar con la fórmula; esto cambia el AC de PS-0000 y el plan lo marca como decisión suya).

**H-2 (Media, [V]). El banco de fotos del día: el código lo abre a 13 roles y el flujo 14 dice 4.** `GET /api/proyectos/[id]/fotos-campo` y `GET …/fotos-campo/[fotoId]` usan `puedeVerInformes` (los 13 roles): `fotos-campo/route.ts:19`, `[fotoId]/route.ts:24`; L.md §2 confirma 200 en los 13. El flujo 14 tabla 1, línea 63, dice «Banco de fotos del día»: solo Admin, JP, JOT y SOp, y su nota ¹¹ afirma a la vez que lo ven los 13 roles «salvo el banco de fotos, que es de quienes toman fotos». La fila para la Matriz de permisos (M.md) repite los 4 roles. No hay dinero en las fotos, pero hay una contradicción acceso-código-documento que la política de coherencia de `AGENTS.md` manda resolver. Decide Victor (restringir la ruta GET a `puedeTomarFotoCampo`, o corregir la fila y la nota a 13 roles). La página `/informes/foto` sí exige `puedeTomarFotoCampo` más alcance (`foto/page.tsx:14`).

**H-3 (Media, [V]). «Guardar Mis formatos»: discrepancia ya anotada (chequeo k).** El código permite también a SCo y JCo: `formatos-usuario/route.ts:39` usa `puedeCrearInforme(r) || puedeCrearInformeCostos(r)`, y rechaza con 403 un formato con bloques de Costos sin economía (línea 49). La lista del plan decía los cuatro roles. El flujo 14 ya está escrito con 6 roles (fila de la tabla 2, columnas SCo y JCo con ✓). Es decisión de Victor: confirmar los 6 o quitar SCo y JCo; si los quita, es un cambio de una línea en la ruta y en la fila.

**H-4 (Media, [V]). Trazabilidad de la Punch List: `Observado` sin disposición individual.** El encabezado del plan (línea 7) y el Registro (línea 743) dicen que Victor cierra L1, L2, L6 y L7, pero siguen `Observado` con «lo cierra L» **E2, E3, E4, F1, F3, F4, F5, F6 y G7** (plan líneas 478-497; probablemente también D1–D7, K7, N4, S3/S4 con otro formato) y L.md no los reabre uno a uno (los recorridos de L2 cubren parte, con la cuenta de administrador, y L2 mismo quedó `Observado`). El conteo «124 de 124» cuenta los `Observados` como cerrados, y es coherente con la convención del plan, pero el Gate 2 no sabe qué ítems quedaron realmente sin probar. Cierra: Orquestador (actualizar estado por ítem con la evidencia de L, y listar los que quedan para Victor).

**H-5 (Media, [R]/[NV]). Riesgo de peso de descarga vs. 4,5 MB de Vercel sin cerrar.** G.md mide 20 fotos de ruido (peor caso): 6,0 MB por archivo tras sharp (308 KB por foto a 1000 px) y reconoce que la meta de ~4 MB «NO se logró». L mide 357–362 KB con 6 fotos (≈55 KB por foto) y extrapola 1,1 MB para 20; las dos cifras no son comparables (distinto contenido de foto) y ninguna usa fotos reales de campo. El límite de 4,5 MB es «por confirmar» contra el plan de Vercel. `maxDuration = 60` también por confirmar. Cierra: Victor (fotos reales de un celular, un informe semanal de 20 fotos; confirmar el plan de Vercel).

**H-6 (Media, [R]/[NV]). Recálculo del PR al desplegar (R43).** El PR guarda `costo_materiales_acum` y `costo_subcontratos_acum` al recalcular (db/102:361-365); un PR anterior a la 102 los tiene en 0 hasta recalcular. En PS-0000 se resolvió con «Recalcular PR». En los demás servicios no se hizo [NV]. Sin el recálculo, PR, Dashboard y Costos darían un AC menor que la Curva S (la diferencia observada fue 3.270,51 en PS-0000). Cierra: Victor autoriza una vez `select recalcular_pr_desde_rdt(proyecto_id) from proyecto_pr;` o el botón por servicio, y compara con `db/pruebas/102_comparacion_ac.sql`. El informe COSTOS PS-0000-ID-2 quedó congelado en 93.944,55 (inmutable).

**H-7 (Baja, [V]). `npm test` reescribe el snapshot de Curva S** (5 tandas; M6, M10). Se repite en mi corrida. Falta `.gitattributes` en el worktree (`ls .gitattributes` = no existe).

**H-8 (Baja, [V]). `db/100` repite dos veces el mismo `grant execute … curva_s_proyecto … to authenticated`** (líneas 567 y 569) y la 102 lo revoca después; inofensivo mientras la 102 corra después de la 100 (orden documentado). Si se aplicara la 100 sola sin la 102, `curva_s_proyecto` queda ejecutable por `authenticated`.

**H-9 (Baja, [V]). Lectura de un borrador ajeno y de fotos.** `GET fotos-campo` con `?fecha=` devuelve todas las fotos del servicio, incluidas las asignadas a bloques de un borrador ajeno (`informeId`/`bloqueId` en la fila), por decisión R36. No expone contenido del borrador, pero sí que existe. Aceptado por el Orquestador; se deja constancia.

**H-10 (Baja, [R]). P29: la medición del subcontrato se guarda por `(proyecto_id, descripcion)`**: dos subcontratos con igual descripción en un servicio comparten medición (db/101: `unique (proyecto_id, descripcion)`) [V la restricción]. No visto en datos reales.

**H-11 (Info, [V]). Doble ruta de COSTOS en listados: el GET del listado no responde 403 a un rol sin economía, sino que omite los informes COSTOS** (`informes/route.ts:69-73` con `puedeVerInforme`); detalle y descarga sí dan 403. Coherente con L.md («la lista oculta el COSTOS»). No es defecto.

## (d) Accesos: flujo 14 contra el código

- **COSTOS sin economía = 403 en todas las rutas [V por lectura]**: ver detalle (`cargarInformeVisible`, `ruta.ts:106-108`) → 403; descargar (`descargar/route.ts:41`, vía `cargarInformeVisible`); nueva versión (`nueva-version/route.ts:23-29` y `estados.ts:67`); emitir (`emitir/route.ts:30-31`, `puedeEmitirInformeCostos`); crear (`informes/route.ts:89-90`); editar (`[informeId]/route.ts:56`, `puedeEditarInforme` y bloques con dinero); formatos propios (`formatos-usuario/route.ts:49-50`); asignar foto (`fotos-campo/[fotoId]/route.ts:67`); banco por `?informeId=` (`fotos-campo/route.ts:27`, `cargarInformeVisible`). Todas pasan antes por `validarEscrituraProyecto` (sesión 401, rol 403, alcance 403; `guard-proyecto.ts:11-28`). `puedeVerInformeCostos`, `puedeCrearInformeCostos` y `puedeEmitirInformeCostos` = `puedeVerEconomia` (5 roles) (`permisos.ts:306-317`).
- **Tabla de 13 roles observada en vivo [R, L.md §2]**: administrador, JP y JOT crean y ven COSTOS; SOp crea informes no COSTOS y fotos, 403 en COSTOS; SCo y JCo crean COSTOS, 403 en fotos e informes no COSTOS; los otros 7 roles ven y descargan lo no económico y reciben 403 en todo lo demás, también por URL directa. Coincide con `permisos.ts` (`puedeCrearRdtEstructurado` = administrador, JP, JOT y SOp, `permisos.ts:378-384`) y con el flujo 14 salvo la fila del banco (H-2).
- `registro-accesos.ts:462-482`: `informe-servicio` con `puedeVerInformes` (13) y `foto-campo` con `puedeTomarFotoCampo` (4), acceso rápido nº 8 (línea 199); coincide con las filas del flujo 14 y con el flujo 16.
- Ruta `dashboard/descargar`: `puedeVerDashboard` más alcance; la economía se resuelve por servidor (`puedeVerEconomia` + `tipo_dashboard`), no por parámetro. `pr/subcontratos`: `puedeMedirSubcontratos` (5 roles) y `exigirAlcance`; el `PUT` dispara `recalcularPr` (línea 91). Límite: «borrador ajeno = 404» y «alcance real» **no están observados en vivo** (suplantador `ver-como` conserva el id del administrador, L1) [NV: Victor con segunda cuenta]; `cargarInformeVisible` lo cubre por código (`ruta.ts:105`: borrador ajeno → 404) y por pruebas de ruta [V].

## (e) Sin dinero fuera de Costos

- Código [V]: `bloquesSinDineroSiNoEsCostos` + `esBloqueEconomico`; `exportar/fuente.ts:40` («R5: ningún bloque con dinero sale de un informe que no es COSTOS»); `sin-dinero.test.ts` recorre la salida de todos los formatos no COSTOS y el semanal con la lista de claves de dinero y un patrón de texto (S/, USD, US$, $), con control negativo (COSTOS sí trae dinero). Verde en la corrida.
- Dashboard Parcial [V]: `resolverTipoDashboard(tipo_dashboard, conEconomia)` es la misma función en la página (`dashboard/page.tsx:125`) y en la descarga (`datos-descarga.ts:119`); `descarga-dashboard.test.ts:65` («K5: el Parcial no contiene dinero en PDF ni Excel») y `modo-efectivo.test.ts` verdes. Defecto M9 corregido en 7067a79 y re-verificado en vivo [R, L.md §11: Parcial 0 «US$»; Completo 398].
- Limitación [V]: el detector de dinero es heurístico (claves y patrón de monedas); los textos libres que el usuario escriba (bloques TEXTO/TABLA) no son datos del sistema y no se filtran. Aceptable, no es una fuga de datos de la app.
- En vivo [R, L.md §5]: 18 archivos abiertos; sin «$», «S/», «USD», «costo», «CPI» fuera de COSTOS.

## (f) Migraciones [V por lectura; sin aplicar por mí]

- 098: aditiva e idempotente (`if not exists`), RLS activada sin política en las cuatro tablas, trigger de inmutabilidad con la excepción exacta EMITIDO→REEMPLAZADO, función de código atómica (`on conflict … do update`). Reversa documentada.
- 099: columna nueva + relleno condicionado a nulo (idempotente). Es una escritura de datos (P16), aceptada.
- 100: columnas `horas_extra`, `horas_standby`, `estado_equipo` con `if not exists` y checks (`>= 0`); redefine tres funciones con `create or replace` (`guardar_rdt_parte`, `recalcular_pr_desde_rdt`, `curva_s_proyecto`). `delete from rdt_partes` (línea 83) es parte del reemplazo de un parte dentro de `guardar_rdt_parte` (comportamiento heredado de la versión anterior [R]); lo señalo para que quien aplicó la migración lo haya cotejado [NV].
- 101: tabla nueva, RLS sin política, `check (modo <> 'MANUAL' or monto_manual is not null)`.
- 102: **conserva la parte de la 100** (diferencia puntual y acotada descrita en el chequeo 1b), agrega materiales/subcontratos, y revoca la ejecución de `ac_materiales_subcontratos_al_corte` y `curva_s_proyecto` a `public, anon, authenticated` (db/102:60-61, 495-496; corrección de seguridad P37). Las rutas que usan esas funciones validan sesión, rol y alcance y llaman con el cliente de servicio.
- `db/README.md`: numeración de líneas 099/100 ya corregida en a7e61af. Ninguna migración toca `db/095*`.
- Aplicación real: «Victor aplicó a mano 096 y 098–102» [R, Registro 2026-10-17]. **[NV]** que el esquema real coincida con los archivos; lo puede cerrar Victor con una consulta de solo lectura al catálogo.

## (j) Estados de L y M

- **L1, L2, L6, L7 `Observado`**, con causa escrita: L1/L2 sin segunda cuenta, L6 sin celular real, L7 sin subcontrato manual ni parte con extra/stand-by. **Coincido.** L3, L4, L5 `Conforme`: L3 respaldada (scrollWidth 390, 28 capturas en `03-evidencia/capturas/…/L/`; solo conté el directorio [V]); L4 respaldada [R]; **L5 `Conforme` es optimista** (ver H-1: la 100 no se ejercitó con datos), y L4 indica que la corrección de PDF aa843f5 «no consta re-verificada» en el plan. Sugiero dejar L5 en `Conforme` solo para «las migraciones están aplicadas», y trasladar la prueba de la 100 a L7/Victor.
- **M1–M8 `Conforme`** (M.md usa otros identificadores, `M-inventario`…`M-cierre-filas`, que no coinciden uno a uno con M1–M8 del plan; la correspondencia está en la línea 593 del plan). Mi lectura: M1, M2 (con pendientes R47/P21), M3, M6, M7 y M8 están respaldados por el HEAD de los flujos y por `verificar-referencias`. **M4**: las filas y notas del flujo 14 existen, pero la fila del banco contradice el código (H-2) y la Matriz (el artefacto) no está al día, por lo que lo dejaría `Observado` hasta resolver H-2. **M5**: el propio plan reconoce que el árbol del marco de maquetas (P1) «no se tocó» pese a que el ítem decía «árbol del panel izquierdo»; debería ser `Observado` (pequeño) o redefinirse el alcance a «flujo 16». No es bloqueante.

## (i) Trazabilidad de la política de coherencia (AGENTS.md)

- Toda interfaz/acción nueva tiene fila en el flujo 14 [V]: informes (ver, crear, emitir, versión nueva, COSTOS, Mis formatos, foto, banco, inasistencias, descargas de informe, de inasistencias y del Dashboard), Reporte → Subcontratos, RDT con campos nuevos, y la nota ¹² para el supervisor a cargo. Rutas sin fila propia: `recurso-partidas` (documentada en la nota ¹¹), `pr/recalcular` (preexistente).
- La Matriz de permisos (artefacto) **no está actualizada** (P12): la regla de `AGENTS.md` pide actualizarla «en la misma tarea». Lo único posible hoy es la lista de M.md. **[NV]** (artefacto inaccesible); lo cierra Victor, o él decide P12.
- Flujos 18 y 19 siguen con cambios sin commitear de otros planes; este plan no los toca. Los cambios sin commitear en 06, 14, 16 y `design.md` son de otros planes (M.md §Archivos de otros planes; el diff del árbol sobre HEAD es de 14, 16 y 06: +14/−7 líneas) y los commits de este plan sí están en HEAD.

## (l) Riesgos abiertos para el Gate 2

1. **Recálculo del PR en servicios reales** (H-6): sin él el AC de PR/Dashboard/Costos queda por debajo de la Curva S.
2. **Peso de descarga** (H-5) y `maxDuration=60`, por confirmar con el plan de Vercel.
3. **Lista de celular real L6** (cámara con `capture`, GPS de ~10 s al guardar con ubicación marcada, sin señal, PDF/Word en el celular): sin probar. La cabecera `camera=()` no está verificada; solo se cambió `geolocation=(self)`. Si `camera=()` bloqueara `capture`, la foto de campo no funcionaría en celular [NV: Victor].
4. **Borrador ajeno = 404 sin segunda cuenta** (cubierto por código y pruebas, no en vivo).
5. **Datos de prueba en PS-0000** (H5): informes PS-0000-ID-1 (v1 REEMPLAZADO, v2 EMITIDO, v3 BORRADOR), IS-1, ID-2 (COSTOS EMITIDO, inmutable, congelado en 93.944,55), ID-3, ID-5, seis fotos «PRUEBA». **ID-4 y la descarga de v3 son de origen desconocido** (L.md §8; el Worker no los creó). En el árbol de docs hay además `.playwright-mcp/` con PDF, Word y Excel de prueba sin seguimiento (H1/H6). `tipo_dashboard` de PS-0000 quedó en COMPLETO sin saber si era el valor original (H6).
6. **H-1**: HH extra/stand-by y subcontrato manual con datos reales.
7. **Pendientes de decisión de Victor** en el Registro: unidad HM (R47/P5), BAC del PR contra el del Dashboard (P21), «Mis formatos» (H-3), P1, P61, Matriz (P12).
8. Integración: `local-worker-3` contiene a `main` y a los otros dos Workers; el merge a `main` debería ser un avance rápido. Antes de él, cruzar con el plan «cronograma dentro del sistema» (P44: `local-worker-4`/`-6`, migraciones desde la 103) y con `db/095` sin seguimiento. El `node_modules` del repositorio principal de la app sigue a medias (P45/H3), por lo que el principal no corre pruebas hasta reinstalar.

## Clasificación de hallazgos

- `APLICAR AHORA`
  - **A1.** Corregir «21 flujos» a «22» en `AGENTS.md:32`, `docs/01-contexto-repositorio/06-mapa-documental.md:5` y revisar `01-contexto-repositorio/02` (P61). Mecánico, sin cambio de fondo; lo hace el Orquestador o Victor antes del cierre porque `AGENTS.md` es norma y el Documentador no la toca.
  - **A2.** Actualizar en el plan el estado por ítem de los `Observado` que dependían de L (E2–E4, F1, F3–F6, G7, y los que queden) con la evidencia de L o dejarlos explícitos para Victor (H-4). Orquestador.
  - **A3.** Quitar el reescrito del snapshot de la Curva S de raíz (`.gitattributes` o escritura LF en el test) en la app antes del merge (H-7, M6, M10; reincidencia nº 5 confirmada en esta auditoría). Un Worker, cambio de una línea, sin riesgo de negocio.
  - **A4.** Cerrar la contradicción interna de la nota ¹¹ del flujo 14 («los 13 roles… salvo el banco de fotos») cuando Victor decida H-2 (queda como parte de PROPONER A RESPONSABLE-1; no editar antes de la decisión).
- `PROPONER A RESPONSABLE`
  - **P-R1 (Victor).** H-2: banco de fotos, 13 roles en código o 4 roles en el flujo. Recomiendo restringir la ruta GET (y la foto individual) a `puedeTomarFotoCampo`, que es lo que el flujo, la Matriz y el Spec decían; es un cambio de una línea y deja el código igual que lo escrito.
  - **P-R2 (Victor).** H-3: confirmar los 6 roles de «Guardar Mis formatos» o quitar SCo y JCo.
  - **P-R3 (Victor, con Orquestador).** H-1: probar un parte con HH extra y HM stand-by y un subcontrato manual en PS-0000 y comparar el AC con la fórmula; sin esto, el cálculo de costo real nuevo sigue sin verificación contra datos.
  - **P-R4 (Victor).** H-6: autorizar el recálculo del PR de cada servicio al desplegar la 102 y medir con `db/pruebas/102_comparacion_ac.sql`; resolver P21 y R47 en la misma pasada.
  - **P-R5 (Victor).** H-5: medir el peso con fotos reales de celular y confirmar el límite de Vercel antes de depender de la descarga directa.
  - **P-R6 (Victor).** L1, L2, L6, L7: segunda cuenta (borrador ajeno 404, alcance), celular real, subcontrato manual. Más H5/H6: decidir si los datos de prueba de PS-0000 se desactivan; ID-4 de origen desconocido; confirmar `tipo_dashboard`.
  - **P-R7 (Victor).** M4/M5: aceptar que M4 y M5 queden `Observado`, o redefinir el alcance de M5 a «flujo 16»; y P12 (ver más abajo).
  - **P-R8 (Orquestador).** P44/P45: cruzar los archivos de este plan con el plan del cronograma y con `db/095` antes del merge, y reparar el `node_modules` del repositorio principal (H3/H7).
  - **P-R9 (Orquestador/Victor).** Decidir la limpieza de `.playwright-mcp/` (H1/H6), sin borrar sin orden.
  - **P-R10 (Orquestador).** P29/H-10: decidir si la clave de medición del subcontrato debe incluir un identificador, en un plan futuro.
- `NO PROMOVER`
  - H-8 (grant duplicado en la 100: inofensivo mientras se aplique en orden), H-9 (decisión R36 aceptada), H-11 (comportamiento correcto), P29 como política, P34, P57 (informativas), M1–M4, M7, M8 de «Mejoras» ya trasladadas, P1 (maqueta no normativa; basta que Victor decida si quiere el árbol al día), P60 (error de conteo en la línea de otro plan; avisar al plan dueño), P52 (la prueba `cobertura-pantallas.test.ts` ya existe; el hueco fue la excepción temporal de E, ya resuelta por F).
- `PROPONER SKILL`
  - **S1.** `verificar-permisos-por-rol` (P48, P58, P59): añadir (a) la tabla de 13 roles queda `Observado` hasta que existan las migraciones y la segunda cuenta; (b) `ver-como` conserva el id del administrador y no permite observar «borrador ajeno = 404»; (c) no hay sonda sin efecto para POST de creación (creó la v3 de ID-1). Tres ocurrencias en este plan, con evidencia en L.md.
  - **S2.** `cerrar-tanda`/plantilla de brief (P30, B y Q): exigir en el resumen la tabla esperado/observado o la lectura verificable del Skill, porque un Worker dejó el permiso de COSTOS en 3 roles en vez de 5 y otro aplicó el Skill sin abrirlo (dos casos).
  - **S3.** Aprendizaje de trabajo repetido en 7 tandas (M14–M16, M24): editar archivos en Windows con Write o scripts y no con heredocs de Bash; candidato a una línea en el brief estándar o a un Skill corto.

## Observaciones sobre la política, una por una

Criterio: lo que es un fallo del proceso se clasifica; lo que es deuda del producto o de otro plan no se promueve.

| Fila | Clasificación | Razón y responsable |
|---|---|---|
| P11 | PROPONER A RESPONSABLE | Los docs 09 y 10 del estándar están escritos para opencode; en Claude Code el Orquestador improvisó una equivalencia por tipo de tarea. Victor define la tabla equivalente en el estándar. |
| P12 | PROPONER A RESPONSABLE | Contradicción real entre `AGENTS.md` (la Matriz es la base y se actualiza «en la misma tarea») y la imposibilidad de abrirla. Recomiendo que las tablas del flujo 14 sean la fuente editable por los agentes y que el artefacto se regenere desde ellas, o que Victor lo comparta con la cuenta. Decide Victor en el Gate 2. |
| P17, P44 | PROPONER A RESPONSABLE | Dos planes tocando los mismos flujos (06, 14, 16, `design.md`); coordinación manual con `git merge-file` y cambios ajenos sin commitear en el árbol. Regla de congelación de archivos entre planes en curso: Analista/Victor. |
| P25 | PROPONER A RESPONSABLE | Lint con 9 errores y 22 avisos preexistentes; candidato a corregirse en «Revisión completa de la app». No es fallo de política, es deuda: Victor decide el plan. |
| P26, P43 | PROPONER A RESPONSABLE | El verificador (`scripts/verificar.ps1`) escaló avances rápidos ya pre-autorizados y bloqueó un push de documentación autorizado. Analista del flujo: separar push de docs de push de código y leer la pre-autorización. No lo reproduje [NV]. |
| P30 | PROPONER SKILL (S2) | Reincidente (B, Q); ver S2. |
| P36 | PROPONER A RESPONSABLE | Los Workers no pueden leer las cuentas de prueba y todo ítem con captura queda `Observado`; el estándar (pruebas y evidencia) debe definir cómo se entrega una cuenta sin guardarla en el repositorio. Victor/Orquestador. |
| P42 | PROPONER A RESPONSABLE | El clasificador de permisos de Claude Code bloqueó un `git merge` pre-autorizado; es configuración del entorno, no del estándar. Victor ajusta permisos; no promover a `AGENTS.md`. |
| P48, P58, P59 | PROPONER SKILL (S1) | Ver S1. |
| P52 | NO PROMOVER | Ya existe `cobertura-pantallas.test.ts` (la excepción de E fue puntual). |
| P60 | NO PROMOVER | Error de conteo en la línea de otro plan; avisar al dueño de esa línea. |
| P61 | APLICAR AHORA (A1) | Cifra desactualizada en `AGENTS.md` y mapa documental. |
| P1, P29, P34, P57 | NO PROMOVER | Maqueta no normativa / informativas / sin cambio de política. |
| P5, P21, R47 | PROPONER A RESPONSABLE | No son política: decisiones de datos de Victor (unidad HM, BAC). |

## Pendientes técnicos y documentales

1. Decisiones de Victor: H-2, H-3, P12, P1, P5/R47, P21, H5/H6, R40 y las reglas R23–R47 que el Registro deja a su validación en el Gate 2 (todas escritas en los flujos como «decidida por el Orquestador»).
2. Verificación en vivo pendiente (Victor): L1, L2, L6, L7 (+H-1), peso real de descargas, GPS/cámara en celular.
3. Cierres por el Orquestador: A1–A3 y el estado por ítem (H-4). Pasos 16a a 16c y mensaje de cierre, según `cierre-de-plan-completo`.
4. Fuera de mi acceso **[NV]**: estado real de la base de datos, contenido real de la Matriz de permisos, comportamiento del verificador de acciones, plan de Vercel, y que `db/100` en producción no haya perdido el `guardar_rdt_parte` anterior (Victor, comparando con `pg_get_functiondef`).

## Recomendación

**Apto con condiciones** (`Listo para Gate 2` con las condiciones siguientes). No veo defecto de seguridad ni fuga de dinero en el código revisado: las rutas validan en servidor, COSTOS sin economía da 403 en todas, los formatos no económicos y el Dashboard Parcial no llevan dinero, y las migraciones son aditivas con RLS sin política. La rama puede pasar al Gate 2 si antes: (1) Victor decide H-2 (banco de fotos) y H-3 (Mis formatos); (2) se aplican A1–A3 y se deja por escrito qué `Observado` quedan sin probar (H-4); (3) Victor acepta explícitamente, como riesgos abiertos, H-1, H-5, H-6 y los L1/L2/L6/L7 que él mismo cierra. No recomiendo hacer el merge a `main` ni pedir el despliegue de la 102 sin el recálculo del PR (H-6) ni sin una prueba con datos de la 100 (H-1).
