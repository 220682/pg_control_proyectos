# Control de Proyectos en Construcción — Estudio a Profundidad

**Contexto:** Victor es ingeniero industrial, trabaja en oficina técnica de proyectos de construcción en el rubro minero. Este documento parte del Módulo 4 ("Gestión del Cronograma y Control de la Mano de Obra") del curso *Oficina Técnica en Proyectos de Construcción* (Costos Educa), pero va más allá de su contenido, con la mira puesta en un objetivo propio: **diseñar, a futuro, un sistema de control de proyectos que combine Valor Ganado (EVM) y Last Planner System (LPS)**.

---

## 1. ¿Qué es el Control de Proyectos?

**Control de proyectos** es la disciplina que mide continuamente el desempeño real de un proyecto (alcance, costo, plazo y calidad) contra una **línea base** aprobada, detecta desviaciones tan pronto como es posible, y dispara acciones correctivas o preventivas para que el proyecto termine dentro de lo comprometido — o, cuando eso ya no es posible, para que el cierre se produzca con la mejor información disponible y sin sorpresas.

No es lo mismo que "gestión de proyectos" (que incluye planificar, organizar, dirigir personas, contratar, etc.). El control de proyectos es la función específica de **comparar planeado vs. real y generar la señal de alarma**. En una constructora esa función suele vivir en la **Oficina Técnica (OT)**, que es el "cerebro" de costos, plazos y documentación de la obra, distinta del área de producción/campo que ejecuta.

### 1.1 El ciclo de control

Todo sistema de control de proyectos, sea EVM, LPS o cualquier otro, sigue el mismo ciclo de fondo (versión constructiva del PDCA):

1. **Línea base** — se congela un plan de referencia: presupuesto meta, cronograma maestro, EDT/WBS con códigos de costo.
2. **Medición** — se levanta el dato real de campo (avance físico, horas-hombre, costo incurrido, calidad, seguridad).
3. **Comparación** — real vs. planeado, con indicadores.
4. **Diagnóstico** — se identifica la causa raíz de la desviación (no solo el síntoma).
5. **Acción correctiva/preventiva** — se decide y ejecuta un ajuste (recursos, secuencia, alcance, reclamo contractual).
6. **Reproyección** — se actualiza la estimación a la conclusión (costo y plazo) con la nueva realidad.

Este ciclo debe correr en **al menos dos frecuencias simultáneas**: una de corto plazo (diaria/semanal, terreno) y otra de mediano-largo plazo (mensual, dirección/cliente). Esa doble frecuencia es exactamente el punto de encuentro entre EVM (fuerte en el nivel mensual/gerencial) y LPS (fuerte en el nivel semanal/operativo) — ver sección 4.

### 1.2 Objetivos que debe cumplir el control de proyectos

Tal como lo plantea el propio Módulo 2 del brochure, un buen sistema de control debe permitir:

- **Identificar desviaciones** apenas ocurren (no al cierre del mes).
- **Tomar acciones oportunamente**, con datos accionables, no solo reportes descriptivos.
- **Proyectar de manera confiable** el resultado final (costo al cierre, fecha de término).

### 1.3 Línea base y estructura de control

Antes de medir nada se necesita:

- **EDT/WBS** (Estructura de Desglose del Trabajo): divide el proyecto en partidas/paquetes de trabajo controlables.
- **Presupuesto Meta** (costo objetivo interno, distinto del "Presupuesto de Venta" al cliente): la brecha entre Venta y Meta es la utilidad esperada.
- **Cronograma maestro** (hitos contractuales) + cronograma detallado con relaciones de precedencia (CPM).
- **Códigos de control / cuentas de costo**: cada partida de campo debe poder cruzarse contra una partida de presupuesto y una actividad de cronograma — sin esta trazabilidad, ni EVM ni ningún otro método funciona.

---

## 2. Método del Valor Ganado (Earned Value Management — EVM)

### 2.1 Qué mide y por qué es distinto de "comparar gasto vs. presupuesto"

El error más común de control de costos "artesanal" es comparar **gasto acumulado vs. presupuesto acumulado**. Eso no dice si vas atrasado o adelantado en el cronograma — solo dice si gastaste mucho o poco dinero, lo cual puede deberse a que hiciste más trabajo, menos trabajo, o el mismo trabajo más caro/barato. EVM resuelve esto introduciendo una tercera variable: **cuánto trabajo real se completó, valorizado al costo presupuestado** (el "valor ganado").

