# Plan único — Implementación de política de Orquestador, sesiones y worktrees (Claude + fallback local)

> **Estado:** PROPUESTO. No ejecutar hasta que Victor lo apruebe explícitamente.
>
> **Objetivo:** instalar una única política de trabajo para que Victor pueda iniciar tareas con un Orquestador, usar Planner, Workers y Auditor cuando haga falta, conservar chats visibles como bitácora, reutilizar ramas de trabajo y controlar el crecimiento del contexto.
>
> **Resultado esperado:** al finalizar, los documentos del repositorio contendrán la política operativa aprobada y se podrá iniciar una primera tarea real usando este flujo.

---

## Compatibilidad de entornos

### Entorno principal: Claude

- Claude (app de escritorio o web) es el entorno principal para ejecutar esta política.
- Allí se pueden usar sesiones separadas para Orquestador, Planner, Workers y Auditor, cuando la plataforma lo permita.
- Los chats son bitácoras de una tarea; no sustituyen el archivo de tarea ni el Registro de decisiones.
- Los nombres de chats se gestionan manualmente desde la interfaz disponible.

### Entorno alternativo: VS Code + otro LLM local

- Cuando no haya tokens o no sea posible continuar en Claude, se puede continuar localmente desde VS Code con otro LLM.
- VS Code no se considera fuente de gestión de sesiones cloud. La continuidad se conserva en Git y en los archivos Markdown del repositorio.
- Antes de cambiar de entorno, registrar en el archivo de tarea: etapa actual, rama, worktree, último commit, pruebas realizadas, bloqueos y siguiente paso.
- Al iniciar en el LLM local, el primer prompt debe indicar que lea `AGENTS.md`, `docs/README.md`, los documentos aplicables de `docs/00-sistema/` y el archivo de tarea activo.
- Si el LLM local no conserva chats/sesiones visibles, el archivo de tarea y el Registro de decisiones son la bitácora obligatoria.
- No se cambia de rama ni se crea infraestructura por el solo hecho de cambiar de LLM.

---

## Resultado final

Al terminar este plan debe existir un sistema con este ciclo:

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

La política debe permitir trabajar en local, nube o híbrido, y conservar la trazabilidad mediante el archivo de tarea, ramas, worktrees y chats/sesiones (cuando estén disponibles).

---

## Restricciones globales

- No borrar archivos, ramas, worktrees ni chats sin aprobación explícita de Victor.
- No hacer commit, push, merge, PR, creación de rama o creación de worktree sin autorización explícita de Victor.
- No imprimir ni guardar secretos, tokens, contraseñas, cadenas de conexión ni archivos `.env`.
- Mantener una única fuente de verdad por concepto; no duplicar reglas entre archivos.
- Los cambios de documentación de esta implementación se hacen en `main` del repositorio documental, respetando `AGENTS.md` y la política vigente del repositorio.
- Al usar `git add`, agregar archivos de forma explícita; no usar `git add .`.
- Registrar toda decisión nueva de Victor en el `## Registro de decisiones` de esta tarea, en el momento en que ocurra.

---

## Decisiones que deben confirmarse

El Orquestador debe preguntar estas decisiones al inicio de la primera ejecución y guardar las respuestas como convención permanente:

- [ ] Entorno preferido: `local`, `nube` o `híbrido`.
- [ ] Herramienta principal de ejecución: Claude (app de escritorio o web).
- [ ] Rol de VS Code: solo abrir/revisar archivos, no administrar sesiones ni ejecutar la orquestación.
- [ ] Rol de app/web de Claude: ver chats, historial y renombrar chats manualmente.
- [ ] Ubicación de worktrees: carpetas hermanas o `.worktrees/` dentro del repositorio.
- [ ] Cantidad inicial del pool de ramas: recomendado `work-1` a `work-4`.
- [ ] Política de chats cerrados: mantener como historial o renombrar con prefijo `hist_`.

Cuando una convención se apruebe, debe registrarse en:

```text
docs/00-sistema/convenciones-de-trabajo.md
```

---

## Estructura documental objetivo

Crear o actualizar únicamente estos archivos de política:

```text
AGENTS.md
  └── deriva a docs/README.md

docs/README.md
  └── manual de trabajo del agente e índice de políticas

docs/00-sistema/
  ├── roles-y-flujo.md
  ├── convenciones-de-trabajo.md
  └── gestion-de-sesiones-y-contexto.md

docs/Tareas de implementacion/
  └── YYYY-MM-DD-<tema>.md
```

