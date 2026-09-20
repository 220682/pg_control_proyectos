# Visual companion — mockups HTML

Artefactos de interfaz para alinear **py_control_proyectos_web** con el diseño acordado.

## Convención de interfaz → [design.md](design.md)

**Antes de crear o modificar cualquier pantalla**, leer [`design.md`](design.md) completo — es el sistema de diseño obligatorio (layout, tokens, componentes, columnas, accesibilidad). Este `README.md` ya no contiene la convención; solo el índice de mockups y la nomenclatura oficial.

## Cómo verlos

1. Abre **`index.html`** en el navegador (doble clic).
2. O abre cualquier `.html` de esta carpeta directamente.

Ruta en tu PC:

```
C:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\visual-companion\
```

## Nomenclatura oficial (2026-08-19)

| Uso | Texto |
|-----|-------|
| Módulo / pantalla | **Requerimiento de servicios** |
| Botón, chip, acción | **Crear requerimiento de servicios** |
| Modal consulta | **Ver partidas** |

## Archivos

| Archivo | Contenido |
|---------|-----------|
| `index.html` | Índice de todos los mockups |
| `requerimiento-de-servicios-crear.html` | Formulario completo + modal partidas |
| `requerimiento-de-servicios-listado.html` | Bandeja Logística |
| `requerimiento-de-servicios-partidas.html` | Modal partidas (solo referencia) |
| `entorno-trabajo-herramientas.html` | Entorno con chip Crear RQ |

## Campos del formulario (spec)

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

---

Generados por Cursor el 2026-08-19. Si cambias el diseño, edita estos HTML o pide regenerarlos en el chat.
