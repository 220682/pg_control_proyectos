# Resultados — Tanda T2 · Worker 1 · carril `local-worker-5`

Worker 1 · DeepSeek V4.1 Flash · rama `local-worker-5`, worktree `py_control_proyectos_web/.worktrees/local-worker-5`, HEAD `5e773c7`, árbol **limpio** al cerrar (sin cambios de código). Dev levantado en **3115** por este Worker (estaba caído) y **detenido al cerrar**. Navegador Chrome vía Playwright, un solo navegador. Cuentas leídas con **Read**, nunca impresas. **No se borró nada** (el borrado lo hará Victor).

**Skills revisados:** `pg_control_proyectos/.claude/skills/` = {cerrar-tanda, seguir-flujo-de-planes, trasladar-hallazgos, verificar-permisos-por-rol}; el worktree de la app **no** tiene `.claude/skills`. Usados: `verificar-permisos-por-rol` (con «Ver como») y `cerrar-tanda`. Capturas nuevas en `03-evidencia/capturas/dashboard-economia-y-curva-s/`.

## Proyecto de prueba creado — `PRUEBA-DASH` (lo que Victor debe borrar)

Creado con sesión real (Victor, admin) usando APIs de la app con sesión (nunca SQL). Prefijo `PRUEBA-DASH` en todos los nombres marcados.

| Pieza | Identificador exacto |
|---|---|
| **Servicio** | **PS-0009** · id `da33f1fa-0d2c-4cf6-adf3-2d723390b44d` · nombre `PRUEBA-DASH Servicio T2` |
| Cliente | `Cliente PRUEBA-DASH` |
| N° OC/OS | `PRUEBA-DASH-OC-001` |
| Área / estado | `OT` · `EN_PLANEACION` (NO desactivado) |
| Portafolio | `31598abb-e89a-4a8a-98af-bdbbe413d973` (programa `2cc56c7d-6273-4ac3-82e2-46121e37092b`) |
| DP importado | `PPTO-prueba-01.xlsx` → BAC **US$ 4.482,54**; 9 partidas con HH/HM con costo; storage `documentos-proyecto/da33f1fa-0d2c-4cf6-adf3-2d723390b44d/dp-origen-PPTO-prueba-01.xlsx` |
| Cronograma importado | `Cron-prueba-01.xlsx` → 14 actividades, 11 enlazadas al DP |
| Filas relacionadas | `proyecto_miembros` (Victor), `proyecto_documentos` (13 checklist AL_INICIO), notificaciones `DOCUMENTO_REQUERIDO` y storage con prefijo `da33f1fa-…/` |

Borrado sugerido: eliminar el proyecto `da33f1fa-0d2c-4cf6-adf3-2d723390b44d` (PS-0009) y sus filas/archivos por `proyecto_id`.

## Estados

| Ítem | Estado | Evidencia / causa |
|---|---|---|
| **F12** | **Observado — parcial (~80 %)** | Servicio creado/adjudicado por interfaz/API con datos marcados; **DP con partidas + HH/HM + costo** y **cronograma** importados y confirmados. **Falta**: Plan Maestro (requiere Paquetes de trabajo con partidas → no existe ninguno), aprobación del PM y **RDTs emitidos/validados hasta ~50 %**. No se borró nada ni se aplicó SQL. |
| **F13** | **Observado — parcial** | Con PS-0009 real: Dashboard **Completo** (KPIs económicos, `Costo directo (US$)`, BAC US$ 4.482,54, bloque «Costo real de recursos» con AC=0, Bloque E) y Dashboard **Parcial** con «Ver como» `supervisor_operativo` (sin `US$`, sin `Costo directo`, con Bloque E y enlace Curva S). **Curva S no dibujable** en PS-0009: sin PM aprobado PV/EV/AC quedan «Pendiente» (comportamiento correcto; la estructura ya quedó verificada en Tanda D con PS-0004). |
| **V03** | **Conforme** | Con «Ver como» `supervisor_operativo`: `perfil.roles=["supervisor_operativo"]`, y `PATCH /api/proyectos/da33f1fa…/tipo-dashboard` `{tipoDashboard:"COMPLETO"}` → **403 `{"error":"No autorizado"}`**. «Ver como» restaurado (`DELETE /api/ver-como` → 200). |
| **V04** | **Conforme** | Sesión real de López Cáceres (`supervisor_operativo`, área Supervisión operativa): `GET /api/curva-s?proyectoId=da33f1fa…&modo=economica` y `&modo=fisica` → **403 `{"error":"No tienes esta OT a cargo"}`**; Dashboard → «No tienes acceso al Dashboard de este servicio.»; Curva S → «No tienes acceso a la Curva S de este servicio.» Captura `T2-V04-*`. |

