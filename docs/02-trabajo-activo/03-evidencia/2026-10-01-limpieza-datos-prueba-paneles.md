# Limpieza de datos de prueba - plan paneles-servicio-persistente

Autorizada por Victor (2026-10-01, "realiza la limpieza"). Solo datos creados por el plan; ningun dato real tocado.

## A. Servicio de prueba
- PS-0006 "PRUEBA-PL SVX servicio de prueba F6-R2" (uuid 5769ee50-f49c-4aab-9968-65ad56fe7c07, portafolio Servicios Marcobre).
- Eliminado con la accion "Eliminar proyecto" de la ficha (DELETE /api/proyectos/[id]) como administrador. Confirmacion de la app: estado EN_PLANEACION, cronograma 14 actividades / 8 vinculos, DP 9 partidas y 15 recursos, 11 documentos, 0 RDT, 0 requerimientos.
- Verificado: ya no existe (count 0); quedan PS-0004 y PS-0005; la grilla del portafolio no lista PRUEBA-PL. "Ver como" restaurado (DELETE /api/ver-como = 200).

## B. Registros de Recursos (12, todos activo=false)
Borrados por id exacto con script Node de un solo uso (service role, ya eliminado), tras SELECT previo y 0 referencias en rdt_tareo.personal_id, rdt_equipos_parte.equipo_id, rdt_actividades.cnc_causa_id, recursos_cargo_equivalencias y recursos_equipo_equivalencias.
- recursos_personal: 4b684958-9bf1-40ff-8a37-ab27b7e0fa80 (DNI 99999901), 14cf565a-7dfb-40ff-8824-abf8732d3bf0 (99999902), 21c74f04-72af-4f7b-9468-2b220793035f (99999903)
- recursos_cargos: 3f33340d-dddb-4b83-8609-27b680580867, 05f3588d-dafa-47b7-a02d-65f5b21df4b5, a64c1983-5005-4c39-84f6-ab4f5c7e60e6
- recursos_equipos: 4595f1f6-f744-4cbb-a579-cb285113afce, ee137571-1645-410e-a154-a36a7db5cc55, 6e19a25e-eb9e-4658-b9d3-8fa9465eab1b
- catalogo_cnc: 68287d9a-803e-43c4-a6c5-d11e7e32a07f, 8531979e-4545-4975-819d-9f2c60672506, 508b0a99-a19c-40d1-a6e2-a82488f7307a
- Verificado tras el borrado: 0 filas PRUEBA-PL en las 4 tablas.

Sin commits ni cambios de codigo. Servidor dev en 3111 detenido.
