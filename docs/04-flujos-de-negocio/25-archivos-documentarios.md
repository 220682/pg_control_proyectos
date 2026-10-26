# 25 — Gestión documentaria (antes «Archivos documentarios»)
> Lee si: la tarea toca el apartado «Gestión documentaria» (el árbol de archivos de cada documento por área y tipo, la versión vigente, los estados de archivo Aprobado/En revisión/Observado/Falta, los comentarios, abrir y descargar, la subida a mano) o el almacén de archivos en Cloudflare R2 y la copia de adjuntos desde Gmail.

Origen: plan [Archivos documentarios](../02-trabajo-activo/01-planes/2026-10-25-repositorio-de-archivos-documentarios.md) (pedido de Victor el 2026-10-25). Es la **tercera de tres interfaces**: 1 [Gestión de interesados](23-estado-del-servicio.md) (de dónde salen los correos), 2 [Gestión documentaria](24-gestion-documentaria.md) (el estado de cada documento), 3 esta (los archivos). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md); la lista de pantallas, en el [flujo 16](16-paneles.md).

## Qué es

Una pantalla por servicio (`/proyectos/{id}/gestion-documentaria`, chip «Gestión documentaria» en el grupo Planificación) que muestra **los archivos de cada documento de la Gestión de emails**, ordenados como carpetas: **Área → Tipo → Documento**. El servicio es la propia página, no una carpeta. Cada documento es una fila con su **archivo vigente**; sus demás archivos son **versiones**.

## Árbol y filas (calcado de la maqueta del dossier)

Victor pidió el 2026-10-25 que esta pantalla se parezca a la maqueta `maqueta_dossier`: un árbol denso de carpetas y archivos con dos columnas editables, no tarjetas. Tiene el encabezado **Carpeta / archivo · Observaciones · Estado** y, a la derecha de cada archivo, las acciones.

* **Carpetas:** el **área** va en una banda de color (como los tomos de la maqueta) y el **tipo**, en ámbar y negrita, con cuántos documentos y archivos tienen; el área marca además cuántos **faltan**. Las carpetas vacías no aparecen. Hay «Expandir todo», «Colapsar todo» y la casilla **«Solo carpetas»** (la estructura sin los documentos). Al buscar por texto el árbol se abre solo.
* **Fila de archivo:** cada documento con archivo es una fila con el **nombre del documento y su revisión**, debajo el **nombre del archivo vigente y su fecha**, la marca **«Nuevo»** (más un borde verde a la izquierda) si el archivo es de los últimos 7 días, la **observación** (el comentario de esa versión, editable por el administrador: se guarda al salir del campo o con Enter) y el **estado** (lista para el administrador, etiqueta de color para los demás). A la derecha: **Abrir** (pestaña nueva), **Descargar** y **Correo** (el correo que traía el archivo). Junto al nombre, un contador abre las **versiones**, una fila por archivo con su propia observación y estado.
* **Documento sin archivo:** una **fila punteada** en cursiva con el campo «sin archivo — anota aquí lo que falta» y el estado **Falta**. Lo que se anota ahí es la **nota del documento** (la misma que se ve en la Gestión de emails). Un documento que solo tiene archivos de referencia (por ejemplo, la solicitud del cliente) también está en **Falta**: no hay entregable.
* **Resumen y filtros:** abajo, un resumen con el total y un punto de color por estado (verde Aprobado, azul En revisión, ámbar Observado, rojo Falta) con su conteo; tocarlo filtra. Arriba: búsqueda por texto (sin tildes, en el nombre del documento y de sus archivos), **área**, **tipo** y la casilla **«Solo sin aprobar»** (todo lo que no está aprobado, incluido lo que falta).
* **Se actualiza solo:** la pantalla vuelve a leer los datos cada 30 segundos mientras está a la vista y nadie escribe, así lo que llega de los correos aparece sin recargar.
* **Pendientes (.md):** baja un archivo Markdown con lo que no está aprobado, por área y tipo, cada documento con su estado y su observación (o la nota si falta el archivo): el equivalente a la lista de pendientes de la maqueta.

## De dónde salen los archivos y su estado

Cada **adjunto** de los correos de un documento es una versión, con tres limpiezas: no cuentan las **imágenes** (firmas, logos, capturas), las invitaciones de calendario ni los correos reenviados; si el mismo archivo (mismo nombre y tamaño) viene repetido en varias respuestas del hilo, **queda el más antiguo**; y los correos que son copia en el otro buzón se leen una sola vez (los adjuntos viven en el correo original). El **estado nace del movimiento del correo** que traía el archivo:

| Movimiento del correo | Estado de la versión |
|---|---|
| Enviado | En revisión |
| Observado | Observada |
| Aprobado | Aprobada |
| Solicitud o Información | Referencia (no cuenta como entregable) |

