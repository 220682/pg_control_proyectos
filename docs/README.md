# docs — orquestador de esta carpeta

Este archivo ordena **solo `docs/`**. La fuente normativa de todo el repositorio sigue siendo [AGENTS.md](../AGENTS.md) — este archivo existe porque AGENTS.md deriva aquí para saber cómo moverse dentro de `docs/`.

Aquí es donde se trabaja. Lo demás en la raíz del repositorio (`conocimiento/`, `Sistema hibrido/`, `Informacion para pruebas/`, `Formatos/`, etc.) es material de apoyo/referencia, no el flujo activo de trabajo.

## Qué hay y para qué sirve cada cosa

| Carpeta | Qué es | Se lee para contexto general |
|---|---|---|
| [Flujos de trabajo/](Flujos%20de%20trabajo/) | Los conceptos/temas permanentes del sistema (uno por archivo numerado). Es la fuente de verdad de cada tema. | Sí — todos |
| [Tareas de implementacion/](Tareas%20de%20implementacion/) | Lo que hacen los Workers: trabajo operativo de construcción (código, pantallas, consultas, migraciones). Incluye tanto tareas del flujo de Orquestador (plantilla `plantilla-tarea.md`) como lotes con Punch List interactiva — ver "Diferencia entre Tareas de implementación y Mejoras continuas" abajo. | Solo la tarea activa relacionada |
| [Mejoras continuas/](Mejoras%20continuas/) | Solo aprendizajes sobre **cómo trabajamos** (método, herramientas, workarounds), extraídos de una tarea de `Tareas de implementacion/`. **No** contiene trabajo de implementación ni reglas de negocio del sistema (esas van directo al Flujo correspondiente). | El resumen de aprendizajes vigentes |
| [visual-companion/](visual-companion/) | `design.md` es el sistema de diseño obligatorio (layout, tokens, componentes, columnas, accesibilidad) para crear o modificar cualquier interfaz. El resto son mockups HTML que fijan cómo se ve y cómo se llama cada pantalla (nomenclatura, campos). Referencia de UI, no de pendientes. | No, salvo tarea de diseño de UI — ahí `design.md` es lectura obligatoria, no opcional |
| [00-sistema/](00-sistema/) | Políticas operativas del flujo con Orquestador: roles (`roles-y-flujo.md`), convenciones de entorno/ramas/worktrees (`convenciones-de-trabajo.md`) y gestión de sesiones/chats (`gestion-de-sesiones-y-contexto.md`). Define **cómo se trabaja**, no de qué trata el sistema. | Solo si la tarea usa el flujo de Orquestador |

## Diferencia entre Tareas de implementación y Mejoras continuas

> Corregido el 2026-09-23 a pedido de Victor — son **tres** categorías, no dos.

- **Tarea de implementación** = lo que hacen los Workers: código, pantallas, consultas, migraciones. Vive en `Tareas de implementacion/`. Registra QUÉ se implementó — no es el lugar de la regla permanente.
- **Mejora de trabajo / mejora continua** = un aprendizaje sobre **cómo trabajamos** (método, herramientas, workarounds operativos) — no una regla del sistema. Vive en `Mejoras continuas/` como destino final (no se traslada más allá). Ejemplo: "intentamos correr SQL por la conexión directa de Postgres, falló por falta de salida IPv6 en el sandbox, se resolvió usando la Management API de Supabase."
- **Regla de negocio** = una regla del sistema (cómo se calcula, valida o comporta algo). **No se guarda en un archivo aparte** — va directo al `Flujo de trabajo` que corresponda, integrada en su estructura existente (no pegada al final). Si contradice una regla ya escrita, se modifica lo existente con lo acordado con Victor durante la tarea; no quedan las dos versiones. Ejemplo: "el AC se calcula de la suma de HH+HM más los porcentajes de avance de materiales y subcontratos" → va a `18-control-avance.md`.

Toda tarea de implementación tiene tres apartados obligatorios (`## Mejoras (de trabajo)`, `## Reglas de negocio acordadas en esta tarea` y `## Carpetas/archivos huérfanos`, ver `Tareas de implementacion/plantilla-tarea.md`) que **se llenan en el momento en que ocurre cada hallazgo**, no recién al cerrar — igual que el Registro de decisiones. Si una regla de negocio nueva contradice una ya escrita en un flujo, el agente pregunta a Victor ahí mismo, valida la respuesta, la escribe en el apartado y recién entonces continúa (repite el ciclo si no queda resuelto). Al cerrar la tarea, cada entrada ya registrada se traslada a su destino final: mejoras de trabajo a `Mejoras continuas/`, reglas de negocio directo al Flujo correspondiente, huérfanos reportados a Victor (en `pg_control_proyectos` y `py_control_proyectos_web`, sin borrar nada por su cuenta). Así, una tarea ya cerrada no necesita releerse: lo vigente ya está en su destino final — evita leer la misma información dos veces.

