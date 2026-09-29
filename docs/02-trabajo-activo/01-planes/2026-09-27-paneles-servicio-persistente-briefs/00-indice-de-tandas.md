# Índice de tandas — paneles: servicio persistente (plan v8)

Este archivo es la hoja de ruta del Orquestador: lanza las tandas **una tras otra, en este orden**, sin consultar a Victor salvo en los casos de «Qué debe escalar». Cada tanda = un Worker nuevo (subagente) = una sesión. Reglas comunes: `00-reglas-de-contexto.md`. Medición y metas: `medicion.md`. Detalle de cada tanda: su brief (`f<fase>-tanda-<letra>.md`, ≤ 8 KB). Plan: `../2026-09-27-paneles-servicio-persistente.md` (v8; solo el Auditor y el Orquestador lo leen entero).

Entorno fijo: código en `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-1` (rama `local-worker-1`, creada desde `main` `1942b01`; `.env.local` ya copiado; un solo worktree activo). Estado inicial verificado el 2026-09-29: árbol limpio, sin upstream remoto.

## Tandas (orden de ejecución)

| # | Tanda (brief) | Fase | Ítems PL (n) | Archivos compartidos que toca | Depende de | Estado |
|---|---|---|---|---|---|---|
| 1 | `F0-A` (`f0-tanda-a.md`) | F0 | PL-127, PL-146 (2) | Ninguno (solo evidencia) | Gate 1 aprobado | Pendiente |
| 2 | `F0-B` (`f0-tanda-b.md`) | F0 | LB-02 a LB-05 (0) | Ninguno (solo evidencia) | F0-A cerrada | Pendiente |
| 3 | `F0-C` (`f0-tanda-c.md`) | F0 | PL-147 (1) | Ninguno (solo evidencia) | F0-A cerrada | Pendiente |
| 4 | `F1-A` (`f1-tanda-a.md`) | F1 | PL-51 (1) | `src/lib/config/registro-accesos.ts` (nuevo), `nav-proyecto.ts`, `nav-proyecto.test.ts` | F0-A, F0-B y F0-C cerradas | Pendiente |
| 5 | `F1-B` (`f1-tanda-b.md`) | F1 | PL-50, PL-52 (2) | `grupo-proceso.ts`, `EntornoTrabajoGrupo.tsx`, `PanelSecciones.tsx`, `WorkspaceShell.tsx` (solo rutas fijas), `registro-accesos.ts` | F1-A cerrada | Pendiente |
| 6 | `F2-A` (`f2-tanda-a.md`) | F2 | PL-01, PL-15, PL-16, PL-37, PL-47, PL-66, PL-72 (7) | `WorkspaceShell.tsx`, `servicio-contexto.ts` (nuevo), `registro-accesos.ts`, `(workspace)/layout.tsx` | F1-B cerrada | Pendiente |
| 7 | `F2-B` (`f2-tanda-b.md`) | F2 | PL-02 a PL-04, PL-11, PL-12, PL-14 (6) | `FormularioCronograma.tsx`, `FormularioPaquetesTrabajo.tsx`, `FormularioPlanMaestro.tsx`, `mi-entorno/page.tsx` | F2-A cerrada | Pendiente |
| 8 | `F2-C` (`f2-tanda-c.md`) | F2 | PL-05 a PL-10, PL-13 (7) | `FormularioCrearRdt.tsx`, `TablaStatusRdts.tsx`, `TablaListadoRdts.tsx`, `TablaConsolidadoRdts.tsx`, `ListadoRequerimientos.tsx`, `TablaConsolidadoRq.tsx`, páginas `rdts/*`, `requerimientos`, `logistica/consolidado-rq` | F2-A y F2-B cerradas | Pendiente |
| 9 | `F2-D` (`f2-tanda-d.md`) | F2 | PL-19 a PL-21, PL-70 (4) | 14 páginas con `redirect('/mi-entorno')`, `CabeceraPagina.tsx`, `FormularioCrearRdt.tsx`, `FormularioRequerimiento.tsx`, `proyectos/[id]/{mi-entorno,entorno/[grupo],requerimientos}/page.tsx` | F2-A, F2-B y F2-C cerradas | Pendiente |
| 10 | `F2-E` (`f2-tanda-e.md`) | F2 | PL-17, PL-18, PL-67, PL-69 (4) | Solo correcciones puntuales sobre lo de F2-A a F2-D | F2-A a F2-D cerradas | Pendiente |
| 11 | `F2B-A` (`f2b-tanda-a.md`) | F2B | PL-92, PL-94, PL-119, PL-120 (4) | `permisos.ts` (+ test), páginas y APIs de Cronograma, Paquetes, RDTs, RQ, Recursos, `grupo-proceso.ts` | F2-E cerrada | Pendiente |
| 12 | `F2B-B` (`f2b-tanda-b.md`) | F2B | PL-121, PL-152, PL-154 (3) | `rdts/exportar`, `rdts/partes/[id]/pdf`, `rdts/[id]/archivo`, `requerimientos/exportar` (rutas API), `TablaListadoRdts.tsx`, `ListadoRequerimientos.tsx`, `BotonDescargarPdf.tsx` | F2B-A cerrada | Pendiente |
| 13 | `F3-A` (`f3-tanda-a.md`) | F3 | PL-22 a PL-26 (5) | `WorkspaceShell.tsx` (`ContenidoNav`), componente de chip y sección nuevo en `src/components/ui/`, `registro-accesos.ts`, `FormularioPaquetesTrabajo.tsx`, `paquetes-trabajo/page.tsx` | F2B-B cerrada | Pendiente |
| 14 | `F3-B` (`f3-tanda-b.md`) | F3 | PL-27 a PL-29, PL-49, PL-59, PL-60, PL-62 (7) | `WorkspaceShell.tsx` (bloque Recursos, pie, `CajonMovil`) | F3-A cerrada | Pendiente |
| 15 | `F3-C` (`f3-tanda-c.md`) | F3 | PL-38 a PL-40, PL-48, PL-61, PL-63, PL-64, PL-71 (8) | Componente de chip compartido, `WorkspaceShell.tsx`; correcciones puntuales | F3-A y F3-B cerradas | Pendiente |
| 16 | `F4-A` (`f4-tanda-a.md`) | F4 | PL-30 a PL-34, PL-41, PL-42 (7) | `WorkspaceShell.tsx` (`ContenidoHerramientas`), `PanelSecciones.tsx`, `registro-accesos.ts`, `EntornoTrabajoGrupo.tsx` | F3-C cerrada | Pendiente |
| 17 | `F4B-A` (`f4b-tanda-a.md`) | F4B | PL-102 a PL-107 (6) | `WorkspaceShell.tsx`, `ChatPlaceholder.tsx`, `programas/[id]/portafolios/[portafolioId]/page.tsx` | F4-A cerrada | Pendiente |
| 18 | `F4B-B` (`f4b-tanda-b.md`) | F4B | PL-108 a PL-111 (4) | `ChatPlaceholder.tsx`, `WorkspaceShell.tsx`; ajustes de posición y clases | F4B-A cerrada | Pendiente |
| 19 | `F4B-C` (`f4b-tanda-c.md`) | F4B | PL-112 a PL-116 (5) | Ninguno nuevo (correcciones puntuales en `WorkspaceShell.tsx` / `ChatPlaceholder.tsx`) | F4B-B cerrada | Pendiente |
| 20 | `F5-A` (`f5-tanda-a.md`) | F5 | PL-53, PL-55 a PL-57 (4) | `cobertura-pantallas.test.ts` (nuevo), `registro-accesos.ts` (+ test) | F4B-C cerrada | Pendiente |
| 21 | `F5B-A` (`f5b-tanda-a.md`) | F5B | PL-88 a PL-90, PL-125, PL-174, PL-175 (6) | `permisos.ts` (+ test), `pr/page.tsx`, `dashboard/page.tsx`, `api/proyectos/[id]/tipo-dashboard/route.ts`, `registro-accesos.ts` | F5-A cerrada | Pendiente |
| 22 | `F5B-B` (`f5b-tanda-b.md`) | F5B | PL-91, PL-122, PL-123, PL-153, PL-176 a PL-178 (7) | `dp/page.tsx`, `dp/exportar/route.ts`, `plan-maestro/page.tsx`, `api/plan-maestro/route.ts`, `api/curva-s/route.ts`, `src/app/programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx` | F5B-A cerrada | Pendiente |
| 23 | `F5B-C` (`f5b-tanda-c.md`) | F5B | PL-93, PL-95, PL-98, PL-99, PL-101, PL-124, PL-179 (7) | `registro-costos/page.tsx`, `PanelRegistroCostos.tsx`, `api/proyectos/[id]/registro-costos/route.ts`, `proyectos/[id]/page.tsx`, `programas/[id]/portafolios/[portafolioId]/page.tsx`, `registro-accesos.ts` | F5B-A y F5B-B cerradas | Pendiente |
| 24 | `F5C-A` (`f5c-tanda-a.md`) | F5C | PL-128 a PL-133, PL-135 (7) | `permisos.ts` (+ test), `programas/**`, `proyectos/nuevo`, `api/proyectos*`, `api/programas`, `api/portafolios`, ficha del servicio, `mi-perfil`, `api/perfil` | F5B-C cerrada | Pendiente |
| 25 | `F5C-B` (`f5c-tanda-b.md`) | F5C | PL-134, PL-136 a PL-138 (4) | `permisos.ts`, `dp/page.tsx`, `api/proyectos/[id]/dp/route.ts`, `rdts/status/page.tsx`, `rdts/listado/page.tsx`, `api/rdts/partes/*`, `api/rdts/[id]/route.ts` | F5C-A cerrada | Pendiente |
| 26 | `F5C-C` (`f5c-tanda-c.md`) | F5C | PL-126, PL-139 a PL-143 (6) | `permisos.ts`, `mi-entorno`, `proyectos/[id]/requerimientos/*`, `api/proyectos/[id]/requerimientos/**`, `api/logistica/requerimientos/exportar-004`, `PanelRegistroCostos.tsx`, `api/proyectos/[id]/registro-costos/route.ts` | F5C-B cerrada | Pendiente |
| 27 | `F5C-D` (`f5c-tanda-d.md`) | F5C | PL-144, PL-145, PL-148, PL-151 (4) | `permisos.test.ts`; correcciones puntuales | F5C-A, F5C-B y F5C-C cerradas | Pendiente |
| 28 | `F5D-A` (`f5d-tanda-a.md`) | F5D | PL-157 a PL-162 (6) | `permisos.ts`, `api/recursos/personal/route.ts` y `[id]/route.ts` (nuevo), `TablaPersonal.tsx`, `api/recursos/catalogo-cnc/*` | F5C-D cerrada | Pendiente |
| 29 | `F5D-B` (`f5d-tanda-b.md`) | F5D | PL-163 a PL-169 (7) | `TablaRecursos.tsx`, `api/recursos/route.ts`, `api/recursos/[id]/route.ts` (nuevo), `TablaCatalogoCnc.tsx` | F5D-A cerrada | Pendiente |
| 30 | `F6-A` (`f6-tanda-a.md`) | F6 | PL-43, PL-96, PL-97 (3) | Ninguno (verificación; correcciones puntuales si algo falla) | F5D-B cerrada | Pendiente |
| 31 | `F6-B` (`f6-tanda-b.md`) | F6 | PL-44 a PL-46, PL-54, PL-73, PL-180 (6) | `registro-accesos.ts` (cambio temporal revertido) | F6-A cerrada | Pendiente |
| 32 | `F6-C` (`f6-tanda-c.md`) | F6 | PL-65, PL-117, PL-170 a PL-172 (5) | Ninguno (verificación; correcciones puntuales) | F6-B cerrada | Pendiente |
| 33 | `F6-D` (`f6-tanda-d.md`) | F6 | PL-68, PL-77, PL-78, PL-80 (4) | Ninguno (verificación; correcciones puntuales) | F6-C cerrada | Pendiente |
| 34 | `F6-E` (`f6-tanda-e.md`) | F6 | PL-35, PL-36, PL-74 a PL-76, PL-79, PL-87 (7) | Ninguno (verificación; correcciones puntuales) | F6-A a F6-D cerradas | Pendiente |
| 35 | `F7-A` (`f7-tanda-a.md`) | F7 | PL-58, PL-84, PL-118 (3) | `docs/04-flujos-de-negocio/{16-paneles,01-configuracion,17-chat-agentico}.md`, `docs/01-contexto-repositorio/05-diseno-y-ui.md`, `docs/05-diseno-y-referencias/design.md` | F6-E cerrada + respuestas de Victor | Pendiente |
| 36 | `F7-B` (`f7-tanda-b.md`) | F7 | PL-83, PL-100, PL-149, PL-155, PL-156, PL-173 (6) | `14-accesos-y-restricciones.md`, artefacto https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT | F7-A cerrada | Pendiente |
| 37 | `F7-C` (`f7-tanda-c.md`) | F7 | PL-82 (1) | `docs/04-flujos-de-negocio/{03-entorno,05-rq,06-rdt,08-programa-portafolio-proyecto,09-importar-dp,11-dashboard,12-checklist,15-cronograma,20-plan-maestro,21-curva-s,README}.md` | F7-A y F7-B cerradas + respuestas de Victor | Pendiente |
| 38 | `F7-D` (`f7-tanda-d.md`) | F7 | PL-81, PL-85, PL-86, PL-150 (4) | `docs/03-aprendizaje-continuo/` (archivo nuevo), `docs/README.md`, `docs/02-trabajo-activo/01-planes/README.md`, progreso y evidencia del plan | F7-A, F7-B y F7-C cerradas | Pendiente |

