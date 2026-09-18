# Memoria del proyecto — pg_control_proyectos

Archivo de continuidad entre sesiones. Guarda el **contexto y las decisiones**, no el contenido de dominio (ese vive en `conocimiento/`).

## Quién es Victor y de qué trata este proyecto

- Ingeniero industrial, trabaja en **oficina técnica (OT)** de proyectos de **construcción en el rubro minero**.
- Está llevando el curso *Oficina Técnica en Proyectos de Construcción* (Costos Educa) — brochure de referencia en `C:\Users\BRANDY\Downloads\BROCHURE-Oficina tecnica en proyectos de construccion.pdf`. El curso cubre 8 módulos (documentación inicial, metodologías de costos, control de costos/resultado operativo, cronograma y mano de obra, valorizaciones/flujo de caja, gestión contractual, control documentario/calidad, BIM).
- **Objetivo propio de Victor (más allá del curso):** entender a fondo el control de proyectos de construcción, en particular **Valor Ganado (EVM)** y **Last Planner System (LPS)**, con la visión a futuro de **diseñar un sistema propio que combine ambas metodologías** para controlar proyectos.

## Estado del proyecto

- Carpeta `conocimiento/` creada: contiene el estudio de fondo.
  - `conocimiento/01-fundamentos-control-de-proyectos-evm-lps.md` — estudio a profundidad: definición de control de proyectos, EVM (fórmulas, ejemplo numérico, limitaciones), Last Planner System (niveles de planificación, restricciones, PPC, CNC, carta balance), por qué EVM y LPS se complementan, evidencia de integración de ambas metodologías, boceto inicial de arquitectura para el sistema integrado, formatos clave de oficina técnica (RDO, matriz de restricciones, plan semanal, curva S, histograma de MO, dashboard de costos, etc.), y particularidades del control de proyectos en minería (EPC/EPCM, sitios remotos, SSOMA como restricción crítica).

## Próximos pasos identificados (sección 9 del estudio)

1. Profundizar con ejemplos numéricos de proyectos mineros reales de Victor.
2. Diseñar plantillas concretas (RDO, matriz de restricciones, plan semanal, curva S, histograma de MO) adaptadas a minería.
3. Bocetar la arquitectura de datos del futuro sistema integrado EVM + LPS (tablas, campos, frecuencia de captura) antes de pensar en herramienta/software.
4. Evaluar alineamiento con un estándar de reporte tipo AACE International (los "owners" mineros suelen exigirlo).

## Cómo trabajar en este proyecto

- El conocimiento de dominio (EVM, LPS, formatos, minería) se documenta en `conocimiento/`, con fuentes citadas al final de cada archivo — no se debe reescribir aquí.
- Este `memoria.md` se actualiza con contexto nuevo (decisiones, objetivos, qué se entregó) cada vez que avance el proyecto, no con el contenido técnico en sí.

## 2026-08-15 — Sistema de control de proyectos: flujo, roles y MOF (v1)

- Victor definió su flujo real de oficina técnica de punta a punta: adjudicación →
  inicio (partidas de control, cronograma, alcance, RDO, listados de materiales/HM)
  → durante (3WLA/plan semanal/PPC del Planner, RDT/informe semanal del Supervisor
  Operativo, requerimientos y gastos de Logística, tareo de indirectos de
  Administración) → cierre (informe final, informe de costos, acta de conformidad,
  RDO/RDTs). Roles confirmados como personas separadas: Jefe de Proyectos,
  Supervisor de Oficina Técnica, Planner, Supervisor de Costos, Supervisor
  Operativo, Supervisor de Logística, Supervisor de Administración, RRHH — todos
  bajo la convención de puesto "Supervisor de \<Área>" salvo Planner y RRHH.
- Se escribió `control_de_proyectos.txt` (raíz del proyecto) con el flujo completo,
  el listado de 22 formatos a implementar (2 ya existen: RDT.xlsx y
  RDO/Ejercicio_Hibrido.xlsx, se ajustan en vez de rehacerse) y el MOF de cada uno
  de los 8 roles + cliente. Es un documento vivo, versión 1, a afinar
  iterativamente — no darlo por definitivo sin que Victor lo revise.
