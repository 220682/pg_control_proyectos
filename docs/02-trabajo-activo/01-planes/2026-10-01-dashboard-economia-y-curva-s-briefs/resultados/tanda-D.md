# Resultados — Tanda D (con Fase T) · Worker 1 · carril `local-worker-5`

Worker 1 · DeepSeek V4.1 Flash · rama `local-worker-5`, worktree `py_control_proyectos_web/.worktrees/local-worker-5`, HEAD `5e773c7`, árbol limpio al cerrar. Dev en **3115** (ya estaba levantado desde este worktree al iniciar; se usó para la verificación y se detuvo al cerrar). Navegador Chrome vía Playwright. Cuentas de prueba leídas con **Read**, nunca impresas. **No se borró nada.**

**Skills revisados:** `pg_control_proyectos/.claude/skills/` = {cerrar-tanda, seguir-flujo-de-planes, trasladar-hallazgos, verificar-permisos-por-rol}; el worktree de la app **no** tiene `.claude/skills`. Usados en vivo: `verificar-permisos-por-rol` (con «Ver como») y `cerrar-tanda`. Capturas en `03-evidencia/capturas/dashboard-economia-y-curva-s/`.

Proyectos usados (existentes; ninguno borrado): **PS-0004** (PM aprobado + RDT), **PS-0007** `PRUEBA-CRONO` (sin PM), **PS-0008** (PM aprobado, sin RDT).

## Fase T

| Ítem | Estado | Evidencia / causa |
|---|---|---|
| F12 | **Observado — no creado** | No se creó el servicio `PRUEBA-DASH-…`: el presupuesto de llamadas se consumió en la verificación en vivo de la Fase D (que exige navegador y capturas) y la creación de extremo a extremo (adjudicar servicio → DP/niveles → partidas → HH/HM con costo → Plan Maestro con asignaciones → RDT validados a ~50 % → marcar/desactivar) no cabe en la ventana. **Faltan** todos esos pasos; no se aplicó SQL ni se tocaron datos. PS-0005 no aparece entre los servicios vigentes. |
| F13 | **Observado (sustancia verificada)** | La estructura completa se vio funcionando en vivo, pero con proyectos existentes, no con un `PRUEBA-DASH`: Dashboard Parcial (PS-0008 con `supervisor_operativo`/`asistente`) y Completo con bloque «Costo real de recursos» (PS-0004/PS-0008 admin); Curva S física y económica (PS-0004); accesos por rol (barrido de 13 roles). Capturas `F03-F04-F05-U05-*`, `U03-F08-F13-*`, `F10-U04-*`, `U04-F09-*`, `E01-F11-*`. |

## Fase D

