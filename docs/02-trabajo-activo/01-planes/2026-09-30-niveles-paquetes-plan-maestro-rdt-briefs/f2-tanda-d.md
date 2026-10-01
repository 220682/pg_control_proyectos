# F2-D · Disciplina: catálogo fijo y disciplina del paquete (migración 085)

Lee primero `00-reglas-de-contexto.md` y `00-protocolo-migraciones.md`. Contratos: `contrato-c2-paquetes.md`. Carril **3 · Paquetes** · rama `local-worker-3` (en `d4c5b3b`), puerto 3113. Meta: ~60 llamadas, ≤ 200k.
**Origen:** decisión de Victor (2026-09-30, noche): crear ahora el catálogo de Disciplina. **No depende de maqueta nueva** (las de F0-R ya traen el selector con catálogo simulado: `mockups/paquetes-agrupar.html`). **Bloquea:** F3-E (disciplina de la partida directa en el Plan Maestro).

## Decisiones de Victor (no repreguntar)

- Catálogo **fijo** de 5 disciplinas, con estos nombres: **Civil, Mecánica, Eléctrica, Instrumentación, Tuberías** (orden 1 a 5). Sin pantalla para editarlo.
- La disciplina es **obligatoria** en el paquete (al crearlo). Una partida dentro de un paquete **hereda** la del paquete. Los paquetes existentes (hoy 0 filas) no se tocan.
- Nadie cambia quién puede qué: las tablas 1 y 2 del flujo 14 siguen igual; ningún chip ni acceso nuevo.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F2D-1 | **Migración `db/085_*.sql`** (aditiva, idempotente, con comentario de cómo deshacer): tabla `disciplinas` (`id uuid pk`, `codigo text unique`, `nombre text`, `orden int`, `activo boolean`), sembrada con las 5 (insertar solo si no existen) y con lectura para usuarios autenticados y escritura solo del servicio (sigue el patrón de las tablas de catálogo y de RLS ya usado en `db/`; léelo en la migración 079 y en otra de catálogo, no inventes otro); columna `disciplina_id uuid null references disciplinas(id)` en `paquetes_trabajo` (nula en la base para no romper filas existentes; la obligatoriedad se exige en la API). **La aplicas tú** con `migrar_F2-D.py` (modos `check` por defecto y `apply`), candado y protocolo; si el sistema deniega, no lo rodees: déjalo listo con el comando exacto | Salida de `check` antes y después, conteos, existencia de tabla, 5 filas y columna |
| F2D-2 | **Lógica y API:** módulo `src/lib/disciplinas/` (tipo, lista de las 5 como respaldo y validación) y `GET /api/disciplinas` de solo lectura para usuarios autenticados. `POST /api/paquetes-trabajo` **exige** `disciplinaId` válida (400 con mensaje claro si falta o no existe); `PATCH` de un borrador permite cambiarla; el `GET` de paquetes la devuelve (`disciplinaId`, `disciplinaNombre`). Los permisos no cambian (solo administrador, jefe de proyectos y planner gestionan paquetes) | Pruebas: crea con y sin disciplina, disciplina inexistente, edición en borrador, no editable en validado/archivado, 13 roles intactos |
| F2D-3 | **Pantalla:** selector «Disciplina» (obligatorio, con asterisco y mensaje de error) en crear y editar paquete, como en `mockups/paquetes-agrupar.html`; el paquete muestra su disciplina (etiqueta) en la lista y el detalle; la lista se carga de `GET /api/disciplinas`. Reglas de diseño vigentes: alineación de tablas y color de avance (`design.md` 1.9.1) | Prueba de la lógica de la pantalla; `tsc`, `vitest`, lint comparado y `next build --webpack` |
| F2D-4 | **Contrato para F3-E:** deja en `resultados/F2-D.md` el esquema exacto de `disciplinas` (nombre de tabla y columnas) y cómo leer la disciplina de un paquete, para que el carril 2 construya contra él. Sin importar nada del carril 2 | Texto del contrato en el resultado |

## Qué NO hacer

- No toques `src/lib/plan-maestro/**`, `FormularioPlanMaestro`, `src/lib/permisos/**`, `src/lib/config/**`, `db/README.md`, `db/053` ni el motor del PR. No crees ramas ni más migraciones que la 085. Sin push. Sin navegador (solo F5).
- Ante contradicción con un flujo, acción destructiva o duda de negocio: detente y devuelve la pregunta.

## Cierre

**Skills:** al empezar, lista `.claude/skills/` de ambos repositorios y anota «Skills revisados»; usa `cerrar-tanda` al terminar (estados y traspaso en `resultados/F2-D.md`). Commit en `local-worker-3` con `git add` explícito. Mensaje final: ítems cerrados, pendientes, preguntas y llamadas.
