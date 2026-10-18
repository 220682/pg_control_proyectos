# Limpieza de datos de prueba del plan Notificaciones — notas para Victor

Preparado el 2026-10-18 por el Worker de datos. Nada se borró ni se escribió en producción: solo se leyó por GET con la sesión del administrador. El script lo revisa y lo aplica Victor en el editor SQL de Supabase (pegar `limpieza-datos-prueba.sql` entero).

Archivos de esta carpeta: `respaldo-antes-de-limpiar.json` (lo que se va a borrar, leído por GET), `limpieza-datos-prueba.sql` y este archivo.

## Ids usados

| Qué | Nombre | Id |
|---|---|---|
| Servicio de prueba (se borra) | PS-0005 «PRUEBA T7» (cliente «PRUEBA», OC/OS `PRUEBA-T7`) | `e15799ae-d964-4db7-b33f-39dc9c1a3860` |
| Servicio de pruebas existente (NO se borra) | PS-0000 «SERVICIO PRUEBA MARCOBRE 2026-10-07-19-33» | `0a20df2f-c5e9-4296-9c08-f89af499182d` |
| RQ SO-001 / SO-002 / SO-003 | `PS-0000-LL-SO-001`, `-002`, `-003` | `9fff5fc7-7118-4ccc-aafe-5da8fe5ba826`, `f5733231-0830-41e8-8ff2-1a930d29813e`, `2cbd3bf7-78cc-480b-9877-d6fa98d49e9b` |
| RDT rechazado 14-10 (se borra) | jeyger22, especialidad PRUEBA, T7B | `dcf5e7b8-0468-452b-8628-ac2b96a3b356` |
| RDT validado 17-10 (opcional, aparte) | jeyger22, especialidad PRUEBA, T7B | `99f82005-60f0-4fc2-8697-fc939bf13e6e` |
| Autor de los dos RDT / responsable de PS-0005 | López Cáceres Loayza (jeyger22) | `c414ba1c-81e2-47e1-a9a1-e71823c3a78c` |
| Cuenta PRUEBA Logística 1 (se conserva) | — | `4aced21b-466c-492f-b872-83ddf0f40d36` |

## Qué borra el script (y cuántas filas)

| Tabla | Filas | Cómo |
|---|---|---|
| `notificaciones` (30 que ve el administrador) | 30 | por id exacto (paso 2.1) |
| `notificaciones` (de otras personas, por referencia o código exacto) | entre 7 y 20, no contables de antemano | paso 2.2: `referencia_id` = id de uno de los 3 RQ o de los 2 RDT, o el mensaje contiene el código exacto `PS-0000-LL-SO-00x`; solo de PS-0000 y con guarda de fecha (aborta si alguna es anterior al 17-10) |
| `notificaciones` (Entorno «PRUEBA T7…» de otras personas) | 0 conocidas | paso 2.3 |
| `proyecto_requerimientos` | 3 | por id (paso 3) |
| `requerimiento_lineas` | 4 (cascada) | SO-003: 2 ítems; SO-002: 1; SO-001: 1 |
| `requerimiento_comentarios` | 5 (cascada) | SO-003: 4; SO-001: 1; SO-002: 0 |
| Adjuntos de los ítems | 0 | ningún ítem tiene archivos |
| `rdt_partes_historial` | 1 | la foto de la acción RECHAZAR del RDT 14-10 |
| `rdt_partes` | 1 | el RDT rechazado 14-10 |
| `rdt_actividades`, `rdt_tareo`, `rdt_tareo_horas` | 1 + 1 + 1 (cascada) | del RDT 14-10; también cae su vínculo a partida si existe |
| `proyectos` | 1 | PS-0005 |
| `proyecto_documentos` | 2 (cascada) | «Requerimientos del servicio» y «PRUEBA T7 plano de campo» |
| `proyecto_miembros` y otras hijas de `proyecto_id` | las que haya (cascada) | jeyger a cargo; Logística 1 y 2 ya estaban retiradas |
| `notificaciones` de PS-0005 | 6 visibles + las ocultas (cascada) | las 6 visibles: asignado/retirado de jeyger y Logística 1 |