Las versiones se ponen al día solas cada vez que se abre la pantalla: se crean las que faltan, se corrige el estado de las que nadie tocó a mano y se quitan las que dejaron de pertenecer al documento (solo si nadie les escribió un comentario ni cambió su estado). El administrador puede **corregir el estado a mano** (el sistema lo marca «(a mano)» y ofrece «Automático» para volver al del correo), y escribir una **observación** (el comentario de la versión). La etiqueta corta (Rev. 1, Final…) se sigue mostrando si existe, pero la pantalla ya no la edita.

## Versión vigente y estado del documento

La **versión vigente** es la **última aprobada**; si no hay ninguna aprobada, la **última que no sea de referencia** (y se avisa «Aún sin aprobar»); si solo hay referencias, no hay vigente. El estado del documento sale de su vigente: Aprobado, En revisión u Observado, o **Falta** si no la hay. **Los archivos no se mueven ni se copian al aprobar:** «aprobados por área» es solo el filtro Estado = Aprobado dentro de esa área.

## Almacén de archivos (Cloudflare R2)

* Los archivos viven en un bucket privado de **Cloudflare R2**, no en Supabase. Las claves de R2 solo las usa el servidor; el navegador nunca las ve.
* **Abrir y descargar** no usan un enlace permanente: el servidor comprueba el permiso sobre el servicio y recién entonces redirige a un **enlace firmado de 5 minutos**. Abrir muestra el archivo en una pestaña nueva si el navegador puede (PDF, imágenes); si no, lo baja. Los adjuntos que ya estaban en el almacén anterior de Supabase se siguen sirviendo desde allí.
* **Claves estables:** `servicios/{número}/adjuntos/{id del adjunto}/{nombre}` para los de correo y `servicios/{número}/manuales/{id de la versión}/{nombre}` para los subidos a mano. No dependen del área ni del nombre del documento, para que cambiar un documento de área no deje la copia desubicada.
* **Copia de adjuntos desde Gmail:** el sistema solo guardaba el nombre, el tipo y el tamaño de cada adjunto; el archivo seguía en Gmail. «**Copiar adjuntos pendientes**» (botón del administrador, y un paso horario en el mismo disparador de la lectura de correos) vuelve a leer el mensaje en el buzón donde llegó —o en el de su copia—, empareja el adjunto por nombre y tamaño y lo sube a R2. Cada llamada avanza lo que alcanza en unos 50 segundos y avisa cuántos quedan. No se copian archivos de más de 30 MB; mientras un archivo no esté copiado se ve «Pendiente de copiar» y no se puede abrir.
* **Subida a mano:** la pantalla **ya no tiene botón «Subir»** (Victor no quiere subir archivos desde la app). El código del servidor para subir y borrar archivos a mano sigue en la base y las rutas, sin uso, porque el bucket no tiene política CORS.

## Permisos

Provisorios, iguales a los de la Gestión de emails para **ver**: el administrador, el jefe de proyecto, el jefe de oficina técnica y el supervisor de oficina técnica, dentro de los servicios a su alcance (ver, abrir, descargar). **Gestiona** —estado a mano, observación, lo que falta de un documento sin archivo y copiar adjuntos— **solo el administrador**. Victor dejó para el final la regla «todos ven, solo el administrador edita»; al aplicarla se cambia aquí, en el flujo 14 y en la Matriz de permisos.

## Pendiente de este flujo

El árbol es el **destino único de archivos**: hoy solo entran los adjuntos de Fuente-Gmail. Los archivos de Fuente-WhatsApp (que esperan el almacén R2) y los de Fuente-Drive (paso 3 del plan de fuentes) entrarán como versiones del mismo documento, sin repetirse (mismo nombre y tamaño = un solo archivo), cuando esas fuentes los traigan.

## Qué no es

No hay visor de PDF dentro de la app, firma electrónica, sincronización de carpetas en vivo ni edición de archivos. Los datos de los correos y los archivos nunca se guardan en el repositorio.

## Datos

Columna `estado_adjuntos.ruta_r2` (clave del archivo en R2; vacía = aún no copiado) y tabla `doc_versiones` (documento, adjunto de origen, nombre, tipo, tamaño, clave en R2 de las subidas a mano, etiqueta, estado, si el estado es a mano, comentario, origen `CORREO|MANUAL`, fecha del correo o de la subida) en [db/121](../../../py_control_proyectos_web/db/121_archivos_documentarios.sql). La «versión vigente» y el estado del documento no se guardan: se calculan. Variables de entorno del servidor: `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` y `R2_BUCKET`; el bucket necesita una política **CORS** que permita `GET`, `HEAD` y `PUT` desde el dominio de la app (la subida a mano no funciona sin ella; el 2026-10-25 Victor dijo que no quiere subir archivos desde la app, así que el CORS no se configura por ahora).
