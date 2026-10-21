# Informe de Auditoría — Correcciones de la prueba del RDT en PS-0001

Fecha: 2026-10-21. Auditor independiente (T6). No se editó código ni flujos; solo este informe.

## Alcance auditado

Plan `../01-planes/2026-10-21-correcciones-prueba-rdt-ps0001.md` (Gate Spec y Gate 1 aprobados el 2026-10-21; Gate 2 pendiente). Los nueve huecos de la prueba del RDT en PS-0001, sus decisiones y su traslado a:

- La app real `py_control_proyectos_web`, commit local `981b2fd` (sin push; el Lote 0 ya está publicado como `ddb18ee`).
- Los flujos 04, 06, 09, 10, 11, 14, 18, 20, 21 y 22, `design.md` y los mockups (ediciones sin commit en este repositorio).
- El libro de hallazgos del plan (M1 y R1 a R7).

## Material revisado

- `AGENTS.md`, `docs/00-estandar-agentes/02-roles-y-delegacion.md` (§ Auditor) y la plantilla `06-informe-auditoria.md`.
- El plan completo (220 líneas) y `docs/02-trabajo-activo/01-planes/README.md`.
- App: `db/116_hh_transversales_fuera_del_ip.sql` contra la función de `db/112`, `db/pruebas/116_hh_transversales_verificacion.sql`, `src/app/api/rdts/partes/route.ts`, `src/app/api/rdts/route.ts`, `src/app/api/rdts/[id]/route.ts`, `src/app/api/rdts/catalogos/route.ts`, `src/app/api/proyectos/[id]/dp/equivalencias-cargos/route.ts`, `src/lib/dp/*`, `src/lib/curva-s/curva-s.ts`, `src/components/ui/FormularioCrearRdt.tsx`, `src/lib/dashboard/*`, `src/lib/informes/*`, `src/lib/config/registro-accesos.ts`, `matriz-base-flujo14.ts`, `src/lib/permisos/permisos.ts`.
- Flujos y mockups: `git diff` de los flujos 04, 06, 09, 10, 11, 14, 18, 20, 21, 22 y `design.md`, más búsquedas de texto residual en `docs/` completo.
- Ejecuciones: `npx tsc --noEmit`, `npx vitest run`, `python -I scripts/verificar-referencias.py`. No se ejecutó build (instrucción del Orquestador).

## Verificación de rama

El plan no usa rama de Worker ni worktree: el Gate 1 aprobó trabajar directo en `main` de la app. Comprobado con `git`:

- App: `main` adelantada de `origin/main` por `981b2fd` (un commit local, sin push). Árbol de la app limpio salvo dos archivos ajenos a este plan sin seguimiento: `db/095_cerrar_lectura_directa.sql` y `db/114_personal_datos_contacto.sql`.
- Este repositorio: `main`. Los cambios en flujos, mockups, `design.md`, el archivo de mejora M1 y el README de planes están sin commit (el propio plan lo reconoce: «falta el commit»). Esos mismos archivos de flujo contienen además ediciones sin commit de otros planes (restricciones, importar DP .xls, transversales, flujos 12, 16, 19). El commit debe tomar solo los hunks de este plan.

## Cumplimiento de SDD, plan, Punch List y evidencia

### 1. Trazabilidad de los nueve huecos