**Tandas de corrección reservadas (no cuentan en las 38):** `F6-R1`, `F6-R2`… El Orquestador las crea solo si tras `F6-E` quedan ítems `Observado` corregibles (un brief mínimo con los IDs y la causa, ≤ 4 KB, mismo formato). Repite hasta 100 % Conforme o hasta que el resto sea externo (p. ej. datos de prueba en Recursos pendientes de Victor).

**Excepciones a «4 a 8 ítems» (decisión de reparto por trabajo, no por ítems):** `F0-B` (entregables de navegador sin fila PL), `F0-A`, `F0-C`, `F1-A`, `F1-B` (F1 es la fase de mayor construcción y tiene 3 ítems), `F2B-B`, `F7-A`, `F7-C` (una fila de PL sobre 11 documentos) y `F6-A` (3 ítems, trabajo de 13 roles).

## Cómo lanzar una tanda

1. Verifica el estado: `git -C "D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-1" status --short` limpio y `git log --oneline -3` (la tanda anterior está commiteada).
2. Lanza un subagente `Worker` con el prompt del plan (§ «Prompt de cada Worker») cambiando solo el ID de tanda. Si la tanda usa las cuentas de prueba, pasa lo necesario desde la memoria (`cuentas-prueba.md`) en el prompt, sin volcarlo a ningún archivo.
3. Al terminar, mide (`medicion.md`) y anota en la tabla de resultados. Si superó una meta, escribe la causa y ajusta el siguiente brief antes de lanzarlo.
4. Lee su mensaje final y su handoff: ítems cerrados, pendientes, preguntas devueltas. Marca el estado en la tabla de arriba (`Cerrada` / `Parcial: <ítems>` / `Bloqueada: <motivo>`).
5. Una tanda `Parcial` se retoma con un Worker nuevo que lee el handoff (no el plan): `<id>-2`, mismo brief más el handoff, solo con los ítems pendientes.