### 2.2 Las tres variables base

| Variable | Nombre | Definición |
|---|---|---|
| **PV** (o BCWS) | *Planned Value* / Valor Planificado | Costo presupuestado del trabajo que **debía** estar hecho a la fecha de corte, según la línea base. |
| **EV** (o BCWP) | *Earned Value* / Valor Ganado | Costo presupuestado del trabajo que **realmente** se completó a la fecha de corte. Es la variable clave: "cuánto vale, a precio de presupuesto, lo que de verdad avancé". |
| **AC** (o ACWP) | *Actual Cost* / Costo Real | Lo que realmente costó (mano de obra, materiales, equipos, subcontratos) producir ese avance. |

Además:

- **BAC** (*Budget At Completion*): presupuesto total aprobado del proyecto (o de la partida) a costo meta.

### 2.3 Índices de desempeño

| Indicador | Fórmula | Interpretación |
|---|---|---|
| **CV** — Variación de Costo | `CV = EV − AC` | > 0: gasté menos de lo que valía el avance (bien). < 0: sobrecosto. |
| **SV** — Variación de Cronograma | `SV = EV − PV` | > 0: adelantado. < 0: atrasado (en términos de **valor**, no de días — ver limitación en 2.5). |
| **CPI** — Índice de Desempeño de Costo | `CPI = EV / AC` | > 1: eficiente en costo. < 1: cada sol/dólar gastado rinde menos de 1 en valor. |
| **SPI** — Índice de Desempeño de Cronograma | `SPI = EV / PV` | > 1: adelantado. < 1: atrasado. |

### 2.4 Proyecciones al cierre

| Indicador | Fórmula | Cuándo usarla |
|---|---|---|
| **ETC** — Estimate To Complete (falta por gastar) | `ETC = EAC − AC` (o reestimación bottom-up del saldo) | Cuando conviene reestimar el saldo desde cero (cambios de alcance, nuevas condiciones). |
| **EAC** — Estimate At Completion (costo final proyectado) | `EAC = AC + (BAC − EV) / CPI` | Caso típico: se asume que el desempeño de costo observado (CPI) se mantendrá en el saldo del proyecto. Es la fórmula que enseña el Módulo 2/3 del curso. |
| **EAC (variante optimista)** | `EAC = AC + (BAC − EV)` | Se asume que la desviación fue puntual y el saldo se ejecutará según el presupuesto original. |
| **EAC (variante pesimista, doble desviación)** | `EAC = AC + (BAC − EV) / (CPI × SPI)` | Cuando además del sobrecosto hay atraso, y ambos afectan el saldo (típico en obra con cuadrillas fijas: si te atrasas, la mano de obra sigue devengando costo). |
| **VAC** — Variación al Cierre | `VAC = BAC − EAC` | Cuánto utilidad/pérdida adicional se proyecta respecto al presupuesto original. |
| **TCPI** — Índice de Desempeño por Completar | `TCPI = (BAC − EV) / (BAC − AC)` | Qué eficiencia (CPI) se necesita **de aquí al cierre** para terminar dentro del presupuesto original. Si TCPI >> CPI actual, la meta ya es prácticamente inalcanzable sin cambiar algo estructural. |

### 2.5 Ejemplo aplicado (obra de movimiento de tierras)

Partida "Corte y relleno masivo", BAC = S/ 1,000,000, plazo 10 semanas. A la semana 6:

- Según cronograma, debía llevar 65% de avance → **PV = S/ 650,000**.
- En campo se verificó (metrado real) que el avance físico real es 50% → **EV = S/ 500,000**.
- El costo real incurrido a la fecha es **AC = S/ 560,000**.