## Inicio de tarea con Orquestador

Cuando Victor pide trabajar con el flujo de Orquestador (frase de activación y roles en [00-sistema/roles-y-flujo.md](00-sistema/roles-y-flujo.md)):

1. Leer [00-sistema/roles-y-flujo.md](00-sistema/roles-y-flujo.md), [00-sistema/convenciones-de-trabajo.md](00-sistema/convenciones-de-trabajo.md) y [00-sistema/gestion-de-sesiones-y-contexto.md](00-sistema/gestion-de-sesiones-y-contexto.md).
2. Crear el archivo de la tarea en [Tareas de implementacion/](Tareas%20de%20implementacion/) con la plantilla mínima de esa carpeta, nombrado `YYYY-MM-DD-<tema>.md`.
3. Cada tarea registra en su propio archivo: entorno (local/nube), chats usados, ramas y worktrees asignados, su Registro de decisiones y sus resultados/cierre.
4. Este tipo de tarea es de implementación única: no sigue el ciclo de `Mejoras continuas/` de abajo (sin Punch List interactiva, sin sección `## Resultados` + `CERRADO 100%`); se cierra según su propia sección `## Cierre`.

## Ciclo de vida de una tarea de implementación (lote con Punch List)

> Antes se llamaba "ciclo de vida de un archivo de Mejoras continuas"; se corrigió el 2026-09-23 porque esto es trabajo de Workers (tarea de implementación), no un aprendizaje — por eso estos archivos viven en `Tareas de implementacion/`.

Un archivo = un objetivo declarado por Victor, no un día del calendario.

1. Victor pide algo concreto (pantallas, comportamiento).
2. Se abre el archivo vigente con ese objetivo (o se crea uno nuevo si no hay ninguno abierto), nombrado `YYYY-MM-DD-<tema>.md` con la fecha del día en que se declaró el objetivo, en `Tareas de implementacion/`.
3. Se implementa en `py_control_proyectos_web`, solo el flujo indicado.
4. Se verifica con la **Punch List de Mejoras** (ver abajo) — no con una tabla dentro del .md.
5. Mientras algún ítem de la Punch List no esté Conforme, el archivo sigue abierto y se le sigue agregando avance (nuevas fechas de sesión dentro del mismo archivo).
6. Cuando todos los ítems quedan Conforme en la Punch List, el archivo se cierra: se agrega la sección `## Resultados` con el resumen final y se marca `CERRADO 100%`. No se vuelve a tocar, salvo la excepción de "Mejoras a flujos" de abajo.
7. Antes de cerrar, se completan los apartados `## Mejoras (de trabajo)` y `## Reglas de negocio acordadas en esta tarea` (ver "Diferencia..." arriba) — "ninguna" si no aplica. Las mejoras de trabajo se extraen a un archivo nuevo en `Mejoras continuas/`; las reglas de negocio se integran directo en el Flujo de trabajo correspondiente (nunca quedan solo anotadas en la tarea). La tarea de implementación no se borra ni se resume — queda íntegra en `Tareas de implementacion/`, con la referencia de a dónde se trasladó cada hallazgo.
8. Solo cuando Victor pide explícitamente un objetivo nuevo se crea el siguiente archivo, con la fecha de ese momento.

**No debe existir una memoria de sesión aparte** (tipo `memoria-sesion.md`). Todo pendiente y todo lo ya hecho vive dentro del o los archivos de `Tareas de implementacion/` que sigan abiertos — un solo lugar, sin duplicar.

## Tareas futuras

> Renombrado el 2026-09-23 (antes "Mejoras futuras" en `Mejoras continuas/`): el nombre anterior contradecía la distinción entre Tareas de implementación y Mejoras continuas (ver esa sección abajo) — es un backlog de trabajo de implementación pospuesto, no de aprendizajes.