## Autonomía del Orquestador (Victor, 2026-09-29)

> «El Orquestador lanza las tandas una tras otra y decide por su cuenta lo que pueda decidir; solo consulta a Victor por lo que no le corresponda decidir (contradicciones con flujos escritos, cambios de permisos, acciones destructivas o de infraestructura no autorizadas, dudas de negocio).»

### Qué SÍ puede decidir el Orquestador sin consultar

- Orden y momento de lanzar cada tanda; relanzar una tanda cortada por límite de uso o por el tope de llamadas (retomar desde el handoff).
- Dividir una tanda que supera las metas de `medicion.md`, o ajustar un brief (archivos, líneas, comandos verificados, orden interno de ítems) **sin cambiar** el texto de los ítems ni su criterio de evidencia.
- Aceptar un ítem `Observado` cuando la causa es técnica y externa (servidor caído, navegador, cupo) y programar su repetición; crear tandas `F6-R#` de corrección.
- Contestar a un Worker lo que ya está decidido en el plan, el Registro de decisiones, las tablas 1 y 2 del flujo 14 o el artefacto aprobado (citando la fuente).
- Decisiones técnicas dentro de lo aprobado: nombres de funciones, archivos de prueba, puertos, forma del helper, `tipo` en cuerpo o en ruta de la API de Recursos, posición del icono del asistente (con las mediciones del Worker).
- Commits en `local-worker-1` al cerrar cada tanda (con `git add` explícito, sin logs ni capturas pesadas), y anotar en la tabla el commit.
- Crear o completar los archivos de progreso y evidencia del plan a partir de las plantillas (`03-progreso.md`, `04-evidencia.md`) y registrar hallazgos en los apartados obligatorios del plan.
- Elegir entre opciones que el plan ya recomienda (decisiones 3, 4, 5, 6, E1, E3 y supuestos A1 a A11 aprobados con el plan).

