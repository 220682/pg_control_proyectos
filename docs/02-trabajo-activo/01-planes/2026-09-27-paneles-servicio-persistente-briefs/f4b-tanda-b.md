# F4B-B · Asistente: posición, capas, panel desplegado y accesibilidad (mediciones)

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F4B · **Depende de:** F4B-A cerrada.
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-108 | Escritorio: posición y capas verificadas con Playwright: el icono no tapa chips de ningún panel, el pie del panel izquierdo, controles del contenido ni el final de las tablas largas (Consolidado RDTs, Status de RDTs, PR, Plan Maestro) y formularios largos (comprobación con la caja del elemento y `elementFromPoint`) | Cajas medidas + capturas |
| PL-109 | Móvil: el icono no tapa la cabecera (botón de menú y botón de herramientas), no se solapa con los cajones ni con la zona segura inferior; con un cajón o un modal abierto (capa `z-50`) el asistente queda por debajo o se oculta, sin quedar encima | Capturas con cajón y modal abiertos |
| PL-110 | Panel desplegado: cabe en pantalla (alto máximo con scroll interno), en escritorio no cubre los paneles laterales y en móvil deja visible cómo cerrarlo y no impide usar la navegación | Capturas escritorio y móvil |
| PL-111 | Accesibilidad: el botón tiene nombre accesible ("Asistente"), `aria-expanded` y `aria-controls`; el panel tiene rol y etiqueta; se llega con Tab, Enter o Espacio abren, Escape cierra y devuelve el foco al icono; el objetivo táctil mide al menos 40 px | Snapshot de accesibilidad + prueba con teclado |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Medición con `browser_evaluate`: `getBoundingClientRect()` del icono y de los chips de cada panel, del pie del panel izquierdo y del final de las tablas; `document.elementFromPoint` sobre las esquinas del icono. Pantallas de tablas largas: `/rdts/consolidado`, `/rdts/status`, `/proyectos/<SV1>/pr`, `/plan-maestro` y formularios largos.
- Modales `fixed … z-50` (R20): `PanelVerRq.tsx`, `ModalPartidasServicio.tsx`, `ModalHistorialRdt.tsx`, `ResolverRecursosImportacion.tsx`, y `CajonMovil` (`WorkspaceShell.tsx` ~313). Con cualquiera abierto el asistente queda por debajo u oculto, nunca encima (móvil 390 px y escritorio).
- Móvil: no tapa la cabecera (botón de menú `aria-label="Abrir menú"`, herramientas `aria-label="Abrir herramientas"`), ni la zona segura inferior.
- Panel desplegado: alto máximo con scroll interno; en escritorio no cubre paneles laterales; en móvil deja visible cómo cerrarlo y no impide la navegación.
- Accesibilidad (PL-111): nombre accesible «Asistente», `aria-expanded` y `aria-controls`; el panel con rol y etiqueta; Tab llega, Enter o Espacio abren, Escape cierra y devuelve el foco al icono; objetivo táctil ≥ 40 px. Verifica con `browser_snapshot` y `browser_press_key`. Patrón de referencia: `CajonMovil` (`role="dialog"`, Escape en `WorkspaceShellInner` ~370-378).
- Si una medición falla, ajusta la posición/capa aquí y repite la medición del caso.

## Qué NO hacer

- No cambies el contenido del asistente ni lo conectes a datos. Una captura por ítem como máximo (máx. 8 en la tanda).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