| Hueco / decisión | App (evidencia) | Flujo (evidencia) | Estado |
|---|---|---|---|
| Fecha futura bloqueada | `src/app/api/rdts/partes/route.ts:196` (`esFechaFutura`, 400 en POST, cubre crear y reemplazar); `FormularioCrearRdt.tsx` con `max=hoy` | 06 (fecha del reporte) | OK |
| Cargo sin tarifa bloquea (`CARGO_SIN_TARIFA`) | `partes/route.ts` (`cargosSinTarifaDelServicio`, 400) | 06, 04 (`rdt.recursos_sin_tarifa`) | OK |
| Equipos sin partida (WBS fuera) | `partes/route.ts` manda `wbs: null`; RPC `guardar_rdt_parte` inserta `v_equipo->>'wbs'` en columna nullable; se quitó la validación «equipo sin WBS válido del DP» en `[id]/route.ts`; columna eliminada del formulario | 06, 10, 22:45, `design.md:300` | OK, con residuos (ver abajo) |
| Met. acum. por clave, sin RECHAZADO | `catalogos/route.ts` (`.neq('estado_validacion','RECHAZADO')` y `acumularPorClave`); `estado_validacion` es `not null default 'REGISTRADO'` (`db/040:18-19`), el `neq` no pierde filas | 06, 18 | OK |
| Programado y avance reaplicados al cambiar la fecha | `FormularioCrearRdt.tsx` (`cambiarFecha`, `reaplicarProgramadoPorFecha`) | 06 | OK |
| Banner de motivo de rechazo | `FormularioCrearRdt.tsx` (`motivoRechazo`) | 06 | OK |
| HH de transversales fuera del IP | `db/116` y lectores de `hh_transversal_acum` | 06, 10, 11, 18, 20 | OK |
| Equivalencias de cargos del servicio | `equivalencias-cargos/route.ts`, `dp/route.ts` (409 `cargosSinFila`), `src/lib/dp/*` | 09 (sección nueva), 14 (fila línea 96, nota 18 línea 201) | OK |
| Curva S semanal con fecha de corte | `src/lib/curva-s/curva-s.ts` (`agruparSerieSemanal(serie, fechaCorte)`, `parcial`), `textos.ts` (`etiquetaSemanaCurvaS`) | 21 (Granularidad reescrita) | OK en la app; ver residuo R-4 |

Texto residual contradictorio encontrado (a corregir):

- **R-1** `docs/04-flujos-de-negocio/06-rdt.md:53`: «Avance real (%) de una partida = Met. acum. del servicio sobre la suma de sus metrados en el plan». El selector usa el avance por clave (`avanceRealDeClave`). Contradice la regla nueva de Met. acum. por clave.
- **R-2** Mockups con la columna de partida de equipos o el selector para equipos: `docs/05-diseno-y-referencias/mockups/crear-rdt-selector-paquetes.html:255` («Mismo selector para el WBS de las actividades C/NC, de los materiales y de los equipos») y las líneas de la tabla de equipos (~236-237, 339-341); `mockups/index.html:195` («mismo selector para C/NC, materiales y equipos»); `mockups/informes-supervision.html` (~392, 433, 544, columna «Partida» de equipos, válida solo para RDT anteriores al 2026-10-21).
- **R-3** `docs/04-flujos-de-negocio/11-dashboard.md:132`: «Tocar un cargo o un equipo muestra en qué partidas se usó». Con la regla nueva, un equipo de un RDT nuevo muestra «Sin partida vinculada» (`src/lib/dashboard/recurso-partidas.ts:99-103`). El flujo debe decir que el desglose por partida del equipo solo cubre RDT anteriores.
- **R-4** `docs/04-flujos-de-negocio/21-curva-s.md:127`: afirma que la descarga del Dashboard aplica `agruparSerieSemanal` con la fecha de corte. En la app `serieSemanal` (`src/lib/dashboard/datos-descarga.ts:293`) está exportada y probada, pero ninguna ruta de producción la llama. La afirmación no tiene respaldo en el código.

Sin residuos: no queda «Resuélvelo en Importar DP» en `docs/`; «posterior a la fecha de corte» en el flujo 21 sigue siendo válido (aplica a semanas que empiezan después del corte); `docs/01-contexto-repositorio/08-arquitectura-funcional-y-datos.md` no contradice (solo habla de la relación WBS-cronograma genérica).

Inconsistencia interna del plan (informativa): las filas T2 (línea 127) y Lote 3 (línea 143) citan `db/115`; la migración real es `db/116` (no existe `db/115`). La sección Entorno ya dice `db/116`.

### 2. Matriz de permisos y flujo 14

