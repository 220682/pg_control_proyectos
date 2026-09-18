# AGENTS.md

## Propósito y alcance

Este repositorio funciona como fuente documental y arquitectónica del sistema de control de proyectos. No es la aplicación web de producción; aquí se guarda la lógica de negocio, los flujos, los formatos, las decisiones de diseño y la documentación que luego se materializa en la app real.

Este archivo es la fuente normativa para todos los agentes de IA que trabajen en este repositorio. Debe leerse antes de modificar cualquier documento, flujo, especiﬁcación o diseño. La regla central es: no inventar convenciones, tecnologías, rutas ni reglas que no estén confirmadas por este repositorio o por la app hermana real.

## Stack y comandos

### Estado verificado del stack

- Este repositorio no contiene un proyecto Node.js/Next.js completo con package.json.
- No hay evidencia verificada de scripts de lint, build, tests ni migraciones en esta carpeta.
- La aplicación web real se menciona como un proyecto hermano fuera de este repositorio, y no se debe asumir que aquí se desarrolla el runtime.
- El contenido actual es principalmente documentación, especificaciones, ejemplos, plantillas y archivos de soporte.

### Comandos verificados

Instalación:
- No verificada en este repositorio.

Desarrollo:
- No verificado en este repositorio.

Lint:
- No verificado.

Type-check:
- No verificado.

Pruebas:
- No verificado en este repositorio.

Build:
- No verificado en este repositorio.

Migraciones:
- No verificado en este repositorio.
- No se deben ejecutar migraciones SQL ni cambios destructivos sin revisión explícita del contexto real del proyecto.

Git y publicación:
- Verificado: el repositorio fue inicializado y publicado a GitHub.
- La rama principal se usa como main.

Si un comando no fue confirmado aquí, se considera "por confirmar" y no se debe inventar.

## Estructura del repositorio

- [README.md](README.md): resumen general del repositorio.
- [memoria.md](memoria.md): memoria del proyecto y continuidad entre sesiones.
- [control_de_proyectos.txt](control_de_proyectos.txt): resumen funcional y base documental del control de proyectos.
- [conocimiento](conocimiento): fundamentos teóricos y conceptuales de EVM y LPS.
- [docs](docs): documentación operativa, flujos y mejoras.
- [docs/Flujos de trabajo](docs/Flujos%20de%20trabajo): conjunto principal de especificaciones por flujo.
- [docs/Mejoras continuas](docs/Mejoras%20continuas): cambios y mejoras documentadas.
- [Sistema hibrido](Sistema%20hibrido): documentos y archivos del diseño híbrido del sistema.
- [Informacion para pruebas](Informacion%20para%20pruebas): datos, RDO y archivos de evaluación.
- [Formatos](Formatos): formatos del proyecto.
- [plantillas](plantillas): plantillas y ejemplos.
- [Dashboard ejemplo](Dashboard%20ejemplo): referencias visuales del dashboard.
- [RDTs movimiento de tierra, instlacion de bancoductos](RDTs%20movimiento%20de%20tierra,%20instlacion%20de%20bancoductos): evidencia de ejecución y reportes diarios.

## Arquitectura funcional

La organización funcional que aparece con mayor consistencia es la siguiente:

- Autenticación.
- Usuarios y permisos.
- Servicios y proyectos.
- Presupuesto / DP.
- Cronograma.
- Paquetes de trabajo.
- Plan Maestro.
- Plan semanal / 3WLA.
- RDT.
- PR.
- Dashboard.
- RQ.
- Notificaciones.

### Flujo principal documentado

1. Presupuesto + alcance.
2. Cronograma.
3. Relación WBS ↔ cronograma.
4. Plan Maestro.
5. Plan semanal / 3WLA.
6. RDT.
7. PR.
8. Dashboard.

La regla central documentada es que el sistema no debe mezclar:
- lo planificado,
- lo ejecutado,
- lo estimado,
- lo consolidado,
- y la vista ejecutiva.

## Modelo de datos y fuentes de verdad

### Presupuesto / DP
Fuente del alcance, partidas, metrados y costos base.
- Es la base contractual del proyecto.
- No debe confundirse con ejecución real.

### Cronograma
Fuente de fechas, duración y secuencia.
- Define cuándo se ejecuta cada actividad.
- No es, por sí solo, la fuente del costo programado semanal.

### Plan Maestro
Fuente del valor planificado temporal.
- Reparte metrado y costo por semana.
- Es el origen del PV.
- No reemplaza el plan semanal operativo.

### RDT validado
Fuente del avance real y de los costos reales medidos.
- Alimenta la ejecución real y validación del campo.
- Los materiales sin control real no deben convertirse en costo real sin validación.

