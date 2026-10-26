# 24 — Gestión de Email (antes «Gestión documentaria»)
> Lee si: la tarea toca el apartado «Gestión de Email» (un documento por fila con su estado Solicitado/Enviado/Observado/Levantado/Aprobado, la vida del documento en casillas o en vista compacta, el correo en el panel de la derecha, a quién le toca moverlo, el semáforo de días esperando, las cinco áreas, «Otros correos»/«Sin ubicar», «Por asignar», la carga inicial desde los correos) o el botón «Abrir en Gmail» del correo completo.

Origen: plan [Gestión documentaria](../02-trabajo-activo/01-planes/2026-10-25-gestion-documentaria.md) (pedido de Victor el 2026-10-25; Spec y Gate 1 aprobados por él). Es la **segunda de tres interfaces**: 1 [Gestión de interesados](23-estado-del-servicio.md) (de dónde salen los correos), 2 esta, 3 [Archivos documentarios](25-archivos-documentarios.md) (el árbol de archivos de cada documento). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md); la lista de pantallas, en el [flujo 16](16-paneles.md).

## Qué es

Una pantalla por servicio (`/proyectos/{id}/gestion-emails`, chip «Gestión de Email» en el grupo Planificación) que responde **qué documentos están en juego, en qué estado, a quién le toca moverlos y cuántos días llevan esperando**. No guarda los archivos (eso es la [tercera interfaz](25-archivos-documentarios.md)): lleva el **estado** del documento a partir de los correos que ya lee la Fuente-Gmail.

## Un documento = una fila

Cada documento tiene: **nombre**, **tipo** (plano, ficha técnica, procedimiento/PETS, informe, trámite, valorización, otros), **área**, **revisión** (opcional), una **nota** corta de qué trata y los **correos** que le pertenecen. Los correos son las notas de la Fuente-Gmail (`estado_notas.documento_id`); un documento puede tener varios y una nota pertenece como máximo a uno. Borrar un documento **no borra sus correos**: vuelven a «Por asignar».

**Un documento agrupa por tema, no por nombre de archivo** (Victor, 2026-10-26). Todo lo que trate de lo mismo va en **un solo documento**, aunque cada correo nombre un archivo distinto: todos los planos (cerco perimétrico, pérgola, distribución, envíos para revisión) en «Planos»; todos los cronogramas (ejecución, histograma, valorizado) en «Cronograma»; el contrato, la adjudicación, las reuniones de contrato y las garantías en «Contrato y adjudicación»; los trámites de movilización, migración y acceso de personal y vehículos en uno. Un documento con su propio ciclo de revisión (por ejemplo el Plan de Ejecución o el Plan de habitabilidad) se mantiene aparte. **Un mismo tema no puede quedar en dos áreas:** el área del documento agrupado manda (cronogramas y planos son de Oficina Técnica; contrato y compras, de Gerencia; accesos y movilización, de Administración). Los correos de un reporte periódico (diario o semanal) y las reuniones no son documentos: van a sus temas («Reportes diarios», «Reuniones y minutas»).

### Las familias de documentos (igual en todos los servicios)

La lista siguiente es la misma para los cuatro servicios y para los que vengan (Victor, 2026-10-26). Cada familia es **un solo documento por servicio**, con su nombre, su área y su tipo fijos. La app la guarda en `src/lib/gestion-emails/familias.ts`; **para sumar o cambiar una familia se avisa a Victor y se actualiza el código y esta tabla a la vez**.

