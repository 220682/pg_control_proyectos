# Brief — Tanda A: base compartida, supervisor a cargo con columna propia y restricción de ejecución

## Rol, modelo y tanda

Worker 1, Sonnet, esfuerzo medio. Tanda A, Ola 0, carril W1. Subagente «Worker 1 · A». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List PL-01, PL-23, PL-25)

- **A1**: migración `db/099_supervisor_operativo_a_cargo.sql`: `alter table proyectos add column supervisor_operativo_id uuid references perfiles(id)` (nulo permitido) y relleno inicial: para cada servicio, el miembro con rol supervisor operativo de `asignado_en` más reciente (la misma lógica que hoy usa `resolverSupervisorOperativoActual`). Los servicios sin ese miembro quedan en nulo y **no retroceden de estado**. Aditiva, reversa en comentario, línea en `db/README.md`. Nueva `src/lib/proyectos/supervisor-operativo.ts` con `obtenerSupervisorACargo` (lee la columna). `api/proyectos/[id]/datos/route.ts` deja de usar la resolución por «último miembro» — hecho: una sola función usada por todos — prueba: unitaria.
- **A2**: `api/proyectos/[id]/confirmar-transicion/route.ts` exige columna no nula al pasar a `EJECUCION`; si falta → 400 con «No se puede pasar a Ejecución: el servicio no tiene supervisor operativo a cargo. Asígnalo en Editar servicio». Con los tres requisitos (Plan Maestro aprobado, checklist completo, supervisor) pasa igual que hoy — prueba: de ruta.
- **A3**: `PATCH datos` escribe `supervisor_operativo_id`; comprueba en servidor que la persona tenga el rol supervisor operativo (si no → 400) y la agrega como miembro del servicio (alcance). Con el servicio en `EJECUCION` se puede **cambiar** pero **no vaciar** (400). Corrige además que reasignar a alguien que ya era miembro no lo volvía el actual — prueba: de ruta (cambiar, vaciar, rol equivocado).
- **A4**: el botón de confirmar la transición lista lo que falta (Plan Maestro, checklist, supervisor a cargo) — archivos: `proyectos/[id]/page.tsx`, `confirmar-transicion.tsx` — prueba: unitaria del armado de faltantes; captura solo si puedes levantar la app (si no, «Observado: sin captura»).
- **A5**: extraer de `dashboard/page.tsx` el cargador de datos (PR, plan maestro, corte, recursos) a `src/lib/dashboard/cargar-dashboard.ts`, **sin cambio visible** — prueba: unitaria; la página usa el cargador.
- **A6**: extraer de `api/curva-s/route.ts` el cálculo a `src/lib/curva-s/cargar-curva-s.ts`; la ruta delega — hecho: respuesta JSON idéntica — prueba: `curva-s.test.ts` y comparación antes/después.
- **A7**: regresión: `npm test`, `npm run lint`, `npm run build`, `npx tsc --noEmit`.
- **A8**: en `src/lib/permisos/permisos.ts`, `puedeMedirSubcontratos` (los 5 roles con economía: administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos, jefe de costos — reutiliza el criterio de `puedeVerEconomia`/`puedeVerPr`) y `puedeVerInasistencias` (los 13 roles con rol conocido), con pruebas unitarias por rol. Las usarán otros Workers sin tocar ese archivo.

Ya resuelto por Victor (no se pregunta): columna propia para el supervisor; en ejecución se cambia, no se vacía; relleno inicial desde el miembro actual; la transición lo exige y se valida en servidor.

## Rama, worktree y puerto

Rama `local-worker-1`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-1` (ya al día con `main` y con `.env.local` copiado por el Worker git). Trabaja **solo** dentro de ese worktree. Si necesitas levantar la app, usa el puerto 3011.

## Qué leer, y qué no

1. `src/app/api/proyectos/[id]/datos/route.ts` (busca `resolverSupervisorOperativoActual`).
2. `src/app/api/proyectos/[id]/confirmar-transicion/route.ts`.
3. `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx` y `src/app/api/curva-s/route.ts`.
4. `db/096_rdt_borradores_e_inasistencias.sql` (forma de una migración reciente) y `db/README.md`.
5. `src/lib/permisos/permisos.ts` (solo las funciones de economía y roles).
6. Flujos (repositorio de documentación `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`): `08-*.md` párrafos «Transición `EN_PLANEACION` → `EJECUCION`» y «Estructura de niveles y paso a ejecución»; `14-accesos-y-restricciones.md` línea de la nota ³.

**No leas** el plan completo, maquetas, otros flujos ni el estándar.

## Qué puede trabajar

Puede crear o editar: `db/099*`, una línea en `db/README.md`, `src/lib/proyectos/supervisor-operativo.ts`, `src/lib/dashboard/cargar-dashboard.ts`, `src/lib/curva-s/cargar-curva-s.ts`, `src/lib/permisos/permisos.ts`, las rutas `datos` y `confirmar-transicion`, `dashboard/page.tsx`, `api/curva-s/route.ts`, `proyectos/[id]/page.tsx`, `confirmar-transicion.tsx`, y sus pruebas.

**No toca:** `src/lib/pdf/hoja.ts`, `src/lib/rdts/**`, `api/rdts/**`, `registro-accesos.ts`, `next.config.ts`, `package.json`, `db/095*` (sin seguimiento, es de otra tarea: **no lo agregues a ningún commit**), flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica la migración** a ninguna base: solo escribe el archivo (la aplica el Orquestador).

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-1` (nunca a `main`) al cerrar A1–A4 y al cerrar A5–A8; nunca a medias de un ítem. Agrega los archivos por nombre (`git add <ruta>`), nunca `git add -A`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/A.md`, con la plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` de ese repositorio. No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Primera migración libre: **099** para esta tanda (098 es de la tanda B; 097 existe en `main`). Re-verifica con `ls db/` y `git log --oneline -3 main` antes de crear el archivo.
- Hoy el supervisor a cargo **no es una columna**: `resolverSupervisorOperativoActual` toma, entre los miembros con rol supervisor operativo, el de `asignado_en` más reciente.
- `confirmar-transicion` valida solo Plan Maestro `APROBADO` y checklist completo, con compare-and-swap del estado; errores con 400.
- Tablas nuevas o columnas: RLS como en la 095/096 (sin política; solo el servidor lee). Aquí solo se agrega una columna a `proyectos`.
- Base de prueba: Victor no indicó ninguna → la migración queda «revisada, no probada en base» en el resumen.

## Skills que debe usar

`cerrar-tanda` al terminar (en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`: léelo y sigue su secuencia; el commit de documentación no lo haces tú, lo hace el Orquestador).

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra el ítem en curso, haz commit y push y escribe el traspaso. Punto de corte: A1–A4 / A5–A8.

## Cómo registra hallazgos y preguntas

Los hallazgos van a tu resumen, en los cinco grupos. Si encuentras un conflicto con una regla de negocio o algo que el brief no decide (por ejemplo, un servicio en `EJECUCION` sin supervisor que el relleno no puede resolver), **detente y devuélvelo como pregunta** en tu respuesta final; no lo decidas tú.

## Criterios de salida

A1–A8 en `Conforme` u `Observado` con causa; `npm test`, `lint`, `build` y `tsc --noEmit` en verde; commits en `local-worker-1` comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final al Orquestador en ≤ 25 líneas: estado por ítem, commits, resultado de los cuatro comandos, preguntas abiertas.
