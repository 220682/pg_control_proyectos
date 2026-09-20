---
version: 1.2.4
proyecto: Control de Proyectos Web
stack: Next.js 16 + React 19 + Tailwind CSS v4
actualizado: 2026-09-20
estado: activo
---

# DESIGN.md — Sistema de diseño, UI/UX y reglas de datos

**Propósito:** esta es la fuente de verdad visual y de comportamiento para toda interfaz de **Control de Proyectos Web**. Su objetivo es que cada pantalla nueva conserve los mismos espacios, tipografías, anchos, componentes, patrones de datos y criterios de accesibilidad.

**Regla principal:** antes de diseñar, generar o modificar una interfaz, el agente debe leer este archivo completo y reutilizar los componentes y tokens existentes. No debe inventar estilos, anchos, colores, componentes ni opciones de datos.

**Dónde vive esto y por qué:** este archivo está en `pg_control_proyectos` (repositorio documental), pero describe código real de `py_control_proyectos_web` (la app hermana). Eso es intencional — es la misma excepción que ya reconoce [AGENTS.md](../../AGENTS.md) en "Reglas de interfaz": este repo no ejecuta el runtime, pero sí documenta directrices de interfaz verificadas contra la app real. Cada componente, clase y archivo nombrado aquí fue confirmado leyendo el código de `py_control_proyectos_web` el 2026-09-20 — no son inventados. Si en el futuro un nombre de archivo o componente ya no existe, hay que corregir este documento, no asumir que sigue vigente.

Este archivo **anula** al antiguo `README.md` de esta misma carpeta en materia de convención de interfaz. `README.md` conserva el índice de mockups y la nomenclatura oficial; la convención de UI vive aquí.

---

## 0. Protocolo obligatorio para el agente

Antes de tocar código de interfaz:

1. Leer este archivo completo.
2. Leer los componentes existentes en `src/components/ui/` que se usarán.
3. Identificar si la tarea afecta una pantalla de listado, formulario, detalle, tablero, modal o navegación.
4. Para una tabla/listado, responder primero el **Análisis de pre-vuelo** de la sección 11. No escribir código hasta completar dicho análisis.
5. Reutilizar componentes, clases compartidas y tokens existentes.
6. Si la regla no cubre el caso, presentar opciones breves y preguntar al usuario; no asumir una decisión visual o de datos.
7. Al terminar, verificar visualmente escritorio y móvil, y registrar una propuesta para actualizar este archivo si apareció una regla nueva reutilizable.

### Regla de evolución

Cuando el usuario corrija una decisión visual repetible —espaciado, tamaño, jerarquía, ancho, componente, comportamiento de tabla o formato— el agente debe proponer:

1. Ajustar la pantalla actual.
2. Actualizar la regla correspondiente en este `DESIGN.md`.
3. Informar qué pantallas futuras se beneficiarán.

No modificar una regla global sin confirmación del usuario, salvo que sea una corrección objetiva de una referencia rota o de una contradicción interna.

---

## 1. Stack tecnológico y límites

- Next.js 16 con App Router.
- React 19.
- Tailwind CSS v4, configurado mediante `@theme inline` en `globals.css` (no hay `tailwind.config.js`).
- Sin biblioteca externa de componentes: no usar MUI, shadcn/ui, Chakra, Ant Design ni equivalentes.
- Iconos: `lucide-react`.
- Componentes propios en `src/components/ui/`.
- Usar clases Tailwind nativas y tokens CSS existentes. Ejemplos: `w-20`, `mb-2`, `px-1.5`, `bg-bg-elevated`.
- No introducir estilos inline, CSS modules, valores arbitrarios o nuevas dependencias de UI sin aprobación explícita.

---

## 2. Fuente de verdad visual y de datos

Antes de inventar o duplicar algo, el agente debe localizar la fuente existente en el repositorio.

