# Informe de Auditoría — Dashboard por economía, Curva S con selector y costo real de recursos

> Archivo propio del Auditor, mismo nombre base que el plan (`docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s.md`). Formato `06-informe-auditoria.md`. No implementa, no hace merge, no aprueba en nombre de Victor.

## Alcance auditado

Plan `2026-10-01-dashboard-economia-y-curva-s` (fases A, T, B, C, D, E + tandas T2, T3, P03, E2), su Spec («Spec / SDD», criterios 1–8), su Punch List (40 ítems) y su libro de hallazgos. El código vive en `py_control_proyectos_web`, rama `local-worker-5` (worktree `.worktrees/local-worker-5`); la documentación, en `pg_control_proyectos` (`main`). Fecha de auditoría: 2026-10-02.

## Material revisado

- Plan completo (incluido el Spec, la tabla (iii) del Gate 1, las decisiones PD1–PD6, la Punch List y el libro de hallazgos M1–M9 / RB1–RB8 / OP1–OP9).
- Progreso y evidencia homónimos + carpeta de capturas `03-evidencia/capturas/dashboard-economia-y-curva-s/` (16 PNG: `F03-F04-F05-U05-*`, `U03-F08-F13-*`, `F10-U04-*`, `U04-F09-*`, `E01-F11-*`, `F13-R02-*`, `R05-*` ×2, `T2-F13-*` ×2, `T2-V04-*`, `T3-F13-*` ×4).
- Los 8 resúmenes de tanda en `…-briefs/resultados/` (A, B, C, D, T2, T3, E, P03).
- Flujos 11, 14, 16 y 21 ya editados (commit `d262395`) y la nota ¹ del flujo 14.
- Código del worktree `local-worker-5` (solo lectura): `src/lib/permisos/permisos.ts`, `src/lib/config/matriz-base-flujo14.ts`, `src/lib/dashboard/costo-recursos.ts`, `src/components/dashboard/CostoRealRecursos.tsx`, `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`, `src/app/api/curva-s/route.ts`, `src/lib/curva-s/curva-s.ts` y `ToggleTipoDashboard.tsx`.
- `scripts/verificar-referencias.py` (núcleo y carpetas del plan), el índice de `03-aprendizaje-continuo/` y los 6 archivos M1–M8.
- Skills citados en el plan: `seguir-flujo-de-planes` (Orquestador), `verificar-permisos-por-rol` (A/D/T2/T3), `cerrar-tanda` (A–P03), `trasladar-hallazgos` (E/E2).

## Verificación de rama (primer chequeo)

Comprobado con `git log` / `git branch --contains` reales, no de memoria. Repo `py_control_proyectos_web`:

```text
git log --oneline -6 local-worker-5
  98df43c tanda P03: permisos.test.ts vuelve a comparar las filas Dashboard Parcial/Completo y Curva S fisica/economica contra el flujo 14
  5e773c7 tanda C: Curva S con selector economica/fisica, contrato GET /api/curva-s?modo y serie fisica PV/BAC, EV/BAC
  94a5f79 tanda B: Dashboard Parcial sin economia (PD5), Bloque E en ambos (PD6), enlace Curva S ?modo=fisica y bloque Costo real de recursos
  d40cd74 tanda A: Dashboard y Curva S a 13 roles, puedeVerCurvaSEconomica (5) y Parcial forzado en servidor

git branch --contains d40cd74 / 94a5f79 / 5e773c7 / 98df43c
  * local-worker-5   (única rama en los cuatro casos)

git log --oneline -3 main
  35ac5dd fix(cronograma): trazado del binario nativo de @napi-rs/canvas …   (NINGUNO de los 4 commits del plan)
git status (main)
  On branch main / up to date with origin/main / sin merge en progreso (`.git/MERGE_HEAD` no existe)
```

