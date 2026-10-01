# F0-U1 · Maquetas con los tres paneles (Importar DP, Cronograma, Paquetes) y regla de alineación de tablas

Lee primero `00-reglas-de-contexto.md`. **Carril de diseño**: trabajas en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos` (rama `main`), sin worktree de la app. Escribes solo en `docs/05-diseno-y-referencias/**` (más tu `resultados/F0-U1.md`). Commit en `main` con `git add` explícito; sin push. Nunca incluyas `Trazabilidad.xlsx` ni el archivo de progreso. Otro Worker (F0-U2) trabaja a la vez en `plan-maestro-tres-paneles.html`, `plan-maestro-lienzo.html` y `crear-rdt-selector-paquetes.html`: **no los toques**; si el commit falla por bloqueo del índice de git, espera unos segundos y repite. Meta: ~60 llamadas, ≤ 200k de contexto.
**Origen:** indicaciones de Victor del 2026-09-30. **Bloquea:** F1-C y F2-B (esperan estas maquetas aprobadas).

## Cómo trabajar (para no pasar de contexto)

F0-R llegó a 245k por reescribir maquetas enteras. Aquí **no reescribas**: lee una vez el marco (`mockups/plan-maestro-tres-paneles.html`: CSS líneas 7-198, constructores de paneles en el script desde la línea 277) y mete el contenido central actual de cada maqueta dentro de ese marco con **ediciones puntuales** (Edit). No releas un archivo ya leído. Sigue la convención de las maquetas existentes (archivos que abren con doble clic); si extraes el marco a un archivo compartido, debe abrir igual desde `file://`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse |
|---|---|
| F0U1-1 | `importar-dp-niveles`, `cronograma-niveles`, `paquetes-declarar` y `paquetes-agrupar` muestran **los tres paneles como en la app**: izquierdo (navegación), centro (el contenido ya aprobado, sin cambiar su lógica ni sus textos) y derecho (accesos rápidos), con el mismo marco, rótulos, iconos de ocultar/mostrar (esquina superior interior del encabezado), asistente flotante y vista móvil en cajón que `plan-maestro-tres-paneles.html`. Los rótulos y accesos salen de ese marco (que a su vez sale de la app): no inventes ninguno. Cada maqueta marca como activo el acceso que corresponde a su pantalla, solo si ese acceso existe en el marco |
| F0U1-2 | **Estado de paneles por pantalla:** `paquetes-declarar` abre con **ambos paneles ocultos** (iconos visibles para mostrarlos; el centro toma el ancho; es la regla de su encargo original); las otras tres abren con los tres abiertos. En las cuatro se pueden alternar los paneles y el centro no se deforma. Si las tablas del centro se aprietan con los tres abiertos, conserva el **scroll horizontal** sin perder contexto (`design.md` §8) |
| F0U1-3 | **Alineación de tablas (regla de Victor, para todas las pantallas):** el encabezado de cada columna va **sobre su dato y alineado igual**: texto a la izquierda; numéricos, porcentajes, montos y unidades a la **derecha**, con el encabezado también a la derecha. **No dar ancho de más** a una columna cuyo dato no lo necesita («Und.», «Met.», «%», códigos cortos): ancho justo al contenido, y el espacio sobrante a la columna de texto largo. Hoy «Und.» y «Met.» tienen el encabezado a la izquierda y el dato a la derecha, separados (captura de Victor). Corrige **todas las tablas de las cuatro maquetas de esta tanda** (incluidas las de Niveles y las de partidas del cuadro de paquetes) |
| F0U1-4 | `design.md`: regla nueva de alineación de tablas (en §5 «Tablas», con un ejemplo correcto y uno incorrecto en una línea cada uno, y añadida al checklist de §11), y una línea en §3 que diga que **toda maqueta del plan se muestra con los tres paneles** (marco de `plan-maestro-tres-paneles.html`). Versión 1.9.0 y §15. Las pantallas ya existentes de la app quedan fuera de este plan (se unificarán en un plan aparte) |
| F0U1-5 | `mockups/index.html` y `mockups/README.md` al día: las cuatro maquetas «con los tres paneles, pendiente de revisión de Victor»; `plan-maestro-lienzo.html` pasa a «reemplazada por `plan-maestro-tres-paneles.html`» (F0-U2 le pone la redirección; tú solo el texto del índice y del README); `crear-rdt-selector-paquetes.html` «con los tres paneles (F0-U2)» |
| F0U1-6 | `resultados/F0-U1.md`: estados, handoff y **máx. 3 preguntas para Victor** (lenguaje simple, sin códigos internos, una decisión por pregunta, con ejemplo y recomendación). Hallazgos clasificados en los cuatro grupos de las reglas |

## Qué NO hacer

- No tocar código de la app ni crear ramas. No editar flujos de `04-flujos-de-negocio/`. No cambiar la lógica, los datos de ejemplo ni las decisiones ya aprobadas de esas cuatro maquetas: solo el marco y la alineación. No decidir lo que no esté aquí: va a las preguntas.
- No uses navegador (el Orquestador las abre para Victor): revisa por lectura y con `node --check` de los scripts. El resultado queda `Observado` hasta que Victor las vea.
- Sin credenciales.

## Cierre

Skills: lista `.claude/skills/` de ambos repositorios (el de la app no tiene) y usa `cerrar-tanda` al terminar (estados y traspaso en `resultados/F0-U1.md`). Mensaje final: ítems cerrados, pendientes, preguntas y llamadas.