Regla: `roles-y-flujo.md` explica quién hace qué; `convenciones-de-trabajo.md` conserva decisiones estables de entorno/ramas/worktrees; `gestion-de-sesiones-y-contexto.md` define chats, nombres y cierre de contexto.

---

# Fase 0 — Diagnóstico y congelamiento

## Objetivo

Validar el estado real del repositorio y confirmar que no se sobrescribirá una política existente.

## Pasos

- [ ] Leer `AGENTS.md` completo.
- [ ] Leer `docs/README.md` completo.
- [ ] Revisar si existe `docs/00-sistema/` y leer sus documentos relevantes.
- [ ] Localizar el archivo de tarea donde se ejecutará este plan.
- [ ] Verificar rama actual y estado de Git con:

```powershell
git branch --show-current
git status
```

- [ ] Identificar cambios no relacionados; no agregarlos al commit de esta tarea.
- [ ] Confirmar que esta implementación se hará en el repositorio documental y en `main`, según la norma vigente.
- [ ] Crear o actualizar el `## Registro de decisiones` de la tarea activa.
- [ ] Presentar informe de impacto a Victor antes de crear o modificar archivos.

## Entregable

Un informe breve con:

- Archivos que se crearán o modificarán.
- Posibles contradicciones con la documentación existente.
- Preguntas pendientes de Victor.
- Propuesta de ubicación para cada política.

**Punto de control:** no seguir a Fase 1 sin aprobación explícita de Victor.

---

# Fase 1 — Definir convenciones iniciales

## Objetivo

Definir una sola vez las convenciones de entorno, ramas, worktrees y sesiones antes de crear infraestructura.

## Preguntas obligatorias

El Orquestador debe preguntar exactamente lo necesario:

```text
✅ Orquestador activo.

Antes de instalar el entorno necesito confirmar las convenciones base:

1. ¿Trabajaremos normalmente en local, nube o híbrido?
2. ¿Confirmas usar Claude (app de escritorio o web) para ejecutar el flujo?
3. ¿Confirmas usar VS Code solo para revisar archivos y no para administrar sesiones?
4. ¿Dónde deben vivir los worktrees?
   A) Como carpetas hermanas del repositorio.
   B) En .worktrees/ dentro del repositorio.
5. ¿Cuántas ramas persistentes deseas inicialmente?
   Recomendado: work-1, work-2, work-3 y work-4.
6. Al cerrar una tarea, ¿los chats se conservan con su nombre histórico o se renombran con hist_?
```

## Pasos

- [ ] Esperar respuestas de Victor; no asumir valores si faltan.
- [ ] Crear `docs/00-sistema/convenciones-de-trabajo.md`.
- [ ] Guardar las respuestas como configuración estable.
- [ ] Indicar que estas convenciones se reutilizan en tareas futuras, salvo cambio explícito de Victor.
- [ ] Registrar en la tarea que las convenciones fueron aprobadas y dónde viven.

## Contenido mínimo de `convenciones-de-trabajo.md`

```markdown
# Convenciones de trabajo

## Entorno por defecto

- Modo: local / nube / híbrido.
- Ejecución del flujo: Claude (app de escritorio o web).
- VS Code: revisión de archivos, no gestión de chats/sesiones.
- App/web de Claude: visualización de chats, historial y cambio manual de nombre.

## Pool de ramas

- Rama integrada: `main`.
- Ramas de trabajo persistentes: `work-1`, `work-2`, `work-3`, `work-4`.
- Las ramas `work-N` no se borran por rutina; se reutilizan después de sincronizarlas con `main`.

## Worktrees

- Ubicación aprobada: <valor confirmado por Victor>.
- Cada worktree corresponde a una rama `work-N`.
- No se crea ni elimina un worktree sin autorización de Victor.

## Chats

- Un chat corresponde a una tarea o etapa clara.
- No se reutiliza un chat de una tarea cerrada para una tarea nueva.
- Los chats se renombran manualmente en app/web según esta política.
```

**Punto de control:** presentar el archivo a Victor y esperar aprobación antes de crear ramas o worktrees.

---

# Fase 2 — Instalar roles y flujo

## Objetivo

Crear la política que define responsabilidades, aprobaciones y comunicación entre Orquestador, Planner, Worker y Auditor.

## Pasos