Cálculos:
- CV = 500,000 − 560,000 = **−60,000** (sobrecosto: cada avance está costando más de lo presupuestado).
- SV = 500,000 − 650,000 = **−150,000** (atraso, en valor).
- CPI = 500,000 / 560,000 = **0.89** (por cada sol gastado, se ganan 0.89 soles de avance).
- SPI = 500,000 / 650,000 = **0.77** (avanzando al 77% de la velocidad planificada).
- EAC = 560,000 + (1,000,000 − 500,000) / 0.89 = **S/ 1,121,500** proyectado, es decir ~12% de sobrecosto si nada cambia.
- TCPI = (1,000,000 − 500,000) / (1,000,000 − 560,000) = **1.14** → de aquí al cierre se necesitaría un CPI de 1.14 (mejor que el promedio histórico de la industria) solo para no pasarse del BAC original. Señal de alerta temprana para el Jefe de OT.

Este es exactamente el tipo de ejercicio que trabaja el Módulo 3 del curso ("Taller de Reporte de Resultado a la fecha", "Análisis de Brechas", "Estimación de Proyección del Saldo").

### 2.6 Limitaciones de EVM que justifican complementarlo con LPS

- **SV/SPI son variaciones de valor, no de tiempo real (días).** Un SPI de 0.90 no te dice cuántos días de atraso tienes en la ruta crítica; para eso se necesita el cronograma CPM y su análisis de holguras. Existe una variante ("Earned Schedule") que traduce SV/SPI a unidades de tiempo, pero en la práctica de obra el CPM sigue siendo la referencia de plazo.
- **EVM es un indicador agregado y "de retrovisor":** dice qué tan mal/bien fue el desempeño **acumulado**, pero no explica **por qué** — no distingue si el problema es falta de materiales, cuadrillas incompletas, diseño no compatibilizado, clima, permisos, etc.
- **EVM no mide la confiabilidad de la planificación semanal**, que es justamente la causa raíz de la mayoría de esas desviaciones. Ahí es donde entra el Last Planner System.

---

## 3. Last Planner System (LPS)

### 3.1 Origen y filosofía

El **Last Planner System** (Glenn Ballard y Greg Howell, Lean Construction Institute, años 90) nace de una constatación simple: en obra, el "último planificador" — el capataz, el ingeniero de producción, el subcontratista — es quien realmente decide qué se hace mañana, y sus compromisos suelen fallar por causas predecibles y repetitivas. LPS no reemplaza al cronograma maestro; **agrega una capa de planificación colaborativa de corto plazo que protege el flujo de trabajo**, reduciendo la variabilidad antes de que se convierta en atraso.

Su métrica central no es "cuánto avanzamos" sino **"qué tan confiable es nuestra promesa de trabajo"**.

### 3.2 Los niveles de planificación (cascada)

LPS trabaja con una jerarquía de planes, cada uno más detallado y de menor horizonte que el anterior:

| Nivel | Horizonte | Pregunta que responde | Salida típica |
|---|---|---|---|
| **Plan Maestro** | Todo el proyecto | ¿Qué **debería** hacerse? | Cronograma CPM/Gantt, hitos contractuales |
| **Planificación por Fases (Pull Planning / Phase Scheduling)** | Una fase (ej. estructuras, un tren de trabajo) | ¿Qué **se necesita** para que el trabajo fluya sin interrupciones, trabajando hacia atrás desde el hito? | Mapa de fase con relaciones de precedencia negociadas por todos los responsables |
| **Lookahead Planning (Planificación Anticipada)** | 3 a 6 semanas (típico 4) | ¿Qué **se puede** hacer, si se liberan las restricciones a tiempo? | Programa lookahead + **matriz de restricciones** |
| **Plan Semanal de Trabajo (Weekly Work Plan)** | 1 semana | ¿Qué **se hará** de verdad? (solo entra lo que ya está libre de restricciones) | Plan semanal firmado por cada "last planner" |
| **Plan Diario / Reunión de coordinación diaria** | 1 día | ¿Qué se **hizo** ayer y qué se hará hoy? | Reporte diario, ajustes de cuadrillas |

La lógica **DEBERÍA → PODRÍA → SE HARÁ → SE HIZO** (Should–Can–Will–Did) es el hilo conductor de toda la cascada: solo se compromete (Will) lo que efectivamente está libre de restricciones (Can), y se audita después contra lo que realmente se hizo (Did).

### 3.3 Restricciones (Constraints) y la matriz de restricciones

Una **restricción** es cualquier condición que debe cumplirse antes de que una tarea pueda ejecutarse: diseño/planos aprobados, material en obra, equipo disponible, permiso, frente liberado por otra especialidad, procedimiento/PETS aprobado, personal calificado, condiciones de acceso, etc.

