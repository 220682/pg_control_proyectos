# F3-A · Panel izquierdo con servicio: estructura, grupos, chips y acciones

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F3 · **Depende de:** F2B-B cerrada (fin de F2B).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-22 | Con servicio, el panel izquierdo muestra los grupos acordados (decisiones 5 y 6): Alcance y presupuesto, Planificación, Recursos del servicio, Documentación, Reportes, y el grupo Servicio si se aprueba; las acciones van separadas de los informativos | Captura |
| PL-23 | Cada chip del panel izquierdo cuya pantalla existe abre esa pantalla con SV1 (DP, Paquetes de Trabajo, Cronograma, Plan Maestro, Consolidado RDTs, Requerimiento, PR, Dashboard, Curva S, Registro de costos y, si se aprueba, Ficha del servicio, Editar servicio y Editar checklist) | Tabla chip → URL → servicio visible |
| PL-24 | Los chips sin pantalla (Alcance, Presupuesto, Cargos HH, Equipos HM, Planos, PETS y los que fije la decisión 5) se ven, no tienen enlace, el clic no cambia la URL y no hay error en consola | Captura + registro de consola |
| PL-25 | Acciones: Generar RQ abre Crear RQ con SV1; Crear RDT abre Crear RDTs con SV1; Crear paquete abre Paquetes de Trabajo con SV1 y el formulario de paquete nuevo abierto; Subir RDT abre su formulario con SV1. Ninguna guarda al abrir | Captura de cada formulario |
| PL-26 | Las acciones quedan fijadas al servicio actual (según E1): el formulario abre con SV1 y, si se cambia el servicio dentro de la acción, la URL y los paneles lo siguen (no puede haber dos servicios distintos a la vez) | Captura antes y después |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Hoy (`WorkspaceShell.tsx`): `ContenidoNav` ~123-287 muestra Recursos solo con `usuario.puedeVerRecursos` (~162), el bloque «Proyecto» solo con `puedeVerApartadoProyectos` (~204) usando `itemsGrupoProyecto` armado en `WorkspaceShellInner` (~389-405: DP → PR → Dashboard → Curva S) y el pie `mt-auto` (~243-283). Reescribe el bloque con servicio para los **13 roles**.
- Estructura acordada (flujo 16 y decisiones 5 y 6; plan §«Decisiones abiertas 3 a 6»): Alcance y presupuesto (Alcance, Presupuesto, Paquetes de trabajo) · Planificación (Cronograma, Plan Maestro) · Recursos del servicio (**Cargos (HH)**, **Equipos (HM)**) · Documentación (Planos, PETS) · Reportes (Consolidado RDTs, RQ, PR, Dashboard, Curva S, **Registro de costos**) · Acciones (Generar RQ, Crear RDT, Subir RDT, Crear paquete) · grupo **Servicio** (Ficha del servicio, Editar servicio, Editar checklist). Separa informativos de acciones.
- Inertes (sin pantalla; visibles y sin enlace, A6): «(OT) Orden de trabajo», Presupuesto, Alcance del servicio, Personal NUEVO, Consolidado de servicio, Materiales c/c, Cargos (HH), Equipos (HM), Planos, PETS. «Recursos hh, hm, mat. (s/c)» se retira. «Notificaciones» no se repite en el panel izquierdo (A5).
- Rutas nuevas en el registro: Ficha `/proyectos/<id>`, Editar servicio `/proyectos/<id>/editar`, Editar checklist `/proyectos/<id>/checklist/editar`, Registro de costos `/proyectos/<id>/registro-costos`. Generar RQ abre Mi entorno `?proyectoId=&accion=crear-rq`; Subir RDT `?accion=subir-rdt`; Crear RDT `/rdts/crear`; **Crear paquete** `/paquetes-trabajo?proyectoId=&accion=crear` con cambio mínimo en `FormularioPaquetesTrabajo.tsx` para abrir el formulario de paquete nuevo (A7).
- Componente de chip compartido (informativo, acción, deshabilitado, inerte), usado por ambos paneles: estilo del chip deshabilitado en `EntornoTrabajoGrupo.tsx` (`CHIP` ~45, `ChipHerramienta` ~48; `opacity-40 cursor-not-allowed` + título). `design.md` §5 exige justificar componentes nuevos: la aprobación del Gate 1 lo cubre.
- E1: las acciones abren con SV1 y, si se cambia el servicio dentro, la URL y los paneles lo siguen. Ninguna acción guarda al abrir.

## Qué NO hacer

- No cambies permisos (los chips usan el `permiso` vigente del registro). No implementes Recursos de empresa ni el pie (F3-B).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