- [ ] Crear o actualizar `docs/00-sistema/roles-y-flujo.md`.
- [ ] Incluir la activación visible del Orquestador.
- [ ] Definir el flujo: Objetivo → Planificación → Aprobación → Implementación → Auditoría → Revisión de Victor → Cierre.
- [ ] Definir que el Orquestador es el punto único de contacto con Victor.
- [ ] Definir que el Planner prepara planes, Punch List, dependencias, riesgos y división de Workers.
- [ ] Definir que Workers solo implementan el subalcance asignado y no hacen merge.
- [ ] Definir que Auditor revisa evidencia y documentación, sin inventar reglas ni aprobar por Victor.
- [ ] Definir los puntos obligatorios de aprobación humana.
- [ ] Definir límites para impedir acciones externas sin autorización.

## Contenido obligatorio: Orquestador

```markdown
## Orquestador

El Orquestador es el punto único de contacto operativo entre Victor y los demás agentes.

### Activación

Cuando Victor diga una frase equivalente a “Vamos a trabajar en un plan con agente orquestador”, responder:

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
```

## Contenido obligatorio: Planner

```markdown
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
```

## Contenido obligatorio: Worker

```markdown
## Worker

Cada Worker usa una sola rama `work-N`, un worktree si corresponde y un chat propio.

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
```

## Contenido obligatorio: Auditor

```markdown
## Auditor

El Auditor revisa el plan aprobado, los resultados de Workers, la evidencia de pruebas, el Registro de decisiones y los documentos afectados.

Debe devolver al Orquestador:

- APLICAR AHORA: cambios confirmados que deben pasar a documentación permanente.
- PROPONER A VICTOR: cambios que requieren decisión humana.
- NO PROMOVER: hallazgos puntuales o no confirmados.
- Pendientes técnicos/documentales y estado de cierre.

El Auditor no implementa, no hace merge y no aprueba decisiones de Victor.
```

**Punto de control:** presentar las reglas de roles a Victor para aprobación.

---

# Fase 3 — Instalar política de sesiones y contexto

## Objetivo

Evitar que un chat acumule tareas distintas y conservar las conversaciones como bitácora visible.

## Pasos

- [ ] Crear o actualizar `docs/00-sistema/gestion-de-sesiones-y-contexto.md`.
- [ ] Definir que Claude (app de escritorio o web) ejecuta el flujo y soporta local/nube.
- [ ] Definir el uso de app/web de Claude para ver chats, historial y renombrarlos manualmente.
- [ ] Definir que VS Code sirve para leer/revisar documentos, no para gestionar sesiones.
- [ ] Definir “un chat = una tarea o etapa clara”.
- [ ] Definir nomenclatura de chats.
- [ ] Definir inicio con contexto mínimo y cierre con preservación de historial.
- [ ] Definir el uso opcional de `/compact` solo durante una misma tarea larga.

## Contenido obligatorio

```markdown
# Gestión de sesiones y contexto

## Dónde se trabaja

- Claude (app de escritorio o web): ejecución del flujo completo, tanto local como nube.
- VS Code: revisión de planes y documentos; no administración de chats/sesiones.
- App/web de Claude: visualización de chats, historial y renombrado manual de chats.

## Regla de contexto

- Un chat = una tarea o etapa clara de una tarea.
- No mezclar tareas distintas en el mismo chat.
- Al cerrar una tarea, sus chats dejan de ser contexto activo y quedan como historial.
- Para una tarea nueva se abre un chat nuevo con contexto limpio.

## Nombres de chats

```text
Orquestador_<tarea>
Planner_<tarea>
Auditor_<tarea>
Worker_1_<tarea>
Worker_2_<tarea>
Worker_3_<tarea>
Worker_4_<tarea>
```

Ejemplo:

```text
Orquestador_dashboard-fase-4
Planner_dashboard-fase-4
Auditor_dashboard-fase-4
Worker_1_dashboard-fase-4
```

## Inicio de cada chat

El primer mensaje debe contener solo:

- Rol.
- Objetivo/subalcance.
- Rama y worktree, si aplica.
- Documentos que debe leer.
- Criterios de salida.
- Restricciones.

## Cierre de cada chat

Al cerrar una tarea, el Orquestador registra los chats en el archivo de tarea y pregunta a Victor si desea:

1. Conservarlos con el nombre actual como historial.
2. Renombrarlos manualmente con `hist_` como prefijo.

No se reutiliza un chat histórico para una tarea nueva.

## /compact

Puede usarse solo si una tarea larga llena demasiado el contexto. No convierte un chat viejo en contexto válido para una tarea nueva.
```

**Punto de control:** presentar la política de sesiones a Victor para aprobación.

---

# Fase 4 — Preparar pool de ramas y worktrees

