# Plan — Repositorio de archivos documentarios (tercera interfaz)

## Identificación y estado

- Tema: apartado «Archivos documentarios» en `py_control_proyectos_web`: los documentos en su versión aprobada (o la que se elija), ordenados como un árbol de carpetas, con estado, comentario, apertura y descarga.
- Fecha: 2026-10-25.
- Estado: `Implementando` (código construido y comiteado en la app, `f23ddad`; falta que Victor aplique `db/121`, cargue las variables de R2 en Vercel y configure el CORS del bucket, y recién entonces se empuja y se verifica en producción).
- Gate Spec: aprobado por Victor el 2026-10-25 al decir «sigue con el plan de archivos documentarios».
- Gate 1: aprobado en el mismo mensaje (Victor pidió que el Orquestador construya y que él revise al final, sin auditoría).
- Gate 2: pendiente.

## Las tres interfaces y cómo se relacionan

| # | Interfaz | Para qué sirve | Plan |
|---|---|---|---|
| 1 | **Gestión de interesados** | Extrae los correos y los agrupa por tema, para leerlos todos si hace falta | Hecha (flujo 23) |
| 2 | **Gestión documentaria** | Seguimiento: cada documento con área, estado, a quién le toca, semáforo de días y nota | `2026-10-25-gestion-documentaria.md` (Gate 1 pendiente) |
| 3 | **Archivos documentarios** | Los archivos mismos, en jerarquía de carpetas, para elegir qué versión ver, abrirla y descargarla | **Este plan** |

La 2 depende de la 1 (usa sus notas) y la 3 depende de la 2 (cada archivo pertenece a un documento y a una versión).

## Referencia al Spec

Pedido de Victor (2026-10-25), en sus palabras: desde la app llegar a los archivos que se guardan en Cloudflare; un documento puede tener **varias versiones hasta llegar a la aprobada**, y quiere **saltarse la revisión de todas y ver solo la aprobada**; saber si en Cloudflare se puede tener una carpeta de documentos aprobados **por áreas**; y verlos **en la app en forma de jerarquía**, como en la maqueta `D:\VICTOR\CLAUDE CODE\maqueta_dossier` (que hoy se conecta a su disco local y muestra toda la jerarquía de carpetas y archivos). Desde esa pantalla quiere el **redireccionamiento a Cloudflare** para revisar el archivo, sea en revisión o aprobado, **viendo su estado para elegir cuál abrir**; poder **colocar un comentario**, ver el estado, **abrir el archivo y descargarlo**; **filtros** para ver solo un área, solo aprobados, etc. Además pidió, en el plan 2, un enlace desde la app al **correo** de origen.

## Respuestas de diseño a sus preguntas

- **¿Cómo llegar a los archivos de Cloudflare desde la app?** La app genera, al pulsar «Abrir» o «Descargar», un enlace **temporal** (vale unos minutos) a ese archivo. Los archivos no son públicos y no hay que entrar al panel de Cloudflare.
- **¿Carpeta de aprobados por áreas en Cloudflare?** Cloudflare R2 no tiene carpetas reales, tiene rutas de nombre (por ejemplo `servicios/PS-0003/SSOMA/ficha-tecnica/…`), y se pueden ordenar así. **Propuesta:** no mover ni copiar archivos al aprobar. El estado de cada versión vive en la base de datos y «aprobados por área» es una **vista filtrada**, no una segunda copia. Así no se duplica nada y no se pierde el historial de versiones.
- **¿Cómo me salto las versiones intermedias?** Cada documento muestra por defecto su **versión aprobada vigente**; las demás quedan plegadas en «Ver versiones», cada una con su estado (en revisión, observada, aprobada, reemplazada). Si aún no hay aprobada, se muestra la última y se dice «sin aprobar».
- **¿Redirigir al correo?** Se agrega, en el panel del correo, un botón secundario **«Abrir en Gmail»** que lleva al mensaje en el buzón correcto (hay dos buzones). Funciona solo si esa persona tiene ese Gmail abierto en su navegador. Se mantiene el panel actual como lectura principal, porque no depende de iniciar sesión en Gmail.

## Diseño propuesto

**Pantalla** (inspirada en la maqueta): árbol **Servicio → Área → Tipo de documento → Documento**, con:
- Contador de archivos por carpeta y marca de «nuevo» en lo agregado recientemente.
- Columnas **Estado** y **Comentario** por documento (el comentario lo escribe el administrador; el estado sale de la versión aprobada y se puede corregir a mano).
- Botones **Expandir todo / Colapsar todo**, casilla **Solo carpetas**, y filtro por texto en el nombre.
- Carpeta o documento sin archivo aprobado: aparece una fila «**falta**» para ver de un vistazo qué no está.
- Por documento: **Abrir** (en una pestaña nueva), **Descargar**, **Ver versiones**, enlace a su ficha en Gestión documentaria y al correo de origen.

**Filtros:** servicio, área, estado (aprobado, en revisión, observado, sin aprobar), tipo, texto y «solo faltantes».

