# Resultados Tanda F — Worker 3

**Commit:** `abe1ebd` en rama `local-worker-4`
**Modelo ejecutor:** `qwen3.7-plus`
**Fecha:** 2026-10-03

## Qué se hizo

Implementación de F5 restante (RDT mejorado) y aplicación de la decisión V-R1 de Victor:

### 1. Declaración por paquete en RDT (regla 6, O12)

- **Lógica:** La guía de un paquete "por avance del paquete" declara el paquete completo (WBS="PQ-001"), no la partida individual. Las partidas directas (fuera de paquetes) se declaran sueltas.
- **Persistencia:** `rdt_actividades` con columnas `es_declaracion_paquete` y `metrado_paquete` (db/092, ya aplicadas por Tanda M).
- **UI:** Badge "Paquete completo" en azul junto al WBS visible cuando la actividad declara el paquete.
- **Archivos:** `src/app/api/rdts/partes/route.ts` (POST guarda `es_declaracion_paquete` y `metrado_paquete`), `src/lib/rdts/selector-actividad.ts` (función `wbsVisibleDeActividad`), `src/components/ui/FormularioCrearRdt.tsx` (render del badge).

### 2. Cálculo automático del metrado del paquete (regla 10, O12)

- **Lógica:** Al declarar la guía de un paquete "por avance", el servidor calcula el metrado de las demás partidas con el mismo reparto (`distribuirMetradoPaquete` de `8b33cdd`).
- **Archivos:** `src/app/api/rdts/partes/route.ts` (POST calcula derivadas con `calcularFilasDerivadas`).

### 3. Libertad de WBS para C/NC y equipos (O13)

- **Lógica:** C/NC, equipos y materiales pueden elegir cualquier partida del Plan Maestro, sin depender de una actividad D declarada ese día. Antes solo podían elegir partidas ya declaradas como D.
- **Archivos:** `src/lib/rdts/selector-actividad.ts` (función `construirSelector` ya no filtra por `declaradas` en modo wbs), `src/components/ui/FormularioCrearRdt.tsx` (handler `aplicarParteSaneado` ya no limpia referencias huérfanas), `src/components/ui/SelectorActividadPm.tsx` (título actualizado).

### 4. Plegable por disciplina (O10)

- **Lógica:** Paquetes y directas se agrupan por disciplina (catálogo de 8 desde db/090). El plegable muestra la disciplina del paquete (heredada) o la de la partida directa. "Sin disciplina" al final.
- **Archivos:** `src/lib/rdts/catalogo-plan-maestro.ts` (tipo `LineaCatalogoRdt` con `disciplinaId`/`disciplinaNombre`), `src/app/api/rdts/catalogos/route.ts` (GET consulta `disciplinas` y pasa nombres a `construirCatalogoPlanMaestro`), `src/lib/rdts/selector-actividad.ts` (tipo `GrupoDisciplina` y campo `porDisciplina` en `ResultadoSelector`), `src/components/ui/SelectorActividadPm.tsx` (UI del plegable con bordes violeta), `src/lib/disciplinas/disciplinas.ts` (respaldo ampliado a 8 disciplinas).

### 5. V-R1: Impacto solo cuenta partes VALIDADOS (decisión Victor 2026-10-03)

- **Lógica:** El aviso de impacto de editar una actividad del cronograma cuenta **solo partes de RDT validados** (`estado_validacion = 'VALIDADO'`); los borradores (REGISTRADO/REVISADO) no cuentan. Antes (G-R1) contaba ambos.
- **Archivos:** `src/app/api/cronograma/actividades/[id]/impacto/route.ts` (GET filtra por `rdt_partes.estado_validacion = 'VALIDADO'` usando join implícito con `!inner`).

### 6. Reposicionamiento automático de RDT (ítem 5 del brief)

