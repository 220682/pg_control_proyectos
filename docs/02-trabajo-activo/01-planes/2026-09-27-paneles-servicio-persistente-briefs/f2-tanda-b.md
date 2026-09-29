# F2-B · Pantallas con selector existente: Cronograma, Paquetes, Plan Maestro, Mi entorno, Recursos y rutas de servicio

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F2 · **Depende de:** F2-A cerrada (helper de servicio y shell que reconoce `?proyectoId=`).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-02 | Cronograma con SV1: `?proyectoId=` en la URL, ambos paneles con SV1 y selector de OT = SV1 | Captura + URL |
| PL-03 | Paquetes de Trabajo con SV1: ídem PL-02 | Captura + URL |
| PL-04 | Plan Maestro con SV1: ídem PL-02 | Captura + URL |
| PL-11 | Notificaciones, Mi entorno (`?accion=crear-rq` y `?accion=subir-rdt`) y Recursos de empresa (Personal, Cargos, Equipos): los paneles conservan SV1 | Captura + URL de cada una |
| PL-12 | DP, PR, Dashboard, Curva S y Registro de costos (rutas `/proyectos/<id>/…`): ambos paneles con SV1 (regresión de lo que ya funcionaba) | Captura + URL de cada una |
| PL-14 | Cambiar de servicio (SV1 a SV2) con el selector de una pantalla: la URL y ambos paneles pasan a SV2 | URL antes y después + captura |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Las tres pantallas ya leen `searchParams: Promise<{ proyectoId?: string }>` y pasan `proyectoIdInicial={proyectoId ?? ''}`: `(workspace)/cronograma/page.tsx` → `FormularioCronograma` (`src/components/ui/`, estado `useState(proyectoIdInicial)` ~66; efecto ~81 que elige el primero de la lista si no hay inicial), `paquetes-trabajo/page.tsx` → `FormularioPaquetesTrabajo` (~70-100), `plan-maestro/page.tsx` → `FormularioPlanMaestro` (~56-84).
- Falta: que el selector interno **actualice la URL** con `router.replace` usando el helper de F2-A (A1, R11: sin bucle entre selector y URL) y que el panel siga el cambio (PL-14).
- `mi-entorno/page.tsx` lee `proyectoId` y `accion` (`crear-rq`, `subir-rdt`) y pasa `proyectoIdInicial` a `FormularioRequerimiento` y `FormularioSubirRdt`. Notificaciones: `(workspace)/notificaciones/page.tsx`. Recursos: `recursos/{personal,cargos,equipos}/page.tsx` (sin servicio en la URL hoy: los enlaces que llevan a ellas lo conservan, A2).
- Rutas `/proyectos/<id>/{dp,pr,dashboard,curva-s,registro-costos}`: regresión (ya funcionaban). Verifica con SV1 y SV2, cuenta A.
- `accion=crear` de Paquetes de Trabajo NO va aquí (F3-A).

## Qué NO hacer

- No toques RDTs, RQ ni redirects. No cambies permisos.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
