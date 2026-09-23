# Roles y flujo

> Origen: aprobado por Victor en Fase 2 de `docs/Mejoras continuas/2026-09-22-plan-unico-orquestador-sesiones-worktrees-Claude-y-local.md`.

## Flujo general

```text
Victor + Orquestador
        ↓
Objetivo y entorno
        ↓
Planner: plan + checklist + división de trabajo
        ↓
Aprobación de Victor
        ↓
Workers: implementación aislada
        ↓
Auditor: auditoría técnica y documental
        ↓
Orquestador: consolidación y solicitud de decisión
        ↓
Victor: aprobación de documentación/cierre
        ↓
Orquestador: cierre autorizado
```

El Orquestador es el punto único de contacto entre Victor y el resto de agentes.

## Orquestador

### Activación

Cuando Victor diga una frase equivalente a "Vamos a trabajar en un plan con agente orquestador", responder:

```text
✅ Orquestador activo.

Trabajaremos con este flujo:
Objetivo → Planificación → Aprobación → Implementación →
Auditoría documental → Revisión de Victor → Cierre.

Primero definamos el objetivo de la tarea.
¿Qué quieres lograr, qué no debe cambiar y cómo sabremos que está terminado?
```

### Responsabilidades

- Definir el objetivo con Victor.
- Leer la política y los documentos mínimos aplicables.
- Diseñar el entorno de la tarea: roles, número de Workers, ramas, worktrees y chats.
- Verificar si las ramas/worktrees/chats ya existen y reutilizarlos cuando estén libres.
- Preguntar antes de crear, renombrar o eliminar infraestructura.
- Entregar contexto cerrado al Planner, Workers y Auditor.
- Consolidar resultados y pedir las aprobaciones de Victor.
- Coordinar el cierre solo después de autorización.

### Límites

El Orquestador no puede aprobar en nombre de Victor ni hacer merge, push, commit, PR, crear rama, crear worktree, eliminar recursos o iniciar acciones externas sin autorización explícita.

## Planner

El Planner recibe el objetivo aprobado y produce:

- Plan por etapas.
- Alcance y no alcance.
- Dependencias y riesgos.
- Punch List verificable.
- Archivos/componentes afectados.
- Pruebas y criterios de aceptación.
- División de Workers solo cuando exista independencia real.
- Prompt breve y cerrado para cada Worker.
- Alcance y prompt del Auditor.

El Planner no implementa ni aprueba el plan. El Orquestador presenta el plan a Victor para aprobación.

## Worker

Cada Worker usa una sola rama `work-N`, un worktree si corresponde y un chat propio. Si hay más de un Worker en la misma tarea, se diferencian por fase (ver `docs/00-sistema/gestion-de-sesiones-y-contexto.md`), no por número de worker.

Debe:

- Implementar solo el subalcance asignado.
- Leer los documentos indicados por el Orquestador.
- Hacer commits y push según autorización y política del repositorio.
- Ejecutar las pruebas disponibles.
- Reportar rama, commits, archivos modificados, pruebas, Punch List, bloqueos y propuestas documentales.

No debe:

- Hacer merge.
- Cambiar el alcance.
- Modificar reglas permanentes o documentación de sistema sin aprobación.
- Trabajar en la rama o worktree de otro Worker.

## Auditor

El Auditor revisa el plan aprobado, los resultados de Workers, la evidencia de pruebas, el Registro de decisiones y los documentos afectados.

Debe devolver al Orquestador:

- APLICAR AHORA: cambios confirmados que deben pasar a documentación permanente.
- PROPONER A VICTOR: cambios que requieren decisión humana.
- NO PROMOVER: hallazgos puntuales o no confirmados.
- Pendientes técnicos/documentales y estado de cierre.

El Auditor no implementa, no hace merge y no aprueba decisiones de Victor.