Las guardas del inicio abortan todo si el id no corresponde (por ejemplo, si PS-0005 no se llama «PRUEBA T7» con cliente «PRUEBA», si los RQ no coinciden por id y código, si el RDT no es el rechazado del 14-10 de jeyger, o si PS-0005 tiene RDT, cronograma, etc.). Al final una comprobación dentro de la transacción revierte todo si queda algo de lo borrado, y después del `commit` un `select` muestra antes y después por concepto.

## Qué NO borra

- PS-0000 (ni se archiva) y sus 35 RDT restantes: los 33 anteriores al plan, más el RDT del 18-10 (`c0c665e0…`, cargado por Victor, 40 HH, paquete PT 3.3, estado REGISTRADO; no es de las pruebas), más el validado del 17-10 que queda en la sección opcional.
- Las cuentas PRUEBA Logística 1 y 2 y sus membresías a PS-0000.
- Avisos que no son de estas pruebas: los `informe.emitido` PS-0000-ID-1, -2 y -4 (17-10, de otro plan), los mensajes de Victor «hola que tal» (PS-0000) y «hola» (PS-0002), los avisos «falta subir» de PS-0001 a PS-0004 (15-10), los del checklist de PS-0000 del 07-10 y los reales de Victor.
- Archivos en Storage (ver abajo).

## Riesgo de cada parte

| Parte | Riesgo | Nota |
|---|---|---|
| Servicio PS-0005 | Bajo | Mismo borrado en cascada que el botón «Eliminar proyecto». Efecto útil: el siguiente servicio real vuelve a salir como PS-0005 (T7B-H7 y H2: el servidor calcula el N° OT con los servicios existentes). Verificarlo después con una consulta GET al correlativo (`/api/proyectos/siguiente-ot`) |
| RQ SO-001/002/003 | Bajo | Todos son de prueba (ítems «PRUEBA T7…», «PRUEBA T1B…»). Al borrarlos, el correlativo de RQ de PS-0000 vuelve a SO-001 |
| RDT rechazado 14-10 | Bajo | Un RDT RECHAZADO no entra al PR ni al dashboard (el motor solo suma `VALIDADO`) |
| Avisos por id exacto | Bajo | 30 ids leídos del GET |
| Avisos de otras personas (2.2 y 2.3) | Medio-bajo | No se pudieron listar: el administrador no puede ver los avisos de otros (filas de la cola del rol Jefe de Proyectos, avisos al solicitante, a Logística). Se borran solo por referencia a los 3 RQ y 2 RDT o por el código exacto, de PS-0000 y desde el 17-10; la guarda aborta si algo no encaja. Para verlos antes: ejecutar la consulta de vista previa que está comentada en el paso 1 y exportar a CSV desde el editor |
| RDT VALIDADO del 17-10 (sección opcional, comentada) | **Medio** | Ver abajo |

## RDT validado del 17-10: qué pasa si se borra

Es un RDT VALIDADO de PS-0000 (turno día, especialidad «PRUEBA», 1 actividad en el WBS 1.1.4 «PRUEBA T7 actividad», metrado ejecutado 0, 8 HH de un AYUDANTE TOPÓGRAFO del personal real). Validado por el administrador el 18-10.

- **Acumulado, PR y dashboard sí cambian.** `recalcular_pr_desde_rdt` reinicia el PR del proyecto y lo reconstruye sumando todos los RDT VALIDADO; este aporta 8 HH reales a la partida 1.1.4 y su costo real (8 HH × la tarifa del cargo, más el factor de horas extra si hubiera). La curva S y el dashboard salen de esos mismos datos.
- **El avance físico no cambia** (metrado ejecutado 0), así que el EV y el % de avance no se mueven; baja el AC/HH reales en 8 HH, por lo que el CPI de PS-0000 mejora marginalmente.
- **Si se deja el RDT**, el efecto ya está incluido en los números actuales de PS-0000 (servicio de pruebas) y es mínimo.
- **Si se borra**, hay que recalcular el PR en la misma operación (la sección opcional ya lo hace con `select recalcular_pr_desde_rdt(...)`). La app, al borrar un RDT por pantalla, hace lo mismo y además deja una foto `BORRADO` en el historial; el SQL no la crea (se borra su historial y no queda rastro).
- No se midió el monto exacto en dólares: no se leyó el PR por GET. Se puede ver antes y después en el Dashboard de PS-0000.
- Recomendación: dejarlo mientras no estorbe, o borrarlo con la sección opcional en una ejecución separada y revisar después el Dashboard de PS-0000.

