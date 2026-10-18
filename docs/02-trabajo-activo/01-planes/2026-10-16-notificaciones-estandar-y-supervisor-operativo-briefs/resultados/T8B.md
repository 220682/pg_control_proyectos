# Resumen de cierre — T8B

## Tanda, rol y modelo

Documentador · T8B · Sonnet 5.5 · esfuerzo medio. Accesos, paneles, perfil, matriz de permisos, hallazgos e índices (T8-04 a T8-07). Fecha: 2026-10-18. Sin navegador ni cambios en la app; el worktree `local-worker-7` se leyó en solo lectura (HEAD `9611338`, T7fix).

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| T8-04 | Conforme | Flujo 14: tabla 2 con «Devolver un RQ Solicitado con motivo» y «Corregir y reenviar un RQ Devuelto» (nota 15); la fila «Editar perfil extendido (propio)» se reemplazó por «Editar mi celular», «Cambiar mi correo» y «Cambiar mi contraseña» para los 13 roles (nota 14); líneas de decisiones del 2026-09-28 corregidas (el jefe de proyectos y el jefe de oficina técnica ya no «dejan de editar su perfil»); sección Notificaciones precisa que «Entorno» y el aviso a uno mismo no exigen servicio; nota de actualización 2026-10-18. Flujo 16: grupo «Jefatura» (panel derecho y nota de panel izquierdo y título de Mi entorno). Flujo 03: perfil propio con tres bloques, grupo «Jefatura» y título «Entorno · Jefatura». Flujo 02: qué edita cada persona de su perfil. Flujo 07: cambio de contraseña y de correo propios. Flujo 08: avisos por cambio de responsable. «Lee si:» de 02, 03 y 07 actualizados. Flujos 04 y 05 corregidos en los puntos de «Oficina Técnica» y «diferencia temporal» (ver abajo). Commit `d1951b5` | — |
| T8-05 | Observado | La herramienta Artifact (`read`) sobre `4no1PCEfDb5pYmgmnrP5MT` respondió «artifact not found» (primer intento rechazado por la revisión automática; el segundo, 404). No se intentó otra vía | **Victor**: actualizar el artefacto con las filas de abajo («Filas para el artefacto Matriz de permisos») |
| T8-06 | Observado | Libro del plan trasladado con el skill `trasladar-hallazgos`: M1 a M9 y R1 a R15 `Trasladada` con enlace al destino; filas nuevas R11 a R17 y P-3 a P-8 agregadas desde los resúmenes (inventario); O1 a O3 reportados a Victor abajo | Quedan `Pendiente de decisión`: P-1 a P-8 (Auditor / Gate 2), R16 (duda D9, Victor) y R17 (duda D8, Victor) |
| T8-07 | Conforme | Índices al día (`04-flujos-de-negocio/README.md`: disparadores de 02, 03, 04, 05, 06, 07 y 12; `03-aprendizaje-continuo/README.md`: aprendizaje nuevo). `docs/README.md` no necesita cambio (sigue siendo 22 flujos). `python scripts/verificar-referencias.py`: 46 archivos revisados, 0 huérfanos, 0 enlaces rotos, 2 menciones sin archivo ajenas (una en `01-contexto-repositorio/03-entorno-git-y-worktrees.md`, ya reportada por T8A) | — |

## Commits y archivos tocados

Repositorio documental, rama `main`, sin push. Commits: `d1951b5` («flujos 02, 03, 07, 08, 14 y 16 al día, índices y aprendizajes de trabajo») y el commit del libro de hallazgos y de este resumen (el último de la rama).

Archivos: flujos `02-usuarios.md`, `03-entorno.md`, `04-notificaciones.md`, `07-nucleo-auth.md`, `08-programa-portafolio-proyecto.md`, `14-accesos-y-restricciones.md`, `16-paneles.md`; `04-flujos-de-negocio/README.md`; `03-aprendizaje-continuo/README.md` y el archivo nuevo `2026-10-18-notificaciones-aprendizajes-de-trabajo.md`; `coherencia-flujos-codigo.md` (D1 y D5 cerradas por el commit `9611338`); el plan (libro de hallazgos y estados de T8-04 a T8-07) y este resumen. Ningún archivo borrado.

