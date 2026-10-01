# F0-V · Corrección de la maqueta del Plan Maestro: color del avance real y barras de desplazamiento

Lee primero `00-reglas-de-contexto.md`. **Carril de diseño**: trabajas en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos` (rama `main`). Escribes solo en `docs/05-diseno-y-referencias/**` (más tu `resultados/F0-V.md`). Commit en `main` con `git add` explícito; sin push; nunca `Trazabilidad.xlsx`. Tanda corta: ~30 llamadas. Lee cada archivo una vez; ediciones puntuales.
**Origen:** Victor (2026-09-30, noche) revisó las maquetas: «todo está bien», salvo lo de abajo. Con esta corrección el Plan Maestro queda aprobado y arrancan las tandas de código (F3-C y F3-D esperan esta tanda).

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse |
|---|---|
| F0V-1 | **Color del avance físico real, que Victor NO ve en `plan-maestro-tres-paneles.html`.** F0-U2 dice haberlo puesto en el «Físico acum. (%)» de las filas «Real», pero no se ve. Averigua por qué (¿clase CSS sin efecto, color pisado por otra regla, fila Real plegada o de otra columna, el color solo aparece en un estado/semana que no se muestra por defecto, el dato simulado no cae en la vista inicial?) y corrígelo. Debe verse **a simple vista al abrir la maqueta**, sin hacer clic: en las filas «Real» de la vista principal, 0 % en blanco, en curso (> 0 y < 100) en **amarillo** y 100 % en **verde**; nunca lo programado. Hazlo evidente (que el color se note con el tema oscuro: usa los tokens de `design.md` §4.1.2, pero comprueba el contraste real). Para verificar sin navegador: carga el HTML en Node con un DOM mínimo, o razona el cascade con Grep de la regla y de la clase aplicada; deja en el resultado la evidencia concreta (la regla, la celda de ejemplo y el valor que la activa) |
| F0V-2 | **Barras de desplazamiento (horizontal y vertical) blancas:** no era su color original. Restaura el estilo anterior de las barras; si no se puede determinar, usa un tono **azulado** que combine con la paleta oscura actual (pista fina, pulgar azul grisáceo, más claro al pasar el cursor) con `scrollbar-color`/`scrollbar-width` y los `::-webkit-scrollbar*`. Aplícalo a **todas las maquetas del plan** (lo más simple: en `mockups/marco-tres-paneles.css` y en el CSS propio de `plan-maestro-tres-paneles.html` y `crear-rdt-selector-paquetes.html`; sin tocar nada más de ellas) y a los contenedores con scroll interno de las tablas. Registra la regla en `design.md` (§4 o §8; versión 1.9.1 y §15) |
| F0V-3 | **Importar DP: Und. y Met. en columnas separadas** (Victor respondió «no» a juntarlos en una sola columna «85.00 m3»): una columna «Und.» y otra «Met.», cada una con su encabezado sobre su dato, numérico a la derecha, ancho justo (regla de alineación de `design.md` 1.9.0) |
| F0V-4 | `plan-maestro-lienzo.html`: Victor aprobó convertirlo en página mínima con aviso «Reemplazada por la maqueta con los tres paneles» y redirección (`meta refresh` más enlace) a `plan-maestro-tres-paneles.html`. Inténtalo; si el sistema lo deniega, **no lo rodees**: déjalo anotado en tu resultado con el comando exacto |
| F0V-5 | `mockups/README.md` e `index.html`: las cuatro maquetas de F0-U1, Crear RDT y Plan Maestro quedan «aprobadas por Victor (2026-09-30)» (quita «pendiente de revisión»), salvo lo que no se haya podido cerrar. `resultados/F0-V.md` con estados, la evidencia de F0V-1 y llamadas; sin preguntas nuevas salvo bloqueo real |

## Qué NO hacer

- No tocar código de la app ni crear ramas; no editar flujos. No cambiar datos, cálculos ni decisiones ya aprobadas. Sin navegador (el Orquestador abre la maqueta para Victor). Sin credenciales.

## Cierre

Skills: lista `.claude/skills/` de ambos repositorios y usa `cerrar-tanda` (estados y traspaso en `resultados/F0-V.md`). Mensaje final: ítems cerrados, pendientes y llamadas.
