# F0-U2 · Maquetas con los tres paneles (Plan Maestro y Crear RDT) y color del avance real a la vista

Lee primero `00-reglas-de-contexto.md`. **Carril de diseño**: trabajas en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos` (rama `main`), sin worktree de la app. Escribes solo en `docs/05-diseno-y-referencias/mockups/plan-maestro-tres-paneles.html`, `plan-maestro-lienzo.html`, `crear-rdt-selector-paquetes.html` y tu `resultados/F0-U2.md`. **No edites `design.md`, `index.html` ni `README.md`** (los edita F0-U1, que corre a la vez): lo que falte ahí, anótalo en tu resultado. Commit en `main` con `git add` explícito; sin push; si falla por bloqueo del índice de git, espera unos segundos y repite. Nunca incluyas `Trazabilidad.xlsx` ni el archivo de progreso. Meta: ~60 llamadas, ≤ 200k de contexto.
**Origen:** indicaciones de Victor del 2026-09-30. **Bloquea:** F3-C, F3-D y F4-C.

## Cómo trabajar (para no pasar de contexto)

No reescribas maquetas enteras (F0-R llegó a 245k). Usa ediciones puntuales (Edit); lee cada archivo una vez. Lee `design.md` solo con `offset`/`limit`: §4.1.2 (color de avance, F0-S), §5 «Tablas» y «Lienzo del Plan Maestro». El marco de tres paneles ya está en `plan-maestro-tres-paneles.html`; para Crear RDT cópialo de ahí (misma estructura, rótulos e iconos).

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse |
|---|---|
| F0U2-1 | **Crear RDT con los tres paneles:** `crear-rdt-selector-paquetes.html` (la pantalla real de Crear RDT con todas sus secciones y el cuadro «Elegir actividad del Plan Maestro») queda dentro del marco: panel izquierdo (con «Crear RDT» activo), centro (el contenido actual, sin quitar ningún dato) y panel derecho, con iconos de ocultar/mostrar, asistente flotante y cajón en móvil. Abre con los tres paneles abiertos y se pueden alternar sin deformar el centro (scroll horizontal en tablas anchas) |
| F0U2-2 | **El lienzo es una sola maqueta con marco:** `plan-maestro-tres-paneles.html` es la maqueta vigente del Plan Maestro. `plan-maestro-lienzo.html` (solo centro) se **conserva sin borrar**, pero pasa a ser una página mínima con el aviso «Reemplazada por la maqueta con los tres paneles» y redirección (`meta refresh` más enlace) a `plan-maestro-tres-paneles.html`. Antes de reducirla, comprueba que todo su contenido ya está en la otra (estados con datos, vacío, cargando y error; anexo de 4 semanas; personalizar campos; móvil); si falta algo, pásalo |
| F0U2-3 | **Color del avance real a la vista principal del lienzo (Victor no lo vio):** en la vista principal, **en las filas «Real»** y en el **físico acumulado real** (el semanal solo si no estorba; si dudas, déjalo solo en el acumulado y pregúntalo): 0 % en blanco (texto normal), en curso (> 0 y < 100) en amarillo, 100 % en verde, con los tokens de `design.md` §4.1.2 (`text-amber-400`, `text-emerald-400`); **nunca** se colorea lo programado (filas «Prog.»), ni montos, ni metrados. El color no es la única señal: el número va escrito y hay una **leyenda breve visible junto a la tabla**. Los datos simulados de la vista principal deben incluir de verdad los tres casos (una partida sin ejecutar, una en curso, una al 100 %) para que se vea. Mismo criterio en el nivel de paquete y en el total del servicio |
| F0U2-4 | **Color del avance real en Crear RDT:** en el cuadro «Elegir actividad del Plan Maestro» (porcentaje de cada partida y del paquete) y en la columna de avance de la actividad, la misma regla y una fila de cada caso |
| F0U2-5 | **Alineación de tablas** en todas las tablas de estas dos maquetas: el encabezado de cada columna va **sobre su dato y alineado igual** (texto a la izquierda; numéricos, porcentajes, montos y unidades a la **derecha**, encabezado también a la derecha). **No dar ancho de más** a una columna cuyo dato no lo necesita («Und.», «Met.», «%», códigos): ancho justo, y el sobrante a la columna de texto largo. Hoy «Und.» y «Met.» tienen el encabezado a la izquierda y el dato a la derecha, separados (captura de Victor). En el lienzo, los seis subencabezados de cada semana también van sobre su dato |
| F0U2-6 | `resultados/F0-U2.md`: estados, handoff, **qué debe agregar F0-U1 o el Orquestador en `design.md`/índice/README** si algo cambió, y **máx. 3 preguntas para Victor** (lenguaje simple, sin códigos internos, una decisión por pregunta, con ejemplo y recomendación). Hallazgos clasificados en los cuatro grupos de las reglas |

## Qué NO hacer

- No tocar código de la app ni crear ramas. No editar flujos. No cambiar los cálculos, datos ni decisiones ya aprobadas del lienzo y del selector: solo marco, color y alineación. No decidir lo que no esté aquí: va a las preguntas.
- No uses navegador (el Orquestador las abre para Victor): revisa por lectura y con `node --check`. Queda `Observado` hasta que Victor las vea.
- Sin credenciales.

## Cierre

Skills: lista `.claude/skills/` de ambos repositorios (el de la app no tiene) y usa `cerrar-tanda` al terminar (estados y traspaso en `resultados/F0-U2.md`). Mensaje final: ítems cerrados, pendientes, preguntas y llamadas.
