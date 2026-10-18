# Resumen de cierre — T1C

## Tanda, rol y modelo

T1C (cierre de T1) · Worker de maqueta · Sonnet · esfuerzo medio. Sin navegador (lo ocupaba otro Worker) y sin commits.

## Estado de los ítems

| ID | Estado | Evidencia | Causa y quién lo resuelve |
|---|---|---|---|
| T1-07 | Observado | Archivo `docs/05-diseno-y-referencias/mockups/notificaciones-bandeja.html`. Las tres etiquetas `<script>` pasan la comprobación de sintaxis con Node (`new Function`). Revisión del código contra los siete puntos del brief. **No se abrió en navegador** (restricción del brief), así que falta la revisión visual a 1440 px y 390 px | Pasa a Conforme cuando el Orquestador o Victor la abran y confirmen que se ve bien |

Los siete puntos del brief, y dónde está cada uno:

1. Bandeja con insignia N° OT (`PS-0000`) o Entorno, texto, remitente, fecha, estado y grupo: vista 1.
2. Filtros: dirección, OT, estado, grupo y el nuevo Tipo de aviso (Requerimientos, RDT, Servicio, Checklist, Mensajes, Otros). El grupo se llama Jefatura y la lista tiene los ocho grupos: vista 1.
3. Aprobar y Devolver en el RQ Solicitado, con motivo obligatorio, contador de 500 y error «Escribe el motivo»: vistas 1 y 2 (la 2 tiene botones para cada estado).
4. RQ Devuelto: aviso «Requerimiento … devuelto por …: motivo» con Corregir y reenviar (vista 1 con el rol Solicitante, y vista 3). La pantalla del RQ Devuelto tiene insignia propia, motivo visible, ítems, cantidades, fecha y prioridad editables, adjuntos solo lectura y Reenviar. Aprobar queda deshabilitado con su explicación escrita: vista 3.
5. Logística: aviso antes y después (RQ pasa solo a Recepcionado) y la nota de que quien lo abre lo cierra para sus compañeras: vista 4. También se prueba en vivo en la vista 1 con el rol Logística.
6. Campana con contador de pendientes: en la cabecera de la bandeja (se actualiza al abrir avisos) y en el icono de campana del panel izquierdo del marco, sincronizado con ese contador.
7. Vista a 390 px con un aviso de RQ abierto: vista 5.

## Rama, commits y archivos tocados

Rama `main`, sin commits. Archivos creados: `mockups/notificaciones-bandeja.html` y este resumen. Verificado con `git status`: no se modificó `index.html`, `README.md`, `design.md`, el marco compartido ni la app (los modificados que aparecen eran de otras sesiones). Reutiliza `marco-tres-paneles.css` y `.js` sin cambios, con el chip activo `notif`.

## Cómo abrirla

Doble clic al archivo. La barra negra de arriba cambia de vista (1 a 6), el rol (Jefatura que aprueba, Solicitante, Logística), la insignia (texto o pastilla) y los paneles. «Restablecer» devuelve los datos de ejemplo. Datos ficticios: PS-0000, PS-0001 y personas «PRUEBA».

## Qué debe aprobar Victor

(Misma lista en la vista 6 de la maqueta.) 1) La insignia de OT y Entorno: hoy la OT es solo texto de acento; se muestra el Entorno con ese mismo estilo y se ofrece una pastilla pequeña igual para ambos: ¿texto o pastilla? 2) El filtro Tipo de aviso junto al de Grupo, con el grupo renombrado a Jefatura. 3) La opción agregada «Solo Entorno» en el filtro de OT. 4) Aprobar (acento) y Devolver (borde rosa) lado a lado. 5) El motivo obligatorio con contador, error con icono y confirmación explícita. 6) El RQ Devuelto, con una pregunta: ¿el solicitante puede quitar y agregar ítems o solo cambiar los que hay? 7) Un Devuelto no se aprueba (botones deshabilitados y explicación visible). 8) Logística: abrir el aviso recepciona solo y lo cierra para sus compañeras. 9) Al abrir un aviso se ve el texto completo (la fila lo corta con «…» como hoy), porque un motivo largo no cabría.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| T1C-H1 | observación sobre la política / conflicto con un flujo | El panel derecho del marco compartido no trae el grupo «Jefatura» (arranca en Planificación) y el filtro de grupo de la app aún dice «Proyecto». La maqueta usa Jefatura según el brief; el marco no se tocó | Orquestador: decidir si se ajusta el marco (`MARCO_AJUSTE` por maqueta o cambio al marco) y revisar el flujo 14/16 |
| T1C-H2 | conflicto con un flujo o pregunta para Victor | No está definido si el solicitante puede agregar y quitar ítems al corregir un RQ Devuelto; la maqueta muestra ambas opciones | Victor, al aprobar la maqueta |
| T1C-H3 | mejora de trabajo | Sin navegador, la verificación quedó en sintaxis y revisión de código | Pasar una revisión visual (1440 y 390 px) antes de aprobar |

## Componentes reutilizados y nuevos

Reutilizados: marco de tres paneles (paneles, cajones móviles, asistente, campana del pie), `ListaNotificaciones` (fila con insignia de dirección, texto truncado, estado Pendiente/Revisado/Atendido, filtros select), `AccionesRqEnNotificacion` (chips de pasos por rol, botones de Logística, «RQ: estado»), `DetalleRqNotificacion` («Lo solicitado», ítems, enlaces), botones y colores semánticos del design.md §4.1.1 (rosa para rechazo, verde, ámbar), sin colores ni tokens nuevos.

Piezas nuevas (solo composición, a aprobar): bloque «Devolver con motivo» (textarea + contador + error), insignia rosa «Devuelto» del RQ, caja de motivo del solicitante, botón «Corregir y reenviar», insignia Entorno y filtro Tipo de aviso (marcados NUEVO en la maqueta con contorno punteado ámbar).

## Traspaso

Hecho: la maqueta completa con seis vistas y los siete puntos. Falta: revisión visual en navegador y la aprobación de Victor antes de la parte visual de T3 y T5; el Orquestador enlaza la maqueta en `index.html` y `README.md` de mockups (no se tocaron).

## Llamadas y contexto

Unas 20 llamadas en total (lecturas de design.md, marco y app, escritura del archivo, comprobación de sintaxis y este resumen).

## Skills revisados

Ninguno aplica: tarea de maqueta HTML acotada por el brief.

## Fuentes de verdad revisadas

Ninguna actualizada. Quedan para el Orquestador: flujos 14 y 16 (grupo Jefatura, Tipo de aviso) y `design.md` (insignia Entorno, bloque de devolución, insignia Devuelto) una vez que Victor apruebe.