- Investigación web (agente, 2026-08-15) confirmó y amplió lo ya cubierto en
  `conocimiento/01-fundamentos-control-de-proyectos-evm-lps.md`: el 3WLA solo
  funciona si su entregable real es la matriz de restricciones (no un cronograma
  recortado), el PPC necesita CNC categorizadas (no texto libre) para ver
  patrones, y — el hallazgo que más cambió el diseño — PPC (LPS) y SPI/CPI (EVM)
  deben medir la misma unidad de trabajo, lo que exige una tabla "Work Package"
  con relación 1:1 entre partida de control y actividad de cronograma/presupuesto.
  Un caso peruano real (obra vial) documenta esta integración LPS+EVM con
  resultados positivos — fuentes completas quedaron en el output del agente, no
  se copiaron aquí para no duplicar `conocimiento/`.
- **Pendiente explícito de Victor**: confirmar si "Jefe de Proyectos" tiene
  funciones operativas más allá de recibir la adjudicación y dar el visto bueno
  de cierre (quedó así en el MOF v1, marcado como supuesto a validar).
- **Próximo paso acordado**: diseñar los formatos nuevos uno por uno (empezando
  por los de "Al inicio": partidas de control, cronograma base, alcance,
  listados de materiales/HM, tabla Work Package), ajustar RDT/RDO para el
  mapeo Work Package y el cálculo de PPC+CNC, construir el Status de Proyectos
  maestro, y al final correr un proyecto de ejemplo sencillo de punta a punta
  para detectar puntos críticos antes de dar el sistema por definitivo.

## 2026-08-15 (tarde) — control_de_proyectos.txt v2 + Daily report.xlsx

- Victor editó el `.txt` directamente antes de pedir la v2: agrupó Planner y
  Costos como puestos dentro del área Oficina Técnica (no áreas separadas),
  agregó "Listado de Personal requerido" y "Listado PETS" al flujo de inicio,
  y una nueva sección 2.3 "Entrega de información de proyecto".
- Cambio de arquitectura importante: **todo el sistema LPS (Plan Maestro,
  Lookahead+Restricciones, Plan Semanal, PPC+CNC) pasó a vivir en UN SOLO
  archivo Excel multi-hoja, responsable Planner** — y explícitamente
  **multi-proyecto** (el Planner gestiona la ventana corta de TODOS los
  proyectos activos a la vez, no un archivo por proyecto; el Plan Maestro es
  la única hoja específica de cada proyecto). El cálculo de PPC+CNC se movió
  de Oficina Técnica al Planner — Oficina Técnica ahora valida el RDT antes
  de que el Planner calcule sobre él (se mantiene el control de calidad del
  dato, decidido explícitamente por Victor).
- Se agregó **Programación diaria** como formato nuevo: desglose diario del
  Plan Semanal ya comprometido, también multi-proyecto, responsable Planner
  — pero como archivo aparte del Sistema LPS (no una hoja más de ese archivo).
- Se agregó la sección 4.2 "Cuadro detallado": ficha de Finalidad + Estructura
  + Responsable para cada uno de los 22 formatos, a pedido de Victor.
- **Sugerencia hecha y NO aplicada todavía** (pendiente en sección 6 del
  documento): evaluar consolidar también Logística (Status de
  requerimiento + Registro de gastos) y Administración (Tareo + Status de
  capacitación + Programación de capacitaciones) en archivos únicos
  multi-hoja, con la misma lógica que se aplicó al LPS.
- Aparte, se convirtió `Daily report.pdf` (formato real de TECGU para UM Mina
  Justa/Marcobre, código JU-0001-08-02876-0000-13-RD-0158) a
  `Daily report.xlsx` — 2 hojas fieles al PDF (Reporte Diario: MOI/MOD/
  maquinaria/herramientas/servicios/movilidades/resumen de horas; SSOMA:
  actividades oficina/campo, panel fotográfico, responsables). Es un formato
  de un tercero (TECGU), no forma parte todavía del sistema de Victor — queda
  como referencia de cómo luce un Daily Report real de la industria.

## 2026-08-15 (noche) — Sistema hibrido/Consolidado proyecto.xlsx: DP/PR/Dashboard

- Se construyó un caso real completo en `Sistema hibrido/Consolidado
  proyecto.xlsx`: proyecto real de Victor (HDPE Tie-In-06 a GCI, Marcobre,
  cliente COPREFA/TECGU), con su presupuesto y APU reales
  (`Presupuesto_HDPE_TieIn06-GCI_Promcoser.xlsx`, hoja `APU` con el
  desglose de mano de obra/equipos/materiales por partida).