| Tipo de información | Fuente de verdad | Regla |
|---|---|---|
| Colores, fuentes y tokens | `globals.css` / `@theme inline` | Usar variables y tokens existentes; no hardcodear variantes nuevas sin documentarlas (ver 4.1.1 para colores semánticos no tokenizados) |
| Componentes UI | `src/components/ui/` | Reutilizar antes de crear un componente nuevo |
| Tabla y sus clases | `src/components/ui/Table.tsx` | Usar las clases compartidas; no crear un `<Table>` ficticio |
| Estados y etiquetas | Mapas/constantes existentes del dominio | No inventar estados ni etiquetas |
| Catálogos relacionales | Fuente de datos, API, DB o módulo de catálogo existente | Cargar opciones dinámicamente; no hardcodear opciones |
| Tipos de datos | Tipos junto al dominio (ej. `src/lib/rdts/`) | Leer tipo/cardinalidad antes de elegir componente |
| Diseño ya aprobado | Pantallas existentes aprobadas / `visual-companion/` | Copiar patrón, no reinterpretarlo |

Si la ruta exacta no existe o no está clara, el agente debe buscarla en el proyecto y reportar qué archivo tomará como fuente. Si no hay fuente, debe preguntar antes de crear una.

---

## 3. Layout global

### WorkspaceShell

La aplicación usa esta estructura fija (`src/components/ui/WorkspaceShell.tsx`):

```tsx
<aside className="w-60">...</aside>   {/* nav izquierda, fija */}
<main className="flex-1 min-w-0">...</main>  {/* panel central, flexible */}
<aside className="w-64">...</aside>   {/* herramientas/grupos, fija */}
```

### Contenido de página

El contenido de cada página vive dentro de:

```tsx
<div className="flex-1 overflow-auto px-2 py-2 lg:px-4 lg:py-3">
  {children}
</div>
```

### Reglas estrictas

- El panel central ya es flexible mediante `flex-1 min-w-0`.
- **Prohibido** usar `max-w-*` en el contenedor principal de una página: genera espacio muerto antes del panel derecho (ver caso real corregido en Status de RDTs, 2026-09-20).
- No crear otro layout global, sidebar ni wrapper de ancho máximo sin aprobación.
- Mantener densidad de workspace: la interfaz es una herramienta de trabajo, no una landing page.
- Si una pantalla necesita lectura extensa, resolver el ancho dentro de su contenido y sin romper el panel central.

---

## 4. Tokens y densidad visual

### 4.1. Colores existentes (tokens)

Definidos en `globals.css`, bloque `@theme inline`:

| Token | Valor actual | Uso |
|---|---|---|
| `--color-bg-base` | `#05070d` | Fondo principal |
| `--color-bg-elevated` | `#0b0f19` | Superficies elevadas, cabeceras sticky |
| `--color-accent` | `#22d3ee` | Acción/acento principal |
| `--color-accent-secondary` | `#4f7df3` | Acento secundario |
| `--color-text-primary` | `#f8fafc` | Texto principal |
| `--color-text-secondary` | `#94a3b8` | Texto secundario |
| `--color-estado-planeacion` | `#4f7df3` | Estado de **proyecto/servicio**: En Planeación |
| `--color-estado-ejecucion` | `#22d3ee` | Estado de **proyecto/servicio**: Ejecución |
| `--color-estado-cerrado` | `#4b7c62` | Estado de **proyecto/servicio**: Cerrado |

No agregar colores nuevos porque "se ven mejor". Si falta un color semántico, proponer nombre, finalidad, contraste y dónde se definirá antes de usarlo.

#### 4.1.1. Colores semánticos de validación (no tokenizados — usar tal cual)

Los tokens `--color-estado-*` son solo para el **estado de proyecto/servicio** (consumidos por `<BadgeEstado>`). Para flujos de **validación/acción** (ej. RDT: registrado → revisado → validado / rechazado) la app usa paleta Tailwind directa, sin token propio. Esta es la convención real ya implementada en `TablaStatusRdts.tsx` — reutilizarla, no inventar otra:

