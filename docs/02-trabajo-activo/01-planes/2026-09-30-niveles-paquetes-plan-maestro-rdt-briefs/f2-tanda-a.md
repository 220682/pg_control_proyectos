# F2-A · Paquetes: vínculos, API y lógica (sin pantalla)

Lee primero `00-reglas-de-contexto.md`. Carril **3 · Paquetes** · rama `local-worker-3` (worktree `.worktrees/local-worker-3`, puerto 3113).
Fase F2 · **Depende de:** nada · No depende de la maqueta. Contratos que lees: `contrato-c2-paquetes.md` (y `contrato-c1-niveles.md` solo para `NodoEstructura`).
**Migraciones reservadas: `db/079`–`081`** (se escriben, **no se aplican**).
**Punto de commit:** al cerrar la tanda, en `local-worker-3`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F2A-1 | Migraciones 079–081: tabla `paquete_trabajo_vinculos` (PK, claves foráneas al vínculo `cronograma_actividad_partidas` con borrado en cascada, `unique (cronograma_actividad_id, dp_partida_id)`), más `orden` y `nivel` en `paquetes_trabajo`. **Se conservan sin uso** `paquete_trabajo_partidas` y `paquete_trabajo_programacion`. Idempotentes, con RLS de lectura como las de `db/072` | Archivos SQL + lectura crítica (sin aplicar) |
| F2A-2 | Lógica pura en `src/lib/paquetes-trabajo/`: suma del metrado declarado por partida contra el contractual (100 %) y **restante por partida**; hitos no cuentan; selección de jerarquía (**marcar una fila resumen marca sus hijas**, desmarcables); orden y movimiento; plegado. Copia de `sumarMetradoPorPartida` y `partidasConMetradoIncompleto` (hoy en `src/lib/cronograma/vinculos.ts`, que es del carril 1) | Pruebas unitarias |
| F2A-3 | `PUT /api/paquetes-trabajo/vinculos` (archivo nuevo): fija vínculos con metrado y la marca de hito (`requiere_partidas`); valida en servidor (partida del servicio, actividad con fechas, metrado > 0, hito sin metrado); llama `recalcular_pr_fechas_base`; permiso `puedeGestionarPaquetesTrabajo` | Prueba de API con datos simulados |
| F2A-4 | `POST` y `PATCH` de `/api/paquetes-trabajo` con la forma de C2: crear (nombre, nivel, modo, guía, vínculos), editar en `BORRADOR`, **mover** (orden), archivar; un vínculo en **un solo** paquete; una partida puede estar en varios; la guía debe estar entre las partidas del paquete; **sin fechas** | Pruebas |
| F2A-5 | `GET /api/paquetes-trabajo` devuelve paquetes con vínculos, actividades como `NodoEstructura[]` (hoy, con la jerarquía de `RESUMEN`/`TAREA`/`HITO`), partidas del DP para consulta y `restantePorPartida` | Prueba |
| F2A-6 | Guardias: rol sin permiso → 403; servicio inexistente o ajeno → 400/404 según alcance; ver para los 13 roles; `npx tsc --noEmit`, suite y lint comparado con `main` | Salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- API actual `src/app/api/paquetes-trabajo/route.ts`: `GET` (~60) devuelve `{ paquetes, partidasDp }`; `POST` (~128) recibe `{ proyectoId, nombre, descripcion, modoMedicion, partidas[] }` con programación diaria por partida; `PATCH` (~234) solo archiva. Lógica actual en `src/lib/paquetes-trabajo/paquetes-trabajo.ts` (`validarPartidasDelPaquete`, `validarProgramacionPartida`, `unidadYMetradoDeGuia`, `repartirAvanceDelPaquete`; este último se **conserva**: lo usan F4 y el modo por avance del paquete).
- El vínculo hoy: `cronograma_actividad_partidas` PK `(cronograma_actividad_id, dp_partida_id)` + `metrado` nulo o > 0 (`db/039`, `db/071`). El enlace automático 1:1 por EDT (POST del cronograma) ya lo deja con el metrado contractual: tu pantalla lo pre-llena.
- Hitos: `cronograma_actividades.requiere_partidas` (default true, `db/072`); hoy se marcan con `PATCH /api/cronograma/hitos` (archivo del carril 1, que retira la columna Hito de su pantalla): tú lo mueves a Paquetes con `PUT …/vinculos`.
- Permisos (no se tocan): `puedeVerPaquetesTrabajo` = cualquier rol conocido; `puedeGestionarPaquetesTrabajo` = administrador, jefe de proyectos, planner (`src/lib/permisos/permisos.ts`).
- El paquete **no lleva fechas**: la programación diaria vive solo en el Plan Maestro. Cuidado: el `POST /api/plan-maestro` actual lee `paquete_trabajo_programacion`; ese archivo es del carril 2, no lo toques.

## Qué NO hacer

- No apliques migraciones; no edites `db/README.md`. No edites `src/lib/cronograma/**` ni `api/cronograma/**` (carril 1) ni `plan-maestro/**` (carril 2). No toques `permisos.ts` ni `registro-accesos.ts`.
- No borres `paquete_trabajo_partidas` ni `paquete_trabajo_programacion`.
- No cambies permisos. Sin push. Ante contradicción con un flujo, acción destructiva o duda de negocio: detente y devuelve la pregunta.

## Cierre

**Skills:** al empezar, lista `.claude/skills/` de `pg_control_proyectos` (hoy: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`) y del repositorio de la app (hoy sin carpeta de Skills) y anota «Skills revisados» en tu `resultados/F2-A.md`. **Usa `cerrar-tanda` al terminar** (adaptación de este plan: sus pasos de estados, evidencia y traspaso van en tu `resultados/F2-A.md`, no en el plan ni en el progreso compartidos).

`resultados/F2-A.md` (estado de F2A-1 a F2A-6, handoff con migraciones escritas, llamadas). Commit en `local-worker-3`, `git add` explícito.
