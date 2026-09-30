# Plan paneles-servicio-persistente: lecciones de las tandas y medición

**Fecha:** 2026-09-30  
**Origen:** Worker F7-D (traslado del apartado «Mejoras (de trabajo)» del plan)  
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente.md` (medición completa en `docs/02-trabajo-activo/01-planes/2026-09-27-paneles-servicio-persistente-briefs/medicion.md`)

## Lo que funcionó

- **Tandas de unos 80 llamadas o menos, un Worker por sesión.** Un Planner en una sola sesión llegó a 193 llamadas, 685k de contexto y 82,0M de caché leída; el Orquestador anterior, a 220 llamadas y 71,0M. Las sesiones de Worker por tanda (F0-A a F7-C2) quedaron entre 9 y 68 llamadas, con contexto máximo de 177k y caché de 0,1M a 6,3M por sesión; ninguna superó las metas (≤ 80 llamadas, ≤ 200k, ≤ 12M). Fuente: `medicion.md`, tabla «Resultados por tanda», medida con `medir.py`.
- **Brief corto por tanda y «leer solo lo que el brief nombra»** (Grep por ID en vez de leer el plan de 221 KB).
- **Consulta en bloque a Victor antes de editar flujos** (tabla de contradicciones C1 a C36 y V1 a V7 con lo que decía cada flujo y lo que pasaría a decir): una sola aprobación cubrió a todos los Workers de F7 sin volver a preguntar.
- **La política «un cambio que choca con flujos se implementa en todos los afectados»** (Victor, 2026-09-28) se aplicó con la tabla «Trazabilidad por flujo»: cada documento con su destino y su estado.
- **Encadenar las navegaciones de Playwright una a una** sobre el mismo navegador; en paralelo se pisan.

## Lo que no funcionó, y qué hacer

1. **Login repetido A/B/A que sube llamadas.** Alternar cuentas (A, B, A) obliga a cerrar sesión y volver a entrar cada vez. Práctica: agrupar todo lo de la cuenta A y después todo lo de la B; o usar «Ver como» (`POST /api/ver-como`) para los 13 roles en una sola sesión.
2. **Los snapshots del navegador muestran credenciales autocompletadas.** Un snapshot de la pantalla de login puede incluir los valores rellenados por el navegador. Práctica: no tomar snapshot de la pantalla de login con el formulario relleno; comprobar la URL o un atributo. La comprobación PL-86 de F7-D encontró texto de cuentas de prueba en archivos de `.playwright-mcp/` (carpeta ignorada por git, no versionada); conviene borrar esa carpeta al cerrar una sesión de verificación (lo decide Victor).
3. **Un script vació el archivo del plan (F7-B).** Un reemplazo masivo dejó el plan sin contenido; se restauró desde `HEAD` y se reaplicaron 175 estados de la Punch List desde los handoffs. Práctica: nada de scripts de reemplazo masivo sobre el plan (`Grep` del ID + `Edit` de la fila), y commitear los estados antes de tocar el archivo con herramientas automáticas; si no hay commit, copiar el archivo antes.
4. **`redirect()` de servidor devuelve 200 con `NEXT_REDIRECT` en la respuesta al hacer `fetch`.** Una verificación por `fetch` que espere 307 da un falso resultado. Práctica: comprobar la redirección con el navegador (URL final) o leyendo el cuerpo de la respuesta, no solo el código de estado.
5. **«Ver como» aplica el alcance del usuario real.** Cambia los roles, no el alcance por OT (`proyecto_miembros`). Práctica: distinguir `No autorizado` (rol) de `No tienes esta OT a cargo` (alcance) al leer resultados.
6. **Falta de un servicio SVX de prueba.** Varias verificaciones de «con servicio» quedaron `Observado` porque no existe un servicio de prueba con datos. Práctica: preparar un servicio de prueba marcado antes de un plan que dependa de él, o registrar desde el brief qué queda `Observado` por esa razón.
7. **El clasificador de permisos bloqueó `browser_run_code_unsafe`** hasta que se añadieron reglas. Práctica: declarar al inicio del plan las herramientas de navegador que se van a usar y agregar sus reglas de permiso antes de lanzar las tandas de verificación.
8. **Escrituras en Recursos con datos reales.** Los ítems de Recursos pedían «crea/edita/desactiva sin error» y exigían escribir; se resolvió con registros de prueba marcados (`PRUEBA-PL…`, 12 quedaron con `activo=false`). Práctica: pedir la autorización de Victor para los registros de prueba en el brief, no a mitad de la tanda.

## Mejoras del plan y su destino

| Mejora registrada en el plan | Destino |
|---|---|
| El repositorio de la app sí es accesible desde una sesión local; `.worktrees/` sí existía; estado real de ramas y worktrees; `work-1`/`work-2` obsoletos | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (sección «Pool real de ramas y worktrees» actualizada en F7-D) |
| Autorización permanente para copiar `.env.local` a worktrees | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` y memoria del agente (ya vigente) |
| No abrir ni filtrar `cuentas-prueba.md` con `sed`/`grep`; el rol se lee del pie de la interfaz | Este archivo y `00-reglas-de-contexto.md` del plan |
| Comprobar la existencia de una carpeta con `ls`, no con la salida de `git` | Refuerza `2026-09-23-verificar-antes-de-afirmar.md` (si existe en la promoción) |
| Modo local con subagentes y excepción D6 (el Worker devuelve la pregunta al Orquestador) | Propuesta al Auditor para el estándar (`04-flujo-sdd-y-planes.md`, `02-roles-y-delegacion.md`) |
| Comparar (`cmp`/hash y nombres de variable, sin mostrar valores) antes de proponer borrar un `.env.local` | Este archivo |
| Un Worker de fase entera no cabe en una sesión | Este archivo (medición arriba) |
| Política «un cambio que choca con flujos se implementa en todos los afectados» | Ya en `02-arquitectura-y-fuentes-de-verdad.md` y `AGENTS.md`; aplicación en esta tarea: tabla «Trazabilidad por flujo» del progreso |

## Clasificación y destino propuesto

Aprendizaje de método (no una regla del sistema). Etiquetas: `sesiones/contexto`, `playwright`, `permisos`. Pendiente de promoción: el Auditor decide si las lecciones 3, 4 y 7 pasan a `01-contexto-repositorio/04-pruebas-y-evidencia.md`.
