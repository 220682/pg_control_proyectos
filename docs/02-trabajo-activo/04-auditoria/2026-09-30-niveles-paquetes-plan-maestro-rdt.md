# Informe de Auditoría — Niveles, Paquetes, Plan Maestro (lienzo) y RDT desde el Plan Maestro

> Plan auditado: `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`. Auditor de solo lectura; no se editó código, flujos ni documentos y no se hizo commit/merge/push.

## Alcance auditado

Los tres Specs aprobados (niveles de presupuesto y cronograma; paquetes y Plan Maestro grilla; RDT desde Plan Maestro), el plan por tandas con Orquestador/Planner/Workers (4 carriles)/Documentador/Auditor, la Punch List, los `resultados/*.md` (32 archivos), el progreso, la tabla en bloque de cambios a flujos, la matriz de propiedad, el registro de decisiones, el artefacto «Matriz de permisos» y el contraste texto final ↔ código de la rama `main` de la app.

## Material revisado

- Plan (`2026-09-30-niveles-paquetes-plan-maestro-rdt.md`), progreso y (ausencia de) evidencia homónimos.
- `…-briefs/00-indice-de-tandas.md`, `00-reglas-de-contexto.md`, `00-protocolo-migraciones.md`, `00-contratos-tecnicos.md`, `contrato-c*.md`, `f5-tanda-c.md`.
- Los 32 `resultados/*.md` (F0-A/B/R/S/T/U1/U2/V, F1-A/B/C, F2-A/B/C/D, F3-A/B/C/D/E, F4-A/B/C, F5-A/B/B2/D1/D2/D3/E/F/G). **No existe `resultados/F5-C.md`.**
- Flujos modificados (06, 08, 09, 10, 11, 14, 15, 16, 18, 19, 20, 21) por Grep/secciones.
- Código de `py_control_proyectos_web` en `main`: `src/lib/permisos/`, `src/app/api/plan-maestro/route.ts`, `src/app/api/paquetes-trabajo/route.ts`, `src/lib/proyectos/bloqueo-recarga.ts`, `src/lib/plan-maestro/**`, `src/lib/disciplinas/**`, `db/073–086`.
- `docs/03-aprendizaje-continuo/` (README + 5 archivos nuevos) y `04-flujos-de-negocio/14` y `20`.

## Verificación de rama

Comandos ejecutados y salida relevante (primer chequeo, no de memoria):

`py_control_proyectos_web`:
- `git rev-parse HEAD` → `c54cf0827589cff8477043a242ad40f3ea293750` = `git rev-parse origin/main` → mismo hash. `main` = `origin/main`.
- `git rev-list --left-right --count origin/main...local-worker-1|2|3|4` → `0 0`, `19 0`, `19 0`, `21 0`.
- `git log origin/main..main` → vacío (nada sin pushear).
- `git branch --contains <commit>` por tanda (todos presentes en su carril y en `main`, fruto del merge autorizado):
  - Carril 1 (`57984ff`, `2652116`, `ba81f64`) → `local-worker-1, main`.
  - Carril 2 (`72aace7`, `35bcf07`, `82cc863`, `9f631b6`, `70e12d5`) → `local-worker-2, main`.
  - Carril 3 (`73a8680`, `7038e5e`, `d4c5b3b`, `cfc180f`) → `local-worker-3, main`.
  - Carril 4 (`a037e98`, `14bae8d`, `7ba9814`) → `local-worker-4, main`.

`pg_control_proyectos`:
- `git status` → limpio, `main` = `origin/main` (`d6c14e5`). `git rev-list --left-right --count origin/main...main` → `0 0`.

Matiz del primer chequeo: el flujo estándar exige que la implementación esté en la rama del Worker, no en `main`. Aquí **Victor autorizó y ejecutó él mismo el merge a `main`**; consta en el Registro de decisiones del plan (fila `2026-10-01 … Victor hizo el merge y el push de la app a main (0250dab) y autorizó el resto del plan`). `main` avanzó de `0250dab` a `c54cf08` con las correcciones F5-E (`caab04f`), F5-F (`d165893`) y el revert F5-E (`c54cf08`), todas en `main` y pusheadas. Por tanto: **(a)** los commits por tanda están en la rama del carril correcto ✓, **(b)** `main` = `origin/main` en ambos repos ✓, **(c)** la autorización de Victor consta ✓. No bloqueo por «el código está en main».

## Cumplimiento de SDD, plan, Punch List y evidencia