| Significado | Clase | Dónde se usa |
|---|---|---|
| Éxito / validado | `text-emerald-400` | Texto "Validado", iconos de confirmación |
| Error / rechazo / acción destructiva | `text-rose-400` | Botón/ícono "Rechazar", botón "Corregir", texto de inconsistencia bloqueante |
| Advertencia informativa (no bloquea) | `text-amber-400` | Icono de jornada inconsistente (informativo, no impide validar/rechazar) |

Si se necesita un cuarto significado semántico, proponerlo aquí antes de usar un color nuevo.

### 4.2. Tipografía

- Usar la familia tipográfica definida en el proyecto; no agregar fuentes externas sin aprobación.
- Texto de tabla: `text-[11px]`; metadatos muy compactos: `text-[10px]`.
- Mantener jerarquía mediante tamaño, peso, color y espacio; no usar tamaños arbitrarios para cada pantalla.
- No reducir texto crítico por debajo de `text-[10px]`.
- El título de página debe seguir el componente `CabeceraPagina.tsx` o el patrón existente aprobado.

### 4.3. Espaciado

La densidad es deliberadamente compacta.

| Contexto | Regla |
|---|---|
| Celdas de tabla | `px-1.5 py-1` |
| Header de página (`CabeceraPagina.tsx`) | `mb-2` |
| Migas / chip de volver | `mb-1.5` |
| Encabezado de tabla | `py-1` a `py-1.5` |
| Contenido de página | `px-2 py-2 lg:px-4 lg:py-3` |
| Entre bloques de una pantalla de listado (`CabeceraPagina` → fila de filtros/controles → tabla) | Sin `gap` en el contenedor flex — `CabeceraPagina` ya trae su propio `mb-2`; el siguiente bloque (fila de controles, mensaje de error) pone su propio `mb-2` antes de la tabla. **No usar `gap-*` en el contenedor Y `mb-2` en `CabeceraPagina` al mismo tiempo** — se suman (8px + 8px) y el ajuste queda imperceptible, como pasó aquí el 2026-09-20. Una sola medida (`mb-2` por bloque), nunca las dos |

- No añadir padding o margin "para que respire" sin comparar con una pantalla aprobada.
- No dejar espacios muertos verticales entre tabla, filtros, cabecera y contenido.
- Si el usuario pide aumentar o reducir espacios de forma repetible, primero proponer una regla nueva en este documento.

### 4.4. Bordes, radios y elevación

- Usar los valores ya implementados por `Card.tsx`, `Button.tsx`, `Input.tsx` y otros componentes existentes.
- No crear un radio, sombra o borde distinto para una pantalla aislada.
- Toda nueva variante visual debe justificarse como componente reusable y requerir aprobación.

---

## 5. Componentes existentes: reutilizar antes de crear

| Necesidad | Componente o patrón obligatorio |
|---|---|
| Tabla | `<table>` nativo + clases de `Table.tsx` |
| Estado de proyecto/servicio (categoría única) | `<BadgeEstado estado="..." />` — pill con color, ver 4.1 |
| Estado de validación / flujo con acciones (ej. RDT) | Texto + icono `lucide-react` con color semántico de 4.1.1 — **no** es un `<BadgeEstado>`, es un patrón distinto ya aprobado (se descartó el pill de colores en RDT a pedido explícito de Victor) |
| Botón | `Button.tsx` |
| Campo de texto | `Input.tsx` |
| Filtro select | `SelectFiltro.tsx` o `<select>` nativo según caso |
| Tarjeta | `Card.tsx` |
| Breadcrumb | `Breadcrumb.tsx` |
| Cabecera de página | `CabeceraPagina.tsx` |
| Icono | `lucide-react` |

