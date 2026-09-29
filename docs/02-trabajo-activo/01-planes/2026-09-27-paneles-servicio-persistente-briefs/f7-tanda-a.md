# F7-A · Documentación: flujos 16, 01 y 17, política de interfaz nueva y design.md

Lee primero `00-reglas-de-contexto.md`. Repo de trabajo: `D:\VICTOR\CLAUDE CODE\pg_control_proyectos`, rama `main` (documentación; no uses el worktree de la app).
Fase F7 · **Depende de:** F6-E cerrada y **respuestas de Victor** a C1 a C11, C22, C28 y V1, V3, V4, V7 registradas en el Registro de decisiones (el Orquestador las consulta antes de lanzar).
**Punto de commit:** Commit en `main` de `pg_control_proyectos` con `git add` explícito, solo con la autorización vigente de Victor (la confirma el Orquestador).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-58 | Política de "interfaz nueva" escrita en el flujo 16 y en `05-diseno-y-ui.md` con el texto aprobado en el Gate 1, con su plantilla de ítems de Punch List | Diff de `pg_control_proyectos` |
| PL-84 | `design.md` documenta el chip deshabilitado, el registro y la política (con la confirmación de Victor que exige su regla de evolución) | Diff |
| PL-118 | La regla "asistente como icono en toda pantalla" queda escrita en el flujo 16 (subsección propia), con referencias en los flujos 01 y 17 y la posición y capas en `design.md` §3, tras consultar a Victor | Diff de `pg_control_proyectos` |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Trabajas en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos` (rama `main`; no uses el worktree de la app). **No edites un flujo por una contradicción sin la respuesta registrada de Victor**: si falta alguna, no la toques y devuélvela al Orquestador (política de coherencia y trazabilidad, `AGENTS.md`).
- Flujo 16 (`16-paneles.md`, 9,8 KB): C1 a C10, C22, C28, V1, V7: regla 2 (se muestran todos, deshabilitados los no autorizados), regla 3, sin servicio/con servicio (Recursos de empresa con mostrar/ocultar), lista de Recursos (Personal, Cargos, Equipos, Causas CNC; sin Materiales), regla 7 («Salir a Mi entorno»), árbol del panel izquierdo (grupo Servicio, Reportes, Recursos del servicio), «Estado de implementación» y el bloque final (hoy dos versiones superpuestas y una línea cortada «tablas con scrol»), E1, regla 10 y «Tabla de accesos» (la fuente es el registro; el artefacto y el flujo 14 son la base), metadato `requiere servicio` con tercer valor «opcional», **subsección nueva «Asistente: elemento del shell fuera de los tres paneles»** (icono en toda pantalla del workspace, un clic despliega, no es chip ni está en el registro ni en la matriz, disponible para todos los roles, vista previa sin datos, estado al navegar), y V7 (entrar sin ver contenido; excepciones planner/Plan Maestro y supervisor de oficina técnica/DP). Integrado en la estructura, no pegado al final.
- Flujo 01: C11 (Apartado Proyectos para todos; mover la regla de paneles al 16 dejando enlace; «Salir a Mi entorno»). Flujo 17: aclaración de una línea (V2).
- **PL-58:** texto de la política de interfaz nueva: plan §«Política de interfaz nueva — texto propuesto» (Grep por el título) → flujo 16 (regla) y `05-diseno-y-ui.md` (instrucción al Worker y plantilla de ítems). **PL-84/PL-118:** `design.md` (31 KB; solo §3 y §5 por Grep de encabezados): chip deshabilitado, registro, política y posición/capas/patrón del asistente, con la confirmación que exige su regla de evolución.
- Registra en el progreso, por cada cambio, la consulta hecha y el enlace a la sección actualizada (base de PL-150).

## Qué NO hacer

- No edites `14-accesos-y-restricciones.md` ni el artefacto (F7-B). No dejes dos versiones conviviendo.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