**Datos:**
- El archivo vive en R2 con su ruta; la base guarda, por cada versión: documento, número de revisión, archivo (los adjuntos de los correos ya existen en `estado_adjuntos`), estado, comentario y fecha de aprobación.
- Los archivos que hoy están en el disco de Victor (por ejemplo el dossier de calidad) se pueden **subir a mano** a un documento desde la misma pantalla (administrador).
- Requiere que los adjuntos de los correos pasen primero a R2 (el bucket y el token ya existen; la copia se hace desde esta misma pantalla, ver «Refinamientos»).

**Costos:** R2 tiene capa gratuita de 10 GB y descargas sin cargo; lo que hay hoy (unos 200 MB) cabe de sobra.

**Permisos (provisorio):** ver = administrador, jefe de proyectos, jefe de oficina técnica y supervisor de oficina técnica; gestionar (comentar, subir, corregir estado) = administrador. Se ajusta con la decisión final de «todos ven, solo el administrador edita».

## Alcance y no alcance

- **Alcance:** migración de versiones; subida de adjuntos de correos a R2; rutas para abrir, descargar y subir con enlaces temporales; pantalla de árbol con estado, comentario, versiones y filtros; chip en Planificación; flujo nuevo, actualización de flujos 14 y 16 y de la Matriz de permisos.
- **No alcance:** visor de PDF dentro de la app (se abre en pestaña nueva); firma electrónica; sincronizar carpetas del disco en vivo; edición de archivos.
- **Validación esperada:** pruebas de las reglas puras (cuál es la versión vigente, estados), `tsc` y `eslint`; verificación con Playwright de abrir, descargar y filtros; comprobación de que un enlace caducado deja de funcionar y de que un rol sin permiso no obtiene enlace.

## Riesgos

- Los enlaces temporales deben generarse solo en el servidor tras comprobar el permiso del usuario; nunca exponer las claves de R2 al navegador.
- Subir 200 MB de adjuntos exige releer cada mensaje en Gmail y emparejar nombre y tamaño; se hace por lotes con reintentos.
- Los nombres de archivo de los correos son desordenados (por ejemplo `image001.png`); las imágenes de firma no deben llenar el árbol, así que se filtran por tipo y tamaño.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-25 | Son tres interfaces: correos agrupados, seguimiento documentario y archivos en jerarquía; esta última es un plan aparte y es lo siguiente después de Gestión documentaria | Victor |
| 2026-10-25 | La jerarquía se parece a la maqueta del dossier, con estado y comentario por archivo, abrir y descargar desde Cloudflare, y filtros por área y estado | Victor |
| 2026-10-25 | Propuesta del Orquestador (por aprobar): no mover archivos al aprobar; «aprobados por área» es una vista filtrada y la versión aprobada se muestra por defecto | Orquestador |
| 2026-10-25 | «Sigue con el plan de archivos documentarios»: se toma como aprobación del Spec y del Gate 1, incluida la propuesta de arriba | Victor |
| 2026-10-25 | Solo se convierten en versión los adjuntos que no son imágenes, calendarios ni correos reenviados; el mismo nombre y tamaño repetido en el hilo queda una sola vez (el más antiguo); no se copian archivos de más de 30 MB | Orquestador |

## Refinamientos hechos al construir

- **Claves de R2 sin el área:** el Spec ponía el área en la ruta (`servicios/PS-0003/SSOMA/…`), pero cambiar un documento de área dejaría la copia desubicada. La clave es `servicios/{número}/adjuntos/{id del adjunto}/{nombre}` (`…/manuales/{id de la versión}/{nombre}` para lo subido a mano); el área y el tipo salen de la base. Detalle en el [flujo 25](../../04-flujos-de-negocio/25-archivos-documentarios.md).
- **Copia de adjuntos desde la propia pantalla:** `POST /api/archivos-documentarios/copiar` (botón «Copiar adjuntos pendientes» del administrador y un paso horario en el workflow de la lectura de correos) relee el mensaje en Gmail, empareja por nombre y tamaño y sube a R2; cada llamada avanza unos 48 s. En la base había 2404 adjuntos registrados y solo 380 con archivo en Supabase (133 MB): el resto solo estaba en Gmail.
- **CORS del bucket:** el token de R2 que creó Victor solo da lectura y escritura de objetos y no permite cambiar la política CORS del bucket (R2 responde `AccessDenied`); sin CORS el navegador no puede subir a mano. Victor debe configurarla en el panel de Cloudflare (bucket → Configuración → Política de CORS).
- **Estado de versión desde el correo:** Enviado → En revisión, Observado → Observada, Aprobado → Aprobada, Solicitud o Información → Referencia (no cuenta como entregable); el administrador puede corregirlo a mano y volver a «Automático».

## Libro de hallazgos

Mejoras de trabajo, reglas de negocio, observaciones sobre la política y huérfanos: **Ninguno** por ahora.

## Elementos postergados propuestos

- Esquema configurable de tomos (como el dossier de calidad) y descarga en lote (zip) por área.
- Alertas cuando falte una versión aprobada a una fecha.
