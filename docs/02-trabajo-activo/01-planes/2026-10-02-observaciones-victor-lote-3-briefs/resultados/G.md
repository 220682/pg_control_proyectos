# Resultados Tanda G — Worker 1

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Carril:** `local-worker-4` (worktree `.worktrees\local-worker-4`).
**Commits de esta tanda:** `b59a82b` (fix endpoints F2-B/F2-C) y `871b238` (integración del modal en la pantalla). Sin merge, sin push.

## Qué se hizo

### Ítem 1 — Integrar `NotificacionImpacto` en la pantalla del Cronograma (Conforme)

- `src/app/api/cronograma/route.ts` (GET): la respuesta incluye ahora `planMaestroAprobado: boolean` (consulta a `proyecto_plan_maestro` con `estado='APROBADO'`, mismo criterio que la pantalla PR). Cambio de contrato documentado: solo campo de lectura nuevo; no rompe consumidores (el formulario era el único).
- `src/app/(workspace)/cronograma/page.tsx`: pasa `puedeEditarActividad={puedeEditarActividadCronograma(usuario.roles)}` (solo Admin/JP; no se creó permiso nuevo).
- `src/components/ui/FormularioCronograma.tsx`: la tabla de actividades muestra columna «Acciones» con botón «Editar» **solo si** `puedeEditarActividad && planMaestroAprobado`. Al pulsar: se abre `NotificacionImpacto` (que trae el `GET .../impacto` y muestra partes afectadas). «Editar de todos modos» abre el formulario; «Cancelar» cierra sin tocar nada.
- `src/components/cronograma/EditarActividadCronograma.tsx` (nuevo): formulario de nombre / duración / fechas; al guardar llama el `PATCH /api/cronograma/actividades/[id]` existente (`77c3ab2`) y recarga la lista. El servidor re-valida permiso, alcance y Plan Maestro (409) — la columna oculta no es la guardia.

### Fix necesario dentro del carril (commit `b59a82b`)

La verificación en vivo destapó que los dos endpoints de F2 (commits `d985d33`/`77c3ab2`, ya en el carril) no funcionaban contra el esquema real:

1. `GET .../impacto` consultaba `rdt_partes.actividad_id`, **columna que no existe** (42703; el endpoint devolvía 500 con `{"error":""}`). La cadena real de impacto: `cronograma_actividad_partidas` (o el `dp_partida_id` legacy de la actividad) → `rdt_actividad_partidas` → `rdt_actividades.parte_id` → partes distintos. Reescrito así, leyendo los vínculos con el cliente admin (la RLS los oculta al usuario — mismo criterio que `GET /api/cronograma`). Verificado contando a mano por REST en PS-0009: esperado 2, devuelto 2 (×3 actividades).
2. `PATCH .../actividades/[id]` escribía con el cliente del usuario, pero `cronograma_actividades` solo tiene política de **lectura** (db/036) → todo update fallaba (500 con mensaje vacío). Ahora escribe con el admin después de validar rol + alcance en servidor — mismo patrón que el import/reemplazo de `/api/cronograma` y las otras rutas del repo.
3. Además: los 500 de estas rutas ya no devuelven cadena vacía cuando Supabase no trae mensaje.

Ninguno de los dos archivos es del Lienzo del Plan Maestro ni de RDT: son los endpoints del flujo Cronograma que el propio brief da como existentes; sin este fix el ítem 1 era imposible de integrar contra `77c3ab2`. No se tocó `middleware.ts`, ni permisos, ni migraciones.

### Ítem 2 — Botón «Recalcular PR» (Conforme)

- El wiring **ya estaba completo** en el carril: `src/components/pr/RecalcularPr.tsx` (`7f755df`) se importa y renderiza en `src/app/(workspace)/proyectos/[id]/pr/page.tsx:278` bajo `puedeGestionarPr(roles) && cabecera`. Verificado en vivo (abajo): el botón aparece en el SSR de la pantalla del PR y el `POST /api/proyectos/[id]/pr/recalcular` responde 200 `{"ok":true}`. No requirió cambios.

## Validación

Comandos en el worktree `local-worker-4`:

- `npx tsc --noEmit` → **exit 0** (corrido dos veces: tras la integración y tras el fix).
- `npx vitest run src/app/api/cronograma src/lib/cronograma src/lib/pr src/lib/permisos` → **12 archivos, 174/174 pruebas passed** (incluye `cronograma-get.test.ts`, que sigue verde con el campo nuevo).

## Verificación en vivo (técnica SSR/API sin navegador del aprendizaje 2026-10-02)

Servidor: `npm run dev -- --webpack -p 3114` en el worktree (arrancado y detenido por esta tanda; nadie más lo tenía corriendo). Sesión: password grant de Supabase con la cuenta A + cookie `sb-<ref>-auth-token` (`base64-` troceado a 3180, formato verificado leyendo `@supabase/ssr`: `BASE64_PREFIX`, `MAX_CHUNK_SIZE=3180`, chunks `nombre.i`). Credenciales y tokens nunca impresos; scripts temporales fuera del repo (`%TEMP%\opencode`).

