# Reglas de contexto para todo Worker de este plan

Basadas en las del plan de paneles (`2026-09-27-paneles-servicio-persistente-briefs/`), ajustadas a **varios Workers a la vez**. Un Worker de fase entera llegó a 156–191 llamadas; en tandas de ~80 el total bajó a ~28M. Lecciones: `docs/03-aprendizaje-continuo/2026-09-30-plan-paneles-servicio-persistente-tandas.md`.

## Una tanda = un Worker = una sesión

- Recibes **una** tanda (`<id>.md` de esta carpeta), la terminas y **cierras**; el Orquestador lanza un Worker nuevo para la siguiente.
- Meta: ~**80 llamadas**; a las ~60 sin terminar, cierras lo que tienes y escribes el handoff (pasarse no es un fallo). Si la sesión se corta, el siguiente retoma desde el handoff.

## Qué leer (y qué no)

1. Este archivo y **tu brief**. No leas los briefs de otras tandas.
2. Los `contrato-c*.md` que tu brief nombre (índice en `00-contratos-tecnicos.md`): **solo esos**. Te permiten avanzar sin esperar a otro carril.
3. `00-indice-de-tandas.md` § «Matriz de propiedad de archivos»: lee tu fila. **Nunca edites un archivo que no es tuyo.**
4. De la app (`D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`): `AGENTS.md` (687 bytes) y `CLAUDE.md` (626 bytes), **enteros** (Next 16, con cambios de API: consulta `node_modules/next/dist/docs/` con Grep del tema). Verifica contra el código antes de afirmar.
5. Si tocas interfaz: la **maqueta aprobada** de F0 que tu brief nombre (`docs/05-diseno-y-referencias/mockups/`) y `design.md` con `offset`/`limit` solo en las secciones que el brief indique (34 KB: nunca entero).
6. Si el brief lo pide: tablas 1 y 2 del flujo 14 (una vez; no se copian). Código con `offset`/`limit` o Grep; no releer lo ya leído.

**No leer** el plan completo (`2026-09-30-niveles-paquetes-plan-maestro-rdt.md`) salvo un ítem por **Grep de su ID** (`F3A-2`, etc.), ni los Specs completos, salvo que el brief diga la sección.

## Entorno y carriles

- Cada carril tiene **su** worktree, rama y puerto de dev (tabla en `00-indice-de-tandas.md`); trabajas solo en el tuyo. Las ramas 2, 3 y 4 las crea el Orquestador **solo con la autorización de Victor** (Gate 1), desde `main` (`45c9e0a`). Diseño (F0) y documentación (F5-D) trabajan en `pg_control_proyectos` (`main`) y **no** usan worktree de la app.
- El `.env.local` ya está autorizado para copiarse a cada worktree (autorización permanente de Victor): **no lo leas ni muestres sus valores**.
- `node_modules` es un enlace al del repositorio principal: dev y build con `--webpack` (`docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md`). Dev: `npm run dev -- --webpack -p <tu puerto>`. Build: `npx next build --webpack`. Comandos verificados en `package.json`: `npm test` (`vitest run`), `npm run lint`, `npm run build`. **Lint: se compara contra el total medido en `main`**, no contra cero; `npm test` y `npx tsc --noEmit` deben quedar verdes.
- Windows: puertos y procesos con PowerShell; detén solo el servidor que iniciaste. Logs: últimas 30 líneas, sin commitear.

## Migraciones

- Solo escribes `db/NNN_*.sql` **dentro del rango de tu carril** (índice). Si tu tanda tiene migraciones, **las aplicas tú** siguiendo `00-protocolo-migraciones.md` (autorizado por Victor, que ya dejó las credenciales); si no las tiene, no aplicas ninguna. Idempotentes, aditivas; nada se borra ni renombra. Un cambio de restricción o de datos existentes va en el handoff como «requiere autorización expresa». No edites `db/README.md` (lo hace F5-A).

## Navegador y cuentas de prueba