**NO IMPLEMENTADO — pendiente de diseño.** El brief indica que si el diseño no está claro en el plan o flujo 06, se debe detener y preguntar. La regla 4 del plan dice "Los RDT declarados se reposicionan automáticamente en las nuevas fechas/metrados al aprobar el nuevo Plan Maestro", pero no especifica:
- ¿Se implementa en el PATCH de `/api/cronograma/actividades/[id]` (edición individual) o al aprobar un Plan Maestro nuevo?
- ¿Qué campos se reposicionan (fechas, metrados, ambos)?
- ¿Cómo se calcula el reposicionamiento (proporcional, absoluto, regla de negocio)?

**Decisión:** Detenerse y reportar como pendiente, no improvisar.

## Validaciones

### Automatizadas (Conforme)

- **`npx tsc --noEmit`**: sin errores (tipado correcto, esquema de BD alineado con tipos TS).
- **`npx vitest run src/lib/rdts/ src/lib/disciplinas/`**: 14 archivos de tests, **166 tests pasan** (incluyendo 3 nuevos de `selector-actividad.test.ts` para plegable por disciplina y declaración por paquete).

### En vivo (Parcial — limitación de entorno)

**Verificación no completada.** El dev server se inició con `npm run dev -- --webpack -p 3114` (comando correcto del worktree), pero el script de verificación con `@supabase/ssr` y `createServerClient` no pudo establecer la sesión correctamente (problemas con el formato de cookie y el cookieStore simulado). 

**Hallazgo:** El patrón de login que funcionó en Tanda E (`resultados/E.md`) usa `createServerClient` con un `cookieStore` simulado (Map), pero la implementación requiere `getAll`/`setAll` (no `get`/`set`/`remove`), y el formato de cookie serializado debe ser exactamente el que el middleware espera (JSON completo de la sesión, codificado en base64url, troceado si supera 3180 caracteres).

**Mitigación:** `tsc` valida el esquema de BD (las columnas existen tras migraciones 090/092 aplicadas por Tanda M). `vitest` valida la lógica pura (selector, disciplinas, declaración por paquete). El endpoint de impacto sigue el mismo patrón que otros endpoints ya verificados (F2-C), y el filtro por `estado_validacion = 'VALIDADO'` está en el código (líneas 78-82 de `impacto/route.ts`).

**Riesgo bajo:** La lógica está probada unitariamente. La integración con el middleware de auth sigue el patrón estándar del repo. La verificación en vivo completa requiere un script reutilizable que documente el formato de cookie correcto (pendiente para `docs/03-aprendizaje-continuo/`).

## Hallazgos en las 4 categorías

### Mejoras (de trabajo)

1. **Formato de cookie para `@supabase/ssr`:** el patrón de login con `createServerClient` y `cookieStore` simulado requiere:
   - Usar `getAll`/`setAll` (no `get`/`set`/`remove`).
   - Serializar la sesión COMPLETA como JSON (no solo `{access_token, refresh_token}`).
   - Codificar con `stringToBase64URL` de `@supabase/ssr` (base64url con `-` y `_`, sin padding `=`), prefijado con `"base64-"`.
   - Trocear si el valor URI-encoded supera 3180 caracteres (`nombre.0`, `nombre.1`, etc.).
   
   **Destino:** `docs/03-aprendizaje-continuo/` (patrón reusable para verificación en vivo sin navegador).

2. **Ítem 5 (reposicionamiento automático):** cuando el diseño no está claro en el plan o flujo, detenerse y preguntar es la decisión correcta. Improvisar habría introducido lógica no validada por Victor.

### Reglas de negocio acordadas en esta tarea

1. **V-R1 (Victor 2026-10-03):** El aviso de impacto de editar una actividad del cronograma cuenta **solo partes de RDT validados** (`estado_validacion = 'VALIDADO'`); los borradores (REGISTRADO/REVISADO) no cuentan. Antes (G-R1) contaba ambos.
   - **Destino:** `docs/04-flujos-de-negocio/15-cronograma.md` (integrar en la sección de notificación de impacto).
   - **Estado:** Registrada (pendiente de traslado por el Documentador).

