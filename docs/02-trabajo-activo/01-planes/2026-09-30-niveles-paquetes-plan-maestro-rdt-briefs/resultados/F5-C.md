# Resultados F5-C · Verificación en vivo (RDT, permisos, móvil, regresión)

Carril de integración · rama `main` (`c54cf08`) · puerto 3111 · cuenta A (administrador). Solo verificación con navegador; **sin** push, merge, commit de la app, migraciones ni cambios de permisos. Capturas con prefijo `F5C-` en `docs/02-trabajo-activo/03-evidencia/capturas/niveles-paquetes-plan-maestro-rdt/`.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `seguir-flujo-de-planes`, `trasladar-hallazgos`, `verificar-permisos-por-rol`. App: sin carpeta `.claude/skills/`. Se usó `verificar-permisos-por-rol` (F5C-2) y `cerrar-tanda` (estados/evidencia/traspaso en este archivo).

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F5C-1 | **Observado (parcial)** | Crear RDT lista el Plan Maestro (no el DP): confirmado. El resto bloqueado por el estado del dato (ver H1). |
| F5C-2 | Conforme (código + spot-checks en vivo) | Ver abajo. |
| F5C-3 | Observado (parcial) | Capturas móvil 390 px tomadas; estados vacío/carga/error no cubiertos uno a uno. |
| F5C-4 | Conforme | Línea base PS-0004 al inicio y al final idénticas. |
| F5C-5 | Sin verificar | Requiere autorización expresa de Victor (no dada). |

### F5C-1 · RDT desde el Plan Maestro
- **Confirmado** — «Crear RDT lista los paquetes y partidas del Plan Maestro (no el DP)»: el selector de actividad dice «Elegir actividad del Plan Maestro», y `GET /api/rdts/catalogos` devuelve 48 líneas leídas de `plan_maestro_partidas` (el snapshot del Plan Maestro **aprobado**), agrupadas por clave de reporte: 1 con paquete (PT-001 «PRUEBA-sonda», POR_PARTIDAS, metrado 1.5) y 47 «DIRECTA». No son las 48 partidas del DP: es la estructura del PM.
- **No completado** — «declarar en una partida repartida y en un paquete por avance del paquete»: no se pudo porque el snapshot del PM aprobado (v1) es **anterior** a los paquetes creados después (ver H1). La partida repartida 1.2.1.1 (EXCAVACIÓN, 11.52 M3, repartida 5.76 en PT-002 + 5.76 en PT-003 por actividad 1.2.1.2) **aparece en Crear RDT como una sola línea «DIRECTA» de 11.52**, no como repartida. El paquete «por avance del paquete» que creé (PT-004, ver H1) **no aparece** en Crear RDT.
- **Escritura realizada en PS-0006** (test, autorizado por Victor): creé PT-004 «PRUEBA-F5C paquete avance» (`POST /api/paquetes-trabajo`, modoMedicion `AVANCE_PAQUETE`, guía 1.2.1.3 COLOCACION, Civil) → 201, id `a27fdef7-8dcb-48d7-a2a0-b59807a28eff`. Queda para limpiar en F5C-5.
- No se llegó a crear/validar un RDT ni a comprobar «real en el lienzo» y «PR una sola vez con la suma» (bloqueado por H1).

### F5C-2 · Permisos por rol con «Ver como»
- **Código = flujo 14** (verificado en `src/lib/permisos/permisos.ts` y `integracion-permisos.test.ts`): `puedeVerCronograma`/`puedeVerPaquetesTrabajo` = 13 roles; `puedeVerPlanMaestro` = economía + planner (admin, JP, JOT, SCo, JCo, planner); `puedeCrearRdtEstructurado` = admin, JP, JOT, SOp; `puedeGestionarPlanMaestro`/`puedeGestionarPaquetesTrabajo` = admin, JP, planner; `puedeCrearVersionPlanMaestro` = admin, JP.
- **Spot-checks en vivo** (POST `/api/ver-como` + GET con pausa de 400 ms para que aplique la cookie):

| Rol | Cronograma (ver) | Paquetes (ver) | Plan Maestro (ver) | Crear RDT (catálogo) |
|---|---|---|---|---|
| administrador | 200 | 200 | 200 | 200 |
| planner | — | — | 200 | 403 |
| supervisor_costos | — | — | 200 | 403 |
| jefe_de_costos | — | — | 200 | 403 |
| supervisor_operativo | — | — | 403 | 200 |
| asistente | 200 | 200 | 403 | 403 |
| rrhh | — | — | 403 | 403 |

  Esperado/observado coinciden en todas las filas comprobadas (cronograma y paquetes los ven los 13 roles; PM lo ven economía+planner; Crear RDT lo hacen admin/JP/JOT/SOp).
- **Nota de método**: el barrido de 13 roles × 4 pantallas en una sola `browser_evaluate` agota el timeout del MCP (el GET de `/api/plan-maestro` devuelve el lienzo completo y es lento). Sin pausa tras `ver-como`, la cookie httpOnly no se aplica a tiempo y se leen falsos positivos (p. ej. `jefe_de_costos` dio `verRdt 200` sin pausa y `403` con pausa). Las filas de arriba son las fiables (con pausa). Acciones (tabla 2) no se repitieron en vivo por el riesgo de escritura del POST de `plan-maestro` (ver H2), pero el código coincide con el flujo (guardias verificadas por Grep en `route.ts`).