- Se creó la hoja `DP` (Datos de Proyecto): línea base extraída de `CD` +
  `APU` por script (parser de bloques APU cruzado con metrados de `CD`),
  con TODAS las celdas de avance vacías (día cero). Se creó trazabilidad
  completa por fórmula `DP -> PR` en todas las tablas de Recursos (Work
  Package, Mano de Obra, Equipos, Materiales, Subcontrata) y en el resumen
  B2 — antes `PR` tenía números sueltos/de ejemplo sin relación con `DP`.
  Se agregó un bloque "Duración estimada del proyecto" (HH contractual /
  (cuadrilla promedio x horas de jornada)).
- **Aprendizaje de proceso, importante para la próxima vez:** varias veces
  edité el archivo mientras Victor lo tenía abierto en Excel sin
  saberlo, lo que causó confusión real sobre "datos perdidos" (un caso se
  resolvió recuperando el autosave de Excel via COM). Desde entonces, el
  protocolo fijo antes de CUALQUIER escritura a un .xlsx de este proyecto
  es: revisar que no exista el archivo de candado `~$<nombre>.xlsx` en la
  misma carpeta; si existe, parar y pedir que lo cierre primero.
- **Aprendizaje de alcance:** una vez Victor corrigió que había construido
  tablas (Work Package/Mano de Obra) con datos falsos que él ya tenía
  armados en su plantilla real — la lección fue no rehacer/duplicar datos
  que el usuario ya tiene, y preguntar por la ubicación real del archivo
  antes de reconstruir algo desde cero.
- Se diseñó (brainstorming arquitectónico completo, spec + plan escritos)
  un Dashboard híbrido LPS+EVM: specs en
  `Sistema hibrido/dashboard-diseno-lps-evm.md` y
  `Sistema hibrido/dashboard-plan-implementacion.md` (11 tareas). Decisiones
  clave: solo fórmulas nativas (sin VBA ni Power Query, ver spec sección 2),
  hoja `HISTORIAL` nueva para tendencia semanal (snapshots pegados a mano,
  no fórmulas vivas), Resumen Ejecutivo en texto plano SIN jerga de
  índices (CPI/SPI/IP) porque son proyectos pequeños — habla en metrado y
  plata ejecutada, los índices técnicos quedan solo en las tarjetas KPI de
  apoyo. Toda celda que dependa de PV (que no existe todavía) muestra
  "Pendiente", nunca 0 ni error.
- **Pendiente explícito de Victor (2026-08-15):** más adelante quiere crear
  agentes que automaticen todo este flujo de trabajo (construir/actualizar
  estos archivos Excel por script + verificación) de forma automática, en
  vez de hacerlo paso a paso en conversación. Todavía no se ha diseñado
  nada de esto — es una intención declarada, no un plan.

## 2026-08-15 (madrugada siguiente) — Arranca py_control_proyectos_web (app web, sub-proyecto Núcleo)

- Victor decidió llevar el sistema a una app web multiusuario (login,
  permisos por rol, base de datos en la nube, desplegable en Vercel desde
  GitHub) en una carpeta nueva **hermana** de esta: `py_control_proyectos_web`
  (mismo nivel que `pg_control_proyectos`, no dentro). Esta carpeta
  (`pg_control_proyectos`) queda como la fuente de dominio/"cerebro" que
  alimenta el diseño de la app — no se duplica contenido, la app la
  referencia.
- Brainstorming arquitectónico (skill `superpowers:brainstorming`): el
  pedido completo (auth + 22 formatos + dashboard + notificaciones) se
  señaló como demasiado grande para un spec y se descompuso en
  sub-proyectos secuenciales: 1) **Núcleo** (auth, roles, Status de
  Proyectos con su flujo de estado) — spec ya escrita y aprobada; 2) carga/
  descarga de datos por formato; 3) dashboard EVM+LPS en la web; 4) Curva S
  de portafolio (la idea ya anotada más abajo en este archivo).
- Spec del Núcleo:
  `../py_control_proyectos_web/docs/superpowers/specs/2026-08-15-nucleo-design.md`.
  Stack elegido: Next.js + Supabase (auth + Postgres + Storage) + Vercel.
  Se descartó reusar el servidor Postgres MCP ya conectado en este entorno
  (tablas `cliente`/`factura`/`productos`, de otro proyecto en
  `mcp_postgresql/`) — instancia de Supabase propia y separada.
