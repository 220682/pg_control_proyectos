# Brief T1C — Maqueta de la bandeja de avisos (T1-07)

## Rol, modelo y tanda

Worker de diseño (maqueta HTML) · Sonnet · esfuerzo medio · tanda **T1C** (cierre de T1). Se lanza como «Worker maqueta · T1C». No escribe código de la app, no usa el navegador (otro Worker lo ocupa) y no hace commits.

## Ítem de la tanda

| ID | Qué | Evidencia mínima |
|---|---|---|
| T1-07 | Maqueta de la bandeja de avisos con **Entorno**, **N° OT**, grupo **Jefatura**, filtro **Tipo de aviso**, botón **Devolver** con motivo y RQ **Devuelto** (con la acción de corregir y reenviar). Victor la aprueba antes de la parte visual de T3 y T5 | `docs/05-diseno-y-referencias/mockups/notificaciones-bandeja.html` y un párrafo de «qué debe aprobar Victor» en el resumen |

## Qué debe mostrar (decisiones de Victor ya tomadas)

1. **Bandeja** (`/notificaciones` y la lista de Mi entorno son la misma información): cada aviso con insignia **N° OT** (ej. `PS-0000`) o insignia **Entorno** cuando el aviso no pertenece a un servicio (mismo estilo que la insignia de OT); texto, remitente, fecha, estado (Pendiente, Revisado, Atendido) y grupo.
2. **Filtros:** los actuales (servicio/OT, estado, grupo) más el nuevo **Tipo de aviso**: Requerimientos, RDT, Servicio, Checklist, Mensajes, Otros. El grupo se llama **Jefatura** (ya no «Proyecto»): lista de grupos Jefatura, Planificación, Costos, Supervisión operativa, Logística, Oficina Técnica, Administración, SSOMA.
3. **Aviso de RQ con acciones:** un aviso de RQ Solicitado para quien puede aprobar muestra **Aprobar** y **Devolver**. «Devolver» abre un campo de motivo obligatorio (hasta ~500 caracteres, contador) y confirma. Muestra también el estado vacío del motivo (error «Escribe el motivo»).
4. **RQ Devuelto:** el solicitante recibe un aviso «Requerimiento <código> devuelto por <nombre>: <motivo>» con la acción **Corregir y reenviar**; también la vista del RQ Devuelto (insignia de estado propia, motivo visible, ítems/cantidades/fecha/prioridad editables, adjuntos solo lectura, botón **Reenviar**). Un Devuelto no se puede aprobar: muestra el botón deshabilitado con su explicación.
5. **Aviso de Logística:** al abrirlo, el RQ pasa a Recepcionado solo; muestra el aviso antes y después (estado actualizado), y la nota de que la persona de Logística que lo abre lo cierra para sus compañeras.
6. **Campana** con el contador de pendientes.
7. Una vista a 390 px (móvil) de la bandeja con un aviso.

## Qué leer, y qué no (en este orden)

1. `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\05-diseno-y-referencias\design.md`: secciones 0, 3 (layout global, «Toda maqueta del plan se muestra con los tres paneles»), 4 (tokens) y 5 (componentes) por encabezados; el resto no.
2. Modelo de maqueta vigente: `docs\05-diseno-y-referencias\mockups\informes-supervision.html` (estructura, no contenido), `marco-tres-paneles.css` y `marco-tres-paneles.js`: **reutiliza el marco, no lo copies ni lo cambies**.
3. App, solo para copiar el aspecto actual (`D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`): `src/app/(workspace)/notificaciones/ListaNotificaciones.tsx`, `src/components/ui/AccionesRqEnNotificacion.tsx` y `DetalleRqNotificacion.tsx`.

No leas el plan, los flujos ni otras maquetas.

## Qué puede trabajar

Crear **solo** `docs/05-diseno-y-referencias/mockups/notificaciones-bandeja.html` y el resumen en `...\01-planes\2026-10-16-notificaciones-estandar-y-supervisor-operativo-briefs\resultados\T1C.md`. **No tocar** `mockups/index.html` ni `mockups/README.md` (tienen cambios de otras sesiones; el Orquestador los enlaza después), ni el marco compartido, `design.md`, flujos ni código de la app. Datos de ejemplo ficticios y claramente de prueba (PS-0000, «PRUEBA»); sin datos reales.

## Límites

50 llamadas como meta. Reutiliza los componentes y tokens existentes; si falta algo que obligue a crear un componente nuevo, descríbelo en el resumen y no lo inventes. Una duda de negocio o un choque con un flujo se devuelve al Orquestador en el momento.

## Resumen de cierre

Plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md`, en `resultados/T1C.md`. Incluye: qué pantallas trae el archivo y cómo abrirlas, qué decisiones de diseño deben aprobarse y qué componentes del diseño actual se reutilizaron.

## Criterios de salida

El archivo abre solo con doble clic, se ve con los tres paneles, muestra los siete puntos de arriba y no modifica ningún otro archivo.