| Familia (nombre del documento) | Área | Qué entra |
|---|---|---|
| Planos | Oficina Técnica | envíos para revisión, ubicación del campamento, cerco, pérgola, distribución, planos nativos |
| Cronograma | Oficina Técnica | cronograma de ejecución, histograma, valorizado, Last Planner |
| Lista de contactos y coordinación | Oficina Técnica | listas y directorios de contactos, matriz de comunicaciones, contacto con la supervisión |
| Plan y dossier de calidad | Oficina Técnica | plan de calidad, índice del dossier, protocolos, certificados de calidad y fichas de pintura |
| Plan de trabajo y memoria descriptiva | Oficina Técnica | plan de trabajo, memoria descriptiva, vía alterna, comentarios legales |
| Fichas técnicas | Oficina Técnica | fichas técnicas de materiales y equipos |
| Visita técnica | Oficina Técnica | solicitud, confirmación y ejecución de la visita |
| Informes técnicos e inspecciones | Oficina Técnica | informes técnicos, inspección de contenedores |
| Entregables y codificación de documentos | Oficina Técnica | lista de entregables, procedimiento de codificación (Aconex) |
| Contrato y adjudicación | Gerencia | adjudicación, contrato, reuniones de contrato, carta fianza, pólizas |
| Cotizaciones y pagos | Gerencia | cotizaciones, propuestas económicas, adelantos, pagos, baños, buzones |
| Documentación SSO | SSOMA | paquete SSO (todas sus partes), manual de gestión, seguridad de excavaciones, operatividad de equipos, AITAE |
| Solicitud de ingreso FOCAM | SSOMA | solicitud, observaciones y aprobación del FOCAM |
| Movilización, migración y acceso de personal y vehículos | Administración | código de contrato en 2PERSONNEL, migración y activación, formatos de movilización, permisos de ingreso, habilitación de personal, cuadrillas, CV del personal clave |
| Combustible | Administración | habilitación de combustible y reportes de consumo |

**Documentos con ciclo propio** (siguen aparte): el Plan de Ejecución y el Plan de movilización y habitabilidad. **Un tema que aparece una sola vez** (por ejemplo la verificación VAPE) queda como documento propio; solo pasa a ser familia cuando se repite y Victor lo aprueba.

## Cómo se calcula el estado

De los correos del documento, de la nota más antigua a la más nueva (una nota «Información» no mueve el estado):

| Llega… | El documento queda… |
|---|---|
| Solicitud | **Solicitado** (también si ya estaba aprobado: es un pedido nuevo) |
| Enviado | **Enviado**; si estaba Observado, **Levantado** |
| Observado | **Observado** |
| Aprobado | **Aprobado** |

El administrador puede **corregir el estado a mano** («Automático» lo devuelve al cálculo); se muestra «(a mano)».

**A quién le toca:** es la parte contraria de quien escribió el último correo que movió el estado. El dominio `promcoser.com.pe` es «nosotros»; cualquier otro remitente es el cliente. Si el estado fue forzado a mano, le toca: Solicitado → nosotros, Enviado → cliente, Observado → nosotros, Levantado → cliente. Aprobado: a nadie.

## Semáforo de días esperando

Los días se cuentan desde el último correo que movió el estado. **Rojo** al llegar al plazo, **ámbar** desde la mitad del plazo (redondeada hacia arriba), **verde** antes. Un documento **Aprobado no tiene semáforo**. El plazo es de **7 días**; desde el rediseño del 2026-10-25 la pantalla ya no ofrece el desplegable para cambiarlo y el semáforo se ve como el color del «hace N días» del último movimiento en la vista compacta.

## Áreas

**SSOMA** (incluye Medio Ambiente), **Oficina Técnica**, **Calidad**, **Administración** (accesos y otros) y **Gerencia** (contratos y compras, por ahora); se afinan después. El área la decide **quien envía**, igual en contratista y cliente:

1. Si el administrador ya corrigió esa dirección o ese nombre, vale lo aprendido.
2. Si no, las palabras de la dirección o del nombre («seguridad», «calidad», «ingeniería», «contratos»…).
3. Si nada coincide, **Sin área**.

Cuando el administrador corrige el área de un documento, el sistema **aprende la dirección** de quien abrió ese documento y la usa en los siguientes. La contratista usa un correo por área.

## La pantalla