El **Lookahead** no solo lista actividades futuras: para cada una identifica sus restricciones, asigna un **responsable** de liberarla y una **fecha compromiso**. Una tarea solo puede pasar al Plan Semanal si sus restricciones están **liberadas** (o con altísima certeza de estarlo). Este es el mecanismo central de LPS: mover el control de "¿por qué no se hizo?" (reactivo) a "¿qué necesito para poder hacerlo?" (proactivo).

### 3.4 PPC — Porcentaje de Plan Cumplido

Es el indicador estrella de LPS:

```
PPC = (N.° de actividades semanales completadas al 100%) / (N.° total de actividades comprometidas esa semana) × 100
```

Puntos clave:
- Es **binario por actividad**: una tarea completada al 90% cuenta como **no cumplida** (0), no como 0.9. Esto es intencional: mide la confiabilidad de la promesa, no el avance físico parcial (para eso ya está el avance físico/EVM).
- Valores típicos de referencia en la industria: obras "en control" suelen moverse en **70–85% de PPC**; por debajo de 60% de forma sostenida indica un problema serio de planificación o de gestión de restricciones.
- Se lleva **semana a semana** y se grafica en tendencia — el nivel absoluto importa menos que la tendencia y la estabilidad.

### 3.5 Análisis de Causas de No Cumplimiento (CNC)

Cada actividad **no cumplida** debe registrar su causa. Categorías típicas (consistentes con la literatura Lean Construction en Latinoamérica):

- **Trabajo previo / partida antecesora no terminada** (la causa más frecuente reportada en obras peruanas).
- **Mano de obra** (cuadrilla incompleta, ausentismo, falta de calificación).
- **Materiales** (no llegaron, llegaron incompletos o con especificación errónea).
- **Equipos/herramientas** (no disponibles, en mantenimiento, mal dimensionados).
- **Diseño/información** (planos no compatibilizados, RFI sin respuesta).
- **Clima / condiciones de terreno.**
- **Permisos / seguridad** (paralización por SSOMA, permiso de trabajo no vigente — crítico en minería).
- **Reprogramación / cambio de prioridad** por el propio equipo.

El **Pareto de CNC acumulado mes a mes** es, en la práctica, la herramienta de mejora continua más potente de LPS: revela cuál es el cuello de botella sistémico del proyecto (no de una semana puntual), y permite atacar la causa raíz en vez de "apagar incendios" cada lunes.

### 3.6 Medición de productividad dentro de LPS: Carta Balance y Nivel General de Actividad

El Módulo 4 del brochure ya menciona "Carta balance" y "Nivel general de actividades" — son las herramientas de campo que alimentan LPS y el control de mano de obra:

- **Nivel General de Actividad (NGA)**: muestreo aleatorio en campo que clasifica lo que está haciendo cada trabajador en un instante en tres categorías:
  - **TP — Trabajo Productivo**: aporta avance físico directo (vaciar concreto, colocar acero).
  - **TC — Trabajo Contributivo**: necesario pero sin avance directo (transporte de material, recibir instrucciones, mediciones).
  - **TNC — Trabajo No Contributivo**: tiempo perdido (esperas, traslados innecesarios, ocio).
  Sirve para diagnosticar de forma agregada si el problema de productividad es de método, de logística o de supervisión.

- **Carta Balance (Crew Balance Chart)**: análisis más fino a nivel de **una cuadrilla específica en un proceso constructivo puntual**, minuto a minuto, para identificar desbalances (un oficial esperando a un peón, un equipo subutilizado) y redimensionar la cuadrilla. Es la herramienta que sustenta las decisiones de "estrategias para obtener ganancias en la mano de obra" que promete el Módulo 4.

- **Curvas de productividad / Reporte de IP (Índice de Productividad)**: HH reales / HH presupuestadas por unidad de producción, graficadas en el tiempo — conectan directamente con el CPI de EVM cuando la partida es intensiva en mano de obra.

---

## 4. EVM vs. LPS: por qué se complementan (y no compiten)

