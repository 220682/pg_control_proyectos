# Evidencia — Estado del servicio (2026-10-24)

Verificaciones corridas en `py_control_proyectos_web` (sin commit todavía):

| Verificación | Resultado |
|---|---|
| `npx tsc --noEmit` | Sin errores |
| `npx vitest run` (completo) | 208 archivos pasan, 1 omitido; 2306 pruebas pasan, 1 omitida |
| `npx vitest run src/lib/estado-servicio` | 37 pruebas de piezas puras (huella, horarios, reglas, lectura del mensaje, cifrado, validación de la respuesta de IA) pasan |
| `npx eslint` sobre los archivos nuevos (`src/lib/estado-servicio`, `src/components/estado-servicio`, rutas API y las tres páginas) | Sin errores ni avisos |
| `npm run lint` (todo el repositorio) | Ya trae miles de errores previos ajenos a esta tarea; no se usó como criterio |

**No verificado (honestidad):**

* La pantalla no se abrió en un navegador: la migración `db/119_estado_servicio.sql` no está aplicada en Supabase, así que las consultas fallarían.
* La lectura real de Gmail, el flujo de permiso de Google, la clasificación con IA y la descarga de adjuntos reales **no se probaron**: faltan las claves de Victor.
* La Matriz de permisos (artefacto) no se pudo actualizar: esta cuenta no puede abrirla.
