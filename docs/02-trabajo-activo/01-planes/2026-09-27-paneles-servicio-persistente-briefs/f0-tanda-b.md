# F0-B · Línea base en el navegador: paneles, chips, asistente y servicios de prueba

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F0 · **Depende de:** F0-A cerrada.
**Punto de commit:** Ninguno (solo evidencia).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda

Sin filas de Punch List. Entregables LB-02 a LB-05 (sin fila de Punch List; son la base de regresión de PL-16, PL-42, PL-77, PL-80, PL-106 y PL-117).

## Entregables sin ID (evidencia en `03-evidencia/`)
- **LB-05 Servicios de prueba:** elige SV1 (vigente con DP, cronograma y Plan Maestro), SV2 (otro vigente) y SVX (la cuenta B no es miembro en `proyecto_miembros`; si no hay, decláralo). Nómbralos por N° OT. Anota el rol de la cuenta B tal como lo muestra el pie del panel izquierdo (`rolPrincipal`).
- **LB-02 Capturas de paneles (máx. 12 en total, ancho ≤ 1440):** cuenta A con servicio; cuenta B con servicio; cuenta A sin servicio; Mi entorno con A y con B; móvil (390 px) con el cajón izquierdo y con el derecho abiertos, con servicio.
- **LB-03 Tabla chip → destino → habilitado (por cuenta A y B):** derívala del código y confirma unas 10 filas en el navegador, no chip por chip.
- **LB-04 Asistente actual (4 capturas):** barra al pie con servicio en escritorio; sin servicio (no aparece); móvil con servicio (no aparece); copia en la pantalla del portafolio.

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Arranque: `npm run dev -- --webpack -p <puerto libre>` en el worktree (comprueba el puerto con `Get-NetTCPConnection`); al cerrar, detén solo el proceso que iniciaste. No leas `.env.local`.
- Origen de cada chip (para LB-03): `hrefItemPanel` (`src/lib/config/nav-proyecto.ts` ~322: excepciones por clave), `herramientasPorGrupo` (`src/lib/notificaciones/grupo-proceso.ts` ~143: Mi entorno), rutas fijas y grupo Proyecto del panel izquierdo (`src/components/ui/WorkspaceShell.tsx` `ContenidoNav` ~123-287; `RUTA_PERSONAL/CARGOS/EQUIPOS/CAUSAS_CNC` ~36-39), `AccesosRapidos` y `GruposAccordion` (`src/components/ui/PanelSecciones.tsx` ~26 y ~77). El servicio se reconoce en `resolverProyectoId` (~114): solo `/proyectos/[id]/…` y `?proyectoId=` en `/mi-entorno` y `/plan-maestro`.
- Asistente: `<ChatPlaceholder />` en `WorkspaceShell.tsx` ~464 (dentro de `{proyectoId && …hidden…lg:block}`) y en `src/app/(workspace)/programas/[id]/portafolios/[portafolioId]/page.tsx` ~186.
- Playwright: herramientas `mcp__playwright__*` (si no están conectadas, `claude-in-chrome`). Login con las cuentas A y B según `00-reglas-de-contexto.md`.

## Qué NO hacer

- No modifiques código. No guardes, borres ni subas datos.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