| Ítem | Estado | Evidencia |
|---|---|---|
| F03 | **Conforme** | PS-0008 tiene `tipo_dashboard=COMPLETO` (admin ve «Costo directo (US$)»); con `supervisor_operativo` el servidor fuerza **Parcial** (sin USD, sin «Costo directo»). Captura `F03-F04-F05-U05-parcial-sin-economia-sup-operativo.png`. |
| F04 | **Conforme** | En Parcial: `US$`=false y `Costo directo`=false por los 8 roles sin economía (barrido DOM); en Parcial solo % físico, matriz sin columnas PV/EV/AC/SPI/CPI y sin dona ni barras de costo. |
| F05 | **Conforme** | Parcial conserva Filtros (corte/orden), `% avance físico`, matriz sin costo, `DIAGNÓSTICO`, `BLOQUE E — PPC Y PARETO DE CNC` y enlace «Ver Curva S». Captura ídem F03. |
| F06 | **Conforme** | `ToggleTipoDashboard` visible en ambos casos; sin economía cada opción va `disabled` + `title` «Solo los roles con datos económicos…» (2 botones, DOM). Con economía (admin) ambas `aria-disabled=false` y alternan (se pasó a Económica sin recargar la URL). |
| F07 | **Conforme** | El enlace de Bloque E usa `hrefCurvaS`; desde Parcial sin economía es `/proyectos/{id}/curva-s?modo=fisica` (DOM); el nav lateral apunta a la página sin `modo` (el servidor deriva física). |
| F09 | **Conforme** | Selector `role="group"` «Modo de la Curva S» siempre visible. Sin economía: «Económica (USD)» con `aria-disabled="true"`, `disabled=false` y `title` (matiz a); «Avance físico (%)» activo. Con economía (admin): ambos `aria-disabled=false`. Capturas `F09-F10-U04-*`, `U04-F09-*`. |
| F10 | **Conforme** | Física dibuja PV — planificado (PV/BAC) y EV — real (EV/BAC), eje «Avance físico (%)»; sin `US$` en eje/tooltip/tarjetas/tabla. PS-0004 muestra EV real al 12.3 %. Captura `F10-U04-curva-s-fisica-real-PS-0004-admin.png`. |
| F11 | **Conforme (con nota)** | Sin PM (PS-0007): banner «Sin Plan Maestro aprobado… queda «Pendiente» y no se dibuja una curva planificada inventada». El «% real con RDT validados» se vio en PS-0004 (con PM); **no hay** proyecto sin-PM-con-RDT en los datos. Captura `E01-F11-*`. |
| U02 | **Conforme** | Opciones deshabilitadas **visibles** con `title` que explica el permiso (toggle Dashboard, DOM). No se ocultan. |
| U03 | **Conforme** | Tabla «Costo real de recursos»: contenedor `overflow-x-auto`, `th` con `scope="col"` y `position:sticky; top:0`; `main` con `max-width: none` (sin `max-w-*`); paleta de tokens. Captura `U03-F08-F13-*` (escritorio) y móvil `R05-U05-*`. |
| U04 | **Conforme** | Un solo eje por modo: económico «US$ acumulado (CD)» (PV/EV/AC) y físico «Avance físico (%)» (PV/BAC y EV/BAC); nunca % y USD juntos. Capturas `U04-F09-*` y `F10-U04-*`. |
| U05 | **Conforme** | En Parcial no quedan huecos ni secciones vacías (0 `section` sin texto) en escritorio y en móvil 390 px; el grid económico se omite entero. |
| E01 | **Conforme** | (sin PM) PS-0007: «Pendiente» sin curva PV. (sin RDT) PS-0008: nota «Sin RDT validados en el rango: la serie real (EV/BAC) está vacía» y EV «—» en la tabla → **matiz b** confirmado. Nota: con BAC=0 el mensaje es «no tiene BAC» (D03), no la nota de serie vacía. |
| E03 | **Conforme** | Forzado de `GET /api/curva-s` con 500 vía interceptación: la UI muestra el mensaje del cuerpo («Fallo de prueba forzado E03») y «Cargando…» (carga atenuada `transition-opacity opacity-50`, sin salto de layout). |
| E04 | **Conforme** | `GET /api/curva-s?…&modo=economica` con `supervisor_operativo` → **403** `{"error":"No tienes acceso a la Curva S económica"}`; la interfaz nunca ofrece el modo (botón `aria-disabled`). |
| V01 | **Conforme** | Con rol sin economía: `modo=economica` → 403 aunque se fuerce; **sin `modo`** → `modo:"fisica"` (determinista) con claves sin `ac` (sin dinero). Con admin: `modo=economica` → 200. |
| V04 | **Conforme (sin sesión) / Observado (OT ajena)** | Sin sesión, `GET /api/curva-s…` → **307** a `/login` (middleware, rechazo intacto). La ruta «OT ajena» no se probó en vivo (ver-como cambia rol, no alcance; el guard `validarEscrituraProyecto` no se tocó en este plan). |
| R01 | **Conforme** | `npm test` = **102 archivos / 1063 pruebas OK** (`integracion-permisos.test.ts` = 5 OK); `npx tsc --noEmit` = exit 0; `npm run lint` = **27 problemas (9E/18W) = baseline de `main`**; `npx next build --webpack` = exit 0. |
| R02 | **Conforme** | Los 5 roles con economía (admin, jefe de proyectos, jefe de oficina técnica, supervisor de costos, jefe de costos) ven Completo con `US$` y «Costo real de recursos» (barrido DOM de los 5). |
| R03 | **Conforme** | Los 13 roles entran al Dashboard y a la Curva S sin bloqueo (barrido DOM; 8 sin economía → Parcial, 5 con economía → Completo). Dashboard del portafolio (admin) carga sin «No tienes acceso». |
| R05 | **Conforme** | Login real admin, escritorio (1440) y móvil (390 emulado por CDP): sin overflow horizontal, sin chips rotos, enlaces de Curva S correctos, paneles coherentes. Capturas móviles `R05-U05-*`. |