**Importante:** `BadgeEstado` no es de uso universal para "cualquier estado". Es el componente para estados de **entidad/categoría cerrada de proyecto o servicio** (`EN_PLANEACION` / `EJECUCION` / `CERRADO`). Un estado de **validación con múltiples acciones asociadas** (validar, rechazar, revisar, corregir) usa el patrón de icono + color de texto, porque necesita convivir con botones de acción en la misma celda sin competir visualmente con un pill. Antes de renderizar un "estado" nuevo, decidir a cuál de los dos casos pertenece.

### Tablas

`Table.tsx` no es un componente `<Table>`. Es una fuente de clases compartidas. Usar directamente en una tabla HTML nativa:

- `tablaWrapClase`
- `tablaClase`
- `theadFilaClase`
- `thClase`
- `tdClase`
- `filaClase`

### Selects

No hay `<Select>` genérico. Usar `<select>` HTML nativo y mapas de etiqueta existentes, siguiendo el patrón de `SelectFiltro.tsx`.

### Crear componentes nuevos

Solo proponer un componente nuevo si:

1. No existe uno reutilizable.
2. El patrón aparecerá en al menos dos lugares o tiene responsabilidad propia clara.
3. Se documenta su API, estados y lugar en `src/components/ui/`.
4. El usuario aprueba la creación si cambia el sistema de diseño.

---

## 6. Datos, columnas y algoritmo de anchos

Antes de renderizar una columna, leer su tipo, origen y cardinalidad. Aplicar estas reglas sin preguntar, excepto donde se indica expresamente.

| Tipo de dato | Renderizado | Ancho y alineación | Regla |
|---|---|---|---|
| Enum/categoría cerrada, 2 a 4 valores | Texto compacto, select si es editable | `w-16` o `w-20`, centrado | No ocupar más espacio |
| Estado de proyecto/servicio | `<BadgeEstado>` | `w-24` a `w-32`, centrado | Usar mapa de color/etiqueta existente |
| Estado de validación con acciones | Texto/icono + botones (ver 5) | Una sola fila flex, botones `h-6 w-6` | No usar pills; agrupar validar/rechazar/revisar/corregir en una columna única (precedente: columna "Validación" de Status RDTs) |
| Catálogo relacional de DB/API | `<select>` nativo si es editable | Según etiqueta, usualmente medio | Cargar opciones dinámicamente |
| Texto libre **sin precedente** en este documento | No decidir solo | Preguntar al usuario | Prohibido asumir ancho (ver excepción 6.1) |
| Texto libre largo, columna principal de identificación | Texto / enlace / celda principal | `flex-1` o `w-auto` | No truncar por defecto |
| Numérico/cantidad | Texto numérico | `w-12`, alineado a la derecha | Formato consistente |
| Fecha | Texto de fecha | `w-24` | Formato consistente |
| Identificador corto | Texto monoespaciado si aplica | `w-12` a `w-20` | No confundir con nombre principal |
| Acciones | Botones o menú existente | ancho mínimo necesario | No desplazar la información clave |

### 6.1. Precedentes ya resueltos (no volver a preguntar)

Estos campos de texto libre ya tuvieron su decisión de ancho aprobada por Victor. Un agente nuevo debe copiarlos, no volver a preguntar por ellos:

| Campo | Pantalla | Decisión | Motivo |
|---|---|---|---|
| Servicio (nombre) | Status de RDTs y listados equivalentes | Sin truncar, columna principal (`flex-1`/sin `max-w`) | Es el dato principal de identificación; truncarlo obliga a adivinar. Corregido 2026-09-20 tras revertir un truncado que sí molestó. |
| Cargado por | Status de RDTs | `max-w-[130px] overflow-hidden text-ellipsis whitespace-nowrap` + `title` con el nombre completo | Es secundario y compite por espacio con columnas más importantes; el `title` conserva el dato completo al pasar el mouse. |

Si aparece un campo de texto libre **nuevo**, sin fila en esta tabla, sí se debe preguntar (regla general de la sección 6). Al resolverlo, agregar la fila aquí.

### Caso obligatorio: texto libre sin catálogo y sin precedente

