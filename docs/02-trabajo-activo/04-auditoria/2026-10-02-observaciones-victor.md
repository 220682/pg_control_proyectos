# Informe de Auditoría — Observaciones de Victor (Lote 1): checklist, área Jefatura y error de cronograma

> Plan auditado: `docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-plan.md` (Spec: `2026-10-02-observaciones-victor.md`). Auditor de solo lectura: no se editó código, flujos ni documentos; solo este informe. No se hizo merge ni se aprobó en nombre del responsable.

## Alcance auditado

Spec (Gate Spec aprobado), Plan (Gate 1 aprobado), código de `py_control_proyectos_web` en `local-worker-1` (con `local-worker-2` mergeada), flujos `12-checklist.md`, `02-usuarios.md`, `14-accesos-y-restricciones.md`, libro de hallazgos del plan y los comandos de verificación (vitest, tsc, lint; build no re-ejecutado aquí).

## Primer chequeo (git) — textual, no de memoria

Worktree `py_control_proyectos_web\.worktrees\local-worker-1`:

- `git log --oneline local-worker-1 --not main` → los 4 commits del trabajo:
  - `1e8cf52` feat: checklist — catálogo definitivo, responsable para todos y completado por check (Worker 1, O1+O3)
  - `9ad0640` feat: área Jefatura (JF) y cronograma — logging y corrección del error de lectura (Worker 2, O2+O4)
  - `3951668` Merge branch 'local-worker-2' into local-worker-1
  - `ce5623e` chore: integración carriles + área JF en area-usuario + db/README
- `git branch --contains 1e8cf52` → `* local-worker-1` (solo).
- `git branch --contains 9ad0640` → `* local-worker-1`, `+ local-worker-2`.
- `git branch --contains ce5623e` → `* local-worker-1` (solo).
- `git merge-base --is-ancestor ce5623e main` → salida `False` (main **no** contiene el trabajo).
- `main` = `647999a` = `origin/main` (F5-H). `local-worker-2` limpia, HEAD `9ad0640`.

**Conclusión:** la implementación está en `local-worker-1`, con `local-worker-2` mergeada a ella, y **no** está en `main`. Correcto según el flujo SDD. ✓

## Segundo chequeo (libro de hallazgos)

En el plan, filas RB1 y RB2 en `Reglas de negocio acordadas en esta tarea`:

| ID | Estado declarado | Verificación |
|---|---|---|
| RB1 (catálogo definitivo del checklist) | `Trasladada` (commit `5f1ed31`) | ✓ commit `5f1ed31` en `pg_control_proyectos` — "trasladar RB1 … y RB2 … a los flujos"; destino `12-checklist.md` actualizado (13 ítems, completar por check). |
| RB2 (área JF = "Jefatura") | `Trasladada` (commit `5f1ed31`) | ✓ mismo commit; destino `02-usuarios.md` actualizado. Cierre de filas en `cd3465b` "cerrar filas RB1 y RB2 (Trasladada)". |

Ambas filas con destino y commit. ✓

## Revisión técnica (O1–O4)

- **O1 ✓** — `editor-checklist.tsx` ya no pasa `filtrarPorRolClave` (los 3 usos de `SelectorUsuario` van sin filtro). `lista-usuarios.ts` ordena por `PRIORIDAD_ROL_PRINCIPAL` y luego nombre, y eso se refleja en `etiquetaSelector`. El desplegable lista todos los usuarios (administrador incluido) en orden de rol. Matiz menor: el prop `filtrarPorRolClave` sigue existiendo en `SelectorUsuario.tsx` pero quedó sin uso (prop muerto, no es defecto).
- **O2 ✓** — `db/088_area_jefatura.sql` renombra `areas` `PR`/`Proyecto` → `JF`/`Jefatura` de forma idempotente (guarda contra `JF` existente), conservando `id` (los `perfiles.area_id` siguen apuntando). `area-usuario.ts` mapea `jefe_de_proyectos`/`administrador` → `JF`, fallback `JF` y `NOMBRE_POR_CODIGO['JF']='Jefatura'`. No queda `PR` residual como código de área: solo `pr` como clave de documento (reporte del proyecto), que es correcto. ✓
- **O3 ✓** — `db/087_catalogo_checklist.sql`: renombres (`recursos_sin_costo`, `personal_requerido`, `pets`, `requerimiento`), inserts de `cronograma`/`paquete_trabajo`/`plan_maestro` (orden 4/7/8), delete de `materiales_con_costo` (limpiando antes sus `proyecto_documentos`, sin cascade en la FK), orden 1–13, columna `completado` y `alter column rol_responsable_id drop not null`. `checklist.ts` (`documentoCompleto` = flag `completado`), `page.tsx` + `toggle-completado.tsx` y el `PATCH /api/proyectos/[id]/documentos/[documentoId]` implementan el completado manual. `dp/route.ts`, `confirmar-transicion/route.ts` y `documentos/[documentoId]/route.ts` usan `completado`. Grep de consumidores (`documentoCompleto`/`checklistCompleto`/`documentosPendientes`): solo `checklist.ts`/test + las 4 rutas de API, todas coherentes. Nota: `proyectoTieneDp` sigue en `page.tsx` pero solo para etiquetas de navegación (Ver/Cargar DP/PR), no para completitud — aceptable.
- **O4 ✓ (con matiz)** — `api/cronograma/route.ts`: `detectarFormatoCronograma` acepta por MIME y con fallback por extensión (`.xlsx`/`.xlsm`/`.pdf`); `console.error('[cronograma] No se pudo leer/parsear el archivo', { formato, archivo, error })`; `respuestaErrorInesperado` loguea y devuelve el mensaje; el catch de parseo devuelve `No se pudo leer el archivo: ${mensaje}`. `FormularioCronograma` muestra `traducirErrorApi(body.error)` y, al ser mensajes en español, `traducir-error.ts` los deja pasar (el mensaje específico llega a pantalla). **Matiz:** la corrección de raíz fue solo la detección de formato (MIME→extensión); los parsers (`parser-excel`/`parser-pdf`) no cambiaron. Es una causa raíz plausible (algunos navegadores reportan `application/octet-stream` para un `.xlsx`), pero el éxito end-to-end de la importación queda **sin verificar documentalmente** (no hay smoke con los archivos de prueba).