- **Cambio de arquitectura de roles, importante:** se creó el rol **Jefe de
  Oficina Técnica**, separado de Supervisor de Oficina Técnica (que
  conserva sus funciones documentarias intactas). Jefe de Oficina Técnica
  es dueño del ciclo de vida del proyecto en el Status de Proyectos:
  marca la adjudicación (eligiendo qué documentos del catálogo "Al inicio"
  aplican a ese proyecto específico), y confirma cada transición de
  estado cuando el checklist de la fase está completo. Esto le quitó a
  **Supervisor de Costos** el permiso de abrir/cerrar el registro que
  tenía en la v2 del documento — Costos conserva la actualización
  periódica del % de avance físico y las alertas de costo.
  `control_de_proyectos.txt` se actualizó a v3 el mismo día para reflejar
  esto (roles, secciones 2.1/2.4/2.6/3, MOF 5.2 nuevo y 5.5 Costos
  ajustado — MOF 5.2–5.9 se renumeraron a 5.3–5.10 para hacerle espacio).
- Flujo de estado final del Núcleo: **En Planeación → Ejecución → Cerrado**
  (renombrado de NO INICIADO/EN PROCESO/TERMINADO por claridad, mismo
  significado). El checklist de cada fase es de **archivos adjuntos, no
  formularios estructurados** — subir el archivo marca el check
  automáticamente; el contenido estructurado de cada formato es el
  sub-proyecto 2, fuera de alcance del Núcleo. El checklist de Ejecución→
  Cerrado quedó, por decisión explícita de Victor "por ahora", con un solo
  ítem: Acta de conformidad (pendiente evaluar si se amplía a los demás
  entregables de cierre ya documentados en la sección 2.6).
- Notificaciones: solo **in-app** por ahora, sin correo.
- **Próximo paso acordado:** con la spec del Núcleo aprobada, sigue el
  plan de implementación (skill `superpowers:writing-plans`), a pedirse
  cuando Victor confirme que quiere avanzar a esa etapa.
- **2026-08-16 — Núcleo implementado y fusionado a `main`.** Se ejecutó el
  plan (14 tareas, skill `superpowers:subagent-driven-development`) en un
  worktree (`py_control_proyectos_web/.worktrees/nucleo`), a lo largo de
  dos sesiones (la primera se cortó a mitad de la Tarea 14 por límite de
  sesión de la plataforma, se retomó limpio en esta). La revisión final de
  todo el branch (22 commits) encontró un bug real de concurrencia: un
  doble clic en "confirmar transición de estado" podía dejar un proyecto
  trabado para siempre (violación de constraint única que dispara un
  rollback, dejando una fila huérfana que el checklist nunca vuelve a leer
  como completo) — se corrigió con compare-and-swap + upsert idempotente +
  deshabilitar el botón mientras envía. También se corrigieron: falta de
  validación de permisos en la ruta de subir documentos (nombre de archivo
  sin sanitizar → riesgo de sobrescribir archivos de otro proyecto), la
  creación de proyecto aceptaba una lista de documentos vacía o con
  documentos de fase equivocada (bypass del checklist), la marca de
  notificación "vista" no verificaba dueño, `/admin/usuarios` no tenía
  enlace de navegación (única forma de crear cuentas, invisible en la UI),
  y el README no alcanzaba para un despliegue real (faltaba crear el
  bucket de Storage, crear el primer Administrador a mano, y configurar la
  Site URL de Supabase Auth para Vercel). Todo corregido, re-revisado
  limpio, fusionado (fast-forward) a `main`. `py_control_proyectos_web`
  queda con: login, roles, portafolio de proyectos con su flujo de
  estado, checklist de documentos, notificaciones in-app — listo para
  desplegar a Vercel siguiendo el README actualizado.
- **Pendiente explícito, quedó fuera de este plan a propósito:** contador
  de notificaciones no vistas en el layout; el contenido estructurado de
  los 22 formatos, el dashboard EVM+LPS y la Curva S de portafolio (sub-
  proyectos 2, 3 y 4 de la spec); vista/descarga/reemplazo de un documento
  ya subido en el checklist (la revisión final lo marcó como hueco de la
  spec, no de la implementación — pertenece al sub-proyecto 2).
