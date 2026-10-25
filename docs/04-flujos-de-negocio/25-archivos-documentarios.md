# 25 — Archivos documentarios
> Lee si: la tarea toca el apartado «Archivos documentarios» (el árbol de archivos de cada documento por área y tipo, la versión vigente, los estados de archivo Aprobado/En revisión/Observado/Falta, los comentarios, abrir y descargar, la subida a mano) o el almacén de archivos en Cloudflare R2 y la copia de adjuntos desde Gmail.

Origen: plan [Archivos documentarios](../02-trabajo-activo/01-planes/2026-10-25-repositorio-de-archivos-documentarios.md) (pedido de Victor el 2026-10-25). Es la **tercera de tres interfaces**: 1 [Gestión de interesados](23-estado-del-servicio.md) (de dónde salen los correos), 2 [Gestión documentaria](24-gestion-documentaria.md) (el estado de cada documento), 3 esta (los archivos). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md); la lista de pantallas, en el [flujo 16](16-paneles.md).

## Qué es

Una pantalla por servicio (`/proyectos/{id}/archivos-documentarios`, chip «Archivos documentarios» en el grupo Planificación) que muestra **los archivos de cada documento de la Gestión documentaria**, ordenados como carpetas: **Área → Tipo → Documento**. El servicio es la propia página, no una carpeta. Cada documento es una fila con su **archivo vigente**; sus demás archivos son **versiones**.

## Árbol y filas

* **Carpetas:** cada área y cada tipo muestran cuántos documentos y cuántos archivos tienen; el área marca además cuántos **faltan**. Las carpetas vacías no aparecen. Hay «Expandir todo», «Colapsar todo» y la casilla **«Solo carpetas»** (muestra la estructura sin los documentos). Al buscar por texto el árbol se abre solo.
* **Fila de documento:** nombre y revisión, **estado** (Aprobado, En revisión, Observado o **Falta**), el archivo vigente (nombre, fecha, tamaño), el comentario de esa versión, la marca **«Nuevo»** si el archivo es de los últimos 7 días, y los botones **Abrir** (pestaña nueva), **Descargar**, **Ver versiones**, **Ficha** (lleva a la Gestión documentaria) y, para el administrador, **Subir**.
* **Documento sin archivo:** aparece igual, con estado **Falta**, para que se vea qué no hay. Un documento que solo tiene archivos de referencia (por ejemplo, la solicitud del cliente) también está en **Falta**: no hay entregable.
* **Versiones:** cada una muestra nombre, etiqueta, estado, fecha, tamaño, si vino de un correo o se subió a mano, su comentario, el botón **Correo** (abre el correo completo, con «Abrir en Gmail») y Abrir/Descargar.
* **Resumen y filtros:** tarjetas con el total y los conteos por estado (se pueden tocar para filtrar); filtros por **área, tipo, estado, texto** (sin tildes, en el nombre del documento y de sus archivos) y **«Solo faltantes»**; «Sin aprobar» agrupa todo lo que no está aprobado, incluido lo que falta.

## De dónde salen los archivos y su estado

Cada **adjunto** de los correos de un documento es una versión, con tres limpiezas: no cuentan las **imágenes** (firmas, logos, capturas), las invitaciones de calendario ni los correos reenviados; si el mismo archivo (mismo nombre y tamaño) viene repetido en varias respuestas del hilo, **queda el más antiguo**; y los correos que son copia en el otro buzón se leen una sola vez (los adjuntos viven en el correo original). El **estado nace del movimiento del correo** que traía el archivo:

| Movimiento del correo | Estado de la versión |
|---|---|
| Enviado | En revisión |
| Observado | Observada |
| Aprobado | Aprobada |
| Solicitud o Información | Referencia (no cuenta como entregable) |

Las versiones se ponen al día solas cada vez que se abre la pantalla: se crean las que faltan, se corrige el estado de las que nadie tocó a mano y se quitan las que dejaron de pertenecer al documento (solo si nadie les escribió un comentario ni cambió su estado). El administrador puede **corregir el estado a mano** (el sistema lo marca «(a mano)» y ofrece «Automático» para volver al del correo), poner una **etiqueta** corta (Rev. 1, Final…) y un **comentario**.

