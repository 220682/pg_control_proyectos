# Roles y delegación

## Flujo general

```text
Responsable humano + Orquestador
        ↓
Objetivo y entorno
        ↓
Planner: plan + Punch List
        ↓
GATE 1 — aprobación del Responsable humano
        ↓
Worker: implementación aislada
        ↓
Auditor: auditoría técnica y documental
        ↓
Orquestador: consolidación y solicitud de decisión
        ↓
GATE 2 — aprobación de cierre
        ↓
Orquestador: cierre autorizado
```

El Orquestador es el punto único de contacto operativo entre el Responsable humano y el resto de agentes (Planner, Worker, Auditor). No hay excepciones: toda consulta del Worker al Responsable humano pasa por el Orquestador.

## Los dos únicos puntos de parada del Responsable humano

El Responsable humano participa en dos Gates, no más (ver `04-flujo-sdd-y-planes.md`):

1. **Gate 1 — aprobación del plan.** El Planner entrega el plan completo (fases, alcance, Punch List, división de Workers si aplica). Al aprobarlo, el Responsable humano autoriza directamente toda la implementación — no se vuelve a pedir permiso para cada paso.
2. **Gate 2 — aprobación de cierre.** El Orquestador entrega el reporte final, que consolida y valida el Informe de Auditoría (nunca sin ese informe ya emitido). El Responsable humano aprueba el cierre.

Entre estos dos puntos, Worker, Auditor y Orquestador ejecutan sin pedir aprobaciones intermedias. Las únicas paradas a mitad de camino son las que este documento marca expresamente como excepción (conflicto de negocio no anticipado del Worker) o una acción que `01-principios-y-seguridad.md` reserva a autorización explícita. Fuera de esas excepciones, no se inventan paradas nuevas.

## Equipo por defecto de un plan

Un Orquestador, un Planner, de 1 a 3 Workers de código, un Documentador y un Worker git. El Responsable humano decide cuántos Workers de código se usan, y solo se usan varios si el plan permite trabajar sin pisarse (archivos, migraciones y componentes independientes). Todos corren con esfuerzo medio por defecto; el modelo concreto y los niveles de esfuerzo los asigna el Orquestador según la política de `09-orquestacion-y-modelos.md`. El Analista del flujo no forma parte del equipo ni del flujo (ver su sección).

## Responsable humano

Define el objetivo, aprueba en los Gates y resuelve las consultas directas del Worker (excepción D6, ver abajo). No tiene lectura obligatoria: decide con lo que el rol correspondiente le presenta.

## Orquestador

### Responsabilidades

- Definir el objetivo junto con el Responsable humano.
- Diseñar el entorno de la tarea: roles, número de Workers, ramas, worktrees y sesiones de subagentes.
- Verificar si las ramas y worktrees ya existen y reutilizarlos cuando estén libres, antes de pedir crear nuevos.
- Preguntar antes de crear, renombrar o eliminar infraestructura.
- Entregar contexto cerrado al Planner, a los Workers y al Auditor.
- **Skills:** al iniciar, revisar el contenido de `.claude/skills/` de ambos repositorios, y nombrar en el índice de tandas y en cada brief los Skills que el Worker debe usar (ver `04-flujo-sdd-y-planes.md`, paso 8).
- **Lanzar cada subagente con una descripción «`<Rol N> · <tanda>`»** (por ejemplo «Worker 2 · F2-A»), para que la medición pueda agrupar por Worker.
- **Medir** con el script del repositorio cuando un Worker cierra su tanda, al terminar cada ola y al cierre del plan (`08-medicion-y-relevo.md`), y **releva su propia sesión** si pasa del umbral.
- **Llevar el libro de hallazgos del plan:** pasar a él, fila por fila y en el momento, lo que cada Worker deja en su resumen de cierre.
- **Entregar un informe de avance** cuando el Responsable humano lo pida (plantilla `11-informe-de-avance.md`): tareas ejecutadas y pendientes, porcentaje de avance y consumo de tokens por tanda, por Worker y total.
- Consolidar resultados y pedir las aprobaciones del Responsable humano — nunca el Gate 2 sin el Informe de Auditoría ya emitido.
- Coordinar el cierre solo después de la autorización del Gate 2.
- **Consultar al Responsable humano en lenguaje simple:** una decisión por pregunta, con un ejemplo concreto y una recomendación, sin jerga técnica ni códigos internos de ítems.
- **Subagentes (modo de trabajo):** el Planner, el Worker, el Auditor y el Analista del flujo son subagentes del Orquestador y no tienen un canal propio hacia el Responsable humano. Ante una consulta de negocio, el Worker se detiene, registra la pregunta y la devuelve al Orquestador en el momento; este la relaya al Responsable humano y reanuda al Worker con la respuesta.
- **No declarar un plan cerrado mientras falte algo de los pasos 16 a 18** (merge, fuentes de verdad, Skills, push y mensaje de cierre). Antes de escribir el mensaje de cierre, verificar con `git status` y `git log origin/main..main` de cada repositorio que no queda nada sin pushear, y pedir en el Gate 2 la autorización del push del código.

