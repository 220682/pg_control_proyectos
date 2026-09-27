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

## Cuándo se actualiza README raíz y AGENTS.md

- `README.md` (raíz) se actualiza solo cuando hay cambios que alteran contenido ya existente ahí (visión, estructura, arquitectura) — no en cada sesión ni por cada mejora menor.
- `AGENTS.md` se actualiza cuando cambia cómo deben trabajar los agentes (reglas, límites, flujo de Orquestador, frases de activación).
- Ambos cambios siguen el mismo camino: Auditor propone, Gate 2 aprueba, Orquestador aplica.

## Revisión obligatoria de fuentes de verdad

Ver `00-estandar-agentes/05-aprendizaje-continuo.md` § Revisión obligatoria de fuentes de verdad para el procedimiento completo (se ejecuta después de cada sesión relevante, cada fase de plan, cada implementación y cada corrección aprobada).
