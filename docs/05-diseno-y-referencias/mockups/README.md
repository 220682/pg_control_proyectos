# Mockups

Mockups HTML de referencia visual, migrados desde `docs/visual-companion/`. No es evidencia de pruebas de un plan — eso vive en `docs/02-trabajo-activo/03-evidencia/`.

## Cómo verlos

Abre `index.html` en el navegador, o cualquier `.html` de esta carpeta directamente.

## Archivos

| Archivo | Contenido |
|---------|-----------|
| `index.html` | Índice de todos los mockups |
| `requerimiento-de-servicios-crear.html` | Formulario completo + modal partidas |
| `requerimiento-de-servicios-listado.html` | Bandeja Logística |
| `requerimiento-de-servicios-partidas.html` | Modal partidas (solo referencia) |
| `entorno-trabajo-herramientas.html` | Entorno con chip Crear RQ |
| `crear-rdts.html` | Pantalla de creación de RDTs |
| `importar-dp-niveles.html` | Importar DP: confirmación de niveles (4 y 5 niveles, aviso de recarga). Propuesta F0-A, pendiente de aprobación |
| `cronograma-niveles.html` | Cronograma: confirmación de niveles con roles propios. Propuesta F0-A, pendiente de aprobación |
| `paquetes-declarar.html` | Paquetes de trabajo, paso Declarar (cronograma con Metrado + DP solo partidas). Propuesta F0-A, pendiente de aprobación |
| `paquetes-agrupar.html` | Paquetes de trabajo, paso Agrupar (crear paquete, marca, orden, plegado). Propuesta F0-A, pendiente de aprobación |
| `plan-maestro-lienzo.html` | Plan Maestro: lienzo con columnas fijas, días por semana, seis columnas por semana, filas Prog./Real, anexo de 4 semanas. Propuesta F0-B, pendiente de aprobación |
| `paneles-ocultables.html` | Ocultar y mostrar los paneles laterales (escritorio) y cajón móvil. Propuesta F0-B, pendiente de aprobación |
| `crear-rdt-selector-paquetes.html` | Crear RDT: selector de actividad desde el Plan Maestro (paquetes, partidas, por avance del paquete). Propuesta F0-B, pendiente de aprobación |

## Campos del formulario de Requerimiento de servicios (spec, 2026-08-19)

**Encabezado**
- N° OT (servicio seleccionado, solo lectura)
- Ver partidas (botón junto al N° OT)
- Servicio / nombre (texto de apoyo)
- Fecha de requerimiento *
- Fecha de entrega *
- Código (auto: `{N°OT}-RQ-{secuencia}`)
- Solicitante (usuario en sesión, auto)

**Ítems** (mínimo 1)
- N° (auto)
- Descripción *
- Unidad *
- Cantidad *
- Observaciones (opcional)

**No incluido en v1:** partida/WBS obligatoria en cada ítem.

**Ver partidas:** WBS, Partida, Unidad, Metrado — **sin costos**.

Si cambia el diseño, se editan estos HTML directamente o se pide regenerarlos en el chat.
