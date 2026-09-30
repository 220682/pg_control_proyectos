# F0-R · Ajustes a las maquetas tras la revisión de Victor

Lee primero `00-reglas-de-contexto.md`. **Carril de diseño**: trabajas en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos` (rama `main`), sin worktree de la app. Escribes solo en `docs/05-diseno-y-referencias/**` (más tu `resultados/F0-R.md`). Commit en `main` con `git add` explícito; sin push. Nunca incluyas `Trazabilidad.xlsx` ni el archivo de progreso.
**Origen:** decisiones de Victor del 2026-09-30 sobre F0-A y F0-B (registradas en el progreso, «Decisiones de Victor sobre las maquetas»). **Bloquea:** F1-C, F2-B, F3-C, F3-D y F4-C (esperan estas maquetas).

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse |
|---|---|
| F0R-1 | Las cuatro maquetas de F0-A (`importar-dp-niveles`, `cronograma-niveles`, `paquetes-declarar`, `paquetes-agrupar`) reflejan las seis respuestas aprobadas: (1) una fila de muestra por grupo de hermanas con botón «Ver N hermanas»; (2) las filas «para revisar» **bloquean** el botón de aprobar hasta resolverlas; (3) el restante por partida se ve en **ambas** listas; (4) la marca de paquete **alterna dos colores** entre paquetes contiguos, más el borde; (5) en pantallas angostas, **pestañas** para Cronograma y DP; (6) el plegado de un paquete **se reinicia** al abrir la pantalla. Quita «pendiente de aprobación» de esas cuatro en `design.md` y `mockups/README.md` (quedan aprobadas) |
| F0R-2 | **Lienzo del Plan Maestro** (aprobado por Victor; quita su «pendiente de aprobación»). Cambios: columna opcional **Disciplina** en «Personalizar campos» (además del BAC; ninguna otra); la línea divisoria usa el **amarillo de advertencia que ya existe**; la semana plegada se deja **como está hoy**; la columna de metrado se rotula **«Met.»** |
| F0R-3 | **Paneles ocultables**: no hay botones de texto en la barra. Un **solo icono por panel, dentro del propio panel y en su borde interior** (el lado que da al contenido), visible también con el panel oculto, sin deformar el panel izquierdo. Conserva el control para ocultar ambos si cabe sin distorsión; si no cabe, elimínalo y dilo |
| F0R-4 | **El asistente no ocupa espacio**: es un icono **flotante** sobre el contenido. Elimina la franja inferior reservada (4 rem) de todas las maquetas (lienzo, paneles) y la regla correspondiente de `design.md` §8; el lienzo aprovecha ese alto |
| F0R-5 | **Crear RDT: se usa la pantalla que ya existe, no una nueva.** Reescribe `mockups/crear-rdt-selector-paquetes.html` sobre la pantalla real: lee (solo lectura) `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\src\components\ui\FormularioCrearRdt.tsx` y parte de `mockups/crear-rdts.html`. Conserva **todas** sus secciones (identificación, reporte de avance, tareo de personal, equipos, materiales, observaciones, plantilla, cargar RDT). Mejora el diseño con los tokens de `design.md` sin quitar ningún dato. Conserva el cuadro «Elegir actividad del Plan Maestro» (paquetes plegables, partidas directas aparte, modo «por avance del paquete»), que a Victor le gusta, abierto desde el campo de partida de la actividad. Las horas **C/NC** y los **materiales** usan el mismo selector |
| F0R-6 | **Abreviaturas iguales en todas las pantallas del plan:** «Met.» (metrado), «Acum.», «Prog.», «Ejec.». En Crear RDT los tres encabezados quedan **«Met. acum.», «Met. prog.» y «Met. ejec.»**, completos, sin cortarse (hoy se ve «Metrado acum…»). Agrega la regla a `design.md` |
| F0R-7 | **Disciplina:** (a) en la maqueta de **crear paquete**, un selector de disciplina; (b) para la **partida directa** (sin paquete), un selector de disciplina; (c) columna opcional en el lienzo (F0R-2). El catálogo es **simulado** y rotulado así (Civil, Mecánica, Eléctrica, Instrumentación); la lista real la dará Victor. No edites flujos: el Orquestador los trata como regla nueva |
| F0R-8 | `design.md` (versión y §15), `mockups/index.html` y `mockups/README.md` actualizados y enlazados. `resultados/F0-R.md` con estados, handoff y **máx. 4 preguntas para Victor** en lenguaje simple |

## Qué mirar (solo lo necesario)

- Tus propias maquetas de F0-A y F0-B (ya commiteadas) y `design.md` (con `offset`/`limit` en las secciones que cambias).
- Flujo 19, solo la sección de clasificadores (Grep de «Disciplina»): la disciplina del paquete ya sale de un catálogo fijo.
- Capturas de Victor: no las tienes; sus observaciones están arriba.

## Qué NO hacer

- No tocar código de la app ni crear ramas. No editar flujos de `04-flujos-de-negocio/`. No decidir lo que no esté aquí: va a las preguntas.
- Sin credenciales. Verifica abriendo las maquetas en un navegador solo si el Orquestador te lo permite en el prompt; si no, revisa estructura y cálculos por lectura.

## Cierre

Skills: lista `.claude/skills/` de ambos repositorios; usa `cerrar-tanda` al terminar (estados y traspaso en `resultados/F0-R.md`). Mensaje final: ítems cerrados, pendientes y llamadas. Meta: ~80 llamadas.