### PR
Consolidado técnico del proyecto.
- No es la fuente original del alcance ni del cronograma.
- Sí es la capa de consolidación entre plan y real para análisis técnico.

### Dashboard
Vista derivada.
- Consume el PR y el historial.
- No es fuente de datos; es una representación ejecutiva del estado del proyecto.

### Paquetes de trabajo
Agrupación operativa opcional.
- No reemplazan la partida contractual ni la estructura base del presupuesto.

## Flujos principales

Los flujos documentados con mayor detalle son:

- [docs/Flujos de trabajo/01-interfaz.md](docs/Flujos%20de%20trabajo/01-interfaz.md)
- [docs/Flujos de trabajo/02-usuarios.md](docs/Flujos%20de%20trabajo/02-usuarios.md)
- [docs/Flujos de trabajo/03-entorno.md](docs/Flujos%20de%20trabajo/03-entorno.md)
- [docs/Flujos de trabajo/04-notificaciones.md](docs/Flujos%20de%20trabajo/04-notificaciones.md)
- [docs/Flujos de trabajo/05-rq.md](docs/Flujos%20de%20trabajo/05-rq.md)
- [docs/Flujos de trabajo/06-rdt.md](docs/Flujos%20de%20trabajo/06-rdt.md)
- [docs/Flujos de trabajo/07-nucleo-auth.md](docs/Flujos%20de%20trabajo/07-nucleo-auth.md)
- [docs/Flujos de trabajo/08-programa-portafolio-proyecto.md](docs/Flujos%20de%20trabajo/08-programa-portafolio-proyecto.md)
- [docs/Flujos de trabajo/09-importar-dp.md](docs/Flujos%20de%20trabajo/09-importar-dp.md)
- [docs/Flujos de trabajo/10-generacion-pr.md](docs/Flujos%20de%20trabajo/10-generacion-pr.md)
- [docs/Flujos de trabajo/11-dashboard.md](docs/Flujos%20de%20trabajo/11-dashboard.md)
- [docs/Flujos de trabajo/12-checklist.md](docs/Flujos%20de%20trabajo/12-checklist.md)
- [docs/Flujos de trabajo/13-orden-de-trabajo.md](docs/Flujos%20de%20trabajo/13-orden-de-trabajo.md)
- [docs/Flujos de trabajo/14-accesos-y-restricciones.md](docs/Flujos%20de%20trabajo/14-accesos-y-restricciones.md)
- [docs/Flujos de trabajo/15-cronograma.md](docs/Flujos%20de%20trabajo/15-cronograma.md)
- [docs/Flujos de trabajo/16-paneles.md](docs/Flujos%20de%20trabajo/16-paneles.md)
- [docs/Flujos de trabajo/17-chat-agentico.md](docs/Flujos%20de%20trabajo/17-chat-agentico.md)
- [docs/Flujos de trabajo/18-control-avance.md](docs/Flujos%20de%20trabajo/18-control-avance.md)

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

## Flujo de trabajo del agente

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
- Los cambios deben hacerse en ramas de trabajo y revisarse antes de fusionarse.
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

### Fuente canónica
- Este archivo: [AGENTS.md](AGENTS.md)

### Fuente complementaria
- [README.md](README.md)
- [memoria.md](memoria.md)
- [control_de_proyectos.txt](control_de_proyectos.txt)
- [docs/Flujos de trabajo/README.md](docs/Flujos%20de%20trabajo/README.md)
- [docs/Flujos de trabajo/18-control-avance.md](docs/Flujos%20de%20trabajo/18-control-avance.md)
- [.cursor/rules/flujos-aislamiento.mdc](.cursor/rules/flujos-aislamiento.mdc)
- [.cursor/rules/memoria-sesion-control-proyectos.mdc](.cursor/rules/memoria-sesion-control-proyectos.mdc)

### Duplicada
- No se detectaron duplicados de instrucciones formales con conflicto directo; sí hay documentación funcional repetida en varios archivos, pero no una fuente normativa rival.

### Desactualizada
- El contenido de varias notas de memoria puede estar parcialmente sesgado por continuidad de sesión. Se deben tratar como contexto operativo, no como norma definitiva del repositorio.

### Contradictoria
- No se detectó contradicción directa en las instrucciones del repositorio; sí hay una diferencia operacional clara entre este repositorio documental y la app real que vive fuera del workspace.

### Generada o no normativa
- Los archivos de sesión y memoria de continuidad son útiles para contexto, pero no deben reemplazar la fuente normativa.

## Nota importante

Este repositorio no es la aplicación web de producción; es la base documental y conceptual que alimenta el sistema real. El agente debe trabajar con esta limitación explícita y no inventar implementación ni runtime que no estén confirmados por este repositorio o por la app hermana.