La IA no puede calcular automáticamente el ancho correcto de un campo de texto libre sin catálogo definido ni precedente en 6.1. Debe preguntar exactamente o de forma equivalente:

> "El campo [Nombre] es texto libre y no tiene un catálogo definido. ¿Qué ancho máximo o comportamiento deseas? Por ejemplo: `w-40`, `w-full`, columna flexible, o límite de caracteres."

No asumir un ancho. No ocultar el problema con truncamiento automático.

### Texto largo y truncamiento

- La columna principal de identificación nunca se trunca por defecto.
- Si hay competencia real por espacio, proponer al usuario una de estas alternativas: columna flexible, mayor ancho mínimo, detalle/modal, tooltip con `title`, o truncamiento explícitamente aprobado.
- Para una columna secundaria aprobada para truncamiento: `max-w-* overflow-hidden text-ellipsis whitespace-nowrap` + atributo `title`.

---

## 7. Formato de datos

La fuente de verdad de formato son los helpers existentes del proyecto (ej. `src/lib/rdts/`). Antes de crear un formatter nuevo, buscar uno existente.

Si todavía no existe una convención implementada, proponer y documentar la decisión antes de aplicarla de manera masiva:

| Dato | Tabla/listado | Detalle/reporte |
|---|---|---|
| Fecha | Formato compacto único definido por el proyecto | Puede incluir hora si aporta valor |
| Número | Alineado a la derecha; precisión solo necesaria | Separadores/precisión según unidad |
| Moneda | Símbolo, separadores y decimales uniformes | Misma convención que tabla |
| Porcentaje | Valor y símbolo %; precisión definida | Misma convención que tabla |
| Estado | Etiqueta humana mediante mapa | Mismo mapa y color semántico |

No usar formatos diferentes en dos pantallas para el mismo dato. No usar el locale del navegador de manera implícita si el proyecto define formato propio.

---

## 8. Scroll y tablas extensas

**No usar `max-h-[Nvh]` para la caja de una tabla de página completa.** Se probó con `70vh` y luego `80vh` en Status de RDTs y las dos veces terminó igual: en una ventana más chica o con un encabezado más alto de lo estimado, la caja queda más alta que la ventana real y el borde inferior (con la barra de scroll horizontal) se sale de la vista — exactamente el problema que este patrón debía evitar. Un porcentaje fijo de la ventana no puede saber cuánto mide el encabezado de cada pantalla.

**Patrón correcto: `flex-1 min-h-0`, no un alto adivinado.** La página se estructura como columna flex con el alto real disponible del panel central, y la caja de la tabla ocupa lo que sobra — así nunca puede quedar más alta que la ventana, sea cual sea su tamaño o el alto del encabezado:

```tsx
// page.tsx de la pantalla
<div className="flex h-full min-w-0 flex-col p-1">

// componente de listado
<div className="flex h-full flex-col gap-3">
  <CabeceraPagina ... />
  {/* fila de controles (filtros, Personalizar campos, etc.) sin flex-1: tamaño natural */}
  <div className={`${tablaWrapClase} flex-1 min-h-0 overflow-y-auto`}>
    <table className={tablaClase}>...</table>
  </div>
</div>
```

El encabezado de la tabla debe permanecer visible:

```tsx
sticky top-0 z-20 bg-bg-elevated
```

**Si la tabla tiene dos filas de encabezado (etiquetas + filtros, como `TablaStatusRdts.tsx`), las DOS deben ser sticky, apiladas.** Poner `sticky` solo en la primera fila hace que la fila de filtros desaparezca al bajar el scroll — no queda pegada, se va con el resto de filas.

**El `sticky` va en cada `<th>`, nunca en el `<tr>`.** Se probó primero con `sticky` + `h-6`/`top-6` en el `<tr>` completo y el resultado fue peor que el bug original: las filas se superponían visualmente al hacer scroll (texto de una fila tapando a otra), porque los navegadores no manejan bien `position: sticky` combinado con un alto forzado en dos `<tr>` apiladas. El patrón correcto — y el que ya usa `TablaConsolidadoRdts.tsx` para sus columnas pegadas al desplazar horizontalmente — es aplicar `sticky` a cada celda (`<th>`/`<td>`), no a la fila:

