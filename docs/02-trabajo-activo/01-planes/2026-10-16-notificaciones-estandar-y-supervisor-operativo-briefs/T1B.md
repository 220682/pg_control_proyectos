# Brief T1B — Comprobar el cierre de avisos y «cómo funciona hoy» (ciclo del RQ y bandeja del supervisor operativo)

## Rol, modelo y tanda

Worker de verificación · Sonnet · esfuerzo medio · tanda **T1B** (segunda mitad de T1). Se lanza como «Worker verificación · T1B». No escribe código ni hace commits: la evidencia queda en archivos y el Orquestador los commitea. Usa el **único navegador** (herramientas `mcp__playwright__*`; cárgalas con ToolSearch en una sola llamada): ningún otro Worker lo usa mientras tú trabajas.

## Ítems de la tanda

| ID | Qué | Evidencia mínima |
|---|---|---|
| T1-03 (comprobación) | Victor dice que ya aplicó `cerrar-avisos-restantes.sql`. Comprueba en la app, con su sesión, que sus 18 avisos recibidos quedaron en ATENDIDO y que los RQ siguen igual | Conteo por estado antes (del respaldo) y después |
| T1-04 | Informe «cómo funciona hoy» del ciclo del RQ en `PS-0000`: crear, aprobar, Logística recibe, En almacén, Atendido | `informe-ciclo-rq-hoy.md`: una fila por paso con quién actúa, a quién llega el aviso, a quién **no**, texto exacto y qué aviso se cierra |
| T1-05 | Informe «cómo funciona hoy» de la bandeja del supervisor operativo, y prueba con dos personas del mismo rol (hallazgo H8) | `informe-bandeja-supervisor-hoy.md` y una captura de la bandeja de cada persona antes y después de que una abra o atienda el aviso |

## Qué leer, y qué no (en este orden)

1. Memoria: `C:\Users\BRANDY\.claude\projects\D--VICTOR-CLAUDE-CODE-pg-control-proyectos\memory\cuentas-prueba.md` (cuentas y claves; úsalas directamente en el formulario, nunca en el chat, en archivos ni en capturas).
2. Evidencia de T1A, en `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\02-trabajo-activo\03-evidencia\2026-10-16-notificaciones-estandar-y-supervisor-operativo\`: `datos-de-prueba.md`, `respaldo-avisos-victor-todos.json` y `estado-rq-antes.json`.
3. Flujo `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\05-rq.md` (ciclo del RQ).
4. App (`D:\VICTOR\CLAUDE CODE\py_control_proyectos_web`, solo para saber qué esperar; lo que cuenta es lo que ves): `src/app/api/proyectos/[id]/requerimientos/route.ts`, `.../[rqId]/estado/route.ts` y `src/lib/requerimientos/transicion-notificar.ts`.

No leas el plan ni los demás flujos.

## Cuentas y producción

Producción: `https://py-control-proyectos-web.vercel.app` (es `main`, tal como está hoy: así se documenta «cómo funciona hoy»). Cuentas: administrador (`victorperez.nj`), supervisor operativo (`jeyger22`), `victor.sup22+logistica1` y `victor.sup22+logistica2` (supervisor de Logística, miembros de `PS-0000`). Faltan por crear las de jefe de proyectos, jefe de oficina técnica, segundo supervisor operativo y supervisor de administración (límite de correos de Supabase): **no las crees**. Sin ellas, el aprobador es el administrador y el solicitante es `jeyger22`. Cierra sesión entre una cuenta y otra.

## Qué puede trabajar

Escribir solo en la carpeta de evidencia indicada arriba y en `...\01-planes\2026-10-16-notificaciones-estandar-y-supervisor-operativo-briefs\resultados\T1B.md`. En la app, crear **únicamente en `PS-0000`** datos marcados «PRUEBA» (por ejemplo, en la descripción o el título del RQ), y solo los RQ que necesita el recorrido (uno completo; un segundo solo si lo exige T1-05). **No** borres nada, no cambies estados de RQ ajenos, no toques otros servicios ni otros usuarios.

## Cómo hacerlo

**T1-03.** Con la sesión de Victor haz `fetch('/api/notificaciones?direccion=recibidos')` (sin `visto`) y cuenta por estado. Se esperan 18 en ATENDIDO. Si quedan pendientes, repórtalos (no uses `atender`; si hace falta cerrar alguno, devuelve la lista al Orquestador). Revisa que `PS-0000` sigue sin RQ ajenos a los tuyos.

**T1-04.** Recorrido, con cuentas distintas y mirando **la bandeja de todos los roles implicados** (administrador, `jeyger22`, `logistica1`, `logistica2`) tras cada paso: (1) `jeyger22` crea el RQ; (2) el administrador lo aprueba (desde el aviso, para ver el comportamiento real); (3) Logística 1 abre el aviso y luego usa su botón de recepcionar; (4) En almacén; (5) Atendido. En cada paso anota: quién recibe aviso, quién no, texto exacto, qué aviso anterior se cerró y cuál quedó pendiente, y qué cambia en la campana. Anota también cualquier paso que no avise a nadie.

**T1-05.** Con el RQ del recorrido o uno aparte: lista qué le llega y qué no al supervisor operativo (aviso por RQ, comentario sobre su RQ, RDT validado o rechazado, servicio asignado: lo que puedas probar sin alterar datos ajenos; lo demás, «no probado»). Con `logistica1` y `logistica2`, que comparten rol: captura la bandeja y el contador de la campana de **ambas** antes de que una abra el aviso, después de que una lo abra y después de que lo atienda. Anota si el cambio de una se refleja en la otra.

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes y escribe el traspaso. Una captura por ítem como máximo (sin claves a la vista). No uses acciones de borrado. Si una pregunta de negocio o un conflicto con un flujo aparece, devuélvela al Orquestador en el momento.

## Resumen de cierre

Plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md`, en `resultados/T1B.md`. Hallazgos en los cinco grupos; nunca escribas claves.

## Criterios de salida

Conteo de avisos de Victor comprobado, dos informes escritos con una fila por paso, capturas de las dos personas del mismo rol, y la lista de lo que no se pudo probar y por qué.
