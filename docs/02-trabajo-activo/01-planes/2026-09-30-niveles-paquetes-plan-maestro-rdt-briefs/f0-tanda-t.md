# F0-T · Maqueta del Plan Maestro con los tres paneles reales

Lee primero `00-reglas-de-contexto.md`. **Carril de diseño**: trabajas en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos` (rama `main`), sin worktree de la app. Escribes solo en `docs/05-diseno-y-referencias/**` (más tu `resultados/F0-T.md`). Commit en `main` con `git add` explícito; sin push. Nunca incluyas `Trazabilidad.xlsx` ni el archivo de progreso. Meta: ~30 llamadas.
**Origen:** Victor pidió ver una maqueta del Plan Maestro con los **tres paneles como se ven en la app** (hoy el lienzo los muestra como cajas grises con un título). Captura de referencia de Victor: panel izquierdo de navegación (marca «Control de Proyectos», «Consolidado de servicio», bloque ACCIONES con Generar RQ, Crear RDT, Subir RDT, Crear paquete; bloque SERVICIO con Ficha del servicio; ACCIONES con Editar servicio y Editar checklist; pie con iconos, «VER COMO» y el usuario), centro con el contenido, y panel derecho («ACCESOS RÁPIDOS» con chips y «GRUPOS DEL SERVICIO» plegables: Planificación, Costos, Supervisión operativa con sus accesos, Logística).

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse |
|---|---|
| F0T-1 | Nueva maqueta `mockups/plan-maestro-tres-paneles.html`: pantalla completa con el panel izquierdo, el centro (el lienzo del Plan Maestro aprobado, reutilizando su contenido y cálculos de `plan-maestro-lienzo.html`) y el panel derecho, con **el contenido y el aspecto reales** de los paneles. Lee (solo lectura) `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\src\components\ui\WorkspaceShell.tsx` y los componentes de panel que use, y `design.md`; **no inventes** nombres ni accesos: toma los rótulos de la app y de las tablas del flujo 14 (Plan Maestro y sus acciones en el contexto de un servicio) |
| F0T-2 | Icono de ocultar/mostrar de cada panel en la esquina superior interior de su encabezado (izquierdo: a la derecha, junto a «Control de Proyectos»; derecho: a la izquierda, junto a «ACCESOS RÁPIDOS»), como define `design.md` §3. Cuatro estados seleccionables: los tres abiertos; solo el izquierdo oculto; solo el derecho oculto; ambos ocultos (el centro toma el ancho). Con el panel oculto el icono sigue visible y el centro no se deforma |
| F0T-3 | El asistente es un icono flotante sobre el contenido (sin franja reservada). Incluye los estados con datos, vacío, cargando y error del lienzo, y la vista móvil (390 px), donde los paneles son cajón y no llevan el icono nuevo |
| F0T-4 | `mockups/index.html` y `mockups/README.md` enlazan la maqueta (marcada «pendiente de revisión de Victor»); `design.md` solo si hace falta aclarar algo (sube versión en ese caso). `resultados/F0-T.md` con estados, handoff y **máx. 3 preguntas para Victor** |

## Qué NO hacer

- No tocar código de la app ni crear ramas; no editar flujos. No cambiar las maquetas ya aprobadas (esta es nueva; el lienzo anterior se conserva).
- Sin credenciales; no uses navegador: revisa por lectura y con `node --check` de los scripts.

## Cierre

Skills: lista `.claude/skills/` de ambos repositorios; usa `cerrar-tanda` (estados y traspaso en `resultados/F0-T.md`). Mensaje final: ítems cerrados, pendientes y llamadas.