## Objetivo

Preparar infraestructura persistente para Workers sin crear/eliminar ramas en cada implementación.

## Reglas

```text
main    → rama integrada y aprobada
work-1  → Worker 1
work-2  → Worker 2
work-3  → Worker 3
work-4  → Worker 4
```

Las ramas `work-N` son un pool persistente. No se borran por rutina. Una rama libre puede reutilizarse para una nueva tarea después de sincronizarla con `main` y verificar que no contenga trabajo pendiente.

## Pasos

- [ ] Consultar si Victor autoriza crear el pool de ramas definido en la convención.
- [ ] Crear solo las ramas aprobadas que aún no existan.
- [ ] Consultar si Victor autoriza crear los worktrees correspondientes.
- [ ] Crear worktrees solo en la ubicación aprobada.
- [ ] Verificar asociación rama ↔ worktree.
- [ ] Registrar rutas y estado en `docs/00-sistema/convenciones-de-trabajo.md`.
- [ ] Registrar resultado en la tarea activa.

## Referencia de asociación

```text
work-1 ↔ <ruta-worktree-work-1> ↔ Worker_1_<tarea>
work-2 ↔ <ruta-worktree-work-2> ↔ Worker_2_<tarea>
work-3 ↔ <ruta-worktree-work-3> ↔ Worker_3_<tarea>
work-4 ↔ <ruta-worktree-work-4> ↔ Worker_4_<tarea>
```

## Preguntas de creación

Si el entorno requerido no existe, el Orquestador debe preguntar en términos concretos:

```text
Para esta tarea se necesitan tres Workers.

Disponibles: work-1 y work-2.
Falta: work-3 y su worktree.

¿Autorizas crear work-3 y el worktree en la ubicación acordada?
```

Si ya existe todo lo necesario, el Orquestador continúa sin pedir recrear nada.

**Punto de control:** no crear ramas/worktrees sin autorización explícita de Victor.

---

# Fase 5 — Integrar el flujo en tareas de implementación

## Objetivo

Definir la plantilla mínima que toda tarea futura debe usar cuando se trabaje con Orquestador.

## Pasos

- [ ] Agregar a `docs/README.md` un enlace a las tres políticas de `docs/00-sistema/`.
- [ ] Agregar una sección “Inicio de tarea con Orquestador”.
- [ ] Definir plantilla/estructura mínima de tarea en `docs/Tareas de implementacion/`.
- [ ] Asegurar que cada tarea registre entorno, chats, ramas, worktrees, decisiones y resultados.

## Plantilla mínima

```markdown
# <Fecha> — <Título de tarea>

## Estado

Propuesta / Planificando / Implementando / En auditoría / Pendiente de Victor / Cerrada.

## Objetivo

- Resultado esperado:
- Alcance:
- No alcance:
- Validación esperada:

## Entorno

- Modo: local / nube / híbrido.
- Orquestador: chat `Orquestador_<tarea>`.
- Planner: chat `Planner_<tarea>`.
- Auditor: chat `Auditor_<tarea>`.

## Asignaciones

| Rol | Chat | Rama | Worktree | Estado |
| --- | --- | --- | --- | --- |
| Orquestador | `Orquestador_<tarea>` | `main` | N/A | Activo |
| Planner | `Planner_<tarea>` | `main` | N/A | Pendiente |
| Worker 1 | `Worker_1_<tarea>` | `work-1` | `<ruta>` | Pendiente |
| Auditor | `Auditor_<tarea>` | `main` | N/A | Pendiente |

## Plan aprobado

- [ ] Pendiente de Planner.

## Punch List

- [ ] Pendiente de Planner.

## Registro de decisiones

| # | Fecha | Decisión | Origen | Destino | Estado |
| --- | --- | --- | --- | --- | --- |

## Resultados de Workers

- Rama:
- Commits:
- Pruebas:
- Bloqueos:

## Informe de Auditoría

### Aplicar ahora

### Proponer a Victor

### No promover

## Cierre

- Documentación promovida:
- Pendientes:
- Autorización de cierre:
```

**Punto de control:** verificar que la plantilla no contradiga el sistema documental actual.

---

# Fase 6 — Prueba controlada del flujo

## Objetivo

Probar la política con una tarea pequeña, sin cambios de alto riesgo, antes de usarla en una implementación grande.

## Pasos

