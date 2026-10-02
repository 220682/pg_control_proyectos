# AGENTS.md

## Propósito y alcance

Este repositorio funciona como fuente documental y arquitectónica del sistema de control de proyectos. No es la aplicación web de producción; aquí se guarda la lógica de negocio, los flujos, los formatos, las decisiones de diseño y la documentación que luego se materializa en la app real.

Este archivo es la fuente normativa para todos los agentes de IA que trabajen en este repositorio. Debe leerse antes de modificar cualquier documento, flujo, especiﬁcación o diseño. La regla central es: no inventar convenciones, tecnologías, rutas ni reglas que no estén confirmadas por este repositorio o por la app hermana real.

## Stack y comandos

Este repositorio es documental: no tiene `package.json` ni scripts verificados de instalación, desarrollo, lint, type-check, pruebas, build ni migraciones. La aplicación real es el proyecto hermano `py_control_proyectos_web`; aquí no se desarrolla el runtime. El repositorio está publicado en GitHub y su rama principal es `main`. Todo comando no confirmado se considera "por confirmar" y no se inventa. No se ejecutan migraciones SQL ni cambios destructivos sin revisión explícita del contexto real.

## Estructura del repositorio

- [README.md](README.md): resumen general del repositorio.
- [docs](docs): documentación operativa, flujos y mejoras — ver [docs/README.md](docs/README.md) para el mapa completo de las siete áreas.
- [scripts](scripts/README.md): herramientas locales (medición de sesiones, verificación de referencias, verificador de acciones).
- [docs/00-estandar-agentes](docs/00-estandar-agentes): estándar reusable de agentes (roles, flujo Spec/SDD → Cierre, plantillas).
- [docs/01-contexto-repositorio](docs/01-contexto-repositorio): configuración específica de este repositorio (propósito, fuentes de verdad, entorno Git/worktrees, pruebas, diseño).
- [docs/02-trabajo-activo](docs/02-trabajo-activo): planes, progreso, evidencia, auditoría y eficiencia de cada tarea real — incluye lo que hacen los Workers (código, pantallas, consultas, migraciones) y las tareas del flujo de Orquestador con Punch List.
- [docs/03-aprendizaje-continuo](docs/03-aprendizaje-continuo): solo aprendizajes sobre cómo se trabaja (método, herramientas, workarounds), extraídos de un plan. No contiene reglas de negocio del sistema.
- [docs/04-flujos-de-negocio](docs/04-flujos-de-negocio): conjunto principal de especificaciones por flujo, fuente de verdad de las reglas funcionales.
- [docs/05-diseno-y-referencias](docs/05-diseno-y-referencias): sistema de diseño (`design.md`) y mockups de referencia.
- [docs/06-material-de-apoyo](docs/06-material-de-apoyo): material de referencia no normativo — incluye `conocimiento/` (fundamentos EVM/LPS), `Informacion para pruebas/`, `Formatos/`, `Dashboard ejemplo/` e `Imagenes para fronted/`.

## Arquitectura y fuentes de verdad

La arquitectura funcional, el flujo principal documentado (presupuesto, cronograma, Plan Maestro, plan semanal, RDT, PR, dashboard) y el modelo de datos con la fuente de verdad de cada pieza están en [docs/01-contexto-repositorio/08-arquitectura-funcional-y-datos.md](docs/01-contexto-repositorio/08-arquitectura-funcional-y-datos.md). Regla central: el sistema no mezcla lo planificado, lo ejecutado, lo estimado, lo consolidado y la vista ejecutiva.

## Flujos principales

Los 21 flujos de negocio, con su índice, viven en [docs/04-flujos-de-negocio/README.md](docs/04-flujos-de-negocio/README.md); son la fuente de verdad de las reglas funcionales. Los de uso más frecuente: [14 accesos y restricciones](docs/04-flujos-de-negocio/14-accesos-y-restricciones.md), [16 paneles](docs/04-flujos-de-negocio/16-paneles.md), [18 control de avance](docs/04-flujos-de-negocio/18-control-avance.md) y [20 plan maestro](docs/04-flujos-de-negocio/20-plan-maestro.md).

## Políticas de coherencia y trazabilidad

Políticas de este repositorio (Victor, 2026-09-28). El texto completo está en [docs/01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md](docs/01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md) § Políticas de coherencia y trazabilidad.

- **La matriz de permisos es la base de los accesos.** El artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT) es la base del flujo 14, ligado al flujo 16 (Paneles). Toda interfaz, acción, permiso o acceso nuevo, modificado o eliminado actualiza el artefacto y el flujo 14 en la misma tarea.
- **Un Spec o plan que entra en conflicto con lo escrito se implementa en todos los afectados.** Se listan y actualizan todos los flujos y documentos afectados, se consulta a Victor cada contradicción antes de editar un flujo, y no se deja nada suelto: el Auditor verifica la trazabilidad antes del Gate 2.