### Qué DEBE escalar a Victor (y esperar respuesta; puede seguir con las tandas que no dependan)

- **Contradicciones con flujos escritos:** cada una de C1 a C36 y V1 a V7 antes de que un Worker edite un flujo (tandas F7-A a F7-C). Recomendación: reunirlas en **una sola consulta** con la tabla del plan (acción propuesta y recomendación por fila) antes de lanzar `F7-A`; C35 ya está resuelta.
- **Cambios de permisos** que no estén en las tablas 1 y 2 del flujo 14 / artefacto aprobado, o cualquier hallazgo del Worker que sugiera cambiar quién puede qué; las descargas propuestas A12 y no listadas A13 (PL-155/PL-156).
- **Acciones destructivas o irreversibles:** borrar o escribir datos reales (incluidos registros de prueba en Recursos, PL-158 a PL-172), migraciones o cualquier cambio en `db/`, borrar ramas, worktrees o carpetas.
- **Infraestructura no autorizada:** crear ramas o worktrees nuevos, instalar paquetes, `git push` (la rama `local-worker-1` no tiene upstream: el primer push crea una rama remota), merge, tocar variables de entorno distintas del `.env.local` ya autorizado.
- **Dudas de negocio:** dinero encontrado en pantallas «sin economía» (PL-121), alcance por OT en un portafolio (PL-176), renombrar un cargo con referencias vivas (F5D-B), y toda pregunta que un Worker devuelva y que el plan no resuelva.
- Ediciones del artefacto «Matriz de permisos» más allá de lo ya decidido por Victor; el Gate 2, el Informe de Auditoría y el estado del plan (`Pendiente del Responsable humano` hasta que Victor lo cambie).

