---
name: cerrar-tanda
description: Cierra una tanda de trabajo de un plan grande con la misma secuencia siempre: estados de la lista de ítems, evidencia, traspaso breve, revisión de fuentes de verdad y commit verificado. Úsalo al terminar cada tanda.
---

# Cerrar una tanda de trabajo

Aplica a cualquier plan dividido en tandas con una lista de ítems, un archivo de evidencia y un archivo de progreso.

## Pasos

1. **Estados de la lista de ítems, fila por fila.** Por cada ítem de la tanda, busca su identificador y edita solo esa fila. Nunca uses scripts de reemplazo masivo sobre el plan, el índice ni la evidencia; si hace falta automatizar, guarda antes una copia o un commit del estado previo.
2. **Estados permitidos:** Conforme (con evidencia real), Observado (con la causa y quién lo resuelve) o No aplica (con el motivo). No marques Conforme sin haberlo verificado.
3. **Evidencia.** Escribe en el archivo de evidencia qué se comprobó, con qué comando o pantalla y el resultado real, con enlace a capturas si las hay.
4. **Traspaso breve** (máximo 15 líneas) en el archivo de progreso, o en el resumen de cierre propio de la tanda si el plan lo manda así (con varios trabajadores a la vez, nadie edita los archivos compartidos del plan): tanda, ítems con estado, archivos tocados, comandos de verificación con resultado, hallazgos, pendientes.
5. **Hallazgos.** Clasifica cada hallazgo en uno de cinco grupos (mejora de trabajo, regla de negocio acordada, observación sobre la política, archivo o carpeta huérfano, conflicto o pregunta para el responsable humano). Una pregunta de negocio no espera a este paso: se devuelve al orquestador en el momento.
6. **Fuentes de verdad revisadas.** Anota la frase «Fuentes de verdad revisadas: …» con las que se actualizaron y las que quedan pendientes de decisión. El trabajador no edita las fuentes centrales; las deja anotadas.
7. **Limpieza.** Borra temporales y carpetas de snapshots del navegador; comprueba con `git status` que solo quedan los cambios esperados.
8. **Commit.** Añade los archivos de uno en uno (`git add <ruta>`, nunca `git add .`), con un mensaje que nombre la tanda. Verifica con `git branch --contains <commit>` y `git log` que el commit está en la rama correcta.
9. **Push** solo según la política del repositorio (la rama del trabajador con la cadencia acordada; el código a `main` solo con autorización).

## Reglas

- Sin credenciales en ningún archivo.
- Una tanda no se cierra si dejó algo a medias en un ítem.
- Si algo no se pudo verificar, queda como Observado con la limitación escrita.