- **Resultado: CONFORME.** La implementación está solo en `local-worker-5` (worktree `.worktrees/local-worker-5`, HEAD `98df43c`), no en `main`; `main` termina en `35ac5dd` sin los commits del plan y está limpio, sin merge en progreso. Existieron sesiones de Worker separadas por tanda (A, B, C, D, T2, T3, P03) con sus resúmenes en `…-briefs/resultados/`.
- Los commits del plan son de código en el repo de la app; en el repo documental el plan y sus traslados están en `main` (`d262395`, `2ec79de`, `0e757f3`, `ffeeb74`, `e5bc395`, `f3af620`, `9f0c4dd`), como corresponde al flujo.
- Nota: `main` de la app tiene cambios sin commitear (`db/README.md` y `db/090`–`092`) **ajenos a este plan** (lote de migraciones de otro trabajo). No forman parte de la implementación auditada y no se tocaron.
- Incidencia menor: el resumen de la tanda E cita un commit `1e3f09d` («Ronda E2») que **no aparece** en `main` del repo documental (solo `f3af620` y `9f0c4dd`). Parece un hash alucinado en el resumen; el contenido sí está en `f3af620`/`9f0c4dd`. Se reporta como observación de trazabilidad (no afecta el contenido ni la implementación).

## Cumplimiento de SDD, plan, Punch List y evidencia

### (a) Dashboard sin economía no muestra ningún dato monetario — PD5

**CONFORME.** En `page.tsx` todo lo monetario está detrás de `puedeEditarTipo` (`puedeVerEconomia`):

- Cabecera «Costo directo (US$)» (`page.tsx:306`), chip semáforo (`:310-314`), tarjetas KPI de dinero BAC/PV/EV/AC/SPI/CPI (`:340-396`, solo queda «% avance físico»), dona de composición (`:400-419`), gráfico de desempeño por partida (`:408-417`), bloque «Costo real de recursos» (`:441`), resumen ejecutivo (`:445`) y columnas de costo de la matriz (`mostrarCosto={puedeEditarTipo}`, `:425`).
- Orden «mayor desviación de costo» forzado a `WBS` sin economía (`:157-160`).
- **Se conservan**: filtros (`FiltrosDashboard`), % avance físico (`:333-339`), matriz sin costo (`:421-426`), diagnóstico (`:428-439`), Bloque E PPC/Pareto (`:443`) y enlace a Curva S (`hrefCurvaS`, `:286-288`).
- Confirmado en vivo (tanda D): 8 roles sin economía → Parcial sin `US$` ni «Costo directo»; matices (a) y (b) de C confirmados.

Nota de hallazgo (no crítico, ver OP2): el prompt de auditoría del plan decía «los 10 KPI»; la lista cerrada PD5 oculta **6 KPI**. Se implementó la lista del brief.

### (b) «Costo real de recursos» suma exactamente el AC sin doble contar el legacy

**CONFORME.** `reconciliarCostoRecursos` (`costo-recursos.ts:45-56`): `subtotalRecursos = Σ filas`, `total = ac` (leído del mismo `indicadoresProyecto.ac` que el KPI), `diferencia = ac − Σ`, `mostrarDiferencia` solo si `|diferencia| ≥ 0.005`. Las filas son `pr_recursos` MO+HM (`page.tsx:273-279`). `CostoRealRecursos.tsx`: fila «Sin resolver / diferencia» solo bajo `mostrarDiferencia` (`:77-90`); el balde `costo_legacy_sin_partida_acum` es **nota informativa no sumable** (`:104-109`), nunca fila. Verificado en vivo (T3, PS-0009): Σ MO+HM = Total = KPI AC = US$ 297,76, sin fila «Sin resolver».

### (c) 403 en modo económico sin permiso y `modo=fisica` sin USD

**CONFORME.** `route.ts:45-56`: `modo` inválido → 400; `modo=economica` sin `puedeVerCurvaSEconomica` → 403 «No tienes acceso a la Curva S económica»; sin `modo` se deriva por permiso (determinista). En `modo==='fisica'` (`:149-171`) la respuesta devuelve `{serie:[{fecha,pvPct,evPct}]}` sin `pvAcum`/`evAcum`/`acAcum` ni `bac` (el BAC se lee en servidor y no se devuelve). Verificado en vivo: 403 forzado; sin `modo` → `fisica` sin claves de dinero.