### Puntos de pausa previstos

- **Antes de `F5D-A`:** confirmar con Victor si autoriza registros de prueba marcados en Recursos de empresa (si no, PL-158 a PL-172 quedan con el camino feliz `Observado`).
- **Antes de `F7-A`:** consulta única de contradicciones y confirmación de descargas (A12, A13) y de la autorización de commit en `main` de `pg_control_proyectos`.
- **Después de `F6-E`:** informe «qué cambió por rol» (PL-97) a Victor para su revisión; el Gate 2 y el Auditor siguen a F7.

## Mapa ítem → tanda (orden por ID)

PL-01→F2-A; PL-02→F2-B; PL-03→F2-B; PL-04→F2-B; PL-05→F2-C; PL-06→F2-C; PL-07→F2-C; PL-08→F2-C; PL-09→F2-C; PL-10→F2-C; PL-11→F2-B; PL-12→F2-B; PL-13→F2-C; PL-14→F2-B; PL-15→F2-A; PL-16→F2-A; PL-17→F2-E; PL-18→F2-E; PL-19→F2-D; PL-20→F2-D; PL-21→F2-D; PL-22→F3-A; PL-23→F3-A; PL-24→F3-A; PL-25→F3-A; PL-26→F3-A; PL-27→F3-B; PL-28→F3-B; PL-29→F3-B; PL-30→F4-A; PL-31→F4-A; PL-32→F4-A; PL-33→F4-A; PL-34→F4-A; PL-35→F6-E; PL-36→F6-E; PL-37→F2-A; PL-38→F3-C; PL-39→F3-C; PL-40→F3-C; PL-41→F4-A; PL-42→F4-A; PL-43→F6-A; PL-44→F6-B; PL-45→F6-B; PL-46→F6-B; PL-47→F2-A; PL-48→F3-C; PL-49→F3-B; PL-50→F1-B; PL-51→F1-A; PL-52→F1-B; PL-53→F5-A; PL-54→F6-B; PL-55→F5-A; PL-56→F5-A; PL-57→F5-A; PL-58→F7-A; PL-59→F3-B; PL-60→F3-B; PL-61→F3-C; PL-62→F3-B; PL-63→F3-C; PL-64→F3-C; PL-65→F6-C; PL-66→F2-A; PL-67→F2-E; PL-68→F6-D; PL-69→F2-E; PL-70→F2-D; PL-71→F3-C; PL-72→F2-A; PL-73→F6-B; PL-74→F6-E; PL-75→F6-E; PL-76→F6-E; PL-77→F6-D; PL-78→F6-D; PL-79→F6-E; PL-80→F6-D; PL-81→F7-D; PL-82→F7-C; PL-83→F7-B; PL-84→F7-A; PL-85→F7-D; PL-86→F7-D; PL-87→F6-E; PL-88→F5B-A; PL-89→F5B-A; PL-90→F5B-A; PL-91→F5B-B; PL-92→F2B-A; PL-93→F5B-C; PL-94→F2B-A; PL-95→F5B-C; PL-96→F6-A; PL-97→F6-A; PL-98→F5B-C; PL-99→F5B-C; PL-100→F7-B; PL-101→F5B-C; PL-102→F4B-A; PL-103→F4B-A; PL-104→F4B-A; PL-105→F4B-A; PL-106→F4B-A; PL-107→F4B-A; PL-108→F4B-B; PL-109→F4B-B; PL-110→F4B-B; PL-111→F4B-B; PL-112→F4B-C; PL-113→F4B-C; PL-114→F4B-C; PL-115→F4B-C; PL-116→F4B-C; PL-117→F6-C; PL-118→F7-A; PL-119→F2B-A; PL-120→F2B-A; PL-121→F2B-B; PL-122→F5B-B; PL-123→F5B-B; PL-124→F5B-C; PL-125→F5B-A; PL-126→F5C-C; PL-127→F0-A; PL-128→F5C-A; PL-129→F5C-A; PL-130→F5C-A; PL-131→F5C-A; PL-132→F5C-A; PL-133→F5C-A; PL-134→F5C-B; PL-135→F5C-A; PL-136→F5C-B; PL-137→F5C-B; PL-138→F5C-B; PL-139→F5C-C; PL-140→F5C-C; PL-141→F5C-C; PL-142→F5C-C; PL-143→F5C-C; PL-144→F5C-D; PL-145→F5C-D; PL-146→F0-A; PL-147→F0-C; PL-148→F5C-D; PL-149→F7-B; PL-150→F7-D; PL-151→F5C-D; PL-152→F2B-B; PL-153→F5B-B; PL-154→F2B-B; PL-155→F7-B; PL-156→F7-B; PL-157→F5D-A; PL-158→F5D-A; PL-159→F5D-A; PL-160→F5D-A; PL-161→F5D-A; PL-162→F5D-A; PL-163→F5D-B; PL-164→F5D-B; PL-165→F5D-B; PL-166→F5D-B; PL-167→F5D-B; PL-168→F5D-B; PL-169→F5D-B; PL-170→F6-C; PL-171→F6-C; PL-172→F6-C; PL-173→F7-B; PL-174→F5B-A; PL-175→F5B-A; PL-176→F5B-B; PL-177→F5B-B; PL-178→F5B-B; PL-179→F5B-C; PL-180→F6-B

Cobertura verificada por script el 2026-09-29: 180 ítems abiertos asignados exactamente una vez; PL-181 cerrado (`No aplica`); total 181.