```tsx
<th className="... sticky top-0 z-20 h-6 bg-bg-elevated">   {/* cada th de la fila 1: etiquetas, alto fijo h-6 */}
<th className="... sticky top-6 z-20 bg-bg-elevated">       {/* cada th de la fila 2: filtros, top = alto de la fila 1 */}
```

El alto fijo (`h-6` = 24px) en los `<th>` de la fila 1 es necesario para que el `top-6` de la fila 2 sea exacto — sin un alto fijo, el offset se calcula a ciegas y se puede desalinear. Regla general: **sticky de celda, no de fila**, siempre que haya más de una fila de encabezado.

Patrón ya corregido en `TablaStatusRdts.tsx` (2026-09-20) — copiarlo igual en toda tabla nueva de muchas filas. **`TablaConsolidadoRdts.tsx` todavía usa el `max-h-[70vh]` viejo** y puede tener el mismo problema latente; no se tocó porque no se pidió — señalarlo si aparece la misma queja ahí.

Reglas:

- Resolver scroll vertical y horizontal en el wrapper correcto.
- El usuario no debe tener que recorrer toda la tabla para encontrar contexto de columna o controles importantes, ni bajar la página entera para llegar a la barra de scroll horizontal.
- Mantener cabeceras sticky cuando el contenido pueda superar la altura visible.
- Verificar que el panel central no se desborde por una tabla ancha.
- No reemplazar tabla nativa por divs sin necesidad técnica y sin aprobación.
- No usar `max-h-[Nvh]` en la caja de una tabla de página completa — usar `flex-1 min-h-0` dentro de una columna flex de alto real (`h-full`). `max-h` en vh sí es aceptable dentro de modales centrados (`PanelVerRq.tsx`, `ModalPartidasServicio.tsx`, `ModalHistorialRdt.tsx`), donde no compite con un encabezado de página.

---

## 9. Formularios, feedback y estados

### Formularios

- Todo input debe tener label visible; el placeholder complementa, no reemplaza la etiqueta.
- Campos de catálogo usan `<select>` nativo con opciones reales.
- Mostrar estado de error próximo al campo y explicar cómo corregirlo.
- No usar solo color para comunicar un error; incluir texto o icono con significado.
- Marcar campos obligatorios siguiendo el patrón existente; no crear una convención distinta.

### Botones y acciones

- Reutilizar `Button.tsx`.
- El texto debe usar un verbo claro: "Guardar", "Crear", "Actualizar", "Cancelar", "Eliminar".
- Las acciones destructivas requieren confirmación y estilo semántico existente (precedente: confirmación de jornada inconsistente antes de guardar un RDT, y motivo obligatorio al rechazar).
- No ocultar acciones críticas solo bajo un icono si no existe señalización accesible (precedente: todo botón de solo-icono en `TablaStatusRdts.tsx` lleva `title` + `aria-label`).

### Estados de pantalla

Toda pantalla que carga datos debe considerar, cuando corresponda:

1. Cargando.
2. Vacío sin resultados.
3. Error recuperable.
4. Datos cargados.
5. Acción guardada o fallida.

Reutilizar componentes/patrones existentes. Si no existen, proponer el patrón antes de duplicar mensajes improvisados. Los errores técnicos/de base de datos **nunca** se muestran crudos al usuario — se traducen a un mensaje claro en español y el error real se registra en servidor (`console.error`).

---

## 10. Accesibilidad mínima obligatoria

