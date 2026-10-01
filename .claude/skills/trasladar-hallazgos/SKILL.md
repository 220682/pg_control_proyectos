---
name: trasladar-hallazgos
description: Traslada a su destino final los hallazgos que un plan fue registrando (reglas de negocio, mejoras de trabajo, observaciones sobre la política, archivos huérfanos), sin editar por su cuenta las fuentes centrales y sin dejar nada suelto. Úsalo en la tanda final de documentación de un plan.
---

# Trasladar los hallazgos de un plan

Aplica a cualquier plan que registre sus hallazgos en un libro con estados (`Registrada`, `Trasladada`, `Descartada`, `Pendiente de decisión`) y que tenga un documento de flujo por cada tema del negocio.

## Antes de empezar

1. Lee tu brief, los apartados del libro de hallazgos del plan, la tabla de cambios a flujos que el responsable humano aprobó en la primera aprobación y los resúmenes de cierre de todas las tandas.
2. Lista los Skills disponibles y anota «Skills revisados».

## Pasos, en este orden

1. **Inventario.** Lista las filas en estado `Registrada` y cotéjalas con los resúmenes de cierre de las tandas: si un hallazgo está en un resumen y no en el libro, agrégalo como fila nueva y avisa al orquestador.
2. **Reglas de negocio.** Intégralas en el flujo dueño, dentro de su estructura, nunca pegadas al final ni en un archivo aparte, aplicando la tabla aprobada. Si una regla contradice algo escrito y no está en esa tabla, **no edites**: devuélvela al orquestador para consultarla al responsable humano y deja la fila como `Pendiente de decisión`.
3. **Mejoras de trabajo.** Un archivo por mejora en la carpeta de aprendizaje continuo, con la plantilla de aprendizaje y su etiqueta de categoría, y una línea en el índice de esa carpeta. Marca las que ya se repitieron como candidatas a Skill.
4. **Observaciones sobre la política.** No edites el estándar, la norma raíz ni los Skills. Reúnelas en una lista para el auditor, con el documento afectado y la propuesta.
5. **Archivos huérfanos.** Reporta cada uno al responsable humano. No borres nada.
6. **Derivados.** Actualiza los artefactos derivados de las reglas que cambiaste y los índices de las carpetas que tocaste.
7. **Referencias.** Ejecuta la verificación de referencias del repositorio sobre las carpetas tocadas: ningún archivo sin enlazar desde su índice y ningún enlace roto.
8. **Cierre de filas.** Marca cada fila `Trasladada` (con enlace al destino y commit), `Descartada` (con motivo) o `Pendiente de decisión` (con quién decide).

## Entrega

Tu resumen de cierre de tanda, con la lista de lo pendiente de política, los huérfanos y las preguntas abiertas. Commits por tema, con `git add` archivo por archivo y verificación de la rama con `git branch --contains`.

## Reglas

- Sin credenciales en ningún archivo ni mensaje.
- Cambios puntuales por fila: nunca reemplazos masivos sobre el plan ni sobre la evidencia.
- Si algo no se pudo verificar, queda `Pendiente de decisión` con la limitación escrita.
- No marques `Trasladada` sin haber abierto el destino y comprobado que el texto está.
