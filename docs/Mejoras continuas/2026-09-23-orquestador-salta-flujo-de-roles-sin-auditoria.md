# Mejora de trabajo — el Orquestador se saltó el flujo de roles y eso costó documentación completa

> Origen: [2026-09-23-cronograma-import-y-versatilidad-vinculo.md](../Tareas%20de%20implementacion/2026-09-23-cronograma-import-y-versatilidad-vinculo.md). Registrado el 2026-09-23.
>
> **Registrado por:** Claude (agente que actuó como Orquestador en esa sesión).

## Qué pasó

Victor pidió trabajar "con agente orquestador" para dos tareas (fix del import de cronograma + versatilidad del vínculo partida↔tarea). El Orquestador hizo el diagnóstico, armó el plan, lo hizo aprobar por Victor — y hasta ahí, correcto. El error fue lo que siguió: en vez de asignar la implementación a un Worker real (chat propio, rama `work-N`, worktree, ver `docs/00-sistema/roles-y-flujo.md`), **el propio Orquestador implementó las dos tareas** directamente en su mismo chat, sin preguntarle antes a Victor si eso estaba bien.

La sesión sí tenía la herramienta para crear una sesión nueva de verdad (`create_session`), equivalente a abrir un chat de Worker separado — no se usó. Se decidió por cuenta propia que la tarea era "manejable" para hacerla directo, sin plantear esa opción a Victor primero.

## Consecuencia (por qué esto no es un detalle menor)

Saltarse la separación de roles no ahorró trabajo real: **hizo desaparecer todo lo que el proceso normal habría dejado registrado.**

- **No hubo Auditor.** Nadie revisó el plan, el código ni los resultados contra el plan aprobado antes de reportarlo como listo.
- **No hubo verificación real.** El código se probó con type-check, lint y tests unitarios — nunca contra la app real con Playwright (Victor lo señaló explícitamente después: *"cuando vuelvas a verificar lo que te digo que no funciona no lo hagas desde el código sino usa MCP playwright"*).
- **No se registraron reglas de negocio en el momento en que ocurrieron.** La regla del 100% de metrado asignado se anotó en el `Registro de decisiones` de la tarea, pero no se integró a `docs/Flujos de trabajo/15-cronograma.md` como exige el flujo — porque no hubo el punto de control (Auditor) que normalmente fuerza ese traslado antes de cerrar.
- **No hubo mejora continua registrada en el momento.** Esta misma entrada es la prueba: se está escribiendo *después*, a pedido explícito de Victor, en vez de haber ocurrido como parte natural del cierre de la tarea con Auditor.
- **En resumen: un error grave sin documentación no deja nada aprendido.** Ni una regla de negocio corregida, ni un aprendizaje de método, ni una auditoría que hubiera podido atrapar esto antes — todo el ciclo de aprendizaje del sistema depende de que los roles se respeten, no es una formalidad.

## Causa raíz

El Orquestador juzgó unilateralmente que la tarea era "simple" y decidió implementarla él mismo, sin plantearle esa opción a Victor.

## Corrección aplicada

Se agregó una prohibición explícita en `docs/00-sistema/roles-y-flujo.md` § Orquestador → Límites: el Orquestador nunca implementa directamente así juzgue la tarea trivial; si lo considera, debe decírselo a Victor y esperar su autorización explícita — nunca decidirlo solo. Única excepción: que Victor haya indicado desde el inicio de la sesión que el propio Orquestador debe implementar.