- La acción «Equivalencias de cargos del servicio» usa `puedeImportarDp` (`src/lib/permisos/permisos.ts:456`: administrador y jefe de proyectos), igual que la ruta (403 si no cumple) y la página `dp/page.tsx`. Coherente con la fila del flujo 14 (línea 96) y la nota 18 (línea 201).
- No existe prueba automática que lo cubra: `src/lib/config/matriz-base-flujo14.ts` y `src/lib/config/registro-accesos.ts` no tienen filas para «Importar DP» ni para la nueva acción, y `src/lib/config/matriz-accesos.test.ts` compara registro contra matriz base solo para accesos registrados (`DIFERENCIAS_CONOCIDAS` vacío). El commit `981b2fd` no tocó `src/lib/config` ni `src/lib/permisos`. No hay desajuste detectado, pero tampoco hay protección; es informativo.
- Hay prueba de permisos propia de la ruta: `equivalencias-cargos-api.test.ts` recorre los 13 roles.
- El artefacto «Matriz de permisos» (política de AGENTS.md) no se pudo actualizar desde esta cuenta (inaccesible); queda como pendiente de Victor para el Gate 2.

### 3. Revisión del código de `981b2fd`

- **(a) `db/116` frente a `db/112`.** El diff de la función `recalcular_pr_desde_rdt` cambia solo lo declarado: el reinicio añade `hh_transversal_acum = 0`, y la actualización de transversales pone `hh_d_acum = 0`, `hh_reales_acum = 0` y `hh_transversal_acum = hh_und_partida * metrado_contractual * v_p`. Es idempotente (`add column if not exists` y `create or replace`), por lo que aplicarla dos veces no falla. No redefine `curva_s_proyecto` (queda la de `db/112`, correcto). Ninguna migración posterior (113, 114) redefine `recalcular_pr_desde_rdt`. En la app, `hh_ganadas = Σ(metrado_acumulado × hh_und) − Σ hh_transversal_acum` cancela exactamente la fila transversal. `db/pruebas/116_hh_transversales_verificacion.sql` es de solo lectura, usa un identificador de reemplazo y es coherente con las fórmulas. Sin defectos.
- **(b) Riesgo de desplegar antes de la migración (BLOQUEANTE para el push, no es un defecto de código).** Cuatro lecturas piden la columna explícitamente: `src/app/(workspace)/proyectos/[id]/pr/page.tsx:183`, `src/lib/dashboard/cargar-dashboard.ts:63`, `src/app/(workspace)/programas/[id]/portafolios/[portafolioId]/page.tsx:76` y `src/app/programas/[id]/portafolios/[portafolioId]/dashboard/page.tsx:103`. Si `hh_transversal_acum` no existe, PostgREST devuelve error y `data: null`; los llamadores solo destructuran `{ data }` y usan `partidasDb ?? []`. Resultado: PR, Dashboard, dashboards de portafolio, Informes y descargas mostrarían cero partidas (BAC y EV en 0) sin error visible. El plan ya lista esto como pendiente; aquí se fija como condición dura: aplicar `db/116` antes del push o despliegue, y después recalcular el PR (el recálculo ocurre al validar o rechazar un RDT).
- **(c) Validación en servidor de `FECHA_FUTURA` y `CARGO_SIN_TARIFA`.** Solo `POST /api/rdts/partes` llama a `guardar_rdt_parte` (verificado por búsqueda), y ahí están ambas validaciones, incluido `reemplazar`. `POST /api/rdts` (subir RDT por archivo) usa la fecha del servidor, no puede ser futura. `PATCH /api/rdts/[id]` (validar o rechazar) no recibe fecha. Los borradores (`PUT` de borradores) aceptan cualquier fecha: están documentados en el flujo 06 como borradores no definitivos (informativo). Huecos informativos, ya documentados: cargos fuera del catálogo `recursos_cargos` y servicios sin presupuesto no se bloquean; un RDT antiguo validado con cargo sin tarifa sigue avisando por `avisarRecursosSinTarifa` (ahora registra los fallos).
- **(d) `PUT /api/proyectos/[id]/dp/equivalencias-cargos`.** 401 sin sesión; 403 si no `puedeImportarDp`; `exigirAlcance`; validación de cuerpo (máximo 100); 404 servicio; 400 si el servicio está CERRADO (únicamente existen EN_PLANEACION, EJECUCION y CERRADO según `db/001`); 400 sin presupuesto; `validarAsignacionesCargoFila` (cargo existe, sin tarifa aún, fila existe y es HH o MOI no MES, fila no ocupada por otro cargo, sin duplicados); luego `aplicarResolucionesRecursos`. La unicidad (proyecto + descripción del presupuesto) está protegida por la restricción única de base de datos y `upsert`; una carrera entre dos usuarios simultáneos solo se resolvería por esa restricción (menor, informativo).
- **(e) Dependientes de `rdt_equipos_parte.wbs`.** `recalcular_pr_desde_rdt`: el equipo sin WBS cae en `v_hm_legacy_equipos` y `v_costo_legacy_equipos`, es decir, en `costo_legacy_sin_partida_acum` y `hm_legacy_sin_partida_acum`; el PR lo muestra como fila «Equipos (sin partida)» (`pr/page.tsx:386-398`). Dos observaciones: la etiqueta puede ser imprecisa porque el mismo balde contiene también el costo legacy de actividades C/NC (informativo, proponer al responsable), y `hm_legacy_sin_partida_acum` no entra a HH ni IP (duda abierta ya anotada en los flujos 06 y 10). Informes: `armar-datos-costos.ts:121`, `datos-rdt.ts:182` y `cargar-fuentes.ts:38` muestran «—» (el flujo 22 línea 45 lo dice solo para RDT anteriores). El PDF, `parte.ts` y `plantilla.ts` están actualizados. No hay otro dependiente roto. Residuo documental: R-3.
- **(f) RDT RECHAZADOS fuera del acumulado.** Correcto (ver tabla). Nota informativa preexistente: al revisar un RDT no rechazado (REGISTRADO o REVISADO), su propio metrado cuenta en el Met. acum. que se muestra.

