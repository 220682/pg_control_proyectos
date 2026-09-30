# F4-B · RDT: API de partes (crear, validar, modo por avance del paquete)

Lee primero `00-reglas-de-contexto.md`. Carril **4 · RDT** · rama `local-worker-4`, puerto 3114.
Fase F4 · **Depende de:** F4-A cerrada. No depende de la maqueta (sin pantalla). Contrato que lees: `contrato-c5-rdt.md`.
**Punto de commit:** al cerrar la tanda, en `local-worker-4`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F4B-1 | **Crear parte** (`POST /api/rdts/partes`): exige Plan Maestro aprobado (mensaje claro sin él) y valida en servidor que el `(paquete, partida)` de cada actividad D, y de cada C/NC y material, pertenece al Plan Maestro aprobado vigente del servicio | Pruebas de los casos válido, sin plan y fuera del plan |
| F4B-2 | **Validar** (`PATCH` de `partes/[id]`): escribe el vínculo con **partida y paquete**; las actividades C/NC y los materiales cargan a una clave (paquete × partida o directa) elegida por el supervisor | Prueba |
| F4B-3 | **Modo «por avance del paquete»**: se declara la unidad de la guía; el servidor calcula y guarda las filas derivadas de las demás partidas (mismo %), **de solo lectura**; en modo «por partidas» se declara cada una | Prueba del reparto y de que el cliente no puede falsearlas |
| F4B-4 | **Reasignar paquete** de un RDT mientras esté `REGISTRADO` o `REVISADO`, no cuando esté `VALIDADO`; el PR **suma por partida** aunque la partida esté en dos paquetes (prueba de lectura sobre el motor existente; no se edita) | Prueba |
| F4B-5 | Permisos intactos (crear: administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo; validar o rechazar: administrador, jefe de proyectos, jefe de oficina técnica; rechazar uno validado: administrador y jefe de proyectos); 403 por rol, 400/404 por servicio; `npx tsc --noEmit`, suite y lint comparado con `main` | Pruebas de las funciones de permiso para los 13 roles + salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- `src/app/api/rdts/partes/route.ts` (`POST` ~121) y `src/app/api/rdts/partes/[id]/route.ts` (`PATCH` ~154; vínculos ~244-294: hoy resuelve `wbs → dp_partidas.id` y reescribe `rdt_actividad_partidas`; exige WBS existente en el DP del mismo servicio; `DELETE` ~332 dispara el recálculo del PR).
- Flujo 06: estados `REGISTRADO → REVISADO → VALIDADO | RECHAZADO`; solo `VALIDADO` es real oficial; un RDT validado no se reemplaza por una carga nueva de la misma fecha y turno; corregir un RDT rechazado: administrador, jefe de proyectos y supervisor operativo.
- Modo A/B del plan del 23-sep: A = se declara la unidad de la **partida guía**, `% = declarado ÷ metrado de la guía` y se aplica a todas las partidas del paquete; B = partida por partida. La función `repartirAvanceDelPaquete` ya existe en `src/lib/paquetes-trabajo/paquetes-trabajo.ts` (se **importa**). Con partida repartida, la base es la porción de la guía dentro de ese paquete.
- Notificación al subir: solo Administración (sin cambio). Nada de esto toca `recalcular_pr_desde_rdt`.

## Qué NO hacer

- No cambies permisos ni el motor del PR (`db/053`, `src/lib/pr/**`). No edites `paquetes-trabajo/**`, `plan-maestro/**`. No apliques migraciones. Sin push.
- No aceptes del cliente las filas derivadas ni la clave sin validarlas en servidor.
- Ante contradicción con un flujo, acción destructiva o duda de negocio: detente y devuelve la pregunta.

## Cierre

**Skills:** al empezar, lista `.claude/skills/` de `pg_control_proyectos` (hoy: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`) y del repositorio de la app (hoy sin carpeta de Skills) y anota «Skills revisados» en tu `resultados/F4-B.md`. **Usa `cerrar-tanda` al terminar** (adaptación de este plan: sus pasos de estados, evidencia y traspaso van en tu `resultados/F4-B.md`, no en el plan ni en el progreso compartidos).

`resultados/F4-B.md` (estado de F4B-1 a F4B-5, handoff, llamadas). Commit en `local-worker-4`, `git add` explícito.