```
=== VERIFICACION EN VIVO (dev :3114, cuenta A, sin secretos en salida) ===
OK  · GET /api/proyectos/vigentes · PS-0004=true PS-0007=true
OK  · SSR GET /cronograma?proyectoId=PS-0004 · HTTP 200, 77816 bytes
OK  · GET /api/cronograma PS-0004 · planMaestroAprobado · actividades=65
OK  · GET /api/cronograma PS-0007 · planMaestroAprobado=false · actividades=14
OK  · PATCH PS-0007 (sin PM) rechaza 409 · HTTP 409 · "Solo se puede editar el cronograma cuando el proyecto tiene un Plan Maestro apro…"
OK  · GET impacto (actividad 1 de PS-0004) · HTTP 200 · partesAfectadas=0 · "No hay RDT asociados…"
OK  · PATCH editar nombre (PS-0004) · HTTP 200
OK  · PATCH restaurar nombre original · HTTP 200
OK  · Lectura devuelta: nombre restaurado (dato intacto) · orden=1
OK  · SSR GET /proyectos/PS-0004/pr muestra «Recalcular PR» · HTTP 200, 523616 bytes
OK  · POST /api/proyectos/PS-0004/pr/recalcular · HTTP 200 · {"ok":true}
OK  · PATCH id inexistente rechaza 404 · HTTP 404
=> TODO OK (12/12)
```

Extra (cadena de impacto con RDT reales, PS-0009 `PRUEBA-DASH`): el conteo esperado calculado por REST coincide con el endpoint — `GET impacto -> HTTP 200 | esperado 2 | devuelto 2` en tres actividades («Esta edición afectará a 2 parte(s) de RDT…»).

Escrituras hechas (todas reversibles y verificadas restauradas; los servicios existentes son de prueba según Victor, 2026-09-30): PS-0004 nombre de actividad 1 → «… · G» → restaurado; PS-0004 `POST pr/recalcular` (idempotente, mismo cálculo que al validar un RDT). PS-0007 solo recibió el PATCH rechazado por 409 (sin escribir).

## Hallazgos

### Mejoras (de trabajo)

- G-M1 | El patrón de evidencia sin navegador (MB2) funcionó de punta a punta con formato exacto verificado en `@supabase/ssr` (versión actual: prefijo `base64-`, chunks `.0/.1` con nombre-sufijo, no separador `%`); vale la pena fijar en el brief la ruta de la memoria (`cuentas-prueba.md`) y el puerto del carril para no re-buscarlos.
- G-M2 | Antes de integrar endpoints ajenos ya commiteados, conviene una llamada viva mínima (GET/PATCH con valor neutro) — aquí destapó en una corrida los dos fallos de esquema que tsc y vitest no podían ver (mock de Supabase devuelve tabla vacía, no error de columna).

### Reglas de negocio acordadas en esta tarea

- G-R1 | Impacto de editar una actividad del cronograma = número de **partes de RDT distintos** que tocan, directa o indirectamente, las partidas vinculadas a esa actividad (cadena `cronograma_actividad_partidas`/`dp_partida_id` legacy → `rdt_actividad_partidas` → `rdt_actividades.parte_id`); no existe relación directa `rdt_partes → actividad`. Implementado en `GET /api/cronograma/actividades/[id]/impacto` (commit `b59a82b`). — **no se cuenta el estado de validación del parte** (borrador y validado cuentan); a confirmar con Victor si el aviso debe limitar a VALIDADOS.
- G-R2 | Edición individual de actividades: habilitada en pantalla solo con permiso `puedeEditarActividadCronograma` **y** Plan Maestro `APROBADO`; el servidor re-valida (403/409/404) y el aviso de impacto se muestra antes de editar (flujo 15, reglas ya escritas — queda reflejado en la implementación; el flujo debe anotar la columna `planMaestroAprobado` del GET y que el conteo de impacto sigue G-R1).

### Observaciones sobre la política

- G-O1 | Los endpoints `77c3ab2`/`d985d33` (tandas anteriores del mismo carril) quedaron commiteados sin ninguna verificación en vivo contra la base real — tsc/vitest verdes daban falsa señal de cierre; fallaban 100 % al primer uso. Sugiere que el criterio de «Conforme» de un endpoint exija al menos una llamada real (o que el Auditor lo pida explícitamente). Clasifica el Auditor.
- G-O2 | La ruta `crearClienteServidor` escribe tablas cuyas políticas RLS solo permiten lectura; el fallo viene como error de PostgREST con `message` vacío (difícil de diagnosticar en pantalla). No es regla de negocio; posible nota de convención. Clasifica el Auditor.

### Carpetas/archivos huérfanos

- Ninguno creado por esta tanda. El script de evidencia SSR/API quedó en `%TEMP%\opencode` (fuera de ambos repos, sin secretos en contenido); dev server de 3114 detenido.

## Pendientes

- Que el reposicionamiento automático de RDTs al confirmar la edición (texto del aviso: «deberán reposicionarse automáticamente») no está implementado en el PATCH — hoy el PATCH solo guarda nombre/duración/fechas y el aviso lo anticipa. Es terreno de RDT (tanda E/F): no lo toqué; reportar a Victor/Orquestador.
- Integración del GET `/impacto` en PS-0004 devuelve 0 porque los RDT reales de ese servicio no están vinculados por partida a sus actividades de cronograma (los 51 vínculos `rdt_actividad_partidas` no intersectan los 18 `cronograma_actividad_partidas` de PS-0004). Caso positivo probado en PS-0009. No es bug del endpoint, es dato; puede interesar a la tanda de RDT.
- Cierre documental (flujo 15 / matriz de permisos si el Auditor lo ve necesario) y decisión sobre borrar `PS-0007`/`PS-0009` siguen en manos del Documentador/Victor.