- [ ] Elegir una tarea documental pequeña y reversible.
- [ ] Activar el Orquestador con la frase definida.
- [ ] Validar que salude y pida objetivo.
- [ ] Validar que consulte o cargue las convenciones guardadas.
- [ ] Hacer que Planner produzca un plan corto y Punch List.
- [ ] Aprobar el plan.
- [ ] Usar un solo Worker o ninguno si la prueba es documental.
- [ ] Ejecutar Auditor.
- [ ] Verificar que el Orquestador consolide el resultado y solicite aprobación.
- [ ] Confirmar que el cierre registra chats, ramas, decisiones y documentación promovida.
- [ ] Registrar mejoras necesarias en el Registro de decisiones; no alterar la política sin aprobación de Victor.

## Criterios de aceptación

- [ ] El Orquestador se activa con saludo visible.
- [ ] Se registran objetivo, entorno y decisiones.
- [ ] El Planner entrega plan y Punch List antes de implementar.
- [ ] Ninguna rama/worktree/chat se crea sin autorización.
- [ ] Los roles quedan separados y trazables.
- [ ] El Auditor entrega los tres grupos de salida.
- [ ] El Orquestador solicita aprobación antes del cierre.
- [ ] El chat de prueba queda preservado como historial y no se reutiliza para otra tarea.

---

# Fase 7 — Cierre de esta implementación

## Pasos

- [ ] Auditor revisa consistencia entre `docs/README.md`, `roles-y-flujo.md`, `convenciones-de-trabajo.md`, `gestion-de-sesiones-y-contexto.md` y la plantilla de tarea.
- [ ] Resolver contradicciones, enlaces rotos o duplicaciones.
- [ ] Presentar a Victor los cambios documentales que pasarán a ser permanentes.
- [ ] Con aprobación de Victor, actualizar documentos aprobados.
- [ ] Actualizar este archivo con resultados y destino de cada decisión.
- [ ] Solicitar autorización explícita antes de hacer commit/push.
- [ ] Hacer commit y push solo con los archivos revisados y autorizados.
- [ ] Renombrar esta tarea a `— CERRADO 100%.md` únicamente cuando no queden pendientes.

## Cierre esperado

```text
✅ Política instalada y validada.

- Convenciones guardadas:
- Roles y flujo instalados:
- Política de sesiones instalada:
- Pool de ramas/worktrees:
- Prueba controlada:
- Documentación promovida:
- Pendientes futuros:

¿Autorizas el commit/push final y el cierre documental?
```

---

# Registro de decisiones

> Registrar aquí, en el momento, toda respuesta de Victor, decisión del Orquestador, cambio de convención o hallazgo relevante. Al cerrar, trasladar cada decisión aprobada al documento permanente correspondiente.

| # | Fecha | Decisión / aprendizaje | Origen | Destino | Estado |
| --- | --- | --- | --- | --- | --- |
| 1 | Pendiente | Definir modo de trabajo: local, nube o híbrido | Pendiente de Victor | `docs/00-sistema/convenciones-de-trabajo.md` | Pendiente |
| 2 | Pendiente | Definir ubicación de worktrees | Pendiente de Victor | `docs/00-sistema/convenciones-de-trabajo.md` | Pendiente |
| 3 | Pendiente | Definir cantidad inicial de ramas `work-N` | Pendiente de Victor | `docs/00-sistema/convenciones-de-trabajo.md` | Pendiente |
| 4 | Pendiente | Definir preservación de chats históricos | Pendiente de Victor | `docs/00-sistema/gestion-de-sesiones-y-contexto.md` | Pendiente |

---

# Prompt para iniciar este plan

Copia este mensaje en Claude (app de escritorio o web), dentro del repositorio documental:

```text
Vamos a trabajar en un plan con agente orquestador.

Entorno principal: Claude (app de escritorio o web).
Entorno alternativo: VS Code + otro LLM local si no se puede continuar en Claude.

Ejecuta este único plan:
docs/Tareas de implementacion/2026-09-22-plan-unico-orquestador-sesiones-worktrees.md

Empieza por Fase 0 — Diagnóstico y congelamiento.

No modifiques, crees, renombres, borres, commitees, pushees, hagas merge, abras PR, crees ramas, crees worktrees ni abras sesiones cloud antes de presentarme el informe de impacto y obtener mi aprobación explícita.

Lee AGENTS.md, docs/README.md y los documentos aplicables de docs/00-sistema/. Mantén actualizado el Registro de decisiones de esta tarea.

Si se cambia a VS Code + LLM local, registra primero el estado de traspaso en la tarea: etapa, rama, worktree, último commit, pruebas, bloqueos y siguiente paso.
```