## Capturas (nuevas)
- `T2-F13-dashboard-completo-PS-0009.png` — Completo, KPIs económicos + Costo real de recursos.
- `T2-F13-dashboard-parcial-sin-economia-PS-0009.png` — Parcial con «Ver como» sin economía (sin USD, con Bloque E y enlace Curva S).
- `T2-V04-dashboard-ajeno-denegado-lopez.png` — Dashboard ajeno denegado a López.

## Handoff (≤15 líneas)
1. F12 quedó **parcial**: PS-0009 (`da33f1fa-…`) creado y marcado `PRUEBA-DASH`, con **DP** (BAC 4.482,54; HH/HM con costo) y **cronograma** (14 act.) cargados; falta **Paquetes de trabajo → Plan Maestro → aprobar PM → RDTs a ~50 %**.
2. El Plan Maestro **no se puede crear** sin Paquetes de trabajo (`/plan-maestro` lo exige); no existían y no se crearon.
3. F13 verificado en PS-0009 solo en la parte económica/parcial; **Curva S de PS-0009 no dibuja** por falta de PM (correcto), no es un fallo.
4. **V03 cerrado**: PATCH tipo-dashboard con rol sin economía → 403.
5. **V04 cerrado**: López (OT/servicio ajeno) recibe 403 de API y «No tienes acceso» en Dashboard y Curva S.
6. «Ver como» restaurado; servidor 3115 detenido; sin cambios de código; sin commits.
7. Pendiente para Victor: borrar PS-0009 y sus filas/archivos por `proyecto_id`.
8. **Llamadas: ~71** (objetivo ~60; se excedió por la importación real de DP/cronograma con esperas del parser).

## Mejoras (de trabajo)
- Importar el DP/cronograma reales por UI exige 2 pasos (analizar niveles → «Aprobar niveles») y cada POST del parser tarda 30–40 s; conviene reservar ~10 llamadas solo para esa carga.
- `playwright_browser_file_upload` no era fiable aquí: se usó `page.setInputFiles` con la ruta del fixture copiado a Temp con nombre ASCII (el original trae `N°`).
- Para la verificación en vivo fue más barato forzar «Ver como» por `POST /api/ver-como` + `page.reload` que por el combobox.

## Reglas de negocio detectadas
- Ninguna nueva. Confirmado que `/plan-maestro` exige partidas declaradas en Paquetes de trabajo (no basta el cronograma ni el DP); coherente con flujo 20. No se editó ningún flujo.

## Observaciones sobre la política
- El alcance de F12 (adjudicar → DP/cronograma → partidas HH/HM → PM con asignaciones → aprobar → RDTs a ~50 % → validar) no cabe en ~60 llamadas junto con F13/V03/V04: la sola carga de DP + cronograma con confirmación de niveles consume ~10 llamadas y >90 s de parser. Queda para clasificación del Auditor / decisión de Victor.

## Carpetas/archivos huérfanos
- Ninguno detectado. Se eliminó un `login-snap.md` temporal creado por error en la raíz de `pg_control_proyectos`.

## Fuentes de verdad revisadas
`src/app/api/proyectos/route.ts`, `.../[id]/dp/route.ts`, `.../[id]/tipo-dashboard/route.ts`, `.../ver-como/route.ts`, `src/app/(workspace)/.../dp|cronograma|plan-maestro|dashboard|curva-s`. Flujos 20 (por el requisito de Plan Maestro) inferido del propio código; **Fase E no tocada**.

## Número de llamadas
**~71** (excede el objetivo ~60).
