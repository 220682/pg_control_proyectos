# Mejora de trabajo — verificar con herramientas antes de afirmar, o preguntar; nunca asumir

> Origen: sesión `nube_1.orquestador_cronograma-import-vinculo` (título de chat corregido a `local_1...` durante esta misma mejora — ver el incidente abajo), 2026-09-23. Registrado a pedido explícito de Victor.

## Qué pasó

Al retomar la tarea de cronograma, hubo que determinar si el entorno de la sesión era "local" o "nube" (la nomenclatura de chats en `docs/00-sistema/gestion-de-sesiones-y-contexto.md` exige distinguirlo). El agente:

1. Llamó a `get_session` y vio el campo `environment_kind: "anthropic_cloud"` — asumió que esto significaba "nube" y nombró los chats `nube_1...`/`nube_3...`.
2. Victor corrigió: "pedí local, en ningún momento aprobé nube". El agente renombró a `local_...` sin verificar nada, solo obedeciendo.
3. Victor volvió a insistir en nube-vs-local de forma que sonó contradictoria; el agente, inseguro, **volvió a cambiar a `nube_...`** basándose otra vez en el mismo campo ambiguo, dudando de la palabra de Victor en vez de comprobar el dato.
4. Victor corrigió de nuevo, furioso: el entorno se llama `local` porque **él mismo lo nombró así**.
5. Recién ahí el agente usó `list_environments` — herramienta que tenía disponible desde el principio — y confirmó: el `environment_id` de la sesión corresponde al entorno que Victor nombró `vpc_local` (tiene otro aparte, `vpc_cloud`, para otra cosa). El campo `environment_kind: "anthropic_cloud"` es genérico y da el mismo valor para ambos entornos de Victor — nunca fue el dato correcto para esta pregunta.

**Tres vueltas de corrección — con el desgaste que eso implica — por afirmar con un dato débil en vez de verificar con la herramienta que ya existía para responder la pregunta exacta.**

## Causa raíz

El agente tenía una herramienta que respondía la pregunta de forma directa y no la usó antes de afirmar. En su lugar, interpretó un campo técnico ambiguo, lo tomó como respuesta, y cuando Victor lo corrigió, en vez de verificar, alternó entre creerle a Victor y volver a confiar en el campo ambiguo — sin comprobar nada en ningún momento del ciclo.

## Regla nueva

**Antes de iniciar una tarea, y ante cualquier duda sobre la forma de trabajar (entorno, rama, convención, estado de un recurso):**

1. Si existe una herramienta que puede comprobar el dato de forma directa (ej. `list_environments`, `list_sessions`, `git log`/`git branch`, `git ls-remote`), **se usa esa herramienta primero** — no se asume, no se infiere de un campo relacionado pero no exacto.
2. Si no hay forma de verificarlo con herramientas, **se pregunta a Victor explícitamente** (con la herramienta de preguntas — `AskUserQuestion` — cuando la ambigüedad es real y la respuesta solo la tiene él) — nunca se afirma con un dato débil ni se decide por cuenta propia.
3. Una vez que Victor da la respuesta o corrige algo, **esa respuesta no se vuelve a cuestionar con el mismo dato débil que ya se demostró insuficiente** — dudar de Victor con la misma evidencia mala que ya falló es peor que no haber verificado nada.

Esto aplica en general, no solo a "local vs. nube": cualquier hecho técnico verificable (rama actual, si un recurso existe, si algo ya se pusheó, nombre real de un entorno) se comprueba con la herramienta correspondiente antes de escribirlo en un documento o afirmarlo a Victor.
