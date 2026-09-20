# docs — orquestador de esta carpeta

Este archivo ordena **solo `docs/`**. La fuente normativa de todo el repositorio sigue siendo [AGENTS.md](../AGENTS.md) — este archivo existe porque AGENTS.md deriva aquí para saber cómo moverse dentro de `docs/`.

Aquí es donde se trabaja. Lo demás en la raíz del repositorio (`conocimiento/`, `Sistema hibrido/`, `Informacion para pruebas/`, `Formatos/`, etc.) es material de apoyo/referencia, no el flujo activo de trabajo.

## Qué hay y para qué sirve cada cosa

| Carpeta | Qué es | Se lee para contexto general |
|---|---|---|
| [Flujos de trabajo/](Flujos%20de%20trabajo/) | Los conceptos/temas permanentes del sistema (uno por archivo numerado). Es la fuente de verdad de cada tema. | Sí — todos |
| [Mejoras continuas/](Mejoras%20continuas/) | Bitácora real del trabajo, en archivos con fecha. Ver ciclo de vida abajo. | Solo el de fecha más reciente |
| [visual-companion/](visual-companion/) | `design.md` es el sistema de diseño obligatorio (layout, tokens, componentes, columnas, accesibilidad) para crear o modificar cualquier interfaz. El resto son mockups HTML que fijan cómo se ve y cómo se llama cada pantalla (nomenclatura, campos). Referencia de UI, no de pendientes. | No, salvo tarea de diseño de UI — ahí `design.md` es lectura obligatoria, no opcional |

## Ciclo de vida de un archivo de Mejoras continuas

Un archivo = un objetivo declarado por Victor, no un día del calendario.

1. Victor pide algo concreto (pantallas, comportamiento).
2. Se abre el archivo vigente con ese objetivo (o se crea uno nuevo si no hay ninguno abierto), nombrado `YYYY-MM-DD-<tema>.md` con la fecha del día en que se declaró el objetivo.
3. Se implementa en `py_control_proyectos_web`, solo el flujo indicado.
4. Se verifica con la **Punch List de Mejoras** (ver abajo) — no con una tabla dentro del .md.
5. Mientras algún ítem de la Punch List no esté Conforme, el archivo sigue abierto y se le sigue agregando avance (nuevas fechas de sesión dentro del mismo archivo, como en `2026-08-29-orden-recursos-antes-rdt.md`).
6. Cuando todos los ítems quedan Conforme en la Punch List, el archivo se cierra: se agrega la sección `## Resultados` con el resumen final y se marca `CERRADO 100%` (como en `2026-08-23-...md`). No se vuelve a tocar, salvo la excepción de "Mejoras a flujos" de abajo.
7. Antes de cerrar, se completa la sección `## Mejoras a flujos` (ver abajo) — puede quedar vacía si no aplicó nada.
8. Solo cuando Victor pide explícitamente un objetivo nuevo se crea el siguiente archivo, con la fecha de ese momento.

**No debe existir una memoria de sesión aparte** (tipo `memoria-sesion.md`). Todo pendiente y todo lo ya hecho vive dentro del o los archivos de `Mejoras continuas/` que sigan abiertos — un solo lugar, sin duplicar.

## Mejoras futuras

[`Mejoras continuas/mejoras-futuras.md`](Mejoras%20continuas/mejoras-futuras.md) es un archivo permanente — siempre el **último** de `Mejoras continuas/` (sin fecha en el nombre a propósito, para quedar al final en cualquier listado). No es un lote: no lleva checklist ni se cierra. Ahí se listan mejoras de alguna sesión u otro archivo que **Victor indica explícitamente** que se posponen a futuro, sin fecha de retomar. Cada ítem anota de dónde salió, en qué consiste y por qué se pospuso. Cuando Victor decide retomar un ítem, se saca de ahí y se abre como archivo nuevo de `Mejoras continuas/` con la fecha del día en que se retoma. El agente no decide por su cuenta mover algo aquí — solo cuando Victor lo pide.

## Verificación en vivo — Punch List de Mejoras

El checklist de cada lote **no es una tabla en el .md** — es este artifact interactivo, con guardado en la nube:

**https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd**

Cada lote (tab) tiene sus ítems con estado **Conforme / Observado / Sin verificar**, comentario y capturas de pantalla pegadas (Ctrl+V). Victor lo usa mientras prueba en la app real. Al crear un nuevo lote de Mejoras continuas, se agrega ahí como checklist nuevo (botón "+ Nueva mejora"). El .md correspondiente solo registra el resultado final una vez que la Punch List queda toda en Conforme.

## Mejoras a flujos detectadas durante la implementación

Cada archivo de `Mejoras continuas/` termina con un apartado `## Mejoras a flujos` (puede quedar vacío). Si durante o después de implementar un punto del lote el agente detecta que un `Flujo de trabajo` ya establecido debería mejorarse o entra en conflicto con lo implementado (p. ej. un punto que Victor aprobó afecta una regla ya documentada en un flujo):

1. El agente **no edita el flujo directamente**.
2. Registra ahí la propuesta: qué flujo, qué cambiaría, por qué.
3. Se lo consulta a Victor.
4. Solo si Victor confirma que sí procede (al analizarlo), se actualiza el archivo del flujo correspondiente, y se anota en este mismo apartado que ya se aplicó.

Así no solo se implementa: el sistema (los Flujos de trabajo) también se corrige cuando la implementación real lo exige.

## Ramas de trabajo

El repositorio está en GitHub. Por defecto se trabaja directo en `main` (así se ha trabajado hasta ahora). Se usa una rama solo cuando Victor lo pide explícitamente para ese cambio.

## Qué leer al iniciar sesión

Cuando Victor dice **"inicia sesión en control de proyectos"**:

1. Leer **todos los archivos de `Mejoras continuas/` que sigan abiertos** (sin `CERRADO 100%`) → ahí está en qué quedó el proyecto: qué está hecho y qué falta. Puede ser más de uno si hay varios frentes abiertos.
2. Leer **todos** los archivos de `Flujos de trabajo/` → contexto general del sistema completo.
3. No leer `visual-companion/` salvo que la tarea sea de diseño/verificación de UI.
4. Responder con: pendientes de esas sesiones abiertas + contexto general del sistema.

## Qué hace el agente al cerrar sesión

Cuando Victor dice **"cierra sesión en control de proyectos"**:

1. Actualizar el o los archivos de `Mejoras continuas/` tocados en la sesión: avance real, estado de la Punch List, y el apartado `## Mejoras a flujos` con cualquier pendiente detectado.
2. Todo se guarda **ahí, en ningún otro archivo** — no se crea ninguna memoria de sesión aparte.
3. Confirmar a Victor qué se guardó y listar los pendientes para la siguiente sesión.
