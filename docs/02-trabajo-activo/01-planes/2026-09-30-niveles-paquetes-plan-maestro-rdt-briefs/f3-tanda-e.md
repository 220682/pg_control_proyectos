# F3-E · Disciplina en el Plan Maestro: partida directa, herencia y columna del lienzo (migración 086)

Lee primero `00-reglas-de-contexto.md` y `00-protocolo-migraciones.md`; luego `resultados/F2-D.md` (sección «Contrato para F3-E»: esquema exacto de `disciplinas`, ya **aplicada en la base**) y `resultados/F3-D.md` (qué dejó el lienzo). Carril **2 · Plan Maestro** · rama `local-worker-2` (en `9f631b6`), puerto 3112. Meta: ~60 llamadas, ≤ 200k.
**Origen:** decisión de Victor (2026-09-30, noche): 5 disciplinas fijas (Civil, Mecánica, Eléctrica, Instrumentación, Tuberías); la disciplina es **obligatoria** en el paquete y en la partida directa; la partida dentro de un paquete **hereda** la del paquete; columna opcional «Disciplina» en el lienzo (maqueta aprobada: `mockups/plan-maestro-tres-paneles.html`, selector de directa y columna en «Personalizar campos»).

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F3E-1 | **Migración `db/086_*.sql`** (aditiva, idempotente, comentario de cómo deshacer): columna `disciplina_id uuid null references disciplinas(id)` en `plan_maestro_partidas` (la línea del lienzo). Nula en la base: las 240 líneas existentes no se tocan. **La aplicas tú** con `migrar_F3-E.py` (modos `check` por defecto y `apply`; Victor tiene permitidos `python *migrar_*.py check` y `apply`), siguiendo el protocolo; fuera del repositorio, borrado al terminar. Si el sistema deniega, no lo rodees: déjalo listo con el comando exacto | `check` antes y después, conteos (`plan_maestro_partidas` 240, `proyecto_plan_maestro` 5) iguales, columna existe |
| F3E-2 | **Regla en servidor** (`src/lib/plan-maestro/**`, `src/app/api/plan-maestro/route.ts`): una **línea de partida directa** exige `disciplinaId` válida y activa al crear el borrador y al **aprobar**; una línea **dentro de un paquete** hereda la disciplina del paquete (la lees de `paquetes_trabajo.disciplina_id`; no se guarda ni se acepta del cliente en esa línea). Las líneas anteriores sin disciplina no rompen la lectura ni los planes aprobados existentes; un borrador de versión nueva no puede aprobarse con una directa sin disciplina (mensaje claro). Copia la validación de `validarDisciplinaId` (no importes del carril 3). `GET` devuelve `disciplinaId` y `disciplinaNombre` por línea y el catálogo (`disciplinas`) | Pruebas: directa sin disciplina (400), con inexistente/inactiva, herencia del paquete, aprobar con directa sin disciplina, línea antigua nula sin error, 13 roles intactos |
| F3E-3 | **Lienzo:** selector «Disciplina *» en la partida directa (obligatorio, con asterisco y mensaje de error, como en la maqueta); la línea dentro de un paquete la muestra heredada y no editable; columna opcional «Disciplina» en «Personalizar campos» (junto a «Costo total ($)» y «HH totales»), apagada por defecto. Reglas de diseño vigentes (`design.md` 1.9.1): alineación de tablas, color del avance real, barras azuladas | Prueba de la lógica de la vista; `tsc`, `vitest`, lint comparado con el total de F3-D (27) y `next build --webpack` |
| F3E-4 | `resultados/F3-E.md` con estados, handoff, hallazgos y lista corta de comprobaciones de navegador para F5 | — |

## Qué NO hacer

- No toques `src/lib/paquetes-trabajo/**`, `src/lib/disciplinas/**` ni la API de paquetes (carril 3), `src/lib/permisos/**`, `src/lib/config/**`, `db/README.md`, `db/053` ni el motor del PR. No crees más migraciones que la 086. Sin push. Sin navegador (solo F5).
- Ante contradicción con un flujo, acción destructiva o duda de negocio: detente y devuelve la pregunta.

## Cierre

**Skills:** al empezar, lista `.claude/skills/` de ambos repositorios y anota «Skills revisados»; usa `cerrar-tanda` al terminar (estados y traspaso en `resultados/F3-E.md`). Escribe los archivos con Write (los heredocs largos de Bash con comillas fallan). Commit en `local-worker-2` con `git add` explícito. Mensaje final: ítems cerrados, pendientes, preguntas y llamadas.
