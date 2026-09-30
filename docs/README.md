# docs — orquestador de esta carpeta

Este archivo ordena **solo `docs/`**. La fuente normativa de todo el repositorio sigue siendo [AGENTS.md](../AGENTS.md) — este archivo existe porque `AGENTS.md` deriva aquí para saber cómo moverse dentro de `docs/`.

## Mapa de las siete áreas

| Carpeta | Qué vive ahí |
|---|---|
| [00-estandar-agentes/](00-estandar-agentes/README.md) | Estándar reusable de agentes: roles, flujo Spec/SDD → Cierre, plantillas. Aplicable a cualquier repositorio. |
| [01-contexto-repositorio/](01-contexto-repositorio/README.md) | Configuración específica de este repositorio: propósito, fuentes de verdad, entorno Git/worktrees, pruebas, diseño. |
| [02-trabajo-activo/](02-trabajo-activo/README.md) | Plan / progreso / evidencia / auditoría de cada tarea real, activa o cerrada. |
| [03-aprendizaje-continuo/](03-aprendizaje-continuo/README.md) | Mejoras de trabajo, histórico de promociones, pendientes de promoción. |
| [04-flujos-de-negocio/](04-flujos-de-negocio/README.md) | Reglas de negocio permanentes del sistema, una por tema dueño. |
| [05-diseno-y-referencias/](05-diseno-y-referencias/README.md) | Sistema de diseño (`design.md`) y mockups de referencia. |
| [06-material-de-apoyo/](06-material-de-apoyo/README.md) | Material de referencia no normativo (conocimiento EVM/LPS, formatos, datos de prueba). |

## Conversación simple vs. trabajo con plan

- **Conversación simple** (pregunta, análisis, corrección puntual): no activa el flujo de roles. Basta leer el contexto del repositorio (`01-contexto-repositorio/`) y el flujo de negocio concreto que la pregunta toca.
- **Trabajo con plan** (cambio con fases, que toca más de un archivo o requiere aprobación explícita): activa el flujo de Objetivo a Cierre descrito en `00-estandar-agentes/04-flujo-sdd-y-planes.md`, con Orquestador, Planner, Worker y Auditor.

## Plan, progreso, evidencia y aprendizaje — no son lo mismo

| Documento | Contiene | Vive en |
|---|---|---|
| **Plan** | Spec/SDD, plan, Punch List, roles, registro de decisiones y mensaje de cierre — todo en un único archivo (el informe de auditoría vive aparte) | `02-trabajo-activo/01-planes/` |
| **Progreso** | Estado vivo: fase actual, avances, pendientes, commits/ramas, bloqueos, hallazgos y handoffs | `02-trabajo-activo/02-progreso/` |
| **Evidencia** | Punch List ejecutada con resultado por ítem, pruebas y enlace al artifact de checklist visual | `02-trabajo-activo/03-evidencia/` |
| **Auditoría** | Informe del Auditor de ese plan: verificación, cumplimiento y clasificación de hallazgos. Uno por plan, separado | `02-trabajo-activo/04-auditoria/` |
| **Aprendizaje** | Una lección sobre **cómo se trabaja** (método, herramientas, workarounds) — nunca una regla del sistema | `03-aprendizaje-continuo/` |

Una regla de negocio (cómo se calcula, valida o comporta algo del sistema) no vive en ninguno de los cuatro: va directo al flujo de negocio dueño, en `04-flujos-de-negocio/`.

## Ruta de lectura mínima

Ver `00-estandar-agentes/00-indice.md` para la tabla completa por rol y tipo de solicitud. Regla clave (D10, Gate 1 del 2026-09-27): el Orquestador, el Planner y el Auditor leen todos los flujos de negocio; el Worker lee solo los que el plan indica afectados por su parte. Ningún rol lee `docs/` completo de entrada.

## Verificación en vivo — Punch List de Mejoras

El checklist de cada lote de implementación no es una tabla estática en un `.md` — es este artifact interactivo, con guardado en la nube:

**https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd**

El archivo de evidencia correspondiente (`02-trabajo-activo/03-evidencia/`) enlaza a este artifact y registra el resultado en texto — los dos lugares coexisten.