[`Tareas de implementacion/tareas-futuras.md`](Tareas%20de%20implementacion/tareas-futuras.md) es un archivo permanente. No es una tarea con Plan/Punch List/Cierre como las demás de esa carpeta, ni un lote de `Mejoras continuas/`: no lleva checklist ni se cierra. Ahí se lista trabajo de implementación de alguna sesión u otro archivo que **Victor indica explícitamente** que se pospone a futuro, sin fecha de retomar. Cada ítem anota de dónde salió, en qué consiste y por qué se pospuso. Cuando Victor decide retomar un ítem, se saca de ahí y se abre como archivo de tarea nuevo en `Tareas de implementacion/` con la fecha del día en que se retoma. El agente no decide por su cuenta mover algo aquí — solo cuando Victor lo pide.

## Verificación en vivo — Punch List de Mejoras

El checklist de cada lote **no es una tabla en el .md** — es este artifact interactivo, con guardado en la nube:

**https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd**

Cada lote (tab) tiene sus ítems con estado **Conforme / Observado / Sin verificar**, comentario y capturas de pantalla pegadas (Ctrl+V). Victor lo usa mientras prueba en la app real. Al crear un nuevo lote de implementación, se agrega ahí como checklist nuevo (botón "+ Nueva mejora"). El .md correspondiente (en `Tareas de implementacion/`) solo registra el resultado final una vez que la Punch List queda toda en Conforme.

## Reglas de negocio detectadas durante la implementación

Cada archivo de `Tareas de implementacion/` termina con el apartado `## Reglas de negocio acordadas en esta tarea` (puede quedar vacío). Si durante o después de implementar el agente detecta que un `Flujo de trabajo` ya establecido debería actualizarse, agregarse o entra en conflicto con lo implementado (p. ej. un punto que Victor aprobó afecta o amplía una regla ya documentada):

1. El agente **no edita el flujo por su cuenta** sin haberlo consultado.
2. Propone a Victor: qué flujo, qué regla, por qué (nueva regla, o cambio sobre una existente).
3. Solo si Victor confirma, se integra la regla **directo en la estructura del flujo** correspondiente — en la sección donde encaja, no pegada al final. Si contradice una regla ya escrita, se modifica lo existente con lo acordado, no quedan las dos versiones.
4. Se anota en el apartado de la tarea que ya se aplicó (con el enlace al flujo).

Así el sistema (los Flujos de trabajo) se corrige y crece cuando la implementación real lo exige, siempre integrado en el documento del flujo — nunca como una nota aparte en otro lugar.

## Ramas de trabajo

El repositorio está en GitHub. Por defecto se trabaja directo en `main` (así se ha trabajado hasta ahora). Se usa una rama solo cuando Victor lo pide explícitamente para ese cambio.

Para tareas ejecutadas con el flujo de Orquestador existe además un pool persistente de ramas `work-N` reservado para Workers (ver [00-sistema/convenciones-de-trabajo.md](00-sistema/convenciones-de-trabajo.md)). Fuera de ese flujo, la norma de trabajar directo en `main` no cambia.

## Qué leer al iniciar sesión

Cuando Victor dice **"inicia sesión en control de proyectos"**:

1. Leer **todos los archivos de `Tareas de implementacion/` que sigan abiertos** (sin `CERRADO 100%` ni `## Cierre` completado) → ahí está en qué quedó el proyecto: qué está hecho y qué falta. Puede ser más de uno si hay varios frentes abiertos.
2. Leer **todos** los archivos de `Flujos de trabajo/` → contexto general del sistema completo.
3. No leer `visual-companion/` salvo que la tarea sea de diseño/verificación de UI.
4. Responder con: pendientes de esas sesiones abiertas + contexto general del sistema.

## Qué hace el agente al cerrar sesión

Cuando Victor dice **"cierra sesión en control de proyectos"**:

1. Actualizar el o los archivos de `Tareas de implementacion/` tocados en la sesión: avance real, estado de la Punch List, y los apartados `## Mejoras (de trabajo)` y `## Reglas de negocio acordadas en esta tarea` con cualquier hallazgo de la sesión.
2. Mejoras de trabajo con contenido nuevo → extraer a un archivo en `Mejoras continuas/`. Reglas de negocio con contenido nuevo → consultar a Victor e integrarlas directo en el Flujo de trabajo correspondiente (ver "Diferencia..." y "Ciclo de vida" arriba).
3. Todo se guarda **ahí, en ningún otro archivo** — no se crea ninguna memoria de sesión aparte.
4. Confirmar a Victor qué se guardó y listar los pendientes para la siguiente sesión.
