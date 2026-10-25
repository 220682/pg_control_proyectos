# 24 — Gestión documentaria
> Lee si: la tarea toca el apartado «Gestión documentaria» (un documento por fila con su estado Solicitado/Enviado/Observado/Levantado/Aprobado, a quién le toca moverlo, el semáforo de días esperando, las cinco áreas, «Por asignar», la carga inicial desde los correos) o el botón «Abrir en Gmail» del correo completo.

Origen: plan [Gestión documentaria](../02-trabajo-activo/01-planes/2026-10-25-gestion-documentaria.md) (pedido de Victor el 2026-10-25; Spec y Gate 1 aprobados por él). Es la **segunda de tres interfaces**: 1 [Gestión de interesados](23-estado-del-servicio.md) (de dónde salen los correos), 2 esta, 3 [Archivos documentarios](25-archivos-documentarios.md) (el árbol de archivos de cada documento). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md); la lista de pantallas, en el [flujo 16](16-paneles.md).

## Qué es

Una pantalla por servicio (`/proyectos/{id}/gestion-documentaria`, chip «Gestión documentaria» en el grupo Planificación) que responde **qué documentos están en juego, en qué estado, a quién le toca moverlos y cuántos días llevan esperando**. No guarda los archivos (eso es la [tercera interfaz](25-archivos-documentarios.md)): lleva el **estado** del documento a partir de los correos que ya lee la Gestión de interesados.

## Un documento = una fila

Cada documento tiene: **nombre**, **tipo** (plano, ficha técnica, procedimiento/PETS, informe, trámite, valorización, otros), **área**, **revisión** (opcional), una **nota** corta de qué trata y los **correos** que le pertenecen. Los correos son las notas de la Gestión de interesados (`estado_notas.documento_id`); un documento puede tener varios y una nota pertenece como máximo a uno. Borrar un documento **no borra sus correos**: vuelven a «Por asignar».

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

Los días se cuentan desde el último correo que movió el estado. **Rojo** al llegar al plazo, **ámbar** desde la mitad del plazo (redondeada hacia arriba), **verde** antes. Un documento **Aprobado no tiene semáforo**. El plazo se elige en un desplegable (3, 5, 7, 10, 15 o 30 días; **7 por defecto**) y se recuerda en el navegador de cada persona.

## Áreas

**SSOMA** (incluye Medio Ambiente), **Oficina Técnica**, **Calidad**, **Administración** (accesos y otros) y **Gerencia** (contratos y compras, por ahora); se afinan después. El área la decide **quien envía**, igual en contratista y cliente:

1. Si el administrador ya corrigió esa dirección o ese nombre, vale lo aprendido.
2. Si no, las palabras de la dirección o del nombre («seguridad», «calidad», «ingeniería», «contratos»…).
3. Si nada coincide, **Sin área**.

Cuando el administrador corrige el área de un documento, el sistema **aprende la dirección** de quien abrió ese documento y la usa en los siguientes. La contratista usa un correo por área.

## La pantalla

* **Tarjetas por área** con cuatro conteos: *Por emitir* (nos toca), *Esperando al cliente*, *Observados*, *Aprobados*. Al tocar una tarjeta o un conteo se filtra la lista.
* **Filtros:** área (y «Sin área»), tipo, estado, a quién le toca, remitente, rango de fechas del último movimiento, «solo pendientes», «esperando más de X días» y el plazo del semáforo.
* **Ficha compacta de dos líneas** por documento: tipo, nombre y revisión, chips de área, estado y semáforo (con los días); debajo, remitente, asunto, fecha del último correo y «a quién le toca». La **nota** de qué trata va debajo. Un desplegable muestra el **historial** de correos (con adjuntos), cada uno con su botón «Correo» (panel lateral con el correo completo y sus adjuntos).
* **Por asignar:** los correos de movimiento (no los informativos) que aún no pertenecen a ningún documento. Se marcan varios y se crea con ellos un documento nuevo (el nombre se propone desde el asunto sin «RE:»/«RV:») o se suman a uno existente. Un correo se puede sacar de un documento y vuelve a esta lista.
* **Exportar a Excel:** descarga lo que se ve (con los filtros) en un archivo CSV separado por «;» con codificación UTF-8 con BOM, que Excel en español abre directo.
* El administrador (y quien gestione) puede **crear, editar y borrar** documentos y asignar correos. El resto solo ve.

## Carga inicial y correos nuevos

La primera vez, los correos ya leídos de los cuatro servicios se agrupan por **hilo** (o por asunto sin «RE:») y se crea un documento por grupo, con origen «CARGA»; se excluyen los temas «Reportes diarios» y «Reuniones y minutas» y los grupos que solo tienen notas informativas. Los correos nuevos que llegan después caen en **Por asignar** hasta que alguien los agrupe; la creación automática de documentos para correos nuevos queda como mejora posterior. Los datos de los correos nunca se guardan en el repositorio.

## «Abrir en Gmail»

En el correo completo (de cualquiera de las dos interfaces) hay un botón secundario **Abrir en Gmail**: abre el mensaje en Gmail del buzón donde llegó (si llegó a los dos buzones, un botón por buzón). Hay que tener esa cuenta abierta en el navegador; si no, Gmail pide elegirla.

## Permisos

Provisorios, iguales a los de la Gestión de interesados: **ven** el administrador, el jefe de proyecto, el jefe de oficina técnica y el supervisor de oficina técnica; **gestionan** el administrador y el jefe de proyecto. Victor dejó para el final la regla «todos ven, solo el administrador crea, edita y elimina»; al aplicarla se cambia aquí, en el flujo 23 y en la Matriz de permisos.

## Datos

Tablas `doc_documentos` (documento: servicio, área, tipo, nombre, revisión, nota, estado forzado, origen `MANUAL|CARGA|IA`, quién lo creó) y `doc_remitentes_area` (dirección o nombre → área aprendida), y la columna `estado_notas.documento_id` ([db/120](../../../py_control_proyectos_web/db/120_gestion_documentaria.sql) en la app). Todo se lee y escribe desde el servidor; ninguna tabla es legible directo desde el navegador.