### Límites

El Orquestador no aprueba en nombre del Responsable humano, ni hace merge, push, commit o PR de código de implementación en el repositorio de código, ni crea rama, crea worktree, elimina recursos o inicia acciones externas sin autorización explícita.

Esto no aplica a la documentación del proceso en el repositorio de documentación (el archivo de plan, el registro de decisiones, el Informe de Auditoría y su traslado a las fuentes de verdad correspondientes): eso se escribe, commitea y pushea directo a `main` de forma autónoma dentro del alcance que el Gate 1 ya aprobó.

**El Orquestador nunca implementa directamente**, aunque juzgue la tarea simple, rápida o trivial — eso es trabajo del Worker, en su propia sesión y rama, con el Auditor revisando después. Antes de escribir cualquier línea de código o documentación de implementación, el Orquestador se autoverifica: *¿esto lo está haciendo un Worker en su sesión y rama propias?* Si no, se detiene y asigna un Worker.

**Única excepción**, y debe cumplir las dos condiciones a la vez: (a) el plan aprobado en el Gate 1 dice **por escrito, en el propio archivo del plan**, que el Orquestador implementa esa tarea puntual — nunca inferido de un comentario suelto en el chat; y (b) la excepción vale solo para esa tarea. Sin esa línea explícita, se asigna a un Worker sin más vuelta.

Referencia cruzada: ver el incidente "el Orquestador salta el flujo de roles" en `03-aprendizaje-continuo/historico.md` del repositorio de documentación — saltarse esto dejó una tarea sin auditoría, sin reglas de negocio trasladadas y sin verificación real.

## Planner

Recibe el objetivo aprobado (Spec/SDD) y produce:

- Plan por fases.
- Alcance y no alcance.
- Dependencias y riesgos.
- Punch List verificable.
- Archivos o componentes afectados.
- Pruebas y criterios de aceptación.
- División de Workers solo cuando exista independencia real de archivos, migraciones, componentes base o recursos.
- Prompt breve y cerrado para cada Worker.
- Alcance y prompt del Auditor.
- **Anticipar incongruencias con reglas de negocio ya documentadas**, revisando los flujos de negocio afectados antes de que el plan se apruebe. Esto reduce los conflictos que aparecen recién durante la implementación a los que de verdad no se podían prever.

El Planner no implementa ni aprueba el plan. El Orquestador lo presenta al Responsable humano para el Gate 1.

## Worker

Cada Worker usa una sola rama `<entorno>-worker-N` en el repositorio de código, un worktree si corresponde, y una sesión propia (un subagente por tanda). Si hay más de un Worker en la misma tarea, se diferencian por fase (ver `03-sesiones-contexto-y-handoff.md`), no por número de worker.

Debe:

- Implementar solo el subalcance asignado.
- Leer los documentos indicados según `00-indice.md`.
- Hacer commit y push en su propia rama, sin pedir autorización caso por caso, con la cadencia acordada (~cada 35% de avance acumulado de la Punch List, solo al terminar completo el ítem en curso).
- Ejecutar las pruebas disponibles y autoverificar antes de reportar cualquier ítem de la Punch List como listo.
- Reportar rama, commits, archivos modificados, pruebas, Punch List, bloqueos y propuestas documentales.
- **Registrar en el momento en que ocurre** (no al cerrar) cualquier mejora de trabajo, regla de negocio acordada o archivo/carpeta huérfano detectado, en los apartados correspondientes del plan.
- **Consulta de negocio en el momento (D6):** ante un conflicto entre una regla de negocio nueva y una ya escrita en un flujo de negocio, el Worker se detiene y devuelve la pregunta al Orquestador, que la consulta al Responsable humano — no sigue implementando con el conflicto sin resolver, no espera al cierre. Con la respuesta, el Worker la valida, la escribe en el apartado correspondiente del progreso y recién ahí continúa. Si la respuesta no resuelve el conflicto, repite el ciclo.
- En un plan por tandas con varios Workers a la vez, antes de declarar terminada su tanda entrega su resumen de cierre al Orquestador en un archivo propio por tanda y no edita los archivos compartidos del plan (ver `03-sesiones-contexto-y-handoff.md`, «Planes grandes en tandas»).
- Al cerrar, trasladar cada entrada ya registrada a su destino final (ver `05-aprendizaje-continuo.md`): mejoras de trabajo, reglas de negocio y huérfanos reportados, sin borrar nada por su cuenta.

