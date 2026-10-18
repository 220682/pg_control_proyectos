# Resumen de cierre — T8A

## Tanda, rol y modelo

Documentador · T8A · Sonnet · esfuerzo medio. Flujos de avisos, RQ, RDT y checklist (T8-01, T8-02, T8-03 y T8-08). Fecha: 2026-10-18. Sin navegador ni cambios en la app; el worktree `local-worker-7` se leyó en solo lectura (HEAD `85626fd`, árbol limpio).

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| T8-01 | Conforme | `docs/04-flujos-de-negocio/04-notificaciones.md` reescrito (de 13 a unas 140 líneas): qué es un aviso, estados y cierre (manual, al abrir, automático por referencia), por usuario o por rol y tarjeta única con dos roles, servicio / N° OT / «Entorno», grupos con «Jefatura» y filtros (incluido «Solo Entorno» y «Tipo de aviso»), catálogo de los 22 eventos con disparador, destinatario, texto, grupo y cierre, `informe.emitido` reservado, contrato de la API, migración 108 y diferencias temporales. «Lee si:» actualizado. Commit `c7fd383` | — |
| T8-02 | Conforme | `05-rq.md`: ciclo con tabla de pasos y avisos, cada paso solo desde su estado de origen (409), Recepcionado al abrir (solo Logística, una vez, quién recepcionó sin pisar), Devolver / Corregir y reenviar / Un Devuelto no avanza, comentarios que avisan al solicitante, consolidado sin Devolver, permisos de Devolver y Corregir (con remisión al flujo 14), migración 109. «Lee si:» actualizado. Commit `c7fd383` | — |
| T8-03 | Conforme | `06-rdt.md`: sección «Avisos del RDT» (subido, registrado, validado, rechazado con motivo, cierres) en lugar de la línea «Notificación al subir: solo Administración»; `12-checklist.md`: sección «Avisos del checklist» («falta subir» con N° OT, cierre automático al subir, completar o quitar, reasignar, ya no se avisa de documentos de cierre). Ambos con «Lee si:» actualizado. Commit `c7fd383` solo con mis hunks | — |
| T8-08 | Conforme | `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/coherencia-flujos-codigo.md`: 22 filas del catálogo contra el código (archivo y línea), 13 reglas generales y 10 diferencias. 22 de 22 eventos coinciden. Commit `c7fd383` | — |

## Rama, commits y archivos tocados

Repositorio documental, rama `main`, sin push. Un commit: `c7fd383` («Plan Notificaciones: flujos 04, 05, 06 y 12 al dia y tabla de coherencia con el codigo»).

Archivos: `docs/04-flujos-de-negocio/04-notificaciones.md` y `05-rq.md` (sin cambios ajenos; commiteados enteros), `06-rdt.md` y `12-checklist.md` (con cambios ajenos sin commitear; ver abajo) y la tabla de coherencia (archivo nuevo).