| Dimensión | EVM | LPS |
|---|---|---|
| Pregunta central | ¿Cuánto vale lo que avancé vs. lo que gasté/debía avanzar? | ¿Qué tan confiable es lo que prometí hacer esta semana? |
| Horizonte típico | Mensual / quincenal, con vista acumulada de todo el proyecto | Semanal / diario, con vista de las próximas 3-6 semanas |
| Nivel de detalle | Partidas de presupuesto (agregado) | Tareas de cuadrilla, frente o proceso (muy detallado) |
| Naturaleza del indicador | Financiero-físico, retrospectivo y proyectivo (EAC) | Operativo, de confiabilidad del compromiso, diagnóstico de causa raíz |
| A quién sirve mejor | Gerencia, cliente, control de resultado operativo | Producción, capataces, ingenieros de campo |
| Su gran fortaleza | Cuantifica el impacto económico y proyecta el cierre | Explica el **porqué** y previene la desviación antes de que ocurra |
| Su gran debilidad | No explica causas; reacciona cuando el daño ya está en el costo | No traduce directamente a S/ o USD ni a "fecha de término" del proyecto completo |

**La idea central para el sistema que Victor visualiza:** LPS actúa en la "trinchera" (semana a semana, restricción a restricción) para que el **EV real** se acerque lo más posible al **PV planeado** — es decir, un buen PPC sostenido es, causalmente, el mecanismo que produce un buen SPI. Y el Pareto de CNC es el diagnóstico que explica por qué el CPI/SPI se está moviendo como se mueve. En sentido inverso, EVM le da a LPS el "marcador" agregado en unidades de dinero y de EAC que un capataz no puede ver desde su plan semanal, y permite priorizar **en qué frentes** vale la pena invertir el esfuerzo de gestión de restricciones (los de mayor peso/impacto en el BAC, o los de la ruta crítica).

### 4.1 Qué dice la evidencia sobre integrarlos

La búsqueda de literatura confirma que esta integración ya se ha estudiado y aplicado, no es una idea aislada:

- Existen tesis y artículos peruanos y chilenos específicamente sobre la **implementación conjunta de Last Planner y Valor Ganado** en proyectos de edificación, puentes y vialidad, incluyendo un caso reciente de una obra vial en Perú ("Application of the Last Planner System with Earned Value Management: A Case Study from a Road Construction Project in Peru").
- El patrón que reportan estos estudios coincide con el planteado arriba: se mantiene el **cronograma maestro (CPM)** como "contrato" formal de plazo frente al cliente, y se usa **LPS para la operación semanal**, mientras **EVM consolida mensualmente** el resultado económico y la proyección de cierre — el llamado enfoque **híbrido**.
- Algunas propuestas académicas (p. ej. herramientas tipo "matriz" que cruzan PAC/PPC con factores de productividad de EVM) van más allá y buscan que el **avance ganado (EV)** de cada semana se calcule directamente a partir del cumplimiento de las tareas del Plan Semanal de LPS, en vez de un metrado de campo independiente — cerrando el ciclo entre ambos sistemas en una sola fuente de datos.

### 4.2 Boceto de arquitectura para un sistema integrado (a desarrollar más adelante)

No es el alcance de este documento diseñarlo en detalle, pero como semilla para la visión de Victor, la arquitectura más consistente con la evidencia sería:

1. **Una única EDT/código de control** que sirva simultáneamente de partida presupuestal (para EVM) y de "paquete de trabajo" del Lookahead (para LPS) — sin esto, cualquier intento de cruzar datos exige doble digitación y termina abandonado.
2. **Captura de avance físico diaria en campo** (Reporte Diario de Obra) que alimente: (a) el metrado real → EV de EVM, y (b) el estado de cumplimiento de la tarea comprometida → PPC de LPS. Es el mismo dato de origen, consumido dos veces.
3. **Costo real (AC)** desde el sistema de costos/ERP, con la misma codificación.
4. **Matriz de restricciones** como capa de alerta temprana: una restricción no liberada a tiempo es, en esencia, un **riesgo de que el próximo corte de EVM muestre SV/SPI negativo** en esa partida — se podría "puntuar" el riesgo de cada partida según el estado de sus restricciones.
5. **Tablero único** con tres vistas: (i) semanal — PPC + Pareto de CNC (producción), (ii) mensual — curva S, SPI/CPI, EAC por partida (gerencia/cliente), (iii) puente entre ambas — qué restricciones/incumplimientos semanales explican la variación mensual observada.