Rediseñada el 2026-10-25 a pedido de Victor (maqueta aprobada por él). Es un **cuadro con una fila por documento** —no por correo— y el correo se lee en un **panel fijo a la derecha**. Como en las demás pantallas de la app, **solo se desliza el panel central**; el panel del correo no se mueve.

* **Aviso de cobertura (banner verde):** «**Ningún correo queda fuera.** N correos del servicio: A en documentos · B en temas · C sin ubicar», con la leyenda de colores de las casillas. Cuenta los correos originales del servicio (una copia en el otro buzón no se cuenta dos veces) y siempre suma el total.
* **Una sola tabla, con tres grupos** (ajuste del 2026-10-26, pedido de Victor: ocupar poco espacio): **Documentos** (por área), **Otros correos del servicio** (una fila por tema) y **Sin ubicar** (una fila con todo lo que no encajó). Las dos vistas la muestran completa, con un interruptor (por defecto la **compacta**):
  * **Compacta:** área, documento, quién lo pide, fecha del pedido, último movimiento (con los días esperando en el color del semáforo), correos (total y cuántos con archivo) y estado. La columna «Correos» dice «N correos · M con archivo». La flecha de la fila despliega sus casillas, de la más antigua a la más nueva; al buscar se despliegan todas.
  * **En casillas:** a la derecha de área, documento y estado (que quedan fijos al deslizar) van las casillas en orden, de izquierda a derecha, sin huecos. Los documentos sin aprobar terminan con una casilla punteada que dice quién tiene la pelota («Esperando respuesta del cliente hace N días» o «Nos toca moverlo hace N días», en rojo si el semáforo está en rojo). Ya no hay columnas fijas por etapa ni tablas separadas según quién pide.
* **Quién lo pide:** lo pedimos nosotros si la primera solicitud del documento salió de la contratista (`promcoser.com.pe`); en cualquier otro caso (incluido un documento sin solicitud) lo pide el cliente.
* **La casilla** (176 × 84 px, como en la maqueta) tiene tres líneas: el movimiento (Pedido, Enviado, Observado, Aprobado, Entregado, Informativo); «fecha · quién escribió» (Cliente o Contratista) y, abajo, un clip con «con archivo» o «Sin archivo» si es solo mensaje. La fecha va en corto («02 oct»). Al pasar el mouse (o al enfocarla con el teclado) sale, sobre la tabla y sin recortarse con el scroll, un cuadro con el asunto en negrita, la **nota** del correo y «Clic para abrir el correo». Al tocarla se abre el **correo completo en el panel de la derecha** (CORREO, asunto, chip y «Documento: X» o «Tema: X», De/Para/Fecha), con la caja «Nota para revisión rápida» arriba y el cuerpo. **La cabecera del panel es fija** (no se desliza con el correo) y trae tres botones: «Abrir en Gmail», «Descargar archivo» —si el correo trae varios, un desplegable «Descargar archivos (N)» con el nombre y tamaño de cada uno— y la X para cerrar. Escape también lo cierra. En pantallas angostas el panel ocupa toda la pantalla.
* **Otros correos del servicio, por tema** y **Sin ubicar:** son grupos de la misma tabla (ver arriba): los correos que no pertenecen a un documento y sí a un tema de la Fuente-Gmail (reportes diarios, reuniones y minutas, restricciones, reenvíos…), incluidos los informativos y las notas escritas a mano, y al final los correos sin nota ni tema, para que ninguno quede fuera. No se crean «comentarios» aparte.
* **Encabezado como en la maqueta:** a la izquierda migas, título y descripción; a la derecha el interruptor «Vista compacta / Vista en casillas» y «Buscar». Debajo, el aviso de cobertura y una fila con las pestañas Documentos/Por asignar, los filtros, Nuevo documento y Excel. El panel del correo mide 400 px. **Filtros (pocos):** buscador (nombre del documento, asunto, remitente o nota; sin tildes ni mayúsculas; al buscar se despliegan todas las filas), **quién lo pide** (cliente / nosotros), **área** (y «Sin área») y **estado**. Con área, estado o quién lo pide activos se ocultan los correos sueltos, porque esos filtros hablan de documentos.
* **Por asignar:** pestaña aparte con los correos de movimiento (no los informativos) que aún no pertenecen a ningún documento. Se marcan varios y se crea con ellos un documento nuevo (el nombre se propone desde el asunto sin «RE:»/«RV:») o se suman a uno existente. Un correo se puede sacar de un documento con **Quitar del documento** (en el panel del correo) y vuelve a esta lista.
* **Exportar a Excel:** descarga lo que se ve (con los filtros) en un archivo CSV separado por «;» con codificación UTF-8 con BOM, que Excel en español abre directo.
* El administrador (y quien gestione) puede **crear, editar y borrar** documentos (lápiz y papelera en la fila) y asignar correos. El resto solo ve.
* **Ya no están** (quitados en el rediseño): las tarjetas por área con sus cuatro conteos, el filtro por tipo, a quién le toca, remitente, rango de fechas, «solo pendientes» y «esperando más de X días», y el desplegable del plazo del semáforo.