### (d) Flujos 11, 14, 16 y 21 y matriz derivada

**CONFORME (con dos observaciones).**

- Flujo 11: «Los dos Dashboards» (Parcial sin dato económico, Completo con él), interruptor deshabilitado fijo en Parcial, chip a 13 roles, §«Costo real de recursos» (MO/HM, Total = AC, «Sin resolver», legacy no sumable), orden forzado a WBS, enlace `?modo=fisica`. Coincide con la tabla (iii).
- Flujo 14: tabla 1 con «Dashboard — Parcial» (13) / «Dashboard — Completo» (5) y «Curva S — avance físico (%)» (13) / «Curva S — económica (USD)» (5); nota ¹ reescrita (Completo = exactamente los 5, sin «estado objetivo / plan futuro»). Coincide con `permisos.ts`.
- Flujo 16: chip Dashboard y Curva S a 13 roles en «Estado de implementación», restricción económica dentro de la pantalla. Sin cambio de texto de reglas.
- Flujo 21: dos modos con selector, % planificado PV/BAC y % real EV/BAC, endpoint con `modo=` y 403, eje único por modo, BAC del modo físico leído y no devuelto, BAC=0 sin serie. Coincide con `curva-s.ts` y `route.ts`.
- Matriz derivada: `MATRIZ_BASE_FLUJO14` (`dashboard: TODOS`, `curva-s: TODOS`; `pr`/`costos-servicios`/`dp`/`plan-maestro` con economía) y `derivarMatrizAccesos()` con 0 diferencias (`matriz-accesos.test.ts`); `permisos.test.ts` compara 9 filas × 13 = 117 celdas contra el flujo 14 (commit `98df43c`).
- **Observación 1 (control de coherencia):** en el working tree de `pg_control_proyectos` el flujo 14 tiene un diff **sin commitear** (nota ¹¹ «Editar vs Reemplazar», +3 líneas) ajeno a este plan. La versión **commiteada** (`d262395`) es la que coincide con la implementación; recordar commitear/descartar ese diff aparte. No lo toqué.
- **Observación 2 (menor, textual):** el flujo 11 §«Costo real de recursos» dice «Filas: `pr_recursos` de tipo MO … y HM … **con** `descripcion`»; si la descripción es NULL (deuda `db/055`), la fila igual puede existir con descripción NULL. Precisar que «con descripcion» es la fuente, no una condición de filtro.
- El artefacto «Matriz de permisos» lo revisa Victor (**P05**, pendiente) — fuera del alcance del Auditor.

### (e) Verificación en vivo (dos caras) y evidencia ítem por ítem

**CONFORME.** `verificar-permisos-por-rol` se usó en modo estático (A) y en vivo con «Ver como» (D, T2, T3); las dos caras quedaron cubiertas: 5 roles con economía (Completo + ambas curvas) y 8 sin economía (Parcial + curva física). Se forzaron 403 (modo económico, PATCH `tipo-dashboard`) y OT ajena (López → 403 en API y «No tienes acceso» en pantalla). Toda la Punch List tiene fila en `03-evidencia/` con estado, método y enlace; 39 ítems Conforme y **P05 Pendiente** (Victor). Capturas reales (16). Toda la implementación está verificada en vivo salvo: F11 «% real sin PM» (no existe proyecto sin-PM-con-RDT en los datos; nota documentada) y E02 «bloque vacío en vivo» (cubierto por test; los datos de prueba tienen recursos).

### (f) Trazabilidad del libro de hallazgos (segundo chequeo)

**CONFORME.** Ninguna fila queda en `Registrada` (solo aparecen las 2 menciones de la definición del estado, en la leyenda y en el resumen de E). Verificado que los traslados existen de verdad:

