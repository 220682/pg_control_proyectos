# Reglas de contexto para todo Worker de este plan

Basadas en las del plan de paneles (`2026-09-27-paneles-servicio-persistente-briefs/00-reglas-de-contexto.md` y su `medicion.md`), ajustadas a **varios Workers a la vez**. Motivo de las tandas: un Worker de fase entera llegó a 156–191 llamadas y 625–682k de contexto; repartido en tandas de unas 80 llamadas el total bajó a ~28M. Lección del plan anterior que aplica aquí: `docs/03-aprendizaje-continuo/2026-09-30-plan-paneles-servicio-persistente-tandas.md`.

## Una tanda = un Worker = una sesión

- Recibes **una** tanda (`<id>.md` de esta carpeta), la terminas y **cierras**. No sigues con la siguiente: el Orquestador lanza un Worker nuevo.
- Meta: unas **80 llamadas**; a las ~60 sin terminar, dejas de abrir frentes, cierras lo que tienes y escribes el handoff. Pasarse de la meta no es un fallo.
- Si la sesión se corta, el siguiente Worker retoma desde el handoff, no desde el plan.

## Qué leer (y qué no)

1. Este archivo y **tu brief**. No leas los briefs de otras tandas.
2. `00-contratos-tecnicos.md`: **solo** las secciones que tu brief nombre (Grep del título «## C1», «## C2»…). Es lo que te permite avanzar sin esperar a otro carril.
3. `00-indice-de-tandas.md` § «Matriz de propiedad de archivos»: lee tu fila. **Nunca edites un archivo que no es tuyo.**
4. Del repositorio de la app (`D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`): `AGENTS.md` (687 bytes) y `CLAUDE.md` (626 bytes), **enteros** (verificado 2026-09-30: advierten que es Next 16, con cambios de API respecto de lo que conoces; consulta `node_modules/next/dist/docs/` **con Grep del tema**). Si verificas contra el código, hazlo antes de afirmar.
5. Si tocas interfaz: la **maqueta aprobada** de F0 que tu brief nombre (está en `docs/05-diseno-y-referencias/mockups/`) y `docs/05-diseno-y-referencias/design.md` con `offset`/`limit` solo en las secciones que el brief indique. Nunca entero (34 KB).
6. Si el brief lo pide: tablas 1 y 2 de `docs/04-flujos-de-negocio/14-accesos-y-restricciones.md` (una vez). No se copian a ningún archivo.
7. Código con `offset`/`limit` o Grep. No releer lo ya leído.

**No leer** el plan completo (`2026-09-30-niveles-paquetes-plan-maestro-rdt.md`) salvo un ítem por **Grep de su ID** (`F3A-2`, etc.), ni los Specs completos, salvo que el brief diga la sección.

## Entorno y carriles

- Cada carril tiene **su** worktree y **su** rama; trabajas solo en el tuyo:

| Carril | Rama | Worktree | Puerto de dev |
|---|---|---|---|
| 1 Niveles | `local-worker-1` | `…\py_control_proyectos_web\.worktrees\local-worker-1` | 3111 |
| 2 Plan Maestro | `local-worker-2` | `…\.worktrees\local-worker-2` | 3112 |
| 3 Paquetes | `local-worker-3` | `…\.worktrees\local-worker-3` | 3113 |
| 4 RDT | `local-worker-4` | `…\.worktrees\local-worker-4` | 3114 |

  Las ramas 2, 3 y 4 las crea el Orquestador **solo con la autorización de Victor** (Gate 1), desde `main` (`45c9e0a`). Las tandas de diseño (F0) y de documentación (F5-D) trabajan en `pg_control_proyectos` (`main`) y **no** usan worktree de la app.
- El `.env.local` ya está autorizado para copiarse a cada worktree (autorización permanente de Victor): **no lo leas ni muestres sus valores**.
- `node_modules` es un enlace al del repositorio principal: dev y build con `--webpack` (`docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md`). Dev: `npm run dev -- --webpack -p <tu puerto>`. Build: `npx next build --webpack`. Comandos verificados en `package.json`: `npm test` (`vitest run`), `npm run lint`, `npm run build`. **Lint: se compara contra el total medido en `main`**, no contra cero; `npm test` y `npx tsc --noEmit` deben quedar verdes.
- Windows: puertos y procesos con PowerShell nativo; detén solo el servidor que iniciaste. Logs: últimas 30 líneas, no se commitean.

## Migraciones

- Solo escribes archivos `db/NNN_*.sql` **dentro del rango de tu carril** (`00-indice-de-tandas.md`). **Nunca aplicas** una migración: Victor las pega en el SQL Editor y confirma cada una. Idempotentes (`if not exists`), aditivas; nada se borra ni se renombra. Un cambio de restricción o de datos existentes se señala en el handoff como «requiere autorización expresa».
- No edites `db/README.md` (lo actualiza F5-A).

## Navegador y cuentas de prueba

- **Solo F5-B y F5-C usan el navegador para verificar en vivo** (un solo carril a la vez: dos Playwright en paralelo se pisan). Las demás tandas verifican con `vitest`, `tsc`, lint y `next build --webpack`; lo que exija navegador queda `Observado — pendiente de F5` con la lista de comprobación. Excepción: el Orquestador puede conceder un turno de navegador en tu prompt de lanzamiento.
- Cuentas A (permisos altos) y B (sin permisos de administración): viven **solo en la memoria del agente**; nunca en archivos del repositorio, evidencia, commits ni chat. No hagas `grep`/`sed`/`cat` sobre `cuentas-prueba.md`; léelo con `Read` y usa solo el valor necesario.
- Prácticas (aprendizaje del plan anterior): agrupa todo lo de la cuenta A y luego lo de la B, o usa «Ver como» (`POST /api/ver-como`, cambia roles pero **no** el alcance por OT); no tomes snapshot del login relleno (puede mostrar credenciales autocompletadas); comprueba redirecciones con la URL final, no con el código de `fetch`; `403 por rol` = rechazado, `404/400` = pasó la guardia de rol; encadena las navegaciones una a una; lee con `textContent()` (hay etiquetas con `uppercase`); una captura por ítem como máximo.
- **Solo lectura sobre datos reales.** Las pruebas de escritura se hacen en el servicio de prueba dedicado de F5-B (autorizado por Victor), con registros marcados `PRUEBA-…`.

## Cierre de tanda (obligatorio; cambia respecto del plan anterior)

Con varios Workers a la vez **nadie edita el mismo archivo compartido**. Por eso:

1. **No edites el plan, el progreso ni la evidencia.** Escribe tu cierre en **un archivo propio**: `2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/resultados/<id-de-tu-tanda>.md` (lo creas tú), con: estado de **tus** ítems (`Conforme` / `Observado` / `No aplica`, con su evidencia), handoff de máx. 15 líneas (qué falta, comandos exactos para retomar, hallazgos, decisiones técnicas), mejoras de trabajo y reglas de negocio detectadas **en el momento**, huérfanos, y **número de llamadas**. El Orquestador consolida esos archivos en el plan, el progreso y la evidencia.
2. Commit en **tu rama** de la app con `git add` explícito (nunca `-A` ni `.`), sin logs, capturas pesadas ni temporales. **Sin push ni merge.** El `resultados/<id>.md` lo commitea el Orquestador en `pg_control_proyectos`. Solo F0 y F5-D commitean en `pg_control_proyectos`, únicamente sobre los archivos que les pertenecen y con `git add` explícito.
3. Último mensaje al Orquestador: ítems cerrados, pendientes, preguntas devueltas y llamadas usadas.

## Cuándo detenerte y devolver una pregunta

Eres un subagente y no hablas con Victor. **Detente** y devuelve la pregunta al Orquestador (con opciones y recomendación) ante: una contradicción con un flujo escrito, un cambio de permisos que las tablas 1 y 2 del flujo 14 no decidan, un cambio en un **contrato** o en un archivo que no es tuyo, una acción destructiva o irreversible, infraestructura no autorizada (ramas, worktrees, paquetes, push, otros archivos de entorno), o una duda de negocio. Antes de devolver, deja hecho el commit de lo terminado y avanza con lo que no dependa de la pregunta. **Nada de editar flujos de `04-flujos-de-negocio/` fuera de F5-D** ni sin la respuesta registrada de Victor a cada cambio (la tabla en bloque del plan).

## Restricciones heredadas

- No cambia quién puede hacer qué: tablas 1 y 2 del flujo 14. Ningún chip ni acceso nuevo en este plan; `permisos.ts`, `registro-accesos.ts` y sus pruebas, `nav-proyecto.ts`/`.test.ts`, `panel-*`, `matriz-accesos*`, `db/README.md` y `package.json` están **congelados** hasta F5-A. Única excepción: el carril 2 añade `puedeCrearVersionPlanMaestro` a `permisos.ts` en F3-B (ver el índice). Si necesitas otro cambio ahí, pregunta.
- Mantén el motor del PR, el Dashboard y la Curva S sin modificar (`src/lib/pr`, `src/lib/dashboard`, `src/lib/curva-s`, `db/053`, `db/061`, `db/070`): solo **pruebas** que los lean.
- Todo en USD y costo directo. No convertir una estimación en real. No conectar el asistente a datos (flujo 17).
- Sin credenciales en repositorios. Reutiliza componentes existentes; `design.md`, `05-diseno-y-ui.md` y la maqueta aprobada mandan.