- **Skills (paso 12):** `cerrar-tanda` consta usado en los 32 `resultados/*.md`. `verificar-permisos-por-rol`: usado en F3-B (`puedeCrearVersionPlanMaestro`) y en F5-A (estático, sin navegador, comparando esperado vs `permisos.ts`/pruebas); **F5-C pendiente** (es la tanda de navegador que debía usarlo en vivo). `seguir-flujo-de-planes`: lo usa el Orquestador (consta en progreso y en los resultados como «del Orquestador»); el «antes del cierre» queda pendiente porque el plan no está cerrado.
- **Matriz de propiedad:** sin evidencia de que dos carriles editaran el mismo archivo en la misma fase; cada carril commitea solo su carpeta/API/rango de migraciones. Única excepción autorizada y respetada: el carril 2 añade `puedeCrearVersionPlanMaestro` a `permisos.ts` (congelado). La integración (F5-A) resolvió sin conflictos, coherente con la matriz.
- **Tabla en bloque:** las 10 filas + el artefacto tienen «Aplicado ☑ (2026-10-01)». Cada cambio a flujos corresponde a una fila aprobada del Gate 1.
- **Punch List:** los ítems se verificaron en `resultados/*.md` con «Conforme/Observado»; la Punch List embebida del plan sigue mostrando «Sin verificar» (adaptación del plan: estados en `resultados/`, pendiente de consolidación final por el Orquestador).
- **Evidencia:** el archivo `03-evidencia/2026-09-30-niveles-paquetes-plan-maestro-rdt.md` **no existe**; la evidencia vive en `resultados/*.md` y en `capturas/niveles-paquetes-plan-maestro-rdt/` (F5B-*, F5B2-*). No bloquea, pero es una laguna documental.

## Verificación de la revisión de fuentes de verdad por fase

- **Traslado de hallazgos (segundo chequeo):** no queda ninguna fila en estado `Registrada` en los apartados del plan (los cuatro apartados del plan quedaron «Ninguna todavía»; los hallazgos se registraron en `resultados/*.md` y se consolidaron en el progreso). Las **mejoras de trabajo** se trasladaron a cinco archivos nuevos en `03-aprendizaje-continuo/` (con 5 filas en su `README.md`, estado «pendiente de revisión»): `editar-archivos-sin-heredocs-largos`, `pruebas-de-api-con-base-simulada`, `verificar-maquetas-y-lint-sin-infraestructura-nueva`, `clasificador-bloquea-scripts-de-migracion`, `artefacto-con-estado-guardado-aparte`. Las **reglas de negocio** están integradas en los flujos (ver abajo), no en archivos aparte. Los **huérfanos** están reportados en `F5-D3` (tablas `paquete_trabajo_partidas`/`_programacion`, `generarPropuestaDiaria`, `repartirAvanceDelPaquete`, `sumarMetradoPorPartida`, `SelectorPartidasDp`, `mockups/crear-rdts.html`, etc.) sin borrar nada.
- **Texto final = código (muestra contrastada en `main`):**
  - Permisos flujo 14: `puedeCrearVersionPlanMaestro` = administrador + jefe de proyectos (`permisos.ts:391`), usado solo en `POST` de `/api/plan-maestro` (`route.ts:201`); `puedeGestionarPlanMaestro` = administrador + jefe de proyectos + planner (`permisos.ts:377`), usado en `PATCH` para `GUARDAR_ASIGNACIONES`/`APROBAR` (`route.ts:395`, `490`). Coincide con la nota 9 y el punto 6 del flujo 14 y con la tabla del flujo 20: **crear versión nueva = 2 roles; aprobar el borrador de reemplazo = 3 roles** (tras el revert de F5-E). Sin brecha de código.
  - Reasignar paquete: `puedeValidarRdt` = administrador + jefe de proyectos + jefe de oficina técnica (`permisos.ts:317`), coherente con flujo 06 y 14 (nota 10).
  - Bloqueo de recarga: `evaluarRecarga`/`decidirRecarga` (`bloqueo-recarga.ts`) → 409 `bloqueadoPorPlanAprobado` con Plan Maestro APROBADO, y `confirmarPerdida` sin él (el borrador no bloquea). Coincide con flujos 09 y 15.
  - Disciplina obligatoria: `validarDisciplinaId` en `POST`/`PATCH` de paquetes (400 «Elige la disciplina del paquete»), y en el Plan Maestro la directa obligatoria al **aprobar** con herencia del paquete (`src/lib/plan-maestro/disciplina.ts`). Coincide con flujos 19 y 20.
  - Columnas del lienzo: `CAMPOS_FIJOS` (fijas: WBS, Descripción, Und., Met., Costo unitario, HH por unidad + «Falta repartir»; Disciplina opcional vía «Personalizar campos»). Coincide con flujos 18 y 20 (sin columnas de Tiempo).