## Carga inicial y correos nuevos

La primera vez, los correos ya leídos de los cuatro servicios se agrupan por **hilo** (o por asunto sin «RE:») y se crea un documento por grupo, con origen «CARGA»; se excluyen los temas «Reportes diarios» y «Reuniones y minutas» y los grupos que solo tienen notas informativas. **Los correos nuevos se asignan solos** (2026-10-26): al clasificar un correo, el sistema lo sigue hasta su documento así: (1) si otro correo del **mismo hilo** ya está en un documento, va al mismo; (2) si no, y el correo mueve el estado (pedido, envío, observación o aprobación), busca su **familia** por el asunto con la lista de arriba y usa el documento de esa familia en el servicio, **creándolo si no existe** (origen «IA»); (3) si no encaja en ninguna familia, queda en **Por asignar** (o en Otros correos / Sin ubicar si es informativo) hasta que alguien lo agrupe. Los reportes diarios y las reuniones nunca se asignan. Si algo falla, el correo queda en Por asignar y no se pierde. La asignación automática no cambia lo que ya ubicó una persona.

**Reagrupar lo ya cargado:** el script `scripts/revision/reagrupar-familias.mjs` de la app aplica la misma lista a los documentos existentes de todos los servicios: funde los documentos de una familia en uno (conserva todos sus correos), pasa los correos sueltos a su documento y deja el resto como estaba. Primero simula y guarda un respaldo; solo escribe con `--aplicar`. Los datos de los correos nunca se guardan en el repositorio.

## «Abrir en Gmail»

En el correo completo (de cualquiera de las dos interfaces) hay un botón secundario **Abrir en Gmail**: abre el mensaje en Gmail del buzón donde llegó (si llegó a los dos buzones, un botón por buzón). Hay que tener esa cuenta abierta en el navegador; si no, Gmail pide elegirla.

## Permisos

Provisorios, iguales a los de la Fuente-Gmail: **ven** el administrador, el jefe de proyecto, el jefe de oficina técnica y el supervisor de oficina técnica; **gestionan** el administrador y el jefe de proyecto. Victor dejó para el final la regla «todos ven, solo el administrador crea, edita y elimina»; al aplicarla se cambia aquí, en el flujo 23 y en la Matriz de permisos.

## Datos

Tablas `doc_documentos` (documento: servicio, área, tipo, nombre, revisión, nota, estado forzado, origen `MANUAL|CARGA|IA`, quién lo creó) y `doc_remitentes_area` (dirección o nombre → área aprendida), y la columna `estado_notas.documento_id` ([db/120](../../../py_control_proyectos_web/db/120_gestion_documentaria.sql) en la app). Todo se lee y escribe desde el servidor; ninguna tabla es legible directo desde el navegador.