- Usar HTML semántico: `<button>`, `<label>`, `<table>`, `<thead>`, `<th>`, `<main>`, `<nav>` según corresponda.
- Los `<th>` deben tener `scope="col"` cuando sean encabezados de columna (`scope="colgroup"` si agrupan varias columnas, como en encabezados de dos filas).
- Botones con solo icono deben tener `aria-label` descriptivo y `title` como tooltip (ya aplicado en `TablaStatusRdts.tsx`).
- Todos los controles deben poder operarse con teclado.
- Mantener foco visible; no eliminar estilos `focus` sin un reemplazo accesible.
- Los estados no dependen solamente del color: incluir etiqueta, icono o texto.
- Verificar contraste de texto y acciones contra fondos oscuros antes de aprobar nuevos tokens.

> **Deuda técnica reconocida (2026-09-20):** ninguna tabla existente (`TablaStatusRdts.tsx`, `TablaConsolidadoRdts.tsx`, `TablaConsolidadoRq.tsx`, `TablaListadoRdts.tsx`, `TablaPersonal.tsx`, `TablaRecursos.tsx`, `ListadoRequerimientos.tsx`, `ModalPartidasServicio.tsx`, `ModalHistorialRdt.tsx`, `FormularioCrearRdt.tsx`, `FormularioPlanMaestro.tsx`, `FormularioCronograma.tsx`) tiene todavía `scope="col"` en sus `<th>`. La regla aplica de inmediato a toda tabla **nueva o modificada** a partir de hoy. El retrofit del resto de tablas existentes es un cambio mecánico pendiente, no incluido en este cierre — no ejecutarlo en lote sin que Victor lo pida, porque `FormularioPlanMaestro.tsx` tiene encabezados de dos filas con `colSpan` que necesitan `scope="colgroup"` en vez de `scope="col"` y conviene revisarlo con cuidado, no en bloque.

---

## 11. Checklist de pre-vuelo para listados y tablas

**Obligatorio:** antes de entregar código que cree o modifique un listado/tabla, el agente debe responder este análisis de forma breve y específica.

1. ¿Cuál es el origen, tipo y cardinalidad de cada columna? Enum, catálogo, texto libre, numérico, fecha, identificador, estado o acción.
2. ¿Qué columnas son editables y cuáles deben renderizarse como `<select>` por provenir de un catálogo?
3. ¿Existe algún texto libre sin catálogo definido? Si existe: ¿ya tiene precedente en 6.1? Si no, ¿ya se preguntó y respondió el ancho o comportamiento requerido?
4. ¿Cuál será la columna principal que no debe truncarse?
5. ¿Qué componentes y clases existentes se reutilizarán?
6. ¿Cómo se aplicarán los anchos, alineaciones y truncamientos permitidos de la sección 6?
7. ¿Cómo se resolverá scroll vertical, horizontal y encabezado sticky?
8. ¿Qué estados de carga, vacío y error requiere la pantalla?
9. ¿Qué requisito de accesibilidad aplica especialmente aquí (incluyendo `scope="col"` en tablas nuevas/modificadas)?
10. ¿Hay una pantalla aprobada similar que deba usarse como referencia?

Si falta una respuesta crítica, especialmente sobre un campo de texto libre sin precedente, el agente debe preguntar antes de escribir código. Si no presenta este análisis, el código será rechazado.

---

## 12. Anti-patrones y prohibiciones estrictas

- No usar `max-w-*` en el contenedor principal de página.
- No crear un layout paralelo a `WorkspaceShell.tsx` sin aprobación.
- No poner padding o margin excesivo en `<th>`; máximo `py-2`.
- No truncar la columna principal de identificación por defecto.
- No usar inputs de texto libre para datos provenientes de catálogo relacional.
- No hardcodear opciones, estados, etiquetas o colores que ya tienen fuente de verdad.
- No dejar tablas largas sin `max-h`, scroll apropiado y encabezado sticky.
- No asumir ancho para texto libre sin preguntar, salvo que ya exista precedente en 6.1.
- No introducir librerías de UI ni dependencias visuales sin aprobación.
- No inventar componentes si existe uno reutilizable.
- No forzar `<BadgeEstado>` sobre un estado de validación con acciones — usar el patrón de la sección 5.
- No aplicar correcciones visuales solo a una pantalla si representan una regla que debe quedar en este documento.
- No modificar `DESIGN.md` global sin confirmación cuando el cambio afecte pantallas existentes.

