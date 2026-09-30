# Resultados F0-A · Maquetas de Niveles y de Paquetes de Trabajo

Carril de diseño, `main` de `pg_control_proyectos`. Retomó el trabajo parcial del commit d0b700e (revisado ítem por ítem, sin rehacer). Sin push.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada), verificar-permisos-por-rol (no aplica: sin permisos), seguir-flujo-de-planes (del Orquestador). Repositorio de la app: sin carpeta de Skills.

## Estado de ítems
| ID | Estado | Evidencia |
|---|---|---|
| F0A-1 | Conforme | `mockups/importar-dp-niveles.html`: ejemplos de 4 y 5 niveles, fila de muestra por grupo con desplegable de rol, filas «Para revisar», «Aprobar niveles», aviso de recarga (bloqueo duro con plan aprobado; lista de lo que se perdería y confirmación sin él). Revisado por estructura (grep), sin navegador |
| F0A-2 | Conforme | `mockups/cronograma-niveles.html`: mismo patrón con roles propios del cronograma, hitos y servicio implícito |
| F0A-3 | Conforme | `mockups/paquetes-declarar.html`: cronograma con columna Metrado, partida pre-llenada («auto»), hitos atenuados, restante por partida; DP solo partidas en consulta; ejemplo 06.03.01 a 06.03.07 |
| F0A-4 | Conforme | `mockups/paquetes-agrupar.html`: botón «Crear paquete», casillas, marca de paquete, flechas y Alt + flecha, plegar, ejemplo 1 (01–06 agrupadas, 07 directa) y ejemplo 2 (partida repartida 250 + 170 = 420 m3) |
| F0A-5 | Conforme | En las cuatro: secciones vacío, cargando (`aria-busy`), error (`role="alert"`), `@media` y vista 390 px, `th scope`, `:focus-visible`, `aria-expanded`; teclado en Agrupar |
| F0A-6 | Conforme | `design.md` v1.5.0: subsección «Jerarquía en árbol con casillas, marca de paquete y plegado» (sin tokens ni componentes nuevos) y §15 actualizado |
| F0A-7 | Conforme | `mockups/index.html` y `mockups/README.md` enlazan las cuatro; preguntas abajo |

## Handoff
- Nada falta de construcción. Pendiente: que Victor apruebe las maquetas (desbloquea F1-C y F2-B). Al aprobar, quitar «pendiente de aprobación» en `design.md` y `mockups/README.md`.
- Nota: verificación solo estructural (sin navegador, según el brief); conviene abrirlas una vez a simple vista.

## Preguntas de diseño para Victor
1. En la confirmación de niveles, ¿la fila de muestra por grupo de hermanas debe mostrar solo un ejemplo o permitir ver todas las hermanas del grupo?
2. ¿Las filas «para revisar» bloquean el botón de aprobar hasta que se resuelvan, o solo se advierten?
3. En Declarar, ¿el restante por partida se muestra en la fila de la partida del DP, en la del cronograma, o en ambas?
4. En Agrupar, ¿la marca de paquete debe usar un solo color o alternar dos colores entre paquetes contiguos?
5. En pantallas angostas, ¿Cronograma y DP pasan a pestañas (propuesto) o se apilan?
6. ¿Plegar un paquete debe recordarse entre sesiones o reiniciarse al abrir la pantalla?

## Mejoras de trabajo
Ninguna nueva.

## Reglas de negocio detectadas
Ninguna nueva.

## Huérfanos
Ninguno. `Trazabilidad.xlsx` modificado ya existía en el árbol; no se tocó ni se commitea.

## Llamadas
8 (esta sesión de cierre; el trabajo previo ya estaba en d0b700e).
