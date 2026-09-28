# PG Control de Proyectos

Repositorio documental y de arquitectura para el control de proyectos en obra, con foco en la integración entre presupuesto, cronograma, ejecución, costos, indicadores y dashboard.

## Visión general

Este proyecto reúne la base conceptual, metodológica y operativa para gestionar el avance del proyecto sin mezclar conceptos clave. La intención no es trabajar con un solo archivo aislado, sino con una cadena completa que conecta:

- alcance y presupuesto,
- cronograma y programación,
- relación WBS ↔ cronograma,
- Plan Maestro,
- Plan semanal / 3WLA,
- RDT,
- PR,
- dashboard ejecutivo.

La diferencia central del sistema es que separa claramente:

- lo planificado,
- lo ejecutado,
- lo estimado,
- lo consolidado,
- y la vista ejecutiva.

## Objetivo del repositorio

Este repositorio sirve como base de trabajo para:

- comprender la lógica del control de proyectos,
- definir cómo se genera el avance y el costo programado,
- distinguir entre ejecución real y estimación provisional,
- documentar flujos de trabajo y decisiones de diseño,
- preparar la implementación en la aplicación web real.

## Qué contiene

El contenido del repositorio está organizado en varias áreas temáticas:

- documentación de flujos y procesos,
- fundamentos teóricos de EVM y LPS,
- ejemplos de dashboard, cronograma y trazabilidad,
- formularios, plantillas y formatos del proyecto,
- archivos de prueba y datos de evaluación,
- evidencia de ejecución y reportes diarios,
- memoria histórica del proyecto,
- políticas operativas de trabajo con Orquestador/Planner/Worker/Auditor.

## Estructura principal

Ver [docs/README.md](docs/README.md) para el mapa completo de las siete áreas de `docs/`. Resumen:

- [docs/04-flujos-de-negocio](docs/04-flujos-de-negocio): flujo operacional y de negocio principal.
- [docs/02-trabajo-activo](docs/02-trabajo-activo): lo que hacen los Workers — código, pantallas, consultas, migraciones —, tanto planes únicos del flujo de Orquestador como lotes con checklist de verificación (Punch List).
- [docs/03-aprendizaje-continuo](docs/03-aprendizaje-continuo): solo aprendizajes sobre cómo se trabaja (método, herramientas, workarounds) extraídos de un plan. No contiene reglas de negocio del sistema — esas van directo al `Flujo de trabajo` correspondiente.
- [docs/00-estandar-agentes](docs/00-estandar-agentes): estándar reusable de trabajo con Orquestador (roles, convenciones de entorno/ramas/worktrees, gestión de sesiones) — define cómo se trabaja, no de qué trata el sistema.
- [docs/06-material-de-apoyo/conocimiento](docs/06-material-de-apoyo/conocimiento): bases conceptuales de control de proyectos, EVM y LPS.
- [docs/06-material-de-apoyo/Informacion para pruebas](docs/06-material-de-apoyo/Informacion%20para%20pruebas): datos, RDO, archivos de apoyo y evaluación.
- [docs/06-material-de-apoyo/Formatos](docs/06-material-de-apoyo/Formatos): formatos del proyecto.
- [docs/00-estandar-agentes/06-plantillas](docs/00-estandar-agentes/06-plantillas): plantillas operativas y de ejemplo.
- [docs/06-material-de-apoyo/Dashboard ejemplo](docs/06-material-de-apoyo/Dashboard%20ejemplo): referencias visuales del dashboard.
- [README.md](README.md): mapa general del repositorio.

## Regla de diseño central

El sistema se construye por capas y cada una tiene una responsabilidad distinta.

1. Presupuesto y alcance definen la línea base del trabajo.
2. El cronograma define la secuencia y la duración.
3. La relación WBS ↔ cronograma permite distribuir el trabajo en el tiempo.
4. El Plan Maestro genera el valor planificado por semana.
5. El plan semanal/3WLA define el compromiso operativo de corto plazo.
6. El RDT mide la ejecución real.
7. El PR consolida plan y ejecución.
8. El dashboard presenta la situación del proyecto de forma ejecutiva.

## Regla clave del negocio

El proyecto no debe mezclar:

- costo real medido,
- costo estimado,
- avance programado,
- avance ejecutado,
- y resumen financiero o ejecutivo.

Esto es especialmente importante para materiales y costos no validados: si no hay control real, deben permanecer como estimación provisional y no como costo real.

## Fuentes de verdad

Cada documento tiene un rol distinto; no se duplican reglas entre ellos:

- **[AGENTS.md](AGENTS.md)** — norma raíz para agentes de IA: qué pueden y no pueden hacer, cómo deben trabajar.
- **[README.md](README.md)** (este archivo) — visión del sistema, arquitectura general y reglas de alto nivel.
- **[docs/README.md](docs/README.md)** — manual de trabajo dentro de `docs/`: qué leer, cómo se organiza cada carpeta, ciclos de vida.
- **[docs/04-flujos-de-negocio/NN-*.md](docs/04-flujos-de-negocio)** — reglas de negocio detalladas, una por flujo.

Ante una contradicción entre estos documentos, se resuelve consultando a Victor — no se asume cuál prevalece. Excepción: en el flujo de trabajo con agente Orquestador, manda el diagrama normativo del flujo (`docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`), no se consulta a Victor para esa contradicción puntual.

## Ciclo de mejora continua

Cuando un plan de `docs/02-trabajo-activo/01-planes/` genera un hallazgo, en el flujo con Worker (ver `docs/00-estandar-agentes/02-roles-y-delegacion.md`) el propio Worker lo escribe directo al consolidar su tarea, sin pedir autorización previa para esa escritura puntual en el plan/progreso. Lo que sí sigue necesitando autorización explícita de Victor es la promoción final a una fuente de verdad central — el agente no edita una fuente de verdad por su cuenta sin ese paso:

- Un aprendizaje sobre **cómo se trabaja** (método, herramientas) se promueve a `docs/03-aprendizaje-continuo/`.
- Una **regla de negocio** (cómo se calcula/valida/comporta algo del sistema) se promueve directo e integrada al `Flujo de trabajo` que corresponda (`docs/04-flujos-de-negocio/`) — nunca a un archivo aparte.

Ver `docs/README.md` para el detalle y ejemplos.

- **`README.md`** (este archivo) se actualiza solo cuando hay cambios que alteran contenido ya existente aquí (visión, estructura, arquitectura) — no en cada sesión ni por cada mejora menor.
- **`AGENTS.md`** se actualiza cuando cambia cómo deben trabajar los agentes (reglas, límites, flujo de Orquestador).
- **`docs/04-flujos-de-negocio/NN-*.md`** se actualiza cuando cambia una regla de negocio de ese flujo.

## Estado del repositorio

Este repositorio está en fase de documentación y diseño conceptual. No es un runtime de aplicación ni un proyecto de frontend ejecutable en esta carpeta; es la fuente normativa y de referencia para la definición operativa del sistema y para la app real que funciona en un repositorio hermano.

## Documentación recomendada para empezar

- [README.md](README.md)
- [docs/README.md](docs/README.md)
- [docs/04-flujos-de-negocio/README.md](docs/04-flujos-de-negocio/README.md)
- [docs/04-flujos-de-negocio/18-control-avance.md](docs/04-flujos-de-negocio/18-control-avance.md)

## Nota final

La intención de este repositorio es dejar una base clara para el diseño, la operación y la continuidad del proyecto, evitando inventar reglas, mezclas conceptuales o convenciones sin respaldo documental.