**Hunks de otras sesiones que quedan sin commitear** (siguen como `M` en el árbol de trabajo): `14-accesos-y-restricciones.md` (fila «Recursos del servicio», nota ⁷ de 2026-10-15, nota ¹³ movida, línea «Elegir servicio» y ampliación de «Recursos»), `16-paneles.md` (chips vivos y «Elegir servicio», Subcontratos, conteo de chips y «Recursos del servicio»), `06-rdt.md` y `12-checklist.md` (los de T8A), y todos los demás (09, 18, 19, 20, 22, design, mockups). Método: un script aplicó la misma lista de sustituciones al archivo de trabajo y a la versión del índice (`git show :archivo`), y el índice se actualizó con `git hash-object` y `git update-index --cacheinfo`; el índice quedó con solo mis cambios (comprobado con `git diff --cached`). Las capturas nuevas de `…/03-evidencia/…/t7/` (T7C) y el resto de archivos sin seguimiento son ajenos y no se incluyeron.

## Cambios de T8B sobre lo que dejó T8A

* Flujo 04: «RQ pendiente de aprobación» nace siempre en **Jefatura**; la tarjeta unificada muestra el grupo de la fila del rol de la persona (Jefatura primero si coinciden varias); la «diferencia temporal» del panel izquierdo quedó como «Ninguna abierta». El flujo 05 no tenía ninguno de los dos puntos (ya decía lo correcto); no se tocó.
* Tabla de coherencia: D1 y D5 marcadas como cerradas por `9611338`.
* **D8 y D9 no se tocaron**: el flujo 05 (comentario con dos avisos) y el flujo 06 (cierre de avisos al reemplazar un RDT, con su marca «por validar») siguen como los dejó T8A. En el libro quedan como R17 y R16, `Pendiente de decisión` (Victor).

## Filas para el artefacto «Matriz de permisos» (para Victor)

La cuenta de Claude Code no puede abrir el artefacto. Hay que agregar o cambiar, en la **tabla de acciones** (columnas Admin, JP, JOT, SOT, Plnr, SCo, JCo, SOp, SLog, SAdm, SSO, Asist, RRHH; última columna «Requiere OT a cargo»):

| Acción | Roles | Requiere OT a cargo |
|---|---|---|
| **Reemplazar** «Editar perfil extendido (propio)» (hoy solo Admin y JP) por las tres filas siguientes | — | — |
| Editar mi celular (propio; solo el celular, nunca nombre, cargo, área ni roles) | Los 13 roles ✓ | No |
| Cambiar mi correo (propio; pide la contraseña actual y rige al confirmarlo por enlace) | Los 13 roles ✓ | No |
| Cambiar mi contraseña (propia; pide la actual) | Los 13 roles ✓ | No |
| Devolver un RQ Solicitado con motivo (mismo reparto que «Derivar RQ a logística») | Admin, JP, JOT ✓; el resto — | Sí |
| Corregir y reenviar un RQ Devuelto (el solicitante del RQ y el administrador) | Admin ✓; los otros 12 roles `*` («si es el solicitante») | Sí |

