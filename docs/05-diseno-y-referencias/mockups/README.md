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
| `importar-dp-niveles.html` | Importar DP: confirmación de niveles (4 y 5 niveles, aviso de recarga). Con los tres paneles, aprobada por Victor (2026-09-30); alineación de tablas corregida |
| `cronograma-niveles.html` | Cronograma: confirmación de niveles con roles propios. Con los tres paneles, aprobada por Victor (2026-09-30); alineación de tablas corregida |
| `paquetes-declarar.html` | Paquetes de trabajo, paso Declarar (cronograma con Metrado + DP solo partidas). Con los tres paneles, aprobada por Victor (2026-09-30); alineación de tablas corregida (abre con ambos paneles ocultos) |
| `paquetes-agrupar.html` | Paquetes de trabajo, paso Agrupar (crear paquete, marca, orden, plegado). Con los tres paneles, aprobada por Victor (2026-09-30); alineación de tablas corregida |
| `plan-maestro-lienzo.html` | Plan Maestro: lienzo con columnas fijas (Disciplina y BAC opcionales), días por semana, seis columnas por semana, filas Prog./Real, anexo de 4 semanas, asistente flotante. Aprobado por Victor (F0-B); ajustado en F0-R. F0-S: color del Físico acum. real (0 % blanco, en curso amarillo, 100 % verde; ejemplo 4) e icono de los paneles en la esquina de su encabezado | **Reemplazada por `plan-maestro-tres-paneles.html`** (F0-V la dejó como página mínima con aviso y redirección).
| `plan-maestro-tres-paneles.html` | Plan Maestro con los tres paneles como se ven en la app (panel izquierdo y derecho con los rótulos reales del registro de accesos), icono de ocultar de cada panel en cuatro estados, asistente flotante, estados con datos, vacío, cargando y error, y cajones en móvil (390 px). Nueva (F0-T); aprobada por Victor (2026-09-30) tras F0-V (color del avance real corregido, barras de desplazamiento azuladas). El lienzo anterior queda como página mínima con aviso y redirección |
| `paneles-ocultables.html` | Ocultar y mostrar los paneles laterales: un icono por panel en la esquina superior interior de su encabezado (escritorio) y cajón móvil; asistente flotante. Rehecha en F0-R, icono reubicado en F0-S; pendiente de revisión de Victor |
| `crear-rdt-selector-paquetes.html` | Crear RDT: la pantalla existente completa (secciones 1.0, 2.0, 3.0, equipos, materiales, plantilla) con el selector de actividad del Plan Maestro. Rehecha en F0-R; F0-S: avance de partidas y paquetes con color (0 % blanco, en curso amarillo, 100 % verde); aprobada por Victor (2026-09-30). Con los tres paneles (F0-U2) |

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


Marco compartido de los tres paneles (F0-U1): `marco-tres-paneles.css` y `marco-tres-paneles.js` (copia fiel del marco de `plan-maestro-tres-paneles.html`; cada maqueta indica su acceso activo y si abre con los paneles ocultos). Abren igual con doble clic (file://).