### Matices devueltos por la tanda C
- **(a) Confirmado:** el selector de la Curva S usa `aria-disabled` + `title` (no `disabled`), accesible por teclado. El `ToggleTipoDashboard` del Dashboard sí usa `disabled`+`title` (otro componente).
- **(b) Confirmado:** cuando todas las EV del rango son 0, no se dibuja la serie real y aparece la nota «la serie real (EV/BAC) está vacía».

## Handoff (≤15 líneas)
1. Fase D cerrada en su mayoría; capturas agrupadas por pantalla (9 archivos) en `03-evidencia/capturas/dashboard-economia-y-curva-s/`.
2. **F12 no ejecutada**: falta crear el `PRUEBA-DASH-…` de extremo a extremo; no se tocó BD ni se borró nada.
3. Verificado en vivo con PS-0004/PS-0007/PS-0008; PS-0005 no está vigente.
4. V04 OT-ajena queda Observado: el guard no cambió; haría falta sesión con alcance ajeno (López) para probarlo.
5. F11/F13 usan proyectos existentes, no el de prueba marcado (F12).
6. R01 verde: test 1063, tsc 0, lint 27 (9E/18W baseline), build 0.
7. Dos matices de C confirmados.
8. **Presupuesto excedido**: ~108 llamadas (límite ~80).
9. No se tocó código → no hay commit en `local-worker-5` (HEAD sigue `5e773c7`, árbol limpio).
10. Pendiente: decidir si se crea F12 en una tanda nueva o se acepta F13 con datos existentes.

## Mejoras (de trabajo)
- Con 22 ítems de Fase D + Fase T, «una captura por ítem» no cabe en ~80 llamadas: conviene agrupar por pantalla (un archivo para varios IDs) desde el brief.
- `browser_resize` no aplicaba el viewport (seguía 1440); para móvil 390 px hubo que usar CDP `Emulation.setDeviceMetricsOverride`.
- El servidor dev ya estaba levantado en 3115 desde el worktree al iniciar la sesión; se reutilizó y se detuvo al cerrar.

## Reglas de negocio detectadas
- Ninguna nueva. El comportamiento coincide con flujos 16/21 y con PD3/PD5. Aclaración de E01: la nota «serie real vacía» solo aparece cuando hay BAC (>0) y EV=0; si `BAC=0` el mensaje es «Este servicio no tiene BAC…» y no se dibuja gráfico (D03). No se editó ningún flujo (Fase E).

## Observaciones sobre la política
- El presupuesto (~80) está subestimado para una tanda con Fase T + 22 ítems de Fase D con navegador y captura individual. Se excedió (~108). Nadie edita el estándar por su cuenta: queda para clasificación del Auditor / decisión de Victor.

## Carpetas/archivos huérfanos
- Ninguno detectado.

## Fuentes de verdad revisadas
Fuentes de verdad revisadas: `docs/04-flujos-de-negocio/16-paneles.md` (patrón «ver no es acceder» y chips) y `21-curva-s.md` leídos solo por lo verificado; `src/lib/permisos/permisos.ts`, `src/app/api/curva-s/route.ts`, `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`, `TipoDashboard`. **Pendientes de decisión en Fase E** (no editadas aquí): flujo 21 (BAC del modo físico y E01), flujo 14/16/21 con la fila de Curva S física/económica.

## Número de llamadas
**~108** (excede el objetivo ~80).