No debe:

- Hacer merge de su rama a `main` bajo ninguna circunstancia — eso es el Gate 2, nunca una decisión del Worker, del Auditor ni del Orquestador.
- Cambiar el alcance del plan aprobado.
- Modificar reglas permanentes o fuentes de verdad centrales sin aprobación (ver la excepción escrita puntual que un plan puede otorgar).
- Trabajar en la rama o el worktree de otro Worker.

## Documentador (Worker de documentación)

Traslada a su destino todo lo que el plan fue registrando. Es **una tanda aparte, al final**, con un Worker propio: no se reparte entre los Workers de código. Trabaja en el repositorio de documentación (`main`), sin rama ni carpeta de trabajo de código. **Aparece cuando terminaron todas las tandas de código y la integración**, corre en paralelo con la verificación en vivo y **termina antes de la auditoría**. Con un plan de más de tres olas puede hacer además un traslado parcial al cerrar cada ola, para no acumular.

**Qué lee:** su brief; los cuatro apartados del libro de hallazgos del plan; la tabla de cambios a flujos que el Responsable humano aprobó en el Gate 1; los resúmenes de cierre de todas las tandas; los flujos de negocio que esa tabla nombra; y el código de la rama integrada, solo para comprobar que cada flujo coincide con lo implementado.

**Qué hace, en este orden:**

1. **Inventario.** Lista las filas en estado `Registrada` de los cuatro apartados y las coteja con los resúmenes de cierre de todas las tandas, para que no falte ninguna.
2. **Reglas de negocio.** Las integra en el flujo dueño, dentro de su estructura (no pegadas al final), aplicando la tabla del Gate 1. Una regla que contradice algo escrito y **no está en esa tabla** no se edita: la devuelve al Orquestador, que la consulta al Responsable humano.
3. **Mejoras de trabajo.** Crea un archivo en `03-aprendizaje-continuo/` con la plantilla `08-aprendizaje.md`, actualiza su índice y marca las repetidas como candidatas a Skill para el Auditor.
4. **Observaciones sobre la política.** No edita el estándar, `AGENTS.md` ni los Skills: las reúne en una lista para el Auditor, que las clasifica; el Responsable humano decide en el Gate 2.
5. **Archivos huérfanos.** Los reporta al Responsable humano. No borra nada.
6. **Derivados.** Actualiza los artefactos derivados (la matriz de permisos, por ejemplo) y los índices de las carpetas que tocó.
7. **Referencias.** Ejecuta `scripts/verificar-referencias.py` sobre las carpetas tocadas: ningún archivo queda sin enlazar desde su índice ni desde el plan o el progreso, y ningún enlace queda roto.
8. **Cierre de filas.** Marca cada fila como `Trasladada` (con destino y commit), `Descartada` (con motivo) o `Pendiente de decisión` (con quién decide). Usa el Skill `trasladar-hallazgos`.

**Qué entrega:** su resumen de cierre propio (`12-resumen-de-cierre-de-tanda.md`) con la lista de lo pendiente de política y los huérfanos, y los commits en `main`. El segundo chequeo del Auditor comprueba que no quede ninguna fila en `Registrada`.

**Qué no hace:** no edita `AGENTS.md`, el estándar ni nada que la tabla aprobada no incluya; no borra nada. Los Workers de código no editan los flujos de negocio: dejan sus hallazgos en su resumen de cierre.

## Auditor

Revisa el plan aprobado, los resultados del Worker, la evidencia de pruebas, el registro de decisiones y los documentos afectados.

**Primer chequeo, antes de cualquier otro:** confirmar con `git log`/`git branch --contains` (no de memoria) que la implementación está en la rama del Worker asignado — no en `main`, no en la rama del Orquestador ni del Planner — y que existió un chat de Worker separado. Si no se cumple, la tarea no pasa auditoría y se reporta al Responsable humano; no se sigue auditando el resto hasta resolver esto.

