# Resultado F2-D · Disciplina: catálogo fijo y disciplina del paquete

Carril 3 · rama `local-worker-3` · commit `cfc180f` (sobre `d4c5b3b`). Sin push.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `seguir-flujo-de-planes`, `verificar-permisos-por-rol`. El repositorio de la app no tiene carpeta de Skills. Aplicado: `cerrar-tanda` (con la adaptación del plan: estados y traspaso aquí). `verificar-permisos-por-rol` no aplica (permisos sin cambio; prueba de los 13 roles en vitest).

## Estado de ítems

| ID | Estado | Evidencia |
|---|---|---|
| F2D-1 | **Observado: migración 085 escrita, NO aplicada** (el sistema denegó el script) | `db/085_disciplinas.sql`: tabla `disciplinas`, semilla de 5 con `on conflict (codigo) do nothing`, RLS con lectura `authenticated` (sin política de escritura: solo llave de servicio, patrón de 054/079), columna `paquetes_trabajo.disciplina_id uuid null references disciplinas(id)`, comentario de cómo deshacer. Aditiva e idempotente. No hay salida de `check` (ver «Pendiente de Victor»). |
| F2D-2 | Conforme | `src/lib/disciplinas/disciplinas.ts` (tipo, respaldo de 5, `validarDisciplinaId`, `disciplinasActivas`, `nombreDeDisciplina`); `GET /api/disciplinas` (solo lectura, activas, cualquier usuario autenticado; sin usuario 403). `POST /api/paquetes-trabajo` exige `disciplinaId` (400: «Elige la disciplina del paquete» / «La disciplina elegida no existe»); `PATCH EDITAR` en BORRADOR la exige y la cambia; VALIDADO/ARCHIVADO siguen en 400; `GET` devuelve `disciplinaId` y `disciplinaNombre` (null en paquetes anteriores). Pruebas: `paquetes-api.test.ts` (bloque F2D, 8), `disciplinas-api.test.ts` (los 13 roles leen), `disciplinas.test.ts`. |
| F2D-3 | Conforme (render: Observado, pendiente de F5) | Selector «Disciplina *» (obligatorio, `aria-required`, error por `role=alert`) en crear y editar (`PasoAgrupar.tsx`), cargado de `GET /api/disciplinas` (`FormularioPaquetesTrabajo.tsx`); etiqueta de disciplina en la cabecera del paquete de la lista. `cuerpoNuevoPaquete` y `cuerpoEditarPaquete` validan la disciplina (pruebas). El «Detalle» no se tocó: la disciplina se ve en la cabecera del paquete, que es visible con el detalle abierto. `npx tsc --noEmit`: 0 errores. `npx vitest run`: 76 archivos, 746 pruebas verdes. `npm run lint`: 27 problemas (9 errores), idéntico a F2-C; eslint sobre mis rutas: 0. `npx next build --webpack`: compila. |
| F2D-4 | Conforme | Contrato abajo. |

## Contrato para F3-E (esquema exacto)

Tabla `disciplinas` (`db/085`): `id uuid pk default gen_random_uuid()`, `codigo text not null unique`, `nombre text not null`, `orden int not null`, `activo boolean not null default true`. Filas (codigo / nombre / orden): `CIVIL` Civil 1, `MECANICA` Mecánica 2, `ELECTRICA` Eléctrica 3, `INSTRUMENTACION` Instrumentación 4, `TUBERIAS` Tuberías 5. RLS: lectura `authenticated`; escritura solo servicio.
Disciplina del paquete: `paquetes_trabajo.disciplina_id uuid null → disciplinas(id)` (nula solo en filas anteriores; la API la exige al crear/editar). Leer: `select disciplina_id, disciplinas(nombre) from paquetes_trabajo` o por la API: `GET /api/paquetes-trabajo?proyectoId=` → `paquetes[].disciplinaId` y `paquetes[].disciplinaNombre`. Catálogo: `GET /api/disciplinas` → `{ disciplinas: { id, codigo, nombre, orden, activo }[] }`. Una partida dentro de un paquete hereda la del paquete (se resuelve por `paquete_trabajo_vinculos.paquete_id` → `paquetes_trabajo.disciplina_id`); la de una partida directa la define F3-E (columna propia, fuera de esta tanda). Validación reutilizable: `validarDisciplinaId` en `src/lib/disciplinas/disciplinas.ts` (el carril 2 debe copiarla, no importar del carril 3, según la regla de carriles).

## Pendiente de Victor: aplicar la migración 085
El sistema denegó el script (`migrar_F2-D.py`, con `check` por defecto y `apply`), así que no se rodeó. Queda listo, fuera del repositorio:
`C:\Users\BRANDY\AppData\Local\Temp\claude\D--VICTOR-CLAUDE-CODE-pg-control-proyectos\cfbd2d3e-42a3-49ac-aa8d-f1c95c49efa2\scratchpad\migrar_F2-D.py`
Comandos (Victor, con el prefijo `!`): `! python <ruta del script> check` y luego `! python <ruta del script> apply`. Lee solo `PR_DB_URL` dentro del proceso, imprime estado antes/después (existencia de tabla, 5 filas, conteo de `paquetes_trabajo`, columna) y revierte si falla. El candado `CANDADO-MIGRACIONES.txt` no llegó a crearse (la orden también fue denegada); si Victor aplica, que no haya otro candado vigente. Borrar el script después. Hasta que se aplique, `GET /api/disciplinas` y el `GET`/`POST` de paquetes fallarán en la base real (tabla y columna inexistentes): **aplicar antes de F5**.

## Handoff
- Falta: aplicar 085 y comprobar en navegador (F5).
- Retomar: `cd D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-3`; `npm run dev -- --webpack -p 3113`; `/paquetes-trabajo?proyectoId=<id>`.
- Decisión técnica: la validación de disciplina en la API se hace contra la tabla (existente y activa); en la pantalla contra el catálogo cargado. Si la lista no carga, el selector queda vacío y crear falla con mensaje claro.
- Los imports de `src/lib/paquetes-trabajo/` a `disciplinas` son relativos (vitest no define el alias `@`).
- Sin cambio de permisos, chips ni accesos; flujo 14 y matriz no se tocan.
- Efecto en flujos escritos para F5-D: flujo de paquetes (19) debe registrar la disciplina obligatoria y la herencia.

## Comprobaciones de navegador para F5
1. Crear paquete: el selector «Disciplina *» lista las 5 en orden; sin elegirla, error claro y no guarda.
2. Editar un borrador: precarga la disciplina; cambiarla y recargar persiste.
3. La cabecera del paquete muestra la disciplina; paquete antiguo sin disciplina: sin etiqueta y al editar exige elegirla.
4. VALIDADO/ARCHIVADO: sin Editar; cuenta sin gestión: sin selector.

## Mejoras de trabajo
- Heredocs largos de Bash con comillas fallan y los `\n` escritos dentro de un heredoc de Python se vuelven saltos reales: guardar los scripts de ajuste con Write y escapar `\n` solo ahí. Los lib que prueba vitest usan imports relativos (sin alias `@`).
- Un script de migración y el candado en `resultados/` pueden ser denegados por el sistema: dejar el script listo y anotar los comandos, sin insistir.

## Reglas de negocio detectadas
Ninguna nueva (ya decididas por Victor: catálogo fijo de 5, obligatoria en paquete, herencia).

## Huérfanos
Los de F2-B/F2-C siguen igual. Nada borrado.

## Llamadas
Aproximadamente 35.
