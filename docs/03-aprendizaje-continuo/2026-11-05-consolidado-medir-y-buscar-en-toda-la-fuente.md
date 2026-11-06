# 2026-11-05 — Medir en todas las fuentes y buscar un dato sin suponer dónde está

## Origen

Plan [Consolidado como fuente única](../02-trabajo-activo/01-planes/2026-11-05-consolidado-fuente-unica.md): cifras distintas entre pantallas, datos de los 4 servicios y limpieza de los equipos del RDT.

## Método que funcionó

- **Un candado automático protege mejor que una regla escrita.** Una prueba que falla si alguien salta la frontera del Consolidado detiene el error antes de publicarlo.
- **Medir la misma cifra en todas sus fuentes antes de arreglar** evitó adivinar la causa.
- **Revisar los códigos contra el Excel celda por celda** mostró que `4.02` era un número y `04.01` un texto.
- **Barrer todas las tablas del servicio antes de corregir un código**, en vez de confiar en la lista conocida, confirmó que no quedaba ninguna referencia suelta.

## Trampas encontradas

- **Leer el dato de la fuente antes de reportarlo.** Un reporte dio 1,248 h del conductor en cada lado, y en gastos generales eran 208 h.
- **No afirmar que algo no existe después de buscar en un solo lugar.** Se dijo que PS-108 no tenía retroexcavadora tras revisar solo los recursos de tipo equipo; estaba cargada como material. Antes de decir «no hay», buscar por nombre en todos los tipos y en el Excel original.
- **Probar una regla nueva con los datos reales.** El aviso de códigos dio falsa alarma con `2.10.1` en PS-108; las pruebas con datos inventados no la mostraron.