### 4. Libro de hallazgos

- M1: archivo `docs/03-aprendizaje-continuo/2026-10-21-esperados-independientes-de-la-app.md` existe, línea agregada al README del índice, y el script `scripts/esperados_rdt_ps0001.py` existe. Trasladada.
- R1 a R7: cada regla está escrita en su flujo (ver tabla de trazabilidad), integrada en la estructura del flujo y no como nota aparte. Trasladadas, salvo los residuos R-1, R-3 y R-4.
- Secciones obligatorias del plan (Mejoras, Reglas de negocio, Observaciones sobre la política, Carpetas/archivos huérfanos): presentes y completas. «Observaciones sobre la política: Ninguna» y «Huérfanos: Ninguno detectado» coinciden con `python -I scripts/verificar-referencias.py`: 47 archivos, huérfanos 0, enlaces rotos 0. El script lista 2 «menciones sin archivo» (`convenciones-de-trabajo.md` en `docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md`), preexistentes y ajenas a este plan.
- Faltan los archivos de progreso y evidencia homónimos: `docs/02-trabajo-activo/02-progreso/2026-10-21-correcciones-prueba-rdt-ps0001.md` y `docs/02-trabajo-activo/03-evidencia/2026-10-21-correcciones-prueba-rdt-ps0001/` no existen (el plan, línea 174, dice que se crean al activar el Gate 1). No hay registro de las pruebas de esta tanda.

### 5. Entorno

- `npx tsc --noEmit`: salida 0, sin errores.
- `npx vitest run`: 203 archivos aprobados y 1 omitido; 2225 pruebas aprobadas y 1 omitida; salida 0 (el plan citaba 2146 al cierre del Lote 0).
- Build no ejecutado (por instrucción).

## Verificación de la revisión de fuentes de verdad por fase

