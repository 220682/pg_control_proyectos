# Aprendizaje continuo

## Categorías, no dos, sino varias

Un hallazgo durante un plan puede ser una de estas cosas — nunca se mezclan:

| Categoría | Qué es | Dónde vive |
|---|---|---|
| **Hallazgo** | Cualquier observación registrada en el momento en que ocurre, antes de clasificarla. | El progreso o el plan de la tarea activa, en el apartado que corresponda. |
| **Mejora de trabajo / aprendizaje** | Un aprendizaje sobre **cómo se trabaja** (método, herramientas, workarounds operativos) — no una regla del sistema que se está construyendo. | Un archivo individual en `03-aprendizaje-continuo/` del repositorio de documentación. |
| **Regla de negocio** | Una regla del sistema que se está construyendo (cómo se calcula, valida o comporta algo). | Directo en el flujo de negocio dueño de esa regla, integrada en su estructura — nunca como nota aparte. |
| **Decisión pendiente** | Algo que el Responsable humano decide explícitamente postergar. | `planes-futuros.md` (o el archivo equivalente de trabajo pospuesto). |
| **Evidencia** | El resultado verificado de un ítem de la Punch List. | El archivo de evidencia homónimo del plan. |
| **Procedimiento reusable** | Un procedimiento que ya se repitió más de una vez y conviene convertir en Skill. | Propuesta del Auditor (`PROPONER SKILL`) → Skill agnóstico tras el Gate 2. |

## Revisión obligatoria de fuentes de verdad

Después de cada sesión relevante, cada fase de un plan, cada implementación y cada corrección aprobada, el rol que trabajó ejecuta esta revisión:

1. Revisar si lo realizado creó, corrigió, aclaró o contradijo una regla documentada.
2. Clasificar el destino según la tabla de arriba (o la tabla concreta de fuentes de verdad del repositorio, en `01-contexto-repositorio/`).
3. Escribir lo que le corresponde a su rol; anotar en el progreso lo que corresponde a otro rol.
4. Registrar qué fuente se actualizó (o se propone), qué sección, por qué y con qué evidencia.
5. Si nada aplica, registrar explícitamente: **"Fuentes de verdad revisadas: sin cambios requeridos."** El silencio no cuenta como revisión hecha.

## Proceso de promoción

```text
hallazgo (registrado en el momento) → clasificación → evidencia → auditoría → aprobación → actualización del destino correcto
```

No todo aprendizaje se promueve: una experiencia aislada, sin evidencia ni repetición, se registra pero no cambia ninguna fuente de verdad sin que el Auditor la proponga y el Gate 2 la apruebe.

**El Worker nunca edita directamente una fuente de verdad central** (el estándar de agentes, la navegación general, la arquitectura del repositorio) por hallazgos propios: los deja anotados en el progreso para que el Auditor los evalúe. Una tarea puede recibir una excepción escrita y acotada cuando su objeto explícito es construir o modificar esa estructura — la excepción se declara en el propio plan, nunca se infiere.

## Escalación a Skill

Cuando un procedimiento reusable **se repite** (no la primera vez que aparece, sino cuando ya se demostró que vuelve a ser necesario), el Auditor puede proponer (`PROPONER SKILL`) convertirlo en un Skill agnóstico, redactado para ser copiable a otro repositorio sin depender de nombres, rutas ni datos propios. Requiere aprobación en el Gate 2; lo crea el Orquestador.

## Formato del índice de aprendizajes

El índice de `03-aprendizaje-continuo/README.md` (o el archivo equivalente en cada repositorio) etiqueta cada mejora con una **etiqueta corta de categoría**, para que cualquier rol la escanee rápido y abra solo la que aplica a lo que está por hacer — nunca la carpeta completa por defecto (ver `00-indice.md`).

Un archivo migrado o promovido **no se borra**: queda en la carpeta y su estado pasa a "promovido" (o "rechazado"/"reemplazado") en el histórico correspondiente, con enlace a su destino final.
