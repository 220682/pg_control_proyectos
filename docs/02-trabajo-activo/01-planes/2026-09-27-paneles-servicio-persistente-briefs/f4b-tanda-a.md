# F4B-A · Asistente como icono en el shell: construcción y visibilidad en toda pantalla

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F4B · **Depende de:** F4-A cerrada (mismo archivo `WorkspaceShell.tsx`).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-102 | Con servicio, en escritorio: el icono del asistente es visible en **todas** las pantallas del workspace, incluidas las que hoy no muestran la barra (recorrido de cada ruta de PL-02 a PL-13, Mi entorno, Notificaciones, Recursos, Configuraciones y Mi perfil) | Tabla ruta → icono visible + capturas |
| PL-103 | Sin servicio, en escritorio: icono visible en Todos los servicios, Programas, Portafolio, Mi entorno, Recursos, Notificaciones, Usuarios, Configuraciones y Mi perfil | Tabla ruta → icono visible |
| PL-104 | En móvil (390 px), con y sin servicio: icono visible en las mismas pantallas (hoy la barra no se mostraba en móvil) | Capturas móvil |
| PL-105 | El clic en el icono despliega el panel (mensaje de vista previa, campo y botón Enviar); un segundo clic en el icono o el botón de cerrar lo repliega a solo icono, y el foco vuelve al icono | Captura abierto y cerrado + foco |
| PL-106 | Ya no hay barra fija al pie: en escritorio con servicio desaparece la banda "Pregúntale algo al asistente…" y el área de contenido recupera esa altura respecto de la línea base de F0 | Captura antes y después + medida del contenedor |
| PL-107 | No hay duplicado: en la pantalla del portafolio y en cualquier otra hay **una sola** instancia del asistente (conteo de elementos con su nombre accesible = 1) | Conteo por pantalla |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- `src/components/ui/ChatPlaceholder.tsx` (48 líneas): hoy barra con botón `aria-expanded` que despliega un panel con un mensaje de ejemplo «¿Cuántos proyectos tiene este portafolio?», el aviso «Este asistente todavía no está conectado a ningún dato…» y un formulario con `preventDefault`. **Se modifica este componente** (no se crea uno paralelo): pasa a icono más panel desplegable. Neutraliza el ejemplo (A10) y conserva el aviso.
- Quitar las dos copias: `WorkspaceShell.tsx` ~464 (`{proyectoId && (<div className="hidden shrink-0 border-t … lg:block"><ChatPlaceholder /></div>)}`) y `(workspace)/programas/[id]/portafolios/[portafolioId]/page.tsx` ~186 (+ import ~9). El shell renderiza **un único** asistente en toda pantalla de `(workspace)`, con y sin servicio, escritorio y móvil.
- Posición propuesta (el Worker puede cambiarla justificándola con Playwright): escritorio, esquina inferior derecha del área central **dentro de `<main>`**, no fija a la ventana (no invadir el panel derecho `w-64`); móvil, en la cabecera móvil (junto a los botones de menú y herramientas, `h-10 w-10`) o flotante respetando `env(safe-area-inset-bottom)`. Capa por debajo de los modales y cajones (`z-50`) y por encima de las cabeceras fijas de tablas (`z-20` a `z-30`).
- Estado abierto/cerrado en el shell (`WorkspaceShellInner` ~358, junto a `panelMovil`), que no se remonta al navegar. Sin llamadas a `/api`: sigue siendo vista previa (flujo 17: no habilitado).
- Rutas de PL-102/103: todas las de PL-02 a PL-13, Mi entorno, Notificaciones, Recursos, Configuraciones, Mi perfil; sin servicio: Todos los servicios, Programas, Portafolio, Usuarios. Un recorrido con `browser_evaluate` que cuente elementos por nombre accesible (esperado 1 por pantalla).

## Qué NO hacer

- No conectes el asistente a datos ni a ninguna API. No lo registres en el registro de accesos. Mediciones finas de posición y a11y son de F4B-B.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