- **Ajuste sobre la spec ya escrita (mismo día, revisión de Victor):** se
  agregó **Presupuesto del proyecto** (archivo del presupuesto aprobado,
  responsable Supervisor de Costos) como documento nuevo del checklist
  "Al inicio" — no estaba en el índice de 22 formatos, queda pendiente
  asignarle número formal en la sección 4 más adelante. De paso se
  corrigió un error propio: había puesto "RDO plantilla" como parte del
  catálogo de checklist "Al inicio", pero en el índice esa RDO tiene fase
  "Durante", no "Al inicio" — ya no está en ese catálogo. También se
  confirmó que **Informe de costos NO entra** al checklist de cierre
  (Ejecución→Cerrado); sigue pendiente si entran los otros tres
  entregables de cierre de la sección 2.6 (informe final, RDO
  consolidado, RDTs).

## 2026-08-16 — Núcleo desplegado a Vercel + hoja DP corregida y documentada

- **Despliegue del Núcleo a producción:** repo subido a GitHub (privado),
  importado a Vercel, desplegado en `https://py-control-proyectos-web.vercel.app`.
  En el camino se corrigieron: un env var con valor de plantilla sin editar
  (bloqueaba el login), la Site URL de Supabase Auth (seguía apuntando a
  `localhost`, rota para invitaciones en producción — ya corregida), y se
  detectó que la captura de pantalla de una consola expuso en texto plano
  la `service_role key` real y una contraseña — se roto la key (la vieja
  queda inservible) y se actualizó en Vercel. Después del despliegue se
  corrigió también un detalle de estilo (encabezados de tabla sin espaciado
  horizontal, hueco que venía del código original de la Tarea 9 del plan).
- **`Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DP`: bug real
  encontrado y corregido.** Victor había editado la hoja `DP` y varias
  fórmulas del "Cuadro Resumen" (B2) quedaron apuntando a la celda vecina
  equivocada (corridas una columna, ej. `=H53` en vez de `=G53`) — el TOTAL
  de esa sección sumaba celdas vacías. Además el bloque "Duración estimada
  del proyecto" (agregado el 2026-08-15) quedó completamente vacío y rompió
  un enlace en la hoja `PR` (`#REF!`). Se corrigió todo: las 4 fórmulas de
  costo del Cuadro Resumen, se sacaron las 2 filas de HH del TOTAL (mezclar
  horas con dólares no tenía sentido — confirmado con Victor), y se
  reconstruyó la Duración estimada (176.02 HH totales ÷ (3.06 personas de
  cuadrilla promedio × 10 horas/jornada) = 5.75 días), recalculando la
  cuadrilla promedio y la jornada directamente del archivo APU real
  (`Presupuesto_HDPE_TieIn06-GCI_Promcoser.xlsx`), no de memoria.
- **No existía ningún spec de cómo se construye `DP`** (solo quedaba el
  resumen narrativo de la sesión del 2026-08-15 en este archivo, sin
  script guardado). Se escribió
  `Sistema hibrido/spec-hoja-dp.md`: de dónde sale cada bloque (`CD` +
  `APU`), la regla de agregación de Mano de Obra/Equipos (sumar
  `Cuadrilla × HH-por-persona × Metrado` de cada insumo a través de TODAS
  las partidas donde aparece — verificado contra el APU real con un
  script, no solo leído), la trazabilidad completa `DP → PR`/`DASHBOARD`
  celda por celda, y las limitaciones conocidas (Herramientas menores y la
  cuadrilla promedio de Duración son valores manuales, no fórmulas vivas).
  Es la base para el agente que Victor quiere construir más adelante para
  generar esta hoja automáticamente en proyectos nuevos.

## 2026-08-16 — Arranca sub-proyecto 2 (formatos): correcciones a DP antes del piloto web

- Victor confirmó seguir con `py_control_proyectos_web` (Núcleo ya en
  producción, ver entrada anterior). Brainstorming (skill
  `superpowers:brainstorming`) decompuso sub-proyecto 2 (22 formatos) en:
  A) ver/descargar/reemplazar un documento ya subido en el checklist
  (pendiente, mejora acotada del Núcleo) y B) contenido estructurado por
  formato, empezando con **un piloto** para fijar el patrón antes de
  replicar al resto. Orden acordado: A primero, luego B.