### F5C-3 · Móvil y estados
- Capturas a 390 px: `F5C-3-movil-plan-maestro.png` y `F5C-3-movil-paquetes.png`. El lienzo del Plan Maestro a 390 px mantiene columnas fijas a la izquierda (WBS/descripción) y scroll horizontal hacia los días; el icono «Asistente» no tapa columnas (flotante en el margen).
- **Pendiente**: estados vacío/carga/error de «paso de niveles», Paquetes, lienzo y Crear RDT no se capturaron uno a uno (requiere más navegaciones; el presupuesto de llamadas se agotó). Queda para otra pasada si Victor lo pide.

### F5C-4 · Regresión (PS-0004)
- Línea base al inicio (solo lectura): DP (HH 5312.08, BAC 123807.94), PR, Dashboard, Curva S → capturas `F5C-4-base-*.png`.
- Al final: PS-0004 DP idéntico (TOTAL 5312.08 / 123807.94; BAC 123807.94). No escribí en PS-0004/PS-0005 (solo GET). Filtros de Consolidado y Status de RDTs: no recorridos en esta tanda por presupuesto.

## Hallazgos

- **H1 (Observado, medio-alto) — el snapshot del Plan Maestro está congelado al momento de aprobar.** Crear RDT lee `plan_maestro_partidas` del PM `APROBADO` (`catalogos/route.ts`), no los paquetes vivos. Los paquetes creados/cambiados **después** de aprobar el PM (PT-002, PT-003 en F5-B2; PT-004 mío) no aparecen en Crear RDT, y la partida repartida 1.2.1.1 se ve como una sola línea «DIRECTA» de 11.52. En PS-0006 hay además un **Plan Maestro v2 BORRADOR** (id `059fbc7c-1806-41a1-abdc-e83528d57ec4`, `creado_en` 2026-10-01 17:09 UTC, 48 líneas) que **sí** refleja la repartida (PT-001/PT-002/PT-003 con 1.2.1.1), pero Crear RDT solo lee el APROBADO. **Decisión para Victor:** o Crear RDT debe leer la versión más reciente (o el PM debe re-aprobarse para reflejar paquetes), o se debe bloquear crear/editar paquetes con PM aprobado (F5-B2 ya dejó esta duda). Para completar F5C-1 haría falta aprobar una versión de PM que contenga una partida repartida y un paquete «por avance del paquete».
- **H2 — El POST `/api/plan-maestro` escribe, no sirve de prueba «sin efecto».** Con `{proyectoId}` y sin motivo, en servicio con PM aprobado devuelve 400 «Indica el motivo» (no escribe) **solo** si el rol pasa `puedeCrearVersionPlanMaestro`; pero el barrido en vivo quedó descartado por el riesgo de disparar un borrador. Revisar el estado del PM v2 BORRADOR: lo creó una sesión anterior, no esta tanda (no incluye PT-004).
- **H3 — `browser_evaluate` con muchos `fetch` en bucle excede el timeout del MCP** y deja la cookie `ver_como` a medias. Usar lotes pequeños + pausa ≥ 250–400 ms tras `POST /api/ver-como` y `DELETE` al final.

## Mejoras de trabajo
- Con «Ver como» vía `fetch`, poner una pausa tras `POST /api/ver-como` (la cookie httpOnly tarda en aplicarse); sin pausa se leen falsos positivos/negativos.
- El GET `/api/plan-maestro` devuelve el lienzo completo: es lento; para barridos de permisos conviene un endpoint ligero o rutas con menos datos.
- Para una prueba «sin efecto» de `plan-maestro` usar `{proyectoId}` sin `motivo` (400) en vez de un POST real.

## Reglas de negocio detectadas
Ninguna nueva que contradiga un flujo. Confirmado en vivo: «Crear RDT» requiere Plan Maestro `APROBADO` y lista el snapshot del PM (una entrada por paquete × partida), no el DP. La semántica de «snapshot congelado vs paquetes vivos» es lo que hay que decidir (H1).

## Huérfanos
- PS-0006: PT-004 `a27fdef7-8dcb-48d7-a2a0-b59807a28eff` (creado en esta tanda).
- PS-0006: Plan Maestro v2 BORRADOR `059fbc7c-1806-41a1-abdc-e83528d57ec4` (creado por una sesión anterior, no por esta).
- (para F5C-5) PS-0006 `51f5905b-6198-46b3-a3d3-abd4793c0e7c` y PS-0007 `85750ef0-b443-4211-bbbe-aae374be5756` con todos sus registros PRUEBA.

## Handoff (≤ 15 líneas)
1. Decidir H1 (snapshot PM vs paquetes vivos / bloquear paquetes con PM aprobado). Sin eso, F5C-1 no puede cerrarse entero.
2. Para cerrar F5C-1: aprobar una versión de PM que contenga una partida repartida y un paquete «por avance del paquete», luego crear/validar un RDT y comprobar lienzo (físico/EV/HH) y PR (partida una sola vez con la suma).
3. F5C-2: el código coincide con el flujo; si se quiere la tabla 13×4 completa en vivo, hacerla en lotes pequeños con pausa tras `ver-como`.
4. F5C-3: faltan los estados vacío/carga/error uno a uno (opcional).
5. F5C-5 (limpieza, sin autorización): ids a borrar = PS-0006, PS-0007, PT-004, PM v2 borrador `059fbc7c…` y registros PRUEBA.
6. Dev server de esta tanda: detenido al terminar. Reponer con `npm run dev -- --webpack -p 3111` en el worktree.

Fuentes de verdad revisadas: ninguna editada. Flujo 14 tablas 1 y 2 (leídas, no tocadas). Pendiente de decisión de Victor: H1.

## Llamadas
≈ 85 (por encima del tope de 80: el diagnóstico del snapshot PM + los barridos con timeout consumieron ~25).