**Hunks de otras sesiones que quedan sin commitear** (siguen como `M` en el árbol de trabajo, intactos): `06-rdt.md` (tres hunks: «Qué elige el supervisor», «Avance por paquete», «Actividades C y NC» y el de «Disciplinas») y `12-checklist.md` (la nota de 2026-10-15 en «Ítems sin pantalla todavía (RB2)»). El método fue el pedido: copia del estado previo en el scratchpad, `diff -u` solo de mis cambios y `git apply --cached`; el índice quedó con solo mis hunks (comprobado con `git diff --cached`). No se tocó ningún otro archivo ajeno (09, 14, 16, 18, 19, 20, 22 siguen como estaban).

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| T8A-H1 | conflicto con un flujo o pregunta para el Responsable humano | **D5.** El aviso «pendiente de aprobación» del RQ se rotula «Oficina Técnica» para un administrador que además es jefe de oficina técnica (una fila por rol y la tarjeta única toma el grupo de una de ellas; hallazgo T7A-H2). El flujo 04 dice «según el rol» | Victor: ¿se deja así o esa cola va siempre en «Jefatura»? |
| T8A-H2 | conflicto con un flujo o pregunta para el Responsable humano | **D6.** Los avisos al solicitante del RQ nacen con el grupo fijo «Jefatura» aunque sea un supervisor operativo; el diseño inicial decía «el grupo del rol de la persona». El flujo 04 documenta lo que hace el código | Victor |
| T8A-H3 | conflicto con un flujo o pregunta para el Responsable humano | **D8.** Si el solicitante también es de un rol que recibe la cola (jefe de proyectos), recibe dos avisos por un comentario (T4-H3). El flujo 05 describe el comportamiento actual | Victor: dejar o deduplicar |
| T8A-H4 | conflicto con un flujo o pregunta para el Responsable humano | **D9.** Al reemplazar un RDT por una corrección se cierran los avisos «registrado» y «rechazado» del RDT anterior, y «registrado» también se cierra al validar o rechazar (decisión del Worker 7, marcada «por validar», T6-H3). Está escrito en el flujo 06 tal como lo hace el código | Victor: confirmar |
| T8A-H5 | observación sobre la política | **D1.** El rótulo del grupo del panel izquierdo (`lib/config/registro-accesos.ts:122`) sigue en «Proyecto» en el código; los flujos dicen «Jefatura» (diferencia temporal registrada en el flujo 04 y en la tabla de coherencia) | Orquestador: corregir el código; T8B: flujos 02, 08 y 16 |
| T8A-H6 | observación sobre la política | **D2.** `cerrarAvisos` no cae al cierre por texto cuando falta la migración 108 (sí lo hace `avisar` al crear); los avisos de checklist, RDT y `servicio.asignado` anteriores a T6b no tienen referencia y no se cierran solos | Auditor |
| T8A-H7 | observación sobre la política | **D7 / O1.** `marcar-visto` (alias heredado) no cierra los informativos como `revisar` | Auditor (huérfano O1) |
| T8A-H8 | mejora de trabajo | Archivos con cambios ajenos sin commitear: guardar una copia antes de editar, hacer `diff -u` de mis cambios y aplicarlos con `git apply --cached` funcionó a la primera para 06 y 12 (los hunks propios y ajenos no se solapan si se editan en zonas distintas). Un `heredoc` de Bash con comillas y paréntesis falló al analizarse: usar `sed -i` o la herramienta de edición | `docs/03-aprendizaje-continuo/` (M10 si el Orquestador lo suma) |

## Traspaso

* Hecho: flujos 04, 05, 06 y 12 y la tabla de coherencia, commiteados en `c7fd383`.
* Para T8B: los flujos ya llaman a «Jefatura»; el flujo 05 remite a la tabla 2 del flujo 14 para los permisos de Devolver (administrador, jefe de proyectos y jefe de oficina técnica) y Corregir y reenviar (solicitante y administrador): esas filas las agrega T8B. El flujo 04 remite al flujo 14 para el permiso de enviar a un servicio («Entorno» no lo exige; Q2). El flujo 14 aún tiene, sin editar, la fila 94 y las líneas 183 y 184 (Q8).
* No toqué los índices (`docs/README.md`, `04-flujos-de-negocio/README.md`): son de T8B; su línea «Lee si:» de los flujos 04 y 05 cambió y el índice las copia.
* `python scripts/verificar-referencias.py`: 0 enlaces rotos; 2 menciones sin archivo, ajenas a esta tanda (una en `docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md`). La corrida oficial es de T8B.
* No inventé nada fuera del plan, los resúmenes y el código. Las decisiones de Victor del 2026-10-18 (cambio de responsable, maqueta, «Jefatura», lista de informativos, 409 por estado de origen, rol vs usuario) están escritas.

## Llamadas y contexto

Unas 55 llamadas a herramientas.

## Skills revisados

`trasladar-hallazgos` y `cerrar-tanda` existen en `.claude/skills/` del repositorio documental; no aplican a esta parte (el traslado es de T8B). Ninguno usado.

## Fuentes de verdad revisadas

Actualizadas: flujos 04, 05, 06 y 12. Pendientes (T8B): 14, 02, 08, 16, 03, 07, el artefacto «Matriz de permisos», índices y el traslado del libro de hallazgos. Sin cambios en `AGENTS.md`.
