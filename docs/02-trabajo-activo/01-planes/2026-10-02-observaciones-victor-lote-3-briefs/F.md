# Brief Tanda F — Worker 3 (Plus por lógica nueva; flash no autorizado para esta)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Carril:** rama `local-worker-4`, worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-4` (NO ramas nuevas, NO `main`, NO merge, NO push). **Precondition:** aplica TÚ las migraciones `090` y `092` (una por vez, orden 090→092) siguiendo `2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-protocolo-migraciones.md` (candado, transacción, conteos, script `migrar_F.py` fuera del repo, sin secretos; si el clasificador deniega: NO la rodees, anota el comando exacto y detente). Verifica después: `catalogo_disciplinas` con 8 filas y columnas de `092` en `rdt_actividades`. **No arrancar hasta que cierre la Tanda E** (mismo carril, Commits secuenciales).

## Qué hacer (completar F5, plan § Reglas confirmadas 6-10 y O10-O13)

1. **RDT: declaración por paquete** — al declarar, el paquete completo figura como `WBS="PQ-001"` (no por partida individual); partidas **directas** (fuera de paquetes) se declaran sueltas. Persistir en `rdt_actividades` con las columnas de `092`.
2. **Cálculo automático del metrado del paquete** al declararlo (regla 10; coherente con `distribuirMetradoPaquete` de `8b33cdd`).
3. **Libertad de WBS para C/NC y equipos**: no exigir D previa con WBS vinculado (permitir WBS libre según flujo 06).
4. **Plegable por disciplina** con el catálogo de 8 (090) en la pantalla RDT, e icono flotante con reserva de espacio (patrón F4-A).
5. **Pendiente heredado de G:** reposicionamiento automático de los RDT declarados cuando se edita una actividad del cronograma (nuevas fechas/metrados) — implementar en el `PATCH` de `/api/cronograma/actividades/[id]` (o donde la regla 4 del plan lo ubique: al aprobar el nuevo Plan Maestro). Si el diseño no es evidente desde el plan/flujo 06, **detener y preguntar al Orquestador**, no improvisar.
6. G-R1 abierta: el aviso de impacto hoy cuenta borradores y validados; si Victor responde "solo VALIDADOS" antes de tu tanda, aplica esa regla; si no, deja el comportamiento actual y repórtalo.

## Reglas

- No tocar Lienzo del Plan Maestro (firma de E) más de lo estrictamente necesario; no `middleware.ts`; no cambiar permisos.
- G-M2/G-O1: una llamada viva mínima por cada camino nuevo (SSR/API sin navegador, puertos del worktree, sin secretos en salida).
- Validación: `npx tsc --noEmit` · `npx vitest run` de suites de rdt/cronograma/plan-maestro · verificación en vivo con datos de prueba (PS-0007/PS-0009 o servicios `PRUEBA-…` nuevos; nunca tocar datos reales).
- Commits claros en `local-worker-4`. Cierre en `resultados/F.md` con hallazgos en las 4 categorías.
