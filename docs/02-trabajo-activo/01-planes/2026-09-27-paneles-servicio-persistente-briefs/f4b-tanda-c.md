# F4B-C · Asistente: estado al navegar, red, reutilización, roles y pantallas fuera del shell

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F4B · **Depende de:** F4B-B cerrada.
**Punto de commit:** Al cerrar la fase F4B (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-112 | Estado al cambiar de pantalla: con el panel abierto, navegar a otra pantalla del shell lo conserva abierto (el estado vive en el shell) y al recargar vuelve a icono; el comportamiento queda escrito en la evidencia y en el flujo (si el Worker decide otro, lo documenta) | Secuencia de capturas |
| PL-113 | Sigue siendo vista previa: abrir el panel o pulsar Enviar no genera ninguna llamada de red a `/api` y el formulario no envía; el texto "todavía no está conectado a ningún dato" sigue visible | Registro de red de Playwright |
| PL-114 | Reutilización y diseño: se modifica `ChatPlaceholder` en vez de crear un componente paralelo; se usan tokens y clases existentes y el patrón de diálogo y Escape de `CajonMovil`; sin dependencias nuevas y sin `max-w-*` nuevo en contenedores de página | Revisión del diff |
| PL-115 | Disponible para los 13 roles (sin permiso propio): cuenta A, cuenta B y una muestra de roles con "Ver como" ven el icono; el asistente no forma parte del registro de accesos ni de la matriz del flujo 14 (queda escrito) | Capturas + nota |
| PL-116 | Pantallas fuera del shell: login y activar cuenta no muestran el asistente (sin sesión); la pantalla `programas/[id]/portafolios/[portafolioId]/dashboard` (fuera de `(workspace)`) queda como excepción declarada y se reporta a Victor | Captura + nota (V4, R21) |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **PL-112:** con el panel abierto, navegar dentro del shell lo conserva; al recargar vuelve a icono. Riesgo R23: el shell envuelve su contenido en `Suspense` y usa `useSearchParams`; si el estado se pierde, corrígelo o documenta el comportamiento en la evidencia.
- **PL-113:** abrir el panel y pulsar Enviar no genera ninguna llamada a `/api` y no envía el formulario: `browser_network_requests` filtrado. El texto «todavía no está conectado a ningún dato» sigue visible.
- **PL-114:** revisión del diff (`git diff main -- src/components/ui/ChatPlaceholder.tsx src/components/ui/WorkspaceShell.tsx`): se modificó `ChatPlaceholder` (no hay componente paralelo), tokens y clases existentes, patrón de diálogo/Escape de `CajonMovil`, sin dependencias nuevas en `package.json` y sin `max-w-*` nuevo en contenedores de página.
- **PL-115:** cuenta A, cuenta B y una muestra de roles con «Ver como» ven el icono; el asistente no está en el registro de accesos ni en la matriz del flujo 14 (queda escrito en la evidencia).
- **PL-116:** login (`src/app/(inicio)/login/page.tsx`) y activar (`(inicio)/auth/activar`) no muestran el asistente (sin sesión). `src/app/programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx` está fuera de `(workspace)` (sin paneles ni asistente): queda como excepción declarada y **se reporta a Victor** (R13, R21, V4); no se mueve la página.

## Qué NO hacer

- No muevas pantallas fuera del shell. No conectes el asistente a datos.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