- M1–M6, M8 → archivos en `03-aprendizaje-continuo/` (`2026-10-02-desacoplar-prueba-permisos-del-flujo-14.md`, `…-agrupar-capturas-por-pantalla…`, `…-viewport-movil-con-cdp-emulation.md`, `…-reservar-llamadas-importacion-datos-reales.md`, `…-tecnicas-de-verificacion-en-vivo-con-playwright.md`) e índice de la carpeta actualizado (commits `2ec79de`, `f3af620`).
- RB1–RB8 → integradas en 11/14/16/21 (commit `d262395`), dentro de la estructura de cada flujo, no como nota al final.
- M7/M9 y OP1–OP9 → `Pendiente de decisión` (decide Victor en Gate 2), como corresponde.
- Huérfanos: ninguno (confirmado por A–D y por el Documentador; no se borró nada).
- `verificar-referencias.py` (núcleo): **45 archivos, 0 huérfanos, 0 enlaces rotos**, 2 menciones sin archivo preexistentes y ajenas → R06 Conforme.

## Verificación de la revisión de fuentes de verdad por fase

- Fase A: leyó flujo 14 (tablas y notas) y `design.md`; no editó flujos (correcto). Fase B: flujos 11/21. Fase C: flujo 21 y `design.md`. Fase D/T2/T3: flujos 16/20/21 y código en solo lectura; no editaron flujos. Fase E: editó 11/14/16/21 según la tabla (iii) aprobada y verificó contra el código del worktree. Fase E2: trasladó M4–M9 y selló el libro.
- Sin ediciones no autorizadas de reglas permanentes. Las 2 contradicciones no anticipadas (nota ¹ y «sin interruptor / plan futuro») estaban listadas y se resolvieron por (iii) filas 7 y 2.

## Clasificación de hallazgos

### APLICAR AHORA

- **Ninguno sobre fuentes centrales.** La documentación de negocio ya quedó trasladada y coherente con el código; no hay un cambio confirmado pendiente de pasar a documentación permanente.

### PROPONER A RESPONSABLE

- **OP1 — ventana doc↔código con `npm test` rojo.** Cuando la prueba compara la doc por ruta absoluta y la doc se edita después (E), entre A y E conviven tests ajustados y doc vieja. La tensión se resolvió ajustando el mapa en A y restaurándolo en P03. Propuesta: definir en el estándar cómo se maneja esa ventana (p. ej. que el ajuste de la prueba vaya en la misma tanda que la edición del flujo). Decisión de Victor.
- **OP2 — «10 KPI» vs 6 en el prompt de auditoría del plan.** Corregir la referencia de PD5 (la lista cerrada oculta 6 KPI); el brief mandó. Afecta la plantilla/redacción de los planes.
- **OP3 — PD4 dice `disabled`; se implementó `aria-disabled`.** Alineado a U01 y `design.md` §254 (accesible por teclado). Confirmar PD4 como `aria-disabled` para todo el plan.
- **OP5 / OP7 / OP9 — presupuesto de llamadas.** ~80 subestimado para Fase T + 22 ítems de Fase D con navegador (~108); la creación de datos de extremo a extremo necesita presupuesto propio (~68–71 y dividible). Ajustar la estimación de briefs de tandas con navegador/creación real de datos.
- **OP6 — merge en progreso sin Gate 2 hallado al retomar (se abortó).** `local-worker-5` → `main` de la app, 17 archivos staged, sin Gate 2; se abortó y `main` volvió a `35ac5dd` (0/0). Riesgo de proceso: reforzar el control de que el merge solo ocurre tras Gate 2 (p. ej. recordatorio en el paso 16a y verificación del verificador de acciones). Decisión de Victor.
- **Técnicos/negocio:** **OP8** (bug fuera de alcance: `PATCH /api/plan-maestro` APROBAR con `asignaciones` inline valida pero no persiste → plan APROBADO con PV 0) → decidir plan de arreglo aparte o `planes-futuros.md`. **M7/M9** (conocimiento de API: APROBAR no reemplaza a GUARDAR_ASIGNACIONES; payload mínimo de RDT) → si se conservan, integrarlos en los flujos 20/06 (hoy sin destino).
- **P05** — artefacto «Matriz de permisos» (solo Victor).
- **Borrado de PS-0009** y sus filas/archivos por `proyecto_id` (lista exacta en `resultados/tanda-T2.md` y `tanda-T3.md`). El agente no borra nada.
- **Commit del diff sin commitear del flujo 14** (nota ¹¹) y aclarar el hash alucinado `1e3f09d` del resumen de E.