### Comandos de verificación

- `npx vitest run` → **99 archivos, 1026 tests, todos pasan**. ✓
- `npx tsc --noEmit` → **sin errores**. ✓
- `npm run lint` → 27 problemas (9 errores, 18 warnings), **todos en archivos ajenos al plan** (CarpetaRdts, FormularioRequerimiento, ListadoRequerimientos, RefrescoDatos, TablaListadoRdts, `dp/agregacion.ts`, etc.). El único aviso en archivo tocado es `checklist.ts:32` (`_documento` sin usar, parámetro `_` intencional). Coherente con lo reportado por los Workers. ✓
- `npm run build` → **no re-ejecutado aquí** (pesado); reportado verde por los Workers y consistente con tsc + vitest.

## Contradicción a evaluar (flujo 14)

El Documentador dejó sin editar `14-accesos-y-restricciones.md`. Su nota 4 y la fila «Subir documento del proyecto (catálogo AL_INICIO/CIERRE)» describen la acción ligada a `catalogo_documentos.rol_responsable_id` y al auto-completado. Tras O3: (a) `rol_responsable_id` es nullable y deja de ser la fuente del responsable (manda el responsable concreto por proyecto, `responsable_usuario_id`, D6); (b) completar se separa de subir (check manual). La acción «Subir documento» **sigue vigente en código** (POST `documentos/[documentoId]` para ARCHIVO; `puedeSubirDocumentoAsignado` ya usa el rol override de `proyecto_documentos`, no el del catálogo), pero la **redacción de la nota 4** («según `catalogo_documentos.rol_responsable_id`») quedó desactualizada, y el flujo 12 (ya actualizado) sigue citando en su línea 5 la «nota 4 de esa tabla». **Clasificación: PROPONER A RESPONSABLE** (deuda documental; no bloquea el merge de código).

## Clasificación de hallazgos

### APLICAR AHORA

1. **Completar la fase documental D:** no existen `02-progreso/2026-10-02-observaciones-victor.md`, ni `03-evidencia/2026-10-02-observaciones-victor.md`, ni la carpeta `…-briefs/`. El Spec (sección «Estrategia de prueba / evidencia») exige evidencia de smoke (checklist GET/PATCH con orden/nombres/responsables; importación de cronograma éxito y fallo con mensaje específico; área «JF — Jefatura»). Sin ella, O4 (y los criterios de aceptación) quedan sin evidencia documental. El Documentador debe generar progreso y evidencia (o declarar explícitamente dónde viven).
2. **Confirmar O4 con smoke real** usando `CRON-PROMCOSER-AESA-001.pdf` y `Cron-prueba N°01.xlsx` (éxito + fallo con mensaje específico). Es la única forma de cerrar R1/B4: por lectura de código solo está verificado el mecanismo de detección de formato, no que la importación funcione de punta a punta.

### PROPONER A RESPONSABLE

1. **Flujo 14 (contradicción de arriba):** actualizar la nota 4 y la fila «Subir documento del proyecto» a la nueva semántica — el responsable es el concreto del ítem en el proyecto (o administrador/jefe de proyectos), y «completar por check» se separa de «subir archivo» — y alinear la referencia desde el flujo 12 (línea 5).
2. **Archivo de prueba modificado y sin commitear** en el repo de documentación: `docs/06-material-de-apoyo/Informacion para pruebas/PPTO-prueba N°01.xlsx` (está `M`). No es del Auditor; confirmar con el responsable si debe commitearse o revertirse.

### NO PROMOVER

1. El prop muerto `filtrarPorRolClave` en `SelectorUsuario.tsx` (quedó sin uso; limpieza opcional, no es defecto).
2. `proyectoTieneDp` que permanece en `page.tsx` (solo para etiquetas Ver/Cargar DP/PR; no afecta la completitud; correcto dejarlo).
3. Cambios en `parser-excel`/`parser-pdf` (no necesarios para esta corrección si la raíz era la detección de MIME).

### PROPONER SKILL

1. Consolidar como Skill la **variante «smoke de API sin navegador»** (Node contra endpoints reales con `.env.local`), ya decidida como estrategia en este Spec; evita repetir el procedimiento en cada plan.

## Pendientes técnicos y documentales

1. Evidencia de smoke ausente (O4/B4 y criterios de aceptación O1–O4 sin capturas).
2. Progreso homónimo ausente.
3. Briefs de tanda ausentes.
4. Flujo 14 nota 4 desactualizada (y la cita desde el flujo 12, línea 5).
5. Archivo de prueba `PPTO-prueba N°01.xlsx` modificado sin commitear en el repo de docs.
6. `build` no re-ejecutado por el auditor (pesado); reportado verde por los Workers, consistente con tsc + vitest.

## Recomendación

**`Requiere corrección`** (a nivel documental/verificación, no de código). El código de O1–O4 es correcto y mergeable; los comandos verificados están verdes (salvo errores de lint preexistentes en archivos ajenos). Para Gate 2 faltan: (1) la evidencia de smoke que cierra O4/R1, y (2) la resolución de la contradicción del flujo 14 (nota 4) y su alineación con el flujo 12.
