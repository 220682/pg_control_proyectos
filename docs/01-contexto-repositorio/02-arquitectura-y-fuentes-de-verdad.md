# Arquitectura y fuentes de verdad

## Las tres fuentes de verdad centrales

```text
AGENTS.md      → norma raíz para agentes.
README.md      → visión, arquitectura y cambios de alto nivel del sistema.
docs/README.md → navegación y operación documental dentro de docs/.
```

Los flujos de negocio (`docs/04-flujos-de-negocio/NN-*.md`) son la fuente de verdad de las reglas funcionales de cada tema — una regla se escribe una sola vez, en su flujo dueño.

## Qué flujo es dueño de cada regla

Ver el índice de `docs/04-flujos-de-negocio/README.md` para la lista completa de los 21 flujos y su tema. Ante la duda de a qué flujo pertenece una regla nueva, se revisa primero ese índice — nunca se crea un flujo nuevo ni se duplica una regla ya escrita en otro.

## Cómo se promueve un cambio

| Tipo de hallazgo | Destino | Quién escribe y cuándo |
|---|---|---|
| Regla funcional/de negocio validada por Victor en el momento | Flujo de negocio dueño de la regla | Worker, al consolidar hallazgos (antes de entregar) |
| Mejora de trabajo / aprendizaje | `03-aprendizaje-continuo/` | Worker, al consolidar hallazgos |
| Evidencia de una implementación | Archivo de evidencia del plan | Worker |
| Cambio de arquitectura/visión | `README.md` raíz | Auditor propone → Victor aprueba en Gate 2 → Orquestador aplica |
| Cambio de comportamiento de agentes | `AGENTS.md` o `00-estandar-agentes/` | Auditor propone → Gate 2 → Orquestador aplica |
| Cambio de navegación de `docs/` | `docs/README.md` | Auditor propone → Gate 2 → Orquestador aplica |
| Cambio específico de este repositorio | `01-contexto-repositorio/` | Auditor propone → Gate 2 → Orquestador aplica |
| Diseño/UI | `05-diseno-y-referencias/design.md` | Auditor propone → Gate 2 → Orquestador aplica |
| Procedimiento reusable que ya se repitió | Skill agnóstico en `.claude/skills/<nombre>/SKILL.md` | Auditor propone (`PROPONER SKILL`) → Gate 2 → Orquestador crea |
| Pendiente fuera de alcance | `planes-futuros.md` | Solo con decisión explícita de Victor |

**El Worker nunca edita** `AGENTS.md`, `README.md`, `docs/README.md` ni el estándar de agentes por hallazgos propios: los deja anotados en el progreso para que el Auditor los evalúe. Excepción escrita y acotada: cuando el objeto explícito del plan es construir esa estructura (ver el plan de reestructuración documental, §10.1, como precedente de esta excepción).

**Ejemplos concretos de las dos categorías más frecuentes** (ver la distinción completa en `00-estandar-agentes/05-aprendizaje-continuo.md`):

- **Regla de negocio** (va directo al flujo dueño): "el AC se calcula de la suma de HH+HM más los porcentajes de avance de materiales y subcontratos" → va a `04-flujos-de-negocio/18-control-avance.md`, integrada en su estructura, nunca como nota aparte.
- **Mejora de trabajo** (va a `03-aprendizaje-continuo/`): "intentamos correr SQL por la conexión directa de Postgres, falló por falta de salida IPv6 en el sandbox, se resolvió usando la Management API de Supabase" → es un aprendizaje sobre cómo se trabaja, no una regla del sistema.

## Políticas de coherencia y trazabilidad (Victor, 2026-09-28)

Políticas de este repositorio, no reglas de negocio del sistema. Aplican a todo rol (Orquestador, Planner, Worker, Auditor) y a todo Spec o plan.

