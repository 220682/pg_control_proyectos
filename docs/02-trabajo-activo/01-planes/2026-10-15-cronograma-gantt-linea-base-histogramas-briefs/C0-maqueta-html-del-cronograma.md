# Brief de tanda C0 — Maqueta HTML del cronograma

## Rol, modelo y tanda

CR-1, nivel 2 (n2), **Haiku** (Victor pidió Haiku para las tareas simples; la maqueta la revisa él antes de C1, así que un error se detecta barato), esfuerzo Medio. Ola 0. Se lanza como «Worker CR-1 · C0». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-01**: Maqueta de tres paneles con tabla y Gantt (barra base, barra de seguimiento con %, resumen, hito, flechas, hoy, leyenda). Evidencia: abrir el HTML sin errores de consola, una captura.
- **CG-02**: Cuatro estados (vacío, cargando, error, datos) y las tres puertas de creación (DP, archivo, a mano).
- **CG-03**: Pestaña Histogramas: barras HH/HM, acumulado, pico, filtros cargo/equipo, rótulo programado/estimado.
- **CG-04**: Interruptor modo RDT / manual, etiqueta «Manual», historial y selector de línea base.
- **CG-05**: Opciones de exportar y vista móvil solo lectura; enlace en mockups/index.html y README.md.
- **CG-06**: Victor aprueba (lo hace el Orquestador al presentarla; el Worker no declara aprobada).

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Sin rama ni worktree: esta tanda no toca código de la app. La maqueta vive en el repo documental (`D:\VICTOR\CLAUDE CODE\pg_control_proyectos`), directo en `main`. No crees rama, no hagas commit ni push: deja los archivos sin commit y el Orquestador los sube (hay otros cambios sin commit de otros planes en `mockups/index.html` y `mockups/README.md`: edítalos sin sobrescribir). Si Playwright no abre `file://`, sirve la carpeta con `python -m http.server 8123` desde `mockups/` y detenlo al terminar.

## Qué leer, y qué no

- docs/05-diseno-y-referencias/mockups/plan-maestro-tres-paneles.html y cronograma-niveles.html (partir de ellos), marco-tres-paneles.css/.js
- docs/05-diseno-y-referencias/design.md §1, §3, §5, §8, §13
- docs/06-material-de-apoyo/Informacion para pruebas/CRON-PROMCOSER-AESA-001.pdf (usar pdftotext -layout o PyMuPDF con python -I; el Read no renderiza PDF)
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: Crear docs/05-diseno-y-referencias/mockups/cronograma-editor-gantt.html (nuevo)
- Puede: Agregar solo la entrada en mockups/index.html y mockups/README.md (ya tienen cambios sin commit del Orquestador: editar, no sobrescribir)
- NO puede: Código de la app, flujos, design.md, AGENTS.md, el Spec
- NO puede: No usar el morado de MS Project: tokens del sistema
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Entrega: `docs/05-diseno-y-referencias/mockups/cronograma-editor-gantt.html` (sin commit).
- Resumen de cierre: `resultados/C0.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- Sin librería de Gantt ni de gráficos (design.md §1 y §13): SVG o rejilla CSS a mano, como la Curva S.
- Semana de sábado a viernes; calendario lunes a sábado; línea «hoy» punteada con su fecha; nunca solo color.
- Árbol con sangría de 14 px; columnas Id, EDT, Nombre, Duración, Comienzo, Fin, Predecesoras, Sucesoras, % avance, variación de fin.
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- dataviz (reglas de color y leyenda de los gráficos)

## Comandos de verificación

- Abrir el HTML con Playwright (file://) y revisar consola; una captura por ítem como máximo.

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Ronda 2 (pedida por Victor el 2026-10-15, tras revisar la primera entrega)

Victor aprobó tres cosas y pidió mejorar el acabado. Aprobado: la paleta de colores de las series de los histogramas (azul, naranja, verde, ámbar, magenta); «Var. fin» en **días laborables** (lunes a sábado, sin los no laborables; rótulo «d lab.»); **Comienzo y Fin siempre visibles** en la tabla a 1440 px (el resto con desplazamiento horizontal).

Su observación: el acabado se ve básico y **no hay leyenda ni nada que diga qué está viendo**. La captura que mandó era la pestaña Histogramas con los paneles «Ambos ocultos», filtro Cargo = Operario y Equipo = Retroexcavadora: un solo color de barras, el eje «300» sin unidad, ningún título de ejes, la leyenda y las etiquetas de semana quedaban **fuera de la pantalla** (debajo del gráfico), sin texto que explique qué significa el color ni qué filtra cada selector.

Qué mejorar (todo dentro del mismo archivo `cronograma-editor-gantt.html`, sin librerías):

1. **Leyenda y explicación siempre a la vista**, arriba del gráfico, no debajo: qué muestran las barras (HH programadas por semana), qué es cada color, qué es la línea (acumulado) y qué es el número sobre la barra (el pico). Con un filtro activo, un rótulo «Mostrando: Operario» y el color de esa serie en la leyenda.
2. **Ejes con título y unidad**: eje vertical «HH por semana» (y «HM por semana» en el otro gráfico), eje horizontal «Semana (sábado a viernes)» con las etiquetas de fecha legibles en todas las barras.
3. **Filtros claros**: aclarar que Cargo filtra el gráfico de HH y Equipo el de HM; botón «Quitar filtros».
4. **Cada gráfico completo cabe en una pantalla de 900 px de alto** (ejes, leyenda y pie sin desplazarse), con los paneles en cualquier combinación y a 1440 y 1920 px de ancho.
5. **Cronograma**: Comienzo y Fin siempre visibles; «Var. fin» en días laborables; ayuda al pasar el cursor sobre cada barra (base, seguimiento, % y fechas) y sobre cada encabezado de columna; un botón «¿Qué veo?» que abre una explicación breve de cada elemento del Gantt (barra base, barra de seguimiento, resumen, hito, flecha, línea Hoy).
6. **Acabado general**: jerarquía visual, espaciados, estados al pasar el cursor y activos, coherencia con `design.md`; que no parezca un borrador.
7. **Verificación**: capturas del histograma y del Gantt a 1440 y a 1873 px de ancho con «Ambos ocultos» y con «Tres abiertos», sin errores de consola; en cada captura se debe leer la leyenda y los ejes sin desplazarse. Una captura por ítem como máximo.

## Criterios de salida

- Los 5 ítems funcionales hechos y el CG-06 dejado para Victor. Una tanda no se cierra con un ítem a medias.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