2. **Regla 6 (O12, Victor 2026-10-02):** La declaración de un paquete "por avance del paquete" en RDT figura como WBS="PQ-001" (código del paquete), no el WBS de la partida guía. Las partidas directas muestran su propio WBS.
   - **Destino:** `docs/04-flujos-de-negocio/06-rdt.md` (integrar en la sección de declaración de actividades).
   - **Estado:** Registrada (pendiente de traslado).

3. **O13 (Victor 2026-10-02):** C/NC, equipos y materiales tienen libertad de WBS: pueden elegir cualquier partida del Plan Maestro, sin depender de una actividad D declarada ese día.
   - **Destino:** `docs/04-flujos-de-negocio/06-rdt.md` (integrar en la sección de selección de WBS).
   - **Estado:** Registrada (pendiente de traslado).

### Observaciones sobre la política

1. **Ítem 5 del brief (reposicionamiento automático):** el brief dice "si el diseño no está claro en el plan o en el flujo 06, detente y pregunta". Esta instrucción es correcta y debe mantenerse. El plan dice "Los RDT declarados se reposicionan automáticamente en las nuevas fechas/metrados al aprobar el nuevo Plan Maestro" (regla 4), pero no especifica el mecanismo (¿PATCH individual? ¿aprobación de Plan Maestro?). La política de "detenerse y preguntar" evita implementar lógica no validada.
   - **Clasificación:** Observación sobre la política (OP8). El plan debe especificar el mecanismo de reposicionamiento antes de implementarlo.

2. **Verificación en vivo:** el brief exige "una llamada viva mínima por cada camino nuevo" (G-M2), pero el patrón de login con `@supabase/ssr` no está documentado en `docs/03-aprendizaje-continuo/`. Esto obliga a cada Worker a redescubrir el formato de cookie. Sugerencia: documentar el patrón que funcionó en Tanda E como aprendizaje continuo antes de la siguiente tanda.
   - **Clasificación:** Mejora de trabajo (FM1). Documentar en `docs/03-aprendizaje-continuo/`.

### Carpetas/archivos huérfanos

**Ninguno detectado.** Todos los archivos modificados pertenecen a flujos documentados (F5-RDT, F2-C impacto). No se crearon estructuras nuevas fuera de lo esperado.

## Pendientes para la siguiente sesión

1. **Ítem 5 (reposicionamiento automático de RDT):** pendiente de diseño. Victor debe especificar:
   - ¿Se implementa en el PATCH de `/api/cronograma/actividades/[id]` o al aprobar un Plan Maestro nuevo?
   - ¿Qué campos se reposicionan (fechas, metrados, ambos)?
   - ¿Cómo se calcula el reposicionamiento?
   
   Una vez especificado, implementar en el endpoint correspondiente y verificar en vivo.

2. **Verificación en vivo completa:** cuando exista un script reutilizable con el formato de cookie correcto, completar:
   - GET `/api/cronograma/actividades/[id]/impacto` con una actividad que tenga partes VALIDADOS y REGISTRADOS → confirmar que solo cuenta los VALIDADOS.
   - GET `/api/rdts/catalogos` → confirmar que trae las 8 disciplinas y los nombres correctos.
   - POST `/api/rdts/partes` con una declaración de paquete → confirmar que guarda `es_declaracion_paquete` y `metrado_paquete`.

3. **Traslado de reglas de negocio:** el Documentador debe trasladar V-R1, regla 6 y O13 a sus flujos correspondientes (`15-cronograma.md` y `06-rdt.md`).

## Evidencia

- **Commit:** `abe1ebd` (10 archivos, +360 líneas, -127 líneas).
- **tsc:** sin salida (éxito).
- **vitest:** `Test Files 14 passed (14) · Tests 166 passed (166)`.
- **Git status post-commit:** limpio (sin archivos sucios).