- **Piloto elegido para B: DP** (Datos de Proyecto — vínculo
  APU→DP→PR ya construido en `Sistema hibrido/Consolidado proyecto.xlsx`),
  no un ítem cualquiera del índice de 22 formatos — es, en palabras de
  Victor, "el primer vínculo real entre el presupuesto y el reporte de
  proyecto". Alcance acordado para el piloto: solo DP (línea base) en un
  proyecto individual, dejando el Lookahead de portafolio y la
  configurabilidad de dashboard (LPS por defecto + EVM opcional según
  duración, administrable) como ganchos previstos en el modelo de datos
  pero NO implementados — son sub-proyectos 3/4 futuros. Captura de datos:
  importando el Excel de presupuesto (CD+APU), parseado automáticamente
  (no digitado a mano), siguiendo `spec-hoja-dp.md` como referencia. DP
  estructurado **reemplaza** (no convive con) los ítems de checklist
  "Partidas de control" y "Tabla Work Package" — dejan de ser archivos
  sueltos, pasan a marcarse completos cuando DP tiene datos.
- **Antes de diseñar el importador web**, Victor pidió corregir 3 cosas en
  el Excel real y su spec (orden explícito: primero Excel+spec, recién
  después el diseño web) — hecho el mismo día, ver
  `Sistema hibrido/spec-hoja-dp.md` §2 (C2) y §4.1 para el detalle
  completo:
  1. **Filas dinámicas**: el modelo debe capturar tantas filas de
     MO/equipos/materiales/subcontratos como tenga cada proyecto (uno
     puede tener 5 equipos, otro 10) — ya es el criterio conceptual de
     `spec-hoja-dp.md` (una fila por insumo único), pasa a ser una
     restricción explícita para el importador y el esquema de la web
     (tablas de BD, no rangos fijos de Excel).
  2. **"Herramientas Manuales" (`DP!G62`) ya no es un valor arbitrario**:
     se rastreó en el APU real — es una línea `%MO` (3% del costo de MO
     de esa partida específica) presente solo en algunas partidas (en
     este proyecto: 02.01-02.06 y 04.01, 7 de 15), agregada como
     `Σ (costo unitario de la línea × metrado)` sobre las partidas que la
     tienen. El valor que ya estaba puesto a mano (68.07) resultó ser
     correcto (68.065 calculado) — se documentó la fórmula, no se cambió
     el número.
  3. **Bloque de auditoría agregado a `DP`** (filas 91-104, con fórmulas
     nativas `TEXT()`/`&`, mismo criterio que el Resumen Ejecutivo del
     Dashboard): compara el Costo Directo Total top-down (Work Package,
     `G33`) contra bottom-up (Recursos agregados, `D43`), con veredicto
     automático. Verificado con Excel real vía COM (mismo protocolo de
     recalculo ya usado): diferencia de $0.03 (0.0005%), causada por que
     Work Package guarda el P.U. redondeado a 3 decimales mientras
     Recursos usa el valor sin redondear del APU — no es un error de
     datos, veredicto "OK, dentro de tolerancia".
  - **Aprendizaje técnico real, para cualquier fórmula futura con texto
    largo:** cada literal `"..."` dentro de una fórmula de Excel tiene un
    límite de 255 caracteres. Al construir la nota de auditoría con un
    solo literal largo, el archivo se corrompió *solo para Excel real*
    (`openpyxl` lo seguía leyendo sin quejarse) — el síntoma fue
    `Workbooks.Open` vía COM fallando con un error genérico
    (`-2146827284`) mientras `openpyxl.load_workbook` abría el mismo
    archivo sin error. Se resolvió partiendo el texto en fragmentos
    cortos unidos con `&`. Aplica a cualquier fórmula futura con texto
    narrativo largo (p. ej. el Resumen Ejecutivo del Dashboard, que ya
    usa el mismo patrón `TEXTJOIN`/`&` — revisar que ningún fragmento
    individual pase de 255 caracteres).
  - **Protocolo de recalculo vía COM, nota operativa:** si `Workbooks.Open`
    falla con un error genérico sin causa obvia, revisar primero si quedó
    un proceso `EXCEL.EXE` huérfano de un intento anterior fallido (no se
    llegó a `Quit()` tras una excepción) antes de asumir que el archivo
    está corrupto — en esta sesión pasaron ambas cosas a la vez y había
    que descartarlas por separado.
  - Se hizo un backup (`Consolidado proyecto.xlsx.bak-<fecha>`) antes de
    editar, borrado al confirmar que la corrección quedó bien — no se
    deja como archivo permanente del proyecto.
- **Próximo paso acordado:** con el Excel+spec corregidos, sigue diseñar
  el importador web de DP (modelo de datos, cómo se marca el checklist,
  ganchos de configuración futuros) — el brainstorming se retoma desde
  ahí, todavía no se ha escrito la spec de sub-proyecto 2 en
  `py_control_proyectos_web/docs/superpowers/specs/`.