---

## 13. Control de calidad antes de entregar

Antes de declarar una interfaz terminada, el agente debe verificar:

- Se leyó este archivo y se reutilizaron componentes existentes.
- No se agregaron `max-w-*` al contenedor principal.
- No hay valores visuales inventados o duplicados sin razón.
- Columnas, selects y badges/estados respetan su tipo/origen (proyecto vs. validación, ver sección 5).
- La columna principal no se truncó sin aprobación.
- Tabla con scroll y header sticky, si corresponde.
- Labels, foco, teclado y semántica mínima están presentes (`scope="col"` si la tabla es nueva o fue modificada).
- Se revisó escritorio y móvil o se declaró qué falta revisar.
- Se identificó si alguna corrección merece actualizar `DESIGN.md`.
- Se corrió `tsc`, `eslint`, `vitest` y `build` — no se declara terminado sin esa evidencia.

---

## 14. Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.2.4 | 2026-09-20 | Sección 8 corregida otra vez: el fix de 1.2.3 (sticky en el `<tr>` completo) causaba filas superpuestas/tapadas al hacer scroll — peor que el bug original. Movido el `sticky` de la fila a cada celda (`<th>`), que es el patrón ya probado en `TablaConsolidadoRdts.tsx`. Regla añadida: sticky siempre va en la celda, nunca en la fila, con más de un encabezado apilado. |
| 1.2.3 | 2026-09-20 | Dos correcciones sobre lo publicado hace un momento, tras feedback de Victor en vivo: (1) sección 8 — encabezados de tabla de dos filas necesitan las DOS filas sticky y apiladas (`top-0`/`h-6` + `top-6`), no solo la primera, porque la fila de filtros desaparecía al bajar el scroll; (2) sección 4.3 — el `gap-2` del contenedor se sumaba al `mb-2` propio de `CabeceraPagina`, por eso la reducción de espacio no se notaba; ahora es una sola medida por bloque (`mb-2`), sin `gap` en el contenedor. |
| 1.2.2 | 2026-09-20 | Sección 4.3: agregada la medida fija (`gap-2`) entre `CabeceraPagina`, la fila de filtros/controles y la tabla en una pantalla de listado — antes era `gap-3`, un espacio más suelto que Victor marcó como excesivo en Status de RDTs. |
| 1.2.1 | 2026-09-20 | Sección 8 corregida: `max-h-[Nvh]` en la caja de una tabla de página completa quedó comprobado como frágil (probado con 70vh y 80vh en Status de RDTs, las dos veces empujó la barra de scroll horizontal fuera de la vista). Reemplazado por el patrón `flex-1 min-h-0` con altura real (`h-full`) — ya no depende de adivinar qué porcentaje de ventana ocupa el encabezado. |
| 1.2.0 | 2026-09-20 | Adaptación del borrador de Victor tras revisión contra el código real: aclarado dónde vive el documento y por qué (4.1.1), separados los dos patrones de "estado" (proyecto vs. validación, secciones 5 y 6), agregados los colores semánticos de validación no tokenizados, agregados precedentes ya resueltos de ancho de columna (6.1), y reconocida como deuda técnica pendiente la falta de `scope="col"` en tablas existentes (sección 10). Reemplaza y anula la sección de convención de `README.md` de esta carpeta. |
| 1.1.0 | 2026-09-20 | Consolidación del documento de convenciones: protocolo de agente, fuente de verdad, layout, tokens, algoritmo de columnas, formato de datos, estados, accesibilidad y QA. |
| 1.0.0 | 2026-09-20 | Reglas iniciales de UI/UX, layout, tablas, columnas y pre-vuelo. |
