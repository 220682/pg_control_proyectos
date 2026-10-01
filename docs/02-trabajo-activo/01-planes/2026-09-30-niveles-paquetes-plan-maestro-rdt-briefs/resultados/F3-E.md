# Resultados F3-E · Disciplina en el Plan Maestro (migración 086)

Carril 2 · rama `local-worker-2` · commit `70e12d5` sobre `9f631b6`. Sin push ni merge. Sin navegador.

## Skills revisados

`pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `seguir-flujo-de-planes`, `verificar-permisos-por-rol`. La app no tiene carpeta de Skills. Se aplicó `cerrar-tanda`. `verificar-permisos-por-rol` no aplica: no cambia quién puede qué (se reutilizan `puedeGestionarPlanMaestro` y `puedeCrearVersionPlanMaestro`; ninguna prueba cambió esas reglas y una nueva fija los 13 roles).

## Estado de los ítems

| ID | Estado | Evidencia |
|---|---|---|
| F3E-1 | **Observado — migración 086 por aplicar** (archivo listo; el sistema denegó el script) | `db/086_plan_maestro_partidas_disciplina.sql`: `alter table plan_maestro_partidas add column if not exists disciplina_id uuid references disciplinas(id)`, con comentario de cómo deshacer. Aditiva e idempotente, sin tocar datos. El `check` fue **denegado** por el sistema («Auto-Mode Bypass»); no se rodeó, no se creó el candado, no se ejecutó nada contra la base. Comando abajo. Los conteos antes/después (240 / 5) y la existencia de la columna **no se pudieron medir**. |
| F3E-2 | Conforme (pruebas); depende de aplicar 086 en la base real | `src/lib/plan-maestro/disciplina.ts` (copia de `validarDisciplinaId`, sin importar del carril 3) y `src/app/api/plan-maestro/route.ts`. Reglas: la **directa** guarda su disciplina (`plan_maestro_partidas.disciplina_id`); la línea **de paquete** no la guarda ni la acepta del cliente (400: «hereda») y se lee de `paquetes_trabajo.disciplina_id`. `POST` acepta `disciplinas: [{ claveReporte, disciplinaId }]` opcional, validada (inexistente/inactiva/sin id: 400, no crea nada); una versión nueva parte de la disciplina de las directas de la aprobada (misma actividad y WBS). `PATCH` acepta `disciplinas: [{ lineaId, disciplinaId }]` en `GUARDAR_ASIGNACIONES` y `APROBAR`. **Aprobar** exige que toda directa tenga disciplina existente y activa (400 con los WBS). Líneas antiguas nulas: se leen sin error; solo impiden aprobar un borrador. `GET` devuelve `disciplinaId`, `disciplinaNombre` y `disciplinaHeredada` por línea y `disciplinas` (catálogo). Pruebas nuevas: 10 en `plan-maestro-api.test.ts` (sección «Disciplina») y 20 en `disciplina.test.ts` (30 nuevas en total) (directa sin disciplina, inexistente, inactiva, herencia, aprobar con directa sin disciplina, línea antigua nula, 13 roles intactos). |
| F3E-3 | Conforme (lógica y build); vista **Observado — pendiente de F5** | `LienzoPlanMaestro.tsx`: selector «Disciplina *» (con `aria-required`, borde rojo y «Elige la disciplina» tras intentar crear) en la directa editable; en la de paquete, etiqueta «Hereda: X» sin editar; columna opcional «Disciplina» en «Personalizar campos» (tras «HH totales», apagada por defecto, alineada a la izquierda). Si la columna está apagada, el selector va junto a la etiqueta «Prog.» de la descripción. `FormularioPlanMaestro.tsx` envía las disciplinas al guardar y al crear, y «Crear Plan Maestro» queda bloqueado con el motivo «Falta la disciplina de N líneas de partida directa» (`habilitacionCrear`, 3.er parámetro). Lógica en `disciplina.ts` y `lienzo-vista.ts`, probada. |
| F3E-4 | Conforme | Este archivo. |

Verificación: `npx tsc --noEmit` limpio; `npx vitest run`: 77 archivos, **800 pruebas verdes** (770 en F3-D); `eslint src`: **27 problemas (9 errores, 18 avisos), igual que F3-D y `main`**; `npx next build --webpack` correcto.

## Pendiente de Victor: aplicar la migración 086

El sistema denegó `python <ruta>\migrar_F3-E.py check` (y la creación del candado). Queda listo, fuera del repositorio:
`C:\Users\BRANDY\AppData\Local\Temp\claude\D--VICTOR-CLAUDE-CODE-pg-control-proyectos\cfbd2d3e-42a3-49ac-aa8d-f1c95c49efa2\scratchpad\migrar_F3-E.py`

Comandos (Victor, con el prefijo `!`): `! python "<ruta>\migrar_F3-E.py" check` y luego `! python "<ruta>\migrar_F3-E.py" apply`. Lee solo la variable `PR_DB_URL` dentro del proceso (primero del entorno, si no del archivo de entorno de DIARIO), nunca imprime valores; imprime conteos antes/después de `plan_maestro_partidas` (esperado 240), `proyecto_plan_maestro` (esperado 5), `disciplinas` (esperado 5) y si existe la columna; en `apply` ejecuta el SQL en una transacción y **revierte si los conteos cambian** o falla. Después: borrar el script (nada con credenciales quedó en el repositorio). Hasta aplicarla, el `GET` y el `POST` de `/api/plan-maestro` **fallan en la base real** (columna inexistente): aplicar antes de F5.

## Handoff

- Falta: aplicar 086 (arriba) y las comprobaciones de navegador de F5.
- Retomar: `cd D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-2` · `npx vitest run src/lib/plan-maestro src/app/api/plan-maestro` · `npm run dev -- --webpack -p 3112`.
- Decisión técnica (para validar): el borrador se **crea** con las directas sin disciplina (la interfaz solo puede elegirla cuando las líneas ya existen); lo que se valida al crear es la disciplina que el cliente envíe en `POST` (por clave de reporte) y la herencia de la versión anterior; la obligatoriedad **dura** se aplica al **aprobar** (y al guardar cualquier valor enviado). Es la lectura de «al crear el borrador y al aprobar» que cabe con la maqueta (selector sobre la línea). Si Victor prefiere exigirla antes de crear, habría que elegir la disciplina en un paso previo a «Crear borrador».
- Una línea de paquete cuyo paquete es anterior a db/085 (sin disciplina) hereda «—» y **no** bloquea la aprobación (no la define el Plan Maestro).
- Integración (F5-A): ninguna; los archivos tocados son del carril 2 (`lineas.ts`, `lienzo.ts`, `lienzo-vista.ts` y `route.ts` ya eran de F3). Sin cambio de permisos, chips ni accesos: flujo 14 y matriz no se tocan.
- Efecto en flujos escritos para F5-D: flujo 20 (Plan Maestro) debe registrar la disciplina de la directa (obligatoria al aprobar), la herencia del paquete, la columna opcional y que la versión nueva parte de la disciplina de la aprobada.

## Comprobaciones de navegador para F5 (tras aplicar 086)

1. Servicio con paquetes y partidas directas: cada directa muestra «Disciplina *» (5 opciones en orden: Civil, Mecánica, Eléctrica, Instrumentación, Tuberías); las de paquete muestran «Hereda: X» y no se editan.
2. Con directas sin disciplina y el 100 % repartido, «Crear Plan Maestro» muestra «Falta la disciplina de N líneas de partida directa» y marca en rojo los selectores faltantes; al elegirlas y guardar, persiste tras recargar y se puede crear.
3. «Personalizar campos»: «Disciplina» aparece junto a «Costo total ($)» y «HH totales», apagada por defecto; al encenderla, el selector pasa a la columna.
4. `APROBADO`: sin selectores, nombre de la disciplina (o «Sin disciplina» en una línea antigua). Versión nueva: las directas parten con la disciplina de la aprobada.
5. Filas de 28 px: el selector de la descripción (con columna apagada) no desborda; alineación y colores según `design.md` 1.9.1.

## Mejoras de trabajo

- El sistema (auto mode) denegó el `check` del script de migración aunque estaba autorizado en `/permissions` y el protocolo lo permite; igual que en F2-D. Conviene que el Orquestador aplique la 086 por otra vía o que Victor la corra con `!`. Las pruebas de API con base simulada (`plan-maestro-api.test.ts`) no persisten `update`: para probar aprobar con disciplina se siembra `disciplina_id` en las tablas simuladas.
- Heredocs de Bash con comillas simples y tildes siguen fallando: escribir los scripts de ajuste con Write y ejecutarlos.

## Reglas de negocio detectadas

Ninguna nueva (ya decididas por Victor: 5 disciplinas fijas, obligatoria en la directa, herencia del paquete, columna opcional). Sí se fijó, por decisión técnica, que la obligatoriedad dura se verifica al aprobar (ver Handoff); se propone a Victor confirmarla para el flujo 20.

## Huérfanos

Sin cambios respecto de F3-D. Nada borrado.

## Llamadas

Aproximadamente 38.