## Reglas de interfaz

Como este repositorio no contiene la implementación visual en ejecución, estas reglas se toman como directrices documentadas y no como inventario de componentes reales en código.

- Mantener consistencia visual con el sistema ya descrito en la documentación.
- No crear una segunda interfaz sin referirse primero a los flujos y pantallas existentes.
- Priorizar reutilización sobre nuevas construcciones aisladas.
- Mantener separación entre paneles de trabajo, estado operativo y resúmenes ejecutivos.
- Usar scroll horizontal en tablas largas sin perder contexto.
- No convertir un paquete operativo en una partida contractual sin validación.
- No declarar avances reales sin una fuente documentada de ejecución validada.
- Si no existe un componente real en el repo, no inventar su nombre ni su comportamiento.

## Reglas de backend y API

Cuando se trabaje con backend o contratos en repositorios derivados o en la app real:

- Validar siempre en servidor.
- Verificar permisos por servicio o proyecto.
- Validar pertenencia del usuario al contexto antes de ejecutar acciones.
- Validar entrada y límites de negocio antes de escribir.
- Manejar errores de forma explícita.
- No confiar solo en datos enviados por el navegador.
- No exponer secretos ni tokens.
- Documentar cambios de contrato y su impacto.

## Base de datos y migraciones

- No borrar ni renombrar columnas sin plan de migración.
- No ejecutar migraciones destructivas sin autorización expresa.
- Revisar datos existentes antes de cambiar restricciones o integridad referencial.
- Mantener consistencia entre WBS, cronograma, PR y dashboard.
- Si se añade un campo nuevo, documentar su uso y origen.
- No convertir estimaciones en costo real sin fuente validada.

## Autenticación y permisos

La documentación indica que existen roles, permisos y flujo de acceso por proyecto y por rol. Algunos puntos clave detectados:

- La app real no está en este repositorio, pero el diseño y la documentación sí reconocen roles de administración, proyecto y área.
- El administrador no debe ser el único punto de gestión del sistema; se debe respetar la lógica de roles del proyecto.
- El acceso debe limitarse por servicio, proyecto y flujo de trabajo.
- La validación de permisos debe hacerse al nivel de negocio, no solo de frontend.

## Pruebas y validación

No se encontraron pruebas ejecutables en este repositorio. Por tanto:

- Las validaciones deben realizarse con evidencia real del repositorio o del entorno del proyecto relacionado.
- Si un cambio afecta documentos de flujo, se debe verificar que la documentación siga siendo coherente.
- Si el repositorio derivado o app real se modifica, deben ejecutarse sus validaciones específicas.
- No se afirmará que una tarea está terminada sin evidencia de verificación.

## Frase de inicio de sesión

Hay dos frases de activación distintas — no se mezclan:

