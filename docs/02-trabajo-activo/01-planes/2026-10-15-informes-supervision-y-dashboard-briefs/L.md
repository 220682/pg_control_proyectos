# Brief — Tanda L: Integración y verificación en vivo

## Rol, modelo y tanda

Worker 3, Sonnet, esfuerzo medio. Tanda L, última de W3 (tras F, G y Q). Subagente «Worker 3 · L». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **L1**: tabla de permisos por rol observada (Skill `verificar-permisos-por-rol`, suplantación `ver-como` y llamadas sin efecto) para informes, fotos, Costos, descargas y transición.
- **L2**: recorrido Playwright de A (diario y semanal, tres formatos y uno propio, emitir, versión 2), B y C con las dos cuentas.
- **L3**: 390 px de listado, nuevo, editor, foto de campo y Dashboard.
- **L4**: cada archivo descargado abierto y revisado contra la vista previa.
- **L5**: las migraciones 099, 098, 100, 101 y 102 (en ese orden; la 102 después de la 100 y la 101) se aplican antes de esta tanda (Orquestador, una por una, con verificador y autorización); aquí se comprueban.
- **L6**: lista para que Victor pruebe la cámara en un celular real.
- **L7**: el RDT con extra y stand-by, la pestaña Inasistencias y el subcontrato manual entran al recorrido y a la tabla de permisos observada, y se comprueba que el AC del PR, el de la Curva S, el del Dashboard y el del formato Costos coinciden al mismo corte (cuentas de prueba, 390 px).

Punto de corte: L1–L3 / L4–L7.

## Inicio de sesión y cuentas de prueba (léelo primero)

**Ningún Worker puede leer las cuentas de prueba** (P36): no viven en el repositorio ni se te entregan. **El inicio de sesión lo coordina el Orquestador con Victor**: antes de lanzarte, el Orquestador confirma con Victor cómo se abre la sesión de Playwright (sesión ya iniciada por Victor o un paso manual suyo). Si no hay sesión, **detente y pídela al Orquestador**; no busques, no leas ni escribas credenciales. **L es la que verifica en vivo, con las migraciones ya aplicadas**: si al empezar L5 muestra que alguna de 098 a 102 no está aplicada, detente y avisa; no la apliques tú. Todo ítem que dependa de captura o sesión y no se pueda hacer queda «Observado» con la causa.

## Rama, worktree y puerto

Rama `local-worker-3`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-3`. **Parte de `local-worker-3` con `local-worker-1` incorporada** (D en el primer corte; G al final, la incorpora el Worker git antes de L): verifica con `git log --oneline -10` que están E, F, Q y los commits de D y G de `local-worker-1`; si falta algo, detente y avisa. Puerto 3013 para la app. Mientras W3 corre, no cambies de rama ni toques otros worktrees.

## Qué leer, y qué no

1. Skill `verificar-permisos-por-rol`: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/verificar-permisos-por-rol/SKILL.md` (obligatorio; mecanismo `ver-como` y llamadas sin efecto).
2. Los resúmenes de cierre de las tandas ya hechas, en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/` (A, B, C, D, E, F, G, O, R, P, Q y, si están, N, H, S, I, J, K): ahí están las tablas de permisos «Observado» que L debe cerrar y los hallazgos pendientes.
3. `src/lib/permisos/permisos.ts` (funciones `puede*Informe*`, `puedeVerInasistencias`, `puedeMedirSubcontratos`) y `src/lib/config/registro-accesos.ts`, para derivar lo esperado por rol.
4. La maqueta `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/05-diseno-y-referencias/mockups/informes-supervision.html` como referencia visual de lo esperado en 390 px y escritorio.

**No leas** el plan completo ni los flujos salvo `14-accesos-y-restricciones.md` en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/` (tabla esperada).

## Qué puede trabajar

Es una tanda de verificación: ejecutar la app, Playwright (capturas en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/03-evidencia/capturas/2026-10-15-informes-supervision-y-dashboard/`, una subcarpeta por tanda; esa carpeta la fija el Orquestador), llamadas sin efecto con `ver-como`, abrir los PDF, Word y Excel descargados. Corregir en código solo defectos **menores y propios de W3** (`src/app/(workspace)/proyectos/[id]/informes/**`, `src/components/informes/**`, `src/app/api/inasistencias/**`, `src/lib/config/registro-accesos.ts`); todo defecto en carpetas de W1 o W2 se anota como hallazgo y se devuelve al Orquestador.

**No toca:** `db/**` y **no aplica migraciones** (las aplica Victor a mano o el Orquestador con autorización), `db/095*` (sin seguimiento: no lo agregues a ningún commit), `src/lib/informes/tipos.ts`, `permisos.ts`, `package.json`, `next.config.ts`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. No crea ni borra datos reales de servicios de producción: usa los de prueba que indique el Orquestador.

## Dónde deja su entrega y su evidencia

- Código (si hubo correcciones menores): commit y push a `local-worker-3` (nunca a `main`) al cerrar L1–L3 y al cerrar L4–L7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/L.md`, con una captura por ítem, la tabla esperado contra observado de los 13 roles, el cuadre del AC en cuatro lugares (L7) y la lista de L6 para el celular. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Reglas a observar: `COSTOS` sin economía = 403 (listado, detalle y descarga por URL directa); lo crean y emiten los 5 roles con economía (P30); crear informe y foto de campo: administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo; ver y descargar: los 13 roles; Inasistencias: los 13, dentro de su alcance; el borrador ajeno = 404; el emitido es inmutable (409 al editar).
- L7: AC del PR = AC de la Curva S = AC del Dashboard = AC del formato Costos al mismo corte (materiales y subcontratos incluidos a nivel servicio, R20); el costo por partida no los incluye.
- Los formatos distintos de `COSTOS` no llevan dinero en ningún byte, también en los archivos descargados (L4).
- Cámara: la cabecera `camera=()` puede no afectar a `capture` (**no verificado**); L6 solo prepara la lista para que **Victor** pruebe en un celular real; el GPS depende de P7.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador) y `verificar-permisos-por-rol` (obligatorio en L1 y L7). Comandos tras cualquier corrección: `npm test` (si solo cambia por fin de línea el `.snap` de curva-s, restaurarlo con `git checkout`); `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar nuevos, anota el conteo); `npx next build --webpack`. `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

L1–L7 en `Conforme` u `Observado` con causa (un ítem sin sesión o sin migración aplicada queda «Observado», nunca «Conforme»); evidencia por ítem; comandos en verde si hubo cambios; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen con la tabla de 13 roles. Respuesta final en <= 25 líneas: estado por ítem, commits, resultados, preguntas abiertas.
