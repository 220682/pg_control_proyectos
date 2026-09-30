---
name: seguir-flujo-de-planes
description: Recorre un plan de trabajo con roles separados (Orquestador, Planner, Worker, Auditor) y dos aprobaciones del responsable humano, y verifica cada puerta antes de avanzar, sobre todo antes de declarar cerrado un plan. Úsalo al activar el flujo con Orquestador y otra vez antes de escribir el mensaje de cierre.
---

# Seguir el flujo de planes

Aplica a cualquier repositorio que trabaje con un documento normativo del flujo (Objetivo, Spec, Plan, Implementación, Auditoría, Cierre), con roles separados y dos aprobaciones del responsable humano.

## Al activar el flujo

1. Lee completos, no de memoria, el documento normativo del flujo y el de roles de tu repositorio. Si existe una versión visual o interactiva del flujo, ábrela. Si difiere del documento, manda el documento.
2. Lista los Skills disponibles en los repositorios donde vas a trabajar y usa los que apliquen.
3. Di en qué paso del flujo estás, qué puerta sigue y qué necesita el responsable humano de ti.

## Puertas: no avances sin esto

- **Spec aprobado** por el responsable antes de que nadie planifique.
- **Plan y lista de ítems aprobados** en la primera aprobación, junto con los cambios a las reglas ya escritas (una tabla de «dice hoy» y «pasaría a decir»). Esa aprobación es también donde se pide autorización para crear ramas y carpetas de trabajo; sin ella, no se crean.
- **Implementación solo por Workers**, cada uno en su rama. El Orquestador no implementa. Nadie hace merge antes de la segunda aprobación.
- **Auditoría emitida**: el informe existe como archivo propio, confirma que los commits están en la rama del Worker y trae la clasificación de hallazgos (aplicar ahora, proponer al responsable, no promover, proponer Skill). Sin informe emitido no se pide la segunda aprobación. Si falta la clasificación, se devuelve al Auditor.
- **Segunda aprobación**: pide en ella, de forma explícita, la autorización para subir el código.

## Antes de declarar cerrado un plan

Verifica cada punto con un comando o una lectura, no por suposición:

1. El merge del código está hecho, después de la segunda aprobación.
2. En **cada repositorio** que tocó el plan: `git status` sin cambios propios pendientes y `git rev-list --left-right --count origin/<rama>...<rama>` da `0 0`.
3. Las mejoras de política y cambios a fuentes de verdad aprobados están aplicados.
4. Los Skills aprobados están creados y son agnósticos.
5. Las reglas de negocio y mejoras registradas durante el plan están en su destino final; los archivos huérfanos se reportaron sin borrar nada.
6. El mensaje de cierre está dentro del plan, dice lo que de verdad ocurrió en los puntos 1 a 5, y está subido.
7. Solo entonces escribe «cerrado». Si falta algo, dile al responsable exactamente qué falta.

## Cómo hablar con el responsable humano

- Lenguaje simple, sin códigos internos de ítems ni siglas.
- Una decisión por pregunta, con un ejemplo concreto y una recomendación.
- Di qué verificaste y qué no pudiste verificar.

## Reglas

- El Orquestador no aprueba por el responsable, no hace merge ni sube código, y no crea ramas ni carpetas de trabajo sin autorización explícita.
- No borres archivos ni reescribas historial sin aprobación.
- Si te saltaste un paso, dilo y corrígelo; no lo ocultes.