## Clasificación de hallazgos

- `APLICAR AHORA`:
  1. Dejar constancia de que las migraciones **085 y 086** quedaron aplicadas: F5-B las observó en vivo (`/api/disciplinas` devuelve las 5; el gating de disciplina de las 47 directas funcionó), mientras `resultados/F2-D.md` y `F3-E.md` aún dicen «migración 085/086 sin aplicar» (las aplicó después el Orquestador con autorización de Victor). Corregir ese estado al consolidar.
  2. Consolidar la Punch List del plan y el progreso con los estados finales por ítem y por tanda (hoy dispersos en `resultados/*.md` y la Punch List del plan en «Sin verificar»).
- `PROPONER A RESPONSABLE`:
  1. Decidir **H5** (F5-B2): el aviso de recarga con borrador anuncia pérdidas (vínculos, paquetes, borrador) que **no se materializan**; o el aviso se hace exacto o la recarga borra lo que anuncia.
  2. Decidir si, con Plan Maestro aprobado, «Declarar» y «Crear paquete» en Paquetes deben **bloquearse** (hoy no bloquean; F5-B2 lo dejó como nota a confirmar).
  3. Selector «control directo / por paquetes / mixto» del flujo 19 (la app no lo tiene): retirar o dejar como diseño futuro.
  4. Flujo 18, «Paquetes atrasados» del Dashboard (los paquetes ya no tienen fechas): retirar o redefinir.
  5. Volver a marcar **«Aprobada»** en el artefacto «Matriz de permisos» (`matriz/actual` v47 quedó con «Aprobada» = false).
- `NO PROMOVER`:
  1. Etiquetas «migración 085/086 sin aplicar» en `F2-D.md`/`F3-E.md` (desactualizadas respecto del estado real; no es un fallo funcional).
  2. Falta el archivo de evidencia markdown del plan (la evidencia está en `resultados/` y `capturas/`); laguna documental, no bloqueante.
  3. `matriz/actual` no es un archivo del repo (vive en la base del artefacto Claude); el chequeo por Glob no aplica y el estado se verifica solo por lo que documentan F5-D2/F5-G.
- `PROPONER SKILL`:
  1. Variante **«sin navegador»** del Skill `verificar-permisos-por-rol` (comparación estática esperado vs `permisos.ts` + pruebas de los 13 roles), usada en F3-B y F5-A, como complemento a la verificación en vivo con «Ver como».
  2. Procedimiento de migración idempotente con `check`/`apply`, candado, lectura de credenciales sin imprimirlas y reversión si los conteos cambian (repetido en 7+ tandas; hoy en `00-protocolo-migraciones.md`, candidato a Skill agnóstico).

## Pendientes técnicos y documentales

1. **F5-C (técnico, bloqueante):** no hecha; no existe `resultados/F5-C.md`. Requiere navegador/Playwright, login real y «Ver como». Ítems F5C-1 a F5C-5: RDT desde el Plan Maestro (real por paquete × partida en lienzo y PR suma por partida); permisos de los 13 roles por rol (incluida versión nueva); móvil 390 px y estados vacío/carga/error; regresión en PS-0004/PS-0005; limpieza de datos de prueba.
2. **Limpieza de datos de prueba** PS-0006 y PS-0007 (F5-C-5) solo con autorización expresa de Victor.
3. Victor: marcar «Aprobada» en la matriz; resolver H5 y las decisiones 2–4 de «PROPONER A RESPONSABLE».
4. Orquestador: `seguir-flujo-de-planes` antes del cierre, consolidar Punch List/progreso y pasos 16–18 (merge/push autorizado ya hecho; falta el mensaje de cierre).
5. Documental menor: crear el archivo de evidencia o declarar explícitamente que la evidencia vive en `resultados/` + `capturas/`.

## Recomendación

`Requiere corrección`.

Razones: F5-C pendiente (verificación en vivo de RDT, permisos por rol, móvil y regresión, más la limpieza de datos de prueba) sin la cual no hay verificación en vivo completa; decisiones abiertas de Victor (H5, bloqueo de Declarar/Crear con plan aprobado, selector del flujo 19, «Paquetes atrasados» del 18) y la marca «Aprobada» del artefacto aún no repuesta.