- **Solo F5-B y F5-C usan el navegador** (uno a la vez: dos Playwright en paralelo se pisan). Las demás verifican con `vitest`, `tsc`, lint y `next build --webpack`; lo que exija navegador queda `Observado — pendiente de F5` con su lista de comprobación, salvo turno concedido en tu prompt.
- Cuentas A (permisos altos) y B (sin permisos de administración): viven **solo en la memoria del agente**; nunca en archivos del repositorio, evidencia, commits ni chat. No hagas `grep`/`sed`/`cat` sobre `cuentas-prueba.md`; léelo con `Read` y usa solo el valor necesario.
- Prácticas del plan anterior: agrupa todo lo de la cuenta A y luego lo de la B, o usa «Ver como» (`POST /api/ver-como`; cambia roles, **no** el alcance por OT); sin snapshot del login relleno; redirecciones por URL final, no por `fetch`; `403 por rol` = rechazado, `404/400` = pasó la guardia de rol; navegaciones una a una; `textContent()` (hay `uppercase`); una captura por ítem.
- **Solo lectura sobre datos reales.** Las pruebas de escritura se hacen en el servicio de prueba dedicado de F5-B (autorizado por Victor), con registros marcados `PRUEBA-…`.

## Skills (política vigente, flujo paso 8)

- **Al empezar**, todo Worker lista `.claude/skills/` de `pg_control_proyectos` (hoy: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`) y del repositorio de la app (hoy **no tiene carpeta de Skills**; compruébalo) y usa el que aplique, o anota «Skills revisados: ninguno aplica» con el motivo. Lo anotas en la sección «Skills revisados» de tu `resultados/<tanda>.md`; el Orquestador la copia al progreso.
- **`cerrar-tanda`** al final de **toda** tanda. **Adaptación de este plan:** con varios Workers a la vez, sus pasos de estados, evidencia y traspaso (1, 3 y 4) se escriben en tu `resultados/<tanda>.md`, **no** en el plan, la evidencia ni el progreso compartidos; los demás pasos (estados permitidos, fuentes de verdad, limpieza, commit verificado) van igual.
- **`verificar-permisos-por-rol`** en las tandas que tocan permisos por rol: F3-B, F5-A y F5-C (cada brief lo dice). `seguir-flujo-de-planes` lo usa el Orquestador, no el Worker.

## Cierre de tanda (obligatorio; cambia respecto del plan anterior)

Con varios Workers a la vez **nadie edita el mismo archivo compartido**. Por eso:

1. **No edites el plan, el progreso ni la evidencia.** Escribe tu cierre en **un archivo propio**: `2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/resultados/<id-de-tu-tanda>.md` (lo creas tú), con: estado de **tus** ítems (`Conforme` / `Observado` / `No aplica`, con su evidencia), handoff de máx. 15 líneas (qué falta, comandos exactos para retomar, hallazgos, decisiones técnicas), mejoras de trabajo y reglas de negocio detectadas **en el momento**, huérfanos, y **número de llamadas**. El Orquestador consolida esos archivos en el plan, el progreso y la evidencia.
2. Commit en **tu rama** de la app con `git add` explícito (nunca `-A` ni `.`), sin logs, capturas pesadas ni temporales. **Sin push ni merge.** El `resultados/<id>.md` lo commitea el Orquestador en `pg_control_proyectos`. Solo F0 y F5-D commitean en `pg_control_proyectos`, únicamente sobre los archivos que les pertenecen y con `git add` explícito.
3. Último mensaje al Orquestador: ítems cerrados, pendientes, preguntas devueltas y llamadas usadas.

## Cuándo detenerte y devolver una pregunta

No hablas con Victor. **Detente** y devuelve la pregunta al Orquestador (opciones y recomendación) ante: contradicción con un flujo escrito, permisos que las tablas 1 y 2 del flujo 14 no decidan, cambio de un **contrato** o de un archivo ajeno, acción destructiva o irreversible, infraestructura no autorizada (ramas, worktrees, paquetes, push, otros archivos de entorno) o duda de negocio. Antes, deja hecho el commit de lo terminado. **No edites flujos de `04-flujos-de-negocio/` fuera de F5-D** ni sin la fila aprobada de la tabla en bloque del plan.

## Restricciones heredadas

- No cambia quién puede hacer qué: tablas 1 y 2 del flujo 14. Ningún chip ni acceso nuevo. Los archivos **congelados** hasta F5-A y su única excepción están en el índice; para otro cambio ahí, pregunta.
- El motor del PR, el Dashboard y la Curva S no se modifican (`src/lib/pr`, `dashboard`, `curva-s`, `db/053`, `061`, `070`): solo **pruebas** que los lean.
- USD y costo directo. No convertir una estimación en real. No conectar el asistente a datos (flujo 17). Sin credenciales en repositorios. Reutiliza componentes; `design.md` y la maqueta aprobada mandan.