**1. La matriz de permisos es la base de los accesos.** El artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT) es el instrumento editable de la matriz de interfaces (con y sin datos económicos) y de acciones por rol. Es la base del flujo 14 (Accesos y restricciones), que a su vez está ligado al flujo 16 (Paneles). Toda tarea que cree, cambie o elimine una **interfaz, acción, permiso o acceso** (una pantalla, un chip, una ruta, un rol) actualiza **en la misma tarea** el artefacto, el flujo 14 (que conserva la última versión aprobada) y el flujo 16 o el registro único de accesos cuando exista. Una interfaz o acción nueva que no figura en el artefacto no está terminada. Los flujos 14 y 16 citan el artefacto. El plan futuro de gestionar permisos desde la app web (`docs/02-trabajo-activo/01-planes/planes-futuros.md`) también se somete a este artefacto.

**2. Un Spec o plan que entra en conflicto con lo escrito se implementa en todos los afectados.** Si un Spec, un plan o un flujo entra en conflicto con otro flujo, con el artefacto o con una regla ya escrita, la implementación **abarca todos los flujos, planes y documentos afectados**, no solo el de origen. Se listan los afectados en el plan (sección de contradicciones), se consulta a Victor cada contradicción antes de editar un flujo (regla de "Integrar una regla de negocio nueva en un flujo"), se actualizan todos, y se anota dónde quedó aplicado cada cambio (enlace al flujo y a la sección). **No se deja nada suelto:** el Auditor verifica, antes del Gate 2, que no queda ningún flujo o documento afectado sin actualizar ni ninguna referencia que apunte a la versión anterior. El objetivo es la trazabilidad completa del proyecto.

## Ante una contradicción entre fuentes

Ante una contradicción entre `AGENTS.md`, `README.md`, `docs/README.md` o un flujo de negocio, se consulta a Victor — no se asume cuál prevalece.

**Excepción (D1):** para el flujo de trabajo con Orquestador/Planner/Worker/Auditor específicamente, la fuente normativa es `00-estandar-agentes/04-flujo-sdd-y-planes.md` (el diagrama del Spec a Cierre), no el plan ni ningún otro documento — si un plan, un progreso o un artifact derivado difiere de lo que dice ese archivo, se corrige el plan o el artifact, no el estándar. Esta excepción no aplica a las reglas de negocio del sistema (`04-flujos-de-negocio/`), donde la contradicción sigue resolviéndose consultando a Victor.

## Integrar una regla de negocio nueva en un flujo

El agente **no edita el flujo por su cuenta sin haberlo consultado primero** cuando la regla nueva contradice una ya escrita. Al integrar:

1. Se escribe **dentro de la estructura existente del flujo**, en la sección donde encaja — nunca pegada al final como nota aparte.
2. Si contradice una regla ya escrita, se **modifica lo existente** con lo acordado con el Responsable humano; no quedan las dos versiones (la vieja y la nueva) conviviendo en el mismo flujo.
3. Si el conflicto surgió durante la implementación (Worker), la consulta es directa, en el propio chat del Worker (excepción D6, ver `00-estandar-agentes/02-roles-y-delegacion.md`) — no se sigue implementando con el conflicto sin resolver.
4. Se anota en el plan/progreso dónde quedó aplicada la regla (enlace al flujo y a la sección).

## Cuándo se actualiza README raíz y AGENTS.md

- `README.md` (raíz) se actualiza solo cuando hay cambios que alteran contenido ya existente ahí (visión, estructura, arquitectura) — no en cada sesión ni por cada mejora menor.
- `AGENTS.md` se actualiza cuando cambia cómo deben trabajar los agentes (reglas, límites, flujo de Orquestador, frases de activación).
- Ambos cambios siguen el mismo camino: Auditor propone, Gate 2 aprueba, Orquestador aplica.

## Revisión obligatoria de fuentes de verdad

Ver `00-estandar-agentes/05-aprendizaje-continuo.md` § Revisión obligatoria de fuentes de verdad para el procedimiento completo (se ejecuta después de cada sesión relevante, cada fase de plan, cada implementación y cada corrección aprobada).