Y en la **tabla de interfaces** (pendientes de 2026-10-15 y 2026-10-17 que los flujos ya traen y el artefacto aún no): «Recursos del servicio, ver» (13 roles), «Alcance del servicio: ver y descargar» (13 roles) y «Presupuesto del servicio: ver y descargar» (Admin, JP, JOT, SOT, SCo, JCo), más las filas de informes de supervisión de la tanda M del plan de Informes (ya señaladas en el flujo 14, nota 11). La sección «Notificaciones» del artefacto, si la tiene, precisa que enviar o atender un aviso exige el servicio solo cuando el aviso es de un servicio. Para el artefacto: al reflejar las filas, quitar la marca «Aprobada» solo si Victor lo desea (ya estaba quitada desde 2026-09-30).

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| T8B-H1 | observación sobre la política | La política exige actualizar el artefacto en la misma tarea, pero esta cuenta no puede abrirlo (P-8); la actualización depende siempre de Victor | Auditor / Gate 2 |
| T8B-H2 | conflicto con un flujo (preexistente, ajeno) | El flujo 14 tiene **dos notas ⁷** (la de recursos del servicio, de 2026-10-15, y la de descargas, de 2026-09-30) y la nota ⁶ aparece después de la ⁷ de recursos: numeración desordenada. Es un cambio sin commitear de otra sesión; no lo toqué | Quien cierre esa sesión |
| T8B-H3 | pregunta para el Responsable humano | `puedeEditarPerfilExtendido` sigue en `permisos.ts` sin uso en el perfil; el flujo 14 ya no lo cita como fila. Queda como código sin uso | Orquestador / Auditor |
| T8B-H4 | mejora de trabajo | Técnica de «sustituciones duales» (archivo de trabajo + versión del índice) para comitear solo hunks propios; más robusta que `diff -u` + `git apply --cached` | Ya en el aprendizaje nuevo, punto 7 (candidata a Skill) |
| T8B-H5 | observación sobre la política | Un heredoc de Bash con comillas simples y paréntesis falló otra vez al analizarse («unexpected EOF»); se resolvió con la herramienta de escritura | Ya en el aprendizaje nuevo, punto 6 |

## Archivos huérfanos reportados a Victor (sin borrar nada)

O1 `src/app/api/notificaciones/[id]/marcar-visto/route.ts` (alias heredado, ninguna pantalla lo llama; además no cierra los informativos: P-4), O2 `src/app/api/notificaciones/route.ts` (consulta de respaldo `COLUMNAS_LEGACY`) y O3 `src/app/api/areas/route.ts` (tres consultas de comprobación sin uso). Del repositorio documental: sin huérfanos nuevos (el script da 0). Archivos sin seguimiento ajenos que Victor debería revisar: `login-ojo-contrasena.png` (raíz) y la carpeta `.playwright-mcp/` con snapshots que contienen claves (M8; excluida de git en `.git/info/exclude` local, borrarla es decisión suya).

## Observaciones sobre la política para el Auditor

P-1 (pre-autorizaciones masivas en producción), P-2 (política de escritura en `perfiles`, confirmar en vivo), P-3 (`cerrarAvisos` sin respaldo por texto sin la migración 108), P-4 (`marcar-visto`), P-5 (redirección y plantilla del correo de confirmación), P-6 (etiqueta de `supervisor_ssoma`), P-7 (identificador común para unificar tarjetas), P-8 (artefacto no accesible). Todas en el libro del plan, `Pendiente de decisión`.

## Para el Orquestador / Victor

* **Dudas D8 y D9** sin responder (R17 y R16): se mantienen como comportamiento actual, sin escribir que Victor las aprobó.
* Mejoras de trabajo trasladadas: un solo archivo nuevo en `03-aprendizaje-continuo/` (8 puntos) en lugar de uno por mejora; si se prefiere uno por mejora, se divide.
* `coherencia-flujos-codigo.md` ya no refleja el HEAD `85626fd` en su encabezado; las filas D1 y D5 indican `9611338`.

## Llamadas y contexto

Unas 95 llamadas a herramientas en total (cortadas por un límite de uso; retomadas desde el índice de git).

## Skills revisados

`trasladar-hallazgos` (usado para el libro) y `cerrar-tanda` (no usado: el cierre lo hace el Orquestador). `verificar-permisos-por-rol` no aplica (no hay verificación en vivo en esta parte).

## Fuentes de verdad revisadas

Actualizadas: flujos 02, 03, 04, 07, 08, 14 y 16, índice de flujos, índice de aprendizaje y tabla de coherencia. Pendiente de Victor: artefacto «Matriz de permisos». Sin cambios en `AGENTS.md`.
