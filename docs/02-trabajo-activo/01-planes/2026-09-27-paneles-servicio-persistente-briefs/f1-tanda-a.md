# F1-A · Registro único de accesos: contrato, derivaciones y NAV_PROYECTO

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F1 · **Depende de:** F0-A, F0-B y F0-C cerradas.
**Punto de commit:** Al cerrar la tanda, en `local-worker-1` (sin cambio visible).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-51 | Cada acceso tiene todos los metadatos (id, nombre, grupo, tipo, ruta o acción, requiere servicio, permiso, visibilidad por panel) y la prueba de integridad lo comprueba (ids únicos, sin rutas sin permiso declarado por omisión silenciosa) | `npm test` |

## Entregable sin ID: registro base
Crear `src/lib/config/registro-accesos.ts` (+ `.test.ts`) con el contrato de abajo, migrar a él los 41 ítems de `NAV_PROYECTO` y hacer que `NAV_PROYECTO`, `encontrarItemNavProyecto`, `clavesConRutaEntorno` y `hrefItemPanel` sean derivaciones puras del registro (parametrizadas por él, para probarlas con un registro de prueba). **Sin cambio visible.**

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Contrato propuesto (el Worker puede ajustar nombres si lo justifica):
```ts
interface AccesoRegistrado {
  id: string; etiqueta: string; grupo: string; tipo: 'informativo' | 'accion';
  ruta?: (servicioId?: string) => string;            // sin ruta => chip inerte
  requiereServicio: 'si' | 'opcional' | 'no';         // 'opcional': abre sin servicio y lo preselecciona si lo hay
  permiso?: (roles: Rol[]) => boolean;               // en F1: la función VIGENTE de permisos.ts (no cambia quién puede)
  tituloDeshabilitado?: string;
  visible: { izquierdo: boolean; centro: boolean; derecho: boolean; accesoRapido?: boolean };
  icono; colorClase; orden;
}
```
- Hoy (`src/lib/config/nav-proyecto.ts`, 365 líneas): `ItemNavProyecto {clave, etiqueta, icono, colorClase, ruta?}`, `GrupoNavProyecto {titulo, colorTexto, items}`, `NAV_PROYECTO` (8 grupos, 41 ítems; 9 de ellos son `itemNotificaciones`), `CHIPS_ACCESO_RAPIDO` (7 claves, ~297), `hrefItemPanel` (~322: 9 excepciones por clave: `crear-requerimiento-servicios`, `rdt`, `notificaciones-*`, `status-requerimiento`, `consolidado-rq`, `crear-rdt`, `status-rdts`, `listado-rdts`, `consolidado-rdts`, `plan-maestro`).
- Pruebas actuales: `nav-proyecto.test.ts` (181 líneas) fija 41 ítems (líneas 24-28), 8 notificaciones (~106) y que Cronograma exige servicio. Reescríbelas como pruebas de ubicación y comportamiento (no solo el contador).
- **PL-51:** prueba de integridad: ids únicos; cada acceso con todos los metadatos; ninguna ruta sin `permiso` declarado por omisión silenciosa (un acceso sin restricción declara `permiso` explícito).
- Mantén `requiereServicio: 'si'` en Cronograma (decisión previa; C20). Los cambios de destino declarados de la migración (unión `rdt`/`subir-rdt`, E3) se hacen en F1-B.

## Qué NO hacer

- No toques `grupo-proceso.ts`, `WorkspaceShell.tsx` ni `PanelSecciones.tsx` (F1-B y fases siguientes). No cambies permisos.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
