# Plantilla — Plan

> Un plan real vive en `02-trabajo-activo/01-planes/YYYY-MM-DD-<tema>.md`, con progreso, evidencia y auditoría homónimos en las carpetas hermanas (`02-progreso/`, `03-evidencia/`, `04-auditoria/`).

## Identificación y estado

Nombre del tema, fecha, estado — uno de estos 6 valores: `Propuesta` / `Planificando` / `Implementando` / `En auditoría` / `Pendiente del Responsable humano` / `Cerrada`.

Puertas (las lee el script del verificador; se escriben tal cual):

- Gate Spec: `pendiente` / `aprobado por <Responsable humano> (fecha)`
- Gate 1: `pendiente` / `aprobado por <Responsable humano> (fecha)`
- Gate 2: `pendiente` / `aprobado por <Responsable humano> (fecha)`

## Referencia al Spec aprobado

## Objetivo, alcance y no alcance

- Resultado esperado:
- Alcance:
- No alcance:
- Validación esperada:

## Entorno, repositorios, ramas y worktrees

## Skills aplicables

Skills de `.claude/skills/` (repositorio de documentación y de código) que aplican a este plan, y en qué tanda se usan. Si ninguno aplica: «ninguno aplica» con una frase de motivo.

## Fases y dependencias

## Equipo del plan

Por defecto: un Orquestador, un Planner, de 1 a 3 Workers de código (el Responsable humano decide cuántos y solo si el plan permite trabajar sin pisarse), un Documentador y un Worker git. Todos en Sonnet salvo el Worker git (Haiku), a menos que el Responsable humano indique otro modelo. El Analista del flujo no figura aquí: no participa en el flujo.

| Rol | Modelo | Sesión o tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|
| Orquestador | Sonnet | | `main` | N/A | |
| Planner | Sonnet | | `main` | N/A | |
| Worker 1 | Sonnet | | `local-worker-1` | | |
| Worker 2 | Sonnet | | `local-worker-2` | | |
| Worker 3 | Sonnet | | `local-worker-3` | | |
| Documentador | Sonnet | tanda final | `main` | N/A | |
| Worker git | Haiku | a pedido | opera sobre las demás | | |
| Auditor | Sonnet | | `main` | N/A | |

### Brief de cada Worker

El brief de cada tanda vive en la carpeta `-briefs/` del plan, con la plantilla `13-brief-de-tanda.md` (8 KB como máximo). Aquí solo se enlaza.

### Prompt del Auditor

<!-- Alcance a auditar, documentos a revisar, criterios de §6, formato del informe. -->

## Archivos / componentes afectados

## Punch List embebida

Formato de `05-punch-list.md`.

## Riesgos y bloqueos

## Registro de decisiones

Tabla fecha / decisión / quién.

## Enlaces a progreso y evidencia homónimos

## Libro de hallazgos

Los cuatro apartados siguientes son **el libro oficial de hallazgos del plan**. Un hallazgo se anota en el momento en que ocurre, no al cerrar. Los Workers no editan este archivo: dejan sus hallazgos en su resumen de cierre y el Orquestador los pasa aquí, fila por fila, a medida que llegan. Al final, el Documentador traslada cada fila a su destino. Si un apartado no tiene filas: «Ninguna».

Formato de cada fila:

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|

Estados: `Registrada` → `Trasladada` (con enlace y commit) · `Descartada` (con motivo) · `Pendiente de decisión` (con quién decide).

## Mejoras (de trabajo)

Cómo se trabaja: método, herramientas, trucos operativos. Destino: un archivo en `03-aprendizaje-continuo/`.

## Reglas de negocio acordadas en esta tarea

Cómo se comporta el sistema. Destino: directo en el flujo de negocio dueño, integrada en su estructura. Una regla que contradice algo escrito se consulta al Responsable humano antes de editar.

## Observaciones sobre la política

Fallos, huecos o contradicciones del proceso mismo (estándar, `AGENTS.md`, Skills). Destino: lista para el Auditor, que las clasifica; el Responsable humano decide en el Gate 2. Nadie las edita por su cuenta.

## Carpetas/archivos huérfanos

Se reportan al Responsable humano; no se borra nada por cuenta de un agente.

## Informe de Auditoría

Enlace al archivo homónimo en `02-trabajo-activo/04-auditoria/` (formato de `06-informe-auditoria.md`). El informe no se escribe dentro del plan.

## Mensaje de cierre

Formato de `09-cierre.md`.

## Elementos postergados propuestos para planes futuros
