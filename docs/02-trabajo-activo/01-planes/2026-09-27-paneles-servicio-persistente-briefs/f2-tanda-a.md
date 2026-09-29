# F2-A · Servicio persistente en el shell: helper, panel izquierdo y envío del servicio

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F2 · **Depende de:** F1-B cerrada (registro único con `hrefItemPanel` derivado).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-01 | Cuenta A abre SV1 desde "Todos los servicios": el panel izquierdo muestra el servicio actual (N° OT y nombre) y el panel derecho tiene sus chips activos | Captura de ambos paneles y URL |
| PL-15 | Volver a "Todos los servicios" y elegir SV2: los paneles muestran SV2 sin restos de SV1 | Captura |
| PL-16 | "Todos los servicios" limpia el servicio: paneles sin servicio, los chips que requieren servicio quedan inertes y los que funcionan sin servicio (Plan Maestro, Status de Requerimiento, Consolidado RQ, Status de RDTs) navegan como en la línea base | Captura + comparación con la línea base de F0 |
| PL-37 | El N° OT y el nombre que muestra el panel izquierdo corresponden al `id` de la URL (SV1 y SV2) | Captura + comparación con la ficha del servicio |
| PL-47 | `?proyectoId=` inexistente, de un servicio archivado o sin acceso: el shell no falla, trata la sesión como sin servicio (o muestra un aviso claro) y no revela nombre ni datos del servicio | Captura + consola |
| PL-66 | Usuario o momento sin servicio elegido: los paneles muestran el estado sin servicio, sin errores y con Recursos de empresa visible | Captura |
| PL-72 | Los redirects del servidor conservan el servicio sin abrir un redireccionamiento abierto: el helper solo acepta identificadores con formato de id y rutas internas | Prueba unitaria del helper |

## Entregable sin ID: helper de servicio
`src/lib/config/servicio-contexto.ts` (+ `.test.ts`): añadir y leer `?proyectoId=`; solo acepta identificadores con formato de id y rutas internas (sin redirección abierta: PL-72). El registro envía el servicio a todo acceso con `requiereServicio` `si` u `opcional`.

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- `resolverProyectoId(pathname, proyectoIdQuery)` (`WorkspaceShell.tsx` ~114) solo reconoce `/proyectos/[id]/…` y `?proyectoId=` en `/mi-entorno` y `/plan-maestro`. Debe reconocer `?proyectoId=` en **toda** ruta del workspace y validar el servicio contra los servicios visibles del usuario (fuente por verificar: `src/app/api/proyectos/vigentes/route.ts` o consulta en `(workspace)/layout.tsx`, 62 líneas, que arma `UsuarioShell`).
- `WorkspaceShellInner` (~358) usa `usePathname`/`useSearchParams`; `WorkspaceShell` (~493) lo envuelve en `Suspense` con fallback «Cargando…». `ContenidoNav` (~123): enlace «Todos los servicios» (`rutaTodosLosProyectos`) y bloque Proyecto; `ContenidoHerramientas` (~289) muestra «Selecciona un servicio para habilitar las herramientas del panel.» cuando no hay servicio.
- Muestra el servicio actual (N° OT y nombre) en el panel izquierdo. Solo «Todos los servicios» y el logo limpian el servicio; los enlaces del pie y de Recursos lo conservan (A2); `/programas/**` no lleva servicio.
- **Next 16:** `searchParams` asíncrono, `useSearchParams` bajo `Suspense`: consulta `node_modules/next/dist/docs/` con Grep del tema antes de tocar el shell (R10). La URL es la única fuente de verdad; cambios con `router.replace` (R11).
- PL-16 se compara con la línea base LB-03 de F0-B. PL-47: `?proyectoId=` inexistente, archivado o ajeno: sin fallo ni datos del servicio.

## Qué NO hacer

- No cambies permisos. No toques las pantallas de RDTs/RQ (F2-C) ni los redirects (F2-D).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