---

## 5. Formatos clave que debe tener una Oficina Técnica / constructora

A continuación, los formatos "vivos" (se llenan y actualizan periódicamente) que sostienen todo lo anterior. Están agrupados por frecuencia, de mayor a menor detalle temporal.

### 5.1 Diarios

**Reporte Diario de Obra (RDO)**
Documento legal-técnico que deja constancia de lo ocurrido cada día. Contenido mínimo:
- Datos generales (proyecto, fecha, clima/condiciones — crítico en minería por altura, temporada de lluvias, nevadas).
- Personal en obra por especialidad/subcontratista (HH disponibles).
- Equipos y maquinaria (disponibles, operativos, en mantenimiento).
- Actividades ejecutadas y avance del día por frente.
- Materiales recibidos/consumidos.
- Incidencias: paralizaciones, accidentes/incidentes SSOMA, observaciones de calidad, visitas de supervisión/cliente.
- Instrucciones del cliente/supervisión (referencia a RFI/cuaderno de obra si aplica).
- Fotografías con georreferencia/frente.
Es la fuente primaria de datos de todo el sistema: de aquí salen el metrado real, las HH reales, y el estado de cumplimiento del Plan Semanal.

**Plan Diario / Tablero de coordinación diaria**
Reunión corta (10-15 min) de ajuste del día en curso a partir del Plan Semanal vigente; en LPS es donde se detectan restricciones de último momento.

### 5.2 Semanales

**Plan Semanal de Trabajo (Weekly Work Plan)** — listado de tareas comprometidas por cada "last planner" (subcontratista/capataz), ya libres de restricciones, con responsable y cuadrilla asignada.

**Matriz de Restricciones** — tabla con: actividad, tipo de restricción, responsable de liberarla, fecha compromiso de liberación, estado (abierta/en proceso/liberada), y semana en que se necesita liberada para no bloquear el Lookahead.

**Reporte de PPC y Causas de No Cumplimiento (CNC)** — el cumplimiento de la semana anterior, con el detalle de causa por cada tarea incumplida, alimentando el Pareto acumulado.

**Reporte de Índice de Productividad (IP) semanal** por partida crítica (HH reales/HH presupuestadas).

### 5.3 Quincenales / mensuales

**Curva S** — avance acumulado programado vs. real, en dos variantes que conviene no confundir:
- **Curva S física** (% de avance de obra) — insumo directo del PV/EV de EVM.
- **Curva S financiera / valorizada** (S/ o USD acumulados) — cruza con el Flujo de Caja (Módulo 5 del curso).

**Histograma de Mano de Obra (y de recursos en general)** — barras de HH o N.° de trabajadores requeridos por semana/mes según cronograma, comparado contra lo realmente movilizado; sirve para prever picos de contratación/desmovilización (relevante en minería por camp/logística y rotación de turnos) y para detectar sobre- o sub-dimensionamiento de cuadrillas antes de que impacte el CPI.

**Lookahead (3-6 semanas)** — programa de mediano plazo con sus restricciones asociadas, actualizado semanalmente (ventana móvil).

**Reporte de Resultado Operativo / Cuadro de Control de Costos** — el "reporte estrella" del Módulo 3: Venta y Meta a la fecha, Costo Real, Utilidad/Brecha, indicadores EVM (SV/SPI/CV/CPI), proyección EAC, y análisis de brechas por partida crítica.

**Dashboard de Control de Costos** — consolidado visual (tablas dinámicas, semáforos) para reporte a gerencia/cliente, típicamente en Excel o BI.

**Curva de Productividad de Mano de Obra y Materiales** — tendencia mensual del IP, para decisiones de refuerzo de cuadrillas o cambio de método constructivo.

### 5.4 Otros formatos de control documentario y contractual (soporte transversal)

- **Dossier de Calidad** (protocolos, registros de liberación, ensayos) — estructura que garantiza trazabilidad; conecta con el concepto de "Avance por Unidad Ejecutada vs. Unidad Liberada" del Módulo 7: en control de proyectos serio, una partida no debería considerarse "ganada" (EV) hasta que está liberada por calidad, no solo ejecutada físicamente.
- **Log de RFI/SI** (Solicitudes de Información / Instrucciones de Sitio) y de cambios técnicos.
- **Cronograma de Adquisiciones** y **Control de Subcontratos** — insumos directos de restricciones de material/equipo en el Lookahead.
- **Log de Adicionales** y **Valorización de Obra** (avance físico vs. financiero, anticipos y amortizaciones).
- **Matriz FODA** del proyecto y registro de riesgos — vínculo entre control de proyectos y gestión de riesgos.

