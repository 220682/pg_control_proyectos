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
- memoria histórica del proyecto.

## Estructura principal

- [docs/Flujos de trabajo](docs/Flujos%20de%20trabajo): flujo operacional y de negocio principal.
- [docs/Mejoras continuas](docs/Mejoras%20continuas): mejoras y evoluciones documentadas.
- [conocimiento](conocimiento): bases conceptuales de control de proyectos, EVM y LPS.
- [Sistema hibrido](Sistema%20hibrido): diseño híbrido, especificaciones y archivos de referencia.
- [Informacion para pruebas](Informacion%20para%20pruebas): datos, RDO, archivos de apoyo y evaluación.
- [RDTs movimiento de tierra, instlacion de bancoductos](RDTs%20movimiento%20de%20tierra,%20instlacion%20de%20bancoductos): evidencia física y reportes de avance.
- [Formatos](Formatos): formatos del proyecto.
- [plantillas](plantillas): plantillas operativas y de ejemplo.
- [Dashboard ejemplo](Dashboard%20ejemplo): referencias visuales del dashboard.
- [memoria.md](memoria.md): historial y continuidad de decisiones.
- [control_de_proyectos.txt](control_de_proyectos.txt): resumen funcional del sistema.
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

## Estado del repositorio

Este repositorio está en fase de documentación y diseño conceptual. No es un runtime de aplicación ni un proyecto de frontend ejecutable en esta carpeta; es la fuente normativa y de referencia para la definición operativa del sistema y para la app real que funciona en un repositorio hermano.

## Documentación recomendada para empezar

- [README.md](README.md)
- [control_de_proyectos.txt](control_de_proyectos.txt)
- [memoria.md](memoria.md)
- [docs/Flujos de trabajo/README.md](docs/Flujos%20de%20trabajo/README.md)
- [docs/Flujos de trabajo/18-control-avance.md](docs/Flujos%20de%20trabajo/18-control-avance.md)

## Nota final

La intención de este repositorio es dejar una base clara para el diseño, la operación y la continuidad del proyecto, evitando inventar reglas, mezclas conceptuales o convenciones sin respaldo documental.
