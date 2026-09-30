# F0-S · Posición de los iconos de los paneles y color de los porcentajes de avance

Lee primero `00-reglas-de-contexto.md`. **Carril de diseño**: trabajas en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos` (rama `main`), sin worktree de la app. Escribes solo en `docs/05-diseno-y-referencias/**` (más tu `resultados/F0-S.md`). Commit en `main` con `git add` explícito; sin push. Nunca incluyas `Trazabilidad.xlsx` ni el archivo de progreso.
**Origen:** dos indicaciones de Victor del 2026-09-30, después de F0-R. **Bloquea:** las tandas de interfaz (F1-C, F2-B, F3-C, F3-D, F4-C). Tanda corta: meta ~40 llamadas.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse |
|---|---|
| F0S-1 | **Posición del icono de ocultar/mostrar en las maquetas de paneles y del lienzo.** Así se ven los tres paneles en toda la app (captura de Victor): el **panel izquierdo** (navegación) lleva el icono en la **esquina superior derecha de su encabezado**, a la altura del título «Control de Proyectos»; el **panel derecho** (accesos rápidos) lo lleva en la **esquina superior izquierda de su encabezado**, a la altura de «ACCESOS RÁPIDOS». Es decir, en el borde interior y en la franja del encabezado, no a media altura. Con el panel oculto, el icono sigue visible en esa misma esquina. Mismo icono, tamaño y estilo en todas las pantallas. Lee (solo lectura) `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\src\components\ui\WorkspaceShell.tsx` para respetar la estructura real de los tres paneles y sus anchos; no inventes componentes |
| F0S-2 | **Color de los porcentajes de avance, solo en ejecución.** Regla: una partida (o paquete) **sin ejecutar aún = 0 %** se muestra con el número en **blanco** (color de texto normal); **en ejecución (mayor que 0 y menor que 100 %) = número en amarillo**; **al 100 % = número en verde**. Aplica **solo a porcentajes de avance** (no a montos ni metrados) y **solo durante la ejecución del servicio** (valores reales; en el lienzo, el físico del «Real», no el del «Prog.»). Usa los tokens semánticos que ya existen en `design.md` §4 (advertencia y éxito); no crees colores nuevos. El color nunca es la única señal: el número va siempre escrito y la leyenda lo explica |
| F0S-3 | Aplica la regla F0S-2 en las maquetas de este plan donde aparezca un porcentaje de avance real: el lienzo (filas «Real»), el cuadro «Elegir actividad del Plan Maestro» de Crear RDT (porcentaje de cada partida y del paquete) y, si hay alguno, Paquetes (Declarar y Agrupar). Incluye una fila de cada caso (0 %, en curso, 100 %) y una leyenda breve |
| F0S-4 | `design.md`: regla nueva (dónde vive, p. ej. junto a los tokens o a la tabla de porcentajes), con una línea que diga que las pantallas ya existentes de la app (PR, Dashboard, etc.) **no se modifican en este plan** y se unificarán en un plan aparte; y la posición de los iconos de los paneles (F0S-1). Versión 1.8.0 y §15. `mockups/index.html` y `mockups/README.md` al día |
| F0S-5 | `resultados/F0-S.md` con estados, handoff y **máx. 3 preguntas para Victor** (sin códigos internos; una decisión por pregunta, con ejemplo y recomendación) |

## Qué NO hacer

- No tocar código de la app ni crear ramas. No editar flujos de `04-flujos-de-negocio/`. No decidir lo que no esté aquí: va a las preguntas.
- No cambiar nada más de las maquetas aprobadas (F0-A, lienzo, selector del RDT): solo estos ajustes.
- Sin credenciales. No uses navegador: revisa por lectura (el Orquestador las abre para Victor al terminar).

## Cierre

Skills: lista `.claude/skills/` de ambos repositorios; usa `cerrar-tanda` al terminar (estados y traspaso en `resultados/F0-S.md`). Mensaje final: ítems cerrados, pendientes y llamadas.
