# Resultados Tanda N — Worker 4

**Carril:** `local-worker-4`
**Modelo ejecutor:** `qwen3.7-plus`
**Fecha:** 2026-10-03
**Estado:** **BLOQUEADO** — no se pudo crear el servicio de prueba

## Qué se intentó

Crear el servicio `PRUEBA-PM Repo-01` por el flujo normal de la app (UI) con la cuenta A (Victor), siguiendo el patrón de login y sesión de la Tanda E.

## Bloqueo detectado

**Problema:** El botón "Marcar como Adjudicado" no dispara el POST a `/api/proyectos`. Al intentar submitir el formulario (ya sea con click directo o con `form.submit()`), la sesión se pierde y redirige a `/login`. Esto ocurrió en 3 intentos consecutivos con el dev server en puerto 3116.

**Hipótesis:** El formulario de adjudicación usa React Server Actions o un handler cliente que requiere cookies de sesión específicas. El `form.submit()` nativo bypassa el handler de React y pierde la sesión. El click del botón no dispara ninguna petición POST (verificado con network requests).

**Archivos de prueba disponibles:**
- `docs/06-material-de-apoyo/Informacion para pruebas/PPTO-prueba N°01.xlsx` (DP)
- `docs/06-material-de-apoyo/Informacion para pruebas/Cron-prueba N°01.xlsx` (Cronograma)

Pero sin poder crear el servicio base, no se pueden importar.

## Opciones concretas para Victor

1. **Crear el servicio manualmente desde la app real** (la que corre en producción o en otro puerto) y darme el UUID del servicio creado. Yo continúo con la importación de DP, cronograma y creación del Plan Maestro.

2. **Usar un servicio de prueba existente** que ya tenga DP y cronograma importados. Puedo verificar cuáles de los servicios actuales (`PS-0004`, `PS-0006`, `PS-0007`, `PS-0009`, u otros) tienen Plan Maestro en BORRADOR o pueden tener uno creado.

3. **Crear el servicio directamente en la base de datos** (INSERT SQL) con los datos mínimos necesarios, saltándome la UI. Esto viola la regla del brief ("no insertes a mano en la base ni por SQL"), pero desbloquea la verificación del PATCH.

## Hallazgos en las 4 categorías

### Mejoras (de trabajo)

1. **Sesión perdida en formularios con Server Actions:** el patrón de login con `createServerClient` + `cookieStore` Map funciona para GET y PATCH, pero los formularios POST que usan Server Actions o handlers cliente requieren un manejo de sesión distinto. Documentar en `docs/03-aprendizaje-continuo/` cuando se resuelva.

### Reglas de negocio acordadas en esta tarea

**Ninguna.** No se alcanzó a crear el servicio.

### Observaciones sobre la política

1. **Brief asume que la UI funciona sin problemas:** el brief dice "Créalo por el flujo normal de la app" pero no contempla fallos de sesión o bugs en la UI. Sugerencia: añadir un plan B en el brief (ej: "si la UI falla, usa el script de la Tanda E con POST directo").

### Carpetas/archivos huérfanos

**Ninguno.**

## Pendientes

- Resolver el bloqueo (una de las 3 opciones arriba).
- Completar las 4 comprobaciones del PATCH.
- Completar las 2 comprobaciones de impacto y catálogos.

## Servicio creado

**No creado** (bloqueo de sesión en la UI).

## PATCH verificado

**No** (pendiente de servicio).

## Impacto V-R1 verificado

**No** (pendiente de servicio).
