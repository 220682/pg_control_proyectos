# Resultados F5-F (corrección corta, arreglo A de H1)

Skills revisados: `cerrar-tanda` (aplica y se usó); la app no tiene carpeta de Skills.

## Estado
| Ítem | Estado | Evidencia |
|---|---|---|
| H1 arreglo A: `GET /api/paquetes-trabajo` | Conforme (pruebas); verificación en pantalla pendiente | Los vínculos se leen con `crearClienteAdmin()` mediante un tercer parámetro opcional de `cargarDatosDelServicio` (por defecto, el mismo cliente; POST/PATCH/PUT no cambian) |
| H1 arreglo A: `GET /api/cronograma` | Conforme (pruebas); verificación en pantalla pendiente | La lectura de `cronograma_actividad_partidas` usa el cliente admin |

Guardia: ninguno de los dos GET usa `exigirAlcance`. Su guardia es rol (`puedeVerPaquetesTrabajo` / `puedeVerCronograma`) y lectura del proyecto con el cliente del usuario (RLS) antes de llegar a los vínculos. No se cambió esa guardia ni el alcance. El admin solo lee los vínculos de las actividades ya leídas para ese servicio (`.in('cronograma_actividad_id', ids)`).

## Evidencia
- `npx vitest run src/app/api/paquetes-trabajo src/app/api/cronograma src/lib/paquetes-trabajo src/lib/cronograma`: 11 archivos, 124 pruebas verdes.
- `npx tsc --noEmit`: sin errores.
- eslint de lo tocado (`src/app/api/paquetes-trabajo`, `src/app/api/cronograma`, `src/lib/paquetes-trabajo`): sin problemas.
- Pruebas nuevas: paquetes (el mock simula RLS vacío para el cliente del usuario) con vínculos presentes en la respuesta y con rechazo de rol ajeno (403) y servicio inexistente (404); `cronograma-get.test.ts` (nuevo) con vínculos presentes, `dp_enlazado`, sin vínculos de actividades ajenas, y 403 y 404.
- Commit en `local-worker-1`: ver `git log` (mensaje «F5-F: ...»), 5 archivos con `git add` explícito.

## Rutas similares (otras lecturas de `cronograma_actividad_partidas`)
Todas las demás ya usan cliente admin; no se encontró ninguna otra con el cliente del usuario: `plan-maestro/route.ts` (admin), `paquetes-trabajo/vinculos/route.ts` (admin), `cronograma/route.ts` POST/otras (admin), `lib/proyectos/bloqueo-recarga.ts`, `dependencias-borrado.ts`, `borrado-cascada.ts` (admin). Nota: `paquete_trabajo_vinculos` también la lee el cliente del usuario en el GET de paquetes; no mostró síntomas en F5-B y no se tocó.

## Handoff
1. Volver a probar por pantalla F5B-3 (Agrupar, hito, dos paquetes con partida repartida, marcar, mover, plegar, «Crear paquete») en un servicio PRUEBA; pendiente de F5.
2. Sin push ni merge; sin migraciones ni cambios de políticas RLS.

## Mejoras de trabajo
Para simular RLS en pruebas: el mock de `crearClienteServidor` vacía tablas listadas y el de `crearClienteAdmin` no.

Reglas de negocio nuevas: ninguna. Huérfanos: ninguno. Fuentes de verdad revisadas: ninguna requería cambio (no cambia permisos ni alcance).

Llamadas: ~17.