- **"inicia sesión en control de proyectos"** (o equivalente claro): flujo normal. No preguntar de cero. Leer [docs/README.md](docs/README.md) — ese archivo es el orquestador de `docs/` y dice exactamente qué leer (los archivos de `docs/02-trabajo-activo/01-planes/` que sigan abiertos para saber en qué quedó el proyecto, y el **índice** de `docs/04-flujos-de-negocio/`). Un flujo concreto se abre solo cuando la tarea lo nombre; para decidir si aplica, basta su línea `Lee si:`. Responder con los pendientes de esas sesiones abiertas y el contexto general del sistema.
- **"vamos a trabajar en un plan con agente orquestador"** (o equivalente claro): flujo de Orquestador. Ver [Flujo con Orquestador](#flujo-con-orquestador) más abajo.

## Frase de cierre de sesión

Si el usuario dice **"cierra sesión en control de proyectos"**: actualizar el o los archivos de `docs/02-trabajo-activo/01-planes/` tocados en la sesión (avance, checklist, apartados "Mejoras (de trabajo)", "Reglas de negocio acordadas en esta tarea" y "Carpetas/archivos huérfanos" — llenados en el momento en que ocurrió cada hallazgo, no recién ahora) — tanto si es una tarea del flujo de Orquestador (Registro de decisiones, resultados, cierre) como si es un lote de trabajo tradicional. Mejoras de trabajo con contenido → extraer a un archivo en `docs/03-aprendizaje-continuo/`. Reglas de negocio con contenido → integrarlas directo en el Flujo de trabajo correspondiente (`docs/04-flujos-de-negocio/`), nunca como nota aparte. Huérfanos detectados → reportados a Victor, sin borrar nada (ver `docs/README.md`). No crear ninguna memoria de sesión aparte. Confirmar qué se guardó y listar los pendientes para la siguiente sesión.

## Flujo con Orquestador

Cuando el usuario dice una frase equivalente a "vamos a trabajar en un plan con agente orquestador", aplica la política de [docs/00-estandar-agentes/02-roles-y-delegacion.md](docs/00-estandar-agentes/02-roles-y-delegacion.md): el Orquestador es el punto único de contacto operativo entre Victor y los demás agentes (Planner, Worker, Auditor y Analista del flujo); coordina objetivo, plan, aprobación, implementación, auditoría y cierre, y no aprueba en nombre de Victor ni hace merge, push, commit, PR, ni crea rama, worktree o infraestructura sin autorización explícita.

**Primera lectura obligatoria de este flujo:** [docs/00-estandar-agentes/04-flujo-sdd-y-planes.md](docs/00-estandar-agentes/04-flujo-sdd-y-planes.md), la fuente normativa de los 18 pasos, con los dos Gates y el cierre, y su versión visual e interactiva, el artefacto «Flujo SDD a Cierre» (https://claude.ai/artifact/8Wq3QsjFfiNs8YSs5T1gjd). Se trabaja en terminal con un Orquestador y subagentes (sin chats con nombre); no se usa Opus (ver [docs/01-contexto-repositorio/09-medicion-y-modelos.md](docs/01-contexto-repositorio/09-medicion-y-modelos.md)). El Orquestador mide sus sesiones y releva su propia sesión según [docs/00-estandar-agentes/08-medicion-y-relevo.md](docs/00-estandar-agentes/08-medicion-y-relevo.md), y antes de acciones irreversibles consulta al verificador ([07-verificador-de-acciones.md](docs/00-estandar-agentes/07-verificador-de-acciones.md), borrador por probar). Usar además el Skill `seguir-flujo-de-planes` (en `.claude/skills/`) al activar el flujo y antes de declarar cerrado un plan, y revisar los Skills disponibles al empezar (ver [docs/00-estandar-agentes/03-sesiones-contexto-y-handoff.md](docs/00-estandar-agentes/03-sesiones-contexto-y-handoff.md)).

Las tareas ejecutadas con este flujo viven en [docs/02-trabajo-activo/01-planes/](docs/02-trabajo-activo/01-planes/), no en `docs/03-aprendizaje-continuo/`; el informe del Auditor de cada plan vive aparte, en [docs/02-trabajo-activo/04-auditoria/](docs/02-trabajo-activo/04-auditoria/). Antes de empezar, leer también [docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md](docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md) y [docs/00-estandar-agentes/03-sesiones-contexto-y-handoff.md](docs/00-estandar-agentes/03-sesiones-contexto-y-handoff.md).

### Tareas de implementación, Mejoras continuas y Reglas de negocio

Cuatro categorías distintas, no menos:

- **Tarea de implementación** = lo que hace un Worker: código, pantallas, consultas, migraciones — trabajo operativo de construcción. Vive en `docs/02-trabajo-activo/01-planes/`. Registra QUÉ se implementó, no la regla permanente.
- **Mejora de trabajo / mejora continua** = un aprendizaje sobre **cómo trabajamos** (método, herramientas, workarounds operativos) — no una regla del sistema. Vive en `docs/03-aprendizaje-continuo/` como destino final.
- **Regla de negocio** = una regla del sistema (cómo se calcula, valida o comporta algo). **No se guarda en un archivo aparte** — va directo al `Flujo de trabajo` correspondiente, integrada en su estructura (no pegada al final). Si contradice una regla ya escrita, se modifica lo existente con lo acordado con Victor durante la tarea.
- **Observación sobre la política** = un fallo, hueco o contradicción del proceso mismo (estándar, `AGENTS.md`, Skills). Se anota en el apartado «Observaciones sobre la política» del plan; nadie la edita por su cuenta: el Auditor la clasifica y Victor decide en el Gate 2.

**Cómo trasladar:** toda tarea de implementación tiene cuatro apartados obligatorios, que forman el libro de hallazgos del plan (`## Mejoras (de trabajo)`, `## Reglas de negocio acordadas en esta tarea`, `## Observaciones sobre la política`, `## Carpetas/archivos huérfanos` — ver `docs/00-estandar-agentes/06-plantillas/02-plan.md`) que **se llenan en el momento en que ocurre cada hallazgo**, no al cerrar. Si una regla nueva contradice una ya escrita en un flujo, el agente pregunta a Victor ahí mismo, valida la respuesta, la escribe en el apartado y recién entonces continúa (repite el ciclo si no queda resuelto). El agente no edita una fuente de verdad por su cuenta. Al cerrar, el Documentador (ver `docs/00-estandar-agentes/02-roles-y-delegacion.md`) traslada cada entrada ya registrada a su destino: mejoras de trabajo a un archivo nuevo en `docs/03-aprendizaje-continuo/`, reglas de negocio directo al Flujo correspondiente, huérfanos reportados a Victor (en `pg_control_proyectos` y `py_control_proyectos_web`, sin borrar nada por su cuenta). El Auditor verifica que esto se haya hecho antes de cerrar la tarea (ver `docs/00-estandar-agentes/02-roles-y-delegacion.md` § Auditor). Ver `docs/README.md` para el detalle del ciclo.

## Flujo de trabajo del agente

**Verificar antes de afirmar, siempre.** Ante cualquier dato técnico dudoso (entorno, rama, si un recurso existe, si algo ya se pusheó, nombre real de algo que Victor configuró) — si hay una herramienta que puede comprobarlo directamente, se usa esa herramienta primero, nunca se infiere de un campo relacionado pero no exacto. Si no hay forma de verificarlo con herramientas, se pregunta a Victor explícitamente. Una vez que Victor corrige algo, esa corrección no se vuelve a cuestionar con el mismo dato débil que ya falló (ver `docs/03-aprendizaje-continuo/2026-09-23-verificar-antes-de-afirmar.md`, promovido a `docs/00-estandar-agentes/01-principios-y-seguridad.md`).

1. Leer este archivo y la especificación del flujo solicitado.
2. Inspeccionar los archivos relacionados antes de modificar.
3. Identificar si el cambio pertenece a documentación, diseño o implementación real.
4. Buscar referencias reutilizables antes de crear nuevas estructuras.
5. Presentar un plan para cambios medianos o grandes.
6. Esperar aprobación cuando el cambio sea arquitectónico, destructivo o de alto riesgo.
7. Implementar en fases pequeñas.
8. Validar cada fase con evidencia.
9. Revisar el diff antes de cerrar la tarea.
10. Reportar archivos tocados, validaciones, riesgos y pendientes.

## Límites y archivos prohibidos

El agente nunca debe:

- Leer, copiar ni mostrar secretos reales.
- Modificar variables de entorno reales.
- Publicar credenciales o tokens.
- Borrar archivos sin aprobación explícita del usuario.
- Ejecutar migraciones destructivas sin revisión previa.
- Crear duplicados de entidades o módulos sin justificación técnica.
- Declarar una tarea terminada sin pruebas o sin explicar la falta de evidencia.
- Convertir una estimación en costo real sin validación.
- Separar el proyecto por “capas” ficticias que no existan en la documentación.

## Git y entrega

- El repositorio fue inicializado y publicado a GitHub.
- Por defecto se trabaja directo en `main` (así se ha trabajado hasta ahora). Se usa una rama de trabajo solo cuando Victor lo pide explícitamente para ese cambio.
- El diff debe ser limpio y comprensible.
- No se deben hacer cambios de infraestructura ni de secretos sin aprobación.
- Los archivos de documentación funcional deben conservarse salvo acuerdo explícito del usuario.

## Checklist de finalización

Antes de cerrar una tarea, revisar:

- [ ] Se leyó este archivo.
- [ ] Se inspeccionó el contexto correcto del repositorio.
- [ ] No se inventaron tecnologías ni comandos no verificados.
- [ ] El cambio respeta las fuentes de verdad documentadas.
- [ ] No se eliminaron archivos sin aprobación explícita.
- [ ] Se ejecutó validación o se documentó la falta de evidencia.
- [ ] El diff es entendible y limitado al alcance pedido.
- [ ] La documentación relevante sigue coherente.

## Inventario de fuentes de instrucciones

- **Canónica:** este archivo. **Complementarias:** [README.md](README.md), [docs/README.md](docs/README.md) (orquestador de `docs/`) y [docs/04-flujos-de-negocio/README.md](docs/04-flujos-de-negocio/README.md).
- Los archivos de sesión y de memoria de continuidad son contexto operativo, no norma: no reemplazan la fuente normativa.
- No se detectaron duplicados ni contradicciones directas entre instrucciones formales. Hay una diferencia operacional clara entre este repositorio documental y la app real, que vive fuera del workspace.

## Nota importante

Este repositorio no es la aplicación web de producción; es la base documental y conceptual que alimenta el sistema real. El agente debe trabajar con esta limitación explícita y no inventar implementación ni runtime que no estén confirmados por este repositorio o por la app hermana.
