# 2026-10-02 — Spec: observaciones de Victor navegando la app (lote inicial)

> Spec del **Orquestador** con el Responsable humano (plantilla `01-spec-sdd.md`). Es un **registro vivo de observaciones**: cada vez que Victor detecta algo navegando la app, se anota aquí como fila nueva. Las filas se atacan por **lotes**; el Plan (`Gate 1`) organiza cada lote en fases y Punch List. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`.

## Estado

`Aprobado (Gate Spec)` — Lote 1 (O1–O4), cerrado.

Puertas:
- Gate Spec (Lote 1): `aprobado por Victor (2026-10-02)`
- Gate 1 (Lote 1): `aprobado por Victor (2026-10-02)` — ver [`2026-10-02-observaciones-victor-plan.md`](2026-10-02-observaciones-victor-plan.md)
- Gate 2 (Lote 1): `aprobado por Victor (2026-10-02)` — merge `ce5623e`, ver el plan
- **Lote 2 (O5, O6, O7):** `registrado 2026-10-02` — Gate Spec **pendiente** (grupos de O5 decididos por Victor; queda la nota OT / Recursos del servicio / 3WLA)

## Registro de observaciones de Victor

| ID | Fecha | Qué vio Victor (en sus palabras) | Hallazgo verificado (código) + resolución | Estado | Lote |
|---|---|---|---|---|---|
| O1 | 2026-10-02 | "El desplegable de responsable existe pero solo lista a uno de los dos usuarios; debe incluir a todos, también al administrador, en orden de roles." | En `Editar checklist`, el `SelectorUsuario` de los ítems de catálogo se pasa con `filtrarPorRolClave={item.rolResponsableClave}`: solo lista usuarios con el rol responsable de ese documento. Por eso ve 1 de 2 y el administrador no aparece. | `Registrada` | 1 |
| O2 | 2026-10-02 | "Encontré un rol con iniciales PR; hay que eliminarlo si no existe o cambiarlo por JF, indicando rol para jefatura." | **No es rol, es el área** código `PR` = "Proyecto" (tabla `areas`, `db/014`). **Resolución:** renombrarla a **`JF` = "Jefatura"**, como área para asignar a los jefes. | `Registrada` | 1 |
| O3 | 2026-10-02 | "Reordenar el checklist con esta lista definitiva; los no mencionados de AL_INICIO se eliminan; **todos los ítems llevan casilla y todos llevan responsable**; completar se marca por check." | Ver sección «Catálogo definitivo del checklist». | `Registrada` | 1 |
| O4 | 2026-10-02 | "El importador de cronograma falla (salió error después de intentar leer el archivo, Excel o PDF); antes mostraba qué tipo de error era y ahora solo dice 'error'. Quiero que se **documente/loguee el error** (por si vuelve a fallar) **y se arregle**." | Triple alcance: (a) regresión en la superficie del error (`FormularioCronograma.tsx` → `traducirErrorApi` / `respuestaErrorInesperado` de `api/cronograma/route.ts`); (b) **loguear el error en servidor** con detalle (mensaje, archivo, formato) para trazabilidad futura; (c) corregir el error subyacente de lectura/parseo (Excel y PDF). Causa raíz a diagnosticar al iniciar el Plan (ver riesgo R1). | `Registrada` | 1 |
| O5 | 2026-10-02 | "En checklist debemos diferenciar qué acción requiere cada documento: al igual que DP y PR (Crear DP, Ver DP, Crear PR, Ver PR) o como presupuesto («Seleccionar archivo»). No podemos poner «Seleccionar archivo» al paquete de trabajo, cuando el paquete se crea en la interfaz, y lo mismo sucede con otros documentos. Revisar e indicar cómo se arregla, mostrando las listas de los grupos a los que pertenecerá." | Ver sección «Grupos de acción del checklist (O5)». Verificado en `page.tsx` (proyecto): hoy solo `tipo_captura = 'ESTRUCTURADO'` (claves `dp`/`pr`) muestra enlace con etiqueta propia; **el resto — incluidos `cronograma`, `paquete_trabajo`, `plan_maestro` y `requerimiento`— muestra el input de archivo («Seleccionar archivo»)**, aunque esos documentos se crean/importan en pantallas propias de la app. | `Registrada` | 2 |
| O6 | 2026-10-02 | "El cronograma sigue mostrando el mensaje solo de 'ERROR', no indica el motivo de la falla, y no llega a importar el cronograma ni en formato Excel ni en PDF como base." | **Reabre O4.** Victor probó en la **app desplegada** y confirmó que Vercel **se despliega sola con cada push a main**: la prueba corre sobre el código vigente (`ce5623e`), no sobre una versión anterior. Verificado en el repo: ese commit incluye `9ad0640`, que solo añadió detección de formato por extensión, `console.error` en servidor y devolución del mensaje; **los parsers no cambiaron y el éxito end-to-end nunca se verificó** — el informe del Auditor lo dejó como APLICAR AHORA («Confirmar O4 con smoke real») y sigue sin evidencia (no existen `02-progreso/` ni `03-evidencia/` de ese plan). Mecanismo verificado que oculta el motivo en pantalla: `src/lib/errores/traducir-error.ts` devuelve el fallback genérico cuando el mensaje empieza con `identificador:` (p. ej. `Error: …`), y en `FormularioCronograma.tsx` el `?? 'No se pudo leer el cronograma'` nunca llega a aplicarse. Causa raíz del fallo de lectura (Excel y PDF): a diagnosticar reproduciendo con los archivos de prueba. | `Registrada` | 2 |
| O7 | 2026-10-02 | "Vi en la web que «Acta de conformidad» figuraba en la lista; esta no va." | El ítem existe en `catalogo_documentos` (fase CIERRE) y sus filas aparecen en la lista del checklist del proyecto (`page.tsx` lista todos los `proyecto_documentos`). **Contradice la decisión D5 del Lote 1** («el Acta de conformidad se mantiene»): Victor decide ahora que **no va** en la lista. Lote 2: quitarla de la lista del checklist y actualizar la regla en `04-flujos-de-negocio/12-checklist.md` y en todo documento que la cite como parte del checklist. El mecanismo (ocultar vs. eliminar con migración que preserve las filas existentes) lo define el Planner. | `Registrada` | 2 |

Estados: `Registrada` → `Trasladada` · `Descartada` · `Pendiente de decisión`.

## Catálogo definitivo del checklist (O3)

Orden y nombres exactos pedidos por Victor. **Los ítems de AL_INICIO no listados se eliminan** (D5: el "Acta de conformidad" de CIERRE se mantiene — **esta decisión fue derogada por O7**: Victor decide que no va en la lista; ver fila O7 y «Resultado esperado (Lote 2)»).

| # | Nombre definitivo | Clave (actual o nueva) | Completar | Responsable |
|---|---|---|---|---|
| 1 | Orden de trabajo (OT) | `ot` (existe) | Check | Sí |
| 2 | Alcance | `alcance` (existe) | Check | Sí |
| 3 | Presupuesto | `presupuesto_proyecto` (existe) | Check | Sí |
| 4 | Cronograma | `cronograma` (**nuevo**) | Check | Sí |
| 5 | Recursos del servicio | `recursos_sin_costo` → **renombrar** | Check | Sí |
| 6 | DP (Datos del proyecto) | `dp` (existe) | Check | Sí |
| 7 | Paquetes de trabajo | `paquete_trabajo` (**nuevo**) | Check | Sí |
| 8 | Plan maestro | `plan_maestro` (**nuevo**) | Check | Sí |
| 9 | PR (Reporte del proyecto) | `pr` (existe) | Check | Sí |
| 10 | 3WLA | `3wla` (existe) | Check | Sí |
| 11 | Requerimientos del servicio | `requerimiento` (existe) | Check | Sí |
| 12 | Listado de personal nuevo | `personal_requerido` → **renombrar** ("Lista"→"Listado") | Check | Sí |
| 13 | Listado de pets | `pets` → **renombrar** (hoy "Elaboración de PETS") | Check | Sí |

- **Eliminar (AL_INICIO):** `materiales_con_costo` ("Materiales con costo") y cualquier otro ítem de AL_INICIO no listado.
- **Todos los ítems son marcables (casilla de check) y todos llevan responsable.** Sin excepción por "generado por el sistema": la fuente de datos (manual vs. módulo) es informativa para el futuro (p. ej. "Recursos del servicio" se generará desde el DP), no cambia que hoy se completan marcando la casilla.
- **Completar = marca por check** (manual) para todos los ítems, incluidos DP y PR (cambio respecto al auto-completado actual por `proyectoTieneDp`).
- **Chips renombrados (tenerlo en cuenta):** "Listado de personal nuevo" y "Listado de pets". El ítem de navegación "Personal NUEVO" (`src/lib/config/registro-accesos.ts`) se alinea a "Listado de personal nuevo".

## Grupos de acción del checklist (O5)

**Decidido por Victor (2026-10-02): dos grupos.** Cada ítem del catálogo queda en un grupo de acción, y la fila del checklist muestra la acción de su grupo (hoy muestra «Seleccionar archivo» en todos salvo DP/PR):

| # | Ítem | Grupo | Acción que mostraría |
|---|---|---|---|
| 1 | Orden de trabajo (OT) | B — Pantalla propia | Crear / Ver (ver nota pendiente abajo) |
| 2 | Alcance | A — Archivo | Seleccionar archivo |
| 3 | Presupuesto | A — Archivo | Seleccionar archivo |
| 4 | Cronograma | B — Pantalla propia | Crear / Ver → `/cronograma` |
| 5 | Recursos del servicio | B — Pantalla propia | Crear / Ver (ver nota pendiente abajo) |
| 6 | DP (Datos del proyecto) | B — Pantalla propia | Crear DP / Ver DP (ya existe) |
| 7 | Paquetes de trabajo | B — Pantalla propia | Crear / Ver → `/paquetes-trabajo` |
| 8 | Plan maestro | B — Pantalla propia | Crear / Ver → `/plan-maestro?proyectoId=` |
| 9 | PR (Reporte del proyecto) | B — Pantalla propia | Crear / Ver PR (ya existe) |
| 10 | 3WLA | B — Pantalla propia | Crear / Ver (ver nota pendiente abajo) |
| 11 | Requerimientos del servicio | B — Pantalla propia | Crear / Ver → `/requerimientos?proyectoId=` |
| 12 | Listado de personal nuevo | A — Archivo | Seleccionar archivo |
| 13 | Listado de pets | A — Archivo | Seleccionar archivo |

- **Grupo A (Archivo) — 4 ítems:** 2 Alcance, 3 Presupuesto, 12 Listado de personal nuevo, 13 Listado de pets. Se sube el documento como hasta ahora.
- **Grupo B (Pantalla propia) — 9 ítems:** 1, 4, 5, 6, 7, 8, 9, 10, 11. Mismas acciones **Crear / Ver** para todos, en la pantalla de su módulo; la fila del checklist **no** ofrece subir archivo, solo el enlace. DP y PR conservan sus etiquetas actuales.

**Pendiente de decisión de Victor (no bloquea el resto):** 1 OT, 5 Recursos del servicio y 10 3WLA están en Pantalla propia pero **hoy no tienen pantalla** (chips inertes en `registro-accesos.ts`; el 3WLA ni está construido y "Recursos del servicio" se generará desde el DP — ver «No alcance»). Definir si hasta que exista su pantalla se quedan con «Seleccionar archivo» o si el Lote 2 incluye crearlas.

**Cómo se arregla (dirección, lo concreta el Planner en el plan):** `page.tsx` hoy solo decide entre enlace (ESTRUCTURADO, solo DP/PR) e input de archivo para todo lo demás. Hace falta que cada ítem del catálogo declare su grupo: (i) columna nueva en `catalogo_documentos` (grupo + ruta/etiquetas) vía migración — recomendada: es la fuente de verdad y mover un ítem de grupo no toca código — o (ii) mapa por `clave` en el código. Cualquier opción debe conservar la casilla de check y el responsable de todos los ítems (O3/D2) y respetar permisos por pantalla (flujo 14).


## Problema y contexto

Victor navega la app y detecta defectos puntuales. Este Spec los registra y define el **lote inicial (Lote 1)** para atacar ya; el resto queda anotado para lotes futuros.

## Resultado esperado (Lote 1)

- **O1:** En `Editar checklist`, los desplegables de responsable listan **todos los usuarios** (incluido el administrador), **ordenados por rol**, sin filtro por el rol del documento.
- **O2:** El área `PR` ("Proyecto") pasa a llamarse **`JF` ("Jefatura")**.
- **O3:** El checklist queda con el **catálogo definitivo** de arriba: orden exacto, tres ítems nuevos, tres renombres y eliminación de los AL_INICIO no mencionados; **todos marcables y todos con responsable**; completar se marca por check.
- **O4:** Se **corrige el error subyacente** de lectura/parseo de la importación de cronograma; el error queda **logueado en servidor** con su detalle (mensaje, archivo, formato) para trazabilidad futura; y la pantalla vuelve a mostrar el **mensaje de error específico** (el motivo), no uno genérico.

## Resultado esperado (Lote 2)

- **O5:** cada fila del checklist muestra la acción de su grupo (sección «Grupos de acción del checklist»): «Seleccionar archivo» solo en los 4 ítems del Grupo A; enlace **Crear / Ver** a la pantalla del módulo en los 9 del Grupo B, con sus etiquetas. Queda pendiente de decisión de Victor la nota de OT / Recursos del servicio / 3WLA (sin pantalla hoy).
- **O6:** la importación de cronograma **funciona de punta a punta** con los archivos de prueba (plantilla Excel y PDF de MS Project); cuando falla, la pantalla muestra el motivo específico (sin mensaje genérico) y el error queda logueado en servidor con formato, nombre de archivo y mensaje. Se cierra solo con evidencia de smoke — lo que faltó en el Lote 1.
- **O7:** «Acta de conformidad» ya **no figura** en la lista del checklist del proyecto, y la regla del flujo 12 queda actualizada (deroga la decisión D5).

## Alcance

- Lote 1: O1, O2, O3 y O4 (cerrado).
- Lote 2: O5, O6 y O7 (Gate Spec pendiente).

## No alcance

- Generación automática de "Recursos del servicio" desde los datos del DP (plan futuro).
- Fusión de chips (solo se renombran).
- Cualquier observación futura que Victor agregue después de aprobar esta Spec: se registra como fila nueva y se agenda en un lote posterior.
- ~~El "Acta de conformidad" (CIERRE) no se modifica~~ — **derogado por O7** (Lote 2: quitarla de la lista del checklist).

## Usuarios / roles afectados

- Administrador y Jefe de Proyectos (editan el checklist: `puedeModificarChecklist`).
- Jefe de Proyectos, Administrador y Planner (suben cronograma: `puedeSubirCronograma`).
- Cualquier usuario con rol conocido (ve el checklist).
- Los jefes ganan un área asignable "Jefatura" (O2).

## Reglas de negocio y documentos afectados

- `docs/04-flujos-de-negocio/12-checklist.md` (catálogo, orden, asignación de responsable, completar por check).
- `docs/04-flujos-de-negocio/15-cronograma.md` (importación y mensaje de error) — si el traslado documental lo exige.
- `docs/04-flujos-de-negocio/02-usuarios.md` (área "Jefatura" / JF).
- `docs/01-contexto-repositorio/08-arquitectura-funcional-y-datos.md` — si cambia el catálogo o las áreas.

## Datos, API, migraciones o dependencias

- Migración nueva (catálogo del checklist): insertar `cronograma`, `paquete_trabajo`, `plan_maestro`; renombrar `recursos_sin_costo` → "Recursos del servicio", `personal_requerido` → "Listado de personal nuevo", `pets` → "Listado de pets"; eliminar los AL_INICIO no listados (incl. `materiales_con_costo`); fijar el `orden` 1–13. Idempotente, patrón `db/006`/`db/009`.
- Migración nueva (áreas, O2): renombrar `areas` `PR`/`Proyecto` → `JF`/`Jefatura`, conservando `perfiles.area_id`.
- `src/components/ui/SelectorUsuario.tsx` (quitar filtro por rol / ordenar por rol).
- `src/app/(workspace)/proyectos/[id]/checklist/editar/editor-checklist.tsx` (todos con responsable y check).
- `src/lib/usuarios/lista-usuarios.ts` (orden por rol).
- `src/lib/config/registro-accesos.ts` ("Personal NUEVO" → "Listado de personal nuevo").
- `src/lib/checklist/checklist.ts` (`documentoCompleto`: completar por check manual para todos, incluidos DP/PR).
- `src/app/api/cronograma/route.ts` + `src/components/ui/FormularioCronograma.tsx` + `src/lib/errores/traducir-error.ts` (O4): logging de error en servidor (patrón `console.error` con contexto) + restaurar mensaje específico + corregir el parseo.

## Diseño / UI aplicable

- Desplegables de responsable: misma componente, sin filtro por rol, con orden por rol.
- Catálogo del checklist: orden nuevo, nombres nuevos, ítems nuevos, todos con casilla y responsable.
- Importación de cronograma: corregir el error y restaurar el texto específico del error.

## Riesgos y decisiones

Decisiones ya resueltas por Victor (no quedan pendientes):
- **D5:** la eliminación aplica solo a AL_INICIO; "Acta de conformidad" (CIERRE) se mantiene.
- **D2:** completar se marca por check (manual) para todos los ítems.
- **D6:** todos los ítems llevan responsable; se descarta la distinción "sistema = sin responsable".

Riesgos de implementación a vigilar en el Plan:
- **R1 (O4):** la causa raíz del error de importación no está identificada aún. Primer paso del Plan: restaurar el mensaje específico y reproducir con un archivo de prueba (Excel plantilla y PDF de MS Project) para ver el error real y corregirlo.
- **R2 (O3):** cambiar DP/PR de auto-completado (`proyectoTieneDp`) a check manual afecta el indicador "checklist completo" del proyecto y la pantalla del proyecto; revisar todos los consumidores de `checklistCompleto`/`documentosPendientes`.
- **R3 (O3):** la migración del catálogo debe preservar los `proyecto_documentos` existentes (no dejar huérfanos al eliminar `materiales_con_costo`).

## Criterios de aceptación

- **O1:** en Editar checklist, todo ítem muestra un desplegable con **todos** los usuarios (incluido el administrador) ordenados por rol.
- **O2:** el selector "Área" de crear/editar usuario muestra "JF — Jefatura" en lugar de "PR — Proyecto".
- **O3:** el checklist muestra, en el orden exacto de la tabla, los 13 ítems con esos nombres; no queda "Materiales con costo"; **todos** tienen casilla y responsable; completar se marca por check. "Acta de conformidad" (CIERRE) sigue igual.
- **O4:** al importar un cronograma (PDF o Excel) el error de lectura/parseo queda corregido (la importación funciona); cuando sí falla, la pantalla muestra el motivo específico y el error queda registrado en el log del servidor con su detalle.

## Estrategia de prueba / evidencia

- `npm test`, `npx tsc --noEmit`, `npm run lint`, `npm run build` (repositorio `py_control_proyectos_web`).
- **Tooling de verificación (decisión del Orquestador):** pruebas unitarias (vitest) para la lógica pura + **script de smoke de API** (Node, golpea los endpoints reales con `.env.local`, sin navegador) + **navegación manual de Victor** para la confirmación visual. Playwright solo opcional si una pantalla concreta lo exigiera (se evita por su inestabilidad).
- Smoke de API: checklist (GET/PATCH) con orden/nombres/responsables; importación de cronograma con archivos de prueba (`docs/06-material-de-apoyo/Informacion para pruebas/CRON-PROMCOSER-AESA-001.pdf` y `Cron-prueba N°01.xlsx`) cubriendo éxito y fallo con mensaje específico; área "JF — Jefatura".
- Evidencia en `docs/02-trabajo-activo/03-evidencia/` con capturas y salidas del smoke.

## Aprobación (Gate Spec)

- [x] El Responsable humano aprueba este Spec.
