# F3-C · Panel izquierdo: permisos, chips deshabilitados accesibles y diseño

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F3 · **Depende de:** F3-A y F3-B cerradas.
**Punto de commit:** Al cerrar la fase F3 (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-38 | Cuenta A con SV1: cada chip del panel izquierdo está habilitado o deshabilitado según la matriz base del flujo 14 y sus acciones (administrador y jefe de proyectos con acceso a todo, según lo que resuelva CO5); las diferencias con el código vigente se listan, no se corrigen en silencio | Tabla chip → estado esperado → estado real |
| PL-39 | Cuenta B con SV1: el panel izquierdo **es visible** (antes no lo era); los chips que su rol no puede usar están deshabilitados con `opacity-40`, `cursor-not-allowed` y título explicativo; los que puede usar están activos | Tabla + captura |
| PL-40 | Cuenta B: hacer clic en un chip deshabilitado no navega (URL sin cambios) y no hay error en consola | Captura + consola |
| PL-48 | "Ver no es modificar": dentro de las pantallas, los botones de acción (Consolidado RQ, Status de RDTs, Paquetes de Trabajo, Recursos) siguen la matriz de acciones del flujo 14 (con los cambios de F5C); poder ver una interfaz no habilita ninguna acción | Comparación con la línea base y con el flujo 14 |
| PL-61 | Chip deshabilitado accesible: `aria-disabled="true"`, título, no enfocable como enlace y no depende solo del color (texto legible) | Snapshot de accesibilidad |
| PL-63 | La marca informativo/acción es visible y no depende solo del color, en ambos paneles | Captura |
| PL-64 | Diseño: se usan los tokens y el estilo de `EntornoTrabajoGrupo.tsx`, sin `max-w-*` nuevo en contenedores de página y sin dependencias visuales nuevas | Revisión de diff |
| PL-71 | Cambiar quién "ve" un chip no cambió quién "puede" usarlo, salvo lo decidido en el flujo 14: el diff de `permisos.ts` coincide con la matriz base y con "Acciones que cambian con esta decisión"; ninguna otra función cambia de roles; `permisos.test.ts` verde | Diff + `npm test` |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Fuente de «estado esperado»: tablas 1 y 2 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md`, leídas del archivo (no se copian). Cuenta A y cuenta B con SV1; el rol de B sale del pie del panel izquierdo. Diferencias con el código vigente se **listan**, no se corrigen en silencio.
- Chip deshabilitado: `aria-disabled="true"`, título explicativo, no enfocable como enlace, `opacity-40 cursor-not-allowed`, texto legible (no depende solo del color); clic sin cambio de URL y sin error en consola (`browser_console_messages`). La marca informativo/acción no depende solo del color, en ambos paneles.
- **PL-48:** los botones de acción dentro de Consolidado RQ, Status de RDTs, Paquetes de Trabajo y Recursos siguen la línea base F0-C (los cambios de acciones son F5C).
- **PL-71:** `git diff main -- src/lib/permisos/permisos.ts` acumulado hasta F3 solo contiene lo de F2B-A (funciones de ver y `puedeVerStatusRequerimiento`) y `npm test` verde.
- **PL-64:** sin `max-w-*` nuevo en contenedores de página ni dependencias visuales nuevas: `git diff main` filtrado por `max-w` y `package.json`. Tokens y estilo de `EntornoTrabajoGrupo.tsx`; `design.md` (31 KB): lee por Grep de encabezados solo §3, §5, §9, §10 y §12.

## Qué NO hacer

- No cambies permisos. Si una diferencia con la matriz es un hallazgo, anótalo y sigue.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