- Reglas de negocio nuevas: escritas en los flujos 06, 09, 10, 11, 14, 18, 20, 21 y 22 y en el 04; no se guardaron en archivos aparte. Hay cuatro residuos que contradicen lo nuevo (R-1 a R-4) y los mockups (R-2). Política de AGENTS.md («un Spec que entra en conflicto con lo escrito se implementa en todos los afectados»): incumplida parcialmente hasta corregir esos residuos.
- Flujo 14 al día con la acción nueva; artefacto «Matriz de permisos» sin actualizar (pendiente de Victor).
- No se detectó ninguna regla editada sin consultar a Victor en el libro de hallazgos.

## Clasificación de hallazgos

Prioridad según el Orquestador: bloqueante / a corregir antes del Gate 2 / informativo.

- `APLICAR AHORA` (a corregir antes del Gate 2):
  1. Crear el progreso y la evidencia homónimos (`02-progreso/` y `03-evidencia/`) con los resultados de `tsc`, `vitest`, verificación de `db/116` y esperados de la prueba.
  2. Corregir `06-rdt.md:53` (R-1).
  3. Corregir los mockups con equipos y partida (R-2) o marcarlos como válidos solo para RDT anteriores.
  4. Corregir `11-dashboard.md:132` (R-3).
  5. Corregir o respaldar con código la afirmación del flujo 21 línea 127 sobre la descarga del Dashboard (R-4): o se conecta `serieSemanal` a la descarga, o el flujo deja de afirmarlo.
  6. Cambiar `db/115` por `db/116` en las filas T2 y Lote 3 del plan.
  7. Comitear solo los hunks propios de este plan (los flujos tienen ediciones de otros planes).
- `PROPONER A RESPONSABLE` (Victor):
  1. **BLOQUEANTE para el push:** aplicar `db/116` antes de publicar `981b2fd` y recalcular el PR; si no, PR, Dashboard, portafolios, Informes y descargas muestran cero partidas sin error.
  2. Actualizar el artefacto «Matriz de permisos» con «Equivalencias de cargos del servicio».
  3. Decidir la duda abierta: `hm_legacy_sin_partida_acum` y las HH contractuales de transversales en el Plan Maestro frente a HH e IP.
  4. Decidir si la fila «Equipos (sin partida)» del PR necesita otra etiqueta, porque el balde incluye también costo legacy de C/NC.
  5. Limpieza de los cinco RDT de prueba y la decisión sobre Braulio (pendientes de la prueba).
- `NO PROMOVER`: los borradores aceptan fechas futuras; el metrado propio del RDT en revisión cuenta en Met. acum.; la numeración de migraciones salta el 115; `db/README.md` no lista migraciones recientes. Son observaciones de bajo riesgo.
- `PROPONER SKILL`: ninguno.

## Pendientes técnicos y documentales

- Aplicar `db/116` (ruta completa: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\db\116_hh_transversales_fuera_del_ip.sql`), luego ejecutar el SQL de verificación `...\db\pruebas\116_hh_transversales_verificacion.sql` sustituyendo el identificador de proyecto, y recién entonces hacer push a `main`.
- Registrar progreso y evidencia del plan.
- Corregir los cuatro residuos documentales y los mockups.
- Commit del repositorio documental limitado a los hunks de este plan.
- Informativo: ninguna prueba automática relaciona el flujo 14 con la acción de equivalencias; conviene agregar «Importar DP» y la acción nueva al registro y a la matriz base en un plan futuro.

## Recomendación

`Requiere corrección`.

No hay defectos de código que impidan el Gate 2: `tsc` limpio, 2225 pruebas aprobadas y la lógica de `db/116`, las validaciones de servidor y la ruta de equivalencias son correctas. Se pide corregir los residuos documentales, crear progreso y evidencia, y dejar como condición del push que `db/116` esté aplicada antes del despliegue (hallazgo bloqueante de despliegue, no de código). Con eso queda `Listo para Gate 2`.
