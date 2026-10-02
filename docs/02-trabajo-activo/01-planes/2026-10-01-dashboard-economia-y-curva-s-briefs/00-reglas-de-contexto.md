# Reglas de contexto para todo Worker de este plan

Plan: `../2026-10-01-dashboard-economia-y-curva-s.md`. Basadas en las del plan de niveles (`2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-reglas-de-contexto.md`). Un plan con **un solo Worker de código** (su solo carril toca `permisos.ts` y `registro-accesos.ts`); el Documentador y el Auditor trabajan en `pg_control_proyectos` (`main`).

## Una tanda = un Worker = una sesión

- Recibes **una** tanda (`<id>.md` de esta carpeta), la terminas y **cierras**; el Orquestador lanza un Worker nuevo para la siguiente.
- Meta: ~**80 llamadas**; a las ~60 sin terminar, cierras lo que tienes y escribes el handoff.

## Qué leer (y qué no)

1. Este archivo y **tu brief**. No leas briefs de otras tandas.
2. De la app (`D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`): `AGENTS.md` y `CLAUDE.md` **enteros**.
3. Del plan (`../2026-10-01-dashboard-economia-y-curva-s.md`): **solo ítems por Grep de su ID** (`F04`, `PD5`, etc.), nunca completo.
4. Los flujos de negocio **solo** los que tu brief nombre, y solo las secciones indicadas.
5. Código con `offset`/`limit` o Grep; no releer lo ya leído. Si tocas interfaz, la sección de `docs/05-diseno-y-referencias/design.md` que tu brief indique.

**No leer** el progreso ni la evidencia completos, ni los Specs/planes de otros temas.

## Entorno, rama y worktree

- Carril único: rama `local-worker-5`, worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-5`, puerto dev **3115**. Trabajas solo ahí.
- `.env.local` ya copiado (autorización permanente de Victor): **no lo leas ni muestres sus valores**.
- `node_modules` es junction al repo principal: dev y build con `--webpack` (`npm run dev -- --webpack -p 3115`; `npx next build --webpack`). Comandos: `npm test` (`vitest run`), `npx tsc --noEmit`, `npm run lint`.
- **Lint se compara contra el total medido en `main`**, no contra cero. `npm test` y `tsc` deben quedar verdes.
- Windows/PowerShell: detén solo el servidor que inicies; logs sin commitear.

## Migraciones y datos

- Este plan **no tiene migraciones** (el Spec lo dice). No crees ni apliques SQL.
- **Solo lectura** sobre datos reales en A–C. La verificación en vivo con escritura es la Fase D/T, con el proyecto de prueba autorizado.

## Navegador y cuentas de prueba

- **Solo la Fase D usa el navegador/Playwright** (login real y «Ver como»). En A–C, lo que exija navegador queda `Observado — pendiente de D` con su lista de comprobación.
- Cuentas de prueba: viven solo en memoria del agente; nunca en el repo, evidencia ni commit.

## Skills (política vigente)

- **Al empezar**, lista `.claude/skills/` de `pg_control_proyectos` (hoy: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`, `trasladar-hallazgos`) y del repo de la app (hoy **no tiene** carpeta de Skills; compruébalo) y anota «Skills revisados» en tu `resultados/<tanda>.md`.
- **`cerrar-tanda`** al final de **toda** tanda; sus pasos de estados/evidencia/traspaso van en `resultados/<tanda>.md`, no en el plan/progreso/evidencia compartidos.
- **`verificar-permisos-por-rol`** en A y D (`Fase A`: modo estático esperado vs `permisos.ts` + pruebas; `Fase D`: en vivo con «Ver como»).
- `seguir-flujo-de-planes` lo usa el Orquestador.

## Cierre de tanda (obligatorio)

1. **No edites el plan, el progreso ni la evidencia.** Escribe tu cierre en `2026-10-01-dashboard-economia-y-curva-s-briefs/resultados/<id-de-tu-tanda>.md` (lo creas tú): estado de **tus** ítems (`Conforme`/`Observado`/`No aplica`), handoff ≤15 líneas, mejoras de trabajo, reglas de negocio detectadas en el momento, huérfanos y **número de llamadas**.
2. Commit en **tu rama** con `git add` explícito (nunca `-A` ni `.`), sin logs, capturas pesadas ni temporales. **Sin push ni merge.** El `resultados/<id>.md` lo commitea el Orquestador en `pg_control_proyectos`.
3. Último mensaje al Orquestador: ítems cerrados, pendientes, preguntas devueltas y llamadas usadas.

## Cuándo detenerte y devolver una pregunta

No hablas con Victor. **Detente** y devuelve la pregunta al Orquestador (opciones y recomendación) ante: contradicción con un flujo escrito, permisos que las tablas 1 y 2 del flujo 14 no decidan, cambio de un archivo ajeno o del contrato, acción destructiva o irreversible, infraestructura no autorizada (ramas, worktrees, push, otros archivos de entorno) o duda de negocio. Antes, deja hecho el commit de lo terminado. **No edites flujos de `04-flujos-de-negocio/` fuera de la Fase E.**

## Restricciones heredadas

- No cambia quién puede hacer qué salvo las filas aprobadas de este plan (Dashboard Parcial/Completo y Curva S física/económica).
- El Dashboard y la Curva S **siguen leyendo, no recalculan**: no se toca `evm.ts`, `dashboard.ts`, `curva-s.ts` (motor) ni funciones SQL (`db/053`, `061`, `070`); solo pruebas que los lean.
- Reutiliza componentes y la paleta de `design.md`. Sin credenciales en el repo.
