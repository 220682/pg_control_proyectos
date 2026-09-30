# Resultados F0-R · Ajustes a las maquetas

Worker F0-R · carril de diseño (`pg_control_proyectos`, `main`) · sin navegador: revisión por lectura y comprobación de sintaxis del JavaScript de las 7 maquetas (`new Function` sobre cada `<script>`, todas OK). jsdom no está instalado, así que los comportamientos interactivos quedan por ver en navegador por el Orquestador.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: `cerrar-tanda` (usado), `seguir-flujo-de-planes` (lo usa el Orquestador), `verificar-permisos-por-rol` (no aplica: no se tocan permisos). Repositorio de la app: no tiene carpeta `.claude/skills`; ninguno aplica.

## Estado de los ítems
| ID | Estado | Evidencia |
|---|---|---|
| F0R-1 | Observado (pendiente de ver en navegador) | Las cuatro maquetas de F0-A ya tenían fila de muestra + «Ver N hermanas» (1). Nuevo: filas «Para revisar» con botón «Confirmar rol» que bloquean «Aprobar niveles» hasta resolverlas (2; `importar-dp-niveles`, y el mismo código en `cronograma-niveles`, que hoy no tiene filas por revisar). Restante por partida en ambas listas (3): ya estaba en `paquetes-declarar` (columna «Restante de la partida» y «Restante»), se dejó y se anotó. Marca de paquete alterna cian/azul con fondo tenue, recalculada al mover (4; `paquetes-agrupar`, función `recolor`). Pestañas «Cronograma / DP» bajo 900 px (5; se renombró «Presupuesto» a «DP»). Plegado se reinicia al abrir y al cambiar de ejemplo (6). «Pendiente de aprobación» quitado de las cuatro en `mockups/README.md`, `index.html` y `design.md` |
| F0R-2 | Observado (pendiente de ver en navegador) | `plan-maestro-lienzo`: columna opcional Disciplina (además del BAC, ninguna otra) en «Personalizar campos»; divisoria con `--warn` (ya era el amarillo de advertencia, el texto ahora lo dice); semana plegada sin cambios; rótulo «Met.». Se quitó «pendiente de aprobación» |
| F0R-3 | Observado | `paneles-ocultables` y el lienzo: sin botones de texto; un icono por panel, dentro del panel y en su borde interior, posición absoluta, con tira de 24 px cuando el panel está oculto. «Ocultar ambos» eliminado (no hay barra donde ponerlo sin distorsionar) |
| F0R-4 | Observado | Quitada la franja de 4 rem (`padding-bottom:58px`, caja «reserva», texto en notas) del lienzo y de `paneles-ocultables` (escritorio y móvil); el asistente flota (`absolute`, z-40). Regla de `design.md` §3 reescrita |
| F0R-5 | Observado | `crear-rdt-selector-paquetes.html` rehecho sobre `FormularioCrearRdt.tsx` (leído entero, solo lectura): 1.0 Identificación (9 campos), 2.0 Avance (12 columnas), 3.0 Tareo (persona, DNI, nombre, cargo, especialidad, horas T1..Tn, total contra jornada), Equipos, Materiales, Observaciones, cargar/guardar plantilla, «Cargar RDT al sistema», modo Revisar. Selector «Elegir actividad del Plan Maestro» abierto desde el campo de partida, con paquetes plegables, directas aparte, por avance del paquete, y Contributoria / No contributoria |
| F0R-6 | Observado | «Met.» en lienzo, Declarar, Agrupar, Importar DP; «Met. acum./prog./ejec.» en Crear RDT con ancho mínimo y sin cortar. Regla en `design.md` §5 y §7 |
| F0R-7 | Observado | Selector de disciplina al crear paquete y en la partida directa (`paquetes-agrupar`), columna opcional en el lienzo; catálogo rotulado «simulado» |
| F0R-8 | Observado | `design.md` 1.7.0 (frontmatter corregido: decía 1.5.0 con historial hasta 1.6.0; §3, §5, §7, §15), `mockups/index.html`, `mockups/README.md`. Sin flujos tocados |

Todos quedan «Observado» y no «Conforme» porque no se abrió ninguna maqueta en navegador (lo hará el Orquestador para Victor).

## Handoff
- Falta: abrir las 7 maquetas en navegador. Comprobar sobre todo: `crear-rdt-selector-paquetes` (selector, guía/calculada, Revisar), iconos de panel en `paneles-ocultables` y lienzo (estado oculto), alternancia de colores al mover paquetes.
- Archivos tocados (todos en `docs/05-diseno-y-referencias/`): `design.md`, `mockups/{README,index,importar-dp-niveles,cronograma-niveles,paquetes-declarar,paquetes-agrupar,plan-maestro-lienzo,paneles-ocultables,crear-rdt-selector-paquetes}.html|md`.
- Decisión técnica: en Crear RDT el selector también sirve a los equipos (comparten el mismo origen de WBS que C/NC y materiales en el código real).
- Hallazgo: el frontmatter de `design.md` estaba en 1.5.0 aunque el historial llegaba a 1.6.0.

## Preguntas para Victor (máx. 4, lenguaje simple)
1. En Crear RDT, ¿los equipos también deben elegir su partida con el mismo cuadro? Lo dejé así porque hoy usan la misma lista que materiales.
2. ¿La disciplina es obligatoria al crear un paquete y en la partida directa? El flujo 19 dice obligatoria para el paquete; para la partida directa no está escrito.
3. Quité «Ocultar ambos paneles»: sin barra no cabe sin deformar. ¿Basta con un icono por panel?
4. En el lienzo, ¿la disciplina de una partida dentro de un paquete se hereda del paquete, o cada partida puede tener la suya? (la maqueta muestra una distinta en «Acero» solo como ejemplo).

## Mejoras de trabajo
- Las maquetas se validan sin navegador con `new Function` sobre el script; conviene tener jsdom en el repositorio de la app para comprobar clics.
- Un script Python que reemplaza cadenas con `assert count==1` evitó ediciones dobles; un índice de `.index()` buscado en el texto equivocado duplicó un bloque (se detectó y se corrigió): buscar anclas únicas.

## Reglas de negocio detectadas (para el Orquestador; no se editó ningún flujo)
- Filas «para revisar» bloquean aprobar niveles (flujos 08/09/15).
- Disciplina en paquete y partida directa, y columna opcional en el lienzo (flujos 19/20).
- El plegado de paquetes se reinicia al abrir; restante visible en ambas listas (flujo 19).
- Abreviaturas Met./Acum./Prog./Ejec. (transversal).

## Huérfanos
Ninguno nuevo. `mockups/crear-rdts.html` (mockup antiguo en papel) sigue existiendo y ya no es el punto de partida de Crear RDT; no se borró.

## Llamadas
~45.