---

## 6. Particularidades del control de proyectos en construcción minera

El rubro minero (donde Victor ejerce) añade capas específicas sobre el marco general anterior:

- **Modalidad contractual EPC/EPCM**: en minería son predominantes los contratos EPC (llave en mano) o **EPCM** (el contratista gestiona Ingeniería + Procura + Construcción como servicio profesional, sin ejecutar directamente la obra). El control de proyectos EPCM usa técnicas, procedimientos y estructuras de control **distintas al control tradicional de obra civil** — más orientadas a consolidar múltiples subcontratistas/paquetes bajo una sola línea base y un solo reporte al dueño del proyecto (owner).
- **Sitios remotos y logística compleja**: campamentos, turnos (14x7, 20x10, etc.), altitud, clima extremo — todo esto impacta directamente el histograma de mano de obra (rotación, aclimatación) y el Nivel General de Actividad (fatiga, tiempos de traslado interno como Trabajo Contributivo).
- **Permisos y gestión SSOMA como restricción crítica de LPS**: en minería, un permiso de trabajo de alto riesgo (PETAR), un IPERC, o una paralización por seguridad son restricciones tan bloqueantes como la falta de material — y suelen ser la causa de no cumplimiento (CNC) más frecuente y menos "negociable".
- **Multiplicidad de disciplinas e interfaces**: proyectos mineros integran obras civiles, estructuras metálicas, montaje electromecánico, instrumentación — el control de costos y cronograma debe consolidar EDTs de distinta naturaleza bajo un mismo Presupuesto Meta y un mismo cronograma maestro, con alta necesidad de compatibilización (BIM 4D/5D, Módulo 8 del curso, gana especial relevancia aquí).
- **Exigencia de reporte al "owner"**: las mineras suelen exigir formatos de reporte estandarizados (a veces propios, a veces bajo normas como AACE International) para el control de costos, con curvas S, EAC y forecast mensual auditable — reforzando la necesidad de que el sistema EVM esté bien documentado y trazable frente al cliente.

---

## 7. Glosario rápido

| Término | Significado |
|---|---|
| PV / BCWS | Valor Planificado |
| EV / BCWP | Valor Ganado |
| AC / ACWP | Costo Real |
| BAC | Presupuesto Total a la Conclusión |
| EAC | Estimación (proyección) del Costo Total al Cierre |
| ETC | Estimación de lo que falta por gastar |
| VAC | Variación proyectada al cierre |
| CPI / SPI | Índices de desempeño de costo / cronograma |
| TCPI | Eficiencia necesaria de aquí al cierre para lograr el BAC |
| LPS | Last Planner System |
| PPC | Porcentaje de Plan Cumplido |
| CNC | Causas de No Cumplimiento |
| Lookahead | Programación de mediano plazo (3-6 semanas) con restricciones |
| TP / TC / TNC | Trabajo Productivo / Contributivo / No Contributivo |
| RDO | Reporte Diario de Obra |
| EDT / WBS | Estructura de Desglose del Trabajo |
| IP | Índice de Productividad (HH reales / HH presupuestadas) |

---

## 8. Fuentes consultadas