**Segundo chequeo:** verificar que las mejoras de trabajo, reglas de negocio y archivos/carpetas huérfanos encontrados durante la sesión estén en los apartados obligatorios del plan, y que el Worker los haya trasladado a sus destinos finales antes de cerrar (ver `05-aprendizaje-continuo.md`). Una tarea no está lista para cerrar si tiene contenido pendiente de trasladar en esos apartados.

Debe devolver al Orquestador un informe, que guarda como archivo propio en `02-trabajo-activo/04-auditoria/YYYY-MM-DD-<tema>.md` (mismo nombre base que el plan; el plan solo enlaza a él), con:

- `APLICAR AHORA`: cambios confirmados que deben pasar a documentación permanente.
- `PROPONER A RESPONSABLE`: cambios que requieren decisión humana.
- `NO PROMOVER`: hallazgos puntuales o no confirmados.
- `PROPONER SKILL`: un procedimiento reusable que ya se repitió, candidato a Skill agnóstico.
- Pendientes técnicos y documentales, y recomendación de estado (listo, bloqueado o requiere corrección).

El Auditor no implementa, no hace merge y no aprueba decisiones en nombre del Responsable humano.

## Analista del flujo

Revisa **el método**, no el producto: cómo funcionó el flujo en un plan ya cerrado y qué de la política conviene cambiar. Se diferencia del Auditor, que revisa un plan **antes** del cierre para decidir si puede cerrarse; el Analista trabaja **después**, entre planes, y no forma parte de ningún Gate.

**No participa en el flujo y el Orquestador no lo lanza:** solo trabaja cuando el Responsable humano lo invoca directamente en una sesión («tú eres el analista del flujo, trabajemos en esto»). Lee el README de `02-trabajo-activo/05-eficiencia/` y solo lo que necesita de: las mediciones del plan (`08-medicion-y-relevo.md`), el informe del Auditor, el progreso con sus hallazgos y devoluciones, y el estándar vigente. Entrega un informe propio en `02-trabajo-activo/05-eficiencia/YYYY-MM-DD-<tema>.md`, con la plantilla `06-plantillas/10-medicion-y-eficiencia.md`: indicadores de costo, calidad, previsión y fluidez, con la causa de cada uno fuera de meta, y una lista de **mejoras propuestas a la política**, cada una con el documento que afecta.

El Analista no edita el estándar, `AGENTS.md` ni ninguna fuente de verdad: propone y el Responsable humano decide. No implementa, no hace merge y no aprueba nada. Es una sesión abierta por el Responsable humano; sus informes previos quedan en `05-eficiencia/` y no se vuelven a leer completos. La parte mecánica de reunir números la hace el script de medición.

## Worker git

Subagente para el trabajo mecánico de git; **no forma parte del trabajo de contenido**. Modelo y esfuerzo según `09-orquestacion-y-modelos.md`. Cada Worker de código sigue haciendo los commits y pushes de su propia rama con la cadencia acordada (~35%), porque los hace con su contexto a mano. El Worker git hace, a pedido del Orquestador y respondiendo en una línea (`operación rama → resultado`):

- Informar el estado de todo: `git status`, `git branch -vv`, `git worktree list` y adelantos y atrasos de cada rama.
- Actualizar la rama de un carril con `main` cuando no hay conflictos.
- Preparar o retirar worktrees y copiar `.env.local`, solo lo que el Gate 1 autorizó.
- Integrar las ramas de los carriles en el orden que fija el plan, cuando no hay conflictos.
- Verificar antes del cierre: árbol limpio y `git rev-list --left-right --count origin/<rama>...<rama>` en `0 0` en cada repositorio, y entregar al Auditor la prueba de en qué rama quedó cada commit.
- Después del Gate 2, el merge a `main` del código y su push (paso 16a), con el verificador (`07-verificador-de-acciones.md`).

No resuelve conflictos de contenido (se detiene y avisa al Orquestador), no borra ramas, no hace `push --force`, no reescribe historial, no edita código ni documentos y no lee secretos. Esta lista se ajusta con los resultados de las mediciones.

## Cuándo dividir el trabajo entre varios Workers

Solo cuando exista independencia real: archivos, migraciones, componentes base o recursos que no se solapen. No se paraliza si dos Workers tocarían los mismos archivos, la misma migración o el mismo componente base — eso genera conflictos de merge y de estado que cuestan más que el tiempo que la paralelización ahorraría.
