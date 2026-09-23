# Mejora de trabajo — preguntas frecuentes sobre el flujo de Orquestador

> Origen: sesión del 2026-09-23 donde Victor pidió auditar `docs/00-sistema/roles-y-flujo.md` en busca de huecos (ver también [2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md](2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md), que es el incidente que originó la auditoría). Durante la conversación salieron dudas operativas que no estaban claras ni siquiera después de corregir los huecos — se guardan aquí como referencia rápida, en formato pregunta/respuesta, para no tener que rederivarlas de la política cada vez.
>
> **No es una fuente normativa nueva.** La fuente normativa sigue siendo `docs/00-sistema/roles-y-flujo.md` y `docs/00-sistema/convenciones-de-trabajo.md` — este archivo es una explicación en lenguaje llano de lo que ya dicen esos documentos (algunas de estas preguntas, de hecho, hicieron que se corrigiera texto ambiguo en esos documentos; ver `Mejoras continuas/2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md` § Seguimiento y § Seguimiento 2).

## ¿En qué momento se para la implementación?

Solo en dos situaciones, nunca por juicio propio del agente:

1. **Conflicto de regla de negocio no anticipado** (Worker): regla nueva contradice una ya escrita en un Flujo de trabajo. El Worker pregunta a Victor en el momento (no sigue implementando con el conflicto sin resolver, no espera al cierre) → valida la respuesta → la escribe en el apartado → recién ahí continúa. Si la respuesta no resuelve el conflicto, repite el ciclo.
2. **Una acción puntual reservada a autorización explícita**: crear/renombrar/eliminar rama o worktree, merge, push a infraestructura, eliminar recursos.

Fuera de esas dos, nada más detiene la implementación. El chequeo de rama del Auditor frena la *auditoría*, no la implementación (ocurre después, cuando el Worker ya entregó). La excepción de "Orquestador implementa él mismo" se decide en el plan, antes de empezar — no es una pausa a mitad de tarea.

## ¿Cómo se manejan commit, push y merge?

- **Commit** = guardar un paquete de cambios localmente, con una nota de qué y por qué. Nadie más lo ve todavía.
- **Push** = subir esos commits a GitHub, a la rama en la que se está trabajando (ej. `work-1`). Sigue siendo una rama aislada — no toca el proyecto oficial (`main`).
- **Merge** = juntar los cambios de una rama (`work-1`) dentro de `main`. Es el paso que realmente publica/despliega el trabajo — es el Gate 2 de Victor.

| Acción | Quién | ¿Pide autorización cada vez? |
|---|---|---|
| Commit + push en `work-N` | Worker, en su propia rama | No — ya está pre-autorizado por convención: ~cada 35% de avance acumulado, nunca a medias de un ítem |
| Merge (`work-N` → `main`) | Nadie sin autorización de Victor | Sí, siempre — es el Gate 2 |
| Commit/push/merge/PR/crear rama | Orquestador, Planner, Auditor | No deberían tocar esto — no implementan, no están en `work-N` |

## ¿Qué hace el Orquestador al inicio de una tarea?

Cuando Victor dice "vamos a trabajar en un plan con agente orquestador":

1. Responde con el flujo completo y pregunta el objetivo (qué lograr, qué no debe cambiar, cómo se sabe que terminó).
2. Lee la política (`roles-y-flujo.md`, `convenciones-de-trabajo.md`, `gestion-de-sesiones-y-contexto.md`) y los documentos mínimos aplicables.
3. Diseña el entorno: cuántos Workers, qué ramas (`work-N`), qué worktrees, qué chats — revisa si ya hay recursos libres para reutilizar antes de pedir crear nuevos.
4. Pregunta antes de crear, renombrar o eliminar cualquier rama/worktree/chat (eso sí necesita autorización explícita — es infraestructura, no uno de los 2 Gates).
5. Entrega el objetivo al Planner, que arma el plan.

Lo que nunca hace, así se vea simple: implementar él mismo. Se autoverifica antes de tocar código/documentación: *¿esto lo está haciendo un Worker en su rama propia?* Si no, para y asigna un Worker.

## ¿Qué hace el Orquestador si encuentra una tarea anterior ya cerrada al 100%?

1. No la toca ni la reabre — queda íntegra tal cual.
2. Revisa si la rama `work-N` de esa tarea quedó libre: la sincroniza con `main` y verifica que no le quede trabajo pendiente.
3. Si está libre, la reutiliza para el Worker de la tarea nueva — no crea una rama nueva porque sí (el pool `work-1`/`work-2` es persistente).
4. El chat viejo lleva prefijo `hist_` (se lo pone si no lo tenía) y no se reutiliza — la tarea nueva siempre abre chat propio. Se reutiliza la rama/worktree, no el chat.
5. No pregunta para esto — reutilizar algo que ya está libre no es "crear/renombrar/eliminar infraestructura".

## ¿El Orquestador puede borrar y abrir chats?

- **Abrir chat nuevo:** sí, es autónomo — así se crea el chat propio de cada Worker/Planner/Auditor (existe la herramienta `create_session` para sesiones en la nube; en local se abre manualmente en la app).
- **Borrar chat:** no, nunca — ni siquiera el Orquestador. No existe una herramienta de agente para eso, y la política tampoco lo pide. Un chat cerrado se **renombra** con el prefijo `hist_` y queda como historial indefinidamente — misma lógica que una tarea cerrada en `Tareas de implementacion/` no se borra.
- Si alguna vez Victor quiere borrar un chat de verdad, es una acción manual suya desde la app de Claude — no es un paso del flujo ni algo que un agente ejecute, ni con autorización.

## Corrección de fondo detrás de estas preguntas

Varias de estas respuestas expusieron redacciones ambiguas en la política (ver detalle completo en `Mejoras continuas/2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md` § Seguimiento y § Seguimiento 2):

- La excepción de "Orquestador implementa" ahora exige quedar por escrito en el plan aprobado, acotada a esa tarea.
- El Auditor verifica primero, con `git log`/`git branch --contains`, la rama real de los commits.
- El Orquestador no puede pedir cierre a Victor sin Informe de Auditoría ya emitido.
- Se documentó el modelo de 2 únicos Gates de Victor (plan, cierre) — entre ambos, cero aprobaciones intermedias.
- Commit/push del Worker en `work-N` es autónomo, no pide autorización caso por caso.
- Los chats no se borran, se renombran `hist_`.

Todo esto ya está aplicado en `docs/00-sistema/roles-y-flujo.md` y `docs/00-sistema/convenciones-de-trabajo.md` (commits `35a24f5`, `9b44725`, `7683aed`).