### NO PROMOVER

- **OP4 — interpretación de E01 «EV=0 → no dibujar serie real + nota».** Confirmada en D como comportamiento correcto y ya reflejada en el flujo 21 (RB7); no es un cambio del estándar.
- **F11 y E02 como limitaciones de datos.** No existe proyecto sin-PM-con-RDT ni bloque vacío en vivo; cubiertos por nota y por test. No exigen cambio de política.
- **Hash `1e3f09d` del resumen de E.** Error puntual de cita, no una práctica; basta la nota para no repetirlo.

### PROPONER SKILL

- **Skill «verificación en vivo con Playwright»** (agnóstico): agrupar capturas por pantalla (M2), `Emulation.setDeviceMetricsOverride` para móvil (M3), `setInputFiles` con fixture ASCII (M5), «Ver como» por API + reload (M6) y re-`fetch` dentro de cada evaluate (M8). El procedimiento ya se repitió en las tandas D, T2 y T3 y hoy vive en 3 archivos de `03-aprendizaje-continuo/`; es candidato natural a Skill reusable.
- **Ajustar/crear Skill existente** `verificar-permisos-por-rol`: añadir el patrón de reservar llamadas para la importación de datos reales (M4) y el orden «dato real → permiso → captura» ya usado.
- **Cerrar-tanda**: incorporar la regla de presupuesto propio para tandas con Fase T (OP5/OP7/OP9).

## Pendientes técnicos y documentales

1. **P05**: artefacto «Matriz de permisos» actualizado por Victor (misma tarea).
2. **Borrado de PS-0009** por Victor (servicio `da33f1fa-…`, paquete `4bd2dd7c-…`, PM v1 `3e7e030a-…` / v2 `7074c8ad-…`, RDTs `92a97e60-…` / `4fc8d898-…`, DP/cronograma y archivos de storage `documentos-proyecto/da33f1fa-…/`).
3. **Bug OP8**: `PATCH /api/plan-maestro` APROBAR con asignaciones inline no persiste → plan de arreglo aparte o `planes-futuros.md`.
4. **M7/M9**: decidir si se conservan como conocimiento de API y, si aplica, integrarlos en los flujos 20/06.
5. **OP6**: reforzar el control del merge post-Gate 2.
6. **Flujo 14**: commitear/descartar el diff sin commitear de la nota ¹¹ (ajeno a este plan).
7. **Commit del código** `local-worker-5` → `main` (Worker git, solo tras Gate 2).
8. **Decisión de Victor sobre OP1–OP9** en el Gate 2.

## Recomendación

**Listo para Gate 2.** Los dos chequeos son Conforme: la implementación está aislada en `local-worker-5` (no en `main`, sin merge), y el libro de hallazgos no tiene filas en `Registrada` con traslados verificados. Los criterios 1–8 del Spec se cumplen (a–f Conforme), con tres observaciones no bloqueantes: OP2 (texto del prompt), la precisión textual del flujo 11 sobre `descripcion` y el hash alucinado en el resumen de E. Quedan pendientes de decisión humana P05, el borrado de PS-0009, el bug OP8 y M7/M9, más la clasificación OP1–OP9. No se autoriza ningún merge: eso es el Gate 2 con autorización explícita de Victor.

---

*Auditor · 2026-10-02 · repo documental `pg_control_proyectos`, `main`. No se implementó nada, no se hizo merge, no se aprobó en nombre de Victor. Este informe se commiteó solo (archivo propio) y se pusheó a `origin/main`.*