## Lo que queda fuera de la base (Storage)

El SQL no borra archivos del almacenamiento de Supabase (bucket `documentos-proyecto`).

1. Carpeta `e15799ae-d964-4db7-b33f-39dc9c1a3860/` (PS-0005): contiene el archivo subido al documento «PRUEBA T7 plano de campo», `PRUEBA-T7-plano.txt`, con nombre `…-PRUEBA-T7-plano.txt`. Cómo quitarlo: Supabase → Storage → `documentos-proyecto` → abrir la carpeta `e15799ae-d964-4db7-b33f-39dc9c1a3860` → seleccionar todo → Delete. La carpeta es solo de PS-0005, no hay nada real dentro. Hacerlo después de aplicar el SQL (el SQL borra el registro del archivo; ya no se podría ver el nombre desde la app).
2. Adjuntos de ítems de RQ: las rutas serían `0a20df2f-c5e9-4296-9c08-f89af499182d/rq/<id del RQ>/…`; los ítems de los 3 RQ no tienen adjuntos, así que no debería existir nada. Conviene mirar de todos modos la carpeta `0a20df2f…/rq/` en Storage y borrar las subcarpetas de los 3 ids si hubiera algo.
3. El archivo local `PRUEBA-T7-plano.txt` en la carpeta `.playwright-mcp/` del repositorio es de las pruebas (ignorado por el repositorio o a limpiar a mano); no es de producción.

## Otros datos de prueba que NO se tocan (para decidir aparte)

- Cuenta PRUEBA Logística 1: celular de prueba `999000111` y un cambio de correo pendiente de confirmar (`+logistica1b`, vive en Supabase Auth). Opcional 2 del SQL (comentada) devuelve el celular a vacío; el correo pendiente no se toca desde SQL.
- Cuenta PRUEBA Logística 2: clave cambiada en T7C (la nueva solo está en la memoria local de cuentas).
- Roles temporales: ya revertidos según T7B.

## Límites de este respaldo y del conteo

- El respaldo JSON tiene los datos de los 3 RQ (cabecera, ítems, comentarios), los 2 RDT (con el nombre y DNI de la persona del personal reemplazados por `[REDACTADO]` porque es un trabajador real y el repositorio es público), la ficha y el checklist de PS-0005 y los 28 avisos visibles (36 filas) con su id. No tiene los avisos de otras personas (el administrador no los ve); la vista previa comentada del SQL los lista.
- No se pudo leer por GET: `proyecto_miembros`, `proyecto_documentos` ni las rutas exactas de Storage (la app no las expone); los conteos de esas tablas salen del SQL (`antes`).
- Para ver los avisos de otras personas con exactitud habría que iniciar sesión con sus cuentas; no se hizo porque el encargo fue usar solo la cuenta del administrador.

## Orden recomendado para Victor

1. Revisar este archivo y el SQL. Opcional: ejecutar sola la consulta comentada del paso 1 y exportar a CSV.
2. Pegar y ejecutar `limpieza-datos-prueba.sql` entero. Si alguna guarda aborta, no queda nada a medias.
3. Leer la tabla de «antes / después» del final (todos los «después» en 0; el control de RDT de PS-0000 en 35).
4. Quitar la carpeta de Storage de PS-0005.
5. Decidir las secciones opcionales (RDT validado, celular).
6. Verificar con un GET que el próximo N° OT es PS-0005 y que PS-0000 sigue con sus RDT.
