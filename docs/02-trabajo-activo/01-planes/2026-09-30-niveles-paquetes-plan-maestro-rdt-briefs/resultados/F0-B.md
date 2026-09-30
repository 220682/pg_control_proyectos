# Resultados F0-B · Maquetas del lienzo del Plan Maestro, paneles ocultables y selector del RDT

Carril de diseño, `main` de `pg_control_proyectos`. Sin push.

## Skills revisados
`pg_control_proyectos/.claude/skills/`: cerrar-tanda (usada), verificar-permisos-por-rol (no aplica: sin permisos), seguir-flujo-de-planes (del Orquestador). Repositorio de la app: sin carpeta de Skills (verificado).

## Estado de ítems
| ID | Estado | Evidencia |
|---|---|---|
| F0B-1 | Conforme | `mockups/plan-maestro-lienzo.html`: columnas fijas (WBS, descripción, Und., metrado, costo unitario, HH por unidad, más «Falta repartir») a la izquierda de la línea ámbar; una columna por día agrupada por semana (sáb a vie) con scroll; total del servicio en el encabezado; sin columnas de Tiempo. Botón «Personalizar campos» con el mismo aspecto del componente `PersonalizarCampos.tsx` (leído en la app) |
| F0B-2 | Conforme | Seis columnas por semana rotuladas (nombre y unidad), interruptor «Acumuladas», semanas plegables/expandibles (una a una y todas) |
| F0B-3 | Conforme | Nivel y paquetes plegables con subtotal, partidas por paquete, directa, «Falta repartir» por fila, indicador global con `<progress>`, «Crear Plan Maestro» con `aria-disabled` hasta el 100 % y mensaje que lista las partidas que faltan (probado en navegador: ejemplo 2 da 93,29 % y nombra Acero y Eliminación) |
| F0B-4 | Conforme | Subfilas «Prog.» (campos) y «Real» (solo lectura) con interruptor; real por paquete × partida; ejemplo 3 agrega la semana S5 extendida con etiqueta «real fuera del rango»; BORRADOR y APROBADO (todos los campos deshabilitados, probado) |
| F0B-5 | Conforme | `mockups/paneles-ocultables.html`: botones izquierdo, derecho y ambos (ancho del lienzo 847 → 1343 px al ocultar ambos), franja inferior reservada para el icono del asistente, vista móvil 390 px con cajón |
| F0B-6 | Conforme | `mockups/crear-rdt-selector-paquetes.html`: paquetes plegables con partidas, directas aparte, modo por avance del paquete (probado: guía 20 m³ → 25 % → afirmado 10 m³ solo lectura), horas C/NC y materiales con el mismo selector, mensaje sin Plan Maestro aprobado |
| F0B-7 | Conforme | Comparación número a número ejecutando el cálculo de la propia maqueta en navegador: físico semanal total 22,56 / 26,22 / 27,44 / 23,78; acumulado 22,56 / 48,78 / 76,22 / 100 %; económico 1 850 / 2 150 / 2 250 / 1 950 (BAC $ 8 200); HH 47 / 52 / 39 / 34 (172); paquete 1, paquete 2 y directa coinciden con el anexo en las 4 medidas. Estados vacío, carga, error, móvil y accesibilidad en las tres maquetas. `design.md` v1.6.0 (§3, §5, §8, §15); `mockups/index.html` y `mockups/README.md` enlazados |

## Handoff
- Nada falta de construcción. Pendiente: que Victor apruebe las tres maquetas (desbloquea F3-C, F3-D y F4-C). Al aprobar, quitar «pendiente de aprobación» / «vigente cuando Victor apruebe» en `design.md` y `mockups/README.md`.
- Verificado con Playwright sobre un servidor local temporal (ya detenido); sin errores de consola salvo el favicon. Captura de escritorio del lienzo revisada a simple vista; la vista móvil se verificó por CSS, no por captura.
- Decisiones de diseño: línea divisoria en `amber` (token semántico existente) en vez de un naranja nuevo; «Falta repartir» entra en la zona fija; BAC es el único campo opcional de «Personalizar campos» (el anexo lo nombra); en un paquete «por avance del paquete» el selector del RDT solo elige el paquete, no sus partidas.
- Los códigos WBS y nombres del lienzo son simulados (anexo del Spec), no datos reales.

## Preguntas de diseño para Victor
1. El flujo 18 lista Área, Disciplina, Frente, BAC, HH contractuales y método de medición como columnas. ¿Quieres alguna como opción en «Personalizar campos» del lienzo? Hoy solo se ofrece el BAC.
2. La línea entre lo fijo y los días usa el amarillo de advertencia que ya existe. ¿Prefieres el naranja de tu imagen? Sería un color nuevo que hay que aprobar.
3. Una semana plegada deja sus columnas de totales (seis, o tres sin acumuladas). ¿O prefieres una sola columna con un resumen?
4. Los paneles laterales: ¿un botón para cada uno y uno para ambos (propuesto), o solo uno que oculte los dos?
5. Para que el icono del asistente no tape columnas se reserva una franja de 4 rem abajo. ¿Te parece bien perder ese alto?
6. En el RDT, ¿las horas NC (no contribuyentes) también se asignan a una actividad, o solo las horas C?

## Mejoras de trabajo
- Las maquetas con datos se pueden comprobar en navegador local con un servidor Node mínimo (el navegador de pruebas bloquea `file:`; `python -m http.server` no respondió en este entorno). Exponer el cálculo en `window.__maqueta` permite la comparación número a número.

## Reglas de negocio detectadas
Ninguna nueva.

## Huérfanos
Ninguno. Se borró la carpeta temporal `.playwright-mcp` (ignorada por git). `Trazabilidad.xlsx` modificado no se toca ni se commitea.

## Llamadas
~34.