## Versión vigente y estado del documento

La **versión vigente** es la **última aprobada**; si no hay ninguna aprobada, la **última que no sea de referencia** (y se avisa «Aún sin aprobar»); si solo hay referencias, no hay vigente. El estado del documento sale de su vigente: Aprobado, En revisión u Observado, o **Falta** si no la hay. **Los archivos no se mueven ni se copian al aprobar:** «aprobados por área» es solo el filtro Estado = Aprobado dentro de esa área.

## Almacén de archivos (Cloudflare R2)

* Los archivos viven en un bucket privado de **Cloudflare R2**, no en Supabase. Las claves de R2 solo las usa el servidor; el navegador nunca las ve.
* **Abrir y descargar** no usan un enlace permanente: el servidor comprueba el permiso sobre el servicio y recién entonces redirige a un **enlace firmado de 5 minutos**. Abrir muestra el archivo en una pestaña nueva si el navegador puede (PDF, imágenes); si no, lo baja. Los adjuntos que ya estaban en el almacén anterior de Supabase se siguen sirviendo desde allí.
* **Claves estables:** `servicios/{número}/adjuntos/{id del adjunto}/{nombre}` para los de correo y `servicios/{número}/manuales/{id de la versión}/{nombre}` para los subidos a mano. No dependen del área ni del nombre del documento, para que cambiar un documento de área no deje la copia desubicada.
* **Copia de adjuntos desde Gmail:** el sistema solo guardaba el nombre, el tipo y el tamaño de cada adjunto; el archivo seguía en Gmail. «**Copiar adjuntos pendientes**» (botón del administrador, y un paso horario en el mismo disparador de la lectura de correos) vuelve a leer el mensaje en el buzón donde llegó —o en el de su copia—, empareja el adjunto por nombre y tamaño y lo sube a R2. Cada llamada avanza lo que alcanza en unos 50 segundos y avisa cuántos quedan. No se copian archivos de más de 30 MB; mientras un archivo no esté copiado se ve «Pendiente de copiar» y no se puede abrir.
* **Subida a mano (administrador):** botón **Subir** en la fila del documento; hasta 30 MB. El navegador sube el archivo directo a R2 con un enlace firmado de 15 minutos y el servidor confirma que llegó antes de mostrarlo. Si la subida falla, el registro se descarta. El administrador puede borrar los archivos que subió a mano (los que vienen de un correo no se borran desde aquí).

## Permisos

Provisorios, iguales a los de la Gestión documentaria para **ver**: el administrador, el jefe de proyecto, el jefe de oficina técnica y el supervisor de oficina técnica, dentro de los servicios a su alcance (ver, abrir, descargar). **Gestiona** —estado a mano, etiqueta, comentario, subir, borrar lo subido y copiar adjuntos— **solo el administrador**. Victor dejó para el final la regla «todos ven, solo el administrador edita»; al aplicarla se cambia aquí, en el flujo 14 y en la Matriz de permisos.

## Qué no es

No hay visor de PDF dentro de la app, firma electrónica, sincronización de carpetas en vivo ni edición de archivos. Los datos de los correos y los archivos nunca se guardan en el repositorio.

## Datos

Columna `estado_adjuntos.ruta_r2` (clave del archivo en R2; vacía = aún no copiado) y tabla `doc_versiones` (documento, adjunto de origen, nombre, tipo, tamaño, clave en R2 de las subidas a mano, etiqueta, estado, si el estado es a mano, comentario, origen `CORREO|MANUAL`, fecha del correo o de la subida) en [db/121](../../../py_control_proyectos_web/db/121_archivos_documentarios.sql). La «versión vigente» y el estado del documento no se guardan: se calculan. Variables de entorno del servidor: `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` y `R2_BUCKET`; el bucket necesita una política **CORS** que permita `GET`, `HEAD` y `PUT` desde el dominio de la app (la subida a mano no funciona sin ella; el 2026-10-25 Victor dijo que no quiere subir archivos desde la app, así que el CORS no se configura por ahora).