- [Control de costos con valor ganado: PV, EV, AC, CPI y SPI — Platzi](https://platzi.com/cursos/fundamentos-project-management/control-de-costos-con-valor-ganado-pv-ev/)
- [La gestión del valor ganado y su aplicación — PMI](https://www.pmi.org/learning/library/es-las-mejores-practicas-de-gestion-del-valor-ganado-7045)
- [Método del Valor Ganado (EVM) en construcción: fórmulas, indicadores y ejemplo práctico — Opus Planet](https://opus-planet.mx/blog/valor-ganado-evm-construccion/)
- [EVM para planners: SPI, CPI y EAC explicados con ejemplos reales — TecnoAdmin](https://www.tecnoadminconsulting.com/blog/evm-earned-value-management)
- [Metodología de la Gestión del Valor Ganado (EVM) — Ingenieros Top](https://ingenierostop.com/articulos/3-Metodolog%C3%ADa-de-la-Gesti%C3%B3n-del-Valor-Ganado-(EVM)-para-medir-el-desempe%C3%B1o-de-los-proyectos)
- [Last Planner System — Lean Construction Blog](https://leanconstructionblog.com/What-is-the-Last-Planner-System-Que-es-el-Last-Planner-System.html)
- [Last Planner System vs. planificación tradicional — Opus Planet](https://opus-planet.mx/blog/last-planner-system-vs-planificacion-tradicional/)
- [Qué es PPC en Last Planner System y cómo usarlo en obra — CFO Austral](https://www.cfoaustral.cl/recursos/ppc-last-planner-system/)
- [¿Qué es Last Planner System en Lean Construction? — Foco en Obra](https://focoenobra.com/blog/last-planner-lean-construction/)
- [Last Planner System — Universitat Politècnica de València (tesis)](https://riunet.upv.es/server/api/core/bitstreams/c13f88f6-72d1-45b1-9d3b-83c9ae02458a/content)
- [Implementación de Last Planner System — UPC (tesis)](https://repositorioacademico.upc.edu.pe/bitstream/handle/10757/623900/Cornejo_lk.pdf?sequence=13)
- [Reporte de obra diario de construcción gratuito — SafetyCulture](https://safetyculture.com/es/listas-de-verificacion/reporte-de-obra)
- [Plantilla de Informe Diario de Obra para Excel — ProjectManager](https://www.projectmanager.com/es/plantilla-de-informe-diario-de-obra-excel)
- [Acerca de EPCM en minería — Stantec](https://www.stantec.com/es/markets/mining/epcm-mining/about-ecpm-mining)
- [Gerencia de Proyectos Industriales EPC — R&B](https://ryb.pe/curso/gerencia-proyectos-industriales-epc-ingenieria-procura-construccion/)
- [Implementación del Last Planner y la metodología del valor ganado en proyectos civiles — UPC (tesis, puentes Red Vial 5 Huacho)](https://repositorioacademico.upc.edu.pe/handle/10757/652128?show=full&locale-attribute=es)
- [La implementación de la técnica del valor ganado y del sistema de último planificador en una empresa constructora chilena — PMI](https://www.pmi.org/learning/library/es-valor-ganado-ultima-planificadora-chilena-7097)
- [Implementación del Last Planner System en edificación multifamiliar usando SPI — UNJBG (tesis)](https://repositorio.unjbg.edu.pe/items/eb936576-270a-42bb-9a74-454b7fc664b1)
- [Evolution and global impact of the Last Planner System: a literature review — SciELO Colombia](http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0122-34612018000100187)
- [Application of the Last Planner System with Earned Value Management: A Case Study from a Road Construction Project in Peru — ResearchGate](https://www.researchgate.net/publication/400115606_Application_of_the_Last_Planner_System_with_Earned_Value_Management_A_Case_Study_from_a_Road_Construction_Project_in_Peru)
- [Técnicas de medición de rendimientos de mano de obra — Dialnet](https://dialnet.unirioja.es/descarga/articulo/6299721.pdf)
- [Manuales Universitarios de Edificación — Aldo D. Mattos, Editorial Reverté (Curva S e Histogramas)](https://www.reverte.com/media/reverte/files/sample-89150.pdf)
- Brochure del curso *Oficina Técnica en Proyectos de Construcción* — Costos Educa (documento propio del usuario, usado como contexto y punto de partida del Módulo 4).

---

## 9. Próximos pasos sugeridos

1. Profundizar cada sección con ejemplos numéricos propios de proyectos mineros reales de Victor (anonimizados si es necesario).
2. Diseñar las plantillas concretas (Excel/formato) de: Reporte Diario de Obra, Matriz de Restricciones, Plan Semanal, Curva S, Histograma de MO — adaptadas al rubro minero.
3. A partir de la sección 4.2, bocetar la arquitectura de datos del futuro sistema integrado EVM + LPS (tablas, campos, frecuencia de captura) antes de pensar en herramienta/software.
4. Revisar si conviene alinear el sistema con un estándar de reporte tipo AACE International, dado que los "owners" mineros suelen exigirlo.
